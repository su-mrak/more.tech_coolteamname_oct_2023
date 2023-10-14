from dataclasses import dataclass

from repository.db_repository import DbRepository
from schemas.atm import ATM
from schemas.geo import Coordinate
from schemas.office import Office
from supplier.ort_supplier import ORTSupplier, Profiles


@dataclass
class ViewService:
    db_repository: DbRepository
    ort_supplier: ORTSupplier

    async def get_atms(self) -> list[ATM]:
        return await self.db_repository.get_atms()

    async def get_offices(self) -> list[Office]:
        return await self.db_repository.get_offices()

    async def get_route(
        self, start: Coordinate, end: Coordinate, profile: Profiles
    ) -> str:
        return await self.ort_supplier.get_route(start, end, profile)
