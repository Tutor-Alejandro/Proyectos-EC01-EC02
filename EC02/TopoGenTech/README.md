# TopogenTech 🌴🛰️

**Análisis topológico de la expansión de palma aceitera en Ecuador mediante Machine Learning y datos satelitales**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 📋 Descripción

TopogenTech es una plataforma de análisis geoespacial que combina **Machine Learning** con **Topological Data Analysis (TDA)** para estudiar la expansión del cultivo de palma aceitera en Ecuador y su impacto sobre ecosistemas frágiles.

### Problema a resolver

El cultivo de palma aceitera en Ecuador está causando una **expansión acelerada sobre ecosistemas frágiles** como:
- Bosques húmedos tropicales
- Manglares
- Áreas de amortiguamiento de reservas naturales

Los mapas de cobertura tradicionales **no capturan la estructura topológica del paisaje** (conectividad, fragmentación, corredores ecológicos), lo que limita la capacidad de:
- Anticipar impactos ambientales
- Diseñar políticas de conservación efectivas
- Monitorear cambios tempranos en el territorio

### Nuestra solución

Integramos tecnologías avanzadas para proporcionar análisis profundos del paisaje:

🔍 **Detección temprana** de patrones de expansión  
📊 **Cuantificación objetiva** de fragmentación ecológica  
🌐 **Indicadores topológicos** para gestión territorial sostenible  
🛰️ **Análisis multitemporal** con datos satelitales

## 🎯 Público objetivo

### Instituciones gubernamentales
- **Ministerio del Ambiente, Agua y Transición Ecológica (MAATE)**: Toma de decisiones en política ambiental y ordenamiento territorial
- **Gobiernos locales y provinciales** (Esmeraldas, Santo Domingo, Los Ríos): Planificación de uso de suelo y control de deforestación

### Organizaciones internacionales
- **ONGs ambientales** (WWF, Conservation International)
- **Organismos multilaterales** (FAO, PNUD)
- **Iniciativas de certificación sostenible**

## 🚀 Características principales

- **Análisis topológico** mediante homología persistente
- **Embeddings multitemporales** de imágenes satelitales
- **Detección de patrones** de expansión agrícola
- **Métricas de fragmentación** del paisaje
- **Visualización interactiva** de resultados
- **API REST** para integración con otros sistemas

## 🛠️ Tecnologías

- **Python 3.8+**
- **Machine Learning**: scikit-learn, TensorFlow/PyTorch
- **TDA**: Giotto-tda, Ripser
- **Geoespacial**: GDAL, Rasterio, GeoPandas
- **Visualización**: Matplotlib, Plotly, Folium
- **Datos satelitales**: Sentinel-2, Landsat, mapas globales de palma aceitera

## 📦 Instalación
```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/topogentech.git
cd topogentech

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
