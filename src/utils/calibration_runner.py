"""
Pipeline de Calibración Automática y Análisis de Sensibilidad
Desarrolla optimización y validación de parámetros para métricas macroeconómicas realistas.
"""

import os
import sys
import json
import time
import logging
import argparse
import numpy as np
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, asdict
import optuna
from optuna.samplers import TPESampler, GridSampler
from optuna.pruners import MedianPruner
import itertools

# Agregar el directorio raíz al path para imports
current_dir = Path(__file__).parent
root_dir = current_dir.parent.parent
sys.path.append(str(root_dir))

from src.config.DatosEconomicosReales import CalibradorEconomicoRealista, IndicadoresEconomicosReales
from src.config.ConfiguradorSimulacion import ConfiguradorSimulacion


@dataclass
class CalibrationResult:
    """Resultado de una ejecución de calibración"""
    parameters: Dict[str, float]
    metrics: Dict[str, float]
    score: float
    execution_time: float
    trial_number: Optional[int] = None
    success: bool = True
    error_message: Optional[str] = None


@dataclass
class CalibrationConfig:
    """Configuración del proceso de calibración"""
    # Parámetros de calibración
    parameters: Dict[str, Tuple[float, float]] = None  # {param_name: (min, max)}
    
    # Configuración de optimización
    optimization_method: str = "bayesian"  # "bayesian", "grid", "random"
    n_trials: int = 100
    timeout_seconds: Optional[float] = None
    
    # Configuración de simulación
    simulation_cycles: int = 20  # Reducido para calibración rápida
    base_config_file: str = "config_simulacion.json"
    
    # Métricas objetivo
    target_metrics: Dict[str, Tuple[float, float]] = None  # {metric: (target, weight)}
    
    # Configuración de resultados
    results_dir: str = "results/calibrations"
    save_intermediate: bool = True


class CalibrationRunner:
    """Pipeline principal de calibración automática"""
    
    def __init__(self, config: CalibrationConfig):
        self.config = config
        self.calibrador_economico = CalibradorEconomicoRealista()
        self.indicadores_reales = IndicadoresEconomicosReales()
        self.results: List[CalibrationResult] = []
        
        # Configurar parámetros por defecto si no están definidos
        if self.config.parameters is None or not self.config.parameters:
            self.config.parameters = self.get_default_parameter_space()
        
        # Configurar logging
        self.setup_logging()
        
        # Crear directorio de resultados
        os.makedirs(self.config.results_dir, exist_ok=True)
        
        # Cargar configuración base
        self.base_config = self.load_base_config()
        
        # Configurar métricas objetivo por defecto
        if self.config.target_metrics is None:
            self.config.target_metrics = self.get_default_target_metrics()
    
    def setup_logging(self):
        """Configura el sistema de logging"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"{self.config.results_dir}/calibration_{timestamp}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("Pipeline de calibración iniciado")
    
    def load_base_config(self) -> Dict:
        """Carga la configuración base del simulador"""
        config_path = os.path.join(str(root_dir), self.config.base_config_file)
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            self.logger.info(f"Configuración base cargada desde {config_path}")
            return config
        except Exception as e:
            self.logger.error(f"Error cargando configuración base: {e}")
            raise
    
    def get_default_target_metrics(self) -> Dict[str, Tuple[float, float]]:
        """Define métricas objetivo por defecto basadas en indicadores reales"""
        return {
            'pib_final': (100000.0, 1.0),  # (target, weight)
            'inflacion_promedio': (0.02, 2.0),  # 2% target, peso alto
            'desempleo_promedio': (0.06, 1.5),  # 6% target
            'crecimiento_pib': (0.02, 1.0),  # 2% crecimiento
            'volatilidad_inflacion': (0.01, 0.5),  # Baja volatilidad
        }
    
    def get_default_parameter_space(self) -> Dict[str, Tuple[float, float]]:
        """Define el espacio de parámetros por defecto basado en datos económicos reales"""
        return {
            # PIB inicial
            'pib_inicial': (50000, 200000),
            
            # Parámetros de inflación
            'tasa_inflacion_objetivo': (0.005, 0.05),  # 0.5% - 5%
            
            # Elasticidades
            'elasticidad_precio_base': (-2.0, -0.3),  # Elasticidad precio-demanda
            'elasticidad_ingreso_base': (0.5, 2.0),   # Elasticidad ingreso-demanda
            
            # Rigidez de precios
            'ajuste_maximo_por_ciclo': (0.05, 0.30),  # 5% - 30% ajuste máximo
            'sensibilidad_competencia': (0.05, 0.25), # Sensibilidad a competencia
            
            # Mercado laboral (intensidad búsqueda)
            'probabilidad_contratacion_base': (0.2, 0.8),
            'habilidad_minima_base': (0.05, 0.3),
            
            # Sistema bancario
            'tasa_interes_base': (0.01, 0.08),        # 1% - 8%
            'ratio_prestamo_ingreso': (3.0, 7.0),    # Ratio préstamo/ingreso
            
            # Desempleo inicial
            'tasa_desempleo_inicial': (0.05, 0.20),   # 5% - 20%
        }
    
    def apply_parameters_to_config(self, parameters: Dict[str, float], base_config: Dict) -> Dict:
        """Aplica parámetros de calibración a la configuración base"""
        config = base_config.copy()
        
        # Aplicar parámetros económicos básicos
        if 'pib_inicial' in parameters:
            config['economia']['pib_inicial'] = parameters['pib_inicial']
        
        if 'tasa_inflacion_objetivo' in parameters:
            config['economia']['tasa_inflacion_objetivo'] = parameters['tasa_inflacion_objetivo']
        
        if 'tasa_desempleo_inicial' in parameters:
            config['economia']['tasa_desempleo_inicial'] = parameters['tasa_desempleo_inicial']
        
        # Aplicar parámetros de precios
        if 'ajuste_maximo_por_ciclo' in parameters:
            if 'precios' not in config:
                config['precios'] = {}
            config['precios']['ajuste_maximo_por_ciclo'] = parameters['ajuste_maximo_por_ciclo']
        
        if 'sensibilidad_competencia' in parameters:
            if 'precios' not in config:
                config['precios'] = {}
            config['precios']['sensibilidad_competencia'] = parameters['sensibilidad_competencia']
        
        # Aplicar parámetros de mercado laboral
        if 'probabilidad_contratacion_base' in parameters:
            if 'mercado_laboral' not in config:
                config['mercado_laboral'] = {}
            config['mercado_laboral']['probabilidad_contratacion_base'] = parameters['probabilidad_contratacion_base']
        
        if 'habilidad_minima_base' in parameters:
            if 'mercado_laboral' not in config:
                config['mercado_laboral'] = {}
            config['mercado_laboral']['habilidad_minima_base'] = parameters['habilidad_minima_base']
        
        # Aplicar parámetros bancarios
        if 'tasa_interes_base' in parameters:
            if 'sistema_bancario' not in config:
                config['sistema_bancario'] = {}
            config['sistema_bancario']['tasa_interes_base'] = parameters['tasa_interes_base']
        
        if 'ratio_prestamo_ingreso' in parameters:
            if 'sistema_bancario' not in config:
                config['sistema_bancario'] = {}
            config['sistema_bancario']['ratio_prestamo_ingreso'] = parameters['ratio_prestamo_ingreso']
        
        # Reducir ciclos para calibración rápida
        config['simulacion']['num_ciclos'] = self.config.simulation_cycles
        
        # Desactivar sistemas lentos durante calibración
        if 'agentes_ia' in config:
            config['agentes_ia']['activar'] = False
        
        return config
    
    def run_simulation_with_parameters(self, parameters: Dict[str, float]) -> Dict[str, float]:
        """Ejecuta simulación con parámetros específicos y retorna métricas"""
        try:
            # Aplicar parámetros a configuración
            config_dict = self.apply_parameters_to_config(parameters, self.base_config)
            
            # Crear configurador temporal
            configurador = ConfiguradorSimulacion()
            configurador.config = config_dict
            
            # Importar función de simulación
            from main import ejecutar_simulacion_completa
            
            # Ejecutar simulación con logging mínimo
            old_level = logging.getLogger().level
            logging.getLogger().setLevel(logging.ERROR)
            
            try:
                # Ejecutar simulación - retorna el objeto mercado directamente
                mercado = ejecutar_simulacion_completa(configurador, prefijo_resultados="calibration_temp")
                
                # Extraer métricas directamente del mercado
                metrics = self.extract_metrics_from_mercado(mercado)
                
                return metrics
                
            finally:
                logging.getLogger().setLevel(old_level)
                
        except Exception as e:
            self.logger.warning(f"Error en simulación: {e}")
            return self.get_default_failure_metrics()
    
    def extract_metrics_from_mercado(self, mercado) -> Dict[str, float]:
        """Extrae métricas clave directamente del objeto mercado"""
        if mercado is None:
            return self.get_default_failure_metrics()
        
        try:
            # PIB final y crecimiento
            pib_historico = getattr(mercado, 'pib_historico', [])
            pib_final = pib_historico[-1] if pib_historico else 0
            pib_inicial = pib_historico[0] if len(pib_historico) > 1 else pib_final
            crecimiento_pib = (pib_final - pib_inicial) / pib_inicial if pib_inicial > 0 else 0
            
            # Inflación
            inflacion_historico = getattr(mercado, 'inflacion_historico', [])
            inflacion_promedio = np.mean(inflacion_historico) if inflacion_historico else 0
            volatilidad_inflacion = np.std(inflacion_historico) if len(inflacion_historico) > 1 else 0
            
            # Desempleo
            desempleo_historico = getattr(mercado, 'desempleo_historico', [])
            if not desempleo_historico:
                # Calcular desempleo actual si no hay histórico
                consumidores = mercado.getConsumidores() if hasattr(mercado, 'getConsumidores') else []
                total_consumidores = len(consumidores)
                desempleados = len([c for c in consumidores if not getattr(c, 'empleado', True)])
                desempleo_actual = desempleados / max(1, total_consumidores)
                desempleo_promedio = desempleo_actual
            else:
                desempleo_promedio = np.mean(desempleo_historico)
            
            # Métricas de estabilidad
            transacciones_totales = getattr(mercado, 'transacciones_totales', 0)
            
            empresas = mercado.getEmpresas() if hasattr(mercado, 'getEmpresas') else []
            empresas_activas = len([e for e in empresas if not getattr(e, 'en_quiebra', False)])
            
            return {
                'pib_final': float(pib_final),
                'crecimiento_pib': float(crecimiento_pib),
                'inflacion_promedio': float(inflacion_promedio),
                'volatilidad_inflacion': float(volatilidad_inflacion),
                'desempleo_promedio': float(desempleo_promedio),
                'transacciones_totales': float(transacciones_totales),
                'empresas_activas': float(empresas_activas),
            }
            
        except Exception as e:
            self.logger.warning(f"Error extrayendo métricas del mercado: {e}")
            return self.get_default_failure_metrics()
    
    def extract_metrics_from_result(self, resultado) -> Dict[str, float]:
        """Extrae métricas clave del resultado de simulación"""
        if resultado is None:
            return self.get_default_failure_metrics()
        
        try:
            # Obtener métricas del mercado
            mercado = resultado.get('mercado')
            if mercado is None:
                return self.get_default_failure_metrics()
            
            # PIB final y crecimiento
            pib_historico = getattr(mercado, 'pib_historico', [])
            pib_final = pib_historico[-1] if pib_historico else 0
            pib_inicial = pib_historico[0] if pib_historico else 1
            crecimiento_pib = (pib_final - pib_inicial) / pib_inicial if pib_inicial > 0 else 0
            
            # Inflación
            inflacion_historico = getattr(mercado, 'inflacion_historico', [])
            inflacion_promedio = np.mean(inflacion_historico) if inflacion_historico else 0
            volatilidad_inflacion = np.std(inflacion_historico) if inflacion_historico else 0
            
            # Desempleo
            desempleo_historico = getattr(mercado, 'desempleo_historico', [])
            desempleo_promedio = np.mean(desempleo_historico) if desempleo_historico else 0
            
            # Métricas de estabilidad
            transacciones_totales = getattr(mercado, 'transacciones_totales', 0)
            empresas_activas = len([e for e in mercado.getEmpresas() if not getattr(e, 'en_quiebra', False)])
            
            return {
                'pib_final': float(pib_final),
                'crecimiento_pib': float(crecimiento_pib),
                'inflacion_promedio': float(inflacion_promedio),
                'volatilidad_inflacion': float(volatilidad_inflacion),
                'desempleo_promedio': float(desempleo_promedio),
                'transacciones_totales': float(transacciones_totales),
                'empresas_activas': float(empresas_activas),
            }
            
        except Exception as e:
            self.logger.warning(f"Error extrayendo métricas: {e}")
            return self.get_default_failure_metrics()
    
    def get_default_failure_metrics(self) -> Dict[str, float]:
        """Métricas por defecto para simulaciones fallidas"""
        return {
            'pib_final': 0.0,
            'crecimiento_pib': -1.0,
            'inflacion_promedio': 1.0,  # Hiperinflación como penalización
            'volatilidad_inflacion': 1.0,
            'desempleo_promedio': 1.0,  # 100% desempleo como penalización
            'transacciones_totales': 0.0,
            'empresas_activas': 0.0,
        }
    
    def calculate_objective_score(self, metrics: Dict[str, float]) -> float:
        """Calcula score objetivo basado en distancia a métricas objetivo"""
        total_score = 0.0
        total_weight = 0.0
        
        for metric_name, (target, weight) in self.config.target_metrics.items():
            if metric_name in metrics:
                actual = metrics[metric_name]
                
                # Calcular score normalizado para cada métrica
                if metric_name in ['inflacion_promedio', 'desempleo_promedio']:
                    # Para porcentajes, usar error absoluto con tolerancia
                    error = abs(actual - target)
                    tolerance = max(target * 0.5, 0.01)  # Tolerancia del 50% del target o 1%
                    score = max(0, 1 - error / tolerance)
                elif metric_name == 'pib_final':
                    # Para PIB, usar ratio con tolerancia
                    if target > 0 and actual > 0:
                        ratio = min(actual / target, target / actual)  # Ratio simétrico
                        score = ratio  # Score entre 0 y 1
                    elif actual > 0:
                        score = 0.5  # Algo es mejor que nada
                    else:
                        score = 0
                elif metric_name == 'crecimiento_pib':
                    # Para crecimiento, penalizar fuertemente valores negativos extremos
                    if actual >= target:
                        score = 1.0
                    elif actual > -0.5:  # Si no es colapso total
                        # Score lineal entre target y -50%
                        score = max(0, 1 - abs(actual - target) / abs(target + 0.5))
                    else:
                        score = 0  # Colapso económico total
                elif metric_name in ['transacciones_totales', 'empresas_activas']:
                    # Para métricas de actividad económica
                    if target > 0 and actual > 0:
                        ratio = min(actual / target, target / actual)
                        score = ratio
                    elif actual > 0:
                        score = 0.3  # Actividad mínima
                    else:
                        score = 0
                else:
                    # Para otras métricas, usar error relativo
                    if target != 0:
                        error = abs(actual - target) / abs(target)
                        score = max(0, 1 - error)
                    else:
                        score = 1 if actual == 0 else 0
                
                # Aplicar peso
                total_score += score * weight
                total_weight += weight
        
        # Normalizar por peso total
        if total_weight > 0:
            final_score = total_score / total_weight
        else:
            final_score = 0.0
        
        # Bonus por estabilidad básica (evitar colapsos económicos)
        if metrics.get('empresas_activas', 0) > 0 and metrics.get('pib_final', 0) > 0:
            final_score += 0.1  # Bonus del 10% por economía funcionando
        
        return min(1.0, final_score)  # Asegurar que no exceda 1.0
    
    def run_bayesian_optimization(self) -> List[CalibrationResult]:
        """Ejecuta optimización Bayesiana usando Optuna"""
        self.logger.info("Iniciando optimización Bayesiana con Optuna")
        
        def objective(trial):
            # Generar parámetros para este trial
            parameters = {}
            for param_name, (min_val, max_val) in self.config.parameters.items():
                if isinstance(min_val, float) or isinstance(max_val, float):
                    parameters[param_name] = trial.suggest_float(param_name, min_val, max_val)
                else:
                    parameters[param_name] = trial.suggest_int(param_name, int(min_val), int(max_val))
            
            # Ejecutar simulación
            start_time = time.time()
            metrics = self.run_simulation_with_parameters(parameters)
            execution_time = time.time() - start_time
            
            # Calcular score
            score = self.calculate_objective_score(metrics)
            
            # Guardar resultado
            result = CalibrationResult(
                parameters=parameters,
                metrics=metrics,
                score=score,
                execution_time=execution_time,
                trial_number=trial.number
            )
            self.results.append(result)
            
            # Log progreso
            self.logger.info(f"Trial {trial.number}: Score={score:.4f}, PIB={metrics.get('pib_final', 0):.0f}, "
                           f"Inflación={metrics.get('inflacion_promedio', 0):.3f}, "
                           f"Desempleo={metrics.get('desempleo_promedio', 0):.3f}")
            
            return score
        
        # Configurar estudio Optuna
        study = optuna.create_study(
            direction='maximize',
            sampler=TPESampler(seed=42),
            pruner=MedianPruner(n_startup_trials=5, n_warmup_steps=3)
        )
        
        # Ejecutar optimización
        study.optimize(
            objective, 
            n_trials=self.config.n_trials,
            timeout=self.config.timeout_seconds
        )
        
        self.logger.info(f"Optimización Bayesiana completada. Mejor score: {study.best_value:.4f}")
        
        return self.results
    
    def run_grid_search(self) -> List[CalibrationResult]:
        """Ejecuta búsqueda en grid"""
        self.logger.info("Iniciando búsqueda en grid")
        
        # Crear grid de parámetros
        grid_points = {}
        for param_name, (min_val, max_val) in self.config.parameters.items():
            # Crear 5 puntos para cada parámetro
            if isinstance(min_val, float) or isinstance(max_val, float):
                grid_points[param_name] = np.linspace(min_val, max_val, 5)
            else:
                grid_points[param_name] = np.linspace(int(min_val), int(max_val), 5, dtype=int)
        
        # Generar todas las combinaciones
        param_names = list(grid_points.keys())
        param_values = [grid_points[name] for name in param_names]
        
        total_combinations = 1
        for values in param_values:
            total_combinations *= len(values)
        
        self.logger.info(f"Ejecutando {total_combinations} combinaciones de grid search")
        
        trial_num = 0
        for combination in itertools.product(*param_values):
            parameters = dict(zip(param_names, combination))
            
            # Ejecutar simulación
            start_time = time.time()
            metrics = self.run_simulation_with_parameters(parameters)
            execution_time = time.time() - start_time
            
            # Calcular score
            score = self.calculate_objective_score(metrics)
            
            # Guardar resultado
            result = CalibrationResult(
                parameters=parameters,
                metrics=metrics,
                score=score,
                execution_time=execution_time,
                trial_number=trial_num
            )
            self.results.append(result)
            
            # Log progreso
            if trial_num % 10 == 0:
                self.logger.info(f"Grid {trial_num}/{total_combinations}: Score={score:.4f}")
            
            trial_num += 1
            
            # Limitar número de trials si es necesario
            if trial_num >= self.config.n_trials:
                break
        
        return self.results
    
    def run_calibration(self) -> List[CalibrationResult]:
        """Ejecuta el proceso de calibración completo"""
        self.logger.info(f"Iniciando calibración con método: {self.config.optimization_method}")
        
        start_time = time.time()
        
        if self.config.optimization_method == "bayesian":
            results = self.run_bayesian_optimization()
        elif self.config.optimization_method == "grid":
            results = self.run_grid_search()
        else:
            raise ValueError(f"Método de optimización no válido: {self.config.optimization_method}")
        
        total_time = time.time() - start_time
        self.logger.info(f"Calibración completada en {total_time:.2f} segundos")
        
        # Generar reportes
        self.generate_reports()
        
        return results
    
    def generate_reports(self):
        """Genera reportes de resultados de calibración"""
        if not self.results:
            self.logger.warning("No hay resultados para generar reportes")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Convertir resultados a DataFrame
        data = []
        for result in self.results:
            row = {**result.parameters, **result.metrics}
            row['score'] = result.score
            row['execution_time'] = result.execution_time
            row['trial_number'] = result.trial_number
            data.append(row)
        
        df = pd.DataFrame(data)
        
        # Guardar CSV completo
        csv_file = f"{self.config.results_dir}/calibration_results_{timestamp}.csv"
        df.to_csv(csv_file, index=False)
        self.logger.info(f"Resultados completos guardados en: {csv_file}")
        
        # Guardar mejores resultados (top 10)
        best_results = df.nlargest(10, 'score')
        best_csv = f"{self.config.results_dir}/calibration_best_{timestamp}.csv"
        best_results.to_csv(best_csv, index=False)
        self.logger.info(f"Mejores resultados guardados en: {best_csv}")
        
        # Generar resumen JSON
        summary = {
            'calibration_config': asdict(self.config),
            'total_trials': len(self.results),
            'best_score': float(df['score'].max()),
            'best_parameters': df.loc[df['score'].idxmax()].to_dict(),
            'metrics_statistics': {
                col: {
                    'mean': float(df[col].mean()),
                    'std': float(df[col].std()),
                    'min': float(df[col].min()),
                    'max': float(df[col].max())
                }
                for col in df.columns if col not in ['trial_number', 'execution_time']
            },
            'timestamp': timestamp
        }
        
        summary_file = f"{self.config.results_dir}/calibration_summary_{timestamp}.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        self.logger.info(f"Resumen guardado en: {summary_file}")
        
        # Log del mejor resultado
        best_idx = df['score'].idxmax()
        best_result = df.loc[best_idx]
        self.logger.info("🏆 MEJOR RESULTADO:")
        self.logger.info(f"   Score: {best_result['score']:.4f}")
        self.logger.info(f"   PIB Final: ${best_result.get('pib_final', 0):,.0f}")
        self.logger.info(f"   Inflación: {best_result.get('inflacion_promedio', 0):.3f}")
        self.logger.info(f"   Desempleo: {best_result.get('desempleo_promedio', 0):.3f}")


def create_preset_configs():
    """Crea configuraciones preset para diferentes escenarios de calibración"""
    presets_dir = "config/presets"
    os.makedirs(presets_dir, exist_ok=True)
    
    # Preset 1: Calibración económica básica
    basic_config = CalibrationConfig(
        parameters={
            'pib_inicial': (80000, 150000),
            'tasa_inflacion_objetivo': (0.015, 0.035),
            'tasa_desempleo_inicial': (0.08, 0.15),
            'ajuste_maximo_por_ciclo': (0.10, 0.25),
        },
        optimization_method="bayesian",
        n_trials=50,
        simulation_cycles=15,
        target_metrics={
            'pib_final': (100000.0, 1.0),
            'inflacion_promedio': (0.02, 2.0),
            'desempleo_promedio': (0.06, 1.5),
        }
    )
    
    # Preset 2: Análisis de sensibilidad de precios
    pricing_config = CalibrationConfig(
        parameters={
            'ajuste_maximo_por_ciclo': (0.05, 0.30),
            'sensibilidad_competencia': (0.05, 0.25),
            'elasticidad_precio_base': (-2.0, -0.3),
            'elasticidad_ingreso_base': (0.5, 2.0),
        },
        optimization_method="grid",
        n_trials=100,
        simulation_cycles=10,
        target_metrics={
            'inflacion_promedio': (0.02, 3.0),
            'volatilidad_inflacion': (0.01, 1.0),
        }
    )
    
    # Preset 3: Calibración sistema bancario
    banking_config = CalibrationConfig(
        parameters={
            'tasa_interes_base': (0.02, 0.07),
            'ratio_prestamo_ingreso': (3.0, 6.0),
            'probabilidad_contratacion_base': (0.3, 0.7),
        },
        optimization_method="bayesian",
        n_trials=75,
        simulation_cycles=20,
        target_metrics={
            'desempleo_promedio': (0.06, 2.0),
            'transacciones_totales': (200.0, 1.0),
        }
    )
    
    # Guardar presets
    presets = {
        'basic_economic': basic_config,
        'pricing_sensitivity': pricing_config,
        'banking_system': banking_config
    }
    
    for name, config in presets.items():
        preset_file = f"{presets_dir}/{name}.json"
        with open(preset_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(config), f, indent=2, ensure_ascii=False)
        print(f"Preset '{name}' guardado en: {preset_file}")


def main():
    """Función principal ejecutable"""
    parser = argparse.ArgumentParser(description="Pipeline de Calibración Automática")
    
    parser.add_argument('--method', type=str, choices=['bayesian', 'grid'], 
                       default='bayesian', help='Método de optimización')
    parser.add_argument('--trials', type=int, default=50, 
                       help='Número de trials/iteraciones')
    parser.add_argument('--cycles', type=int, default=15, 
                       help='Ciclos de simulación por trial')
    parser.add_argument('--preset', type=str, 
                       help='Usar configuración preset (basic_economic, pricing_sensitivity, banking_system)')
    parser.add_argument('--config', type=str, 
                       help='Archivo de configuración personalizado')
    parser.add_argument('--create-presets', action='store_true',
                       help='Crear archivos de configuración preset')
    parser.add_argument('--timeout', type=float,
                       help='Timeout en segundos para la optimización')
    
    args = parser.parse_args()
    
    # Crear presets si se solicita
    if args.create_presets:
        create_preset_configs()
        return
    
    try:
        # Configurar calibración
        if args.config:
            # Cargar configuración personalizada
            with open(args.config, 'r', encoding='utf-8') as f:
                config_dict = json.load(f)
            config = CalibrationConfig(**config_dict)
        elif args.preset:
            # Cargar preset
            preset_file = f"config/presets/{args.preset}.json"
            if os.path.exists(preset_file):
                with open(preset_file, 'r', encoding='utf-8') as f:
                    config_dict = json.load(f)
                config = CalibrationConfig(**config_dict)
            else:
                print(f"Preset '{args.preset}' no encontrado. Usando configuración por defecto.")
                config = CalibrationConfig()
        else:
            # Configuración por defecto
            config = CalibrationConfig(parameters={})
        
        # Aplicar argumentos CLI
        config.optimization_method = args.method
        config.n_trials = args.trials
        config.simulation_cycles = args.cycles
        if args.timeout:
            config.timeout_seconds = args.timeout
        
        # Ejecutar calibración (el runner se encargará de configurar parámetros por defecto)
        runner = CalibrationRunner(config)
        results = runner.run_calibration()
        
        print(f"\n🎯 Calibración completada exitosamente!")
        print(f"📊 Total de trials: {len(results)}")
        print(f"🏆 Mejor score: {max(r.score for r in results):.4f}")
        print(f"📁 Resultados en: {config.results_dir}")
        
    except Exception as e:
        print(f"❌ Error en calibración: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()