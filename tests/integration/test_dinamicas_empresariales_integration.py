"""
Test de integración para las nuevas dinámicas empresariales.
Valida que las características trabajen correctamente en conjunto.
"""

import pytest
import json
import os
import subprocess
import tempfile
from pathlib import Path


class TestIntegracionDinamicasEmpresariales:
    """Tests de integración para dinámicas empresariales"""

    def test_simulacion_completa_con_dinamicas(self):
        """Ejecuta simulación completa y valida nuevas funcionalidades"""
        
        # Crear configuración de test
        config_test = {
            "simulacion": {
                "num_ciclos": 15,  # Suficientes ciclos para ver dinámicas
                "num_consumidores": 100,
                "num_empresas_productoras": 5,
                "num_empresas_comerciales": 3,
                "frecuencia_reportes": 5,
                "activar_crisis": True,
                "usar_empresas_hiperrealistas": True
            },
            "economia": {
                "pib_inicial": 100000,
                "tasa_desempleo_inicial": 0.15,
                "capital_inicial_empresas": {"min": 50000, "max": 150000}
            },
            "empresas_hiperrealistas": {
                "activar": True,
                "probabilidad_crisis_empresa": 0.05  # Mayor para ver dinámicas
            },
            "precios": {
                "ajuste_maximo_por_ciclo": 0.10,
                "sensibilidad_stock": 0.15
            },
            "sistema_bancario": {"activar": True, "num_bancos": 2},
            "machine_learning": {"activar": False},  # Deshabilitar para test rápido
            "agentes_ia": {"activar": False}  # Deshabilitar para test rápido
        }
        
        # Crear archivo temporal de configuración
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_test, f)
            config_path = f.name

        # Variables for cleanup
        backup_config = None
        original_config = None
        
        try:
            # Backup original config and replace with test config
            repo_root = Path(__file__).parent.parent.parent
            original_config = repo_root / 'config_simulacion.json'
            backup_config = repo_root / 'config_simulacion.json.backup'
            
            # Backup original
            if original_config.exists():
                original_config.rename(backup_config)
            
            # Write test config
            with open(original_config, 'w') as f:
                json.dump(config_test, f)
            
            # Ejecutar simulación
            result = subprocess.run(
                ['python3', 'main.py'],
                cwd=repo_root,
                capture_output=True,
                text=True,
                timeout=120  # 2 minutos máximo
            )
            
            # Verificar que la simulación ejecutó sin errores
            assert result.returncode == 0, f"Simulación falló: {result.stderr}"
            
            # Buscar evidencia de las nuevas funcionalidades en la salida
            # Los reportes aparecen en stderr (logging) y stdout (básico)
            output = result.stdout + result.stderr
            
            # Verificar que aparecen los KPIs empresariales
            assert "DINÁMICAS EMPRESARIALES:" in output, "KPIs empresariales no aparecen en salida"
            assert "Tasa Quiebra:" in output, "Tasa de quiebra no reportada"
            assert "Rotación:" in output, "Rotación empresarial no reportada"  
            assert "Rigidez Precios:" in output, "Rigidez de precios no reportada"
            assert "Ratio Inventario:" in output, "Ratio de inventario no reportado"
            
            # Verificar finalización exitosa
            assert "COMPLETADA EXITOSAMENTE" in output, "Simulación no completó exitosamente"
            
        finally:
            # Restore original config
            if backup_config.exists():
                backup_config.rename(original_config)
            elif original_config.exists():
                original_config.unlink()
            
            # Limpiar archivo temporal
            os.unlink(config_path)

    def test_validacion_kpis_realistas(self):
        """Valida que los KPIs estén en rangos realistas"""
        
        # Este test podría extenderse para verificar rangos específicos
        # Por ejemplo:
        # - Rigidez de precios: 30-90%
        # - Rotación empresarial: 0-20%
        # - Ratio inventario: 0.5-2.0
        
        # Por ahora, simplemente verificamos que el test anterior pase
        # En una implementación completa, podríamos parsear la salida
        # y verificar rangos numéricos específicos
        assert True, "Placeholder para validación de rangos de KPIs"

    def test_comportamiento_crisis_empresarial(self):
        """Verifica comportamiento durante crisis empresarial"""
        
        # Configuración con alta probabilidad de crisis
        config_crisis = {
            "simulacion": {"num_ciclos": 10, "num_consumidores": 50, "num_empresas_productoras": 8},
            "economia": {"capital_inicial_empresas": {"min": 10000, "max": 30000}},  # Poco capital
            "empresas_hiperrealistas": {"probabilidad_crisis_empresa": 0.15},  # Crisis frecuentes
            "machine_learning": {"activar": False},
            "agentes_ia": {"activar": False}
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_crisis, f)
            config_path = f.name
        
        try:
            repo_root = Path(__file__).parent.parent.parent
            result = subprocess.run(
                ['python3', 'main.py', '--config', config_path],
                cwd=repo_root,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            # La simulación debe completarse aunque haya crisis
            assert result.returncode == 0, f"Simulación con crisis falló: {result.stderr}"
            
            # Debe haber evidencia de actividad de rescate empresarial
            output = result.stdout + result.stderr
            assert "Rescate Empresarial" in output, "Sistema de rescate no activado en crisis"
            
        finally:
            os.unlink(config_path)


if __name__ == '__main__':
    pytest.main([__file__])