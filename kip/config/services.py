import pathlib

from kip.config.storage import persistent_config


def add_kip_file(kip_file: pathlib.Path) -> None:
    with persistent_config() as config:
        kip_file_str = str(kip_file)
        if kip_file_str not in config.kip_files:
            config.kip_files.append(kip_file_str)


def remove_kip_file(kip_file: pathlib.Path) -> None:
    with persistent_config() as config:
        try:
            config.kip_files.remove(str(kip_file))
        except ValueError:
            pass


def list_kip_files() -> list[pathlib.Path]:
    with persistent_config() as config:
        return [pathlib.Path(kip_file) for kip_file in config.kip_files]


def get_kip_file_for_path(path: pathlib.Path) -> pathlib.Path:
    kip_file_parents_dir = {kip_file.parent: kip_file for kip_file in list_kip_files()}
    for directory in (path, *path.parents):
        if directory in kip_file_parents_dir:
            return kip_file_parents_dir[directory]
    raise ValueError(
        f"No kip file in path {path}. Run 'kip config list' to list all available kip files."
        f"Run 'kip config add' to add a kip file"
    )
