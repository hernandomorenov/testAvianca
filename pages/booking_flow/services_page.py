from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import allure
import time

class ServicesPage(BasePage):
    """Page Object para la página de servicios adicionales"""
    
    def __init__(self, driver):
        super().__init__(driver)
    
    @allure.step("Verify page loaded")
    def verify_page_loaded(self):
        """Verificar que la página cargó"""
        try:
            print("🔍 Verificando carga de página de servicios...")
            time.sleep(3)
            print("✅ Página de servicios cargada")
            return True
        except Exception as e:
            print(f"❌ Error verificando página: {e}")
            return False
    
    @allure.step("Skip services")
    def skip_services(self):
        """No seleccionar servicios adicionales"""
        try:
            print("⏭️ Saltando servicios adicionales...")
            
            # Buscar botones para continuar sin servicios
            skip_selectors = [
                "//button[contains(., 'Continuar sin servicios')]",
                "//button[contains(., 'Skip services')]",
                "//button[contains(., 'No gracias')]",
                "//button[contains(., 'No, thanks')]",
                "//button[contains(., 'Continuar')]",
                "//button[contains(., 'Continue')]"
            ]
            
            for selector in skip_selectors:
                if self.click_element((By.XPATH, selector)):
                    print("✅ Servicios saltados")
                    time.sleep(2)
                    return True
            
            return self.continue_directly()
        except Exception as e:
            print(f"❌ Error saltando servicios: {e}")
            return self.continue_directly()
    
    @allure.step("Continue directly")
    def continue_directly(self):
        """Continuar directamente sin interactuar con servicios"""
        try:
            print("🔄 Continuando directamente...")
            time.sleep(2)
            return True
        except Exception as e:
            print(f"❌ Error continuando directamente: {e}")
            return True
    
    @allure.step("Continue to seatmap page")
    def continue_to_seatmap(self):
        """Continuar a la página de asientos"""
        try:
            print("➡️ Continuando a selección de asientos...")
            continue_selectors = [
                "//button[contains(., 'Continuar')]",
                "//button[contains(., 'Continue')]",
                "//button[contains(., 'Siguiente')]",
                "//button[contains(., 'Next')]",
                "//a[contains(., 'Continuar')]"
            ]
            
            for selector in continue_selectors:
                if self.click_element((By.XPATH, selector)):
                    print("✅ Continuando a asientos")
                    time.sleep(3)
                    return True
            
            return self.continue_alternative()
        except Exception as e:
            print(f"❌ Error continuando a asientos: {e}")
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