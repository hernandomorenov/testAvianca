import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuración centralizada para las pruebas"""
    
    KEEP_BROWSER_OPEN = False

    # ===== CONFIGURACIÓN DEL ENTORNO =====
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'uat4')

    # ===== URLs BASE DINÁMICAS =====
    # Se configuran según el entorno
    @classmethod
    def _get_base_domain(cls):
        """Obtener dominio base según entorno"""
        domains = {
            'uat1': 'https://nuxqa4.avtest.ink/',
            'uat2': 'https://nuxqa5.avtest.ink/',
            'uat3': 'https://nuxqa3.avtest.ink/'
        }
        return domains.get(cls.ENVIRONMENT, 'https://nuxqa4.avtest.ink/')

    @classmethod
    def _build_urls(cls):
        """Construir URLs dinámicamente según entorno"""
        base = cls._get_base_domain()
        cls.BASE_URL = base
        cls.BASE_URL_ES = f"{base}es/"
        cls.BASE_URL_EN = f"{base}en/"
        cls.BASE_URL_FR = f"{base}fr/"
        cls.BASE_URL_PT = f"{base}pt/"
        
        # URLs específicas por entorno
        cls.BASE_URL_UAT1 = "https://nuxqa4.avtest.ink/"
        cls.BASE_URL_UAT2 = "https://nuxqa5.avtest.ink/"
        cls.BASE_URL_UAT3 = "https://nuxqa3.avtest.ink/"

    # ===== CONFIGURACIÓN DEL NAVEGADOR =====
    BROWSER = os.getenv('BROWSER', 'chrome')
    HEADLESS = os.getenv('HEADLESS', 'false').lower() == 'true'
    WINDOW_WIDTH = int(os.getenv('WINDOW_WIDTH', '1920'))
    WINDOW_HEIGHT = int(os.getenv('WINDOW_HEIGHT', '1080'))
    
    # ===== TIMEOUTS =====
    IMPLICIT_WAIT = int(os.getenv('IMPLICIT_WAIT', '5'))
    EXPLICIT_WAIT = int(os.getenv('EXPLICIT_WAIT', '10'))
    PAGE_LOAD_TIMEOUT = int(os.getenv('PAGE_LOAD_TIMEOUT', '15'))
    
    # ===== DATOS DE PRUEBA =====
    TEST_ORIGIN = os.getenv('TEST_ORIGIN', 'BOG')
    TEST_DESTINATION = os.getenv('TEST_DESTINATION', 'MDE')
    
    # Usuarios de prueba
    TEST_USERNAME = os.getenv('TEST_USERNAME', '21734198706')
    TEST_PASSWORD = os.getenv('TEST_PASSWORD', 'Lifemiles1')
    
    LANGUAGE = os.getenv('LANGUAGE', 'french')
    POS = os.getenv('POS', 'france')
    
    PASSENGERS = {
        "adults": int(os.getenv('PASSENGERS_ADULTS', '3')),
        "youth": int(os.getenv('PASSENGERS_YOUTH', '3')),
        "children": int(os.getenv('PASSENGERS_CHILDREN', '3')),
        "infants": int(os.getenv('PASSENGERS_INFANTS', '3'))
    }
    
    # Datos de tarjeta de prueba
    TEST_CREDIT_CARD = {
        "number": os.getenv('CREDIT_CARD_NUMBER', '4111111111111111'),
        "name": os.getenv('CREDIT_CARD_NAME', 'TEST USER'),
        "expiry": os.getenv('CREDIT_CARD_EXPIRY', '12/25'),
        "cvv": os.getenv('CREDIT_CARD_CVV', '123')
    }
    
    # ===== RUTAS Y DIRECTORIOS ORGANIZADOS =====
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # Directorios principales
    TEST_RESULTS_DIR = os.path.join(BASE_DIR, "test_results")
    SCREENSHOT_DIR = os.path.join(TEST_RESULTS_DIR, "screenshots")
    VIDEO_DIR = os.path.join(TEST_RESULTS_DIR, "videos")
    ALLURE_RESULTS_DIR = os.path.join(BASE_DIR, "allure-results")
    LOGS_DIR = os.path.join(BASE_DIR, "logs")
    DATABASE_DIR = os.path.join(BASE_DIR, "database")
    
    DATABASE_PATH = os.getenv('DATABASE_PATH', os.path.join(DATABASE_DIR, 'test_results.db'))
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///test_results.db')
    
    # ===== CONFIGURACIÓN DE PRUEBAS =====
    FAST_EXECUTION = os.getenv('FAST_EXECUTION', 'false').lower() == 'true'
    RECORD_VIDEO = os.getenv('RECORD_VIDEO', 'false').lower() == 'true'
    TAKE_SCREENSHOTS = os.getenv('TAKE_SCREENSHOTS', 'true').lower() == 'true'
    
    # ===== MÉTODOS PARA RUTAS ORGANIZADAS =====
    @classmethod
    def get_screenshot_path(cls, filename):
        """Obtiene la ruta completa para capturas con timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]  # Incluye milisegundos
        name, ext = os.path.splitext(filename)
        if not ext:
            ext = ".png"
        new_filename = f"{name}_{timestamp}{ext}"
        return os.path.join(cls.SCREENSHOT_DIR, new_filename)
    
    @classmethod
    def get_video_path(cls, test_name):
        """Obtiene la ruta completa para videos con timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_test_name = "".join(c for c in test_name if c.isalnum() or c in ('-', '_'))
        return os.path.join(cls.VIDEO_DIR, f"{safe_test_name}_{timestamp}.mp4")
    
    @classmethod
    def get_log_path(cls):
        """Obtiene la ruta para archivos de log"""
        timestamp = datetime.now().strftime("%Y%m%d")
        return os.path.join(cls.LOGS_DIR, f"test_execution_{timestamp}.log")

    @classmethod
    def get_base_url(cls):
        """Obtener URL base según el entorno"""
        if cls.ENVIRONMENT == "uat1":
            return cls.BASE_URL_UAT1
        elif cls.ENVIRONMENT == "uat2":
            return cls.BASE_URL_UAT2
        else:
            return cls.BASE_URL_UAT3
    
    @classmethod
    def get_action_delay(cls):
        """Retorna delay basado en configuración de ejecución rápida"""
        return 1 if cls.FAST_EXECUTION else 3
    
    @classmethod
    def get_base_url_by_language(cls, language='es'):
        """Obtener URL base por idioma"""
        urls = {
            'es': cls.BASE_URL_ES,
            'en': cls.BASE_URL_EN,
            'fr': cls.BASE_URL_FR,
            'pt': cls.BASE_URL_PT
        }
        return urls.get(language, cls.BASE_URL)
    
    @classmethod
    def validate_config(cls):
        """Validar que la configuración sea correcta"""
        required_envs = ['ENVIRONMENT']
        for env in required_envs:
            if not getattr(cls, env):
                raise ValueError(f"Configuración requerida faltante: {env}")
        
        valid_environments = ['uat1', 'uat2', 'uat3']
        if cls.ENVIRONMENT not in valid_environments:
            raise ValueError(f"Entorno no válido: {cls.ENVIRONMENT}. Debe ser uno de: {valid_environments}")
        
        valid_browsers = ['chrome', 'firefox', 'edge']
        if cls.BROWSER not in valid_browsers:
            raise ValueError(f"Navegador no válido: {cls.BROWSER}. Debe ser uno de: {valid_browsers}")
        
        # Validar que los números de pasajeros sean válidos
        if cls.PASSENGERS["adults"] < 1:
            raise ValueError("Debe haber al menos 1 adulto")
        
        if cls.PASSENGERS["infants"] > cls.PASSENGERS["adults"]:
            raise ValueError("No puede haber más infantes que adultos")
    
    @classmethod
    def setup_directories(cls):
        """Crear directorios necesarios si no existen"""
        directories = [
            cls.TEST_RESULTS_DIR,
            cls.SCREENSHOT_DIR, 
            cls.VIDEO_DIR, 
            cls.ALLURE_RESULTS_DIR,
            cls.LOGS_DIR,
            cls.DATABASE_DIR
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            # Evitar emojis para compatibilidad con Windows cmd
            try:
                print(f"[OK] Directorio asegurado: {directory}")
            except:
                pass  # Silencioso si hay problemas de encoding
    
    @classmethod
    def print_config(cls):
        """Imprimir configuración actual"""
        # Reconstruir URLs según entorno actual
        cls._build_urls()

        print("\n🔧 CONFIGURACIÓN ACTUAL:")
        print(f"   🌍 ENVIRONMENT: {cls.ENVIRONMENT}")
        print(f"   🌐 BASE_URL: {cls.BASE_URL}")
        print(f"   🌐 BASE_URL_ES: {cls.BASE_URL_ES}")
        print(f"   🌐 BASE_URL_EN: {cls.BASE_URL_EN}")
        print(f"   🌐 BASE_URL_FR: {cls.BASE_URL_FR}")
        print(f"   🌐 BASE_URL_PT: {cls.BASE_URL_PT}")
        print(f"   🖥️  BROWSER: {cls.BROWSER}")
        print(f"   👻 HEADLESS: {cls.HEADLESS}")
        print(f"   📏 WINDOW: {cls.WINDOW_WIDTH}x{cls.WINDOW_HEIGHT}")
        print(f"   ⏱️  TIMEOUTS: implicit={cls.IMPLICIT_WAIT}s, explicit={cls.EXPLICIT_WAIT}s")
        print(f"   ✈️  TEST ROUTE: {cls.TEST_ORIGIN} -> {cls.TEST_DESTINATION}")
        print(f"   🔐 USERNAME: {cls.TEST_USERNAME}")
        print(f"   🌍 LANGUAGE: {cls.LANGUAGE}")
        print(f"   🇫🇷 POS: {cls.POS}")
        print(f"   👥 PASSENGERS: {cls.PASSENGERS}")
        print(f"   💳 CARD: {cls.TEST_CREDIT_CARD['number'][:6]}...{cls.TEST_CREDIT_CARD['number'][-4:]}")
        print(f"   🚀 FAST_EXECUTION: {cls.FAST_EXECUTION}")
        print(f"   📸 TAKE_SCREENSHOTS: {cls.TAKE_SCREENSHOTS}")
        print(f"   🎥 RECORD_VIDEO: {cls.RECORD_VIDEO}")
        print(f"   📁 DIRECTORIOS:")
        print(f"      - Screenshots: {cls.SCREENSHOT_DIR}")
        print(f"      - Videos: {cls.VIDEO_DIR}")
        print(f"      - Logs: {cls.LOGS_DIR}")
        print(f"      - Allure: {cls.ALLURE_RESULTS_DIR}")
        print("="*50)
        print()

    @classmethod
    def initialize(cls):
        """Inicializar configuración - método principal a llamar al inicio"""
        try:
            cls._build_urls()
            cls.setup_directories()
            # No validar automáticamente - se hará en conftest.py
            # cls.validate_config()
            # cls.print_config()
        except Exception as e:
            # Evitar emojis para compatibilidad con Windows cmd
            try:
                print(f"[WARNING] Advertencia inicializando configuracion: {e}")
            except:
                pass  # Silencioso en caso de error de encoding


# Inicializar configuración básica automáticamente al importar
try:
    Config.initialize()
except Exception as e:
    try:
        print(f"[WARNING] Error en inicializacion automatica de Config: {e}")
    except:
        pass  # Silencioso en caso de error de encoding

# Constantes adicionales
TEST_ORIGIN = "Bogotá - BOG"
TEST_DESTINATION = "Medellín - MDE" 
BASE_URL_EN = "https://nuxqa4.avtest.ink/en/"