"""
Tests unitarios para el sistema de validación económica formal
===========================================================

Tests para validadores de KPIs económicos, consistencia de datos
y generación de reportes de validación.

Autor: Sistema de Tests Económicos
Versión: 1.0
"""

import unittest
import tempfile
import json
import os
from unittest.mock import patch, MagicMock

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.utils.validators import (
    ValidadorEconomicoFormal, 
    TipoValidacion, 
    ResultadoValidacion,
    validar_resultados_simulacion
)


class TestValidadorEconomicoFormal(unittest.TestCase):
    """Tests para la clase ValidadorEconomicoFormal"""
    
    def setUp(self):
        """Configurar tests"""
        self.validador = ValidadorEconomicoFormal()
        self.datos_normales = {
            'pib': 100000,
            'inflacion': 2.5,
            'desempleo': 5.0,
            'empresas_activas': 5,
            'transacciones': 1000,
            'depositos_bancarios': 500000,
            'prestamos_totales': 300000,
            'capital_bancario': 50000
        }
    
    def test_creacion_validador(self):
        """Test que se puede crear el validador"""
        self.assertIsInstance(self.validador, ValidadorEconomicoFormal)
        self.assertEqual(len(self.validador.resultados), 0)
        self.assertEqual(self.validador.validaciones_exitosas, 0)
    
    def test_validar_pib_normal(self):
        """Test validación de PIB en rango normal"""
        resultado = self.validador.validar_pib(100000, "test_normal")
        
        self.assertEqual(resultado.indicador, 'pib')
        self.assertEqual(resultado.valor_actual, 100000)
        self.assertEqual(resultado.tipo, TipoValidacion.INFO)
        self.assertIn("rango normal", resultado.mensaje)
        self.assertEqual(self.validador.validaciones_exitosas, 1)
    
    def test_validar_pib_bajo(self):
        """Test validación de PIB demasiado bajo"""
        resultado = self.validador.validar_pib(5000, "test_bajo")
        
        self.assertEqual(resultado.tipo, TipoValidacion.ADVERTENCIA)
        self.assertIn("fuera de rango", resultado.mensaje)
        self.assertEqual(self.validador.advertencias, 1)
    
    def test_validar_pib_critico(self):
        """Test validación de PIB crítico"""
        resultado = self.validador.validar_pib(4000000, "test_critico")  # Clearly above 3M limit
        
        self.assertEqual(resultado.tipo, TipoValidacion.CRITICA)
        self.assertIn("fuera de rango", resultado.mensaje)
        self.assertEqual(self.validador.errores, 1)
    
    def test_validar_inflacion_normal(self):
        """Test validación de inflación normal"""
        resultado = self.validador.validar_inflacion(2.5, "test_normal")
        
        self.assertEqual(resultado.indicador, 'inflacion_pct')
        self.assertEqual(resultado.tipo, TipoValidacion.INFO)
        self.assertIn("rango normal", resultado.mensaje)
    
    def test_validar_inflacion_alta(self):
        """Test validación de inflación alta"""
        resultado = self.validador.validar_inflacion(25.0, "test_alta")
        
        self.assertEqual(resultado.tipo, TipoValidacion.ADVERTENCIA)
        self.assertIn("fuera de rango", resultado.mensaje)
    
    def test_validar_inflacion_hiperinflacion(self):
        """Test validación de hiperinflación"""
        resultado = self.validador.validar_inflacion(100.0, "test_hiper")
        
        self.assertEqual(resultado.tipo, TipoValidacion.CRITICA)
        self.assertIn("fuera de rango", resultado.mensaje)
    
    def test_validar_sistema_bancario_normal(self):
        """Test validación del sistema bancario con valores normales"""
        resultados = self.validador.validar_sistema_bancario(
            depositos=500000,
            prestamos=300000,
            capital=50000,
            escenario="test_bancario"
        )
        
        self.assertEqual(len(resultados), 2)  # ratio préstamos y ratio capital
        
        # Verificar ratio préstamos/depósitos
        ratio_prestamos = next(r for r in resultados if r.indicador == 'ratio_prestamos_depositos')
        self.assertEqual(ratio_prestamos.valor_actual, 0.6)  # 300000/500000
        
        # Verificar ratio capital/depósitos  
        ratio_capital = next(r for r in resultados if r.indicador == 'ratio_capital_depositos')
        self.assertEqual(ratio_capital.valor_actual, 0.1)  # 50000/500000
    
    def test_validar_sistema_bancario_riesgo(self):
        """Test validación del sistema bancario con alto riesgo"""
        resultados = self.validador.validar_sistema_bancario(
            depositos=100000,
            prestamos=120000,  # Más préstamos que depósitos - riesgoso
            capital=5000,      # Capital muy bajo
            escenario="test_riesgo"
        )
        
        self.assertEqual(len(resultados), 2)
        
        # Debería generar advertencias por alto apalancamiento
        tipos = [r.tipo for r in resultados]
        self.assertIn(TipoValidacion.ADVERTENCIA, tipos)
    
    def test_validar_consistencia_stocks_flujos(self):
        """Test validación de consistencia entre stocks y flujos"""
        datos = {
            'pib': 100000,
            'transacciones': 0,  # Inconsistencia: PIB sin transacciones
            'empresas_activas': 5
        }
        
        resultados = self.validador.validar_consistencia_stocks_flujos(datos, "test_consistencia")
        
        self.assertGreater(len(resultados), 0)
        # Debería detectar inconsistencia PIB-transacciones
        inconsistencia = next((r for r in resultados if 'inconsistencia' in r.mensaje.lower()), None)
        self.assertIsNotNone(inconsistencia)
    
    def test_validar_consistencia_critica(self):
        """Test validación de inconsistencia crítica"""
        datos = {
            'pib': 100000,
            'empresas_activas': 0  # Crítico: PIB sin empresas
        }
        
        resultados = self.validador.validar_consistencia_stocks_flujos(datos, "test_critico")
        
        # Debería generar error crítico
        errores_criticos = [r for r in resultados if r.tipo == TipoValidacion.CRITICA]
        self.assertGreater(len(errores_criticos), 0)
    
    def test_validar_datos_completos_ok(self):
        """Test validación de datos completos"""
        datos = {
            'pib': 100000,
            'inflacion': 2.5,
            'desempleo': 5.0,
            'empresas_activas': 5,
            'transacciones': 1000
        }
        
        resultado = self.validador.validar_datos_completos(datos, "test_completo")
        
        self.assertEqual(resultado.tipo, TipoValidacion.INFO)
        self.assertIn("presentes", resultado.mensaje)
    
    def test_validar_datos_incompletos(self):
        """Test validación con datos faltantes"""
        datos = {
            'pib': 100000,
            'inflacion': 2.5
            # Faltan: desempleo, empresas_activas, transacciones
        }
        
        resultado = self.validador.validar_datos_completos(datos, "test_incompleto")
        
        self.assertEqual(resultado.tipo, TipoValidacion.ADVERTENCIA)
        self.assertIn("faltantes", resultado.mensaje)
    
    def test_ejecutar_validacion_completa(self):
        """Test ejecución de validación completa"""
        reporte = self.validador.ejecutar_validacion_completa(self.datos_normales, "test_completo")
        
        self.assertIn('timestamp', reporte)
        self.assertIn('resumen', reporte)
        self.assertIn('validaciones', reporte)
        self.assertIn('estado_general', reporte)
        
        # Verificar estructura del resumen
        resumen = reporte['resumen']
        self.assertIn('validaciones_exitosas', resumen)
        self.assertIn('advertencias', resumen)
        self.assertIn('errores', resumen)
        self.assertIn('total_validaciones', resumen)
        
        # Con datos normales, debería tener validaciones exitosas
        self.assertGreater(resumen['validaciones_exitosas'], 0)
    
    def test_determinar_estado_general(self):
        """Test determinación del estado general del sistema"""
        # Estado estable - sin errores ni advertencias
        self.validador.errores = 0
        self.validador.advertencias = 0
        self.assertEqual(self.validador._determinar_estado_general(), "ESTABLE")
        
        # Estado aceptable - pocas advertencias
        self.validador.advertencias = 2
        self.assertEqual(self.validador._determinar_estado_general(), "ACEPTABLE")
        
        # Estado de advertencia - muchas advertencias
        self.validador.advertencias = 5
        self.assertEqual(self.validador._determinar_estado_general(), "ADVERTENCIA")
        
        # Estado crítico - errores presentes
        self.validador.errores = 1
        self.assertEqual(self.validador._determinar_estado_general(), "CRITICO")
    
    def test_resultado_validacion_to_dict(self):
        """Test conversión de ResultadoValidacion a diccionario"""
        resultado = ResultadoValidacion(
            indicador='pib',
            valor_actual=100000,
            rango_esperado=(15000, 2000000),
            tipo=TipoValidacion.INFO,
            mensaje="Test mensaje",
            escenario="test"
        )
        
        dict_resultado = resultado.to_dict()
        
        self.assertEqual(dict_resultado['indicador'], 'pib')
        self.assertEqual(dict_resultado['valor_actual'], 100000)
        self.assertEqual(dict_resultado['rango_esperado'], [15000, 2000000])
        self.assertEqual(dict_resultado['tipo'], 'INFO')
        self.assertEqual(dict_resultado['mensaje'], "Test mensaje")
    
    def test_guardar_reporte_json(self):
        """Test guardado de reporte en formato JSON"""
        # Ejecutar validación para tener datos
        self.validador.ejecutar_validacion_completa(self.datos_normales, "test_json")
        
        # Crear archivo temporal
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            ruta_temp = f.name
        
        try:
            # Guardar reporte
            ruta_guardada = self.validador.guardar_reporte_json(ruta_temp)
            self.assertEqual(ruta_guardada, ruta_temp)
            
            # Verificar que el archivo existe y es JSON válido
            self.assertTrue(os.path.exists(ruta_temp))
            
            with open(ruta_temp, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            
            # Verificar estructura JSON
            self.assertIn('timestamp', datos)
            self.assertIn('resumen', datos)
            self.assertIn('validaciones', datos)
            self.assertIn('estado_general', datos)
            
        finally:
            # Limpiar archivo temporal
            if os.path.exists(ruta_temp):
                os.unlink(ruta_temp)


class TestFuncionValidarResultados(unittest.TestCase):
    """Tests para la función principal validar_resultados_simulacion"""
    
    def test_validar_resultados_simulacion_basico(self):
        """Test función principal de validación"""
        datos = {
            'pib': 100000,
            'inflacion': 2.5,
            'desempleo': 5.0,
            'empresas_activas': 5,
            'transacciones': 1000
        }
        
        reporte = validar_resultados_simulacion(datos, "test_funcion")
        
        self.assertIsInstance(reporte, dict)
        self.assertIn('timestamp', reporte)
        self.assertIn('resumen', reporte)
        self.assertIn('validaciones', reporte)
        self.assertIn('estado_general', reporte)
    
    def test_validar_resultados_datos_problematicos(self):
        """Test validación con datos problemáticos"""
        datos = {
            'pib': 5000,      # Muy bajo
            'inflacion': 50,  # Muy alta
            'desempleo': 30,  # Muy alto
            'empresas_activas': 0,  # Crítico
            'transacciones': 0
        }
        
        reporte = validar_resultados_simulacion(datos, "test_problemas")
        
        # Debería detectar múltiples problemas
        resumen = reporte['resumen']
        self.assertGreater(resumen['errores'], 0)
        self.assertGreater(resumen['advertencias'], 0)
        self.assertEqual(reporte['estado_general'], 'CRITICO')


class TestValidacionIntegracion(unittest.TestCase):
    """Tests de integración del sistema de validación"""
    
    def test_validacion_escenario_completo(self):
        """Test validación de un escenario completo realista"""
        # Simular datos de una simulación exitosa
        datos_simulacion = {
            'pib': 187500,
            'inflacion': 1.8,
            'desempleo': 4.2,
            'empresas_activas': 7,
            'transacciones': 1250,
            'depositos_bancarios': 750000,
            'prestamos_totales': 450000,
            'capital_bancario': 75000,
            'duracion_s': 45
        }
        
        validador = ValidadorEconomicoFormal()
        reporte = validador.ejecutar_validacion_completa(datos_simulacion, "escenario_realista")
        
        # Verificar que se generó reporte completo
        self.assertIn('resumen', reporte)
        self.assertIn('validaciones', reporte)
        self.assertGreater(len(reporte['validaciones']), 5)
        
        # Con datos realistas, debería ser ESTABLE o ACEPTABLE
        self.assertIn(reporte['estado_general'], ['ESTABLE', 'ACEPTABLE'])
    
    def test_validacion_escenario_crisis(self):
        """Test validación durante una crisis económica"""
        # Simular datos de crisis económica
        datos_crisis = {
            'pib': 45000,     # PIB bajo por crisis
            'inflacion': 12,  # Inflación alta
            'desempleo': 18,  # Desempleo alto
            'empresas_activas': 2,  # Pocas empresas
            'transacciones': 150,   # Pocas transacciones
            'depositos_bancarios': 300000,
            'prestamos_totales': 350000,  # Más préstamos que depósitos - problema
            'capital_bancario': 15000     # Capital insuficiente
        }
        
        validador = ValidadorEconomicoFormal()
        reporte = validador.ejecutar_validacion_completa(datos_crisis, "escenario_crisis")
        
        # Durante crisis, debería generar advertencias/errores
        resumen = reporte['resumen']
        self.assertGreater(resumen['advertencias'] + resumen['errores'], 0)
        
        # Estado debería reflejar problemas
        self.assertIn(reporte['estado_general'], ['ADVERTENCIA', 'CRITICO'])


if __name__ == '__main__':
    # Configurar logging para tests
    import logging
    logging.basicConfig(level=logging.WARNING)
    
    unittest.main(verbosity=2)