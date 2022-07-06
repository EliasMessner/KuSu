from elasticsearch import Elasticsearch
from flask import Flask, request, render_template, redirect
import querying
from src.constants import default_index_name

app = Flask(__name__)


@app.route("/")
def index():                                                    # the default state when opened
    return render_template("index.html")                        # wird von Flask relativ zu diesem file in "./templates/" gesucht


@app.route("/", methods=["POST", "GET"])                         # what happens if the button is pressed
def form_post():
    if request.method == "POST":
        query = request.form["query"]                           # the written user input
        colors = request.form["colors"]                         # 0 to all colors as a string separated by comma
        colors = colors.split(",")
        categories = request.form["categories"]                 # 0 to all categories as a string separated by comma
        categories = categories.split(",")

        results = [["Bild A", "M. Musterfrau", "localhost:5000"], \
                   ["Malerei", "Unbekannt", "localhost:5000"]]

        # check if client connected
        results = []
        client = prepare_client()
        if client is None:
            query = "Client not connected. Please make sure that ElasticSearch is running on your computer"
            return render_template("index.html", query=query, results=results)

        # concatenate categories and colors to query
        query += ' ' + ' '.join(categories) + ' ' + ' '.join(colors)

        # search the index
        # TODO check if default index exists, if not give bad response
        res = querying.search(client=client, index=default_index_name, query_string=query)
        for hit in res['hits']['hits']:
            # results = [[title, author, url], [title, author, url], ...]
            results.append([', '.join(hit['_source']['titles']),
                            prettify_authors(hit),
                            hit['_source']['img_url']])

    return render_template("index.html", query=query, results=results)      # this updates the HTML page with the results


def prettify_authors(hit) -> str:
    authors = []
    for event in hit['_source']['events']:
        author = ""
        if event.get('actors') is None:
            continue
        author += event['actors']
        if event.get('actors') is not None:
            author += f" ({event['types']})"
        authors.append(author)
    authors = '; '.join(authors)
    return authors


def prepare_client():
    client = Elasticsearch([{"host": "localhost", "port": 9200}])
    if not client.ping():  # assert that the client is connected
        return None
    return client


if __name__ == '__main__':
    app.run(debug=True)
