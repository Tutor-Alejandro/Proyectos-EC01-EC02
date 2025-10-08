#  Proyecto: Sistema Predictivo de Inventario y Demanda

##  Equipo de Trabajo

| Nombre | Rol | Función |
|--------|------|---------|
| **Joshua Vallejo Luna** | **Project Manager** | Supervisa el cumplimiento de objetivos, coordina las tareas del equipo y asegura la coherencia entre los módulos del sistema. Gestiona el cronograma. |
| **Joshúa Castillo Merejildo** | **Data Processing Specialist** | Prepara los datos para el modelo predictivo. Se encarga de la limpieza, validación y análisis exploratorio de los datos. |
| **Jhon Villacís Ramón** | **Predictive Modeling Engineer** | Desarrolla el algoritmo de forecasting de demanda. |
| **Juan Larrea Martínez** | **Software Developer** | Implementa el sistema funcional que integra los datos, el modelo y las alertas. Diseña la interfaz del prototipo en una plataforma interactiva. |
| **Brithany Suárez Palacios** | **Business Analyst** | Elabora los informes, la presentación y la estrategia de comunicación del impacto del proyecto. |

---

##  Planteamiento del Problema

En las tiendas minoristas, la gestión ineficiente del inventario provoca dificultades para anticipar la demanda, generando faltantes de productos o exceso de stock.  
Esto a su vez produce pérdidas económicas, desperdicio de productos (especialmente perecederos) e insatisfacción del cliente, disminuyendo la competitividad del negocio.

---

## Objetivo General

**Predecir la demanda futura con datos en tiempo real** para reducir pérdidas, evitar desabastecimientos y promover la toma de decisiones estratégicas en tiendas minoristas.

---

## Objetivos Específicos

- Desarrollar una plataforma de análisis de inventario y demanda.  
- Diseñar un algoritmo predictivo para la reposición de inventario.  
- Construir un sistema de visualización y reporte para microcomercios.

---

##  Herramientas Utilizadas

- **Lenguaje:** Python  
- **Bibliotecas:** `pandas`, `numpy`, `matplotlib`, `seaborn`  
- **Análisis de datos:** Agrupación por categoría, series temporales y tendencias de venta.  
- **Visualización:** Gráficos de barras, pastel, distribuciones, boxplots, evolución de ventas y predicciones.  
- **Entorno de trabajo:** Google Colab  

---

##  Funcionamiento del Código

###  ENTRADAS
**Archivo CSV con información de inventario**, con las siguientes columnas principales:
- `Fecha (date)`
- `Tienda (store_id)`
- `Producto (product_id)`
- `Categoría (category)`
- `Nivel de inventario (inventory_level)`
- `Unidades vendidas (units_sold)`
- `Precio`, `descuentos`, `promociones`
- `Pronóstico de demanda (demand_forecast)`

---

###  PROCESO

####  Paso 1: Cargar y limpiar datos
1. Busca automáticamente el archivo de datos.  
2. Limpia nombres de columnas.  
3. Convierte fechas al formato correcto.  
4. Crea nuevas métricas importantes.

####  Paso 2: Detectar problemas
1. Calcula **“sell-through” = (ventas / inventario)**.  
2. Clasifica productos en 3 categorías:
   - **SOBRESTOCK:** menos del 30% vendido.  
   - **NORMAL:** entre 30% y 90% vendido.  
   - **DESABASTECIMIENTO:** más del 90% vendido.  

>  *Los valores 30% y 90% no provienen de un estándar fijo de la industria, sino que son umbrales heurísticos de referencia ampliamente utilizados y ajustados según el comportamiento histórico de las ventas y políticas de inventario de cada organización.*

####  Paso 3: Analizar por categoría y tienda
1. Agrupa productos por categoría (ropa, electrónicos, etc.).  
2. Analiza cada tienda por separado.  
3. Calcula métricas clave para cada grupo.

####  Paso 4: Crear modelo predictivo
Fórmula utilizada:  
**Demanda Futura = Ventas Actuales + (Ventas × Descuento × 0.075) + (Ventas × Promoción × 0.025)**

####  Paso 5: Generar gráficos y reportes
1. Gráficos de líneas para tendencias.  
2. Gráficos de pastel para distribución.  
3. Gráficos de barras para comparaciones.  
4. Reportes ejecutivos con recomendaciones automáticas.

---

## SALIDAS

### Diagnósticos identificados
```
# PROBLEMAS ENCONTRADOS:
- 30.3% de productos con SOBRESTOCK (22,131 productos)
- 10.2% de productos con DESABASTECIMIENTO (7,434 productos)
- $338 millones inmovilizados en inventario excesivo
```

### Gráficos generados
```
# VISUALIZACIONES CREADAS:
1. Distribución general de estados de inventario
2. Ventas mensuales por categoría
3. Tendencias por tienda
4. Análisis comparativo entre tiendas
```

### Recomendaciones automáticas
```
# ACCIONES SUGERIDAS:

PRIORIDAD ALTA:
- Reducir sobrestock con promociones.
- Ajustar niveles de reposición.
- Revisar políticas de compra.

PRIORIDAD MEDIA:
- Optimizar modelo predictivo.
- Establecer KPIs por categoría.
```

---

##  Reporte Ejecutivo

**Resumen Final:**
> “El 40.4% de los productos presentan problemas de inventario.  
> El sobrestock representa el 74.9% de los casos.  
> Se requiere acción inmediata en las categorías identificadas.”

---

###  Autoría
Proyecto desarrollado por el **SmartInventory**.
