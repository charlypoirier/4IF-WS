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

    """ print(results) """
    oeuvres = []
    for result in results["results"]["bindings"]:
        oeuvres.append(result["title"]["value"])
        oeuvres.append(result["date"]["value"])
        oeuvres.append(result["language"]["value"])
        
    return oeuvres

   
# Requête pour obtenir les détails d'un auteur
def getAuthorsDetail(authorName, dateBirth):
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")

    dateBirth = '"'+dateBirth+'"'
    """print("Pour Mr/Mme "+authorName+", la date de naissance est:"+dateBirth+":")"""
    requestDate = ""
    if dateBirth != "":
        requestDate = """?auteur dbo:birthDate ?date
        FILTER(substr(str(?date),1,4) = """+dateBirth+""" )"""

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
            ?oeuvre rdfs:label ?titre.
            FILTER(LANG(?titre) = "" || LANGMATCHES(LANG(?titre), "fr"))
            #OPTIONAL { ?oeuvre dbp:title ?titre }
            #OPTIONAL { ?oeuvre dbp:name ?titre }
            #OPTIONAL { ?oeuvre foaf:name ?titre }
            OPTIONAL{ ?oeuvre dbo:abstract ?resume }
            OPTIONAL{ ?oeuvre dbp:genre ?genre }
            OPTIONAL{ ?oeuvre dbo:literaryGenre ?genreUri.
                        ?genreUri rdfs:label ?genre.
                        FILTER(LANG(?genre) = "" || LANGMATCHES(LANG(?genre), "fr")) }
            OPTIONAL{ ?oeuvre dbo:language ?langueUri.
                        ?langueUri rdfs:label ?langue.
                        FILTER(LANG(?langue) = "" || LANGMATCHES(LANG(?langue), "fr")) }
            OPTIONAL{ ?oeuvre dbo:publisher ?publicateur }
            OPTIONAL{ ?oeuvre foaf:depiction ?image }
            FILTER(LANG(?resume) = "" || LANGMATCHES(LANG(?resume), "fr"))
            FILTER(regex(?nom, """ + rgxqry + """))
        } GROUP BY ?resume
        LIMIT 20
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
        
    return(results["results"]["bindings"])

# Requête pour obtenir les détails d'un livre
def getBooksDetail(bookName):
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")

    print("getBookDetail - Recherche du livre "+bookName)
    """ rgxqry = '".*{0}.*"'.format(bookName) """
    rgxqry = '"{0}"'.format(bookName)

    sparql.setQuery("""
        PREFIX dbp: <http://dbpedia.org/property/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX dbo: <http://dbpedia.org/ontology/>
        SELECT  ?oeuvre ?auteur ?authorName ?authorBirth ?titre ?resume ?langue ?genreLabel ?genre ?publicateur ?image WHERE {
            ?auteur rdf:type foaf:Person.
            ?oeuvre dbo:author ?auteur.
            ?oeuvre rdfs:label ?titre .
            #?oeuvre rdfs:label """+rgxqry+""" .

            OPTIONAL { ?auteur rdfs:label ?authorName.
                         FILTER(LANG(?authorName) = "" || LANGMATCHES(LANG(?authorName), "fr"))}
            OPTIONAL { ?auteur dbo:birthDate ?authorBirth.}
            #OPTIONAL { ?oeuvre dbp:title ?titre }
            #OPTIONAL { ?oeuvre dbp:name ?titre }
            #OPTIONAL { ?oeuvre foaf:name ?titre }
            OPTIONAL{ ?oeuvre dbo:abstract ?resume 
                    FILTER(LANG(?resume) = "" || LANGMATCHES(LANG(?resume), "fr"))}
            OPTIONAL{ ?oeuvre dbp:genre ?genreLabel . }
                        #?genre rdfs:label ?genreLabel}
            OPTIONAL{ ?oeuvre dbo:literaryGenre ?genreUri.
                        ?genreUri rdfs:label ?genre
                        FILTER(LANG(?genre) = "" || LANGMATCHES(LANG(?genre), "fr"))}
            OPTIONAL{ ?oeuvre dbo:language ?langueUri.
                      ?langueUri rdfs:label ?langue. 
                      FILTER(LANG(?langue) = "" || LANGMATCHES(LANG(?langue), "fr"))}
            OPTIONAL{ ?oeuvre dbo:publisher ?publicateurUri .  
                      ?publicateurUri rdfs:label ?publicateur 
                      FILTER(LANG(?publicateur) = "" || LANGMATCHES(LANG(?publicateur), "fr"))}
            OPTIONAL{ ?oeuvre foaf:depiction ?image }
            #FILTER(regex(str(?titre), """ + rgxqry + """, "i"))
            FILTER((str(?titre) = """ + rgxqry + """))
        } GROUP BY ?resume
        LIMIT 1
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    datalist = results["results"]["bindings"]
    if len(datalist) == 0:
        datalist = [{}]
    else:
        datalist = datalist[0]

    if "authorBirth" in datalist:
        date = datalist["authorBirth"]["value"].split("-")
        datalist["authorBirth"]["value"] = date
        
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
        SELECT ?nom ?oeuvresDerivees ?genre WHERE {
            ?auteur rdf:type foaf:Person ;
            foaf:name ?nomAuteur.
            ?oeuvre dbo:author ?auteur.
            ?oeuvresDerivees dbo:basedOn ?oeuvre.
            OPTIONAL { ?oeuvre dbp:name ?nom }
            OPTIONAL { ?oeuvre foaf:name ?nom }
            OPTIONAL { ?oeuvre dbp:title ?nom }
            OPTIONAL { ?oeuvre dbp:genre ?genre }
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
        SELECT DISTINCT ?auteur2 ?nom ?birth ?occupation (count(?s) as ?compatibilite) 
        WHERE {
            ?auteur rdf:type dbo:Writer.
            ?auteur rdfs:label """ + authorName + """@fr.
            ?auteur2 rdf:type dbo:Writer.
            ?auteur rdf:type ?s.
            ?auteur2 rdf:type ?s.
            ?auteur2 rdfs:label ?nom.
            ?auteur2 dbo:birthDate ?birth.
            ?auteur2 dbp:occupation ?occupation.
            FILTER(LANG(?nom) = "" || LANGMATCHES(LANG(?nom), "fr"))
            #FILTER LangMatches(lang(?nom), 'fr')
            FILTER(?auteur != ?auteur2)

        } 
        ORDER BY DESC (?compatibilite) 
        LIMIT 20
    """) 

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert() 
       
    datalist = results["results"]["bindings"]

    auteurs= set()
    resultats=[]
    i=0
    for auteur in datalist:
        taille = len(auteurs)
        if "birth" in datalist[i] and taille <10:
            date = datalist[i]["birth"]["value"].split("-")
            datalist[i]["birth"]["value"] = [date[0]]
            auteurs.add(str(datalist[i]["nom"]["value"])+str(datalist[i]["birth"]["value"]))
            if (len(auteurs) == taille+1):
                resultats.append(datalist[i])
        i=i+1
    """ print("\nLes auteurs sans doublolns sont:")
    print(auteurs)
    print("\n") """

    return(resultats)
    

# Requête pour obtenir une liste de livres selon des mots-clés
def getBooks(bookName):
    sparql = SPARQLWrapper("https://data.bnf.fr/sparql")
    
    rgxqry = '".*{0}.*"'.format(bookName)
    
    sparql.setQuery("""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX dcterms: <http://purl.org/dc/terms/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX bnf-onto: <http://data.bnf.fr/ontology/bnf-onto/>
        PREFIX rdaw: <http://rdaregistry.info/Elements/w/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
		PREFIX rdam: <http://rdaregistry.info/Elements/m/>
        
        SELECT ?uri (SAMPLE(?title) as ?title) (SAMPLE(?date) AS ?publicationDate)  (SAMPLE(?authorName) AS ?authorName) 
        WHERE {
            ?book rdaw:P10004 <http://data.bnf.fr/vocabulary/work-form/te> ;
			dcterms:creator ?author ;
            rdfs:label ?title ;
            dcterms:date ?date.
            ?uri foaf:focus ?book.
            OPTIONAL { ?book dcterms:language ?language }
            
            ?author rdf:type foaf:Person ;
            foaf:name ?authorName ;
            bnf-onto:firstYear ?birth.
            OPTIONAL { ?author bnf-onto:lastYear ?death }
            FILTER(regex(?title, """ + rgxqry + """, "i"))
        }
        GROUP BY ?uri ?date
        ORDER BY ASC(?date)
        LIMIT 50
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    return(results["results"]["bindings"])

def getBookDetailBnf(bookName, uri):
    sparql = SPARQLWrapper("https://data.bnf.fr/sparql")
    
    rgxqry = '".*{0}.*"'.format(bookName)
    
    sparql.setQuery(""" 
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX rdaw: <http://rdaregistry.info/Elements/w/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdam: <http://rdaregistry.info/Elements/m/>
    PREFIX rdarelationships: <http://rdvocab.info/RDARelationshipsWEMI/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX bnf-onto: <http://data.bnf.fr/ontology/bnf-onto/>
     
    SELECT DISTINCT  ?titre ?authorNameBnf ?birth ?death ?publicationDate ?publicateur ?pages ?langue ?resume
    WHERE {
        
        <""" + uri + """> foaf:focus ?Oeuvre .
        ?edition    rdarelationships:workManifested ?Oeuvre.
        ?Oeuvre     dcterms:creator     ?author.
        ?author     foaf:name           ?authorNameBnf.
        ?edition    dcterms:date        ?publicationDate.
        ?author     bnf-onto:firstYear  ?birth.
        OPTIONAL {?edition  dcterms:language    ?langueUri. ?langueUri <http://www.w3.org/2004/02/skos/core#altLabel> ?langue }
        OPTIONAL {?author   bnf-onto:lastYear   ?death      }
        OPTIONAL {?edition  dcterms:title       ?titre      }
        OPTIONAL {?edition  dcterms:publisher   ?publicateur}
        OPTIONAL {?edition  dcterms:abstract    ?resume     }
        OPTIONAL {?edition  dcterms:description ?pages      }
            
            FILTER (regex(?publicationDate,"^[0-9]+$"))
            } 

            ORDER BY (?publicationDate)
            LIMIT 100
        
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    return(results["results"]["bindings"])
    
def getAuteurs2(authorName): 
    
    sparql = SPARQLWrapper("https://data.bnf.fr/sparql")
    rgxqry = '".*{0}.*"'.format(authorName)

    sparql.setQuery( """
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
        SELECT ?nom ?fnom ?birth ?death ?bio (count(?edition) as ?relevance)
        WHERE {
        	?oeuvre dcterms:creator ?auteur.
            ?auteur rdf:type foaf:Person.
            ?auteur bnf-onto:firstYear ?birth.
            OPTIONAL {?auteur foaf:name ?nom.}
            OPTIONAL {?auteur foaf:familyName ?fnom.}
            OPTIONAL {?auteur bnf-onto:lastYear ?death }
            ?auteur rdagroup2elements:biographicalInformation ?bio. 
            ?a foaf:focus ?oeuvre .
            ?edition rdarelationships:workManifested ?oeuvre.
        
            FILTER	( regex(?nom, """ +rgxqry + """ , "i") ||  regex(?fnom, """ +rgxqry + """, "i") )
        }
        ORDER BY DESC (count(?edition))
        LIMIT 100
        """ )
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return(results["results"]["bindings"])


def getResumeBnfUri(uri): 
    sparql = SPARQLWrapper("https://data.bnf.fr/sparql")

    sparql.setQuery("""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX bnf-onto: <http://data.bnf.fr/ontology/bnf-onto/>
    PREFIX rdaw: <http://rdaregistry.info/Elements/w/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdam: <http://rdaregistry.info/Elements/m/>
    PREFIX rdarelationships: <http://rdvocab.info/RDARelationshipsWEMI/>
    SELECT ?resume 
    WHERE {
    <""" + uri + """>   foaf:focus ?book.
    ?book rdaw:P10004 <http://data.bnf.fr/vocabulary/work-form/te>.
    ?book rdfs:label ?titre.
    ?publication rdam:P30135 ?book.
    ?publication dcterms:abstract ?resume 
    }
    ORDER BY DESC (strlen(str(?resume)))
    LIMIT 1
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if(len(results["results"]["bindings"]) == 0):
        return ""
    else:
        return(results["results"]["bindings"][0]["resume"]["value"])







