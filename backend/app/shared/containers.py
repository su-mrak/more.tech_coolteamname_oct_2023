from dataclasses import dataclass


@dataclass
class Container:
    ...


def init_combat_container() -> Container:
    return Container()
