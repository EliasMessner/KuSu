import os
from bs4 import BeautifulSoup


def parse_relevance_judgements(dir_path) -> list:
    """
    Reads from each feedback file the relevance feedback for each hit, for each query.
    Determines for each hit the unique _id for, each of the 8 indices.
    Returns a list of tuples, each with the values:
    (qid, 0, doc, rel)
    Meaning:
        qid: topic number
        0: unused, always 0
        doc: a dict with 8 entries, one for each index, where key is index name and value is the _id of the hit doc in
            the index -> {index_name: doc_id}
        rel: relevance judgement (bool)
    """
    relevance_judgements = []
    for filename in os.listdir(dir_path):
        filepath = os.path.join(dir_path, filename)
        for (qid, query), hits in zip(parse_topics(filepath), parse_hits(filepath)):
            for hit in parse_hits(query):
                doc = get_doc_ids(hit)
                rel = get_relevance_judgement(hit)
                relevance_judgements.append((qid, 0, doc, rel))
    return relevance_judgements


def parse_topics(feedback_file_path):
    topics = []
    with open(feedback_file_path, encoding="UTF-8") as fp:
        soup = BeautifulSoup(fp, "html.parser")
    topic_elements = soup.find_all("h2")
    for t in topic_elements:
        # get topic_number and query by string operations
        topic_number = int(t.text[t.text.find(" ") : t.text.find(":")].strip())
        query = t.text[t.text.find("'")+1 : t.text.find("'", t.text.find("'")+1)]
        topics.append((topic_number, query))
    return topics


def parse_hits(feedback_file_path):
    raise NotImplementedError  # TODO


def get_doc_ids(hit):
    raise NotImplementedError  # TODO


def get_relevance_judgement(hit):
    raise NotImplementedError  # TODO
