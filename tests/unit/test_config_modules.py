"""
Tests para Módulos de Configuración
===================================

Tests unitarios para los módulos de configuración:
- ConfigEconomica
- ConfiguradorSimulacion
- DatosEconomicosReales
"""

import unittest
import sys
import os
import json

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.config.ConfigEconomica import ConfigEconomica
from src.config.ConfiguradorSimulacion import ConfiguradorSimulacion
from src.config.DatosEconomicosReales import IndicadoresEconomicosReales


class TestConfigEconomica(unittest.TestCase):
    """Tests para ConfigEconomica"""
    
    def test_constantes_definidas(self):
        """Test que las constantes económicas están definidas"""
        # Dinero inicial consumidores
        self.assertIsInstance(ConfigEconomica.DINERO_INICIAL_CONSUMIDOR_MIN, int)
        self.assertIsInstance(ConfigEconomica.DINERO_INICIAL_CONSUMIDOR_MAX, int)
        self.assertLess(ConfigEconomica.DINERO_INICIAL_CONSUMIDOR_MIN, 
                       ConfigEconomica.DINERO_INICIAL_CONSUMIDOR_MAX)
        
        # Dinero inicial empresas
        self.assertIsInstance(ConfigEconomica.DINERO_INICIAL_EMPRESA_MIN, int)
        self.assertIsInstance(ConfigEconomica.DINERO_INICIAL_EMPRESA_MAX, int)
        self.assertLess(ConfigEconomica.DINERO_INICIAL_EMPRESA_MIN,
                       ConfigEconomica.DINERO_INICIAL_EMPRESA_MAX)
        
        # Salarios
        self.assertIsInstance(ConfigEconomica.SALARIO_BASE_MIN, int)
        self.assertIsInstance(ConfigEconomica.SALARIO_BASE_MAX, int)
        self.assertLess(ConfigEconomica.SALARIO_BASE_MIN, ConfigEconomica.SALARIO_BASE_MAX)
    
    def test_rangos_logicos(self):
        """Test que los rangos de valores son lógicos"""
        # Los consumidores deben tener menos dinero inicial que las empresas
        self.assertLess(ConfigEconomica.DINERO_INICIAL_CONSUMIDOR_MAX,
                       ConfigEconomica.DINERO_INICIAL_EMPRESA_MIN)
        
        # Los valores deben ser positivos
        self.assertGreater(ConfigEconomica.DINERO_INICIAL_CONSUMIDOR_MIN, 0)
        self.assertGreater(ConfigEconomica.DINERO_INICIAL_EMPRESA_MIN, 0)
        self.assertGreater(ConfigEconomica.SALARIO_BASE_MIN, 0)
    
    def test_constantes_presupuesto_gobierno(self):
        """Test constantes del presupuesto gubernamental"""
        self.assertIsInstance(ConfigEconomica.PRESUPUESTO_GOBIERNO_BASE, int)
        self.assertGreater(ConfigEconomica.PRESUPUESTO_GOBIERNO_BASE, 0)
        
        # El presupuesto debe ser significativamente mayor que el dinero individual
        self.assertGreater(ConfigEconomica.PRESUPUESTO_GOBIERNO_BASE,
                          ConfigEconomica.DINERO_INICIAL_EMPRESA_MAX * 10)
    
    def test_tasas_economicas(self):
        """Test tasas económicas básicas"""
        if hasattr(ConfigEconomica, 'TASA_INFLACION_BASE'):
            self.assertIsInstance(ConfigEconomica.TASA_INFLACION_BASE, float)
            self.assertGreaterEqual(ConfigEconomica.TASA_INFLACION_BASE, 0.0)
            self.assertLessEqual(ConfigEconomica.TASA_INFLACION_BASE, 0.1)  # Max 10%
        
        if hasattr(ConfigEconomica, 'TASA_DESEMPLEO_INICIAL'):
            self.assertIsInstance(ConfigEconomica.TASA_DESEMPLEO_INICIAL, float)
            self.assertGreaterEqual(ConfigEconomica.TASA_DESEMPLEO_INICIAL, 0.0)
            self.assertLessEqual(ConfigEconomica.TASA_DESEMPLEO_INICIAL, 0.3)  # Max 30%


class TestConfiguradorSimulacion(unittest.TestCase):
    """Tests para ConfiguradorSimulacion"""
    
    def setUp(self):
        self.configurador = ConfiguradorSimulacion()
    
    def test_creacion_configurador(self):
        """Test creación del configurador"""
        self.assertIsInstance(self.configurador.config, dict)
    
    def test_cargar_configuracion_archivo(self):
        """Test carga de configuración desde archivo"""
        # Crear archivo de configuración temporal
        config_temp = {
            "simulacion": {
                "num_ciclos": 50,
                "num_consumidores": 100
            },
            "economia": {
                "pib_inicial": 200000,
                "tasa_inflacion": 0.025
            }
        }
        
        # Escribir archivo temporal
        with open("/tmp/test_config.json", "w") as f:
            json.dump(config_temp, f)
        
        # Cargar configuración
        resultado = self.configurador.cargar_desde_archivo("/tmp/test_config.json")
        
        self.assertTrue(resultado)
        self.assertEqual(self.configurador.config["simulacion"]["num_ciclos"], 50)
        self.assertEqual(self.configurador.config["economia"]["pib_inicial"], 200000)
        
        # Limpiar archivo temporal
        os.remove("/tmp/test_config.json")
    
    def test_obtener_seccion_existente(self):
        """Test obtención de sección existente"""
        # Configurar datos de prueba
        self.configurador.config = {
            "simulacion": {
                "num_ciclos": 30,
                "activar_crisis": False
            }
        }
        
        seccion = self.configurador.obtener_seccion("simulacion")
        
        self.assertIsInstance(seccion, dict)
        self.assertEqual(seccion["num_ciclos"], 30)
        self.assertFalse(seccion["activar_crisis"])
    
    def test_obtener_seccion_inexistente(self):
        """Test obtención de sección inexistente"""
        seccion = self.configurador.obtener_seccion("no_existe")
        
        self.assertIsInstance(seccion, dict)
        self.assertEqual(len(seccion), 0)
    
    def test_obtener_parametro_existente(self):
        """Test obtención de parámetro específico"""
        self.configurador.config = {
            "economia": {
                "tasa_inflacion": 0.02,
                "pib_inicial": 150000
            }
        }
        
        tasa = self.configurador.obtener_parametro("economia", "tasa_inflacion")
        self.assertEqual(tasa, 0.02)
        
        pib = self.configurador.obtener_parametro("economia", "pib_inicial")
        self.assertEqual(pib, 150000)
    
    def test_obtener_parametro_con_default(self):
        """Test obtención de parámetro con valor por defecto"""
        valor = self.configurador.obtener_parametro("no_existe", "param", default=42)
        self.assertEqual(valor, 42)
        
        valor = self.configurador.obtener_parametro("economia", "param_inexistente", default="test")
        self.assertEqual(valor, "test")
    
    def test_validar_configuracion_basica(self):
        """Test validación básica de configuración"""
        # Configuración válida
        config_valida = {
            "simulacion": {
                "num_ciclos": 30,
                "num_consumidores": 100,
                "num_empresas": 10
            },
            "economia": {
                "pib_inicial": 100000,
                "tasa_inflacion": 0.025
            }
        }
        
        self.configurador.config = config_valida
        
        # El configurador debe validar sin errores
        # (Si existe método de validación)
        if hasattr(self.configurador, 'validar'):
            resultado = self.configurador.validar()
            self.assertTrue(resultado)
    
    def test_configuracion_por_defecto(self):
        """Test que existe configuración por defecto"""
        # Si no se carga ningún archivo, debe haber configuración básica
        if len(self.configurador.config) > 0:
            self.assertIsInstance(self.configurador.config, dict)
        
        # Debe poder obtener secciones básicas sin error
        sim_config = self.configurador.obtener_seccion("simulacion")
        self.assertIsInstance(sim_config, dict)


class TestIndicadoresEconomicosReales(unittest.TestCase):
    """Tests para IndicadoresEconomicosReales"""
    
    def test_datos_pib_mundial(self):
        """Test datos de PIB mundial"""
        pib_data = IndicadoresEconomicosReales.PIB_CRECIMIENTO_ANUAL
        self.assertIsInstance(pib_data, dict)
        
        # Verificar categorías básicas
        self.assertIn('desarrolladas', pib_data)
        self.assertIn('emergentes', pib_data)
        
        # Verificar rangos
        desarrolladas = pib_data['desarrolladas']
        self.assertIsInstance(desarrolladas, tuple)
        self.assertEqual(len(desarrolladas), 2)
        self.assertLess(desarrolladas[0], desarrolladas[1])
    
    def test_datos_inflacion_paises(self):
        """Test datos de inflación por países"""
        inflacion_data = IndicadoresEconomicosReales.INFLACION
        self.assertIsInstance(inflacion_data, dict)
        
        # Verificar objetivo central
        self.assertIn('objetivo_central', inflacion_data)
        objetivo = inflacion_data['objetivo_central']
        self.assertIsInstance(objetivo, float)
        self.assertGreaterEqual(objetivo, 0.0)
        self.assertLessEqual(objetivo, 0.05)  # Máximo 5%
        
        # Verificar rango normal
        self.assertIn('rango_normal', inflacion_data)
        rango = inflacion_data['rango_normal']
        self.assertIsInstance(rango, tuple)
        self.assertLess(rango[0], rango[1])
    
    def test_datos_desempleo(self):
        """Test datos de desempleo"""
        desempleo_data = IndicadoresEconomicosReales.DESEMPLEO
        self.assertIsInstance(desempleo_data, dict)
        
        # Verificar desempleo estructural
        if 'estructural' in desempleo_data:
            estructural = desempleo_data['estructural']
            self.assertIsInstance(estructural, tuple)
            self.assertGreaterEqual(estructural[0], 0.0)
            self.assertLessEqual(estructural[1], 0.15)  # Max 15%
    
    def test_rangos_coherentes(self):
        """Test que los rangos de datos son coherentes"""
        # PIB: emergentes deberían crecer más que desarrolladas
        pib = IndicadoresEconomicosReales.PIB_CRECIMIENTO_ANUAL
        if 'desarrolladas' in pib and 'emergentes' in pib:
            desarrolladas_max = pib['desarrolladas'][1]
            emergentes_min = pib['emergentes'][0]
            # Puede haber overlap, pero emergentes debería tener potencial mayor
            self.assertGreaterEqual(pib['emergentes'][1], pib['desarrolladas'][1])
        
        # Inflación: objetivo debe estar en rango normal
        inflacion = IndicadoresEconomicosReales.INFLACION
        if 'objetivo_central' in inflacion and 'rango_normal' in inflacion:
            objetivo = inflacion['objetivo_central']
            rango = inflacion['rango_normal']
            self.assertGreaterEqual(objetivo, rango[0])
            self.assertLessEqual(objetivo, rango[1])
    
    def test_datos_tipos_cambio(self):
        """Test datos de tipos de cambio si existen"""
        if hasattr(IndicadoresEconomicosReales, 'TIPOS_CAMBIO'):
            cambio_data = IndicadoresEconomicosReales.TIPOS_CAMBIO
            self.assertIsInstance(cambio_data, dict)
            
            # Verificar que las tasas son positivas
            for moneda, tasa in cambio_data.items():
                self.assertIsInstance(tasa, (int, float))
                self.assertGreater(tasa, 0)
    
    def test_datos_tasas_interes(self):
        """Test datos de tasas de interés si existen"""
        if hasattr(IndicadoresEconomicosReales, 'TASAS_INTERES'):
            tasas_data = IndicadoresEconomicosReales.TASAS_INTERES
            self.assertIsInstance(tasas_data, dict)
            
            # Verificar rangos razonables
            for banco, tasa in tasas_data.items():
                self.assertIsInstance(tasa, float)
                self.assertGreaterEqual(tasa, 0.0)
                self.assertLessEqual(tasa, 0.25)  # Max 25%


class TestConfiguracionIntegracion(unittest.TestCase):
    """Tests de integración para los módulos de configuración"""
    
    def test_configuracion_completa_simulacion(self):
        """Test configuración completa de una simulación"""
        configurador = ConfiguradorSimulacion()
        
        # Configurar parámetros para una simulación de prueba
        config_simulacion = {
            "simulacion": {
                "num_ciclos": ConfigEconomica.DINERO_INICIAL_CONSUMIDOR_MIN // 1000,  # Usar constantes
                "num_consumidores": 50,
                "num_empresas": 5
            },
            "economia": {
                "pib_inicial": ConfigEconomica.PRESUPUESTO_GOBIERNO_BASE // 10,
                "salario_base": ConfigEconomica.SALARIO_BASE_MIN
            }
        }
        
        configurador.config = config_simulacion
        
        # Verificar que la configuración es coherente
        sim_config = configurador.obtener_seccion("simulacion")
        eco_config = configurador.obtener_seccion("economia")
        
        self.assertIsInstance(sim_config, dict)
        self.assertIsInstance(eco_config, dict)
        self.assertGreater(sim_config["num_ciclos"], 0)
        self.assertGreater(eco_config["pib_inicial"], 0)
    
    def test_datos_reales_configuracion(self):
        """Test uso de datos reales en configuración"""
        configurador = ConfiguradorSimulacion()
        
        # Usar datos reales para configurar la simulación
        inflacion_objetivo = IndicadoresEconomicosReales.INFLACION['objetivo_central']
        
        config_realista = {
            "economia": {
                "tasa_inflacion_objetivo": inflacion_objetivo,
                "pib_inicial": 100000
            }
        }
        
        configurador.config = config_realista
        tasa = configurador.obtener_parametro("economia", "tasa_inflacion_objetivo")
        
        self.assertIsInstance(tasa, float)
        self.assertGreaterEqual(tasa, -0.05)
        self.assertLessEqual(tasa, 0.20)


if __name__ == '__main__':
    unittest.main()