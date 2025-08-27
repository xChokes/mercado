"""
Sistema de Perfiles de Personalidad Hiperrealistas para Consumidores IA
======================================================================

Cada consumidor tiene un perfil único de personalidad que influye en:
- Decisiones de compra
- Tolerancia al riesgo
- Comportamiento social
- Adaptación a crisis
- Preferencias de productos
- Patrones de gasto
"""

import random
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import math


class TipoPersonalidad(Enum):
    """Tipos de personalidad basados en psicología económica"""
    CONSERVADOR = "conservador"
    IMPULSIVO = "impulsivo"
    ESTRATEGICO = "estrategico"
    SOCIAL = "social"
    MINIMALISTA = "minimalista"
    HEDONISTA = "hedonista"
    INVERSOR = "inversor"
    ALTRUISTA = "altruista"


class EstiloVida(Enum):
    """Estilos de vida que afectan patrones de consumo"""
    TRADICIONAL = "tradicional"
    URBANO_MODERNO = "urbano_moderno"
    ECOLOGICO = "ecologico"
    LUJOSO = "lujoso"
    FRUGAL = "frugal"
    TECNOLOGICO = "tecnologico"
    FAMILIAR = "familiar"
    BOHEMIO = "bohemio"


class NivelEducativo(Enum):
    """Nivel educativo que afecta decisiones económicas"""
    BASICO = "basico"
    SECUNDARIO = "secundario"
    TECNICO = "tecnico"
    UNIVERSITARIO = "universitario"
    POSTGRADO = "postgrado"


@dataclass
class RasgosPsicologicos:
    """Rasgos psicológicos fundamentales del consumidor"""
    # Big Five de personalidad (0.0 a 1.0)
    apertura: float = 0.5           # Apertura a experiencias
    responsabilidad: float = 0.5    # Conscientiousness
    extraversion: float = 0.5       # Extroversión
    amabilidad: float = 0.5         # Agreeableness
    neuroticismo: float = 0.5       # Neuroticism
    
    # Rasgos económicos específicos
    aversion_riesgo: float = 0.5    # Aversión al riesgo financiero
    materialismo: float = 0.5       # Importancia de posesiones materiales
    impulsividad: float = 0.5       # Tendencia a compras impulsivas
    planificacion: float = 0.5      # Capacidad de planificación financiera
    conformidad_social: float = 0.5  # Seguir tendencias sociales
    
    # Valores económicos personales
    importancia_precio: float = 0.5      # Qué tan importante es el precio
    importancia_calidad: float = 0.5     # Qué tan importante es la calidad
    importancia_marca: float = 0.5       # Lealtad a marcas
    importancia_sostenibilidad: float = 0.5  # Importancia de sostenibilidad
    importancia_conveniencia: float = 0.5    # Importancia de conveniencia


@dataclass
class PreferenciasConsumo:
    """Preferencias específicas de consumo del individuo"""
    # Preferencias por categorías de productos (0.0 a 1.0)
    preferencia_alimentacion: float = 0.5
    preferencia_tecnologia: float = 0.5
    preferencia_ropa: float = 0.5
    preferencia_entretenimiento: float = 0.5
    preferencia_educacion: float = 0.5
    preferencia_salud: float = 0.5
    preferencia_viajes: float = 0.5
    preferencia_hogar: float = 0.5
    
    # Patrones temporales de consumo
    preferencia_compras_matutinas: float = 0.5
    preferencia_compras_online: float = 0.5
    preferencia_promociones: float = 0.5
    
    # Marcas y proveedores preferidos
    marcas_favoritas: set = field(default_factory=set)
    vendedores_confiables: set = field(default_factory=set)
    
    # Umbrales de decisión personalizados
    umbral_precio_alto: float = 100.0     # Precio considerado "alto"
    umbral_descuento_atractivo: float = 0.15  # Descuento considerado atractivo
    frecuencia_compras_objetivo: int = 7   # Días entre compras ideales


@dataclass
class ContextoSocioeconomico:
    """Contexto socioeconómico del consumidor"""
    nivel_educativo: NivelEducativo = NivelEducativo.SECUNDARIO
    ocupacion: str = "empleado"
    sector_laboral: str = "servicios"
    estado_civil: str = "soltero"
    numero_dependientes: int = 0
    region_geografica: str = "urbana"
    
    # Influencias sociales
    grupo_referencia: List[str] = field(default_factory=list)  # IDs de consumidores influyentes
    influencers_seguidos: List[str] = field(default_factory=list)
    redes_sociales_activo: bool = True
    
    # Acceso a información
    acceso_internet: bool = True
    usa_comparadores_precios: bool = True
    lee_reviews: bool = True
    
    # Características financieras específicas
    historial_crediticio: float = 0.7  # 0.0 a 1.0
    experiencia_inversiones: float = 0.3
    conocimiento_financiero: float = 0.5


class GeneradorPerfilesPersonalidad:
    """Genera perfiles únicos de personalidad para consumidores"""
    
    @staticmethod
    def generar_perfil_unico() -> 'PerfilPersonalidadCompleto':
        """Genera un perfil completamente único y coherente"""
        # Seleccionar tipo de personalidad principal
        tipo_personalidad = random.choice(list(TipoPersonalidad))
        estilo_vida = random.choice(list(EstiloVida))
        
        # Generar rasgos psicológicos coherentes con el tipo
        rasgos = GeneradorPerfilesPersonalidad._generar_rasgos_coherentes(tipo_personalidad)
        
        # Generar preferencias coherentes con rasgos y estilo de vida
        preferencias = GeneradorPerfilesPersonalidad._generar_preferencias_coherentes(
            rasgos, estilo_vida
        )
        
        # Generar contexto socioeconómico
        contexto = GeneradorPerfilesPersonalidad._generar_contexto_socioeconomico(
            tipo_personalidad, estilo_vida
        )
        
        # Crear perfil completo
        perfil = PerfilPersonalidadCompleto(
            tipo_personalidad=tipo_personalidad,
            estilo_vida=estilo_vida,
            rasgos_psicologicos=rasgos,
            preferencias_consumo=preferencias,
            contexto_socioeconomico=contexto
        )
        
        return perfil
    
    @staticmethod
    def _generar_rasgos_coherentes(tipo_personalidad: TipoPersonalidad) -> RasgosPsicologicos:
        """Genera rasgos psicológicos coherentes con el tipo de personalidad"""
        
        # Plantillas base por tipo de personalidad
        plantillas = {
            TipoPersonalidad.CONSERVADOR: {
                'apertura': (0.2, 0.4), 'responsabilidad': (0.7, 0.9),
                'extraversion': (0.3, 0.6), 'amabilidad': (0.6, 0.8),
                'neuroticismo': (0.3, 0.6), 'aversion_riesgo': (0.7, 0.9),
                'materialismo': (0.3, 0.6), 'impulsividad': (0.1, 0.3),
                'planificacion': (0.7, 0.9), 'conformidad_social': (0.6, 0.8)
            },
            TipoPersonalidad.IMPULSIVO: {
                'apertura': (0.6, 0.8), 'responsabilidad': (0.2, 0.5),
                'extraversion': (0.7, 0.9), 'amabilidad': (0.5, 0.7),
                'neuroticismo': (0.4, 0.7), 'aversion_riesgo': (0.2, 0.5),
                'materialismo': (0.6, 0.8), 'impulsividad': (0.7, 0.9),
                'planificacion': (0.1, 0.4), 'conformidad_social': (0.7, 0.9)
            },
            TipoPersonalidad.ESTRATEGICO: {
                'apertura': (0.5, 0.8), 'responsabilidad': (0.8, 1.0),
                'extraversion': (0.4, 0.7), 'amabilidad': (0.4, 0.7),
                'neuroticismo': (0.2, 0.4), 'aversion_riesgo': (0.4, 0.6),
                'materialismo': (0.4, 0.6), 'impulsividad': (0.1, 0.3),
                'planificacion': (0.8, 1.0), 'conformidad_social': (0.3, 0.6)
            },
            TipoPersonalidad.SOCIAL: {
                'apertura': (0.6, 0.8), 'responsabilidad': (0.5, 0.7),
                'extraversion': (0.8, 1.0), 'amabilidad': (0.7, 0.9),
                'neuroticismo': (0.3, 0.6), 'aversion_riesgo': (0.5, 0.7),
                'materialismo': (0.5, 0.8), 'impulsividad': (0.4, 0.7),
                'planificacion': (0.4, 0.7), 'conformidad_social': (0.8, 1.0)
            },
            TipoPersonalidad.MINIMALISTA: {
                'apertura': (0.4, 0.7), 'responsabilidad': (0.6, 0.8),
                'extraversion': (0.3, 0.6), 'amabilidad': (0.6, 0.8),
                'neuroticismo': (0.2, 0.5), 'aversion_riesgo': (0.6, 0.8),
                'materialismo': (0.1, 0.3), 'impulsividad': (0.2, 0.4),
                'planificacion': (0.7, 0.9), 'conformidad_social': (0.2, 0.5)
            },
            TipoPersonalidad.HEDONISTA: {
                'apertura': (0.7, 0.9), 'responsabilidad': (0.3, 0.6),
                'extraversion': (0.7, 0.9), 'amabilidad': (0.5, 0.7),
                'neuroticismo': (0.4, 0.7), 'aversion_riesgo': (0.3, 0.6),
                'materialismo': (0.7, 0.9), 'impulsividad': (0.6, 0.8),
                'planificacion': (0.2, 0.5), 'conformidad_social': (0.6, 0.8)
            },
            TipoPersonalidad.INVERSOR: {
                'apertura': (0.5, 0.7), 'responsabilidad': (0.7, 0.9),
                'extraversion': (0.4, 0.7), 'amabilidad': (0.4, 0.6),
                'neuroticismo': (0.2, 0.4), 'aversion_riesgo': (0.3, 0.6),
                'materialismo': (0.5, 0.7), 'impulsividad': (0.1, 0.3),
                'planificacion': (0.8, 1.0), 'conformidad_social': (0.3, 0.6)
            },
            TipoPersonalidad.ALTRUISTA: {
                'apertura': (0.6, 0.8), 'responsabilidad': (0.6, 0.8),
                'extraversion': (0.5, 0.8), 'amabilidad': (0.8, 1.0),
                'neuroticismo': (0.3, 0.6), 'aversion_riesgo': (0.5, 0.7),
                'materialismo': (0.2, 0.5), 'impulsividad': (0.3, 0.6),
                'planificacion': (0.6, 0.8), 'conformidad_social': (0.4, 0.7)
            }
        }
        
        plantilla = plantillas[tipo_personalidad]
        rasgos = RasgosPsicologicos()
        
        # Generar cada rasgo dentro del rango específico
        for rasgo, (min_val, max_val) in plantilla.items():
            if hasattr(rasgos, rasgo):
                setattr(rasgos, rasgo, random.uniform(min_val, max_val))
        
        # Generar valores económicos específicos
        rasgos.importancia_precio = 1.0 - rasgos.materialismo * 0.8
        rasgos.importancia_calidad = rasgos.responsabilidad * 0.8 + 0.2
        rasgos.importancia_marca = rasgos.materialismo * 0.7 + rasgos.conformidad_social * 0.3
        rasgos.importancia_sostenibilidad = rasgos.apertura * 0.6 + rasgos.amabilidad * 0.4
        rasgos.importancia_conveniencia = 1.0 - rasgos.planificacion * 0.6
        
        return rasgos
    
    @staticmethod
    def _generar_preferencias_coherentes(rasgos: RasgosPsicologicos, 
                                       estilo_vida: EstiloVida) -> PreferenciasConsumo:
        """Genera preferencias de consumo coherentes con rasgos y estilo de vida"""
        
        preferencias = PreferenciasConsumo()
        
        # Modificadores por estilo de vida
        modificadores_estilo = {
            EstiloVida.TRADICIONAL: {
                'alimentacion': 0.8, 'tecnologia': 0.3, 'ropa': 0.6,
                'entretenimiento': 0.5, 'educacion': 0.7, 'salud': 0.8,
                'viajes': 0.4, 'hogar': 0.9
            },
            EstiloVida.URBANO_MODERNO: {
                'alimentacion': 0.6, 'tecnologia': 0.9, 'ropa': 0.8,
                'entretenimiento': 0.8, 'educacion': 0.7, 'salud': 0.7,
                'viajes': 0.7, 'hogar': 0.6
            },
            EstiloVida.ECOLOGICO: {
                'alimentacion': 0.9, 'tecnologia': 0.5, 'ropa': 0.6,
                'entretenimiento': 0.5, 'educacion': 0.8, 'salud': 0.9,
                'viajes': 0.6, 'hogar': 0.8
            },
            EstiloVida.LUJOSO: {
                'alimentacion': 0.8, 'tecnologia': 0.8, 'ropa': 0.9,
                'entretenimiento': 0.9, 'educacion': 0.6, 'salud': 0.7,
                'viajes': 0.9, 'hogar': 0.9
            },
            EstiloVida.FRUGAL: {
                'alimentacion': 0.7, 'tecnologia': 0.3, 'ropa': 0.4,
                'entretenimiento': 0.3, 'educacion': 0.8, 'salud': 0.8,
                'viajes': 0.2, 'hogar': 0.6
            },
            EstiloVida.TECNOLOGICO: {
                'alimentacion': 0.5, 'tecnologia': 1.0, 'ropa': 0.5,
                'entretenimiento': 0.8, 'educacion': 0.9, 'salud': 0.6,
                'viajes': 0.5, 'hogar': 0.7
            },
            EstiloVida.FAMILIAR: {
                'alimentacion': 0.9, 'tecnologia': 0.6, 'ropa': 0.7,
                'entretenimiento': 0.8, 'educacion': 0.9, 'salud': 0.9,
                'viajes': 0.6, 'hogar': 0.9
            },
            EstiloVida.BOHEMIO: {
                'alimentacion': 0.6, 'tecnologia': 0.4, 'ropa': 0.8,
                'entretenimiento': 0.9, 'educacion': 0.8, 'salud': 0.6,
                'viajes': 0.8, 'hogar': 0.4
            }
        }
        
        modificador = modificadores_estilo[estilo_vida]
        
        # Aplicar modificadores base
        preferencias.preferencia_alimentacion = modificador['alimentacion'] + random.uniform(-0.1, 0.1)
        preferencias.preferencia_tecnologia = modificador['tecnologia'] + random.uniform(-0.1, 0.1)
        preferencias.preferencia_ropa = modificador['ropa'] + random.uniform(-0.1, 0.1)
        preferencias.preferencia_entretenimiento = modificador['entretenimiento'] + random.uniform(-0.1, 0.1)
        preferencias.preferencia_educacion = modificador['educacion'] + random.uniform(-0.1, 0.1)
        preferencias.preferencia_salud = modificador['salud'] + random.uniform(-0.1, 0.1)
        preferencias.preferencia_viajes = modificador['viajes'] + random.uniform(-0.1, 0.1)
        preferencias.preferencia_hogar = modificador['hogar'] + random.uniform(-0.1, 0.1)
        
        # Ajustar por rasgos psicológicos
        preferencias.preferencia_tecnologia *= (rasgos.apertura * 0.7 + 0.3)
        preferencias.preferencia_entretenimiento *= (rasgos.extraversion * 0.8 + 0.2)
        preferencias.preferencia_salud *= (rasgos.responsabilidad * 0.6 + 0.4)
        preferencias.preferencia_viajes *= (rasgos.apertura * 0.8 + 0.2)
        
        # Patrones temporales y de compra
        preferencias.preferencia_compras_matutinas = rasgos.responsabilidad * 0.8 + random.uniform(0.0, 0.2)
        preferencias.preferencia_compras_online = rasgos.apertura * 0.6 + modificador['tecnologia'] * 0.4
        preferencias.preferencia_promociones = rasgos.importancia_precio * 0.8 + random.uniform(0.0, 0.2)
        
        # Umbrales personalizados
        factor_precio = 1.0 + rasgos.materialismo * 2.0 - rasgos.importancia_precio
        preferencias.umbral_precio_alto = 50.0 * factor_precio + random.uniform(-20, 20)
        preferencias.umbral_descuento_atractivo = (1.0 - rasgos.materialismo) * 0.3 + 0.05
        preferencias.frecuencia_compras_objetivo = int(7 / (rasgos.impulsividad + 0.5)) + random.randint(-2, 2)
        
        # Normalizar valores entre 0.0 y 1.0
        for attr in ['preferencia_alimentacion', 'preferencia_tecnologia', 'preferencia_ropa',
                     'preferencia_entretenimiento', 'preferencia_educacion', 'preferencia_salud',
                     'preferencia_viajes', 'preferencia_hogar', 'preferencia_compras_matutinas',
                     'preferencia_compras_online', 'preferencia_promociones']:
            value = getattr(preferencias, attr)
            setattr(preferencias, attr, max(0.0, min(1.0, value)))
        
        return preferencias
    
    @staticmethod
    def _generar_contexto_socioeconomico(tipo_personalidad: TipoPersonalidad,
                                       estilo_vida: EstiloVida) -> ContextoSocioeconomico:
        """Genera contexto socioeconómico coherente"""
        
        # Probabilidades de nivel educativo por tipo de personalidad
        prob_educacion = {
            TipoPersonalidad.ESTRATEGICO: [0.05, 0.15, 0.20, 0.40, 0.20],
            TipoPersonalidad.INVERSOR: [0.05, 0.10, 0.20, 0.45, 0.20],
            TipoPersonalidad.CONSERVADOR: [0.10, 0.25, 0.30, 0.25, 0.10],
            TipoPersonalidad.IMPULSIVO: [0.20, 0.30, 0.25, 0.20, 0.05],
            TipoPersonalidad.SOCIAL: [0.10, 0.20, 0.25, 0.35, 0.10],
            TipoPersonalidad.MINIMALISTA: [0.15, 0.25, 0.25, 0.25, 0.10],
            TipoPersonalidad.HEDONISTA: [0.20, 0.25, 0.25, 0.25, 0.05],
            TipoPersonalidad.ALTRUISTA: [0.10, 0.15, 0.20, 0.35, 0.20]
        }
        
        contexto = ContextoSocioeconomico()
        
        # Seleccionar nivel educativo
        probs = prob_educacion[tipo_personalidad]
        niveles = list(NivelEducativo)
        contexto.nivel_educativo = np.random.choice(niveles, p=probs)
        
        # Generar ocupación coherente con educación
        ocupaciones_por_nivel = {
            NivelEducativo.BASICO: ["obrero", "vendedor", "conductor", "limpieza"],
            NivelEducativo.SECUNDARIO: ["empleado", "vendedor", "tecnico_basico", "seguridad"],
            NivelEducativo.TECNICO: ["tecnico", "supervisor", "especialista", "instructor"],
            NivelEducativo.UNIVERSITARIO: ["profesional", "analista", "gerente", "consultor"],
            NivelEducativo.POSTGRADO: ["ejecutivo", "director", "investigador", "especialista_senior"]
        }
        
        contexto.ocupacion = random.choice(ocupaciones_por_nivel[contexto.nivel_educativo])
        
        # Sector laboral coherente con estilo de vida
        sectores_por_estilo = {
            EstiloVida.TECNOLOGICO: ["tecnologia", "telecomunicaciones", "investigacion"],
            EstiloVida.URBANO_MODERNO: ["servicios", "finanzas", "comunicaciones"],
            EstiloVida.TRADICIONAL: ["manufactura", "agricultura", "gobierno"],
            EstiloVida.ECOLOGICO: ["agricultura_organica", "energias_renovables", "consultoria_ambiental"],
            EstiloVida.LUJOSO: ["finanzas", "lujo", "entretenimiento"],
            EstiloVida.FRUGAL: ["gobierno", "educacion", "agricultura"],
            EstiloVida.FAMILIAR: ["educacion", "salud", "servicios_sociales"],
            EstiloVida.BOHEMIO: ["arte", "entretenimiento", "turismo"]
        }
        
        if estilo_vida in sectores_por_estilo:
            contexto.sector_laboral = random.choice(sectores_por_estilo[estilo_vida])
        else:
            contexto.sector_laboral = random.choice(["servicios", "manufactura", "comercio"])
        
        # Estado civil y dependientes
        if tipo_personalidad in [TipoPersonalidad.CONSERVADOR, TipoPersonalidad.ALTRUISTA]:
            contexto.estado_civil = random.choice(["casado", "union_libre", "soltero"])
            if contexto.estado_civil in ["casado", "union_libre"]:
                contexto.numero_dependientes = random.choices([0, 1, 2, 3, 4], weights=[0.2, 0.3, 0.3, 0.15, 0.05])[0]
        else:
            contexto.estado_civil = random.choice(["soltero", "soltero", "casado"])  # Más probabilidad soltero
            contexto.numero_dependientes = random.choices([0, 1, 2], weights=[0.7, 0.2, 0.1])[0]
        
        # Región geográfica
        contexto.region_geografica = random.choice(["urbana", "suburbana", "rural"])
        
        # Características digitales
        contexto.redes_sociales_activo = tipo_personalidad in [TipoPersonalidad.SOCIAL, TipoPersonalidad.HEDONISTA]
        contexto.acceso_internet = contexto.nivel_educativo != NivelEducativo.BASICO or random.random() < 0.8
        contexto.usa_comparadores_precios = (
            tipo_personalidad in [TipoPersonalidad.ESTRATEGICO, TipoPersonalidad.MINIMALISTA] or
            random.random() < 0.6
        )
        contexto.lee_reviews = contexto.acceso_internet and random.random() < 0.7
        
        # Características financieras
        if contexto.nivel_educativo in [NivelEducativo.UNIVERSITARIO, NivelEducativo.POSTGRADO]:
            contexto.historial_crediticio = random.uniform(0.6, 0.9)
            contexto.experiencia_inversiones = random.uniform(0.3, 0.8)
            contexto.conocimiento_financiero = random.uniform(0.5, 0.9)
        else:
            contexto.historial_crediticio = random.uniform(0.3, 0.7)
            contexto.experiencia_inversiones = random.uniform(0.1, 0.4)
            contexto.conocimiento_financiero = random.uniform(0.2, 0.6)
        
        # Ajustar por tipo de personalidad
        if tipo_personalidad == TipoPersonalidad.INVERSOR:
            contexto.experiencia_inversiones = max(0.5, contexto.experiencia_inversiones)
            contexto.conocimiento_financiero = max(0.6, contexto.conocimiento_financiero)
        elif tipo_personalidad == TipoPersonalidad.IMPULSIVO:
            contexto.historial_crediticio *= 0.8
        elif tipo_personalidad == TipoPersonalidad.CONSERVADOR:
            contexto.historial_crediticio = max(0.7, contexto.historial_crediticio)
        
        return contexto


@dataclass
class PerfilPersonalidadCompleto:
    """Perfil completo de personalidad de un consumidor"""
    tipo_personalidad: TipoPersonalidad
    estilo_vida: EstiloVida
    rasgos_psicologicos: RasgosPsicologicos
    preferencias_consumo: PreferenciasConsumo
    contexto_socioeconomico: ContextoSocioeconomico
    
    # Métricas dinámicas que evolucionan con el tiempo
    satisfaccion_vida: float = 0.5
    confianza_economia: float = 0.5
    stress_financiero: float = 0.0
    experiencia_mercado: float = 0.0
    
    def calcular_factor_decision(self, tipo_decision: str, contexto: Dict[str, Any]) -> float:
        """Calcula un factor de decisión específico basado en el perfil"""
        
        if tipo_decision == "compra_impulsiva":
            factor = (
                self.rasgos_psicologicos.impulsividad * 0.4 +
                (1.0 - self.rasgos_psicologicos.planificacion) * 0.3 +
                self.rasgos_psicologicos.materialismo * 0.2 +
                (1.0 - self.rasgos_psicologicos.aversion_riesgo) * 0.1
            )
            
            # Modificar por estado emocional
            if self.stress_financiero > 0.7:
                factor *= 0.5  # Reducir impulsividad cuando está estresado
            elif self.satisfaccion_vida > 0.8:
                factor *= 1.2  # Aumentar cuando está feliz
                
        elif tipo_decision == "negociacion_precio":
            factor = (
                self.rasgos_psicologicos.importancia_precio * 0.4 +
                (1.0 - self.rasgos_psicologicos.amabilidad) * 0.3 +
                self.rasgos_psicologicos.extraversion * 0.2 +
                self.experiencia_mercado * 0.1
            )
            
        elif tipo_decision == "compra_grupal":
            factor = (
                self.rasgos_psicologicos.conformidad_social * 0.4 +
                self.rasgos_psicologicos.extraversion * 0.3 +
                self.rasgos_psicologicos.importancia_precio * 0.2 +
                (1.0 - self.rasgos_psicologicos.aversion_riesgo) * 0.1
            )
            
        elif tipo_decision == "inversion_riesgo":
            factor = (
                (1.0 - self.rasgos_psicologicos.aversion_riesgo) * 0.4 +
                self.contexto_socioeconomico.experiencia_inversiones * 0.3 +
                self.rasgos_psicologicos.planificacion * 0.2 +
                self.contexto_socioeconomico.conocimiento_financiero * 0.1
            )
            
        elif tipo_decision == "lealtad_marca":
            factor = (
                self.rasgos_psicologicos.importancia_marca * 0.4 +
                self.rasgos_psicologicos.responsabilidad * 0.3 +
                (1.0 - self.rasgos_psicologicos.apertura) * 0.2 +
                self.rasgos_psicologicos.conformidad_social * 0.1
            )
            
        else:
            factor = 0.5  # Factor neutro por defecto
        
        # Normalizar entre 0.0 y 1.0
        return max(0.0, min(1.0, factor))
    
    def actualizar_estado_emocional(self, evento: str, intensidad: float = 0.1):
        """Actualiza el estado emocional basado en eventos"""
        
        if evento == "compra_exitosa":
            self.satisfaccion_vida = min(1.0, self.satisfaccion_vida + intensidad * 0.5)
            self.stress_financiero = max(0.0, self.stress_financiero - intensidad * 0.3)
            
        elif evento == "compra_fallida":
            self.satisfaccion_vida = max(0.0, self.satisfaccion_vida - intensidad * 0.3)
            self.stress_financiero = min(1.0, self.stress_financiero + intensidad * 0.2)
            
        elif evento == "ganancia_dinero":
            self.satisfaccion_vida = min(1.0, self.satisfaccion_vida + intensidad)
            self.stress_financiero = max(0.0, self.stress_financiero - intensidad * 0.5)
            self.confianza_economia = min(1.0, self.confianza_economia + intensidad * 0.3)
            
        elif evento == "perdida_dinero":
            self.satisfaccion_vida = max(0.0, self.satisfaccion_vida - intensidad * 0.8)
            self.stress_financiero = min(1.0, self.stress_financiero + intensidad)
            self.confianza_economia = max(0.0, self.confianza_economia - intensidad * 0.4)
            
        elif evento == "crisis_economica":
            self.confianza_economia = max(0.0, self.confianza_economia - intensidad * 0.6)
            self.stress_financiero = min(1.0, self.stress_financiero + intensidad * 0.8)
            
        elif evento == "recuperacion_economica":
            self.confianza_economia = min(1.0, self.confianza_economia + intensidad * 0.4)
            self.stress_financiero = max(0.0, self.stress_financiero - intensidad * 0.3)
            
        # Incrementar experiencia de mercado gradualmente
        self.experiencia_mercado = min(1.0, self.experiencia_mercado + 0.001)
    
    def get_descripcion_personalidad(self) -> str:
        """Obtiene una descripción textual del perfil de personalidad"""
        
        desc_rasgos = []
        
        # Describir tipo principal
        desc_rasgos.append(f"Personalidad {self.tipo_personalidad.value.title()}")
        desc_rasgos.append(f"Estilo de vida {self.estilo_vida.value.replace('_', ' ').title()}")
        
        # Describir rasgos dominantes
        rasgos = self.rasgos_psicologicos
        if rasgos.impulsividad > 0.7:
            desc_rasgos.append("Muy impulsivo")
        elif rasgos.planificacion > 0.7:
            desc_rasgos.append("Muy planificador")
            
        if rasgos.aversion_riesgo > 0.7:
            desc_rasgos.append("Adverso al riesgo")
        elif rasgos.aversion_riesgo < 0.3:
            desc_rasgos.append("Tolerante al riesgo")
            
        if rasgos.materialismo > 0.7:
            desc_rasgos.append("Materialista")
        elif rasgos.materialismo < 0.3:
            desc_rasgos.append("No materialista")
            
        if rasgos.conformidad_social > 0.7:
            desc_rasgos.append("Sigue tendencias")
        elif rasgos.conformidad_social < 0.3:
            desc_rasgos.append("Independiente")
            
        # Describir contexto
        desc_rasgos.append(f"Educación {self.contexto_socioeconomico.nivel_educativo.value}")
        desc_rasgos.append(f"Ocupación: {self.contexto_socioeconomico.ocupacion}")
        
        return " | ".join(desc_rasgos)
