# Proyecto LaboraData

## 📊 Descripción

Este proyecto analiza los principales indicadores laborales del Ecuador utilizando la base de datos de la Encuesta Nacional de Empleo, Desempleo y Subempleo (ENEMDU) 2024. El objetivo es obtener una visión general de la informalidad, el empleo, el desempleo y la distribución del ingreso según distintas características sociodemográficas.

## Estructura del Proyecto

```bash
Proyecto-LaboraData/
│
├── Proyecto-LaboraData.ipynb          # Notebook principal con el análisis
├── BDDenemdu_personas_2024_anual.csv  # Dataset de la ENEMDU 2024
└── README.md                           # Descripción del proyecto
```

## Contenido del Notebook

El notebook incluye los siguientes apartados:

### 1. **Carga y exploración de datos**

- Lectura del dataset
- Revisión de tipos de variables, valores nulos y duplicados

### 2. **Limpieza y preprocesamiento**

- Eliminación de valores vacíos y registros inactivos
- Creación de variables derivadas (por ejemplo, empleo formal/informal)

### 3. **Análisis descriptivo**

- Distribución de la población por edad, sexo y condición de actividad
- Tasas de empleo, desempleo e informalidad por características demográficas

### 4. **Visualizaciones clave**

- Pirámide poblacional
- Tasa de desempleo por grupo etario y sexo
- Distribución de ingresos por nivel educativo
- Beneficios laborales por categoría de ocupación
- Distribución de empleados por sector económico

### 5. **Conclusiones**

- Principales hallazgos y patrones observados en el mercado laboral ecuatoriano

## Dataset

- **Nombre:** `BDDenemdu_personas_2024_anual.csv`
- **Fuente:** Instituto Nacional de Estadística y Censos (INEC) – ENEMDU 2024
- **Descripción:** Contiene microdatos anonimizados de personas encuestadas, incluyendo información sobre empleo, ingresos, nivel educativo, sexo, edad y localización geográfica.

## 🔧 Requisitos

Para ejecutar el notebook, se recomienda tener instalado:

- Python 3.10 o superior
- Jupyter Notebook o VS Code
- Bibliotecas necesarias:

```bash
pip install pandas numpy matplotlib seaborn
```

## Ejecución

1. **Clonar el repositorio:**

   ```bash
   git clone https://github.com/Tutor-Alejandro/Proyectos-EC01-EC02.git
   ```

2. **Acceder al directorio del proyecto:**

   ```bash
   cd Proyectos-EC01-EC02/EC02/LaboraData
   ```

3. **Abrir el notebook:**

   ```bash
   jupyter notebook Proyecto-LaboraData.ipynb
   ```

4. **Ejecutar todas las celdas para reproducir el análisis completo.**

## Resultados Esperados

- Tablas con tasas de empleo e informalidad
- Gráficos estadísticos que resumen las condiciones laborales
- Insights sobre los sectores con mayor informalidad y diferencias por sexo o nivel educativo

## Créditos

- **Autor:** Dilan Coral
- **Institución:** Yachay Tech University
- **Curso:** Samsung Innovation Campus (SIC)
- **Año:** 2025
