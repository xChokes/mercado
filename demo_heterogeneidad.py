#!/usr/bin/env python3
"""
Demostración final de heterogeneidad de consumidores y Gini
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from src.models.Mercado import Mercado
from src.models.Bien import Bien
from src.models.Consumidor import Consumidor
from src.systems.ValidadorEconomico import ValidadorEconomico

def demostrar_heterogeneidad():
    """Demuestra la heterogeneidad implementada"""
    print("=== DEMOSTRACIÓN DE HETEROGENEIDAD DE CONSUMIDORES ===")
    
    # Crear mercado
    bienes = {
        'Arroz': Bien('Arroz', 'alimentos_basicos'),
        'Carne': Bien('Carne', 'alimentos_lujo'),
        'Entretenimiento': Bien('Entretenimiento', 'servicios_lujo'),
        'Vivienda': Bien('Vivienda', 'servicios'),
    }
    mercado = Mercado(bienes)
    
    # Configuración de heterogeneidad activada
    config_hetero = {
        'activar': True,
        'distribucion_ingresos': 'lognormal',
        'ingreso_lognormal_mu': 8.5,
        'ingreso_lognormal_sigma': 0.8,
        'ingreso_min_garantizado': 1500,
        'tipo_preferencias': 'cobb_douglas',
        'ces_elasticity_substitution': 1.5,
        'tasa_descuento_temporal': 0.05,
        'factor_paciencia_min': 0.7,
        'factor_paciencia_max': 0.98,
        'gini_objetivo': 0.45
    }
    
    # Crear consumidores heterogéneos
    print("Creando 200 consumidores con heterogeneidad activada...")
    consumidores = []
    for i in range(200):
        consumidor = Consumidor(f'Consumidor_{i+1}', mercado, config_hetero=config_hetero)
        consumidores.append(consumidor)
        mercado.agregar_persona(consumidor)
    
    print("\n=== ANÁLISIS DE HETEROGENEIDAD ===")
    
    # 1. Distribución de ingresos
    ingresos_dinero = [c.dinero for c in consumidores]
    ingresos_mensuales = [c.ingreso_mensual for c in consumidores if c.empleado]
    
    print(f"📊 DISTRIBUCIÓN DE INGRESOS INICIALES:")
    print(f"   Mínimo: ${min(ingresos_dinero):,.2f}")
    print(f"   Máximo: ${max(ingresos_dinero):,.2f}")
    print(f"   Promedio: ${sum(ingresos_dinero)/len(ingresos_dinero):,.2f}")
    print(f"   Mediana: ${sorted(ingresos_dinero)[len(ingresos_dinero)//2]:,.2f}")
    
    print(f"\n💰 INGRESOS MENSUALES (empleados):")
    if ingresos_mensuales:
        print(f"   Mínimo: ${min(ingresos_mensuales):,.2f}")
        print(f"   Máximo: ${max(ingresos_mensuales):,.2f}")
        print(f"   Promedio: ${sum(ingresos_mensuales)/len(ingresos_mensuales):,.2f}")
    
    # 2. Factores de paciencia
    factores_paciencia = [c.factor_paciencia for c in consumidores]
    print(f"\n⏰ FACTORES DE PACIENCIA:")
    print(f"   Mínimo: {min(factores_paciencia):.3f}")
    print(f"   Máximo: {max(factores_paciencia):.3f}")
    print(f"   Promedio: {sum(factores_paciencia)/len(factores_paciencia):.3f}")
    
    # 3. Tipos de preferencias
    tipos_preferencias = [c.tipo_preferencias for c in consumidores]
    print(f"\n🎯 TIPOS DE PREFERENCIAS:")
    for tipo in set(tipos_preferencias):
        count = tipos_preferencias.count(tipo)
        print(f"   {tipo}: {count} consumidores ({count/len(consumidores)*100:.1f}%)")
    
    # 4. Cálculo de Gini
    validador = ValidadorEconomico()
    gini = validador._calcular_gini(ingresos_dinero)
    print(f"\n📈 ÍNDICE DE GINI: {gini:.4f}")
    
    if 0.3 <= gini <= 0.6:
        print("   ✅ Dentro del rango objetivo (0.3-0.6)")
    else:
        print(f"   ⚠️  Fuera del rango objetivo (actual: {gini:.4f})")
    
    # 5. Test de utilidades
    print(f"\n🔧 TEST DE FUNCIONES DE UTILIDAD:")
    consumidor_ejemplo = consumidores[0]
    cantidades_ejemplo = {'Arroz': 5, 'Carne': 2, 'Entretenimiento': 1, 'Vivienda': 1}
    
    utilidad_cd = consumidor_ejemplo.calcular_utilidad_cobb_douglas(cantidades_ejemplo)
    utilidad_ces = consumidor_ejemplo.calcular_utilidad_ces(cantidades_ejemplo)
    
    print(f"   Utilidad Cobb-Douglas: {utilidad_cd:.4f}")
    print(f"   Utilidad CES: {utilidad_ces:.4f}")
    
    # 6. Test de demanda óptima
    precios_ejemplo = {'Arroz': 10, 'Carne': 30, 'Entretenimiento': 50, 'Vivienda': 100}
    presupuesto_ejemplo = 1000
    
    demanda_optima = consumidor_ejemplo.calcular_demanda_optima(presupuesto_ejemplo, precios_ejemplo)
    gasto_total = sum(demanda_optima[bien] * precios_ejemplo[bien] for bien in precios_ejemplo)
    
    print(f"\n🛒 TEST DE DEMANDA ÓPTIMA (Presupuesto: ${presupuesto_ejemplo}):")
    for bien, cantidad in demanda_optima.items():
        gasto_bien = cantidad * precios_ejemplo[bien]
        print(f"   {bien}: {cantidad:.2f} unidades (${gasto_bien:.2f})")
    print(f"   Gasto total: ${gasto_total:.2f}")
    
    # 7. Test de restricción intertemporal
    tasa_baja = 0.02
    tasa_alta = 0.10
    
    propension_baja = consumidor_ejemplo.aplicar_restriccion_intertemporal(1000, tasa_baja)
    propension_alta = consumidor_ejemplo.aplicar_restriccion_intertemporal(1000, tasa_alta)
    
    print(f"\n💸 TEST DE RESTRICCIÓN INTERTEMPORAL:")
    print(f"   Propensión con tasa baja (2%): {propension_baja:.3f}")
    print(f"   Propensión con tasa alta (10%): {propension_alta:.3f}")
    print(f"   Factor paciencia: {consumidor_ejemplo.factor_paciencia:.3f}")
    
    print(f"\n=== CRITERIOS DE ACEPTACIÓN ===")
    
    # Verificar criterios
    criterios_cumplidos = 0
    total_criterios = 3
    
    # 1. Gini reportado (0.3–0.6 configurable)
    if 0.3 <= gini <= 0.6:
        print("✅ 1. Gini reportado en rango objetivo (0.3-0.6)")
        criterios_cumplidos += 1
    else:
        print(f"❌ 1. Gini fuera de rango: {gini:.4f}")
    
    # 2. Consumo agregado responde a ingresos y tasas
    if propension_alta <= propension_baja:  # Con tasas altas, menor propensión al consumo
        print("✅ 2. Consumo responde a tasas de interés")
        criterios_cumplidos += 1
    else:
        print("❌ 2. Consumo no responde apropiadamente a tasas")
    
    # 3. Tests de unidad de utilidades y demanda
    if utilidad_cd > 0 and utilidad_ces > 0 and gasto_total <= presupuesto_ejemplo * 1.01:
        print("✅ 3. Funciones de utilidad y demanda funcionan correctamente")
        criterios_cumplidos += 1
    else:
        print("❌ 3. Error en funciones de utilidad o demanda")
    
    print(f"\n🏆 CRITERIOS CUMPLIDOS: {criterios_cumplidos}/{total_criterios}")
    
    if criterios_cumplidos == total_criterios:
        print("🎉 ¡TODOS LOS CRITERIOS DE ACEPTACIÓN CUMPLIDOS!")
        return True
    else:
        print("⚠️  Algunos criterios no se cumplieron completamente")
        return False

if __name__ == "__main__":
    success = demostrar_heterogeneidad()
    sys.exit(0 if success else 1)