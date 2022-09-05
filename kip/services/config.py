import os
import pathlib

KIP_FILE = '.kip'


def get_kip_file():
    file = pathlib.Path(os.getenv("HOME")) / KIP_FILE
    if not file.exists():
        file.touch()
    return str(file)
