import shutil
import os

def clean_chromedriver():
    # Limpiar caché de WebDriver Manager
    wdm_path = os.path.expanduser("~/.wdm")
    if os.path.exists(wdm_path):
        shutil.rmtree(wdm_path)
        print("✅ Caché de WebDriver Manager limpiada")
    
    # También limpiar cualquier chromedriver.exe en el PATH
    paths = os.environ["PATH"].split(";")
    for path in paths:
        chromedriver_path = os.path.join(path, "chromedriver.exe")
        if os.path.exists(chromedriver_path):
            os.remove(chromedriver_path)
            print(f"✅ ChromeDriver removido de: {path}")

if __name__ == "__main__":
    clean_chromedriver()