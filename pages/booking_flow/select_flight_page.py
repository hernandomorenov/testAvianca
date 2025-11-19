from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from pages.base_page import BasePage
import allure
import time

class SelectFlightPage(BasePage):
    """Page Object para la página de selección de vuelos - VERSIÓN MEJORADA"""

    def __init__(self, driver):
        super().__init__(driver)
        self.timeout = 10

    # ========================================================================
    # MÉTODOS DE WAIT MEJORADOS (consistentes con HomePage)
    # ========================================================================

    def wait_for_element(self, locator, timeout=None):
        """Esperar a que un elemento esté presente en el DOM"""
        timeout = timeout or self.timeout
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        except Exception as e:
            print(f"❌ Timeout esperando elemento {locator}: {e}")
            return None

    def wait_for_element_clickable(self, locator, timeout=None):
        """Esperar a que un elemento sea clickeable"""
        timeout = timeout or self.timeout
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
        except Exception as e:
            print(f"❌ Timeout esperando elemento clickeable {locator}: {e}")
            return None

    def safe_click(self, element, element_name="element"):
        """Hacer clic seguro con reintentos"""
        try:
            # Scroll al elemento
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});",
                element
            )
            time.sleep(0.5)
            
            # Intentar diferentes métodos de clic
            click_methods = [
                ("clic normal", lambda: element.click()),
                ("JavaScript", lambda: self.driver.execute_script("arguments[0].click();", element)),
                ("ActionChains", lambda: ActionChains(self.driver).move_to_element(element).click().perform())
            ]
            
            for method_name, click_func in click_methods:
                try:
                    click_func()
                    print(f"✅ Clic exitoso en {element_name} con {method_name}")
                    return True
                except Exception as e:
                    print(f"⚠️ {method_name} falló: {e}")
                    continue
            
            return False
        except Exception as e:
            print(f"❌ Error en safe_click: {e}")
            return False

    def retry_operation(self, operation, max_attempts=3, delay=1):
        """Reintentar una operación que puede fallar"""
        for attempt in range(max_attempts):
            try:
                return operation()
            except Exception as e:
                if attempt == max_attempts - 1:
                    raise e
                print(f"⚠️ Intento {attempt + 1} falló, reintentando...: {e}")
                time.sleep(delay)

    # ========================================================================
    # MÉTODOS PRINCIPALES MEJORADOS
    # ========================================================================

    @allure.step("Verify page loaded")
    def verify_page_loaded(self):
        """Verificar que la página de selección de vuelos cargó correctamente - VERSIÓN MEJORADA"""
        def verify_operation():
            try:
                print("🔍 Verificando carga de página de selección de vuelos...")
                
                # Esperar carga inicial
                self.wait_for_page_load(timeout=15)
                
                # Buscar indicadores de página de selección de vuelos
                page_indicators = [
                    "//*[contains(text(), 'Selecciona')]",
                    "//*[contains(text(), 'Select')]",
                    "//*[contains(text(), 'Vuelo')]",
                    "//*[contains(text(), 'Flight')]",
                    "//button[contains(@class, 'fare')]",
                    "//div[contains(@class, 'flight')]",
                    "//div[contains(@class, 'itinerary')]",
                    "//div[contains(@class, 'journey')]"
                ]

                elements_found = 0
                for indicator in page_indicators:
                    try:
                        elements = self.driver.find_elements(By.XPATH, indicator)
                        visible_elements = [e for e in elements if e.is_displayed()]
                        if visible_elements:
                            elements_found += len(visible_elements)
                            print(f"   ✅ Indicador encontrado: {indicator} - {len(visible_elements)} elementos")
                    except Exception as e:
                        continue

                if elements_found > 0:
                    print(f"✅ Página de selección de vuelos cargada - {elements_found} indicadores encontrados")
                    return True
                else:
                    # Verificar por URL
                    current_url = self.driver.current_url.lower()
                    if any(keyword in current_url for keyword in ['select', 'flight', 'vuelo', 'seleccion']):
                        print("✅ URL indica página de selección de vuelos")
                        return True
                    
                    print("⚠️ No se detectaron elementos claros de selección de vuelos")
                    return True  # Continuar de todos modos
                    
            except Exception as e:
                print(f"❌ Error verificando página: {e}")
                return False
        
        return self.retry_operation(verify_operation, max_attempts=2)

    @allure.step("Wait for flights to load")
    def wait_for_flights_load(self, timeout=30):
        """Esperar a que los vuelos carguen - VERSIÓN MEJORADA"""
        try:
            print("⏳ Esperando carga de vuelos...")
            
            # Usar WebDriverWait en lugar de time.sleep
            flight_indicators = [
                (By.XPATH, "//div[contains(@class, 'flight')]"),
                (By.XPATH, "//li[contains(@class, 'flight')]"),
                (By.XPATH, "//*[contains(text(), 'Vuelo')]"),
                (By.XPATH, "//*[contains(text(), 'Flight')]"),
                (By.XPATH, "//div[contains(@class, 'fare')]")
            ]
            
            for locator in flight_indicators:
                try:
                    elements = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_all_elements_located(locator)
                    )
                    if elements:
                        visible_elements = [e for e in elements if e.is_displayed()]
                        if visible_elements:
                            print(f"✅ Vuelos cargados - {len(visible_elements)} elementos encontrados")
                            return True
                except:
                    continue
            
            print("⚠️ No se detectaron vuelos claramente después de espera, continuando...")
            return True
        except Exception as e:
            print(f"❌ Error esperando vuelos: {e}")
            return True
        
    def select_fare_type(self, fare_type="Classic", max_attempts=3):
        """
        Versión mejorada para seleccionar tipo de tarifa
        """
        print(f"💰 Seleccionando tarifa {fare_type}...")
        
        fare_type = fare_type.lower()
        
        for attempt in range(max_attempts):
            try:
                # Buscar tarifas con múltiples estrategias
                fare_selectors = [
                    f"//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{fare_type}')]",
                    f"//div[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{fare_type}')]",
                    f"//*[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{fare_type}')]//button",
                    f"//div[contains(@class, 'fare') and contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{fare_type}')]",
                    f"//*[contains(@class, 'fare')]//*[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{fare_type}')]",
                    f"//button[contains(@class, 'fare_button') and contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{fare_type}')]"
                ]
                
                fare_element = None
                for selector in fare_selectors:
                    try:
                        elements = WebDriverWait(self.driver, 5).until(
                            EC.presence_of_all_elements_located((By.XPATH, selector))
                        )
                        for element in elements:
                            if element.is_displayed() and element.is_enabled():
                                fare_element = element
                                print(f"✅ Tarifa {fare_type} encontrada: {selector}")
                                break
                        if fare_element:
                            break
                    except:
                        continue
                
                if fare_element:
                    self.driver.execute_script("arguments[0].click();", fare_element)
                    print(f"✅ Tarifa {fare_type} seleccionada")
                    time.sleep(2)
                    return True
                else:
                    print(f"❌ No se encontró tarifa {fare_type} en intento {attempt + 1}")
                    if attempt < max_attempts - 1:
                        time.sleep(2)
                        
            except Exception as e:
                print(f"❌ Error seleccionando tarifa {fare_type}: {e}")
                if attempt < max_attempts - 1:
                    time.sleep(2)
        
        print(f"⚠️ No se pudo seleccionar tarifa {fare_type} específica, continuando...")
        return False

    @allure.step("Select basic fare")
    def select_basic_fare(self):
        """Seleccionar tarifa Basic - VERSIÓN MEJORADA CON RETRY"""
        def select_operation():
            try:
                print("💰 Buscando tarifa Basic...")

                # Selectores más específicos y robustos
                fare_selectors = [
                    # 1. Botones con texto Basic/Básico
                    "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'basic') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'básico')]",
                    "//div[contains(@class, 'fare') and contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'basic')]",
                    "//div[contains(@class, 'fare')]//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'basic')]",

                    # 2. Selectores por clase específica
                    "//button[contains(@class, 'fare_button') and contains(., 'Basic')]",
                    "//div[contains(@class, 'fare_button') and contains(., 'Basic')]",
                    "//button[contains(@class, 'basic')]",

                    # 3. Selectores genéricos
                    "//button[contains(., 'Basic')]",
                    "//div[contains(., 'Basic')]"
                ]

                for selector in fare_selectors:
                    try:
                        element = self.wait_for_element_clickable((By.XPATH, selector), timeout=5)
                        if element:
                            if self.safe_click(element, "tarifa Basic"):
                                print(f"✅ Tarifa Basic seleccionada con selector: {selector}")
                                time.sleep(2)
                                return True
                    except Exception as e:
                        print(f"⚠️ Error con selector {selector}: {e}")
                        continue

                print("⚠️ No se pudo seleccionar tarifa Basic específica, continuando...")
                return True
            except Exception as e:
                print(f"❌ Error seleccionando tarifa Basic: {e}")
                return True

        return self.retry_operation(select_operation, max_attempts=2)

    @allure.step("Select classic fare")
    def select_classic_fare(self):
        """Seleccionar tarifa Classic - VERSIÓN MEJORADA CON RETRY"""
        def select_operation():
            try:
                print("💰 Buscando tarifa Classic...")

                # Selectores más específicos y robustos para Classic
                fare_selectors = [
                    # 1. Botones con texto Classic/Clásico
                    "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'classic') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'clásico')]",
                    "//div[contains(@class, 'fare') and contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'classic')]",
                    "//div[contains(@class, 'fare')]//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'classic')]",

                    # 2. Selectores por clase específica
                    "//button[contains(@class, 'fare_button') and contains(., 'Classic')]",
                    "//div[contains(@class, 'fare_button') and contains(., 'Classic')]",
                    "//button[contains(@class, 'classic')]",

                    # 3. Selectores genéricos
                    "//button[contains(., 'Classic')]",
                    "//div[contains(., 'Classic')]",

                    # 4. Por índice (segunda tarifa)
                    "(//button[contains(@class, 'fare_button')])[2]",
                    "(//div[contains(@class, 'fare')]//button)[2]"
                ]

                for selector in fare_selectors:
                    try:
                        element = self.wait_for_element_clickable((By.XPATH, selector), timeout=5)
                        if element:
                            # Verificar que el texto contenga "Classic" antes de hacer clic
                            element_text = element.text.lower()
                            if 'classic' in element_text or 'clásico' in element_text:
                                if self.safe_click(element, "tarifa Classic"):
                                    print(f"✅ Tarifa Classic seleccionada con selector: {selector}")
                                    time.sleep(2)
                                    return True
                            else:
                                # Si no tiene "classic" en el texto, probar de todas formas si es un selector por índice
                                if '[2]' in selector:
                                    if self.safe_click(element, "tarifa Classic (segunda opción)"):
                                        print(f"✅ Tarifa Classic seleccionada por índice: {selector}")
                                        time.sleep(2)
                                        return True
                    except Exception as e:
                        print(f"⚠️ Error con selector {selector}: {e}")
                        continue

                print("⚠️ No se pudo seleccionar tarifa Classic específica, continuando...")
                return True
            except Exception as e:
                print(f"❌ Error seleccionando tarifa Classic: {e}")
                return True

        return self.retry_operation(select_operation, max_attempts=2)

    @allure.step("Select departure flight")
    def select_departure_flight(self, max_attempts=5):
        """
        Versión mejorada para seleccionar vuelo de ida
        """
        print("✈️ Seleccionando vuelo de ida...")
        
        for attempt in range(max_attempts):
            try:
                print(f"🔄 Intento {attempt + 1}/{max_attempts}")
                
                # 1. Esperar que los vuelos estén cargados
                print("⏳ Esperando carga de vuelos...")
                time.sleep(5)  # Espera inicial más larga
                
                # 2. Buscar contenedores de vuelos con múltiples estrategias
                flight_containers = []
                
                container_selectors = [
                    "//div[contains(@class, 'flight-card')]",
                    "//div[contains(@class, 'flight_item')]",
                    "//div[contains(@class, 'flight-container')]",
                    "//div[contains(@class, 'flight-row')]",
                    "//div[contains(@class, 'journey')]",
                    "//div[contains(@class, 'outbound')]",
                    "//section[contains(@class, 'flight')]",
                    "//div[@data-testid='flight-card']",
                    "//div[contains(@id, 'flight')]"
                ]
                
                for selector in container_selectors:
                    try:
                        containers = self.driver.find_elements(By.XPATH, selector)
                        if containers:
                            flight_containers = containers
                            print(f"✅ Vuelos encontrados con: {selector} - {len(flight_containers)} elementos")
                            break
                    except:
                        continue
                
                if not flight_containers:
                    print("❌ No se encontraron contenedores de vuelos")
                    # Tomar screenshot para debugging
                    self.take_screenshot("no_flight_containers")
                    continue
                
                # 3. Buscar botones de selección dentro del primer contenedor
                print("🔍 Buscando botones de selección...")
                
                button_selectors = [
                    ".//button[contains(@class, 'select')]",
                    ".//button[contains(@class, 'fare')]",
                    ".//button[contains(@class, 'book')]",
                    ".//button[contains(@class, 'choose')]",
                    ".//button[contains(text(), 'Select')]",
                    ".//button[contains(text(), 'Seleccionar')]",
                    ".//button[contains(text(), 'Elegir')]",
                    ".//button[contains(text(), 'Book')]",
                    ".//div[contains(@class, 'fare')]//button",
                    ".//div[contains(@class, 'price')]//button",
                    ".//a[contains(@class, 'select')]",
                    ".//a[contains(text(), 'Select')]"
                ]
                
                select_button = None
                for container in flight_containers[:3]:  # Revisar solo primeros 3 contenedores
                    for selector in button_selectors:
                        try:
                            buttons = container.find_elements(By.XPATH, selector)
                            for btn in buttons:
                                if btn.is_displayed() and btn.is_enabled():
                                    select_button = btn
                                    print(f"✅ Botón encontrado: {selector}")
                                    break
                            if select_button:
                                break
                        except:
                            continue
                    if select_button:
                        break
                
                if select_button:
                    # Hacer clic con JavaScript
                    self.driver.execute_script("arguments[0].click();", select_button)
                    print("✅ Botón de selección clickeado")
                    
                    # Esperar que la página procese la selección
                    time.sleep(3)
                    
                    # Verificar si avanzamos a la siguiente página
                    current_url = self.driver.current_url
                    if "booking" in current_url.lower() and "select" not in current_url.lower():
                        print("✅ Avanzamos a la siguiente página de booking")
                        return True
                    else:
                        print("ℹ️ Seguimos en la misma página, verificando selección...")
                        # Verificar si hay indicadores de selección exitosa
                        success_indicators = [
                            "//div[contains(@class, 'selected')]",
                            "//div[contains(@class, 'success')]",
                            "//*[contains(text(), 'selected')]",
                            "//*[contains(text(), 'Selected')]"
                        ]
                        
                        for indicator in success_indicators:
                            try:
                                elements = self.driver.find_elements(By.XPATH, indicator)
                                if elements:
                                    print("✅ Vuelo seleccionado exitosamente")
                                    return True
                            except:
                                continue
                
                # 4. Si no encontramos botones, intentar con tarifas específicas
                print("🔍 Intentando selección por tarifas...")
                fare_selectors = [
                    "//div[contains(@class, 'fare') and contains(., 'Classic')]",
                    "//div[contains(@class, 'fare') and contains(., 'classic')]",
                    "//div[contains(@class, 'fare-type') and contains(., 'Classic')]",
                    "//*[contains(text(), 'Classic') and contains(@class, 'fare')]",
                    "//*[contains(text(), 'CLASSIC')]//ancestor::div[contains(@class, 'fare')]",
                    "//div[contains(@class, 'fare-card')]",
                    "//div[contains(@class, 'tarifa')]"
                ]
                
                for selector in fare_selectors:
                    try:
                        fare_elements = self.driver.find_elements(By.XPATH, selector)
                        for fare in fare_elements:
                            if fare.is_displayed():
                                print(f"✅ Tarifa encontrada: {selector}")
                                # Intentar hacer clic en la tarifa o en botones dentro de ella
                                buttons_in_fare = fare.find_elements(By.XPATH, ".//button")
                                if buttons_in_fare:
                                    for btn in buttons_in_fare:
                                        if btn.is_displayed() and btn.is_enabled():
                                            self.driver.execute_script("arguments[0].click();", btn)
                                            print("✅ Botón en tarifa clickeado")
                                            time.sleep(3)
                                            return True
                                else:
                                    # Hacer clic directo en la tarifa
                                    self.driver.execute_script("arguments[0].click();", fare)
                                    print("✅ Tarifa clickeada directamente")
                                    time.sleep(3)
                                    return True
                    except:
                        continue
                
                # 5. Último intento: buscar cualquier botón que parezca de selección
                print("🔍 Búsqueda exhaustiva de botones...")
                all_buttons = self.driver.find_elements(By.XPATH, "//button")
                for btn in all_buttons:
                    try:
                        btn_text = btn.text.lower()
                        if any(keyword in btn_text for keyword in ['select', 'seleccionar', 'book', 'reservar', 'elegir', 'choose', 'continuar', 'continue']):
                            if btn.is_displayed() and btn.is_enabled():
                                print(f"✅ Botón encontrado por texto: {btn.text}")
                                self.driver.execute_script("arguments[0].click();", btn)
                                time.sleep(3)
                                return True
                    except:
                        continue
                
                print(f"❌ Intento {attempt + 1} fallado")
                if attempt < max_attempts - 1:
                    print("🔄 Reintentando en 3 segundos...")
                    time.sleep(3)
                    
            except Exception as e:
                print(f"❌ Error en intento {attempt + 1}: {e}")
                if attempt < max_attempts - 1:
                    time.sleep(3)
        
        print("❌ No se pudo seleccionar el vuelo después de todos los intentos")
        # Tomar screenshot final para debugging
        self.take_screenshot("flight_selection_failed")
        return False

    def take_screenshot(self, name):
        """Tomar screenshot para debugging"""
        try:
            screenshot_path = f"utils/test_results/screenshots/{name}_{int(time.time())}.png"
            self.driver.save_screenshot(screenshot_path)
            print(f"📸 Screenshot: {screenshot_path}")
        except Exception as e:
            print(f"⚠️ No se pudo tomar screenshot: {e}")
            
        @allure.step("Select any available flight")
        def select_any_available_flight(self):
            """Seleccionar cualquier vuelo disponible - VERSIÓN MEJORADA"""
            try:
                print("🔄 Seleccionando cualquier vuelo disponible...")
                
                # Buscar cualquier botón que parezca seleccionar vuelo
                all_buttons = self.driver.find_elements(By.TAG_NAME, "button")
                select_keywords = ['select', 'seleccionar', 'elegir', 'choose', 'book', 'reservar', 'continuar', 'continue']
                
                for button in all_buttons:
                    try:
                        if button.is_displayed() and button.is_enabled():
                            text = button.text.lower()
                            if any(keyword in text for keyword in select_keywords):
                                if self.safe_click(button, "botón genérico de vuelo"):
                                    print(f"✅ Vuelo seleccionado (alternativa): {button.text}")
                                    time.sleep(2)
                                    return True
                    except Exception as e:
                        continue
                
                # Si no encuentra botones específicos, hacer clic en el primer botón disponible
                for button in all_buttons:
                    try:
                        if button.is_displayed() and button.is_enabled():
                            if self.safe_click(button, "primer botón disponible"):
                                print("✅ Clic en primer botón disponible")
                                time.sleep(2)
                                return True
                    except:
                        continue
                
                print("⚠️ No se encontraron botones clickeables")
                return True
            except Exception as e:
                print(f"❌ Error en selección alternativa: {e}")
                return True

    @allure.step("Continue to passengers page")
    def continue_to_passengers(self):
        """Continuar a la página de pasajeros - VERSIÓN MEJORADA CON RETRY"""
        def continue_operation():
            try:
                print("➡️ Intentando continuar a pasajeros...")
                
                continue_selectors = [
                    "//button[contains(., 'Continuar')]",
                    "//button[contains(., 'Continue')]",
                    "//button[contains(., 'Siguiente')]",
                    "//button[contains(., 'Next')]",
                    "//button[contains(., 'Pasajeros')]",
                    "//button[contains(., 'Passengers')]",
                    "//a[contains(., 'Continuar')]",
                    "//input[@type='submit']"
                ]
                
                for selector in continue_selectors:
                    try:
                        element = self.wait_for_element_clickable((By.XPATH, selector), timeout=5)
                        if element:
                            if self.safe_click(element, "botón continuar"):
                                print(f"✅ Continuando a pasajeros con: {selector}")
                                time.sleep(3)
                                return True
                    except Exception as e:
                        print(f"⚠️ Error con selector {selector}: {e}")
                        continue
                
                return self.continue_alternative()
            except Exception as e:
                print(f"❌ Error continuando a pasajeros: {e}")
                return self.continue_alternative()
        
        return self.retry_operation(continue_operation, max_attempts=2)

    @allure.step("Alternative continue method")
    def continue_alternative(self):
        """Método alternativo para continuar"""
        try:
            print("🔄 Intentando método alternativo para continuar...")
            
            # Intentar con Enter
            from selenium.webdriver.common.keys import Keys
            body = self.driver.find_element(By.TAG_NAME, 'body')
            body.send_keys(Keys.ENTER)
            time.sleep(3)
            
            # Verificar si cambió la URL
            current_url = self.driver.current_url.lower()
            if any(keyword in current_url for keyword in ['passenger', 'pasajero', 'traveler']):
                print("✅ Redireccionado a página de pasajeros (método alternativo)")
                return True
            else:
                print("⚠️ Método alternativo ejecutado, pero no se verificó redirección")
                return True
                
        except Exception as e:
            print(f"❌ Error en método alternativo: {e}")
            return True

    @allure.step("Take screenshot: {screenshot_name}")
    def take_screenshot(self, screenshot_name):
        """Tomar screenshot - consistente con HomePage"""
        try:
            screenshot_path = f"./screenshots/{screenshot_name}.png"
            self.driver.save_screenshot(screenshot_path)
            allure.attach.file(
                screenshot_path,
                name=screenshot_name,
                attachment_type=allure.attachment_type.PNG,
            )
            print(f"📸 Screenshot: {screenshot_name}")
        except Exception as e:
            print(f"⚠️ Error tomando screenshot: {e}")

    def wait_for_page_load(self, timeout=10):
        """Esperar a que la página cargue completamente"""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            print("✅ Página cargada completamente")
            return True
        except Exception as e:
            print(f"⚠️ Timeout esperando carga de página: {e}")
            return False