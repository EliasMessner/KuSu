from pprint import pprint

from elasticsearch import Elasticsearch

import src.querying as q
from src.cleanResults import getCleanResults, get_clean_results
from src.indexing import index_documents


def mainloop(function_mapping):
    """
    Prompts the user for new input every loop to execute commands. The input is tokenized. The first token is the
    command name, the following tokens (optional) are arguments for that command.
    The possible commands must be specified in the function_mapping parameter.
    :param function_mapping: a dict like
    {
        command_name: {
            "fun": the function to be called as object,
            "alts": aliases (shorthand notations) als list of strings,
            "help": explanatory help string,
            "args": list of argument names
            }
        }
    """
    print("Connecting to default client at localhost:9200...")
    client = Elasticsearch([{"host": "localhost", "port": 9200}])
    assert client.ping()  # assert that the client is connected
    print("Client connected.")
    while True:
        input_tokens = input().lower().split()
        cmd = input_tokens[0]
        if cmd in ["quit", "q"]:
            break
        if cmd == "help":
            print_help(function_mapping)
            continue
        try_execute_function(function_mapping, input_tokens, client)


def try_execute_function(function_mapping, input_tokens, client):
    cmd = input_tokens[0]
    fun = get_fun(function_mapping, cmd)
    if fun is None:
        print(f"Unrecognized command '{cmd}'. Enter 'help' for help.")
        return
    try:
        check_arg_count(fun, input_tokens)
        fun["fun"](client, input_tokens)
    except ValueError as ve:
        print(str(ve))


def get_fun(function_mappings, cmd):
    """
    Returns the mapping for a specific command. The mapping contains the function, arguments, etc., as specified in
    get_function_mapping
    """
    fun = function_mappings.get(cmd)
    if fun is None:
        # check if a shorthand notation for the command was used
        for item in function_mappings.items():
            if cmd in item[1]["alts"]:
                return item[1]
        return None
    else:
        return fun


def print_help(function_mappings):
    """
    generates and prints a help string from the function_mappings
    """
    help_string = ""
    for key in function_mappings:
        help_string += '[ ' + ' | '.join([key] + function_mappings[key]["alts"]) + ' ] '\
                       + " ".join([f"<{arg_name}>" for arg_name in function_mappings[key]["args"]]) \
                       + ": "
        help_string += function_mappings[key]["help"] + "\n"
    help_string += "quit: quit\n"
    print(help_string)


def get_function_mappings():
    """
    get the mapping from commands to functions.
    fun = the function to be called
    alts = alternative commands (shorthands)
    help = explanatory help string
    args = argument specifications in correct order (will be used to generate help string and check argument count)
           if many tokens are possible add an * as suffix to an argument
    """
    return {
        "create_index": {
            "fun": create_index,
            "alts": ["c"],
            "help": "Creates a new index.",
            "args": ["index_name"]
        },
        "delete_index": {
            "fun": delete_index,
            "alts": ["d"],
            "help": "Deletes an index.",
            "args": ["index_name"]
        },
        "index_all": {
            "fun": index_all,
            "alts": ["ia"],
            "help": "Indexes all xml documents in '../docs' to the specified index.",
            "args": ["index_name"]
        },
        "search": {
            "fun": search,
            "alts": ["s"],
            "help": "searches in given index",
            "args": ["index_name", "query_string*"]
        },
        "list_indices": {
            "fun": list_indices,
            "alts": ["l"],
            "help": "Lists all indices",
            "args": []
        }
    }


def search(client, input_tokens):
    index = input_tokens[1]
    query_string = ' '.join(input_tokens[2:])  # the second and following tokens are parsed as query_string
    if not client.indices.exists(index):
        print(f"Index '{index}' does not exist.")
        return
    res = q.search(client, index, query_string)
    print(f"Hits: {len(res['hits']['hits'])}\n")
    pprint(get_clean_results(res))


def index_all(client, input_tokens):
    index_documents(client, index_name=input_tokens[1])


def create_index(client, input_tokens):
    if client.indices.exists(input_tokens[1]):
        print(f"Index {input_tokens[1]} already exists.")
        return
    print(client.indices.create(input_tokens[1]))


def delete_index(client, input_tokens):
    print(client.indices.delete(input_tokens[1]))


def list_indices(client, input_tokens):
    print(client.indices.get_alias("*"))


def check_arg_count(fun, input_tokens):
    expected = len(fun["args"])
    got = len(input_tokens) - 1
    allow_more = any(arg.endswith("*") for arg in fun["args"])
    if allow_more:
        condition = got >= expected
    else:
        condition = got == expected
    if not condition:
        raise ValueError(f"Command '{fun['fun'].__name__}' takes {expected} argument(s){' or more' if allow_more else ''}, got {got} instead.")


if __name__ == "__main__":
    mainloop(get_function_mappings())
