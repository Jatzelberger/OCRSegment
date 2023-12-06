from pathlib import Path

from docopt import docopt

from ocr_services import parse_handler, ocropy_handler, kraken_handler, fix_handler

_version = "OCRSegment v1.0"

_docstring = """
OCRSegment Command Line Tool:
Binarize, normalize and segment PDF or image files, output PageXML files.
Output made for OCR4all. Uses Ocropy ocropus-nlbin and Kraken

Usage:
    ocrsegment (-h | --help)
    ocrsegment (-v | --version)
    ocrsegment parse INPUT_PATH BOOKS_PATH ORIG_DIR [-p] [-i] [--dpi=<dpi>] [--size=<size>] [--orig=<orig>]
    ocrsegment nlbin BOOKS_PATH ORIG_DIR PROCESSED_DIR
    ocrsegment segment BOOKS_PATH PROCESSED_DIR KRAKEN_MODEL (--bin | --nrm) [--bl] [--suffix=<suffix>]
    ocrsegment fix BOOKS_PATH PROCESSED_DIR [-s] [-n] [--suffix=<suffix>] [--orig=<orig>]

Arguments:
    parse                   Parse PDF or image files to usable .png files.
    nlbin                   Normalize and binarize original png files with ocropy.
    segment                 Segment processed images with kraken and pagexml output.
    fix                     Fix kraken output (see flags).
    INPUT_PATH              Absolute path to input files: input_folder/<book_name>/(file.pdf/.<image_suffix>).
    BOOKS_PATH              Absolute output path containing parsed and processed books.
    ORIG_DIR                Name of folder in BOOKS_PATH/<book_name>/ORIG_DIR/ containing parsed original files.
    PROCESSED_DIR           Name of folder in BOOKS_PATH/<book_name>/PROCESSED_DIR/ containing processed original files.
    KRAKEN_MODEL            Absolute path to Kraken segmentation model.
    
Options:
    -h --help               Show this screen.
    -v --version            Show version.
    -p                      Parse PDF files to usable .png file.
    -i                      Parse image files to usable .png file.
    -s                      Fix: make PageXML file valid for official scheme.
    -n                      Fix: change @imageFilename tag in PageXML file from absolute path to <filename><orig>.png.
    --bin                   Use binarized .bin.png files for segmentation.
    --nrm                   Use normalized .nrm.png files for segmentation.
    --bl                    Use baseline module for segmentation.
    --orig=<orig>           Additional suffix for original files, e.g. '.orig' for 0001.orig.png.
    --dpi=<dpi>             DPI for PDF scanning. [default: 300]
    --size=<size>           Height for output .png files, to keep original size, do not specify.
    --suffix=<suffix>       PageXML suffix including leading dot. [default: .xml]
    
GitHub:
    https://github.com/Jatzelberger/OCRSegment
    
ZPD:
    Developed at \"Zentrum für Philologie und Digitalität\" at the \"Julius-Maximilians-Universität of Würzburg\".
"""


def parse(argv: list) -> None:
    """
    Parsing cli arguments with docopt and runs selected methods

    :param argv: output from sys.argv
    :return: None
    """
    args = docopt(docstring=_docstring, version=_version, argv=argv[1:])
    # print(args)

    if args.get('parse'):
        parse_handler(
            in_path=Path(args.get('INPUT_PATH')),
            books_path=Path(args.get('BOOKS_PATH')),
            orig_dir=args.get('ORIG_DIR'),
            pdf_mode=args.get('-p'),
            image_mode=args.get('-i'),
            dpi=int(args.get('--dpi')),
            size=None if args.get('--size') is None else int(args.get('--size')),
            orig_suffix=args.get('--orig'),
        )

    if args.get('nlbin'):
        ocropy_handler(
            books_path=Path(args.get('BOOKS_PATH')),
            orig_dir=args.get('ORIG_DIR'),
            processed_dir=args.get('PROCESSED_DIR'),
        )

    if args.get('segment'):
        kraken_handler(
            books_path=Path(args.get('BOOKS_PATH')),
            processed_dir=args.get('PROCESSED_DIR'),
            kraken_model=Path(args.get('KRAKEN_MODEL')),
            use_bin=args.get('--bin'),
            baseline=args.get('--bl'),
            suffix=args.get('--suffix'),
        )

    if args.get('fix'):
        fix_handler(
            books_path=Path(args.get('BOOKS_PATH')),
            processed_dir=args.get('PROCESSED_DIR'),
            scheme_mode=args.get('-s'),
            filename_mode=args.get('-n'),
            xml_suffix=args.get('--suffix'),
            orig_suffix=args.get('--orig'),
        )
