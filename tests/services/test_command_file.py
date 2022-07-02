from hypothesis import given

from src.services.command_file import load_from_command_file, persistent_command_set
from tests.strategies import command_set, non_empty_command_set


@given(commands=command_set)
def test_load_from_command_file(command_file_factory, commands):
    command_file = command_file_factory(commands)
    assert load_from_command_file(command_file) == commands


def test_load_empty_command_file(tmp_path):
    command_file = tmp_path / "commands.json"
    command_file.touch()
    assert load_from_command_file(command_file) == set()


@given(commands=non_empty_command_set)
def test_remove_from_persistent_command_set(command_file_factory, commands):
    command_file = command_file_factory(commands)
    with persistent_command_set(command_file) as persistent_commands:
        removed_command = persistent_commands.pop()
    assert load_from_command_file(command_file) == commands - {removed_command}


@given(commands=non_empty_command_set)
def test_add_to_persistent_command_set(command_file_factory, commands):
    command_to_add = commands.pop()
    command_file = command_file_factory(commands)
    with persistent_command_set(command_file) as persistent_commands:
        persistent_commands.add(command_to_add)
    assert load_from_command_file(command_file) == commands | {command_to_add}
