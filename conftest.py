import pytest
import allure
import sqlite3
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from utils.config import Config
from utils.database import Database
from utils.video_recorder import VideoRecorder


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser to run tests: chrome, firefox, edge")
    parser.addoption("--headless", action="store_true", help="Run in headless mode")
    parser.addoption("--env", action="store", default="uat1", help="Environment: uat1, uat2")


@pytest.fixture(scope="session")
def config(request):
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    environment = request.config.getoption("--env")
    
    Config.BROWSER = browser
    Config.HEADLESS = headless
    Config.ENVIRONMENT = environment
    
    return Config


@pytest.fixture(scope="function")
def setup(request, config):
    """
    Fixture principal para configuración del driver y recursos
    """
    driver = None
    db = Database()
    video_recorder = None
    
    try:
        # Inicializar driver según navegador
        if config.BROWSER.lower() == "chrome":
            options = Options()
            if config.HEADLESS:
                options.add_argument("--headless")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            driver = webdriver.Chrome(options=options)
            
        elif config.BROWSER.lower() == "firefox":
            options = FirefoxOptions()
            if config.HEADLESS:
                options.add_argument("--headless")
            driver = webdriver.Firefox(options=options)
        
        # Configuración común
        driver.implicitly_wait(10)
        driver.maximize_window()
        
        # Iniciar grabación de video si está habilitada
        if Config.RECORD_VIDEO:
            video_recorder = VideoRecorder()
            video_recorder.start_recording(f"test_{request.node.name}")
        
        # Crear estructura de datos para el test
        test_data = {
            'driver': driver,
            'db': db,
            'video_recorder': video_recorder,
            'config': config
        }
        
        yield test_data
        
    except Exception as e:
        print(f"❌ Error en fixture setup: {e}")
        raise
    
    finally:
        # Finalizar grabación de video
        if video_recorder and Config.RECORD_VIDEO:
            video_path = video_recorder.stop_recording()
            if video_path and hasattr(request.node, 'test_result'):
                # Adjuntar video a Allure
                allure.attach.file(video_path, name=f"Video_{request.node.name}", 
                                 attachment_type=allure.attachment_type.MP4)
        
        # Cerrar driver
        if driver:
            try:
                driver.quit()
            except Exception as e:
                print(f"⚠️ Error cerrando driver: {e}")
        
        # Cerrar conexión a BD
        db.close_connection()


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
            db.insert_result(
                test_name=item.name,
                status=report.outcome,
                browser=Config.BROWSER,
                url=getattr(item.function, '__url__', 'N/A'),
                execution_time=0,  # Se calcularía con timing
                error_message=str(report.longrepr) if report.failed else None
            )
        except Exception as e:
            print(f"⚠️ Error guardando resultado en BD: {e}")


def pytest_sessionstart(session):
    """Inicializar recursos al inicio de la sesión"""
    print("\n" + "="*60)
    print("🚀 INICIANDO EJECUCIÓN DE PRUEBAS AUTOMATIZADAS")
    print("="*60)
    
    # Crear directorios necesarios
    os.makedirs("screenshots", exist_ok=True)
    os.makedirs("videos", exist_ok=True)
    os.makedirs("allure-results", exist_ok=True)
    os.makedirs("database", exist_ok=True)


def pytest_sessionfinish(session):
    """Finalizar recursos al terminar la sesión"""
    print("\n" + "="*60)
    print("✅ EJECUCIÓN DE PRUEBAS COMPLETADA")
    print("="*60)