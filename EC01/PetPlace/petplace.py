
import pandas as pd

# Cargar el archivo Excel (debe tener una hoja con tus datos)
df = pd.read_excel("mascotas3.xlsx")  # Cambia el nombre del archivo

# Convertir a JSON
df.to_json("mascotas3.json", orient="records", indent=2, force_ascii=False)

print("Conversión completada. Se guardó en 'mascotas3.json'")

# ============================================
# PROGRAMA PARA REGISTRAR Y CONTROLAR MASCOTAS
# ============================================

import json
import datetime
import os
from tabulate import tabulate

# ---- Excel (pandas) ----
try:
    import pandas as pd
except ImportError:
    pd = None

# ---- Notificaciones ----
try:
    from plyer import notification
except ImportError:
    notification = None

EXCEL_FILE = "Cálculo de la Ración Diaria1.xlsx"
EXCEL_SHEET = 0
RECORD_FILE = "recordatorios.json"

# ------------------------------
# Datos y persistencia JSON (mascotas)
# ------------------------------
mascotas = []

def cargar_datos():
    global mascotas
    try:
        with open("mascotas3.json", "r", encoding="utf-8") as archivo:
            mascotas = json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        mascotas = []

def guardar_datos():
    with open("mascotas3.json", "w", encoding="utf-8") as archivo:
        json.dump(mascotas, archivo, indent=2, ensure_ascii=False)

# ------------------------------
# Utilidades generales
# ------------------------------
def pausar():
    input("\nPresiona ENTER para continuar...")

def preguntar_numero(minimo, maximo, texto="Elige una opción: "):
    while True:
        respuesta = input(texto).strip()
        if not respuesta.isdigit():
            print(f"Por favor escribe un número entre {minimo} y {maximo}.")
            continue
        numero = int(respuesta)
        if minimo <= numero <= maximo:
            return numero
        print(f"Debe ser entre {minimo} y {maximo}.")

def preguntar_si_no(texto):
    while True:
        respuesta = input(texto + " (s/n): ").strip().lower()
        if respuesta in ("s", "n"):
            return respuesta == "s"
        print("Responde con 's' o 'n' solamente.")

def preguntar_float(mensaje, minimo=None, maximo=None, default=None):
    while True:
        txt = input(mensaje).strip()
        if txt == "" and default is not None:
            return default
        try:
            v = float(txt)
            if minimo is not None and v < minimo:
                print(f"Debe ser ≥ {minimo}.")
                continue
            if maximo is not None and v > maximo:
                print(f"Debe ser ≤ {maximo}.")
                continue
            return v
        except ValueError:
            print("Valor inválido. Intenta de nuevo.")

# ------------------------------
# Cálculos de energía y ración
# ------------------------------
def calcular_kcal_por_dia(peso_kg, factor=1.6):
    rer = 70 * (peso_kg ** 0.75)
    return factor * rer

def calcular_racion_gramos(kcal_dia, kcal_por_gramo=3.5):
    if kcal_por_gramo <= 0:
        return 0
    return kcal_dia / kcal_por_gramo

# ------------------------------
# Funciones para Excel
# ------------------------------
def excel_asegurar_pandas():
    if pd is None:
        print("\n[Error] Necesitas instalar pandas y openpyxl.")
        print("Ejecuta: pip install pandas openpyxl")
        return False
    return True

def _norm(s: str) -> str:
    s = (str(s) if s is not None else "").strip().lower()
    rep = {"á":"a","é":"e","í":"i","ó":"o","ú":"u","ü":"u","ñ":"n","\n":" ","\r":" "}
    for a,b in rep.items():
        s = s.replace(a,b)
    return " ".join(s.split())

def excel_leer_raw():
    if not excel_asegurar_pandas():
        return None
    try:
        df = pd.read_excel(EXCEL_FILE, sheet_name=EXCEL_SHEET, engine="openpyxl")
        return df
    except FileNotFoundError:
        print(f"\n[Error] No se encontró el archivo: {EXCEL_FILE}")
        return None
    except Exception as e:
        print(f"\n[Error] No se pudo abrir el Excel: {e}")
        return None

def excel_guardar_raw(df):
    if not excel_asegurar_pandas():
        return
    try:
        with pd.ExcelWriter(EXCEL_FILE, engine="openpyxl", mode="w") as writer:
            df.to_excel(writer, index=False)
    except Exception as e:
        print(f"\n[Error] No se pudo guardar el Excel: {e}")

def excel_mostrar_tabla_raw(df, titulo="TABLA (Excel)"):
    if df is None or df.empty:
        print("\n(No hay registros en el Excel aún)")
        return
    print(f"\n=== {titulo} ===\n")
    print(tabulate(df.fillna(""), headers=list(df.columns), tablefmt="grid"))

def excel_col_finder(df):
    normcols = {_norm(c): c for c in df.columns}
    def pick(keys):
        for k in keys:
            if k in normcols:
                return normcols[k]
        return None
    return {
        "nombre": pick(["nombre","mascota"]),
        "especie": pick(["especie","tipo"]),
        "peso": pick(["peso","pesaje (kg)","peso (kg)"]),
        "energia": pick(["kcal/dia","necesidad energetica","der"]),
        "kcalg": pick(["kcal/g","kcal por gramo"]),
        "racion": pick(["racion (g/dia)","racion","ración (g/día)"]),
        "factor": pick(["factor","actividad"])
    }

def excel_buscar_indices_por_nombre(df, col_nombre, nombre_objetivo):
    if col_nombre is None:
        return []
    objetivo = _norm(nombre_objetivo)
    idxs = []
    for i, v in enumerate(df[col_nombre].fillna("").astype(str).tolist()):
        if _norm(v) == objetivo:
            idxs.append(i)
    return idxs

# ------------------------------
# MÓDULO DE RECORDATORIOS CON HORA Y NOTIFICACIONES
# ------------------------------
def cargar_recordatorios():
    if not os.path.exists(RECORD_FILE):
        return []
    try:
        with open(RECORD_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def guardar_recordatorios(datos):
    with open(RECORD_FILE, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)

def mostrar_recordatorios():
    recordatorios = cargar_recordatorios()
    if not recordatorios:
        print("\nNo hay recordatorios registrados.")
        pausar()
        return
    print("\n=== LISTA DE RECORDATORIOS ===")
    filas = []
    for i, r in enumerate(sorted(recordatorios, key=lambda x: (x["fecha"], x.get("hora", "")))):
        filas.append([
            i + 1,
            r.get("fecha", ""),
            r.get("hora", ""),
            r.get("nombre_mascota", ""),
            r.get("evento", ""),
            r.get("notas", "")
        ])
    print(tabulate(filas, headers=["#", "Fecha", "Hora", "Mascota", "Evento", "Notas"], tablefmt="grid"))
    pausar()

def agregar_recordatorio():
    print("\n--- Agregar nuevo recordatorio ---")
    nombre = input("Nombre de la mascota (o 'General'): ").strip() or "General"
    evento = input("Evento o tarea: ").strip()
    notas = input("Notas opcionales: ").strip()
    while True:
        fecha_txt = input("Fecha (AAAA-MM-DD): ").strip()
        try:
            fecha = datetime.datetime.strptime(fecha_txt, "%Y-%m-%d").date()
            break
        except ValueError:
            print("Formato inválido. Usa AAAA-MM-DD.")
    while True:
        hora_txt = input("Hora (HH:MM, formato 24h, opcional): ").strip()
        if not hora_txt:
            hora_txt = None
            break
        try:
            datetime.datetime.strptime(hora_txt, "%H:%M")
            break
        except ValueError:
            print("Formato inválido. Usa HH:MM, por ejemplo 14:30.")
    data = cargar_recordatorios()
    data.append({
        "nombre_mascota": nombre,
        "evento": evento,
        "notas": notas,
        "fecha": fecha.strftime("%Y-%m-%d"),
        "hora": hora_txt
    })
    guardar_recordatorios(data)
    print(f"\nRecordatorio para {nombre} agregado correctamente.")
    pausar()

def eliminar_recordatorio():
    recordatorios = cargar_recordatorios()
    if not recordatorios:
        print("\nNo hay recordatorios para eliminar.")
        pausar()
        return
    mostrar_recordatorios()
    num = preguntar_numero(1, len(recordatorios), "Elige el número del recordatorio a eliminar: ")
    r = recordatorios.pop(num - 1)
    guardar_recordatorios(recordatorios)
    print(f"\nRecordatorio '{r.get('evento')}' eliminado.")
    pausar()

def revisar_recordatorios_hoy_mañana():
    recordatorios = cargar_recordatorios()
    if not recordatorios:
        return
    hoy = datetime.date.today()
    ahora = datetime.datetime.now().time()
    manana = hoy + datetime.timedelta(days=1)
    avisar_hoy = []
    avisar_manana = []
    for r in recordatorios:
        fecha_str = r.get("fecha")
        hora_str = r.get("hora")
        try:
            fecha = datetime.datetime.strptime(fecha_str, "%Y-%m-%d").date()
        except Exception:
            continue
        if fecha == hoy:
            if hora_str:
                try:
                    hora = datetime.datetime.strptime(hora_str, "%H:%M").time()
                    if hora <= ahora:
                        avisar_hoy.append(r)
                except:
                    avisar_hoy.append(r)
            else:
                avisar_hoy.append(r)
        elif fecha == manana:
            avisar_manana.append(r)
    for r in avisar_hoy:
        nombre = r.get("nombre_mascota", "General")
        evento = r.get("evento", "")
        fecha = r.get("fecha")
        hora = r.get("hora", "")
        notas = r.get("notas", "")
        print(f"\nRecordatorio ({fecha} {hora or ''}) - {nombre}: {evento}")
        if notas:
            print(f"   Notas: {notas}")
        if notification:
            try:
                notification.notify(
                    title=f"Recordatorio: {nombre}",
                    message=f"{evento} ({fecha} {hora or ''})",
                    app_name="Control Mascotas",
                    timeout=10
                )
            except Exception as e:
                print(f"[Aviso] No se pudo mostrar notificación del sistema: {e}")
    if avisar_manana:
        print("\nRecordatorios para mañana:")
        for r in avisar_manana:
            print(f" - {r.get('nombre_mascota','')}: {r.get('evento','')} ({r.get('hora','')})")

def menu_recordatorios():
    while True:
        print("\n======= RECORDATORIOS =======")
        print("1. Ver todos los recordatorios")
        print("2. Agregar recordatorio")
        print("3. Eliminar recordatorio")
        print("4. Volver al menú principal")
        op = preguntar_numero(1, 4, "Elige una opción: ")
        if op == 1:
            mostrar_recordatorios()
        elif op == 2:
            agregar_recordatorio()
        elif op == 3:
            eliminar_recordatorio()
        elif op == 4:
            break

# ------------------------------
# MENÚ PRINCIPAL
# ------------------------------
def menu():
    cargar_datos()
    revisar_recordatorios_hoy_mañana()
    while True:
        print("\n=========== MENÚ PRINCIPAL ===========")
        print("1. Ver lista de mascotas")
        print("2. Agregar una nueva mascota")
        print("3. Ver datos de una mascota")
        print("4. Editar una mascota")
        print("5. Eliminar una mascota")
        print("6. Ver tabla completa de todas las mascotas")
        print("7. Raciones de comida (consultar/agregar/ver)")
        print("8. Recordatorios (ver/agregar/eliminar)")
        print("9. Salir")
        opcion = preguntar_numero(1, 9, "Elige una opción: ")
        if opcion == 1:
            print("\nMascotas registradas:")
            for i, m in enumerate(mascotas, 1):
                print(f"{i}. {m.get('nombre', '(sin nombre)')} - {m.get('especie', '(sin especie)')}")
            pausar()
        elif opcion == 2:
            print("\nFunción para agregar mascotas aquí...")
            pausar()
        elif opcion == 3:
            print("\nFunción para ver mascota aquí...")
            pausar()
        elif opcion == 4:
            print("\nFunción para editar mascota aquí...")
            pausar()
        elif opcion == 5:
            print("\nFunción para eliminar mascota aquí...")
            pausar()
        elif opcion == 6:
            print("\nFunción para ver tabla completa aquí...")
            pausar()
        elif opcion == 7:
            print("\nMenú de raciones (Excel) aún conectado a tu hoja existente.")
            pausar()
        elif opcion == 8:
            menu_recordatorios()
        elif opcion == 9:
            print("Cerrando el programa. Hasta pronto.")
            break

# ------------------------------
# PUNTO DE ENTRADA
# ------------------------------
if __name__ == "__main__":
    menu()