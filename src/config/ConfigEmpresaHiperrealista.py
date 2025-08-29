"""
Configuración Avanzada para Empresas Hiperrealistas
=================================================

Este archivo permite personalizar el comportamiento de las empresas hiperrealistas
ajustando parámetros específicos según las necesidades de simulación.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
import json

@dataclass
class ConfigRRHH:
    """Configuración para gestión de recursos humanos"""
    salario_base_minimo: float = 2500
    salario_base_maximo: float = 8000
    factor_bonificacion_max: float = 0.3
    
    # Capacitación
    presupuesto_capacitacion_pct: float = 0.02  # 2% de ingresos
    horas_capacitacion_mes: int = 8
    
    # Rotación y satisfacción
    factor_rotacion_base: float = 0.05  # 5% mensual
    satisfaccion_minima_critica: float = 30
    
    # Promociones
    antiguedad_minima_promocion: int = 12  # meses
    factor_promocion_salario: float = 0.15

@dataclass
class ConfigInnovacion:
    """Configuración para gestión de innovación y desarrollo"""
    presupuesto_id_pct_min: float = 0.03  # 3% mínimo
    presupuesto_id_pct_max: float = 0.12  # 12% máximo (empresas tech)
    
    # Tipos de proyectos
    probabilidad_proyecto_producto: float = 0.4
    probabilidad_proyecto_proceso: float = 0.3
    probabilidad_proyecto_investigacion: float = 0.2
    probabilidad_proyecto_tecnologia: float = 0.1
    
    # Duración proyectos (meses)
    duracion_min: int = 3
    duracion_max: int = 18
    
    # Éxito de proyectos
    tasa_exito_base: float = 0.65
    factor_experiencia: float = 0.1

@dataclass
class ConfigRiesgos:
    """Configuración para gestión de riesgos"""
    evaluacion_frecuencia_meses: int = 3
    limite_riesgo_critico: float = 80
    
    # Tipos de riesgo y probabilidades base
    probabilidades_riesgo: Dict[str, float] = None
    
    def __post_init__(self):
        if self.probabilidades_riesgo is None:
            self.probabilidades_riesgo = {
                'liquidez': 0.15,
                'mercado': 0.25,
                'operacional': 0.20,
                'regulatorio': 0.10,
                'reputacional': 0.12,
                'tecnologico': 0.18
            }

@dataclass
class ConfigResponsabilidadSocial:
    """Configuración para responsabilidad social corporativa"""
    presupuesto_rsc_pct: float = 0.01  # 1% de ingresos
    
    # Programas disponibles
    programas_disponibles: List[str] = None
    
    # Impacto en reputación
    factor_reputacion_programa: float = 5.0
    
    def __post_init__(self):
        if self.programas_disponibles is None:
            self.programas_disponibles = [
                'medio_ambiente',
                'educacion_comunitaria',
                'desarrollo_local',
                'inclusion_laboral',
                'voluntariado_corporativo',
                'donaciones_ong'
            ]

@dataclass
class ConfigCompetencia:
    """Configuración para análisis de competencia"""
    frecuencia_analisis_meses: int = 2
    num_competidores_seguimiento: int = 5
    
    # Factores de competitividad
    peso_precio: float = 0.25
    peso_calidad: float = 0.25
    peso_innovacion: float = 0.20
    peso_market_share: float = 0.15
    peso_eficiencia: float = 0.15

@dataclass
class ConfigProblemasEmpresariales:
    """Configuración para generación de problemas empresariales"""
    frecuencia_evaluacion: int = 2  # cada 2 ciclos
    
    # Probabilidades base por tipo de problema
    probabilidades_problemas: Dict[str, float] = None
    
    # Factores de severidad
    factor_severidad_capital: float = 0.3
    factor_severidad_sector: float = 0.2
    factor_severidad_tamaño: float = 0.25
    
    def __post_init__(self):
        if self.probabilidades_problemas is None:
            self.probabilidades_problemas = {
                'cadena_suministro': 0.20,
                'personal': 0.25,
                'regulatorio': 0.15,
                'tecnologia': 0.20,
                'liquidez': 0.10,
                'calidad': 0.15,
                'competencia': 0.18,
                'operacional': 0.22
            }

@dataclass
class ConfigCrisisEmpresarial:
    """Configuración para gestión de crisis empresariales"""
    umbral_crisis_liquidez_meses: float = 2.0
    umbral_crisis_perdidas_pct: float = 0.15  # 15% de capital
    
    # Costos de resolución de crisis (como % del capital)
    costos_resolucion_crisis: Dict[str, float] = None
    
    # Efectividad de medidas anti-crisis
    efectividad_reestructuracion: float = 0.7
    efectividad_recorte_costos: float = 0.6
    efectividad_nueva_estrategia: float = 0.5
    
    def __post_init__(self):
        if self.costos_resolucion_crisis is None:
            self.costos_resolucion_crisis = {
                'financiera': 0.08,
                'operacional': 0.05,
                'reputacional': 0.03,
                'mercado': 0.06
            }

@dataclass
class ConfigEmpresaHiperrealista:
    """Configuración principal para empresas hiperrealistas"""
    
    # Sub-configuraciones
    rrhh: ConfigRRHH = None
    innovacion: ConfigInnovacion = None
    riesgos: ConfigRiesgos = None
    responsabilidad_social: ConfigResponsabilidadSocial = None
    competencia: ConfigCompetencia = None
    problemas: ConfigProblemasEmpresariales = None
    crisis: ConfigCrisisEmpresarial = None
    
    # Configuración general
    ciclos_plan_estrategico: int = 6  # Revisar plan cada 6 ciclos
    umbral_performance_critica: float = 30
    umbral_performance_excelente: float = 85
    
    # Configuración financiera
    factor_crecimiento_organico: float = 0.05  # 5% mensual máximo
    limite_endeudamiento_pct: float = 0.4  # 40% del capital
    
    # Configuración operacional
    factor_eficiencia_base: float = 0.75
    capacidad_produccion_base: int = 1000
    
    def __post_init__(self):
        if self.rrhh is None:
            self.rrhh = ConfigRRHH()
        if self.innovacion is None:
            self.innovacion = ConfigInnovacion()
        if self.riesgos is None:
            self.riesgos = ConfigRiesgos()
        if self.responsabilidad_social is None:
            self.responsabilidad_social = ConfigResponsabilidadSocial()
        if self.competencia is None:
            self.competencia = ConfigCompetencia()
        if self.problemas is None:
            self.problemas = ConfigProblemasEmpresariales()
        if self.crisis is None:
            self.crisis = ConfigCrisisEmpresarial()
    
    def guardar_configuracion(self, archivo: str = "config_empresa_hiperrealista.json"):
        """Guarda la configuración en un archivo JSON"""
        config_dict = {
            'rrhh': {
                'salario_base_minimo': self.rrhh.salario_base_minimo,
                'salario_base_maximo': self.rrhh.salario_base_maximo,
                'factor_bonificacion_max': self.rrhh.factor_bonificacion_max,
                'presupuesto_capacitacion_pct': self.rrhh.presupuesto_capacitacion_pct,
                'factor_rotacion_base': self.rrhh.factor_rotacion_base,
                'satisfaccion_minima_critica': self.rrhh.satisfaccion_minima_critica
            },
            'innovacion': {
                'presupuesto_id_pct_min': self.innovacion.presupuesto_id_pct_min,
                'presupuesto_id_pct_max': self.innovacion.presupuesto_id_pct_max,
                'tasa_exito_base': self.innovacion.tasa_exito_base,
                'duracion_min': self.innovacion.duracion_min,
                'duracion_max': self.innovacion.duracion_max
            },
            'riesgos': {
                'evaluacion_frecuencia_meses': self.riesgos.evaluacion_frecuencia_meses,
                'limite_riesgo_critico': self.riesgos.limite_riesgo_critico,
                'probabilidades_riesgo': self.riesgos.probabilidades_riesgo
            },
            'responsabilidad_social': {
                'presupuesto_rsc_pct': self.responsabilidad_social.presupuesto_rsc_pct,
                'factor_reputacion_programa': self.responsabilidad_social.factor_reputacion_programa,
                'programas_disponibles': self.responsabilidad_social.programas_disponibles
            },
            'problemas': {
                'frecuencia_evaluacion': self.problemas.frecuencia_evaluacion,
                'probabilidades_problemas': self.problemas.probabilidades_problemas
            },
            'general': {
                'ciclos_plan_estrategico': self.ciclos_plan_estrategico,
                'umbral_performance_critica': self.umbral_performance_critica,
                'umbral_performance_excelente': self.umbral_performance_excelente,
                'factor_crecimiento_organico': self.factor_crecimiento_organico
            }
        }
        
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(config_dict, f, indent=2, ensure_ascii=False)
        
        return f"Configuración guardada en {archivo}"
    
    @classmethod
    def cargar_configuracion(cls, archivo: str = "config_empresa_hiperrealista.json"):
        """Carga configuración desde un archivo JSON"""
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                config_dict = json.load(f)
            
            # Crear sub-configuraciones
            config_rrhh = ConfigRRHH(**config_dict.get('rrhh', {}))
            config_innovacion = ConfigInnovacion(**config_dict.get('innovacion', {}))
            config_riesgos = ConfigRiesgos(**config_dict.get('riesgos', {}))
            config_rsc = ConfigResponsabilidadSocial(**config_dict.get('responsabilidad_social', {}))
            config_competencia = ConfigCompetencia(**config_dict.get('competencia', {}))
            config_problemas = ConfigProblemasEmpresariales(**config_dict.get('problemas', {}))
            config_crisis = ConfigCrisisEmpresarial(**config_dict.get('crisis', {}))
            
            # Crear configuración principal
            config_general = config_dict.get('general', {})
            return cls(
                rrhh=config_rrhh,
                innovacion=config_innovacion,
                riesgos=config_riesgos,
                responsabilidad_social=config_rsc,
                competencia=config_competencia,
                problemas=config_problemas,
                crisis=config_crisis,
                **config_general
            )
        
        except FileNotFoundError:
            print(f"Archivo {archivo} no encontrado. Usando configuración por defecto.")
            return cls()
        except Exception as e:
            print(f"Error cargando configuración: {e}. Usando configuración por defecto.")
            return cls()

# Configuraciones predefinidas para diferentes tipos de empresas

class ConfiguracionesPredefinidas:
    """Configuraciones predefinidas para diferentes tipos de empresas"""
    
    @staticmethod
    def empresa_tecnologia():
        """Configuración optimizada para empresas de tecnología"""
        config = ConfigEmpresaHiperrealista()
        
        # Mayor inversión en I+D
        config.innovacion.presupuesto_id_pct_min = 0.08
        config.innovacion.presupuesto_id_pct_max = 0.20
        config.innovacion.tasa_exito_base = 0.70
        
        # Salarios más altos para retener talento
        config.rrhh.salario_base_minimo = 4000
        config.rrhh.salario_base_maximo = 12000
        config.rrhh.factor_bonificacion_max = 0.5
        
        # Mayor inversión en capacitación
        config.rrhh.presupuesto_capacitacion_pct = 0.04
        
        # Riesgos específicos del sector
        config.riesgos.probabilidades_riesgo['tecnologico'] = 0.30
        config.riesgos.probabilidades_riesgo['mercado'] = 0.35
        
        return config
    
    @staticmethod
    def empresa_tradicional():
        """Configuración para empresas de sectores tradicionales"""
        config = ConfigEmpresaHiperrealista()
        
        # Menor inversión en I+D
        config.innovacion.presupuesto_id_pct_min = 0.01
        config.innovacion.presupuesto_id_pct_max = 0.05
        
        # Enfoque en eficiencia operacional
        config.factor_eficiencia_base = 0.85
        
        # Riesgos operacionales más altos
        config.riesgos.probabilidades_riesgo['operacional'] = 0.30
        config.riesgos.probabilidades_riesgo['regulatorio'] = 0.20
        
        return config
    
    @staticmethod
    def empresa_startup():
        """Configuración para startups"""
        config = ConfigEmpresaHiperrealista()
        
        # Alta inversión en I+D pero con mayor riesgo
        config.innovacion.presupuesto_id_pct_min = 0.10
        config.innovacion.presupuesto_id_pct_max = 0.25
        config.innovacion.tasa_exito_base = 0.45  # Menor tasa de éxito
        
        # Salarios variables con equity
        config.rrhh.factor_bonificacion_max = 0.8
        
        # Mayores riesgos financieros
        config.riesgos.probabilidades_riesgo['liquidez'] = 0.35
        config.crisis.umbral_crisis_liquidez_meses = 1.0
        
        # Menor inversión en RSC inicialmente
        config.responsabilidad_social.presupuesto_rsc_pct = 0.005
        
        return config
    
    @staticmethod
    def empresa_multinacional():
        """Configuración para grandes multinacionales"""
        config = ConfigEmpresaHiperrealista()
        
        # Inversión balanceada en I+D
        config.innovacion.presupuesto_id_pct_min = 0.04
        config.innovacion.presupuesto_id_pct_max = 0.10
        
        # Mayor inversión en RSC
        config.responsabilidad_social.presupuesto_rsc_pct = 0.02
        
        # Análisis de competencia más frecuente
        config.competencia.frecuencia_analisis_meses = 1
        config.competencia.num_competidores_seguimiento = 10
        
        # Gestión de riesgos más sofisticada
        config.riesgos.evaluacion_frecuencia_meses = 1
        
        return config

# Función de utilidad para crear configuraciones personalizadas

def crear_configuracion_personalizada(
    sector: str = "general",
    tamaño: str = "mediana",
    enfoque_innovacion: str = "moderado",
    sensibilidad_riesgo: str = "media"
) -> ConfigEmpresaHiperrealista:
    """
    Crea una configuración personalizada basada en parámetros específicos
    
    Args:
        sector: "tecnologia", "tradicional", "servicios", "manufactura"
        tamaño: "startup", "pequeña", "mediana", "grande", "multinacional"
        enfoque_innovacion: "bajo", "moderado", "alto", "disruptivo"
        sensibilidad_riesgo: "baja", "media", "alta"
    """
    
    config = ConfigEmpresaHiperrealista()
    
    # Ajustar según sector
    if sector == "tecnologia":
        config.innovacion.presupuesto_id_pct_min = 0.08
        config.innovacion.presupuesto_id_pct_max = 0.15
        config.rrhh.salario_base_minimo = 4000
        
    elif sector == "tradicional":
        config.innovacion.presupuesto_id_pct_min = 0.01
        config.innovacion.presupuesto_id_pct_max = 0.04
        config.rrhh.salario_base_minimo = 2000
        
    # Ajustar según tamaño
    if tamaño == "startup":
        config.crisis.umbral_crisis_liquidez_meses = 1.0
        config.riesgos.probabilidades_riesgo['liquidez'] = 0.30
        
    elif tamaño == "multinacional":
        config.responsabilidad_social.presupuesto_rsc_pct = 0.025
        config.competencia.num_competidores_seguimiento = 15
    
    # Ajustar según enfoque de innovación
    if enfoque_innovacion == "alto":
        config.innovacion.presupuesto_id_pct_min *= 1.5
        config.innovacion.presupuesto_id_pct_max *= 1.3
        
    elif enfoque_innovacion == "bajo":
        config.innovacion.presupuesto_id_pct_min *= 0.5
        config.innovacion.presupuesto_id_pct_max *= 0.7
    
    # Ajustar según sensibilidad al riesgo
    if sensibilidad_riesgo == "alta":
        config.riesgos.evaluacion_frecuencia_meses = 1
        config.riesgos.limite_riesgo_critico = 60
        
    elif sensibilidad_riesgo == "baja":
        config.riesgos.evaluacion_frecuencia_meses = 6
        config.riesgos.limite_riesgo_critico = 90
    
    return config

# Ejemplo de uso
if __name__ == "__main__":
    # Crear configuración por defecto
    config_default = ConfigEmpresaHiperrealista()
    print("✅ Configuración por defecto creada")
    
    # Guardar configuración
    mensaje = config_default.guardar_configuracion()
    print(f"✅ {mensaje}")
    
    # Crear configuraciones específicas
    config_tech = ConfiguracionesPredefinidas.empresa_tecnologia()
    config_tech.guardar_configuracion("config_empresa_tecnologia.json")
    print("✅ Configuración de empresa tecnológica guardada")
    
    config_startup = ConfiguracionesPredefinidas.empresa_startup()
    config_startup.guardar_configuracion("config_empresa_startup.json")
    print("✅ Configuración de startup guardada")
    
    # Crear configuración personalizada
    config_personalizada = crear_configuracion_personalizada(
        sector="tecnologia",
        tamaño="mediana", 
        enfoque_innovacion="alto",
        sensibilidad_riesgo="media"
    )
    config_personalizada.guardar_configuracion("config_empresa_personalizada.json")
    print("✅ Configuración personalizada guardada")
    
    print("\n📋 Archivos de configuración creados:")
    print("   • config_empresa_hiperrealista.json (configuración por defecto)")
    print("   • config_empresa_tecnologia.json (empresa de tecnología)")
    print("   • config_empresa_startup.json (startup)")
    print("   • config_empresa_personalizada.json (configuración personalizada)")
