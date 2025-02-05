FROM python:3.9-slim

WORKDIR /app

# Instalar Tesseract y otras dependencias
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-spa \
    libtesseract-dev \
    poppler-utils \
    && apt-get clean

ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/5/tessdata/
ENV TOKENIZERS_PARALLELISM=false
    
COPY ./backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./backend /app
COPY ./frontend /app

EXPOSE 5000

CMD ["python", "main.py"]
