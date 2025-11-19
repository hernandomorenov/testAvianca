"""
BasePage - Clase base para todos los Page Objects
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import allure
import time
import os
import logging

# Configurar logger
logger = logging.getLogger(__name__)


class BasePage:
    """Clase base para todos los Page Objects"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        #Mejora de tiempos de respuesta
        self.short_wait = WebDriverWait(driver, 5)
        self.long_wait = WebDriverWait(driver, 20)
    
    # ========================================================================
    # MÉTODOS BÁSICOS DE SELENIUM
    # ========================================================================
    
    @allure.step("Navigate to: {url}")
    def navigate_to(self, url):
        """Navegar a una URL"""
        try:
            self.driver.get(url)
            logger.info(f"Navegando a: {url}")
            print(f"🌐 Navegando a: {url}")

            # Esperar a que la página cargue (optimizado)
            if self.wait_for_page_load(timeout=15):
                logger.info(f"Página cargada exitosamente: {url}")
                print(f"✅ Página cargada exitosamente: {url}")
                return True
            else:
                logger.warning(f"Timeout esperando carga, pero continuando: {url}")
                print(f"⚠️ Página cargada pero timeout en espera: {url}")
                return True  # Continuar aunque el timeout falle

        except Exception as e:
            logger.error(f"Error navegando a {url}: {e}")
            print(f"❌ Error navegando a {url}: {e}")
            return False
       
    
    @allure.step("Get current URL")
    def get_current_url(self):
        """Obtener URL actual"""
        return self.driver.current_url
    
    @allure.step("Get page title")
    def get_page_title(self):
        """Obtener título de la página"""
        return self.driver.title
    
    @allure.step("Refresh page")
    def refresh_page(self):
        """Refrescar página"""
        self.driver.refresh()
        print("🔄 Página refrescada")
    
    # ========================================================================
    # MÉTODOS DE ESPERA
    # ========================================================================
    
    @allure.step("Wait for element: {locator}")
    def wait_for_element(self, locator, timeout=10):
        """Esperar a que un elemento esté presente y visible"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.visibility_of_element_located(locator))
            logger.debug(f"Elemento encontrado: {locator}")
            print(f"✅ Elemento encontrado: {locator}")
            return element
        except TimeoutException:
            logger.warning(f"Timeout esperando elemento: {locator}")
            print(f"❌ Timeout esperando elemento: {locator}")
            return None
    
    @allure.step("Wait for element clickable: {locator}")
    def wait_for_element_clickable(self, locator, timeout=10):
        """Esperar a que un elemento sea clickeable"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.element_to_be_clickable(locator))
            logger.debug(f"Elemento clickeable: {locator}")
            print(f"✅ Elemento clickeable: {locator}")
            return element
        except TimeoutException:
            logger.warning(f"Timeout esperando elemento clickeable: {locator}")
            print(f"❌ Timeout esperando elemento clickeable: {locator}")
            return None
    
    @allure.step("Wait for page to load")
    def wait_for_page_load(self, timeout=15):
        """Esperar a que la página cargue completamente (optimizado)"""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            logger.debug("Página cargada completamente")
            print("✅ Página cargada completamente")
            return True
        except TimeoutException:
            logger.warning("Timeout esperando carga de página")
            print("❌ Timeout esperando carga de página")
            return False
    
    # ========================================================================
    # MÉTODOS DE INTERACCIÓN
    # ========================================================================
    
    @allure.step("Click element: {locator}")
    def click_element(self, locator, timeout=10):
        """Hacer clic en un elemento (optimizado con espera clickeable)"""
        try:
            element = self.wait_for_element_clickable(locator, timeout)
            if element:
                try:
                    element.click()
                    logger.debug(f"Clic en elemento: {locator}")
                    print(f"✅  Clic en elemento: {locator}")
                    return True
                except Exception as e:
                    # Intentar con JavaScript como fallback
                    logger.debug(f"Usando JavaScript click para: {locator}")
                    self.driver.execute_script("arguments[0].click();", element)
                    return True
            return False
        except Exception as e:
            logger.error(f"Error haciendo clic en {locator}: {e}")
            return False
    
    @allure.step("Type text: {text} in element: {locator}")
    def type_text(self, locator, text):
        """Escribir texto en un campo"""
        element = self.wait_for_element(locator)
        if element:
            element.clear()
            element.send_keys(text)
            print(f"✅ Texto escrito: '{text}' en {locator}")
            return True
        return False
    
    @allure.step("Get text from element: {locator}")
    def get_element_text(self, locator):
        """Obtener texto de un elemento"""
        element = self.wait_for_element(locator)
        if element:
            return element.text
        return None
    
    @allure.step("Get attribute: {attribute} from element: {locator}")
    def get_element_attribute(self, locator, attribute):
        """Obtener atributo de un elemento"""
        element = self.wait_for_element(locator)
        if element:
            return element.get_attribute(attribute)
        return None
    
    @allure.step("Check if element is displayed: {locator}")
    def is_element_displayed(self, locator):
        """Verificar si un elemento está visible"""
        try:
            element = self.driver.find_element(*locator)
            return element.is_displayed()
        except NoSuchElementException:
            return False
    
    @allure.step("Check if element exists: {locator}")
    def is_element_present(self, locator):
        """Verificar si un elemento existe en el DOM"""
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
    
    # ========================================================================
    # MÉTODOS DE SCROLL
    # ========================================================================
    
    @allure.step("Scroll to element: {locator}")
    def scroll_to_element(self, locator):
        """Hacer scroll hasta un elemento"""
        element = self.wait_for_element(locator)
        if element:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            print(f"✅ Scroll hasta elemento: {locator}")
            return True
        return False
    
    @allure.step("Scroll to bottom of page")
    def scroll_to_bottom(self):
        """Hacer scroll hasta el final de la página"""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print("✅ Scroll hasta el final de la página")
    
    @allure.step("Scroll to top of page")
    def scroll_to_top(self):
        """Hacer scroll hasta el inicio de la página"""
        self.driver.execute_script("window.scrollTo(0, 0);")
        print("✅ Scroll hasta el inicio de la página")
    
    # ========================================================================
    # MÉTODOS DE CAPTURA DE PANTALLA
    # ========================================================================
    
    @allure.step("Take screenshot: {name}")
    def take_screenshot(self, name):
        """Tomar screenshot y adjuntar a Allure"""
        try:
            screenshot_dir = "screenshots"
            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)
            
            filename = f"{screenshot_dir}/{name}_{int(time.time())}.png"
            self.driver.save_screenshot(filename)
            
            # Adjuntar screenshot a Allure
            allure.attach.file(
                filename,
                name=name,
                attachment_type=allure.attachment_type.PNG
            )
            
            print(f"📸 Screenshot tomado: {filename}")
            return filename
        except Exception as e:
            print(f"❌ Error tomando screenshot: {e}")
            return None
    
    @allure.step("Take screenshot on failure")
    def take_screenshot_on_failure(self, test_name):
        """Tomar screenshot cuando falla un test"""
        screenshot_name = f"FAILED_{test_name}"
        return self.take_screenshot(screenshot_name)
    
    # ========================================================================
    # MÉTODOS DE VERIFICACIÓN
    # ========================================================================
    
    @allure.step("Verify page title contains: {expected_text}")
    def verify_title_contains(self, expected_text):
        """Verificar que el título contiene texto esperado"""
        actual_title = self.get_page_title()
        result = expected_text.lower() in actual_title.lower()
        
        if result:
            print(f"✅ Título verificado: '{expected_text}' encontrado en '{actual_title}'")
        else:
            print(f"❌ Título no contiene texto esperado. Actual: '{actual_title}', Esperado: '{expected_text}'")
        
        return result
    
    @allure.step("Verify URL contains: {expected_text}")
    def verify_url_contains(self, expected_text):
        """Verificar que la URL contiene texto esperado"""
        actual_url = self.get_current_url()
        result = expected_text.lower() in actual_url.lower()
        
        if result:
            print(f"✅ URL verificado: '{expected_text}' encontrado en '{actual_url}'")
        else:
            print(f"❌ URL no contiene texto esperado. Actual: '{actual_url}', Esperado: '{expected_text}'")
        
        return result
    
    @allure.step("Verify element text: {locator} contains: {expected_text}")
    def verify_element_text_contains(self, locator, expected_text):
        """Verificar que el texto de un elemento contiene texto esperado"""
        actual_text = self.get_element_text(locator)
        if actual_text is None:
            print(f"❌ Elemento no encontrado: {locator}")
            return False
        
        result = expected_text.lower() in actual_text.lower()
        
        if result:
            print(f"✅ Texto verificado: '{expected_text}' encontrado en '{actual_text}'")
        else:
            print(f"❌ Texto no contiene texto esperado. Actual: '{actual_text}', Esperado: '{expected_text}'")
        
        return result
    
    @allure.step("Verify element is visible: {locator}")
    def verify_element_visible(self, locator):
        """Verificar que un elemento es visible"""
        result = self.is_element_displayed(locator)
        
        if result:
            print(f"✅ Elemento visible: {locator}")
        else:
            print(f"❌ Elemento no visible: {locator}")
        
        return result
    
    # ========================================================================
    # MÉTODOS DE IDIOMA
    # ========================================================================
    
    @allure.step("Get page language")
    def get_page_language(self):
        """Obtener idioma de la página"""
        try:
            # Intentar obtener del atributo lang del HTML
            html_lang = self.driver.execute_script("return document.documentElement.lang")
            if html_lang:
                return html_lang
            
            # Intentar obtener de la URL
            current_url = self.driver.current_url.lower()
            if '/es/' in current_url:
                return 'es'
            elif '/en/' in current_url:
                return 'en'
            elif '/fr/' in current_url:
                return 'fr'
            elif '/pt/' in current_url:
                return 'pt'
            else:
                return 'unknown'
                
        except Exception as e:
            print(f"⚠️ Error obteniendo idioma: {e}")
            return 'unknown'
    
    # ========================================================================
    # MÉTODOS DE NAVEGACIÓN
    # ========================================================================
    
    @allure.step("Go back")
    def go_back(self):
        """Volver a la página anterior"""
        self.driver.back()
        print("↩️ Navegando hacia atrás")
        time.sleep(2)
    
    @allure.step("Go forward")
    def go_forward(self):
        """Avanzar a la página siguiente"""
        self.driver.forward()
        print("↪️ Navegando hacia adelante")
        time.sleep(2)
    
    # ========================================================================
    # MÉTODOS DE MANEJO DE VENTANAS
    # ========================================================================
    
    @allure.step("Switch to new window")
    def switch_to_new_window(self):
        """Cambiar a la nueva ventana"""
        try:
            # Esperar a que haya más de una ventana
            WebDriverWait(self.driver, 10).until(
                lambda driver: len(driver.window_handles) > 1
            )
            
            # Cambiar a la última ventana
            self.driver.switch_to.window(self.driver.window_handles[-1])
            print("✅ Cambiado a nueva ventana")
            return True
        except TimeoutException:
            print("❌ No se encontró nueva ventana")
            return False
    
    @allure.step("Close current window and switch back")
    def close_current_window_and_switch_back(self):
        """Cerrar ventana actual y volver a la principal"""
        try:
            if len(self.driver.window_handles) > 1:
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
                print("✅ Ventana cerrada y vuelto a ventana principal")
            return True
        except Exception as e:
            print(f"❌ Error manejando ventanas: {e}")
            return False
    
    # ========================================================================
    # MÉTODOS DE LOGGING
    # ========================================================================
    
    @allure.step("Log page info")
    def log_page_info(self):
        """Log información de la página actual"""
        print(f"📄 Título: {self.get_page_title()}")
        print(f"🌐 URL: {self.get_current_url()}")
        print(f"🗣️ Idioma: {self.get_page_language()}")
        
    # ========================================================================
    # MÉTODOS DE ESPERA RÁPIDA
    # ========================================================================
        
        
    def wait_for_element_quick(self, locator, timeout=2):
        """Wait rápido para elementos con timeout corto"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        except:
            return None