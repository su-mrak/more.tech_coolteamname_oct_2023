import calendar
import enum
from datetime import datetime, time
from typing import Any

from pydantic import Field, validator

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


weekday_ru_to_int: dict[WeekdaysRu, int] = {
    WeekdaysRu.MONDAY: calendar.MONDAY,
    WeekdaysRu.TUESDAY: calendar.TUESDAY,
    WeekdaysRu.WEDNESDAY: calendar.WEDNESDAY,
    WeekdaysRu.THURSDAY: calendar.THURSDAY,
    WeekdaysRu.FRIDAY: calendar.FRIDAY,
    WeekdaysRu.SATURDAY: calendar.SATURDAY,
    WeekdaysRu.SUNDAY: calendar.SUNDAY,
}

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


_weekday_en_to_int: dict[Weekdays, int] = {
    Weekdays.MONDAY: calendar.MONDAY,
    Weekdays.TUESDAY: calendar.TUESDAY,
    Weekdays.WEDNESDAY: calendar.WEDNESDAY,
    Weekdays.THURSDAY: calendar.THURSDAY,
    Weekdays.FRIDAY: calendar.FRIDAY,
    Weekdays.SATURDAY: calendar.SATURDAY,
    Weekdays.SUNDAY: calendar.SUNDAY,
}

_weekday_int_to_en: dict[int, Weekdays] = {
    value: key for key, value in _weekday_en_to_int.items()
}

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
    individual_is_working_now: bool | None = None
    legal_entity_schedule: Schedule
    legal_entity_is_working_now: bool | None = None
    metro_station: str | None = None
    my_branch: bool
    kep: bool = False
    has_ramp: bool = False
    suo_availability: bool = False
    sale_point_format: str
    office_type: str

    @staticmethod
    def _sort_weedkays(dict_: Schedule) -> Schedule:
        new_dict: Schedule = {}
        for key in sorted(dict_.keys(), key=lambda x: _weekday_en_to_int[x]):
            new_dict[key] = dict_[key]

        return new_dict

    @validator("individual_schedule", "legal_entity_schedule", always=True)
    @classmethod
    def sort_schedule(cls, v: Schedule) -> Schedule:
        return cls._sort_weedkays(v)

    @validator("individual_is_working_now", always=True)
    @classmethod
    def set_individual_is_working_now(
        cls, v: bool | None, values: dict[str, Any]
    ) -> bool:
        now_ = datetime.now()
        try:
            day_schedule: OpenHours = values["individual_schedule"][
                _weekday_int_to_en[now_.weekday()]
            ]
        except KeyError:
            return False

        if day_schedule.opens_at <= now_.time() <= day_schedule.closes_at:
            if (
                day_schedule.break_starts_at is not None
                and day_schedule.break_ends_at is not None
            ):
                return not (
                    day_schedule.break_starts_at
                    <= now_.time()
                    <= day_schedule.break_ends_at
                )
            return True
        return False

    # TODO make dry
    @validator("legal_entity_is_working_now", always=True)
    @classmethod
    def set_legal_entity_working_now(
        cls, v: bool | None, values: dict[str, Any]
    ) -> bool:
        now_ = datetime.now()
        try:
            day_schedule: OpenHours = values["legal_entity_schedule"][
                _weekday_int_to_en[now_.weekday()]
            ]
        except KeyError:
            return False

        if day_schedule.opens_at <= now_.time() <= day_schedule.closes_at:
            if (
                day_schedule.break_starts_at is not None
                and day_schedule.break_ends_at is not None
            ):
                return not (
                    day_schedule.break_starts_at
                    <= now_.time()
                    <= day_schedule.break_ends_at
                )
            return True
        return False
