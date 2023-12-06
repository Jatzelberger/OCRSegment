import os
from pathlib import Path

from .helper import mkdir_if_not_exists, is_empty, read_config
from .constants import CONFIG_FILE, CONFIG


def ocropy_handler(
        books_path: Path,
        orig_dir: str,
        processed_dir: str,
) -> None:
    """
    Handles orcopy nlbin input

    :param books_path: path to image file
    :param orig_dir: directory name containing original image files
    :param processed_dir: output directory, will be generated if it does not exist
    :return: None
    """
    if is_empty(books_path):
        print("! No books found")
        return None

    cfg = read_config(CONFIG_FILE, CONFIG.OCROPY)
    print(cfg)

    books = sorted(books_path.glob('*/'))
    for book in books:
        processed_path = books_path.joinpath(book.name, processed_dir)
        mkdir_if_not_exists(processed_path)
        files = list(sorted(book.glob(f'{orig_dir}/*.png')))
        if not files:
            print("! Book is empty")
            continue
        call = f'{cfg.get("python")} "{cfg.get("ocropy_path")}ocropus-nlbin" -n "{book.joinpath("*")}" -o "{processed_path}" --maxskew 0 {cfg.get("additional_args")}'
        print(call)
        try:
            os.system(call)
        except Exception as e:
            print('! Error with book: ' + book.as_posix())
            print(e)
