import time

from elasticsearch import Elasticsearch
import os

from lido_handler import prettify
from evaluation import get_run_configurations, get_unique_hits_from_configurations, parse_topics
from constants import manual_relevance_feedbacks_dir, queries_dir


def main():
    print("Establishing Connection...")
    client = Elasticsearch([{"host": "localhost", "port": 9200}])
    print("Done.")
    time.sleep(3)  # sleep

    for queries_filename in os.listdir(queries_dir):
        if queries_filename in ["queries_kunstgeschichte.xml", "queries_kunstschaffende.xml", "queries_laien.xml"]:
            continue
        name = queries_filename[8:-4]
        rel_feedback_filename = "rel_feedback_" + name + ".txt"
        with open(os.path.join(manual_relevance_feedbacks_dir, rel_feedback_filename), 'w') as rel_feedback_file:
            topics = parse_topics(os.path.join(queries_dir, queries_filename))
            for topic, i in zip(topics, range(2)):
                print(f"\n\nQuery {topic['number']}/{len(topics)}: {topic['query']}\n###########")
                hits = get_unique_hits_from_configurations(topic["query"], client=client, size=20)
                for hit in hits:
                    print("\n")
                    print(prettify(hit))
                    rel = get_rel_feedback()
                    new_line = f"{topic['number']} 0 {hit['_id']} {rel}\n"
                    rel_feedback_file.write(new_line)


def get_rel_feedback():
    msg = "relevant? [y/n]"
    while True:
        rel = input(msg)
        if rel == 'y':
            return 1
        if rel == 'n':
            return 0
        msg = f"Bad response '{rel}'. Enter 'y' or 'n'"


if __name__ == "__main__":
    main()
