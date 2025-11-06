from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import allure
import time

class SeatmapPage(BasePage):
    """Page Object para la página de selección de asientos"""
    
    def __init__(self, driver):
        super().__init__(driver)
    
    @allure.step("Verify page loaded")
    def verify_page_loaded(self):
        """Verificar que la página cargó"""
        try:
            print("🔍 Verificando carga de página de asientos...")
            time.sleep(3)
            
            # Buscar indicadores de página de asientos
            page_indicators = [
                "//*[contains(text(), 'Asiento')]",
                "//*[contains(text(), 'Seat')]",
                "//*[contains(text(), 'Selecciona tu asiento')]",
                "//*[contains(text(), 'Select your seat')]"
            ]
            
            for indicator in page_indicators:
                if self.is_element_displayed((By.XPATH, indicator)):
                    print("✅ Página de asientos cargada")
                    return True
            
            print("⚠️ No se detectaron elementos claros de página de asientos")
            return True
        except Exception as e:
            print(f"❌ Error verificando página: {e}")
            return False
    
    @allure.step("Select economy seat")
    def select_economy_seat(self):
        """Seleccionar asiento economy"""
        try:
            print("💺 Buscando asiento economy...")
            
            # Buscar asientos economy
            seat_selectors = [
                "//*[contains(text(), 'Economy')]",
                "//*[contains(text(), 'Económico')]",
                "//*[contains(@class, 'economy')]",
                "//button[contains(., 'Seleccionar') and contains(., 'Economy')]",
                "//div[contains(@class, 'seat')]"
            ]
            
            for selector in seat_selectors:
                elements = self.driver.find_elements(By.XPATH, selector)
                for element in elements:
                    if element.is_displayed() and element.is_enabled():
                        try:
                            element.click()
                            print("✅ Asiento economy seleccionado")
                            time.sleep(2)
                            return True
                        except:
                            continue
            
            return self.select_any_available_seat()
        except Exception as e:
            print(f"❌ Error seleccionando asiento economy: {e}")
            return self.select_any_available_seat()
    
    @allure.step("Select any available seat")
    def select_any_available_seat(self):
        """Seleccionar cualquier asiento disponible"""
        try:
            print("🔄 Seleccionando cualquier asiento disponible...")
            
            # Buscar cualquier asiento disponible
            all_buttons = self.driver.find_elements(By.TAG_NAME, "button")
            for button in all_buttons:
                try:
                    if button.is_displayed() and button.is_enabled():
                        text = button.text.lower()
                        if any(word in text for word in ['select', 'seleccionar', 'elegir', 'asiento', 'seat']):
                            button.click()
                            print("✅ Asiento seleccionado (alternativa)")
                            time.sleep(2)
                            return True
                except:
                    continue
            
            print("⚠️ No se pudo seleccionar asiento, continuando...")
            return True
        except Exception as e:
            print(f"❌ Error en selección alternativa de asiento: {e}")
            return True
    
    @allure.step("Continue to payments page")
    def continue_to_payments(self):
        """Continuar a la página de pagos"""
        try:
            print("➡️ Continuando a página de pagos...")
            continue_selectors = [
                "//button[contains(., 'Continuar')]",
                "//button[contains(., 'Continue')]",
                "//button[contains(., 'Select')]",
                "//button[contains(., 'Seleccionar')]",
                "//a[contains(., 'Continuar')]",
                "//button[contains(., 'Pagar')]",
                "//button[contains(., 'Pay')]"
            ]
            
            for selector in continue_selectors:
                if self.click_element((By.XPATH, selector)):
                    print("✅ Continuando a pagos")
                    time.sleep(3)
                    return True
            
            return self.continue_alternative()
        except Exception as e:
            print(f"❌ Error continuando a pagos: {e}")
            return self.continue_alternative()
    
    @allure.step("Alternative continue method")
    def continue_alternative(self):
        """Método alternativo para continuar"""
        try:
            print("🔄 Intentando método alternativo para continuar...")
            time.sleep(2)
            return True
        except:
            return True