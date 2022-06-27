from src.services.command_file import save_to_command_file, load_from_command_file


def test_load_from_command_file(command_list, command_file):
    save_to_command_file(command_list, command_file)
    assert load_from_command_file(command_file) == command_list

