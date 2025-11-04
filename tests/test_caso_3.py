import pytest
import allure
import time
from pages.booking_flow.home_page import HomePage
from pages.booking_flow.select_flight_page import SelectFlightPage
from utils.config import Config


@pytest.mark.caso_3
@pytest.mark.regression
class TestCasoAutomatizado3:
    """
    Caso automatizado 3: Realizar Login en UAT
    """
    
    @allure.feature("Caso Automatizado 3")
    @allure.story("Login y configuración de búsqueda")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Caso 3: Login y validación de sesión")
    def test_caso_3_login_uat(self, setup):
        """
        Home:
        - Realizar login con usuario: 21734198706, password: Lifemiles1
        - Seleccionar Idioma: Francés, POS: France
        - Tipo de Viaje: Cualquiera, Origen/Destino: Cualquiera
        - Cantidad de pasajeros: 3 de cada tipo
        - Validar que cargue página de Select flight
        - Capturar datos de sesión desde DevTools
        """
        driver = setup['driver']
        db = setup['db']
        start_time = time.time()
        
        try:
            # ===== HOME PAGE - LOGIN =====
            with allure.step("Paso 1: Login en el sistema"):
                home_page = HomePage(driver)
                
                # Navegar a la página
                assert home_page.navigate_to(Config.BASE_URL), "❌ No se pudo navegar a la página"

                # Realizar login
                assert home_page.login(Config.TEST_USERNAME, Config.TEST_PASSWORD), "❌ Login fallido"
                
                home_page.take_screenshot("caso3_login_success")
            
            # ===== CONFIGURACIÓN DE BÚSQUEDA =====
            with allure.step("Paso 2: Configuración de búsqueda post-login"):
                # Configurar idioma
                assert home_page.change_language("french"), "❌ No se pudo cambiar a francés"
                
                # Configurar POS
                assert home_page.change_pos("other"), "❌ No se pudo cambiar POS"  # Usar 'other' como France
                
                # Configurar tipo de viaje (cualquiera)
                trip_success = (home_page.select_trip_type("one-way") or 
                              home_page.select_trip_type("round-trip"))
                assert trip_success, "❌ No se pudo seleccionar tipo de viaje"
                
                # Configurar origen y destino (cualquiera)
                assert home_page.set_origin_destination("CDG", "ORY"), "❌ No se pudo configurar origen/destino"
                
                # Configurar pasajeros (3 de cada tipo)
                assert home_page.set_passengers(adults=3, youth=3, children=3, infants=3), "❌ No se pudo configurar pasajeros"
                
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
            
            # ===== CAPTURAR DATOS DE SESIÓN =====
            with allure.step("Paso 5: Capturar datos de sesión desde DevTools"):
                # Ejecutar script para capturar datos de red y sesión
                session_data = driver.execute_script("""
                    // Capturar información de la sesión
                    const sessionInfo = {
                        url: window.location.href,
                        title: document.title,
                        userAgent: navigator.userAgent,
                        language: navigator.language,
                        cookies: document.cookie,
                        localStorage: JSON.stringify(localStorage),
                        sessionStorage: JSON.stringify(sessionStorage),
                        timestamp: new Date().toISOString(),
                        performance: JSON.stringify(performance.timing)
                    };
                    
                    // Intentar capturar eventos de red simulados
                    const networkEvents = {
                        sessionEvents: [],
                        xhrRequests: []
                    };
                    
                    // Override XMLHttpRequest para capturar requests
                    const originalXHR = window.XMLHttpRequest;
                    window.XMLHttpRequest = function() {
                        const xhr = new originalXHR();
                        const originalOpen = xhr.open;
                        const originalSend = xhr.send;
                        
                        xhr.open = function(method, url) {
                            this._url = url;
                            this._method = method;
                            return originalOpen.apply(this, arguments);
                        };
                        
                        xhr.send = function(data) {
                            if (this._url && this._url.includes('session') || this._url.includes('Session')) {
                                networkEvents.sessionEvents.push({
                                    method: this._method,
                                    url: this._url,
                                    data: data,
                                    timestamp: new Date().toISOString()
                                });
                            }
                            networkEvents.xhrRequests.push({
                                method: this._method,
                                url: this._url,
                                timestamp: new Date().toISOString()
                            });
                            return originalSend.apply(this, arguments);
                        };
                        return xhr;
                    };
                    
                    return {
                        sessionInfo: sessionInfo,
                        networkEvents: networkEvents
                    };
                """)
                
                # Adjuntar datos de sesión a Allure
                if session_data:
                    allure.attach(
                        str(session_data['sessionInfo']), 
                        name="Session Information", 
                        attachment_type=allure.attachment_type.JSON
                    )
                    
                    if session_data['networkEvents']['sessionEvents']:
                        allure.attach(
                            str(session_data['networkEvents']['sessionEvents']), 
                            name="Session Network Events", 
                            attachment_type=allure.attachment_type.JSON
                        )
                    
                    print("✅ Datos de sesión capturados exitosamente")
                    print(f"   URL: {session_data['sessionInfo']['url']}")
                    print(f"   Timestamp: {session_data['sessionInfo']['timestamp']}")
                    print(f"   Eventos de sesión: {len(session_data['networkEvents']['sessionEvents'])}")
            
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
                error_message=None
            )
            
        except AssertionError as ae:
            execution_time = time.time() - start_time
            error_msg = str(ae)
            
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
            
            db.insert_result(
                test_name="caso_3_login_uat",
                status="ERROR",
                browser=Config.BROWSER,
                url=Config.BASE_URL,
                execution_time=f"{execution_time:.2f}s",
                error_message=error_msg
            )
            
            raise