from dataclasses import dataclass

from repository.db_repository import DbRepository
from schemas.atm import ATM
from schemas.office import Office


@dataclass
class ViewService:
    db_repository: DbRepository

    async def get_atms(self) -> list[ATM]:
        return await self.db_repository.get_atms()

    async def get_offices(self) -> list[Office]:
        return await self.db_repository.get_offices()
