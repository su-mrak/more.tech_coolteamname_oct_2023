from shared.containers import Container


class TestIntegration:
    async def test_check_ok(self, combat_container: Container):
        await combat_container.heath_service.check()
