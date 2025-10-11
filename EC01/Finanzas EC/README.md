# FinanzasEC
## 1. Descripción General
**FinanzasEC** es una herramienta desarrollada en Python para realizar un análisis fiscal y financiero integral de pequeñas y medianas empresas (PYMES) ecuatorianas, combinando información del **Servicio de Rentas Internas (SRI)** y de la **Superintendencia de Compañías, Valores y Seguros (SCVS)**.

El sistema permite calcular el **IVA mensual a pagar**, evaluar indicadores de rentabilidad operativa y financiera, y comparar los resultados de una empresa con los promedios de su sector económico.

---

## 2. Objetivo
Brindar a las PYMES una herramienta práctica que permite:
- Controlar su comportamiento fiscal frente al entorno económico.
- Evaluar su desempeño operativo y financiero respecto al sector.
- Tomar decisiones informadas en materia de gestión tributaria y rentabilidad.

---

## 3. Entradas del Sistema
El programa requiere los siguientes archivos en formato CSV ubicados en el mismo directorio:

- `sri_ventas_[AÑO].csv` — Información tributaria mensual del SRI.  
- `bi_ranking.csv` — Estados financieros empresariales provenientes de la SCVS.  
- `SRI_RUC_[PROVINCIA].csv` — Registro de contribuyentes por provincia, con códigos CIIU y ubicación.

El usuario debe ingresar manualmente los siguientes datos:
- RUC de la empresa.  
- Año fiscal y mes de análisis.  
- Ventas netas gravadas.  
- Compras netas gravadas.  
- Utilidad antes de impuestos.  
- Activos totales.  
- Patrimonio.  
- Utilidad neta.

---

## 4. Procesamiento y Cálculos
El sistema calcula lo siguiente:

### 4.1 Cálculo fiscal
- **IVA cobrado:** `VENTAS_NETAS_TARIFA_GRAVADA × 0.15`
- **IVA crédito:** `COMPRAS_NETAS_TARIFA_GRAVADA × 0.15`
- **IVA neto a pagar:** diferencia entre el IVA cobrado y el IVA crédito.

### 4.2 Indicadores financieros
- **Margen operativo:** Utilidad antes de impuestos / Ventas netas.  
- **ROA (Rentabilidad sobre activos):** Utilidad neta / Activos totales.  
- **ROE (Rentabilidad sobre patrimonio):** Utilidad neta / Patrimonio.

### 4.3 Comparaciones sectoriales
- Obtiene el promedio sectorial del IVA mensual usando `CODIGO_SECTOR_N1` del SRI.
- Calcula promedios de **margen operativo**, **ROA** y **ROE** para el sector económico (CIIU6) a partir del archivo `bi_ranking.csv`.

### 4.4 Interpretación automática
Genera un texto explicativo que compara los valores de la empresa con los promedios sectoriales, identificando si se encuentran por encima, dentro o por debajo del rango esperado.

---

## 5. Salidas del Sistema
El programa entrega:

1. **Resultados**:
   - IVA mensual a pagar.
   - Indicadores financieros individuales.
   - Promedios sectoriales y comparaciones.

2. **Gráficos comparativos individuales:**
   - Margen operativo vs. sector.
   - ROA vs. sector.
   - ROE vs. sector.

3. **Informe**, que resume el análisis financiero y fiscal de la empresa.
