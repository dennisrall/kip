from hypothesis import given

from kip.services.add_command import add_command
from kip.storage.command_file import load_from_command_file
from tests.strategies import command, command_set


@given(command_to_add=command, commands=command_set)
def test_add_command(command_file_factory, command_to_add, commands):
    command_file = command_file_factory(commands)
    add_command(command_to_add, command_file)
    assert load_from_command_file(command_file) == commands | {command_to_add}


@given(duplicated_command=command, commands=command_set)
def test_add_duplicated_command(command_file_factory, duplicated_command, commands):
    commands |= {duplicated_command}
    command_file = command_file_factory(commands)
    add_command(duplicated_command, command_file)
    assert load_from_command_file(command_file) == commands
