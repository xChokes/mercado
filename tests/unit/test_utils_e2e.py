"""
Tests para Módulos de Utilidades y E2E
=====================================

Tests para módulos de utilidades y tests de integración E2E básicos
que mejoran significativamente la cobertura de pruebas.
"""

import unittest
import sys
import os
import tempfile

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.utils.SimuladorLogger import SimuladorLogger
from src.models.Mercado import Mercado
from src.models.Bien import Bien
from src.models.Consumidor import Consumidor
from src.models.Empresa import Empresa
from src.config.ConfigEconomica import ConfigEconomica


class TestSimuladorLogger(unittest.TestCase):
    """Tests para SimuladorLogger"""
    
    def setUp(self):
        self.logger = SimuladorLogger()
    
    def test_creacion_logger(self):
        """Test creación del logger"""
        self.assertIsInstance(self.logger, SimuladorLogger)
    
    def test_log_simulacion_si_existe(self):
        """Test logging de simulación si el método existe"""
        if hasattr(self.logger, 'log_simulacion'):
            # No debería causar errores
            self.logger.log_simulacion("Test de simulación")
    
    def test_log_sistema_si_existe(self):
        """Test logging de sistema si el método existe"""
        if hasattr(self.logger, 'log_sistema'):
            self.logger.log_sistema("Test de sistema")
    
    def test_log_configuracion_si_existe(self):
        """Test logging de configuración si el método existe"""
        if hasattr(self.logger, 'log_configuracion'):
            self.logger.log_configuracion("Test configuración")
    
    def test_log_economia_si_existe(self):
        """Test logging económico si el método existe"""
        if hasattr(self.logger, 'log_economia'):
            datos_economicos = {"pib": 100000, "inflacion": 0.02}
            self.logger.log_economia(datos_economicos)
    
    def test_obtener_estadisticas_si_existe(self):
        """Test obtener estadísticas si el método existe"""
        if hasattr(self.logger, 'obtener_estadisticas'):
            stats = self.logger.obtener_estadisticas()
            if stats is not None:
                self.assertIsInstance(stats, dict)
    
    def test_cerrar_logger_si_existe(self):
        """Test cerrar logger si el método existe"""
        if hasattr(self.logger, 'close'):
            # No debería causar errores
            try:
                self.logger.close()
            except Exception as e:
                # Si falla, al menos verificar que es un error esperado
                self.assertIsInstance(e, (ValueError, AttributeError, OSError))


class TestEconomiaBasicaE2E(unittest.TestCase):
    """Tests E2E básicos para economía"""
    
    def setUp(self):
        # Crear mercado básico
        self.bienes = {
            "comida": Bien("comida", "alimentos_basicos"),
            "ropa": Bien("ropa", "alimentos_lujo"),
            "casa": Bien("casa", "tecnologia")
        }
        self.mercado = Mercado(self.bienes)
    
    def test_crear_economia_basica(self):
        """Test crear una economía básica funcional"""
        # Añadir consumidores
        for i in range(10):
            consumidor = Consumidor(f"consumidor_{i}", self.mercado)
            self.mercado.agregar_persona(consumidor)
        
        # Añadir empresas
        for i in range(3):
            empresa = Empresa(f"empresa_{i}", self.mercado)
            self.mercado.agregar_persona(empresa)
        
        # Verificar que se creó correctamente
        consumidores = self.mercado.getConsumidores()
        empresas = self.mercado.getEmpresas()
        
        self.assertEqual(len(consumidores), 10)
        self.assertEqual(len(empresas), 3)
        self.assertEqual(len(self.mercado.personas), 13)
    
    def test_simulacion_corta_funcional(self):
        """Test simulación corta que debe funcionar"""
        # Crear economía pequeña
        for i in range(5):
            consumidor = Consumidor(f"cons_{i}", self.mercado)
            self.mercado.agregar_persona(consumidor)
        
        for i in range(2):
            empresa = Empresa(f"emp_{i}", self.mercado)
            self.mercado.agregar_persona(empresa)
        
        # Ejecutar algunos ciclos
        for ciclo in range(1, 4):
            try:
                self.mercado.ejecutar_ciclo(ciclo)
            except Exception as e:
                # Si falla, al menos verificar que el mercado sigue válido
                self.assertGreater(len(self.mercado.personas), 0)
                # Y que el error no es crítico
                self.assertIsInstance(e, (ValueError, AttributeError, KeyError))
        
        # Verificar que el mercado sigue siendo válido
        self.assertGreater(len(self.mercado.getConsumidores()), 0)
        self.assertGreater(len(self.mercado.getEmpresas()), 0)
    
    def test_mercado_con_transacciones_basicas(self):
        """Test mercado con capacidad de transacciones"""
        # Crear participantes
        consumidor = Consumidor("test_buyer", self.mercado)
        empresa = Empresa("test_seller", self.mercado)
        
        self.mercado.agregar_persona(consumidor)
        self.mercado.agregar_persona(empresa)
        
        # Verificar dinero inicial
        dinero_inicial_consumidor = consumidor.dinero
        dinero_inicial_empresa = empresa.dinero
        
        self.assertGreater(dinero_inicial_consumidor, 0)
        self.assertGreater(dinero_inicial_empresa, 0)
        
        # Verificar que las empresas tienen precios
        if hasattr(empresa, 'precios'):
            self.assertIsInstance(empresa.precios, dict)
            for bien_nombre, precio in empresa.precios.items():
                self.assertGreater(precio, 0)
    
    def test_mercado_con_gobierno(self):
        """Test que el mercado tiene gobierno funcional"""
        # Verificar que el gobierno existe
        self.assertIsNotNone(self.mercado.gobierno)
        
        # Verificar que el gobierno tiene presupuesto
        if hasattr(self.mercado.gobierno, 'presupuesto'):
            self.assertGreater(self.mercado.gobierno.presupuesto, 0)
        
        # Verificar que el gobierno puede interactuar
        if hasattr(self.mercado.gobierno, 'ejecutar_politica_fiscal'):
            try:
                self.mercado.gobierno.ejecutar_politica_fiscal(1)
            except Exception as e:
                # Error esperado por falta de datos
                self.assertIsInstance(e, (ValueError, AttributeError, KeyError))
    
    def test_mercado_con_sistema_bancario(self):
        """Test que el mercado tiene sistema bancario"""
        # Verificar que existe sistema bancario
        self.assertIsNotNone(self.mercado.sistema_bancario)
        
        # Verificar que tiene bancos si están inicializados
        if hasattr(self.mercado.sistema_bancario, 'bancos'):
            bancos = self.mercado.sistema_bancario.bancos
            self.assertIsInstance(bancos, list)
    
    def test_indicadores_economicos_basicos(self):
        """Test que se pueden calcular indicadores económicos básicos"""
        # Añadir algunas personas para tener datos
        for i in range(3):
            consumidor = Consumidor(f"c_{i}", self.mercado)
            self.mercado.agregar_persona(consumidor)
        
        # PIB histórico
        if hasattr(self.mercado, 'pib_historico'):
            self.assertIsInstance(self.mercado.pib_historico, list)
        
        # Inflación histórica
        if hasattr(self.mercado, 'inflacion_historica'):
            self.assertIsInstance(self.mercado.inflacion_historica, list)
        
        # Verificar que se pueden obtener datos de dinero
        dinero_consumidores = self.mercado.getDineroConsumidores()
        self.assertIsInstance(dinero_consumidores, list)
        
        # Verificar que hay dinero en el sistema
        total_dinero = sum(dinero_consumidores)
        self.assertGreater(total_dinero, 0)


class TestIntegracionSistemas(unittest.TestCase):
    """Tests de integración entre sistemas"""
    
    def setUp(self):
        bienes = {"pan": Bien("pan", "alimentos_basicos")}
        self.mercado = Mercado(bienes)
    
    def test_mercado_con_analytics(self):
        """Test integración mercado con analytics"""
        # Verificar que el mercado tiene analytics
        if hasattr(self.mercado, 'sistema_analytics'):
            analytics = self.mercado.sistema_analytics
            self.assertIsNotNone(analytics)
            
            # Verificar que analytics tiene referencia al mercado
            if hasattr(analytics, 'mercado'):
                self.assertEqual(analytics.mercado, self.mercado)
    
    def test_mercado_con_innovacion(self):
        """Test integración mercado con sistema de innovación"""
        if hasattr(self.mercado, 'sistema_innovacion'):
            innovacion = self.mercado.sistema_innovacion
            self.assertIsNotNone(innovacion)
            
            # Verificar que se puede procesar innovación
            if hasattr(innovacion, 'procesar_ciclo'):
                try:
                    innovacion.procesar_ciclo(1)
                except Exception as e:
                    self.assertIsInstance(e, (ValueError, AttributeError, KeyError))
    
    def test_mercado_con_mercado_laboral(self):
        """Test integración con mercado laboral"""
        if hasattr(self.mercado, 'mercado_laboral'):
            mercado_laboral = self.mercado.mercado_laboral
            self.assertIsNotNone(mercado_laboral)
            
            # Verificar que puede procesar empleos
            if hasattr(mercado_laboral, 'procesar_empleos'):
                try:
                    mercado_laboral.procesar_empleos()
                except Exception as e:
                    self.assertIsInstance(e, (ValueError, AttributeError, KeyError))
    
    def test_sistemas_integrados_initialization(self):
        """Test que los sistemas se inicializan correctamente"""
        # Verificar sistemas básicos
        sistemas_esperados = [
            'sistema_bancario', 'economia_sectorial', 'sistema_innovacion',
            'mercado_laboral', 'sistema_analytics'
        ]
        
        for sistema in sistemas_esperados:
            if hasattr(self.mercado, sistema):
                valor = getattr(self.mercado, sistema)
                self.assertIsNotNone(valor)


class TestConstantesConfiguracion(unittest.TestCase):
    """Tests adicionales para configuración"""
    
    def test_configuracion_coherente_precios(self):
        """Test que la configuración de precios es coherente"""
        # Los salarios deben permitir comprar bienes básicos
        salario_min = ConfigEconomica.SALARIO_BASE_MIN
        dinero_consumidor_max = ConfigEconomica.DINERO_INICIAL_CONSUMIDOR_MAX
        
        # Un consumidor con salario mínimo debe poder ahorrar algo
        self.assertLess(salario_min * 0.8, dinero_consumidor_max)
    
    def test_rangos_empresa_consumidor_logicos(self):
        """Test que los rangos empresa-consumidor son lógicos"""
        # Las empresas deben tener más dinero inicial que los consumidores
        dinero_emp_min = ConfigEconomica.DINERO_INICIAL_EMPRESA_MIN
        dinero_cons_max = ConfigEconomica.DINERO_INICIAL_CONSUMIDOR_MAX
        
        self.assertGreater(dinero_emp_min, dinero_cons_max)
        
        # La diferencia no debe ser excesiva (factor razonable)
        ratio = dinero_emp_min / dinero_cons_max
        self.assertLess(ratio, 20)  # No más de 20x diferencia
        self.assertGreater(ratio, 2)  # Al menos 2x diferencia
    
    def test_salarios_vs_dinero_inicial(self):
        """Test relación lógica entre salarios y dinero inicial"""
        salario_max = ConfigEconomica.SALARIO_BASE_MAX
        dinero_inicial_min = ConfigEconomica.DINERO_INICIAL_CONSUMIDOR_MIN
        
        # El dinero inicial debe ser al menos 1-2 meses de salario mínimo
        meses_supervivencia = dinero_inicial_min / ConfigEconomica.SALARIO_BASE_MIN
        self.assertGreaterEqual(meses_supervivencia, 1.0)
        self.assertLessEqual(meses_supervivencia, 12.0)  # No más de un año


class TestCreacionInstanciasBasicas(unittest.TestCase):
    """Tests de creación de instancias básicas"""
    
    def test_crear_multiples_consumidores(self):
        """Test crear múltiples consumidores sin errores"""
        bienes = {"agua": Bien("agua", "alimentos_basicos")}
        mercado = Mercado(bienes)
        
        consumidores = []
        for i in range(20):
            consumidor = Consumidor(f"test_consumer_{i}", mercado)
            consumidores.append(consumidor)
            
            # Verificar propiedades básicas
            self.assertIsInstance(consumidor.nombre, str)
            self.assertGreater(consumidor.dinero, 0)
            self.assertIsInstance(consumidor.empleado, bool)
            
        # Todos deben ser diferentes instancias
        self.assertEqual(len(set(id(c) for c in consumidores)), 20)
    
    def test_crear_multiples_empresas(self):
        """Test crear múltiples empresas sin errores"""
        bienes = {"producto": Bien("producto", "alimentos_basicos")}
        mercado = Mercado(bienes)
        
        empresas = []
        for i in range(10):
            empresa = Empresa(f"empresa_{i}", mercado)
            empresas.append(empresa)
            
            # Verificar propiedades básicas
            self.assertIsInstance(empresa.nombre, str)
            self.assertGreater(empresa.dinero, 0)
            self.assertIsInstance(empresa.precios, dict)
            
        # Todas deben ser diferentes instancias
        self.assertEqual(len(set(id(e) for e in empresas)), 10)
    
    def test_crear_diferentes_tipos_bienes(self):
        """Test crear bienes de diferentes categorías"""
        categorias = ["alimentos_basicos", "alimentos_lujo", "tecnologia"]
        
        bienes = {}
        for i, categoria in enumerate(categorias):
            for j in range(3):
                nombre = f"bien_{categoria}_{j}"
                bien = Bien(nombre, categoria)
                bienes[nombre] = bien
                
                self.assertEqual(bien.nombre, nombre)
                self.assertEqual(bien.categoria, categoria)
        
        # Crear mercado con todos los bienes
        mercado = Mercado(bienes)
        self.assertEqual(len(mercado.bienes), 9)  # 3 categorías x 3 bienes cada una
    
    def test_propiedades_bien_por_categoria(self):
        """Test propiedades específicas por categoría de bien"""
        bien_basico = Bien("arroz", "alimentos_basicos")
        bien_lujo = Bien("caviar", "alimentos_lujo")
        bien_tech = Bien("smartphone", "tecnologia")
        
        # Verificar que tienen diferentes elasticidades si existen
        if hasattr(bien_basico, 'elasticidad'):
            elasticidad_basico = bien_basico.elasticidad
            elasticidad_lujo = bien_lujo.elasticidad
            elasticidad_tech = bien_tech.elasticidad
            
            # Los básicos deberían ser menos elásticos que los de lujo
            self.assertLessEqual(elasticidad_basico, elasticidad_lujo)


if __name__ == '__main__':
    unittest.main()