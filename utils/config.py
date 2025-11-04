import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuración centralizada para las pruebas"""
    
    # ===== URLs BASE =====
    BASE_URL = os.getenv('BASE_URL', 'https://nuxqa4.avtest.ink/')
    BASE_URL_UAT1 = "https://nuxqa4.avtest.ink/"
    BASE_URL_UAT2 = "https://nuxqa5.avtest.ink/"
    BASE_URL_EN = os.getenv('BASE_URL_EN', 'https://nuxqa4.avtest.ink/en/')
    BASE_URL_ES = os.getenv('BASE_URL_ES', 'https://nuxqa4.avtest.ink/es/')
    BASE_URL_FR = os.getenv('BASE_URL_FR', 'https://nuxqa4.avtest.ink/fr/')
    BASE_URL_PT = os.getenv('BASE_URL_PT', 'https://nuxqa4.avtest.ink/pt/')
    
    # ===== CONFIGURACIÓN DEL ENTORNO =====
    ENVIRONMENT = "uat1"
    
    # ===== CONFIGURACIÓN DEL NAVEGADOR =====
    BROWSER = os.getenv('BROWSER', 'chrome')
    HEADLESS = os.getenv('HEADLESS', 'false').lower() == 'true'
    WINDOW_WIDTH = int(os.getenv('WINDOW_WIDTH', '1920'))
    WINDOW_HEIGHT = int(os.getenv('WINDOW_HEIGHT', '1080'))
    
    # ===== TIMEOUTS =====
    IMPLICIT_WAIT = int(os.getenv('IMPLICIT_WAIT', '10'))
    EXPLICIT_WAIT = int(os.getenv('EXPLICIT_WAIT', '30'))
    PAGE_LOAD_TIMEOUT = int(os.getenv('PAGE_LOAD_TIMEOUT', '60'))
    
    # ===== DATOS DE PRUEBA =====
    TEST_ORIGIN = os.getenv('TEST_ORIGIN', 'BOG')
    TEST_DESTINATION = os.getenv('TEST_DESTINATION', 'MDE')
    
    # Usuarios de prueba
    TEST_USERNAME = "21734198706"
    TEST_PASSWORD = "Lifemiles1"
    
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
            return cls.BASE_URL_UAT1
    
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
        print("\n🔧 CONFIGURACIÓN ACTUAL:")
        print(f"   🌐 BASE_URL: {cls.BASE_URL}")
        print(f"   🌐 BASE_URL_ES: {cls.BASE_URL_ES}")
        print(f"   🌐 BASE_URL_EN: {cls.BASE_URL_EN}")
        print(f"   🖥️  BROWSER: {cls.BROWSER}")
        print(f"   👻 HEADLESS: {cls.HEADLESS}")
        print(f"   📏 WINDOW: {cls.WINDOW_WIDTH}x{cls.WINDOW_HEIGHT}")
        print(f"   ⏱️  TIMEouts: implicit={cls.IMPLICIT_WAIT}s, explicit={cls.EXPLICIT_WAIT}s")
        print(f"   ✈️  TEST ROUTE: {cls.TEST_ORIGIN} -> {cls.TEST_DESTINATION}")
        print(f"   🚀 FAST_EXECUTION: {cls.FAST_EXECUTION}")
        print(f"   📸 TAKE_SCREENSHOTS: {cls.TAKE_SCREENSHOTS}")
        print()