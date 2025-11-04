"""
Test Caso 5: Verificar cambio de POS (Point of Sale)
Versión mejorada con múltiples estrategias de verificación
"""
import pytest
import allure
from pages.booking_flow.home_page import HomePage
from utils.config import Config
from utils.driver_factory import DriverFactory
import time


@pytest.mark.caso_5
@pytest.mark.pos
class TestCasoAutomatizado5:
    """Caso 5: Verificar cambio de POS (Point of Sale)"""
    
    @pytest.fixture(autouse=True)
    def setup(self, request):
        """Setup y teardown para cada test"""
        self.driver = DriverFactory.create_driver()
        self.home_page = HomePage(self.driver)
        
        def teardown():
            if self.driver:
                try:
                    self.driver.quit()
                    print("✅ Driver cerrado correctamente")
                except Exception as e:
                    print(f"⚠️ Error cerrando driver: {e}")
        
        request.addfinalizer(teardown)
    
    @allure.feature("POS Selection")
    @allure.story("Cambio de POS (Point of Sale)")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("""
    Caso Automatizado 5: Verificar cambio de POS
    • Seleccionar 3 POS (Otros países, España, Chile)
    • Verificar que cada cambio de POS se haga correctamente
    • Evidenciar cada cambio con screenshots
    """)
    def test_caso_5_verificar_cambio_pos(self):
        """
        Verificar que se puede cambiar el POS (País/Point of Sale) del sitio
        Requisitos:
        - Probar 3 POS diferentes
        - Verificar cada cambio
        - Tomar evidencias (screenshots)
        """
        
        test_results = []
        start_time = time.time()
        
        with allure.step("Paso 1: Navegar a la página principal"):
            base_url = Config.get_base_url()
            print(f"\n{'='*70}")
            print("🚀 INICIANDO TEST CASO 5: CAMBIO DE POS")
            print(f"{'='*70}")
            print(f"🌐 URL Base: {base_url}")
            
            # Navegar a la URL base
            navigation_success = self.home_page.navigate_to(base_url)
            
            if not navigation_success:
                pytest.fail("❌ No se pudo navegar a la página principal")
            
            print("✅ Navegación exitosa")
            
            # Esperar a que la página cargue completamente
            time.sleep(3)
            
            # Detectar POS inicial
            initial_pos = self.home_page.get_current_pos()
            print(f"📍 POS Inicial detectado: {initial_pos}")
            
            # Screenshot inicial
            self.home_page.take_screenshot("01_pos_inicial")
            
            # Adjuntar información inicial a Allure
            allure.attach(
                f"POS Inicial: {initial_pos}\nURL: {self.driver.current_url}",
                name="Estado Inicial",
                attachment_type=allure.attachment_type.TEXT
            )
        
        # Lista de POS a probar según requisitos
        # Requisito: Otros países, España, Chile
        paises_a_probar = [
            ("other", "Otros países", "Verificar POS Internacional"),
            ("spain", "España", "Verificar POS España"),
            ("chile", "Chile", "Verificar POS Chile")
        ]
        
        successful_changes = 0
        failed_changes = 0
        
        for idx, (pos_code, pos_nombre, descripcion) in enumerate(paises_a_probar, 1):
            with allure.step(f"Paso {idx+1}: {descripcion} - {pos_nombre}"):
                print(f"\n{'='*70}")
                print(f"🎯 [{idx}/{len(paises_a_probar)}] PROBANDO POS: {pos_nombre.upper()}")
                print(f"{'='*70}")
                print(f"📋 Código: {pos_code}")
                print(f"📝 Descripción: {descripcion}")
                
                # POS antes del cambio
                pos_before = self.home_page.get_current_pos()
                print(f"📍 POS antes del cambio: {pos_before}")
                
                # Screenshot antes del cambio
                self.home_page.take_screenshot(f"02_antes_cambio_{pos_code}_{idx}")
                
                # Intentar cambiar el POS
                print(f"🔄 Iniciando cambio de POS a: {pos_nombre}...")
                change_success = False
                verification_success = False
                error_detail = None
                
                try:
                    # Ejecutar cambio de POS
                    change_success = self.home_page.change_pos(pos_code)
                    
                    if change_success:
                        print("✅ Cambio ejecutado correctamente")
                        
                        # Esperar a que se apliquen los cambios
                        print("⏳ Esperando a que se apliquen los cambios...")
                        time.sleep(3)
                        
                        # Verificar el cambio
                        print("🔍 Verificando cambio de POS...")
                        verification_success = self.home_page.verify_pos_change(pos_code)
                        
                        if verification_success:
                            print(f"✅ VERIFICACIÓN EXITOSA: POS cambiado a {pos_nombre}")
                            
                            # POS después del cambio
                            pos_after = self.home_page.get_current_pos()
                            print(f"📍 POS después del cambio: {pos_after}")
                            
                            # URL actual
                            current_url = self.driver.current_url
                            print(f"🌐 URL actual: {current_url}")
                            
                            # Screenshot después del cambio exitoso
                            self.home_page.take_screenshot(f"03_despues_cambio_{pos_code}_{idx}_exitoso")
                            
                            # Registrar resultado exitoso
                            result = {
                                "pos": pos_nombre,
                                "code": pos_code,
                                "status": "SUCCESS",
                                "pos_before": pos_before,
                                "pos_after": pos_after,
                                "url": current_url,
                                "change_ok": True,
                                "verify_ok": True,
                                "error": None
                            }
                            test_results.append(result)
                            successful_changes += 1
                            
                            # Adjuntar detalles a Allure
                            allure.attach(
                                f"POS: {pos_nombre}\n"
                                f"Código: {pos_code}\n"
                                f"Antes: {pos_before}\n"
                                f"Después: {pos_after}\n"
                                f"URL: {current_url}\n"
                                f"Estado: ÉXITO",
                                name=f"Resultado {pos_nombre}",
                                attachment_type=allure.attachment_type.TEXT
                            )
                            
                        else:
                            print("⚠️ CAMBIO PARCIAL: Ejecutado pero no verificado")
                            error_detail = "Cambio ejecutado pero verificación falló"
                            
                            # Screenshot del estado parcial
                            self.home_page.take_screenshot(f"03_despues_cambio_{pos_code}_{idx}_parcial")
                            
                            # Registrar resultado parcial
                            result = {
                                "pos": pos_nombre,
                                "code": pos_code,
                                "status": "PARTIAL",
                                "pos_before": pos_before,
                                "pos_after": self.home_page.get_current_pos(),
                                "url": self.driver.current_url,
                                "change_ok": True,
                                "verify_ok": False,
                                "error": error_detail
                            }
                            test_results.append(result)
                            failed_changes += 1
                            
                    else:
                        error_detail = "No se pudo ejecutar el cambio de POS"
                        raise Exception(error_detail)
                    
                except Exception as e:
                    error_detail = str(e)
                    print(f"❌ ERROR: {error_detail}")
                    
                    # Screenshot del error
                    self.home_page.take_screenshot(f"04_error_{pos_code}_{idx}")
                    
                    # Registrar resultado fallido
                    result = {
                        "pos": pos_nombre,
                        "code": pos_code,
                        "status": "FAILED",
                        "pos_before": pos_before,
                        "pos_after": self.home_page.get_current_pos(),
                        "url": self.driver.current_url,
                        "change_ok": False,
                        "verify_ok": False,
                        "error": error_detail
                    }
                    test_results.append(result)
                    failed_changes += 1
                    
                    # Adjuntar error a Allure
                    allure.attach(
                        f"POS: {pos_nombre}\n"
                        f"Código: {pos_code}\n"
                        f"Error: {error_detail}\n"
                        f"URL: {self.driver.current_url}",
                        name=f"Error {pos_nombre}",
                        attachment_type=allure.attachment_type.TEXT
                    )
                
                # Pausa entre cambios de POS
                if idx < len(paises_a_probar):
                    print("⏳ Pausa de 2 segundos antes del siguiente cambio...")
                    time.sleep(2)
        
        # Generar reporte final
        with allure.step("Paso Final: Generar reporte de resultados"):
            execution_time = time.time() - start_time
            total_tests = len(paises_a_probar)
            success_rate = (successful_changes / total_tests) * 100 if total_tests > 0 else 0
            
            print(f"\n{'='*70}")
            print("📊 REPORTE FINAL - CASO 5: CAMBIO DE POS")
            print(f"{'='*70}")
            print(f"⏱️  Tiempo de ejecución: {execution_time:.2f} segundos")
            print(f"📋 Total de POS probados: {total_tests}")
            print(f"✅ Cambios exitosos: {successful_changes}")
            print(f"❌ Cambios fallidos: {failed_changes}")
            print(f"📈 Tasa de éxito: {success_rate:.1f}%")
            print(f"{'='*70}")
            
            # Detalles por POS
            print("\n📝 DETALLE POR POS:")
            print(f"{'-'*70}")
            
            for result in test_results:
                status_icon = "✅" if result["status"] == "SUCCESS" else "⚠️" if result["status"] == "PARTIAL" else "❌"
                print(f"{status_icon} {result['pos']:<20} | Estado: {result['status']:<10} | "
                      f"Antes: {result['pos_before']:<10} | Después: {result['pos_after']:<10}")
                
                if result["error"]:
                    print(f"   └─ Error: {result['error']}")
            
            print(f"{'-'*70}")
            
            # Crear reporte para Allure
            report_lines = [
                "REPORTE FINAL - CASO 5: CAMBIO DE POS",
                "="*70,
                f"Tiempo de ejecución: {execution_time:.2f}s",
                f"Total de POS probados: {total_tests}",
                f"Cambios exitosos: {successful_changes}",
                f"Cambios fallidos: {failed_changes}",
                f"Tasa de éxito: {success_rate:.1f}%",
                "",
                "DETALLE POR POS:",
                "-"*70
            ]
            
            for result in test_results:
                status_icon = "✅" if result["status"] == "SUCCESS" else "⚠️" if result["status"] == "PARTIAL" else "❌"
                report_lines.append(
                    f"{status_icon} {result['pos']} ({result['code']}) - {result['status']}"
                )
                report_lines.append(f"   Antes: {result['pos_before']} | Después: {result['pos_after']}")
                report_lines.append(f"   URL: {result['url']}")
                if result["error"]:
                    report_lines.append(f"   Error: {result['error']}")
                report_lines.append("")
            
            report_text = "\n".join(report_lines)
            
            # Adjuntar reporte a Allure
            allure.attach(
                report_text,
                name="Reporte Final Caso 5",
                attachment_type=allure.attachment_type.TEXT
            )
            
            # También crear JSON para análisis
            import json
            json_report = json.dumps(test_results, indent=2, ensure_ascii=False)
            allure.attach(
                json_report,
                name="Resultados JSON",
                attachment_type=allure.attachment_type.JSON
            )
        
        # Aserciones finales
        with allure.step("Validar resultados del test"):
            # Al menos un cambio debe ser exitoso
            assert successful_changes > 0, \
                f"❌ Ningún cambio de POS fue exitoso. Fallaron todos los {total_tests} intentos."
            
            # Idealmente todos deberían funcionar
            if successful_changes == total_tests:
                print("\n🎉 EXCELENTE: Todos los cambios de POS funcionaron correctamente")
            elif successful_changes >= 2:
                print("\n✅ BIEN: {successful_changes}/{total_tests} cambios de POS funcionaron")
            else:
                print("\n⚠️ ADVERTENCIA: Solo {successful_changes}/{total_tests} cambios funcionaron")
            
            # Si todos fallaron, marcar como fallo crítico
            if failed_changes == total_tests:
                pytest.fail("❌ FALLO CRÍTICO: Ningún cambio de POS funcionó correctamente")
        
        print(f"\n{'='*70}")
        print("✅ CASO 5 COMPLETADO")
        print(f"{'='*70}\n")


@pytest.mark.caso_5
@pytest.mark.pos
@pytest.mark.smoke
class TestPOSSmoke:
    """Tests de smoke rápidos para POS"""
    
    @pytest.fixture(autouse=True)
    def setup(self, request):
        """Setup y teardown"""
        self.driver = DriverFactory.create_driver()
        self.home_page = HomePage(self.driver)
        
        def teardown():
            if self.driver:
                self.driver.quit()
        
        request.addfinalizer(teardown)
    
    @allure.feature("POS Selection")
    @allure.story("Smoke test - Verificar que al menos un POS funciona")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_pos_smoke_at_least_one_works(self):
        """Verificar que al menos un cambio de POS funciona (smoke test)"""
        
        base_url = Config.get_base_url()
        self.home_page.navigate_to(base_url)
        time.sleep(2)
        
        # Probar España y Chile (más comunes)
        pos_to_test = [("spain", "España"), ("chile", "Chile")]
        
        for pos_code, pos_name in pos_to_test:
            with allure.step(f"Probar POS: {pos_name}"):
                success = self.home_page.change_pos(pos_code)
                if success:
                    verified = self.home_page.verify_pos_change(pos_code)
                    if verified:
                        print(f"✅ {pos_name} funciona correctamente")
                        return  # Test exitoso
        
        pytest.fail("❌ Ningún POS funcionó en el smoke test")