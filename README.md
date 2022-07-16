# KuSu

This search engine was built for a lab project in the Information Retrieval course lectured by Prof Martin Potthast at 
the University of Leipzig.

The name KuSu (short for KulturSuchmaschine) stems from the German word ["Kusu"](https://de.wikipedia.org/wiki/Kusus), a marsupial home to Australia.

### The Data

The data we use for our index comes from three different sources.

One data set is a lido data set provided by the Museum für Kunst und Gewerbe Hamburg (MKG), and can be found [here](https://github.com/MKGHamburg/MKGCollectionOnlineLIDO_XML).

We use the files <i>mkg_lido-dC.web_0.xml</i>, <i>mkg_lido-dC.web_1.xml</i>, and <i>mkg_lido-dC.web_2.xml</i>., totaling to about 12k documents.

Additionally, we use a data set provided by Deutsches Museum (München), which can be found [here](https://dmd.plus/opendata/digiporta/dm/xml/)

The last data set is provided by Westmünsterland Museum and can be found [here](https://download.codingdavinci.de/index.php/s/y7wHa8r6dWtnTTm?dir=undefined&path=%2F&openfile=551921).
Remarkable about this data set is that is consists of lido xml data as well as images to each entry.
The images will be used for image analysis.

Overall, the data consists of 18851 documents.

### Dependencies:
* Elasticsearch 7.17.x

### Python Packages:
* python 3.10
* elasticsearch 7.13.x
* tqdm
* scipy
* numpy
* matplotlib
* validators
* flask
* xmltodict
* jupyter
* pip
* webcolors
* extcolors

To automatically create an Anaconda environment, use

> conda create env -f conda_env.yml

# User Manual

First, make sure that the Elasticsearch (v 7.17.x) client is up and running on your computer.

## Preparing the data and index

Skip this part if you already have access to an Elasticsearch cluster with the data indexed.

### Downloading the data

The data from Westmünsterland Museum is already present in the "../data" folder.
The data sets from MKG and Deutsches Museum need to be downloaded, since they are too large to be shipped with this project.

To download and prepare the data sets, run the prepare_data.py script.

The data is now ready to be indexed.

### Creating the default index

By default, KuSu searches on the default index. The default index can be automatically created by running 
create_default_index.py.

The default index is the one with the optimal settings as determined in the course of our 
research.

Creating the default index can take from 5 minutes to 1 hour, depending on your machine's performance. When the script has
finished creating the index, you are good to go.

## Running and using KuSu Search Engine

### Web Interface

For a convenient user experience, you can use the KuSu Web Interface.

To start the web interface, run the server.py script. You are prompted to enter the URL, port, username, and password of an
Elasticsearch remote. If you want to connect to localhost:9200, enter "localhost" as URL and leave the password blank.

When the connection to Elasticsearch is established, you can access the web interface by visiting localhost:5000 in your
favorite web browser.

### Command Line Interface

If you are an advanced user, you can also use the KuSu Command Line Interface, which enables you to create your own 
indices.

In order to start up the CLI, run the main_controller.py file.

You are prompted to enter the URL, port, username, and password of an
Elasticsearch remote. If you want to connect to localhost:9200, enter "localhost" as URL and leave the password blank.

When you see "Client connected." on the console, you can start indexing and searching.

#### Indexing Example

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

#### Searching Example

If you want to search in your index, use the search command as follows:

> search my-index <query_string>

where query_string are the search terms separated by whitespace. No additional " are needed.
For example:

> search my-index druck landscape

searches my-index for the terms "druck" and "landscape", and outputs the resulting hits.
You can also write

> s my-index druck landscape

For shorthand.
