import enum
from datetime import datetime, time
from typing import Any

from pydantic import Field, validator

from schemas.base import CamelizedBaseModel
from schemas.dates import Weekdays, weekday_en_to_int, weekday_int_to_en
from schemas.geo import GeoObject


class Features(str, enum.Enum):
    INDIVIDUAL_MORTGAGE_LENDING = "INDIVIDUAL_MORTGAGE_LENDING"
    INDIVIDUAL_DEPOSITS = "INDIVIDUAL_DEPOSITS"
    INDIVIDUAL_CURRENCY_EXCHANGE_OPERATIONS = "INDIVIDUAL_CURRENCY_EXCHANGE_OPERATIONS"

    LEGAL_ENTITY_LENDING = "LEGAL_ENTITY_LENDING"
    LEGAL_ENTITY_SETTLEMENT_SERVICE = "LEGAL_ENTITY_SETTLEMENT_SERVICE"

    HAS_RAMP = "HAS_RAMP"
    MY_BRANCH = "MY_BRANCH"
    KEP = "KEP"
    SUO_AVAILABILITY = "SUO_AVAILABILITY"


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
    sale_point_format: str
    office_type: str
    features: set[Features] = set()

    @staticmethod
    def _sort_weedkays(dict_: Schedule) -> Schedule:
        new_dict: Schedule = {}
        for key in sorted(dict_.keys(), key=lambda x: weekday_en_to_int[x]):
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
                weekday_int_to_en[now_.weekday()]
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
                weekday_int_to_en[now_.weekday()]
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
