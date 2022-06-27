from hypothesis import given
from hypothesis.strategies import text, composite, lists

from src.command import decode_commands_from_json, Command, encode_commands_to_json


@composite
def command(draw):
    command_str, description, alias = draw(text()), draw(text()), draw(text())
    return Command(command_str, description, alias)


@composite
def command_list(draw):
    return draw(lists(command()))


@given(command_list())
def test_encode_decode(commands):
    assert decode_commands_from_json(encode_commands_to_json(commands)) == commands
