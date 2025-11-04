"""
Driver Factory para crear instancias de WebDriver
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from utils.config import Config
import os


class DriverFactory:
    """Factory para crear WebDrivers"""
    
    @staticmethod
    def create_driver():
        """Crear instancia de WebDriver según configuración"""
        browser = Config.BROWSER.lower()
        
        if browser == "chrome":
            return DriverFactory._create_chrome_driver()
        elif browser == "firefox":
            return DriverFactory._create_firefox_driver()
        elif browser == "edge":
            return DriverFactory._create_edge_driver()
        else:
            raise ValueError(f"Browser no soportado: {browser}")
    
    @staticmethod
    def _create_chrome_driver():
        """Crear Chrome Driver"""
        chrome_options = Options()
        
        # Configuraciones básicas
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-notifications")
        
        # Configuraciones de performance
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        if Config.HEADLESS:
            chrome_options.add_argument("--headless")
        
        # Configurar timeouts
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(Config.IMPLICIT_WAIT)
        driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)  # ✅ ESTO NECESITA EL ATRIBUTO
        
        return driver
    
    @staticmethod
    def _create_firefox_driver():
        """Crear Firefox Driver"""
        firefox_options = FirefoxOptions()
        
        if Config.HEADLESS:
            firefox_options.add_argument("--headless")
        
        driver = webdriver.Firefox(options=firefox_options)
        driver.maximize_window()
        driver.implicitly_wait(Config.IMPLICIT_WAIT)
        driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)  # ✅ ESTO NECESITA EL ATRIBUTO
        
        return driver
    
    @staticmethod
    def _create_edge_driver():
        """Crear Edge Driver"""
        driver = webdriver.Edge()
        driver.maximize_window()
        driver.implicitly_wait(Config.IMPLICIT_WAIT)
        driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)  # ✅ ESTO NECESITA EL ATRIBUTO
        
        return driver