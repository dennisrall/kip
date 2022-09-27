import subprocess

from kip.config import get_kip_file
from kip.models import Command
from kip.storage import persistent_command_set, load_from_command_file


def add_command(command: Command, kip_file=get_kip_file()) -> None:
    with persistent_command_set(kip_file) as commands:
        commands.add(command)


def get_command_by_alias(alias: str) -> Command:
    commands = list_commands()
    for command in commands:
        if command.alias == alias:
            return command
    raise ValueError(
        f"No command with alias {alias} found. Run kip list to see all commands or kip search to find a specific one.")


def list_commands(kip_file=get_kip_file()) -> set[Command]:
    return load_from_command_file(kip_file)


def remove_command(command: Command, kip_file=get_kip_file()):
    with persistent_command_set(kip_file) as commands:
        if command in commands:
            commands.remove(command)


def run_command(command: Command) -> None:
    subprocess.run(command.command, shell=True)


def search_command(kip_file=get_kip_file()) -> Command:
    print("mocking of searching a command with string")
    first, *_ = list_commands(kip_file=kip_file)
    return first