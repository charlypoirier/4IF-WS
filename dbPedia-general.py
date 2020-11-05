from SPARQLWrapper import SPARQLWrapper, JSON

qry = "Hugo"
rgxqry='\".*' +qry +'.*\"'

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
print(query)

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery(query)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for item in results["results"]["bindings"]:
    print("Auteur : ", item["author"]["value"] )



#SELECT ?author WHERE {
 #  ?a a dbo:Writer .
  # ?a rdfs:label ?author .
  # ?a dbo:birthPlace dbr:France
#}

############################
# Tous les livres d'un auteur

#SELECT * WHERE {
#        ?book dbo:author <http://dbpedia.org/resource/Mark_Twain>
#}
