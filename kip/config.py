import os
import pathlib

KIP_FILE = '.kip'


def get_kip_file() -> pathlib.Path:
    file = pathlib.Path(os.getenv("HOME", default="~")) / KIP_FILE
    if not file.exists():
        file.touch()
    return file
