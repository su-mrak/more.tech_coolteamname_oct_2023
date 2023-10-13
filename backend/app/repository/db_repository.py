from dataclasses import dataclass
from typing import Any

from pydantic import ValidationError
from shapely import wkb
from sqlalchemy import insert, select, text
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.schema import CreateTable

from persistence.database import ATM
from schemas.atm import ATM as ATMModel
from schemas.geo import Coordinate
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
        self, address: str, all_day: bool, services: Any, lat: float, lng: float
    ) -> None:
        async with self._engine.connect() as session:
            statement = insert(ATM).values(
                address=address,
                all_day=all_day,
                services=services,
                coordinate=f"SRID={self.srid};POINT({lng} {lat})",
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
                        all_day=row.all_day,
                        services=row.services,
                    )
                )
            except ValidationError:
                logger.exception(f"Unable to parse model, {row=}")

        return res

    def compile_table(self, table) -> str:  # noqa: ANN001
        return CreateTable(table.__table__).compile(dialect=postgresql.dialect())
