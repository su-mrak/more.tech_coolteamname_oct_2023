from datetime import time

from persistence.database import ATM, Office
from schemas.office import OpenHours, Weekdays
from shared.containers import Container


class TestIntegration:
    def test_get_ddl_ok(self, combat_container: Container):
        print(combat_container.heath_service.db_repository.compile_table(ATM))
        print(combat_container.heath_service.db_repository.compile_table(Office))

    async def test_check_ok(self, combat_container: Container):
        await combat_container.heath_service.check()

    async def test_upload_ok(self, combat_container: Container):
        await combat_container.upload_service.upload()

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
            opens_at=time(9, 0), closes_at=time(18, 0)
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
