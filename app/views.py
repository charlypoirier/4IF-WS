from app import app
from flask import render_template


@app.route("/")
def index():
    data = {'a': "hello_world 1", 'b': 'hello_world 2','c':'hello world 3'}
    return render_template("index.html", data=data)

@app.route("/about")
def about():
    return "All about Flask"

