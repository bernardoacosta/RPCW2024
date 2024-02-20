import json

# Load JSON data from file
with open("plantas.json", "r") as f:
    bd = json.load(f)
    f.close()

# Initialize a set for unique individuals
individuals_set = set()

# Initialize TTL string
ttl = ""

# Loop through each tree in the database
for arvore in bd:
    # Replace spaces and other characters to create valid IDs
    def format_id(value):
        return value.replace(" ", "_")

    # Generate unique identifiers for repeated properties and add them if they are not already in the set
    properties = {
        'Caldeira': arvore['Caldeira'],
        'Código de rua': str(arvore['Código de rua']),
        'Gestor': arvore['Gestor'],
        'Freguesia': arvore['Freguesia'],
        'Espécie': arvore['Espécie'],
        'Nome Científico': arvore['Nome Científico'],
        'Origem': arvore['Origem'],
        'Data de actualização': arvore['Data de actualização'],
        'Data de Plantação': arvore['Data de Plantação'],
        'Implantação': arvore['Implantação'],
        'Local': arvore['Local'],
        'Rua': arvore['Rua'],
        'Tutor': arvore['Tutor'],
        'Número de intervenções': str(arvore['Número de intervenções']),
    }

    for prop, value in properties.items():
        if value:  # Skip empty values
            prop_id = format_id(value)
            prop_type = prop.replace(" ", "_")
            if prop_id not in individuals_set:
                ttl += f"""
###  http://rpcw.di.uminho.pt/2024/plantas#{prop_id}
:{prop_id} rdf:type owl:NamedIndividual ,
              :{prop_type} .
"""
                individuals_set.add(prop_id)

    # Generate the tree individual with references to the unique property individuals
    ttl += f"""
###  http://rpcw.di.uminho.pt/2024/plantas#20615557{arvore['Id']}
<http://rpcw.di.uminho.pt/2024/plantas#{arvore['Id']}> rdf:type owl:NamedIndividual ,
                                                      :Arvore ;
                                             :temCaldeira :{format_id(arvore['Caldeira'])} ;
                                             :temCodigoRua :{format_id(str(arvore['Código de rua']))} ;
                                             :temDataAtualizacao :{format_id(arvore['Data de actualização'])} ;
                                             :temDataPlantacao :{format_id(arvore['Data de Plantação'])} ;
                                             :temEspecie :{format_id(arvore['Espécie'])} ;
                                             :temEstado :{arvore['Estado']} ;
                                             :temFreguesia :{format_id(arvore['Freguesia'])} ;
                                             :temGestor :{format_id(arvore['Gestor'])} ;
                                             :temImplantacao :{format_id(arvore['Implantação'])} ;
                                             :temLocal :{format_id(arvore['Local'])} ;
                                             :temNomeCientifico :{format_id(arvore['Nome Científico'])} ;
                                             :temNumeroIntervencoes :{format_id(str(arvore['Número de intervenções']))} ;
                                             :temOrigem :{format_id(arvore['Origem'])} ;
                                             :temRua :{format_id(arvore['Rua'])} ;
                                             :temTutor :{format_id(arvore['Tutor'])} ;
                                             :id "{arvore['Id']}"^^xsd:int ;
                                             :numRegisto "{arvore['Número de Registo']}"^^xsd:int .
"""


print(ttl)

