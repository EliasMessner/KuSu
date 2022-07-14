from elasticsearch import Elasticsearch

from constants import get_all_search_fields


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


def get_improved_query_body(query_string: str) -> dict:
    """
    inserts given query string into elasticsearch query body so that results are ranked highest if they match the phrase
    exactly. If they don't match exactly, they are still ranked in a more-matches-is-better approach.
    :param query_string:
    :return:
    """
    body = {
        "query": {
            "bool": {
                "should": [
                    {
                        "multi_match": {
                            "query": query_string,
                            "fields": get_all_search_fields()
                        }
                    },
                    {
                        "multi_match": {
                            "query": query_string,
                            "fields": get_all_search_fields(),
                            "operator": "and"
                        }
                    }
                ]
            }
        }
    }
    for search_field in get_all_search_fields():
        body["query"]["bool"]["should"].append(
            {
                "match_phrase": {
                    search_field: {
                        "query": query_string,
                        "boost": 2
                    }
                }
            }
        )
    return body


def search(client: Elasticsearch, index: str, query_string: str, size=20):
    return client.search(index=index, body=get_query_body(query_string), size=size)


def get_default_client(url, password):
    if url == "localhost":
        return Elasticsearch([{"host": "localhost", "port": 9200}])
    return Elasticsearch([url],
                         http_auth=("elastic", password),
                         port=9243)
