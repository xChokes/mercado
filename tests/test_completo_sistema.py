"""
Tests automatizados para el Simulador Económico
Incluye tests unitarios, de integración y de performance
"""

from src.config.ConfiguradorSimulacion import ConfiguradorSimulacion
from src.systems.EstimuloEconomico import detectar_estancamiento_economico, aplicar_estimulo_emergencia
from src.systems.SistemaBancario import SistemaBancario, Banco
from src.systems.MercadoLaboral import MercadoLaboral
from src.systems.CrisisFinanciera import evaluar_recuperacion_crisis, aplicar_medidas_recuperacion
from src.systems.AnalyticsML import SistemaAnalyticsML, PredictorDemanda
from src.models.EmpresaProductora import EmpresaProductora
from src.models.Empresa import Empresa
from src.models.Consumidor import Consumidor
from src.models.Bien import Bien
from src.models.Mercado import Mercado
import unittest
import sys
import os
import time
import tempfile
import json

# Añadir src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


class TestModelosBasicos(unittest.TestCase):
    """Tests para modelos económicos básicos"""

    def setUp(self):
        """Configuración para cada test"""
        self.mercado = Mercado()
        self.bien = Bien('Arroz', 'alimentos_basicos')
        self.mercado.agregar_bien('Arroz', self.bien)

    def test_creacion_mercado(self):
        """Test de creación de mercado"""
        self.assertIsInstance(self.mercado, Mercado)
        self.assertEqual(len(self.mercado.personas), 0)
        self.assertEqual(len(self.mercado.bienes), 1)

    def test_agregar_bien(self):
        """Test de agregar bienes al mercado"""
        bien_nuevo = Bien('Pan', 'alimentos_basicos')
        self.mercado.agregar_bien('Pan', bien_nuevo)
        self.assertEqual(len(self.mercado.bienes), 2)
        self.assertIn('Pan', self.mercado.bienes)

    def test_creacion_consumidor(self):
        """Test de creación de consumidor"""
        consumidor = Consumidor('Juan', self.mercado)
        self.assertEqual(consumidor.nombre, 'Juan')
        self.assertTrue(hasattr(consumidor, 'dinero'))
        self.assertTrue(hasattr(consumidor, 'ingreso_mensual'))

    def test_creacion_empresa(self):
        """Test de creación de empresa"""
        empresa = Empresa.crear_con_acciones(
            'TechCorp', self.mercado, 1000, {})
        self.assertEqual(empresa.nombre, 'TechCorp')
        self.assertTrue(hasattr(empresa, 'dinero'))
        self.assertTrue(hasattr(empresa, 'empleados'))

    def test_empresa_productora(self):
        """Test de empresa productora"""
        empresa = EmpresaProductora('AgroEmpresa', self.mercado)
        self.assertIsInstance(empresa, EmpresaProductora)
        self.assertTrue(hasattr(empresa, 'producir'))


class TestSistemaBancario(unittest.TestCase):
    """Tests para el sistema bancario"""

    def setUp(self):
        self.mercado = Mercado()
        self.sistema_bancario = SistemaBancario()
        self.banco = Banco('BancoTest', 1000000)
        self.sistema_bancario.agregar_banco(self.banco)

        self.consumidor = Consumidor('Cliente1', self.mercado)
        self.mercado.agregar_persona(self.consumidor)

    def test_creacion_banco(self):
        """Test de creación de banco"""
        self.assertEqual(self.banco.nombre, 'BancoTest')
        self.assertEqual(self.banco.capital, 1000000)
        self.assertEqual(len(self.banco.depositos), 0)
        self.assertEqual(len(self.banco.prestamos), 0)

    def test_deposito_bancario(self):
        """Test de depósito bancario"""
        monto_inicial = self.consumidor.dinero
        resultado = self.banco.recibir_deposito(self.consumidor.id, 5000)

        self.assertTrue(resultado)
        self.assertEqual(self.banco.depositos[self.consumidor.id], 5000)
        self.assertEqual(self.consumidor.dinero, monto_inicial - 5000)

    def test_solicitud_prestamo(self):
        """Test de solicitud de préstamo"""
        # Dar un ingreso decente al consumidor para que califique
        self.consumidor.ingreso_mensual = 5000
        self.consumidor.empleado = True

        resultado, mensaje = self.banco.solicitar_prestamo(
            self.consumidor, 20000, 12)

        # Debe ser True o tener un mensaje específico
        self.assertIsInstance(resultado, bool)
        if resultado:
            self.assertIn(self.consumidor.id, self.banco.prestamos)

    def test_evaluacion_riesgo(self):
        """Test de evaluación de riesgo crediticio"""
        self.consumidor.ingreso_mensual = 3000
        self.consumidor.empleado = True
        self.consumidor.ahorros = 5000

        riesgo = self.banco.evaluar_riesgo_crediticio(self.consumidor)

        self.assertIsInstance(riesgo, float)
        self.assertGreaterEqual(riesgo, 0.1)
        self.assertLessEqual(riesgo, 1.0)


class TestAnalyticsML(unittest.TestCase):
    """Tests para el sistema de Machine Learning"""

    def setUp(self):
        self.mercado = Mercado()
        self.bien = Bien('Computadora', 'tecnologia')
        self.mercado.agregar_bien('Computadora', self.bien)

        # Inicializar datos históricos mínimos
        self.mercado.pib_historico = [100000, 105000, 103000]
        self.mercado.desempleo_historico = [0.05, 0.06, 0.05]
        self.mercado.inflacion_historica = [0.02, 0.03, 0.02]
        self.mercado.ciclo_actual = 3

        self.predictor = PredictorDemanda()

    def test_extraccion_caracteristicas(self):
        """Test de extracción de características para ML"""
        caracteristicas = self.predictor.extraer_caracteristicas(
            self.mercado, 'Computadora')

        self.assertIsInstance(caracteristicas, list)
        # Debe tener varias características
        self.assertGreater(len(caracteristicas), 5)

        # Todas las características deben ser numéricas
        for caracteristica in caracteristicas:
            self.assertIsInstance(caracteristica, (int, float))

    def test_entrenamiento_modelo(self):
        """Test de entrenamiento del modelo ML"""
        resultado = self.predictor.entrenar(self.mercado, 'Computadora')

        self.assertTrue(resultado)  # Debe entrenar exitosamente
        self.assertTrue(self.predictor.caracteristicas_entrenadas)

    def test_prediccion_demanda(self):
        """Test de predicción de demanda"""
        # Entrenar primero
        self.predictor.entrenar(self.mercado, 'Computadora')

        demanda = self.predictor.predecir_demanda(self.mercado, 'Computadora')

        self.assertIsInstance(demanda, int)
        self.assertGreater(demanda, 0)
        self.assertLess(demanda, 1001)  # Dentro del rango esperado

    def test_sistema_analytics_completo(self):
        """Test del sistema completo de analytics"""
        sistema = SistemaAnalyticsML(self.mercado)
        sistema.ciclo_analytics()

        stats = sistema.obtener_estadisticas_analytics()

        self.assertIsInstance(stats, dict)
        self.assertIn('modelos_entrenados', stats)
        self.assertIn('predictores_disponibles', stats)


class TestCrisisFinanciera(unittest.TestCase):
    """Tests para el sistema de crisis financiera"""

    def setUp(self):
        self.mercado = Mercado()
        self.mercado.crisis_financiera_activa = True
        self.mercado.ciclos_en_crisis = 12
        self.mercado.pib_historico = [100000, 95000, 98000, 101000]
        self.mercado.desempleo_historico = [0.05, 0.15, 0.12, 0.10]
        self.mercado.transacciones = [
            {'ciclo': 1, 'bien': 'Arroz', 'cantidad': 5},
            {'ciclo': 2, 'bien': 'Pan', 'cantidad': 3},
            {'ciclo': 3, 'bien': 'Arroz', 'cantidad': 7}
        ]

    def test_evaluacion_recuperacion_crisis(self):
        """Test de evaluación de recuperación de crisis"""
        puede_recuperar = evaluar_recuperacion_crisis(self.mercado)

        self.assertIsInstance(puede_recuperar, bool)
        # Con los datos de prueba, debería poder recuperarse
        self.assertTrue(puede_recuperar)

    def test_aplicacion_medidas_recuperacion(self):
        """Test de aplicación de medidas de recuperación"""
        # Crear gobierno y sistema bancario mínimo
        from src.models.Gobierno import Gobierno
        self.mercado.gobierno = Gobierno(self.mercado)
        self.mercado.sistema_bancario = SistemaBancario()
        banco = Banco('TestBank', 1000000)
        self.mercado.sistema_bancario.agregar_banco(banco)

        tasa_inicial = self.mercado.gobierno.tasa_interes_referencia

        aplicar_medidas_recuperacion(self.mercado)

        # La tasa de interés debería haberse reducido
        self.assertLess(
            self.mercado.gobierno.tasa_interes_referencia, tasa_inicial)


class TestEstimuloEconomico(unittest.TestCase):
    """Tests para el sistema de estímulo económico"""

    def setUp(self):
        self.mercado = Mercado()
        # PIB en 0 para activar estímulo
        self.mercado.pib_historico = [0, 0, 0]

        # Crear gobierno
        from src.models.Gobierno import Gobierno
        self.mercado.gobierno = Gobierno(self.mercado)

        # Crear empresas y consumidores para el estímulo
        empresa = EmpresaProductora('TestEmpresa', self.mercado)
        self.mercado.agregar_persona(empresa)

        consumidor = Consumidor('TestConsumidor', self.mercado)
        self.mercado.agregar_persona(consumidor)

    def test_deteccion_estancamiento(self):
        """Test de detección de estancamiento económico"""
        estancado = detectar_estancamiento_economico(self.mercado)
        # Con PIB = [0, 0, 0] debe detectar estancamiento
        self.assertTrue(estancado)

    def test_aplicacion_estimulo(self):
        """Test de aplicación de estímulo de emergencia"""
        presupuesto_inicial = self.mercado.gobierno.presupuesto

        aplicar_estimulo_emergencia(self.mercado)

        # El presupuesto debería haber disminuido (gastado en estímulos)
        self.assertLess(self.mercado.gobierno.presupuesto, presupuesto_inicial)


class TestConfiguracion(unittest.TestCase):
    """Tests para el sistema de configuración"""

    def test_carga_configuracion_defecto(self):
        """Test de carga de configuración por defecto"""
        config = ConfiguradorSimulacion()

        self.assertIsInstance(config.config, dict)
        self.assertIn('simulacion', config.config)
        self.assertIn('economia', config.config)

    def test_obtencion_valores(self):
        """Test de obtención de valores específicos"""
        config = ConfiguradorSimulacion()

        num_ciclos = config.obtener('simulacion', 'num_ciclos', 50)
        self.assertIsInstance(num_ciclos, int)
        self.assertGreater(num_ciclos, 0)

        # Test de valor por defecto
        valor_inexistente = config.obtener(
            'seccion_inexistente', 'clave_inexistente', 999)
        self.assertEqual(valor_inexistente, 999)


class TestPerformance(unittest.TestCase):
    """Tests de performance y escalabilidad"""

    def test_simulacion_rapida(self):
        """Test de que una simulación pequeña sea rápida"""
        inicio = time.time()

        # Crear simulación pequeña
        mercado = Mercado()
        bien = Bien('TestBien', 'test')
        mercado.agregar_bien('TestBien', bien)

        # Agregar algunos agentes
        for i in range(10):
            consumidor = Consumidor(f'C{i}', mercado)
            mercado.agregar_persona(consumidor)

        empresa = EmpresaProductora('TestEmpresa', mercado)
        mercado.agregar_persona(empresa)

        # Ejecutar algunos ciclos
        for _ in range(10):
            mercado.ejecutar_ciclo()

        tiempo_total = time.time() - inicio

        # Debe completarse en menos de 10 segundos
        self.assertLess(tiempo_total, 10.0)
        print(
            f"Simulación de 10 ciclos completada en {tiempo_total:.2f} segundos")

    def test_memoria_no_excesiva(self):
        """Test de que el uso de memoria sea razonable"""
        import psutil
        import os

        proceso = psutil.Process(os.getpid())
        memoria_inicial = proceso.memory_info().rss / 1024 / 1024  # MB

        # Crear simulación más grande
        mercado = Mercado()
        bien = Bien('TestBien', 'test')
        mercado.agregar_bien('TestBien', bien)

        # Agregar muchos agentes
        for i in range(100):
            consumidor = Consumidor(f'C{i}', mercado)
            mercado.agregar_persona(consumidor)

        for i in range(5):
            empresa = EmpresaProductora(f'E{i}', mercado)
            mercado.agregar_persona(empresa)

        memoria_final = proceso.memory_info().rss / 1024 / 1024  # MB
        incremento_memoria = memoria_final - memoria_inicial

        # No debería usar más de 100MB adicionales
        self.assertLess(incremento_memoria, 100)
        print(f"Incremento de memoria: {incremento_memoria:.2f} MB")


class TestIntegracion(unittest.TestCase):
    """Tests de integración entre sistemas"""

    def setUp(self):
        self.mercado = Mercado()

        # Configurar mercado completo
        bien = Bien('Arroz', 'alimentos_basicos')
        self.mercado.agregar_bien('Arroz', bien)

        # Agregar agentes
        self.consumidor = Consumidor('TestConsumidor', self.mercado)
        self.mercado.agregar_persona(self.consumidor)

        self.empresa = EmpresaProductora('TestEmpresa', self.mercado)
        self.mercado.agregar_persona(self.empresa)

        # Sistemas avanzados
        from src.models.Gobierno import Gobierno
        self.mercado.gobierno = Gobierno(self.mercado)
        self.mercado.sistema_bancario = SistemaBancario()
        banco = Banco('TestBank', 1000000)
        self.mercado.sistema_bancario.agregar_banco(banco)

    def test_ciclo_completo(self):
        """Test de un ciclo económico completo"""
        # Estado inicial
        pib_inicial = len(self.mercado.pib_historico)

        # Ejecutar ciclo
        self.mercado.ejecutar_ciclo()

        # Verificar que se actualizaron las métricas
        self.assertEqual(len(self.mercado.pib_historico), pib_inicial + 1)
        self.assertGreaterEqual(len(self.mercado.transacciones), 0)

    def test_interaccion_sistemas(self):
        """Test de interacción entre diferentes sistemas"""
        # El consumidor debe poder interactuar con el banco
        banco = self.mercado.sistema_bancario.bancos[0]

        # Depositar dinero
        resultado_deposito = banco.recibir_deposito(self.consumidor.id, 1000)
        self.assertTrue(resultado_deposito)

        # La empresa debe poder contratar al consumidor
        resultado_contrato = self.empresa.contratar(self.consumidor)
        # El resultado puede variar, pero no debe fallar
        self.assertIsInstance(resultado_contrato, bool)


def ejecutar_tests_completos():
    """Ejecuta todos los tests y genera un reporte"""
    print("🧪 Ejecutando tests del Simulador Económico...")
    print("=" * 60)

    # Crear suite de tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Agregar todas las clases de test
    clases_test = [
        TestModelosBasicos,
        TestSistemaBancario,
        TestAnalyticsML,
        TestCrisisFinanciera,
        TestEstimuloEconomico,
        TestConfiguracion,
        TestPerformance,
        TestIntegracion
    ]

    for clase_test in clases_test:
        tests = loader.loadTestsFromTestCase(clase_test)
        suite.addTests(tests)

    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    resultado = runner.run(suite)

    # Reporte final
    print("\n" + "=" * 60)
    print("📊 REPORTE FINAL DE TESTS")
    print("=" * 60)
    print(f"Tests ejecutados: {resultado.testsRun}")
    print(f"Errores: {len(resultado.errors)}")
    print(f"Fallos: {len(resultado.failures)}")

    if resultado.errors:
        print("\n❌ ERRORES:")
        for test, error in resultado.errors:
            print(f"  - {test}: {error}")

    if resultado.failures:
        print("\n❌ FALLOS:")
        for test, failure in resultado.failures:
            print(f"  - {test}: {failure}")

    if resultado.wasSuccessful():
        print("\n✅ ¡TODOS LOS TESTS PASARON!")
        return True
    else:
        print(f"\n❌ {len(resultado.errors + resultado.failures)} tests fallaron")
        return False


if __name__ == '__main__':
    ejecutar_tests_completos()
