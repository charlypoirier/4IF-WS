from app import app
from flask import render_template, request, jsonify
from SPARQLWrapper import SPARQLWrapper, JSON

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
        # For testing purpose :
        strqry  = request.form['strqry']
        rgxqry='\".*' +strqry +'.*\"'

        query = """
            PREFIX dbr: <http://dbpedia.org/resource/> 
            PREFIX dbp: <http://dbpedia.org/property/> 
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            PREFIX dbo: <http://dbpedia.org/ontology/>

            SELECT ?author WHERE {
                ?author a dbo:Writer .
                Filter(regex(?author,""" + rgxqry + """))
            }
        """

        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        for item in results["results"]["bindings"]:
             datalist.append(item["author"]["value"])
        print(datalist)
    return render_template("search.html", datalist=datalist)
