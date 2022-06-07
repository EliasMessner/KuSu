from flask import Flask, request, render_template, redirect
app = Flask(__name__)


@app.route("/")
def index():                                                                # the default state when opened
    return render_template("index.html")                                    # wird von Flask relativ zu diesem file in "./templates/" gesucht

@app.route("/", methods=['POST','GET'])                                     # what happens if the button is pressed
def form_post():
    if request.method == 'POST':
        query = request.form['query']                                       # this gets the query from the input field

        results = [ ["a", "A", 1] , ["b", "B", 2] , ["c", "C", 3] ]         # placeholder
                                                                            # insert everything here
                                                                            # results need to be a list of lists as [title, author, url]
                                                                            # necessary for a variable-sized table

    return render_template("index.html", querycopy=query, results=results)  # updates the page

if __name__ == '__main__':
    app.run()
