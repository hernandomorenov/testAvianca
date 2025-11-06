import pytest
import allure
import time
from datetime import datetime, timedelta
from pages.booking_flow.home_page import HomePage
from pages.booking_flow.select_flight_page import SelectFlightPage
from pages.booking_flow.passengers_page import PassengersPage
from pages.booking_flow.services_page import ServicesPage
from pages.booking_flow.seatmap_page import SeatmapPage
from pages.booking_flow.payments_page import PaymentsPage
from utils.config import Config


@pytest.mark.caso_2
@pytest.mark.regression
class TestCasoAutomatizado2:
    """
    Caso automatizado 2: Realizar booking Round-trip (Ida y vuelta)
    """
    
    @allure.feature("Caso Automatizado 2")
    @allure.story("Booking Round-Trip con validaciones completas")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Caso 2: Booking Round-Trip completo")
    def test_caso_2_booking_round_trip(self, setup):
        """
        Home: Seleccionar idioma, pos, origen, destino y 1 pasajero de cada tipo
        Select flight: Seleccionar tarifa Basic (Ida) y Flex (Vuelta)
        Passengers: Ingresar la información de los pasajeros
        Services: Seleccionar Avianca Lounges o cualquier disponible
        Seatmap: Seleccionar asiento Plus, Economy, Premium y Economy
        Payments: Llenar información de pago, pero no enviarla
        """
        driver = setup['driver']
        db = setup['db']
        start_time = time.time()
        
        try:
            # ===== HOME PAGE =====
            with allure.step("Paso 1: Configuración en Home Page"):
                home_page = HomePage(driver)
                
                # Navegar a la página
                assert home_page.navigate_to(Config.BASE_URL), "❌ No se pudo navegar a la página"

                # Configurar idioma y POS
                assert home_page.change_language("english"), "❌ No se pudo cambiar el idioma"
                assert home_page.change_pos("spain"), "❌ No se pudo cambiar el POS"
                
                # Configurar tipo de viaje
                assert home_page.select_trip_type("round-trip"), "❌ No se pudo seleccionar round-trip"
                
                # Configurar origen y destino
                assert home_page.set_origin_destination("MAD", "BCN"), "❌ No se pudo configurar origen/destino"
                
                # Configurar fechas (mañana y pasado mañana)
                tomorrow = (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")
                day_after = (datetime.now() + timedelta(days=3)).strftime("%d/%m/%Y")
                assert home_page.set_dates(tomorrow, day_after), "❌ No se pudo configurar fechas"
                
                # Configurar pasajeros
                assert home_page.set_passengers(adults=1, youths=1, children=1, infants=1), "❌ No se pudo configurar pasajeros"
                
                # Buscar vuelos
                assert home_page.search_flights(), "❌ No se pudo buscar vuelos"
                
                home_page.take_screenshot("caso2_home_completed")
            
            # ===== SELECT FLIGHT PAGE =====
            with allure.step("Paso 2: Selección de vuelos y tarifas"):
                select_flight_page = SelectFlightPage(driver)
                
                # Esperar carga de vuelos
                assert select_flight_page.wait_for_flights_load(), "❌ Los vuelos no cargaron"
                
                # Seleccionar tarifa Basic para ida
                assert select_flight_page.select_basic_fare(), "❌ No se pudo seleccionar tarifa Basic"
                
                # Seleccionar vuelo de ida
                assert select_flight_page.select_departure_flight(), "❌ No se pudo seleccionar vuelo de ida"
                
                # Seleccionar tarifa Flex para vuelta
                assert select_flight_page.select_flex_fare(), "❌ No se pudo seleccionar tarifa Flex"
                
                # Seleccionar vuelo de regreso
                assert select_flight_page.select_return_flight(), "❌ No se pudo seleccionar vuelo de regreso"
                
                # Continuar a pasajeros
                assert select_flight_page.continue_to_passengers(), "❌ No se pudo continuar a pasajeros"
                
                select_flight_page.take_screenshot("caso2_flights_selected")
            
            # ===== PASSENGERS PAGE =====
            with allure.step("Paso 3: Información de pasajeros"):
                passengers_page = PassengersPage(driver)
                
                # Verificar que cargó la página
                assert passengers_page.verify_page_loaded(), "❌ Página de pasajeros no cargó"
                
                # Llenar información de todos los pasajeros
                assert passengers_page.fill_all_passengers(adults=1, youth=1, children=1, infants=1), "❌ No se pudo llenar información de pasajeros"
                
                # Continuar a servicios
                assert passengers_page.continue_to_services(), "❌ No se pudo continuar a servicios"
                
                passengers_page.take_screenshot("caso2_passengers_completed")
            
            # ===== SERVICES PAGE =====
            with allure.step("Paso 4: Servicios adicionales"):
                services_page = ServicesPage(driver)
                
                # Verificar que cargó la página
                assert services_page.verify_page_loaded(), "❌ Página de servicios no cargó"
                
                # Intentar seleccionar Avianca Lounges
                lounge_selected = services_page.select_lounge_service()
                
                # Si no está disponible, seleccionar cualquier servicio
                if not lounge_selected:
                    assert services_page.select_available_service(), "❌ No se pudo seleccionar ningún servicio"
                
                # Continuar a asientos
                assert services_page.continue_to_seatmap(), "❌ No se pudo continuar a asientos"
                
                services_page.take_screenshot("caso2_services_selected")
            
            # ===== SEATMAP PAGE =====
            with allure.step("Paso 5: Selección de asientos múltiples"):
                seatmap_page = SeatmapPage(driver)
                
                # Verificar que cargó la página
                assert seatmap_page.verify_page_loaded(), "❌ Página de asientos no cargó"
                
                # Seleccionar diferentes tipos de asientos para 4 pasajeros
                seat_types = ["plus", "economy", "premium", "economy"]
                assert seatmap_page.select_seats_for_all(passengers_count=4, seat_types=seat_types), "❌ No se pudo seleccionar asientos"
                
                # Continuar a pagos
                assert seatmap_page.continue_to_payments(), "❌ No se pudo continuar a pagos"
                
                seatmap_page.take_screenshot("caso2_seats_selected")
            
            # ===== PAYMENTS PAGE =====
            with allure.step("Paso 6: Formulario de pago (sin enviar)"):
                payments_page = PaymentsPage(driver)
                
                # Verificar que cargó la página
                assert payments_page.verify_page_loaded(), "❌ Página de pagos no cargó"
                
                # Llenar información de pago pero NO enviar
                assert payments_page.fill_payment_form_only(), "❌ No se pudo llenar información de pago"
                
                # Capturar datos de sesión
                session_data = payments_page.capture_session_data()
                if session_data:
                    allure.attach(str(session_data), name="Session Data", attachment_type=allure.attachment_type.JSON)
                
                payments_page.take_screenshot("caso2_payment_form_filled")
            
            # ===== VERIFICACIÓN FINAL =====
            execution_time = time.time() - start_time
            print(f"\n🎉 CASO 2 COMPLETADO EXITOSAMENTE en {execution_time:.2f}s")
            
            # Guardar resultado en BD
            db.insert_result(
                test_name="caso_2_booking_round_trip",
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
                test_name="caso_2_booking_round_trip",
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
                test_name="caso_2_booking_round_trip",
                status="ERROR",
                browser=Config.BROWSER,
                url=Config.BASE_URL,
                execution_time=f"{execution_time:.2f}s",
                error_message=error_msg
            )
            
            raise