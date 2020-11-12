from app import app
from flask import render_template, request, jsonify
from SPARQLWrapper import SPARQLWrapper, JSON
from .bnf_requests import hugo_sample_req, generic, getAuteurs, getAuthorsDetail, getAuthorsBooks


@app.route("/")
def root():
    return render_template("search.html")


@app.route("/index",  methods=['GET', 'POST'])
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

@app.route("/search", methods=["GET", "POST"])
def search():
    datalist = []
    if request.method == 'POST':
        print(request.form)
        field = request.form.get('strqry')
        print("\n\n\n")
        print(field)
        print("\n\n\n")
        datalist = getAuteurs(field) 
        for item in datalist:
            print(item)
        print("\n\n\n")
    return render_template("search.html", datalist=datalist)


@app.route("/author/<name>")
def author(name):
    print(request.form)
    name = name.replace('_',' ')
    dateMort=""
    if "dMort" in request.args:
        dateMort = request.args["dMort"]
        print("\n\nYes "+name+" date Mort : "+dateMort+"\n\n")
    else:
        print("\n\nNo date Mort\n\n")
    datalist = []
    datalist = getAuthorsDetail(name, dateMort)
    """ datalist.append(getAuthorsBooks(name)) """
    for item in datalist:
        print("\n\nItem!!\n")
        print(item)
    print("\n\n\n")
    return render_template("author.html", datalist=datalist, name=name)
