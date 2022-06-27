from src.services.command_file import load_from_command_file
from src.services.remove_command import remove_command


def test_remove_existing_command(command1, command2, command_file):
    remove_command(command1, command_file)
    assert load_from_command_file(command_file) == {command2}


def test_remove_non_existing_command(command_set, command3, command_file):
    remove_command(command3, command_file)
    assert load_from_command_file(command_file) == command_set
