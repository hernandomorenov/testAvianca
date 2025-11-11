import pytest
import allure
import time
import json
from pages.booking_flow.home_page import HomePage
from pages.booking_flow.select_flight_page import SelectFlightPage
from utils.config import Config

@pytest.mark.caso_3
@pytest.mark.regression
class TestCasoAutomatizado3:
    """Caso automatizado 3: Realizar Login en UAT3"""
    
    @allure.feature("Caso Automatizado 3")
    @allure.story("Login y configuración de búsqueda")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Caso 3: Login y validación de sesión")
    def test_caso_3_login_uat(self, setup):
        """Test caso 3 - con mejor logging"""
        driver = setup['driver']
        db = setup['db']
        start_time = time.time()
        
        # Configurar logging más detallado
        import logging
        logging.basicConfig(level=logging.INFO)
        
        try:
            print("🚀 INICIANDO TEST CASO 3 - LOGIN UAT")
            
            # ===== HOME PAGE - LOGIN =====
            with allure.step("Paso 1: Login en el sistema"):
                home_page = HomePage(driver)
                
                # Navegar a la página UAT3
                print("🌐 Navegando a la página UAT3...")
                driver.get(Config.BASE_URL)
                time.sleep(5)  # Espera más larga inicial
                
                print("🔍 Realizando login...")
                # Realizar login
                login_result = home_page.login(Config.TEST_USERNAME, Config.TEST_PASSWORD)
                
                if not login_result:
                    print("❌ LOGIN FALLIDO - Abortando test")
                    assert False, "Login fallido"
                
                print("✅ LOGIN EXITOSO - Continuando con el test...")
        
            # ===== CONFIGURACIÓN DE BÚSQUEDA =====
            with allure.step("Paso 2: Configuración de búsqueda post-login"):
                # Configurar idioma Francés
                assert home_page.change_language("french"), "❌ No se pudo cambiar a francés"
                
                # Configurar POS France
                assert home_page.change_pos("france"), "❌ No se pudo cambiar POS a France"
                
                # Configurar tipo de viaje (cualquiera)
                trip_success = (home_page.select_trip_type("one-way") or 
                              home_page.select_trip_type("round-trip"))
                assert trip_success, "❌ No se pudo seleccionar tipo de viaje"
                
                # Configurar origen y destino (cualquiera)
                # Usar aeropuertos franceses para consistencia
                assert home_page.set_origin_destination("CDG", "ORY"), "❌ No se pudo configurar origen/destino"
                
                # Configurar pasajeros (3 de cada tipo)
                assert home_page.set_passengers(
                    adults=Config.PASSENGERS["adults"],
                    youth=Config.PASSENGERS["youth"], 
                    children=Config.PASSENGERS["children"],
                    infants=Config.PASSENGERS["infants"]
                ), "❌ No se pudo configurar pasajeros"
                
                home_page.take_screenshot("caso3_search_configuration")
            
            # ===== BUSCAR VUELOS =====
            with allure.step("Paso 3: Buscar vuelos y validar"):
                # Buscar vuelos
                assert home_page.search_flights(), "❌ No se pudo buscar vuelos"
                
                # ===== SELECT FLIGHT PAGE =====
                with allure.step("Paso 4: Validar página de selección de vuelos"):
                    select_flight_page = SelectFlightPage(driver)
                    
                    # Validar que cargó la página de selección
                    assert select_flight_page.verify_page_loaded(), "❌ Página de selección de vuelos no cargó"
                    
                    select_flight_page.take_screenshot("caso3_select_flight_loaded")
            
            # ===== CAPTURAR DATOS DE SESIÓN DESDEVTOOLS =====
            with allure.step("Paso 5: Capturar datos de sesión desde DevTools"):
                # Script mejorado para capturar datos de sesión específicos
                session_data = driver.execute_script("""
                    // Función para capturar datos específicos de sesión
                    function captureSessionData() {
                        const sessionInfo = {
                            // Información básica
                            url: window.location.href,
                            title: document.title,
                            userAgent: navigator.userAgent,
                            language: navigator.language,
                            
                            // Cookies y almacenamiento
                            cookies: document.cookie,
                            localStorage: JSON.stringify(localStorage),
                            sessionStorage: JSON.stringify(sessionStorage),
                            
                            // Timestamp
                            timestamp: new Date().toISOString(),
                            
                            // Información de performance
                            performance: JSON.stringify(performance.timing),
                            
                            // Información específica de la sesión
                            sessionData: {
                                userInfo: localStorage.getItem('userInfo') || 
                                         sessionStorage.getItem('userInfo') ||
                                         'No disponible',
                                authToken: localStorage.getItem('authToken') ||
                                          sessionStorage.getItem('authToken') ||
                                          document.cookie.match(/(^| )token=([^;]+)/)?.[2] ||
                                          'No disponible',
                                sessionId: localStorage.getItem('sessionId') ||
                                          sessionStorage.getItem('sessionId') ||
                                          document.cookie.match(/(^| )sessionId=([^;]+)/)?.[2] ||
                                          'No disponible'
                            }
                        };
                        
                        // Capturar información de la página actual
                        const pageData = {
                            flightElements: document.querySelectorAll('[class*="flight"], [class*="vuelo"]').length,
                            priceElements: document.querySelectorAll('[class*="price"], [class*="precio"]').length,
                            selectButtons: document.querySelectorAll('button[class*="select"], button[class*="seleccionar"]').length
                        };
                        
                        return {
                            sessionInfo: sessionInfo,
                            pageData: pageData,
                            networkData: {
                                // Simular captura de eventos de red
                                capturedRequests: window.performance.getEntriesByType('resource')
                                    .filter(entry => entry.name.includes('session') || 
                                                   entry.name.includes('auth') ||
                                                   entry.name.includes('flight'))
                                    .map(entry => ({
                                        name: entry.name,
                                        duration: entry.duration,
                                        size: entry.transferSize
                                    }))
                            }
                        };
                    }
                    
                    return captureSessionData();
                """)
                
                # Adjuntar datos de sesión a Allure
                if session_data:
                    # Adjuntar información de sesión completa
                    allure.attach(
                        json.dumps(session_data['sessionInfo'], indent=2), 
                        name="Session_Information_Complete", 
                        attachment_type=allure.attachment_type.JSON
                    )
                    
                    # Adjuntar información específica de la sesión
                    allure.attach(
                        json.dumps(session_data['sessionInfo']['sessionData'], indent=2), 
                        name="Session_Data_Specific", 
                        attachment_type=allure.attachment_type.JSON
                    )
                    
                    # Adjuntar datos de la página
                    allure.attach(
                        json.dumps(session_data['pageData'], indent=2), 
                        name="Page_Elements_Data", 
                        attachment_type=allure.attachment_type.JSON
                    )
                    
                    # Adjuntar datos de red
                    if session_data['networkData']['capturedRequests'].length > 0:
                        allure.attach(
                            json.dumps(session_data['networkData']['capturedRequests'], indent=2), 
                            name="Network_Requests", 
                            attachment_type=allure.attachment_type.JSON
                        )
                    
                    print("✅ Datos de sesión capturados exitosamente")
                    print(f"   URL: {session_data['sessionInfo']['url']}")
                    print(f"   Timestamp: {session_data['sessionInfo']['timestamp']}")
                    print(f"   User Info: {session_data['sessionInfo']['sessionData']['userInfo']}")
                    print(f"   Auth Token disponible: {session_data['sessionInfo']['sessionData']['authToken'] != 'No disponible'}")
                    print(f"   Session ID disponible: {session_data['sessionInfo']['sessionData']['sessionId'] != 'No disponible'}")
                    print(f"   Elementos de vuelo encontrados: {session_data['pageData']['flightElements']}")
            
            # ===== VERIFICACIÓN FINAL =====
            execution_time = time.time() - start_time
            print(f"\n🎉 CASO 3 COMPLETADO EXITOSAMENTE en {execution_time:.2f}s")
            
            # Guardar resultado en BD
            db.insert_result(
                test_name="caso_3_login_uat",
                status="PASS",
                browser=Config.BROWSER,
                url=Config.BASE_URL,
                execution_time=f"{execution_time:.2f}s",
                error_message=None,
                # Agregar datos específicos del caso 3
                additional_data=json.dumps({
                    "username": Config.TEST_USERNAME,
                    "language": Config.LANGUAGE,
                    "pos": "france",
                    "passengers": Config.PASSENGERS
                })
            )
            
        except AssertionError as ae:
            execution_time = time.time() - start_time
            error_msg = str(ae)
            
            # Tomar screenshot en caso de error
            try:
                driver.save_screenshot(f"./screenshots/caso3_error_{int(time.time())}.png")
            except:
                pass
            
            # Guardar resultado fallido en BD
            db.insert_result(
                test_name="caso_3_login_uat",
                status="FAIL",
                browser=Config.BROWSER,
                url=Config.BASE_URL,
                execution_time=f"{execution_time:.2f}s",
                error_message=error_msg
            )
            
            raise
            
        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = f"Error inesperado: {str(e)}"
            
            # Tomar screenshot en caso de error
            try:
                driver.save_screenshot(f"./screenshots/caso3_unexpected_error_{int(time.time())}.png")
            except:
                pass
            
            db.insert_result(
                test_name="caso_3_login_uat",
                status="ERROR",
                browser=Config.BROWSER,
                url=Config.BASE_URL,
                execution_time=f"{execution_time:.2f}s",
                error_message=error_msg
            )
            
            raise