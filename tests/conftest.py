import pytest

from src.services.command_file import save_to_command_file


@pytest.fixture(scope="session")
def command_file_factory(tmp_path_factory):
    def create_command_file(initial_commands):
        command_file = tmp_path_factory.mktemp("test") / "commands.json"
        command_file.touch(exist_ok=True)
        save_to_command_file(initial_commands, command_file)
        return command_file

    return create_command_file
