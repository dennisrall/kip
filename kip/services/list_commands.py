from kip.models.command import Command
from kip.services.config import get_kip_file
from kip.storage.command_file import load_from_command_file


def list_commands(kip_file=get_kip_file()) -> set[Command]:
    return load_from_command_file(kip_file)
