from pages.base_page import BasePage 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import allure
import time


class SelectFlightPage(BasePage):
    """Page Object para la página de selección de vuelos"""
    
    # Selectores para la página de selección de vuelos
    FLIGHT_OPTIONS = (By.XPATH, "//div[contains(@class, 'flight-option')] | //div[contains(@class, 'flight-card')]")
    SELECT_BUTTON = (By.XPATH, "//button[contains(text(), 'Seleccionar')] | //button[contains(text(), 'Select')]")
    CONTINUE_BUTTON = (By.XPATH, "//button[contains(text(), 'Continuar')] | //button[contains(text(), 'Continue')]")
    PRICE_ELEMENT = (By.XPATH, "//span[contains(@class, 'price')] | //div[contains(@class, 'price')]")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    @allure.step("Select first available flight")
    def select_first_available_flight(self):
        """Seleccionar el primer vuelo disponible"""
        try:
            # Esperar a que carguen las opciones de vuelo
            flight_options = self.wait_for_elements(self.FLIGHT_OPTIONS, timeout=15)
            
            if flight_options and len(flight_options) > 0:
                print(f"✅ Se encontraron {len(flight_options)} opciones de vuelo")
                
                # Seleccionar la primera opción
                first_flight = flight_options[0]
                first_flight.click()
                print("✅ Primera opción de vuelo seleccionada")
                
                # Hacer clic en continuar
                time.sleep(2)
                self.click_element(self.CONTINUE_BUTTON)
                print("✅ Botón continuar clickeado")
                
                return True
            else:
                print("❌ No se encontraron opciones de vuelo")
                return False
                
        except Exception as e:
            print(f"❌ Error seleccionando vuelo: {e}")
            return False
    
    @allure.step("Verify flight selection page loaded")
    def verify_page_loaded(self):
        """Verificar que la página de selección de vuelos cargó correctamente"""
        try:
            return self.wait_for_element(self.FLIGHT_OPTIONS, timeout=15) is not None
        except Exception as e:
            print(f"❌ Error verificando carga de página: {e}")
            return False
    
    @allure.step("Get flight prices")
    def get_flight_prices(self):
        """Obtener precios de los vuelos disponibles"""
        try:
            prices = []
            price_elements = self.driver.find_elements(*self.PRICE_ELEMENT)
            
            for element in price_elements:
                try:
                    price_text = element.text.strip()
                    if price_text and any(char.isdigit() for char in price_text):
                        prices.append(price_text)
                except:
                    continue
            
            print(f"💰 Precios encontrados: {prices}")
            return prices
            
        except Exception as e:
            print(f"❌ Error obteniendo precios: {e}")
            return []
    
    @allure.step("Wait for multiple elements")
    def wait_for_elements(self, locator, timeout=10):
        """Esperar a que múltiples elementos estén presentes"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            elements = wait.until(EC.presence_of_all_elements_located(locator))
            return elements
        except TimeoutException:
            print(f"❌ Timeout esperando elementos: {locator}")
            return []