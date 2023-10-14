import enum
import uuid

from pydantic import Field

from schemas.atm import ATM
from schemas.base import CamelizedBaseModel
from schemas.geo import Coordinate
from schemas.office import Office
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


class ATMServices(str, enum.Enum):
    WITHDRAWAL = "withdrawal"
    REPLENISHMENT = "replenishment"


class ATMFeatures(str, enum.Enum):
    NFC_SUPPORT = "NFC_SUPPORT"
    QR_SUPPORT = "QR_SUPPORT"
    VISUALLY_IMPAIRED_SUPPORT = "VISUALLY_IMPAIRED_SUPPORT"


class ATMFilter(CamelizedBaseModel):
    services: set[ATMServices] | None = None
    features: set[ATMFeatures] | None = None


class OfficeServices(str, enum.Enum):
    INDIVIDUAL_MORTGAGE_LENDING = "INDIVIDUAL_MORTGAGE_LENDING"
    INDIVIDUAL_DEPOSITS = "INDIVIDUAL_DEPOSITS"
    INDIVIDUAL_CURRENCY_EXCHANGE_OPERATIONS = "INDIVIDUAL_CURRENCY_EXCHANGE_OPERATIONS"
    LEGAL_ENTITY_LENDING = "LEGAL_ENTITY_LENDING"
    LEGAL_ENTITY_SETTLEMENT_SERVICE = "LEGAL_ENTITY_SETTLEMENT_SERVICE"


class OfficeFilter(CamelizedBaseModel):
    is_working_now: bool | None = None
    services: set[OfficeServices] | None = None
    available_with_limited_mobility: bool | None = None


class GetTopTellers(CamelizedBaseModel):
    limit: int = 10
    lat: float = 55.801432
    lng: float = 37.702547

    atm_filters: ATMFilter = ATMFilter()
    office_filters: OfficeFilter = OfficeFilter()


class TopTellersResponse(CamelizedBaseModel):
    atms: list[ATM]
    offices: list[Office]
