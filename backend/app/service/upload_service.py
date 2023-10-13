from dataclasses import dataclass
from typing import Any

import ujson
from tqdm import tqdm

from repository.db_repository import DbRepository
from schemas.atm import ServiceConfiguration, Services
from schemas.office import (
    OpenHours,
    Schedule,
    WeekdaysRu,
    weekday_ru_to_en,
    weekdays_ru,
)
from shared.base import logger


@dataclass
class UploadService:
    db_repository: DbRepository

    def __post_init__(self) -> None:
        self.atms_json_filename = "./app/data/atms.json"
        self.offices_json_filename = "./app/data/offices.json"

        self._weekend = "выходной"
        self._no_legal_entiry = "Не обслуживает ЮЛ"

    def _parse_hours(self, hours: str) -> OpenHours:
        hours_splited = hours.split("-")
        return OpenHours(opens_at=hours_splited[0], closes_at=hours_splited[1])

    def _process_day(self, schedule: Schedule, day: str, hours: str) -> None:
        if hours == self._weekend:
            return
        en_day = weekday_ru_to_en[day]
        schedule[en_day] = self._parse_hours(hours)

    def schedule_to_dict(self, schedule: Schedule) -> dict[str, Any]:
        dict_ = {}
        for key, value in schedule.items():
            dict_[key] = value.jsonable_encoder(exclude_none=True)

        return dict_

    def parse_schedule(  # noqa: C901, CCR001
        self,
        schedule_unparsed: list[dict[str, str]],
    ) -> Schedule:
        schedule: Schedule = {}
        has_break = False
        break_hours: OpenHours | None = None
        break_first_day: WeekdaysRu | None = None
        break_last_day: WeekdaysRu | None = None

        for day in schedule_unparsed:
            days = day["days"]
            hours = day["hours"]
            if days == self._no_legal_entiry:
                return {}

            if days in weekday_ru_to_en:
                self._process_day(schedule=schedule, day=days, hours=hours)

            days_splited = days.split("-")
            if len(days_splited) == 2:
                first_day = WeekdaysRu(days_splited[0])
                last_day = WeekdaysRu(days_splited[1])
                if weekday_ru_to_en[first_day] in schedule:
                    # Этот день уже был, значит это расписание перерыва
                    break_first_day = first_day
                    break_last_day = last_day
                    break_hours = self._parse_hours(hours)
                    has_break = True
                    continue

                for idx, day in enumerate(weekdays_ru):
                    if first_day.order() <= idx <= last_day.order():
                        self._process_day(schedule=schedule, day=day, hours=hours)

            two_days = days.split(",")
            if len(two_days) == 2:
                self._process_day(schedule=schedule, day=two_days[0], hours=hours)
                self._process_day(schedule=schedule, day=two_days[1], hours=hours)

        if has_break:
            for idx, day in enumerate(weekdays_ru):
                if (
                    break_first_day.order() <= idx <= break_last_day.order()
                    and weekday_ru_to_en[day] in schedule
                ):
                    schedule[
                        weekday_ru_to_en[day]
                    ].break_starts_at = break_hours.opens_at
                    schedule[
                        weekday_ru_to_en[day]
                    ].break_ends_at = break_hours.closes_at

        return schedule

    async def upload(self) -> None:
        with open(self.atms_json_filename) as f:
            atms: list[dict] = ujson.load(f)["atms"]
            logger.info("Fetched {} atms", len(atms))

        with open(self.offices_json_filename) as f:
            offices: list[dict] = ujson.load(f)
            logger.info("Fetched {} offices", len(offices))

        for atm in tqdm(atms):
            break
            await self.db_repository.insert_atm(
                address=atm["address"],
                all_day=atm["allDay"],
                services=Services(
                    blind=ServiceConfiguration(
                        service_activity=atm["services"]["blind"]["serviceActivity"]
                        == "AVAILABLE",
                        service_capability=atm["services"]["blind"]["serviceCapability"]
                        == "SUPPORTED",
                    ),
                    nfc_for_bank_cards=ServiceConfiguration(
                        service_activity=atm["services"]["nfcForBankCards"][
                            "serviceActivity"
                        ]
                        == "AVAILABLE",
                        service_capability=atm["services"]["nfcForBankCards"][
                            "serviceCapability"
                        ]
                        == "SUPPORTED",
                    ),
                    supports_charge_rub=ServiceConfiguration(
                        service_activity=atm["services"]["supportsChargeRub"][
                            "serviceActivity"
                        ]
                        == "AVAILABLE",
                        service_capability=atm["services"]["supportsChargeRub"][
                            "serviceCapability"
                        ]
                        == "SUPPORTED",
                    ),
                    supports_eur=ServiceConfiguration(
                        service_activity=atm["services"]["supportsEur"][
                            "serviceActivity"
                        ]
                        == "AVAILABLE",
                        service_capability=atm["services"]["supportsEur"][
                            "serviceCapability"
                        ]
                        == "SUPPORTED",
                    ),
                    supports_rub=ServiceConfiguration(
                        service_activity=atm["services"]["supportsRub"][
                            "serviceActivity"
                        ]
                        == "AVAILABLE",
                        service_capability=atm["services"]["supportsRub"][
                            "serviceCapability"
                        ]
                        == "SUPPORTED",
                    ),
                    supports_usd=ServiceConfiguration(
                        service_activity=atm["services"]["supportsUsd"][
                            "serviceActivity"
                        ]
                        == "AVAILABLE",
                        service_capability=atm["services"]["supportsUsd"][
                            "serviceCapability"
                        ]
                        == "SUPPORTED",
                    ),
                    qr_read=ServiceConfiguration(
                        service_activity=atm["services"]["qrRead"]["serviceActivity"]
                        == "AVAILABLE",
                        service_capability=atm["services"]["qrRead"][
                            "serviceCapability"
                        ]
                        == "SUPPORTED",
                    ),
                    wheelchair=ServiceConfiguration(
                        service_activity=atm["services"]["wheelchair"][
                            "serviceActivity"
                        ]
                        == "AVAILABLE",
                        service_capability=atm["services"]["wheelchair"][
                            "serviceCapability"
                        ]
                        == "SUPPORTED",
                    ),
                ).jsonable_encoder(),
                lng=atm["longitude"],
                lat=atm["latitude"],
            )

        for office in tqdm(offices):
            await self.db_repository.insert_office(
                address=office["address"],
                lng=office["longitude"],
                lat=office["latitude"],
                sale_point_format=office["salePointFormat"],
                my_branch=office["myBranch"],
                kep=bool(office["kep"]),
                has_ramp=office["hasRamp"] == "Y",
                suo_availability=office["suoAvailability"] == "Y",
                office_type=office["officeType"],
                sale_point_name=office["salePointName"],
                metro_station=office["metroStation"],
                individual_schedule=self.schedule_to_dict(
                    self.parse_schedule(office["openHoursIndividual"])
                ),
                legal_entity_schedule=self.schedule_to_dict(
                    self.parse_schedule(office["openHours"])
                ),
            )
