import pytest
import allure
import sqlite3
import time
import os
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from utils.config import Config
from utils.database import Database
from utils.video_recorder import VideoRecorder
from utils.logger import setup_logger

# Configurar logger al inicio
logger = setup_logger()


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
    test_start_time = time.time()

    try:
        logger.info(f"Iniciando test: {request.node.name}")

        # Inicializar driver según navegador
        if config.BROWSER.lower() == "chrome":
            options = Options()
            if config.HEADLESS:
                options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            # Optimización para carga más rápida
            prefs = {
                "profile.default_content_setting_values.notifications": 2,
                "profile.default_content_settings.popups": 0
            }
            options.add_experimental_option("prefs", prefs)
            driver = webdriver.Chrome(options=options)
            logger.info("Chrome driver inicializado")

        elif config.BROWSER.lower() == "firefox":
            options = FirefoxOptions()
            if config.HEADLESS:
                options.add_argument("--headless")
            driver = webdriver.Firefox(options=options)
            logger.info("Firefox driver inicializado")

        # Configuración común optimizada
        driver.implicitly_wait(config.IMPLICIT_WAIT)
        driver.set_page_load_timeout(config.PAGE_LOAD_TIMEOUT)
        driver.maximize_window()
        logger.info("Driver configurado correctamente")
        
        # Iniciar grabación de video si está habilitada
        if Config.RECORD_VIDEO:
            video_recorder = VideoRecorder()
            video_recorder.start_recording(f"test_{request.node.name}")
            logger.info("Grabación de video iniciada")

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
        raise
    
    finally:
        # Calcular tiempo de ejecución
        execution_time = time.time() - test_start_time
        logger.info(f"Test finalizado: {request.node.name} - Tiempo: {execution_time:.2f}s")

        # Finalizar grabación de video
        if video_recorder and Config.RECORD_VIDEO:
            video_path = video_recorder.stop_recording()
            if video_path:
                # Adjuntar video a Allure
                allure.attach.file(video_path, name=f"Video_{request.node.name}",
                                 attachment_type=allure.attachment_type.MP4)
                logger.info(f"Video guardado: {video_path}")

        # Cerrar driver
        if driver:
            try:
                driver.quit()
                logger.info("Driver cerrado correctamente")
            except Exception as e:
                logger.warning(f"Error cerrando driver: {e}")
                print(f"⚠️ Error cerrando driver: {e}")

        # Cerrar conexión a BD
        db.close_connection()
        logger.info("Conexión a BD cerrada")


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
    directories = ["screenshots", "videos", "allure-results", "database", "logs"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.debug(f"Directorio verificado: {directory}")

    # Imprimir configuración
    Config.print_config()


def pytest_sessionfinish(session):
    """Finalizar recursos al terminar la sesión"""
    print("\n" + "="*60)
    print("✅ EJECUCIÓN DE PRUEBAS COMPLETADA")
    print("="*60)

    logger.info("="*60)
    logger.info("SESIÓN DE PRUEBAS COMPLETADA")
    logger.info("="*60)