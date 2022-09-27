from dataclasses import dataclass


@dataclass(frozen=True)
class Command:
    command: str
    description: str
    alias: str

    def __eq__(self, other):
        return self.alias == other.alias

    def __hash__(self):
        return hash(self.alias)

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, d: dict):
        return cls(**d)
