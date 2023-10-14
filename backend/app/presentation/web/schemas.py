import enum

from pydantic import Field

from schemas.base import CamelizedBaseModel
from schemas.geo import Coordinate
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
