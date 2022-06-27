from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Command:
    command: str
    description: str
    alias: str


def decode_commands_from_json(json_str: str) -> list[Command]:
    return Command.schema().loads(json_str, many=True)


def encode_commands_to_json(commands: list[Command]) -> str:
    return Command.schema().dumps(commands, many=True)
