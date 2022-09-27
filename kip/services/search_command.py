from kip.models.command import Command
from kip.services.config import get_kip_file
from kip.services.list_commands import list_commands


def search_command(kip_file=get_kip_file()) -> Command:
    print("mocking of searching a command with string")
    first, *_ = list_commands(kip_file=kip_file)
    return first
