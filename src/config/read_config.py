import pathlib

from src.config.base import KIP_FILE


def get_kip_file():
    file = pathlib.Path(KIP_FILE)
    if not file.exists():
        file.touch()
    return KIP_FILE
