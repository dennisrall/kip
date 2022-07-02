from kip.command import Command
from kip.services.command_file import persistent_command_set
from kip.util.types import file_name


def remove_command(command: Command, command_file: file_name):
    with persistent_command_set(command_file) as commands:
        if command in commands:
            commands.remove(command)
