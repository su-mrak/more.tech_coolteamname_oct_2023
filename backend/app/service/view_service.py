from dataclasses import dataclass

from repository.db_repository import DbRepository
from schemas.atm import ATM


@dataclass
class ViewService:
    db_repository: DbRepository

    async def get_atms(self) -> list[ATM]:
        return await self.db_repository.get_atms()
