"""
Quiz de Economía/Finanzas 
"""
import sys   # Proporciona funciones y variables para manipular el entorno de ejecución de Py
import os    # Permite interactuar con el sistema operativo
import sqlite3 # Proporciona una interfaz para trabajar con bases de datos SQLite
import random  # Ofrece funciones para generar números aleatorios y realizar selecciones aleatorias

# Verificar e instalar dependencias automáticamente si es necesario
try:
    import tkinter as tk
    from tkinter import ttk, messagebox
    import pandas as pd
    import numpy as np
    import matplotlib
    matplotlib.use('TkAgg')
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import matplotlib.pyplot as plt
except ImportError as e:
    print(f"Error: {e}")
    print("Instalando dependencias necesarias...")
    try:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas", "numpy", "matplotlib"])
        print("Dependencias instaladas correctamente. Por favor, ejecuta el programa nuevamente.")
    except Exception as install_error:
        print(f"Error instalando dependencias: {install_error}")
    sys.exit(1)

print("Iniciando aplicación Quiz...")

# =============== BASE DE DATOS INTEGRADA ===============

class DatabaseManager:
    """Gestor de base de datos SQLite integrada"""
    
    def __init__(self):
        self.db_path = "quiz_economia.db"
        self.init_database()
    
    def init_database(self):
        """Inicializa la base de datos con preguntas de 3 dificultades"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Crear tabla de preguntas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS preguntas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                categoria TEXT NOT NULL,
                tema TEXT NOT NULL,
                dificultad INTEGER NOT NULL CHECK (dificultad IN (1, 2, 3)),
                pregunta TEXT NOT NULL,
                opcion_a TEXT NOT NULL,
                opcion_b TEXT NOT NULL,
                opcion_c TEXT NOT NULL,
                opcion_d TEXT NOT NULL,
                correcta TEXT NOT NULL CHECK (correcta IN ('a', 'b', 'c', 'd'))
            )
        ''')
        
        # Verificar si ya hay datos
        cursor.execute("SELECT COUNT(*) FROM preguntas")
        count = cursor.fetchone()[0]
        
        if count == 0:
            self._insertar_datos_ejemplo(cursor)
        
        conn.commit()
        conn.close()
        print(f"Base de datos inicializada con {count} preguntas existentes")
    
    def _insertar_datos_ejemplo(self, cursor):
        """Inserta preguntas de ejemplo con 3 niveles de dificultad"""
        preguntas = [
            # ========== MICROECONOMÍA ==========
            # Dificultad 1 (Fácil)
            ('micro', 'Oferta y Demanda', 1, 
             '¿Qué ocurre en el mercado cuando aumenta la demanda?',
             'Disminuye el precio', 'Aumenta el precio', 'No cambia nada', 'Disminuye la oferta',
             'b'),
            
            ('micro', 'Oferta y Demanda', 1,
             '¿Qué representa la ley de la oferta?',
             'Precio alto, oferta baja', 'Precio alto, oferta alta', 'Precio bajo, oferta alta', 'No hay relación',
             'b'),
            
            ('micro', 'Costos', 1,
             'Los costos que no varían con la producción se llaman:',
             'Costos variables', 'Costos fijos', 'Costos marginales', 'Costos totales',
             'b'),
            
            # Dificultad 2 (Medio)
            ('micro', 'Oferta y Demanda', 2,
             'El punto donde se cruzan oferta y demanda se llama:',
             'Punto de quiebre', 'Equilibrio de mercado', 'Punto crítico', 'Intersección económica',
             'b'),
            
            ('micro', 'Elasticidad', 2,
             'Un bien con elasticidad precio mayor a 1 se considera:',
             'Elástico', 'Inelástico', 'Unitario', 'Complementario',
             'a'),
            
            ('micro', 'Mercados', 2,
             'En competencia perfecta, las empresas son:',
             'Formadoras de precio', 'Aceptantes de precio', 'Monopolistas', 'Oligopolistas',
             'b'),
            
            # Dificultad 3 (Difícil)
            ('micro', 'Elasticidad', 3,
             'La elasticidad cruzada de demanda mide:',
             'Cambio en cantidad demandada por cambio en precio del bien', 
             'Cambio en cantidad demandada por cambio en ingreso',
             'Cambio en cantidad demandada por cambio en precio de bien relacionado',
             'Cambio en cantidad ofrecida por cambio en precio',
             'c'),
            
            ('micro', 'Teoría del Consumidor', 3,
             'La utilidad marginal decreciente establece que:',
             'Cada unidad adicional proporciona más utilidad', 
             'Cada unidad adicional proporciona menos utilidad',
             'La utilidad total siempre aumenta',
             'La utilidad es constante',
             'b'),
            
            # ========== MACROECONOMÍA ==========
            # Dificultad 1 (Fácil)
            ('macro', 'PIB', 1,
             '¿Qué mide el PIB?',
             'La riqueza total', 'El valor de bienes y servicios finales', 'La inflación', 'El desempleo',
             'b'),
            
            ('macro', 'Inflación', 1,
             'La inflación se mide comúnmente con:',
             'IPC', 'PIB', 'Tasa de interés', 'Déficit fiscal',
             'a'),
            
            ('macro', 'Desempleo', 1,
             'El desempleo que ocurre en recesiones económicas es:',
             'Friccional', 'Estructural', 'Cíclico', 'Estacional',
             'c'),
            
            # Dificultad 2 (Medio)
            ('macro', 'Política Fiscal', 2,
             'La política fiscal expansiva implica:',
             'Aumentar impuestos y reducir gasto', 'Reducir impuestos y aumentar gasto', 
             'Mantener impuestos y gasto constantes', 'Solo reducir impuestos',
             'b'),
            
            ('macro', 'Balanza Comercial', 2,
             'Un superávit comercial ocurre cuando:',
             'Las importaciones superan a las exportaciones', 'Las exportaciones superan a las importaciones',
             'Importaciones y exportaciones son iguales', 'No hay comercio internacional',
             'b'),
            
            ('macro', 'Dinero', 2,
             'La función principal del dinero es:',
             'Solo medio de cambio', 'Medio de cambio, unidad de cuenta y reserva de valor',
             'Solo reserva de valor', 'Solo unidad de cuenta',
             'b'),
            
            # Dificultad 3 (Difícil)
            ('macro', 'Política Monetaria', 3,
             'El efecto Crowding Out se refiere a:',
             'Aumento de inversión privada por gasto público', 
             'Desplazamiento de inversión privada por gasto público',
             'Aumento del consumo por menores impuestos',
             'Reducción del ahorro por mayor consumo',
             'b'),
            
            ('macro', 'Crecimiento Económico', 3,
             'En el modelo de Solow, el estado estacionario ocurre cuando:',
             'El ahorro es cero', 'La inversión iguala la depreciación',
             'El consumo es máximo', 'La población no crece',
             'b'),
            
            # ========== FINANZAS ==========
            # Dificultad 1 (Fácil)
            ('finanzas', 'Interés Compuesto', 1,
             'El interés compuesto se calcula sobre:',
             'Solo el capital inicial', 'Capital + intereses acumulados', 'La tasa nominal', 'La inflación',
             'b'),
            
            ('finanzas', 'Diversificación', 1,
             'La diversificación reduce:',
             'La rentabilidad', 'El riesgo', 'La liquidez', 'Los costos',
             'b'),
            
            ('finanzas', 'Valor Presente', 1,
             'El valor presente neto (VPN) se usa para:',
             'Medir inflación', 'Evaluar proyectos de inversión', 'Calcular intereses', 'Determinar precios',
             'b'),
            
            # Dificultad 2 (Medio)
            ('finanzas', 'Riesgo y Retorno', 2,
             'La relación entre riesgo y rendimiento esperado es:',
             'Inversa', 'Directa', 'No existe relación', 'Aleatoria',
             'b'),
            
            ('finanzas', 'Acciones y Bonos', 2,
             'La principal diferencia entre acciones y bonos es:',
             'Las acciones representan deuda, los bonos propiedad',
             'Los bonos representan deuda, las acciones propiedad',
             'Ambos representan deuda',
             'Ambos representan propiedad',
             'b'),
            
            ('finanzas', 'Mercado de Capitales', 2,
             'La bolsa de valores es un mercado:',
             'Primario', 'Secundario', 'Terciario', 'Informal',
             'b'),
            
            # Dificultad 3 (Difícil)
            ('finanzas', 'Beta', 3,
             'El coeficiente Beta mide:',
             'El riesgo diversificable de un activo', 'El riesgo no diversificable de un activo',
             'La rentabilidad esperada', 'La volatilidad total',
             'b'),
            
            ('finanzas', 'CAPM', 3,
             'En el modelo CAPM, la fórmula es: E(R) = Rf + β*(Rm - Rf). ¿Qué representa Rm?',
             'Tasa libre de riesgo', 'Rentabilidad del mercado', 'Rentabilidad del activo', 'Prima de riesgo',
             'b'),
            
            ('finanzas', 'Opciones Financieras', 3,
             'Una opción call da al comprador el derecho a:',
             'Vender un activo a precio fijo', 'Comprar un activo a precio fijo',
             'Vender un activo a precio variable', 'Comprar un activo a precio variable',
             'b'),
            
            # ========== MÁS PREGUNTAS PARA VARIEDAD ==========
            ('micro', 'Competencia', 1, 'En un mercado competitivo, las empresas son:', 
             'Pocas y grandes', 'Muchas y pequeñas', 'Una sola', 'Dos empresas dominantes', 'b'),
            
            ('macro', 'Bancos Centrales', 2, 'La principal función de un banco central es:', 
             'Realizar préstamos a personas', 'Controlar la política monetaria', 
             'Competir con bancos comerciales', 'Emitir acciones', 'b'),
            
            ('finanzas', 'Inflación', 2, 'La inflación afecta a los ahorradores porque:', 
             'Aumenta el poder adquisitivo', 'Reduce el poder adquisitivo', 
             'No afecta el poder adquisitivo', 'Solo afecta a los deudores', 'b'),
            
            ('micro', 'Externalidades', 3, 'Una externalidad negativa ocurre cuando:', 
             'Los beneficios sociales superan los privados', 'Los costos sociales superan los privados', 
             'No hay diferencia entre costos sociales y privados', 'El gobierno interviene', 'b'),
            
            ('macro', 'Paridad de Poder Adquisitivo', 3, 'La teoría de la PPA sugiere que:', 
             'Los tipos de cambio reflejan diferencias de inflación', 
             'Los tipos de cambio son siempre fijos', 
             'La inflación no afecta los tipos de cambio', 
             'Los mercados son siempre eficientes', 'a')
        ]
        
        cursor.executemany('''
            INSERT INTO preguntas (categoria, tema, dificultad, pregunta, opcion_a, opcion_b, opcion_c, opcion_d, correcta)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', preguntas)
        
        print(f"Insertadas {len(preguntas)} preguntas en la base de datos")

    def obtener_preguntas(self, categorias, temas, dificultad=None):
        """Obtiene preguntas filtradas de la base de datos"""
        conn = sqlite3.connect(self.db_path)
        
        query = '''
            SELECT * FROM preguntas 
            WHERE categoria IN ({}) AND tema IN ({})
        '''.format(','.join('?' * len(categorias)), ','.join('?' * len(temas)))
        
        params = categorias + temas
        
        if dificultad:
            query += ' AND dificultad = ?'
            params.append(dificultad)
        
        query += ' ORDER BY RANDOM()'
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        
        return df

    def obtener_temas_disponibles(self, categorias):
        """Obtiene temas disponibles para las categorías dadas"""
        conn = sqlite3.connect(self.db_path)
        
        query = '''
            SELECT DISTINCT tema FROM preguntas 
            WHERE categoria IN ({})
            ORDER BY tema
        '''.format(','.join('?' * len(categorias)))
        
        cursor = conn.cursor()
        cursor.execute(query, categorias)
        temas = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        return temas

    def obtener_estadisticas_dificultad(self):
        """Obtiene estadísticas por dificultad"""
        conn = sqlite3.connect(self.db_path)
        query = '''
            SELECT dificultad, COUNT(*) as cantidad 
            FROM preguntas 
            GROUP BY dificultad 
            ORDER BY dificultad
        '''
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

# =============== MÓDULOS DEL QUIZ ===============

class BancoPreguntas:
    """Gestión de preguntas desde base de datos"""
    
    def __init__(self):
        self.db = DatabaseManager()
    
    def temas_disponibles(self, categorias):
        return self.db.obtener_temas_disponibles(categorias)
    
    def filtrar(self, categorias, temas, dificultad=None):
        return self.db.obtener_preguntas(categorias, temas, dificultad)
    
    def samplear(self, df, n=8):
        if len(df) <= n:
            return df.copy()
        return df.sample(n=n, random_state=42).copy()
    
    def mostrar_estadisticas(self):
        """Muestra estadísticas de la base de datos"""
        return self.db.obtener_estadisticas_dificultad()

class QuizEngine:
    """Lógica del quiz integrada"""
    
    def __init__(self, df_preguntas):
        self.df_preguntas = df_preguntas.reset_index(drop=True)
        self.total = len(df_preguntas)
        self.idx = 0
        self.elegidas = [''] * self.total
        self.tiempos = [0] * self.total
        self.inicio_pregunta = None
    
    def pregunta_actual(self):
        if self.idx < self.total:
            return self.df_preguntas.iloc[self.idx]
        return None
    
    def iniciar_pregunta(self):
        self.inicio_pregunta = pd.Timestamp.now()
    
    def marcar_respuesta(self, letra):
        self.elegidas[self.idx] = letra
    
    def ir_siguiente(self):
        if self.idx < self.total - 1:
            if self.inicio_pregunta is not None:
                fin = pd.Timestamp.now()
                self.tiempos[self.idx] = (fin - self.inicio_pregunta).total_seconds()
            self.idx += 1
            return True
        return False
    
    def ir_anterior(self):
        if self.idx > 0:
            if self.inicio_pregunta is not None:
                fin = pd.Timestamp.now()
                self.tiempos[self.idx] = (fin - self.inicio_pregunta).total_seconds()
            self.idx -= 1
            return True
        return False
    
    def finalizar(self):
        if self.inicio_pregunta is not None and self.tiempos[self.idx] == 0:
            fin = pd.Timestamp.now()
            self.tiempos[self.idx] = (fin - self.inicio_pregunta).total_seconds()
        
        correctas = 0
        resultados = []
        
        for i in range(self.total):
            pregunta = self.df_preguntas.iloc[i]
            elegida = self.elegidas[i]
            correcta = str(pregunta['correcta']).lower().strip()
            es_correcta = (elegida != '' and elegida.lower() == correcta)
            
            if es_correcta:
                correctas += 1
            
            resultados.append({
                'id': pregunta['id'],
                'categoria': pregunta['categoria'],
                'tema': pregunta['tema'],
                'dificultad': pregunta['dificultad'],
                'pregunta': pregunta['pregunta'],
                'opcion_elegida': elegida,
                'correcta': correcta,
                'correcta_bool': es_correcta,
                'tiempo_seg': self.tiempos[i]
            })
        
        df_resultados = pd.DataFrame(resultados)
        return correctas, self.total, df_resultados

# Funciones de gráficos (se mantienen igual)
def grafico_barras_por_tema(df):
    fig, ax = plt.subplots(figsize=(6, 4))
    try:
        if 'tema' in df.columns and 'correcta_bool' in df.columns:
            resultado_por_tema = df.groupby('tema')['correcta_bool'].mean() * 100
            bars = ax.bar(resultado_por_tema.index, resultado_por_tema.values, color='skyblue')
            ax.set_title('Aciertos por Tema')
            ax.set_ylabel('Porcentaje Correcto (%)')
            plt.xticks(rotation=45, ha='right')
    except Exception:
        ax.text(0.5, 0.5, 'Datos insuficientes', ha='center', va='center', transform=ax.transAxes)
    fig.tight_layout()
    return fig

def grafico_linea_evolucion(df):
    fig, ax = plt.subplots(figsize=(6, 4))
    try:
        if 'correcta_bool' in df.columns:
            df_sorted = df.reset_index(drop=True)
            acumulado_correcto = df_sorted['correcta_bool'].cumsum()
            preguntas = range(1, len(df_sorted) + 1)
            porcentaje_acumulado = (acumulado_correcto / preguntas) * 100
            ax.plot(preguntas, porcentaje_acumulado, marker='o', linewidth=2)
            ax.set_title('Evolución del Desempeño')
            ax.set_xlabel('Número de Pregunta')
            ax.set_ylabel('Porcentaje Acumulado (%)')
            ax.grid(True, alpha=0.3)
    except Exception:
        ax.text(0.5, 0.5, 'Datos insuficientes', ha='center', va='center', transform=ax.transAxes)
    fig.tight_layout()
    return fig

def grafico_dificultad(df):
    """Nuevo gráfico para mostrar desempeño por dificultad"""
    fig, ax = plt.subplots(figsize=(6, 4))
    try:
        if 'dificultad' in df.columns and 'correcta_bool' in df.columns:
            resultado_por_dificultad = df.groupby('dificultad')['correcta_bool'].mean() * 100
            dificultades = ['Fácil', 'Medio', 'Difícil']
            valores = [resultado_por_dificultad.get(i, 0) for i in range(1, 4)]
            bars = ax.bar(dificultades, valores, color=['green', 'orange', 'red'])
            ax.set_title('Desempeño por Dificultad')
            ax.set_ylabel('Porcentaje Correcto (%)')
            
            # Agregar valores en las barras
            for bar, valor in zip(bars, valores):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                       f'{valor:.1f}%', ha='center', va='bottom')
    except Exception:
        ax.text(0.5, 0.5, 'Datos insuficientes', ha='center', va='center', transform=ax.transAxes)
    fig.tight_layout()
    return fig

# =============== INTERFAZ MEJORADA CON BOTONES VISIBLES ===============

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz de Economía y Finanzas - Base de Datos")
        self.root.geometry("900x700")  # Aumenté el tamaño para mejor visibilidad
        self.root.configure(bg='white')
        
        # Variables
        self.sel_micro = tk.BooleanVar(value=True)
        self.sel_macro = tk.BooleanVar(value=True)
        self.sel_fin = tk.BooleanVar(value=True)
        self.dificultad = tk.StringVar(value="todas")
        self.temas_vars = {}
        
        # Cargar datos desde base de datos
        self.banco = BancoPreguntas()
        
        self.mostrar_inicio()
    
    def limpiar_pantalla(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def mostrar_inicio(self):
        self.limpiar_pantalla()
        
        # Título principal
        titulo = tk.Label(self.root, text=" Quiz de Economía y Finanzas", 
                         font=('Arial', 20, 'bold'), bg='white', fg='navy')
        titulo.pack(pady=30)
        
        subtitulo = tk.Label(self.root, text="Base de Datos con 3 Niveles de Dificultad", 
                           font=('Arial', 12), bg='white', fg='gray')
        subtitulo.pack(pady=5)
        
        # Estadísticas rápidas
        stats = self.banco.mostrar_estadisticas()
        stats_text = "Preguntas disponibles:\n"
        for _, row in stats.iterrows():
            nivel = ["Fácil", "Medio", "Difícil"][row['dificultad'] - 1]
            stats_text += f"• {nivel}: {row['cantidad']} preguntas\n"
        
        lbl_stats = tk.Label(self.root, text=stats_text, 
                           font=('Arial', 10), bg='white', justify='left')
        lbl_stats.pack(pady=10)
        
        # Botón para comenzar (más grande y visible)
        btn_comenzar = tk.Button(self.root, text=" COMENZAR QUIZ", 
                               font=('Arial', 16, 'bold'), bg='#4CAF50', fg='white',
                               command=self.mostrar_configuracion,
                               width=20, height=2, relief='raised', bd=3)
        btn_comenzar.pack(pady=30)
        
        # Información adicional
        info_frame = tk.Frame(self.root, bg='white')
        info_frame.pack(pady=20)
        
        info_text = """
• Selecciona entre 3 categorías: Micro, Macro y Finanzas
• Elige el nivel de dificultad: Fácil, Medio o Difícil  
• 8 preguntas por quiz con timer de 10 minutos
• Resultados con gráficos detallados
        """
        lbl_info = tk.Label(info_frame, text=info_text, font=('Arial', 10), 
                          bg='white', justify='left')
        lbl_info.pack()
    
    def mostrar_configuracion(self):
        self.limpiar_pantalla()
        
        # Frame principal con scroll para mejor visibilidad
        main_container = tk.Frame(self.root, bg='white')
        main_container.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Título
        titulo = tk.Label(main_container, text="⚙️ CONFIGURAR QUIZ", 
                         font=('Arial', 18, 'bold'), bg='white', fg='navy')
        titulo.pack(pady=15)
        
        # Frame para opciones (organizado en fila)
        opciones_frame = tk.Frame(main_container, bg='white')
        opciones_frame.pack(fill='both', expand=True, pady=10)
        
        # ========== COLUMNA IZQUIERDA - CATEGORÍAS ==========
        cat_frame = tk.LabelFrame(opciones_frame, text="📚 CATEGORÍAS", 
                                 font=('Arial', 12, 'bold'), bg='white', 
                                 padx=15, pady=15, relief='groove', bd=2)
        cat_frame.pack(side='left', fill='both', expand=True, padx=5)
        
        # Botones de categorías más grandes y visibles
        categorias = [
            (" Microeconomía", self.sel_micro),
            (" Macroeconomía", self.sel_macro),
            (" Finanzas", self.sel_fin)
        ]
        
        for texto, variable in categorias:
            btn = tk.Checkbutton(cat_frame, text=texto, variable=variable,
                               command=self.actualizar_temas,
                               font=('Arial', 11, 'bold'), bg='white',
                               selectcolor='lightgreen', height=2,
                               width=20, anchor='w')
            btn.pack(fill='x', pady=8, padx=10)
        
        # ========== COLUMNA CENTRAL - TEMAS ==========
        temas_frame = tk.LabelFrame(opciones_frame, text="📖 TEMAS DISPONIBLES",
                                   font=('Arial', 12, 'bold'), bg='white',
                                   padx=15, pady=15, relief='groove', bd=2)
        temas_frame.pack(side='left', fill='both', expand=True, padx=5)
        
        # Canvas con scroll para temas
        canvas_container = tk.Frame(temas_frame, bg='white')
        canvas_container.pack(fill='both', expand=True)
        
        # Canvas y scrollbar
        self.canvas = tk.Canvas(canvas_container, bg='white', height=200)
        scrollbar = tk.Scrollbar(canvas_container, orient='vertical', command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg='white')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # ========== COLUMNA DERECHA - DIFICULTAD ==========
        dificultad_frame = tk.LabelFrame(opciones_frame, text=" NIVEL DE DIFICULTAD",
                                        font=('Arial', 12, 'bold'), bg='white',
                                        padx=15, pady=15, relief='groove', bd=2)
        dificultad_frame.pack(side='left', fill='both', expand=True, padx=5)
        
        # Botones de dificultad más visibles
        dificultades = [
            ("✅ Todas las dificultades", "todas", 'black'),
            ("🟢 Fácil (Nivel 1)", "1", 'green'),
            ("🟡 Medio (Nivel 2)", "2", 'orange'),
            ("🔴 Difícil (Nivel 3)", "3", 'red')
        ]
        
        for texto, valor, color in dificultades:
            btn = tk.Radiobutton(dificultad_frame, text=texto, variable=self.dificultad, 
                               value=valor, font=('Arial', 11), bg='white', fg=color,
                               selectcolor='lightblue', height=2,
                               width=20, anchor='w')
            btn.pack(fill='x', pady=8, padx=10)
        
        # ========== BOTONES DE CONTROL ==========
        control_frame = tk.Frame(main_container, bg='white', pady=20)
        control_frame.pack(fill='x')
        
        # Botón Volver
        btn_volver = tk.Button(control_frame, text="⬅️ VOLVER", 
                              font=('Arial', 12, 'bold'), bg='#607D8B', fg='white',
                              command=self.mostrar_inicio,
                              width=15, height=1, relief='raised', bd=2)
        btn_volver.pack(side='left', padx=20)
        
        # Botón Comenzar (muy visible)
        btn_comenzar = tk.Button(control_frame, text=" COMENZAR QUIZ", 
                               font=('Arial', 14, 'bold'), bg='#2196F3', fg='white',
                               command=self.iniciar_quiz,
                               width=20, height=2, relief='raised', bd=3)
        btn_comenzar.pack(side='right', padx=20)
        
        # Botón Estadísticas
        btn_stats = tk.Button(control_frame, text=" VER ESTADÍSTICAS", 
                            font=('Arial', 10, 'bold'), bg='#FF9800', fg='white',
                            command=self.mostrar_estadisticas_completas,
                            width=15, height=1, relief='raised', bd=2)
        btn_stats.pack(side='left', padx=10)
        
        self.actualizar_temas()
    
    def mostrar_estadisticas_completas(self):
        """Muestra ventana con estadísticas completas de la base de datos"""
        stats = self.banco.mostrar_estadisticas()
        
        stats_window = tk.Toplevel(self.root)
        stats_window.title(" Estadísticas de la Base de Datos")
        stats_window.geometry("400x300")
        stats_window.configure(bg='white')
        
        tk.Label(stats_window, text=" ESTADÍSTICAS COMPLETAS", 
                font=('Arial', 16, 'bold'), bg='white').pack(pady=20)
        
        # Estadísticas por dificultad
        for _, row in stats.iterrows():
            nivel = ["Fácil", "Medio", "Difícil"][row['dificultad'] - 1]
            color = ['green', 'orange', 'red'][row['dificultad'] - 1]
            texto = f"• {nivel}: {row['cantidad']} preguntas"
            lbl = tk.Label(stats_window, text=texto, font=('Arial', 12), 
                          bg='white', fg=color)
            lbl.pack(pady=5)
        
        # Estadísticas por categoría
        categorias = ['micro', 'macro', 'finanzas']
        tk.Label(stats_window, text="\nPor categoría:", 
                font=('Arial', 12, 'bold'), bg='white').pack(pady=10)
        
        for cat in categorias:
            temas = self.banco.temas_disponibles([cat])
            total_preguntas = sum(1 for _ in temas)  # Simplificado para demo
            texto = f"• {cat.title()}: {len(temas)} temas"
            lbl = tk.Label(stats_window, text=texto, font=('Arial', 10), 
                          bg='white')
            lbl.pack(pady=2)
        
        tk.Button(stats_window, text="Cerrar", 
                 command=stats_window.destroy).pack(pady=20)
    
    def actualizar_temas(self):
        """Actualiza la lista de temas con mejor visualización"""
        # Limpiar frame de temas
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        categorias = []
        if self.sel_micro.get(): categorias.append('micro')
        if self.sel_macro.get(): categorias.append('macro')
        if self.sel_fin.get(): categorias.append('finanzas')
        
        if not categorias:
            label = tk.Label(self.scrollable_frame, 
                            text=" Selecciona al menos una categoría\npara ver los temas disponibles", 
                            font=('Arial', 10, 'bold'), bg='white', fg='gray',
                            justify='center')
            label.pack(pady=20)
            return
        
        temas = self.banco.temas_disponibles(categorias)
        self.temas_vars = {}
        
        if not temas:
            label = tk.Label(self.scrollable_frame, 
                            text="No hay temas disponibles\npara las categorías seleccionadas", 
                            font=('Arial', 10), bg='white', fg='red')
            label.pack(pady=10)
            return
        
        # Título con cantidad de temas
        titulo_temas = tk.Label(self.scrollable_frame, 
                               text=f"📚 {len(temas)} temas encontrados:", 
                               font=('Arial', 11, 'bold'), bg='white')
        titulo_temas.pack(pady=5)
        
        # Crear checkboxes para cada tema con mejor formato
        for tema in temas:
            frame_tema = tk.Frame(self.scrollable_frame, bg='white')
            frame_tema.pack(fill='x', pady=3, padx=10)
            
            var = tk.BooleanVar(value=True)
            self.temas_vars[tema] = var
            
            chk = tk.Checkbutton(frame_tema, text=tema, variable=var,
                               font=('Arial', 10), bg='white',
                               selectcolor='lightblue', width=25, anchor='w')
            chk.pack(side='left')
            
            # Indicador de categoría
            cat_color = {'micro': '🟢', 'macro': '🔵', 'finanzas': '🟣'}
            for cat in categorias:
                if cat in tema.lower() or any(cat in t for t in [tema]):
                    lbl_cat = tk.Label(frame_tema, text=cat_color.get(cat, '⚫'), 
                                     font=('Arial', 8), bg='white')
                    lbl_cat.pack(side='right')
                    break
        
        # Actualizar canvas
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def iniciar_quiz(self):
        categorias = []
        if self.sel_micro.get(): categorias.append('micro')
        if self.sel_macro.get(): categorias.append('macro')
        if self.sel_fin.get(): categorias.append('finanzas')
        
        if not categorias:
            messagebox.showwarning("Configuración Incompleta", 
                                 "❌ Debes seleccionar al menos una categoría")
            return
        
        temas_sel = [tema for tema, var in self.temas_vars.items() if var.get()]
        if not temas_sel:
            messagebox.showwarning("Configuración Incompleta", 
                                 "❌ Debes seleccionar al menos un tema")
            return
        
        # Procesar dificultad seleccionada
        dificultad_seleccionada = None if self.dificultad.get() == "todas" else int(self.dificultad.get())
        
        df_filtrado = self.banco.filtrar(categorias, temas_sel, dificultad_seleccionada)
        if len(df_filtrado) == 0:
            messagebox.showwarning("Sin Preguntas", 
                                 "📭 No hay preguntas que coincidan con los filtros seleccionados.\n\n"
                                 "💡 Intenta con:\n• Menos filtros\n• Otra dificultad\n• Más categorías")
            return
        
        n_preguntas = min(8, len(df_filtrado))
        df_quiz = self.banco.samplear(df_filtrado, n=n_preguntas)
        
        # Mostrar info sobre las preguntas seleccionadas
        niveles = df_quiz['dificultad'].value_counts().sort_index()
        info_dificultad = "🎯 Preguntas seleccionadas:\n\n"
        for nivel, cantidad in niveles.items():
            nombre_nivel = ["Fácil", "Medio", "Difícil"][nivel - 1]
            color_emoji = ["🟢", "🟡", "🔴"][nivel - 1]
            info_dificultad += f"{color_emoji} {nombre_nivel}: {cantidad} preguntas\n"
        
        info_dificultad += f"\n📊 Total: {n_preguntas} preguntas"
        
        self.quiz = QuizEngine(df_quiz)
        self.tiempo_restante = 600
        self.timer_id = None
        
        messagebox.showinfo("✅ Configuración Lista", info_dificultad)
        self.mostrar_quiz()

    # Los métodos restantes (mostrar_quiz, cargar_pregunta_actual, etc.) se mantienen igual
    def mostrar_quiz(self):
        self.limpiar_pantalla()
        
        # Header con información de dificultad
        header_frame = tk.Frame(self.root, bg='lightgray', height=50)
        header_frame.pack(fill='x', padx=10, pady=5)
        header_frame.pack_propagate(False)
        
        self.lbl_info = tk.Label(header_frame, text="Pregunta 1/8", 
                                font=('Arial', 11, 'bold'), bg='lightgray')
        self.lbl_info.pack(side='left', padx=10)
        
        self.lbl_dificultad = tk.Label(header_frame, text="Dificultad: -", 
                                      font=('Arial', 10), bg='lightgray')
        self.lbl_dificultad.pack(side='left', padx=20)
        
        self.lbl_timer = tk.Label(header_frame, text="10:00", 
                                 font=('Arial', 12, 'bold'), bg='lightgray', fg='red')
        self.lbl_timer.pack(side='right', padx=10)
        
        # Pregunta
        pregunta_frame = tk.Frame(self.root, bg='white', padx=20, pady=20)
        pregunta_frame.pack(fill='x', padx=10, pady=10)
        
        self.lbl_pregunta = tk.Label(pregunta_frame, text="", wraplength=700,
                                    font=('Arial', 12, 'bold'), bg='white', justify='left')
        self.lbl_pregunta.pack(anchor='w')
        
        # Opciones
        opciones_frame = tk.Frame(self.root, bg='white', padx=20, pady=10)
        opciones_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.botones_opciones = []
        for i in range(4):
            btn = tk.Button(opciones_frame, text="", font=('Arial', 10),
                           command=lambda idx=i: self.seleccionar_opcion(idx),
                           width=60, height=2, bg='white', relief='raised')
            btn.pack(fill='x', pady=5)
            self.botones_opciones.append(btn)
        
        # Feedback
        self.lbl_feedback = tk.Label(self.root, text="", font=('Arial', 11), bg='white')
        self.lbl_feedback.pack(pady=10)
        
        # Navegación
        nav_frame = tk.Frame(self.root, bg='white', pady=20)
        nav_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Button(nav_frame, text="← Anterior", font=('Arial', 10),
                 command=self.anterior_pregunta).pack(side='left')
        
        tk.Button(nav_frame, text="Siguiente →", font=('Arial', 10),
                 command=self.siguiente_pregunta).pack(side='left', padx=10)
        
        tk.Button(nav_frame, text="Finalizar Quiz", font=('Arial', 10, 'bold'), bg='red', fg='white',
                 command=self.finalizar_quiz).pack(side='right')
        
        self.cargar_pregunta_actual()
        self.iniciar_timer()
    
    def cargar_pregunta_actual(self):
        pregunta = self.quiz.pregunta_actual()
        if pregunta is None:
            self.finalizar_quiz()
            return
        
        self.quiz.iniciar_pregunta()
        
        self.lbl_info.config(text=f"Pregunta {self.quiz.idx + 1}/{self.quiz.total}")
        
        # Mostrar nivel de dificultad con color
        nivel = pregunta['dificultad']
        nombre_dificultad = ["Fácil", "Medio", "Difícil"][nivel - 1]
        color_dificultad = ['green', 'orange', 'red'][nivel - 1]
        self.lbl_dificultad.config(text=f"Dificultad: {nombre_dificultad}", fg=color_dificultad)
        
        self.lbl_pregunta.config(text=pregunta['pregunta'])
        
        opciones = [
            f"A) {pregunta['opcion_a']}",
            f"B) {pregunta['opcion_b']}",
            f"C) {pregunta['opcion_c']}",
            f"D) {pregunta['opcion_d']}"
        ]
        
        for i, texto in enumerate(opciones):
            self.botones_opciones[i].config(text=texto, bg='white')
        
        respuesta_actual = self.quiz.elegidas[self.quiz.idx]
        if respuesta_actual:
            letras = ['a', 'b', 'c', 'd']
            if respuesta_actual in letras:
                idx = letras.index(respuesta_actual)
                self.botones_opciones[idx].config(bg='lightblue')
            self.lbl_feedback.config(text=f"Seleccionado: {respuesta_actual.upper()}", fg='blue')
        else:
            self.lbl_feedback.config(text="")
    
    def seleccionar_opcion(self, indice):
        letras = ['a', 'b', 'c', 'd']
        letra = letras[indice]
        self.quiz.marcar_respuesta(letra)
        
        for i, btn in enumerate(self.botones_opciones):
            if i == indice:
                btn.config(bg='lightblue')
            else:
                btn.config(bg='white')
        
        self.lbl_feedback.config(text=f"Seleccionado: {letra.upper()}", fg='blue')
    
    def anterior_pregunta(self):
        if self.quiz.ir_anterior():
            self.cargar_pregunta_actual()
    
    def siguiente_pregunta(self):
        if self.quiz.ir_siguiente():
            self.cargar_pregunta_actual()
        else:
            self.lbl_feedback.config(text="¡Última pregunta! Usa 'Finalizar Quiz'", fg='green')
    
    def iniciar_timer(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        
        if self.tiempo_restante <= 0:
            messagebox.showinfo("Tiempo agotado", "Se acabó el tiempo del quiz.")
            self.finalizar_quiz()
            return
        
        minutos = self.tiempo_restante // 60
        segundos = self.tiempo_restante % 60
        self.lbl_timer.config(text=f"{minutos:02d}:{segundos:02d}")
        
        self.tiempo_restante -= 1
        self.timer_id = self.root.after(1000, self.iniciar_timer)
    
    def finalizar_quiz(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        
        puntaje, total, df_detalle = self.quiz.finalizar()
        self.mostrar_resultados(puntaje, total, df_detalle)
    
    def mostrar_resultados(self, puntaje, total, df_detalle):
        self.limpiar_pantalla()
        
        titulo = tk.Label(self.root, text="Resultados del Quiz", 
                         font=('Arial', 18, 'bold'), bg='white')
        titulo.pack(pady=20)
        
        porcentaje = (puntaje / total) * 100 if total > 0 else 0
        color = 'green' if porcentaje >= 70 else 'orange' if porcentaje >= 50 else 'red'
        
        puntaje_text = f"Puntaje: {puntaje}/{total} ({porcentaje:.1f}%)"
        lbl_puntaje = tk.Label(self.root, text=puntaje_text, 
                              font=('Arial', 16, 'bold'), bg='white', fg=color)
        lbl_puntaje.pack(pady=10)
        
        # Gráficos
        charts_frame = tk.Frame(self.root, bg='white')
        charts_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        fig1 = grafico_barras_por_tema(df_detalle)
        canvas1 = FigureCanvasTkAgg(fig1, charts_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(side='left', fill='both', expand=True, padx=5)
        
        fig2 = grafico_dificultad(df_detalle)
        canvas2 = FigureCanvasTkAgg(fig2, charts_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side='left', fill='both', expand=True, padx=5)
        
        # Detalle con información de dificultad
        detalle_frame = tk.Frame(self.root, bg='white')
        detalle_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        texto_detalle = tk.Text(detalle_frame, font=('Arial', 9), width=80, height=10)
        texto_detalle.pack(fill='both', expand=True)
        
        texto_detalle.insert('end', "Detalle de respuestas:\n\n")
        for i, row in df_detalle.iterrows():
            estado = "✓ CORRECTO" if row['correcta_bool'] else "✗ INCORRECTO"
            nivel = ["Fácil", "Medio", "Difícil"][row['dificultad'] - 1]
            texto_detalle.insert('end', f"Pregunta {i+1} ({nivel}): {estado}\n")
            texto_detalle.insert('end', f"  Tu respuesta: {row['opcion_elegida'].upper() if row['opcion_elegida'] else 'No respondida'}\n")
            texto_detalle.insert('end', f"  Correcta: {row['correcta'].upper()}\n")
            texto_detalle.insert('end', "-" * 50 + "\n")
        
        texto_detalle.config(state='disabled')
        
        # Botones finales
        btn_frame = tk.Frame(self.root, bg='white', pady=20)
        btn_frame.pack(fill='x')
        
        tk.Button(btn_frame, text="Nuevo Quiz", font=('Arial', 12, 'bold'), bg='green', fg='white',
                 command=self.mostrar_inicio).pack(side='left', padx=20)
        
        tk.Button(btn_frame, text="Salir", font=('Arial', 12),
                 command=self.root.quit).pack(side='right', padx=20)

# =============== EJECUCIÓN PRINCIPAL ===============

if __name__ == "__main__":
    try:
        print("Inicializando base de datos...")
        root = tk.Tk()
        app = QuizApp(root)
        print("Aplicación iniciada correctamente")
        root.mainloop()
    except Exception as e:
        print(f"Error crítico: {e}")
        import traceback
        traceback.print_exc()
        input("Presiona Enter para cerrar...")
