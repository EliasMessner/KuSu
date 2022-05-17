import os
import xmltodict
from elasticsearch import Elasticsearch
from pprint import pprint


def xml_to_dict(filepath):
    """
    Takes an XML file containing a single Lido entry, and converts it to a ready-to-index dictionary.
    :param filepath: the filepath of the xml file
    :return: a dictionary representing the Lido entry
    """
    with open(filepath, 'r') as file:
        xml_data = file.read()
    return xmltodict.parse(xml_data)


def index_documents(client: Elasticsearch, index_name: str, overwrite=True) -> list[str]:
    """
    Indexes all xml documents in ../docs. If overwrite is set to True (default), it deletes the index first (if the index
    exists) and creates a new one. Otherwise, it adds seen data to the existing index.
    :param client: Elasticsearch client with active connection
    :param index_name: the name of the index
    :param overwrite: boolean value to specify if the index should be overwritten or added to
    :return: a list of strings, containing a response string for each indexed document
    """
    assert client.ping()  # assert that the client is connected
    if overwrite:
        client.indices.delete(index=index_name, ignore=[400, 404])  # "ignore" is in case index does not exist
    dir_path = "../docs"
    directory = os.fsencode(dir_path)
    responses = []
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".xml"):
            filepath = os.path.join(dir_path, filename)
            data_dict = xml_to_dict(filepath)
            res = client.index(index=index_name, body=data_dict)
            print(res)
            responses.append(res)
    return responses


if __name__ == "__main__":
    client = Elasticsearch([{"host": "localhost", "port": 9200}])
    responses = index_documents(client, "test-index")
    pprint(responses)
