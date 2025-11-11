import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuración centralizada para las pruebas"""

    # ===== CONFIGURACIÓN DEL ENTORNO =====
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'uat3')

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
        return domains.get(cls.ENVIRONMENT, 'https://nuxqa3.avtest.ink/')

    @classmethod
    def _build_urls(cls):
        """Construir URLs dinámicamente según entorno"""
        base = cls._get_base_domain()
        cls.BASE_URL = base
        cls.BASE_URL_ES = f"{base}es/"
        cls.BASE_URL_EN = f"{base}en/"
        cls.BASE_URL_FR = f"{base}fr/"
        cls.BASE_URL_PT = f"{base}pt/"

    # Inicializar URLs con valores por defecto
    #BASE_URL = os.getenv('BASE_URL', 'https://nuxqa4.avtest.ink/')
    BASE_URL = "https://nuxqa3.avtest.ink/"  #metodo empleado para el caso 3
    BASE_URL_UAT1 = "https://nuxqa4.avtest.ink/"
    BASE_URL_UAT2 = "https://nuxqa5.avtest.ink/"
    BASE_URL_UAT3 = "https://nuxqa3.avtest.ink/"
    BASE_URL_EN = os.getenv('BASE_URL_EN', 'https://nuxqa3.avtest.ink/en/')
    BASE_URL_ES = os.getenv('BASE_URL_ES', 'https://nuxqa3.avtest.ink/es/')
    BASE_URL_FR = os.getenv('BASE_URL_FR', 'https://nuxqa3.avtest.ink/fr/')
    BASE_URL_PT = os.getenv('BASE_URL_PT', 'https://nuxqa3.avtest.ink/pt/')
    
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
    TEST_DESTINATION = os.getenv('TEST_DESTINATION', 'ORY')
    
    # Usuarios de prueba
    TEST_USERNAME = "21734198706"
    TEST_PASSWORD = "Lifemiles1"
    
    LANGUAGE = "french"
    POS = "france"
    PASSENGERS = {
        "adults": 3,
        "youth": 3, 
        "children": 3,
        "infants": 3
    }
    
    # Datos de tarjeta de prueba
    TEST_CREDIT_CARD = {
        "number": "4111111111111111",
        "name": "TEST USER",
        "expiry": "12/25",
        "cvv": "123"
    }
    
    # ===== RUTAS Y DIRECTORIOS =====
    SCREENSHOT_DIR = "screenshots"
    VIDEO_DIR = "videos"
    DATABASE_PATH = "database/test_results.db"
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///test_results.db')
    
    # ===== CONFIGURACIÓN DE PRUEBAS =====
    FAST_EXECUTION = False
    RECORD_VIDEO = False
    TAKE_SCREENSHOTS = True
    
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
        print(f"   🚀 FAST_EXECUTION: {cls.FAST_EXECUTION}")
        print(f"   📸 TAKE_SCREENSHOTS: {cls.TAKE_SCREENSHOTS}")
        print(f"   🎥 RECORD_VIDEO: {cls.RECORD_VIDEO}")
        print()