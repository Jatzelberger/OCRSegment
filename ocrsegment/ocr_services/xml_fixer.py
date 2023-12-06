from pathlib import Path

from lxml import etree


def pagexml_fix(
        books_path: Path,
        processed_dir: str,
        xml_suffix: str = '.xml',
) -> None:
    """
    Making pagexml files valid

    :param books_path: Absolute output path containing parsed and processed books
    :param processed_dir: directory name containing .bin.png and .nrm.png image files
    :param xml_suffix: suffix of xml files
    :return: None
    """
    files = sorted(books_path.glob(f'**/{processed_dir}/*{xml_suffix}'))
    for fp in files:
        # get root element from file
        root = etree.parse(fp.as_posix()).getroot()
        ro = list()

        # change @custom to @type attribute
        for region in root.findall(".//{*}TextRegion"):
            custom = region.get("custom")
            if not custom:
                continue
            _type = custom.replace('structure {type:', '')
            _type = _type.replace(';}', '')
            region.set('type', _type)

        for idx, text_region in enumerate(root.findall('.//{*}TextRegion')):
            # set new text_region id
            new_id = f"r_{str(idx).zfill(4)}"
            text_region.set("id", new_id)
            ro.append(f"r_{str(idx).zfill(4)}")

            # fix negative coords
            for line in text_region.findall("./{*}TextLine"):
                line_coords = line.find("./{*}Coords")
                line_points = line_coords.get("points")
                if "-" in line_points:
                    line_points = line_points.replace("-", "")
                    line_coords.set("points", line_points)

        # create reading order element
        page_elem = root.find("./{*}Page")
        reading_order_element = etree.Element("ReadingOrder")
        ordered_group_element = etree.SubElement(reading_order_element, "OrderedGroup")
        ordered_group_element.set("id", "g0")
        for idx, elem in enumerate(ro):
            region_ref_index_elem = etree.SubElement(ordered_group_element, "RegionRefIndexed")
            region_ref_index_elem.set("index", str(idx))
            region_ref_index_elem.set("regionRef", elem)
        page_elem.insert(0, reading_order_element)

        # save changes
        with fp.open("w") as outfile:
            outfile.write(etree.tostring(root, encoding="unicode", pretty_print=True))


def filename_fix(
        books_path: Path,
        processed_dir: str,
        xml_suffix: str = '.xml',
        orig_suffix: str = ''
) -> None:
    """
    Fixing @imageFilename tag from absolute path to <xml_name><orig_suffix>.png

    :param books_path: Absolute output path containing parsed and processed books
    :param processed_dir: directory name containing .bin.png and .nrm.png image files
    :param xml_suffix: suffix of xml files
    :param orig_suffix: additional suffix for imageFilename
    :return: None
    """
    files = sorted(books_path.glob(f'**/{processed_dir}/*{xml_suffix}'))
    for file in files:
        img_name = file.name.replace(xml_suffix, f'{orig_suffix}.png')
        root = etree.parse(file.as_posix()).getroot()
        if root is None:
            print('Error parsing file' + file.as_posix())
            continue
        page = root.find(".//{*}Page")
        page.set('imageFilename', img_name)
        with open(file.as_posix(), "w") as outfile:
            outfile.write(etree.tostring(root, encoding="unicode", pretty_print=True))


def fix_handler(
        books_path: Path,
        processed_dir: str,
        scheme_mode: bool,
        filename_mode: bool,
        xml_suffix: str = '.xml',
        orig_suffix: str = ''
) -> None:
    """
    Handles fixes on xml files

    :param books_path: Absolute output path containing parsed and processed books
    :param processed_dir: directory name containing .bin.png and .nrm.png image files
    :param scheme_mode: fix pagexml scheme
    :param filename_mode: fix imageFilename tag
    :param xml_suffix: suffix of xml files
    :param orig_suffix: additional suffix for imageFilename
    :return: None
    """
    if filename_mode:
        print("Fixing @imageFilename tags...")
        filename_fix(
            books_path=books_path,
            processed_dir=processed_dir,
            xml_suffix=xml_suffix,
            orig_suffix=orig_suffix,
        )
    if scheme_mode:
        print("Fixing pagexml scheme...")
        pagexml_fix(
                books_path=books_path,
                processed_dir=processed_dir,
                xml_suffix=xml_suffix,
            )