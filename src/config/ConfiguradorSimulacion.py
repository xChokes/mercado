"""
Cargador de configuración para el simulador económico
Permite cargar parámetros desde archivo JSON externo
"""

import json
import os


class ConfiguradorSimulacion:
    """Maneja la configuración de la simulación desde archivo externo"""

    def __init__(self, archivo_config='config_simulacion.json'):
        self.archivo_config = archivo_config
        self.config = self.cargar_configuracion()

    def cargar_configuracion(self):
        """Carga configuración desde archivo JSON"""
        ruta_config = os.path.join(os.path.dirname(
            __file__), '..', '..', self.archivo_config)

        try:
            with open(ruta_config, 'r', encoding='utf-8') as archivo:
                config = json.load(archivo)
                print(f"✅ Configuración cargada desde {self.archivo_config}")
                return config
        except FileNotFoundError:
            print(
                f"⚠️  Archivo de configuración {self.archivo_config} no encontrado. Usando valores por defecto.")
            return self.configuracion_por_defecto()
        except json.JSONDecodeError as e:
            print(
                f"⚠️  Error leyendo configuración: {e}. Usando valores por defecto.")
            return self.configuracion_por_defecto()

    def configuracion_por_defecto(self):
        """Configuración por defecto si no se puede cargar el archivo"""
        return {
            "simulacion": {
                "num_ciclos": 50,
                "num_consumidores": 250,
                "num_empresas_productoras": 5,
                "num_empresas_comerciales": 8,
                "frecuencia_reportes": 5,
                "activar_crisis": True,
                "tiempo_maximo_crisis": 15
            },
            "economia": {
                "pib_inicial": 100000,
                "tasa_desempleo_inicial": 0.15,
                "tasa_inflacion_objetivo": 0.02,
                "salario_base_minimo": 2000,
                "capital_inicial_empresas": {
                    "min": 100000,
                    "max": 1500000
                },
                "dinero_inicial_consumidores": {
                    "min": 5000,
                    "max": 15000
                }
            },
            "mercado_laboral": {
                "probabilidad_contratacion_base": 0.5,
                "habilidad_minima_base": 0.1,
                "capacidad_empleo_factor": 1.2,
                "subsidio_contratacion_crisis": 0.2
            },
            "sistema_bancario": {
                "activar": True,
                "num_bancos": 3,
                "capital_inicial_bancos": 3000000,
                "tasa_interes_base": 0.05,
                "ratio_prestamo_ingreso": 5.0
            },
            "machine_learning": {
                "activar": True,
                "generar_datos_sinteticos": True,
                "num_datos_sinteticos": 20,
                "reentrenar_cada_ciclos": 10
            },
            "precios": {
                "ajuste_maximo_por_ciclo": 0.15,
                "margen_minimo": 0.05,
                "margen_maximo": 3.0,
                "sensibilidad_competencia": 0.1,
                "sensibilidad_stock": 0.15
            }
        }

    def obtener(self, seccion, clave, valor_por_defecto=None):
        """Obtiene un valor de configuración específico"""
        try:
            return self.config[seccion][clave]
        except KeyError:
            return valor_por_defecto

    def obtener_seccion(self, seccion):
        """Obtiene una sección completa de configuración"""
        return self.config.get(seccion, {})

    def actualizar_configuracion_economica(self, config_economica):
        """Actualiza ConfigEconomica con valores del archivo"""
        economia = self.obtener_seccion('economia')
        mercado_laboral = self.obtener_seccion('mercado_laboral')

        # Actualizar valores si están disponibles
        if 'salario_base_minimo' in economia:
            config_economica.SALARIO_BASE_MIN = economia['salario_base_minimo']

        if 'tasa_inflacion_objetivo' in economia:
            config_economica.TASA_INFLACION_OBJETIVO = economia['tasa_inflacion_objetivo']

        if 'tasa_desempleo_inicial' in economia:
            config_economica.TASA_DESEMPLEO_OBJETIVO = economia['tasa_desempleo_inicial']

        print(f"✅ ConfigEconomica actualizada con parámetros externos")


# Instancia global para uso en toda la aplicación
configurador = ConfiguradorSimulacion()
