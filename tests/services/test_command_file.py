from src.services.command_file import load_from_command_file, persistent_command_set


def test_load_from_command_file(command_set, command_file):
    assert load_from_command_file(command_file) == command_set


def test_persistent_command_list(command_set, command_file, command1, command2):
    with persistent_command_set(command_file) as commands:
        commands.remove(command2)
    assert load_from_command_file(command_file) == {command1}
