# Paquete booking_flow

from pages.base_page import BasePage
from .home_page import HomePage
from .select_flight_page import SelectFlightPage
from .passengers_page import PassengersPage
from .services_page import ServicesPage
from .seatmap_page import SeatmapPage
from .payments_page import PaymentsPage

__all__ = [
    'BasePage',
    'HomePage', 
    'SelectFlightPage',
    'PassengersPage',
    'ServicesPage',
    'SeatmapPage',
    'PaymentsPage'
]