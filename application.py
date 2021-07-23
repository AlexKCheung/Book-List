from flask import Flask, render_template, request, redirect
from flask.globals import session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# SQLAlchemy database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# sqlalchemy database
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_title = db.Column(db.String(100))
    book_status = db.Column(db.String(100))
    
    # constructor
    def __init__(self, book_title, book_status):
        self.book_title = book_title
        self.book_status = book_status 
    def __repr__(self): 
        return '<Book %r>' % self.book_title 

db.create_all()
db.session.commit()

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
#    USERS[book_title] = book_status
    # print(USERS) # console print for debugging

    a_book = User(book_title, book_status)
    db.session.add(a_book)
    db.session.commit()
    
    #return render_template("book_success.html")
    # redirect instead of success template page
    return redirect("/book_list")

# book list
@app.route("/book_list")
def book_list():
    # USERS is local

    # Case sensitive! "sapiens" and "sapiens " are different
    # also if status are different but title is same, will count as different, no overridding yet
    return render_template("book_list.html", books=User.query.with_entities(User.book_title, User.book_status).distinct())

    #return render_template("book_list.html", books=User.query.with_entities(User.book_title).distinct())
    return render_template("book_list.html", books=User.query.all())

# todo: prevent duplicates
# delete entire table database
# cookies? session

# delete table database
# TODO

if __name__ == "__application__":
    app.run(debug=True)
    db.create_all()