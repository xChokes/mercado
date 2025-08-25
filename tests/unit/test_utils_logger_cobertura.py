"""
Tests adicionales para SimuladorLogger para aumentar cobertura
"""

import unittest
import sys
import os
import logging
import glob

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.utils.SimuladorLogger import SimuladorLogger, get_simulador_logger, init_logging, close_logging


class TestSimuladorLoggerCobertura(unittest.TestCase):
    def setUp(self):
        # Usar un directorio temporal de logs
        self.logger = SimuladorLogger(log_dir="test_logs", log_level=logging.DEBUG)

    def tearDown(self):
        # Cerrar y limpiar
        self.logger.close()
        for f in glob.glob('test_logs/*.log'):
            os.remove(f)
        if os.path.exists('test_logs'):
            os.rmdir('test_logs')

    def test_get_logger_component(self):
        banco_logger = self.logger.get_logger('Banco')
        self.assertIsNotNone(banco_logger)
        banco_logger.info("msg test banco")

    def test_logs_basicos(self):
        self.logger.log_inicio("arranque")
        self.logger.log_configuracion("cfg")
        self.logger.log_ciclo_inicio(1)
        self.logger.log_metricas_ciclo(1, 100000, 0.02, 0.1, 50)
        self.logger.log_ciclo_fin(1, 0.123)
        self.logger.log_crisis("crisis")
        self.logger.log_precios("precio ok")
        self.logger.log_metricas("kpis")
        self.logger.log_reporte("reporte")
        self.logger.log_fin("fin")
        self.logger.log_warning('Mercado', 'warn')
        self.logger.log_error('err')
        self.logger.log_error_with_component('Banco', 'err2')

    def test_singleton_helpers(self):
        lg = get_simulador_logger()
        self.assertIsNotNone(lg)
        lg2 = init_logging()
        self.assertIsNotNone(lg2)
        close_logging()


if __name__ == '__main__':
    unittest.main()
