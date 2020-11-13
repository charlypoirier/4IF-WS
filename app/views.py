from app import app
from flask import render_template, request, jsonify
from SPARQLWrapper import SPARQLWrapper, JSON
from .bnf_requests import hugo_sample_req, generic, getAuteurs, getBooksDetail, getAuthorsDetail, getAuthorsBooks, getRelatedAuthors, getAuteurs2

# Page principale avec la recherche générique
@app.route("/")
def root():
    return render_template("search.html")

@app.route("/search", methods=["GET", "POST"])
def search():
    auteurs = []
    if request.method == "POST":
        query = request.form.get("query")
        auteurs = getAuteurs2(query)
    return render_template("search.html", results=auteurs)

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
    "print(relatedAuthors)"
    books = getAuthorsBooks(name)
    """ print(books) """
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

# Page de détails d'un livre - Test
@app.route("/book")
def book():
    name = "La Peste"
    name = name.replace('_', ' ')
    results = getBooksDetail(name)
    if len(results) == 0:
        results = [{}]
    return render_template("book.html", details=results[0], name=name)
