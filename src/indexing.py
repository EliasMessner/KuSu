import datetime
import os
import timeit
from pprint import pprint

import xmltodict
from elasticsearch import Elasticsearch
from tqdm import tqdm

from src.lido_handler import parse_lido_entry


def xml_to_dict(filepath: str):
    """
    Takes an XML file containing a single lido entry and converts it to a ready-to-index dictionary.
    :param filepath: the filepath of the xml file
    :return: a dictionary representing the xml file
    """
    with open(filepath, 'r') as file:
        xml_data = file.read()
    lido_dict = xmltodict.parse(xml_data)
    parsed_dict = parse_lido_entry(lido_dict)
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
        res = client.index(index=index_name, body=data_dict)
        if console_output:
            print(res)
        responses.append(res)
    stop = timeit.default_timer()
    print(f"Done indexing {len(xml_filepaths)} documents. Took {str(datetime.timedelta(seconds=stop-start)).split('.')[0]}.")
    return responses
