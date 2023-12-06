# OCRSegment

Binarize, normalize and segment PDF or image files, output PageXML files.

Output made for [OCR4all](https://github.com/OCR4all/OCR4all) / [LAREX](https://github.com/OCR4all/LAREX). 

Uses [Ocropy ocropus-nlbin](https://github.com/ocropus-archive/DUP-ocropy) and [Kraken](https://github.com/mittagessen/kraken).

## Setup

### Base

#### Clone project

```bash
git clone https://github.com/Jatzelberger/OCRSegment
```

#### Install dependencies

```bash
pip install -r pagesegment/requirements.txt
```

### Setup DUP-ocropy (Binarize/Normalize)

Ocropy requires Python 2 (recommended: 2.7.18)

#### Install 2.7.18 via PyENV

```bash
pyenv install 2.7.18
```

#### Download ocropy somewhere

```bash
git clone https://github.com/ocropus-archive/DUP-ocropy
```

#### Change config.cfg

Change `ocropy_path = /path/to/DUP-ocropy-master/` to new path

#### Install ocropy dependencies

```bash
PYENV_VERSION=2.7.18 pip2 install -r /path/to/DUP-ocropy-master/requirements.txt
```

### Setup Kraken (Segmentation)

Recommended (and working) PyEnv Version: `3.10.13`

#### Install 3.10.13 via PyENV

```bash
$ pyenv install 3.10.13
```

#### Install Kraken

Version 4.3.10 seems to work fine (4.3.0 get a lot of overlapping polygon errors and requires pytorch-lightning==1.6.0)

```bash
$ PYENV_VERSION=3.10.13 pip3 install kraken==4.3.10
```

Upgrade Shapely version (2.0.2):

```bash
$ PYENV_VERSION=3.10.13 pip3 install Shapely==2.0.2
```
## Config
`config.cfg` file located in _OCRSegment_ root folder:
```cfg
[OCROPY]
# path to ocropy root (absolute)
ocropy_path = /path/to/DUP-ocropy-master/

# python argument, e.g. python2
python = PYENV_VERSION=2.7.18 python

# additional ocropus nlbin args (see https://github.com/ocropus-archive/DUP-ocropy/blob/master/ocropus-nlbin)
additional_args =

[KRAKEN]
# environment argument, leave empty if kraken is installed globally
environment = PYENV_VERSION=3.10.13

# additional kraken args (see https://kraken.re/main/advanced.html)
additional_args =
```

## Usage
### Parse Module
Parsing PDF and image files to .png files sorted by book names:
```bash
python3 ocrsegment parse INPUT_PATH BOOKS_PATH ORIG_DIR [-p] [-i] [--dpi=<dpi>] [--size=<size>] [--orig=<orig>]
```
- `INPUT_PATH`: Absolute path to input files: input_folder/<book_name>/(file.pdf/.<image_suffix>).
- `BOOKS_PATH`: Absolute output path containing parsed and processed books.
- `ORIG_DIR`: Name of folder in BOOKS_PATH/<book_name>/ORIG_DIR/ containing parsed original files.
- `--dpi=<dpi>`: DPI for PDF scanning. [default: 300]
- `--size=<size>`: Height for output .png files, to keep original size, do not specify.
- `--orig=<orig>`: Additional suffix for original files, e.g. '.orig' for 0001.orig.png.
- `-p`: Parse PDF files to usable .png file.
- `-i`: Parse image files to usable .png file.

#### Example
```bash
python3 ocrsegment parse /home/usr/Documents/filein/ /home/usr/Documents/booksout/ input -ip --size=1000
```
Result:
```
From:
filein
└─ book1
│  └─ something.pdf
└─ book2
   │  0001.tif
   └─ 0002.jpg
  
To:
booksout
└─ book1
│  └─ input
│     │  0001.png
│     │  0002.png
│     └─ ...
└─ book2
   └─ input
      │  0001.png
      │  0002.png
      └─ ...
```

### NLBIN Module
Binarize and normalize image files with OCRopy's _ocropus-nlbin_ module:
```bash
python3 ocrsegment nlbin BOOKS_PATH ORIG_DIR PROCESSED_DIR
```
- `BOOKS_PATH`: Absolute output path containing parsed and processed books.
- `ORIG_DIR`: Name of folder in BOOKS_PATH/<book_name>/ORIG_DIR/ containing parsed original files.
- `PROCESSED_DIR`: Name of folder in BOOKS_PATH/<book_name>/PROCESSED_DIR/ containing processed original files.

#### Example
```bash
python3 .\ocrsegment nlbin /home/usr/Documents/booksout/ input processing
```
Result:
```
booksout
└─ book1
│  └─ input
│     │  0001.png
│     │  0002.png
│     └─ ...
│  └─ processing
│     │  0001.bin.png
│     │  0001.nrm.png
│     │  0002.bin.png
│     └─ ...
└─ book2
   └─ input
      └─ ...
   └─ processing
      └─ ...      
```

### Segment Module
Segment image files with Kraken, outputs (probably invalid!) PageXML files:
```bash
python3 ocrsegment segment BOOKS_PATH PROCESSED_DIR KRAKEN_MODEL (--bin | --nrm) [--bl] [--suffix=<suffix>]
```
- `BOOKS_PATH`: Absolute output path containing parsed and processed books.
- `PROCESSED_DIR`: Name of folder in BOOKS_PATH/<book_name>/PROCESSED_DIR/ containing processed original files.
- `KRAKEN_MODEL`: Absolute path to Kraken segmentation model.
- `(--bin | --nrm)`: Use either binarized .bin.png files or normalized .nrm.png for segmentation.
- `--bl`: Use baseline module for segmentation.
- `--suffix=<suffix>`: PageXML suffix including leading dot. [default: .xml]
#### Example
```
python3 ocrsegment segment /home/usr/Documents/booksout/ processing /path/to/model.mlmodel --bin --bl
```
Result:
```
booksout
└─ book1
   └─ input
      └─ ...
   └─ processing
      │  0001.bin.png
      │  0001.nrm.png
      |  0001.xml
      │  0002.bin.png
      └─ ...
```

### Fix Module
Fixes invalid PageXML files and changes @imageFilename tag from absolute image paths to flat filenames
```bash
python3 ocrsegment fix BOOKS_PATH PROCESSED_DIR [-s] [-n] [--suffix=<suffix>] [--orig=<orig>]
```
- `BOOKS_PATH`: Absolute output path containing parsed and processed books.
- `PROCESSED_DIR`: Name of folder in BOOKS_PATH/<book_name>/PROCESSED_DIR/ containing processed original files.
- `-s`: Fix: make PageXML file valid for official scheme.
- `-n`: Fix: change @imageFilename tag in PageXML file from absolute path to <filename><orig>.png.
- `--suffix=<suffix>`: PageXML suffix including leading dot. [default: .xml]
- `--orig=<orig>`: Additional suffix for original files, e.g. '.orig' for 0001.orig.png.
#### Example
```bash
python3 ocrsegment fix /home/usr/Documents/booksout/ processing -sn
```
Results in valid PageXML files and:
```
0001.xml
...
<Page imageFilename="0001.png" imageHeight="2318" imageWidth="1669">
...
```

### Help Module
```bash
python3 ocrsegment -h
```

```
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
```

## Fixes

### Ocropy

#### Module _tkinter not found
- uninstall python2.7.18: `pyenv uninstall 2.7.18`
- install tkinter-dev: `sudo apt install tk-dev`
- reinstall python2.7.18: `pyenv install 2.7.18`

## ZPD
Developed at [Zentrum für Philologie und Digitalität](https://www.uni-wuerzburg.de/en/zpd/startseite/) at the [Julius-Maximilians-Universität of Würzburg](https://www.uni-wuerzburg.de/en/home/)