import os
import re
import xml.etree.ElementTree as ET
from elasticsearch import Elasticsearch
from pathlib import Path
import random
from tqdm import tqdm

import querying
from src.constants import queries_dir, run_files_dir, boost_default, boost_2, get_settings, docs_dir, query_results_dir
from indexing import index_documents


def main():
    print("Establishing Connection...")
    client = Elasticsearch([{"host": "localhost", "port": 9200}])
    print("Done.")
    print("Creating Indices...")
    create_all_indices(client)
    print("Done.")
    print("Creating results files...")
    create_results_files(client)
    print("Done.")
    print("Creating run files...")
    create_run_files(client)
    print("Done.")


def create_results_files(client):
    """
    Create human-readable file for users to evaluate each search result w.r.t. relevance.
    """
    Path(query_results_dir).mkdir(parents=True, exist_ok=True)  # create the directory if not exists
    for queries_file_name in os.listdir(queries_dir):
        # create one results file per query file
        with open(os.path.join(query_results_dir, queries_file_name.split('.')[0] + "_results" + ".txt"), 'w') as results_file:
            for topic in tqdm(parse_topics(os.path.join(queries_dir, queries_file_name))):
                results = set()
                for configuration_name, _ in get_run_configurations():
                    res = querying.search(client=client, index=configuration_name, query_string=topic["query"], size=20)
                    for hit in res["hits"]["hits"]:
                        results.add(prettify(hit))
                topic_headline = f"Suchanfrage {topic['number']}: '{topic['query']}'\n"
                results_file.write(topic_headline)
                # shuffle the results to avoid ranking bias when presenting them to the users
                results_shuffled = random.sample(list(results), len(results))
                results_file.write('\n'.join(results_shuffled) + '\n\n')


def prettify(hit):
    result = f"Titel: {hit['_source']['titles']}\n" \
              f"Beschreibung: {hit['_source']['inscriptions']}\n" \
              f"Klassifikation: {hit['_source']['classification']}\n" \
              f"Kategorie: {hit['_source']['work_type']}\n" \
              f"Maße: {hit['_source']['measurements']}\n" \
              f"Ereignisse: {hit['_source']['events']}\n" \
              f"Verwandte Themen: {hit['_source']['related_subjects']}\n" \
              f"Bild-URL: {hit['_source']['img_url']}\n"
    return result


def create_run_files(client):
    """
    Create a run file for each query file. The run file can then be used to evaluate the search results on different
    configurations.
    """
    Path(queries_dir).mkdir(parents=True, exist_ok=True)  # create the directory if not exists
    for queries_file_name in os.listdir(queries_dir):
        # create one run file per query file
        with open(os.path.join(run_files_dir, queries_file_name.split('.')[0] + "_run_file" + ".txt"), 'w') as run_file:
            # iterate the configurations. configuration_name is also the name of the index that uses this config.
            for configuration_name, _ in tqdm(get_run_configurations()):
                topics = parse_topics(os.path.join(queries_dir, queries_file_name))
                for topic in topics:
                    # need to scroll through results because there are too many (ranking all 18k documents)
                    rank = 1
                    for hits in scroll(client, index=configuration_name, body=querying.get_query_body(topic["query"]), scroll='30s', size=500):
                        for hit in hits:
                            new_line = ' '.join([topic["number"], "Q0", hit["_id"], str(rank), str(hit["_score"]), configuration_name])
                            run_file.write(new_line + "\n")
                            rank += 1


def scroll(client, index, body, scroll, size, **kw):
    page = client.search(index=index, body=body, scroll=scroll, size=size, **kw)
    scroll_id = page['_scroll_id']
    hits = page['hits']['hits']
    while len(hits):
        yield hits
        page = client.scroll(scroll_id=scroll_id, scroll=scroll)
        scroll_id = page['_scroll_id']
        hits = page['hits']['hits']
    client.clear_scroll(scroll_id=page['_scroll_id'])


def create_all_indices(client: Elasticsearch):
    for index_name, conf_body in get_run_configurations():
        if client.indices.exists(index_name):
            continue
        client.indices.create(index=index_name, body=conf_body)
        index_documents(client=client, index_name=index_name, docs_dir=docs_dir)


def parse_topics(filepath):
    # add pseudo root node so that non-well-formatted xml can be parsed
    with open(filepath) as f:
        xml = f.read()
    root = ET.fromstring(re.sub(r"(<\?xml[^>]+\?>)", r"\1<root>", xml) + "</root>")
    topics = []
    for child in list(root):
        topics.append({
            "number": child.attrib.get("number"),
            "query": child.find("query").text.strip(),
            "description": child.find("description").text.strip(),
            "narrative": child.find("narrative").text.strip()
        })
    return topics


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
