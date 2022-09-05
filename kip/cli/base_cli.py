import typer

from kip.models.command import Command
from kip.services.list_commands import list_commands
from kip.services.add_command import add_command
from kip.services.get_command import get_command_by_alias
from kip.services.remove_command import remove_command
from kip.services.run_command import run_command
from kip.services.search_command import search_command

app = typer.Typer()


# shell completion
# ensure aliases are unique

def complete_alias(incomplete: str):
    for command in list_commands():
        if command.alias.startswith(incomplete):
            yield command.alias, f"{command.description} || {command.command}"


@app.command()
def add(command: str = typer.Option(..., prompt=True),
        description: str = typer.Option(..., prompt=True),
        alias: str = typer.Option(..., prompt=True)) -> None:
    command = Command(command, description, alias)
    add_command(command)


@app.command()
def remove(alias: str = typer.Argument(..., autocompletion=complete_alias)) -> None:
    command = get_command_by_alias(alias)
    typer.confirm(f"Are you sure you want to delete the command:\n{command}\n", abort=True)
    remove_command(command)


@app.command()
def search() -> None:
    print(search_command())


@app.command("list")
def _list():
    commands = list_commands()
    for command in commands:
        print(command)


@app.command()
def run(alias: str = typer.Argument(..., autocompletion=complete_alias)):
    command = get_command_by_alias(alias)
    typer.confirm(f"{command.command}\nRun?", abort=True)
    run_command(command)


def main():
    app()


if __name__ == '__main__':
    main()
