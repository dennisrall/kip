import pathlib

from kip.config.storage import persistent_config


def add_config_file(kip_file: pathlib.Path) -> None:
    with persistent_config() as config:
        kip_file_str = str(kip_file)
        if kip_file_str not in config.kip_files:
            config.kip_files.append(kip_file_str)


def remove_config_file(kip_file: pathlib.Path) -> None:
    with persistent_config() as config:
        try:
            config.kip_files.remove(str(kip_file))
        except ValueError:
            pass


def list_kip_files() -> list[pathlib.Path]:
    with persistent_config() as config:
        return [pathlib.Path(kip_file) for kip_file in config.kip_files]
