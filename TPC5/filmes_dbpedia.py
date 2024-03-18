import requests
import json

# Define the DBpedia SPARQL endpoint
sparql_endpoint = "http://dbpedia.org/sparql"

# Updated SPARQL query to get names instead of URIs and handle grouping
sparql_query = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?film ?name (GROUP_CONCAT(DISTINCT ?actorLabel; SEPARATOR=", ") AS ?actors) (GROUP_CONCAT(DISTINCT ?producerLabel; SEPARATOR=", ") AS ?producers) (GROUP_CONCAT(DISTINCT ?writerLabel; SEPARATOR=", ") AS ?writers) (GROUP_CONCAT(DISTINCT ?musicLabel; SEPARATOR=", ") AS ?musics)
WHERE {{
    ?film a dbo:Film .
    OPTIONAL {{?film foaf:name ?name . FILTER(LANG(?name) = 'en')}}
    OPTIONAL {{?film dbo:starring ?actor . ?actor rdfs:label ?actorLabel .}}
    OPTIONAL {{?film dbo:producer ?producer . ?producer rdfs:label ?producerLabel .}}
    OPTIONAL {{?film dbo:writer ?writer . ?writer rdfs:label ?writerLabel .}}
    OPTIONAL {{?film dbp:music ?music . ?music rdfs:label ?musicLabel .}}
    FILTER (LANG(?actorLabel) = 'en' || !BOUND(?actorLabel))
    FILTER (LANG(?producerLabel) = 'en' || !BOUND(?producerLabel))
    FILTER (LANG(?writerLabel) = 'en' || !BOUND(?writerLabel))
    FILTER (LANG(?musicLabel) = 'en' || !BOUND(?musicLabel))
}}
GROUP BY ?film ?name
"""

# Define the headers
headers = {
    "Accept": "application/sparql-results+json"
}

# Define the parameters
params = {
    "query": sparql_query,
    "format": "json"
}

# Send the SPARQL query using requests
response = requests.get(sparql_endpoint, params=params, headers=headers)

# Process and save the results
if response.status_code == 200:
    results = response.json()
    filmes = []
    for result in results["results"]["bindings"]:
        filme = {
            "uri": result["film"]["value"],
            "nome": result["name"]["value"] if "name" in result else "Unknown",
            "atores": result["actors"]["value"].split(", ") if "actors" in result else [],
            "realizadores": result["producers"]["value"].split(", ") if "producers" in result else [],
            "escritores": result["writers"]["value"].split(", ") if "writers" in result else [],
            "musicos": result["musics"]["value"].split(", ") if "musics" in result else []
        }
        filmes.append(filme)

    with open("filmes.json", "w") as f:
        json.dump(filmes, f, ensure_ascii=False, indent=4)
else:
    print("Error:", response.status_code)
    print(response.text)


