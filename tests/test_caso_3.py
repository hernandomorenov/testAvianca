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
    """Caso automatizado 3: Realizar Login en UAT1 (nuxqa3.avtest.ink) - VERSIÓN MEJORADA"""
    
    @allure.feature("Caso Automatizado 3")
    @allure.story("Login y configuración de búsqueda")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Caso 3: Login y validación de sesión")
    def test_caso_3_login_uat(self, setup):
        """Test caso 3 - Versión mejorada con HomePage y SelectFlightPage actualizados"""
        driver = setup['driver']
        db = setup['db']
        start_time = time.time()
        
        try:
            print("🚀 INICIANDO TEST CASO 3 - LOGIN UAT1 (nuxqa3.avtest.ink)")
            print(f"📍 URL Base: {Config.BASE_URL}")
            print(f"👤 Usuario: {Config.TEST_USERNAME}")

            # ===== HOME PAGE - LOGIN =====
            with allure.step("Paso 1: Login en el sistema UAT1"):
                home_page = HomePage(driver)

                # Navegar a la página UAT1
                print("🌐 Navegando a la página UAT1...")
                driver.get(Config.BASE_URL)
                
                # Esperar carga inicial
                home_page.wait_for_page_load(timeout=15)
                home_page.take_screenshot("caso3_inicio")
                
                print("🔍 Realizando login...")
                # Realizar login con el método mejorado
                login_result = home_page.login(Config.TEST_USERNAME, Config.TEST_PASSWORD)
                
                if not login_result:
                    print("❌ LOGIN FALLIDO - Verificando credenciales y estado...")
                    print(f"   Usuario usado: {Config.TEST_USERNAME}")
                    print(f"   URL actual: {driver.current_url}")
                    
                    # Tomar screenshot de error
                    home_page.take_screenshot("caso3_login_fallido_detalle")
                    
                    # Verificar si las credenciales están configuradas
                    if not Config.TEST_USERNAME or Config.TEST_USERNAME == "tu_usuario":
                        print("❌ CREDENCIALES NO CONFIGURADAS - Revisa utils/config.py")
                        assert False, "Credenciales no configuradas en config.py"
                    else:
                        assert False, f"Login fallido con usuario: {Config.TEST_USERNAME}"
                
                print("✅ LOGIN EXITOSO - Continuando con el test...")
                home_page.take_screenshot("caso3_login_exitoso")
        
            # ===== CONFIGURACIÓN DE BÚSQUEDA =====
            with allure.step("Paso 2: Configuración de búsqueda post-login"):
                # Esperar a que la página esté lista después del login
                home_page.wait_for_page_load(timeout=10)
                
                # Configurar idioma Francés
                print("🔧 Configurando idioma Francés...")
                language_success = home_page.change_language("french")
                assert language_success, "❌ No se pudo cambiar a francés"
                print("✅ Idioma configurado: Francés")
                
                # Configurar POS France
                print("🔧 Configurando POS France...")
                pos_success = home_page.change_pos("france")
                assert pos_success, "❌ No se pudo cambiar POS a France"
                print("✅ POS configurado: France")
                
                # Configurar tipo de viaje
                print("🔧 Configurando tipo de viaje...")
                trip_success = home_page.select_trip_type("one-way")
                if not trip_success:
                    trip_success = home_page.select_trip_type("round-trip")
                assert trip_success, "❌ No se pudo seleccionar tipo de viaje"
                print("✅ Tipo de viaje configurado")
                
                # Configurar origen y destino (aeropuertos franceses)
                print("🔧 Configurando origen y destino...")
                origin_dest_success = home_page.set_origin_destination("CDG - Paris Charles de Gaulle", "ORY - Paris Orly")
                if not origin_dest_success:
                    # Intentar método alternativo
                    origin_dest_success = home_page.set_origin_destination_alternative("CDG", "ORY")
                assert origin_dest_success, "❌ No se pudo configurar origen/destino"
                print("✅ Origen y destino configurados")
                
                # Configurar pasajeros
                print("🔧 Configurando pasajeros...")
                passengers_config = getattr(Config, 'PASSENGERS', {'adults': 1, 'youth': 0, 'children': 0, 'infants': 0})
                passengers_success = home_page.set_passengers(
                    adults=passengers_config.get("adults", 1),
                    youth=passengers_config.get("youth", 0), 
                    children=passengers_config.get("children", 0),
                    infants=passengers_config.get("infants", 0)
                )
                assert passengers_success, "❌ No se pudo configurar pasajeros"
                print("✅ Pasajeros configurados")
                
                home_page.take_screenshot("caso3_search_configuration")
            
            # ===== BUSCAR VUELOS =====
            with allure.step("Paso 3: Buscar vuelos y validar"):
                # Buscar vuelos
                print("🔍 Buscando vuelos...")
                search_success = home_page.search_flights()
                assert search_success, "❌ No se pudo buscar vuelos"
                print("✅ Búsqueda de vuelos iniciada")
                
                # Esperar redirección
                home_page.wait_for_page_load(timeout=15)
                
                # ===== SELECT FLIGHT PAGE =====
                with allure.step("Paso 4: Validar página de selección de vuelos"):
                    select_flight_page = SelectFlightPage(driver)
                    
                    # Validar que cargó la página de selección (con retry mechanism)
                    page_loaded = select_flight_page.verify_page_loaded()
                    assert page_loaded, "❌ Página de selección de vuelos no cargó"
                    
                    # Esperar a que los vuelos carguen
                    flights_loaded = select_flight_page.wait_for_flights_load()
                    assert flights_loaded, "❌ Los vuelos no cargaron correctamente"
                    
                    select_flight_page.take_screenshot("caso3_select_flight_loaded")
                    print("✅ Página de selección de vuelos cargada correctamente")
            
            # ===== CAPTURAR DATOS DE SESIÓN =====
            with allure.step("Paso 5: Capturar datos de sesión desde DevTools/Network"):
                print("📊 Capturando datos de sesión desde DevTools...")

                session_capture = {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "url": driver.current_url,
                    "title": driver.title,
                    "test_case": "caso_3_login_uat",
                    "components_used": ["HomePage_mejorado", "SelectFlightPage_mejorado"]
                }

                # Capturar datos de almacenamiento
                try:
                    storage_data = driver.execute_script("""
                        return {
                            localStorage: JSON.parse(JSON.stringify(localStorage)),
                            sessionStorage: JSON.parse(JSON.stringify(sessionStorage)),
                            cookies: document.cookie
                        };
                    """)
                    session_capture["storage"] = storage_data
                    print(f"✅ Datos de almacenamiento capturados")
                except Exception as e:
                    print(f"⚠️ Error capturando storage: {e}")

                # Extraer campos específicos
                extracted_fields = {
                    "test_config": {
                        "username": Config.TEST_USERNAME,
                        "base_url": Config.BASE_URL,
                        "browser": getattr(Config, 'BROWSER', 'chrome')
                    },
                    "session_capture_time": session_capture["timestamp"],
                    "current_url": session_capture["url"],
                    "page_title": session_capture["title"],
                    "language_set": "french",
                    "pos_set": "france",
                    "components": "HomePage_mejorado + SelectFlightPage_mejorado"
                }

                session_capture["extracted_fields"] = extracted_fields

                # Adjuntar datos a Allure
                allure.attach(
                    json.dumps(session_capture, indent=2, default=str),
                    name="Complete_Session_Capture",
                    attachment_type=allure.attachment_type.JSON
                )

                allure.attach(
                    json.dumps(extracted_fields, indent=2, default=str),
                    name="Extracted_Session_Fields",
                    attachment_type=allure.attachment_type.JSON
                )

                print("✅ Captura de sesión completada exitosamente")
                print(f"   📍 URL actual: {session_capture['url']}")
                print(f"   ⏰ Timestamp: {session_capture['timestamp']}")
                print(f"   🔧 Componentes: {session_capture['components_used']}")
            
            # ===== VERIFICACIÓN FINAL =====
            execution_time = time.time() - start_time
            print(f"\n🎉 CASO 3 COMPLETADO EXITOSAMENTE en {execution_time:.2f}s")
            
            # Guardar resultado en BD
            db.insert_result(
                test_name="caso_3_login_uat",
                status="PASS",
                browser=getattr(Config, 'BROWSER', 'chrome'),
                url=Config.BASE_URL,
                execution_time=f"{execution_time:.2f}s",
                error_message=None,
                additional_data=json.dumps({
                    "username": Config.TEST_USERNAME,
                    "language": "french",
                    "pos": "france",
                    "passengers": getattr(Config, 'PASSENGERS', {'adults': 1, 'youth': 0, 'children': 0, 'infants': 0}),
                    "execution_time": f"{execution_time:.2f}s",
                    "components": "HomePage_mejorado + SelectFlightPage_mejorado"
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
                browser=getattr(Config, 'BROWSER', 'chrome'),
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
                browser=getattr(Config, 'BROWSER', 'chrome'),
                url=Config.BASE_URL,
                execution_time=f"{execution_time:.2f}s",
                error_message=error_msg
            )
            
            raise