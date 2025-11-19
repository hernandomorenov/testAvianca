# -*- coding: utf-8 -*-
"""
Test simple para verificar SOLO la selección de pasajeros
"""
import sys
import io
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.booking_flow.home_page import HomePage
from utils.config import Config

# Configurar encoding UTF-8 para Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def test_passengers_selector():
    """Test simple para verificar que el selector de pasajeros funciona"""

    # Configurar Chrome
    chrome_options = Options()
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')

    driver = webdriver.Chrome(options=chrome_options)

    try:
        print("="*60)
        print("🧪 TEST DE SELECTOR DE PASAJEROS")
        print("="*60)

        # Navegar a la página
        print("\n1️⃣ Navegando a la página...")
        driver.get(Config.BASE_URL_EN)
        time.sleep(3)

        # Crear instancia de HomePage
        home_page = HomePage(driver)

        # Configurar pasajeros
        print("\n2️⃣ Configurando pasajeros: 1 Adulto, 1 Joven, 1 Niño, 1 Infante...")
        result = home_page.set_passengers(adults=1, youth=1, children=1, infants=1)

        if result:
            print("\n✅ ¡TEST EXITOSO! Los pasajeros se configuraron correctamente")
        else:
            print("\n⚠️ TEST COMPLETADO CON ADVERTENCIAS")

        # Esperar para visualización
        print("\n⏳ Esperando 10 segundos para que puedas ver el resultado...")
        time.sleep(10)

    except Exception as e:
        print(f"\n❌ ERROR EN EL TEST: {e}")
        import traceback
        traceback.print_exc()

        # Esperar para visualización del error
        time.sleep(10)

    finally:
        print("\n🔚 Cerrando navegador...")
        driver.quit()
        print("="*60)

if __name__ == "__main__":
    test_passengers_selector()
