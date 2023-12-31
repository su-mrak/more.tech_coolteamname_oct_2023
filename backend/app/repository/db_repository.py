import uuid
from dataclasses import dataclass
from typing import Any

from geoalchemy2.functions import ST_Distance
from pydantic import ValidationError
from shapely import wkb
from sqlalchemy import insert, select, text
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.schema import CreateTable

from persistence.database import ATM, Office
from schemas.atm import ATM as ATMModel
from schemas.atm import Features as ATMFeatures
from schemas.geo import Coordinate
from schemas.office import Features as OfficeFeatures
from schemas.office import Office as OfficeModel
from shared.base import logger
from shared.settings import app_settings


@dataclass
class DbRepository:
    def __post_init__(self) -> None:
        self._engine = create_async_engine(
            f"postgresql+asyncpg://{app_settings.pg_username}:{app_settings.pg_password}@"
            f"{app_settings.pg_host}:{app_settings.pg_port}/{app_settings.pg_database}",
        )
        self.srid = 4326

    async def check(self) -> None:
        async with self._engine.connect() as session:
            result = await session.execute(text("select 1"))
            one = result.fetchone()
            if one is not None and one[0] != 1:
                raise Exception('Should be 1 from "select 1"')

    async def insert_atm(
        self,
        lat: float,
        lng: float,
        prediction: int,
        address: str,
        features: list[ATMFeatures],
    ) -> None:
        async with self._engine.connect() as session:
            statement = insert(ATM).values(
                address=address,
                coordinate=self.make_point(lat=lat, lng=lng),
                features=features,
                prediction=prediction,
            )
            await session.execute(statement)
            await session.commit()

    def make_point(self, lat: float, lng: float) -> str:
        return f"SRID={self.srid};POINT({lng} {lat})"

    async def insert_office(
        self,
        address: str,
        lat: float,
        lng: float,
        load: int,
        sale_point_name: str,
        individual_schedule: Any,
        legal_entity_schedule: Any,
        features: list[OfficeFeatures],
        metro_station: str,
        sale_point_format: str,
        office_type: str,
    ) -> None:
        async with self._engine.connect() as session:
            statement = insert(Office).values(
                address=address,
                coordinate=self.make_point(lat=lat, lng=lng),
                sale_point_name=sale_point_name,
                individual_schedule=individual_schedule,
                legal_entity_schedule=legal_entity_schedule,
                metro_station=metro_station,
                features=features,
                sale_point_format=sale_point_format,
                office_type=office_type,
                prediction=load,
            )
            await session.execute(statement)
            await session.commit()

    @staticmethod
    def wkb_to_coordinate(wkb_point: Any) -> Coordinate:
        coordinates = wkb.loads(str(wkb_point))
        return Coordinate(lat=coordinates.y, lng=coordinates.x)

    async def get_atms(self) -> list[ATMModel]:
        async with self._engine.connect() as session:
            statement = select(ATM)
            rows = (await session.execute(statement)).fetchall()
        res: list[ATMModel] = []
        for row in rows:
            try:
                res.append(
                    ATMModel(
                        id=row.internal_id,
                        address=row.address,
                        coordinate=DbRepository.wkb_to_coordinate(row.coordinate),
                        features=row.features,
                        load=row.prediction,
                    )
                )
            except ValidationError:
                logger.exception(f"Unable to parse model, {row=}")

        return res

    async def get_office(self, id_: uuid.UUID) -> OfficeModel | None:
        async with self._engine.connect() as session:
            statement = select(Office).where(Office.internal_id == id_)
            row = (await session.execute(statement)).fetchone()
        if row is None:
            return None

        return OfficeModel(
            id=row.internal_id,
            address=row.address,
            coordinate=DbRepository.wkb_to_coordinate(row.coordinate),
            sale_point_format=row.sale_point_format,
            legal_entity_schedule=row.legal_entity_schedule,
            features=row.features,
            office_type=row.office_type,
            sale_point_name=row.sale_point_name,
            individual_schedule=row.individual_schedule,
            load=row.prediction,
        )

    async def get_atm(self, id_: uuid.UUID) -> ATMModel | None:
        async with self._engine.connect() as session:
            statement = select(ATM).where(ATM.internal_id == id_)
            row = (await session.execute(statement)).fetchone()
        if row is None:
            return None

        return ATMModel(
            id=row.internal_id,
            address=row.address,
            coordinate=DbRepository.wkb_to_coordinate(row.coordinate),
            features=row.features,
            load=row.prediction,
        )

    async def get_offices(self) -> list[OfficeModel]:
        async with self._engine.connect() as session:
            statement = select(Office)
            rows = (await session.execute(statement)).fetchall()
        res: list[OfficeModel] = []
        for row in rows:
            try:
                res.append(
                    OfficeModel(
                        id=row.internal_id,
                        address=row.address,
                        coordinate=DbRepository.wkb_to_coordinate(row.coordinate),
                        sale_point_format=row.sale_point_format,
                        legal_entity_schedule=row.legal_entity_schedule,
                        features=row.features,
                        office_type=row.office_type,
                        sale_point_name=row.sale_point_name,
                        individual_schedule=row.individual_schedule,
                        load=row.prediction,
                    )
                )
            except ValidationError:
                logger.exception(f"Unable to parse model, {row=}")

        return res

    def compile_table(self, table) -> str:  # noqa: ANN001
        return CreateTable(table.__table__).compile(dialect=postgresql.dialect())

    async def search_atms(
        self, lat: float, lng: float, limit: int, features: set[ATMFeatures] | None
    ) -> list[ATMModel]:
        async with self._engine.connect() as session:
            statement = (
                select(ATM)
                .order_by(
                    ST_Distance(ATM.coordinate, self.make_point(lat=lat, lng=lng))
                )
                .limit(limit)
            )
            if features is not None:
                statement = statement.where(
                    ATM.features.comparator.contains(
                        [feature.value for feature in features]
                    )
                )

            rows = (await session.execute(statement)).fetchall()
        res: list[ATMModel] = []
        for row in rows:
            try:
                res.append(
                    ATMModel(
                        id=row.internal_id,
                        address=row.address,
                        coordinate=DbRepository.wkb_to_coordinate(row.coordinate),
                        features=row.features,
                        load=row.prediction,
                    )
                )
            except ValidationError:
                logger.exception(f"Unable to parse model, {row=}")

        return res

    async def search_offices(
        self, lat: float, lng: float, limit: int, features: set[OfficeFeatures] | None
    ) -> list[OfficeModel]:
        async with self._engine.connect() as session:
            statement = (
                select(Office)
                .order_by(
                    ST_Distance(Office.coordinate, self.make_point(lat=lat, lng=lng))
                )
                .limit(limit)
            )
            if features is not None:
                statement = statement.where(
                    Office.features.comparator.contains(
                        [feature.value for feature in features]
                    )
                )
            rows = (await session.execute(statement)).fetchall()
        res: list[OfficeModel] = []
        for row in rows:
            try:
                res.append(
                    OfficeModel(
                        id=row.internal_id,
                        address=row.address,
                        coordinate=DbRepository.wkb_to_coordinate(row.coordinate),
                        sale_point_format=row.sale_point_format,
                        legal_entity_schedule=row.legal_entity_schedule,
                        features=row.features,
                        office_type=row.office_type,
                        sale_point_name=row.sale_point_name,
                        individual_schedule=row.individual_schedule,
                        load=row.prediction,
                    )
                )
            except ValidationError:
                logger.exception(f"Unable to parse model, {row=}")

        return res
