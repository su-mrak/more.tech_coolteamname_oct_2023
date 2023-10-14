import enum
import uuid
from dataclasses import dataclass

from repository.db_repository import DbRepository
from schemas.atm import ATM
from schemas.geo import Coordinate
from schemas.office import Office
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
