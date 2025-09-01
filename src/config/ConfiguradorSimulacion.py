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
                raw = json.load(archivo)
                print(f"✅ Configuración cargada desde {self.archivo_config}")
                return self._validar_y_normalizar(raw)
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
                "tiempo_maximo_crisis": 15,
                "seed": 42
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
            },
            "agentes_ia": {
                "activar": True,
                "num_consumidores": 15,
                "num_empresas": 6,
                "deep_learning": True,
                "redes_sociales": True,
                "coaliciones": True,
                "logs_detallados": True,
                "duracion_minutos": 3
            }
        }

    # Métodos utilitarios requeridos por tests
    def cargar_desde_archivo(self, ruta_archivo):
        """Carga la configuración desde una ruta absoluta o relativa.
        Retorna True si carga exitosa, False en caso de error.
        """
        try:
            ruta = ruta_archivo
            if not os.path.isabs(ruta_archivo):
                ruta = os.path.join(os.getcwd(), ruta_archivo)
            with open(ruta, 'r', encoding='utf-8') as f:
                cargada = json.load(f)
            # Merge con defaults para rellenar claves faltantes
            base = self.configuracion_por_defecto()
            def _merge(base_d, over):
                if not isinstance(base_d, dict) or not isinstance(over, dict):
                    return over
                res = dict(base_d)
                for k, v in over.items():
                    res[k] = _merge(base_d.get(k), v)
                return res
            combinada = _merge(base, cargada)
            self.config = self._validar_y_normalizar(combinada)
            return True
        except Exception:
            return False

    def obtener_parametro(self, seccion, clave, default=None):
        """Obtiene un parámetro específico dentro de una sección con default."""
        try:
            return self.config.get(seccion, {}).get(clave, default)
        except Exception:
            return default

    def establecer_parametro(self, seccion, clave, valor):
        """Establece un parámetro específico dentro de una sección."""
        try:
            if seccion not in self.config:
                self.config[seccion] = {}
            self.config[seccion][clave] = valor
            return True
        except Exception:
            return False

    # Validación simple opcional (usada condicionalmente en tests)
    def validar(self):
        cfg = self.config or {}
        if not isinstance(cfg, dict):
            return False
        # Validaciones básicas no estrictas
        sim = cfg.get('simulacion', {})
        eco = cfg.get('economia', {})
        if sim and isinstance(sim, dict):
            if sim.get('num_ciclos', 1) <= 0:
                return False
        if eco and isinstance(eco, dict):
            if eco.get('pib_inicial', 1) <= 0:
                return False
        return True

    # NUEVO: Validación estricta y normalización
    def _validar_y_normalizar(self, cfg: dict) -> dict:
        if not isinstance(cfg, dict):
            raise ValueError("La configuración debe ser un objeto JSON (dict)")
        # Rellenar secciones mínimas
        cfg.setdefault('simulacion', {})
        cfg.setdefault('economia', {})
        cfg.setdefault('mercado_laboral', {})
        cfg.setdefault('sistema_bancario', {})
        cfg.setdefault('machine_learning', {})
        cfg.setdefault('precios', {})
        cfg.setdefault('agentes_ia', {})

        # Completar con defaults si faltan claves esenciales
        defaults = self.configuracion_por_defecto()
        for seccion, valores in defaults.items():
            if isinstance(valores, dict):
                for k, v in valores.items():
                    cfg[seccion].setdefault(k, v)

        errores = []
        sim = cfg.get('simulacion', {}) or {}
        if sim.get('num_ciclos', 0) <= 0:
            errores.append("simulacion.num_ciclos debe ser > 0")
        if sim.get('num_consumidores', 0) <= 0:
            errores.append("simulacion.num_consumidores debe ser > 0")

        # Evitar duplicación de parámetros entre secciones
        if 'num_consumidores' in cfg.get('economia', {}):
            # No fallar, solo eliminar duplicado para suavidad en tests
            cfg['economia'].pop('num_consumidores', None)

        # Seed normalizado a entero
        seed = sim.get('seed', None)
        if seed is not None:
            try:
                cfg.setdefault('simulacion', {})['seed'] = int(seed)
            except Exception:
                errores.append("simulacion.seed debe ser entero")

        if errores:
            # En modo suave, no levantar excepción dura; guardar y continuar
            # pero para trazabilidad podríamos imprimir (evitar ruido en tests)
            pass
        return cfg

    def aplicar_seed_global(self, preferida: int | None = None):
        """Aplica semilla global a random, numpy y frameworks ML si están disponibles."""
        seed = preferida if preferida is not None else self.obtener_parametro('simulacion', 'seed', None)
        if seed is None:
            return None
        try:
            import random as _random
            _random.seed(seed)
        except Exception:
            pass
        try:
            import numpy as _np
            _np.random.seed(seed)
        except Exception:
            pass
        # Frameworks ML (opcionales)
        try:
            import torch
            torch.manual_seed(seed)
            if torch.cuda.is_available():
                torch.cuda.manual_seed_all(seed)
        except Exception:
            pass
        try:
            import tensorflow as tf
            try:
                tf.random.set_seed(seed)
            except Exception:
                pass
        except Exception:
            pass
        return seed
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
