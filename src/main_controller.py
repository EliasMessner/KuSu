from pprint import pprint

from elasticsearch import Elasticsearch

from src.constants import data_dir, docs_dir
import src.querying as querying
from src.indexing import index_documents


def mainloop(command_function_mapping):
    """
    Prompts the user for new input every loop to execute commands. The input is tokenized. The first token is the
    command name, the following tokens (optional) are arguments for that command.
    The possible commands must be specified in the function_mapping parameter.
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
            print_help(command_function_mapping)
            continue
        try_execute_function(command_function_mapping, input_tokens, client)


def try_execute_function(command_function_mapping, input_tokens, client):
    """
    Tries to invoke a function call given the input tokens, where the first token is read as the command name to
    be invoked. If such a command name does not exist, it gives a respective console output and returns normally.
    :param command_function_mapping: The mapping from command names to method calls and further info
      See constants.command_function_mapping
    :param input_tokens: the input tokens as list. The first one is the command name, the following ones (optional) are
      arguments for that command
    :param client: Elasticsearch client with active connection
    """
    cmd = input_tokens[0]
    fun = get_fun(command_function_mapping, cmd)
    if fun is None:
        print(f"Unrecognized command '{cmd}'. Enter 'help' for help.")
        return
    try:
        check_arg_count(fun, input_tokens)
        fun["fun"](client, input_tokens)
    except ValueError as ve:
        print(str(ve))


def get_fun(command_function_mapping, cmd):
    """
    Returns the entry mapped to a specified command. The entry contains the function, arguments, etc., as specified in
    constants.command_function_mapping.
    If the command does not exist, returns None.
    """
    fun = command_function_mapping.get(cmd)
    if fun is None:
        # check if a shorthand notation for the command was used
        for item in command_function_mapping.items():
            if cmd in item[1]["alts"]:
                return item[1]
        return None
    else:
        return fun


def print_help(command_function_mapping):
    """
    Generates and prints a help string from the function_mappings.
    """
    help_string = ""
    for key in command_function_mapping:
        help_string += '[ ' + ' | '.join([key] + command_function_mapping[key]["alts"]) + ' ] '\
                       + " ".join([f"<{arg_name}>" for arg_name in command_function_mapping[key]["args"]]) \
                       + ": "
        help_string += command_function_mapping[key]["help"] + "\n"
    help_string += "quit: quit\n"
    print(help_string)


def search(client, input_tokens):
    """
    Search the index using the second and following input tokens as query string.
    The results are printed to the console.
    :param client:
    :param input_tokens:
    :return:
    """
    index = input_tokens[1]
    query_string = ' '.join(input_tokens[2:])  # the second and following tokens are parsed as query_string
    if not client.indices.exists(index):
        print(f"Index '{index}' does not exist.")
        return
    res = querying.search(client, index, query_string)
    print(f"Hits: {len(res['hits']['hits'])}\n")
    pprint(res['hits']['hits'])


def index_all(client, input_tokens):
    index_documents(client, index_name=input_tokens[1], docs_dir=docs_dir)


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


def get_command_function_mapping():
    """
    command_function_mapping: a dict like
    {
        command_name: {
            "fun": the function to be called as object,
            "alts": aliases (shorthand notations) als list of strings,
            "help": explanatory help string,
            "args": list of argument names
            }
    }
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


if __name__ == "__main__":
    mainloop(get_command_function_mapping())