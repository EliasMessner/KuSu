# InformationRetrieval

This search engine was built for a lab project in the Information Retrieval course lectured by Prof Martin Potthast at 
the University of Leipzig.

Dependencies:
* Elasticsearch 7.17.3

Python Packages:
* elasticsearch 7.13.3
* xmltodict

## Preparing the data

To download the data set, run the getData.py script.
3 Files will be downloaded into the "../data" folder.

Next, run the combine.py script, to combine the three xml files you just downloaded to one large xml file.
The output file will be written to "../data/combined_data.xml"

Finally, run the atomize.py script, so that the combined_data.xml file gets broken up into ~12k atomic xml files, each 
representing a document for retrieval.

The data is now ready to be indexed.

## Running and using the search engine

Before you start the search engine, make sure that elasticsearch is up and running on your computer by opening 
localhost:9200 in your browser.

In order to start up the search engine, run the main method in the mainController.py file.
The search engine will now try to establish a connection to the standard elasticsearch client at localhost:9200.
When you see "Client connected." on the console, you can start indexing and searching.

### Indexing Example

to create a new index called my-index, enter
> create_index my-index

or simply shorthand

> c my-index

You can delete the index by

> delete_index my-index

or

> d my-index

In order to bulk-index the data we have just prepared into our new index, enter

> index_all my-index

or simply

> ia my-index

If my-index does not exist, it will be created automatically.

To see all available commands, use

> help

### Searching Example

If you want to search in your index, use the search command as follows:

> search my-index <query_string>

where query_string are the search terms separated by whitespace. No additional " are needed.
For example:

> search my-index druck landscape

searches my-index for the terms "druck" and "landscape", and outputs the resulting hits.
You can also write

> s my-index druck landscape

For shorthand.
