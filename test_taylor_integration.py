#!/usr/bin/env python3
"""
Test Script para Banco Central con Regla de Taylor
==================================================

Script simple para probar la integración del nuevo sistema de política monetaria.
"""

import sys
import os

# Configurar path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.config.ConfiguradorSimulacion import ConfiguradorSimulacion
from src.systems.central_bank import CentralBank
from main import crear_bienes_expandidos
from src.models.Mercado import Mercado

def test_taylor_rule_integration():
    """Test de integración del sistema Taylor Rule"""
    print("🧪 TEST: Integración Banco Central con Regla de Taylor")
    print("=" * 60)
    
    # Cargar configuración
    configurador = ConfiguradorSimulacion()
    configurador.archivo_config = 'config_test_taylor.json'
    config = configurador.cargar_configuracion()
    
    print(f"✅ Configuración cargada")
    print(f"📊 Política monetaria activa: {config['politica_monetaria']['activar']}")
    
    # Crear mercado básico
    bienes = crear_bienes_expandidos()
    bienes_test = {k: v for k, v in list(bienes.items())[:5]}
    mercado = Mercado(bienes_test)
    
    # Simular datos históricos
    mercado.pib_historico = [100000, 101000, 102000, 103000, 105000]
    mercado.inflacion_historica = [0.02, 0.025, 0.03, 0.035, 0.04]  # Inflación creciente
    
    # Crear banco central con Taylor Rule
    banco_central = CentralBank(mercado, config['politica_monetaria'])
    
    print(f"🏦 Banco Central inicializado:")
    print(f"   Meta inflación: {banco_central.params.meta_inflacion:.1%}")
    print(f"   Tasa neutral: {banco_central.params.tasa_neutral:.1%}")
    print(f"   Peso inflación: {banco_central.params.peso_inflacion}")
    print(f"   Peso PIB: {banco_central.params.peso_producto}")
    
    # Simular 5 ciclos de política monetaria
    print("\n📈 Simulando política monetaria (5 ciclos):")
    print("-" * 50)
    
    for ciclo in range(1, 6):
        # Simular inflación creciente que requiere respuesta
        if ciclo > 2:
            # Después del ciclo 2, la inflación sube por encima de la meta
            mercado.inflacion_historica.append(0.03 + (ciclo - 2) * 0.005)
        
        resultado = banco_central.ejecutar_politica_monetaria(ciclo)
        
        print(f"Ciclo {ciclo}:")
        print(f"  📊 Inflación actual: {resultado['inflacion_actual']:.1%} (meta: {resultado['meta_inflacion']:.1%})")
        print(f"  💰 Tasa anterior: {resultado['tasa_anterior']:.2%}")
        print(f"  💰 Tasa nueva: {resultado['tasa_interes']:.2%}")
        print(f"  🎯 Acción: {resultado['accion']}")
        print(f"  💭 Justificación: {resultado['justificacion']}")
        print()
    
    # Estadísticas finales
    stats = banco_central.obtener_estadisticas()
    print("📊 ESTADÍSTICAS FINALES:")
    print("-" * 30)
    print(f"Decisiones totales: {stats['decisiones_totales']}")
    print(f"Cambios de política: {stats['cambios_tasa_totales']}")
    print(f"Convergencia inflación: {stats['convergencia_inflacion']:.1%}")
    print(f"Tasa final: {stats['tasa_actual']:.2%}")
    
    # Test de shock inflacionario
    print("\n🚨 TEST: Respuesta a Shock Inflacionario")
    print("-" * 40)
    
    shock_response = banco_central.simular_shock_inflacionario(0.03)  # 3% shock
    print(f"Shock de inflación: +{shock_response['shock_inflacion']:.1%}")
    print(f"Respuesta de tasa: +{shock_response['cambio_puntos_basicos']} puntos básicos")
    print(f"Respuesta adecuada: {'✅ SÍ' if shock_response['respuesta_adecuada'] else '❌ NO'}")
    
    print("\n✅ TEST COMPLETADO EXITOSAMENTE")
    return True

if __name__ == "__main__":
    test_taylor_rule_integration()