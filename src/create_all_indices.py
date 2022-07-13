"""
Wrapper for single function call.
"""
from elasticsearch import Elasticsearch
from evaluation import create_all_indices

print("Establishing Connection...")
client = Elasticsearch([{"host": "localhost", "port": 9200}])
print("Done.")

print("Creating Indices...")
create_all_indices(client, overwrite_if_exists=True)
print("Done.")
