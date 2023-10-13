import asyncio

from shared.containers import init_combat_container


def main() -> None:
    loop = asyncio.new_event_loop()
    loop.run_until_complete(init_combat_container().upload_service.upload())


if __name__ == "__main__":
    main()
