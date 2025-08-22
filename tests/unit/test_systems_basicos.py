"""
Tests para Sistemas Básicos del Simulador
==========================================

Tests unitarios para los sistemas fundamentales:
- ValidadorEconomico
- SistemaBancario
- PreciosDinamicos
- AnalyticsML
"""

import unittest
import sys
import os

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.systems.ValidadorEconomico import ValidadorEconomico, TipoAlerta
from src.systems.SistemaBancario import SistemaBancario, Banco
from src.systems.AnalyticsML import SistemaAnalyticsML
from src.models.Mercado import Mercado
from src.models.Bien import Bien


class TestValidadorEconomico(unittest.TestCase):
    """Tests para el validador económico"""
    
    def setUp(self):
        self.validador = ValidadorEconomico()
    
    def test_creacion_validador(self):
        """Test creación del validador económico"""
        self.assertIsInstance(self.validador.alertas, list)
        self.assertIsInstance(self.validador.indicadores, dict)
    
    def test_validar_inflacion_normal(self):
        """Test validación de inflación normal"""
        # Inflación del 2.5% - normal
        resultado = self.validador.validar_inflacion(0.025)
        
        self.assertIsInstance(resultado, dict)
        self.assertEqual(resultado['estado'], 'normal')
        self.assertLess(len(resultado.get('alertas', [])), 1)
    
    def test_validar_inflacion_alta(self):
        """Test validación de inflación alta"""
        # Inflación del 15% - alta
        resultado = self.validador.validar_inflacion(0.15)
        
        self.assertEqual(resultado['estado'], 'alerta')
        self.assertGreater(len(resultado.get('alertas', [])), 0)
    
    def test_validar_desempleo_normal(self):
        """Test validación de desempleo normal"""
        # Desempleo del 5% - normal
        resultado = self.validador.validar_desempleo(0.05)
        
        self.assertEqual(resultado['estado'], 'normal')
    
    def test_validar_desempleo_alto(self):
        """Test validación de desempleo alto"""
        # Desempleo del 20% - crítico
        resultado = self.validador.validar_desempleo(0.20)
        
        self.assertEqual(resultado['estado'], 'critico')
        self.assertGreater(len(resultado.get('alertas', [])), 0)
    
    def test_calcular_indice_estabilidad(self):
        """Test cálculo del índice de estabilidad"""
        # Datos económicos de prueba
        datos = {
            'inflacion': 0.025,
            'desempleo': 0.05,
            'crecimiento_pib': 0.03,
            'indice_precios': 1.0
        }
        
        indice = self.validador.calcular_indice_estabilidad(datos)
        
        self.assertIsInstance(indice, float)
        self.assertGreaterEqual(indice, 0.0)
        self.assertLessEqual(indice, 1.0)
    
    def test_generar_reporte_estabilidad(self):
        """Test generación de reporte de estabilidad"""
        # Simular algunos datos
        self.validador.indicadores = {
            'inflacion': [0.02, 0.025, 0.03],
            'desempleo': [0.05, 0.055, 0.06],
            'pib': [100000, 102000, 104000]
        }
        
        reporte = self.validador.generar_reporte_estabilidad()
        
        self.assertIsInstance(reporte, dict)
        self.assertIn('resumen', reporte)
        self.assertIn('indicadores', reporte)


class TestSistemaBancario(unittest.TestCase):
    """Tests para el sistema bancario"""
    
    def setUp(self):
        # Crear mercado de prueba
        bienes = {
            "pan": Bien("pan", "alimentos_basicos"),
            "agua": Bien("agua", "alimentos_basicos")
        }
        self.mercado = Mercado(bienes)
        self.sistema_bancario = SistemaBancario(self.mercado)
    
    def test_creacion_sistema_bancario(self):
        """Test creación del sistema bancario"""
        self.assertEqual(self.sistema_bancario.mercado, self.mercado)
        self.assertIsInstance(self.sistema_bancario.bancos, list)
        self.assertIsInstance(self.sistema_bancario.prestamos_activos, list)
    
    def test_crear_banco(self):
        """Test creación de un banco"""
        banco = self.sistema_bancario.crear_banco("Banco Test", 1000000)
        
        self.assertIsInstance(banco, Banco)
        self.assertEqual(banco.nombre, "Banco Test")
        self.assertEqual(banco.capital, 1000000)
        self.assertIn(banco, self.sistema_bancario.bancos)
    
    def test_calcular_tasa_interes_base(self):
        """Test cálculo de tasa de interés base"""
        tasa = self.sistema_bancario.calcular_tasa_interes_base()
        
        self.assertIsInstance(tasa, float)
        self.assertGreaterEqual(tasa, 0.0)
        self.assertLessEqual(tasa, 0.20)  # Máximo 20%
    
    def test_evaluar_riesgo_crediticio(self):
        """Test evaluación de riesgo crediticio"""
        # Datos de prueba para evaluación
        datos_solicitante = {
            'dinero': 10000,
            'ingreso_mensual': 3000,
            'historial_crediticio': 'bueno',
            'empleado': True
        }
        
        monto_solicitado = 5000
        riesgo = self.sistema_bancario.evaluar_riesgo_crediticio(datos_solicitante, monto_solicitado)
        
        self.assertIsInstance(riesgo, dict)
        self.assertIn('nivel_riesgo', riesgo)
        self.assertIn('tasa_interes', riesgo)
        self.assertIn('aprobado', riesgo)
    
    def test_procesar_pagos_prestamos(self):
        """Test procesamiento de pagos de préstamos"""
        # Crear un banco para pruebas
        banco = self.sistema_bancario.crear_banco("Banco Prueba", 500000)
        
        # Simular un préstamo activo
        prestamo = {
            'id': 'test_001',
            'banco': banco,
            'monto_original': 10000,
            'saldo_pendiente': 8000,
            'tasa_interes': 0.08,
            'cuota_mensual': 500,
            'prestatario': 'test_client'
        }
        self.sistema_bancario.prestamos_activos.append(prestamo)
        
        # Procesar pagos
        self.sistema_bancario.procesar_pagos_prestamos()
        
        # Verificar que el sistema procesó el pago
        self.assertLessEqual(prestamo['saldo_pendiente'], 8000)


class TestAnalyticsML(unittest.TestCase):
    """Tests para el sistema de Analytics ML"""
    
    def setUp(self):
        # Crear mercado de prueba
        bienes = {
            "comida": Bien("comida", "alimentos_basicos"),
            "ropa": Bien("ropa", "alimentos_lujo")
        }
        self.mercado = Mercado(bienes)
        self.analytics = SistemaAnalyticsML(self.mercado)
    
    def test_creacion_sistema_analytics(self):
        """Test creación del sistema de analytics ML"""
        self.assertEqual(self.analytics.mercado, self.mercado)
        self.assertIsInstance(self.analytics.predictor_demanda, dict)
        self.assertIsInstance(self.analytics.modelos_precio, dict)
    
    def test_entrenar_predictor_demanda(self):
        """Test entrenamiento de predictor de demanda"""
        # Datos históricos de prueba
        datos_historicos = {
            'ventas': [100, 110, 95, 120, 105],
            'precios': [10, 11, 9, 12, 10],
            'ciclos': [1, 2, 3, 4, 5]
        }
        
        resultado = self.analytics.entrenar_predictor_demanda("comida", datos_historicos)
        
        self.assertTrue(resultado)
        self.assertIn("comida", self.analytics.predictor_demanda)
    
    def test_predecir_demanda(self):
        """Test predicción de demanda"""
        # Primero entrenar el modelo
        datos_historicos = {
            'ventas': [100, 110, 95, 120, 105, 130],
            'precios': [10, 11, 9, 12, 10, 13],
            'ciclos': [1, 2, 3, 4, 5, 6]
        }
        self.analytics.entrenar_predictor_demanda("comida", datos_historicos)
        
        # Hacer predicción
        contexto = {
            'precio_actual': 11,
            'ciclo': 7,
            'tendencia': 'creciente'
        }
        
        prediccion = self.analytics.predecir_demanda("comida", contexto)
        
        self.assertIsInstance(prediccion, dict)
        self.assertIn('demanda_estimada', prediccion)
        self.assertIn('confianza', prediccion)
    
    def test_analizar_patrones_consumo(self):
        """Test análisis de patrones de consumo"""
        # Simular datos de transacciones
        transacciones = [
            {'bien': 'comida', 'cantidad': 5, 'precio': 10, 'ciclo': 1},
            {'bien': 'comida', 'cantidad': 7, 'precio': 11, 'ciclo': 2},
            {'bien': 'ropa', 'cantidad': 2, 'precio': 50, 'ciclo': 1},
            {'bien': 'ropa', 'cantidad': 3, 'precio': 48, 'ciclo': 2}
        ]
        
        patrones = self.analytics.analizar_patrones_consumo(transacciones)
        
        self.assertIsInstance(patrones, dict)
        self.assertIn('comida', patrones)
        self.assertIn('ropa', patrones)
    
    def test_optimizar_precio_ml(self):
        """Test optimización de precios con ML"""
        # Datos de mercado
        datos_mercado = {
            'demanda_actual': 100,
            'precio_actual': 12,
            'competencia': [10, 11, 13],
            'costos': 8,
            'inventario': 200
        }
        
        precio_optimizado = self.analytics.optimizar_precio_ml("comida", datos_mercado)
        
        self.assertIsInstance(precio_optimizado, dict)
        self.assertIn('precio_sugerido', precio_optimizado)
        self.assertIn('motivo', precio_optimizado)
        
        # El precio debe ser razonable
        precio = precio_optimizado['precio_sugerido']
        self.assertGreater(precio, 0)
        self.assertLess(precio, 1000)  # Sanity check
    
    def test_generar_insights_mercado(self):
        """Test generación de insights del mercado"""
        # Simular algunos datos en el sistema
        self.analytics.datos_mercado = {
            'comida': {
                'ventas_historicas': [100, 110, 95],
                'precios_historicos': [10, 11, 9],
                'tendencia': 'estable'
            }
        }
        
        insights = self.analytics.generar_insights_mercado()
        
        self.assertIsInstance(insights, dict)
        self.assertIn('resumen_general', insights)
        self.assertIn('recomendaciones', insights)


class TestBanco(unittest.TestCase):
    """Tests para la clase Banco"""
    
    def test_creacion_banco(self):
        """Test creación de un banco"""
        banco = Banco("Banco Nacional", 1000000)
        
        self.assertEqual(banco.nombre, "Banco Nacional")
        self.assertEqual(banco.capital, 1000000)
        self.assertEqual(banco.reservas, 100000)  # 10% del capital
        self.assertIsInstance(banco.prestamos, list)
        self.assertIsInstance(banco.depositos, list)
    
    def test_calcular_capacidad_prestamo(self):
        """Test cálculo de capacidad de préstamo"""
        banco = Banco("Banco Test", 1000000)
        
        capacidad = banco.calcular_capacidad_prestamo()
        
        self.assertIsInstance(capacidad, float)
        self.assertGreater(capacidad, 0)
        self.assertLessEqual(capacidad, banco.capital - banco.reservas)
    
    def test_otorgar_prestamo(self):
        """Test otorgamiento de préstamo"""
        banco = Banco("Banco Test", 1000000)
        
        # Otorgar préstamo pequeño
        prestamo = banco.otorgar_prestamo(
            prestatario="cliente_test",
            monto=50000,
            tasa_interes=0.08,
            plazo_meses=24
        )
        
        self.assertIsNotNone(prestamo)
        self.assertEqual(prestamo['monto'], 50000)
        self.assertEqual(prestamo['prestatario'], "cliente_test")
        self.assertIn(prestamo, banco.prestamos)
    
    def test_otorgar_prestamo_insuficiente_capital(self):
        """Test otorgamiento de préstamo con capital insuficiente"""
        banco = Banco("Banco Pequeño", 100000)
        
        # Intentar préstamo mayor al capital disponible
        prestamo = banco.otorgar_prestamo(
            prestatario="cliente_test",
            monto=200000,
            tasa_interes=0.08,
            plazo_meses=24
        )
        
        self.assertIsNone(prestamo)


if __name__ == '__main__':
    unittest.main()