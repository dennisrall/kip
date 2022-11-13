import pathlib
from collections.abc import Callable

import pytest
from pytest import TempPathFactory

from kip.base.models import Command
from kip.base.storage import save_to_command_file

command_file_factory_type = Callable[[set[Command]], pathlib.Path]


@pytest.fixture(scope="session")
def command_file_factory(
    tmp_path_factory: TempPathFactory,
) -> command_file_factory_type:
    def create_command_file(initial_commands: set[Command]) -> pathlib.Path:
        command_file = tmp_path_factory.mktemp("test") / "commands.json"
        command_file.touch(exist_ok=True)
        save_to_command_file(initial_commands, command_file)
        return command_file

    return create_command_file


@pytest.fixture(scope="session")
def ls_command() -> Command:
    return Command("ls -l", "list files in the current directory", "ls-test")


@pytest.fixture(scope="session")
def ls_command_dict() -> dict[str, str]:
    return {
        "command": "ls -l",
        "description": "list files in the current directory",
        "alias": "ls-test",
    }
