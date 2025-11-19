"""
Script de diagnóstico para problemas de navegación
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests


def test_network_connectivity():
    """Verificar conectividad de red"""
    print("🔍 Verificando conectividad de red...")
    
    test_urls = [
        "https://nuxqa3.avtest.ink/",
        "https://nuxqa4.avtest.ink/",
        "https://nuxqa5.avtest.ink/",
        ]
    
    for url in test_urls:
        try:
            response = requests.get(url, timeout=7)
            print(f"✅ {url} - Status: {response.status_code}")
        except Exception as e:
            print(f"❌ {url} - Error: {e}")


def test_browser_navigation():
    """Verificar navegación del navegador"""
    print("\n🔍 Verificando navegación del navegador...")
    
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    driver = None
    
    try:
        driver = webdriver.Chrome(options=options)
        
        test_urls = [
            "https://nuxqa4.avtest.ink/",
            "https://nuxqa4.avtest.ink/es/",
            "https://nuxqa4.avtest.ink/en/"
        ]
        
        for url in test_urls:
            print(f"\n🌐 Probando: {url}")
            try:
                driver.get(url)
                
                # Esperar carga
                WebDriverWait(driver, 15).until(
                    lambda d: d.execute_script("return document.readyState") == "complete"
                )
                
                time.sleep(2)
                
                # Verificar elementos básicos
                current_url = driver.current_url
                title = driver.title
                print(f"✅ Cargado - URL: {current_url}")
                print(f"📄 Título: {title}")
                
                # Verificar que la página tiene contenido
                page_source = driver.page_source
                if len(page_source) > 1000:
                    print("✅ La página tiene contenido suficiente")
                else:
                    print("⚠️ La página podría no haber cargado completamente")
                
                # Tomar screenshot
                driver.save_screenshot(f"diagnostic_{url.split('//')[1].replace('/', '_')}.png")
                
            except Exception as e:
                print(f"❌ Error: {e}")
                continue
                
    except Exception as e:
        print(f"❌ Error general del navegador: {e}")
        
    finally:
        if driver:
            driver.quit()


def test_element_selectors():
    """Verificar que los selectores funcionan"""
    print("\n🔍 Verificando selectores de elementos...")
    
    options = Options()
    options.add_argument("--start-maximized")
    
    driver = None
    
    try:
        driver = webdriver.Chrome(options=options)
        driver.get("https://nuxqa4.avtest.ink/es/")
        
        time.sleep(5)
        
        # Probar selectores comunes
        selectors_to_test = [
            ("//input[contains(@placeholder, 'Origen')]", "Input Origen"),
            ("//input[contains(@placeholder, 'Destino')]", "Input Destino"),
            ("//button[contains(text(), 'Buscar')]", "Botón Buscar"),
            ("//select[contains(@id, 'language')]", "Selector Idioma"),
            ("//select[contains(@id, 'country')]", "Selector País")
        ]
        
        for selector, description in selectors_to_test:
            try:
                elements = driver.find_elements(By.XPATH, selector)
                if elements:
                    print(f"✅ {description} - Encontrado ({len(elements)} elementos)")
                    for elem in elements[:2]:  # Mostrar primeros 2
                        print(f"   - Texto: '{elem.text}', Visible: {elem.is_displayed()}")
                else:
                    print(f"❌ {description} - No encontrado")
            except Exception as e:
                print(f"❌ {description} - Error: {e}")
                
    except Exception as e:
        print(f"❌ Error en prueba de selectores: {e}")
        
    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    print("=" * 60)
    print("🔧 DIAGNÓSTICO DE NAVEGACIÓN")
    print("=" * 60)
    
    test_network_connectivity()
    test_browser_navigation()
    test_element_selectors()
    
    print("\n" + "=" * 60)
    print("✅ DIAGNÓSTICO COMPLETADO")
    print("=" * 60)