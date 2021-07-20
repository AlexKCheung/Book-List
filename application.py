from flask import Flask, render_template, request

app = Flask(__name__)

# basic route, index 
# default method is GET
@app.route('/') 
def index():
    # request.args for get requests
    return render_template("index.html", name=request.args.get("name", "world"))

# greeting route
@app.route("/greet", methods=["POST"])
def greet():
    # request.form for post requests
    return render_template("greet.html", name=request.form.get("name", "there"))


if __name__ == "__application__":
    app.run(debug=True)