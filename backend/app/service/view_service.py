import enum
import uuid
from dataclasses import dataclass

from repository.db_repository import DbRepository
from schemas.atm import ATM
from schemas.geo import Coordinate
from schemas.office import Office
from schemas.search import GetTopTellers
from supplier.ort_supplier import ORTSupplier, Profiles


class TellerNotFound(Exception):
    ...


class TellerType(str, enum.Enum):
    OFFICE = "OFFICE"
    ATM = "ATM"


@dataclass
class ViewService:
    db_repository: DbRepository
    ort_supplier: ORTSupplier

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

    async def get_top_teller_filtered(  # noqa: CCR001
        self, top_tellers_request: GetTopTellers
    ) -> tuple[list[ATM], list[Office]]:
        atms = await self.db_repository.search_atms(
            lat=top_tellers_request.lat,
            lng=top_tellers_request.lng,
            limit=top_tellers_request.limit,
            features=top_tellers_request.atm_feature,
        )

        offices = await self.db_repository.search_offices(
            lat=top_tellers_request.lat,
            lng=top_tellers_request.lng,
            limit=top_tellers_request.limit,
            features=top_tellers_request.office_feature,
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
