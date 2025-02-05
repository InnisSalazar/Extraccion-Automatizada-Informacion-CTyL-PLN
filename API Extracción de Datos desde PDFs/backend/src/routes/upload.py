import os
from flask import Blueprint, request, jsonify, render_template, send_from_directory, current_app
from concurrent.futures import ThreadPoolExecutor
from src.utils.extract import procesar_archivo

# Definir el Blueprint
upload_routes = Blueprint('upload', __name__)

# Variable global para almacenar resultados procesados
processed_results = []

@upload_routes.route('/upload', methods=['POST'])
def upload_file():
    """
    Maneja la carga de archivos y su procesamiento.
    """
    files = request.files.getlist('file')
    if not files:
        return jsonify({'error': 'No se seleccionaron archivos.'}), 400

    global processed_results
    processed_results = []

    file_paths = []

    # Guardar y validar archivos cargados
    for file in files:
        if file.filename == '':
            return jsonify({'error': 'Archivo sin nombre.'}), 400

        if file and file.filename.endswith('.pdf'):
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            file_paths.append(file_path)
        else:
            return jsonify({'error': 'Solo se permiten archivos PDF.'}), 400

    # Procesar archivos en paralelo
    with ThreadPoolExecutor(max_workers=4) as executor:  # Ajusta max_workers según tu hardware
        resultados = list(executor.map(procesar_archivo, file_paths))

    # Agregar resultados procesados y eliminar archivos temporales
    for file_path, datos in zip(file_paths, resultados):
        datos['pdf_url'] = f'/uploads/{os.path.basename(file_path)}'
        processed_results.append(datos)

    return jsonify(processed_results), 200

@upload_routes.route('/resultados/<int:index>', methods=['GET'])
def get_resultado(index):
    """
    Retorna un resultado específico basado en el índice proporcionado.
    """
    if 0 <= index < len(processed_results):
        return jsonify(processed_results[index])
    return 'Índice fuera de rango.', 404

@upload_routes.route('/')
def index():
    """
    Sirve el formulario de carga.
    """
    return render_template('index.html', resultados=None, pdf_url=None)


@upload_routes.route('/uploads/<filename>', methods=['GET'])
def uploaded_file(filename):
    """
    Sirve archivos PDF desde la carpeta de uploads.
    """
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
