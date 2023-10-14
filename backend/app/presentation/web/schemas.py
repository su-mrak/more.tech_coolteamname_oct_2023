import enum
import uuid

from pydantic import Field

from schemas.base import CamelizedBaseModel
from schemas.geo import Coordinate
from service.view_service import TellerType
from supplier.ort_supplier import Profiles


class HealthStatuses(str, enum.Enum):
    OK = "OK"
    ERR = "ERR"


class HealthResponse(CamelizedBaseModel):
    status: HealthStatuses
    error: str | None = None


class Route(CamelizedBaseModel):
    start: Coordinate = Field(..., example=Coordinate(lat=55.729414, lng=37.610190))
    end: Coordinate = Field(..., example=Coordinate(lat=55.733137, lng=37.619521))
    profile: Profiles = Profiles.FOOT_WALKING


class RouteByTeller(CamelizedBaseModel):
    start: Coordinate = Field(..., example=Coordinate(lat=55.801432, lng=37.702547))
    profile: Profiles = Profiles.FOOT_WALKING

    teller_id: uuid.UUID = Field(
        ..., example=uuid.UUID("018b2aee-bb0a-1491-d31d-e3c2802f53d5")
    )
    teller_type: TellerType = Field(..., example=TellerType.ATM)
