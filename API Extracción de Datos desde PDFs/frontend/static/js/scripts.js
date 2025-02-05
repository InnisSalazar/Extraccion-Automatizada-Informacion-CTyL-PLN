document.addEventListener('DOMContentLoaded', () => {
    let files = [];
    let currentFileIndex = 0;
    let resultadosProcesados = [];

    const headers = [
        "Fecha", "Hora", "No. Consulta", "Matrícula Inmobiliaria", "Referencia Catastral",
        "Referencia Catastral Anterior", "Cédula Catastral", "Departamento", "Municipio", "Vereda",
        "Nupre", "Dirección Actual del Inmueble", "Direcciones Anteriores", "Determinación", 
        "Destinación Económica", "Modalidad", "Fecha de Apertura del Folio", "Tipo de Instrumento", 
        "Fecha de Instrumento", "Estado Folio", "Matricula(s) Matriz", "Matricula(s) Derivada(s)", 
        "Tipo de Predio", "Complementaciones", "Cabidad y Linderos", "Linderos Técnicamente Definidos", 
        "Área (Hectáreas)", "Área (Metros Cuadrados)"
    ];

    const loadingIndicator = document.getElementById('loading-indicator');

    function toggleLoading(show) {
        loadingIndicator.style.display = show ? 'block' : 'none';
    }



    function updateFileName() {
        const fileInput = document.getElementById('file');
        const fileNameDisplay = document.getElementById('file-name');
        files = Array.from(fileInput.files);

        if (files.length === 0) {
            fileNameDisplay.innerText = "Ningún archivo seleccionado";
            document.getElementById('prev-button').disabled = true;
            document.getElementById('next-button').disabled = true;
        } else if (files.length === 1) {
            fileNameDisplay.innerText = files[0].name;
            document.getElementById('prev-button').disabled = true;
            document.getElementById('next-button').disabled = true;
        } else {
            fileNameDisplay.innerText = `${files.length} archivos seleccionados`;
            document.getElementById('prev-button').disabled = currentFileIndex === 0;
            document.getElementById('next-button').disabled = currentFileIndex === (files.length - 1);
        }

        currentFileIndex = 0;
        mostrarResultado();
    }

    function navigateFile(direction) {
        currentFileIndex += direction;

        if (currentFileIndex < 0) currentFileIndex = 0;
        if (currentFileIndex >= resultadosProcesados.length) currentFileIndex = resultadosProcesados.length - 1;

        mostrarResultado();
    }

    function mostrarResultado() {
        const resultsContainer = document.querySelector('.results');
        const pdfContainer = document.querySelector('.pdf-container');
        const textContainer = document.querySelector('.text-container');

        if (resultadosProcesados.length === 0) {
            resultsContainer.innerHTML = '<h3 class="center mb-4">Resultados Extraídos:</h3><p>No hay resultados para mostrar.</p>';
            pdfContainer.innerHTML = '<h3 class="center mb-4">Documento PDF:</h3><p>No hay vista previa disponible para este archivo.</p>';
            textContainer.innerHTML = '<h3 class="center mb-4">Cabidad y Linderos:</h3><p>No se encontraron datos de Cabidad y Linderos.</p>';
            return;
        }

        const resultado = resultadosProcesados[currentFileIndex];

        resultsContainer.innerHTML = `
            <h3 class="center mb-4">Resultados Extraídos:</h3>
            ${headers.map(header => {
                const value = resultado[header] || 'Información no contenida';
                return `<div class="result-item">
                            <p><span class="key">${header}:</span> <span class="value">${value}</span></p>
                        </div>`;
            }).join('')}
        `;

        pdfContainer.innerHTML = `
            <h3 class="center mb-4">Documento PDF:</h3>
            ${resultado.pdf_url
                ? `<iframe src="${resultado.pdf_url}" width="100%" height="350px"></iframe>`
                : `<p>No hay vista previa disponible para este archivo.</p>`}
        `;

        textContainer.innerHTML = `
            <h3 class="center mb-4">Cabidad y Linderos:</h3>
            ${resultado['Cabidad y Linderos']
                ? `<div class="result-item"><p><span class="value">${resultado['NER']}</span></p></div>`
                : `<p>No se encontraron datos de Cabidad y Linderos.</p>`}
        `;

        // Deshabilitar botones si es necesario
        document.getElementById('prev-button').disabled = currentFileIndex === 0;
        document.getElementById('next-button').disabled = currentFileIndex === (resultadosProcesados.length - 1);
    }

    document.querySelector('form').addEventListener('submit', async (event) => {
        event.preventDefault();
        toggleLoading(true); // Mostrar indicador de carga

        const formData = new FormData(event.target);

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) throw new Error('Error al procesar los documentos');

            const data = await response.json();
            resultadosProcesados = data;

            if (resultadosProcesados.length > 0) {
                currentFileIndex = 0;
                mostrarResultado();
                document.getElementById('result-container').style.display = 'block';
            } else {
                alert('No se encontraron resultados válidos.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert(error.message || 'Error desconocido.');
        } finally {
            toggleLoading(false); // Ocultar indicador de carga
        }
    });



    function downloadExcel() {
        if (resultadosProcesados.length === 0) {
            alert("No hay datos para descargar.");
            return;
        }

        const sheetData = [headers]; // Agregar encabezados
        resultadosProcesados.forEach(resultado => {
            const row = headers.map(header => resultado[header] || "Información no contenida");
            sheetData.push(row);
        });

        const worksheet = XLSX.utils.aoa_to_sheet(sheetData);
        const workbook = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(workbook, worksheet, "Resultados");

        try {
            XLSX.writeFile(workbook, "resultados.xlsx");
        } catch (error) {
            console.error("Error al guardar el archivo:", error);
            alert("Ocurrió un error al guardar el archivo.");
        }
    }

    document.getElementById('prev-button').addEventListener('click', () => navigateFile(-1));
    document.getElementById('next-button').addEventListener('click', () => navigateFile(1));
    document.getElementById('file').addEventListener('change', updateFileName);
    document.getElementById('download-button').addEventListener('click', downloadExcel);
});
