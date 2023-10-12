from dataclasses import dataclass

from repository.db_repository import DbRepository
from service.heath_service import HeathService


@dataclass
class Container:
    heath_service: HeathService


def init_combat_container() -> Container:
    db_repository = DbRepository()
    heath_service = HeathService(db_repository=db_repository)

    return Container(heath_service=heath_service)
