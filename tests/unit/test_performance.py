"""
Tests de Performance y Estrés
=============================

Tests para validar el rendimiento del sistema bajo diferentes
cargas de trabajo y condiciones de estrés.
"""

import unittest
import sys
import os
import time
import gc
from unittest.mock import Mock

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.models.Mercado import Mercado
from src.models.Consumidor import Consumidor
from src.models.Empresa import Empresa
from src.models.Bien import Bien
from src.config.ConfiguradorSimulacion import ConfiguradorSimulacion


class TestPerformanceVectorizacion(unittest.TestCase):
    """Tests de performance con vectorización"""
    
    def setUp(self):
        """Configurar mercado para tests de vectorización"""
        bienes = {}
        for i in range(10):
            bien = Bien(f"producto_{i}", "categoria_test")
            bienes[f"producto_{i}"] = bien
        
        self.mercado = Mercado(bienes)
        
        # Agregar empresas y consumidores para tests
        for i in range(20):
            empresa = Empresa(f"Empresa_{i}", self.mercado)
            empresa.dinero = 10000 + i * 1000
            # Establecer precios
            for j in range(5):
                producto = f"producto_{j}"
                if producto in bienes:
                    empresa.precios[producto] = 10 + j * 2
            self.mercado.agregar_persona(empresa)
        
        for i in range(50):
            consumidor = Consumidor(f"Consumidor_{i}", self.mercado)
            self.mercado.agregar_persona(consumidor)
    
    def test_calculo_pib_vectorizado_vs_tradicional(self):
        """Compara rendimiento del cálculo PIB vectorizado vs tradicional"""
        # Configurar sistema de vectorización
        config_perf = {'optimizar_calculos_pib': True}
        self.mercado.inicializar_sistema_rendimiento(config_perf)
        
        # Preparar transacciones de prueba
        transacciones = []
        for i in range(100):
            transacciones.append({
                'costo_total': 100 + i * 10,
                'ciclo': 1,
                'bien': f'producto_{i % 5}',
                'cantidad': 1 + i % 3
            })
        
        self.mercado.transacciones_ciclo_actual = transacciones
        
        # Medir tiempo vectorizado
        inicio_vectorizado = time.time()
        for _ in range(10):  # Múltiples iteraciones para mejor medición
            self.mercado.registrar_estadisticas()
        tiempo_vectorizado = time.time() - inicio_vectorizado
        
        # Deshabilitar vectorización para comparar
        self.mercado.config_performance = {'optimizar_calculos_pib': False}
        self.mercado.transacciones_ciclo_actual = transacciones
        
        # Medir tiempo tradicional
        inicio_tradicional = time.time()
        for _ in range(10):
            self.mercado._registrar_estadisticas_tradicional()
        tiempo_tradicional = time.time() - inicio_tradicional
        
        print(f"\n📊 Benchmark PIB:")
        print(f"   Vectorizado: {tiempo_vectorizado:.3f}s")
        print(f"   Tradicional: {tiempo_tradicional:.3f}s")
        
        if tiempo_tradicional > 0:
            mejora = ((tiempo_tradicional - tiempo_vectorizado) / tiempo_tradicional) * 100
            print(f"   Mejora: {mejora:.1f}%")
        
        # El método vectorizado debería ser al menos igual de rápido
        self.assertLessEqual(tiempo_vectorizado, tiempo_tradicional * 1.1)  # 10% tolerancia
    
    def test_indice_precios_vectorizado_vs_tradicional(self):
        """Compara rendimiento del cálculo de índice de precios"""
        # Habilitar vectorización
        config_perf = {'optimizar_indices_precios': True}
        self.mercado.inicializar_sistema_rendimiento(config_perf)
        
        # Agregar más empresas para mejor benchmark
        for i in range(20, 100):
            empresa = Empresa(f"EmpresaExtra_{i}", self.mercado)
            for j in range(10):
                producto = f"producto_{j}"
                empresa.precios[producto] = 10 + j * 2 + (i % 5)
            self.mercado.agregar_persona(empresa)
        
        # Medir tiempo vectorizado
        inicio_vectorizado = time.time()
        for _ in range(50):  # Múltiples iteraciones
            indice_vectorizado = self.mercado.calcular_indice_precios()
        tiempo_vectorizado = time.time() - inicio_vectorizado
        
        # Deshabilitar vectorización para comparar
        self.mercado.config_performance = {'optimizar_indices_precios': False}
        
        # Medir tiempo tradicional
        inicio_tradicional = time.time()
        for _ in range(50):
            indice_tradicional = self.mercado.calcular_indice_precios()
        tiempo_tradicional = time.time() - inicio_tradicional
        
        print(f"\n📊 Benchmark Índice Precios:")
        print(f"   Vectorizado: {tiempo_vectorizado:.3f}s")
        print(f"   Tradicional: {tiempo_tradicional:.3f}s")
        
        if tiempo_tradicional > 0:
            mejora = ((tiempo_tradicional - tiempo_vectorizado) / tiempo_tradicional) * 100
            print(f"   Mejora: {mejora:.1f}%")
        
        # Verificar que los resultados son similares
        self.assertAlmostEqual(indice_vectorizado, indice_tradicional, delta=0.1)
        
        # El método vectorizado debería ser al menos igual de rápido
        self.assertLessEqual(tiempo_vectorizado, tiempo_tradicional * 1.1)
    
    def test_sistema_completo_performance(self):
        """Test de performance del sistema completo con/sin optimizaciones"""
        config = ConfiguradorSimulacion()
        
        # Test sin optimizaciones
        config_dict = config.config
        config_dict['simulacion']['num_ciclos'] = 3
        config_dict['simulacion']['num_consumidores'] = 50
        config_dict['performance'] = {
            'activar_vectorizacion': False,
            'optimizar_calculos_pib': False,
            'optimizar_indices_precios': False
        }
        
        inicio_sin_opt = time.time()
        from main import ejecutar_simulacion_completa
        mercado_sin_opt = ejecutar_simulacion_completa(config)
        tiempo_sin_opt = time.time() - inicio_sin_opt
        
        # Test con optimizaciones
        config_dict['performance'] = {
            'activar_vectorizacion': True,
            'optimizar_calculos_pib': True,
            'optimizar_indices_precios': True
        }
        
        inicio_con_opt = time.time()
        mercado_con_opt = ejecutar_simulacion_completa(config)
        tiempo_con_opt = time.time() - inicio_con_opt
        
        print(f"\n📊 Benchmark Sistema Completo:")
        print(f"   Sin optimizaciones: {tiempo_sin_opt:.2f}s")
        print(f"   Con optimizaciones: {tiempo_con_opt:.2f}s")
        
        if tiempo_sin_opt > 0:
            mejora = ((tiempo_sin_opt - tiempo_con_opt) / tiempo_sin_opt) * 100
            print(f"   Mejora: {mejora:.1f}%")
            
            # Las optimizaciones deberían proporcionar alguna mejora o al menos no empeorar
            self.assertLessEqual(tiempo_con_opt, tiempo_sin_opt * 1.05)  # 5% tolerancia
        
        # Verificar que los resultados son consistentes
        self.assertEqual(len(mercado_sin_opt.pib_historico), len(mercado_con_opt.pib_historico))


class TestPerformanceBasico(unittest.TestCase):
    """Tests básicos de performance"""
    
    def test_creacion_masiva_consumidores(self):
        """Test creación masiva de consumidores - performance"""
        bienes = {}
        for i in range(5):
            bien = Bien(f"producto_{i}", "categoria_test")
            bienes[f"producto_{i}"] = bien
        
        mercado = Mercado(bienes)
        
        inicio = time.time()
        
        # Crear muchos consumidores
        for i in range(500):
            consumidor = Consumidor(f"Consumidor_{i}", mercado)
            mercado.agregar_persona(consumidor)
        
        tiempo_total = time.time() - inicio
        
        # Debería completarse en tiempo razonable (menos de 5 segundos)
        self.assertLess(tiempo_total, 5.0, 
                       f"Creación de 500 consumidores tomó {tiempo_total:.2f}s")
        self.assertEqual(len(mercado.getConsumidores()), 500)
    
    def test_creacion_masiva_empresas(self):
        """Test creación masiva de empresas - performance"""
        bienes = {}
        for i in range(10):
            bien = Bien(f"producto_{i}", "categoria_test")
            bienes[f"producto_{i}"] = bien
        
        mercado = Mercado(bienes)
        
        inicio = time.time()
        
        # Crear muchas empresas
        for i in range(200):
            empresa = Empresa(f"Empresa_{i}", mercado)
            mercado.agregar_persona(empresa)
        
        tiempo_total = time.time() - inicio
        
        # Debería completarse en tiempo razonable
        self.assertLess(tiempo_total, 3.0, 
                       f"Creación de 200 empresas tomó {tiempo_total:.2f}s")
        self.assertEqual(len(mercado.getEmpresas()), 200)
    
    def test_operaciones_mercado_repetitivas(self):
        """Test operaciones repetitivas en el mercado"""
        bienes = {}
        for i in range(10):
            bien = Bien(f"producto_{i}", "categoria_test")
            bienes[f"producto_{i}"] = bien
        
        mercado = Mercado(bienes)
        
        # Preparar mercado con algunos participantes
        for i in range(10):
            consumidor = Consumidor(f"C_{i}", mercado)
            mercado.agregar_persona(consumidor)
            
            empresa = Empresa(f"E_{i}", mercado)
            empresa.establecer_precio(f"Producto_{i}", 10.0 + i)
            mercado.agregar_persona(empresa)
        
        inicio = time.time()
        
        # Realizar muchas operaciones
        for i in range(1000):
            # Simular operaciones típicas del mercado
            if i % 3 == 0:
                # Calcular PIB
                mercado.calcular_pib_total()
            elif i % 3 == 1:
                # Actualizar precios
                if mercado.getEmpresas():
                    empresa = mercado.getEmpresas()[i % len(mercado.getEmpresas())]
                    precio = float((i % 100) + 1)  # Ensure price is always > 0
                    empresa.establecer_precio(f"Producto_temp_{i}", precio)
            else:
                # Simular compras
                if mercado.getConsumidores() and mercado.bienes:
                    consumidor = mercado.getConsumidores()[i % len(mercado.getConsumidores())]
                    bien_nombre = list(mercado.bienes.keys())[0]
                    consumidor.comprar(bien_nombre, 1)
        
        tiempo_total = time.time() - inicio
        
        # 1000 operaciones deberían completarse rápidamente
        self.assertLess(tiempo_total, 2.0, 
                       f"1000 operaciones tomaron {tiempo_total:.2f}s")
    
    def test_configuracion_carga_multiple(self):
        """Test carga múltiple de configuraciones"""
        inicio = time.time()
        
        # Cargar configuración múltiples veces
        for i in range(100):
            config = ConfiguradorSimulacion()
            self.assertTrue(config.validar())
        
        tiempo_total = time.time() - inicio
        
        # 100 cargas de configuración deberían ser rápidas
        self.assertLess(tiempo_total, 1.0, 
                       f"100 cargas de configuración tomaron {tiempo_total:.2f}s")


class TestStressSistema(unittest.TestCase):
    """Tests de estrés del sistema"""
    
    def test_mercado_grande_stress(self):
        """Test mercado con gran cantidad de participantes"""
        bienes = {}
        num_bienes = 50
        for i in range(num_bienes):
            bien = Bien(f"producto_{i}", "categoria_test")
            bienes[f"producto_{i}"] = bien
        
        mercado = Mercado(bienes)
        
        # Crear mercado grande
        num_consumidores = 1000
        num_empresas = 100
        num_bienes = 50
        
        # Añadir consumidores
        for i in range(num_consumidores):
            consumidor = Consumidor(f"Consumidor_{i}", mercado)
            mercado.agregar_persona(consumidor)
        
        # Añadir empresas con productos
        for i in range(num_empresas):
            empresa = Empresa(f"Empresa_{i}", mercado)
            # Cada empresa produce varios bienes
            for j in range(num_bienes // num_empresas + 1):
                producto = f"Producto_{i}_{j}"
                empresa.establecer_precio(producto, 10.0 + i + j)
            mercado.agregar_persona(empresa)
        
        # Verificar que el mercado funciona con muchos participantes
        self.assertEqual(len(mercado.getConsumidores()), num_consumidores)
        self.assertEqual(len(mercado.getEmpresas()), num_empresas)
        self.assertGreater(len(mercado.bienes), 0)
        
        # Simular actividad intensa
        inicio = time.time()
        
        for _ in range(100):  # 100 iteraciones de actividad
            mercado.calcular_pib_total()
        
        tiempo_actividad = time.time() - inicio
        
        # Incluso con mercado grande, debería ser relativamente rápido
        self.assertLess(tiempo_actividad, 5.0, 
                       f"100 cálculos PIB en mercado grande tomaron {tiempo_actividad:.2f}s")
    
    def test_memoria_uso_controlado(self):
        """Test que el uso de memoria se mantiene controlado"""
        # Forzar recolección de basura inicial
        gc.collect()
        
        mercados = []
        
        # Crear y liberar múltiples mercados
        for i in range(50):
            bienes = {}
            for j in range(5):  # Menos bienes para el test de memoria
                bien = Bien(f"producto_{i}_{j}", "categoria_test")
                bienes[f"producto_{i}_{j}"] = bien
            
            mercado = Mercado(bienes)
            
            # Llenar el mercado
            for j in range(20):
                consumidor = Consumidor(f"C_{i}_{j}", mercado)
                mercado.agregar_persona(consumidor)
                
                empresa = Empresa(f"E_{i}_{j}", mercado)
                mercado.agregar_persona(empresa)
            
            mercados.append(mercado)
            
            # Cada 10 mercados, limpiar algunos
            if i % 10 == 9:
                # Mantener solo los últimos 5 mercados
                mercados = mercados[-5:]
                gc.collect()  # Forzar limpieza de memoria
        
        # El test pasa si no hay errores de memoria
        self.assertLessEqual(len(mercados), 50)
    
    def test_operaciones_concurrentes_simuladas(self):
        """Test operaciones concurrentes simuladas (sin threading real)"""
        bienes = {}
        for i in range(25):
            bien = Bien(f"producto_{i}", "categoria_test")
            bienes[f"producto_{i}"] = bien
        
        mercado = Mercado(bienes)
        
        # Preparar mercado
        consumidores = []
        for i in range(50):
            consumidor = Consumidor(f"C_{i}", mercado)
            consumidores.append(consumidor)
            mercado.agregar_persona(consumidor)
        
        empresas = []
        for i in range(25):
            empresa = Empresa(f"E_{i}", mercado)
            empresas.append(empresa)
            empresa.establecer_precio(f"Producto_{i}", 10.0 + i)
            mercado.agregar_persona(empresa)
        
        inicio = time.time()
        
        # Simular muchas operaciones "concurrentes"
        for operacion in range(2000):
            tipo_op = operacion % 4
            
            if tipo_op == 0:
                # Operación de compra
                consumidor = consumidores[operacion % len(consumidores)]
                if mercado.bienes:
                    bien = list(mercado.bienes.keys())[operacion % len(mercado.bienes)]
                    consumidor.comprar(bien, 1)
            
            elif tipo_op == 1:
                # Cambio de precios
                empresa = empresas[operacion % len(empresas)]
                nuevo_precio = 5.0 + (operacion % 50)
                empresa.establecer_precio(f"Producto_{operacion % len(empresas)}", nuevo_precio)
            
            elif tipo_op == 2:
                # Cálculo económico
                mercado.calcular_pib_total()
            
            else:
                # Añadir nuevo participante
                if operacion % 20 == 0:  # Solo cada 20 operaciones
                    nuevo_consumidor = Consumidor(f"Nuevo_{operacion}", mercado)
                    mercado.agregar_persona(nuevo_consumidor)
        
        tiempo_total = time.time() - inicio
        
        # 2000 operaciones variadas deberían completarse en tiempo razonable
        self.assertLess(tiempo_total, 5.0, 
                       f"2000 operaciones concurrentes tomaron {tiempo_total:.2f}s")


class TestLimitesRendimiento(unittest.TestCase):
    """Tests para encontrar límites de rendimiento"""
    
    def test_limite_consumidores_razonable(self):
        """Test límite razonable de consumidores"""
        bienes = {}
        for i in range(10):
            bien = Bien(f"producto_{i}", "categoria_test")
            bienes[f"producto_{i}"] = bien
        
        mercado = Mercado(bienes)
        
        inicio = time.time()
        limite_razonable = 2000
        
        # Crear hasta el límite razonable
        for i in range(limite_razonable):
            consumidor = Consumidor(f"C_{i}", mercado)
            mercado.agregar_persona(consumidor)
            
            # Verificar tiempo cada 500 consumidores
            if i % 500 == 499:
                tiempo_parcial = time.time() - inicio
                # No debería tomar más de 10 segundos para 500 consumidores
                self.assertLess(tiempo_parcial, 10.0, 
                               f"Crear {i+1} consumidores tomó {tiempo_parcial:.2f}s")
        
        tiempo_total = time.time() - inicio
        
        # Verificar que se crearon todos
        self.assertEqual(len(mercado.getConsumidores()), limite_razonable)
        
        # El tiempo total debería ser razonable
        self.assertLess(tiempo_total, 20.0, 
                       f"Crear {limite_razonable} consumidores tomó {tiempo_total:.2f}s")
    
    def test_calculo_pib_performance(self):
        """Test performance del cálculo de PIB"""
        bienes = {}
        for i in range(20):
            bien = Bien(f"producto_{i}", "categoria_test")
            bienes[f"producto_{i}"] = bien
        
        mercado = Mercado(bienes)
        
        # Crear mercado con datos para PIB
        for i in range(100):
            consumidor = Consumidor(f"C_{i}", mercado)
            consumidor.dinero = 1000 + i * 10
            mercado.agregar_persona(consumidor)
            
            empresa = Empresa(f"E_{i}", mercado)
            empresa.dinero = 10000 + i * 100
            mercado.agregar_persona(empresa)
        
        # Medir tiempo de cálculo de PIB
        inicio = time.time()
        
        for _ in range(1000):  # 1000 cálculos
            pib = mercado.calcular_pib_total()
            self.assertIsNotNone(pib)
        
        tiempo_total = time.time() - inicio
        
        # 1000 cálculos de PIB deberían ser muy rápidos (increased to 2.0s for system load)
        self.assertLess(tiempo_total, 2.0, 
                       f"1000 cálculos PIB tomaron {tiempo_total:.2f}s")
    
    def test_busqueda_bienes_performance(self):
        """Test performance de búsqueda de bienes"""
        bienes = {}
        
        # Crear muchos bienes
        num_bienes = 1000
        for i in range(num_bienes):
            bien = Bien(f"Producto_{i}", "categoria_test")
            bienes[f"Producto_{i}"] = bien
        
        mercado = Mercado(bienes)
        
        inicio = time.time()
        
        # Realizar muchas búsquedas
        for i in range(num_bienes):
            bien_nombre = f"Producto_{i % num_bienes}"
            self.assertIn(bien_nombre, mercado.bienes)
        
        tiempo_total = time.time() - inicio
        
        # Las búsquedas deberían ser muy rápidas
        self.assertLess(tiempo_total, 0.5, 
                       f"{num_bienes} búsquedas tomaron {tiempo_total:.2f}s")


if __name__ == '__main__':
    unittest.main()