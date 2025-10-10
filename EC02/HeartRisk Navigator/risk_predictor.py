import json
import os
import joblib
import numpy as np
from typing import Dict, List, Optional

# Rutas principales del modelo y resultados
MODEL_PATH = "modelo_logistico_heart_failure.joblib"
RESULTS_JSON = "resultados_modelo_logistico.json"


def cargar_caracteristicas_json(path: str = RESULTS_JSON):
    # Lee el archivo JSON 
    if not os.path.exists(path):
        raise FileNotFoundError(f"No se encontró el archivo: {path}")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("features", [])

# Carga el modelo entrenado
def cargar_modelo(path: str = MODEL_PATH):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Modelo no encontrado en: {path}")
    return joblib.load(path)

# Convierte el diccionario del paciente en un vector con en el orden correcto
def convertir_paciente_a_vector(paciente: Dict[str, float], orden_features: List[str]):
    faltantes = [f for f in orden_features if f not in paciente]
    if faltantes:
        raise ValueError(f"Faltan variables en el paciente: {faltantes}")
    valores = [paciente[f] for f in orden_features]
    return np.array(valores, dtype=float).reshape(1, -1)

# Predice la probabilidad de DEATH_EVENT para los pacientes
def predecir_riesgo(paciente: Dict[str, float], model_path: str = MODEL_PATH, orden_features: Optional[List[str]] = None, umbral: float = 0.5) -> Dict:
    modelo = cargar_modelo(model_path)
    if orden_features is None:
        orden_features = cargar_caracteristicas_json()

    X = convertir_paciente_a_vector(paciente, orden_features)
    
    # Verificar si el modelo permite obtener probabilidades para poder usarlo
    try:
        prob_muerte = modelo.predict_proba(X)[0, 1]
    except AttributeError:
        prob_muerte = float(modelo.predict(X)[0])

    resultado = {
        "probability": float(prob_muerte),
        "label": int(prob_muerte >= umbral),
        "feature_order": orden_features
    }
    return resultado
