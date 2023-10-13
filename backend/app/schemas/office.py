import enum
from datetime import time

from pydantic import Field

from schemas.base import CamelizedBaseModel
from schemas.geo import GeoObject


class Weekdays(str, enum.Enum):
    MON = "MON"
    TUE = "TUE"
    WED = "WED"
    THU = "THU"
    FRI = "FRI"
    SAT = "SAT"
    SUN = "SUN"


class OpenHours(CamelizedBaseModel):
    opens_at: time
    closes_at: time


class Office(GeoObject):
    sale_point_name: str = Field(
        ..., example="ДО «Солнечногорский» Филиала № 7701 Банка ВТБ (ПАО)"
    )
    schedule: dict[Weekdays, OpenHours]
