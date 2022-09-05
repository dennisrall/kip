import fire

from kip.cli.user_input import user_input, get_choice, confirm
from kip.command import Command
from kip.config.read_config import get_kip_file
from kip.services.add_command import add_command
from kip.services.command_file import load_from_command_file
from kip.services.remove_command import remove_command
from kip.services.run_command import run_command
from kip.services.search_command import search_command

UNSET = object()


class KipCli:

    def add(self, command: str = UNSET, description: str = UNSET, alias: str = UNSET):
        if command is UNSET:
            command = user_input("Enter a command to save: ")
        if description is UNSET:
            description = user_input("Enter a description for the provided command: ")
        if alias is UNSET:
            alias = user_input("Enter a alias for the command (optional): ")
        command_to_add = Command(command, description, alias)
        add_command(command_to_add, get_kip_file())

    def remove(self, search_str: str):
        commands = search_command(search_str, get_kip_file())
        if len(commands) == 0:
            print("No matching command found")
            print("Aborting...")
        command_to_remove = get_choice(commands)
        print(f"Remove {command_to_remove}")
        if confirm():
            remove_command(command_to_remove, get_kip_file())

    def search(self, search_str: str):
        commands = search_command(search_str, get_kip_file())
        for command in commands:
            print(command)

    def list(self):
        commands = load_from_command_file(get_kip_file())
        for command in commands:
            print(command)

    def run(self, search_str):
        commands = search_command(search_str, get_kip_file())
        if len(commands) == 0:
            print("No matching command found")
            print("Aborting...")
            return
        command_to_execute = get_choice(commands)

        print(command_to_execute.command)
        if confirm():
            run_command(command_to_execute)


def main():
    fire.Fire(KipCli)
