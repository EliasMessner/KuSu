import os
import time
from pathlib import Path

import es_helper
from constants import qrels_dir, queries_dir
from evaluation import get_all_hits_from_all_configs_merged_as_set, parse_topics
from lido_handler import prettify


def main():
    client = es_helper.prepare_client_dialog()
    time.sleep(2)  # sleep so that elasticsearch warnings can be output and not interrupt the following outputs
    queries_filename = ask_queries_filename()
    name = queries_filename[8:-4]  # 'queries_test.xml' becomes 'test'
    rel_feedback_filename = "qrels_" + name + ".txt"
    Path(qrels_dir).mkdir(parents=True, exist_ok=True)  # create the directory if not exists
    with open(os.path.join(qrels_dir, rel_feedback_filename), 'w') as rel_feedback_file:
        topics = parse_topics(os.path.join(queries_dir, queries_filename))
        for topic in topics:
            print(f"\n\nQuery {topic['number']}/{len(topics)}: {topic['query']}\n###########")
            hits = get_all_hits_from_all_configs_merged_as_set(topic["query"], client=client, size=20)
            if not len(hits):
                print("No Results.\n")
            for i, hit in enumerate(hits, start=1):
                print(f"\nResult {i}/{len(hits)}:")
                print(prettify(hit))
                rel = get_rel_feedback(0, 5)
                new_line = f"{topic['number']} 0 {hit['_id']} {rel}\n"
                rel_feedback_file.write(new_line)


def ask_queries_filename():
    while True:
        queries_filename = input("Enter filename of queries xml file: ")
        if not queries_filename.endswith("xml"):
            print("Filename must end with '.xml'")
            continue
        break
    return queries_filename


def get_rel_feedback(min_value: int, max_value: int):
    msg = f"How relevant? [{min_value}-{max_value}]"
    while True:
        rel = input(msg)
        if rel.isdigit() and min_value <= int(rel) <= max_value:
            return int(rel)
        msg = f"Bad response '{rel}'. Enter number from {min_value} to {max_value}"


def print_results_without_asking_feedback():
    client = es_helper.prepare_client_dialog()
    time.sleep(2)  # sleep so that elasticsearch warnings can be output and not interrupt the following outputs
    queries_filename = ask_queries_filename()
    topics = parse_topics(os.path.join(queries_dir, queries_filename))
    for topic in topics:
        print(f"\n\nQuery {topic['number']}/{len(topics)}: {topic['query']}\n###########")
        hits = get_all_hits_from_all_configs_merged_as_set(topic["query"], client=client, size=20)
        if not len(hits):
            print("No Results.\n")
        for i, hit in enumerate(hits, start=1):
            print(f"\nResult {i}/{len(hits)}:")
            print(prettify(hit))
            print("How relevant? [0-5]")


if __name__ == "__main__":
    main()
    # print_results_without_asking_feedback()
