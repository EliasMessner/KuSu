import datetime
import os
import timeit
from pprint import pprint

import xmltodict
from elasticsearch import Elasticsearch
from tqdm import tqdm

from lido_handler import parse_lido_entry
from constants import textfiles_muenchen, textfiles_westmuensterland


def xml_to_dict(filepath: str):
    """
    Takes an XML file containing a single lido entry and converts it to a ready-to-index dictionary.
    :param filepath: the filepath of the xml file
    :return: a dictionary representing the xml file
    """
    with open(filepath, 'r') as file:
        xml_data = file.read()
    lido_dict = xmltodict.parse(xml_data)
    parsed_dict = parse_lido_entry(lido_dict, os.path.basename(filepath))
    return parsed_dict


def get_all_xml_filepaths(dir_path):
    """
    returns a list of filepaths of all xml files in a given directory path
    :param dir_path: path to the directory
    :return: list of filepaths
    """
    directory = os.fsencode(dir_path)
    return [os.path.join(dir_path, os.fsdecode(file))
            for file in os.listdir(directory)
            if os.fsdecode(file).endswith(".xml")]


def index_documents(client: Elasticsearch, index_name: str, docs_dir: str, overwrite=True, console_output=False) -> list[str]:
    """
    Indexes all xml documents in dir_path. If overwrite is set to True (default), it deletes the index first (if the index
    exists) and creates a new one. Otherwise, it adds seen data to the existing index.
    :param docs_dir: relative path containing the xml files.
    :param client: Elasticsearch client with active connection
    :param index_name: the name of the index
    :param overwrite: boolean value to specify if the index should be overwritten or added to
    :param console_output: if set to True, the response for each indexed document is printed to the console. This might
    significantly increase runtime.
    :return: a list of strings, containing a response string for each indexed document
    """
    start = timeit.default_timer()
    if overwrite:
        client.indices.delete(index=index_name, ignore=[400, 404])  # "ignore" is in case index does not exist
    xml_filepaths = get_all_xml_filepaths(docs_dir)
    responses = []
    for filepath in tqdm(xml_filepaths):  # tqdm is for progress bar in console
        data_dict = xml_to_dict(filepath)
        data_dict["colors"] = read_image_data_if_exists(data_dict["img_id"])
        res = client.index(index=index_name, body=data_dict, id=data_dict['filename'])
        if console_output:
            print(res)
        responses.append(res)
    stop = timeit.default_timer()
    print(f"Done indexing {len(xml_filepaths)} documents into index '{index_name}'. Took {str(datetime.timedelta(seconds=stop-start)).split('.')[0]}.")
    return responses


def read_image_data_if_exists(img_id):
    """
    Checks if a txt file exists, where the colors of the image to this file were extracted to. Such a file is assumed
    to have the same name as the img_id of the lido entry
    :param img_id: the img_id, should correspond with the file name where colors are stored
    """
    if img_id.startswith("PT_"):
        text_files_dir = textfiles_muenchen
    elif img_id.startswith("HM-"):
        text_files_dir = textfiles_westmuensterland
    else:
        return ""
    txt_filename = img_id + ".txt"
    file_path = os.path.join(text_files_dir, txt_filename)
    if not os.path.exists(file_path):
        return ""
    with open(file_path, encoding="ISO-8859-1") as file:  # this encoding works for umlaut in 'grün'
        colors = file.read().strip()
    return colors
