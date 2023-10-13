import enum
from datetime import time

from pydantic import Field

from schemas.base import CamelizedBaseModel
from schemas.geo import GeoObject


class Weekdays(str, enum.Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"


class OpenHours(CamelizedBaseModel):
    opens_at: time
    closes_at: time


class Office(GeoObject):
    sale_point_name: str = Field(
        ..., example="ДО «Солнечногорский» Филиала № 7701 Банка ВТБ (ПАО)"
    )
    individual_schedule: dict[Weekdays, OpenHours]
    legal_entity_schedule: dict[Weekdays, OpenHours]
    metro_station: str | None = None
    my_branch: bool
    kep: bool = False
    has_ramp: bool = False
    suo_availability: bool = False
    sale_point_format: str
    office_type: str
