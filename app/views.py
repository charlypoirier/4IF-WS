from app import app
from flask import render_template, request, jsonify


@app.route("/",  methods=['GET', 'POST'])
def index():
    data = {'a': "hello_world 1", 'b': 'hello_world 2','c':'hello world 3'}
    if request.method == 'POST' :
        language = request.form.get('language')
        framework = request.form['framework']
        data['language'] = language
        data['framework'] = framework
    return render_template("index.html", data=data)

@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)


@app.route('/query-example')
def query_example():
    parameter = request.args.get('param') #if key doesn't exist, returns None
    return '''<h1>The param value is: {}</h1>
              '''.format(parameter)

@app.route("/about")
def about():
    return "All about Flask"

