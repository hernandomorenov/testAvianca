from selenium.webdriver.common.by import By
from pages.booking_flow import BasePage
from faker import Faker
import allure
import time


class PassengersPage(BasePage):
    """Page Object para página de información de pasajeros"""
    
    # Selectores generales de pasajeros
    PASSENGER_FORM = (By.XPATH, "//form[contains(@class, 'passenger')]")
    FIRST_NAME_INPUT = (By.XPATH, "//input[contains(@id, 'firstName') or contains(@name, 'firstName')]")
    LAST_NAME_INPUT = (By.XPATH, "//input[contains(@id, 'lastName') or contains(@name, 'lastName')]")
    EMAIL_INPUT = (By.XPATH, "//input[contains(@id, 'email') or contains(@type, 'email')]")
    PHONE_INPUT = (By.XPATH, "//input[contains(@id, 'phone') or contains(@name, 'phone')]")
    
    # Selectores específicos por tipo de pasajero
    ADULT_TITLE = (By.XPATH, "//select[contains(@id, 'adult-title')]")
    ADULT_BIRTH_DATE = (By.XPATH, "//input[contains(@id, 'adult-birth')]")
    
    YOUTH_TITLE = (By.XPATH, "//select[contains(@id, 'youth-title')]")
    YOUTH_BIRTH_DATE = (By.XPATH, "//input[contains(@id, 'youth-birth')]")
    
    CHILD_TITLE = (By.XPATH, "//select[contains(@id, 'child-title')]")
    CHILD_BIRTH_DATE = (By.XPATH, "//input[contains(@id, 'child-birth')]")
    
    INFANT_TITLE = (By.XPATH, "//select[contains(@id, 'infant-title')]")
    INFANT_BIRTH_DATE = (By.XPATH, "//input[contains(@id, 'infant-birth')]")
    
    # Botones
    CONTINUE_BUTTON = (By.XPATH, "//button[contains(text(), 'Continue') or contains(text(), 'Continuar')]")
    SAVE_BUTTON = (By.XPATH, "//button[contains(text(), 'Save') or contains(text(), 'Guardar')]")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.fake = Faker()
    
    @allure.step("Fill passenger information for {passenger_type}")
    def fill_passenger_info(self, passenger_type, passenger_index=0):
        """Llenar información del pasajero según su tipo"""
        try:
            # Datos ficticios según tipo de pasajero
            if passenger_type == "adult":
                first_name = self.fake.first_name()
                last_name = self.fake.last_name()
                birth_date = "01/01/1980"
                title = "Mr"
            elif passenger_type == "youth":
                first_name = self.fake.first_name()
                last_name = self.fake.last_name()
                birth_date = "01/01/2005"
                title = "Ms"
            elif passenger_type == "child":
                first_name = self.fake.first_name()
                last_name = self.fake.last_name()
                birth_date = "01/01/2015"
                title = "Miss"
            elif passenger_type == "infant":
                first_name = self.fake.first_name()
                last_name = self.fake.last_name()
                birth_date = "01/01/2022"
                title = "Baby"
            else:
                print(f"❌ Tipo de pasajero no válido: {passenger_type}")
                return False
            
            # Construir selectores dinámicos basados en índice y tipo
            first_name_locator = (By.XPATH, f"//input[contains(@id, '{passenger_type}{passenger_index}-firstname') or contains(@name, '{passenger_type}{passenger_index}-firstname')]")
            last_name_locator = (By.XPATH, f"//input[contains(@id, '{passenger_type}{passenger_index}-lastname') or contains(@name, '{passenger_type}{passenger_index}-lastname')]")
            
            # Llenar información básica
            success_first = self.type_text(first_name_locator, first_name)
            success_last = self.type_text(last_name_locator, last_name)
            
            # Llenar información específica si está disponible
            email_success = True
            phone_success = True
            
            # Solo el primer pasajero necesita email y teléfono
            if passenger_index == 0:
                email_locator = (By.XPATH, "//input[contains(@id, 'email')]")
                phone_locator = (By.XPATH, "//input[contains(@id, 'phone')]")
                
                email_success = self.type_text(email_locator, self.fake.email())
                phone_success = self.type_text(phone_locator, self.fake.phone_number())
            
            success = success_first and success_last and email_success and phone_success
            
            if success:
                print(f"✅ Información de {passenger_type} {passenger_index + 1} completada")
            else:
                print(f"❌ Error completando información de {passenger_type} {passenger_index + 1}")
            
            return success
            
        except Exception as e:
            print(f"❌ Error llenando información de pasajero: {e}")
            return False
    
    @allure.step("Fill all passengers information")
    def fill_all_passengers(self, adults=1, youth=0, children=0, infants=0):
        """Llenar información para todos los pasajeros"""
        try:
            # Llenar adultos
            for i in range(adults):
                if not self.fill_passenger_info("adult", i):
                    return False
                time.sleep(1)
            
            # Llenar jóvenes
            for i in range(youth):
                if not self.fill_passenger_info("youth", i):
                    return False
                time.sleep(1)
            
            # Llenar niños
            for i in range(children):
                if not self.fill_passenger_info("child", i):
                    return False
                time.sleep(1)
            
            # Llenar infantes
            for i in range(infants):
                if not self.fill_passenger_info("infant", i):
                    return False
                time.sleep(1)
            
            print(f"✅ Información de todos los pasajeros completada")
            return True
            
        except Exception as e:
            print(f"❌ Error llenando información de todos los pasajeros: {e}")
            return False
    
    @allure.step("Continue to services page")
    def continue_to_services(self):
        """Continuar a página de servicios"""
        success = self.click_element(self.CONTINUE_BUTTON)
        if success:
            time.sleep(3)  # Esperar transición
        return success
    
    @allure.step("Verify passengers page loaded")
    def verify_page_loaded(self):
        """Verificar que la página de pasajeros cargó"""
        try:
            return self.is_element_present(self.PASSENGER_FORM, timeout=10)
        except Exception as e:
            print(f"❌ Error verificando página de pasajeros: {e}")
            return False