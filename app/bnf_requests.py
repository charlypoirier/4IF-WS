from SPARQLWrapper import SPARQLWrapper, JSON



def hugo_sample_req():
    sparql = SPARQLWrapper("https://data.bnf.fr/sparql")
    sparql.setQuery("""
    PREFIX bio: <http://vocab.org/bio/0.1/>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    SELECT distinct ?nom ?auteur ?birth
    WHERE {
    ?oeuvre dcterms:creator ?auteur.
    ?auteur bio:birth ?birth ;
    foaf:name ?nom.
    FILTER (regex(?nom, ".* Hugo.*"))
    }
    LIMIT 100
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    names = []
    #return results["results"]["bindings"] 
    for result in results["results"]["bindings"]:
        names.append(result["nom"]["value"])
    return names


namesresults = hugo_sample_req()
print(namesresults)


def generic(name):
    sparql = SPARQLWrapper("https://data.bnf.fr/sparql")
    
    rgxqry = '".*{0}.*"'.format(name)
    
    sparql.setQuery("""
        PREFIX bio: <http://vocab.org/bio/0.1/>
        PREFIX dcterms: <http://purl.org/dc/terms/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        SELECT distinct ?nom ?auteur ?birth
        WHERE {
        ?oeuvre dcterms:creator ?auteur.
        ?auteur bio:birth ?birth ;
        foaf:name ?nom.
        FILTER(regex(?nom, """ + rgxqry + """, "i"))
        }
        LIMIT 100
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    names = []
    #return results["results"]["bindings"] 
    for result in results["results"]["bindings"]:
        names.append(result["nom"]["value"])
    return names

namesresults = hugo_sample_req()
print(namesresults)

# Nombre total d'éditions d'oeuvres d'un auteur

#PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#PREFIX dcterms: <http://purl.org/dc/terms/>
#PREFIX foaf: <http://xmlns.com/foaf/0.1/>
#PREFIX rdarelationships: <http://rdvocab.info/RDARelationshipsWEMI/>
#SELECT (count(*) as ?count)
#WHERE {
#?a foaf:focus ?Oeuvre .
#?Oeuvre dcterms:creator ?auteur .
#?auteur foaf:name ?nom.
#?edition rdarelationships:workManifested ?Oeuvre.
#OPTIONAL{?edition dcterms:date ?date}
#OPTIONAL{?edition dcterms:title ?titre}
#OPTIONAL{?edition dcterms:publisher ?editeur}
#Filter(regex(?nom, "Michel Houellebecq"))
#} 

#############################################
# Auteurs avec noms 

#PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
#PREFIX owl: <http://www.w3.org/2002/07/owl#>
#PREFIX rdagroup2elements: <http://rdvocab.info/ElementsGr2/>
#PREFIX bio: <http://vocab.org/bio/0.1/>
#PREFIX dcterms: <http://purl.org/dc/terms/>
#PREFIX foaf: <http://xmlns.com/foaf/0.1/>
#PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
#SELECT DISTINCT ?auteur ?nom ?external
#WHERE {
#?oeuvre dcterms:creator ?auteur.
#?auteur rdf:type foaf:Person.
#?auteur foaf:name ?nom.
##?auteur rdagroup2elements:biographicalInformation ?bio .
##OPTIONAL {?auteur owl:sameAs ?external }
#FILTER (regex(?nom, "Victor Hugo"))
#
#}


# PAGE DBPEDIA

#PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
#PREFIX owl: <http://www.w3.org/2002/07/owl#>
#PREFIX rdagroup2elements: <http://rdvocab.info/ElementsGr2/>
#PREFIX bio: <http://vocab.org/bio/0.1/>
#PREFIX dcterms: <http://purl.org/dc/terms/>
#PREFIX foaf: <http://xmlns.com/foaf/0.1/>
#PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
#SELECT DISTINCT ?auteur ?nom ?external
#WHERE {
#?oeuvre dcterms:creator ?auteur.
#?auteur rdf:type foaf:Person.
#?auteur foaf:name ?nom.
#OPTIONAL {?auteur owl:sameAs ?external 
#    FILTER(regex(?external,".*dbpedia.org.*"))
#  }
#FILTER (regex(?nom, "Victor Hugo"))
#}

