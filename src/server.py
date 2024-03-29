from flask import Flask, request, render_template

import es_helper
from constants import default_index_name
from lido_handler import prettify

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

        # check if client connected
        results = []
        if CLIENT is None:
            query = "Client not connected. Please make sure that ElasticSearch is running on your computer"
            return render_template("index.html", query=query, results=results)

        # concatenate categories and colors to query
        query += ' ' + ' '.join(categories) + ' ' + ' '.join(colors)

        # search the index
        # TODO check if default index exists, if not give bad response
        res = es_helper.search(client=CLIENT, index=default_index_name, query_string=query)
        for hit in res['hits']['hits']:
            # results = [[title, author, url], [title, author, url], ...]
            results.append([hit['_source']['titles'],
                            f"{prettify(hit, include_title=False)}",
                            hit['_source']['img_url']])

    return render_template("index.html", query=query, results=results)      # this updates the HTML page with the results


if __name__ == '__main__':
    CLIENT = es_helper.prepare_client_dialog()
    # if debug=True, user needs to enter credentials two times. Therefore, reset to False after debugging
    app.run(debug=False)
