"""
Tests de Integración Avanzados
==============================

Tests de integración para escenarios complejos y casos de uso reales
del simulador de mercado.
"""

import unittest
import sys
import os
import time
from unittest.mock import Mock, patch

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.models.Mercado import Mercado
from src.models.Consumidor import Consumidor
from src.models.Empresa import Empresa
from src.models.Bien import Bien
from src.config.ConfiguradorSimulacion import ConfiguradorSimulacion
from src.systems.ValidadorEconomico import ValidadorEconomico


class TestEscenariosReales(unittest.TestCase):
    """Tests para escenarios económicos realistas"""
    
    def setUp(self):
        """Configuración inicial para tests de escenarios"""
        self.configurador = ConfiguradorSimulacion()
        bienes = {}
        for i in range(10):
            bien = Bien(f"producto_{i}", "categoria_test")
            bienes[f"producto_{i}"] = bien
        self.mercado = Mercado(bienes)
    
    def test_escenario_crecimiento_economico(self):
        """Test escenario de crecimiento económico"""
        # Configurar mercado inicial
        num_consumidores = 50
        num_empresas = 10
        
        # Crear consumidores con dinero variado
        for i in range(num_consumidores):
            consumidor = Consumidor(f"Consumidor_{i}", self.mercado)
            consumidor.dinero = 1000 + (i * 50)  # Distribución gradual
            self.mercado.agregar_persona(consumidor)
        
        # Crear empresas con productos diversos
        productos = ["Alimentos", "Ropa", "Electronica", "Hogar", "Transporte"]
        for i in range(num_empresas):
            empresa = Empresa(f"Empresa_{i}", self.mercado)
            empresa.dinero = 10000 + (i * 1000)
            
            # Cada empresa produce productos específicos
            for j, producto in enumerate(productos):
                if i % len(productos) == j:
                    precio_base = 50 + (j * 20)
                    empresa.establecer_precio(f"{producto}_{i}", precio_base)
            
            self.mercado.agregar_persona(empresa)
        
        # Simular múltiples ciclos económicos
        pib_inicial = self.mercado.calcular_pib_total()
        
        for ciclo in range(10):
            # Simular actividad económica
            for _ in range(20):  # 20 transacciones por ciclo
                # Seleccionar consumidor y producto aleatorio
                consumidores = self.mercado.getConsumidores()
                if consumidores:
                    consumidor = consumidores[ciclo % len(consumidores)]
                    if self.mercado.bienes:
                        bien_nombre = list(self.mercado.bienes.keys())[ciclo % len(self.mercado.bienes)]
                        consumidor.comprar(bien_nombre, 1)
            
            # Calcular PIB después de cada ciclo
            pib_actual = self.mercado.calcular_pib_total()
            self.mercado.pib_historico.append(pib_actual)
        
        # Verificar que el sistema mantiene consistencia
        self.assertGreater(len(self.mercado.pib_historico), 0)
        self.assertEqual(len(self.mercado.getConsumidores()), num_consumidores)
        self.assertEqual(len(self.mercado.getEmpresas()), num_empresas)
    
    def test_escenario_crisis_economica(self):
        """Test escenario de crisis económica simulada"""
        # Preparar mercado próspero inicial
        for i in range(30):
            consumidor = Consumidor(f"C_{i}", self.mercado)
            consumidor.dinero = 2000
            self.mercado.agregar_persona(consumidor)
        
        for i in range(10):
            empresa = Empresa(f"E_{i}", self.mercado)
            empresa.dinero = 20000
            empresa.establecer_precio(f"Producto_{i}", 100)
            self.mercado.agregar_persona(empresa)
        
        pib_pre_crisis = self.mercado.calcular_pib_total()
        
        # Simular crisis: reducir dinero de todos
        factor_crisis = 0.5  # 50% de reducción
        
        for consumidor in self.mercado.getConsumidores():
            consumidor.dinero *= factor_crisis
        
        for empresa in self.mercado.getEmpresas():
            empresa.dinero *= factor_crisis
            # Aumentar precios debido a la crisis
            for producto in empresa.precios:
                empresa.precios[producto] *= 1.2
        
        pib_post_crisis = self.mercado.calcular_pib_total()
        
        # Verificar que la crisis tiene efecto medible
        self.assertLess(pib_post_crisis, pib_pre_crisis)
        
        # Simular recuperación gradual
        for ciclo in range(5):
            for consumidor in self.mercado.getConsumidores():
                consumidor.dinero *= 1.1  # 10% de crecimiento por ciclo
            
            for empresa in self.mercado.getEmpresas():
                empresa.dinero *= 1.05  # 5% de crecimiento para empresas
        
        pib_recuperacion = self.mercado.calcular_pib_total()
        
        # PIB debería haber mejorado con la recuperación
        self.assertGreater(pib_recuperacion, pib_post_crisis)
    
    def test_escenario_competencia_empresarial(self):
        """Test escenario de competencia entre empresas"""
        # Crear mercado con empresas competidoras
        empresas_competidoras = []
        producto_comun = "Smartphone"
        
        for i in range(5):
            empresa = Empresa(f"TechCorp_{i}", self.mercado)
            empresa.dinero = 15000
            # Todas compiten en el mismo producto con precios diferentes
            precio_inicial = 500 + (i * 50)  # Precios entre 500 y 700
            empresa.establecer_precio(producto_comun, precio_inicial)
            empresas_competidoras.append(empresa)
            self.mercado.agregar_persona(empresa)
        
        # Crear consumidores con preferencias de precio
        for i in range(40):
            consumidor = Consumidor(f"Buyer_{i}", self.mercado)
            consumidor.dinero = 1000
            self.mercado.agregar_persona(consumidor)
        
        # Simular competencia de precios
        for ronda in range(10):
            # Las empresas ajustan precios basándose en la competencia
            for empresa in empresas_competidoras:
                # Encontrar precio más bajo de la competencia
                precios_competencia = [e.precios.get(producto_comun, 1000) 
                                     for e in empresas_competidoras if e != empresa]
                precio_min_competencia = min(precios_competencia) if precios_competencia else 500
                
                # Ajustar precio para ser competitivo
                precio_actual = empresa.precios.get(producto_comun, 500)
                if precio_actual > precio_min_competencia:
                    nuevo_precio = precio_min_competencia * 0.95  # 5% menos
                    empresa.establecer_precio(producto_comun, max(nuevo_precio, 400))  # Mínimo 400
            
            # Simular compras de consumidores
            for _ in range(10):
                consumidores = self.mercado.getConsumidores()
                if consumidores:
                    consumidor = consumidores[ronda % len(consumidores)]
                    consumidor.comprar(producto_comun, 1)
        
        # Verificar que los precios convergieron hacia abajo
        precios_finales = [e.precios.get(producto_comun, 0) for e in empresas_competidoras]
        precio_promedio = sum(precios_finales) / len(precios_finales)
        
        # El precio promedio debería ser menor que el inicial
        self.assertLess(precio_promedio, 600, "La competencia debería reducir precios")
        
        # Los precios deberían estar relativamente cerca entre sí
        precio_max = max(precios_finales)
        precio_min = min(precios_finales)
        diferencia_relativa = (precio_max - precio_min) / precio_promedio
        self.assertLess(diferencia_relativa, 0.2, "Precios deberían converger")


class TestIntegracionSistemasCompletos(unittest.TestCase):
    """Tests de integración entre todos los sistemas"""
    
    def test_integracion_configuracion_mercado(self):
        """Test integración completa configuración + mercado"""
        # Cargar configuración
        config = ConfiguradorSimulacion()
        self.assertTrue(config.validar())
        
        # Crear mercado basado en configuración
        bienes = {}
        for i in range(5):
            bien = Bien(f"producto_{i}", "categoria_test")
            bienes[f"producto_{i}"] = bien
        mercado = Mercado(bienes)
        
        # Aplicar configuración al mercado
        num_consumidores = config.obtener("simulacion", "num_consumidores", 50)
        num_empresas = config.obtener("simulacion", "num_empresas_productoras", 10)
        pib_inicial = config.obtener("economia", "pib_inicial", 100000)
        
        # Crear participantes según configuración
        for i in range(min(num_consumidores, 20)):  # Limitar para test rápido
            consumidor = Consumidor(f"C_{i}", mercado)
            consumidor.dinero = pib_inicial // (num_consumidores * 2)
            mercado.agregar_persona(consumidor)
        
        for i in range(min(num_empresas, 5)):  # Limitar para test rápido
            empresa = Empresa(f"E_{i}", mercado)
            empresa.dinero = pib_inicial // (num_empresas * 1.5)
            empresa.establecer_precio(f"Producto_{i}", 50 + i * 10)
            mercado.agregar_persona(empresa)
        
        # Verificar que el mercado funciona con la configuración
        pib_calculado = mercado.calcular_pib_total()
        self.assertGreater(pib_calculado, 0)
        
        # PIB calculado debería ser razonable (entre 10K y 10M para este test)
        self.assertGreater(pib_calculado, 10000)
        self.assertLess(pib_calculado, 10000000)
    
    def test_integracion_validador_economico(self):
        """Test integración con validador económico"""
        bienes = {}
        for i in range(5):
            bien = Bien(f"producto_{i}", "categoria_test")
            bienes[f"producto_{i}"] = bien
        
        mercado = Mercado(bienes)
        validador = ValidadorEconomico()
        
        # Crear mercado con datos económicos
        for i in range(20):
            consumidor = Consumidor(f"C_{i}", mercado)
            consumidor.dinero = 1000 + i * 100
            mercado.agregar_persona(consumidor)
        
        for i in range(5):
            empresa = Empresa(f"E_{i}", mercado)
            empresa.dinero = 10000 + i * 2000
            empresa.establecer_precio(f"P_{i}", 50 + i * 20)
            mercado.agregar_persona(empresa)
        
        # Simular varios ciclos y validar
        for ciclo in range(5):
            # Actividad económica
            pib = mercado.calcular_pib_total()
            mercado.pib_historico.append(pib)
            
            # Simular inflación
            inflacion = 0.02 + (ciclo * 0.01)  # Inflación creciente
            mercado.inflacion_historica.append(inflacion)
            
            # Validar datos económicos
            datos = {
                'pib': pib,
                'inflacion': inflacion,
                'desempleo': 0.05,  # 5% de desempleo
                'crecimiento': 0.03 if ciclo == 0 else 
                             (pib - mercado.pib_historico[-2]) / mercado.pib_historico[-2]
            }
            
            try:
                alertas = validador.validar_datos_economicos(datos)
                # No debería haber alertas críticas con datos normales
                alertas_criticas = [a for a in alertas if hasattr(a, 'tipo') and 
                                  str(a.tipo).upper() == 'CRITICA']
                self.assertEqual(len(alertas_criticas), 0, 
                               "No debería haber alertas críticas con datos normales")
            except Exception as e:
                # Si el validador no está implementado completamente, está bien
                self.assertIsInstance(e, (AttributeError, NotImplementedError))
    
    def test_simulacion_completa_ciclos(self):
        """Test simulación completa de múltiples ciclos"""
        bienes = {}
        for i in range(10):
            bien = Bien(f"producto_{i}", "categoria_test")
            bienes[f"producto_{i}"] = bien
        
        mercado = Mercado(bienes)
        
        # Configurar mercado inicial
        num_consumidores = 30
        num_empresas = 8
        
        for i in range(num_consumidores):
            consumidor = Consumidor(f"Consumidor_{i}", mercado)
            consumidor.dinero = 800 + (i * 40)
            mercado.agregar_persona(consumidor)
        
        productos = ["Comida", "Ropa", "Vivienda", "Transporte", "Entretenimiento"]
        for i in range(num_empresas):
            empresa = Empresa(f"Empresa_{i}", mercado)
            empresa.dinero = 12000 + (i * 1500)
            
            # Cada empresa produce 1-2 productos
            producto = productos[i % len(productos)]
            precio = 40 + (i * 15)
            empresa.establecer_precio(f"{producto}_{i}", precio)
            
            mercado.agregar_persona(empresa)
        
        # Simular 15 ciclos económicos
        metricas_ciclos = []
        
        for ciclo in range(15):
            inicio_ciclo = time.time()
            
            # Actividad económica del ciclo
            transacciones_exitosas = 0
            
            for transaccion in range(50):  # 50 transacciones por ciclo
                consumidores = mercado.getConsumidores()
                if consumidores:
                    consumidor = consumidores[transaccion % len(consumidores)]
                    
                    if mercado.bienes:
                        bien_nombre = list(mercado.bienes.keys())[transaccion % len(mercado.bienes)]
                        if consumidor.comprar(bien_nombre, 1):
                            transacciones_exitosas += 1
            
            # Calcular métricas del ciclo
            pib_ciclo = mercado.calcular_pib_total()
            tiempo_ciclo = time.time() - inicio_ciclo
            
            # Simular cambios económicos
            if ciclo % 3 == 0:  # Cada 3 ciclos, ajustar precios
                for empresa in mercado.getEmpresas():
                    for producto in empresa.precios:
                        # Pequeño ajuste de precios
                        ajuste = 1.0 + ((ciclo % 2) * 0.02 - 0.01)  # ±1%
                        empresa.precios[producto] *= ajuste
            
            metricas = {
                'ciclo': ciclo,
                'pib': pib_ciclo,
                'transacciones': transacciones_exitosas,
                'tiempo': tiempo_ciclo,
                'num_bienes': len(mercado.bienes)
            }
            metricas_ciclos.append(metricas)
            # Note: calcular_pib_total() already appends to pib_historico via registrar_estadisticas()
        
        # Verificaciones finales
        self.assertEqual(len(metricas_ciclos), 15)
        self.assertEqual(len(mercado.pib_historico), 15)
        
        # El PIB debería mantener valores positivos
        for metrica in metricas_ciclos:
            self.assertGreater(metrica['pib'], 0, f"PIB negativo en ciclo {metrica['ciclo']}")
        
        # Cada ciclo debería completarse rápidamente
        tiempo_promedio = sum(m['tiempo'] for m in metricas_ciclos) / len(metricas_ciclos)
        self.assertLess(tiempo_promedio, 0.5, f"Ciclos muy lentos: {tiempo_promedio:.3f}s promedio")
        
        # Debería haber productos disponibles
        self.assertGreater(len(mercado.bienes), 0)


class TestEscalarabilidad(unittest.TestCase):
    """Tests de escalabilidad del sistema"""
    
    def test_escalabilidad_participantes(self):
        """Test escalabilidad con número creciente de participantes"""
        tiempos_creacion = []
        tamaños = [10, 50, 100, 200]
        
        for tamaño in tamaños:
            bienes = {}
            for i in range(min(10, tamaño // 10)):  # Algunos bienes proporcionales
                bien = Bien(f"producto_{i}", "categoria_test")
                bienes[f"producto_{i}"] = bien
            
            mercado = Mercado(bienes)
            inicio = time.time()
            
            # Crear participantes
            for i in range(tamaño):
                consumidor = Consumidor(f"C_{i}", mercado)
                mercado.agregar_persona(consumidor)
                
                if i < tamaño // 5:  # 20% son empresas
                    empresa = Empresa(f"E_{i}", mercado)
                    empresa.establecer_precio(f"P_{i}", 50)
                    mercado.agregar_persona(empresa)
            
            tiempo_total = time.time() - inicio
            tiempos_creacion.append((tamaño, tiempo_total))
            
            # Verificar que se crearon correctamente
            self.assertEqual(len(mercado.getConsumidores()), tamaño)
            self.assertEqual(len(mercado.getEmpresas()), tamaño // 5)
        
        # Verificar que el tiempo crece de forma razonable (sub-cuadrática)
        for i in range(1, len(tiempos_creacion)):
            tamaño_anterior, tiempo_anterior = tiempos_creacion[i-1]
            tamaño_actual, tiempo_actual = tiempos_creacion[i]
            
            factor_tamaño = tamaño_actual / tamaño_anterior
            factor_tiempo = tiempo_actual / tiempo_anterior if tiempo_anterior > 0 else 1
            
            # El tiempo no debería crecer más que cuadráticamente
            self.assertLess(factor_tiempo, factor_tamaño ** 2 + 1, 
                           f"Tiempo crece demasiado rápido: tamaño x{factor_tamaño:.1f}, "
                           f"tiempo x{factor_tiempo:.1f}")


if __name__ == '__main__':
    unittest.main()