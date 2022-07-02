from hypothesis import given

from src.services.search_command import search_command
from tests.strategies import non_empty_command_set, command_set


@given(commands=command_set)
def test_search_command(command_file_factory, ls_command, commands):
    commands.add(ls_command)
    command_file = command_file_factory(commands)
    assert ls_command in search_command("list", command_file)
