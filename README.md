# 🚀 Test Automation Engineer - Prueba Técnica

Sistema completo de automatización de pruebas para plataforma de reservas de vuelos.

## 📋 Requisitos Cumplidos

### ✅ Requisitos Técnicos Obligatorios
- [x] **Allure Reports** para gestión eficiente de resultados (10 Pts)
- [x] **Registros detallados (logs)** para depuración (5 Pts) 
- [x] **Base de datos SQLite** para almacenar resultados (5 Pts)
- [x] **Compatibilidad con múltiples entornos** (UAT1 y UAT2) (5 Pts)
- [x] **Ejecución en paralelo** con pytest-xdist (5 Pts)
- [x] **Manejo robusto de aserciones** para reportes dicientes (5 Pts)

### ✅ Casos de Prueba Implementados
- [x] **Caso 1**: Booking One-way (15 Pts)
- [x] **Caso 2**: Booking Round-trip (15 Pts) 
- [x] **Caso 3**: Login en UAT (10 Pts)
- [x] **Caso 4**: Verificar cambio de idioma (5 Pts)
- [x] **Caso 5**: Verificar cambio de POS (5 Pts)
- [x] **Caso 6**: Redirecciones Header (5 Pts)
- [x] **Caso 7**: Redirecciones Footer (5 Pts)

### ✅ Características Adicionales
- [x] **Grabación de video** como evidencia (15 Pts Extra)
- [x] **Page Object Model** bien estructurado
- [x] **Múltiples navegadores** soportados
- [x] **Configuración centralizada**
- [x] **Manejo de errores robusto**
- [x] **Screenshots automáticos**

## 🛠️ Instalación y Configuración

### Prerrequisitos

#### Windows
```bash
# 1. Instalar Python 3.8+
# Descargar desde: https://www.python.org/downloads/

# 2. Instalar Git
# Descargar desde: https://git-scm.com/download/win

# 3. Verificar instalación
python --version
pip --version
git --version

###### MAC 
# 1. Instalar Homebrew (si no está instalado)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Instalar Python
brew install python

# 3. Instalar Git
brew install git

# 4. Verificar instalación
python3 --version
pip3 --version
git --version

#### Configuración del proyecto 

# 1. Clonar el repositorio
git clone <repository-url>
cd test-automation-engineer

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno virtual
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Instalar Allure (requiere Java 8+)
# Windows: Usar scoop
scoop install allure

# macOS: Usar brew
brew install allure

# 6. Verificar instalación
allure --version

##### ejecucion de pruebas 

# Ejecutar todos los tests
python run_tests.py --test-type=all --generate-report --open-report

# Ejecutar tests de regresión
python run_tests.py --test-type=regression --headless

# Ejecutar caso específico
python run_tests.py --test-type=caso_1 --browser=firefox

# Ejecutar en entorno UAT2
python run_tests.py --test-type=all --env=uat2

# Ejecutar con más workers
python run_tests.py --test-type=all --workers=4

#### Opción 2: Usar pytest directamente

# Ejecutar todos los tests
pytest tests/ -v -n 2 --alluredir=allure-results

# Ejecutar caso específico
pytest tests/test_caso_1.py -v --alluredir=allure-results

# Ejecutar con marcadores
pytest -m "caso_1 or caso_2" -v -n 2 --alluredir=allure-results

# Ejecutar en modo headless
pytest tests/ -v --headless --alluredir=allure-results

####               Ejecucion selectiva 
# Solo casos de regresión
pytest -m regression -v -n 2

# Solo un caso específico
pytest -m caso_1 -v

# Smoke tests
pytest -m smoke -v

### Generara reporte de aAllure
# Generar reporte
allure generate allure-results --clean -o allure-report

# Abrir reporte
allure open allure-report
