from hypothesis import given

from models import Command
from strategies import command


def test_command_to_dict(ls_command: Command, ls_command_dict: dict[str, str]) -> None:
    assert ls_command.to_dict() == ls_command_dict


def test_command_from_dict(ls_command_dict: dict[str, str], ls_command: Command) -> None:
    assert Command.from_dict(ls_command_dict) == ls_command


@given(command_=command)
def test_command_to_from_dict(command_: Command) -> None:
    assert Command.from_dict(command_.to_dict()) == command_
