import subprocess
from pathlib import Path

from kip.base.config_old import get_kip_file
from kip.base.models import Command, Commands
from kip.base.storage import load_from_command_file, persistent_command_set


def add_command(command: Command, kip_file: Path = get_kip_file()) -> None:
    with persistent_command_set(kip_file) as commands:
        commands.add(command)


def get_command_by_alias(alias: str, kip_file: Path = get_kip_file()) -> Command:
    commands = list_commands(kip_file=kip_file)
    for command in commands:
        if command.alias == alias:
            return command
    raise ValueError(
        f"No command with alias {alias} found. Run kip list to see all commands or kip search to find a specific one."
    )


def list_commands(kip_file: Path = get_kip_file()) -> Commands:
    return load_from_command_file(kip_file)


def remove_command(command: Command, kip_file: Path = get_kip_file()) -> None:
    with persistent_command_set(kip_file) as commands:
        if command in commands:
            commands.remove(command)


def run_command(command: Command) -> None:
    subprocess.run(command.command, shell=True)


def search_command(kip_file: Path = get_kip_file()) -> Command:
    print("mocking of searching a command with string")
    first, *_ = list_commands(kip_file=kip_file)
    return first
