## 📊 Análisis Exploratorio de Datos (EDA) - Compatibilidad de Roommates

## 📋 Descripción General
Este proyecto realiza un análisis exploratorio de datos sobre preferencias de convivencia para identificar compatibilidades entre potenciales roommates. El dataset contiene 750 registros con 15 variables relacionadas con hábitos, personalidad y preferencias de estilo de vida.

## 🎯 Objetivo Principal
Identificar relaciones significativas entre variables categóricas usando pruebas de Chi-cuadrado y visualizar los patrones de compatibilidad mediante gráficos de barras y barras apiladas

## 🔧 Características Principales
- Análisis Chi-cuadrado entre variables categóricas y el v de Cramer para determinar la fuerza de la relación en caso de existir
- Visualizaciones con gráficos de barras y barras apiladas
- Cálculo de poder estadístico

## 🔧 Metodología Implementada
1. Preparación de Datos
Carga y verificación del dataset

Selección de variables relevantes para análisis de compatibilidad

Transformación de variables categóricas

Ordenamiento categórico para privacy_importance


Agrupación de social_energy_rating en categorías: "Unsocial", "Neutral", "Very Social"
## 📊 Resultados
Se identificaron relaciones significativas entre las variables profession y room_type_preference.

## 📈 Hallazgos Clave
El análisis revela patrones de compatibilidad en:

profession y room_type_preference.

work_shift y dietary_restrictions

bedtime y dietary_restrrictions

## 🛠️ Tecnologías

- Python
- Pandas
- Scipy
- Matplotlib

##  Análisis Estadístico 

# Chi-cuadrado

###  Cálculo de correlaciones entre variables categóricas
```
chi2, p_value, dof, expected = chi2_contingency(tabla_contingencia)
```
Propósito: Determinar si existe relación estadísticamente significativa entre pares de variables categóricas.

Interpretación:

p-value < 0.05: Relación significativa

p-value ≥ 0.05: No hay evidencia de relación

# V de Cramer
La V de Cramér es una medida de asociación entre dos variables categóricas que va de 0 a 1, donde:

0 = No hay asociación entre las variables

1 = Asociación perfecta entre las variables

```
v_cramer = np.sqrt(chi2 / (n * (min(tabla_contongencia.shape) - 1)))
```

Interpretación

0.00 - 0.10:    Asociación nula o muy débil 

0.10 - 0.20:    Asociación débil 

0.20 - 0.30:    Asociación moderada 

0.30 - 0.40:    Asociación relativamente fuerte 

0.40 - 0.50:    Asociación fuerte 

0.50 - 1.00:    Asociación muy fuerte a perfecta 

## 📊 Poder Estadístico

El cálculo del poder estadístico complementa el análisis Chi-cuadrado, determinando la probabilidad de detectar efectos reales en la población, considerando:

Tamaño de muestra (n=750)

Nivel de significancia (α=0.05)

Tamaño del efecto observado


Este enfoque asegura que las correlaciones identificadas sean tanto estadísticamente significativas como prácticamente relevantes para la toma de decisiones sobre compatibilidad de roommates.

---

> **Autores**

> 1. Aldrin Chávez
> 2. Kevin Sánchez
> 3. Daniela Analuisa
---