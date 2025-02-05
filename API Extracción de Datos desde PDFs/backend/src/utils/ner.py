from transformers import AutoModelForTokenClassification, AutoTokenizer
import torch
import re

# Carga del modelo y tokenizer entrenados
modelo_ner = AutoModelForTokenClassification.from_pretrained("src/models/modelo_bert_optimizado")
tokenizer = AutoTokenizer.from_pretrained("src/models/modelo_bert_optimizado")

# Etiquetas mapeadas según el modelo
id2label = {
    0: "B-AREA_H",
    1: "B-AREA_M",
    2: "B-EXTENSION",
    3: "B-HECTAREA",
    4: "B-METROS_2",
    5: "I-AREA_H",
    6: "I-AREA_M",
    7: "I-EXTENSION",
    8: "I-HECTAREA",
    9: "I-METROS_2",
    10: "O"  # Etiqueta fuera de entidad
}

# Colores para resaltar etiquetas en HTML
colores = {
    'EXTENSION': 'rgba(169, 255, 158, 0.5)',
    'AREA_H': 'rgba(212, 56, 13, 0.5)',
    'HECTAREA': 'rgba(158, 177, 255, 0.5)',
    'AREA_M': 'rgba(255, 158, 205, 0.5)',
    'METROS_2': 'rgba(216, 158, 255, 0.5)'
}

def aplicar_ner(texto):
    """
    Aplica NER al texto proporcionado usando un modelo preentrenado.

    Args:
        texto (str): Texto en el que se buscarán entidades.

    Returns:
        list: Lista de entidades detectadas con su posición y etiqueta.
    """
    texto = texto.lower()

    # Tokenizar el texto
    tokenized_inputs = tokenizer(
        texto,
        return_tensors="pt",
        truncation=True,
        padding=True,
        return_offsets_mapping=True
    )
    offsets = tokenized_inputs.pop("offset_mapping")[0].tolist()

    # Obtener predicciones del modelo
    with torch.no_grad():
        outputs = modelo_ner(**tokenized_inputs)

    logits = outputs.logits
    predictions = torch.argmax(logits, dim=2).squeeze(0).tolist()

    # Reconstruir las entidades
    entidades_resaltadas = []
    current_entity = None

    for offset, label_id in zip(offsets, predictions):
        label = id2label[label_id]
        if offset[0] == 0 and offset[1] == 0:  # Ignorar tokens especiales
            continue

        if label != "O":  # Solo procesar entidades no "O"
            if label.startswith("B-"):
                if current_entity:
                    entidades_resaltadas.append(current_entity)
                current_entity = {"texto": texto[offset[0]:offset[1]], "etiqueta": label[2:], "start": offset[0], "end": offset[1]}
            elif label.startswith("I-") and current_entity and current_entity["etiqueta"] == label[2:]:
                current_entity["texto"] += " " + texto[offset[0]:offset[1]]
                current_entity["end"] = offset[1]
            else:
                if current_entity:
                    entidades_resaltadas.append(current_entity)
                current_entity = None

    if current_entity:
        entidades_resaltadas.append(current_entity)

    return entidades_resaltadas


def resaltar_entidades(texto, entidades_resaltadas):
    """
    Resalta entidades en el texto para su visualización en HTML.

    Args:
        texto (str): Texto original.
        entidades_resaltadas (list): Lista de entidades detectadas con posición.

    Returns:
        str: Texto con entidades resaltadas en HTML.
    """
    texto_resaltado = ""
    last_idx = 0

    for entidad in sorted(entidades_resaltadas, key=lambda x: x["start"]):
        # Agregar texto previo a la entidad
        texto_resaltado += texto[last_idx:entidad["start"]]
        # Resaltar la entidad
        color = colores.get(entidad["etiqueta"], 'rgba(255, 255, 255, 0.5)')
        texto_resaltado += f'<span class="resaltado" style="background-color: {color};">{texto[entidad["start"]:entidad["end"]]}</span>'
        # Actualizar el índice
        last_idx = entidad["end"]

    # Agregar texto restante
    texto_resaltado += texto[last_idx:]
    return texto_resaltado

def unificar_entidades(entidades, etiqueta):
    """
    Une entidades con la misma etiqueta para obtener valores consolidados.

    Args:
        entidades (list): Lista de entidades detectadas.
        etiqueta (str): Etiqueta específica a consolidar.

    Returns:
        list: Lista de valores consolidados para la etiqueta dada.
    """
    valores = []
    entidad_actual = ""
    for entidad in entidades:
        if entidad["etiqueta"] == etiqueta:
            # Concatenar el texto si pertenece a la misma etiqueta
            entidad_actual += entidad["texto"].replace(" ", "")
        else:
            # Agregar la entidad completa si termina una secuencia
            if entidad_actual:
                # Filtrar solo números
                entidad_actual = re.sub(r"[^\d.,]", "", entidad_actual)
                if entidad_actual:  # Agregar solo si no está vacío después del filtrado
                    valores.append(entidad_actual)
                entidad_actual = ""
    # Agregar la última entidad activa
    if entidad_actual:
        entidad_actual = re.sub(r"[^\d.,]", "", entidad_actual)
        if entidad_actual:
            valores.append(entidad_actual)
    return valores
