import pandas as pd
import matplotlib.pyplot as plt
import os
import re

################# VARIABLES GLOBALES ############################

NOMBRE_DATASET_CONSUMO = 'ConsumoFamilias.xlsx'
DIRECTORIO_MODELOS = './'
EXTENSION_MODELOS = '.xlsx'

COLUMNA_COSTO_MENSUAL = 'Costo Mensual ($)'
COLUMNA_CONSUMO_TOTAL_KWH = 'Consumo Total (kWh)'
COLUMNA_CONSUMO_MODELO = 'Consumo Mensual (kWh/mes)'
COLUMNA_NOMBRE_MODELO = 'Producto'

################# FUNCION 1: LECTURA DE DATASET 1 ###############

def cargar_consumo_principal(nombre_archivo):
    try:
        df_consumo = pd.read_excel(nombre_archivo, engine='openpyxl')
        return df_consumo
    except FileNotFoundError:
        print(f"ERROR: No se encontró el archivo principal: {nombre_archivo}.")
        return None
################ FUNCION 2: RELACIONAR ELECTRODOMESTICO CON DATASET 2 ##########

def limpiar_nombre(nombre):
    nombre_limpio = nombre.strip()
    nombre_limpio = re.sub(r'\s+', '', nombre_limpio)
    nombre_limpio = re.sub(r'[^a-zA-Z0-9]', '', nombre_limpio)
    return nombre_limpio.lower()

################ FUNCION 3: CALCULO DE CONSUMO BASE ############################
def calcular_consumo_base(df_consumo):
    df_numerico = df_consumo.select_dtypes(include='number')
    cols_a_excluir = [COLUMNA_COSTO_MENSUAL, COLUMNA_CONSUMO_TOTAL_KWH]
    df_consumo_aparatos = df_numerico.drop(columns=cols_a_excluir, errors='ignore')
    consumo_promedio_mensual = df_consumo_aparatos.mean().sort_values(ascending=False)
    return consumo_promedio_mensual[consumo_promedio_mensual > 0]

################ FUNCION 4: ALGORITMO DE BUSQUEDA DE EFICENCIA ################

def buscar_modelo_eficiente(electrodomestico_a_reemplazar):
    nombre_limpio = limpiar_nombre(electrodomestico_a_reemplazar)

    ruta_min = os.path.join(DIRECTORIO_MODELOS, f'{nombre_limpio}_dataset{EXTENSION_MODELOS}')
    nombre_mayuscula = nombre_limpio.capitalize()
    ruta_mayus = os.path.join(DIRECTORIO_MODELOS, f'{nombre_mayuscula}_dataset{EXTENSION_MODELOS}')

    ruta_final = None
    if os.path.exists(ruta_mayus):
        ruta_final = ruta_mayus
    elif os.path.exists(ruta_min):
        ruta_final = ruta_min

    if ruta_final is None:
        return None, 0

    try:
        df_modelos = pd.read_excel(ruta_final, engine='openpyxl')
    except Exception:
        return None, 0

    if COLUMNA_CONSUMO_MODELO not in df_modelos.columns:
         return None, 0

    modelo_eficiente = df_modelos.loc[df_modelos[COLUMNA_CONSUMO_MODELO].idxmin()]
    consumo_mensual_nuevo = modelo_eficiente[COLUMNA_CONSUMO_MODELO]

    return modelo_eficiente[COLUMNA_NOMBRE_MODELO], consumo_mensual_nuevo

####################### FUNCION 5: GRAFICA ORIGINAL ##########################

def generar_grafica_consumo(datos, titulo, color='skyblue'):
    plt.figure(figsize=(12, 7))
    datos.plot(kind='bar', color=color)
    plt.title(titulo, fontsize=16)
    plt.ylabel('Consumo Mensual Promedio (kWh/mes)', fontsize=12)
    plt.xlabel('Electrodoméstico', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

###################### FUNCION 6: GRAFICO ORIGINAL #############################


def generar_grafica_comparativa_final(gasto_original_mensual, consumo_original_kwh, consumo_propuesto_kwh):

    consumo_total_original_kwh = consumo_original_kwh.sum()
    consumo_total_propuesto_kwh = consumo_propuesto_kwh.sum()

    ahorro_porcentual_kwh = (consumo_total_original_kwh - consumo_total_propuesto_kwh) / consumo_total_original_kwh
    gasto_propuesto_mensual = gasto_original_mensual * (1 - ahorro_porcentual_kwh)

    datos = pd.Series({'Planilla Original': gasto_original_mensual, 'Planilla Propuesta': gasto_propuesto_mensual})

    plt.figure(figsize=(8, 6))
    barras = plt.bar(datos.index, datos.values, color=['#FF6347', '#3CB371'])
    plt.title('Comparación de Planilla Mensual de Costo', fontsize=16)
    plt.ylabel(f'Costo Mensual Estimado ($/mes)', fontsize=12)
    plt.xticks(rotation=0)

    # 1. Eliminar el cuadro de texto flotante de ahorro (quitando el plt.text(0.5, ...) anterior)

    # 2. Eliminar etiquetas de costo sobre las barras (quitando el bucle 'for bar in barras:')

    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

    # 3. Mostrar el dato del ahorro estimado en la consola (fuera del gráfico)
    ahorro_monetario_porcentual = ((gasto_original_mensual - gasto_propuesto_mensual) / gasto_original_mensual) * 100
    print(f"Gasto Original Promedio: ${gasto_original_mensual:.2f}")
    print(f"Gasto Propuesto Promedio: ${gasto_propuesto_mensual:.2f}")
    print(f"Ahorro Estimado: {ahorro_monetario_porcentual:.1f}% mensual")

########################## FUNCION 7: PRINCIPAL ###############################
def ejecutar_algoritmo_ahorro():

    df_consumo = cargar_consumo_principal(NOMBRE_DATASET_CONSUMO)
    if df_consumo is None:
        return

    try:
        gasto_original_promedio = df_consumo[COLUMNA_COSTO_MENSUAL].mean()
    except KeyError:
        print(f"ERROR: No se encontró la columna de Costo Mensual: '{COLUMNA_COSTO_MENSUAL}'.")
        return

    consumo_base_kwh = calcular_consumo_base(df_consumo)

    if consumo_base_kwh.empty:
        print("ERROR: No se encontraron columnas de consumo kWh por electrodoméstico para analizar.")
        return

    # 1. Gráfico Original
    print("\n--- GRÁFICO 1: Consumo Mensual Original (Línea Base) ---")
    generar_grafica_consumo(consumo_base_kwh, 'Consumo Mensual Promedio por Electrodoméstico (kWh/mes)')

    electrodomesticos_ordenados = consumo_base_kwh.index.tolist()

    for i, electrodomestico in enumerate(electrodomesticos_ordenados):

        modelo_nuevo, consumo_nuevo = buscar_modelo_eficiente(electrodomestico)

        if modelo_nuevo is None or consumo_nuevo == 0:
            continue

        consumo_solucion_kwh = consumo_base_kwh.copy()
        consumo_original_item = consumo_solucion_kwh[electrodomestico]
        consumo_solucion_kwh[electrodomestico] = consumo_nuevo

        ahorro_mensual_kwh = consumo_original_item - consumo_nuevo

        print(f"\n--- PROPUESTA {i+1}: Reemplazar el TOP {i+1} consumidor: {electrodomestico} ---")
        print(f"Propuesta: Modelo '{modelo_nuevo}' ofrece un ahorro de {ahorro_mensual_kwh:.2f} kWh/mes.")

        # 2. Gráfico Solución
        generar_grafica_consumo(consumo_solucion_kwh, f'Consumo Mensual Propuesto ({electrodomestico} Reemplazado)', color='#3CB371')

        # 3. Pregunta al usuario
        respuesta = input("¿Acepta esta solución de reemplazo por representar un beneficio/ahorro? (escriba 'si' o 'no'): ").lower()

        if respuesta == 'si':
            print("\n--- GRÁFICO FINAL: Comparación de Planillas ---")

            # 4. Gráfico Final de Planillas y datos en consola
            generar_grafica_comparativa_final(gasto_original_promedio, consumo_base_kwh, consumo_solucion_kwh)
            break

    else:
        print("\nEl algoritmo ha revisado todos los electrodomésticos. No se aceptó ninguna solución.")

####################### DEMOSTRACIÓN ##############################################################
if __name__ == "__main__":
    ejecutar_algoritmo_ahorro()
