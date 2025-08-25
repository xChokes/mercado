"""
Tests para cubrir rutas del CalibradorEconomicoRealista y datos reales
"""

import unittest
import sys
import os

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.config.DatosEconomicosReales import CalibradorEconomicoRealista, BENCHMARKS_HISTORICOS


class TestCalibradorCobertura(unittest.TestCase):
    def setUp(self):
        self.cal = CalibradorEconomicoRealista()

    def test_generar_rangos_validacion_estrictos(self):
        rangos = self.cal.generar_rangos_validacion_estrictos()
        self.assertIn('inflacion', rangos)
        self.assertIn('desempleo', rangos)

    def test_detectar_regimenes(self):
        casos = [
            ({'inflacion': 0.07, 'crecimiento_pib': 0.01, 'desempleo': 0.03}, 'ESTANFLACION'),
            ({'inflacion': 0.01, 'crecimiento_pib': -0.06, 'desempleo': 0.16}, 'DEPRESION'),
            ({'inflacion': 0.05, 'crecimiento_pib': -0.03, 'desempleo': 0.12}, 'RECESION_SEVERA'),
            ({'inflacion': 0.02, 'crecimiento_pib': -0.01, 'desempleo': 0.09}, 'RECESION_LEVE'),
            ({'inflacion': 0.05, 'crecimiento_pib': 0.05, 'desempleo': 0.05}, 'CRECIMIENTO_FUERTE'),
            ({'inflacion': 0.02, 'crecimiento_pib': 0.02, 'desempleo': 0.06}, 'NORMAL'),
        ]
        for ind, esperado in casos:
            self.assertEqual(self.cal.detectar_regimen_economico(ind), esperado)

    def test_sugerir_politicas_por_regimen(self):
        for regimen in ['DEPRESION','RECESION_SEVERA','RECESION_LEVE','ESTANFLACION','SOBRECALENTAMIENTO','CRECIMIENTO_FUERTE','NORMAL','DESCONOCIDO']:
            pol = self.cal.sugerir_politicas_por_regimen(regimen)
            self.assertIn('politica_monetaria', pol)
            self.assertIn('tasas_sugeridas', pol)

    def test_calibrar_configuracion_base(self):
        base = {
            'economia': {}, 'sistema_bancario': {}, 'mercado_laboral': {}, 'precios': {}
        }
        out = self.cal.calibrar_configuracion_base(base)
        self.assertIn('tasa_inflacion_objetivo', out['economia'])
        self.assertIn('tasa_interes_base', out['sistema_bancario'])

    def test_benchmarks_hist(self):
        self.assertIn('crisis_2008', BENCHMARKS_HISTORICOS)


if __name__ == '__main__':
    unittest.main()
