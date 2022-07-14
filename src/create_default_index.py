from getpass import getpass

from constants import default_index_name, docs_dir
from indexing import index_documents
from main_controller import prompt_confirm
import es_helper


def main():
    """
    Creates the default index and gives explanatory console output. If an index with that name already exists,
    prompts the user if it should be overwritten.
    """
    client = es_helper.prepare_client_dialog()
    if client.indices.exists(index=default_index_name):
        if not prompt_confirm(f"Index named {default_index_name} already exists. Should it be overwritten?"):
            quit()
        else:
            client.indices.delete(index=default_index_name)
    index_documents(client=client, index_name=default_index_name, docs_dir=docs_dir)


if __name__ == "__main__":
    main()
