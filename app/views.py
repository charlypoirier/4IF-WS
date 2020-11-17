from app import app
from flask import render_template, request, jsonify
from SPARQLWrapper import SPARQLWrapper, JSON
from .bnf_requests import getBookDetailBnf, getBooksDetail, getBooks, getAuthorsDetail, getAuthorsBooks, getRelatedAuthors, getAuteurs2, getResumeBnfUri

# Page principale avec la recherche générique
@app.route("/")
def root():
    return render_template("search.html")

@app.route("/search", methods=["GET", "POST"])
def search():
    results = []
    if request.method == "POST":
        searchType = request.form.get("searchType")
        query = request.form.get("query")
        if searchType == "author":
            results = getAuteurs2(query)
        else:
            results = getBooks(query)
    return render_template("search.html", results=results, type=searchType)

# Page de détails d'un auteur
@app.route("/author/<name>")
def author(name):
    name = name.replace("_", " ")
    dateBirth = ""
    if "dBirth" in request.args:
        dateBirth = request.args["dBirth"]
    results = getAuthorsDetail(name, dateBirth)
    if len(results) == 0:
        results = [{}] 
    relatedAuthors = getRelatedAuthors(name) 
    books = getAuthorsBooks(name)
    return render_template("author.html", details=results[0], name=name, relatedAuthors = relatedAuthors, books = books)

# Page de détails d'un livre
@app.route("/ABook/<titre>")
def bookDetail(titre):
    name = titre
    name = name.replace('_', ' ')
    results = getBooksDetail(name)
    if len(results) == 0:
        results = [{}]
    return render_template("book.html", details=results[0], name=name)

# Page de détails d'un livre
@app.route("/ABookBnf/<titre>")
def bookDetailBnf(titre):
    name = titre
    name = name.replace('_', ' ')
    bookURI = ""
    if "uri" in request.args:
        bookURI = request.args["uri"]
    results = getBookDetailBnf(name, bookURI)
    if len(results) == 0:
        results = [{}]
    else:
        abstractdict =  { "value" : getResumeBnfUri(bookURI)}
        results[0]["resume"] = abstractdict
    print( "bookDetailBnfStart" )
    print(results)
    return render_template("book.html", details=results[0], name=name)
