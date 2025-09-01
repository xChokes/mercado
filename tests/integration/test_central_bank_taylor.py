"""
Tests de integración para el Banco Central con Regla de Taylor
==============================================================

Verifica que el sistema de política monetaria responda adecuadamente
a shocks inflacionarios y mantenga la estabilidad económica.
"""

import unittest
import sys
import os

# Agregar ruta para importaciones
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.systems.central_bank import CentralBank, TaylorRuleParams
from src.config.ConfiguradorSimulacion import ConfiguradorSimulacion


class TestBancoCentralTaylorRule(unittest.TestCase):
    """Tests de integración para el Banco Central con Taylor Rule"""
    
    def setUp(self):
        """Configurar entorno de prueba"""
        self.configurador = ConfiguradorSimulacion()
        
        # Crear mercado básico de prueba para tests aislados
        from src.models.Mercado import Mercado
        from main import crear_bienes_expandidos
        
        bienes = crear_bienes_expandidos()
        bienes_test = {k: v for k, v in list(bienes.items())[:5]}  # Solo 5 bienes para testing
        
        self.mercado = Mercado(bienes_test)
        
        # Simular algunos datos históricos básicos
        self.mercado.pib_historico = [100000, 102000, 104000]  # Crecimiento 2%
        self.mercado.inflacion_historica = [0.02, 0.025, 0.03]  # Inflación creciente
    
    def test_inicializacion_banco_central(self):
        """Test que el banco central se inicialice correctamente"""
        print("\n🧪 Test: Inicialización del Banco Central")
        
        config_taylor = {
            'taylor_params': {
                'tasa_neutral': 0.03,
                'meta_inflacion': 0.025,
                'peso_inflacion': 1.5,
                'peso_producto': 0.5
            }
        }
        
        banco_central = CentralBank(self.mercado, config_taylor)
        
        # Verificar inicialización
        self.assertEqual(banco_central.params.tasa_neutral, 0.03)
        self.assertEqual(banco_central.params.meta_inflacion, 0.025)
        self.assertEqual(banco_central.params.peso_inflacion, 1.5)
        self.assertEqual(banco_central.tasa_actual, 0.03)
        
        print(f"✅ Banco Central inicializado - Meta: {banco_central.params.meta_inflacion:.1%}, Tasa: {banco_central.tasa_actual:.1%}")
    
    def test_calculo_regla_taylor_basico(self):
        """Test del cálculo básico de la regla de Taylor"""
        print("\n🧪 Test: Cálculo Regla de Taylor")
        
        banco_central = CentralBank(self.mercado)
        
        # Caso 1: Inflación sobre meta
        inflacion_alta = 0.04  # 4% vs meta 2.5%
        brecha_producto = 0.0  # Sin brecha de producto
        
        tasa_objetivo = banco_central._calcular_regla_taylor(inflacion_alta, brecha_producto)
        
        # La tasa debería ser mayor que la neutral debido a inflación alta
        self.assertGreater(tasa_objetivo, banco_central.params.tasa_neutral)
        
        # Caso 2: Inflación bajo meta
        inflacion_baja = 0.01  # 1% vs meta 2.5%
        tasa_objetivo_baja = banco_central._calcular_regla_taylor(inflacion_baja, brecha_producto)
        
        # La tasa debería ser menor que la neutral
        self.assertLess(tasa_objetivo_baja, banco_central.params.tasa_neutral)
        
        print(f"✅ Taylor Rule - Inflación alta ({inflacion_alta:.1%}): tasa {tasa_objetivo:.2%}")
        print(f"✅ Taylor Rule - Inflación baja ({inflacion_baja:.1%}): tasa {tasa_objetivo_baja:.2%}")
    
    def test_shock_inflacionario_respuesta(self):
        """Test crítico: Respuesta a shock inflacionario"""
        print("\n🧪 Test: Respuesta a Shock Inflacionario")
        
        banco_central = CentralBank(self.mercado)
        tasa_inicial = banco_central.tasa_actual
        
        # Simular shock inflacionario del 3%
        respuesta_shock = banco_central.simular_shock_inflacionario(magnitud_shock=0.03)
        
        # Verificaciones críticas
        self.assertGreater(respuesta_shock['cambio_tasa'], 0, 
                          "El banco central debe subir tasas ante shock inflacionario")
        
        self.assertGreater(respuesta_shock['cambio_puntos_basicos'], 100,
                          "El aumento debe ser significativo (>100 pb)")
        
        self.assertTrue(respuesta_shock['respuesta_adecuada'],
                       "La respuesta debe ser proporcionalmente adecuada al shock")
        
        print(f"✅ Shock inflacionario 3%: aumento de {respuesta_shock['cambio_puntos_basicos']} pb")
        print(f"✅ Tasa de respuesta: {respuesta_shock['tasa_respuesta']:.2%}")
        print(f"✅ Respuesta adecuada: {respuesta_shock['respuesta_adecuada']}")
    
    def test_convergencia_inflacion_simulacion(self):
        """Test de convergencia de inflación en simulación"""
        print("\n🧪 Test: Convergencia de Inflación")
        
        banco_central = CentralBank(self.mercado)
        
        # Simular 10 ciclos con política monetaria
        decisiones = []
        inflaciones_simuladas = [0.05, 0.045, 0.04, 0.038, 0.035, 0.032, 0.03, 0.028, 0.026, 0.025]
        
        for ciclo, inflacion in enumerate(inflaciones_simuladas, 1):
            # Simular inflación descendente
            self.mercado.inflacion_historica.append(inflacion)
            
            # Ejecutar política monetaria
            resultado = banco_central.ejecutar_politica_monetaria(ciclo)
            decisiones.append(resultado)
        
        # Verificar convergencia
        inflacion_final = inflaciones_simuladas[-1]
        meta_inflacion = banco_central.params.meta_inflacion
        brecha_final = abs(inflacion_final - meta_inflacion)
        
        self.assertLess(brecha_final, 0.005, 
                       "La inflación debe converger hacia la meta (±0.5%)")
        
        # Verificar que hubo ajustes de política
        cambios_politica = [d for d in decisiones if d['accion'] != 'MANTENER']
        self.assertGreater(len(cambios_politica), 2,
                          "Debe haber múltiples ajustes de política")
        
        print(f"✅ Convergencia lograda - Brecha final: {brecha_final:.3%}")
        print(f"✅ Decisiones de política: {len(cambios_politica)}/{len(decisiones)}")
    
    def test_transmision_sistema_bancario(self):
        """Test de transmisión al sistema bancario"""
        print("\n🧪 Test: Transmisión al Sistema Bancario")
        
        # Configurar sistema bancario mínimo
        from src.systems.SistemaBancario import SistemaBancario, Banco
        
        sistema_bancario = SistemaBancario(self.mercado)
        self.mercado.sistema_bancario = sistema_bancario
        
        # Crear bancos de prueba
        banco1 = Banco("TestBank1", 1000000)
        banco2 = Banco("TestBank2", 1000000)
        sistema_bancario.bancos = [banco1, banco2]
        
        # Configurar banco central
        banco_central = CentralBank(self.mercado)
        tasa_inicial = banco_central.tasa_actual
        
        # Simular cambio de tasa significativo
        banco_central.tasa_actual = 0.05  # 5%
        banco_central._transmitir_al_sistema_bancario()
        
        # Verificar transmisión
        for banco in sistema_bancario.bancos:
            self.assertGreater(banco.tasa_base_prestamos, 0.05,
                             "Las tasas de préstamos deben incluir spread sobre tasa BC")
            
            if hasattr(banco, 'tasa_depositos'):
                self.assertLess(banco.tasa_depositos, banco.tasa_base_prestamos,
                               "Tasa de depósitos debe ser menor que préstamos")
        
        print(f"✅ Transmisión exitosa - Tasa BC: {banco_central.tasa_actual:.2%}")
        print(f"✅ Tasa préstamos banco1: {banco1.tasa_base_prestamos:.2%}")
    
    def test_limites_tasas_operativos(self):
        """Test que las tasas respeten límites operativos"""
        print("\n🧪 Test: Límites Operativos")
        
        banco_central = CentralBank(self.mercado)
        
        # Test límite inferior (deflación severa)
        self.mercado.inflacion_historica = [-0.1]  # -10% deflación
        resultado_bajo = banco_central.ejecutar_politica_monetaria(1)
        
        self.assertGreaterEqual(resultado_bajo['tasa_interes'], banco_central.tasa_minima,
                               "Tasa no puede estar bajo el límite mínimo")
        
        # Test límite superior (hiperinflación)
        self.mercado.inflacion_historica = [0.5]  # 50% inflación
        resultado_alto = banco_central.ejecutar_politica_monetaria(2)
        
        self.assertLessEqual(resultado_alto['tasa_interes'], banco_central.tasa_maxima,
                            "Tasa no puede exceder el límite máximo")
        
        print(f"✅ Límites respetados - Min: {banco_central.tasa_minima:.1%}, Max: {banco_central.tasa_maxima:.1%}")
    
    def test_estadisticas_desempeno(self):
        """Test de estadísticas de desempeño"""
        print("\n🧪 Test: Estadísticas de Desempeño")
        
        banco_central = CentralBank(self.mercado)
        
        # Simular varias decisiones
        for ciclo in range(1, 6):
            banco_central.ejecutar_politica_monetaria(ciclo)
        
        stats = banco_central.obtener_estadisticas()
        
        # Verificar estadísticas básicas
        self.assertEqual(stats['decisiones_totales'], 5)
        self.assertIn('tasa_actual', stats)
        self.assertIn('convergencia_inflacion', stats)
        self.assertGreaterEqual(stats['convergencia_inflacion'], 0)
        self.assertLessEqual(stats['convergencia_inflacion'], 1)
        
        print(f"✅ Estadísticas - Decisiones: {stats['decisiones_totales']}")
        print(f"✅ Convergencia inflación: {stats['convergencia_inflacion']:.1%}")


class TestIntegracionCompleta(unittest.TestCase):
    """Test de integración con el sistema completo"""
    
    def test_integracion_sistema_completo(self):
        """Test de integración con simulación económica completa"""
        print("\n🧪 Test: Integración Sistema Completo")
        
        # Cargar configuración con política monetaria
        configurador = ConfiguradorSimulacion()
        config = configurador.cargar_configuracion()
        
        # Verificar que la configuración incluye política monetaria
        self.assertIn('politica_monetaria', config)
        self.assertTrue(config['politica_monetaria']['activar'])
        self.assertIn('taylor_params', config['politica_monetaria'])
        
        # Crear mercado básico
        from src.models.Mercado import Mercado
        from main import crear_bienes_expandidos
        
        bienes = crear_bienes_expandidos()
        bienes_test = {k: v for k, v in list(bienes.items())[:5]}
        mercado = Mercado(bienes_test)
        
        # Verificar que se puede crear banco central
        banco_central = CentralBank(mercado, config['politica_monetaria'])
        
        self.assertIsNotNone(banco_central)
        self.assertEqual(banco_central.params.meta_inflacion, 
                        config['politica_monetaria']['taylor_params']['meta_inflacion'])
        
        print(f"✅ Integración exitosa - Meta inflación: {banco_central.params.meta_inflacion:.1%}")


if __name__ == '__main__':
    unittest.main(verbosity=2)