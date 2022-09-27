from kip.models.command import Command
from kip.services.list_commands import list_commands


def get_command_by_alias(alias: str) -> Command:
    commands = list_commands()
    for command in commands:
        if command.alias == alias:
            return command
    raise ValueError(
        f"No command with alias {alias} found. Run kip list to see all commands or kip search to find a specific one.")
