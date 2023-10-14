from dataclasses import dataclass
from random import randint
from typing import Any

import ujson
from tqdm import tqdm

from repository.db_repository import DbRepository
from schemas.atm import Features
from schemas.dates import WeekdaysRu, weekday_ru_to_en, weekday_ru_to_int, weekdays_ru
from schemas.office import Features as OfficeFeatures
from schemas.office import OpenHours, Schedule
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
                    if (
                        weekday_ru_to_int[first_day]
                        <= idx
                        <= weekday_ru_to_int[last_day]
                    ):
                        self._process_day(schedule=schedule, day=day, hours=hours)

            two_days = days.split(",")
            if len(two_days) == 2:
                self._process_day(schedule=schedule, day=two_days[0], hours=hours)
                self._process_day(schedule=schedule, day=two_days[1], hours=hours)

        if has_break:
            for idx, day in enumerate(weekdays_ru):
                if (
                    weekday_ru_to_int[break_first_day]
                    <= idx
                    <= weekday_ru_to_int[break_last_day]
                    and weekday_ru_to_en[day] in schedule
                ):
                    schedule[
                        weekday_ru_to_en[day]
                    ].break_starts_at = break_hours.opens_at
                    schedule[
                        weekday_ru_to_en[day]
                    ].break_ends_at = break_hours.closes_at

        return schedule

    @staticmethod
    def _get_random_bool() -> bool:
        return bool(randint(0, 1))  # noqa: S311

    async def upload(self) -> None:  # noqa: CCR001, C901
        with open(self.atms_json_filename) as f:
            atms: list[dict] = ujson.load(f)["atms"]
            logger.info("Fetched {} atms", len(atms))

        with open(self.offices_json_filename) as f:
            offices: list[dict] = ujson.load(f)
            logger.info("Fetched {} offices", len(offices))

        for atm in tqdm(atms):
            atm_features: list[Features] = []
            if atm["services"]["blind"]["serviceActivity"] == "AVAILABLE":
                atm_features.append(Features.BLIND)
            if atm["services"]["nfcForBankCards"]["serviceActivity"] == "AVAILABLE":
                atm_features.append(Features.NFC_FOR_BANK_CARDS)
            if atm["services"]["supportsRub"]["serviceActivity"] == "AVAILABLE":
                atm_features.append(Features.WITHDRAWAL_RUB)
                atm_features.append(Features.REPLENISHMENT_RUB)
            if atm["services"]["supportsEur"]["serviceActivity"] == "AVAILABLE":
                atm_features.append(Features.WITHDRAWAL_EUR)
                atm_features.append(Features.REPLENISHMENT_EUR)
            if atm["services"]["supportsUsd"]["serviceActivity"] == "AVAILABLE":
                atm_features.append(Features.WITHDRAWAL_USD)
                atm_features.append(Features.REPLENISHMENT_USD)
            if atm["services"]["qrRead"]["serviceActivity"] == "AVAILABLE":
                atm_features.append(Features.QR_READ)
            if atm["services"]["wheelchair"]["serviceActivity"] == "AVAILABLE":
                atm_features.append(Features.WHEELCHAIR)
            if atm["allDay"]:
                atm_features.append(Features.ALL_DAY)
            prediction = randint(0, 5)  # noqa: S311
            await self.db_repository.insert_atm(
                address=atm["address"],
                features=atm_features,
                prediction=prediction,
                lng=atm["longitude"],
                lat=atm["latitude"],
            )

        for office in tqdm(offices):
            office_features: list[OfficeFeatures] = []
            if office["myBranch"]:
                office_features.append(OfficeFeatures.MY_BRANCH)
            if office["kep"]:
                office_features.append(OfficeFeatures.KEP)
            if office["hasRamp"] == "Y":
                office_features.append(OfficeFeatures.HAS_RAMP)
            if office["suoAvailability"] == "Y":
                office_features.append(OfficeFeatures.SUO_AVAILABILITY)

            if UploadService._get_random_bool():
                office_features.append(OfficeFeatures.INDIVIDUAL_MORTGAGE_LENDING)
            if UploadService._get_random_bool():
                office_features.append(
                    OfficeFeatures.INDIVIDUAL_CURRENCY_EXCHANGE_OPERATIONS
                )
            if UploadService._get_random_bool():
                office_features.append(OfficeFeatures.INDIVIDUAL_DEPOSITS)
            if UploadService._get_random_bool():
                office_features.append(OfficeFeatures.LEGAL_ENTITY_LENDING)
            if UploadService._get_random_bool():
                office_features.append(OfficeFeatures.LEGAL_ENTITY_SETTLEMENT_SERVICE)
            prediction = randint(0, 5)  # noqa: S311
            await self.db_repository.insert_office(
                address=office["address"],
                lng=office["longitude"],
                lat=office["latitude"],
                sale_point_format=office["salePointFormat"],
                features=office_features,
                load=prediction,
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
