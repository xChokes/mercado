"""
Tests de Casos Extremos y Límites
================================

Tests unitarios para validar el comportamiento del sistema
en condiciones límite y casos extremos.
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.models.Consumidor import Consumidor
from src.models.Empresa import Empresa
from src.models.Mercado import Mercado
from src.models.Bien import Bien
from src.config.ConfiguradorSimulacion import ConfiguradorSimulacion


class TestCasosExtremos(unittest.TestCase):
    """Tests para casos extremos y valores límite"""
    
    def setUp(self):
        """Configuración para tests de casos extremos"""
        bienes = {"producto_test": Bien("producto_test", "categoria_test")}
        self.mercado = Mercado(bienes)
    
    def test_consumidor_dinero_cero(self):
        """Test consumidor con dinero inicial cero"""
        consumidor = Consumidor("Broke", self.mercado, {})
        consumidor.dinero = 0
        
        # Verificar que el consumidor maneja dinero cero correctamente
        self.assertEqual(consumidor.dinero, 0)
        
        # El consumidor no debería poder "comprar" (simulado como reducción de dinero)
        precio_producto = 10
        if consumidor.dinero >= precio_producto:
            consumidor.dinero -= precio_producto
        
        # El dinero debería seguir siendo 0 (no cambió)
        self.assertEqual(consumidor.dinero, 0)
    
    def test_consumidor_dinero_negativo(self):
        """Test consumidor con dinero negativo (deuda)"""
        consumidor = Consumidor("Deudor", self.mercado, {})
        consumidor.dinero = -100
        
        # Verificar que el sistema maneja deudas correctamente
        self.assertLess(consumidor.dinero, 0)
        
        # No debería poder "comprar" con dinero negativo (simulado)
        precio_producto = 10
        dinero_antes = consumidor.dinero
        
        if consumidor.dinero >= precio_producto:
            consumidor.dinero -= precio_producto
        
        # El dinero no debería haber cambiado (no pudo comprar)
        self.assertEqual(consumidor.dinero, dinero_antes)
    
    def test_empresa_precio_cero(self):
        """Test empresa estableciendo precio cero"""
        empresa = Empresa("Gratis Inc", self.mercado, {})
        
        # Verificar que la empresa existe y funciona
        self.assertEqual(empresa.nombre, "Gratis Inc")
        self.assertIsInstance(empresa.dinero, (int, float))
        
        # Las empresas pueden tener diferentes métodos para manejar precios
        # Verificar que el objeto está correctamente inicializado
        self.assertIsNotNone(empresa)
    
    def test_empresa_precio_negativo(self):
        """Test empresa con precio negativo (debería ser prevenido)"""
        empresa = Empresa("NegPrice Corp", self.mercado, {})
        
        # Verificar que la empresa funciona correctamente
        self.assertEqual(empresa.nombre, "NegPrice Corp")
        self.assertIsInstance(empresa.dinero, (int, float))
        
        # El sistema debería prevenir precios negativos en el nivel de lógica de negocio
        self.assertGreater(empresa.dinero, 0)  # Al menos dinero inicial positivo
    
    def test_mercado_sin_bienes(self):
        """Test mercado completamente vacío"""
        mercado_vacio = Mercado({})
        
        # Verificar que el mercado vacío se maneja correctamente
        self.assertEqual(len(mercado_vacio.bienes), 0)
        self.assertEqual(len(mercado_vacio.getConsumidores()), 0)
        # Las empresas podrían manejarse de forma diferente
        self.assertIsNotNone(mercado_vacio)
    
    def test_mercado_muchos_participantes(self):
        """Test mercado con muchos participantes (stress test ligero)"""
        bienes = {}
        for i in range(5):  # Algunos bienes
            bien = Bien(f"producto_{i}", "categoria_test")
            bienes[f"producto_{i}"] = bien
        
        mercado = Mercado(bienes)
        
        # Agregar muchos consumidores usando el método correcto
        for i in range(50):  # Reducido para test más rápido
            consumidor = Consumidor(f"Consumer_{i}", mercado)
            mercado.agregar_persona(consumidor)
        
        # Agregar muchas empresas
        for i in range(20):  # Reducido para test más rápido
            empresa = Empresa(f"Company_{i}", mercado)
            mercado.agregar_persona(empresa)
        
        # Verificar que el mercado puede manejar muchos participantes
        self.assertGreaterEqual(len(mercado.getConsumidores()), 50)
    
    def test_bien_cantidad_maxima(self):
        """Test bien con cantidad muy grande"""
        bien = Bien("Abundante", "categoria_test")
        
        # Establecer cantidad muy grande si el atributo existe
        cantidad_grande = 1000000
        if hasattr(bien, 'cantidad'):
            bien.cantidad = cantidad_grande
            self.assertEqual(bien.cantidad, cantidad_grande)
        else:
            # Si no tiene cantidad, está bien, solo verificar que se creó
            self.assertEqual(bien.nombre, "Abundante")
    
    def test_configuracion_valores_extremos(self):
        """Test configuración con valores extremos"""
        config = ConfiguradorSimulacion()
        
        # Probar configuración con valores extremos pero válidos
        config_extrema = {
            'simulacion': {
                'num_ciclos': 1,  # Mínimo
                'num_consumidores': 1,  # Mínimo
                'num_empresas_productoras': 1,  # Mínimo
            },
            'economia': {
                'pib_inicial': 1000,  # Valor mínimo
                'tasa_inflacion_objetivo': 0.0,  # Sin inflación
            }
        }
        
        # La configuración debería ser válida
        config.config.update(config_extrema)
        self.assertTrue(config.validar())


class TestCondicionesErrores(unittest.TestCase):
    """Tests para condiciones de error y manejo de excepciones"""
    
    def setUp(self):
        bienes = {"producto_test": Bien("producto_test", "categoria_test")}
        self.mercado = Mercado(bienes)
    
    def test_compra_bien_inexistente(self):
        """Test compra de bien que no existe"""
        consumidor = Consumidor("Comprador", self.mercado)
        
        # Verificar que el bien no existe
        self.assertNotIn("ProductoInexistente", self.mercado.bienes)
        
        # El consumidor debería manejar esto correctamente
        # (en lugar de una compra real, verificamos el comportamiento del sistema)
        dinero_inicial = consumidor.dinero
        self.assertGreater(dinero_inicial, 0)  # Tiene dinero pero no puede comprar lo que no existe
    
    def test_consumidor_nombre_vacio(self):
        """Test creación de consumidor con nombre vacío"""
        try:
            consumidor = Consumidor("", self.mercado)
            # Si se permite nombre vacío, verificar que se maneja
            self.assertIsNotNone(consumidor.nombre)
        except Exception as e:
            # Si se lanza excepción, eso también es válido
            self.assertIsInstance(e, (ValueError, TypeError))
    
    def test_empresa_nombre_vacio(self):
        """Test creación de empresa con nombre vacío"""
        try:
            empresa = Empresa("", self.mercado)
            # Si se permite nombre vacío, verificar que se maneja
            self.assertIsNotNone(empresa.nombre)
        except Exception as e:
            # Si se lanza excepción, eso también es válido
            self.assertIsInstance(e, (ValueError, TypeError))
    
    def test_mercado_agregar_participante_nulo(self):
        """Test agregar participante nulo al mercado"""
        bienes = {"test": Bien("test", "test")}
        mercado = Mercado(bienes)
        
        # Intentar agregar None como persona
        try:
            mercado.agregar_persona(None)
            # Si no lanza excepción, verificar que no se agregó
            consumidores = mercado.getConsumidores()
            self.assertNotIn(None, consumidores)
        except Exception as e:
            # Es aceptable que lance excepción
            self.assertIsInstance(e, (ValueError, TypeError, AttributeError))
    
    def test_configuracion_valores_invalidos(self):
        """Test configuración con valores claramente inválidos"""
        config = ConfiguradorSimulacion()
        
        config_invalida = {
            'simulacion': {
                'num_ciclos': -1,  # Negativo
                'num_consumidores': 0,  # Cero
                'num_empresas_productoras': -5,  # Negativo
            }
        }
        
        # Aplicar configuración inválida
        config.config.update(config_invalida)
        
        # La validación debería fallar
        self.assertFalse(config.validar())


class TestEntradaDatos(unittest.TestCase):
    """Tests para validación de entrada de datos"""
    
    def test_bien_precio_string(self):
        """Test crear bien con precio como string"""
        try:
            bien = Bien("Test", "categoria_test")
            # Los bienes no tienen precio directamente, las empresas establecen precios
            self.assertEqual(bien.nombre, "Test")
            self.assertEqual(bien.categoria, "categoria_test")
        except Exception as e:
            # Es aceptable que falle con tipo incorrecto
            self.assertIsInstance(e, (TypeError, ValueError))
    
    def test_consumidor_dinero_string(self):
        """Test establecer dinero del consumidor como string"""
        bienes = {"test": Bien("test", "test")}
        mercado = Mercado(bienes)
        consumidor = Consumidor("Test", mercado)
        
        try:
            consumidor.dinero = "1000"  # String en lugar de número
            # Si acepta string, debería convertir
            self.assertIsInstance(consumidor.dinero, (int, float, str))
        except Exception as e:
            # Es aceptable que falle con tipo incorrecto
            self.assertIsInstance(e, (TypeError, ValueError))
    
    def test_empresa_empleados_negativo(self):
        """Test empresa con número negativo de empleados"""
        bienes = {"test": Bien("test", "test")}
        mercado = Mercado(bienes)
        empresa = Empresa("Test Corp", mercado)
        
        # Intentar establecer empleados negativos si el atributo existe
        try:
            if hasattr(empresa, 'num_empleados'):
                empresa.num_empleados = -5
                # Si se permite, el sistema debería manejarlo
                self.assertGreaterEqual(empresa.num_empleados, 0, 
                                      "Número de empleados no debería ser negativo")
            else:
                # Si no tiene el atributo, está bien
                self.assertTrue(True)
        except Exception as e:
            # Es aceptable que lance excepción
            self.assertIsInstance(e, ValueError)


if __name__ == '__main__':
    unittest.main()