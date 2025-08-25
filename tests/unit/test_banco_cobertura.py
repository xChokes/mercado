"""
Tests adicionales para Banco/SistemaBancario para elevar cobertura focalizada
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.systems.SistemaBancario import Banco, SistemaBancario
from src.models.Mercado import Mercado
from src.models.Bien import Bien


class PersonaDummy:
    def __init__(self, nombre, dinero=10000, empleado=True, ingreso_mensual=3000, deuda=0, ahorros=2000):
        self.nombre = nombre
        self.dinero = dinero
        self.empleado = empleado
        self.ingreso_mensual = ingreso_mensual
        self.deuda = deuda
        self.ahorros = ahorros


class TestBancoCobertura(unittest.TestCase):
    def setUp(self):
        bienes = {"comida": Bien("comida", "alimentos_basicos")}
        self.mercado = Mercado(bienes)
        self.banco = Banco("Banco Test", 1_000_000)
        self.persona = PersonaDummy("Ana")

    def test_depositar_y_retirar(self):
        saldo_inicial = self.persona.dinero
        self.banco.depositar(self.persona, 500)
        self.assertLess(self.persona.dinero, saldo_inicial)
        exito = self.banco.retirar(self.persona, 200)
        self.assertTrue(exito)

    def test_calcular_tasa_prestamo_por_riesgo(self):
        tasa = self.banco.calcular_tasa_prestamo(0.7)
        self.assertIsInstance(tasa, float)
        self.assertGreaterEqual(tasa, 0.03)

    def test_otorgar_prestamo_firmas(self):
        # Firma kwargs básica
        p = self.banco.otorgar_prestamo(prestatario=self.persona, monto=1000, tasa_interes=0.1, plazo_meses=6)
        self.assertIsNotNone(p)
        # Firma (monto, tasa)
        p2 = self.banco.otorgar_prestamo(5000, 0.12)
        self.assertIn('tasa_anual', p2)

    def test_cobrar_cuotas_y_estadisticas(self):
        # Crear préstamo simple avanzado (usando objeto)
        aprobado, msg = self.banco.solicitar_prestamo(self.persona, 2000, plazo_meses=6)
        # Puede no aprobar, pero el método debe retornar tupla
        self.assertIsInstance(aprobado, bool)
        morosos, pagos = self.banco.cobrar_cuotas()
        stats = self.banco.obtener_estadisticas()
        self.assertIn('capital', stats)
        self.assertIn('reservas', stats)


class TestSistemaBancarioCobertura(unittest.TestCase):
    def setUp(self):
        bienes = {"comida": Bien("comida", "alimentos_basicos")}
        self.mercado = Mercado(bienes)
        self.sistema = SistemaBancario(self.mercado)

    def test_ciclo_bancario_y_estadisticas(self):
        res = self.sistema.ciclo_bancario()
        self.assertIn('bancos_activos', res)
        stats = self.sistema.obtener_estadisticas_sistema()
        self.assertIn('capital_total', stats)
        self.assertIn('tasa_referencia', stats)


if __name__ == '__main__':
    unittest.main()
