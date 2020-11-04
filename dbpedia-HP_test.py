from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery("""
    PREFIX dbr: <http://dbpedia.org/resource/> 
    PREFIX dbp: <http://dbpedia.org/property/> 
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    SELECT ?start, ?end, count(?mid) AS ?distance WHERE {
        ?start a dbo:Book; dbo:series dbr:Harry_Potter; dbo:subsequentWork* ?mid. 
        ?mid a dbo:Book; dbo:series dbr:Harry_Potter; dbo:subsequentWork+ ?end. 
        ?end a dbo:Book; dbo:series dbr:Harry_Potter.
    }
    GROUP BY ?start ?end
    ORDER BY ASC(?start) ASC(?distance)
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
print(results)


for result in results["results"]["bindings"]:
    print("Start : ", result["start"]["value"])
    print("End : ", result["end"]["value"])
    print("Distance : ", result["distance"]["value"])
    print("----------------------")

