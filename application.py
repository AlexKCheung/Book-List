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
# USERS = {}

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

# book add to database
@app.route("/book_add", methods=["GET", "POST"])
def book_add():
    if request.method == "GET":
        return render_template("book_add.html", book_status=BOOK_STATUS)
    
    # else POST
    book_title = request.form.get("book_title")
    book_status = request.form.get("book_status")

    # .strip() removes tabs and spaces before and after a string
    book_title = book_title.strip()

    # book list  
    book_list_query=User.query.with_entities(User.book_title, User.book_status).distinct()

    if not book_title and book_status not in BOOK_STATUS:
        return render_template("book_list.html", message="Book title and status missing!", book_status=BOOK_STATUS, books=book_list_query)
        # return render_template("book_failure.html", message="Book Title and Status Missing!")
    if not book_title: 
        return render_template("book_list.html", message="Book title missing!", book_status=BOOK_STATUS, books=book_list_query)
        # return render_template("book_failure.html", message="Book Title Missing!")
    if book_status not in BOOK_STATUS:
        return render_template("book_list.html", message="Book status missing!", book_status=BOOK_STATUS, books=book_list_query)
        # return render_template("book_failure.html", message="Book Status Missing!")
    
    # else success / valid book title
    # USERS is local
    # USERS[book_title] = book_status
    
    exists = User.query.filter_by(book_title=book_title).first()
    # if book_title already exists, override its status
    # else create new book_title and status
    if exists:
        exists.book_title = book_title
        exists.book_status = book_status        
    else:
        a_book = User(book_title, book_status)
        db.session.add(a_book)
    db.session.commit()
    
    #return render_template("book_success.html")
    # redirect instead of success template page
    # return redirect("/book_list")
    return render_template("list.html", message=None, book_status=BOOK_STATUS, books=book_list_query)


# delete single book from database
@app.route("/book_delete", methods=["GET", "POST"])
def book_delete():
    if request.method == "GET":
        return render_template("book_delete.html")
    
    # else POST
    book_title = request.form.get("book_title")

    # .strip() removes tabs and spaces before and after a string
    book_title = book_title.strip()

  # book list  
    book_list_query=User.query.with_entities(User.book_title, User.book_status).distinct()

    # check for book title input
    if not book_title:
        return render_template("book_list.html", message="Book title missing!", book_status=BOOK_STATUS, books=book_list_query)
    
    # check if book title is in database to be able to delete
    exists = User.query.filter_by(book_title=book_title).first()
    if not exists:
        return render_template("book_list.html", message="Book title does not exist!", book_status=BOOK_STATUS, books=book_list_query)

    # else valid book title
    selected_book = User.query.filter_by(book_title=book_title).first()
    db.session.query(User).filter(User.id==selected_book.id).delete()
    db.session.commit()
    # return redirect("/book_list")
    return render_template("list.html", message=None, book_status=BOOK_STATUS, books=book_list_query)


# delete entire db database
@app.route("/book_list_delete")
def book_list_delete():
    db.session.query(User).delete()
    db.session.commit()
    return redirect("/list")

# book list and list are essentially the same, with book list handling error messages
# book list
@app.route("/book_list", methods=["GET", "POST"])
def book_list():
    book_list_query=User.query.with_entities(User.book_title, User.book_status).distinct()

    # maybe dont need get and post statements, just return template with status and books
    if request.method == "GET":
        return render_template("list.html", book_status=BOOK_STATUS, books=book_list_query)
    
    # else POST
    return render_template("list.html", books=book_list_query)


# clean book list with no warnings
@app.route("/list", methods=["GET", "POST"])
def list():
    book_list_query=User.query.with_entities(User.book_title, User.book_status).distinct()

    # maybe dont need get and post statements, just return template with status and books
    if request.method == "GET":
        return render_template("list.html", book_status=BOOK_STATUS, books=book_list_query)
    
    # else POST
    return render_template("list.html", books=book_list_query)

# about page
@app.route("/about")
def about():
    return render_template("about.html")

# TODO
# cookies? session


if __name__ == "__application__":
    app.run(debug=True)
    db.create_all()