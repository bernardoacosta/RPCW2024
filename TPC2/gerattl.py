import json


def load_data_from_json(file_path):
    with open("db.json", 'r') as file:
        data = json.load(file)
    return data


def generate_ttl_for_ontology(data):
    ttl_lines = []



    for instrument in data.get('instrumentos', []):
        ttl_lines.append(f'''
<http://rpcw.di.uminho.pt/2024/musica/Instrumento/{instrument["id"]}> rdf:type :Instrumento ;
    :temID "{instrument["id"]}" ;
    :temNome "{instrument["#text"]}" .
''')


    for curso in data.get('cursos', []):
        ttl_lines.append(f'''
<http://rpcw.di.uminho.pt/2024/musica/Curso/{curso["id"]}> rdf:type :Curso ;
    :temID "{curso["id"]}" ;
    :temNome "{curso["designacao"]}" ;
    :temDuracao "{curso["duracao"]}"^^xsd:integer ;
    :usaInstrumento <http://rpcw.di.uminho.pt/2024/musica/Instrumento/{curso["instrumento"]}#> .
''')


    for aluno in data.get('alunos', []):
        ttl_lines.append(f'''
<http://rpcw.di.uminho.pt/2024/musica/Aluno/{aluno["id"]}> rdf:type :Aluno ;
    :temID "{aluno["id"]}" ;
    :temNome "{aluno["nome"]}" ;
    :temDataNascimento "{aluno["dataNasc"]}"^^xsd:date ;
    :temAnoDeCurso "{aluno["anoCurso"]}"^^xsd:integer ;
    :tocaInstrumento <http://rpcw.di.uminho.pt/2024/musica/Instrumento/{aluno["instrumento"]}#> ;
    :estaInscrito <http://rpcw.di.uminho.pt/2024/musica/Curso/{aluno["curso"]}#> .
''')

    return '\n'.join(ttl_lines)


def main(json_file_path, ttl_file_path):
    data = load_data_from_json(json_file_path)
    ttl_content = generate_ttl_for_ontology(data)
    with open(ttl_file_path, 'a') as ttl_file:
        ttl_file.write(ttl_content)


json_file_path = 'db.json'  
ttl_file_path = 'ontology_populated.ttl'  
main(json_file_path, ttl_file_path)
