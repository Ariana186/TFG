import os
import csv
from flask import current_app,url_for

# Función para examinar si una imagen existe en la ruta 
def image_exists(image_path):
    return os.path.exists(image_path)

# Función para leer datos de un archivo CSV y convertirlos en una lista de diccionarios
def read_csv_file(filename):
    path = os.path.join(current_app.root_path, 'data', filename)
    data = {}
    try:
        with open(path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                if row:
                    pattern_key = row[0].strip()
                    if pattern_key not in data:
                        data[pattern_key] = []
                    data[pattern_key].append(row)
    except FileNotFoundError:
        return "File not found."
    return data

# Función para leer un archivo txt y devolver un diccionario y una lista de las cabeceras
def read_and_process_patterns(filename, csv_data):
    path = os.path.join(current_app.root_path, 'data', filename)
    data = {}
    content=[]
    diagram = ""
    times=""
    ontologies=""
    csv=[]
    value_csv={}
    found_owl_class_section = False
    header_list = []

    try:
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
            patterns = content.split("Pattern ")
            if not patterns[0] :
                patterns.pop(0)

            # guardar los datos del txt
            for index, pattern in enumerate(patterns, start=1):
                pattern_key = f"Pattern {index}" 
                header_list.append(pattern_key)
                lines = pattern.split('\n')
                found_owl_class_section = False
                diagram=""
                for line in lines:
                    line = line.strip()
                    if line.startswith("Ontologies in which it appears"):
                        found_owl_class_section = True
                    elif found_owl_class_section and line:
                        diagram += line + "<br>"
                    elif "Times" in line:
                        times = line;
                    elif "Different ontologies" in line:
                        ontologies= line 
                
                # guardar el texto del csv
                csv=[]
                value_csv={}
                if pattern_key in csv_data:
                    for csv_row in csv_data[pattern_key]:
                        for structure in csv_row[3:]:
                            key = structure.split("-")[0]
                            if key not in value_csv:
                                value_csv[key] = []
                            value_csv[key].append(structure)
                    csv.append(value_csv)
                else:
                    value_csv = {"No data": ["No CSV data found for this pattern."]}

                # Verificar y añadir imagen
                if filename == "Patterns_type.txt":
                    image_file = f"{pattern_key}.svg"
                    image_path = os.path.join(current_app.root_path, 'static', 'images', image_file)
                    image_file=url_for("static", filename=f"images/{image_file}")
                    if not image_exists(image_path):
                        image_file = 'No image available for this pattern.'

                #añadir al diccionario de salida
                if filename == "Patterns_type.txt":
                    content =[diagram,times,ontologies,csv,image_file]
                    data.update({pattern_key:content})
                else:
                    content =[diagram,times,ontologies,csv]
                    data.update({pattern_key:content})
    except FileNotFoundError:
        pattern_content_type = "File not found."

    return data,header_list

# Función para leer Structure Blank Nodes
def read_and_process_file_structure_blank_nodes(filename):
    path = os.path.join(current_app.root_path, 'data', filename)
    try:
        with open(path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        processed_content = ""
        structure_key = ""
        structure_list = {}
        foundFirstParagraph = False
        foundLineHeader = False

        for line in lines:
            line = line.strip()
      
            if line.startswith("Ontology"):
                foundFirstParagraph = True
                processed_content = ""
            elif foundFirstParagraph:  
                if line.startswith("Structure:"):
                    structure_key = line.split(":")[1].strip()
                    foundLineHeader = True
                elif foundLineHeader and line:
                    processed_content += line + "<br>"
                elif line == "":
                    structure_list.update({structure_key:processed_content})
                    foundFirstParagraph = False
                    foundLineHeader = False
                
    except FileNotFoundError:
            return "File not found." 
    return structure_list


# Función leer un archivo txt y devolver un diccionario y una lista de las cabeceras
def read_and_process_file_structure(filename,structure_blank_nodes_list):
    path = os.path.join(current_app.root_path, 'data', filename)
    try:
        with open(path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        data = {}
        content=[]
        ontology_name=""
        diagram_inferred_type =""
        header_list = []
        foundFirstParagraph = False
        foundLineHeader = False

        for line in lines:
            line = line.strip()
      
            if line.startswith("Ontology"):
                ontology_name = line.split(":")[1].strip()
                foundFirstParagraph = True
            elif foundFirstParagraph:  
                if line.startswith("Structure:"):
                    structure_key = line.split(":")[1].strip()
                    foundLineHeader = True
                    header_list.append(structure_key)
                elif foundLineHeader and line:
                    diagram_inferred_type +=line + "<br>"
                elif line == "":
                    foundFirstParagraph = False
                    foundLineHeader = False
                    content =[diagram_inferred_type,structure_blank_nodes_list[structure_key],ontology_name]
                    data.update({structure_key:content})
                    diagram_inferred_type=""
                
    except FileNotFoundError:
            return "File not found." 
    return data, header_list
