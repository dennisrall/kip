import os

from kip.models.command import Command


def run_command(command: Command) -> None:
    os.system(command.command)
