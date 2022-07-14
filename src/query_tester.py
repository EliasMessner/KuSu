"""
Program for determining queries useful for evaluation, by checking if a given query returns different results for any
of the 8 settings.
"""

import es_helper
from evaluation import get_hits_from_all_configs


def main():
    client = es_helper.prepare_client_dialog()
    queries = ["test query", "Heinrich Reinhold"]
    for q in queries:
        results = get_hits_from_all_configs(query=q, client=client, size=20)
        print(f"Query: {q} -> {check_if_any_difference_in_any_config(results)}")


def set_equal(l1: list, l2: list, lam) -> bool:
    """
    Return True iff every element of l1 is also contained in l2 and vice versa.
    Basically, return True iff the set versions of those lists are equal. Useful for lists
    with un-hashable type.
    The equality comparison can be specified by a lambda
    :param l2: first list
    :param l1: second list
    :param lam: lambda mapping an element to the value that should be used for equality check
    """
    return {lam(x) for x in l1} == {lam(x) for x in l2}


def check_if_any_difference_in_any_config(results):
    """
    Return True iff any of the configurations got different hits than any other one
    """
    return any(
        not set_equal(sub_results1, sub_results2, lambda x: x["_id"])
        for sub_results1 in results.values()
        for sub_results2 in results.values())


if __name__ == "__main__":
    main()
