import shutil
from pathlib import Path

import fitz
from PIL import Image

from .helper import or_else, mkdir_if_not_exists, is_empty
from .constants import IMAGE_SUFFIX


def resize_image(image: Path, height: int) -> None:
    """
    Resizes an image and overrides old file

    :param image: path to image
    :param height: new height in pixels. Keeps aspect ratio
    :return: nothing
    """
    with Image.open(image) as img:
        original_width, original_height = img.size
        aspect_ratio = original_width / original_height
        new_width = int(height * aspect_ratio)
        resized = img.resize((new_width, height), Image.LANCZOS)
    resized.save(image)


def image_to_png(image: Path, out_dir: Path, height: int | None = None, suffix: str | None = None) -> Path:
    """
    Copies an image of .png, .jpg, .jpeg or .tif to output dir, changes its type to .png. Resize image if specified

    :param image: path to image file
    :param out_dir: output directory, will be generated if it does not exist
    :param height: rescale each image to fixed height in pixels. Keep original size if None
    :param suffix: suffix for output files: <page_number><suffix>.png, e.g '.orig'
    :return: path to copied and parsed image file
    """
    mkdir_if_not_exists(out_dir)

    if not is_empty(out_dir):
        print('! Image overridden: Output directory is not empty')

    file_name = image.name
    if not image.as_posix().endswith('.png'):  # image type has to be changed
        img = Image.open(image)
        for sfix in [x.value for x in IMAGE_SUFFIX]:
            file_name = file_name.replace(sfix, '.png')
        out_path = out_dir.joinpath(file_name.replace('.png', f'{or_else(suffix, "")}.png'))
        img.save(Path(out_path))
    else:  # file's suffix is already .png
        out_path = out_dir.joinpath(file_name.replace('.png', f'{or_else(suffix, "")}.png'))
        shutil.copy(image, out_path)
    if height is not None:
        resize_image(out_path, height)
    return out_path


def pdf_to_png(pdf: Path, out_dir: Path, dpi: int = 300, height: int | None = None, suffix: str | None = None) -> Path:
    """
    Converts a PDF file to a set of .png image files: <page_number>.png

    :param pdf: path to PDF file
    :param out_dir: output directory, will be generated if it does not exist
    :param dpi: pdf scan dpi
    :param height: rescale each image to fixed height in pixels. Keep original size if None
    :param suffix: suffix for output files: <page_number><suffix>.png, e.g '.orig'
    :return: path to output folder
    """
    if not (pdf.exists() or pdf.is_file()):
        raise FileNotFoundError
    mkdir_if_not_exists(out_dir)

    if not is_empty(out_dir):
        print('! PDF skipped: Output directory is not empty')
        return out_dir

    fp = fitz.open(pdf)
    for i, page in enumerate(fp):
        pixmap = page.get_pixmap(dpi=dpi)
        outfile = out_dir.joinpath(f'{(i + 1):04d}{or_else(suffix, "")}.png')
        pixmap.save(outfile)
        if height is not None:
            resize_image(outfile, height)
    return out_dir


def parse_handler(
        in_path: Path,
        books_path: Path,
        orig_dir: str,
        pdf_mode: bool,
        image_mode: bool,
        dpi: int = 300,
        size: int | None = None,
        orig_suffix: str | None = None
) -> None:
    """
    Handles parse argument input

    :param in_path: Absolute path to input files: input_folder/<book_name>/(file.pdf/.<image_suffix>).
    :param books_path: Absolute output path containing parsed and processed books
    :param orig_dir: Name of folder in BOOKS_PATH/<book_name>/ORIG_DIR/ containing parsed original files.
    :param pdf_mode: Parse PDF files to usable .png file.
    :param image_mode: Parse image files to usable .png file.
    :param dpi: DPI for PDF scanning. [default: 300]
    :param size: Height for output .png files, to keep original size, do not specify.
    :param orig_suffix: Additional suffix for original files, e.g. '.orig' for 0001.orig.png.
    :return: None
    """
    mkdir_if_not_exists(books_path)  # create output path

    if pdf_mode:
        pdfs = in_path.glob('**/*.pdf')
        for pdf in pdfs:
            print(f'...Parsing PDF file: {pdf.as_posix()}')
            book_name = pdf.parent.name
            pdf_to_png(
                pdf=pdf,
                out_dir=books_path.joinpath(book_name, orig_dir),
                dpi=dpi,
                height=size,
                suffix=orig_suffix,
            )
    if image_mode:
        images = []
        for sfix in [x.value for x in IMAGE_SUFFIX]:
            images.extend(in_path.glob(f'**/*{sfix}'))
        for image in images:
            print(f'...Parsing Image file: {image.as_posix()}')
            book_name = image.parent.name
            image_to_png(
                image=image,
                out_dir=books_path.joinpath(book_name, orig_dir),
                height=size,
                suffix=orig_suffix,
            )
