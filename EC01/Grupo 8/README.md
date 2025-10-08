# FocusBoost · Analizador de uso digital y concentración

**FocusBoost** es un prototipo en Python que estima el **puntaje de concentración** de estudiantes universitarios a partir de su **uso digital**. Funciona desde consola y ofrece dos formas de uso:

1) **Probar con el dataset** (modo “dataset”): seleccionas un registro y ves su Focus Score.  
2) **Ingresar tus datos del día** (modo “manual”): respondes preguntas sencillas (no números exactos), el sistema calcula tu Focus Score y te sugiere acciones de mejora.

---

## 🚀 Características

- **Filtro de grupo objetivo**: `occupation = Student` y `device = Smartphone`.  
- **Conversión automática** de textos del dataset a números (p. ej., *“10–30 minutes”* → puntaje de atención; *“4–6”* → 5.0 horas).  
- **Focus Score** con fórmula sencilla:

`score = base + w1 * attention - w2 * social_time - w3 * notifications`

  (recortado a rango **0–100**).  
- **Clasificación** del uso diario: **bajo** (≤1.5h), **moderado** (≤3h), **alto** (>3h).  
- **Recomendaciones** simples y prácticas (silenciar notificaciones, evitar nocturnidad, bloques cortos, etc.).  
- **Registro** de sesiones en `src/logs/focusboost_log.csv` (sirve para ver progreso y KPIs).

---

## 📁 Estructura del proyecto

```
FocusBoost/
├── src/
│   ├── main.py                    # Punto de entrada (CLI)
│   ├── focus_model.py             # Clase FocusScore + clausura de umbral
│   ├── data_processing.py         # Lectura de CSV, normalización y derivaciones
│   ├── interaction_cli.py         # Flujo de interacción por consola (dataset/manual + recomendaciones)
│   ├── recommendations.py         # Reglas de recomendaciones
│   ├── time_tracking.py           # Seguimiento de bloques (Pomodoro/Time-boxing)
│   ├── utils.py                   # Auxiliares (normalize, bubble sort, etc.)
│   └── logs/
│       └── focusboost_log.csv     # Se genera al usar la app
│
├── data/
│   └── data.csv                   # Dataset base (coloca tu archivo aquí)
│
├── requirements.txt               # Dependencias mínimas (pandas)
└── README.md                      # Este documento
```

---

## 🔧 Requisitos

- **Python 3.10+** (recomendado)  
- **pip** para instalar dependencias

---
---

## 📊 Fuente del dataset

El prototipo utiliza el dataset público **"Screen Time Data: Productivity and Attention Span"**, disponible en [Kaggle](https://www.kaggle.com/datasets/muhammadalirazazaidi/screen-time-data-productivity-and-attention-span), creado por **Muhammad Aliraza Zaidi**.  
Se usa únicamente con fines educativos y de investigación académica.

---


## 🧩 Instalación

```bash
# Crea y activa un entorno virtual
# Windows
py -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Instala dependencias
pip install -r requirements.txt
```

Asegúrate de colocar tu `data.csv` en la carpeta `data/`:
```
FocusBoost/data/data.csv
```

---

## ▶️ Uso

Ejecuta el programa principal:

```bash
# Windows
python src\main.py
# macOS / Linux
python src/main.py
```

### Menú principal (simple y claro)
```
Menú:
[1] Probar con un registro del dataset (elige un número)
[2] Ingresar mis datos de hoy (preguntas fáciles)
[3] Salir
```

### Opción 1 · Probar con dataset
- El sistema te dice cuántos registros hay (por ejemplo: “Hay 95 registros…”).
- Te pide **un número entre 0 y N-1** (p. ej., `23`).
- Te muestra tu **Focus Score** y un **resumen entendible**, por ejemplo:

```
Tu Focus Score: 58.0  → Nivel: REGULAR
Resumen: atención media (55/100), uso moderado (~2.5 h), notificaciones normales (~30).
```

> Bajo el capó: el sistema convierte textos como *“10–30 minutes”* o *“More than 10”* a valores numéricos razonables para el cálculo.

### Opción 2 · Ingresar mis datos de hoy
- Respondes **preguntas por categorías** (no números exactos):
  - **Atención**: baja / media / alta  
  - **Tiempo en apps que distraen**: casi nada / poco / algo / moderado / alto  
  - **Notificaciones**: silenciadas / gestionadas / normales / muchas  
  - **Uso principal**: Social / Streaming / Gaming / Mensajería / Educación / Productividad / Otra  
  - **Momento de uso**: mañana / tarde / noche / nocturno  
- El sistema calcula tu **Focus Score**, te da un **resumen** y **recomendaciones**.  
- (Opcional) Registras **bloques de estudio** (Pomodoro/Time-boxing) para medir **adherencia** (en %).

### Logs y KPIs
- Cada ejecución guarda una fila en `src/logs/focusboost_log.csv` con:
  - `timestamp`, `mode` (dataset/manual), `attention`, `social_time`, `notifications`, `focus_score`, `usage_label`, `adherence`, etc.  
- Puedes abrir este CSV para ver tu progreso y calcular indicadores semanales.

---

## 🔍 ¿Cómo funciona por dentro?

1) **Carga y preparación** (`data_processing.py`)  
   - Lee `data/data.csv`, normaliza columnas a *snake_case* y filtra `Student + Smartphone`.  
   - Deriva columnas numéricas:
     - `attention_num` (0–100) a partir de textos como *“Less than 10 minutes”*, *“More than 1 hour”*.  
     - `screen_time_hours` (horas) a partir de *“4–6”*, *“8–10”*, *“More than 10”*.

2) **Modelo** (`focus_model.py`)  
   - Clase `FocusScore` aplica la fórmula y recorta el resultado a **[0, 100]**.  
   - Clausura `threshold_closure(70.0)` para considerar **“Buen enfoque”**.

3) **Interacción** (`interaction_cli.py`)  
   - **Dataset**: selección súper simple por número.  
   - **Manual**: preguntas por categorías → conversión interna a números → cálculo → recomendaciones.  
   - **Registro**: guarda los resultados en `src/logs/focusboost_log.csv`.

4) **Recomendaciones** (`recommendations.py`)  
   - Reglas **if/else** (sin ML): evita nocturnidad, silencia notificaciones, bloques cortos y progresivos, etc.

5) **Bloques de tiempo** (`time_tracking.py`)  
   - Pequeño asistente para **planificar** y **marcar completados**, devolviendo **adherencia %**.

---

## 🧠 Métricas y definiciones

- **Focus Score**: estimación (0–100) basada en:
  - **Atención**: más alta → mejor.  
  - **Tiempo en apps distractoras**: más alto → reduce score.  
  - **Notificaciones**: más alto → reduce score.  
- **Nivel de uso**:
  - **Bajo**: ≤ 1.5h  
  - **Moderado**: ≤ 3h  
  - **Alto**: > 3h  
- **Adherencia**: % de bloques completados sin interrupciones respecto a los planificados.

## 🛠️ Troubleshooting

- **No encuentra `data.csv`**: verifica que esté en `FocusBoost/data/data.csv`.  
- **Error con pandas**: ejecuta `pip install -r requirements.txt` en el entorno virtual activo.  
- **No se crea `focusboost_log.csv`**: se genera al guardar la primera sesión; asegura que existe `src/logs/` (el programa la crea).
