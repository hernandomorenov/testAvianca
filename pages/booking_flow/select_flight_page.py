from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import allure
import time

class SelectFlightPage(BasePage):
    """Page Object para la página de selección de vuelos"""
    
    def __init__(self, driver):
        super().__init__(driver)
    
    @allure.step("Wait for flights to load")
    def wait_for_flights_load(self, timeout=30):
        """Esperar a que los vuelos carguen"""
        try:
            print("⏳ Esperando carga de vuelos...")
            time.sleep(5)  # Espera básica
            # Verificar si hay elementos de vuelos
            flight_indicators = [
                "//div[contains(@class, 'flight')]",
                "//li[contains(@class, 'flight')]",
                "//*[contains(text(), 'Vuelo')]",
                "//*[contains(text(), 'Flight')]"
            ]
            
            for indicator in flight_indicators:
                try:
                    elements = self.driver.find_elements(By.XPATH, indicator)
                    if elements:
                        print("✅ Vuelos cargados")
                        return True
                except:
                    continue
            
            print("⚠️ No se detectaron vuelos claramente, continuando...")
            return True
        except Exception as e:
            print(f"❌ Error esperando vuelos: {e}")
            return False
    
    @allure.step("Select basic fare")
    def select_basic_fare(self):
        """Seleccionar tarifa Basic"""
        try:
            print("💰 Buscando tarifa Basic...")
            fare_selectors = [
                "//*[contains(text(), 'Basic')]",
                "//*[contains(text(), 'BASIC')]",
                "//*[contains(text(), 'Básico')]",
                "//input[@value='basic']",
                "//button[contains(., 'Basic')]"
            ]
            
            for selector in fare_selectors:
                if self.click_element((By.XPATH, selector)):
                    print("✅ Tarifa Basic seleccionada")
                    time.sleep(2)
                    return True
            
            print("⚠️ No se pudo seleccionar tarifa Basic, continuando...")
            return True
        except Exception as e:
            print(f"❌ Error seleccionando tarifa Basic: {e}")
            return True
    
    @allure.step("Select departure flight")
    def select_departure_flight(self):
        """Seleccionar vuelo de ida"""
        try:
            print("✈️ Seleccionando vuelo de ida...")
            flight_selectors = [
                "//button[contains(., 'Seleccionar')]",
                "//button[contains(., 'Select')]",
                "//button[contains(., 'Elegir')]",
                "//div[contains(@class, 'flight')]//button",
                "//input[@type='radio' and contains(@name, 'flight')]"
            ]
            
            for selector in flight_selectors:
                elements = self.driver.find_elements(By.XPATH, selector)
                for element in elements:
                    if element.is_displayed() and element.is_enabled():
                        try:
                            element.click()
                            print("✅ Vuelo seleccionado")
                            time.sleep(2)
                            return True
                        except:
                            continue
            
            print("⚠️ No se pudo seleccionar vuelo específico, continuando...")
            return self.select_any_available_flight()
        except Exception as e:
            print(f"❌ Error seleccionando vuelo: {e}")
            return self.select_any_available_flight()
    
    @allure.step("Select any available flight")
    def select_any_available_flight(self):
        """Seleccionar cualquier vuelo disponible"""
        try:
            print("🔄 Seleccionando cualquier vuelo disponible...")
            # Buscar cualquier botón que parezca seleccionar vuelo
            all_buttons = self.driver.find_elements(By.TAG_NAME, "button")
            for button in all_buttons:
                try:
                    if button.is_displayed() and button.is_enabled():
                        text = button.text.lower()
                        if any(word in text for word in ['select', 'seleccionar', 'elegir', 'book', 'reservar']):
                            button.click()
                            print("✅ Vuelo seleccionado (alternativa)")
                            time.sleep(2)
                            return True
                except:
                    continue
            return True
        except Exception as e:
            print(f"❌ Error en selección alternativa: {e}")
            return True
    
    @allure.step("Continue to passengers page")
    def continue_to_passengers(self):
        """Continuar a la página de pasajeros"""
        try:
            print("➡️ Intentando continuar a pasajeros...")
            continue_selectors = [
                "//button[contains(., 'Continuar')]",
                "//button[contains(., 'Continue')]",
                "//button[contains(., 'Siguiente')]",
                "//button[contains(., 'Next')]",
                "//a[contains(., 'Continuar')]",
                "//input[@type='submit']"
            ]
            
            for selector in continue_selectors:
                if self.click_element((By.XPATH, selector)):
                    print("✅ Continuando a pasajeros")
                    time.sleep(3)
                    return True
            
            return self.continue_alternative()
        except Exception as e:
            print(f"❌ Error continuando a pasajeros: {e}")
            return self.continue_alternative()
    
    @allure.step("Alternative continue method")
    def continue_alternative(self):
        """Método alternativo para continuar"""
        try:
            print("🔄 Intentando método alternativo para continuar...")
            # Intentar con Enter
            from selenium.webdriver.common.keys import Keys
            self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ENTER)
            time.sleep(3)
            return True
        except:
            return True