import subprocess

from hypothesis import given

from kip.services import add_command, run_command, remove_command
from kip.storage import load_from_command_file
from kip.storage import persistent_command_set
from tests.strategies import command, command_set
from tests.strategies import non_empty_command_set


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


def test_run_command_mock(ls_command, mocker):
    run_mock = mocker.Mock()
    mocker.patch.object(subprocess, "run", run_mock)
    run_command(ls_command)
    run_mock.assert_called_with(ls_command.command, shell=True)


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
