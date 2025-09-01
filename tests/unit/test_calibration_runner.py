"""
Tests para el pipeline de calibración automática
"""

import unittest
import os
import json
import tempfile
import shutil
from pathlib import Path
import sys

# Agregar src al path
current_dir = Path(__file__).parent
root_dir = current_dir.parent.parent
sys.path.append(str(root_dir))

from src.utils.calibration_runner import (
    CalibrationRunner, 
    CalibrationConfig, 
    CalibrationResult
)


class TestCalibrationRunner(unittest.TestCase):
    """Tests para la clase CalibrationRunner"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        # Crear directorio temporal para resultados
        self.temp_dir = tempfile.mkdtemp()
        
        # Configuración básica para tests
        self.config = CalibrationConfig(
            parameters={
                'pib_inicial': (80000, 120000),
                'tasa_inflacion_objetivo': (0.015, 0.025),
                'tasa_desempleo_inicial': (0.08, 0.12),
            },
            optimization_method="bayesian",
            n_trials=2,  # Mínimo para tests rápidos
            simulation_cycles=3,  # Ciclos mínimos para tests
            results_dir=self.temp_dir,
            target_metrics={
                'pib_final': (100000.0, 1.0),
                'inflacion_promedio': (0.02, 1.0),
                'desempleo_promedio': (0.06, 1.0),
            }
        )
    
    def tearDown(self):
        """Limpieza después de cada test"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_calibration_config_creation(self):
        """Test creación de configuración de calibración"""
        self.assertIsNotNone(self.config)
        self.assertEqual(self.config.optimization_method, "bayesian")
        self.assertEqual(self.config.n_trials, 2)
        self.assertEqual(self.config.simulation_cycles, 3)
        self.assertIn('pib_inicial', self.config.parameters)
    
    def test_calibration_runner_initialization(self):
        """Test inicialización del runner de calibración"""
        runner = CalibrationRunner(self.config)
        
        self.assertIsNotNone(runner.calibrador_economico)
        self.assertIsNotNone(runner.indicadores_reales)
        self.assertEqual(runner.results, [])
        self.assertIsNotNone(runner.base_config)
        self.assertIn('simulacion', runner.base_config)
    
    def test_default_parameter_space(self):
        """Test generación del espacio de parámetros por defecto"""
        runner = CalibrationRunner(self.config)
        param_space = runner.get_default_parameter_space()
        
        self.assertIn('pib_inicial', param_space)
        self.assertIn('tasa_inflacion_objetivo', param_space)
        self.assertIn('ajuste_maximo_por_ciclo', param_space)
        
        # Verificar que los rangos son tuplas de 2 elementos
        for param, (min_val, max_val) in param_space.items():
            self.assertLess(min_val, max_val)
            self.assertIsInstance(min_val, (int, float))
            self.assertIsInstance(max_val, (int, float))
    
    def test_apply_parameters_to_config(self):
        """Test aplicación de parámetros a configuración"""
        runner = CalibrationRunner(self.config)
        
        test_params = {
            'pib_inicial': 90000,
            'tasa_inflacion_objetivo': 0.02,
            'tasa_desempleo_inicial': 0.10,
            'ajuste_maximo_por_ciclo': 0.15,
        }
        
        modified_config = runner.apply_parameters_to_config(test_params, runner.base_config)
        
        self.assertEqual(modified_config['economia']['pib_inicial'], 90000)
        self.assertEqual(modified_config['economia']['tasa_inflacion_objetivo'], 0.02)
        self.assertEqual(modified_config['economia']['tasa_desempleo_inicial'], 0.10)
        self.assertEqual(modified_config['precios']['ajuste_maximo_por_ciclo'], 0.15)
        self.assertEqual(modified_config['simulacion']['num_ciclos'], 3)  # Desde config
    
    def test_calculate_objective_score(self):
        """Test cálculo de score objetivo"""
        runner = CalibrationRunner(self.config)
        
        # Métricas perfectas (coinciden con targets)
        perfect_metrics = {
            'pib_final': 100000.0,
            'inflacion_promedio': 0.02,
            'desempleo_promedio': 0.06,
        }
        
        score = runner.calculate_objective_score(perfect_metrics)
        self.assertGreaterEqual(score, 0.8)  # Score alto para métricas perfectas
        
        # Métricas de falla económica
        failure_metrics = {
            'pib_final': 0.0,
            'inflacion_promedio': 1.0,  # Hiperinflación
            'desempleo_promedio': 1.0,  # Desempleo total
        }
        
        score = runner.calculate_objective_score(failure_metrics)
        self.assertEqual(score, 0.0)  # Score mínimo para falla total
    
    def test_default_failure_metrics(self):
        """Test métricas de falla por defecto"""
        runner = CalibrationRunner(self.config)
        failure_metrics = runner.get_default_failure_metrics()
        
        self.assertEqual(failure_metrics['pib_final'], 0.0)
        self.assertEqual(failure_metrics['crecimiento_pib'], -1.0)
        self.assertEqual(failure_metrics['inflacion_promedio'], 1.0)
        self.assertEqual(failure_metrics['desempleo_promedio'], 1.0)
    
    def test_mock_simulation_execution(self):
        """Test ejecución simulada (sin simulación real por velocidad)"""
        runner = CalibrationRunner(self.config)
        
        # Simular parámetros válidos
        test_params = {
            'pib_inicial': 95000,
            'tasa_inflacion_objetivo': 0.02,
        }
        
        # En lugar de ejecutar simulación real, testear la estructura
        config_modified = runner.apply_parameters_to_config(test_params, runner.base_config)
        self.assertIsNotNone(config_modified)
        self.assertEqual(config_modified['economia']['pib_inicial'], 95000)


class TestCalibrationPresets(unittest.TestCase):
    """Tests para configuraciones preset"""
    
    def test_preset_files_exist(self):
        """Test que los archivos preset existen"""
        presets_dir = root_dir / "config" / "presets"
        
        expected_presets = [
            'basic_economic.json',
            'pricing_sensitivity.json',
            'banking_system.json'
        ]
        
        for preset_file in expected_presets:
            preset_path = presets_dir / preset_file
            self.assertTrue(preset_path.exists(), f"Preset {preset_file} no existe")
    
    def test_preset_content_validity(self):
        """Test que el contenido de los presets es válido"""
        presets_dir = root_dir / "config" / "presets"
        
        for preset_file in presets_dir.glob("*.json"):
            with open(preset_file, 'r', encoding='utf-8') as f:
                preset_data = json.load(f)
            
            # Verificar estructura básica
            self.assertIn('parameters', preset_data)
            self.assertIn('optimization_method', preset_data)
            self.assertIn('n_trials', preset_data)
            self.assertIn('target_metrics', preset_data)
            
            # Verificar que los parámetros tienen rangos válidos
            for param_name, param_range in preset_data['parameters'].items():
                self.assertEqual(len(param_range), 2)
                self.assertLess(param_range[0], param_range[1])


class TestCalibrationResult(unittest.TestCase):
    """Tests para la clase CalibrationResult"""
    
    def test_calibration_result_creation(self):
        """Test creación de resultado de calibración"""
        parameters = {'pib_inicial': 100000, 'tasa_inflacion_objetivo': 0.02}
        metrics = {'pib_final': 95000, 'inflacion_promedio': 0.025}
        
        result = CalibrationResult(
            parameters=parameters,
            metrics=metrics,
            score=0.85,
            execution_time=30.5,
            trial_number=1
        )
        
        self.assertEqual(result.parameters, parameters)
        self.assertEqual(result.metrics, metrics)
        self.assertEqual(result.score, 0.85)
        self.assertEqual(result.execution_time, 30.5)
        self.assertEqual(result.trial_number, 1)
        self.assertTrue(result.success)
        self.assertIsNone(result.error_message)


if __name__ == '__main__':
    unittest.main()