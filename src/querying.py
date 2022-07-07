from elasticsearch import Elasticsearch


def get_query_body(query_string: str) -> dict:
    """
    Converts given query string to basic query body for elasticsearch client
    :param query_string: the query string
    :return: dict posing as body for ES search
    """
    return {
        "query": {
            "query_string": {
                "query": query_string
            }
        }
    }


def search(client: Elasticsearch, index: str, query_string: str, size=20):
    return client.search(index=index, body=get_query_body(query_string), size=size)
