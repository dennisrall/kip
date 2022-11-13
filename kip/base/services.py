import pathlib
import subprocess

from kip.base.lib import get_cwd
from kip.base.models import Command, Commands
from kip.base.storage import load_from_command_file, persistent_command_set
from kip.config.services import get_kip_file_for_path, list_kip_files


def add_command(command: Command) -> None:
    kip_file = get_kip_file_for_path(get_cwd())
    with persistent_command_set(kip_file) as commands:
        commands.add(command)


def get_command_by_alias(alias: str) -> Command:
    commands = list_commands()
    for command in commands:
        if command.alias == alias:
            return command
    raise ValueError(
        f"No command with alias {alias} found. Run kip list to see all commands or kip search to find a specific one."
    )


def list_commands() -> Commands:
    kip_files = list_kip_files()
    commands_per_file = (load_from_command_file(kip_file) for kip_file in kip_files)
    return set().union(*commands_per_file)


def remove_command(command: Command) -> None:
    kip_files = list_kip_files()
    for kip_file in kip_files:
        with persistent_command_set(kip_file) as commands:
            if command in commands:
                commands.remove(command)


def run_command(command: Command) -> None:
    subprocess.run(command.command, shell=True)


def search_command() -> Command:
    print("mocking of searching a command with string")
    first, *_ = list_commands()
    return first
