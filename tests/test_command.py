from hypothesis import given

from src.command import decode_commands_from_json, encode_commands_to_json
from tests.strategies import command_set


@given(command_set)
def test_encode_decode(commands):
    assert decode_commands_from_json(encode_commands_to_json(commands)) == commands
