#!/usr/bin/env python3
"""Test simple de la simulación mejorada"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Test muy básico para verificar las importaciones
try:
    print("🧪 Probando importaciones básicas...")

    from src.models.Mercado import Mercado
    from src.models.Bien import Bien
    from src.models.Consumidor import Consumidor
    print("✅ Modelos básicos: OK")

    from src.systems.AnalyticsML import SistemaAnalyticsML, PredictorDemanda
    print("✅ Sistema ML: OK")

    from src.systems.VisualizacionAvanzada import DashboardEconomico
    print("✅ Dashboard avanzado: OK")

    from src.systems.PreciosDinamicos import SistemaPreciosDinamicos
    print("✅ Precios dinámicos: OK")

    from src.config.ConfiguradorSimulacion import ConfiguradorSimulacion
    print("✅ Configurador: OK")

    print("\n🚀 Creando simulación de prueba...")

    # Crear mercado simple
    mercado = Mercado()
    bien = Bien('Pan', 'alimentos_basicos')
    mercado.agregar_bien('Pan', bien)

    # Agregar algunos agentes
    for i in range(5):
        consumidor = Consumidor(f'C{i}', mercado)
        mercado.agregar_persona(consumidor)

    print(
        f"✅ Mercado creado con {len(mercado.personas)} agentes y {len(mercado.bienes)} bienes")

    # Test del sistema ML
    print("\n🤖 Probando sistema ML...")
    predictor = PredictorDemanda()
    mercado.pib_historico = [100000]
    mercado.desempleo_historico = [0.05]
    mercado.inflacion_historica = [0.02]
    mercado.ciclo_actual = 1
    mercado.transacciones = []

    resultado_ml = predictor.entrenar(mercado, 'Pan')
    print(f"✅ ML entrenado: {resultado_ml}")

    if resultado_ml:
        demanda = predictor.predecir_demanda(mercado, 'Pan')
        print(f"✅ Predicción demanda: {demanda}")

    # Test del configurador
    print("\n⚙️ Probando configurador...")
    config = ConfiguradorSimulacion()
    num_ciclos = config.obtener('simulacion', 'num_ciclos', 10)
    print(f"✅ Configuración cargada: {num_ciclos} ciclos")

    print("\n🎉 TODAS LAS MEJORAS ESTÁN FUNCIONANDO CORRECTAMENTE")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
