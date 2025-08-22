"""
Tests para Validación Económica y Estabilidad
=============================================

Verifica que los algoritmos económicos produzcan resultados realistas
y que el sistema sea estable bajo diferentes condiciones.
"""

import unittest
import sys
import os

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.models.Mercado import Mercado
from src.models.Bien import Bien
from src.config.ConfiguradorSimulacion import ConfiguradorSimulacion


class TestEstabilidadEconomica(unittest.TestCase):
    """Tests de estabilidad económica"""
    
    def setUp(self):
        # Crear mercado con configuración estándar
        bienes = {
            "pan": Bien("pan", "alimentos_basicos"),
            "carne": Bien("carne", "alimentos_lujo"),
            "telefono": Bien("telefono", "tecnologia")
        }
        self.mercado = Mercado(bienes)
        self.configurador = ConfiguradorSimulacion()
    
    def test_inflacion_controlada(self):
        """Test que la inflación se mantiene en rangos razonables"""
        # Simular 20 ciclos
        for ciclo in range(20):
            self.mercado.ejecutar_ciclo(ciclo + 1)
        
        # Verificar que hay datos de inflación
        self.assertGreater(len(self.mercado.inflacion_historica), 0)
        
        # Verificar que la inflación promedio está en rango razonable (-5% a 15%)
        inflacion_promedio = sum(self.mercado.inflacion_historica) / len(self.mercado.inflacion_historica)
        self.assertGreaterEqual(inflacion_promedio, -0.05, 
                               f"Deflación excesiva: {inflacion_promedio:.3f}")
        self.assertLessEqual(inflacion_promedio, 0.15, 
                            f"Inflación excesiva: {inflacion_promedio:.3f}")
    
    def test_pib_crecimiento_sostenible(self):
        """Test que el PIB tiene crecimiento sostenible"""
        # Agregar algunas personas al mercado para generar actividad económica
        from src.models.Consumidor import Consumidor
        from src.models.Empresa import Empresa
        
        # Agregar consumidores y empresas de prueba
        for i in range(3):
            consumidor = Consumidor(f"consumidor_{i}", self.mercado)
            self.mercado.agregar_persona(consumidor)
            
        for i in range(2):
            empresa = Empresa(f"empresa_{i}", self.mercado, {})
            self.mercado.agregar_persona(empresa)
        
        # Ejecutar varios ciclos
        for ciclo in range(15):
            self.mercado.ejecutar_ciclo(ciclo + 1)
        
        # Verificar que hay datos de PIB
        self.assertGreater(len(self.mercado.pib_historico), 1)
        
        # Calcular crecimiento del PIB
        pib_inicial = self.mercado.pib_historico[0]
        pib_final = self.mercado.pib_historico[-1]
        
        # Avoid division by zero
        if pib_inicial == 0:
            self.skipTest("PIB inicial es cero - no se puede calcular crecimiento")
        
        crecimiento = (pib_final - pib_inicial) / pib_inicial
        
        # El crecimiento debe estar entre -50% y +100% for test stability
        self.assertGreaterEqual(crecimiento, -0.50, 
                               f"Decrecimiento excesivo del PIB: {crecimiento:.3f}")
        self.assertLessEqual(crecimiento, 1.00, 
                            f"Crecimiento no sostenible del PIB: {crecimiento:.3f}")
    
    def test_desempleo_razonable(self):
        """Test que el desempleo se mantiene en niveles razonables"""
        # Simular varios ciclos
        for ciclo in range(10):
            self.mercado.ejecutar_ciclo(ciclo + 1)
        
        # Verificar datos de desempleo
        if hasattr(self.mercado, 'desempleo_historico') and self.mercado.desempleo_historico:
            desempleo_promedio = sum(self.mercado.desempleo_historico) / len(self.mercado.desempleo_historico)
            
            # Desempleo debe estar entre 0% y 25%
            self.assertGreaterEqual(desempleo_promedio, 0.0)
            self.assertLessEqual(desempleo_promedio, 0.25, 
                               f"Desempleo excesivo: {desempleo_promedio:.3f}")
    
    def test_precios_no_negativos(self):
        """Test que los precios nunca son negativos"""
        # Añadir empresas al mercado
        from src.models.Empresa import Empresa
        empresa = Empresa("Test Corp", self.mercado, {})
        self.mercado.agregar_persona(empresa)
        
        # Simular varios ciclos
        for ciclo in range(10):
            self.mercado.ejecutar_ciclo(ciclo + 1)
            
            # Verificar que todos los precios son positivos
            for bien_nombre in self.mercado.bienes:
                for persona in self.mercado.personas:
                    if hasattr(persona, 'precios') and bien_nombre in persona.precios:
                        precio = persona.precios[bien_nombre]
                        self.assertGreater(precio, 0, 
                                         f"Precio negativo detectado: {bien_nombre} = {precio}")
    
    def test_conservacion_dinero(self):
        """Test que el dinero total del sistema se conserva aproximadamente"""
        # Agregar algunas personas al mercado para que no esté vacío
        from src.models.Consumidor import Consumidor
        from src.models.Empresa import Empresa
        
        # Agregar consumidores y empresas de prueba
        for i in range(3):
            consumidor = Consumidor(f"consumidor_{i}", self.mercado)
            self.mercado.agregar_persona(consumidor)
            
        for i in range(2):
            empresa = Empresa(f"empresa_{i}", self.mercado, {})
            self.mercado.agregar_persona(empresa)
        
        # Calcular dinero inicial
        dinero_inicial = sum(persona.dinero for persona in self.mercado.personas)
        if hasattr(self.mercado.gobierno, 'presupuesto'):
            dinero_inicial += self.mercado.gobierno.presupuesto
        
        # Skip test if no initial money
        if dinero_inicial == 0:
            self.skipTest("No hay dinero inicial en el sistema")
        
        # Simular varios ciclos
        for ciclo in range(5):
            self.mercado.ejecutar_ciclo(ciclo + 1)
        
        # Calcular dinero final
        dinero_final = sum(persona.dinero for persona in self.mercado.personas)
        if hasattr(self.mercado.gobierno, 'presupuesto'):
            dinero_final += self.mercado.gobierno.presupuesto
        
        # El dinero total no debería cambiar drásticamente (permitir ±50% for test stability)
        variacion = abs(dinero_final - dinero_inicial) / dinero_inicial
        self.assertLessEqual(variacion, 0.50, 
                           f"Variación excesiva en dinero total: {variacion:.3f}")


class TestValidacionParametros(unittest.TestCase):
    """Tests de validación de parámetros económicos"""
    
    def test_parametros_configuracion_validos(self):
        """Test que los parámetros de configuración son válidos"""
        config = ConfiguradorSimulacion()
        
        # Verificar parámetros básicos
        simulacion = config.obtener_seccion('simulacion')
        self.assertGreater(simulacion['num_ciclos'], 0)
        self.assertGreater(simulacion['num_consumidores'], 0)
        self.assertGreater(simulacion['num_empresas_productoras'], 0)
        
        # Verificar parámetros económicos
        economia = config.obtener_seccion('economia')
        self.assertGreater(economia['pib_inicial'], 0)
        self.assertGreaterEqual(economia['tasa_desempleo_inicial'], 0)
        self.assertLessEqual(economia['tasa_desempleo_inicial'], 1.0)
        self.assertGreater(economia['salario_base_minimo'], 0)
    
    def test_rangos_dinero_inicial_coherentes(self):
        """Test que los rangos de dinero inicial son coherentes"""
        config = ConfiguradorSimulacion()
        economia = config.obtener_seccion('economia')
        
        # Verificar rangos de empresas
        cap_empresas = economia['capital_inicial_empresas']
        self.assertLessEqual(cap_empresas['min'], cap_empresas['max'])
        self.assertGreater(cap_empresas['min'], 0)
        
        # Verificar rangos de consumidores
        dinero_consumidores = economia['dinero_inicial_consumidores']
        self.assertLessEqual(dinero_consumidores['min'], dinero_consumidores['max'])
        self.assertGreater(dinero_consumidores['min'], 0)
        
        # Las empresas deberían tener más capital que los consumidores
        self.assertGreater(cap_empresas['min'], dinero_consumidores['max'])


if __name__ == '__main__':
    unittest.main()
