from selenium.webdriver.common.by import By
from pages.booking_flow import BasePage
import allure
import time


class ServicesPage(BasePage):
    """Page Object para página de servicios adicionales"""
    
    # Selectores de servicios
    LOUNGE_SERVICE = (By.XPATH, "//div[contains(text(), 'Lounge')]//input | //input[contains(@id, 'lounge')]")
    BAGGAGE_SERVICE = (By.XPATH, "//div[contains(text(), 'Baggage')]//input | //input[contains(@id, 'baggage')]")
    MEAL_SERVICE = (By.XPATH, "//div[contains(text(), 'Meal')]//input | //input[contains(@id, 'meal')]")
    INSURANCE_SERVICE = (By.XPATH, "//div[contains(text(), 'Insurance')]//input | //input[contains(@id, 'insurance')]")
    
    # Botones
    CONTINUE_BUTTON = (By.XPATH, "//button[contains(text(), 'Continue') or contains(text(), 'Continuar')]")
    SKIP_BUTTON = (By.XPATH, "//button[contains(text(), 'Skip') or contains(text(), 'Saltar')]")
    NO_THANKS_BUTTON = (By.XPATH, "//button[contains(text(), 'No thanks') or contains(text(), 'No gracias')]")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    @allure.step("Select lounge service")
    def select_lounge_service(self):
        """Seleccionar servicio de lounge"""
        return self.click_element(self.LOUNGE_SERVICE)
    
    @allure.step("Select baggage service")
    def select_baggage_service(self):
        """Seleccionar servicio de equipaje"""
        return self.click_element(self.BAGGAGE_SERVICE)
    
    @allure.step("Select meal service")
    def select_meal_service(self):
        """Seleccionar servicio de comida"""
        return self.click_element(self.MEAL_SERVICE)
    
    @allure.step("Select insurance service")
    def select_insurance_service(self):
        """Seleccionar servicio de seguro"""
        return self.click_element(self.INSURANCE_SERVICE)
    
    @allure.step("Select available service")
    def select_available_service(self):
        """Seleccionar cualquier servicio disponible"""
        services = [
            self.LOUNGE_SERVICE,
            self.BAGGAGE_SERVICE, 
            self.MEAL_SERVICE,
            self.INSURANCE_SERVICE
        ]
        
        for service in services:
            if self.click_element(service):
                print(f"✅ Servicio seleccionado: {service}")
                return True
        
        print("❌ No se encontraron servicios disponibles")
        return False
    
    @allure.step("Skip services")
    def skip_services(self):
        """Saltar servicios adicionales"""
        return self.click_element(self.SKIP_BUTTON) or self.click_element(self.NO_THANKS_BUTTON)
    
    @allure.step("Continue to seatmap page")
    def continue_to_seatmap(self):
        """Continuar a página de selección de asientos"""
        success = self.click_element(self.CONTINUE_BUTTON)
        if success:
            time.sleep(3)
        return success
    
    @allure.step("Verify services page loaded")
    def verify_page_loaded(self):
        """Verificar que la página de servicios cargó"""
        try:
            return (self.is_element_present(self.CONTINUE_BUTTON, timeout=10) or 
                   self.is_element_present(self.SKIP_BUTTON, timeout=10))
        except Exception as e:
            print(f"❌ Error verificando página de servicios: {e}")
            return False