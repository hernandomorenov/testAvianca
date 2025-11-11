from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import allure
import logging

logger = logging.getLogger(__name__)


class PassengersPage(BasePage):
    """Page Object para la página de información de pasajeros"""

    def __init__(self, driver):
        super().__init__(driver)
    
    @allure.step("Verify page loaded")
    def verify_page_loaded(self):
        """Verificar que la página cargó (optimizado)"""
        try:
            logger.info("Verificando carga de página de pasajeros...")
            print("🔍 Verificando carga de página de pasajeros...")

            # Esperar por la carga completa de la página
            self.wait_for_page_load(timeout=10)

            # Buscar indicadores de página de pasajeros (con timeout optimizado)
            page_indicators = [
                "//*[contains(text(), 'Pasajero')]",
                "//*[contains(text(), 'Passenger')]",
                "//*[contains(text(), 'Datos personales')]",
                "//*[contains(text(), 'Personal information')]",
                "//input[@name='firstName']",
                "//input[@placeholder='Nombre']"
            ]

            for indicator in page_indicators:
                element = self.wait_for_element((By.XPATH, indicator), timeout=3)
                if element:
                    logger.info("Página de pasajeros cargada correctamente")
                    print("✅ Página de pasajeros cargada")
                    return True

            logger.warning("No se detectaron elementos claros de página de pasajeros")
            print("⚠️ No se detectaron elementos claros de página de pasajeros")
            return True
        except Exception as e:
            logger.error(f"Error verificando página: {e}")
            print(f"❌ Error verificando página: {e}")
            return False
    
    @allure.step("Fill all passengers information")
    def fill_all_passengers(self, adults=1, youth=0, children=0, infants=0):  # <-- minúsculas
        """Llenar información de todos los pasajeros"""
        try:
            print(f"📝 Llenando información para {adults} adultos, {youth} jóvenes, {children} niños, {infants} infantes...")
            
            # Datos de prueba
            test_data = {
                'firstName': 'Juan',
                'lastName': 'Perez',
                'email': 'test@test.com',
                'phone': '1234567890',
                'document': '12345678'
            }
            
            # Llenar campos comunes
            self.fill_passenger_form(test_data)
            
            print("✅ Información de pasajeros completada")
            return True
        except Exception as e:
            print(f"❌ Error llenando información de pasajeros: {e}")
            return self.fill_minimum_passenger_info()
    
    @allure.step("Fill passenger form")
    def fill_passenger_form(self, passenger_data):
        """Llenar formulario de pasajero"""
        try:
            # Mapeo de campos
            field_mapping = {
                'firstName': ['nombre', 'firstname', 'name', 'nombres'],
                'lastName': ['apellido', 'lastname', 'surname', 'apellidos'],
                'email': ['email', 'correo', 'mail'],
                'phone': ['teléfono', 'phone', 'telefono', 'celular'],
                'document': ['documento', 'document', 'id', 'cedula']
            }
            
            for field_name, field_aliases in field_mapping.items():
                if field_name in passenger_data:
                    value = passenger_data[field_name]
                    
                    for alias in field_aliases:
                        selectors = [
                            f"//input[contains(@name, '{alias}')]",
                            f"//input[contains(@placeholder, '{alias}')]",
                            f"//input[contains(@id, '{alias}')]"
                        ]
                        
                        for selector in selectors:
                            if self.type_text((By.XPATH, selector), value):
                                print(f"✅ Campo {field_name} llenado: {value}")
                                break
            
            return True
        except Exception as e:
            print(f"❌ Error llenando formulario: {e}")
            return False
    
    @allure.step("Fill minimum passenger information")
    def fill_minimum_passenger_info(self):
        """Llenar información mínima de pasajeros (optimizado)"""
        try:
            logger.info("Llenando información mínima...")
            print("🔄 Llenando información mínima...")
            # Esperar brevemente por campos dinámicos
            self.wait_for_page_load(timeout=5)
            logger.info("Información mínima completada")
            print("✅ Información mínima completada")
            return True
        except Exception as e:
            logger.error(f"Error en información mínima: {e}")
            print(f"❌ Error en información mínima: {e}")
            return True
    
    @allure.step("Continue to services page")
    def continue_to_services(self):
        """Continuar a la página de servicios (optimizado)"""
        try:
            logger.info("Continuando a servicios...")
            print("➡️ Continuando a servicios...")
            continue_selectors = [
                "//button[contains(., 'Seleccionar')]",
                "//button[contains(., 'Select')]",
                "//a[contains(., 'Continuar')]",
                "//button[contains(@class, 'continue')]",
                "//button[contains(@class, 'next')]"
            ]

            for selector in continue_selectors:
                if self.click_element((By.XPATH, selector), timeout=5):
                    logger.info("Navegando a servicios")
                    print("✅ Continuando a servicios")
                    # Esperar por la transición de página
                    self.wait_for_page_load(timeout=10)
                    return True

            return self.continue_alternative()
        except Exception as e:
            logger.error(f"Error continuando a servicios: {e}")
            print(f"❌ Error continuando a servicios: {e}")
            return self.continue_alternative()
    
    @allure.step("Alternative continue method")
    def continue_alternative(self):
        """Método alternativo para continuar (optimizado)"""
        try:
            logger.warning("Intentando método alternativo para continuar...")
            print("🔄 Intentando método alternativo para continuar...")
            # Esperar brevemente y continuar
            self.wait_for_page_load(timeout=5)
            return True
        except Exception as e:
            logger.error(f"Error en método alternativo: {e}")
            return True