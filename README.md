# InformationRetrieval

This search engine was built for a lab project in the Information Retrieval course lectured by Prof Martin Potthast at 
the University of Leipzig.

### The Data

The data we use for our index comes from three different sources.

One data set is a lido data set provided by the Museum für Kunst und Gewerbe Hamburg (MKG), and can be found here:
https://github.com/MKGHamburg/MKGCollectionOnlineLIDO_XML.
We use the files <i>mkg_lido-dC.web_0.xml</i>, <i>mkg_lido-dC.web_1.xml</i>, and <i>mkg_lido-dC.web_2.xml</i>., totaling to about 12k documents.

Additionally, we use a data set provided by Deutsches Museum (München), which can be found here:
https://dmd.plus/opendata/digiporta/dm/xml/

The last data set is provided by Westmünsterland Museum and can be found here:
https://download.codingdavinci.de/index.php/s/y7wHa8r6dWtnTTm?dir=undefined&path=%2F&openfile=551921.
Remarkable about this data set is that is consists of lido xml data as well as images to each entry.
The images will be used for image analysis.

Overall, the data consists of 18851 documents.

### Dependencies:
* Elasticsearch 7.17.3

### Python Packages:
* elasticsearch 7.13.3
* xmltodict
* tqdm
* webcolors
* flask

## Preparing the data

The data from Westmünsterland Museum is already present in the "../data" folder.
The data sets from MKG and Deutsches Museum need to be downloaded, since they are too large to be shipped with this project.

To download and prepare the data sets, run the prepare_data.py script.

The data is now ready to be indexed.

## Running and using the search engine

Before you start the search engine, make sure that elasticsearch is up and running on your computer by opening 
localhost:9200 in your browser.

In order to start up the search engine, run the main method in the main_controller.py file.
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
