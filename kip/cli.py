from collections.abc import Iterator

import typer

from kip.models import Command
from kip.services import (
    add_command,
    get_command_by_alias,
    list_commands,
    remove_command,
    run_command,
    search_command,
)

app = typer.Typer()


def complete_alias(incomplete: str) -> Iterator[tuple[str, str]]:
    for command in list_commands():
        if command.alias.startswith(incomplete):
            yield command.alias, f"{command.description} || {command.command}"


@app.command()
def add(
    command: str = typer.Option(..., prompt=True),
    description: str = typer.Option(..., prompt=True),
    alias: str = typer.Option(..., prompt=True),
) -> None:
    new_command = Command(command, description, alias)
    add_command(new_command)


@app.command()
def remove(alias: str = typer.Argument(..., autocompletion=complete_alias)) -> None:
    command = get_command_by_alias(alias)
    typer.confirm(
        f"Are you sure you want to delete the command:\n{command}\n", abort=True
    )
    remove_command(command)


@app.command()
def search() -> None:
    print(search_command())


@app.command("list")
def _list() -> None:
    commands = list_commands()
    for command in commands:
        print(command)


@app.command()
def run(alias: str = typer.Argument(..., autocompletion=complete_alias)) -> None:
    command = get_command_by_alias(alias)
    typer.confirm(f"{command.command}\nRun?", abort=True)
    run_command(command)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
