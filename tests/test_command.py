from hypothesis import given
import hypothesis.strategies as st

from src.command import decode_commands_from_json, Command, encode_commands_to_json


@st.composite
def command(draw):
    command_str, description, alias = draw(st.text()), draw(st.text()), draw(st.text())
    return Command(command_str, description, alias)


@st.composite
def command_list(draw):
    return draw(st.lists(command()))


@given(command_list())
def test_encode_decode(commands):
    assert decode_commands_from_json(encode_commands_to_json(commands)) == commands
