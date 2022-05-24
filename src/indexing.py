import datetime
import os
import timeit

import xmltodict
from elasticsearch import Elasticsearch
from tqdm import tqdm


def xml_to_dict(filepath):
    """
    Takes an XML file and converts it to a ready-to-index dictionary.
    :param filepath: the filepath of the xml file
    :return: a dictionary representing the Lido entry
    """
    with open(filepath, 'r') as file:
        xml_data = file.read()
    return xmltodict.parse(xml_data)


def index_documents(client: Elasticsearch, index_name: str, dir_path="../docs", overwrite=True, console_output=False) -> list[str]:
    """
    Indexes all xml documents in dir_path. If overwrite is set to True (default), it deletes the index first (if the index
    exists) and creates a new one. Otherwise, it adds seen data to the existing index.
    :param dir_path: relative path containing the xml files. Default is "../docs"
    :param client: Elasticsearch client with active connection
    :param index_name: the name of the index
    :param overwrite: boolean value to specify if the index should be overwritten or added to
    :param console_output: if set to True, the response for each indexed document is printed to the console. This might
    significantly increase runtime.
    :return: a list of strings, containing a response string for each indexed document
    """
    start = timeit.default_timer()
    assert client.ping()  # assert that the client is connected
    print("Client connected, starting indexing...")
    if overwrite:
        client.indices.delete(index=index_name, ignore=[400, 404])  # "ignore" is in case index does not exist
    directory = os.fsencode(dir_path)
    all_xml_files = [os.fsdecode(file) for file in os.listdir(directory) if os.fsdecode(file).endswith(".xml")]
    responses = []
    for filename in tqdm(all_xml_files):  # tqdm is for progress bar in console
        filepath = os.path.join(dir_path, filename)
        data_dict = xml_to_dict(filepath)
        res = client.index(index=index_name, body=data_dict)
        if console_output:
            print(res)
        responses.append(res)
    stop = timeit.default_timer()
    print(f"Done indexing {len(all_xml_files)} documents. Took {str(datetime.timedelta(seconds=stop-start)).split('.')[0]}.")
    return responses


if __name__ == "__main__":
    client = Elasticsearch([{"host": "localhost", "port": 9200}])
    indexing_responses = index_documents(client, "test-index")
    # pprint(indexing_responses)
