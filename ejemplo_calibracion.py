#!/usr/bin/env python3
"""
Ejemplo de uso del sistema de calibración automática
Demuestra diferentes casos de uso y análisis de resultados
"""

import os
import sys
import json
import pandas as pd
from pathlib import Path

# Agregar el directorio raíz al path
current_dir = Path(__file__).parent
root_dir = current_dir.parent
sys.path.append(str(root_dir))

from src.utils.calibration_runner import CalibrationRunner, CalibrationConfig


def ejemplo_calibracion_basica():
    """Ejemplo 1: Calibración económica básica"""
    print("=" * 60)
    print("EJEMPLO 1: CALIBRACIÓN ECONÓMICA BÁSICA")
    print("=" * 60)
    
    # Configuración simple para calibración básica
    config = CalibrationConfig(
        parameters={
            'pib_inicial': (80000, 120000),
            'tasa_inflacion_objetivo': (0.015, 0.030),
            'tasa_desempleo_inicial': (0.08, 0.15),
        },
        optimization_method="bayesian",
        n_trials=10,  # Pocos trials para demo rápida
        simulation_cycles=8,
        target_metrics={
            'pib_final': (100000.0, 1.0),
            'inflacion_promedio': (0.02, 2.0),
            'desempleo_promedio': (0.06, 1.5),
        },
        results_dir="results/calibrations/ejemplo1"
    )
    
    print(f"Configuración:")
    print(f"- Método: {config.optimization_method}")
    print(f"- Trials: {config.n_trials}")
    print(f"- Ciclos por simulación: {config.simulation_cycles}")
    print(f"- Parámetros: {list(config.parameters.keys())}")
    
    # Ejecutar calibración
    runner = CalibrationRunner(config)
    results = runner.run_calibration()
    
    # Mostrar mejores resultados
    best_result = max(results, key=lambda r: r.score)
    print(f"\n🏆 MEJOR RESULTADO:")
    print(f"Score: {best_result.score:.4f}")
    print(f"PIB Final: ${best_result.metrics.get('pib_final', 0):,.0f}")
    print(f"Inflación: {best_result.metrics.get('inflacion_promedio', 0):.3f}")
    print(f"Desempleo: {best_result.metrics.get('desempleo_promedio', 0):.3f}")
    
    return results


def ejemplo_analisis_sensibilidad():
    """Ejemplo 2: Análisis de sensibilidad de precios"""
    print("\n" + "=" * 60)
    print("EJEMPLO 2: ANÁLISIS DE SENSIBILIDAD DE PRECIOS")
    print("=" * 60)
    
    # Configuración enfocada en parámetros de precios
    config = CalibrationConfig(
        parameters={
            'ajuste_maximo_por_ciclo': (0.05, 0.25),
            'sensibilidad_competencia': (0.05, 0.20),
        },
        optimization_method="grid",
        n_trials=25,  # 5x5 grid
        simulation_cycles=5,  # Rápido para demo
        target_metrics={
            'inflacion_promedio': (0.02, 3.0),  # Peso alto en inflación
            'volatilidad_inflacion': (0.01, 1.0),
        },
        results_dir="results/calibrations/ejemplo2"
    )
    
    print(f"Configuración:")
    print(f"- Método: {config.optimization_method}")
    print(f"- Grid: 5x5 = 25 combinaciones")
    print(f"- Enfoque: Estabilidad de precios")
    
    # Ejecutar calibración
    runner = CalibrationRunner(config)
    results = runner.run_calibration()
    
    # Análisis de sensibilidad
    df_results = pd.DataFrame([
        {**r.parameters, **r.metrics, 'score': r.score} 
        for r in results
    ])
    
    print(f"\n📊 ANÁLISIS DE SENSIBILIDAD:")
    print(f"Rango scores: {df_results['score'].min():.4f} - {df_results['score'].max():.4f}")
    
    # Correlaciones
    correlations = df_results.corr()['score'].sort_values(ascending=False)
    print(f"\nCorrelaciones con score:")
    for param, corr in correlations.items():
        if param != 'score' and abs(corr) > 0.1:
            print(f"  {param}: {corr:.3f}")
    
    return results


def ejemplo_configuracion_personalizada():
    """Ejemplo 3: Configuración personalizada completa"""
    print("\n" + "=" * 60)
    print("EJEMPLO 3: CONFIGURACIÓN PERSONALIZADA")
    print("=" * 60)
    
    # Configuración avanzada con muchos parámetros
    config = CalibrationConfig(
        parameters={
            'pib_inicial': (85000, 115000),
            'tasa_inflacion_objetivo': (0.018, 0.025),
            'tasa_desempleo_inicial': (0.06, 0.12),
            'ajuste_maximo_por_ciclo': (0.08, 0.20),
            'probabilidad_contratacion_base': (0.3, 0.6),
            'tasa_interes_base': (0.02, 0.06),
        },
        optimization_method="bayesian",
        n_trials=15,
        simulation_cycles=10,
        target_metrics={
            'pib_final': (100000.0, 1.5),      # Peso alto PIB
            'inflacion_promedio': (0.02, 2.0), # Peso alto inflación
            'desempleo_promedio': (0.08, 1.0), # Tolerancia mayor
            'crecimiento_pib': (0.02, 1.0),    # Crecimiento positivo
            'transacciones_totales': (50.0, 0.5), # Actividad económica
        },
        results_dir="results/calibrations/ejemplo3"
    )
    
    print(f"Configuración:")
    print(f"- Parámetros: {len(config.parameters)}")
    print(f"- Métricas objetivo: {len(config.target_metrics)}")
    print(f"- Trials: {config.n_trials}")
    
    # Ejecutar calibración
    runner = CalibrationRunner(config)
    results = runner.run_calibration()
    
    # Análisis multi-objetivo
    print(f"\n🎯 ANÁLISIS MULTI-OBJETIVO:")
    
    # Top 3 resultados
    top_results = sorted(results, key=lambda r: r.score, reverse=True)[:3]
    
    for i, result in enumerate(top_results, 1):
        print(f"\nTop {i} (Score: {result.score:.4f}):")
        print(f"  PIB: ${result.metrics.get('pib_final', 0):,.0f}")
        print(f"  Inflación: {result.metrics.get('inflacion_promedio', 0):.3f}")
        print(f"  Desempleo: {result.metrics.get('desempleo_promedio', 0):.3f}")
        print(f"  Crecimiento: {result.metrics.get('crecimiento_pib', 0):.3f}")
    
    return results


def ejemplo_comparacion_metodos():
    """Ejemplo 4: Comparación entre métodos de optimización"""
    print("\n" + "=" * 60)
    print("EJEMPLO 4: COMPARACIÓN BAYESIANO vs GRID")
    print("=" * 60)
    
    # Configuración base común
    base_params = {
        'pib_inicial': (90000, 110000),
        'tasa_inflacion_objetivo': (0.018, 0.022),
    }
    
    base_metrics = {
        'pib_final': (100000.0, 1.0),
        'inflacion_promedio': (0.02, 2.0),
    }
    
    # Bayesiano
    print("Ejecutando optimización Bayesiana...")
    config_bayes = CalibrationConfig(
        parameters=base_params,
        optimization_method="bayesian",
        n_trials=8,
        simulation_cycles=5,
        target_metrics=base_metrics,
        results_dir="results/calibrations/bayes_comparison"
    )
    
    runner_bayes = CalibrationRunner(config_bayes)
    results_bayes = runner_bayes.run_calibration()
    best_bayes = max(results_bayes, key=lambda r: r.score)
    
    # Grid search
    print("Ejecutando grid search...")
    config_grid = CalibrationConfig(
        parameters=base_params,
        optimization_method="grid",
        n_trials=16,  # 4x4 grid
        simulation_cycles=5,
        target_metrics=base_metrics,
        results_dir="results/calibrations/grid_comparison"
    )
    
    runner_grid = CalibrationRunner(config_grid)
    results_grid = runner_grid.run_calibration()
    best_grid = max(results_grid, key=lambda r: r.score)
    
    # Comparación
    print(f"\n📈 COMPARACIÓN DE RESULTADOS:")
    print(f"Bayesiano - Mejor score: {best_bayes.score:.4f}")
    print(f"  PIB: ${best_bayes.metrics.get('pib_final', 0):,.0f}")
    print(f"  Inflación: {best_bayes.metrics.get('inflacion_promedio', 0):.4f}")
    
    print(f"\nGrid Search - Mejor score: {best_grid.score:.4f}")
    print(f"  PIB: ${best_grid.metrics.get('pib_final', 0):,.0f}")
    print(f"  Inflación: {best_grid.metrics.get('inflacion_promedio', 0):.4f}")
    
    if best_bayes.score > best_grid.score:
        print("\n🏆 Bayesiano obtuvo mejor resultado")
    elif best_grid.score > best_bayes.score:
        print("\n🏆 Grid Search obtuvo mejor resultado")
    else:
        print("\n🤝 Ambos métodos obtuvieron resultados similares")
    
    return results_bayes, results_grid


def generar_reporte_completo(todos_los_resultados):
    """Genera un reporte consolidado de todos los ejemplos"""
    print("\n" + "=" * 60)
    print("REPORTE CONSOLIDADO DE CALIBRACIÓN")
    print("=" * 60)
    
    # Consolidar todos los resultados
    all_results = []
    for ejemplo, results in todos_los_resultados.items():
        if isinstance(results, tuple):  # Comparación métodos
            results = results[0] + results[1]  # Combinar ambos
        
        for result in results:
            result_dict = {
                'ejemplo': ejemplo,
                'score': result.score,
                'pib_final': result.metrics.get('pib_final', 0),
                'inflacion_promedio': result.metrics.get('inflacion_promedio', 0),
                'desempleo_promedio': result.metrics.get('desempleo_promedio', 0),
                'execution_time': result.execution_time
            }
            all_results.append(result_dict)
    
    df_consolidado = pd.DataFrame(all_results)
    
    print(f"Total de trials ejecutados: {len(df_consolidado)}")
    print(f"Score promedio: {df_consolidado['score'].mean():.4f}")
    print(f"Mejor score global: {df_consolidado['score'].max():.4f}")
    print(f"Tiempo total de simulación: {df_consolidado['execution_time'].sum():.1f}s")
    
    # Mejor resultado por ejemplo
    print(f"\nMejores resultados por ejemplo:")
    for ejemplo in df_consolidado['ejemplo'].unique():
        ejemplo_data = df_consolidado[df_consolidado['ejemplo'] == ejemplo]
        best_idx = ejemplo_data['score'].idxmax()
        best = ejemplo_data.loc[best_idx]
        print(f"  {ejemplo}: Score {best['score']:.4f} | PIB ${best['pib_final']:,.0f}")
    
    # Guardar reporte consolidado
    reporte_path = "results/calibrations/reporte_consolidado.csv"
    os.makedirs(os.path.dirname(reporte_path), exist_ok=True)
    df_consolidado.to_csv(reporte_path, index=False)
    print(f"\n📁 Reporte guardado en: {reporte_path}")


def main():
    """Función principal - ejecuta todos los ejemplos"""
    print("🚀 SISTEMA DE CALIBRACIÓN AUTOMÁTICA - EJEMPLOS DE USO")
    print("=" * 80)
    
    # Crear directorio base de resultados
    os.makedirs("results/calibrations", exist_ok=True)
    
    # Ejecutar ejemplos
    resultados = {}
    
    try:
        resultados['basica'] = ejemplo_calibracion_basica()
    except Exception as e:
        print(f"❌ Error en calibración básica: {e}")
        resultados['basica'] = []
    
    try:
        resultados['sensibilidad'] = ejemplo_analisis_sensibilidad()
    except Exception as e:
        print(f"❌ Error en análisis de sensibilidad: {e}")
        resultados['sensibilidad'] = []
    
    try:
        resultados['personalizada'] = ejemplo_configuracion_personalizada()
    except Exception as e:
        print(f"❌ Error en configuración personalizada: {e}")
        resultados['personalizada'] = []
    
    try:
        resultados['comparacion'] = ejemplo_comparacion_metodos()
    except Exception as e:
        print(f"❌ Error en comparación de métodos: {e}")
        resultados['comparacion'] = ([], [])
    
    # Generar reporte final
    try:
        generar_reporte_completo(resultados)
    except Exception as e:
        print(f"❌ Error generando reporte: {e}")
    
    print("\n✅ EJEMPLOS COMPLETADOS")
    print("\nPara más información consultar:")
    print("- docs/CALIBRACION_GUIA.md")
    print("- results/calibrations/ (archivos de resultados)")


if __name__ == "__main__":
    main()