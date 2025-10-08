# MERQUIO — SuperMarket Data Analysis

## Descripción general

    Este proyecto tiene como objetivo analizar las ventas y ganancias de un supermercado utilizando un conjunto de datos público.
    A través de Python, Pandas, Matplotlib, Seaborn e ipywidgets, se realiza un proceso de:

    -Limpieza y preparación de datos.

    -Análisis por intervalos de tiempo (mensual, trimestral y anual).

    -Identificación de productos más y menos vendidos.

    -Cálculo del producto con mayor porcentaje de ganancia.

    -Visualización dinámica mediante una interfaz interactiva.

## Objetivos principales

    -Cargar y limpiar los datos provenientes del dataset en GitHub.

    -Estructurar fechas y horas para facilitar el análisis temporal.

    -Calcular ganancias y ventas agrupadas por intervalos (año, trimestre, mes).

    -Identificar los productos más rentables y más vendidos.

    -Implementar una interfaz visual con filtros interactivos para explorar los datos.

## Tecnologías utilizadas

    -Python 3.10+

    -Pandas → Limpieza y manipulación de datos.

    -NumPy → Operaciones numéricas.

    -Matplotlib / Seaborn → Visualización gráfica.

    -ipywidgets → Filtros y visualización interactiva.

    -KaggleHub → Acceso a datasets (opcional).

## Funciones principales

### cargar_datos(name_file)

    Carga el archivo CSV desde la URL, verifica:

    Información general del dataset.

    Valores nulos y duplicados.

    Convierte las columnas de fecha y hora en un campo unificado (datetime).

    Agrega columnas derivadas (year, month, quarter, weekday, etc.).

### Filtrar_por_intervalo(df, tipo)

    Filtra las ventas por tipo de intervalo:

    "anual"

    "trimestral"

    "mensual"
    Devuelve un DataFrame con la suma total de ventas por periodo.

### ganancia_productos_intervalos(df)

    Agrupa las ganancias (gross income) por año, trimestre y línea de producto.

    productos_mas_vendidos(df, top=10)

    Muestra los productos con mayor cantidad de ventas (Quantity).

    productos_menos_vendidos(df, top=10)

    Muestra los productos con menor cantidad de ventas.

### producto_mayor_ganancia(df)

    Calcula el producto que genera el mayor porcentaje de ganancia total.

    aplicar_filtros_basicos(df, ...)

    Permite filtrar por:

    Línea de producto

    Ciudad o sucursal

    Año

    Mes

    Para ajustar la visualización o análisis.

### plot_top(df, nivel, by, top_n)

    Genera gráficos de barras horizontales para comparar niveles (por ejemplo, ventas por ciudad o producto).

### lanzar_interfaz_niveles_str(df)

    Interfaz interactiva basada en ipywidgets que permite:

    Seleccionar métricas (Sales o Quantity).

    Filtrar por ciudad, producto, año o mes.

    Ajustar el número de elementos mostrados (Top N).

    Visualizar los resultados dinámicamente en gráficos.

## Autores

    Proyecto desarrollado por el Equipo G3 — Hackathon Samsung 2025
    Integrantes:
    Pamela Espinosa
    Jimmy Fuentes
    Bady Mejía
    Richard Pante
    John Peñaloza