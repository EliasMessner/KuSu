from elasticsearch import Elasticsearch


def get_query_body(query_string: str) -> dict:
    return {
        "query": {
            "multi_match": {
                "query": query_string,
                "fields": ["*"]
            }
        }
    }


def search(client: Elasticsearch, index: str, query_string: str):
    return client.search(body=get_query_body(query_string), index=index)
