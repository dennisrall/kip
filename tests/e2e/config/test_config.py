import pathlib

import pytest
from pytest_mock import MockFixture
from typer.testing import CliRunner

import kip.config.storage
from kip.config.models import Config
from kip.main import app


@pytest.fixture
def fake_config() -> Config:
    return Config(["/tmp/dir/test-commands.yaml", "/tmp/another/dir/commands.yaml"])


@pytest.fixture(autouse=True)
def mock_config_file(fake_config: Config, mocker: MockFixture) -> None:
    mocker.patch.object(
        kip.config.storage, "load_config_file", return_value=fake_config
    )
    mocker.patch.object(kip.config.storage, "save_config_file")


def test_list_kip_files(cli_runner: CliRunner, fake_config: Config) -> None:
    result = cli_runner.invoke(app, ["config", "list"])
    assert result.exit_code == 0
    assert "Command files:" in result.stdout
    assert all(kip_file in result.stdout for kip_file in fake_config.kip_files)


def test_add_kip_file(
    fake_config: Config, cli_runner: CliRunner, tmp_path: pathlib.Path
) -> None:
    new_config_file = tmp_path / "commands.yaml"
    new_config_file.touch()
    result = cli_runner.invoke(app, ["config", "add", str(new_config_file)])
    assert result.exit_code == 0
    assert str(new_config_file) in fake_config.kip_files


def test_add_kip_file_file_exists(cli_runner: CliRunner) -> None:
    result = cli_runner.invoke(
        app, ["config", "add", "/tmp/this/file/does/not/exist.yaml"]
    )
    assert result.exit_code == 2
    assert "exist" in result.stdout


def test_add_kip_file_file_is_not_dir(
    cli_runner: CliRunner, tmp_path: pathlib.Path
) -> None:
    dir_to_add = tmp_path / "dir/"
    dir_to_add.mkdir()
    result = cli_runner.invoke(app, ["config", "add", str(dir_to_add)])
    assert result.exit_code == 2
    assert "directory" in result.stdout


def test_add_kip_file_relative_path_is_converted_to_absolute(
    fake_config: Config, cli_runner: CliRunner
) -> None:
    cur_file = pathlib.Path(__file__).relative_to(pathlib.Path().absolute())
    result = cli_runner.invoke(app, ["config", "add", str(cur_file)])
    assert result.exit_code == 0
    assert str(cur_file.absolute()) in fake_config.kip_files


def test_remove_kip_file(fake_config: Config, cli_runner: CliRunner) -> None:
    result = cli_runner.invoke(app, ["config", "remove", "/tmp/dir/test-commands.yaml"])
    assert result.exit_code == 0
    assert fake_config.kip_files == ["/tmp/another/dir/commands.yaml"]


def test_remove_kip_file_relative_path_is_converted_to_absolute(
    fake_config: Config, cli_runner: CliRunner
) -> None:
    cur_file = pathlib.Path(__file__)
    fake_config.kip_files.append(str(cur_file))
    assert len(fake_config.kip_files) == 3
    rel_path_to_cur_file = cur_file.relative_to(pathlib.Path().absolute())
    result = cli_runner.invoke(app, ["config", "remove", str(rel_path_to_cur_file)])
    assert result.exit_code == 0
    assert len(fake_config.kip_files) == 2
