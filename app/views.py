from app import app
from flask import render_template, request, jsonify
from SPARQLWrapper import SPARQLWrapper, JSON
from .bnf_requests import hugo_sample_req, generic, getAuteurs, getAuthorsDetail, getAuthorsBooks

# Page principale avec la recherche générale
@app.route("/")
def root():
    return render_template("search.html")

@app.route("/search", methods=["GET", "POST"])
def search():
    auteurs = []
    if request.method == "POST":
        query = request.form.get("query")
        auteurs = getAuteurs(query)
    return render_template("search.html", results=auteurs)

# Page de détails d'un auteur
@app.route("/author/<name>")
def author(name):
    name = name.replace("_", " ")
    dateMort = ""
    if "dMort" in request.args:
        dateMort = request.args["dMort"]
    results = getAuthorsDetail(name, dateMort)
    if len(results) == 0:
        results = [{}]
    return render_template("author.html", details=results[0], name=name)
