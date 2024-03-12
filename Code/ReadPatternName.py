import re

def crear_archivos_por_patron(archivo_entrada):
    # Abre el archivo de texto de entrada
    with open(archivo_entrada, 'r') as file:
        texto = file.read()

    # Define la expresión regular para buscar el patrón "Pattern X"
    patron = r'Pattern \d+'
    patrones_encontrados = list(re.finditer(patron, texto))  # Convertir a lista

    # Itera sobre los patrones encontrados
    for i, match in enumerate(patrones_encontrados, start=1):
        # Obtiene la posición del inicio y final del patrón encontrado
        inicio_patron = match.start()
        fin_patron = match.end()

        # Extrae el patrón encontrado
        patron_encontrado = match.group()

        # Busca el siguiente patrón o el final del texto
        if i < len(patrones_encontrados):
            siguiente_match = patrones_encontrados[i]
            fin_siguiente_patron = siguiente_match.start()
        else:
            fin_siguiente_patron = len(texto)

        # Extrae la información entre los patrones
        informacion_entre_patrones = texto[fin_patron:fin_siguiente_patron].strip()

        # Crea un archivo para cada patrón encontrado
        nombre_archivo_salida = f"patron_{i}.txt"
        with open(nombre_archivo_salida, 'w') as file:
            # Escribe el patrón encontrado y la información entre patrones en el archivo
            file.write(f"{patron_encontrado}\n")
            file.write(informacion_entre_patrones)

    print(f"Se crearon {i} archivos con los patrones encontrados y la información entre ellos.")

# Llama a la función para procesar el archivo de entrada
crear_archivos_por_patron(r'Output/Patterns_name.txt')
