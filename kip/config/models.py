import dataclasses


@dataclasses.dataclass
class Config:
    kip_files: list[str]
