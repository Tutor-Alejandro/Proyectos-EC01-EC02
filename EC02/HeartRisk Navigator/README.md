# HeartRisk Navigator

# Sistema Profesional de Evaluación del Riesgo Cardiovascular

**HeartRisk Navigator** es una aplicación de escritorio desarrollada en **Python** que permite estimar el riesgo de insuficiencia cardíaca de un paciente utilizando un modelo predictivo de aprendizaje automático (Machine Learning).  
La interfaz gráfica está construida con **Tkinter**, integra visualizaciones con **Matplotlib** y **Seaborn**, y genera reportes profesionales en **PDF** con **ReportLab**.

---

# Características principales

- Interfaz moderna e intuitiva con **Tkinter**  
- Predicción automática mediante un modelo de **Machine Learning**  
- **Explicación detallada** de los factores que influyen en el riesgo  
- **Historial** de pacientes analizados (almacenado en `patient_history.json`)  
- Visualización estadística del dataset con gráficos:
  - Distribución de edades  
  - Tasa de mortalidad (`DEATH_EVENT`)  
  - Relación entre creatinina sérica y mortalidad  
  - Mapa de correlaciones  
- Generación de **reportes en PDF** personalizados y profesionales  

---

# Estructura del proyecto

HeartRiskNavigator/
│
├── main.py # Archivo principal (interfaz y lógica)
├── risk_predictor.py # Módulo del modelo predictivo
├── factor_explainer.py # Explicaciones por cada factor del modelo
├── heart_failure_clinical_records_dataset.csv # Dataset base de entrenamiento
├── patient_history.json # Historial de pacientes evaluados
├── heartrisk.log # Registro de eventos y errores
└── requirements.txt # Librerías necesarias

# Nota: Instalar las librerias necesarias antes de la ejecución