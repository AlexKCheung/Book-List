# Flask-Web-App
Full-stack web application that allows users to track books to read and books that they finished reading. 

Using the Flask web framework, Bootstrap, Python, HTML, CSS, SQLite, and Jinja.

Currently trying to deploy online

### How to run on local environment: 
- set FLASK_APP=application.py 
- python -m flask run   

With debug mode on: 
- set FLASK_APP=application.py
- set FLASK_DEBUG=1
- python -m flask run

Routes run locally should be at: 127.0.0.1:5000/

### Files: 
- application.py: Main chunck of program. 
- requirements.txt: other libraries used in app
- static/: static files like images, CSS files, etc.
- templates/: HTML templates

book_add.html, book_delete.html, book_failure.html, book_success.html can be deleted, code can be changed to reroute to these pages instead of keeping all the functionality on the list page. 

### Book List Ideas (for myself)
- everyone can log in and make an account 
- uses the New York Times' Books API 
-   search book, check if it is a NYT Best Seller
-   search book, check reviews
- use book display API, maybe 
- log in/out?