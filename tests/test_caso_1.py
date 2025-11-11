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
        start_time = time.time()

        try:
            # Mostrar configuración actual
            Config.print_config()
            
            # ===== HOME PAGE =====
            with allure.step("Paso 1: Configuración en Home Page"):
                home_page = HomePage(driver)

                # Navegar a la página
                print("🌐 Navegando a la página principal...")
                home_page.navigate_to(Config.BASE_URL_EN)  # Usar URL específica para español
                home_page.take_screenshot("caso1_pagina_cargada")

                # Configurar POS
                print("🔧 Configurando POS Other...")
                home_page.change_pos("other")

                # Configurar tipo de viaje one-way
                print("🔧 Configurando tipo de viaje One-Way...")
                home_page.select_trip_type("one-way")

                # Configurar origen y destino
                print("🔧 Configurando origen BOG y destino MDE...")
                home_page.set_origin_destination(Config.TEST_ORIGIN, Config.TEST_DESTINATION)

                # Configurar fecha (mañana)
                print("📅 Configurando fecha de salida (mañana)...")
                tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
                home_page.set_dates(tomorrow)

                # Configurar pasajeros - CORREGIDO: parámetros en minúsculas
                print("👥 Configurando pasajeros: 1 Adulto, 1 Joven, 1 Niño, 1 Infante...")
                home_page.set_passengers(adults=1, youth=1, children=1, infants=1)  # <-- CORREGIDO

                # Buscar vuelos
                print("🔍 Buscando vuelos...")
                home_page.search_flights()

                home_page.take_screenshot("caso1_home_completed")
                print("✅ Home Page completado exitosamente")

            # ===== SELECT FLIGHT PAGE =====
            with allure.step("Paso 2: Selección de vuelos y tarifa Basic"):
                print("🛫 Cargando página de selección de vuelos...")

                select_flight_page = SelectFlightPage(driver)
                select_flight_page.wait_for_page_load(timeout=20)
                
                # Esperar carga de vuelos
                print("⏳ Esperando carga de vuelos...")
                select_flight_page.wait_for_flights_load()

                # Seleccionar tarifa Basic
                print("💰 Seleccionando tarifa Basic...")
                select_flight_page.select_basic_fare()

                # Seleccionar vuelo de ida
                print("✈️ Seleccionando vuelo de ida...")
                select_flight_page.select_departure_flight()

                # Continuar a pasajeros
                print("➡️ Continuando a página de pasajeros...")
                select_flight_page.continue_to_passengers()

                select_flight_page.take_screenshot("caso1_flights_selected")
                print("✅ Selección de vuelos completada")

            # ===== PASSENGERS PAGE =====
            with allure.step("Paso 3: Información de pasajeros"):
                print("👤 Cargando página de información de pasajeros...")

                passengers_page = PassengersPage(driver)
                passengers_page.wait_for_page_load(timeout=15)

                # Verificar que cargó la página
                print("🔍 Verificando carga de página de pasajeros...")
                passengers_page.verify_page_loaded()

                # Llenar información de todos los pasajeros
                print("📝 Llenando información de pasajeros...")
                passengers_page.fill_all_passengers(
                    adults=1,  # <-- CORREGIDO
                    youth=1,   # <-- CORREGIDO
                    children=1, # <-- CORREGIDO
                    infants=1   # <-- CORREGIDO
                )

                # Continuar a servicios
                print("➡️ Continuando a servicios...")
                passengers_page.continue_to_services()

                passengers_page.take_screenshot("caso1_passengers_completed")
                print("✅ Información de pasajeros completada")

            # ===== SERVICES PAGE =====
            with allure.step("Paso 4: Servicios adicionales - No seleccionar ninguno"):
                print("🎫 Cargando página de servicios...")

                services_page = ServicesPage(driver)
                services_page.wait_for_page_load(timeout=15)

                # Verificar que cargó la página
                print("🔍 Verificando carga de página de servicios...")
                services_page.verify_page_loaded()

                # No seleccionar servicios (saltar)
                print("⏭️ Saltando servicios adicionales...")
                services_page.skip_services()

                # Continuar a asientos
                print("➡️ Continuando a selección de asientos...")
                services_page.continue_to_seatmap()

                services_page.take_screenshot("caso1_services_skipped")
                print("✅ Servicios saltados exitosamente")

            # ===== SEATMAP PAGE =====
            with allure.step("Paso 5: Selección de asientos economy"):
                print("💺 Cargando página de selección de asientos...")

                seatmap_page = SeatmapPage(driver)
                seatmap_page.wait_for_page_load(timeout=15)

                # Verificar que cargó la página
                print("🔍 Verificando carga de página de asientos...")
                seatmap_page.verify_page_loaded()

                # Seleccionar asiento economy
                print("💺 Seleccionando asiento economy...")
                seatmap_page.select_economy_seat()

                # Continuar a pagos
                print("➡️ Continuando a página de pagos...")
                seatmap_page.continue_to_payments()

                seatmap_page.take_screenshot("caso1_seat_selected")
                print("✅ Selección de asientos completada")

            # ===== PAYMENTS PAGE =====
            with allure.step("Paso 6: Proceso de pago con tarjeta fake"):
                print("💳 Cargando página de pagos...")

                payments_page = PaymentsPage(driver)
                payments_page.wait_for_page_load(timeout=15)

                # Verificar que cargó la página
                print("🔍 Verificando carga de página de pagos...")
                payments_page.verify_page_loaded()

                # Llenar información de pago fake
                print("🏦 Llenando información de pago fake...")
                payments_page.fill_payment_information()

                payments_page.take_screenshot("caso1_payment_completed")
                print("✅ Proceso de pago completado")

            # ===== VERIFICACIÓN FINAL =====
            execution_time = time.time() - start_time
            print(f"\n🎉 CASO 1 COMPLETADO EXITOSAMENTE en {execution_time:.2f} segundos")
            
            # Verificar que llegamos al final del flujo
            final_url = driver.current_url
            print(f"📍 URL final: {final_url}")
            
            # El test pasa si llegamos hasta el final del flujo
            assert True, f"✅ Flujo de booking one-way completado en {execution_time:.2f}s"

        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = f"Error en Caso 1: {str(e)}"
            
            print(f"❌ Error en Caso 1: {error_msg}")
            print(f"⏱️ Tiempo de ejecución: {execution_time:.2f}s")
            
            # Tomar screenshot de error
            try:
                driver.save_screenshot("screenshots/caso1_error.png")
            except:
                pass
            
            # Marcar como fallido
            assert False, error_msg