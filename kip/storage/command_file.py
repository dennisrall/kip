import contextlib

import more_itertools

from kip.models.command import Command, decode_commands_from_json, encode_commands_to_json
from kip.util.types import file_name


def load_from_command_file(command_file_name: file_name) -> set[Command]:
    with open(command_file_name) as command_file:
        lines = command_file.readlines()
        if not lines:
            return set()
        command_str = more_itertools.first(lines)
    return decode_commands_from_json(command_str)


def save_to_command_file(commands: set[Command], command_file_name: file_name) -> None:
    commands_str = encode_commands_to_json(commands)
    with open(command_file_name, 'w') as command_file:
        command_file.write(commands_str)


@contextlib.contextmanager
def persistent_command_set(command_file_name: file_name) -> contextlib.AbstractContextManager[Command]:
    commands = load_from_command_file(command_file_name)
    try:
        yield commands
    finally:
        save_to_command_file(commands, command_file_name)
