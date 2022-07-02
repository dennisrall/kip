import pathlib

from kip.config.base import KIP_FILE
import os


def get_kip_file():
    file = pathlib.Path(os.getenv("HOME")) / KIP_FILE
    if not file.exists():
        file.touch()
    return str(file)
