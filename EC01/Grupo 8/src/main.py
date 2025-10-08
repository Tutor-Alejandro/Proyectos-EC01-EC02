from pathlib import Path
from data_processing import load_and_filter, guess_columns
from interaction_cli import pick_record_simple, compute_score_for_row, manual_entry_with_recs



def _ensure_logs_folder():
    Path("./src/logs").mkdir(parents=True, exist_ok=True)


def main() -> None:
    _ensure_logs_folder()

    print("=== FocusBoost ===")
    csv_path = "./data/data.csv"

    df = None
    try:
        df = load_and_filter(csv_path)
        print(f"Dataset cargado correctamente ({len(df)} registros del grupo objetivo).")
    except Exception as e:
        print("No se pudo cargar el CSV o filtrar el grupo objetivo:", e)
        print("Puedes usar el modo de ingreso manual para calcular tu Focus Score sin el dataset.\n")

    mapping = guess_columns(df) if df is not None else {}

    while True:
        print("\nMenú:")
        if df is not None:
            print("[1] Buscar mi registro y ver mi Focus Score")
        print("[2] Ingresar mis datos de hoy")
        print("[3] Salir")

        opt = input("Elige una opción: ").strip()

        if opt == "1" and df is not None:
            idx = pick_record_simple(df)   # <- aquí la versión simple
            if idx is None:
                continue
            compute_score_for_row(df, mapping, idx)  # esta función ya imprime el reporte amigable


        elif opt == "2":
            manual_entry_with_recs()

        elif opt == "3":
            print("¡Hasta luego!")
            break

        else:
            print("Opción inválida. Intenta de nuevo.")


if __name__ == "__main__":
    main()
