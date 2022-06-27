from src.command import Command

from src.services.command_file import persistent_command_set
from src.util.types import file_name


def add_command(command: Command, command_file_name: file_name) -> None:
    with persistent_command_set(command_file_name) as commands:
        commands.add(command)
