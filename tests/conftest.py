import pathlib
from collections.abc import Callable, Sequence

import pytest
from pytest import TempPathFactory
from pytest_mock import MockerFixture, MockFixture

import kip.base.services
import kip.config.storage
from kip.base.models import Command, Commands
from kip.base.storage import save_to_command_file
from kip.config import Config

initialize_kip_files_type = Callable[[Commands], Sequence[pathlib.Path]]

mock_cwd_type = Callable[[pathlib.Path], None]


@pytest.fixture(scope="session")
def test_config() -> Config:
    return Config([])


@pytest.fixture(autouse=True)
def mock_config_file(test_config: Config, mocker: MockFixture) -> None:
    mocker.patch.object(
        kip.config.storage, "load_config_file", return_value=test_config
    )
    mocker.patch.object(kip.config.storage, "save_config_file")


@pytest.fixture(scope="module")
def mock_cwd(module_mocker: MockerFixture) -> mock_cwd_type:
    def mock_cwd_(new_cwd: pathlib.Path) -> None:
        module_mocker.patch.object(kip.base.services, "get_cwd", return_value=new_cwd)

    return mock_cwd_


@pytest.fixture(scope="session")
def initialize_kip_files(
    tmp_path_factory: TempPathFactory, test_config: Config
) -> initialize_kip_files_type:
    def initialize_kip_files_(
        *initial_commands_sequence: Commands,
    ) -> Sequence[pathlib.Path]:
        kip_files = []
        for initial_commands in initial_commands_sequence:
            kip_file = tmp_path_factory.mktemp("test") / "commands.json"
            kip_file.touch(exist_ok=True)
            save_to_command_file(initial_commands, kip_file)
            kip_files.append(kip_file)
        test_config.kip_files = [str(kip_file) for kip_file in kip_files]
        return kip_files

    return initialize_kip_files_


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
