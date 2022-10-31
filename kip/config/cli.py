import pathlib

import typer
from rich import print

from kip.config.services import add_config_file, list_kip_files, remove_config_file

app = typer.Typer()


@app.command()
def add_file(
    file: pathlib.Path = typer.Argument(
        ..., exists=True, file_okay=False, resolve_path=True
    )
) -> None:
    add_config_file(file)


@app.command()
def remove_file(
    file: pathlib.Path = typer.Argument(
        ...,
        file_okay=False,
        resolve_path=True,
    )
) -> None:
    remove_config_file(file)


@app.command()
def list_files() -> None:
    config_files = list_kip_files()
    print("Command files:")
    for config_file in config_files:
        print(str(config_file))
