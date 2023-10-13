import enum
from datetime import time

from pydantic import Field

from schemas.base import CamelizedBaseModel
from schemas.geo import GeoObject


class WeekdaysRu(str, enum.Enum):
    MONDAY = "пн"
    TUESDAY = "вт"
    WEDNESDAY = "ср"
    THURSDAY = "чт"
    FRIDAY = "пт"
    SATURDAY = "сб"
    SUNDAY = "вс"

    def order(self) -> int:
        if self == self.__class__.MONDAY:
            return 0
        if self == self.__class__.TUESDAY:
            return 1
        if self == self.__class__.WEDNESDAY:
            return 2
        if self == self.__class__.THURSDAY:
            return 3
        if self == self.__class__.FRIDAY:
            return 4
        if self == self.__class__.SATURDAY:
            return 5
        if self == self.__class__.SUNDAY:
            return 6
        return -1


weekdays_ru: list[WeekdaysRu] = [
    WeekdaysRu.MONDAY,
    WeekdaysRu.TUESDAY,
    WeekdaysRu.WEDNESDAY,
    WeekdaysRu.THURSDAY,
    WeekdaysRu.FRIDAY,
    WeekdaysRu.SATURDAY,
    WeekdaysRu.SUNDAY,
]


class Weekdays(str, enum.Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"


weekday_ru_to_en: dict[WeekdaysRu, Weekdays] = {
    WeekdaysRu.MONDAY: Weekdays.MONDAY,
    WeekdaysRu.TUESDAY: Weekdays.TUESDAY,
    WeekdaysRu.WEDNESDAY: Weekdays.WEDNESDAY,
    WeekdaysRu.THURSDAY: Weekdays.THURSDAY,
    WeekdaysRu.FRIDAY: Weekdays.FRIDAY,
    WeekdaysRu.SATURDAY: Weekdays.SATURDAY,
    WeekdaysRu.SUNDAY: Weekdays.SUNDAY,
}


class OpenHours(CamelizedBaseModel):
    opens_at: time
    closes_at: time
    break_starts_at: time | None = None
    break_ends_at: time | None = None


Schedule = dict[Weekdays, OpenHours]


class Office(GeoObject):
    sale_point_name: str = Field(
        ..., example="ДО «Солнечногорский» Филиала № 7701 Банка ВТБ (ПАО)"
    )
    individual_schedule: Schedule
    legal_entity_schedule: Schedule
    metro_station: str | None = None
    my_branch: bool
    kep: bool = False
    has_ramp: bool = False
    suo_availability: bool = False
    sale_point_format: str
    office_type: str
