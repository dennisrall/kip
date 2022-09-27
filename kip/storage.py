import contextlib

import yaml

from kip.models import Command
from kip.lib import file_name


def load_from_command_file(command_file_name: file_name) -> set[Command]:
    with open(command_file_name) as command_file:
        dicts = yaml.safe_load(command_file)
    return {Command.from_dict(d) for d in dicts} if dicts else set()


def save_to_command_file(commands: set[Command], command_file_name: file_name) -> None:
    dicts = [command.to_dict() for command in commands]
    with open(command_file_name, 'w') as command_file:
        yaml.safe_dump(dicts, command_file)


@contextlib.contextmanager
def persistent_command_set(command_file_name: file_name) -> contextlib.AbstractContextManager[set[Command]]:
    commands = load_from_command_file(command_file_name)
    try:
        yield commands
    finally:
        save_to_command_file(commands, command_file_name)
