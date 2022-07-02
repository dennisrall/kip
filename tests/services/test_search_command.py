from hypothesis import given

from src.services.search_command import search_command
from tests.strategies import non_empty_command_set


@given(commands=non_empty_command_set)
def test_search_command(command_file_factory, commands):
    command_file = command_file_factory(commands)
    command_to_search = commands.pop()
    search_str = command_to_search.alias
    assert command_to_search in search_command(search_str, command_file)
