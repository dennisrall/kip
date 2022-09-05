from typing import TypeVar

from more_itertools import first
import readline


def user_input(prompt: str) -> str:
    return input(prompt)


def confirm() -> bool:
    c = user_input("[y/n]: ")
    return c.lower() in ('', 'y', 'yes')


T = TypeVar('T')


def get_choice(choices: list[T]) -> T:
    len_choices = len(choices)
    if len_choices == 0:
        raise ValueError("Cannot choose element from empty list")
    if len_choices == 1:
        return first(choices)
    for index, item in enumerate(choices, start=1):
        print(f"[{index}] {str(item)}")
    choice_str = user_input(f"Enter a number from 1 - {len_choices}: ")
    try:
        choice = int(choice_str)
    except ValueError:
        print("Please enter a number")
        return get_choice(choices)
    if not (1 <= choice <= len_choices):
        print(f"Please enter a number from 1 - {len_choices}")
        return get_choice(choices)
    return choices[choice - 1]
