from hypothesis import given

from models import Command
from storage import load_from_command_file, save_to_command_file, persistent_command_set
from strategies import command_set, command, non_empty_command_set


@given(commands=command_set)
def test_load_commands_from_file(command_file_factory, commands: set[Command]):
    command_file = command_file_factory(commands)
    assert load_from_command_file(command_file) == commands


def test_load_empty_command_file(tmp_path):
    command_file = tmp_path / "commands.yaml"
    command_file.touch()
    assert load_from_command_file(command_file) == set()


@given(commands=command_set)
def test_safe_and_load_commands(command_file_factory, commands: set[Command]):
    command_file = command_file_factory(set())
    save_to_command_file(commands, command_file)
    assert load_from_command_file(command_file) == commands


@given(command_to_add=command, commands=command_set)
def test_persistent_command_set_add(command_file_factory, command_to_add: Command, commands: set[Command]):
    command_file = command_file_factory(commands)
    with persistent_command_set(command_file) as persistent_commands:
        persistent_commands.add(command_to_add)
    assert load_from_command_file(command_file) == commands | {command_to_add}


@given(commands=non_empty_command_set)
def test_persistent_command_set_remove(command_file_factory, commands: set[Command]):
    command_file = command_file_factory(commands)
    command_to_remove = commands.pop()
    with persistent_command_set(command_file) as persistent_commands:
        persistent_commands.remove(command_to_remove)
    assert load_from_command_file(command_file) == commands - {command_to_remove}
