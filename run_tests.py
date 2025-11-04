"""
Script principal para ejecutar las pruebas automatizadas
"""
import subprocess
import sys
import os
import argparse
from utils.allure_helper import AllureHelper


def run_tests(test_type=None, browser="chrome", headless=False, env="uat1", workers=2):
    """Ejecutar pruebas según los parámetros especificados"""
    
    # Comando base de pytest
    base_cmd = [
        "pytest", 
        "-v",
        "--alluredir=allure-results",
        f"-n={workers}"
    ]
    
    # Agregar opciones según parámetros
    if browser:
        base_cmd.append(f"--browser={browser}")
    
    if headless:
        base_cmd.append("--headless")
    
    if env:
        base_cmd.append(f"--env={env}")
    
    # Agregar marcadores según tipo de test
    if test_type == "all":
        base_cmd.append("-m")
        base_cmd.append("caso_1 or caso_2 or caso_3 or caso_4 or caso_5 or caso_6 or caso_7")
    elif test_type == "regression":
        base_cmd.append("-m")
        base_cmd.append("regression")
    elif test_type == "smoke":
        base_cmd.append("-m")
        base_cmd.append("smoke")
    elif test_type and test_type.startswith("caso_"):
        base_cmd.append("-m")
        base_cmd.append(test_type)
    else:
        # Ejecutar todos los tests por defecto
        base_cmd.append("tests/")
    
    print(f"\n🚀 Ejecutando pruebas: {test_type or 'todos los tests'}")
    print(f"📋 Comando: {' '.join(base_cmd)}")
    print("=" * 60)
    
    # Ejecutar pruebas
    result = subprocess.run(base_cmd)
    
    return result.returncode


def generate_allure_report():
    """Generar reporte de Allure"""
    print("\n📊 Generando reporte de Allure...")
    
    # Generar reporte
    result = subprocess.run(["allure", "generate", "allure-results", "--clean", "-o", "allure-report"])
    
    if result.returncode == 0:
        print("✅ Reporte de Allure generado exitosamente")
        print("📁 Reporte disponible en: allure-report/index.html")
    else:
        print("❌ Error generando reporte de Allure")
    
    return result.returncode


def open_allure_report():
    """Abrir reporte de Allure en el navegador"""
    print("\n🌐 Abriendo reporte de Allure...")
    subprocess.run(["allure", "open", "allure-report"])


def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description="Ejecutor de pruebas automatizadas")
    
    parser.add_argument("--test-type", choices=["all", "regression", "smoke", "caso_1", "caso_2", "caso_3", "caso_4", "caso_5", "caso_6", "caso_7"],
                       help="Tipo de tests a ejecutar")
    parser.add_argument("--browser", choices=["chrome", "firefox"], default="chrome",
                       help="Navegador para ejecutar las pruebas")
    parser.add_argument("--headless", action="store_true",
                       help="Ejecutar en modo headless")
    parser.add_argument("--env", choices=["uat1", "uat2"], default="uat1",
                       help="Entorno de pruebas")
    parser.add_argument("--workers", type=int, default=2,
                       help="Número de workers para ejecución paralela")
    parser.add_argument("--generate-report", action="store_true",
                       help="Generar reporte de Allure después de las pruebas")
    parser.add_argument("--open-report", action="store_true",
                       help="Abrir reporte de Allure después de generarlo")
    
    args = parser.parse_args()
    
    # Crear directorios necesarios
    os.makedirs("allure-results", exist_ok=True)
    os.makedirs("screenshots", exist_ok=True)
    os.makedirs("videos", exist_ok=True)
    os.makedirs("database", exist_ok=True)
    
    # Crear propiedades de entorno para Allure
    AllureHelper.create_environment_properties()
    
    # Ejecutar pruebas
    return_code = run_tests(
        test_type=args.test_type,
        browser=args.browser,
        headless=args.headless,
        env=args.env,
        workers=args.workers
    )
    
    # Generar reporte si se solicita
    if args.generate_report or args.open_report:
        generate_allure_report()
    
    # Abrir reporte si se solicita
    if args.open_report:
        open_allure_report()
    
    # Retornar código de salida
    sys.exit(return_code)


if __name__ == "__main__":
    main()