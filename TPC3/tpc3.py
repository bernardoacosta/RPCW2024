import json

dataset = open("mapa-virtual.json")
bd = json.load(dataset)
dataset.close()


city = ""
for cidade in bd["cidades"]:
    city+=f"""
    
###  http://rpcw.di.uminho.pt/2024/mapa-virtual#{cidade["id"]}
:{cidade["id"]} rdf:type owl:NamedIndividual ,
             :cidade ;
    :descricao "{cidade["descrição"]}" ;
    :distrito "{cidade["distrito"]}" ;
    :id "{cidade["id"]}" ;
    :nome "{cidade["nome"]}" ;
    :populacao {cidade["população"]} .
    """
    
for ligacao in bd["ligacoes"]:
    city+=f"""
    
###  http://rpcw.di.uminho.pt/2024/mapa-virtual#{ligacao["id"]}
:{ligacao["id"]} rdf:type owl:NamedIndividual ,
             :ligacao ;
    :destino :{ligacao["destino"]} ;
    :origem :{ligacao["origem"]} ;
    :distancia {ligacao["distância"]} ;
    :id "{ligacao["id"]}" .
"""

mapa_virtual = open("mapa-virtual.ttl", 'a')
mapa_virtual.write(city)
mapa_virtual.close()