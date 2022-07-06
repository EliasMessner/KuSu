from xml.etree import ElementTree

from constants import docs_dir
from indexing import get_all_xml_filepaths


def print_statistics(xml_filepaths):
    lengths = []
    for filepath in xml_filepaths:
        length = get_raw_length(filepath)
        lengths.append(length)
    print(f"Parsed {len(lengths)} length values.")
    print(f"Longest = {max(lengths)}")
    print(f"shortest = {min(lengths)}")
    print(f"Average = {sum(lengths) / len(lengths)}")


def get_raw_length(xml_path):
    """
    Get raw length of the xml file, in number of characters.
    """
    with open(xml_path, 'r') as file:
        xml_data = file.read()
    length = len(xml_data)
    return length


def get_length_only_data(xml_path):
    """
    TODO: getting xml.etree.ElementTree.ParseError: unbound prefix, because xmlns is not defined.
     If this can be fixed, it would be a better length measure for xml files than get_raw_length.
    Return the length of all attribute strings and text string in the xml file concatenated.
    """
    all_data = ""
    dom = ElementTree.parse(xml_path)
    for d in dom.findall(".//{*}"):
        if d.text is not None:
            all_data += d.text
        for a in d.attrib:
            all_data += d.get(a, default="")
    return len(all_data)


if __name__ == "__main__":
    print("ALL:")
    print_statistics(get_all_xml_filepaths(docs_dir))
    print("\nMKG:")
    print_statistics([filepath for filepath in get_all_xml_filepaths(docs_dir) if filepath.split('/')[-1].startswith("atomized_mkg")])
    print("\ndigiporta:")
    print_statistics([filepath for filepath in get_all_xml_filepaths(docs_dir) if filepath.split('/')[-1].startswith("atomized_digiPorta")])
    print("\nLampensammlung:")
    print_statistics([filepath for filepath in get_all_xml_filepaths(docs_dir) if filepath.split('/')[-1].startswith("PT_")])