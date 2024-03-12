// diagramaOntologies.js

// Función para cargar y mostrar el diagrama ontológico desde un archivo de texto
function cargarDiagramaOntologico() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'diagrama_ontologico.txt', true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var diagrama = document.getElementById('ontologia-diagrama');
            diagrama.textContent = xhr.responseText; // Asigna el contenido del archivo al elemento
        }
    };
    xhr.send();
}

cargarDiagramaOntologico();