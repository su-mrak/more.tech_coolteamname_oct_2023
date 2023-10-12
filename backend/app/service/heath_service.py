from dataclasses import dataclass


@dataclass
class Heath:
    def check(self) -> None:
        ...
