from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Command:
    command: str
    description: str
    alias: str

    def __eq__(self, other: object) -> bool:
        # isinstance(other, Command) check is not working here
        return self.alias == other.alias  # type: ignore

    def __hash__(self) -> int:
        return hash(self.alias)

    def to_dict(self) -> dict[str, str]:
        return self.__dict__

    @classmethod
    def from_dict(cls, d: dict[str, str]) -> Command:
        return cls(**d)


Commands = set[Command]
