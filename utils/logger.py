"""
Módulo de logging centralizado para las pruebas
"""
import logging
import os
from datetime import datetime


def setup_logger(name='avianca_tests', level=logging.INFO):
    """
    Configurar logger con formato detallado

    Args:
        name: Nombre del logger
        level: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        Logger configurado
    """
    # Crear directorio de logs si no existe
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Crear logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Evitar duplicación de handlers
    if logger.handlers:
        return logger

    # Formato detallado para archivo
    file_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Formato simple para consola
    console_formatter = logging.Formatter(
        '%(levelname)-8s | %(message)s'
    )

    # Handler para archivo (todos los niveles)
    log_filename = os.path.join(log_dir, f'test_execution_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Handler para archivo de errores (solo errores y críticos)
    error_filename = os.path.join(log_dir, f'test_errors_{datetime.now().strftime("%Y%m%d")}.log')
    error_handler = logging.FileHandler(error_filename, encoding='utf-8')
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(file_formatter)
    logger.addHandler(error_handler)

    # Handler para consola (INFO y superiores)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    logger.info(f"Logger inicializado. Archivo de log: {log_filename}")

    return logger


def get_logger(name='avianca_tests'):
    """
    Obtener logger existente o crear uno nuevo

    Args:
        name: Nombre del logger

    Returns:
        Logger configurado
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        return setup_logger(name)
    return logger
