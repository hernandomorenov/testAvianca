import sqlite3
import time
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class Database:
    """Manejo de base de datos SQLite para resultados de pruebas"""

    def __init__(self, db_path=None):
        self.db_path = db_path or "database/test_results.db"
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.connection = None
        self._initialize_database()
    
    def _initialize_database(self):
        """Inicializar la base de datos y crear tablas si no existen"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            cursor = self.connection.cursor()

            # Tabla de resultados de tests
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS test_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    test_name TEXT NOT NULL,
                    status TEXT NOT NULL,
                    browser TEXT NOT NULL,
                    url TEXT,
                    execution_time REAL,
                    error_message TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    environment TEXT,
                    screenshot_path TEXT,
                    video_path TEXT
                )
            ''')

            # Tabla de evidencias
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS test_evidences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    test_id INTEGER,
                    evidence_type TEXT,
                    evidence_path TEXT,
                    description TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (test_id) REFERENCES test_results (id)
                )
            ''')

            # Tabla de métricas de rendimiento
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS test_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    test_id INTEGER,
                    metric_name TEXT,
                    metric_value REAL,
                    unit TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (test_id) REFERENCES test_results (id)
                )
            ''')

            self.connection.commit()
            logger.info("Base de datos inicializada correctamente")
            print("✅ Base de datos inicializada correctamente")

        except sqlite3.Error as e:
            logger.error(f"Error inicializando base de datos: {e}")
            print(f"❌ Error inicializando base de datos: {e}")
    
    # En utils/database.py - actualiza el método insert_result

    def insert_result(self, test_name, status, browser, url, execution_time, error_message=None, additional_data=None):
        """Insertar resultado de test en la base de datos - VERSIÓN CORREGIDA"""
        try:
            # Primero verificar las columnas de la tabla
            cursor = self.conn.cursor()
            cursor.execute("PRAGMA table_info(test_results)")
            columns = [column[1] for column in cursor.fetchall()]
            
            # Construir la consulta según las columnas disponibles
            if 'video_path' in columns:
                query = """
                INSERT INTO test_results 
                (test_name, status, browser, url, execution_time, error_message, additional_data, video_path, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
                """
                params = (test_name, status, browser, url, execution_time, error_message, additional_data, None)
            else:
                query = """
                INSERT INTO test_results 
                (test_name, status, browser, url, execution_time, error_message, additional_data, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))
                """
                params = (test_name, status, browser, url, execution_time, error_message, additional_data)
            
            cursor.execute(query, params)
            self.conn.commit()
            print(f"✅ Resultado insertado en BD: {test_name} - {status}")
            return True
            
        except Exception as e:
            print(f"❌ Error insertando resultado: {e}")
            # Intentar con consulta básica sin video_path
            try:
                cursor = self.conn.cursor()
                query = """
                INSERT INTO test_results 
                (test_name, status, browser, url, execution_time, error_message, additional_data, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))
                """
                params = (test_name, status, browser, url, execution_time, error_message, additional_data)
                cursor.execute(query, params)
                self.conn.commit()
                print(f"✅ Resultado insertado (fallback): {test_name}")
                return True
            except Exception as e2:
                print(f"❌ Error incluso con fallback: {e2}")
                return False
    
    def add_evidence(self, test_id, evidence_type, evidence_path, description=None):
        """Agregar evidencia (screenshot, video) a un test"""
        try:
            cursor = self.connection.cursor()

            cursor.execute('''
                INSERT INTO test_evidences
                (test_id, evidence_type, evidence_path, description)
                VALUES (?, ?, ?, ?)
            ''', (test_id, evidence_type, evidence_path, description))

            self.connection.commit()
            logger.debug(f"Evidencia agregada: {evidence_type} - {evidence_path}")
            return True

        except sqlite3.Error as e:
            logger.error(f"Error agregando evidencia: {e}")
            print(f"❌ Error agregando evidencia: {e}")
            return False

    def add_metric(self, test_id, metric_name, metric_value, unit='ms'):
        """Agregar métrica de rendimiento a un test"""
        try:
            cursor = self.connection.cursor()

            cursor.execute('''
                INSERT INTO test_metrics
                (test_id, metric_name, metric_value, unit)
                VALUES (?, ?, ?, ?)
            ''', (test_id, metric_name, metric_value, unit))

            self.connection.commit()
            logger.debug(f"Métrica agregada: {metric_name} = {metric_value}{unit}")
            return True

        except sqlite3.Error as e:
            logger.error(f"Error agregando métrica: {e}")
            return False
    
    def get_test_results(self, limit=100):
        """Obtener resultados de tests"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                SELECT * FROM test_results 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (limit,))
            
            return cursor.fetchall()
            
        except sqlite3.Error as e:
            print(f"❌ Error obteniendo resultados: {e}")
            return []
    
    def close_connection(self):
        """Cerrar conexión a la base de datos"""
        if self.connection:
            self.connection.close()