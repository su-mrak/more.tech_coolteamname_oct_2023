from pydantic import Field

from schemas.atm import Features as ATMFeature
from schemas.base import CamelizedBaseModel
from schemas.office import Features as OfficeFeature


class GetTopTellers(CamelizedBaseModel):
    limit: int = 10
    lat: float = Field(..., example=55.801432)
    lng: float = Field(..., example=37.702547)

    atm_feature: set[ATMFeature] | None = None
    office_feature: set[OfficeFeature] | None = None
