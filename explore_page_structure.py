"""
Script para explorar la estructura real de la página y encontrar selectores correctos
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import json


def explore_avianca_page():
    """Explorar la estructura completa de la página de Avianca"""
    
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    driver = webdriver.Chrome(options=options)
    
    try:
        print("🔍 Explorando estructura de la página Avianca...")
        driver.get("https://nuxqa4.avtest.ink/es/")
        time.sleep(5)
        
        # Explorar diferentes secciones de la página
        sections = {
            "inputs": [
                "//input", 
                "//input[@placeholder]",
                "//input[@type='text']",
                "//input[contains(@class, 'input')]"
            ],
            "buttons": [
                "//button",
                "//button[contains(text(), 'Buscar')]",
                "//button[contains(text(), 'Search')]",
                "//a[contains(@class, 'button')]"
            ],
            "selects": [
                "//select",
                "//div[contains(@class, 'select')]",
                "//div[contains(@class, 'dropdown')]"
            ],
            "language_elements": [
                "//*[contains(text(), 'ES')]",
                "//*[contains(text(), 'EN')]", 
                "//*[contains(text(), 'FR')]",
                "//*[contains(text(), 'PT')]",
                "//*[contains(@class, 'language')]",
                "//*[contains(@class, 'lang')]"
            ],
            "forms": [
                "//form",
                "//div[contains(@class, 'form')]",
                "//div[contains(@class, 'booking')]"
            ]
        }
        
        found_elements = {}
        
        for section, selectors in sections.items():
            print(f"\n📂 SECCIÓN: {section.upper()}")
            print("-" * 40)
            
            found_elements[section] = []
            
            for selector in selectors:
                try:
                    elements = driver.find_elements(By.XPATH, selector)
                    if elements:
                        print(f"✅ {selector}")
                        for i, elem in enumerate(elements[:3]):  # Mostrar solo primeros 3
                            element_info = {
                                "selector": selector,
                                "tag": elem.tag_name,
                                "text": elem.text[:50] if elem.text else "",
                                "visible": elem.is_displayed(),
                                "enabled": elem.is_enabled(),
                                "attributes": get_element_attributes(elem)
                            }
                            found_elements[section].append(element_info)
                            
                            print(f"   {i+1}. Tag: {elem.tag_name}")
                            print(f"      Texto: '{elem.text[:30]}...'")
                            print(f"      Visible: {elem.is_displayed()}")
                            print(f"      Atributos: {element_info['attributes']}")
                            
                    else:
                        print(f"❌ {selector} - No encontrado")
                        
                except Exception as e:
                    print(f"⚠️ {selector} - Error: {e}")
        
        # Guardar resultados en archivo
        with open("page_structure.json", "w", encoding="utf-8") as f:
            json.dump(found_elements, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Estructura guardada en: page_structure.json")
        
        # Tomar screenshot completo
        driver.save_screenshot("page_exploration.png")
        print("📸 Screenshot guardado: page_exploration.png")
        
        return found_elements
        
    except Exception as e:
        print(f"❌ Error en exploración: {e}")
        return None
        
    finally:
        driver.quit()


def get_element_attributes(element):
    """Obtener atributos importantes de un elemento"""
    attributes = {}
    try:
        common_attrs = ["id", "name", "class", "type", "placeholder", "value", "href"]
        for attr in common_attrs:
            value = element.get_attribute(attr)
            if value:
                attributes[attr] = value
    except:
        pass
    return attributes


def find_best_selectors(found_elements):
    """Encontrar los mejores selectores basados en la exploración"""
    print("\n🎯 ANALIZANDO MEJORES SELECTORES")
    print("=" * 50)
    
    best_selectors = {}
    
    # Buscar input de origen
    origin_inputs = [e for e in found_elements.get("inputs", []) 
                    if "origen" in e.get("attributes", {}).get("placeholder", "").lower() 
                    or "from" in e.get("attributes", {}).get("placeholder", "").lower()]
    
    if origin_inputs:
        best_selectors["ORIGIN_INPUT"] = origin_inputs[0]["selector"]
        print(f"✅ Input Origen: {origin_inputs[0]['selector']}")
    
    # Buscar input de destino
    destination_inputs = [e for e in found_elements.get("inputs", []) 
                         if "destino" in e.get("attributes", {}).get("placeholder", "").lower()
                         or "to" in e.get("attributes", {}).get("placeholder", "").lower()]
    
    if destination_inputs:
        best_selectors["DESTINATION_INPUT"] = destination_inputs[0]["selector"]
        print(f"✅ Input Destino: {destination_inputs[0]['selector']}")
    
    # Buscar botón de búsqueda
    search_buttons = [e for e in found_elements.get("buttons", []) 
                     if "buscar" in e.get("text", "").lower() 
                     or "search" in e.get("text", "").lower()]
    
    if search_buttons:
        best_selectors["SEARCH_BUTTON"] = search_buttons[0]["selector"]
        print(f"✅ Botón Buscar: {search_buttons[0]['selector']}")
    
    # Buscar elementos de idioma
    language_elements = found_elements.get("language_elements", [])
    if language_elements:
        for elem in language_elements[:4]:  # Primeros 4 elementos de idioma
            lang = "UNKNOWN"
            if "es" in elem.get("text", "").lower():
                lang = "SPANISH"
            elif "en" in elem.get("text", "").lower():
                lang = "ENGLISH"
            elif "fr" in elem.get("text", "").lower():
                lang = "FRENCH"
            elif "pt" in elem.get("text", "").lower():
                lang = "PORTUGUESE"
            
            if lang != "UNKNOWN":
                best_selectors[f"LANGUAGE_{lang}"] = elem["selector"]
                print(f"✅ Idioma {lang}: {elem['selector']}")
    
    return best_selectors


if __name__ == "__main__":
    print("=" * 60)
    print("🔍 EXPLORADOR DE ESTRUCTURA DE PÁGINA AVIANCA")
    print("=" * 60)
    
    structure = explore_avianca_page()
    
    if structure:
        best_selectors = find_best_selectors(structure)
        
        print(f"\n🎉 SELECTORES ENCONTRADOS: {len(best_selectors)}")
        for key, selector in best_selectors.items():
            print(f"   {key}: {selector}")
        
        # Guardar selectores optimizados
        with open("optimized_selectors.py", "w", encoding="utf-8") as f:
            f.write("# SELECTORES OPTIMIZADOS PARA AVIANCA\n")
            f.write("# Generados automáticamente por explore_page_structure.py\n\n")
            f.write("from selenium.webdriver.common.by import By\n\n")
            f.write("class OptimizedSelectors:\n")
            for key, selector in best_selectors.items():
                f.write(f'    {key} = (By.XPATH, "{selector}")\n')
        
        print(f"\n💾 Selectores guardados en: optimized_selectors.py")
    
    print("\n" + "=" * 60)
    print("✅ EXPLORACIÓN COMPLETADA")
    print("=" * 60)