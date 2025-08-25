"""
Tests adicionales de configuración para mejorar cobertura
"""

import unittest
import sys
import os
import json

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.config.ConfiguradorSimulacion import ConfiguradorSimulacion


class TestConfiguradorCobertura(unittest.TestCase):
    def test_cargar_desde_archivo_relativo_y_validar(self):
        cfg = ConfiguradorSimulacion()
        contenido = {"simulacion": {"num_ciclos": 10}, "economia": {"pib_inicial": 50000}}
        ruta = "tmp_config_cov.json"
        with open(ruta, 'w', encoding='utf-8') as f:
            json.dump(contenido, f)
        try:
            ok = cfg.cargar_desde_archivo(ruta)
            self.assertTrue(ok)
            self.assertTrue(cfg.validar())
            self.assertEqual(cfg.obtener("simulacion", "num_ciclos", 0), 10)
            self.assertEqual(cfg.obtener_parametro("economia", "pib_inicial", 0), 50000)
        finally:
            os.remove(ruta)


if __name__ == '__main__':
    unittest.main()
