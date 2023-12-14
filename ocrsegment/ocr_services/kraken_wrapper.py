import os
from pathlib import Path

from .helper import is_empty, read_config
from .constants import CONFIG_FILE, CONFIG


def kraken_handler(
        books_path: Path,
        processed_dir: str,
        kraken_model: Path,
        use_bin: bool = True,
        baseline: bool = True,
        suffix: str = '.xml'
) -> None:
    """
    Handles Kraken API

    :param books_path: path to books root
    :param processed_dir: directory name containing .bin.png and .nrm.png image files
    :param kraken_model: path to kraken model
    :param use_bin: use .bin.png files, else use .nrm.png files
    :param baseline: use kraken baseline module
    :param suffix: output xml suffix
    :return:
    """
    if not kraken_model.exists():
        print("! Kraken model not found")
        return None

    if is_empty(books_path):
        print("! No books found")
        return None

    cfg = read_config(CONFIG_FILE, CONFIG.KRAKEN)
    path = books_path.joinpath('**', processed_dir, f'*{".bin" if use_bin else ".nrm"}.png')
    call = f'{cfg["environment"]} kraken -x -I "{path}" -o {suffix} segment {"-bl " if baseline else ""}--model "{kraken_model}" {cfg.get("additional_args")}'
    print(call)
    try:
        os.system(call)
    except Exception as e:
        print('! Error: ' + str(e))

    print("Changing suffix of files...")
    files = books_path.glob(f'**/{processed_dir}/*{suffix}')
    for file in files:
        new_name = file.name.replace(f'{".bin" if use_bin else ".nrm"}{suffix}', f'{suffix}')
        os.rename(file, file.parent.joinpath(new_name))
