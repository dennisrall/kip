import pathlib

file_name = str | pathlib.Path


def get_cwd() -> pathlib.Path:
    return pathlib.Path.cwd()
