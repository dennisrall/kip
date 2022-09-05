from kip.models.command import Command
from kip.services.config import get_kip_file
from kip.storage.command_file import persistent_command_set


def add_command(command: Command, kip_file=get_kip_file()) -> None:
    with persistent_command_set(kip_file) as commands:
        commands.add(command)
