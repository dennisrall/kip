import pathlib

import pytest
from pytest_mock import MockFixture

import kip.config.storage
from kip.config.models import Config
from kip.config.services import get_kip_file_for_path


@pytest.fixture
def fake_config() -> Config:
    return Config(
        ["/commands.yaml", "/dir/commands.yaml", "/dir/another/dir/commands.yaml"]
    )


@pytest.fixture(autouse=True)
def mock_config_file(fake_config: Config, mocker: MockFixture) -> None:
    mocker.patch.object(
        kip.config.storage, "load_config_file", return_value=fake_config
    )
    mocker.patch.object(kip.config.storage, "save_config_file")


@pytest.mark.parametrize(
    ("path", "kip_file"),
    [
        ("/", "/commands.yaml"),
        ("/dir/", "/dir/commands.yaml"),
        ("/dir/another/dir/", "/dir/another/dir/commands.yaml"),
        ("/should/default/to/root/file", "/commands.yaml"),
        ("/dir/another/other/dir", "/dir/commands.yaml"),
        ("/dir/another/dir/in/dir/", "/dir/another/dir/commands.yaml"),
        ("/this/is/a/file.yaml", "/commands.yaml"),
    ],
)
def test_get_kip_file_for_path(path: str, kip_file: str, fake_config: Config) -> None:
    assert get_kip_file_for_path(pathlib.Path(path)) == pathlib.Path(kip_file)


def test_get_kip_file_for_path_error(fake_config: Config) -> None:
    fake_config.kip_files = ["/dir/commands.yaml", "/dir/another/dir/commands.yaml"]
    with pytest.raises(ValueError):
        get_kip_file_for_path(pathlib.Path("/no/matching/dir"))
