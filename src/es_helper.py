from getpass import getpass
from elasticsearch import Elasticsearch

from constants import bcolors, only_disjunction, combined_operators


def get_query_body_only_disjunction(query_string: str) -> dict:
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


def get_query_body_combined_operators(query_string: str) -> dict:
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
                            "operator": "and",
                            "boost": 2
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


def search(client: Elasticsearch, index: str, query_string: str, query_mode: str, size=20):
    if query_mode == only_disjunction:
        body = get_query_body_only_disjunction(query_string)
    elif query_mode == combined_operators:
        body = get_query_body_combined_operators(query_string)
    else:
        raise ValueError(f"Unknown query mode {query_mode}")
    return client.search(index=index, body=body, size=size)


def prepare_client_dialog():
    """
    Performs a console dialog asking for URL, port, user and password, and attempts to connect to the specified
    ES-cluster with the given credentials.
    If the connection fails, return False.
    Otherwise, return the connected Elasticsearch client.
    """
    print("Please enter the credentials of an Elasticsearch cluster to connect to.")
    credentials = prompt_for_credentials()
    client = Elasticsearch([credentials["url"]],
                           http_auth=(credentials["user"], credentials["password"]),
                           port=credentials["port"])
    if not client.ping():
        print(f"{bcolors.WARNING}Client not connected.{bcolors.ENDC}")
        print(f"Client Info: {str(client.info())}")
        return False
    print("Client connected successfully.")
    return client


def prompt_for_credentials():
    url = input("URL: ")
    port = input("Port: ")
    user = input("User: ")
    password = getpass()
    return {"url": url,
            "port": port,
            "user": user,
            "password": password}


def get_all_search_fields():
    return [
        key
        for key, value
        in get_settings(similarity="boolean", analyzer="german_analyzer")["mappings"]["properties"].items()
        if value.get("enabled", True)
    ]


def get_settings(similarity: str, analyzer: str) -> dict:
    """
    Constructs a dict for elasticsearch settings
    :param similarity: a string specifying the similarity measure to be used, for example BM25.
    :param analyzer: a string specifying the analyzer to be used.
    """
    assert analyzer in ["german_analyzer", "german_light_analyzer"]
    return {
        "settings": {
            "analysis": {

                "filter": {
                    "german_stop": {
                        "type": "stop",
                        "stopwords": "_german_"
                    },
                    "german_stemmer": {
                        "type": "stemmer",
                        "language": "german"
                    },
                    "german_light_stemmer": {
                        "type": "stemmer",
                        "language": "light_german"
                    }
                    # TODO maybe also use german2, minimal_german stemmers https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-stemmer-tokenfilter.html
                },

                "analyzer": {
                    "german_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": [
                            "lowercase",
                            "german_stop",
                            "german_normalization",
                            "german_stemmer"
                        ]
                    },
                    "german_light_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": [
                            "lowercase",
                            "german_stop",
                            "german_normalization",
                            "german_light_stemmer"
                        ]
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "id": {
                    "enabled": False,
                },
                "img_id": {
                    "enabled": False
                },
                "titles": {
                    "type": "text",
                    "similarity": similarity,
                    "analyzer": analyzer,
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "classification": {
                    "type": "text",
                    "similarity": similarity,
                    "analyzer": analyzer,
                },
                "work_type": {
                    "type": "text",
                    "similarity": similarity,
                    "analyzer": analyzer,
                },
                "inscriptions": {
                    "type": "text",
                    "similarity": similarity,
                    "analyzer": analyzer,
                },
                "measurements": {
                    "type": "text",
                    "similarity": similarity,
                    "analyzer": analyzer,
                },
                "events": {
                    "type": "text",
                    "similarity": similarity,
                    "analyzer": analyzer,
                },
                "related_subjects": {
                    "type": "text",
                    "similarity": similarity,
                    "analyzer": analyzer,
                },
                "colors": {
                    "type": "text",
                    "similarity": similarity,
                    "analyzer": analyzer,
                },
                "url": {
                    "enabled": False
                },
                "img_url": {
                    "enabled": False
                }
            }
        }
    }


def get_query_modes():
    return [only_disjunction, combined_operators]
