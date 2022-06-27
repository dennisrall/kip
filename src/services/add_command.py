from src.command import Command

from src.services.command_file import load_from_command_file, save_to_command_file
from src.util.types import file_name


def add_command(command: Command, command_file_name: file_name) -> None:
    commands = load_from_command_file(command_file_name)
    if command not in commands:
        commands.append(command)
        save_to_command_file(commands, command_file_name)
