from flask import Flask, render_template, request

app = Flask(__name__)

BOOK_STATUS = [
    "Read", 
    "To Do"
]

# basic route, index 
# default method is GET
@app.route('/') 
def index():
    return render_template("index.html")

# request.form for post requests
# request.args for get requests

# greeting route
@app.route("/greet", methods=["POST"])
def greet():
    return render_template("greet.html", name=request.form.get("name", "there"))

# book add
@app.route("/book_add", methods=["GET", "POST"])
def book_add():
    if request.method == "GET":
        return render_template("book_add.html", book_status=BOOK_STATUS)
    # else POST
    if not request.form.get("book_title") or request.form.get("book_status") not in BOOK_STATUS:
        return render_template("book_failure.html")
    # else
    return render_template("book_success.html")



# if __name__ == "__application__":
#    app.run(debug=True)