import uuid
from datetime import time

from persistence.database import ATM, Office
from schemas.atm import Features as ATMFeatures
from schemas.geo import Coordinate
from schemas.office import Features as OfficeFeatures
from schemas.office import OpenHours, Weekdays
from schemas.search import GetTopTellers
from shared.containers import Container
from supplier.ort_supplier import Profiles


class TestIntegration:
    def test_get_ddl_ok(self, combat_container: Container):
        print(combat_container.heath_service.db_repository.compile_table(ATM))
        print(combat_container.heath_service.db_repository.compile_table(Office))

    async def test_check_ok(self, combat_container: Container):
        await combat_container.heath_service.check()

    # async def test_upload_ok(self, combat_container: Container):
    #     await combat_container.upload_service.upload()

    async def test_get_atms_ok(self, combat_container: Container):
        res = await combat_container.upload_service.db_repository.get_atms()
        print(res)

    def test_parse_schedule_easy_ok(self, combat_container: Container):
        res = combat_container.upload_service.parse_schedule(
            [
                {"days": "пн", "hours": "09:00-18:00"},
                {"days": "вт", "hours": "09:00-18:00"},
                {"days": "ср", "hours": "09:00-18:00"},
                {"days": "чт", "hours": "09:00-18:00"},
                {"days": "пт", "hours": "09:00-17:00"},
                {"days": "сб", "hours": "выходной"},
                {"days": "вс", "hours": "выходной"},
            ]
        )

        assert Weekdays.SUNDAY not in res
        assert Weekdays.SATURDAY not in res
        assert res[Weekdays.WEDNESDAY] == OpenHours(
            opens_at=time(9, 0), closes_at=time(18, 0)
        )

    def test_parse_schedule_hard_ok(self, combat_container: Container):
        res = combat_container.upload_service.parse_schedule(
            [
                {"days": "пн-чт", "hours": "09:00-18:00"},
                {"days": "пт", "hours": "09:00-17:00"},
                {"days": "пн-пт", "hours": "14:15-15:00"},
                {"days": "сб,вс", "hours": "выходной"},
            ]
        )

        assert Weekdays.SUNDAY not in res
        assert Weekdays.SATURDAY not in res
        assert res[Weekdays.WEDNESDAY] == OpenHours(
            opens_at=time(9, 0),
            closes_at=time(18, 0),
            break_starts_at=time(14, 15),
            break_ends_at=time(15, 0),
        )

    def test_parse_schedule_ok(self, combat_container: Container):
        res = combat_container.upload_service.parse_schedule(
            [
                {"days": "пн-чт", "hours": "09:00-18:00"},
                {"days": "пт", "hours": "09:00-17:00"},
                {"days": "пн-пт", "hours": "14:15-15:00"},
                {"days": "сб,вс", "hours": "выходной"},
            ]
        )

        print(res)

    async def test_get_offices_ok(self, combat_container: Container):
        res = await combat_container.upload_service.db_repository.get_offices()
        print(res)

    async def test_ort_supplier_get_router(self, combat_container: Container):
        await combat_container.view_service.ort_supplier.get_route(
            Coordinate(lat=55.729863, lng=37.609558),
            Coordinate(lat=55.751647, lng=37.625734),
            profile=Profiles.DRIVING_CAR,
        )

    async def test_get_office_ok(self, combat_container: Container):
        res = await combat_container.upload_service.db_repository.get_office(
            id_=uuid.UUID("018b2add-443f-7b5a-af2b-3be58661326c")
        )
        print(res)

    async def test_get_top_tellers(self, combat_container: Container):
        res = await combat_container.view_service.get_top_teller_filtered(
            top_tellers_request=GetTopTellers(
                lat=55.801432,
                lng=37.702547,
                limit=100,
                atm_feature={ATMFeatures.BLIND},
                office_feature={OfficeFeatures.INDIVIDUAL_DEPOSITS},
            ),
        )
        print(res)
