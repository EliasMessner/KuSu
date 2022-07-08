from elasticsearch import Elasticsearch

from indexing import index_documents
from constants import default_index_name, docs_dir
from main_controller import prompt_confirm


def main():
    """
    Creates the default index and gives explanatory console output. If an index with that name already exists,
    prompts the user if it should be overwritten.
    """
    client = Elasticsearch([{"host": "localhost", "port": 9200}])
    if client.indices.exists(index=default_index_name):
        if not prompt_confirm(f"Index named {default_index_name} already exists. Should it be overwritten?"):
            quit()
        else:
            client.indices.delete(index=default_index_name)
    index_documents(client=client, index_name=default_index_name, docs_dir=docs_dir)


if __name__ == "__main__":
    main()
