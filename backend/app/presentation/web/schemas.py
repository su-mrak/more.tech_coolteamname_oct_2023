from schemas.base import CamelizedBaseModel
import enum


class HealthStatuses(str, enum.Enum):
    OK = "OK"
    ERR = "ERR"


class HealthResponse(CamelizedBaseModel):
    status: HealthStatuses
    errors: list[str] | None = None
