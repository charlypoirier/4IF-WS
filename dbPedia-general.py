from SPARQLWrapper import SPARQLWrapper, JSON


# Chercher les auteurs dont le nom contient la chaîne 'Hugo'
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

#########################################
# Sélectionner les auteurs nés en France.
#########################################

#SELECT ?author WHERE {
#  ?a a dbo:Writer .
# ?a rdfs:label ?author .
# ?a dbo:birthPlace dbr:France
#}

##############################
# Tous les livres d'un auteur.
##############################

#SELECT * WHERE {
#        ?book dbo:author <http://dbpedia.org/resource/Mark_Twain>
#}


##################################################
#Sélectionner les noms des auteurs et leurs livres.
##################################################

# SELECT * WHERE {
#    ?author a dbo:Writer .
#    ?book dbo:author ?author .
#    ?author rdfs:label  ?label .
#    FILTER (lang(?label) = 'en')
#    Filter(regex(?author, ".*Hugo.*"))
#}

############################################
# Auteurs appartenant au même genre qu'Hugo. 
############################################

#SELECT ?romanticAuthor WHERE {
#    ?author a dbo:Writer ; dbo:movement ?mov .
#    ?romanticAuthor a dbo:Writer ; dbo:movement ?mov .
#
#    Filter(regex(?author, ".*Hugo.*"))
#}


