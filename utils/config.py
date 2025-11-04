class Config:
    """Configuración centralizada para las pruebas"""
    
    # Navegador
    BROWSER = "chrome"
    HEADLESS = False
    IMPLICIT_WAIT = 10
    EXPLICIT_WAIT = 20
    PAGE_LOAD_TIMEOUT = 60  # ✅ AÑADIR ESTE ATRIBUTO
    
    # Entornos
    BASE_URL_UAT1 = "https://nuxqa4.avtest.ink/"
    BASE_URL_UAT2 = "https://nuxqa5.avtest.ink/"
    
    # Configuración actual
    ENVIRONMENT = "uat1"
    
    @classmethod
    def get_base_url(cls):
        """Obtener URL base según el entorno"""
        if cls.ENVIRONMENT == "uat1":
            return cls.BASE_URL_UAT1
        elif cls.ENVIRONMENT == "uat2":
            return cls.BASE_URL_UAT2
        else:
            return cls.BASE_URL_UAT1
    
    # Usuarios de prueba
    TEST_USERNAME = "21734198706"
    TEST_PASSWORD = "Lifemiles1"
    
    # Rutas
    SCREENSHOT_DIR = "screenshots"
    VIDEO_DIR = "videos"
    DATABASE_PATH = "database/test_results.db"
    
    # Configuración de pruebas
    FAST_EXECUTION = False
    RECORD_VIDEO = False
    TAKE_SCREENSHOTS = True
    
    # Datos de prueba
    TEST_CREDIT_CARD = {
        "number": "4111111111111111",
        "name": "TEST USER",
        "expiry": "12/25",
        "cvv": "123"
    }
    
    @classmethod
    def get_action_delay(cls):
        """Retorna delay basado en configuración de ejecución rápida"""
        return 1 if cls.FAST_EXECUTION else 3