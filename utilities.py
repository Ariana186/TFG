import os
import csv
from flask import current_app,url_for

def image_exists(image_path):
    return os.path.exists(image_path)

# Función para crear el HTML de PatternType y PatternName
def read_and_process_patterns(filename, csv_data):
    path = os.path.join(current_app.root_path, 'data', filename)
    pattern_content_type = ""
    pattern_content_type_aux = ""
    found_owl_class_section = False
    number_of_patterns = 0

    try:
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
            patterns = content.split("Pattern ")
            if patterns[0] == '':
                patterns.pop(0)

            
            number_of_patterns = len(patterns)

            for index, pattern in enumerate(patterns, start=1):
                pattern_key = f"Pattern {index}"
                lines = pattern.split('\n')
                found_owl_class_section = False
                pattern_content_type_aux = ""
                for line in lines:
                    line = line.strip()
                    if line.startswith(str(index)):
                        pattern_content_type += f"<section id='{pattern_key}' class='pt-3 px-5'><div class='container'>"
                        pattern_content_type += f"<h1>{pattern_key}</h1>"
                    elif line.startswith("Ontologies in which it appears"):
                        found_owl_class_section = True
                        pattern_content_type += "<p>\n"
                    elif found_owl_class_section and line:
                        pattern_content_type += line + "\n"
                    if "Times" in line or "Different ontologies" in line:
                        pattern_content_type_aux += line + "\n"

                pattern_content_type += "\n" + pattern_content_type_aux 

                # Concatenar texto del CSV que sea del patrón correspondiente
                if pattern_key in csv_data:
                    for csv_row in csv_data[pattern_key]:
                        pattern_content_type += f"\nEstructuras en las que aparece:\n\n" + "\n".join(csv_row[3:]) + "\n"
                else:
                    pattern_content_type += "\nNo CSV data found for this pattern.\n"

                if filename == "Patterns_type.txt":# Verificar y añadir imagen
                    image_file = f"Pattern {index}.svg"
                    image_path = os.path.join(current_app.root_path, 'static', 'images', image_file)
                    if image_exists(image_path):
                        pattern_content_type += f'\n<img src="{url_for("static", filename=f"images/{image_file}")}" alt="img type {pattern_key}" />'
                    else:
                        pattern_content_type += '<p>No image available for this pattern.</p>'

                pattern_content_type +="</p></div></section>"


    except FileNotFoundError:
        pattern_content_type = "File not found."

    return pattern_content_type, number_of_patterns

   
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


# Función para crear el HTML de Structure
def read_and_process_file_structure(filename):
    path = os.path.join(current_app.root_path, 'data', filename)
    try:
        with open(path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        processed_content = ""
        processed_content_aux = ""
        foundFirstParagraph = False
        foundLineHeader = False

        for line in lines:
            line = line.strip()
      
            if line.startswith("Ontology"):
                ontology_name = line.split(":")[1].strip()
                processed_content_aux = f"<p>Ontología Detectada: {ontology_name}</p>"
                foundFirstParagraph = True
            elif foundFirstParagraph:  
                if line.startswith("Structure:"):
                    structure_type = line.split(":")[1].strip()
                    processed_content += f"<h1>{structure_type}</h1><h3>Estructura Tipo:</h3>"
                    foundLineHeader = True
                elif foundLineHeader and line:
                    processed_content += line + "<br>"
                elif line == "":
                    processed_content += "<br>"+processed_content_aux
                    foundFirstParagraph = False
                    foundLineHeader = False
                
        
        return processed_content
    except FileNotFoundError:
        return "Archivo no encontrado."
    
#Función para crear la Tabla de contenidos
def create_table_of_contents(num_pattern):

    table_of_contents = f"""<div class='row'>
      <div id='toc' class='col-3 pt-4 d-none d-xl-block bg-light px-5'>
        <div class='container'>
          <h4 class='text-secondary pb-2'>Table of Contents</h4>
        </div>
        <div id='toc-ontologists'>"""
    
    for pattern_number in range(1, num_pattern + 1):
        table_of_contents += f"<p><a href='#Pattern {pattern_number}'>Pattern {pattern_number}</a></p>"
    
    table_of_contents += f"""</div>
      </div>
    </div>"""      
        
    return table_of_contents