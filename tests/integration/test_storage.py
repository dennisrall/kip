import pathlib

from conftest import initialize_kip_files_type
from hypothesis import given
from integration.strategies import command, command_set, non_empty_command_set

from kip.base.models import Command
from kip.base.storage import (
    load_from_command_file,
    persistent_command_set,
    save_to_command_file,
)


@given(commands=command_set)
def test_load_commands_from_file(
    initialize_kip_files: initialize_kip_files_type, commands: set[Command]
) -> None:
    (kip_file,) = initialize_kip_files(commands)
    assert load_from_command_file(kip_file) == commands


def test_load_empty_command_file(tmp_path: pathlib.Path) -> None:
    command_file = tmp_path / "commands.yaml"
    command_file.touch()
    assert load_from_command_file(command_file) == set()


@given(commands=command_set)
def test_safe_and_load_commands(
    initialize_kip_files: initialize_kip_files_type, commands: set[Command]
) -> None:
    (kip_file,) = initialize_kip_files(set())
    save_to_command_file(commands, kip_file)
    assert load_from_command_file(kip_file) == commands


@given(command_to_add=command, commands=command_set)
def test_persistent_command_set_add(
    initialize_kip_files: initialize_kip_files_type,
    command_to_add: Command,
    commands: set[Command],
) -> None:
    (kip_file,) = initialize_kip_files(commands)
    with persistent_command_set(kip_file) as persistent_commands:
        persistent_commands.add(command_to_add)
    assert load_from_command_file(kip_file) == commands | {command_to_add}


@given(commands=non_empty_command_set)
def test_persistent_command_set_remove(
    initialize_kip_files: initialize_kip_files_type, commands: set[Command]
) -> None:
    (kip_file,) = initialize_kip_files(commands)
    command_to_remove = commands.pop()
    with persistent_command_set(
        kip_file,
    ) as persistent_commands:
        persistent_commands.remove(command_to_remove)
    assert load_from_command_file(
        kip_file,
    ) == commands - {command_to_remove}
