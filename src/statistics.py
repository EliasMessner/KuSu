from constants import docs_dir
from indexing import get_all_xml_filepaths


def print_statistics(xml_filepaths):
    lengths = []
    for filepath in xml_filepaths:
        with open(filepath, 'r') as file:
            xml_data = file.read()
        length = len(xml_data)
        lengths.append(length)
    print(f"Parsed {len(lengths)} length values.")
    print(f"Longest = {max(lengths)}")
    print(f"shortest = {min(lengths)}")
    print(f"Average = {sum(lengths) / len(lengths)}")


if __name__ == "__main__":
    print("ALL:")
    print_statistics(get_all_xml_filepaths(docs_dir))
    print("\nMKG:")
    print_statistics([filepath for filepath in get_all_xml_filepaths(docs_dir) if filepath.split('/')[-1].startswith("atomized_mkg")])
    print("\ndigiporta:")
    print_statistics([filepath for filepath in get_all_xml_filepaths(docs_dir) if filepath.split('/')[-1].startswith("atomized_digiPorta")])
    print("\nLampensammlung:")
    print_statistics([filepath for filepath in get_all_xml_filepaths(docs_dir) if filepath.split('/')[-1].startswith("PT_")])