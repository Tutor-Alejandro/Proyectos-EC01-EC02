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

## 🏗️ Arquitectura del Sistema

### Backend - Librería Python
- **`topogentech/`** - Librería modular para descarga de embeddings satelitales
  - [`SatelliteEmbeddingsDownloader`](topogentech/downloader.py) - Descarga datos de Google Earth Engine
  - [`RegionConfig`](topogentech/regions.py) - Configuración de regiones predefinidas
  - [`EarthEngineUtils`](topogentech/utils.py) - Utilidades para Earth Engine

### Frontend - Aplicación Web
- **Next.js 14** con TypeScript
- **Componentes interactivos** para análisis geoespacial:
  - [`MapControls`](frontend/components/map-controls.tsx) - Controles de mapa y análisis
  - [`AnalysisTable`](frontend/components/history/analysis-table.tsx) - Historial de análisis realizados
- **UI moderna** con Tailwind CSS y shadcn/ui

### Notebooks de Análisis
- [`analisis_topologico.ipynb`](analisis_topologico.ipynb) - Análisis topológico con TDA
- [`EDA.ipynb`](EDA.ipynb) - Análisis exploratorio de datos

## 🎯 Público objetivo

### Instituciones gubernamentales
- **Ministerio del Ambiente, Agua y Transición Ecológica (MAATE)**: Toma de decisiones en política ambiental y ordenamiento territorial
- **Gobiernos locales y provinciales** (Esmeraldas, Santo Domingo, Los Ríos): Planificación de uso de suelo y control de deforestación

### Organizaciones internacionales
- **ONGs ambientales** (WWF, Conservation International)
- **Organismos multilaterales** (FAO, PNUD)
- **Iniciativas de certificación sostenible**

## 🚀 Características principales

### Análisis Geoespacial
- **Clasificación de Uso de Suelo** - Identificación automática de áreas de palma aceitera
- **Detección de Cambios** - Análisis multitemporal de expansión agrícola
- **Métricas y Estadísticas** - Cuantificación de fragmentación del paisaje
- **Análisis topológico** mediante homología persistente

### Interfaz Web Interactiva
- **Herramientas de dibujo** para selección de áreas de interés
- **Configuración de análisis** con rangos temporales personalizables
- **Visualización de resultados** en tiempo real
- **Historial completo** de análisis realizados
- **Exportación de datos** en múltiples formatos

### Integración con Google Earth Engine
- **Acceso a datos satelitales** Sentinel-2, Landsat
- **Procesamiento en la nube** escalable
- **Exportación automática** a Google Drive o Earth Engine Assets

## 🛠️ Tecnologías

### Backend
- **Python 3.8+**
- **Google Earth Engine API** - Procesamiento de datos satelitales
- **Machine Learning**: scikit-learn, TensorFlow/PyTorch
- **TDA**: Giotto-tda, Ripser
- **Geoespacial**: GDAL, Rasterio, GeoPandas

### Frontend
- **Next.js 14** con TypeScript
- **React** con hooks modernos
- **Tailwind CSS** + shadcn/ui para diseño
- **Lucide React** para iconografía
- **Mapas interactivos** con herramientas de dibujo

### Visualización
- **Matplotlib, Plotly** para gráficos científicos
- **Folium** para mapas interactivos
- **Componentes web responsivos**

## 📦 Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/DaVas1410/TopoGenTech.git
cd TopoGenTech
```

### 2. Configurar el backend (Python)
```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar la librería
pip install -e .

# O instalar con dependencias de desarrollo
pip install -e .[dev]
```

### 3. Configurar el frontend (Next.js)
```bash
cd frontend

# Instalar dependencias
pnpm install
# o npm install

# Ejecutar en modo desarrollo
pnpm dev
# o npm run dev
```

### 4. Configurar Google Earth Engine
```python
import ee
# Autenticar primera vez
ee.Authenticate()
# Inicializar
ee.Initialize()
```

## 🔧 Uso Básico

### Librería Python
```python
from topogentech import SatelliteEmbeddingsDownloader, RegionConfig

# Inicializar descargador
downloader = SatelliteEmbeddingsDownloader(
    project_id='your-gcp-project-id',
    year=2024,
    scale=10
)

# Inicializar Earth Engine
downloader.initialize()

# Obtener límites de Ecuador
ecuador_bounds = RegionConfig.get_country_bounds('ecuador')

# Descargar a Google Drive
task = downloader.download_to_drive(
    region_bounds=ecuador_bounds,
    description='ecuador_embeddings_2024'
)
```

### Aplicación Web
1. Acceder a `http://localhost:3000`
2. Usar las herramientas de dibujo para seleccionar área de interés
3. Configurar rango de fechas y tipo de análisis
4. Ejecutar análisis y visualizar resultados
5. Consultar historial en la sección de análisis realizados

## 📊 Ejemplos de Uso

Ver el archivo [`examples/basic_usage.py`](examples/basic_usage.py) para ejemplos completos de:
- Descarga simple de embeddings
- Análisis por ciudades específicas
- Configuración avanzada de regiones

## 🗺️ Regiones Disponibles

La librería incluye límites predefinidos para:

**Países**: Ecuador, Colombia, Perú, Brasil, Bolivia, Chile, Argentina, Venezuela, y más

**Ciudades**: Quito, Guayaquil, Cuenca, Bogotá, Lima, Santiago, y más

## 📈 Análisis Soportados

1. **Clasificación de Uso de Suelo** - Identificación de cultivos de palma aceitera
2. **Detección de Cambios** - Análisis temporal de expansión agrícola  
3. **Métricas y Estadísticas** - Fragmentación y conectividad del paisaje

## 🤝 Contribuir

1. Fork el repositorio
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📝 Licencia

Distribuido bajo la Licencia MIT. Ver [`LICENSE`](LICENSE) para más información.

## 📞 Contacto

**TopogenTech Team** - contact@topogentech.com

**Project Link**: [https://github.com/DaVas1410/TopoGenTech](https://github.com/DaVas1410/TopoGenTech)

## 🔗 Enlaces Útiles

- [Documentación](https://github.com/DaVas1410/TopoGenTech/blob/main/README.md)
- [Issues](https://github.com/DaVas1410/TopoGenTech/issues)
- [Código Fuente](https://github.com/DaVas1410/TopoGenTech)

---

**Hecho con ❤️ por el equipo TopogenTech para la conservación de ecosistemas ecuatorianos**