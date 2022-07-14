from getpass import getpass

from elasticsearch import Elasticsearch

from constants import get_all_search_fields, bcolors


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


def prepare_client_dialog():
    """
    Performs a console dialog asking for URL, port, user and password, and attempts to connect to the specified ES
    cluster with the given credentials.
    If the connection fails, return False.
    Otherwise, return the connected Elasticsearch client.
    """
    print("Please enter the credentials of an Elasticsearch cluster to connect to.")
    credentials = prompt_for_credentials()
    client = Elasticsearch([credentials["url"]],
                           http_auth=(credentials["user"], credentials["password"]),
                           port=credentials["port"])
    if not client.ping():
        print(f"{bcolors.WARNING}Client not connected. Please make sure you entered valid credentials.{bcolors.ENDC}")
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
