import subprocess

import pytest
from conftest import command_file_factory_type
from hypothesis import given
from pytest_mock import MockerFixture

from kip.models import Command
from kip.services import (
    add_command,
    get_command_by_alias,
    list_commands,
    remove_command,
    run_command,
)
from kip.storage import load_from_command_file
from tests.strategies import command, command_set, non_empty_command_set


@given(command_to_add=command, commands=command_set)
def test_add_command(
    command_file_factory: command_file_factory_type,
    command_to_add: Command,
    commands: set[Command],
) -> None:
    command_file = command_file_factory(commands)
    add_command(command_to_add, command_file)
    assert load_from_command_file(command_file) == commands | {command_to_add}


@given(duplicated_command=command, commands=command_set)
def test_add_duplicated_command(
    command_file_factory: command_file_factory_type,
    duplicated_command: Command,
    commands: set[Command],
) -> None:
    commands |= {duplicated_command}
    command_file = command_file_factory(commands)
    add_command(duplicated_command, command_file)
    assert load_from_command_file(command_file) == commands


@given(commands=non_empty_command_set)
def test_add_command_with_same_alias(
    command_file_factory: command_file_factory_type, commands: set[Command]
) -> None:
    command_file = command_file_factory(commands)
    command_ = commands.pop()
    command_with_same_alias = Command("ls", "test", command_.alias)
    add_command(command_with_same_alias, command_file)
    assert load_from_command_file(command_file) == commands - {command_} | {
        command_with_same_alias
    }


@given(commands=non_empty_command_set)
def test_get_command_by_alias(
    command_file_factory: command_file_factory_type, commands: set[Command]
) -> None:
    command_file = command_file_factory(commands)
    command_ = commands.pop()
    assert get_command_by_alias(command_.alias, command_file) == command_


@given(commands=non_empty_command_set)
def test_get_command_by_alias_non_existing(
    command_file_factory: command_file_factory_type, commands: set[Command]
) -> None:
    command_ = commands.pop()
    command_file = command_file_factory(commands)
    with pytest.raises(ValueError):
        get_command_by_alias(command_.alias, command_file)


@given(commands=command_set)
def test_list_commands(
    command_file_factory: command_file_factory_type, commands: set[Command]
) -> None:
    command_file = command_file_factory(commands)
    assert list_commands(command_file) == load_from_command_file(command_file)


@given(commands=non_empty_command_set)
def test_remove_existing_command(
    command_file_factory: command_file_factory_type, commands: set[Command]
) -> None:
    command_file = command_file_factory(commands)
    command_to_remove = commands.pop()
    remove_command(command_to_remove, command_file)
    assert load_from_command_file(command_file) == commands - {command_to_remove}


@given(commands=non_empty_command_set)
def test_remove_non_existing_command(
    command_file_factory: command_file_factory_type, commands: set[Command]
) -> None:
    command_to_remove = commands.pop()
    command_file = command_file_factory(commands)
    remove_command(command_to_remove, command_file)
    assert load_from_command_file(command_file) == commands


def test_run_command_mock(ls_command: Command, mocker: MockerFixture) -> None:
    run_mock = mocker.Mock()
    mocker.patch.object(subprocess, "run", run_mock)
    run_command(ls_command)
    run_mock.assert_called_with(ls_command.command, shell=True)
