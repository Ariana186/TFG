# Ontology Visualization Web Application

## DESCRIPCIÓN

Esta aplicación web permite la visualización y análisis de modelos ontológicos. Utiliza Flask como framework de backend y Jinja2 para la renderización de plantillas HTML. La aplicación procesa datos de archivos CSV, TXT y SVG para generar las vistas HTML.

## INSTALACIÓN

### 1.Clona el repositorio

```bash
git clone https://github.com/Ariana186/TFG.git
```

### 2.Crea y activa un entorno virtual

```bash
python -m venv env
source env/bin/activate  # En Windows usa `env\\Scripts\\activate`
```

### 3.Instala las dependencias

```bash
pip install -r requirements.txt
```

## USO

1. Asegúrate de tener los archivos de datos necesarios en los directorios correspondientes:
   -/data
   -Patterns_name.csv
   -Patterns_name.txt
   -Patterns_type.csv
   -Patterns_type.txt
   -Structure_term_inferred_blank_nodes.txt
   -Structure_term_inferred_type.txt

-/static/imagenes - Listado de las imágenes Pattern X.svg

2. Ejecuta la aplicación Flask:

```bash
python app.py
```

3. Abre tu navegador web y navega a http://127.0.0.1:5000 para interactuar con la aplicación.
