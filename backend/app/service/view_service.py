import enum
import math
import os
import uuid
from dataclasses import dataclass
from pathlib import Path

import ujson
from shapely.geometry import Point

from repository.db_repository import DbRepository
from schemas.atm import ATM
from schemas.geo import Coordinate, Metro
from schemas.office import Office
from schemas.search import GetTopTellers
from supplier.ort_supplier import ORTSupplier, Profiles

PARENT = Path(os.path.realpath(__file__)).parent


class TellerNotFound(Exception):
    ...


class TellerType(str, enum.Enum):
    OFFICE = "OFFICE"
    ATM = "ATM"


@dataclass
class ViewService:
    db_repository: DbRepository
    ort_supplier: ORTSupplier

    def __post_init__(self) -> None:
        self._metro_max_distance = 3000
        self._metro: list[tuple[Point, str, str]] = []

        with open(PARENT / "metro.json") as f:
            metro_dict = ujson.load(f)

        for line in metro_dict["lines"]:
            for station in line["stations"]:
                # TODO move to RTree
                self._metro.append(
                    (
                        Point(station["lat"], station["lng"]),
                        line["name"],
                        station["name"],
                    )
                )

    async def get_atms(self) -> list[ATM]:
        return await self.db_repository.get_atms()

    async def get_offices(self) -> list[Office]:
        return await self.db_repository.get_offices()

    async def get_route_by_id(
        self,
        start: Coordinate,
        teller_type: TellerType,
        teller_id: uuid.UUID,
        profile: Profiles,
    ) -> str:
        if teller_type == TellerType.OFFICE:
            office = await self.db_repository.get_office(teller_id)
            if office is None:
                raise TellerNotFound()
            end = office.coordinate

        else:
            atm = await self.db_repository.get_atm(teller_id)
            if atm is None:
                raise TellerNotFound()
            end = atm.coordinate

        return await self.get_route(start=start, end=end, profile=profile)

    async def get_route(
        self, start: Coordinate, end: Coordinate, profile: Profiles
    ) -> str:
        return await self.ort_supplier.get_route(start, end, profile)

    def _find_metro(self, point: Coordinate) -> Metro | None:
        begin_point = Point(point.lat, point.lng)
        for metro_point, line, name in self._metro:
            distance = begin_point.distance(metro_point) * 1000 * 100
            if distance <= self._metro_max_distance:
                return Metro(distance=distance, name=name, line=line)

        return None

    def _distance(self, start: Coordinate, end: Coordinate) -> float:
        start_point = Point(start.lat, start.lng)
        end_point = Point(end.lat, end.lng)
        return start_point.distance(end_point) * 1000 * 100

    def _duration_walk(self, distance: float) -> float:
        return math.ceil(distance / 1000 / 4 * 60)

    def _duration_car(self, distance: float) -> float:
        duration = distance / 1000 / 35 * 60
        if duration <= 2:
            return 2
        return math.ceil(duration)

    async def get_top_teller_filtered(  # noqa: CCR001
        self, top_tellers_request: GetTopTellers
    ) -> tuple[list[ATM], list[Office]]:
        atms = await self.db_repository.search_atms(
            lat=top_tellers_request.lat,
            lng=top_tellers_request.lng,
            limit=top_tellers_request.limit,
            features=top_tellers_request.atm_feature,
        )
        for atm in atms:
            atm.distance = self._distance(
                Coordinate(lat=top_tellers_request.lat, lng=top_tellers_request.lng),
                atm.coordinate,
            )
            atm.duration_walk = self._duration_walk(atm.distance)
            atm.duration_car = self._duration_car(atm.distance)
            atm.closest_metro = self._find_metro(
                Coordinate(lat=top_tellers_request.lat, lng=top_tellers_request.lng)
            )

        offices = await self.db_repository.search_offices(
            lat=top_tellers_request.lat,
            lng=top_tellers_request.lng,
            limit=top_tellers_request.limit,
            features=top_tellers_request.office_feature,
        )
        for office in offices:
            office.distance = self._distance(
                Coordinate(lat=top_tellers_request.lat, lng=top_tellers_request.lng),
                office.coordinate,
            )
            office.duration_walk = self._duration_walk(office.distance)
            office.duration_car = self._duration_car(office.distance)
            office.closest_metro = self._find_metro(
                Coordinate(lat=top_tellers_request.lat, lng=top_tellers_request.lng)
            )

        if top_tellers_request.legal_entity_is_working_now:
            new_offices = []
            for office in offices:
                if office.legal_entity_is_working_now:
                    new_offices.append(office)
            offices = new_offices

        if top_tellers_request.individual_is_working_now:
            new_offices = []
            for office in offices:
                if office.individual_is_working_now:
                    new_offices.append(office)
            offices = new_offices

        return atms, offices
