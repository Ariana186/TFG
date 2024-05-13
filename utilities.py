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

# Función para crear el HTML de PatternType y PatternName
def read_and_process_patterns(filename, csv_data):
    path = os.path.join(current_app.root_path, 'data', filename)
    pattern_content_type = ""
    pattern_content_type_aux = ""
    found_owl_class_section = False
    header_list = []

    try:
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
            patterns = content.split("Pattern ")
            if not patterns[0] :
                patterns.pop(0)


            for index, pattern in enumerate(patterns, start=1):
                pattern_key = f"Pattern {index}"
                header_list.append(pattern_key)
                lines = pattern.split('\n')
                found_owl_class_section = False
                pattern_content_type_aux = ""
                for line in lines:
                    line = line.strip()
                    if line.startswith(str(index)):
                        if index==1:
                           pattern_content_type += f"<h4 id='{pattern_key}'>{pattern_key}</h4>" 
                        else:
                            pattern_content_type += f"<h4 id='{pattern_key}'class='pt-5'>{pattern_key}</h4>"
                    elif line.startswith("Ontologies in which it appears"):
                        found_owl_class_section = True
                        pattern_content_type += "<p><code>"
                    elif found_owl_class_section and line:
                        pattern_content_type += line + "<br>"
                    elif "Times" in line or "Different ontologies" in line:
                        pattern_content_type_aux += line + "<br>"

                pattern_content_type += "<br></code>" + pattern_content_type_aux +"</p>"

                # Concatenar texto del CSV que sea del patrón correspondiente
                if pattern_key in csv_data:
                    for csv_row in csv_data[pattern_key]:
                        pattern_content_type += f"""<p>Estructuras en las que aparece:
                        <ol>"""
                        ontologie = ""
                        for structure in csv_row[3:]:
                            if structure.split("-")[0] == ontologie:
                                pattern_content_type+=f"<li>{structure}</li>"
                            else:
                               if ontologie:
                                    pattern_content_type+=f"""                        </ul>
                                """
                               ontologie = structure.split("-")[0]
                               pattern_content_type+=f"""<br><span class='black-letter'><li>{ontologie}</li></span>
                        <ul>
                            <li>{structure}</li>"""
                    pattern_content_type+=f"""                        </ul>
                        </ol>
                    </p>"""
                else:
                    pattern_content_type += "\nNo CSV data found for this pattern.\n"

                # Verificar y añadir imagen
                if filename == "Patterns_type.txt":
                    image_file = f"{pattern_key}.svg"
                    image_path = os.path.join(current_app.root_path, 'static', 'images', image_file)
                    if image_exists(image_path):
                        pattern_content_type += f"""<br><a href="{url_for("static", filename=f"images/{image_file}")}" data-fancybox>
                        <img src="{url_for("static", filename=f"images/{image_file}")}" alt="img type {pattern_key}" /></a>"""
                    else:
                        pattern_content_type += '<p>No image available for this pattern.</p>'

    except FileNotFoundError:
        pattern_content_type = "File not found."

    return pattern_content_type,header_list

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
                    processed_content += "<code>"+line + "</code><br>"
                elif line == "":
                    structure_list.update({structure_key:processed_content})
                    foundFirstParagraph = False
                    foundLineHeader = False
                
    except FileNotFoundError:
            return "Archivo no encontrado." 
    return structure_list


# Función para crear el HTML de Structure
def read_and_process_file_structure(filename,structure_blank_nodes_list):
    path = os.path.join(current_app.root_path, 'data', filename)
    try:
        with open(path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        processed_content = ""
        processed_content_aux = ""
        header_list = []
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
                    
                    if len(header_list)==0:
                        processed_content += f"""<h4 id='{structure_type}'>{structure_type}</h4>"""
                    else:
                        processed_content += f"""<h4 id='{structure_type}' class="pt-3">{structure_type}</h4>"""
                    processed_content += f"""<table class="table table-bordered align-middle pt-3">
                        <thead>
                            <tr>
                                <th scope="col" style="width: 50%;">Structure Term Inferred Type</th>
                                <th scope="col" style="width: 50%;">Structure Term Inferred Blank Nodes</th>
                            </tr>
                        </thead>
                            
                        <tbody>
                            <tr>
                                <td>"""
                    foundLineHeader = True
                    header_list.append(structure_type)
                elif foundLineHeader and line:
                    processed_content +="<code>"+ line + "</code><br>"
                elif line == "":
                    processed_content += f"""</td>
                                <td>{structure_blank_nodes_list[structure_type]}</td>
                        </tbody>
                    </table>
                    """
                    processed_content += "<p>"+processed_content_aux+"</p></details>"
                    foundFirstParagraph = False
                    foundLineHeader = False
                
    except FileNotFoundError:
            return "Archivo no encontrado." 
    return processed_content, header_list

 
#Función para crear la Tabla de contenidos 
def create_table_of_contents(header_list):

    table_of_contents = f"""<div id='toc' class='col-3 pt-4 d-none d-xl-block bg-light px-5'>
        <div class='container'>
          <h4 class='options text-secondary pb-2'>Table of Contents</h4>"""
    
    for structure in header_list:
        table_of_contents += f"<p><a href='#{structure}'>{structure}</a></p>"
    
    table_of_contents += f"""</div>
      </div>"""    
        
    return table_of_contents