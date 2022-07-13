import os
import re
import xml.etree.ElementTree as ET
from elasticsearch import Elasticsearch
from pathlib import Path
import random
from tqdm import tqdm

import querying
from constants import queries_dir, run_files_dir, boost_default, boost_2, get_settings, query_results_dir
from lido_handler import prettify, get_title_and_img_string
from create_all_indices import create_all_indices


def main():
    print("Establishing Connection...")
    client = Elasticsearch([{"host": "localhost", "port": 9200}])
    print("Done.")

    print("Creating Indices...")
    create_all_indices(client, overwrite_if_exists=True)  # TODO set to False
    print("Done.")

    # TODO un-comment code

    # print("Creating unranked results files...")
    # create_results_files(client=client, ranked=False)
    # print("Done.")

    # print("Creating unranked results markdown files...")
    # create_results_markdown(client=client)
    # print("Done.")

    # print("Creating ranked results files...")
    # create_results_files(client=client, ranked=True)
    # print("Done.")

    # print("Creating run files...")
    # create_run_files(client)
    # print("Done.")


def create_results_files(client, ranked: bool, size=20):
    """
    Create human-readable file for users to evaluate each search result w.r.t. relevance.
    """
    Path(query_results_dir).mkdir(parents=True, exist_ok=True)  # create the directory if not exists
    for queries_file_name in os.listdir(queries_dir):
        # create one results file per query file
        filename_ending = "_ranked.txt" if ranked else ".txt"
        with open(os.path.join(query_results_dir, queries_file_name.split('.')[0] + "_results" + filename_ending), 'w') as results_file:
            if ranked:
                write_results_ranked(client, results_file, queries_file_name, size)
            else:
                write_results_unranked_as_set(client, results_file, queries_file_name, size)


def write_results_ranked(client, results_file, queries_file_name, size):
    """
    Separates the topic's search results for EACH configuration, and writes them to the results_file in ranked order.
    """
    for configuration_name, _ in tqdm(get_run_configurations()):
        results_file.write(f"CONFIGURATION: {configuration_name}\n\n")
        for topic in parse_topics(os.path.join(queries_dir, queries_file_name)):
            results_file.write(f"\nQuery #{topic['number']} '{topic['query']}'\n\n")
            res = querying.search(client=client, index=configuration_name, query_string=topic["query"], size=size)
            rank = 1
            for hit in res["hits"]["hits"]:
                results_file.write(f"Rank: {rank}\n")
                results_file.write(get_title_and_img_string(hit))
                results_file.write("\n")
                rank += 1
        results_file.write("\n\n")


def write_results_unranked_as_set(client, results_file, queries_file_name, size):
    """
    Unites the topic's search results of all configurations into a set, shuffles them and writes them to the results_file.
    """
    for topic in tqdm(parse_topics(os.path.join(queries_dir, queries_file_name))):
        results = {prettify(hit) for hit in
                   get_all_hits_from_all_configs_merged_as_set(query=topic["query"], client=client, size=size)}
        topic_headline = f"Suchanfrage {topic['number']}: '{topic['query']}'\n"
        results_file.write(topic_headline)
        # shuffle the results to avoid ranking bias when presenting them to the users
        results_shuffled = random.sample(list(results), len(results))
        results_file.write('\n'.join(results_shuffled) + '\n\n')


def get_hits_from_all_configs(query, client, size):
    results = {}
    for configuration_name, _ in get_run_configurations():
        sub_results = []
        res = querying.search(client=client, index=configuration_name, query_string=query, size=size)
        for hit in res["hits"]["hits"]:
            sub_results.append(hit)
        results[configuration_name] = sub_results
    return results


def get_all_hits_from_all_configs_merged_as_set(query, client, size):
    """
    Performs given query on all indices. Indices names are obtained by calling get_run_configurations.
    The resulting hits from all indices are merged into one list that has no duplicate ids. This list is then returned.
    Note that a set of hits is not allowed because hits are dicts and dicts are not hashable.
    :param query:
    :param client:
    :param size:
    :return:
    """
    results = list(get_hits_from_all_configs(query, client, size).values())
    # flatten results
    results = [result for sub_results in results for result in sub_results]
    # remove duplicate ids
    d = {x['_id']: x for x in results}
    results = list(d.values())
    # assert that there are no duplicate ids
    assert all(this['_id'] != that['_id'] or that == this for this in results for that in results)
    return results


def create_results_markdown(client, size=20):
    """
    Create human-readable markdown file for users to evaluate each search result w.r.t. relevance, by clicking a checkbox
    """
    Path(query_results_dir).mkdir(parents=True, exist_ok=True)  # create the directory if not exists
    for queries_file_name in os.listdir(queries_dir):
        # create one results file per query file
        with open(os.path.join(query_results_dir, queries_file_name.split('.')[0] + "_results.md"), 'w') as results_file:
            for topic in tqdm(parse_topics(os.path.join(queries_dir, queries_file_name))):
                results_file.write(f"#### Suchanfrage {topic['number']}: '{topic['query']}'\n")
                results = {prettify_for_markdown(hit) for hit in
                           get_all_hits_from_all_configs_merged_as_set(query=topic["query"], client=client, size=size)}
                # shuffle the results to avoid ranking bias when presenting them to the users
                results_shuffled = random.sample(list(results), len(results))
                if len(results_shuffled) == 0:
                    results_file.write('Keine Suchergebnisse.\n\n')
                else:
                    results_file.write('\n'.join(results_shuffled) + '\n\n')


def prettify_for_markdown(hit) -> str:
    return f"{hit['_source']['titles']}\n\n" \
           f"<img src=\"{hit['_source']['img_url']}\" width=\"400\" />\n\n" \
           f"{hit['_source']['url']}\n\n" \
           f"relevant: <input type=\"checkbox\" name=\"test\" />\n\n" \
           f"nicht relevant: <input type=\"checkbox\" name=\"test\" />\n\n"


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


def parse_topics(filepath):
    """
    Parse topics from given xml filepath and return them as list of dict with keys 'number', 'query', 'description',
    and 'narrative'
    """
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
