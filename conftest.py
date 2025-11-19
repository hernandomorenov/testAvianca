# -*- coding: utf-8 -*-
import pytest
import allure
import sqlite3
import time
import os
import sys
import logging
import platform
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions

# Importaciones de utils
try:
    from utils.config import Config
    from utils.database import Database
    from utils.video_recorder import VideoRecorder
    from utils.logger import setup_logger
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
    print("⚠️  Asegúrate de que los archivos en la carpeta 'utils' existan")
    
    # Configuración básica como fallback
    class Config:
        BROWSER = "chrome"
        HEADLESS = False
        ENVIRONMENT = "uat1"
        KEEP_BROWSER_OPEN = False
        RECORD_VIDEO = False
        IMPLICIT_WAIT = 10
        PAGE_LOAD_TIMEOUT = 30
        
        @classmethod
        def print_config(cls):
            print(f"🛠️  CONFIGURACIÓN:")
            print(f"   Navegador: {cls.BROWSER}")
            print(f"   Headless: {cls.HEADLESS}")
            print(f"   Environment: {cls.ENVIRONMENT}")
            print(f"   Keep Browser Open: {cls.KEEP_BROWSER_OPEN}")
            print(f"   Record Video: {cls.RECORD_VIDEO}")
            print(f"   Implicit Wait: {cls.IMPLICIT_WAIT}s")
            print(f"   Page Load Timeout: {cls.PAGE_LOAD_TIMEOUT}s")

    class Database:
        def __init__(self): 
            print("✅ Base de datos inicializada correctamente")
        def close_connection(self): pass
        def insert_result(self, **kwargs): pass
        def get_session_summary(self): 
            return {'passed': 0, 'failed': 0, 'skipped': 0, 'avg_time': 0}
    
    class VideoRecorder:
        def start_recording(self, name): pass
        def stop_recording(self): return None
    
    def setup_logger():
        return logging.getLogger(__name__)

# Configurar encoding UTF-8 para Windows
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Configurar logger al inicio
logger = setup_logger()


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser to run tests: chrome, firefox, edge")
    parser.addoption("--headless", action="store_true", help="Run in headless mode")
    parser.addoption("--env", action="store", default="uat1", help="Environment: uat1, uat2")
    parser.addoption("--keep-browser-open", action="store_true", help="Keep browser open after test execution")
    parser.addoption("--record-video", action="store_true", help="Record video of test execution")


@pytest.fixture(scope="session")
def config(request):
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    environment = request.config.getoption("--env")
    keep_browser_open = request.config.getoption("--keep-browser-open")
    record_video = request.config.getoption("--record-video")
    
    Config.BROWSER = browser
    Config.HEADLESS = headless
    Config.ENVIRONMENT = environment
    Config.KEEP_BROWSER_OPEN = keep_browser_open
    Config.RECORD_VIDEO = record_video
    
    return Config


def get_proper_chromedriver_path():
    """
    SOLUCIÓN DEFINITIVA: Obtener ChromeDriver correcto para Windows 64-bit
    """
    try:
        # Limpiar cache problemático primero
        cache_dir = r"C:\Users\HernandoMorenoVargas\.wdm\drivers\chromedriver"
        if os.path.exists(cache_dir):
            print("🔄 Limpiando cache problemático de ChromeDriver...")
            import shutil
            shutil.rmtree(cache_dir, ignore_errors=True)
        
        # Forzar descarga de versión 64-bit específica
        print("📥 Descargando ChromeDriver correcto para Windows 64-bit...")
        
        # Método 1: Usar ChromeDriverManager con parámetros específicos
        driver_path = ChromeDriverManager().install()
        print(f"✅ ChromeDriver descargado en: {driver_path}")
        
        # Verificar que sea el archivo ejecutable correcto
        if driver_path.endswith('chromedriver.exe'):
            return driver_path
        else:
            # Buscar el ejecutable en el directorio
            for file in os.listdir(os.path.dirname(driver_path)):
                if file == 'chromedriver.exe':
                    return os.path.join(os.path.dirname(driver_path), file)
        
        return driver_path
        
    except Exception as e:
        print(f"⚠️ Error con WebDriver Manager: {e}")
        print("🔄 Intentando método alternativo...")
        
        # Método 2: Usar Selenium Manager integrado
        try:
            from selenium.webdriver.chrome.service import Service
            service = Service()
            driver_path = service.path
            print(f"✅ Usando ChromeDriver de Selenium Manager: {driver_path}")
            return driver_path
        except:
            # Método 3: Último recurso - ChromeDriver portable
            print("🔧 Usando ChromeDriver portable...")
            portable_driver = os.path.join(os.getcwd(), "chromedriver.exe")
            if not os.path.exists(portable_driver):
                # Descargar ChromeDriver portable
                import requests
                import zipfile
                
                # URL de ChromeDriver estable para Windows 64-bit
                chromedriver_url = "https://storage.googleapis.com/chrome-for-testing-public/142.0.7444.175/win64/chromedriver-win64.zip"
                
                print(f"📥 Descargando ChromeDriver portable...")
                response = requests.get(chromedriver_url)
                zip_path = "chromedriver.zip"
                
                with open(zip_path, 'wb') as f:
                    f.write(response.content)
                
                # Extraer
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(".")
                
                # Mover el ejecutable
                extracted_dir = "chromedriver-win64"
                if os.path.exists(extracted_dir):
                    chromedriver_exe = os.path.join(extracted_dir, "chromedriver.exe")
                    if os.path.exists(chromedriver_exe):
                        import shutil
                        shutil.move(chromedriver_exe, portable_driver)
                        shutil.rmtree(extracted_dir, ignore_errors=True)
                
                os.remove(zip_path)
            
            return portable_driver


@pytest.fixture(scope="function")
def setup(request, config):
    """
    Fixture principal para configuración del driver y recursos
    """
    driver = None
    db = Database()
    video_recorder = None
    test_start_time = time.time()

    try:
        logger.info(f"Iniciando test: {request.node.name}")
        print(f"🚀 Iniciando test: {request.node.name}")

        # Inicializar driver según navegador
        if config.BROWSER.lower() == "chrome":
            options = Options()
            
            # ⭐ CONFIGURACIÓN OPTIMIZADA PARA WINDOWS
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--disable-extensions")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--remote-debugging-port=0")  # ⭐ CAMBIADO: puerto 0 automático
            options.add_argument("--log-level=3")
            options.add_argument("--disable-features=VizDisplayCompositor")
            options.add_argument("--disable-background-timer-throttling")
            options.add_argument("--disable-backgrounding-occluded-windows")
            options.add_argument("--disable-renderer-backgrounding")
            
            options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
            options.add_experimental_option('useAutomationExtension', False)
            
            if config.HEADLESS:
                options.add_argument("--headless=new")
                options.add_argument("--window-size=1920,1080")
            else:
                options.add_argument("--start-maximized")
            
            # Configuración de ventana
            if not config.HEADLESS:
                options.add_argument("--window-size=1920,1080")
            
            # ⭐ Mantener navegador abierto si se solicita
            if config.KEEP_BROWSER_OPEN:
                options.add_experimental_option("detach", True)
            
            # Optimización para carga más rápida
            prefs = {
                "profile.default_content_setting_values.notifications": 2,
                "profile.default_content_settings.popups": 0,
                "profile.default_content_setting_values.geolocation": 2,
                "profile.default_content_setting_values.images": 1,
                "download.default_directory": os.path.join(os.getcwd(), "downloads"),
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True
            }
            options.add_experimental_option("prefs", prefs)
            
            try:
                # ⭐ SOLUCIÓN PRINCIPAL: Obtener ChromeDriver correcto
                driver_path = get_proper_chromedriver_path()
                print(f"📍 Ruta del ChromeDriver: {driver_path}")
                
                # Verificar que el archivo existe y es ejecutable
                if not os.path.exists(driver_path):
                    raise FileNotFoundError(f"ChromeDriver no encontrado en: {driver_path}")
                
                # Configurar el servicio
                service = Service(executable_path=driver_path)
                
                # ⭐ CONFIGURACIÓN ADICIONAL DEL SERVICE
                service.creationflags = subprocess.CREATE_NO_WINDOW
                
                # Inicializar driver
                driver = webdriver.Chrome(service=service, options=options)
                
                # Ejecutar script para evitar detección de automation
                driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                
                logger.info("✅ Chrome driver inicializado correctamente")
                print("✅ Chrome driver inicializado correctamente")
                
            except Exception as driver_error:
                logger.error(f"Error inicializando Chrome driver: {driver_error}")
                print(f"❌ Error inicializando Chrome driver: {driver_error}")
                raise driver_error

        elif config.BROWSER.lower() == "firefox":
            options = FirefoxOptions()
            if config.HEADLESS:
                options.add_argument("--headless")
            
            driver = webdriver.Firefox(options=options)
            logger.info("Firefox driver inicializado")

        # Configuración común optimizada
        driver.implicitly_wait(config.IMPLICIT_WAIT)
        driver.set_page_load_timeout(config.PAGE_LOAD_TIMEOUT)
        
        if config.BROWSER.lower() != "chrome" or not config.HEADLESS:
            try:
                driver.maximize_window()
            except:
                driver.set_window_size(1920, 1080)
            
        logger.info("Driver configurado correctamente")
        
        # Iniciar grabación de video si está habilitada
        if hasattr(config, 'RECORD_VIDEO') and config.RECORD_VIDEO:
            try:
                video_recorder = VideoRecorder()
                video_recorder.start_recording(f"test_{request.node.name}")
                logger.info("Grabación de video iniciada")
            except Exception as video_error:
                logger.warning(f"No se pudo iniciar grabación de video: {video_error}")
                video_recorder = None
        else:
            logger.info("Grabación de video deshabilitada")
            video_recorder = None

        # Crear estructura de datos para el test
        test_data = {
            'driver': driver,
            'db': db,
            'video_recorder': video_recorder,
            'config': config,
            'start_time': test_start_time
        }

        yield test_data

    except Exception as e:
        logger.error(f"Error en fixture setup: {e}")
        print(f"❌ Error en fixture setup: {e}")
        
        # Adjuntar error a Allure
        with allure.step(f"ERROR en setup: {str(e)}"):
            allure.attach(str(e), name="setup_error", attachment_type=allure.attachment_type.TEXT)
        raise e
    
    finally:
        # Calcular tiempo de ejecución
        execution_time = time.time() - test_start_time
        logger.info(f"Test finalizado: {request.node.name} - Tiempo: {execution_time:.2f}s")

        # Lógica mejorada de cierre del navegador
        if driver:
            if config.KEEP_BROWSER_OPEN:
                print("🖥️  Navegador mantenido abierto por solicitud del usuario")
                logger.info("Navegador mantenido abierto (--keep-browser-open)")
            else:
                try:
                    # Tomar screenshot final antes de cerrar
                    try:
                        os.makedirs("screenshots", exist_ok=True)
                        final_screenshot = f"screenshots/final_{request.node.name}.png"
                        driver.save_screenshot(final_screenshot)
                        if os.path.exists(final_screenshot):
                            allure.attach.file(final_screenshot, 
                                             name=f"Final_Screenshot_{request.node.name}",
                                             attachment_type=allure.attachment_type.PNG)
                    except Exception as screenshot_error:
                        logger.warning(f"No se pudo tomar screenshot final: {screenshot_error}")
                    
                    driver.quit()
                    logger.info("Driver cerrado correctamente")
                    print("✅ Navegador cerrado exitosamente")
                    
                except Exception as e:
                    logger.warning(f"Error cerrando driver: {e}")
                    print(f"⚠️ Error cerrando driver: {e}")

        # Finalizar grabación de video
        if video_recorder and hasattr(config, 'RECORD_VIDEO') and config.RECORD_VIDEO:
            try:
                video_path = video_recorder.stop_recording()
                if video_path and os.path.exists(video_path):
                    # Adjuntar video a Allure
                    allure.attach.file(video_path, 
                                     name=f"Video_{request.node.name}",
                                     attachment_type=allure.attachment_type.MP4)
                    logger.info(f"Video guardado: {video_path}")
                else:
                    logger.warning("No se pudo obtener la ruta del video grabado")
            except Exception as video_error:
                logger.warning(f"Error guardando video: {video_error}")

        # Cerrar conexión a BD
        try:
            db.close_connection()
            logger.info("Conexión a BD cerrada")
        except Exception as db_error:
            logger.warning(f"Error cerrando BD: {db_error}")


# ... (el resto del código permanece igual - hooks de pytest, etc.)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook para capturar el resultado de los tests y guardar en BD
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        # Guardar resultado en BD
        try:
            db = Database()
            execution_time = report.duration if hasattr(report, 'duration') else 0

            db.insert_result(
                test_name=item.name,
                status=report.outcome,
                browser=Config.BROWSER,
                url=getattr(item.function, '__url__', 'N/A'),
                execution_time=execution_time,
                error_message=str(report.longrepr) if report.failed else None,
                environment=Config.ENVIRONMENT
            )

            logger.info(f"Resultado guardado en BD: {item.name} - {report.outcome} - {execution_time:.2f}s")

            # Adjuntar información adicional a Allure para tests fallidos
            if report.failed:
                with allure.step("TEST FAILED - Información del error"):
                    allure.attach(str(report.longrepr), name="error_details", 
                                attachment_type=allure.attachment_type.TEXT)
                    
                    # Tomar screenshot automático para tests fallidos
                    try:
                        if hasattr(item, 'funcargs') and 'setup' in item.funcargs:
                            driver = item.funcargs['setup']['driver']
                            os.makedirs("screenshots", exist_ok=True)
                            screenshot_path = f"screenshots/error_{item.name}.png"
                            driver.save_screenshot(screenshot_path)
                            if os.path.exists(screenshot_path):
                                allure.attach.file(screenshot_path,
                                                 name=f"Error_Screenshot_{item.name}",
                                                 attachment_type=allure.attachment_type.PNG)
                    except Exception as e:
                        logger.warning(f"No se pudo tomar screenshot del error: {e}")

        except Exception as e:
            logger.warning(f"Error guardando resultado en BD: {e}")
            print(f"⚠️ Error guardando resultado en BD: {e}")


def pytest_sessionstart(session):
    """Inicializar recursos al inicio de la sesión"""
    print("\n" + "="*60)
    print("🚀 INICIANDO EJECUCIÓN DE PRUEBAS AUTOMATIZADAS")
    print("="*60)

    logger.info("="*60)
    logger.info("INICIANDO SESIÓN DE PRUEBAS")
    logger.info("="*60)

    # Crear directorios necesarios
    directories = ["screenshots", "videos", "allure-results", "database", "logs", "downloads"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.debug(f"Directorio verificado: {directory}")

    # Imprimir información del sistema
    print(f"💻 Sistema: {platform.system()} {platform.architecture()[0]}")
    print(f"🐍 Python: {platform.python_version()}")
    
    # Imprimir configuración
    Config.print_config()


def pytest_sessionfinish(session, exitstatus):
    """Finalizar recursos al terminar la sesión"""
    print("\n" + "="*60)
    print("✅ EJECUCIÓN DE PRUEBAS COMPLETADA")
    print(f"📊 Estado de salida: {exitstatus}")
    print("="*60)

    logger.info("="*60)
    logger.info("SESIÓN DE PRUEBAS COMPLETADA")
    logger.info(f"Estado de salida: {exitstatus}")
    logger.info("="*60)
    
    # Generar resumen de la sesión
    try:
        db = Database()
        results = db.get_session_summary()
        if results:
            print("\n📈 RESUMEN DE LA SESIÓN:")
            print(f"   Tests exitosos: {results['passed']}")
            print(f"   Tests fallidos: {results['failed']}")
            print(f"   Tests saltados: {results['skipped']}")
            print(f"   Tiempo promedio: {results['avg_time']:.2f}s")
    except Exception as e:
        logger.warning(f"Error generando resumen: {e}")


# Fixture específico para Allure con mejor manejo de steps
@pytest.fixture(scope="function", autouse=True)
def allure_logging(request):
    """Fixture automático para mejorar el logging en Allure"""
    test_name = request.node.name
    
    with allure.step(f"🧪 TEST: {test_name}"):
        # Inicio del test
        allure.attach(f"Iniciando test: {test_name}", name="test_start", 
                     attachment_type=allure.attachment_type.TEXT)
        
        yield
        
        # Fin del test
        allure.attach(f"Finalizado test: {test_name}", name="test_end", 
                     attachment_type=allure.attachment_type.TEXT)