from src.services.add_command import add_command
from src.services.command_file import load_from_command_file, save_to_command_file


def test_add_new_command(command3, command_list, command_file):
    save_to_command_file(command_list, command_file)
    add_command(command3, command_file)
    assert load_from_command_file(command_file) == [*command_list, command3]


def test_add_duplicated_command(command2, command_list, command_file):
    save_to_command_file(command_list, command_file)
    add_command(command2, command_file)
    assert load_from_command_file(command_file) == command_list
