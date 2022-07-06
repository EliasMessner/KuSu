from flask import Flask, request, render_template, redirect
app = Flask(__name__)


@app.route("/")
def index():                                                    # the default state when opened
    return render_template("index.html")                        # wird von Flask relativ zu diesem file in "./templates/" gesucht


@app.route("/", methods=["POST","GET"])                         # what happens if the button is pressed
def form_post():
    if request.method == "POST":
        query = request.form["query"]                           # the written user input
        colors = request.form["colors"]                         # 0 to all colors as a string separated by comma
        if colors.find(",") != -1:
            colors = colors.split(",")
        categories = request.form["categories"]                 # 0 to all categories as a string separated by comma
        if categories.find(",") != -1:
            categories = categories.split(",")

        results = [ ["Bild A", "M. Musterfrau", "localhost:5000"],\
            ["Malerei", "Unbekannt", "localhost:5000"]]

        """
        call search engine with everything that belongs to it here.
        I didn't work on the backend, don't know precisely how to.
        Variables for search engine query, colors, and categories.

        results = [ [title,author,url] , [title,author,url] , ... ]

        if more columns are desired update the result table in the HTML file accordingly and add the variable here.

        if search engine returns too many results:
        results = results[:30]
        or any other appropriate rank-based lower limit

        """

    return render_template("index.html", query=query, results=results)      # this updates the HTML page with the results


if __name__ == '__main__':
    app.run(debug = True)
