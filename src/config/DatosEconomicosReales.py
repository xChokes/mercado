"""
Datos Económicos Reales para Calibración del Simulador
Basado en datos del FMI, Banco Mundial, OCDE y bancos centrales principales
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple
import numpy as np

@dataclass
class IndicadoresEconomicosReales:
    """Indicadores económicos basados en promedios de economías desarrolladas (2020-2024)"""
    
    # INDICADORES MACROECONÓMICOS PRINCIPALES
    PIB_CRECIMIENTO_ANUAL = {
        'desarrolladas': (0.015, 0.035),    # 1.5% - 3.5% anual
        'emergentes': (0.035, 0.065),       # 3.5% - 6.5% anual
        'desarrolladas_crisis': (-0.08, -0.02),  # -8% a -2% en crisis
        'emergentes_crisis': (-0.12, -0.05)      # -12% a -5% en crisis
    }
    
    INFLACION = {
        'objetivo_central': 0.02,           # 2% objetivo mayoría bancos centrales
        'rango_normal': (0.005, 0.04),     # 0.5% - 4% rango normal
        'rango_crisis': (-0.02, 0.08),     # -2% a 8% en crisis
        'hiperinflacion': 0.50              # 50%+ considerado hiperinflación
    }
    
    DESEMPLEO = {
        'estructural': (0.035, 0.055),     # 3.5% - 5.5% desempleo estructural
        'normal': (0.04, 0.08),            # 4% - 8% en condiciones normales
        'crisis': (0.08, 0.15),            # 8% - 15% en crisis
        'depresion': (0.15, 0.25)          # 15%+ en depresión severa
    }
    
    # RANGOS de tasas de interés (conservar para calibraciones internas)
    TASAS_INTERES_RANGOS = {
        'politica_normal': (0.0, 0.06),    # 0% - 6% tasa de política monetaria
        'politica_crisis': (0.0, 0.001),   # Cerca de 0% en crisis (ZLB)
        'prestamos_comerciales': (0.03, 0.12),  # 3% - 12% préstamos comerciales
        'prestamos_consumo': (0.05, 0.25)       # 5% - 25% préstamos consumo
    }

    # Valores puntuales representativos (esperados como floats por los tests)
    TASAS_INTERES = {
        'politica_normal': 0.03,
        'politica_crisis': 0.001,
        'prestamos_comerciales': 0.08,
        'prestamos_consumo': 0.12,
    }

@dataclass
class ParametrosEconomicosCalibrados:
    """Parámetros calibrados para el simulador basados en literatura económica"""
    
    # PRODUCTIVIDAD LABORAL (basado en datos OCDE)
    PRODUCTIVIDAD = {
        'crecimiento_anual': (0.008, 0.025),    # 0.8% - 2.5% anual
        'volatilidad_ciclica': (0.95, 1.05),    # ±5% variación cíclica
        'factor_tecnologia': (1.0, 1.02),       # Progreso tecnológico gradual
        'factor_educacion': (0.98, 1.03)        # Impacto educación/skills
    }
    
    # ELASTICIDADES (basado en estudios econométricos)
    ELASTICIDADES = {
        'precio_demanda': {
            'necesidades_basicas': (-0.3, -0.1),    # Bienes inelásticos
            'bienes_normales': (-1.2, -0.5),        # Elasticidad normal
            'lujo': (-2.5, -1.2)                    # Bienes de lujo más elásticos
        },
        'ingreso_demanda': {
            'necesidades_basicas': (0.1, 0.4),      # Bienes inferiores/básicos
            'bienes_normales': (0.8, 1.2),          # Elasticidad unitaria aprox
            'lujo': (1.5, 3.0)                      # Bienes superiores
        }
    }
    
    # PARÁMETROS SECTOR FINANCIERO
    FINANCIERO = {
        'ratio_capital_activos': (0.08, 0.15),      # Capital/Activos bancarios
        'ratio_prestamos_depositos': (0.7, 0.9),    # Préstamos/Depósitos
        'provision_morosidad': (0.01, 0.05),        # Provisiones por morosidad
        'spread_bancario': (0.02, 0.06)             # Spread tasas activas-pasivas
    }
    
    # PARÁMETROS MERCADO LABORAL
    LABORAL = {
        'tasa_participacion': (0.60, 0.75),         # 60%-75% población activa
        'movilidad_laboral': (0.05, 0.15),          # 5%-15% cambio empleo/año
        'rigidez_salarios': (0.7, 0.9),             # Rigidez nominal salarios
        'productividad_sectorial': {
            'agricultura': (0.3, 0.5),
            'manufactura': (0.8, 1.2),
            'servicios': (0.6, 1.0),
            'tecnologia': (1.5, 2.5)
        }
    }

class CalibradorEconomicoRealista:
    """Calibrador que ajusta parámetros del simulador a rangos económicos realistas"""
    
    def __init__(self):
        self.indicadores = IndicadoresEconomicosReales()
        self.parametros = ParametrosEconomicosCalibrados()
        
    def calibrar_configuracion_base(self, config_actual: Dict) -> Dict:
        """Calibra la configuración base con parámetros realistas"""
        
        config_calibrada = config_actual.copy()
        
        # CALIBRACIÓN MACROECONÓMICA
        config_calibrada['economia'].update({
            'tasa_inflacion_objetivo': self.indicadores.INFLACION['objetivo_central'],
            'tasa_desempleo_inicial': np.random.uniform(*self.indicadores.DESEMPLEO['normal']),
            'crecimiento_pib_objetivo': np.random.uniform(*self.indicadores.PIB_CRECIMIENTO_ANUAL['desarrolladas']),
            'productividad_inicial': 1.0,  # Base normalizada
            'volatilidad_economica': 0.15   # 15% volatilidad base
        })
        
        # CALIBRACIÓN SISTEMA BANCARIO
        config_calibrada['sistema_bancario'].update({
            'tasa_interes_base': np.random.uniform(*self.indicadores.TASAS_INTERES_RANGOS['politica_normal']),
            'ratio_capital_minimo': np.random.uniform(*self.parametros.FINANCIERO['ratio_capital_activos']),
            'spread_bancario': np.random.uniform(*self.parametros.FINANCIERO['spread_bancario']),
            'provision_riesgo': np.random.uniform(*self.parametros.FINANCIERO['provision_morosidad'])
        })
        
        # CALIBRACIÓN MERCADO LABORAL
        config_calibrada['mercado_laboral'].update({
            'tasa_participacion': np.random.uniform(*self.parametros.LABORAL['tasa_participacion']),
            'movilidad_laboral': np.random.uniform(*self.parametros.LABORAL['movilidad_laboral']),
            'rigidez_salarios': np.random.uniform(*self.parametros.LABORAL['rigidez_salarios']),
            'productividad_sectorial': self.parametros.LABORAL['productividad_sectorial']
        })
        
        # CALIBRACIÓN PRECIOS Y ELASTICIDADES
        config_calibrada['precios'].update({
            'elasticidad_precio_base': np.random.uniform(*self.parametros.ELASTICIDADES['precio_demanda']['bienes_normales']),
            'elasticidad_ingreso_base': np.random.uniform(*self.parametros.ELASTICIDADES['ingreso_demanda']['bienes_normales']),
            'ajuste_maximo_por_ciclo': 0.05,  # Más conservador: 5% max
            'sensibilidad_realista': True
        })
        
        return config_calibrada
    
    def generar_rangos_validacion_estrictos(self) -> Dict:
        """Genera rangos de validación más estrictos basados en datos reales"""
        
        return {
            # INDICADORES PRINCIPALES (más estrictos y realistas)
            'pib_crecimiento': (-0.08, 0.065),     # Crisis a emergente fuerte
            'inflacion': (-0.02, 0.08),            # Deflación leve a inflación alta
            'desempleo': (0.035, 0.15),            # 3.5% (pleno empleo) a 15% (crisis)
            'tasa_interes': (0.0, 0.12),           # ZLB a emergencia
            
            # INDICADORES ESPECÍFICOS (calibrados ultra conservadores y estrictos)
            'productividad_laboral': (0.99, 1.01), # ±1% vs base (ULTRA estricto)
            'participacion_laboral': (0.62, 0.68), # Rangos OCDE ultra estrictos
            'ratio_capital_trabajo': (0.95, 1.05), # Intensidad capital ultra conservadora
            'velocidad_dinero': (1.5, 1.8),        # Velocidad circulación ultra conservadora
            
            # SECTORES ECONÓMICOS
            'crecimiento_sectorial': {
                'agricultura': (-0.05, 0.03),
                'manufactura': (-0.10, 0.08),
                'servicios': (-0.08, 0.06),
                'tecnologia': (-0.15, 0.15)        # Menos volátil
            },
            
            # FINANZAS
            'ratio_deuda_pib': (0.3, 1.2),         # 30%-120% deuda/PIB
            'ratio_credito_pib': (0.5, 2.0),       # 50%-200% crédito/PIB
            'spread_riesgo': (0.005, 0.10),        # 0.5%-10% spread riesgo (más conservador)
            
            # PRECIOS (más estrictos)
            'volatilidad_precios': (0.02, 0.15),   # 2%-15% volatilidad precios (menos extrema)
            'concentracion_mercado': (0.1, 0.7),   # Índice Herfindahl más competitivo
            'margen_beneficio': (0.02, 0.25)       # 2%-25% margen empresarial (más conservador)
        }
    
    def detectar_regimen_economico(self, indicadores: Dict) -> str:
        """Detecta el régimen económico actual basado en indicadores"""
        
        inflacion = indicadores.get('inflacion', 0)
        desempleo = indicadores.get('desempleo', 0.05)
        crecimiento = indicadores.get('crecimiento_pib', 0.02)
        
        # DEPRESIÓN ECONÓMICA
        if crecimiento < -0.05 and desempleo > 0.15:
            return "DEPRESION"
        
        # RECESIÓN SEVERA
        elif crecimiento < -0.02 and desempleo > 0.10:
            return "RECESION_SEVERA"
        
        # RECESIÓN LEVE
        elif crecimiento < 0 or desempleo > 0.08:
            return "RECESION_LEVE"
        
        # ESTANFLACIÓN (alta inflación + bajo crecimiento)
        elif inflacion > 0.06 and crecimiento < 0.015:
            return "ESTANFLACION"
        
        # SOBRECALENTAMIENTO (alta inflación + bajo desempleo)
        elif inflacion > 0.04 and desempleo < 0.04:
            return "SOBRECALENTAMIENTO"
        
        # CRECIMIENTO FUERTE
        elif crecimiento > 0.04 and desempleo < 0.06:
            return "CRECIMIENTO_FUERTE"
        
        # NORMAL
        else:
            return "NORMAL"
    
    def sugerir_politicas_por_regimen(self, regimen: str) -> Dict:
        """Sugiere políticas económicas apropiadas según el régimen detectado"""
        
        politicas = {
            "DEPRESION": {
                "politica_monetaria": "Expansiva máxima (tasas cerca 0%)",
                "politica_fiscal": "Estímulo fiscal masivo",
                "prioridades": ["Empleo", "Liquidez", "Estabilidad financiera"],
                "tasas_sugeridas": (0.0, 0.005)
            },
            
            "RECESION_SEVERA": {
                "politica_monetaria": "Expansiva fuerte",
                "politica_fiscal": "Estímulo fiscal significativo", 
                "prioridades": ["Empleo", "Demanda agregada", "Confianza"],
                "tasas_sugeridas": (0.0, 0.02)
            },
            
            "RECESION_LEVE": {
                "politica_monetaria": "Expansiva moderada",
                "politica_fiscal": "Estímulo fiscal selectivo",
                "prioridades": ["Crecimiento", "Empleo", "Competitividad"],
                "tasas_sugeridas": (0.01, 0.03)
            },
            
            "ESTANFLACION": {
                "politica_monetaria": "Restrictiva gradual",
                "politica_fiscal": "Consolidación fiscal prudente",
                "prioridades": ["Inflación", "Reformas estructurales", "Productividad"],
                "tasas_sugeridas": (0.03, 0.06)
            },
            
            "SOBRECALENTAMIENTO": {
                "politica_monetaria": "Restrictiva",
                "politica_fiscal": "Consolidación fiscal",
                "prioridades": ["Inflación", "Estabilidad financiera", "Sostenibilidad"],
                "tasas_sugeridas": (0.04, 0.08)
            },
            
            "CRECIMIENTO_FUERTE": {
                "politica_monetaria": "Neutral a ligeramente restrictiva",
                "politica_fiscal": "Disciplina fiscal",
                "prioridades": ["Estabilidad", "Innovación", "Sostenibilidad"],
                "tasas_sugeridas": (0.025, 0.05)
            },
            
            "NORMAL": {
                "politica_monetaria": "Neutral",
                "politica_fiscal": "Equilibrada",
                "prioridades": ["Estabilidad", "Crecimiento sostenible", "Bienestar"],
                "tasas_sugeridas": (0.02, 0.04)
            }
        }
        
        return politicas.get(regimen, politicas["NORMAL"])

# DATOS HISTÓRICOS PARA BENCHMARKING
BENCHMARKS_HISTORICOS = {
    "crisis_2008": {
        "duracion_meses": 18,
        "caida_pib": -0.056,        # -5.6% PIB
        "pico_desempleo": 0.10,     # 10% desempleo
        "inflacion_minima": -0.004,  # -0.4% deflación
        "tasas_minimas": 0.001      # Tasas cerca 0%
    },
    
    "covid_2020": {
        "duracion_meses": 12,
        "caida_pib": -0.032,        # -3.2% PIB (promedio OCDE)
        "pico_desempleo": 0.087,    # 8.7% desempleo
        "inflacion_maxima": 0.071,  # 7.1% inflación pico
        "recuperacion_meses": 24    # 24 meses recuperación completa
    },
    
    "expansion_2010_2020": {
        "duracion_meses": 120,
        "crecimiento_promedio": 0.024,  # 2.4% anual
        "desempleo_minimo": 0.035,      # 3.5% mínimo
        "inflacion_promedio": 0.015,     # 1.5% promedio
        "volatilidad_baja": True
    }
}
