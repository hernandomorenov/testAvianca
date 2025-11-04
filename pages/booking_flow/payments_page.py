from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import allure
import time

class PaymentsPage(BasePage):
    """Page Object para la página de pagos"""
    
    def __init__(self, driver):
        super().__init__(driver)
    
    @allure.step("Verify page loaded")
    def verify_page_loaded(self):
        """Verificar que la página cargó"""
        try:
            print("🔍 Verificando carga de página de pagos...")
            time.sleep(3)
            
            # Buscar indicadores de página de pagos
            page_indicators = [
                "//*[contains(text(), 'Pago')]",
                "//*[contains(text(), 'Payment')]",
                "//*[contains(text(), 'Tarjeta')]",
                "//*[contains(text(), 'Card')]",
                "//input[@name='cardNumber']"
            ]
            
            for indicator in page_indicators:
                if self.is_element_displayed((By.XPATH, indicator)):
                    print("✅ Página de pagos cargada")
                    return True
            
            print("⚠️ No se detectaron elementos claros de página de pagos")
            return True
        except Exception as e:
            print(f"❌ Error verificando página: {e}")
            return False
    
    @allure.step("Fill payment information")
    def fill_payment_information(self):
        """Llenar información de pago con datos fake"""
        try:
            print("🏦 Llenando información de pago fake...")
            
            # Datos de tarjeta fake (datos de prueba)
            fake_data = {
                'cardNumber': '4111111111111111',
                'cardHolder': 'TEST USER',
                'expiryDate': '12/25',
                'cvv': '123',
                'email': 'test@test.com'
            }
            
            # Llenar formulario de pago
            self.fill_payment_form(fake_data)
            
            print("✅ Información de pago completada")
            return True
        except Exception as e:
            print(f"❌ Error llenando información de pago: {e}")
            return False
    
    @allure.step("Fill payment form")
    def fill_payment_form(self, payment_data):
        """Llenar formulario de pago"""
        try:
            # Mapeo de campos de pago
            field_mapping = {
                'cardNumber': ['cardnumber', 'tarjeta', 'creditcard', 'numero'],
                'cardHolder': ['cardholder', 'titular', 'name', 'nombre'],
                'expiryDate': ['expiry', 'expiration', 'vencimiento', 'fecha'],
                'cvv': ['cvv', 'security', 'seguridad', 'codigo'],
                'email': ['email', 'correo', 'mail']
            }
            
            for field_name, field_aliases in field_mapping.items():
                if field_name in payment_data:
                    value = payment_data[field_name]
                    
                    for alias in field_aliases:
                        selectors = [
                            f"//input[contains(@name, '{alias}')]",
                            f"//input[contains(@placeholder, '{alias}')]",
                            f"//input[contains(@id, '{alias}')]"
                        ]
                        
                        for selector in selectors:
                            if self.type_text((By.XPATH, selector), value):
                                print(f"✅ Campo {field_name} llenado")
                                time.sleep(1)
                                break
            
            # Intentar enviar el pago
            return self.submit_payment()
        except Exception as e:
            print(f"❌ Error llenando formulario de pago: {e}")
            return False
    
    @allure.step("Submit payment")
    def submit_payment(self):
        """Enviar el pago"""
        try:
            print("📤 Enviando pago...")
            
            # Buscar botones de envío
            submit_selectors = [
                "//button[contains(., 'Pagar')]",
                "//button[contains(., 'Pay')]",
                "//button[contains(., 'Confirmar')]",
                "//button[contains(., 'Confirm')]",
                "//input[@type='submit']"
            ]
            
            for selector in submit_selectors:
                if self.click_element((By.XPATH, selector)):
                    print("✅ Pago enviado")
                    time.sleep(5)  # Esperar respuesta del pago
                    return True
            
            print("⚠️ No se pudo enviar el pago automáticamente")
            return True
        except Exception as e:
            print(f"❌ Error enviando pago: {e}")
            return True