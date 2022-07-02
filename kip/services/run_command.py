import os

from kip.command import Command


def run_command(command: Command) -> None:
    os.system(command.command)
