from hypothesis import given

from kip.services.command_file import load_from_command_file
from kip.services.remove_command import remove_command
from tests.strategies import non_empty_command_set


@given(commands=non_empty_command_set)
def test_remove_existing_command(command_file_factory, commands):
    command_file = command_file_factory(commands)
    command_to_remove = commands.pop()
    remove_command(command_to_remove, command_file)
    assert load_from_command_file(command_file) == commands - {command_to_remove}


@given(commands=non_empty_command_set)
def test_remove_non_existing_command(command_file_factory, commands):
    command_to_remove = commands.pop()
    command_file = command_file_factory(commands)
    remove_command(command_to_remove, command_file)
    assert load_from_command_file(command_file) == commands
