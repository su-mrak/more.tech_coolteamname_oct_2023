from persistence.database import ATM, Office
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
