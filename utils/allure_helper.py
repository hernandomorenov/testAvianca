import allure
import json
import os
from datetime import datetime


class AllureHelper:
    """Helper para gestionar reportes de Allure"""
    
    @staticmethod
    def attach_screenshot(driver, name):
        """Adjuntar screenshot a Allure"""
        try:
            screenshot_path = f"screenshots/{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            driver.save_screenshot(screenshot_path)
            allure.attach.file(screenshot_path, name=name, attachment_type=allure.attachment_type.PNG)
            return True
        except Exception as e:
            print(f"⚠️ Error adjuntando screenshot: {e}")
            return False
    
    @staticmethod
    def attach_text(content, name):
        """Adjuntar texto a Allure"""
        try:
            allure.attach(content, name=name, attachment_type=allure.attachment_type.TEXT)
            return True
        except Exception as e:
            print(f"⚠️ Error adjuntando texto: {e}")
            return False
    
    @staticmethod
    def attach_json(data, name):
        """Adjuntar JSON a Allure"""
        try:
            if isinstance(data, dict):
                data = json.dumps(data, indent=2, ensure_ascii=False)
            allure.attach(data, name=name, attachment_type=allure.attachment_type.JSON)
            return True
        except Exception as e:
            print(f"⚠️ Error adjuntando JSON: {e}")
            return False
    
    @staticmethod
    def attach_html(html_content, name):
        """Adjuntar HTML a Allure"""
        try:
            allure.attach(html_content, name=name, attachment_type=allure.attachment_type.HTML)
            return True
        except Exception as e:
            print(f"⚠️ Error adjuntando HTML: {e}")
            return False
    
    @staticmethod
    def create_environment_properties():
        """Crear archivo de propiedades de entorno para Allure"""
        env_properties = {
            "Browser": "Chrome",
            "Environment": "UAT",
            "Python.Version": "3.8+",
            "Selenium.Version": "4.15.0",
            "Test.Framework": "pytest",
            "Parallel.Execution": "pytest-xdist"
        }
        
        with open("allure-results/environment.properties", "w") as f:
            for key, value in env_properties.items():
                f.write(f"{key}={value}\n")