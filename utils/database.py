import sqlite3
import time
import os
from datetime import datetime


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
                    screenshot_path TEXT
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
            
            self.connection.commit()
            print("✅ Base de datos inicializada correctamente")
            
        except sqlite3.Error as e:
            print(f"❌ Error inicializando base de datos: {e}")
    
    def insert_result(self, test_name, status, browser, url=None, execution_time=0, 
                     error_message=None, environment=None, screenshot_path=None):
        """Insertar resultado de test en la base de datos"""
        try:
            cursor = self.connection.cursor()
            
            cursor.execute('''
                INSERT INTO test_results 
                (test_name, status, browser, url, execution_time, error_message, environment, screenshot_path)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (test_name, status, browser, url, execution_time, error_message, environment, screenshot_path))
            
            test_id = cursor.lastrowid
            self.connection.commit()
            
            print(f"✅ Resultado guardado en BD: {test_name} - {status}")
            return test_id
            
        except sqlite3.Error as e:
            print(f"❌ Error insertando resultado: {e}")
            return None
    
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
            return True
            
        except sqlite3.Error as e:
            print(f"❌ Error agregando evidencia: {e}")
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