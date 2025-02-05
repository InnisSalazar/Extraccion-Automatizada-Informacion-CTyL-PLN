from pdf2image import convert_from_path
import pytesseract

OCR_CONFIG = "--oem 3 --psm 6 -l spa"

def extraer_texto_imagen(pdf_path):
    """
    Procesa un archivo PDF y extrae texto usando OCR.

    :param file_path: Ruta del archivo PDF.
    :return: Texto extraído.
    """
    paginas = convert_from_path(pdf_path, 300)  # 300 es la resolución de la imagen
    
    texto_completo = ""
    for pagina in paginas:
        texto_completo += pytesseract.image_to_string(pagina, lang="spa", config=OCR_CONFIG)
    
    return texto_completo.replace("\n", " ")  # Eliminar saltos de línea innecesarios
