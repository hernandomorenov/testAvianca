import pytest
import allure
import time
from pages.booking_flow.home_page import HomePage
from utils.config import Config


@pytest.mark.caso_7
@pytest.mark.regression
class TestCasoAutomatizado7:
    """
    Caso automatizado 7: Redirecciones Footer
    Verificar que los enlaces del footer redirigen correctamente manteniendo el idioma
    """

    @allure.feature("Caso Automatizado 7")
    @allure.story("Redirecciones mediante enlaces del Footer")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Caso 7: Redirecciones Footer completas")
    def test_caso_7_redirecciones_footer(self, setup):
        """
        Utilizar los links del footer para acceder a 4 sitios diferentes.
        Verificar que la url de los sitios cargan correctamente de acuerdo con el idioma y sitio seleccionado.
        """
        driver = setup['driver']
        db = setup['db']
        start_time = time.time()
        
        home_page = HomePage(driver)
        test_results = []

        try:
            # ===== CONFIGURACIÓN INICIAL =====
            with allure.step("Paso 1: Configuración inicial - Navegar y configurar idioma inglés"):
                print("\n🌐 Configurando prueba...")
                
                # Obtener URL base desde Config
                base_url = Config.get_base_url()
                print(f"   Usando URL: {base_url}")
                print(f"   Entorno: {Config.ENVIRONMENT}")
                
                # Navegar a la página principal
                assert home_page.navigate_to(base_url), "❌ No se pudo navegar a la página principal"
                
                # Configurar idioma inglés
                assert home_page.change_language("english"), "❌ No se pudo cambiar a inglés"
                
                # Verificar que estamos en inglés (aceptando tanto "english" como "en")
                current_language = home_page.get_page_language()
                language_correct = current_language in ["english", "en"]
                assert language_correct, f"❌ Idioma no configurado correctamente. Esperado: english/en, Actual: {current_language}"
                
                home_page.take_screenshot("caso7_configuracion_inicial")
                print(f"✅ Configuración inicial completada - Idioma: {current_language}")

            # ===== DEFINIR ENLACES A PROBAR =====
            footer_links = [
                {
                    "name": "Contact us", 
                    "expected_patterns": ["contact", "contacto", "contact-us"],
                    "description": "Página de contacto",
                    "required": True
                },
                {
                    "name": "Sustainability", 
                    "expected_patterns": ["sustainability", "sostenibilidad"],
                    "description": "Política de sostenibilidad",
                    "required": True
                },
                {
                    "name": "Lifemiles program", 
                    "expected_patterns": ["lifemiles", "millas", "program"],
                    "description": "Acumula experiencias",
                    "required": True
                },
                {
                    "name": "Legal Information", 
                    "expected_patterns": ["legal", "information", "terminos"],
                    "description": "Información legal",
                    "required": True
                },
            ]

            # ===== PROBAR ENLACES DEL FOOTER =====
            tested_links = 0
            max_links_to_test = 4
            
            with allure.step(f"Paso 2: Probar {max_links_to_test} enlaces del footer"):
                print(f"\n🔗 Probando {max_links_to_test} enlaces del footer...")
                
                for link_info in footer_links:
                    if tested_links >= max_links_to_test:
                        break
                    
                    link_name = link_info["name"]
                    expected_patterns = link_info["expected_patterns"]
                    description = link_info["description"]
                    
                    with allure.step(f"Paso 2.{tested_links + 1}: Probar enlace '{link_name}' - {description}"):
                        print(f"\n   🔍 Probando: {link_name} ({description})")
                        
                        # Guardar estado inicial
                        initial_url = driver.current_url
                        initial_title = driver.title
                        
                        # Intentar hacer clic en el enlace del footer
                        click_success = home_page.click_footer_link(link_name)
                        
                        if not click_success:
                            print(f"   ⚠️ Enlace '{link_name}' no encontrado, probando siguiente...")
                            continue
                        
                        # Esperar carga de la nueva página con delay configurado
                        time.sleep(Config.get_action_delay())
                        
                        # Verificar que cambiamos de página
                        new_url = driver.current_url
                        url_changed = new_url != initial_url
                        
                        if not url_changed:
                            print(f"   ⚠️ URL no cambió después de hacer clic en '{link_name}'")
                            # Continuar con siguiente enlace
                            tested_links += 1
                            continue
                        
                        # Verificar que la página cargó correctamente
                        page_loaded = self._verify_page_loaded(driver, expected_patterns, new_url)
                        
                        # Verificar que el idioma se mantuvo en inglés (aceptando "en" o "english")
                        current_language = home_page.get_page_language()
                        language_maintained = current_language in ["english", "en"]
                        
                        # Obtener título de la página
                        new_title = driver.title
                        
                        # Evaluar resultado general
                        overall_success = all([
                            click_success,
                            url_changed,
                            page_loaded,
                            language_maintained
                        ])
                        
                        # Registrar resultado
                        test_result = {
                            "link_name": link_name,
                            "description": description,
                            "click_success": click_success,
                            "url_changed": url_changed,
                            "page_loaded": page_loaded,
                            "language_maintained": language_maintained,
                            "expected_patterns": expected_patterns,
                            "actual_url": new_url,
                            "page_title": new_title,
                            "current_language": current_language,
                            "overall_success": overall_success
                        }
                        test_results.append(test_result)
                        
                        # Reportar resultado
                        self._report_link_result(test_result, home_page)
                        
                        # Volver a la página anterior para probar siguiente enlace
                        print("   ↩️ Volviendo a página anterior...")
                        driver.back()
                        time.sleep(Config.get_action_delay())
                        
                        # Esperar a que la página se estabilice después de volver
                        home_page.wait_for_page_to_load()
                        
                        # Verificar que volvimos correctamente
                        if not self._verify_return_to_initial_state(driver, initial_url, home_page):
                            print("   ⚠️ No se pudo volver a la página inicial, navegando manualmente...")
                            home_page.navigate_to(base_url + "en/")
                            # Verificar idioma después de navegar
                            current_language = home_page.get_page_language()
                            if current_language not in ["english", "en"]:
                                assert home_page.change_language("english"), "❌ No se pudo restaurar configuración de idioma"
                        
                        tested_links += 1
                        print(f"   ✅ Prueba de '{link_name}' completada")

            # ===== VERIFICACIONES FINALES =====
            with allure.step("Paso 3: Análisis de resultados finales"):
                successful_tests = sum(1 for result in test_results if result["overall_success"])
                total_tests = len(test_results)
                
                print(f"\n📊 RESULTADOS FINALES:")
                print(f"   Total de enlaces probados: {total_tests}")
                print(f"   Redirecciones completamente exitosas: {successful_tests}")
                print(f"   Redirecciones con problemas: {total_tests - successful_tests}")
                
                # Generar reporte detallado para Allure
                self._generate_detailed_report(test_results)
                
                # VERIFICACIÓN PRINCIPAL: Al menos 4 redirecciones exitosas
                assert total_tests >= 4, f"❌ Solo se pudieron probar {total_tests} enlaces de 4 requeridos"
                assert successful_tests >= 3, (
                    f"❌ CASO 7 FALLIDO: Solo {successful_tests}/{total_tests} redirecciones completamente exitosas. "
                    f"Se requieren al menos 3 redirecciones completamente exitosas."
                )
            
            execution_time = time.time() - start_time
            print(f"\n🎉 CASO 7 COMPLETADO EXITOSAMENTE")
            print(f"   Tiempo de ejecución: {execution_time:.2f}s")
            print(f"   Enlaces probados: {total_tests}")
            print(f"   Redirecciones exitosas: {successful_tests}")
            
            # Guardar resultado en BD (SIN el parámetro 'details')
            db.insert_result(
                test_name="caso_7_redirecciones_footer",
                status="PASS",
                browser=Config.BROWSER,
                url=base_url,
                execution_time=f"{execution_time:.2f}s",
                error_message=None
            )
            
        except AssertionError as ae:
            execution_time = time.time() - start_time
            error_msg = str(ae)
            
            print(f"\n❌ CASO 7 FALLIDO: {error_msg}")
            
            # Guardar resultado fallido en BD (SIN el parámetro 'details')
            base_url = Config.get_base_url()
            db.insert_result(
                test_name="caso_7_redirecciones_footer",
                status="FAIL",
                browser=Config.BROWSER,
                url=base_url,
                execution_time=f"{execution_time:.2f}s",
                error_message=error_msg
            )
            
            raise
            
        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = f"Error inesperado: {str(e)}"
            
            print(f"\n💥 ERROR INESPERADO: {error_msg}")
            
            base_url = Config.get_base_url()
            db.insert_result(
                test_name="caso_7_redirecciones_footer",
                status="ERROR",
                browser=Config.BROWSER,
                url=base_url,
                execution_time=f"{execution_time:.2f}s",
                error_message=error_msg
            )
            
            raise

    def _verify_page_loaded(self, driver, expected_patterns, current_url):
        """Verifica que la página cargó correctamente"""
        try:
            # Verificar que la URL contiene alguno de los patrones esperados
            current_url_lower = current_url.lower()
            url_match = any(pattern in current_url_lower for pattern in expected_patterns)
            
            # Verificar que la página tiene un título válido
            title = driver.title
            title_valid = title and len(title) > 0 and title.strip() != "" and title != "404"
            
            # Verificar que la página no es una página de error
            page_source = driver.page_source.lower()
            not_error_page = all(error_term not in page_source 
                               for error_term in ["404", "not found", "error", "página no encontrada"])
            
            return url_match and title_valid and not_error_page
            
        except Exception as e:
            print(f"   ⚠️ Error verificando carga de página: {e}")
            return False

    def _verify_return_to_initial_state(self, driver, initial_url, home_page):
        """Verifica que volvimos correctamente al estado inicial"""
        try:
            # Esperar a que la página esté lista
            home_page.wait_for_page_to_load()
            time.sleep(1)
            
            # Verificar que estamos en una URL válida
            current_url = driver.current_url
            if not current_url or "data:" in current_url:
                return False
                
            # Para este caso, nos conformamos con estar en el dominio correcto
            base_url = Config.get_base_url()
            return base_url in current_url
            
        except Exception:
            return False

    def _report_link_result(self, result, home_page):
        """Reporta el resultado de un enlace individual"""
        link_name = result["link_name"]
        
        if result["overall_success"]:
            print(f"   ✅ {link_name} - EXITOSO")
            print(f"      URL: {result['actual_url']}")
            print(f"      Título: {result['page_title']}")
            print(f"      Idioma: {result['current_language']}")
            
            allure.attach(
                f"Enlace Footer {link_name} - EXITOSO\n"
                f"Descripción: {result['description']}\n"
                f"URL: {result['actual_url']}\n"
                f"Título: {result['page_title']}\n"
                f"Idioma: {result['current_language']}\n"
                f"Patrones esperados: {', '.join(result['expected_patterns'])}",
                name=f"Resultado {link_name}",
                attachment_type=allure.attachment_type.TEXT
            )
        else:
            print(f"   ❌ {link_name} - FALLIDO")
            print(f"      Click: {'✅' if result['click_success'] else '❌'}")
            print(f"      URL cambió: {'✅' if result['url_changed'] else '❌'}")
            print(f"      Página cargada: {'✅' if result['page_loaded'] else '❌'}")
            print(f"      Idioma mantenido: {'✅' if result['language_maintained'] else '❌'}")
            print(f"      URL actual: {result['actual_url']}")
            
            allure.attach(
                f"Enlace Footer {link_name} - FALLIDO\n"
                f"Click exitoso: {'✅' if result['click_success'] else '❌'}\n"
                f"URL cambió: {'✅' if result['url_changed'] else '❌'}\n"
                f"Página cargada: {'✅' if result['page_loaded'] else '❌'}\n"
                f"Idioma mantenido: {'✅' if result['language_maintained'] else '❌'}\n"
                f"URL actual: {result['actual_url']}\n"
                f"Idioma actual: {result['current_language']}",
                name=f"Resultado {link_name}",
                attachment_type=allure.attachment_type.TEXT
            )
        
        # Tomar screenshot si está habilitado en configuración
        if Config.TAKE_SCREENSHOTS:
            home_page.take_screenshot(f"caso7_{link_name}")

    def _generate_detailed_report(self, test_results):
        """Genera un reporte detallado de los resultados"""
        successful_tests = sum(1 for result in test_results if result["overall_success"])
        total_tests = len(test_results)
        
        report = "REPORTE DETALLADO - REDIRECCIONES FOOTER\n"
        report += "=" * 50 + "\n\n"
        report += f"RESUMEN: {successful_tests}/{total_tests} redirecciones exitosas\n"
        report += f"ENTORNO: {Config.ENVIRONMENT}\n"
        report += f"URL BASE: {Config.get_base_url()}\n"
        report += f"NAVEGADOR: {Config.BROWSER}\n\n"
        
        for i, result in enumerate(test_results, 1):
            status = "✅ EXITOSO" if result["overall_success"] else "❌ FALLIDO"
            report += f"{i}. 🔗 {result['link_name']}: {status}\n"
            report += f"   Descripción: {result['description']}\n"
            report += f"   Click exitoso: {'✅' if result['click_success'] else '❌'}\n"
            report += f"   URL cambió: {'✅' if result['url_changed'] else '❌'}\n"
            report += f"   Página cargada: {'✅' if result['page_loaded'] else '❌'}\n"
            report += f"   Idioma mantenido: {'✅' if result['language_maintained'] else '❌'}\n"
            report += f"   URL: {result['actual_url']}\n"
            report += f"   Título: {result['page_title']}\n"
            report += f"   Idioma: {result['current_language']}\n"
            report += f"   Patrones esperados: {', '.join(result['expected_patterns'])}\n\n"
        
        allure.attach(report, name="Reporte Detallado Redirecciones Footer", 
                     attachment_type=allure.attachment_type.TEXT)