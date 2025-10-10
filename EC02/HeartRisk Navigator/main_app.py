import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from risk_predictor import predecir_riesgo
from factor_explainer import explicacion_por_cada_factor
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')  # Importante para evitar problemas
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from pathlib import Path
from datetime import datetime
import json
import logging
import threading
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.platypus.flowables import HRFlowable
import seaborn as sns

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='heartrisk.log'
)

# Configuración de paths
CSV_FILE = Path("heart_failure_clinical_records_dataset.csv")
HISTORY_FILE = Path("patient_history.json")

# Colores
COLORS = {
    'primary': '#2C3E50',
    'secondary': '#3498DB',
    'success': '#27AE60',
    'warning': '#F39C12',
    'danger': '#E74C3C',
    'light': '#ECF0F1',
    'dark': '#34495E'
}


class HeartRiskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HeartRisk Navigator - Sistema Profesional")
        self.root.geometry("1000x700")
        self.root.configure(bg=COLORS['light'])
        
        # Variables
        self.df = None
        self.patient_history = []
        self.last_prediction = None  # Guardar última predicción para exportar
        
        # Cargar dataset de forma asíncrona
        self.load_dataset()
        
        # Cargar historial
        self.patient_history = self.load_history()
        
        # Configurar estilo
        self.setup_style()
        
        # Crear interfaz
        self.create_widgets()
        
        logging.info("Aplicación iniciada")
    
    def load_dataset(self):
        """Carga el dataset con manejo de errores"""
        try:
            self.df = pd.read_csv(CSV_FILE)
            logging.info(f"Dataset cargado: {len(self.df)} registros")
        except FileNotFoundError:
            messagebox.showerror(
                "Error", 
                f"No se encontró el archivo:\n{CSV_FILE}"
            )
            logging.error(f"Archivo no encontrado: {CSV_FILE}")
            # Crear dataset de ejemplo si no existe
            self.df = self.create_sample_dataset()
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar dataset: {e}")
            logging.error(f"Error cargando dataset: {e}")
            self.df = self.create_sample_dataset()
    
    def create_sample_dataset(self):
        """Crea un dataset de ejemplo si no existe el archivo"""
        return pd.DataFrame({
            'age': [65, 70, 55, 60, 75],
            'ejection_fraction': [38, 35, 40, 45, 30],
            'serum_creatinine': [1.1, 1.5, 1.0, 1.3, 2.0],
            'serum_sodium': [137, 135, 140, 138, 130],
            'DEATH_EVENT': [0, 1, 0, 0, 1]
        })
    
    def load_history(self):
        """Carga el historial de pacientes"""
        if HISTORY_FILE.exists():
            try:
                with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_history(self, patient_data):
        """Guarda el historial de pacientes"""
        try:
            self.patient_history.append({
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'data': patient_data
            })
            self.patient_history = self.patient_history[-50:]  # Últimos 50
            with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.patient_history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logging.error(f"Error guardando historial: {e}")
    
    def setup_style(self):
        """Configura el estilo"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), 
                       background=COLORS['light'], foreground=COLORS['primary'])
        style.configure('Header.TLabel', font=('Arial', 11, 'bold'), 
                       background=COLORS['light'], foreground=COLORS['dark'])
    
    def create_widgets(self):
        """Crea la interfaz principal"""
        # Header
        header = tk.Frame(self.root, bg=COLORS['primary'], height=70)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(
            header, 
            text="❤️ HeartRisk Navigator - Sistema con Modelo Real", 
            font=("Arial", 18, "bold"),
            bg=COLORS['primary'], 
            fg='white'
        ).pack(pady=20)
        
        # Contenedor principal
        main_frame = tk.Frame(self.root, bg=COLORS['light'])
        main_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Panel izquierdo - Entrada
        left_panel = tk.LabelFrame(
            main_frame,
            text=" 📋 Datos del Paciente ",
            font=('Arial', 11, 'bold'),
            bg='white',
            padx=20,
            pady=20
        )
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        self.create_input_section(left_panel)
        
        # Panel derecho - Acciones y estadísticas
        right_panel = tk.Frame(main_frame, bg=COLORS['light'])
        right_panel.pack(side='right', fill='both', expand=True)
        
        self.create_action_section(right_panel)
        self.create_stats_section(right_panel)
        
        # Footer
        footer = tk.Label(
            self.root,
            text=f"📊 Usando modelo entrenado | {len(self.df)} pacientes en BD",
            bg=COLORS['dark'],
            fg='white',
            font=('Arial', 9)
        )
        footer.pack(side='bottom', fill='x')
    
    def create_input_section(self, parent):
        """Crea sección de entrada de datos"""
        fields = [
            ("Edad (años):", "age", "65"),
            ("Fracción de Eyección (%):", "ejection_fraction", "38"),
            ("Creatinina Sérica (mg/dL):", "serum_creatinine", "1.1"),
            ("Sodio Sérico (mEq/L):", "serum_sodium", "137")
        ]
        
        self.entries = {}
        
        for i, (label, key, default) in enumerate(fields):
            tk.Label(
                parent,
                text=label,
                font=('Arial', 10, 'bold'),
                bg='white',
                anchor='w'
            ).grid(row=i*2, column=0, sticky='w', pady=(5, 2))
            
            entry = tk.Entry(
                parent,
                font=('Arial', 11),
                width=25
            )
            entry.grid(row=i*2+1, column=0, sticky='ew', pady=(0, 10))
            entry.insert(0, default)
            
            self.entries[key] = entry
        
        # Botones
        btn_frame = tk.Frame(parent, bg='white')
        btn_frame.grid(row=8, column=0, pady=20, sticky='ew')
        
        tk.Button(
            btn_frame,
            text="🔍 Calcular Riesgo",
            command=self.calcular_riesgo_async,
            bg=COLORS['success'],
            fg='white',
            font=('Arial', 10, 'bold'),
            cursor='hand2',
            padx=20,
            pady=12
        ).pack(fill='x', pady=5)
        
        tk.Button(
            btn_frame,
            text="🔄 Limpiar",
            command=self.limpiar_campos,
            bg=COLORS['warning'],
            fg='white',
            font=('Arial', 9),
            cursor='hand2',
            padx=20,
            pady=8
        ).pack(fill='x')
        
        parent.columnconfigure(0, weight=1)
    
    def create_action_section(self, parent):
        """Crea sección de acciones"""
        action_frame = tk.LabelFrame(
            parent,
            text=" ⚙️ Análisis y Reportes ",
            font=('Arial', 11, 'bold'),
            bg='white',
            padx=15,
            pady=15
        )
        action_frame.pack(fill='x', pady=(0, 10))
        
        buttons = [
            ("📊 Ver Gráficos", self.mostrar_graficos, COLORS['secondary']),
            ("📋 Historial", self.mostrar_historial, COLORS['primary']),
            ("📄 Exportar PDF Paciente", self.exportar_pdf_paciente, COLORS['danger'])
        ]
        
        for text, command, color in buttons:
            tk.Button(
                action_frame,
                text=text,
                command=command,
                bg=color,
                fg='white',
                font=('Arial', 9),
                cursor='hand2',
                padx=15,
                pady=8
            ).pack(fill='x', pady=5)
    
    def create_stats_section(self, parent):
        """Crea sección de estadísticas"""
        stats_frame = tk.LabelFrame(
            parent,
            text=" 📊 Estadísticas del Dataset ",
            font=('Arial', 11, 'bold'),
            bg='white',
            padx=15,
            pady=15
        )
        stats_frame.pack(fill='both', expand=True)
        
        if self.df is not None:
            stats = [
                ("Total pacientes:", len(self.df)),
                ("Eventos muerte:", f"{self.df['DEATH_EVENT'].sum()} ({self.df['DEATH_EVENT'].mean()*100:.1f}%)"),
                ("Edad promedio:", f"{self.df['age'].mean():.1f} años"),
                ("FE promedio:", f"{self.df['ejection_fraction'].mean():.1f}%")
            ]
            
            for label, value in stats:
                frame = tk.Frame(stats_frame, bg='white')
                frame.pack(fill='x', pady=5)
                
                tk.Label(
                    frame,
                    text=label,
                    font=('Arial', 9),
                    bg='white',
                    anchor='w'
                ).pack(side='left')
                
                tk.Label(
                    frame,
                    text=str(value),
                    font=('Arial', 9, 'bold'),
                    bg='white',
                    fg=COLORS['secondary'],
                    anchor='e'
                ).pack(side='right')
    
    def get_patient_data(self):
        """Obtiene y valida datos del paciente"""
        try:
            patient = {}
            for key, entry in self.entries.items():
                patient[key] = float(entry.get())
            
            # Validaciones
            if not (0 <= patient['age'] <= 120):
                raise ValueError("Edad debe estar entre 0 y 120")
            if not (0 <= patient['ejection_fraction'] <= 100):
                raise ValueError("FE debe estar entre 0 y 100%")
            if patient['serum_creatinine'] <= 0:
                raise ValueError("Creatinina debe ser mayor a 0")
            if not (100 <= patient['serum_sodium'] <= 160):
                raise ValueError("Sodio debe estar entre 100 y 160")
            
            return patient
        except ValueError as e:
            messagebox.showerror("Error de Validación", str(e))
            return None
    
    def calcular_riesgo_async(self):
        """Calcula riesgo de forma asíncrona para no bloquear la UI"""
        patient = self.get_patient_data()
        if not patient:
            return
        
        # Deshabilitar botón
        self.root.config(cursor="watch")
        self.root.update()
        
        # Crear thread para la predicción
        thread = threading.Thread(target=self.calcular_riesgo_thread, args=(patient,))
        thread.daemon = True
        thread.start()
    
    def calcular_riesgo_thread(self, patient):
        """Ejecuta la predicción en un thread separado"""
        try:
            # AQUÍ SE USA TU MODELO REAL
            pred = predecir_riesgo(patient)
            exp = explicacion_por_cada_factor(patient)
            
            # Guardar última predicción para exportar
            self.last_prediction = {
                'patient': patient,
                'prediction': pred,
                'explanation': exp,
                'timestamp': datetime.now()
            }
            
            # Guardar en historial
            self.save_history({
                **patient,
                'prediction': pred,
                'explanation': exp
            })
            
            # Actualizar UI en el thread principal
            self.root.after(0, lambda: self.mostrar_resultados(patient, pred, exp))
            self.root.after(0, lambda: self.root.config(cursor=""))
            
            logging.info(f"Predicción realizada: {pred['label']}")
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Error en predicción: {e}"))
            self.root.after(0, lambda: self.root.config(cursor=""))
            logging.error(f"Error en predicción: {e}")
    
    def mostrar_resultados(self, patient, pred, exp):
        """Muestra resultados en ventana nueva"""
        result_window = tk.Toplevel(self.root)
        result_window.title("Resultados - Modelo Real")
        result_window.geometry("650x550")
        result_window.configure(bg=COLORS['light'])
        
        # Header
        header = tk.Frame(result_window, bg=COLORS['primary'], height=60)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="📋 Resultados del Modelo",
            font=('Arial', 14, 'bold'),
            bg=COLORS['primary'],
            fg='white'
        ).pack(pady=15)
        
        # Contenedor con scroll
        canvas = tk.Canvas(result_window, bg=COLORS['light'])
        scrollbar = ttk.Scrollbar(result_window, orient="vertical", command=canvas.yview)
        scrollable = tk.Frame(canvas, bg=COLORS['light'])
        
        scrollable.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Datos del paciente
        patient_frame = tk.LabelFrame(
            scrollable,
            text=" Datos Ingresados ",
            font=('Arial', 10, 'bold'),
            bg='white',
            padx=15,
            pady=10
        )
        patient_frame.pack(fill='x', padx=15, pady=10)
        
        labels_esp = {
            'age': 'Edad',
            'ejection_fraction': 'Fracción de Eyección',
            'serum_creatinine': 'Creatinina Sérica',
            'serum_sodium': 'Sodio Sérico'
        }
        
        for key, value in patient.items():
            tk.Label(
                patient_frame,
                text=f"{labels_esp[key]}: {value}",
                font=('Arial', 9),
                bg='white',
                anchor='w'
            ).pack(anchor='w', pady=2)
        
        # Resultado
        prob = pred['probability']
        label = pred['label']
        color = COLORS['danger'] if label == "ALTO RIESGO" else COLORS['success']
        
        result_frame = tk.Frame(scrollable, bg=color, relief='solid', borderwidth=2)
        result_frame.pack(fill='x', padx=15, pady=10)
        
        tk.Label(
            result_frame,
            text=f"⚠️ {label}",
            font=('Arial', 13, 'bold'),
            bg=color,
            fg='white'
        ).pack(pady=8)
        
        tk.Label(
            result_frame,
            text=f"Probabilidad: {prob:.1%}",
            font=('Arial', 11),
            bg=color,
            fg='white'
        ).pack(pady=(0, 8))
        
        # Explicación
        exp_frame = tk.LabelFrame(
            scrollable,
            text=" Análisis del Modelo ",
            font=('Arial', 10, 'bold'),
            bg='white',
            padx=15,
            pady=10
        )
        exp_frame.pack(fill='both', expand=True, padx=15, pady=10)
        
        tk.Label(
            exp_frame,
            text=exp.get('explanation_text', 'Sin explicación disponible'),
            font=('Arial', 9),
            bg='white',
            justify='left',
            wraplength=550
        ).pack(anchor='w')
        
        canvas.pack(side="left", fill="both", expand=True, padx=(15, 0), pady=15)
        scrollbar.pack(side="right", fill="y", pady=15, padx=(0, 15))
        
        # Botón cerrar
        tk.Button(
            result_window,
            text="Cerrar",
            command=result_window.destroy,
            bg=COLORS['dark'],
            fg='white',
            font=('Arial', 9, 'bold'),
            cursor='hand2',
            padx=30,
            pady=10
        ).pack(pady=15)
    
    def mostrar_graficos(self):
        """Muestra gráficos del dataset con explicaciones profesionales"""
        if self.df is None:
            messagebox.showwarning("Advertencia", "No hay datos para graficar")
            return
        
        graph_window = tk.Toplevel(self.root)
        graph_window.title("Análisis del Dataset")
        graph_window.geometry("1000x700")
        
        notebook = ttk.Notebook(graph_window)

        # ===== Gráfico 1: Histograma de edades =====
        tab1 = ttk.Frame(notebook)
        fig1 = Figure(figsize=(7, 5))
        ax1 = fig1.add_subplot(111)
        ax1.hist(self.df['age'], bins=12, color=COLORS['secondary'], edgecolor='black', alpha=0.7)
        ax1.set_xlabel("Edad (años)", fontweight='bold')
        ax1.set_ylabel("Frecuencia", fontweight='bold')
        ax1.set_title("Distribución de Edades", fontweight='bold')
        ax1.grid(axis='y', alpha=0.3)

        canvas1 = FigureCanvasTkAgg(fig1, master=tab1)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)

        # Nota explicativa
        nota1 = ttk.Label(
            tab1,
            text=(
                "Este histograma muestra la distribución de edades de los pacientes "
                "incluidos en el dataset. Se puede observar cuáles son los rangos de edad "
                "más frecuentes, información relevante para evaluar el riesgo promedio "
                "asociado a la insuficiencia cardíaca en la población estudiada."
            ),
            wraplength=850,
            justify="left"
        )
        nota1.pack(pady=5)
        notebook.add(tab1, text="📊 Edad")

        # ===== Gráfico 2: DEATH_EVENT =====
        tab2 = ttk.Frame(notebook)
        fig2 = Figure(figsize=(7, 5))
        ax2 = fig2.add_subplot(111)
        counts = self.df['DEATH_EVENT'].value_counts()
        ax2.bar(['Sobrevivió', 'Falleció'], counts.values,
            color=[COLORS['success'], COLORS['danger']], alpha=0.8)
        ax2.set_ylabel("Número de pacientes", fontweight='bold')
        ax2.set_title("Resultados de pacientes", fontweight='bold')

        for i, v in enumerate(counts.values):
            ax2.text(i, v + 2, str(v), ha='center', fontweight='bold')

        canvas2 = FigureCanvasTkAgg(fig2, master=tab2)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)

        # Nota explicativa
        nota2 = ttk.Label(
            tab2,
            text=(
                "Este gráfico de barras representa la cantidad de pacientes que sobrevivieron "
                "y los que fallecieron. La distribución de estos resultados permite al modelo "
                "entrenado estimar la probabilidad de DEATH_EVENT en función de los factores clínicos."
            ),
            wraplength=850,
            justify="left"
        )
        nota2.pack(pady=5)
        notebook.add(tab2, text="💔 Resultados")

        # ===== Gráfico 3: Boxplot de creatinina vs DEATH_EVENT =====
        tab3 = ttk.Frame(notebook)
        fig3 = Figure(figsize=(7, 5))
        ax3 = fig3.add_subplot(111)
        sns.boxplot(x='DEATH_EVENT', y='serum_creatinine', data=self.df, palette="Set2", ax=ax3)
        ax3.set_xticks([0, 1])
        ax3.set_xticklabels(['Sobrevivió', 'Muerte'])
        ax3.set_title("Creatinina sérica vs DEATH_EVENT", fontweight='bold')

        canvas3 = FigureCanvasTkAgg(fig3, master=tab3)
        canvas3.draw()
        canvas3.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)

        # Nota explicativa
        nota3 = ttk.Label(
            tab3,
            text=(
                "El boxplot muestra cómo varían los niveles de creatinina sérica en los pacientes "
                "según si sobrevivieron o fallecieron. Valores elevados de creatinina se asocian "
                "con un mayor riesgo, lo que ayuda al modelo a identificar factores críticos de mortalidad."
            ),
            wraplength=850,
            justify="left"
        )
        nota3.pack(pady=5)
        notebook.add(tab3, text="💉 Creatinina")

        # ===== Gráfico 4: Heatmap de correlaciones =====
        tab4 = ttk.Frame(notebook)
        fig4 = Figure(figsize=(8, 6))
        ax4 = fig4.add_subplot(111)
        sns.heatmap(self.df.corr(), annot=True, fmt=".2f", cmap="coolwarm", ax=ax4)
        ax4.set_title("Mapa de correlaciones", fontweight='bold')

        canvas4 = FigureCanvasTkAgg(fig4, master=tab4)
        canvas4.draw()
        canvas4.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)

        # Nota explicativa
        nota4 = ttk.Label(
            tab4,
            text=(
                "El heatmap muestra la correlación entre todas las variables del dataset. "
                "Valores cercanos a 1 o -1 indican relaciones fuertes. Esta información permite "
                "al modelo identificar qué factores clínicos están más asociados con el riesgo de mortalidad."
            ),
            wraplength=850,
            justify="left"
        )
        nota4.pack(pady=5)
        notebook.add(tab4, text="📈 Correlaciones")

        # ===== Mostrar todas las pestañas =====
        notebook.pack(expand=True, fill='both')
    
    def mostrar_historial(self):
        """Muestra historial de evaluaciones"""
        hist_window = tk.Toplevel(self.root)
        hist_window.title("Historial de Evaluaciones")
        hist_window.geometry("850x500")
        hist_window.configure(bg=COLORS['light'])
        
        tk.Label(
            hist_window,
            text="📋 Historial de Evaluaciones con Modelo Real",
            font=('Arial', 14, 'bold'),
            bg=COLORS['primary'],
            fg='white'
        ).pack(fill='x', pady=15)
        
        if not self.patient_history:
            tk.Label(
                hist_window,
                text="No hay registros en el historial",
                font=('Arial', 11),
                bg=COLORS['light']
            ).pack(pady=50)
            return
        
        frame = tk.Frame(hist_window, bg='white')
        frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        tree = ttk.Treeview(
            frame,
            columns=('Fecha', 'Edad', 'FE', 'Creatinina', 'Resultado'),
            show='headings',
            height=15
        )
        
        tree.heading('Fecha', text='Fecha/Hora')
        tree.heading('Edad', text='Edad')
        tree.heading('FE', text='FE (%)')
        tree.heading('Creatinina', text='Creatinina')
        tree.heading('Resultado', text='Resultado')
        
        tree.column('Fecha', width=150)
        tree.column('Edad', width=80)
        tree.column('FE', width=80)
        tree.column('Creatinina', width=100)
        tree.column('Resultado', width=150)
        
        for record in reversed(self.patient_history):
            tree.insert('', 'end', values=(
                record['timestamp'],
                f"{record['data']['age']:.0f}",
                f"{record['data']['ejection_fraction']:.0f}",
                f"{record['data']['serum_creatinine']:.2f}",
                record['data']['prediction']['label']
            ))
        
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def exportar_pdf_paciente(self):
        """Exporta reporte profesional en PDF del último paciente evaluado"""
        if not self.last_prediction:
            messagebox.showwarning(
                "Advertencia", 
                "Primero debe evaluar un paciente antes de exportar el reporte"
            )
            return
        
        try:
            filepath = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                initialfile=f"Reporte_Paciente_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            )
            
            if not filepath:
                return
            
            # Crear documento PDF
            doc = SimpleDocTemplate(filepath, pagesize=letter,
                                   rightMargin=50, leftMargin=50,
                                   topMargin=50, bottomMargin=50)
            
            # Contenedor de elementos
            elements = []
            
            # Estilos
            styles = getSampleStyleSheet()
            
            # Estilo personalizado para título
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#2C3E50'),
                spaceAfter=30,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            )
            
            # Estilo para subtítulos
            subtitle_style = ParagraphStyle(
                'CustomSubtitle',
                parent=styles['Heading2'],
                fontSize=16,
                textColor=colors.HexColor('#3498DB'),
                spaceAfter=12,
                spaceBefore=12,
                fontName='Helvetica-Bold'
            )
            
            # Estilo para texto normal
            normal_style = ParagraphStyle(
                'CustomNormal',
                parent=styles['Normal'],
                fontSize=11,
                textColor=colors.HexColor('#333333'),
                spaceAfter=8,
                alignment=TA_JUSTIFY,
                leading=14
            )
            
            # Estilo para info importante
            info_style = ParagraphStyle(
                'InfoStyle',
                parent=styles['Normal'],
                fontSize=12,
                textColor=colors.HexColor('#2C3E50'),
                spaceAfter=6,
                fontName='Helvetica-Bold'
            )
            
            # === ENCABEZADO ===
            logo = Image("logo.jpg", width=80, height=80)
            logo.hAlign = 'LEFT'  # Alineado a la izquierda
            elements.append(logo)

            elements.append(Paragraph("HeartRisk Navigator", title_style))
            elements.append(Paragraph("Reporte de Evaluación de Riesgo Cardiovascular", subtitle_style))
            elements.append(Spacer(1, 0.2*inch))
            
            # Fecha y hora
            fecha_hora = self.last_prediction['timestamp'].strftime("%d/%m/%Y %H:%M:%S")
            elements.append(Paragraph(f"<b>Fecha de evaluación:</b> {fecha_hora}", normal_style))
            elements.append(Spacer(1, 0.3*inch))
            
            # === DATOS DEL PACIENTE ===
            elements.append(Paragraph("▪ DATOS DEL PACIENTE", subtitle_style))
            
            patient = self.last_prediction['patient']
            
            # Tabla de datos del paciente
            patient_data = [
                ['Parámetro', 'Valor', 'Unidad'],
                ['Edad', f"{patient['age']:.0f}", 'años'],
                ['Fracción de Eyección', f"{patient['ejection_fraction']:.1f}", '%'],
                ['Creatinina Sérica', f"{patient['serum_creatinine']:.2f}", 'mg/dL'],
                ['Sodio Sérico', f"{patient['serum_sodium']:.1f}", 'mEq/L']
            ]
            
            patient_table = Table(patient_data, colWidths=[2.5*inch, 1.5*inch, 1*inch])
            patient_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ECF0F1')),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#BDC3C7')),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 11),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F9FA')])
            ]))
            
            elements.append(patient_table)
            elements.append(Spacer(1, 0.4*inch))
            
            # === RESULTADOS DE LA EVALUACIÓN ===
            elements.append(Paragraph("▪ RESULTADO DE LA EVALUACIÓN", subtitle_style))
            
            pred = self.last_prediction['prediction']
            prob = pred['probability']
            label = pred['label']
            
            # Color según riesgo
            if label == "ALTO RIESGO":
                risk_color = colors.HexColor('#E74C3C')
                risk_bg = colors.HexColor('#FADBD8')
            else:
                risk_color = colors.HexColor('#27AE60')
                risk_bg = colors.HexColor('#D5F4E6')
            
            # Tabla de resultado
            result_data = [
                ['Nivel de Riesgo', 'Probabilidad'],
                [label, f"{prob*100:.1f}%"]
            ]
            
            result_table = Table(result_data, colWidths=[3*inch, 2*inch])
            result_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2C3E50')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), risk_bg),
                ('TEXTCOLOR', (0, 1), (-1, -1), risk_color),
                ('GRID', (0, 0), (-1, -1), 2, colors.HexColor('#2C3E50')),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 1), (-1, -1), 16),
                ('TOPPADDING', (0, 1), (-1, -1), 15),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 15)
            ]))
            
            elements.append(result_table)
            elements.append(Spacer(1, 0.4*inch))
            
            ## === ANÁLISIS DE FACTORES DE RIESGO ===
            elements.append(Paragraph("▪ ANÁLISIS DE FACTORES DE RIESGO", subtitle_style))
            elements.append(Spacer(1, 0.1 * inch))

            # Obtener explicación de forma segura
            exp = self.last_prediction.get('explanation', {})
            explanation_text = exp.get('explanation_text', 'No disponible')

            # Separar la explicación en probabilidad y factores (ignorar recomendaciones)
            lines = []

            if "Probabilidad" in explanation_text and "Factores más influyentes:" in explanation_text:
                prob, rest = explanation_text.split("Factores más influyentes:", 1)
                lines.append(prob.strip())
                
                # Tomar solo los factores, ignorar todo lo que venga después de "Recomendaciones"
                if "Recomendaciones" in rest:
                    rest = rest.split("Recomendaciones", 1)[0]
                
                factors_text = rest.strip()
                lines.append("<b>Factores más influyentes:</b>")
                
                for f in factors_text.split("-"):
                    f = f.strip()
                    if f:
                        lines.append(f"• {f}")
            else:
                lines.append(explanation_text)

            # Agregar cada línea como párrafo al PDF
            for line in lines:
                elements.append(Paragraph(line, normal_style))
                elements.append(Spacer(1, 0.1 * inch))

            # Espacio final antes de la siguiente sección
            elements.append(Spacer(1, 0.3 * inch))
            
            # === RECOMENDACIONES ===
            elements.append(Paragraph("▪ RECOMENDACIONES", subtitle_style))
            
            # Usar recomendaciones del factor_explainer.py
            if 'recommendations' in exp and exp['recommendations']:
                recomendaciones = exp['recommendations']
                for i, recom in enumerate(recomendaciones, 1):
                    elements.append(Paragraph(f"<b>{i}.</b> {recom}", normal_style))
            elif 'recomendaciones' in exp and exp['recomendaciones']:
                recomendaciones = exp['recomendaciones']
                for i, recom in enumerate(recomendaciones, 1):
                    elements.append(Paragraph(f"<b>{i}.</b> {recom}", normal_style))
            else:
                # Si no hay recomendaciones en el explicador, usar las del modelo
                elements.append(Paragraph(
                    "Las recomendaciones específicas deben ser proporcionadas por su médico tratante "
                    "basándose en esta evaluación y su historial clínico completo.",
                    normal_style
                ))
            
            elements.append(Spacer(1, 0.5*inch))
            
            # === INTERPRETACIÓN CLÍNICA ===
            elements.append(Paragraph("▪ INTERPRETACIÓN DE PARÁMETROS", subtitle_style))
            
            interpretaciones = self.generar_interpretaciones(patient)
            
            interp_data = [['Parámetro', 'Valor', 'Interpretación']]
            for param, valor, interp in interpretaciones:
                interp_data.append([param, valor, Paragraph(interp, normal_style)])
            
            interp_table = Table(interp_data, colWidths=[1.8*inch, 1*inch, 2.7*inch])
            interp_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (1, -1), 'CENTER'),
                ('ALIGN', (2, 0), (2, 0), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('TOPPADDING', (0, 0), (-1, 0), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#BDC3C7')),
                ('FONTNAME', (0, 1), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (1, -1), 10),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F9FA')]),
                ('TOPPADDING', (0, 1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
                ('LEFTPADDING', (2, 1), (2, -1), 5),
                ('RIGHTPADDING', (2, 1), (2, -1), 5)
            ]))
            
            elements.append(interp_table)
            elements.append(Spacer(1, 0.5*inch))
            
            # === PIE DE PÁGINA (al final del contenido) ===
            disclaimer_style = ParagraphStyle(
                'Disclaimer',
                parent=styles['Normal'],
                fontSize=9,
                textColor=colors.HexColor('#7F8C8D'),
                alignment=TA_JUSTIFY,
                leading=12
            )

            footer_style = ParagraphStyle(
                'Footer',
                parent=disclaimer_style,
                fontSize=8,
                textColor=colors.HexColor('#95A5A6'),
                alignment=TA_CENTER
            )

            # --- Solo un pequeño espacio antes del pie ---
            elements.append(Spacer(1, 0.3 * inch))

            # Línea divisoria superior del pie
            elements.append(HRFlowable(width="100%", color=colors.HexColor('#BDC3C7'), thickness=0.7))
            elements.append(Spacer(1, 0.1 * inch))

            # Texto legal
            elements.append(Paragraph(
                "<b>NOTA IMPORTANTE:</b> Este reporte es generado por un sistema de apoyo al diagnóstico. "
                "Los resultados deben ser interpretados por un profesional de la salud calificado. "
                "No sustituye el criterio médico ni el diagnóstico clínico profesional.",
                disclaimer_style
            ))

            # Línea final de créditos
            elements.append(Spacer(1, 0.05 * inch))
            elements.append(Paragraph(
                f"Reporte generado por HeartRisk Navigator © {datetime.now().strftime('%Y')}",
                footer_style
            ))
            
            # Construir PDF
            doc.build(elements)
            
            messagebox.showinfo(
                "Éxito", 
                f"Reporte PDF generado correctamente:\n{filepath}"
            )
            logging.info(f"PDF exportado: {filepath}")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el PDF: {e}")
            logging.error(f"Error generando PDF: {e}")
    
    def generar_interpretaciones(self, patient):
        """Genera interpretaciones de los parámetros clínicos"""
        interpretaciones = []
        
        # Edad
        if patient['age'] < 50:
            edad_interp = "Edad relativamente joven"
        elif patient['age'] < 65:
            edad_interp = "Edad adulta media"
        elif patient['age'] < 75:
            edad_interp = "Edad adulta mayor - riesgo moderado"
        else:
            edad_interp = "Edad avanzada - riesgo elevado"
        
        interpretaciones.append([
            'Edad',
            f"{patient['age']:.0f} años",
            edad_interp
        ])
        
        # Fracción de Eyección
        if patient['ejection_fraction'] >= 50:
            fe_interp = "Normal - función cardíaca preservada"
        elif patient['ejection_fraction'] >= 40:
            fe_interp = "Levemente reducida - disfunción leve"
        elif patient['ejection_fraction'] >= 30:
            fe_interp = "Moderadamente reducida - disfunción moderada"
        else:
            fe_interp = "Severamente reducida - disfunción severa"
        
        interpretaciones.append([
            'Fracción de Eyección',
            f"{patient['ejection_fraction']:.1f}%",
            fe_interp
        ])
        
        # Creatinina
        if patient['serum_creatinine'] <= 1.2:
            creat_interp = "Normal - función renal adecuada"
        elif patient['serum_creatinine'] <= 1.5:
            creat_interp = "Levemente elevada - vigilar función renal"
        elif patient['serum_creatinine'] <= 2.0:
            creat_interp = "Moderadamente elevada - compromiso renal"
        else:
            creat_interp = "Elevada - insuficiencia renal significativa"
        
        interpretaciones.append([
            'Creatinina Sérica',
            f"{patient['serum_creatinine']:.2f} mg/dL",
            creat_interp
        ])
        
        # Sodio
        if patient['serum_sodium'] < 135:
            sodio_interp = "Bajo (hiponatremia) - puede indicar retención de líquidos"
        elif patient['serum_sodium'] <= 145:
            sodio_interp = "Normal - balance electrolítico adecuado"
        else:
            sodio_interp = "Elevado (hipernatremia) - vigilar hidratación"
        
        interpretaciones.append([
            'Sodio Sérico',
            f"{patient['serum_sodium']:.1f} mEq/L",
            sodio_interp
        ])
        
        return interpretaciones
    
    def exportar_reporte(self):
        """Función legacy - mantener por compatibilidad"""
        self.exportar_pdf_paciente()
    
    def limpiar_campos(self):
        """Limpia campos de entrada"""
        defaults = {'age': '', 'ejection_fraction': '', 
                   'serum_creatinine': '', 'serum_sodium': ''}
        
        for key, entry in self.entries.items():
            entry.delete(0, 'end')
            entry.insert(0, defaults[key])


def main():
    """Función principal"""
    try:
        root = tk.Tk()
        app = HeartRiskApp(root)
        root.mainloop()
    except Exception as e:
        logging.critical(f"Error crítico: {e}")
        messagebox.showerror("Error Crítico", f"Error fatal:\n{e}")


if __name__ == "__main__":
    main()