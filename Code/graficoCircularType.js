// Funcion para generar un color aleatorio en formato RGBA
function colorAleatorio() {
    var r = Math.floor(Math.random() * 256);
    var g = Math.floor(Math.random() * 256);
    var b = Math.floor(Math.random() * 256);
    return "rgba(" + r + "," + g + "," + b + ", 0.7)";
}

function CargarDatosType(){
    var xhr = new XMLHttpRequest();
    xhr.open('GET','patter2Prueba.txt',true);
    xhr.onreadystatechange = function(){
        if(xhr.readyState === 4 && xhr.status === 200){
            // REGEX para detectar el texto a eliminar (?<eliminar>^Ontologies.*appears)
            var lineas = xhr.responseText.split(';');
            var etiquetas = [];
            var datos = [];
            lineas.forEach(function (linea){
                var partes = linea.split('(');
                etiquetas.push(partes[0]);
                datos.push(parseInt(partes[1]));           
            });
            crearGraficoType(etiquetas, datos);
        }  
    };
    xhr.send();
}
// Función para actualizar el gráfico con nuevos datos
function crearGraficoType(etiquetas, datos) {
    let ctx2 = document.getElementById("identificador2_js").src.match(/\w+=\w+/g);
    ctx2 = ctx2[0].replace(/\w+=/g,"");
    
    // Crear el nuevo gráfico
    var coloresFondo = [];
    datos.forEach(function () {
        coloresFondo.push(colorAleatorio());
    });

    new Chart(ctx2, {
        type: 'pie',
        data: {
            labels: etiquetas,
            datasets: [{
                label: 'Patrones',
                data: datos,
                backgroundColor: coloresFondo,
                borderColor: coloresFondo,
                borderWidth: 1
            }]
        },
        options: {
            responsive: false, // Desactiva la capacidad de respuesta
            
        }
    });
}

CargarDatosType();


