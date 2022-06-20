from flask import Flask, request, render_template, redirect
app = Flask(__name__)


@app.route("/")
def index():                                                                # the default state when opened
    return render_template("index.html")                                    # wird von Flask relativ zu diesem file in "./templates/" gesucht


@app.route("/", methods=["POST","GET"])                                     # what happens if the button is pressed
def form_post():
    if request.method == "POST":
        query = request.form["query"]
        years = [request.form["minyear"], request.form["maxyear"]]
        colors = request.form["colors"].split(",")

        results = [ [query, minyear, colors] , [query, minyear, colors] ]         # placeholder
                                                                            # insert everything here
                                                                            # results need to be a list of lists as [title, author, url]
                                                                            # necessary for a variable-sized table

    return render_template("index.html", query=query, results=results)  # updates the page


if __name__ == '__main__':
    app.run()
