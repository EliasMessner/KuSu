"""
Wrapper for single function call.
"""
from elasticsearch import Elasticsearch

from indexing import index_documents
from constants import docs_dir, boost_default, boost_2, get_settings


def main():
    print("Establishing Connection...")
    client = Elasticsearch([{"host": "localhost", "port": 9200}])
    print("Done.")

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
    for index_name, conf_body in get_run_configurations():
        if client.indices.exists(index_name):
            if overwrite_if_exists:
                client.indices.delete(index=index_name)
                print(f"Overwriting index '{index_name}'.")
            else:
                continue
        client.indices.create(index=index_name, body=conf_body)
        index_documents(client=client, index_name=index_name, docs_dir=docs_dir)


def get_run_configurations():
    """
    Returns a list of run configurations that are useful for evaluation.
    Each element of the list is a tuple, the first element being a descriptive name of the run configuration (which is
    also the name of the index that ought to use this configuration). The second element is the settings dict that
    can be passed as body parameter when creating a new index with the configuration.
    """
    configurations = []  # [(name_of_configuration, body), ...]
    for boost in [boost_default, boost_2]:
        for analyzer in ["german_analyzer", "german_light_analyzer"]:
            for similarity in ["BM25", "boolean"]:
                if boost == boost_default:
                    boost_name = "boost_default"
                elif boost == boost_2:
                    boost_name = "boost_2"
                else:
                    raise RuntimeError("Boost unknown.")
                name = "-".join([boost_name, analyzer, similarity])
                name = name.lower()
                body = get_settings(boost=boost, similarity=similarity, analyzer=analyzer)
                configurations.append((name, body))
    return configurations


if __name__ == "__main__":
    main()
