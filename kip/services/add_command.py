from kip.command import Command

from kip.services.command_file import persistent_command_set
from kip.util.types import file_name


def add_command(command: Command, command_file_name: file_name) -> None:
    with persistent_command_set(command_file_name) as commands:
        commands.add(command)
