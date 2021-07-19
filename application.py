from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html", name=request.args.get("name"))


if __name__ == "__application__":
    app.run(debug=True)