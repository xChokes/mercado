#!/usr/bin/env python3
"""
Test simple para validar el cálculo del índice de Gini
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from src.models.Mercado import Mercado
from src.models.Bien import Bien
from src.models.Consumidor import Consumidor
from src.systems.ValidadorEconomico import ValidadorEconomico

def test_gini_calculation():
    """Test simple del cálculo de Gini"""
    print("=== Test de Cálculo de Índice de Gini ===")
    
    # Crear mercado simple
    bienes = {'Arroz': Bien('Arroz', 'alimentos_basicos')}
    mercado = Mercado(bienes)
    
    # Configuración de heterogeneidad
    config_hetero = {
        'activar': True,
        'distribucion_ingresos': 'lognormal',
        'ingreso_lognormal_mu': 8.5,
        'ingreso_lognormal_sigma': 0.8,
        'ingreso_min_garantizado': 1500,
        'tipo_preferencias': 'cobb_douglas',
        'gini_objetivo': 0.45
    }
    
    mercado.config_hetero = config_hetero
    
    # Crear consumidores con distribución heterogénea
    print("Creando 100 consumidores con distribución lognormal...")
    consumidores = []
    for i in range(100):
        consumidor = Consumidor(f'Test_{i}', mercado, config_hetero=config_hetero)
        consumidores.append(consumidor)
        mercado.agregar_persona(consumidor)
    
    # Calcular Gini
    validador = ValidadorEconomico()
    ingresos = [c.dinero for c in consumidores]
    
    print(f"Ingresos estadísticas:")
    print(f"  Mínimo: ${min(ingresos):,.2f}")
    print(f"  Máximo: ${max(ingresos):,.2f}")
    print(f"  Promedio: ${sum(ingresos)/len(ingresos):,.2f}")
    print(f"  Mediana: ${sorted(ingresos)[len(ingresos)//2]:,.2f}")
    
    gini = validador._calcular_gini(ingresos)
    print(f"\nÍndice de Gini calculado: {gini:.4f}")
    
    # Validar que está en rango esperado
    if 0.25 <= gini <= 0.70:
        print("✅ Gini en rango esperado para economía real")
    else:
        print("⚠️  Gini fuera del rango típico")
    
    # Test con distribución más igual
    print("\n=== Test con distribución uniforme ===")
    ingresos_uniformes = [5000] * 50 + [6000] * 50
    gini_uniforme = validador._calcular_gini(ingresos_uniformes)
    print(f"Gini con distribución más uniforme: {gini_uniforme:.4f}")
    
    # Test con distribución muy desigual
    print("\n=== Test con distribución muy desigual ===")
    ingresos_desiguales = [1000] * 80 + [50000] * 20
    gini_desigual = validador._calcular_gini(ingresos_desiguales)
    print(f"Gini con distribución muy desigual: {gini_desigual:.4f}")
    
    print("\n=== Resumen ===")
    print(f"Gini lognormal: {gini:.4f}")
    print(f"Gini uniforme: {gini_uniforme:.4f}")
    print(f"Gini desigual: {gini_desigual:.4f}")
    
    # Verificar orden correcto
    if gini_uniforme < gini < gini_desigual:
        print("✅ Orden correcto: uniforme < lognormal < desigual")
        return True
    else:
        print("❌ Error en el orden de desigualdad")
        return False

if __name__ == "__main__":
    success = test_gini_calculation()
    sys.exit(0 if success else 1)