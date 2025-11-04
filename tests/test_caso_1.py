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


@pytest.mark.caso_1
@pytest.mark.regression
class TestCasoAutomatizado1:
    """
    Caso automatizado 1: Realizar booking One-way (Solo ida)
    """
    
    @allure.feature("Caso Automatizado 1")
    @allure.story("Booking One-Way con validaciones completas")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Caso 1: Booking One-Way completo")
    def test_caso_1_booking_one_way(self, setup):
        """
        Home: Seleccionar idioma, pos, origen, destino y 1 pasajero de cada tipo
        Select flight: Seleccionar tarifa Basic
        Passengers: Ingresar la información de los pasajeros
        Services: No seleccionar ninguno
        Seatmap: Seleccionar asiento economy
        Payments: Realizar pago con tarjeta utilizando información fake
        """
        driver = setup['driver']
        db = setup['db']
        start_time = time.time()
        
        try:
            # ===== HOME PAGE =====
            with allure.step("Paso 1: Configuración en Home Page"):
                home_page = HomePage(driver)
                
                # Navegar a la página - CORREGIDO: usar navigate_to en lugar de open
                assert home_page.navigate_to(Config.BASE_URL), "❌ No se pudo navegar a la página"

                # Tomar screenshot inicial
                home_page.take_screenshot("caso1_pagina_cargada")
                
                # Configurar idioma y POS
                print("🔧 Configurando idioma...")
                language_success = home_page.change_language("spanish")
                if not language_success:
                    print("⚠️ No se pudo cambiar idioma, continuando...")
                
                print("🔧 Configurando POS...")
                pos_success = home_page.change_pos("other")
                if not pos_success:
                    print("⚠️ No se pudo cambiar POS, continuando...")
                
                # Configurar tipo de viaje
                assert home_page.select_trip_type("one-way"), "❌ No se pudo seleccionar one-way"
                
                # Configurar origen y destino
                assert home_page.set_origin_destination("BOG", "MDE"), "❌ No se pudo configurar origen/destino"
                
                # Configurar fecha (mañana)
                tomorrow = (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")
                assert home_page.set_dates(tomorrow), "❌ No se pudo configurar fecha"
                
                # Configurar pasajeros
                assert home_page.set_passengers(adults=1, youth=1, children=1, infants=1), "❌ No se pudo configurar pasajeros"
                
                # Buscar vuelos
                assert home_page.search_flights(), "❌ No se pudo buscar vuelos"
                
                home_page.take_screenshot("caso1_home_completed")
            
            # ===== SELECT FLIGHT PAGE =====
            with allure.step("Paso 2: Selección de vuelos"):
                select_flight_page = SelectFlightPage(driver)
                
                # Esperar carga de vuelos
                assert select_flight_page.wait_for_flights_load(), "❌ Los vuelos no cargaron"
                
                # Seleccionar tarifa Basic
                assert select_flight_page.select_basic_fare(), "❌ No se pudo seleccionar tarifa Basic"
                
                # Seleccionar vuelo de ida
                assert select_flight_page.select_departure_flight(), "❌ No se pudo seleccionar vuelo de ida"
                
                # Continuar a pasajeros
                assert select_flight_page.continue_to_passengers(), "❌ No se pudo continuar a pasajeros"
                
                select_flight_page.take_screenshot("caso1_flights_selected")
            
            # ===== PASSENGERS PAGE =====
            with allure.step("Paso 3: Información de pasajeros"):
                passengers_page = PassengersPage(driver)
                
                # Verificar que cargó la página
                assert passengers_page.verify_page_loaded(), "❌ Página de pasajeros no cargó"
                
                # Llenar información de todos los pasajeros
                assert passengers_page.fill_all_passengers(adults=1, youth=1, children=1, infants=1), "❌ No se pudo llenar información de pasajeros"
                
                # Continuar a servicios
                assert passengers_page.continue_to_services(), "❌ No se pudo continuar a servicios"
                
                passengers_page.take_screenshot("caso1_passengers_completed")
            
            # ===== SERVICES PAGE =====
            with allure.step("Paso 4: Servicios adicionales"):
                services_page = ServicesPage(driver)
                
                # Verificar que cargó la página
                assert services_page.verify_page_loaded(), "❌ Página de servicios no cargó"
                
                # No seleccionar servicios (saltar)
                assert services_page.skip_services(), "❌ No se pudo saltar servicios"
                
                # Continuar a asientos
                assert services_page.continue_to_seatmap(), "❌ No se pudo continuar a asientos"
                
                services_page.take_screenshot("caso1_services_skipped")
            
            # ===== SEATMAP PAGE =====
            with allure.step("Paso 5: Selección de asientos"):
                seatmap_page = SeatmapPage(driver)
                
                # Verificar que cargó la página
                assert seatmap_page.verify_page_loaded(), "❌ Página de asientos no cargó"
                
                # Seleccionar asiento economy
                assert seatmap_page.select_economy_seat(), "❌ No se pudo seleccionar asiento economy"
                
                # Continuar a pagos
                assert seatmap_page.continue_to_payments(), "❌ No se pudo continuar a pagos"
                
                seatmap_page.take_screenshot("caso1_seat_selected")
            
            # ===== PAYMENTS PAGE =====
            with allure.step("Paso 6: Proceso de pago"):
                payments_page = PaymentsPage(driver)
                
                # Verificar que cargó la página
                assert payments_page.verify_page_loaded(), "❌ Página de pagos no cargó"
                
                # Llenar información de pago y enviar
                assert payments_page.fill_payment_information(), "❌ No se pudo completar el pago"
                
                payments_page.take_screenshot("caso1_payment_completed")
            
            # ===== VERIFICACIÓN FINAL =====
            execution_time = time.time() - start_time
            print(f"\n🎉 CASO 1 COMPLETADO EXITOSAMENTE en {execution_time:.2f}s")
            
            # Guardar resultado en BD
            db.insert_result(
                test_name="caso_1_booking_one_way",
                status="PASS",
                browser=Config.BROWSER,
                url=Config.BASE_URL,
                execution_time=f"{execution_time:.2f}s",
                error_message=None
            )
            
        except AssertionError as ae:
            execution_time = time.time() - start_time
            error_msg = str(ae)
            
            print(f"❌ AssertionError: {error_msg}")
            
            # Tomar screenshot de error
            try:
                driver.save_screenshot("screenshots/caso1_error.png")
            except:
                pass
            
            # Guardar resultado fallido en BD
            db.insert_result(
                test_name="caso_1_booking_one_way",
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
            
            print(f"❌ Exception: {error_msg}")
            
            try:
                driver.save_screenshot("screenshots/caso1_unexpected_error.png")
            except:
                pass
            
            db.insert_result(
                test_name="caso_1_booking_one_way",
                status="ERROR",
                browser=Config.BROWSER,
                url=Config.BASE_URL,
                execution_time=f"{execution_time:.2f}s",
                error_message=error_msg
            )
            
            raise