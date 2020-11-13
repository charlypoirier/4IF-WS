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

#namesresults = hugo_sample_req()
#print(namesresults)

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

def oeuvreSparql(authorName):
    sparql = SPARQLWrapper("https://data.bnf.fr/sparql")
    
    rgxqry='\".* ' +authorName +'.*\"'
    
    sparql.setQuery("""
    PREFIX bio: <http://vocab.org/bio/0.1/>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    SELECT distinct ?oeuvre ?date ?title ?language
    WHERE {
    ?oeuvre dcterms:creator ?auteur ;
            dcterms:date ?date ;
            dcterms:title ?title ; 
            dcterms:language ?language .
    ?auteur foaf:name ?nom.
    FILTER(regex(?nom,""" + rgxqry + """))
    }
    LIMIT 100
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    print(results)
    oeuvres = []
    for result in results["results"]["bindings"]:
        oeuvres.append(result["title"]["value"])
        oeuvres.append(result["date"]["value"])
        oeuvres.append(result["language"]["value"])
        
    return oeuvres

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

# Requête pour obtenir une liste d'auteurs selon des mots-clés
def getAuteurs(authorName):
    sparql = SPARQLWrapper("https://data.bnf.fr/sparql")
    
    rgxqry = '".*{0}.*"'.format(authorName)
    
    sparql.setQuery("""
        PREFIX bnf-onto: <http://data.bnf.fr/ontology/bnf-onto/>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdagroup2elements: <http://rdvocab.info/ElementsGr2/>
        PREFIX bio: <http://vocab.org/bio/0.1/>
        PREFIX dcterms: <http://purl.org/dc/terms/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdarelationships: <http://rdvocab.info/RDARelationshipsWEMI/>
        SELECT DISTINCT ?nom ?birth ?death ?bio (count(?edition) as ?count)
        WHERE {
            ?oeuvre dcterms:creator ?auteur.
            ?auteur rdf:type foaf:Person ;
            foaf:name ?nom ;
            bnf-onto:firstYear ?birth ;
            bnf-onto:lastYear ?death ;
            rdagroup2elements:biographicalInformation ?bio.
            ?a foaf:focus ?oeuvre .
            ?edition rdarelationships:workManifested ?oeuvre.
            FILTER(regex(?nom, """ + rgxqry + """, "i"))
        }
        ORDER BY DESC(?count)
        LIMIT 500
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    return(results["results"]["bindings"])
    
# Requête pour obtenir les détails d'un auteur
def getAuthorsDetail(authorName, dateMort):
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")

    dateMort = '"'+dateMort+'"'
    print("Pour Mr/Mme "+authorName+", la date de mort est:"+dateMort+":")
    requestDate = ""
    if dateMort != "":
        requestDate = """?auteur dbo:deathDate ?date
        FILTER(substr(str(?date),1,4) = """+dateMort+""" )"""

    rgxqry = '"{}"'.format(authorName)

    sparql.setQuery("""
        PREFIX dbp: <http://dbpedia.org/property/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?auteur ?nom ?bio ?school 
        ?bDate ?bPlace ?dDate ?dPlace ?bName 
        ?gender ?genre ?movement ?nationality 
        ?nationality2 ?occupation ?image 
        WHERE {
            ?auteur rdf:type foaf:Person ;
            foaf:name ?nom.
            """+requestDate+"""
            OPTIONAL{ ?auteur dbo:almaMater ?schoolT.
                    ?schoolT rdfs:label ?school
                    FILTER(LANG(?school) = "" || LANGMATCHES(LANG(?school), "fr"))  }
            OPTIONAL{ ?auteur dbo:birthDate ?bDate }
            OPTIONAL{ ?auteur dbo:birthPlace ?bPlaceT.
                    ?bPlaceT rdfs:label ?bPlace
                    FILTER(LANG(?bPlace) = "" || LANGMATCHES(LANG(?bPlace), "fr"))  }
            OPTIONAL{ ?auteur dbo:birthDate ?bDate }
            OPTIONAL{ ?auteur dbo:deathDate ?dDate }
            OPTIONAL{ ?auteur dbo:deathPlace ?dPlaceT.
                    ?dPlaceT rdfs:label ?dPlace
                    FILTER(LANG(?dPlace) = "" || LANGMATCHES(LANG(?dPlace), "fr"))  }
            OPTIONAL{ ?auteur dbo:birthName ?bName }
            OPTIONAL{ ?auteur foaf:gender ?gender }
            OPTIONAL{ ?auteur dbo:genre ?genreT.
                    ?genreT rdfs:label ?genre 
                    FILTER(LANG(?genre) = "" || LANGMATCHES(LANG(?genre), "fr"))  }
            OPTIONAL{ ?auteur dbo:movement ?movementT.
                    ?movementT rdfs:label ?movement 
                    FILTER(LANG(?movement) = "" || LANGMATCHES(LANG(?movement), "fr"))  }
            OPTIONAL{ ?auteur dbo:nationality ?nationalityT.
                    ?nationalityT rdfs:label ?nationality
                    FILTER(LANG(?nationality) = "" || LANGMATCHES(LANG(?nationality), "fr")) 
                    }
            OPTIONAL{ ?auteur dbp:nationality ?nationality2.}
            OPTIONAL{ ?auteur dbp:occupation ?occupation }
            OPTIONAL{ ?auteur foaf:depiction ?image }
            OPTIONAL{ ?auteur dbo:abstract ?bio 
                    FILTER(LANG(?bio) = "" || LANGMATCHES(LANG(?bio), "fr"))}
            FILTER(regex(?nom, """ + rgxqry + """, "i"))
        } 
        LIMIT 1
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    datalist = results["results"]["bindings"]
    if len(datalist) == 0:
        datalist = [{}]
    else:
        datalist = datalist[0]

    if "bDate" in datalist:
        date = datalist["bDate"]["value"].split("-")
        datalist["bDate"]["value"] = date
        """ datalist["bMonth"]["value"] = date[1]
        datalist["bYear"]["value"] = date[0] """
    else:
        print("no bDate...")

    if "dDate" in datalist:
        date = datalist["dDate"]["value"].split("-")
        datalist["dDate"]["value"] = date
        
    return(results["results"]["bindings"])

# Requête pour obtenir la liste des livres d'un auteur 
def getAuthorsBooks(authorName):
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")

    rgxqry = '"{}"'.format(authorName)

    sparql.setQuery("""
        PREFIX dbp: <http://dbpedia.org/property/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX dbo: <http://dbpedia.org/ontology/>
        SELECT MIN(?auteur) as ?auteur MIN(?titre) as ?titre ?resume MIN(?langue) as ?langue MIN(?genre) as ?genre MIN(?publicateur) as ?publicateur MIN(?image) as ?image WHERE {
            ?auteur rdf:type foaf:Person ;
            foaf:name ?nom.
            ?oeuvre dbo:author ?auteur.
            OPTIONAL { ?oeuvre dbp:title ?titre }
            OPTIONAL { ?oeuvre dbp:name ?titre }
            OPTIONAL { ?oeuvre foaf:name ?titre }
            OPTIONAL{ ?oeuvre dbo:abstract ?resume }
            OPTIONAL{ ?oeuvre dbp:genre ?genre }
            OPTIONAL{ ?oeuvre dbo:literaryGenre ?genre }
            OPTIONAL{ ?oeuvre dbo:language ?langue }
            OPTIONAL{ ?oeuvre dbo:publisher ?publicateur }
            OPTIONAL{ ?oeuvre foaf:depiction ?image }
            FILTER(regex(?nom, """ + rgxqry + """))
            FILTER(lang(?resume) = 'en')
        } GROUP BY ?resume
        LIMIT 20
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
        
    return(results["results"]["bindings"])

# Requête pour obtenir les détails d'un livre
def getBooksDetail(bookName):
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")

    rgxqry = '".*{0}.*"'.format(bookName)

    sparql.setQuery("""
        PREFIX dbp: <http://dbpedia.org/property/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX dbo: <http://dbpedia.org/ontology/>
        SELECT  ?oeuvre ?auteur ?titre ?authorName ?image ?langue WHERE{
            ?auteur a foaf:Person.
            ?oeuvre dbo:author ?auteur.
            ?oeuvre rdfs:label ?titre .   FILTER(regex(?titre, ".*la peste.*", "i") && lang(?titre) = 'fr').
            OPTIONAL { ?auteur foaf:name ?authorName.  }
            OPTIONAL{ ?oeuvre foaf:depiction ?image }
            OPTIONAL{ ?auteur dbo:language ?langueUri.
                      ?langueUri rdfs:label ?langue. }
        }
        LIMIT 1
    """)
    #à ajouter à la requête -> FILTER(regex(?titre, """ + rgxqry + """, "i"))
    # FILTER(lang(?resume) = 'en')
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
        
    return(results["results"]["bindings"])
    
# Requête pour obtenir des oeuvres dérivées/similaires
def getRelatedWork(workName, authorName):
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")

    workName = '"{}"'.format(workName)
    authorName = '"{}"'.format(authorName)

    sparql.setQuery("""
        PREFIX dbp: <http://dbpedia.org/property/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX dbo: <http://dbpedia.org/ontology/>
        SELECT ?nom ?oeuvresDerivees WHERE {
            ?auteur rdf:type foaf:Person ;
            foaf:name ?nomAuteur.
            ?oeuvre dbo:author ?auteur.
            ?oeuvresDerivees dbo:basedOn ?oeuvre.
            OPTIONAL { ?oeuvre dbp:name ?nom }
            OPTIONAL { ?oeuvre foaf:name ?nom }
            OPTIONAL { ?oeuvre dbp:title ?nom }
            FILTER(regex(?nom, """ + workName + """))
            FILTER(regex(?nomAuteur, """ + authorName + """))
        }
        LIMIT 20
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()    
    return(results["results"]["bindings"])
   
# Requête pour obtenir des auteurs similaires à un auteur
def getRelatedAuthors(authorName): 
    
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")
    
    authorName = '"{}"'.format(authorName)
    sparql.setQuery("""
        SELECT ?auteur2 ?nom (count(?s) as ?compatibilite)
        WHERE {
            ?auteur rdf:type dbo:Writer.
            ?auteur rdfs:label """ + authorName + """@en.
            ?auteur2 rdf:type dbo:Writer.
            ?auteur rdf:type ?s.
            ?auteur2 rdf:type ?s.
            ?auteur2 rdfs:label ?nom.
            FILTER(lang(?nom) = 'en')
            FILTER(?auteur != ?auteur2)

        } 
        ORDER BY DESC (?compatibilite) 
        LIMIT 10
    """) 
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()    
    return(results["results"]["bindings"])
