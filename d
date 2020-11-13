[1mdiff --git a/app/bnf_requests.py b/app/bnf_requests.py[m
[1mindex 8064e28..5fdda28 100644[m
[1m--- a/app/bnf_requests.py[m
[1m+++ b/app/bnf_requests.py[m
[36m@@ -374,21 +374,34 @@[m [mdef getRelatedAuthors(authorName):[m
     [m
     authorName = '"{}"'.format(authorName)[m
     sparql.setQuery("""[m
[31m-        SELECT ?auteur2 ?nom (count(?s) as ?compatibilite)[m
[32m+[m[32m        SELECT ?auteur2 ?nom ?birth (count(?s) as ?compatibilite)[m
         WHERE {[m
             ?auteur rdf:type dbo:Writer.[m
[31m-            ?auteur rdfs:label """ + authorName + """@en.[m
[32m+[m[32m            ?auteur rdfs:label """ + authorName + """@fr.[m
             ?auteur2 rdf:type dbo:Writer.[m
             ?auteur rdf:type ?s.[m
             ?auteur2 rdf:type ?s.[m
             ?auteur2 rdfs:label ?nom.[m
[31m-            FILTER(lang(?nom) = 'en')[m
[32m+[m[32m            ?auteur2 dbo:birthDate ?birth.[m
[32m+[m[32m            FILTER(lang(?nom) = 'fr')[m
             FILTER(?auteur != ?auteur2)[m
 [m
         } [m
         ORDER BY DESC (?compatibilite) [m
         LIMIT 10[m
     """) [m
[32m+[m
     sparql.setReturnFormat(JSON)[m
[31m-    results = sparql.query().convert()    [m
[32m+[m[32m    results = sparql.query().convert()[m[41m [m
[32m+[m[41m       [m
[32m+[m[32m    datalist = results["results"]["bindings"][m
[32m+[m[32m    if len(datalist) == 0:[m
[32m+[m[32m        datalist = [{}][m
[32m+[m[32m    else:[m
[32m+[m[32m        datalist = datalist[0][m
[32m+[m
[32m+[m[32m    if "birth" in datalist:[m
[32m+[m[32m        date = datalist["birth"]["value"].split("-")[m
[32m+[m[32m        datalist["birth"]["value"] = date[m
[32m+[m
     return(results["results"]["bindings"])[m
[1mdiff --git a/app/templates/author.html b/app/templates/author.html[m
[1mindex 7eb6a15..6f21809 100644[m
[1m--- a/app/templates/author.html[m
[1m+++ b/app/templates/author.html[m
[36m@@ -59,7 +59,7 @@[m
     <h2> Oeuvres de l'auteur</h2>[m
     <ul>[m
     {% for item in books  %}[m
[31m-        <li> <a href = "/ABook/{{ item["titre"]["value"]}}">{{ item["titre"]["value"]}}</a></li>[m
[32m+[m[32m        <li> <a href = "/ABook/{{ item['titre']['value']}}?nom={{name}}">{{ item["titre"]["value"]}}</a></li>[m
     {% endfor %}[m
     </ul>[m
 [m
[36m@@ -68,7 +68,7 @@[m
     <h2> Auteurs liés</h2>[m
     <ul>[m
     {% for item in relatedAuthors  %}[m
[31m-        <li> <a href = "/author/{{ item['nom']['value'].replace(' ','_')}}?dBirth=1802">[m
[32m+[m[32m        <li> <a href = "/author/{{ item['nom']['value'].replace(' ','_')}}?dBirth={{item['birth']['value'][0]}}">[m
             {{ item['nom']['value']}}[m
         </a></li>[m
     {% endfor %}[m
