from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import allure
import time
import unicodedata
import os

from utils.config import Config


class HomePage(BasePage):
    """Page Object COMPLETO para la página principal de reservas"""

    # ========================================================================
    # SELECTORES
    # ========================================================================
    ORIGIN_INPUT = (By.XPATH, "//input[@placeholder] | //input[@name] | //input[@id]")
    DESTINATION_INPUT = (
        By.XPATH,
        "//input[@placeholder] | //input[@name] | //input[@id]",
    )
    DEPARTURE_DATE = (
        By.XPATH,
        "//input[contains(@id, 'departure')] | //input[contains(@name, 'departure')] | //input[@type='date']",
    )
    RETURN_DATE = (
        By.XPATH,
        "//input[contains(@id, 'return')] | //input[contains(@name, 'return')] | //input[contains(@placeholder, 'Vuelta')]",
    )
    SEARCH_BUTTON = (
        By.XPATH,
        "//button | //a[contains(@class, 'btn')] | //input[@type='submit']",
    )

    # Selectores de idiomas
    LANGUAGE_SELECTOR = (
        By.XPATH,
        "//select | //div[contains(@class, 'dropdown')] | //button[contains(@class, 'lang')]",
    )
    LANGUAGE_BUTTON_ES = (
        By.XPATH,
        "//*[contains(text(), 'ES') or contains(text(), 'Español') or contains(@href, '/es/')]",
    )
    LANGUAGE_BUTTON_EN = (
        By.XPATH,
        "//*[contains(text(), 'EN') or contains(text(), 'English') or contains(@href, '/en/')]",
    )
    LANGUAGE_BUTTON_FR = (
        By.XPATH,
        "//*[contains(text(), 'FR') or contains(text(), 'Français') or contains(@href, '/fr/')]",
    )
    LANGUAGE_BUTTON_PT = (
        By.XPATH,
        "//*[contains(text(), 'PT') or contains(text(), 'Português') or contains(@href, '/pt/')]",
    )

    # Selectores de POS
    POS_SELECTOR = (
        By.XPATH,
        "//select[contains(@id, 'country')] | //select[contains(@name, 'country')] | //div[contains(@class, 'country')]",
    )

    def __init__(self, driver):
        super().__init__(driver)
        os.makedirs("./screenshots", exist_ok=True)

    @staticmethod
    def _normalize_text(text: str) -> str:
        """Normaliza texto: quita tildes, lower, strip."""
        if not text:
            return ""
        nfkd = unicodedata.normalize("NFKD", text)
        only_ascii = "".join([c for c in nfkd if not unicodedata.combining(c)])
        return only_ascii.lower().strip()

    # ========================================================================
    # MÉTODOS DE BÚSQUEDA DE VUELOS
    # ========================================================================

    @allure.step("Find and fill origin input")
    def find_and_fill_origin(self, origin):
        """Encontrar y llenar el input de origen"""
        inputs = self.driver.find_elements(*self.ORIGIN_INPUT)
        for input_field in inputs:
            try:
                if input_field.is_displayed() and input_field.is_enabled():
                    placeholder = (
                        input_field.get_attribute("placeholder") or ""
                    ).lower()
                    name = (input_field.get_attribute("name") or "").lower()
                    id_attr = (input_field.get_attribute("id") or "").lower()

                    if (
                        any(
                            word in placeholder
                            for word in ["origen", "from", "salida", "origin"]
                        )
                        or any(word in name for word in ["origin", "from"])
                        or any(word in id_attr for word in ["origin", "from"])
                    ):
                        input_field.clear()
                        input_field.send_keys(origin)
                        print(f"✅ Origen '{origin}' ingresado")
                        return True
            except Exception:
                continue
        print("❌ No se pudo encontrar el input de origen")
        return False

    @allure.step("Find and fill destination input")
    def find_and_fill_destination(self, destination):
        """Encontrar y llenar el input de destino"""
        inputs = self.driver.find_elements(*self.DESTINATION_INPUT)
        for input_field in inputs:
            try:
                if input_field.is_displayed() and input_field.is_enabled():
                    placeholder = (
                        input_field.get_attribute("placeholder") or ""
                    ).lower()
                    name = (input_field.get_attribute("name") or "").lower()
                    id_attr = (input_field.get_attribute("id") or "").lower()

                    if (
                        any(
                            word in placeholder
                            for word in ["destino", "to", "llegada", "destination"]
                        )
                        or any(word in name for word in ["destination", "to"])
                        or any(word in id_attr for word in ["destination", "to"])
                    ):
                        input_field.clear()
                        input_field.send_keys(destination)
                        print(f"✅ Destino '{destination}' ingresado")
                        return True
            except Exception:
                continue
        print("❌ No se pudo encontrar el input de destino")
        return False

    @allure.step("Set origin: {origin} and destination: {destination}")
    def set_origin_destination(self, origin, destination):
        """Configurar origen y destino"""
        success_origin = self.find_and_fill_origin(origin)
        time.sleep(1)
        success_destination = self.find_and_fill_destination(destination)
        return success_origin and success_destination

    @allure.step("Search flights")
    def search_flights(self):
        """Buscar vuelos"""
        buttons = self.driver.find_elements(*self.SEARCH_BUTTON)
        for button in buttons:
            try:
                if button.is_displayed() and button.is_enabled():
                    button_text = button.text.lower()
                    if any(
                        word in button_text
                        for word in ["buscar", "search", "find", "vuelos"]
                    ):
                        button.click()
                        print("✅ Botón de búsqueda clickeado")
                        time.sleep(3)
                        return True
            except Exception:
                continue
        return False

    # ========================================================================
    # MÉTODOS DE CAMBIO DE IDIOMA - CORREGIDOS Y COMPLETOS
    # ========================================================================

    @allure.step("Change language to {language}")
    def change_language(self, language):
        """
        Cambiar idioma - método mejorado con múltiples estrategias
        Compatible con test_caso_4.py
        """
        try:
            print(f"\n🔄 INICIANDO CAMBIO DE IDIOMA A: {language.upper()}")

            # Mapping de idiomas
            language_mapping = {
                "spanish": {"code": "es", "text": "Español", "short": "ES"},
                "english": {"code": "en", "text": "English", "short": "EN"},
                "french": {"code": "fr", "text": "Français", "short": "FR"},
                "portuguese": {"code": "pt", "text": "Português", "short": "PT"},
            }

            lang_info = language_mapping.get(language.lower())
            if not lang_info:
                print(f"❌ Idioma no soportado: {language}")
                return False

            lang_code = lang_info["code"]

            # Tomar screenshot antes
            self.take_screenshot(f"antes_cambio_idioma_{lang_code}")

            # ESTRATEGIA 1: Cambio directo por URL (más confiable)
            print("🔍 Estrategia 1: Cambio por URL...")
            success = self.change_language_by_url(language)
            if success:
                print(f"✅ Idioma cambiado exitosamente a {language} por URL")
                self.take_screenshot(f"despues_cambio_idioma_{lang_code}")
                return True

            # ESTRATEGIA 2: Buscar enlaces de idioma
            print("🔍 Estrategia 2: Buscando enlaces...")
            all_links = self.driver.find_elements(By.TAG_NAME, "a")
            for link in all_links:
                try:
                    if link.is_displayed():
                        href = (link.get_attribute("href") or "").lower()
                        text = link.text.lower()

                        if f"/{lang_code}/" in href or lang_code in text:
                            print(f"   🔗 Encontrado enlace: {text} -> {href}")
                            link.click()
                            time.sleep(3)

                            if self.verify_language_change(language):
                                print("✅ Idioma cambiado exitosamente por enlace")
                                return True
                except Exception:
                    continue

            # ESTRATEGIA 3: Buscar botones
            print("🔍 Estrategia 3: Buscando botones...")
            all_buttons = self.driver.find_elements(By.TAG_NAME, "button")
            for button in all_buttons:
                try:
                    if button.is_displayed():
                        button_text = button.text.lower()
                        if lang_code in button_text or language.lower() in button_text:
                            print(f"   🔘 Encontrado botón: {button_text}")
                            button.click()
                            time.sleep(3)

                            if self.verify_language_change(language):
                                print("✅ Idioma cambiado exitosamente por botón")
                                return True
                except Exception:
                    continue

            print(f"❌ No se pudo cambiar a {language}")
            return False

        except Exception as e:
            print(f"❌ ERROR cambiando idioma: {e}")
            return False

    @allure.step("Change language by URL: {language}")
    def change_language_by_url(self, language):
        """
        Cambiar idioma navegando a la URL correspondiente
        Método mejorado y robusto
        """
        try:
            language_urls = {
                "spanish": "https://nuxqa4.avtest.ink/es/",
                "english": "https://nuxqa4.avtest.ink/en/",
                "french": "https://nuxqa4.avtest.ink/fr/",
                "portuguese": "https://nuxqa4.avtest.ink/pt/",
            }

            target_url = language_urls.get(language.lower())
            if not target_url:
                print(f"❌ Idioma no soportado: {language}")
                return False

            print(f"🌐 Navegando a: {target_url}")

            # Navegar
            try:
                self.driver.get(target_url)
            except Exception as e:
                print(f"⚠️ Warning durante navegación: {e}")

            # Esperar
            time.sleep(2)

            # Verificar URL
            current_url = self.driver.current_url.lower()
            print(f"   📍 URL resultante: {current_url}")

            # Códigos esperados
            language_codes = {
                "spanish": ["/es/", "/es", "nuxqa4.avtest.ink/es"],
                "english": ["/en/", "/en", "nuxqa4.avtest.ink/en"],
                "french": ["/fr/", "/fr", "nuxqa4.avtest.ink/fr"],
                "portuguese": ["/pt/", "/pt", "nuxqa4.avtest.ink/pt"],
            }

            expected_codes = language_codes.get(language.lower(), [])
            url_correct = any(code in current_url for code in expected_codes)

            if url_correct:
                print(f"   ✅ URL correcta para {language}")
                return True
            else:
                print(f"   ❌ URL incorrecta. Esperaba: {expected_codes}")
                return False

        except Exception as e:
            print(f"❌ Error en change_language_by_url: {e}")
            return False

    @allure.step("Verify language change to {expected_language}")
    def verify_language_change(self, expected_language):
        """
        Verificar que el idioma cambió correctamente
        Compatible con ambos test_language.py y test_caso_4.py
        """
        try:
            time.sleep(2)

            # URL actual
            current_url = self.driver.current_url.lower()
            print(f"\n🔍 Verificando idioma: {expected_language}")
            print(f"   📍 URL actual: {current_url}")

            # Códigos esperados por idioma
            expected_codes = {
                "spanish": ["/es/", "/es", "español"],
                "english": ["/en/", "/en", "english"],
                "french": ["/fr/", "/fr", "français"],
                "portuguese": ["/pt/", "/pt", "português"],
            }

            codes = expected_codes.get(expected_language.lower(), [])
            url_match = any(code in current_url for code in codes)

            # Verificar contenido
            page_source = self.driver.page_source.lower()
            content_indicators = {
                "spanish": ["español", "origen", "destino", "buscar"],
                "english": ["english", "origin", "destination", "search"],
                "french": ["français", "origine", "destination", "rechercher"],
                "portuguese": ["português", "origem", "destino", "buscar"],
            }

            indicators = content_indicators.get(expected_language.lower(), [])
            content_match = any(indicator in page_source for indicator in indicators)

            # Resultado
            success = url_match or content_match

            if success:
                print(f"   ✅ Idioma verificado: {expected_language}")
                print(f"      URL match: {url_match}, Content match: {content_match}")
            else:
                print("   ❌ Verificación falló")

            return success

        except Exception as e:
            print(f"❌ Error verificando idioma: {e}")
            return False

    @allure.step("Verify language changed to {expected_language}")
    def verify_language_changed(self, expected_language):
        """
        Alias para verify_language_change - compatibilidad con test_language.py
        """
        return self.verify_language_change(expected_language)

    @allure.step("Get current language")
    def get_current_language(self):
        """
        Obtener el idioma actual basado en URL y contenido
        """
        try:
            current_url = self.driver.current_url.lower()

            # Detectar por URL
            if "/es/" in current_url or "/es" in current_url:
                return "spanish"
            elif "/en/" in current_url or "/en" in current_url:
                return "english"
            elif "/fr/" in current_url or "/fr" in current_url:
                return "french"
            elif "/pt/" in current_url or "/pt" in current_url:
                return "portuguese"

            # Detectar por contenido
            page_source = self.driver.page_source.lower()

            scores = {
                "spanish": sum(
                    1
                    for word in ["español", "origen", "destino"]
                    if word in page_source
                ),
                "english": sum(
                    1
                    for word in ["english", "origin", "destination"]
                    if word in page_source
                ),
                "french": sum(
                    1
                    for word in ["français", "origine", "destination"]
                    if word in page_source
                ),
                "portuguese": sum(
                    1
                    for word in ["português", "origem", "destino"]
                    if word in page_source
                ),
            }

            max_score = max(scores.values())
            if max_score > 0:
                for lang, score in scores.items():
                    if score == max_score:
                        return lang

            return "unknown"

        except Exception as e:
            print(f"Error detectando idioma: {e}")
            return "unknown"

    # ========================================================================


# MÉTODOS DE CAMBIO DE POS - CASO 5
# ========================================================================


    @allure.step("Change POS to {pos}")
    def change_pos(self, pos):
        """
        Cambiar POS (Point of Sale / País) con múltiples estrategias
        Soporta: other, spain, chile
        """
        try:
            print(f"\n🔄 INICIANDO CAMBIO DE POS A: {pos.upper()}")

            # Mapping de POS
            pos_mapping = {
                "other": {
                    "text": ["Otros países", "Other countries", "Otros", "Other"],
                    "code": "other",
                    "url_indicators": ["/en/", "/us/", "/other/"],
                },
                "spain": {
                    "text": ["España", "Spain", "ES"],
                    "code": "es",
                    "url_indicators": ["/es/", "/spain/", "/espana/"],
                },
                "chile": {
                    "text": ["Chile", "CL"],
                    "code": "cl",
                    "url_indicators": ["/cl/", "/chile/"],
                },
                
            }

            pos_info = pos_mapping.get(pos.lower())
            if not pos_info:
                print(f"❌ POS no soportado: {pos}")
                return False

            pos_texts = pos_info["text"]
            pos_code = pos_info["code"]

            # Screenshot antes del cambio
            self.take_screenshot(f"antes_cambio_pos_{pos_code}")

            # ESTRATEGIA 1: Cambio directo por URL (más confiable para algunos POS)
            print("🔍 Estrategia 1: Intentando cambio por URL...")
            try:
                base_domain = Config.get_base_url()
                current_url = self.driver.current_url

                # Construir nueva URL
                if pos_code == "other":
                    new_url = f"{base_domain}en/"
                else:
                    new_url = f"{base_domain}{pos_code}/"

                print(f"   🌐 Navegando a: {new_url}")
                self.driver.get(new_url)
                time.sleep(3)

                if self.verify_pos_change(pos):
                    print("✅ POS cambiado exitosamente por URL")
                    self.take_screenshot(f"despues_cambio_pos_{pos_code}")
                    return True
            except Exception as e:
                print(f"   ⚠️ Cambio por URL no funcionó: {e}")

            # ESTRATEGIA 2: Buscar y hacer clic en selector de POS
            print("🔍 Estrategia 2: Buscando selector de POS en la interfaz...")

            # Selectores posibles para el botón de POS
            pos_button_selectors = [
                "//button[contains(@class, 'point-of-sale-selector_button')]",
                "//div[contains(@class, 'point-of-sale-selector_button')]//button",
                "//button[contains(@id, 'pointOfSaleSelectorId')]",
                "//div[contains(@class, 'pos-selector')]//button",
                "//*[contains(@class, 'country-dropdown')]",
                "//*[contains(@aria-label, 'country')]",
                "//*[contains(@aria-label, 'país')]",
            ]

            pos_button = None
            for selector in pos_button_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        if element.is_displayed() and element.is_enabled():
                            pos_button = element
                            print(f"   ✅ Encontrado selector POS: {selector}")
                            print(f"      Texto: '{element.text}'")
                            break
                    if pos_button:
                        break
                except Exception:
                    continue

            # Si no se encontró, buscar cualquier botón con texto de país
            if not pos_button:
                print("   🔍 Buscando botones con nombres de países...")
                all_buttons = self.driver.find_elements(By.TAG_NAME, "button")
                country_names = [
                    "Colombia",
                    "Chile",
                    "España",
                    
                ]

                for button in all_buttons:
                    try:
                        if button.is_displayed():
                            btn_text = button.text.strip()
                            if any(country in btn_text for country in country_names):
                                pos_button = button
                                print(f"   ✅ Encontrado botón de país: '{btn_text}'")
                                break
                    except Exception:
                        continue

            if not pos_button:
                print("❌ No se encontró selector de POS en la interfaz")
                return False

            # Hacer clic en el selector para abrir el dropdown
            print("🖱️ Abriendo selector de POS...")
            try:
                # Scroll al elemento
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});",
                    pos_button,
                )
                time.sleep(1)

                # Intentar clic
                try:
                    pos_button.click()
                except ElementClickInterceptedException:
                    self.driver.execute_script("arguments[0].click();", pos_button)

                time.sleep(2)
                print("   ✅ Selector abierto")

            except Exception as e:
                print(f"   ❌ Error abriendo selector: {e}")
                return False

            # Screenshot con dropdown abierto
            self.take_screenshot(f"dropdown_pos_abierto_{pos_code}")

            # ESTRATEGIA 3: Buscar y seleccionar la opción del POS
            print(f"🔍 Buscando opción para: {pos_texts}")

            pos_option = None
            for pos_text in pos_texts:
                # Selectores para las opciones
                option_selectors = [
                    f"//div[contains(@class, 'point-of-sale-selector-custom')]//*[contains(text(), '{pos_text}')]",
                    f"//div[contains(@class, 'country')]//*[contains(text(), '{pos_text}')]",
                    f"//li[contains(text(), '{pos_text}')]",
                    f"//a[contains(text(), '{pos_text}')]",
                    f"//button[contains(text(), '{pos_text}')]",
                    f"//span[contains(text(), '{pos_text}')]",
                    f"//label[contains(text(), '{pos_text}')]",
                    f"//*[contains(@class, 'dropdown')]//*[contains(text(), '{pos_text}')]",
                    f"//*[@role='option' and contains(text(), '{pos_text}')]",
                ]

                for selector in option_selectors:
                    try:
                        elements = self.driver.find_elements(By.XPATH, selector)
                        for element in elements:
                            if element.is_displayed() and element.is_enabled():
                                pos_option = element
                                print(
                                    f"   ✅ Encontrada opción: '{pos_text}' usando {selector}"
                                )
                                break
                        if pos_option:
                            break
                    except Exception:
                        continue

                if pos_option:
                    break

            if not pos_option:
                print(f"❌ No se encontró opción para: {pos_texts}")

                # Debug: mostrar opciones disponibles
                print("🔍 Opciones disponibles en el dropdown:")
                try:
                    all_options = self.driver.find_elements(
                        By.XPATH,
                        "//div[contains(@class, 'dropdown')]//li | "
                        "//div[contains(@class, 'point-of-sale')]//li | "
                        "//ul//li | "
                        "//*[@role='option']",
                    )

                    for i, option in enumerate(all_options[:10], 1):  # Mostrar máximo 10
                        if option.is_displayed():
                            print(f"   {i}. {option.text.strip()}")
                except Exception:
                    pass

                # Cerrar dropdown
                try:
                    pos_button.click()
                    time.sleep(1)
                except Exception:
                    pass

                return False

            # Hacer clic en la opción seleccionada
            print(f"🖱️ Seleccionando: {pos_option.text}")

            try:
                # Scroll a la opción
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});",
                    pos_option,
                )
                time.sleep(1)

                # Intentar diferentes métodos de clic
                click_methods = [
                    ("clic normal", lambda: pos_option.click()),
                    (
                        "JavaScript clic",
                        lambda: self.driver.execute_script(
                            "arguments[0].click();", pos_option
                        ),
                    ),
                    (
                        "ActionChains",
                        lambda: ActionChains(self.driver)
                        .move_to_element(pos_option)
                        .click()
                        .perform(),
                    ),
                ]

                for method_name, click_func in click_methods:
                    try:
                        print(f"   Intentando: {method_name}")
                        click_func()
                        time.sleep(3)

                        # Verificar si funcionó
                        if self.verify_pos_change(pos):
                            print(f"✅ POS cambiado exitosamente a: {pos.upper()}")
                            self.take_screenshot(f"despues_cambio_pos_{pos_code}_exitoso")
                            return True
                        else:
                            print(
                                f"   ⚠️ Clic ejecutado pero no verificado con {method_name}"
                            )
                    except Exception as e:
                        print(f"   ⚠️ Error con {method_name}: {e}")
                        continue

                print("❌ No se pudo completar el cambio de POS")
                return False

            except Exception as e:
                print(f"❌ Error en selección de opción: {e}")
                return False

        except Exception as e:
            print(f"❌ ERROR CRÍTICO en change_pos: {e}")
            self.take_screenshot(f"error_critico_pos_{pos}")
            import traceback

            traceback.print_exc()
            return False


    @allure.step("Verify POS change to {expected_pos}")
    def verify_pos_change(self, expected_pos):
        """
        Verificar que el POS cambió correctamente
        Usa múltiples métodos de verificación
        """
        try:
            time.sleep(2)

            print(f"\n🔍 Verificando cambio de POS a: {expected_pos.upper()}")

            # Indicadores por POS
            pos_indicators = {
                "other": {
                    "url": ["/en/", "/us/", "/other/", "nuxqa4.avtest.ink/en"],
                    "content": ["english", "other countries", "select country"],
                },
                "spain": {
                    "url": ["/es/", "/spain/", "/espana/", "nuxqa4.avtest.ink/es"],
                    "content": ["españa", "spain", "español"],
                },
                "chile": {
                    "url": ["/cl/", "/chile/", "nuxqa4.avtest.ink/cl"],
                    "content": ["chile", "chileno"],
                },
                
            }

            indicators = pos_indicators.get(expected_pos.lower())
            if not indicators:
                print(f"❌ POS no reconocido: {expected_pos}")
                return False

            # Verificación 1: URL
            current_url = self.driver.current_url.lower()
            url_match = any(indicator in current_url for indicator in indicators["url"])
            print(f"   📍 URL actual: {current_url}")
            print(f"   {'✅' if url_match else '❌'} Verificación por URL: {url_match}")

            # Verificación 2: Contenido de página
            page_source = self.driver.page_source.lower()
            content_match = any(
                indicator in page_source for indicator in indicators["content"]
            )
            print(
                f"   {'✅' if content_match else '❌'} Verificación por contenido: {content_match}"
            )

            # Verificación 3: Elementos visibles
            element_match = False
            try:
                pos_elements = self.driver.find_elements(
                    By.XPATH,
                    "//*[contains(@class, 'country')] | "
                    "//*[contains(@class, 'point-of-sale')] | "
                    "//*[contains(@class, 'pos-selector')]",
                )

                for element in pos_elements:
                    if element.is_displayed():
                        element_text = element.text.lower()
                        if any(
                            indicator in element_text for indicator in indicators["content"]
                        ):
                            element_match = True
                            print(
                                f"   ✅ Verificación por elemento: texto encontrado '{element_text[:50]}'"
                            )
                            break
            except Exception as e:
                print(f"   ⚠️ Error verificando elementos: {e}")

            # Resultado final
            success = url_match or content_match or element_match

            if success:
                print(f"   ✅ VERIFICACIÓN EXITOSA para {expected_pos}")
            else:
                print(f"   ❌ VERIFICACIÓN FALLÓ para {expected_pos}")
                print(f"      URL match: {url_match}")
                print(f"      Content match: {content_match}")
                print(f"      Element match: {element_match}")

            return success

        except Exception as e:
            print(f"❌ Error en verify_pos_change: {e}")
            return False


    @allure.step("Get current POS")
    def get_current_pos(self):
        """
        Obtener el POS actual detectando desde URL y contenido
        """
        try:
            current_url = self.driver.current_url.lower()

            # Detección por URL
            pos_patterns = {
                "chile": ["/cl/", "/chile/"],
                "spain": ["/es/", "/spain/", "/espana/"],
                "colombia": ["/co/", "/colombia/"],
                "mexico": ["/mx/", "/mexico/"],
                "peru": ["/pe/", "/peru/"],
                "argentina": ["/ar/", "/argentina/"],
                "other": ["/en/", "/us/", "/other/"],
            }

            for pos, patterns in pos_patterns.items():
                if any(pattern in current_url for pattern in patterns):
                    return pos

            # Detección por contenido si URL no es clara
            try:
                page_source = self.driver.page_source.lower()

                content_patterns = {
                    "chile": ["chile", "chileno"],
                    "spain": ["españa", "español", "spain"],
                    "colombia": ["colombia", "colombiano"],
                    "mexico": ["méxico", "mexico", "mexicano"],
                    "peru": ["perú", "peru", "peruano"],
                    "argentina": ["argentina", "argentino"],
                    "other": ["other countries", "otros países"],
                }

                scores = {}
                for pos, patterns in content_patterns.items():
                    scores[pos] = sum(1 for pattern in patterns if pattern in page_source)

                max_score = max(scores.values())
                if max_score > 0:
                    for pos, score in scores.items():
                        if score == max_score:
                            return pos
            except Exception:
                pass

            return "unknown"

        except Exception as e:
            print(f"Error detectando POS actual: {e}")
            return "unknown"

    # ========================================================================
    # UTILIDADES
    # ========================================================================

    @allure.step("Take screenshot: {screenshot_name}")
    def take_screenshot(self, screenshot_name):
        """Tomar screenshot"""
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

    # ========================================================================
    # NAVEGACIÓN POR EL HEADER - CASO 6
    # ========================================================================       
    
    @allure.step("Click header link: {link_text}")
    def click_header_link(self, link_text):
        """Hacer clic en un enlace del header/navbar por texto - VERSIÓN MEJORADA"""
        try:
            print(f"🔍 Buscando enlace del header: '{link_text}'")
            
            # Estrategia 1: Buscar en elementos de navegación específicos
            nav_selectors = [
                "//nav",
                "//header",
                "//div[contains(@class, 'navbar')]",
                "//div[contains(@class, 'navigation')]",
                "//div[contains(@class, 'header')]",
                "//div[contains(@class, 'menu')]",
                "//ul[contains(@class, 'nav')]",
                "//ul[contains(@class, 'menu')]"
            ]
            
            # Primero buscar en áreas específicas del header/nav
            for nav_selector in nav_selectors:
                try:
                    # Buscar enlaces dentro del área de navegación
                    link_selector = f"{nav_selector}//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{link_text.lower()}')]"
                    elements = self.driver.find_elements(By.XPATH, link_selector)
                    
                    for element in elements:
                        if element.is_displayed() and element.is_enabled():
                            print(f"✅ Encontrado enlace en {nav_selector}: '{element.text}'")
                            return self._safe_click_element(element, link_text)
                            
                except Exception as e:
                    continue
            
            # Estrategia 2: Buscar por texto normalizado (case-insensitive)
            normalized_selectors = [
                f"//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{link_text.lower()}')]",
                f"//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{link_text.lower()}')]",
                f"//span[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{link_text.lower()}')]",
                f"//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{link_text.lower()}')]"
            ]
            
            for selector in normalized_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        # Verificar que esté en el área superior de la página (header)
                        location = element.location
                        if location['y'] < 300:  # Elementos del header suelen estar en la parte superior
                            if element.is_displayed() and element.is_enabled():
                                print(f"✅ Encontrado enlace en posición superior: '{element.text}'")
                                return self._safe_click_element(element, link_text)
                except Exception as e:
                    continue
            
            # Estrategia 3: Buscar por atributos comunes de enlaces de navegación
            common_link_selectors = [
                "//a[@href]",
                "//button[@type='button']",
                "//*[@role='button']",
                "//*[@role='link']"
            ]
            
            for selector in common_link_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        if element.is_displayed() and element.is_enabled():
                            element_text = element.text.strip().lower()
                            if link_text.lower() in element_text:
                                print(f"✅ Encontrado por texto parcial: '{element.text}'")
                                return self._safe_click_element(element, link_text)
                except Exception as e:
                    continue
            
            print(f"❌ No se encontró el enlace: '{link_text}'")
            return False
            
        except Exception as e:
            print(f"❌ Error buscando enlace '{link_text}': {e}")
            return False

    def _safe_click_element(self, element, element_name):
        """Método auxiliar para hacer clic seguro en elementos"""
        try:
            # Scroll al elemento
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});",
                element
            )
            time.sleep(1)
            
            # Intentar diferentes métodos de clic
            click_methods = [
                ("clic normal", lambda: element.click()),
                ("JavaScript", lambda: self.driver.execute_script("arguments[0].click();", element)),
                ("ActionChains", lambda: ActionChains(self.driver).move_to_element(element).click().perform())
            ]
            
            for method_name, click_func in click_methods:
                try:
                    print(f"   Intentando clic con: {method_name}")
                    click_func()
                    time.sleep(1)
                    return True
                except ElementClickInterceptedException:
                    print(f"   ⚠️ Elemento interceptado con {method_name}")
                    continue
                except Exception as e:
                    print(f"   ⚠️ Error con {method_name}: {e}")
                    continue
            
            print(f"❌ No se pudo hacer clic en: '{element_name}'")
            return False
            
        except Exception as e:
            print(f"❌ Error en clic seguro: {e}")
            return False

    @allure.step("Verify page loaded successfully")
    def verify_page_loaded_successfully(self):
        """
        Verificar que la página cargó correctamente - VERSIÓN MEJORADA
        """
        try:
            current_url = self.driver.current_url.lower()
            current_title = self.driver.title.lower()
            
            # Verificar errores comunes
            error_indicators = [
                "error", "notfound", "404", "500", "unavailable", 
                "page not found", "not found", "error page"
            ]
            
            if any(indicator in current_url or indicator in current_title for indicator in error_indicators):
                print("❌ Página de error detectada")
                return False
            
            # Verificar que la página tiene contenido razonable
            page_source = self.driver.page_source
            if len(page_source) < 500:
                print("❌ Página con muy poco contenido")
                return False
            
            # Verificar que no es la página de inicio por defecto
            if "nginx" in page_source.lower() or "welcome to nginx" in current_title:
                print("❌ Página por defecto del servidor")
                return False
            
            print("✅ Página cargada correctamente")
            return True
            
        except Exception as e:
            print(f"❌ Error verificando carga de página: {e}")
            return False

    def wait_for_page_load(self, timeout=10):
        """Esperar a que la página cargue completamente"""
        try:
            from selenium.webdriver.support.ui import WebDriverWait
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            print("✅ Página cargada completamente")
            return True
        except Exception as e:
            print(f"⚠️ Timeout esperando carga de página: {e}")
            return False

    def verify_url_contains(self, text):
        """Verificar si la URL contiene cierto texto"""
        try:
            return text.lower() in self.driver.current_url.lower()
        except:
            return False
        """Verificar si la URL contiene cierto texto"""

    #Enlace temporal para revisar los enlaces disponibles     
    
    def debug_find_header_links(self):
        """Método temporal para debug - mostrar todos los enlaces del header"""
        print("\n🔍 DEBUG: Buscando todos los enlaces del header...")
        
        # Buscar en áreas específicas del header
        header_selectors = [
            "//header",
            "//nav", 
            "//div[contains(@class, 'header')]",
            "//div[contains(@class, 'navbar')]",
            "//div[contains(@class, 'navigation')]",
            "//div[contains(@class, 'menu')]"
        ]
        
        all_links_found = []
        
        for selector in header_selectors:
            try:
                elements = self.driver.find_elements(By.XPATH, f"{selector}//a | {selector}//button")
                for element in elements:
                    if element.is_displayed():
                        text = element.text.strip()
                        if text and len(text) > 0:
                            link_info = {
                                "text": text,
                                "tag": element.tag_name,
                                "href": element.get_attribute('href') if element.tag_name == 'a' else None,
                                "class": element.get_attribute('class'),
                                "location": element.location
                            }
                            if link_info not in all_links_found:
                                all_links_found.append(link_info)
            except Exception as e:
                continue
        
        print(f"📋 ENLACES ENCONTRADOS EN EL HEADER ({len(all_links_found)}):")
        for i, link in enumerate(all_links_found, 1):
            print(f"   {i}. '{link['text']}'")
            print(f"      Tag: {link['tag']}, Href: {link['href']}")
            print(f"      Class: {link['class']}")
        
        return all_links_found
    
    def find_dropdown_options(self, menu_name):
        """Buscar opciones en un menú desplegable abierto"""
        try:
            # Selectores para opciones de menú desplegable
            option_selectors = [
                "//div[contains(@class, 'dropdown')]//a",
                "//div[contains(@class, 'dropdown')]//button", 
                "//div[contains(@class, 'menu')]//a",
                "//ul[contains(@class, 'dropdown')]//a",
                "//div[contains(@class, 'main-header_nav-primary_item')]//a",
                "//*[@role='menu']//*[@role='menuitem']"
            ]
            
            options_found = []
            for selector in option_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        if element.is_displayed():
                            text = element.text.strip()
                            if text and text not in options_found:
                                options_found.append(text)
                except:
                    continue
            
            return options_found if options_found else None
            
        except Exception as e:
            print(f"❌ Error buscando opciones del menú: {e}")
            return None

    def click_first_dropdown_option(self, menu_name):
        """Hacer clic en la primera opción de un menú desplegable"""
        try:
            # Buscar la primera opción clickeable en el menú
            option_selectors = [
                "//div[contains(@class, 'dropdown')]//a[1]",
                "//div[contains(@class, 'dropdown')]//button[1]",
                "//div[contains(@class, 'menu')]//a[1]",
                "//ul[contains(@class, 'dropdown')]//a[1]"
            ]
            
            for selector in option_selectors:
                try:
                    element = self.driver.find_element(By.XPATH, selector)
                    if element.is_displayed() and element.is_enabled():
                        print(f"🖱️ Haciendo clic en primera opción: '{element.text}'")
                        element.click()
                        return True
                except:
                    continue
            
            return False
            
        except Exception as e:
            print(f"❌ Error haciendo clic en opción del menú: {e}")
            return False


    def click_footer_link(self, link_name):
        """
        Hacer clic en un enlace específico del footer - Versión MEJORADA
        
        Args:
            link_name (str): Nombre del enlace a hacer clic
            
        Returns:
            bool: True si se pudo hacer clic, False si no se encontró
        """
        try:
            print(f"   🔍 Buscando enlace footer: '{link_name}'")
            
            # Mapeo de nombres alternativos para los enlaces
            link_aliases = {
                "Lifemiles program": ["Lifemiles", "LifeMiles", "Life Miles", "Programa Lifemiles"],
                "Contact us": ["Contact", "Contacto", "Contact Us"],
                "Sustainability": ["Sostenibilidad", "Sostenible"],
                "Legal Information": ["Legal", "Información Legal", "Términos"]
            }
            
            # Obtener todos los alias para este enlace
            aliases = link_aliases.get(link_name, []) + [link_name]
            
            # Diferentes estrategias para encontrar enlaces del footer
            strategies = []
            
            for alias in aliases:
                strategies.extend([
                    # Estrategia 1: Buscar por texto exacto en footer
                    f"//footer//a[normalize-space()='{alias}']",
                    
                    # Estrategia 2: Buscar por texto que contenga (case insensitive)
                    f"//footer//a[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{alias.lower()}')]",
                    
                    # Estrategia 3: Buscar en cualquier parte de la página pero en sección footer
                    f"//a[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{alias.lower()}') and ancestor::footer]",
                    
                    # Estrategia 4: Buscar por texto parcial
                    f"//footer//a[contains(., '{alias.split()[0]}')]" if ' ' in alias else None,
                ])
            
            # Estrategias adicionales
            strategies.extend([
                # Estrategia 5: Buscar por clase común de footer
                "//footer//a[contains(@class, 'footer') or contains(@class, 'link')]",
                
                # Estrategia 6: Buscar cualquier enlace en el footer
                "//footer//a",
                
                # Estrategia 7: Buscar en secciones específicas del footer
                "//div[contains(@class, 'footer')]//a",
                "//section[contains(@class, 'footer')]//a"
            ])
            
            # Filtrar estrategias None y duplicados
            strategies = list(set([s for s in strategies if s]))
            
            print(f"   🔍 Probando {len(strategies)} estrategias para '{link_name}'")
            
            for i, selector in enumerate(strategies, 1):
                try:
                    print(f"   🔍 Intentando estrategia {i}: {selector}")
                    elements = self.driver.find_elements(By.XPATH, selector)
                    
                    if elements:
                        for element in elements:
                            if element.is_displayed() and element.is_enabled():
                                # Obtener texto del enlace para verificación
                                link_text = element.text.strip()
                                print(f"   📝 Enlace encontrado: '{link_text}'")
                                
                                # Verificar si el texto coincide con lo que buscamos
                                if any(alias.lower() in link_text.lower() for alias in aliases):
                                    print(f"   ✅ Coincidencia encontrada: '{link_text}'")
                                    
                                    # Hacer scroll al elemento
                                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                                    time.sleep(1)
                                    
                                    # Hacer clic
                                    element.click()
                                    print(f"   ✅ Clic exitoso en: '{link_name}'")
                                    return True
                                else:
                                    print(f"   ⚠️ Enlace encontrado pero no coincide: '{link_text}'")
                    else:
                        print(f"   ⚠️ No se encontraron elementos con selector: {selector}")
                        
                except Exception as e:
                    print(f"   ⚠️ Estrategia {i} falló: {str(e)}")
                    continue
            
            print(f"   ❌ No se pudo encontrar el enlace: '{link_name}' después de {len(strategies)} estrategias")
            return False
            
        except Exception as e:
            print(f"   💥 Error crítico al buscar '{link_name}': {str(e)}")
            return False
    
    @allure.step("Get page language")
    def get_page_language(self):
     """Obtener idioma de la página - VERSIÓN COMPATIBLE CON TEST_CASO_7"""
     try:
            # Intentar obtener del atributo lang del HTML
            html_lang = self.driver.execute_script("return document.documentElement.lang")
            if html_lang:
                return html_lang
            
            # Intentar obtener de la URL
            current_url = self.driver.current_url.lower()
            if '/es/' in current_url:
                return 'spanish'  # Cambiado de 'es' a 'spanish' para compatibilidad
            elif '/en/' in current_url:
                return 'english'  # Cambiado de 'en' a 'english' para compatibilidad
            elif '/fr/' in current_url:
                return 'french'   # Cambiado de 'fr' a 'french' para compatibilidad
            elif '/pt/' in current_url:
                return 'portuguese'  # Cambiado de 'pt' a 'portuguese' para compatibilidad
            else:
                # Si no se detecta por URL, intentar detectar por contenido
                page_source = self.driver.page_source.lower()
                if any(word in page_source for word in ['english', 'origin', 'destination']):
                    return 'english'
                elif any(word in page_source for word in ['español', 'origen', 'destino']):
                    return 'spanish'
                elif any(word in page_source for word in ['français', 'origine']):
                    return 'french'
                elif any(word in page_source for word in ['português', 'origem']):
                    return 'portuguese'
                else:
                    return 'unknown'
                
     except Exception as e:
            print(f"⚠️ Error obteniendo idioma: {e}")
            return 'unknown'

    @allure.step("Wait for page to load")
    def wait_for_page_to_load(self, timeout=30):
        """Esperar a que la página cargue completamente - VERSIÓN COMPATIBLE"""
        try:
            from selenium.webdriver.support.ui import WebDriverWait
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            print("✅ Página cargada completamente")
            return True
        except Exception as e:
            print(f"⚠️ Timeout esperando carga de página: {e}")
            return False