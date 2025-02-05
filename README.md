# **Extracción Automatizada de Información en Certificados de Tradición y Libertad con Procesamiento del Lenguaje Natural**

Este repositorio contiene el desarrollo de una solución integral para la extracción automatizada de información en Certificados de Tradición y Libertad, utilizando Procesamiento del Lenguaje Natural (PLN) y técnicas de Reconocimiento Óptico de Caracteres (OCR).

## **Descripción del Proyecto**  

El proyecto está compuesto por tres componentes principales:

### **1. Preprocesamiento y Extracción de Datos**  
- Procesamiento masivo de documentos PDF con OCR.  
- Conversión de documentos en imágenes y aplicación de Tesseract para extraer el texto.  
- Limpieza y estructuración de datos en archivos CSV para análisis posterior.  

### **2. Modelo de PLN para Reconocimiento de Entidades**  
- Basado en **BERT en español** con ajuste fino para identificar información relevante.  
- Entrenado con datos anotados en formato BIO para mejorar la precisión en la extracción de entidades.  
- Implementado con **Transformers (Hugging Face)** y **PyTorch**.  

### **3. API de Extracción de Datos**  
- Implementada con Flask y Docker.  
- Utiliza OCR y modelos de PLN para procesar documentos en formato PDF.  
- Contiene una interfaz web para carga y visualización de resultados.  

## **Estructura del Proyecto**  

### **API**  
```
project/
├── backend/                   # Código del backend
│   ├── src/
│   │   ├── app.py             # Configuración principal de la app Flask
│   │   ├── routes/
│   │   │   └── upload.py      # Rutas para la carga de archivos
│   │   ├── utils/
│   │   │   ├── ocr.py         # Funciones relacionadas con OCR
│   │   │   ├── ner.py         # Funciones relacionadas con NER
│   │   │   └── extract.py     # Funciones para extraer y limpiar datos
│   │   └── models/            # Carpeta donde se guarda el modelo
│   │       └── modelo         # Modelo BERT
│   ├── requirements.txt       # Lista de dependencias de Python
│   ├── Dockerfile             # Configuración para Docker del backend
│   └── main.py                # Punto de entrada del backend
│
├── frontend/                  # Código del frontend
│   ├── templates/             # Carpeta para las plantillas HTML
│   │   └── index.html         # Interfaz principal
│   └── static/                # Carpeta para archivos estáticos
│       ├── css/
│       │   └── styles.css     # Estilos CSS
│       └──  js/
│           └── scripts.js     # Lógica de interacción del frontend
│
├── uploads/                   # Carpeta para archivos temporales
├── docker-compose.yml         # Archivo de orquestación para Docker
└── README.md                  # Documentación del proyecto
```

### **Archivos Adicionales**  
Además de la API, en la raíz del repositorio se encuentran los siguientes archivos relacionados con el modelo y el procesamiento de datos:  

- **Extracción de características de documentos.ipynb**  
- **Desarrollo de modelo BERT.ipynb** 

Estos notebooks contienen el código utilizado para el entrenamiento del modelo de PLN y el procesamiento de documentos.  

## **Tecnologías Utilizadas**  
- **Python** (Flask, Transformers, PyTorch, Pandas, Tesseract OCR)  
- **Docker** (Contenerización de la API)  
- **Git LFS** (Almacenamiento de modelos grandes)  
- **Google Colab** (Entrenamiento del modelo PLN)  

## **Documentación**  
Para más detalles sobre cada componente, se pueden consultar los siguientes archivos:  

- **[README de la API](API%20Extracción%20de%20Datos%20desde%20PDFs/README.md)** 
- **Documentación del Modelo y Procesamiento de Datos en los notebooks**  

---

Este proyecto busca mejorar la eficiencia en la gestión de documentos notariales a través del uso de herramientas de inteligencia artificial y procesamiento del lenguaje natural.
