from xml.etree import ElementTree
import matplotlib.pyplot as plt
from tqdm import tqdm

from constants import docs_dir
from indexing import get_all_xml_filepaths


def main():
    all_xml_filepaths = get_all_xml_filepaths(docs_dir)
    mkg_filepaths = \
        [filepath for
         filepath in
         get_all_xml_filepaths(docs_dir) if
         filepath.split('/')[-1].startswith("atomized_mkg")]
    westmuensterland_filepaths = \
        [filepath for
         filepath in
         get_all_xml_filepaths(docs_dir) if
         filepath.split('/')[-1].startswith("atomized_westmuensterland")]
    digiporta_filepaths = \
        [filepath for
         filepath in
         get_all_xml_filepaths(docs_dir) if
         filepath.split('/')[-1].startswith("PT_")]

    response = "ALL:\n" \
               + get_statistics_string(get_all_xml_filepaths(docs_dir)) \
               + "\nMKG:" \
               + get_statistics_string(mkg_filepaths) \
               + "\nLampensammlung:" \
               + get_statistics_string(westmuensterland_filepaths) \
               + "\ndigiporta:" \
               + get_statistics_string(digiporta_filepaths)
    print(response)

    paths_list = [all_xml_filepaths, mkg_filepaths, westmuensterland_filepaths, digiporta_filepaths]
    names = ["All", "MKG", "Westmünsterland", "München"]

    data = [get_lengths(paths) for paths in paths_list]
    fig, ax = plt.subplots()
    ax.set_title("Distribution of Document Lengths")
    ax.boxplot(data)
    plt.xticks(ticks=range(1, len(names)+1), labels=names)
    plt.show()
    fig.savefig("../plots/distr_of_doc_lengths.pdf")


def plot_bar(data):
    plt.bar(range(len(data)), list(data.values()), align='center')
    plt.xticks(range(len(data)), list(data.keys()))
    plt.show()


def get_statistics_string(xml_filepaths):
    scores = get_statistics(xml_filepaths)
    return f"Parsed {scores['counted']} length values.\n" \
           f"Longest = {scores['max']}\n" \
           f"shortest = {scores['min']}\n" \
           f"Average = {scores['avg']}\n"


def get_statistics(xml_filepaths):
    lengths = get_lengths(xml_filepaths)
    return {"counted": len(lengths),
            "max": max(lengths),
            "min": min(lengths),
            "avg": sum(lengths) / len(lengths)}


def get_lengths(xml_filepaths):
    lengths = []
    for filepath in tqdm(xml_filepaths):
        length = len(remove_all_tags(filepath))
        lengths.append(length)
    return lengths


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


def remove_all_tags(xml_path) -> str:
    """
    Removes all tags of an xml file and returns the remaining characters as string
    """
    no_tags = ""
    with open(xml_path, 'r') as xml_file:
        inside_tag = False
        for c in xml_file.read():
            if c in ['<', '>']:
                inside_tag = not inside_tag
                continue
            if not inside_tag:
                no_tags += c
    return no_tags


if __name__ == "__main__":
    main()
