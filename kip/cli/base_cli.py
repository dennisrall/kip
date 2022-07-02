import fire
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from kip.command import Command
from kip.services.add_command import add_command
from kip.services.search_command import search_command
from kip.services.command_file import load_from_command_file
from kip.config.read_config import get_kip_file


class KipCli:

    def add(self, command: str, description: str, alias: str = ""):
        c = Command(command, description, alias)
        add_command(c, get_kip_file())

    def search(self, search_str: str):
        commands = search_command(search_str, get_kip_file())
        print(commands)

    def list(self):
        commands = load_from_command_file(get_kip_file())
        for command in commands:
            print(command)


def main():
    fire.Fire(KipCli)