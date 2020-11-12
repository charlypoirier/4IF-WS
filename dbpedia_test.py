from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery("""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?label
    WHERE { <http://dbpedia.org/resource/Asturias> rdfs:label ?label }
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    print(result["label"]["value"])

print('---------------------------')

for result in results["results"]["bindings"]:
    print('%s: %s' % (result["label"]["xml:lang"], result["label"]["value"]))

#Select  ?auteur2 (count(?s) as ?commonsubject)
#WHERE {
# ?auteur rdf:type dbo:Writer.
# ?auteur rdfs:label "Victor Hugo"@en.
# ?auteur2 rdf:type dbo:Writer.
# ?auteur rdf:type ?s.
# ?auteur2 rdf:type ?s.
# FILTER(?auteur != ?auteur2)
#}
#Group by ?auteur2
#ORDER BY DESC (?commonsubject)


#PREFIX dcterms: <http://purl.org/dc/terms/>
#PREFIX dc: <http://purl.org/dc/elements/1.1/>
#PREFIX foaf: <http://xmlns.com/foaf/0.1/>
#PREFIX bio: <http://vocab.org/bio/0.1/>
#
#SELECT distinct ?ovr ?titre ?autrenom
#WHERE {
#  	?ovr dcterms:contributor ?auteur.
#    ?ovr dcterms:title ?titre.
#    ?ovr dcterms:creator ?autreauteur .
#    ?ovr dcterms:description ?desc .
#	?autreauteur foaf:name ?autrenom.
#  	{
#	SELECT ?auteur ?nom
#	WHERE {
#		?oeuvre dcterms:creator ?auteur.
#		?auteur bio:birth ?date1.
#		?auteur bio:death ?date2.
#		OPTIONAL {?auteur foaf:name ?nom.}
#		FILTER(regex(?nom,".*Victor Hugo.*", "i"))
#	}
#    LIMIT 1
#  }
#}
#LIMIT 100
































