from enum import Enum
from pathlib import Path

# absolute path to config file when tool is called from __main__.py
CONFIG_FILE = Path('config.cfg').absolute()

# xml suffixes
XML_SUFFIX = '.xml'  # default xml suffix
XML_BIN_SUFFIX = '.bin.xml'  # kraken suffix, when .bin files are used for segmentation
XML_NRM_SUFFIX = '.nrm.xml'  # kraken suffix, when .nrm files are used for segmentation


class CONFIG(Enum):
    """
    Config file tags
    """
    OCROPY = 'OCROPY',
    KRAKEN = 'KRAKEN',


class IMAGE_SUFFIX(Enum):
    """
    Image file suffixes
    """
    PNG = '.png'
    JPG = '.jpg'
    JPEG = '.jpeg'
    TIF = '.tif'
