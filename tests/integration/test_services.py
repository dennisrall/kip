import pathlib
import subprocess

import pytest
from conftest import initialize_kip_files_type, mock_cwd_type
from hypothesis import given
from integration.strategies import command, command_set, non_empty_command_set
from pytest_mock import MockerFixture

from kip.base.models import Command, Commands
from kip.base.services import (
    add_command,
    get_command_by_alias,
    list_commands,
    remove_command,
    run_command,
)
from kip.base.storage import load_from_command_file


@given(command_to_add=command, commands=command_set)
def test_add_command(
    initialize_kip_files: initialize_kip_files_type,
    command_to_add: Command,
    commands: Commands,
    mock_cwd: mock_cwd_type,
) -> None:
    (kip_file,) = initialize_kip_files(commands)
    mock_cwd(kip_file.parent)
    add_command(command_to_add)
    assert list_commands() == commands | {command_to_add}


@given(duplicated_command=command, commands=command_set)
def test_add_duplicated_command(
    initialize_kip_files: initialize_kip_files_type,
    duplicated_command: Command,
    commands: Commands,
    mock_cwd: mock_cwd_type,
) -> None:
    commands |= {duplicated_command}
    (kip_file,) = initialize_kip_files(commands)
    mock_cwd(kip_file.parent)
    add_command(duplicated_command)
    assert list_commands() == commands


@given(commands=non_empty_command_set)
def test_add_command_with_same_alias(
    initialize_kip_files: initialize_kip_files_type,
    commands: Commands,
    mock_cwd: mock_cwd_type,
) -> None:
    (kip_file,) = initialize_kip_files(commands)
    mock_cwd(kip_file.parent)
    command_ = commands.pop()
    command_with_same_alias = Command("ls", "test", command_.alias)
    add_command(command_with_same_alias)
    assert list_commands() == commands - {command_} | {command_with_same_alias}


@given(commands=non_empty_command_set)
def test_get_command_by_alias(
    initialize_kip_files: initialize_kip_files_type, commands: Commands
) -> None:
    initialize_kip_files(commands)
    command_ = commands.pop()
    assert get_command_by_alias(command_.alias) == command_


@given(commands=non_empty_command_set)
def test_get_command_by_alias_non_existing(
    initialize_kip_files: initialize_kip_files_type, commands: Commands
) -> None:
    command_ = commands.pop()
    initialize_kip_files(commands)
    with pytest.raises(ValueError):
        get_command_by_alias(command_.alias)


@given(commands=command_set)
def test_list_commands(
    initialize_kip_files: initialize_kip_files_type, commands: Commands
) -> None:
    (kip_file,) = initialize_kip_files(commands)
    assert list_commands() == load_from_command_file(kip_file)


@given(commands=non_empty_command_set)
def test_remove_existing_command(
    initialize_kip_files: initialize_kip_files_type, commands: Commands
) -> None:
    initialize_kip_files(commands)
    command_to_remove = commands.pop()
    remove_command(command_to_remove)
    assert list_commands() == commands - {command_to_remove}


@given(commands=non_empty_command_set)
def test_remove_non_existing_command(
    initialize_kip_files: initialize_kip_files_type, commands: Commands
) -> None:
    command_to_remove = commands.pop()
    initialize_kip_files(commands)
    remove_command(command_to_remove)
    assert list_commands() == commands


def test_run_command_mock(ls_command: Command, mocker: MockerFixture) -> None:
    run_mock = mocker.Mock()
    mocker.patch.object(subprocess, "run", run_mock)
    run_command(ls_command)
    run_mock.assert_called_with(ls_command.command, shell=True)
