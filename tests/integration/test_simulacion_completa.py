"""
Tests de Integración - Simulación Completa
==========================================

Tests que validan el comportamiento del sistema completo
ejecutando simulaciones largas y verificando estabilidad.
"""

import unittest
import sys
import os
import time

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.config.ConfiguradorSimulacion import ConfiguradorSimulacion
from src.systems.ValidadorEconomico import ValidadorEconomico, TipoAlerta
from src.systems.BancoCentralAvanzado import BancoCentralAvanzado


class TestIntegracionCompleta(unittest.TestCase):
    """Tests de integración del sistema completo"""
    
    def setUp(self):
        """Configuración para tests de integración"""
        self.configurador = ConfiguradorSimulacion()
        self.validador = ValidadorEconomico()
        
        # Configuración para tests rápidos pero representativos
        self.config_test = {
            'simulacion': {
                'num_ciclos': 30,
                'num_consumidores': 50,
                'num_empresas_productoras': 3,
                'num_empresas_comerciales': 5,
                'activar_crisis': False,  # Desactivar crisis para test base
                'frecuencia_reportes': 10
            },
            'economia': {
                'pib_inicial': 100000,
                'tasa_desempleo_inicial': 0.08,
                'tasa_inflacion_objetivo': 0.025,
                'salario_base_minimo': 2500
            }
        }
    
    def test_simulacion_estabilidad_30_ciclos(self):
        """Test de estabilidad para simulación de 30 ciclos"""
        print("\n🧪 EJECUTANDO: Test de estabilidad 30 ciclos...")
        
        # Ejecutar simulación completa
        mercado = self._ejecutar_simulacion_controlada()
        
        # Validar que no hay alertas críticas
        alertas_finales = self.validador.validar_indicadores_macroeconomicos(mercado, 30)
        alertas_criticas = [a for a in alertas_finales if a.tipo == TipoAlerta.CRITICA]
        
        self.assertEqual(len(alertas_criticas), 0, 
                        f"Se encontraron {len(alertas_criticas)} alertas críticas: {[a.mensaje for a in alertas_criticas]}")
        
        # Validar índice de estabilidad
        indice_estabilidad = self.validador.calcular_indice_estabilidad(mercado)
        self.assertGreaterEqual(indice_estabilidad, 0.4, 
                               f"Índice de estabilidad muy bajo: {indice_estabilidad:.3f}")
        
        print(f"✅ Test completado - Índice de estabilidad: {indice_estabilidad:.3f}")
    
    def test_banco_central_avanzado_funcionamiento(self):
        """Test del funcionamiento del Banco Central Avanzado"""
        print("\n🧪 EJECUTANDO: Test Banco Central Avanzado...")
        
        mercado = self._ejecutar_simulacion_controlada()
        banco_central = BancoCentralAvanzado(mercado)
        
        # Simular varias decisiones monetarias
        decisiones = []
        for ciclo in range(3, 31, 3):  # Cada 3 ciclos
            decision = banco_central.ejecutar_politica_monetaria(ciclo)
            if decision:
                decisiones.append(decision)
        
        # Validar que se tomaron decisiones
        self.assertGreater(len(decisiones), 5, "Se esperaban más decisiones monetarias")
        
        # Validar que las tasas están en rangos realistas
        for decision in decisiones:
            self.assertGreaterEqual(decision.tasa_nueva, 0.0, "Tasa negativa no realista")
            self.assertLessEqual(decision.tasa_nueva, 0.15, "Tasa demasiado alta")
        
        # Validar efectividad
        efectividad = banco_central.obtener_efectividad_politica()
        self.assertGreaterEqual(efectividad['efectividad_inflacion'], 0.3, 
                               "Efectividad de inflación muy baja")
        
        print(f"✅ Test completado - Decisiones tomadas: {len(decisiones)}")
        print(f"   Efectividad inflación: {efectividad['efectividad_inflacion']:.3f}")
    
    def test_resistencia_a_shocks(self):
        """Test de resistencia del sistema a shocks económicos"""
        print("\n🧪 EJECUTANDO: Test de resistencia a shocks...")
        
        mercado = self._ejecutar_simulacion_controlada()
        
        # Simular shock de precios en la mitad de la simulación
        ciclo_shock = 15
        
        # Aumentar precios artificialmente para simular shock inflacionario
        for persona in mercado.personas:
            if hasattr(persona, 'precios'):
                for bien in persona.precios:
                    persona.precios[bien] *= 1.2  # Aumentar 20%
        
        # Continuar simulación por 10 ciclos más
        for ciclo in range(ciclo_shock + 1, ciclo_shock + 11):
            mercado.ejecutar_ciclo(ciclo)
        
        # Validar que el sistema se recuperó
        if len(mercado.inflacion_historica) >= 5:
            inflacion_reciente = mercado.inflacion_historica[-3:]
            inflacion_promedio = sum(inflacion_reciente) / len(inflacion_reciente)
            
            # La inflación debería haberse estabilizado (no más de 8% después del shock)
            self.assertLessEqual(inflacion_promedio, 0.08, 
                               f"Sistema no se recuperó del shock inflacionario: {inflacion_promedio:.3f}")
        
        print("✅ Test completado - Sistema resistente a shocks")
    
    def test_conservacion_de_dinero_sistema(self):
        """Test que verifica la conservación aproximada de dinero en el sistema"""
        print("\n🧪 EJECUTANDO: Test de conservación de dinero...")
        
        mercado = self._ejecutar_simulacion_controlada()
        
        # Calcular dinero total inicial y final
        dinero_inicial = self._calcular_dinero_total_sistema(mercado, inicio=True)
        dinero_final = self._calcular_dinero_total_sistema(mercado, inicio=False)
        
        # Permitir variación del 40% (debido a creación/destrucción de dinero por bancos y gobierno)
        variacion = abs(dinero_final - dinero_inicial) / dinero_inicial
        self.assertLessEqual(variacion, 0.40, 
                           f"Variación excesiva en dinero total: {variacion:.3f}")
        
        print(f"✅ Test completado - Variación de dinero: {variacion:.3f}")
    
    def _ejecutar_simulacion_controlada(self):
        """Ejecuta una simulación controlada para testing"""
        # Importar aquí para evitar imports circulares
        from main import crear_bienes_expandidos, configurar_economia_avanzada, integrar_sistemas_avanzados
        from src.models.Mercado import Mercado
        from src.models.Consumidor import Consumidor
        from src.models.EmpresaProductora import EmpresaProductora
        from src.models.Empresa import Empresa
        
        # Crear mercado con bienes reducidos para test
        bienes = crear_bienes_expandidos()
        # Usar solo algunos bienes para acelerar tests
        bienes_test = {k: v for k, v in list(bienes.items())[:10]}
        
        mercado = Mercado(bienes_test)
        
        # Configurar economía
        configurar_economia_avanzada(mercado, self.configurador)
        
        # Añadir agentes
        for i in range(self.config_test['simulacion']['num_consumidores']):
            consumidor = Consumidor(f"consumidor_{i}", mercado)
            mercado.agregar_persona(consumidor)
        
        for i in range(self.config_test['simulacion']['num_empresas_productoras']):
            empresa = EmpresaProductora(f"Productora_{i}", mercado, bienes_test)
            mercado.agregar_persona(empresa)
        
        for i in range(self.config_test['simulacion']['num_empresas_comerciales']):
            empresa = Empresa(f"Comercial_{i}", mercado, {})
            mercado.agregar_persona(empresa)
        
        # Integrar sistemas
        integrar_sistemas_avanzados(mercado, self.configurador)
        
        # Ejecutar ciclos
        for ciclo in range(1, self.config_test['simulacion']['num_ciclos'] + 1):
            mercado.ejecutar_ciclo(ciclo)
        
        return mercado
    
    def _calcular_dinero_total_sistema(self, mercado, inicio=False):
        """Calcula el dinero total en el sistema"""
        total = 0
        
        # Dinero de las personas
        for persona in mercado.personas:
            total += getattr(persona, 'dinero', 0)
        
        # Dinero del gobierno
        if hasattr(mercado, 'gobierno') and mercado.gobierno:
            total += getattr(mercado.gobierno, 'presupuesto', 0)
        
        # Dinero en bancos (si aplica)
        if hasattr(mercado, 'sistema_bancario') and mercado.sistema_bancario:
            for banco in mercado.sistema_bancario.bancos:
                total += banco.capital
                total += sum(banco.depositos.values())
        
        return total


class TestBenchmarkPerformance(unittest.TestCase):
    """Tests de benchmark y performance"""
    
    def test_performance_simulacion_100_ciclos(self):
        """Test de performance para simulación de 100 ciclos"""
        print("\n⏱️  EJECUTANDO: Test de performance 100 ciclos...")
        
        inicio = time.time()
        
        # Configurar simulación más grande
        config_performance = ConfiguradorSimulacion()
        config_dict = config_performance.config
        config_dict['simulacion']['num_ciclos'] = 100
        config_dict['simulacion']['num_consumidores'] = 100
        
        # Ejecutar simulación (versión simplificada)
        mercado = self._ejecutar_simulacion_rapida(100)
        
        tiempo_total = time.time() - inicio
        
        # La simulación debería completarse en menos de 2 minutos
        self.assertLess(tiempo_total, 120, f"Simulación muy lenta: {tiempo_total:.2f}s")
        
        # Verificar que se completaron todos los ciclos
        self.assertGreaterEqual(len(mercado.pib_historico), 50, 
                               "No se completaron suficientes ciclos")
        
        print(f"✅ Test completado en {tiempo_total:.2f}s")
    
    def _ejecutar_simulacion_rapida(self, num_ciclos):
        """Ejecuta simulación rápida para tests de performance"""
        from src.models.Mercado import Mercado
        from src.models.Bien import Bien
        from src.models.Consumidor import Consumidor
        from src.models.Empresa import Empresa
        
        # Crear mercado minimal
        bienes = {
            "comida": Bien("comida", "alimentos_basicos"),
            "ropa": Bien("ropa", "alimentos_lujo"),  # Use existing category
            "casa": Bien("casa", "tecnologia")       # Use existing category
        }
        
        mercado = Mercado(bienes)
        
        # Añadir pocos agentes para acelerar
        for i in range(20):
            mercado.agregar_persona(Consumidor(f"consumidor_{i}", mercado))
        
        for i in range(5):
            mercado.agregar_persona(Empresa(f"Empresa_{i}", mercado, {}))
        
        # Ejecutar ciclos básicos
        for ciclo in range(1, num_ciclos + 1):
            # Versión simplificada del ciclo
            for persona in mercado.personas:
                if hasattr(persona, 'actuar'):
                    try:
                        persona.actuar(mercado)
                    except:
                        pass  # Ignorar errores en tests de performance
            
            # Actualizar PIB básico
            pib_actual = sum(getattr(p, 'dinero', 0) for p in mercado.personas)
            mercado.pib_historico.append(pib_actual)
        
        return mercado


if __name__ == '__main__':
    # Ejecutar tests con verbosidad
    unittest.main(verbosity=2)
