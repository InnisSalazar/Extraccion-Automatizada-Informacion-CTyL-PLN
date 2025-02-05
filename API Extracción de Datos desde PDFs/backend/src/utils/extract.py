import re
from src.utils.ocr import extraer_texto_imagen
from src.utils.ner import aplicar_ner, resaltar_entidades, unificar_entidades


def limpiar_texto(texto):
    """
    Limpia el texto eliminando fragmentos no deseados y normalizando el formato.

    :param texto: Texto sin procesar.
    :return: Texto limpio.
    """
    patrones = [
        r"\d{1,2}/\d{1,2}/\d{2}, \d{1,2}:\d{2} [ap]\.m\.\s*-\s*VUR",  # Encabezados
        r"https://www\.vur\.gov\.co/portal/pages/vur/inicio\.jsf\?url=[^ ]+",  # Pies de página
        r"%%datosBasicosTierras \d+/\d+",  # Bloques no deseados
        r"VUR%2F%23%2F%3Ftipo%3D[^ ]+"  # Variaciones de URLs codificadas
    ]
    
    # Eliminar URLs y patrones específicos
    for pattern in patrones:
        texto = re.sub(pattern, "", texto)
    
    texto = re.sub(r"\d{1,2}/\d{1,2}/\d{1,2}, \d{1,2}:\d{2} Consultas VUR", "", texto)
    texto = re.sub(r"(?<=\s)\d+/\d+(?=\s|\b|$)(?!/\d{4})", "", texto)  # Elimina solo números de página
    
    # Eliminar líneas vacías o exceso de espacios
    texto = re.sub(r"\s+", " ", texto).strip()
    
    return texto

def extraer_dato(texto, inicio, fin):
    """
    Extrae texto entre dos delimitadores.

    :param texto: Texto de entrada.
    :param inicio: Delimitador inicial.
    :param fin: Delimitador final.
    :return: Texto extraído.
    """
    texto = texto.replace("N?", "N°").replace("N*", "N°").replace(" N ", "N°").replace("N°Matrícula", "N° Matricula").replace("Matricula", "Matrícula").replace("Inmobiliaria", "Inmobiliaría")
    start = texto.find(inicio)
    if start == -1:
        return None
    start += len(inicio)
    end = texto.find(fin, start)
    if end == -1:
        return texto[start:].strip()
    return texto[start:end].strip()

def extraer_datos(texto):
    """
    Extrae datos relevantes del texto procesado y aplica NER.

    :param texto: Texto limpio.
    :return: Diccionario con datos extraídos.
    """
    fecha = extraer_dato(texto, "Fecha:", "Hora:") or "Información no contenida en el documento"
    hora = extraer_dato(texto, "Hora:", "No. Consulta:") or "Información no contenida en el documento"
    consulta = extraer_dato(texto, "No. Consulta:", "N° Matrícula Inmobiliaría:") or "Información no contenida en el documento"
    matricula = extraer_dato(texto, "N° Matrícula Inmobiliaría:", "Referencia Catastral:") or "Información no contenida en el documento"
    referencia_catastral = extraer_dato(texto, "Referencia Catastral:", "Departamento:") or "Información no contenida en el documento"
    departamento = extraer_dato(texto, "Departamento:", "Referencia Catastral Anterior:") or "Información no contenida en el documento"
    referencia_catastral_anterior = extraer_dato(texto, "Referencia Catastral Anterior:", "Municipio:") or "Información no contenida en el documento"
    municipio = extraer_dato(texto, "Municipio:", "Cédula Catastral:") or "Información no contenida en el documento"
    cedula_catastral = extraer_dato(texto, "Cédula Catastral:", "Vereda:") or "Información no contenida en el documento"
    vereda = extraer_dato(texto, "Vereda:", "Nupre:") or "Información no contenida en el documento"
    nupre = extraer_dato(texto, "Nupre:", "Dirección Actual del Inmueble") or "Información no contenida en el documento"
    direccion_actual = extraer_dato(texto, "Dirección Actual del Inmueble:", "Direcciones Anteriores") or "Información no contenida en el documento"
    direcciones_anteriores = extraer_dato(texto, "Direcciones Anteriores:", "Determinacion:") or "Información no contenida en el documento"
    determinacion = extraer_dato(texto, "Determinacion:", "Destinacion economica:") or "Información no contenida en el documento"
    destinacion_economica = extraer_dato(texto, "Destinacion economica:", "Modalidad:") or "Información no contenida en el documento"
    modalidad = extraer_dato(texto, "Modalidad:", "Fecha de Apertura del Folio:") or "Información no contenida en el documento"
    fecha_apertura_folio = extraer_dato(texto, "Fecha de Apertura del Folio:", "Tipo de Instrumento:") or "Información no contenida en el documento"
    tipo_instrumento = extraer_dato(texto, "Tipo de Instrumento:", "Fecha de Instrumento:") or "Información no contenida en el documento"
    fecha_instrumento = extraer_dato(texto, "Fecha de Instrumento:", "Estado Folio:") or "Información no contenida en el documento"
    estado_folio = extraer_dato(texto, "Estado Folio:", "Matrícula(s) Matriz:") or "Información no contenida en el documento"
    matricula_matriz = extraer_dato(texto, "Matrícula(s) Matriz:", "Matrícula(s) Derivada(s):") or "Información no contenida en el documento"
    matricula_derivada = extraer_dato(texto, "Matrícula(s) Derivada(s):", "Tipo de Predio:") or "Información no contenida en el documento"
    tipo_predio = extraer_dato(texto, "Tipo de Predio:", "Alertas") or "Información no contenida en el documento"
    complementaciones = extraer_dato(texto, "Complementaciones", "Cabidad y Linderos") or "Información no contenida en el documento"
    cabidad_linderos = extraer_dato(texto, "Cabidad y Linderos", "Linderos Tecnicamente Definidos") or "Información no contenida en el documento"
    linderos_tec_definidos = extraer_dato(texto, "Linderos Tecnicamente Definidos", "Area Y Coeficiente") or "Información no contenida en el documento"

    # Aplicar NER a Cabidad y Linderos
    entidades_resaltadas = aplicar_ner(cabidad_linderos)

    # Unificar y tomar el último valor de 'AREA_H'
    valores_area_h = unificar_entidades(entidades_resaltadas, "AREA_H")
    entidades_area_h = valores_area_h[-1] if valores_area_h else "Información no contenida en el documento"

    # Unificar y tomar el último valor de 'AREA_M'
    valores_area_m = unificar_entidades(entidades_resaltadas, "AREA_M")
    entidades_area_m = valores_area_m[-1] if valores_area_m else "Información no contenida en el documento"

    # Resaltar las entidades en el texto
    cabidad_linderos_resaltado = resaltar_entidades(cabidad_linderos, entidades_resaltadas)

    # Crear un diccionario con todos los datos extraídos
    return {
        "Fecha": fecha,
        "Hora": hora,
        "No. Consulta": consulta,
        "Matrícula Inmobiliaria": matricula,
        "Referencia Catastral": referencia_catastral,
        "Referencia Catastral Anterior": referencia_catastral_anterior,
        "Cédula Catastral": cedula_catastral,
        "Departamento": departamento,
        "Municipio": municipio,
        "Vereda": vereda,
        "Nupre": nupre,
        "Dirección Actual del Inmueble": direccion_actual,
        "Direcciones Anteriores": direcciones_anteriores,
        "Determinacion": determinacion,
        "Destinacion economica": destinacion_economica,
        "Modalidad": modalidad,
        "Fecha de Apertura del Folio": fecha_apertura_folio,
        "Tipo de Instrumento": tipo_instrumento,
        "Fecha de Instrumento": fecha_instrumento,
        "Estado Folio": estado_folio,
        "Matricula(s) Matriz": matricula_matriz,
        "Matricula(s) Derivada(s)": matricula_derivada,
        "Tipo de Predio": tipo_predio,
        "Complementaciones": complementaciones,
        "Cabidad y Linderos": cabidad_linderos,
        "Linderos Técnicamente Definidos": linderos_tec_definidos,
        "Área (Hectáreas)": entidades_area_h,
        "Área (Metros Cuadrados)": entidades_area_m,
        "NER": cabidad_linderos_resaltado
    }

# Función para procesar un archivo
def procesar_archivo(file_path):
    """
    Procesa un archivo PDF y extrae datos estructurados.

    :param file_path: Ruta del archivo PDF.
    :return: Diccionario con datos extraídos.
    """
    texto = extraer_texto_imagen(file_path)  # Extraer texto usando OCR
    texto_limpio = limpiar_texto(texto)  # Limpiar texto
    datos = extraer_datos(texto_limpio)  # Extraer datos estructurados
    return datos


