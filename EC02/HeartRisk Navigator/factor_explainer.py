import math
import numpy as np
from typing import Dict, List
from risk_predictor import cargar_caracteristicas_json, cargar_modelo, predecir_riesgo, MODEL_PATH


def obtener_estimador_principal(modelo):
    if hasattr(modelo, "steps"):
        return modelo.steps[-1][1]
    return modelo


def explicacion_por_cada_factor(paciente: Dict[str, float], model_path: str = MODEL_PATH, top_k: int = 3):
    features = cargar_caracteristicas_json()
    modelo = cargar_modelo(model_path)
    estimador = obtener_estimador_principal(modelo)

    if not hasattr(estimador, "coef_"):
        raise AttributeError("El estimador cargado no tiene coeficientes (coef_).")

    coefs = estimador.coef_.ravel()

    # Calcula las contribuciones de cada parámetro
    contribuciones = []
    for i in range(len(features)):
        feat = features[i]
        coef = coefs[i]
        valor = float(paciente[feat])
        contrib = coef * valor

        if contrib > 0:
            direccion = "Incrementa"
        elif contrib < 0:
            direccion = "Disminuye"
        else:
            direccion = "Neutral"

        contribuciones.append({
            "feature": feat,
            "signed_contribution": contrib,
            "direction": direccion,
            "score": abs(contrib)
        })

    # Ordenar por impacto
    contribuciones.sort(key=lambda x: x["score"], reverse=True)

    # Calcula la probabilidad con el modelo
    pred = predecir_riesgo(paciente, model_path=model_path)
    prob = pred["probability"]

    # Recomendaciones generales a partir de los parámetros de cada paciente
    recomendaciones = []

    if paciente["ejection_fraction"] < 40:
        recomendaciones.append("Tiene fracción de eyección baja, debería realizarse un control cardiológico y fármacos")
    else:
        recomendaciones.append("Tiene la fracción de eyección normal, se recomienda ejercicio moderado")

    if paciente["serum_sodium"] < 135:
        recomendaciones.append("Debido a que tiene el sodio bajo, consulte sobre el control de diuréticos")
    else:
        recomendaciones.append("Tiene un porcentaje de sodio correcto")

    if paciente["serum_creatinine"] > 1.5:
        recomendaciones.append("Creatinina elevada, posible disfunción renal. Realice un control médico")
    else:
        recomendaciones.append("Creatinina normal, manténgase hidratado")

    if paciente["age"] > 70:
        recomendaciones.append("Realice chequeos más frecuentemente")
    else:
        recomendaciones.append("Tiene una edad y salud favorable")

    # Construcción del texto
    lineas = []
    prob_pct = prob * 100
    lineas.append(f"Probabilidad de muerte en relación con varios parámetros asociados a la insuficiencia cardíaca: {prob_pct:.1f}%")
    lineas.append("Factores más influyentes:")
    for c in contribuciones[:top_k]:
        lineas.append(f" - {c['feature']}: {c['direction']} el riesgo.")

    lineas.append("Recomendaciones en general:")
    for r in recomendaciones:
        lineas.append(f"- {r}")

    explicacion_texto = "\n".join(lineas)

    return {
        "probability": prob,
        "contributions": contribuciones,
        "explanation_text": explicacion_texto,
        "recommendations": recomendaciones
    }
