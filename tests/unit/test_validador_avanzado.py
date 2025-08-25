"""
Tests avanzados para ValidadorEconomico para aumentar cobertura
"""

import unittest
import sys
import os

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.systems.ValidadorEconomico import ValidadorEconomico, TipoAlerta


class MercadoDummy:
    def __init__(self):
        # Series históricas
        self.inflacion_historica = [0.02] * 8 + [0.03, 0.025]
        self.pib_historico = [100000, 101000, 102000, 101500, 103000, 104000, 104500, 105000, 105800, 106500, 107200]
        self.desempleo_historico = [0.08, 0.079, 0.078, 0.077, 0.076, 0.075, 0.074, 0.073, 0.072, 0.071]

        # Personas con precios para anomalías
        self.personas = [type('Vendedor', (), {'precios': {'comida': 10, 'ropa': 100}})(),
                         type('Vendedor', (), {'precios': {'lujo': 15000, 'gratis': 0}})()]

        # Empresas y consumidores para métricas avanzadas
        self.empresas = [type('Empresa', (), {'ingresos_totales': 10000})(),
                         type('Empresa', (), {'ingresos_totales': 30000})()]
        self.consumidores = [type('Consumidor', (), {'dinero': 1000})(),
                              type('Consumidor', (), {'dinero': 2000})(),
                              type('Consumidor', (), {'dinero': 500})()]

        # Magnitudes macro
        self.pib_total = 200000
        self.masa_monetaria = 100000
        self.deuda_total = 80000


class TestValidadorAvanzado(unittest.TestCase):
    def setUp(self):
        self.validador = ValidadorEconomico()
        self.mercado = MercadoDummy()

    def test_calcular_indice_estabilidad_con_dict(self):
        datos = {'inflacion': 0.03, 'desempleo': 0.07, 'crecimiento_pib': 0.02}
        indice = self.validador.calcular_indice_estabilidad(datos)
        self.assertIsInstance(indice, float)
        self.assertGreaterEqual(indice, 0.0)
        self.assertLessEqual(indice, 1.0)

    def test_calcular_indice_estabilidad_con_mercado(self):
        indice = self.validador.calcular_indice_estabilidad(self.mercado, ventana_ciclos=5)
        self.assertGreater(indice, 0.0)

    def test_generar_reporte_validacion(self):
        reporte = self.validador.generar_reporte_validacion(self.mercado, ciclo=10)
        self.assertIsInstance(reporte, str)
        self.assertIn("REPORTE DE VALIDACIÓN ECONÓMICA", reporte)

    def test_detectar_anomalias_precios(self):
        alertas = self.validador.detectar_anomalias_precios(self.mercado, ciclo=1)
        # Debe detectar precio extremo (>10000) y no válido (<=0)
        tipos = [a.tipo for a in alertas]
        self.assertTrue(any(t in (TipoAlerta.CRITICA, TipoAlerta.ADVERTENCIA) for t in tipos))

    def test_calcular_metricas_avanzadas(self):
        metricas = self.validador.calcular_metricas_avanzadas(self.mercado)
        self.assertIn('velocidad_dinero', metricas)
        self.assertIn('ratio_deuda_pib', metricas)
        self.assertIn('indice_herfindahl', metricas)
        self.assertIn('indice_gini', metricas)
        self.assertGreaterEqual(metricas['indice_herfindahl'], 0.0)

    def test_obtener_alertas_recientes_vacio(self):
        recientes = self.validador.obtener_alertas_recientes(ultimos_ciclos=3)
        self.assertIsInstance(recientes, list)


if __name__ == '__main__':
    unittest.main()
