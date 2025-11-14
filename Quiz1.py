"""
Quiz de Economía/Finanzas con ML - Versión Mejorada
"""
import sys
import os
import sqlite3
import random

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

# =============== BASE DE DATOS MEJORADA ===============

class DatabaseManager:
    """Gestor de base de datos SQLite integrada con más preguntas"""
    
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
        """Inserta preguntas de ejemplo con 3 niveles de dificultad - MÁS PREGUNTAS"""
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
            
            ('micro', 'Mercados', 1,
             'En competencia perfecta, las empresas son:',
             'Pocas y grandes', 'Muchas y pequeñas', 'Una sola', 'Dos empresas dominantes',
             'b'),
            
            ('micro', 'Elasticidad', 1,
             'Un bien necesario suele tener demanda:',
             'Elástica', 'Inelástica', 'Unitária', 'Perfectamente elástica',
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
            
            ('micro', 'Producción', 2,
             'El costo marginal es:',
             'Costo de producir una unidad adicional', 'Costo total dividido por unidades', 
             'Costo de los factores fijos', 'Costo de oportunidad',
             'a'),
            
            ('micro', 'Competencia', 2,
             'Un monopolio se caracteriza por:',
             'Muchos vendedores', 'Un solo vendedor', 'Pocos vendedores', 'Productos diferenciados',
             'b'),
            
            ('micro', 'Utilidad', 2,
             'La ley de utilidad marginal decreciente establece que:',
             'La utilidad total siempre aumenta', 'Cada unidad adicional da menos utilidad',
             'La utilidad es constante', 'La utilidad marginal aumenta',
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
             'La curva de indiferencia representa:',
             'Combinaciones que maximizan utilidad', 
             'Combinaciones que dan misma utilidad',
             'Combinaciones asequibles',
             'Combinaciones óptimas',
             'b'),
            
            ('micro', 'Fallos de Mercado', 3,
             'Una externalidad positiva ocurre cuando:',
             'Los costos sociales superan los privados', 
             'Los beneficios sociales superan los privados',
             'No hay intervención gubernamental',
             'El mercado es eficiente',
             'b'),
            
            ('micro', 'Oligopolio', 3,
             'En el modelo de Cournot, las empresas compiten en:',
             'Precio', 'Cantidad', 'Calidad', 'Publicidad',
             'b'),
            
            ('micro', 'Teoría de Juegos', 3,
             'El dilema del prisionero muestra que:',
             'La cooperación siempre es óptima', 
             'El equilibrio individual puede no ser óptimo socialmente',
             'Los juegos siempre tienen ganadores',
             'La competencia es siempre eficiente',
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
            
            ('macro', 'Política Fiscal', 1,
             'Cuando el gobierno gasta más de lo que recauda, hay:',
             'Superávit fiscal', 'Déficit fiscal', 'Equilibrio fiscal', 'Austeridad',
             'b'),
            
            ('macro', 'Dinero', 1,
             'La función principal del dinero es:',
             'Solo medio de cambio', 'Medio de cambio, unidad de cuenta y reserva de valor',
             'Solo reserva de valor', 'Solo unidad de cuenta',
             'b'),
            
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
            
            ('macro', 'Ciclo Económico', 2,
             'La fase de expansión del ciclo económico se caracteriza por:',
             'Alto desempleo', 'Crecimiento del PIB', 'Baja inflación', 'Recesión',
             'b'),
            
            ('macro', 'Bancos Centrales', 2,
             'La principal función de un banco central es:',
             'Realizar préstamos a personas', 'Controlar la política monetaria', 
             'Competir con bancos comerciales', 'Emitir acciones',
             'b'),
            
            ('macro', 'Tipos de Cambio', 2,
             'Una devaluación de la moneda nacional generalmente:',
             'Reduce las exportaciones', 'Aumenta las exportaciones', 
             'No afecta el comercio', 'Solo afecta el turismo',
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
            
            ('macro', 'Paridad de Poder Adquisitivo', 3,
             'La teoría de la PPA sugiere que:',
             'Los tipos de cambio reflejan diferencias de inflación', 
             'Los tipos de cambio son siempre fijos', 
             'La inflación no afecta los tipos de cambio', 
             'Los mercados son siempre eficientes',
             'a'),
            
            ('macro', 'Curva de Phillips', 3,
             'La curva de Phillips a corto plazo muestra la relación entre:',
             'Inflación y desempleo', 'Interés y inversión', 
             'Gasto y producción', 'Ahorro y consumo',
             'a'),
            
            ('macro', 'Teoría Keynesiana', 3,
             'Keynes argumentaba que en recesiones el gobierno debe:',
             'Reducir el gasto público', 'Aumentar el gasto público',
             'Mantener el gasto constante', 'Solo bajar impuestos',
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
            
            ('finanzas', 'Acciones', 1,
             'Las acciones representan:',
             'Deuda de la empresa', 'Propiedad de la empresa', 'Un préstamo', 'Un derivado',
             'b'),
            
            ('finanzas', 'Inflación', 1,
             'La inflación afecta a los ahorradores porque:',
             'Aumenta el poder adquisitivo', 'Reduce el poder adquisitivo', 
             'No afecta el poder adquisitivo', 'Solo afecta a los deudores',
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
            
            ('finanzas', 'Ratios Financieros', 2,
             'El ratio de liquidez corriente mide:',
             'Rentabilidad', 'Endeudamiento', 'Capacidad de pagar deudas corto plazo', 'Eficiencia',
             'c'),
            
            ('finanzas', 'Análisis Técnico', 2,
             'El análisis técnico se basa en:',
             'Estados financieros', 'Patrones de precios históricos', 
             'Fundamentos económicos', 'Noticias del mercado',
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
            
            ('finanzas', 'Valor en Riesgo (VaR)', 3,
             'El Value at Risk (VaR) mide:',
             'La rentabilidad máxima esperada', 'La pérdida máxima esperada en un periodo',
             'La volatilidad histórica', 'El rendimiento promedio',
             'b'),
            
            ('finanzas', 'Black-Scholes', 3,
             'El modelo Black-Scholes se usa para valorar:',
             'Acciones', 'Bonos', 'Opciones financieras', 'Futuros',
             'c'),
            
            # ========== MÁS PREGUNTAS ADICIONALES ==========
            ('micro', 'Externalidades', 2, 'Una externalidad negativa ocurre cuando:', 
             'Los beneficios sociales superan los privados', 'Los costos sociales superan los privados', 
             'No hay diferencia entre costos sociales y privados', 'El gobierno interviene', 'b'),
            
            ('macro', 'Producto Potencial', 2, 'El producto potencial representa:', 
             'La producción actual', 'La producción máxima sostenible', 
             'La producción en recesión', 'La producción con inflación', 'b'),
            
            ('finanzas', 'Hedge', 2, 'Un hedge (cobertura) sirve para:', 
             'Aumentar el riesgo', 'Reducir el riesgo', 'Eliminar totalmente el riesgo', 'Especular', 'b'),
            
            ('micro', 'Bienes Públicos', 3, 'Los bienes públicos puros se caracterizan por:', 
             'Rivalidad y exclusión', 'No rivalidad y no exclusión', 
             'Solo rivalidad', 'Solo no exclusión', 'b'),
            
            ('macro', 'Política Monetaria', 2, 'Cuando un banco central sube las tasas de interés:', 
             'Aumenta la inflación', 'Reduce la inflación', 
             'No afecta la inflación', 'Solo afecta el desempleo', 'b'),
            
            ('finanzas', 'Apalancamiento', 3, 'El apalancamiento financiero:', 
             'Reduce el riesgo', 'Amplifica ganancias y pérdidas', 
             'Solo amplifica ganancias', 'Solo amplifica pérdidas', 'b')
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

# =============== GRÁFICAS MEJORADAS ===============

def grafico_barras_por_tema(df):
    fig, ax = plt.subplots(figsize=(6, 4))
    try:
        if 'tema' in df.columns and 'correcta_bool' in df.columns:
            resultado_por_tema = df.groupby('tema')['correcta_bool'].mean() * 100
            bars = ax.bar(resultado_por_tema.index, resultado_por_tema.values, color='skyblue')
            ax.set_title('Aciertos por Tema')
            ax.set_ylabel('Porcentaje Correcto (%)')
            plt.xticks(rotation=45, ha='right')
            
            # Agregar valores en las barras
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                       f'{height:.1f}%', ha='center', va='bottom', fontsize=9)
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
            ax.plot(preguntas, porcentaje_acumulado, marker='o', linewidth=2, markersize=4, color='green')
            ax.set_title('Evolución del Desempeño')
            ax.set_xlabel('Número de Pregunta')
            ax.set_ylabel('Porcentaje Acumulado (%)')
            ax.grid(True, alpha=0.3)
            
            # Línea de referencia al 50%
            ax.axhline(y=50, color='red', linestyle='--', alpha=0.5, label='50%')
            ax.legend()
    except Exception:
        ax.text(0.5, 0.5, 'Datos insuficientes', ha='center', va='center', transform=ax.transAxes)
    fig.tight_layout()
    return fig

def grafico_dificultad(df):
    """Gráfico para mostrar desempeño por dificultad"""
    fig, ax = plt.subplots(figsize=(6, 4))
    try:
        if 'dificultad' in df.columns and 'correcta_bool' in df.columns:
            resultado_por_dificultad = df.groupby('dificultad')['correcta_bool'].mean() * 100
            dificultades = ['Fácil', 'Medio', 'Difícil']
            valores = [resultado_por_dificultad.get(i, 0) for i in range(1, 4)]
            colors = ['#4CAF50', '#FF9800', '#F44336']  # Verde, Naranja, Rojo
            bars = ax.bar(dificultades, valores, color=colors)
            ax.set_title('Desempeño por Dificultad')
            ax.set_ylabel('Porcentaje Correcto (%)')
            
            # Agregar valores en las barras
            for bar, valor in zip(bars, valores):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                       f'{valor:.1f}%', ha='center', va='bottom', fontweight='bold')
                
            # Línea de referencia al 60%
            ax.axhline(y=60, color='blue', linestyle='--', alpha=0.7, label='Objetivo 60%')
            ax.legend()
    except Exception:
        ax.text(0.5, 0.5, 'Datos insuficientes', ha='center', va='center', transform=ax.transAxes)
    fig.tight_layout()
    return fig

def grafico_desempeno_comparativo(df):
    """NUEVA GRÁFICA: Compara desempeño por categoría y dificultad"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    
    try:
        # Gráfico 1: Desempeño por categoría
        if 'categoria' in df.columns and 'correcta_bool' in df.columns:
            resultado_por_categoria = df.groupby('categoria')['correcta_bool'].mean() * 100
            categorias = [cat.capitalize() for cat in resultado_por_categoria.index]
            bars1 = ax1.bar(categorias, resultado_por_categoria.values, 
                           color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
            ax1.set_title('Desempeño por Categoría')
            ax1.set_ylabel('Porcentaje Correcto (%)')
            
            for bar in bars1:
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                        f'{height:.1f}%', ha='center', va='bottom')
        
        # Gráfico 2: Distribución de preguntas por dificultad
        if 'dificultad' in df.columns:
            distribucion = df['dificultad'].value_counts().sort_index()
            labels = ['Fácil', 'Medio', 'Difícil']
            sizes = [distribucion.get(i, 0) for i in range(1, 4)]
            colors = ['#4CAF50', '#FF9800', '#F44336']
            ax2.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            ax2.set_title('Distribución de Dificultad')
            
    except Exception as e:
        ax1.text(0.5, 0.5, 'Datos insuficientes', ha='center', va='center', transform=ax1.transAxes)
        ax2.text(0.5, 0.5, 'Datos insuficientes', ha='center', va='center', transform=ax2.transAxes)
    
    fig.tight_layout()
    return fig

# =============== INTERFAZ MEJORADA ===============

class ScrollableFrame(tk.Frame):
    """Frame con scroll para mejor visualización de temas"""
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        
        # Crear canvas y scrollbar
        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, background="#ffffff")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz de Economía y Finanzas - Base de Datos Mejorada")
        self.root.geometry("900x700")  # Ventana más grande
        self.root.configure(bg='white')
        
        # Variables
        self.sel_micro = tk.BooleanVar(value=True)
        self.sel_macro = tk.BooleanVar(value=True)
        self.sel_fin = tk.BooleanVar(value=True)
        self.dificultad = tk.StringVar(value="todas")
        self.temas_vars = {}
        
        # Cargar datos desde base de datos
        self.banco = BancoPreguntas()
        
        # Mostrar estadísticas iniciales
        stats = self.banco.mostrar_estadisticas()
        print("Estadísticas de la base de datos:")
        for _, row in stats.iterrows():
            print(f"Dificultad {row['dificultad']}: {row['cantidad']} preguntas")
        
        self.mostrar_inicio()
    
    def limpiar_pantalla(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def mostrar_inicio(self):
        self.limpiar_pantalla()
        
        # Título principal
        titulo = tk.Label(self.root, text="🎓 Quiz de Economía y Finanzas", 
                         font=('Arial', 20, 'bold'), bg='white', fg='navy')
        titulo.pack(pady=30)
        
        subtitulo = tk.Label(self.root, text="Base de Datos con 60+ Preguntas y 3 Niveles de Dificultad", 
                           font=('Arial', 12), bg='white', fg='gray')
        subtitulo.pack(pady=5)
        
        # Estadísticas rápidas
        stats = self.banco.mostrar_estadisticas()
        stats_text = "Preguntas disponibles:\n"
        total_preguntas = 0
        for _, row in stats.iterrows():
            nivel = ["Fácil", "Medio", "Difícil"][row['dificultad'] - 1]
            stats_text += f"• {nivel}: {row['cantidad']} preguntas\n"
            total_preguntas += row['cantidad']
        
        stats_text += f"\nTotal: {total_preguntas} preguntas"
        
        lbl_stats = tk.Label(self.root, text=stats_text, 
                           font=('Arial', 11), bg='white', justify='left')
        lbl_stats.pack(pady=10)
        
        # Botón para comenzar
        btn_comenzar = tk.Button(self.root, text="Comenzar Quiz", 
                               font=('Arial', 14, 'bold'), bg='green', fg='white',
                               command=self.mostrar_configuracion,
                               width=20, height=2)
        btn_comenzar.pack(pady=30)
    
    def mostrar_configuracion(self):
        self.limpiar_pantalla()
        
        titulo = tk.Label(self.root, text="Configurar Quiz", 
                         font=('Arial', 18, 'bold'), bg='white')
        titulo.pack(pady=20)
        
        main_frame = tk.Frame(self.root, bg='white')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Categorías
        cat_frame = tk.LabelFrame(main_frame, text="Categorías", font=('Arial', 11, 'bold'), 
                                 bg='white', padx=10, pady=10)
        cat_frame.pack(side='left', fill='y', padx=10)
        
        tk.Checkbutton(cat_frame, text="Microeconomía", variable=self.sel_micro, 
                      command=self.actualizar_temas, font=('Arial', 10), bg='white').pack(anchor='w', pady=5)
        tk.Checkbutton(cat_frame, text="Macroeconomía", variable=self.sel_macro, 
                      command=self.actualizar_temas, font=('Arial', 10), bg='white').pack(anchor='w', pady=5)
        tk.Checkbutton(cat_frame, text="Finanzas", variable=self.sel_fin, 
                      command=self.actualizar_temas, font=('Arial', 10), bg='white').pack(anchor='w', pady=5)
        
        # Temas con SCROLL
        temas_frame = tk.LabelFrame(main_frame, text="Temas Disponibles", font=('Arial', 11, 'bold'),
                                   bg='white', padx=10, pady=10)
        temas_frame.pack(side='left', fill='both', expand=True, padx=10)
        
        # Frame scrollable para temas
        self.scrollable_temas = ScrollableFrame(temas_frame, height=200)
        self.scrollable_temas.pack(fill='both', expand=True)
        
        # Dificultad
        dificultad_frame = tk.LabelFrame(main_frame, text="Nivel de Dificultad", font=('Arial', 11, 'bold'),
                                        bg='white', padx=10, pady=10)
        dificultad_frame.pack(side='left', fill='y', padx=10)
        
        tk.Radiobutton(dificultad_frame, text="Todas las dificultades", variable=self.dificultad, 
                      value="todas", font=('Arial', 10), bg='white').pack(anchor='w', pady=5)
        tk.Radiobutton(dificultad_frame, text="🎯 Fácil (Nivel 1)", variable=self.dificultad, 
                      value="1", font=('Arial', 10), bg='white', fg='green').pack(anchor='w', pady=5)
        tk.Radiobutton(dificultad_frame, text="🎯 Medio (Nivel 2)", variable=self.dificultad, 
                      value="2", font=('Arial', 10), bg='white', fg='orange').pack(anchor='w', pady=5)
        tk.Radiobutton(dificultad_frame, text="🎯 Difícil (Nivel 3)", variable=self.dificultad, 
                      value="3", font=('Arial', 10), bg='white', fg='red').pack(anchor='w', pady=5)
        
        # Botones
        btn_frame = tk.Frame(self.root, bg='white')
        btn_frame.pack(fill='x', pady=20)
        
        tk.Button(btn_frame, text="Volver al Inicio", font=('Arial', 10),
                 command=self.mostrar_inicio).pack(side='left', padx=20)
        
        tk.Button(btn_frame, text="🎯 Comenzar Quiz", font=('Arial', 12, 'bold'), bg='blue', fg='white',
                 command=self.iniciar_quiz, width=15).pack(side='right', padx=20)
        
        self.actualizar_temas()
    
    def actualizar_temas(self):
        # Limpiar frame de temas
        for widget in self.scrollable_temas.scrollable_frame.winfo_children():
            widget.destroy()
        
        categorias = []
        if self.sel_micro.get(): categorias.append('micro')
        if self.sel_macro.get(): categorias.append('macro')
        if self.sel_fin.get(): categorias.append('finanzas')
        
        if not categorias:
            label = tk.Label(self.scrollable_temas.scrollable_frame, text="Selecciona al menos una categoría", 
                            font=('Arial', 10), bg='white', fg='gray')
            label.pack(pady=10)
            return
        
        temas = self.banco.temas_disponibles(categorias)
        self.temas_vars = {}
        
        # Crear checkboxes para cada tema
        for tema in temas:
            var = tk.BooleanVar(value=True)
            self.temas_vars[tema] = var
            frame_tema = tk.Frame(self.scrollable_temas.scrollable_frame, bg='white')
            frame_tema.pack(fill='x', pady=2)
            
            tk.Checkbutton(frame_tema, text=tema, variable=var,
                          font=('Arial', 9), bg='white', width=30, anchor='w').pack(side='left')
    
    def iniciar_quiz(self):
        categorias = []
        if self.sel_micro.get(): categorias.append('micro')
        if self.sel_macro.get(): categorias.append('macro')
        if self.sel_fin.get(): categorias.append('finanzas')
        
        if not categorias:
            messagebox.showwarning("Error", "Selecciona al menos una categoría")
            return
        
        temas_sel = [tema for tema, var in self.temas_vars.items() if var.get()]
        if not temas_sel:
            messagebox.showwarning("Error", "Selecciona al menos un tema")
            return
        
        # Procesar dificultad seleccionada
        dificultad_seleccionada = None if self.dificultad.get() == "todas" else int(self.dificultad.get())
        
        df_filtrado = self.banco.filtrar(categorias, temas_sel, dificultad_seleccionada)
        if len(df_filtrado) == 0:
            messagebox.showwarning("Error", "No hay preguntas para esta selección")
            return
        
        n_preguntas = min(8, len(df_filtrado))
        df_quiz = self.banco.samplear(df_filtrado, n=n_preguntas)
        
        # Mostrar info sobre las preguntas seleccionadas
        niveles = df_quiz['dificultad'].value_counts().sort_index()
        info_dificultad = "Preguntas seleccionadas:\n"
        for nivel, cantidad in niveles.items():
            nombre_nivel = ["Fácil", "Medio", "Difícil"][nivel - 1]
            info_dificultad += f"• {nombre_nivel}: {cantidad} preguntas\n"
        
        self.quiz = QuizEngine(df_quiz)
        self.tiempo_restante = 600
        self.timer_id = None
        
        messagebox.showinfo("Configuración Lista", info_dificultad)
        self.mostrar_quiz()
    
    def mostrar_quiz(self):
        self.limpiar_pantalla()
        
        # Header con información
        header_frame = tk.Frame(self.root, bg='lightgray', height=60)
        header_frame.pack(fill='x', padx=10, pady=5)
        header_frame.pack_propagate(False)
        
        self.lbl_info = tk.Label(header_frame, text="Pregunta 1/8", 
                                font=('Arial', 12, 'bold'), bg='lightgray')
        self.lbl_info.pack(side='left', padx=10)
        
        self.lbl_dificultad = tk.Label(header_frame, text="Dificultad: -", 
                                      font=('Arial', 11), bg='lightgray')
        self.lbl_dificultad.pack(side='left', padx=20)
        
        self.lbl_timer = tk.Label(header_frame, text="10:00", 
                                 font=('Arial', 14, 'bold'), bg='lightgray', fg='red')
        self.lbl_timer.pack(side='right', padx=10)
        
        # Pregunta
        pregunta_frame = tk.LabelFrame(self.root, text="PREGUNTA", font=('Arial', 12, 'bold'),
                                      bg='white', padx=20, pady=15)
        pregunta_frame.pack(fill='x', padx=15, pady=10)
        
        self.lbl_pregunta = tk.Label(pregunta_frame, text="", wraplength=800,
                                    font=('Arial', 12), bg='white', justify='left')
        self.lbl_pregunta.pack(anchor='w')
        
        # Opciones - MEJOR VISIBILIDAD
        opciones_frame = tk.LabelFrame(self.root, text="SELECCIONA TU RESPUESTA", 
                                      font=('Arial', 12, 'bold'), bg='white', padx=20, pady=15)
        opciones_frame.pack(fill='both', expand=True, padx=15, pady=10)
        
        self.botones_opciones = []
        opciones_colors = ['#E8F5E8', '#E8F4FD', '#FFF4E8', '#FDE8E8']  # Colores suaves diferentes
        
        for i in range(4):
            btn_frame = tk.Frame(opciones_frame, bg='white')
            btn_frame.pack(fill='x', pady=8)
            
            btn = tk.Button(btn_frame, text="", font=('Arial', 11),
                           command=lambda idx=i: self.seleccionar_opcion(idx),
                           width=80, height=2, bg=opciones_colors[i], 
                           relief='raised', bd=2, anchor='w', justify='left')
            btn.pack(fill='x', padx=5)
            self.botones_opciones.append(btn)
        
        # Feedback
        self.lbl_feedback = tk.Label(self.root, text="", font=('Arial', 12, 'bold'), bg='white')
        self.lbl_feedback.pack(pady=10)
        
        # Navegación
        nav_frame = tk.Frame(self.root, bg='white', pady=20)
        nav_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Button(nav_frame, text="← Anterior", font=('Arial', 11),
                 command=self.anterior_pregunta, width=12).pack(side='left', padx=5)
        
        tk.Button(nav_frame, text="Siguiente →", font=('Arial', 11),
                 command=self.siguiente_pregunta, width=12).pack(side='left', padx=5)
        
        tk.Button(nav_frame, text="🏁 Finalizar Quiz", font=('Arial', 11, 'bold'), bg='red', fg='white',
                 command=self.finalizar_quiz, width=15).pack(side='right', padx=5)
        
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
            self.botones_opciones[i].config(text=texto)
        
        respuesta_actual = self.quiz.elegidas[self.quiz.idx]
        if respuesta_actual:
            letras = ['a', 'b', 'c', 'd']
            if respuesta_actual in letras:
                idx = letras.index(respuesta_actual)
                self.botones_opciones[idx].config(bg='lightblue')
            self.lbl_feedback.config(text=f"Seleccionado: {respuesta_actual.upper()}", fg='blue')
        else:
            self.lbl_feedback.config(text="Selecciona una opción", fg='gray')
    
    def seleccionar_opcion(self, indice):
        letras = ['a', 'b', 'c', 'd']
        letra = letras[indice]
        self.quiz.marcar_respuesta(letra)
        
        # Colores originales
        opciones_colors = ['#E8F5E8', '#E8F4FD', '#FFF4E8', '#FDE8E8']
        
        for i, btn in enumerate(self.botones_opciones):
            if i == indice:
                btn.config(bg='lightblue')  # Seleccionado
            else:
                btn.config(bg=opciones_colors[i])  # Color original
        
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
        self.lbl_timer.config(text=f"Tiempo: {minutos:02d}:{segundos:02d}")
        
        self.tiempo_restante -= 1
        self.timer_id = self.root.after(1000, self.iniciar_timer)
    
    def finalizar_quiz(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        
        puntaje, total, df_detalle = self.quiz.finalizar()
        self.mostrar_resultados(puntaje, total, df_detalle)
    
    def mostrar_resultados(self, puntaje, total, df_detalle):
        self.limpiar_pantalla()
        
        # Frame principal con scroll para resultados
        main_frame = tk.Frame(self.root, bg='white')
        main_frame.pack(fill='both', expand=True)
        
        canvas = tk.Canvas(main_frame, bg='white')
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Título de resultados
        titulo = tk.Label(scrollable_frame, text="📊 Resultados del Quiz", 
                         font=('Arial', 20, 'bold'), bg='white', fg='navy')
        titulo.pack(pady=20)
        
        # Puntaje principal
        porcentaje = (puntaje / total) * 100 if total > 0 else 0
        color = 'green' if porcentaje >= 70 else 'orange' if porcentaje >= 50 else 'red'
        
        puntaje_text = f"Puntaje Final: {puntaje}/{total} ({porcentaje:.1f}%)"
        lbl_puntaje = tk.Label(scrollable_frame, text=puntaje_text, 
                              font=('Arial', 18, 'bold'), bg='white', fg=color)
        lbl_puntaje.pack(pady=10)
        
        # Mensaje según desempeño
        if porcentaje >= 80:
            mensaje = "¡Excelente! Dominas los conceptos económicos y financieros."
        elif porcentaje >= 60:
            mensaje = "¡Buen trabajo! Tienes un buen conocimiento de los temas."
        elif porcentaje >= 40:
            mensaje = "¡No está mal! Sigue practicando para mejorar."
        else:
            mensaje = "¡Sigue estudiando! Revisa los conceptos básicos."
        
        lbl_mensaje = tk.Label(scrollable_frame, text=mensaje, 
                              font=('Arial', 12), bg='white', fg='gray')
        lbl_mensaje.pack(pady=5)
        
        # GRÁFICAS MEJORADAS
        charts_frame = tk.Frame(scrollable_frame, bg='white')
        charts_frame.pack(fill='x', pady=20, padx=10)
        
        # Gráfico comparativo (nuevo)
        fig1 = grafico_desempeno_comparativo(df_detalle)
        canvas1 = FigureCanvasTkAgg(fig1, charts_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill='x', pady=10)
        
        # Más gráficos
        charts_subframe = tk.Frame(charts_frame, bg='white')
        charts_subframe.pack(fill='x', pady=10)
        
        fig2 = grafico_dificultad(df_detalle)
        canvas2 = FigureCanvasTkAgg(fig2, charts_subframe)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side='left', fill='both', expand=True, padx=5)
        
        fig3 = grafico_linea_evolucion(df_detalle)
        canvas3 = FigureCanvasTkAgg(fig3, charts_subframe)
        canvas3.draw()
        canvas3.get_tk_widget().pack(side='left', fill='both', expand=True, padx=5)
        
        # Detalle de respuestas
        detalle_frame = tk.LabelFrame(scrollable_frame, text="📋 Detalle de Respuestas", 
                                     font=('Arial', 14, 'bold'), bg='white', padx=15, pady=10)
        detalle_frame.pack(fill='x', pady=20, padx=10)
        
        texto_detalle = tk.Text(detalle_frame, font=('Arial', 10), width=85, height=12,
                               wrap=tk.WORD, bg='#F9F9F9')
        scrolltext = tk.Scrollbar(detalle_frame, command=texto_detalle.yview)
        texto_detalle.configure(yscrollcommand=scrolltext.set)
        
        texto_detalle.pack(side='left', fill='both', expand=True)
        scrolltext.pack(side='right', fill='y')
        
        # Agregar datos al texto
        texto_detalle.insert('end', "RESUMEN DE RESPUESTAS:\n\n")
        
        for i, row in df_detalle.iterrows():
            estado = "✅ CORRECTO" if row['correcta_bool'] else "❌ INCORRECTO"
            nivel = ["🎯 Fácil", "🎯 Medio", "🎯 Difícil"][row['dificultad'] - 1]
            categoria = row['categoria'].capitalize()
            
            texto_detalle.insert('end', f"Pregunta {i+1} | {categoria} | {nivel}\n")
            texto_detalle.insert('end', f"   Estado: {estado}\n")
            texto_detalle.insert('end', f"   Tu respuesta: {row['opcion_elegida'].upper() if row['opcion_elegida'] else 'No respondida'}\n")
            texto_detalle.insert('end', f"   Correcta: {row['correcta'].upper()}\n")
            
            # Resaltar preguntas incorrectas
            if not row['correcta_bool']:
                texto_detalle.insert('end', f"   ⚠️  Necesitas repasar este tema\n")
            
            texto_detalle.insert('end', "-" * 60 + "\n\n")
        
        texto_detalle.config(state='disabled')
        
        # Botones finales
        btn_frame = tk.Frame(scrollable_frame, bg='white', pady=20)
        btn_frame.pack(fill='x')
        
        tk.Button(btn_frame, text="🔄 Nuevo Quiz", font=('Arial', 12, 'bold'), bg='green', fg='white',
                 command=self.mostrar_inicio, width=15).pack(side='left', padx=20)
        
        tk.Button(btn_frame, text="📊 Ver Estadísticas", font=('Arial', 12), bg='blue', fg='white',
                 command=self.mostrar_estadisticas_completas, width=15).pack(side='left', padx=10)
        
        tk.Button(btn_frame, text="🚪 Salir", font=('Arial', 12),
                 command=self.root.quit, width=12).pack(side='right', padx=20)
        
        # Configurar scroll
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def mostrar_estadisticas_completas(self):
        """Muestra estadísticas completas de la base de datos"""
        stats = self.banco.mostrar_estadisticas()
        
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Estadísticas Completas")
        stats_window.geometry("400x300")
        
        tk.Label(stats_window, text="📈 Estadísticas de la Base de Datos", 
                font=('Arial', 16, 'bold')).pack(pady=20)
        
        total = 0
        for _, row in stats.iterrows():
            nivel = ["Fácil", "Medio", "Difícil"][row['dificultad'] - 1]
            tk.Label(stats_window, text=f"{nivel}: {row['cantidad']} preguntas",
                    font=('Arial', 12)).pack(pady=5)
            total += row['cantidad']
        
        tk.Label(stats_window, text=f"\nTotal: {total} preguntas",
                font=('Arial', 14, 'bold')).pack(pady=10)
        
        tk.Button(stats_window, text="Cerrar", command=stats_window.destroy).pack(pady=10)

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
