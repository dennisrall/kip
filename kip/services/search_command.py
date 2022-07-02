from thefuzz import process

from kip.command import Command
from kip.services.command_file import load_from_command_file
from kip.util.types import file_name


def search_command(search_str: str, command_file_name: file_name) -> list[Command]:
    commands = load_from_command_file(command_file_name)
    command_reprs = [repr(command) for command in commands]
    matching_commands = process.extract(search_str, command_reprs)
    return [eval(command_repr) for command_repr, _ in matching_commands]
