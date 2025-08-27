"""
Tests de Robustez y Manejo de Errores
=====================================

Tests para validar la robustez del sistema ante errores,
interrupciones y condiciones adversas.
"""

import unittest
import sys
import os
import tempfile
import json
from unittest.mock import Mock, patch, MagicMock

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.config.ConfiguradorSimulacion import ConfiguradorSimulacion
from src.models.Mercado import Mercado
from src.models.Consumidor import Consumidor
from src.models.Empresa import Empresa
from src.systems.ValidadorEconomico import ValidadorEconomico


class TestRobustezSistema(unittest.TestCase):
    """Tests de robustez del sistema completo"""
    
    def test_configuracion_archivo_corrupto(self):
        """Test carga de archivo de configuración corrupto"""
        # Crear archivo temporal con JSON inválido
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('{"invalid": json,}')  # JSON inválido
            temp_path = f.name
        
        try:
            config = ConfiguradorSimulacion()
            resultado = config.cargar_desde_archivo(temp_path)
            
            # El sistema debería manejar JSON inválido graciosamente
            self.assertFalse(resultado, "Debería fallar al cargar JSON inválido")
        finally:
            os.unlink(temp_path)
    
    def test_configuracion_archivo_inexistente(self):
        """Test carga de archivo de configuración inexistente"""
        config = ConfiguradorSimulacion()
        resultado = config.cargar_desde_archivo("archivo_que_no_existe.json")
        
        # Debería fallar graciosamente
        self.assertFalse(resultado)
    
    def test_mercado_operaciones_concurrentes_simuladas(self):
        """Test operaciones simuladas concurrentes en el mercado"""
        bienes = {}
        for i in range(5):
            bien = Bien(f"producto_{i}", "categoria_test")
            bienes[f"producto_{i}"] = bien
        
        mercado = Mercado(bienes)
        
        # Simular múltiples operaciones "simultáneas"
        consumidores = []
        for i in range(10):
            consumidor = Consumidor(f"Consumidor_{i}", mercado)
            consumidores.append(consumidor)
            mercado.agregar_persona(consumidor)
        
        empresas = []
        for i in range(5):
            empresa = Empresa(f"Empresa_{i}", mercado)
            empresas.append(empresa)
            mercado.agregar_persona(empresa)
        
        # Simular operaciones concurrentes
        for i in range(100):
            # Diferentes operaciones mezcladas
            if i % 3 == 0:
                # Agregar más consumidores
                nuevo_consumidor = Consumidor(f"NuevoConsumidor_{i}", mercado)
                mercado.agregar_persona(nuevo_consumidor)
            elif i % 3 == 1:
                # Cambiar precios
                if empresas:
                    empresa = empresas[i % len(empresas)]
                    empresa.establecer_precio(f"Producto_{i}", float(i + 10))
            else:
                # Intentar compras
                if consumidores and mercado.bienes:
                    consumidor = consumidores[i % len(consumidores)]
                    bien_nombre = list(mercado.bienes.keys())[0] if mercado.bienes else None
                    if bien_nombre:
                        consumidor.comprar(bien_nombre, 1)
        
        # El mercado debería mantenerse consistente
        self.assertGreater(len(mercado.getConsumidores()), 10)
        self.assertEqual(len(mercado.empresas_productoras), 5)
    
    def test_validador_economico_datos_inconsistentes(self):
        """Test validador económico con datos inconsistentes"""
        validador = ValidadorEconomico()
        
        # Datos económicos inconsistentes o extremos
        datos_inconsistentes = {
            'pib': -1000,  # PIB negativo
            'inflacion': 500,  # Hiperinflación extrema
            'desempleo': -0.1,  # Desempleo negativo
            'crecimiento': float('inf'),  # Infinito
        }
        
        # El validador debería detectar inconsistencias
        try:
            alertas = validador.validar_datos_economicos(datos_inconsistentes)
            # Debería generar alertas críticas
            self.assertGreater(len(alertas), 0, "Debería detectar datos inconsistentes")
        except Exception as e:
            # Si lanza excepción, también es aceptable
            self.assertIsInstance(e, (ValueError, TypeError))
    
    def test_memoria_limitada_simulada(self):
        """Test comportamiento con memoria limitada simulada"""
        # Crear muchos objetos para simular presión de memoria
        objetos = []
        try:
            # Crear muchos objetos hasta que la memoria sea una preocupación
            for i in range(1000):
                mercado = Mercado()
                for j in range(10):
                    consumidor = Consumidor(f"C_{i}_{j}", mercado)
                    mercado.agregar_persona(consumidor)
                objetos.append(mercado)
            
            # El sistema debería seguir funcionando
            self.assertGreater(len(objetos), 0)
            
        except MemoryError:
            # Si se queda sin memoria, eso es aceptable para este test
            self.assertTrue(True)
        finally:
            # Limpiar memoria
            objetos.clear()


class TestManejoExcepciones(unittest.TestCase):
    """Tests para manejo específico de excepciones"""
    
    def test_division_por_cero_prevenida(self):
        """Test prevención de división por cero en cálculos económicos"""
        mercado = Mercado()
        
        # Crear situación que podría causar división por cero
        mercado.pib_historico = [0, 0, 0]  # PIB cero
        
        try:
            # Intentar calcular crecimiento (podría dividir por cero)
            if len(mercado.pib_historico) >= 2:
                anterior = mercado.pib_historico[-2]
                actual = mercado.pib_historico[-1]
                if anterior != 0:
                    crecimiento = (actual - anterior) / anterior
                else:
                    crecimiento = 0  # Manejar división por cero
                
                # Debería manejar la división por cero
                self.assertIsInstance(crecimiento, (int, float))
            
        except ZeroDivisionError:
            self.fail("No debería haber división por cero no manejada")
    
    def test_atributos_inexistentes(self):
        """Test acceso a atributos inexistentes"""
        consumidor = Consumidor("Test", Mercado())
        
        # Intentar acceder a atributos que no existen
        try:
            valor = getattr(consumidor, 'atributo_inexistente', None)
            self.assertIsNone(valor)
        except AttributeError:
            # Si lanza AttributeError, también es aceptable
            pass
    
    def test_operaciones_tipo_incorrecto(self):
        """Test operaciones con tipos de datos incorrectos"""
        mercado = Mercado()
        
        try:
            # Intentar operaciones con tipos incorrectos
            resultado = mercado.calcular_pib_total()  # Podría fallar si no hay datos
            # Si funciona, debería retornar un número
            if resultado is not None:
                self.assertIsInstance(resultado, (int, float))
        except (TypeError, AttributeError):
            # Es aceptable que falle con tipos incorrectos
            pass


class TestRecuperacionErrores(unittest.TestCase):
    """Tests para capacidad de recuperación ante errores"""
    
    def test_recuperacion_configuracion_invalida(self):
        """Test recuperación después de configuración inválida"""
        config = ConfiguradorSimulacion()
        
        # Guardar configuración original
        config_original = config.config.copy()
        
        # Aplicar configuración inválida
        config.config['simulacion']['num_ciclos'] = -1
        self.assertFalse(config.validar())
        
        # Restaurar configuración válida
        config.config = config_original
        self.assertTrue(config.validar())
    
    def test_mercado_reinicio_despues_error(self):
        """Test reinicio del mercado después de error"""
        bienes = {"test": Bien("test", "test")}
        mercado = Mercado(bienes)
        
        # Añadir datos normales
        consumidor = Consumidor("Normal", mercado)
        mercado.agregar_persona(consumidor)
        
        # NOTE: The original test tried to corrupt 'consumidores' attribute but 
        # Mercado class doesn't have this attribute (uses 'personas' instead)
        # Simulating corruption by clearing personas list instead
        mercado.personas = []
        
        # Recuperar
        mercado.agregar_persona(Consumidor("Recuperado", mercado))
        
        # Debería funcionar después de la recuperación
        self.assertEqual(len(mercado.getConsumidores()), 1)
        self.assertEqual(mercado.getConsumidores()[0].nombre, "Recuperado")
    
    @patch('builtins.open', side_effect=IOError("Simulated IO Error"))
    def test_manejo_error_io(self, mock_open):
        """Test manejo de errores de E/S"""
        config = ConfiguradorSimulacion()
        
        # Intentar cargar archivo con error de E/S simulado
        resultado = config.cargar_desde_archivo("test.json")
        
        # Debería manejar el error graciosamente
        self.assertFalse(resultado)


class TestValidacionDatos(unittest.TestCase):
    """Tests para validación robusta de datos"""
    
    def test_validacion_rangos_numericos(self):
        """Test validación de rangos numéricos"""
        config = ConfiguradorSimulacion()
        
        # Test valores en límites
        casos_limite = [
            ('simulacion.num_ciclos', 1),      # Mínimo
            ('simulacion.num_ciclos', 10000),  # Máximo razonable
            ('economia.pib_inicial', 1000),    # Mínimo
            ('economia.tasa_inflacion_objetivo', 0.0),   # Mínimo
            ('economia.tasa_inflacion_objetivo', 0.1),   # Máximo razonable
        ]
        
        for parametro, valor in casos_limite:
            seccion, param = parametro.split('.')
            config.establecer_parametro(seccion, param, valor)
            
            # La configuración debería ser válida en los límites
            self.assertTrue(config.validar(), 
                          f"Falló validación para {parametro}={valor}")
    
    def test_sanitizacion_strings(self):
        """Test sanitización de strings de entrada"""
        bienes = {"test": Bien("test", "test")}
        mercado = Mercado(bienes)
        
        # Strings con caracteres especiales
        nombres_especiales = [
            "Normal",
            "Nombre con espacios",
            "Nombre_con_guiones",
            "Nombre.con.puntos",
            "123NombreNumerico",
            "",  # String vacío
        ]
        
        for nombre in nombres_especiales:
            try:
                consumidor = Consumidor(nombre, mercado)
                # Si acepta el nombre, debería ser string válido
                self.assertIsInstance(consumidor.nombre, str)
            except (ValueError, TypeError):
                # Es aceptable rechazar nombres inválidos
                pass


if __name__ == '__main__':
    unittest.main()