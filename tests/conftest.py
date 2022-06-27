import pytest

from src.command import Command
from src.services.command_file import save_to_command_file


@pytest.fixture
def command1():
    return Command("ls Downloads", "list downloaded files", "list-downloads")


@pytest.fixture
def command2():
    return Command("echo 'Hello World'!", "greet the world", "greet-world")


@pytest.fixture
def command3():
    return Command("cd Documents", "change into documents directory", "cd-docs")


@pytest.fixture
def command_list(command1, command2):
    return [command1, command2]


@pytest.fixture
def command_file(tmp_path):
    command_file = tmp_path / "commands.json"
    command_file.touch()
    return command_file
