"""
Wrapper for single function call.
"""
from elasticsearch import Elasticsearch

from constants import docs_dir
from es_helper import prepare_client_dialog
from indexing import index_documents
from indexing import get_index_configurations


def main():
    client = prepare_client_dialog()
    print("Creating Indices...")
    create_all_indices(client, overwrite_if_exists=True)
    print("Done.")


def create_all_indices(client: Elasticsearch, overwrite_if_exists: bool):
    """
    Creates all indices returned by get_all_run_configurations and fills each of them with data by calling
    indexing.index_documents.
    :param client: ElasticSearch client with active connection.
    :param overwrite_if_exists: if True, overwrite an index if such an index name already exists. If False, omit
        existing index.
    """
    for index_name, conf_body in get_index_configurations():
        if client.indices.exists(index_name):
            if overwrite_if_exists:
                client.indices.delete(index=index_name)
                print(f"Overwriting index '{index_name}'.")
            else:
                continue
        client.indices.create(index=index_name, body=conf_body)
        index_documents(client=client, index_name=index_name, docs_dir=docs_dir)


if __name__ == "__main__":
    main()
