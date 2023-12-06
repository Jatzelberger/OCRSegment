from pathlib import Path
from typing import Any
import configparser
import os

from .constants import CONFIG


def read_config(fp: Path, tag: CONFIG) -> dict:
    """
    returns content of config file by tag

    :param fp: absolute path to config file
    :param tag: config script to be parsed
    :return: dict of content
    """
    cfg = configparser.ConfigParser()
    cfg.read(fp.as_posix())
    return dict(cfg[tag.name])


def mkdir_if_not_exists(dp: Path) -> bool:
    """
    Creates directory from path, if it does not exist. Returns success

    :param dp: path to directory
    :return: success
    """
    if not dp.exists() or not dp.is_dir():
        dp.mkdir(parents=True, exist_ok=True)
        return True
    return False


def is_empty(directory: Path) -> bool:
    """
    Checks if a directory is empty or not

    :param directory: path to directory
    :return: boolean value
    """
    with os.scandir(directory) as it:
        if any(it):
            return False
    return True


def or_else(value: Any | None, default: Any) -> Any:
    """
    returns content of value if value is not None, else return default value

    :param value: value to be checked
    :param default: default value if value is None
    :return: value or default
    """
    return default if value is None else value
