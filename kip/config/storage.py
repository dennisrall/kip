import contextlib
import dataclasses
import pathlib
from collections.abc import Iterator

import typer
import yaml

from kip.config.models import Config

APP_NAME = "kip"
CONFIG_FILE = "config.yaml"


def get_config_file() -> pathlib.Path:
    app_dir_name = typer.get_app_dir(APP_NAME)
    app_dir = pathlib.Path(app_dir_name)
    app_dir.mkdir(exist_ok=True)
    config_file = app_dir / CONFIG_FILE
    config_file.touch(exist_ok=True)
    return config_file


def load_config_file() -> Config:
    with open(get_config_file()) as config_file:
        config_dict = yaml.safe_load(config_file)
    return Config(**config_dict)


def save_config_file(config: Config) -> None:
    with open(get_config_file(), "w") as config_file:
        config_dict = dataclasses.asdict(config)
        yaml.safe_dump(config_dict, config_file)


@contextlib.contextmanager
def persistent_config() -> Iterator[Config]:
    config = load_config_file()
    try:
        yield config
    finally:
        save_config_file(config)
