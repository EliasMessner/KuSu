from src.main_controller import *

urls = ["https://raw.githubusercontent.com/MKGHamburg/MKGCollectionOnlineLIDO_XML/master/mkg_lido-dC.web_0.xml",
            "https://raw.githubusercontent.com/MKGHamburg/MKGCollectionOnlineLIDO_XML/master/mkg_lido-dC.web_1.xml",
            "https://raw.githubusercontent.com/MKGHamburg/MKGCollectionOnlineLIDO_XML/master/mkg_lido-dC.web_2.xml"]

data_dir = "../data/"

logs_dir = "../logs/"

docs_dir = "../docs/"

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
command_function_mapping = {
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
