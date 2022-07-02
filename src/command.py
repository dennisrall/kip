from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(unsafe_hash=True)
class Command:
    command: str
    description: str
    alias: str


def decode_commands_from_json(json_str: str) -> set[Command]:
    commands = Command.schema().loads(json_str, many=True)
    return set(commands)


def encode_commands_to_json(commands: set[Command]) -> str:
    return Command.schema().dumps(list(commands), many=True)
