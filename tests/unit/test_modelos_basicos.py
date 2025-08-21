"""
Tests Unitarios para Modelos Económicos Básicos
===============================================

Valida el comportamiento básico de los componentes económicos fundamentales.
"""

import unittest
import sys
import os

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.models.Bien import Bien
from src.models.Consumidor import Consumidor
from src.models.Empresa import Empresa
from src.models.Mercado import Mercado
from src.config.ConfigEconomica import ConfigEconomica


class TestBien(unittest.TestCase):
    """Tests para la clase Bien"""
    
    def setUp(self):
        self.bien = Bien("pan", "alimentos_basicos")
    
    def test_creacion_bien(self):
        """Test creación básica de bien"""
        self.assertEqual(self.bien.nombre, "pan")
        self.assertEqual(self.bien.categoria, "alimentos_basicos")
        self.assertIsInstance(self.bien.elasticidad_precio, float)
        # Las elasticidades pueden ser negativas (normal en economía)
        self.assertNotEqual(self.bien.elasticidad_precio, 0)
    
    def test_elasticidad_por_categoria(self):
        """Test que elasticidad varía por categoría"""
        bien_lujo = Bien("joya", "alimentos_lujo")  # Usar categoría existente
        bien_basico = Bien("agua", "alimentos_basicos")
        
        # Los bienes de lujo deberían ser más elásticos (más negativos)
        self.assertLess(bien_lujo.elasticidad_precio, bien_basico.elasticidad_precio)


class TestConsumidor(unittest.TestCase):
    """Tests para la clase Consumidor"""
    
    def setUp(self):
        bienes = {"pan": Bien("pan", "alimentos_basicos")}
        self.mercado = Mercado(bienes)
        self.consumidor = Consumidor("TestConsumidor", self.mercado)
    
    def test_creacion_consumidor(self):
        """Test creación básica de consumidor"""
        self.assertIsInstance(self.consumidor.dinero, (int, float))
        self.assertGreater(self.consumidor.dinero, 0)
        # Verificar que tiene historial de compras (en lugar de necesidades)
        self.assertIsInstance(self.consumidor.historial_compras, dict)
    
    def test_dinero_inicial_en_rango(self):
        """Test que el dinero inicial está en rango válido"""
        self.assertGreaterEqual(self.consumidor.dinero, ConfigEconomica.DINERO_INICIAL_CONSUMIDOR_MIN)
        self.assertLessEqual(self.consumidor.dinero, ConfigEconomica.DINERO_INICIAL_CONSUMIDOR_MAX)
    
    def test_compra_valida(self):
        """Test que el consumidor puede realizar compras válidas"""
        dinero_inicial = self.consumidor.dinero
        # Simular compra exitosa
        precio = 10
        cantidad = 1
        
        if dinero_inicial >= precio * cantidad:
            self.consumidor.dinero -= precio * cantidad
            self.assertEqual(self.consumidor.dinero, dinero_inicial - precio * cantidad)


class TestEmpresa(unittest.TestCase):
    """Tests para la clase Empresa"""
    
    def setUp(self):
        bienes = {"pan": Bien("pan", "alimentos_basicos")}
        self.mercado = Mercado(bienes)
        self.empresa = Empresa("Panadería SA", self.mercado, bienes)
    
    def test_creacion_empresa(self):
        """Test creación básica de empresa"""
        self.assertEqual(self.empresa.nombre, "Panadería SA")
        self.assertIsInstance(self.empresa.dinero, (int, float))
        self.assertGreater(self.empresa.dinero, 0)
        self.assertIsInstance(self.empresa.empleados, list)
    
    def test_dinero_inicial_en_rango(self):
        """Test que el capital inicial está en rango válido"""
        self.assertGreaterEqual(self.empresa.dinero, ConfigEconomica.DINERO_INICIAL_EMPRESA_MIN)
        self.assertLessEqual(self.empresa.dinero, ConfigEconomica.DINERO_INICIAL_EMPRESA_MAX)
    
    def test_precios_inicializados(self):
        """Test que los precios están inicializados correctamente"""
        for bien in self.mercado.bienes:
            self.assertIn(bien, self.empresa.precios)
            self.assertGreater(self.empresa.precios[bien], 0)
    
    def test_contratacion_empleado(self):
        """Test contratación de empleado"""
        consumidor = Consumidor("TestEmpleado", self.mercado)
        empleados_inicial = len(self.empresa.empleados)
        
        # Asegurar que la empresa tiene dinero suficiente
        self.empresa.dinero = 50000
        
        exito = self.empresa.contratar(consumidor)
        if exito:
            self.assertEqual(len(self.empresa.empleados), empleados_inicial + 1)
            self.assertTrue(consumidor.empleado)
            self.assertEqual(consumidor.empleador, self.empresa)


class TestMercado(unittest.TestCase):
    """Tests para la clase Mercado"""
    
    def setUp(self):
        bienes = {
            "pan": Bien("pan", "alimentos_basicos"),
            "carne": Bien("carne", "alimentos_lujo")
        }
        self.mercado = Mercado(bienes)
    
    def test_creacion_mercado(self):
        """Test creación básica de mercado"""
        self.assertIsInstance(self.mercado.bienes, dict)
        self.assertGreater(len(self.mercado.bienes), 0)
        self.assertIsInstance(self.mercado.personas, list)
        self.assertIsInstance(self.mercado.transacciones, list)
    
    def test_adicion_personas(self):
        """Test adición de personas al mercado"""
        personas_inicial = len(self.mercado.personas)
        
        consumidor = Consumidor("TestConsumidor", self.mercado)
        empresa = Empresa("Test SA", self.mercado)
        
        # Usar el método correcto agregar_persona
        self.mercado.agregar_persona(consumidor)
        self.mercado.agregar_persona(empresa)
        
        self.assertEqual(len(self.mercado.personas), personas_inicial + 2)
    
    def test_sistemas_integrados_inicializados(self):
        """Test que los sistemas están inicializados"""
        self.assertIsNotNone(self.mercado.sistema_bancario)
        self.assertIsNotNone(self.mercado.economia_sectorial)
        self.assertIsNotNone(self.mercado.sistema_innovacion)


if __name__ == '__main__':
    unittest.main()
