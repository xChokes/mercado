#!/usr/bin/env python3
"""Test muy simple y rápido de las mejoras"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


def test_simple():
    print("🧪 Test simple de mejoras...")

    try:
        # Test 1: Machine Learning
        from src.systems.AnalyticsML import PredictorDemanda
        predictor = PredictorDemanda()
        print("✅ ML: Importación exitosa")

        # Test 2: Configurador
        from src.config.ConfiguradorSimulacion import ConfiguradorSimulacion
        config = ConfiguradorSimulacion()
        ciclos = config.obtener('simulacion', 'num_ciclos', 50)
        print(f"✅ Config: {ciclos} ciclos configurados")

        # Test 3: Visualización
        from src.systems.VisualizacionAvanzada import DashboardEconomico
        print("✅ Dashboard: Importación exitosa")

        # Test 4: Precios dinámicos
        from src.systems.PreciosDinamicos import SistemaPreciosDinamicos
        print("✅ Precios dinámicos: Importación exitosa")

        # Test 5: Crear mercado básico
        from src.models.Mercado import Mercado
        from src.models.Bien import Bien

        bienes = {'Pan': Bien('Pan', 'alimentos_basicos')}
        mercado = Mercado(bienes)
        print("✅ Mercado: Creación exitosa")

        print("\n🎉 TODAS LAS MEJORAS ESTÁN DISPONIBLES")
        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    test_simple()
