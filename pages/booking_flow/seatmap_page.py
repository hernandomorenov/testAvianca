from selenium.webdriver.common.by import By
from pages.booking_flow import BasePage
import allure
import time
import random


class SeatmapPage(BasePage):
    """Page Object para página de selección de asientos"""
    
    # Selectores de asientos
    SEAT_MAP = (By.XPATH, "//div[contains(@class, 'seatmap')]")
    AVAILABLE_SEATS = (By.XPATH, "//div[contains(@class, 'seat-available')]")
    ECONOMY_SEATS = (By.XPATH, "//div[contains(@class, 'economy') and contains(@class, 'available')]")
    PLUS_SEATS = (By.XPATH, "//div[contains(@class, 'plus') and contains(@class, 'available')]")
    PREMIUM_SEATS = (By.XPATH, "//div[contains(@class, 'premium') and contains(@class, 'available')]")
    
    # Botones
    CONTINUE_BUTTON = (By.XPATH, "//button[contains(text(), 'Continue') or contains(text(), 'Continuar')]")
    SKIP_SEATS_BUTTON = (By.XPATH, "//button[contains(text(), 'Skip') or contains(text(), 'Saltar')]")
    CONFIRM_SEATS_BUTTON = (By.XPATH, "//button[contains(text(), 'Confirm') or contains(text(), 'Confirmar')]")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    @allure.step("Select random available seat")
    def select_random_seat(self):
        """Seleccionar un asiento disponible al azar"""
        try:
            seats = self.driver.find_elements(*self.AVAILABLE_SEATS)
            if seats:
                random_seat = random.choice(seats)
                random_seat.click()
                time.sleep(1)
                print("✅ Asiento seleccionado aleatoriamente")
                return True
            else:
                print("❌ No hay asientos disponibles")
                return False
        except Exception as e:
            print(f"❌ Error seleccionando asiento: {e}")
            return False
    
    @allure.step("Select economy seat")
    def select_economy_seat(self):
        """Seleccionar asiento economy"""
        try:
            seats = self.driver.find_elements(*self.ECONOMY_SEATS)
            if seats:
                seats[0].click()
                time.sleep(1)
                print("✅ Asiento economy seleccionado")
                return True
            return False
        except Exception as e:
            print(f"❌ Error seleccionando asiento economy: {e}")
            return False
    
    @allure.step("Select plus seat")
    def select_plus_seat(self):
        """Seleccionar asiento plus"""
        try:
            seats = self.driver.find_elements(*self.PLUS_SEATS)
            if seats:
                seats[0].click()
                time.sleep(1)
                print("✅ Asiento plus seleccionado")
                return True
            return False
        except Exception as e:
            print(f"❌ Error seleccionando asiento plus: {e}")
            return False
    
    @allure.step("Select premium seat")
    def select_premium_seat(self):
        """Seleccionar asiento premium"""
        try:
            seats = self.driver.find_elements(*self.PREMIUM_SEATS)
            if seats:
                seats[0].click()
                time.sleep(1)
                print("✅ Asiento premium seleccionado")
                return True
            return False
        except Exception as e:
            print(f"❌ Error seleccionando asiento premium: {e}")
            return False
    
    @allure.step("Select seats for all passengers")
    def select_seats_for_all(self, passengers_count=1, seat_types=None):
        """Seleccionar asientos para todos los pasajeros"""
        if seat_types is None:
            seat_types = ["economy"] * passengers_count
        
        try:
            for i, seat_type in enumerate(seat_types):
                if seat_type == "economy":
                    success = self.select_economy_seat()
                elif seat_type == "plus":
                    success = self.select_plus_seat()
                elif seat_type == "premium":
                    success = self.select_premium_seat()
                else:
                    success = self.select_random_seat()
                
                if not success:
                    print(f"❌ Error seleccionando asiento {i+1}")
                    return False
                
                time.sleep(1)
            
            print(f"✅ {passengers_count} asientos seleccionados")
            return True
            
        except Exception as e:
            print(f"❌ Error seleccionando asientos: {e}")
            return False
    
    @allure.step("Skip seat selection")
    def skip_seat_selection(self):
        """Saltar selección de asientos"""
        return self.click_element(self.SKIP_SEATS_BUTTON)
    
    @allure.step("Continue to payments page")
    def continue_to_payments(self):
        """Continuar a página de pagos"""
        success = self.click_element(self.CONTINUE_BUTTON)
        if success:
            time.sleep(3)
        return success
    
    @allure.step("Verify seatmap page loaded")
    def verify_page_loaded(self):
        """Verificar que la página de asientos cargó"""
        try:
            return (self.is_element_present(self.SEAT_MAP, timeout=10) or 
                   self.is_element_present(self.SKIP_SEATS_BUTTON, timeout=10))
        except Exception as e:
            print(f"❌ Error verificando página de asientos: {e}")
            return False