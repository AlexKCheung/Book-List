from flask import Flask, render_template, request, redirect

app = Flask(__name__)



# local running
USERS = {
}

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
    book_title = request.form.get("book_title")
    book_status = request.form.get("book_status")
    if not book_title and book_status not in BOOK_STATUS:
        return render_template("book_failure.html", message="Book Title and Status Missing!")
    if not book_title: 
        return render_template("book_failure.html", message="Book Title Missing!")
    if book_status not in BOOK_STATUS:
        return render_template("book_failure.html", message="Book Status Missing!")
    
    # else success
    # USERS is local
    USERS[book_title] = book_status
    # print(USERS) # console print for debugging
    # return render_template("book_success.html")
    # redirect instead of success template page
    return redirect("/book_list")

# book list
@app.route("/book_list")
def book_list():
    # USERS is local
    return render_template("book_list.html", users=USERS)

# if __name__ == "__application__":
#    app.run(debug=True)