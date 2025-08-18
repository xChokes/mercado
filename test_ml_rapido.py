#!/usr/bin/env python3
"""Test rápido del sistema ML mejorado"""

from src.models.Bien import Bien
from src.models.Mercado import Mercado
from src.systems.AnalyticsML import PredictorDemanda
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


def test_ml_mejorado():
    print("🧪 Probando sistema ML mejorado...")

    # Crear mercado de prueba
    mercado = Mercado()
    bien = Bien('Arroz', 'alimentos_basicos')
    mercado.agregar_bien('Arroz', bien)
    mercado.pib_historico = [100000, 105000]
    mercado.desempleo_historico = [0.05, 0.06]
    mercado.inflacion_historica = [0.02, 0.03]
    mercado.ciclo_actual = 2
    mercado.transacciones = []

    # Test del predictor mejorado
    predictor = PredictorDemanda()
    resultado = predictor.entrenar(mercado, 'Arroz')
    print(f'✅ ML Training exitoso: {resultado}')
    print(f'✅ Modelo entrenado: {predictor.caracteristicas_entrenadas}')

    if predictor.caracteristicas_entrenadas:
        # Test de predicción
        demanda = predictor.predecir_demanda(mercado, 'Arroz')
        print(f'✅ Predicción de demanda: {demanda}')
        return True
    else:
        print('❌ Modelo no se entrenó correctamente')
        return False


if __name__ == "__main__":
    test_ml_mejorado()
