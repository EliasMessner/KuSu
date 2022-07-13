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


def get_improved_query_body(query_string: str) -> dict:
    """
    inserts given query string into elasticsearch query body so that results are ranked highest if they match the phrase
    exactly. If they don't match exactly, they are still ranked in a more-matches-is-better approach.
    :param query_string:
    :return:
    """
    return {
        "query": {
            "bool": {
                "should": [
                    {
                        "match": {
                            "content": {
                                "query": query_string
                            }
                        }
                    },
                    {
                        "match": {
                            "content": {
                                "query": query_string,
                                "operator": "and"
                            }
                        }
                    },
                    {
                        "match_phrase": {
                            "content": {
                                "query": query_string,
                                "boost": 2
                            }
                        }
                    }
                ]
            }
        }
    }


def search(client: Elasticsearch, index: str, query_string: str, size=20):
    return client.search(index=index, body=get_improved_query_body(query_string), size=size)
