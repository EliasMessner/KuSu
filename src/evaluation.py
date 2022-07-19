import os
import random
import re
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Callable

import pandas as pd
from matplotlib import pyplot as plt
from tqdm import tqdm
from trectools import TrecQrel, procedures, TrecRes, TrecEval

import es_helper
from constants import queries_dir, run_files_dir, query_results_dir, qrels_dir, plots_dir, FontSizes
from indexing import get_index_configurations
from lido_handler import prettify, get_title_and_img_string
from es_helper import get_query_modes


def main():
    client = es_helper.prepare_client_dialog()

    # print("Creating Indices...")
    # create_all_indices(client, overwrite_if_exists=False)
    # print("Done.")

    # print("Creating unranked results files...")
    # create_results_files(client=client, ranked=False)
    # print("Done.")

    # print("Creating unranked results markdown files...")
    # create_results_markdown(client=client)
    # print("Done.")

    # print("Creating ranked results files...")
    # create_results_files(client=client, ranked=True)
    # print("Done.")

    print("Creating run files...")
    create_run_files(client)
    print("Done.")

    # ks = [10, 20]
    # for k in ks:
    #     # precision at k
    #     plot_results_for_all_groups(k, metric=get_precision_at_k,
    #                                 display_metric=f"Precision at {k}",
    #                                 filename=f"p_at_{k}.pdf")
    #     # ndcg at k
    #     plot_results_for_all_groups(k, metric=get_ndcg_k,
    #                                 display_metric=f"nDCG at {k}",
    #                                 filename=f"ndcg_at_{k}.pdf")
    #     # t test wrt. precision at k, for each group
    #     for group_name, matrix in get_t_test_matrix_for_each_group(metric=f"P_{k}").items():
    #         matrix.to_csv(os.path.join(plots_dir, f"ttests_k{k}_{group_name}.csv"))


def plot_results_for_all_groups(k: int, metric: Callable, display_metric: str, filename: str,
                                qrels_filenames: list[str] = None):
    results, group_names = get_results_for_all_groups(k, metric, qrels_filenames)
    outfile = os.path.join(plots_dir, filename)
    fig = plot_system_rank(results, group_names, display_metric)
    fig.savefig(outfile)
    print(f"Saved figure to {outfile}\n")


def get_results_for_all_groups(k: int, metric: Callable, qrels_filenames: list[str] = None):
    if qrels_filenames is None:
        qrels_filenames = os.listdir(qrels_dir)
    results = []
    group_names = []
    for i, qrels_filename in enumerate(qrels_filenames, start=1):
        print(f"File {i} of {len(qrels_filenames)}")
        results.append(metric(k, qrels_filename))
        group_names.append(get_group_name(qrels_filename))
    return results, group_names


def plot_system_rank(results, group_names, display_metric, offset_increment=0.2):
    plt.rc('font', size=FontSizes.SMALL_SIZE)
    plt.clf()
    size = len(results[0])
    offset = size * offset_increment / 2
    # fig = plt.figure(111)
    for result, group_name in zip(results, group_names):
        # transform to df
        df = pd.DataFrame(result, columns=["name", "value", "ci"])
        df = df.sort_values("value", ascending=False).reset_index(drop=True)
        # get data
        values = df["value"]
        ci = df["ci"]
        team_names = df["name"]
        x = df.index + offset
        offset += offset_increment
        # plot data
        plt.errorbar(x=x, y=values, fmt='o', yerr=ci, label=group_name)
        plt.xticks(ticks=range(1, size+1), labels=team_names, rotation='vertical')
    # Small adjustments for plotting
    plt.legend(loc='lower right', bbox_to_anchor=(1, 1.025))
    fig = plt.gcf()
    fig.subplots_adjust(bottom=0.6)  # increase padding because we use long tick labels
    ax = fig.get_axes()[0]
    ax.set_xlim(0.5, size + 0.5)
    ax.set_ylabel(display_metric)
    return fig


def get_precision_at_k(k: int, qrels_filename: str):
    group_name = get_group_name(qrels_filename)
    qrels = TrecQrel(os.path.join(qrels_dir, qrels_filename))
    runs = procedures.list_of_runs_from_path(os.path.join(run_files_dir, group_name))
    time.sleep(0.1)  # for tqdm console output
    results = evaluate_runs_tqdm(runs, qrels, per_query=True)
    p_at_k = procedures.extract_metric_from_results(results, f"P_{k}")
    return p_at_k


def get_ndcg_k(k: int, qrels_filename: str):
    group_name = get_group_name(qrels_filename)
    qrels = TrecQrel(os.path.join(qrels_dir, qrels_filename))
    runs = procedures.list_of_runs_from_path(os.path.join(run_files_dir, group_name))
    results = []
    for run in tqdm(runs):
        evaluator = TrecEval(run, qrels)
        ndcg_k = evaluator.get_ndcg(depth=k)
        result_run = [{"metric": f"NDCG_{k}", "query": "all", "value": ndcg_k}]
        tres = TrecRes()
        tres.data = pd.DataFrame(result_run)
        tres.runid = run.get_runid()
        results.append(tres)
    return procedures.extract_metric_from_results(results, f"NDCG_{k}")


def evaluate_runs_tqdm(trec_runs, trec_qrel, per_query):
    results = []
    for r in tqdm(trec_runs):
        results.append(r.evaluate_run(trec_qrel, per_query))
    return results


def get_t_test_matrix_for_each_group(qrels_filenames: list[str] = None, metric="P_10"):
    if qrels_filenames is None:
        qrels_filenames = os.listdir(qrels_dir)
    result_matrices = {}
    for i, qrels_filename in enumerate(qrels_filenames, start=1):
        print(f"File {i} of {len(qrels_filenames)}")
        group_name = get_group_name(qrels_filename)
        result_matrix = get_t_test_matrix(metric, qrels_filename)
        result_matrices[group_name] = pd.DataFrame(data=result_matrix)
    return result_matrices


def get_t_test_matrix(metric, qrels_filename):
    result_matrix = {}
    group_name = get_group_name(qrels_filename)
    qrels = TrecQrel(os.path.join(qrels_dir, qrels_filename))
    runs = procedures.list_of_runs_from_path(os.path.join(run_files_dir, group_name))
    for r1 in tqdm(runs):
        v1 = r1.filename.split(".")[0]  # variant name
        result_matrix[v1] = {}
        for r2 in runs:
            if r1.filename == r2.filename:
                continue
            v2 = r2.filename.split(".")[0]
            result_r1 = r1.evaluate_run(qrels, per_query=True)
            result_r2 = r2.evaluate_run(qrels, per_query=True)
            p_value = result_r1.compare_with(result_r2, metric=metric)
            result_matrix[v1][v2] = p_value[1]
    return result_matrix


def create_results_files(client, ranked: bool, size=20):
    """
    Create human-readable file for users to evaluate each search result w.r.t. relevance.
    """
    Path(query_results_dir).mkdir(parents=True, exist_ok=True)  # create the directory if not exists
    for queries_file_name in os.listdir(queries_dir):
        # create one results file per query file
        filename_ending = "_ranked.txt" if ranked else ".txt"
        with open(os.path.join(query_results_dir, queries_file_name.split('.')[0] + "_results" + filename_ending),
                  'w') as results_file:
            if ranked:
                write_results_ranked(client, results_file, queries_file_name, size)
            else:
                write_results_unranked_as_set(client, results_file, queries_file_name, size)


def write_results_ranked(client, results_file, queries_file_name, size):
    """
    Separates the topic's search results for EACH configuration, and writes them to the results_file in ranked order.
    """
    for configuration_name, _, query_mode in tqdm(get_variants()):
        results_file.write(f"VARIANT: {configuration_name + '-' + query_mode}\n\n")
        for topic in parse_topics(os.path.join(queries_dir, queries_file_name)):
            results_file.write(f"\nQuery #{topic['number']} '{topic['query']}'\n\n")
            res = es_helper.search(client=client, index=configuration_name, query_string=topic["query"], size=size)
            rank = 1
            for hit in res["hits"]["hits"]:
                results_file.write(f"Rank: {rank}\n")
                results_file.write(get_title_and_img_string(hit))
                results_file.write("\n")
                rank += 1
        results_file.write("\n\n")


def write_results_unranked_as_set(client, results_file, queries_file_name, size):
    """
    Unites the topic's search results of all configurations into a set, shuffles them and writes them to the
    results_file.
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
    for configuration_name, _, query_mode in get_variants():
        sub_results = []
        res = es_helper.search(client=client,
                               index=configuration_name,
                               query_string=query,
                               query_mode=query_mode,
                               size=size)
        for hit in res["hits"]["hits"]:
            sub_results.append(hit)
        results[(configuration_name, query_mode)] = sub_results
    return results


def get_all_hits_from_all_configs_merged_as_set(query, client, size):
    """
    Performs given query on all indices and all query modes. Indices names are obtained by calling
    get_index_configurations, query modes are obtained by calling get_query_modes.
    The resulting hits from all settings are merged into one list that has no duplicate ids. This list is then returned.
    Note that a set of hits is not allowed because hits are dicts and dicts are not hashable.
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
    Create human-readable markdown file for users to evaluate each search result wrt. relevance, by clicking a checkbox
    """
    Path(query_results_dir).mkdir(parents=True, exist_ok=True)  # create the directory if not exists
    for queries_file_name in os.listdir(queries_dir):
        # create one results file per query file
        with open(os.path.join(query_results_dir, queries_file_name.split('.')[0] + "_results.md"),
                  'w') as results_file:
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
        if "auswahl" not in queries_file_name:
            continue
        topics = parse_topics(os.path.join(queries_dir, queries_file_name))
        group_name = get_group_name(queries_file_name)
        # for each user group: one file containing overall performance, one folder containing a run for each variant
        Path(os.path.join(run_files_dir, group_name)).mkdir(parents=True, exist_ok=True)  # create dir if not exists
        with open(os.path.join(run_files_dir, group_name + "_run_file.txt"), 'w') as group_run_file:
            # iterate the configurations. configuration_name is also the name of the index that uses this config.
            for configuration_name, _, query_mode in tqdm(get_variants()):
                variant_name = get_variant_name(configuration_name, query_mode)
                # one file for each variant (-> one run for each variant)
                with open(os.path.join(run_files_dir, group_name, f"{variant_name}.txt"), 'w') as variant_run_file:
                    for topic in topics:
                        # need to scroll through results because there are too many (ranking all 18k documents)
                        body = es_helper.get_query_body(query_string=topic["query"], query_mode=query_mode)
                        rank = 1
                        for hits in scroll(client, index=configuration_name, body=body, scroll='30s', size=500):
                            for hit in hits:
                                new_line = ' '.join([topic["number"], "Q0", hit["_id"], str(rank), str(hit["_score"]),
                                                     variant_name])
                                group_run_file.write(new_line + "\n")
                                variant_run_file.write(new_line + "\n")
                                rank += 1


def get_variant_name(configuration_name: str, query_mode: str):
    """
    Remove boost mode prefix because we only always use one boost mode.
    Abbreviate "operators" with "op"
    """
    name = configuration_name + '-' + query_mode
    if name.startswith("boost"):
        name = '-'.join(name.split("-")[1:])
    name.replace("operators", "op")
    return name


def get_group_name(queries_file_name):
    """
    get name of user group, e.g. "auswahl_laien.xml" becomes "laien"
    """
    return queries_file_name.split(".")[0].split("_")[-1]


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


def get_variants():
    """
    Return all combinations of index configurations and query modes
    :return: List of tuples containing (index_configuration_name, index_settings, query_mode)
    """
    result = []
    for index_configuration, index_settings in get_index_configurations():
        for query_mode in get_query_modes():
            result.append((index_configuration, index_settings, query_mode))
    return result


if __name__ == "__main__":
    main()
