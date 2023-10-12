from dataclasses import dataclass

from repository.db_repository import DbRepository
from shared.base import logger


class CheckFailed(Exception):
    ...


@dataclass
class HeathService:
    db_repository: DbRepository

    async def check(self) -> None:
        try:
            await self.db_repository.check()
        except Exception as exc:
            raise CheckFailed("Check failed for db_repository") from exc
        else:
            logger.info("db_repository check passed")
