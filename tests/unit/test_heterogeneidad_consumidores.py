"""
Tests unitarios para heterogeneidad de consumidores y restricción presupuestaria
"""

import unittest
import numpy as np
import sys
import os

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.models.Consumidor import Consumidor
from src.models.Mercado import Mercado
from src.models.Bien import Bien
from src.config.ConfigEconomica import ConfigEconomica


class TestHeterogeneidadConsumidores(unittest.TestCase):
    """Tests para la heterogeneidad de consumidores"""
    
    def setUp(self):
        """Configuración inicial para las pruebas"""
        # Crear mercado con bienes de prueba
        bienes = {
            'Arroz': Bien('Arroz', 'alimentos_basicos'),
            'Carne': Bien('Carne', 'alimentos_lujo'),
            'Entretenimiento': Bien('Entretenimiento', 'servicios_lujo')
        }
        self.mercado = Mercado(bienes)
        
        # Configuración de heterogeneidad para pruebas
        self.config_hetero = {
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
    
    def test_distribucion_lognormal_ingresos(self):
        """Test que la distribución lognormal genera ingresos heterogéneos"""
        consumidores = []
        for i in range(100):
            consumidor = Consumidor(f'Test_{i}', self.mercado, config_hetero=self.config_hetero)
            consumidores.append(consumidor)
        
        ingresos = [c.dinero for c in consumidores]
        ingresos_mensuales = [c.ingreso_mensual for c in consumidores if c.empleado]
        
        # Verificar que hay variabilidad en los ingresos
        self.assertGreater(np.std(ingresos), 1000, "Debe haber heterogeneidad en ingresos")
        
        # Verificar que se respeta el mínimo garantizado
        self.assertTrue(all(ing >= self.config_hetero['ingreso_min_garantizado'] for ing in ingresos))
        
        # Verificar que los ingresos mensuales también son heterogéneos
        if ingresos_mensuales:
            self.assertGreater(np.std(ingresos_mensuales), 500, "Debe haber heterogeneidad en ingresos mensuales")
    
    def test_preferencias_cobb_douglas(self):
        """Test que las preferencias Cobb-Douglas se inicializan correctamente"""
        consumidor = Consumidor('Test', self.mercado, config_hetero=self.config_hetero)
        
        # Verificar que se inicializaron las preferencias
        self.assertIsInstance(consumidor.preferencias_cobb_douglas, dict)
        self.assertEqual(len(consumidor.preferencias_cobb_douglas), 3)  # 3 bienes
        
        # Verificar que suman aproximadamente 1
        suma_preferencias = sum(consumidor.preferencias_cobb_douglas.values())
        self.assertAlmostEqual(suma_preferencias, 1.0, places=5)
        
        # Verificar que todas las preferencias son positivas
        self.assertTrue(all(pref > 0 for pref in consumidor.preferencias_cobb_douglas.values()))
    
    def test_utilidad_cobb_douglas(self):
        """Test del cálculo de utilidad Cobb-Douglas"""
        consumidor = Consumidor('Test', self.mercado, config_hetero=self.config_hetero)
        
        # Cantidades de prueba
        cantidades = {'Arroz': 5, 'Carne': 2, 'Entretenimiento': 1}
        
        # Calcular utilidad
        utilidad = consumidor.calcular_utilidad_cobb_douglas(cantidades)
        
        # Verificar que la utilidad es positiva
        self.assertGreater(utilidad, 0)
        
        # Verificar que cantidades mayores dan mayor utilidad
        cantidades_mayores = {'Arroz': 10, 'Carne': 4, 'Entretenimiento': 2}
        utilidad_mayor = consumidor.calcular_utilidad_cobb_douglas(cantidades_mayores)
        self.assertGreater(utilidad_mayor, utilidad)
    
    def test_demanda_cobb_douglas(self):
        """Test del cálculo de demanda óptima Cobb-Douglas"""
        self.config_hetero['tipo_preferencias'] = 'cobb_douglas'
        consumidor = Consumidor('Test', self.mercado, config_hetero=self.config_hetero)
        
        # Precios y presupuesto de prueba
        precios = {'Arroz': 10, 'Carne': 30, 'Entretenimiento': 50}
        presupuesto = 1000
        
        # Calcular demanda óptima
        demanda = consumidor.calcular_demanda_optima(presupuesto, precios)
        
        # Verificar que todas las demandas son no negativas
        self.assertTrue(all(d >= 0 for d in demanda.values()))
        
        # Verificar que el gasto total no excede el presupuesto (con tolerancia)
        gasto_total = sum(demanda[bien] * precios[bien] for bien in precios)
        self.assertLessEqual(gasto_total, presupuesto * 1.01)  # 1% tolerancia
    
    def test_utilidad_ces(self):
        """Test del cálculo de utilidad CES"""
        self.config_hetero['tipo_preferencias'] = 'ces'
        consumidor = Consumidor('Test', self.mercado, config_hetero=self.config_hetero)
        
        # Cantidades de prueba
        cantidades = {'Arroz': 5, 'Carne': 2, 'Entretenimiento': 1}
        
        # Calcular utilidad CES
        utilidad = consumidor.calcular_utilidad_ces(cantidades)
        
        # Verificar que la utilidad es positiva
        self.assertGreater(utilidad, 0)
        
        # Verificar que cantidades mayores dan mayor utilidad
        cantidades_mayores = {'Arroz': 10, 'Carne': 4, 'Entretenimiento': 2}
        utilidad_mayor = consumidor.calcular_utilidad_ces(cantidades_mayores)
        self.assertGreater(utilidad_mayor, utilidad)
    
    def test_restriccion_intertemporal(self):
        """Test de la restricción intertemporal"""
        consumidor = Consumidor('Test', self.mercado, config_hetero=self.config_hetero)
        
        # Probar con diferentes tasas de interés
        tasa_baja = 0.02
        tasa_alta = 0.10
        
        propension_tasa_baja = consumidor.aplicar_restriccion_intertemporal(1000, tasa_baja)
        propension_tasa_alta = consumidor.aplicar_restriccion_intertemporal(1000, tasa_alta)
        
        # Verificar que las propensiones están en rango válido
        self.assertGreaterEqual(propension_tasa_baja, 0.1)
        self.assertLessEqual(propension_tasa_baja, 0.95)
        self.assertGreaterEqual(propension_tasa_alta, 0.1)
        self.assertLessEqual(propension_tasa_alta, 0.95)
        
        # Los consumidores más pacientes deberían consumir menos con tasas altas
        if consumidor.factor_paciencia > 0.8:
            self.assertLessEqual(propension_tasa_alta, propension_tasa_baja)
    
    def test_factor_paciencia_rango(self):
        """Test que el factor de paciencia está en el rango configurado"""
        consumidores = []
        for i in range(50):
            consumidor = Consumidor(f'Test_{i}', self.mercado, config_hetero=self.config_hetero)
            consumidores.append(consumidor)
        
        factores_paciencia = [c.factor_paciencia for c in consumidores]
        
        # Verificar rango
        min_paciencia = min(factores_paciencia)
        max_paciencia = max(factores_paciencia)
        
        self.assertGreaterEqual(min_paciencia, self.config_hetero['factor_paciencia_min'])
        self.assertLessEqual(max_paciencia, self.config_hetero['factor_paciencia_max'])
        
        # Verificar heterogeneidad
        self.assertGreater(np.std(factores_paciencia), 0.05)


class TestValidadorGini(unittest.TestCase):
    """Tests para el cálculo del índice de Gini"""
    
    def test_calculo_gini_distribucion_igual(self):
        """Test Gini con distribución perfectamente igual"""
        from src.systems.ValidadorEconomico import ValidadorEconomico
        
        validador = ValidadorEconomico()
        ingresos_iguales = [1000, 1000, 1000, 1000, 1000]
        
        gini = validador._calcular_gini(ingresos_iguales)
        
        # Con distribución perfectamente igual, Gini debería ser 0
        self.assertAlmostEqual(gini, 0.0, places=3)
    
    def test_calculo_gini_distribucion_desigual(self):
        """Test Gini con distribución desigual"""
        from src.systems.ValidadorEconomico import ValidadorEconomico
        
        validador = ValidadorEconomico()
        ingresos_desiguales = [100, 200, 500, 1000, 5000]
        
        gini = validador._calcular_gini(ingresos_desiguales)
        
        # Con distribución desigual, Gini debería ser mayor a 0
        self.assertGreater(gini, 0.0)
        self.assertLess(gini, 1.0)
    
    def test_gini_rango_objetivo(self):
        """Test que el Gini generado está en el rango objetivo configurado"""
        # Crear muchos consumidores para obtener una distribución representativa
        bienes = {'Arroz': Bien('Arroz', 'alimentos_basicos')}
        mercado = Mercado(bienes)
        
        config_hetero = {
            'activar': True,
            'distribucion_ingresos': 'lognormal',
            'ingreso_lognormal_mu': 8.5,
            'ingreso_lognormal_sigma': 0.8,
            'ingreso_min_garantizado': 1500,
            'gini_objetivo': 0.45
        }
        
        consumidores = []
        for i in range(500):  # Muestra grande para estadística
            consumidor = Consumidor(f'Test_{i}', mercado, config_hetero=config_hetero)
            consumidores.append(consumidor)
        
        ingresos = [c.dinero for c in consumidores]
        
        from src.systems.ValidadorEconomico import ValidadorEconomico
        validador = ValidadorEconomico()
        gini_calculado = validador._calcular_gini(ingresos)
        
        # Verificar que el Gini está en un rango razonable
        # (puede no ser exactamente 0.45 debido a la aleatoriedad)
        self.assertGreater(gini_calculado, ConfigEconomica.GINI_OBJETIVO_MIN)
        self.assertLess(gini_calculado, ConfigEconomica.GINI_OBJETIVO_MAX)


if __name__ == '__main__':
    unittest.main()