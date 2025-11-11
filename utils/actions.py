from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import allure
import time
import os


class Actions:
    """Clase base con acciones comunes para Page Objects"""
    
    def __init__(self, driver):
         self.driver = driver
         self.wait = WebDriverWait(driver, 10)
         self.actions = ActionChains(driver)
    
    def wait_for_page_load(self, timeout=10):
        """Esperar a que la página cargue completamente"""
        return self.wait.until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
    
    @allure.step("Navigate to: {url}")
    def navigate_to(self, url):
        """Navegar a una URL específica"""
        try:
            print(f"🌐 Navegando a: ✈️🛫🛬{url}")
            self.driver.get(url)
            
            # Esperar con diferentes estrategias
            WebDriverWait(self.driver, 5).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            
            # Espera adicional para contenido dinámico
            time.sleep(2)
            
            # Verificar que la URL cargó correctamente
            current_url = self.driver.current_url
            if current_url and "avtest.ink" in current_url:
                print(f"✅ Navegación exitosa a: {current_url}")
                return True
            else:
                print(f"⚠️ Posible redirección: {current_url}")
                return True  # Continuar de todas formas
            
        except Exception as e:
         print(f"❌ Error navegando a {url}: {e}")
          # Intentar recuperación
        try:
             self.driver.get(url)
             time.sleep(5)
             return True
        except:
            return False
    
    @allure.step("Find element: {locator}")
    def find_element(self, locator, timeout=7):
        """Encontrar elemento con espera explícita"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except TimeoutException:
            print(f"❌ Elemento no encontrado: {locator}")
            return None
    
    @allure.step("Click element: {locator}")
    def click_element(self, locator, timeout=5):
        """Hacer clic en un elemento"""
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
            print(f"✅ Clic en elemento: {locator}")
            return True
        except Exception as e:
            print(f"❌ Error haciendo clic en {locator}: {e}")
            return False
    
    @allure.step("Type text: {text} in {locator}")
    def type_text(self, locator, text):
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.clear()
            element.send_keys(text)
            return True
        except:
            return False
    
    @allure.step("Select dropdown option: {option} from {locator}")
    def select_dropdown_option(self, locator, option, by_value=False):
        """Seleccionar opción de dropdown"""
        try:
            from selenium.webdriver.support.select import Select
            element = self.find_element(locator)
            if element:
                select = Select(element)
                if by_value:
                    select.select_by_value(option)
                else:
                    select.select_by_visible_text(option)
                print(f"✅ Opción seleccionada: {option} en {locator}")
                return True
            return False
        except Exception as e:
            print(f"❌ Error seleccionando opción {option} en {locator}: {e}")
            return False
    
    @allure.step("Take screenshot: {name}")
    def take_screenshot(self, name):
        """Tomar screenshot y adjuntar a Allure"""
        try:
            screenshot_dir = "screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            filename = f"{name}_{timestamp}.png"
            filepath = os.path.join(screenshot_dir, filename)
            
            self.driver.save_screenshot(filepath)
            print(f"📸 Screenshot guardado: {filepath}")
            
            # Adjuntar a Allure
            allure.attach.file(filepath, name=name, 
                             attachment_type=allure.attachment_type.PNG)
            
            return filepath
            
        except Exception as e:
            print(f"⚠️ Error tomando screenshot: {e}")
            return None
    
    @allure.step("Wait for page to load")
    def wait_for_page_load(self, timeout=15):
        """Esperar a que la página cargue completamente"""
        try:
            self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
            time.sleep(2)  # Espera adicional para contenido dinámico
            return True
        except Exception as e:
            print(f"⚠️ Error esperando carga de página: {e}")
            return False
    
    @allure.step("Get current URL")
    def get_current_url(self):
        """Obtener URL actual"""
        return self.driver.current_url
    
    @allure.step("Get page title")
    def get_page_title(self):
        """Obtener título de la página"""
        return self.driver.title
    
    def is_element_present(self, locator, timeout=5):
        """Verificar si un elemento está presente"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def is_element_visible(self, locator, timeout=5):
        """Verificar si un elemento es visible"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def navigate_to(self, url):
        """Navegar a una URL específica"""
        try:
            self.driver.get(url)
            self.wait_for_page_load()
            print(f"✅ Navegado exitosamente a: {url}")
            return True
        except Exception as e:
            print(f"❌ Error navegando a {url}: {e}")
            return False