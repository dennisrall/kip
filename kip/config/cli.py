import pathlib

import rich
import typer
from rich import print

from kip.config.services import add_kip_file as add_kip_file_service
from kip.config.services import list_kip_files as list_kip_files_service
from kip.config.services import remove_kip_file as remove_kip_file_service

app = typer.Typer()


@app.command(name="add")
def add_kip_file(
    file: pathlib.Path = typer.Argument(
        ..., exists=True, file_okay=True, dir_okay=False, resolve_path=True
    )
) -> None:
    add_kip_file_service(file)


@app.command(name="remove")
def remove_kip_file(
    file: pathlib.Path = typer.Argument(
        ...,
        resolve_path=True,
    )
) -> None:
    remove_kip_file_service(file)


@app.command(name="list")
def list_kip_files() -> None:
    config_files = list_kip_files_service()
    rich.print("Command files:")
    for config_file in config_files:
        print(str(config_file))
