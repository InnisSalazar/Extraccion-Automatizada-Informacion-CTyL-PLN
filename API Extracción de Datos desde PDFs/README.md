# Extracción de Datos desde PDFs con NER y OCR

Este proyecto implementa un sistema para la extracción automatizada de datos desde archivos PDF utilizando OCR (Reconocimiento Óptico de Caracteres) y NER (Reconocimiento de Entidades Nombradas). Está diseñado para procesar documentos, detectar entidades relevantes y devolver resultados estructurados.

## **Características**
- Procesamiento de archivos PDF utilizando `pytesseract` y `pdf2image`.
- Reconocimiento de entidades mediante un modelo preentrenado de `transformers`.
- Interfaz web interactiva para cargar documentos y ver resultados.
- Contenerización con Docker para un despliegue rápido y sencillo.
- Eliminación automática de los archivos cargados tras el procesamiento para garantizar un almacenamiento limpio.

---

## **Tecnologías Utilizadas**
### **Backend**
- **Flask**: Framework para manejar rutas y lógica del servidor.
- **Tesseract OCR**: Motor para reconocimiento óptico de caracteres.
- **Transformers**: Modelo NER para detección de entidades.

### **Frontend**
- **HTML/CSS**: Estructura y diseño básico de la interfaz.
- **JavaScript**: Lógica del cliente, incluyendo interacción con el backend y manipulación del DOM.
- **Bootstrap**: Estilo y diseño responsivo.

### **Contenerización**
- **Docker**: Para contenerizar la aplicación.
- **Docker Compose**: Orquestación de servicios, incluyendo el backend.

---

## **Estructura del Proyecto**

```plaintext
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
---

## **Instalación**

### **Requisitos Previos**
- **Docker** y **Docker Compose** instalados.

### **Instrucciones**

#### **1.** Clona el repositorio
```bash
git clone <URL-del-repositorio> - REVISAR
cd project
```

#### **2.** Construir y ejecutar con Docker
```bash
docker-compose up --build
```

#### **3.** Acceder a la aplicación
Abre tu navegador y visita: http://localhost:5000.

---
## **Uso**

#### **1.** Sube uno o más archivos PDF utilizando el formulario de carga.
#### **2.** Los archivos serán procesados automáticamente.
#### **3.** Navega entre los resultados detectados o descárgalos en formato Excel.

---