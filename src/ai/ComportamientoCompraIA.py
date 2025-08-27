"""
Sistema de Comportamientos de Compra Únicos
==========================================

Define comportamientos de compra únicos para cada consumidor basándose en:
- Perfil de personalidad
- Experiencias pasadas
- Contexto social y económico
- Factores psicológicos dinámicos
"""

import random
import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
import math
from datetime import datetime, timedelta

from .PerfilPersonalidadIA import PerfilPersonalidadCompleto, TipoPersonalidad, EstiloVida
from ..models.BienHiperrealista import BienHiperrealista, TipoBien


class TipoComportamientoCompra(Enum):
    """Tipos de comportamiento de compra"""
    PLANIFICADO = "planificado"
    IMPULSIVO = "impulsivo"
    EXPLORADOR = "explorador"
    COMPARADOR = "comparador"
    SOCIAL = "social"
    CONSERVADOR = "conservador"
    OPORTUNISTA = "oportunista"
    MINIMALISTA = "minimalista"


class FaseDecisionCompra(Enum):
    """Fases del proceso de decisión de compra"""
    RECONOCIMIENTO_NECESIDAD = "reconocimiento_necesidad"
    BUSQUEDA_INFORMACION = "busqueda_informacion"
    EVALUACION_ALTERNATIVAS = "evaluacion_alternativas"
    DECISION_COMPRA = "decision_compra"
    COMPORTAMIENTO_POST_COMPRA = "comportamiento_post_compra"


@dataclass
class CriterioDecision:
    """Criterio para tomar decisiones de compra"""
    nombre: str
    peso: float  # 0.0 a 1.0
    umbral_minimo: float  # Valor mínimo aceptable
    preferencia_maxima: float  # Valor preferido
    es_eliminatorio: bool = False  # Si no se cumple, elimina la opción


@dataclass
class ContextoCompra:
    """Contexto en el que se realiza una compra"""
    urgencia: float = 0.5  # 0.0 (no urgente) a 1.0 (muy urgente)
    presupuesto_disponible: float = 0.0
    tiempo_disponible: float = 1.0  # 0.0 (sin tiempo) a 1.0 (todo el tiempo)
    compañia: Optional[str] = None  # Solo, familia, amigos
    ubicacion: str = "casa"  # casa, trabajo, tienda, online
    estado_emocional: float = 0.5  # 0.0 (muy mal) a 1.0 (muy bien)
    evento_especial: Optional[str] = None


@dataclass
class ExperienciaCompra:
    """Registro de una experiencia de compra"""
    bien: str
    vendedor: str
    precio_pagado: float
    calidad_percibida: float
    satisfaccion: float
    tiempo_decision: float  # minutos
    fecha: datetime
    contexto: ContextoCompra
    resultado_negociacion: Optional[float] = None
    recomendaria: bool = True


class SistemaComportamientoCompra:
    """Sistema que define comportamientos únicos de compra"""
    
    def __init__(self, perfil_personalidad: PerfilPersonalidadCompleto):
        self.perfil = perfil_personalidad
        self.comportamiento_dominante = self._determinar_comportamiento_dominante()
        self.comportamientos_secundarios = self._determinar_comportamientos_secundarios()
        
        # Criterios de decisión personalizados
        self.criterios_decision = self._generar_criterios_decision()
        
        # Historial de experiencias
        self.experiencias_compra: List[ExperienciaCompra] = []
        self.vendedores_bloqueados: Set[str] = set()
        self.marcas_favoritas: Set[str] = set()
        self.productos_lista_deseos: Set[str] = set()
        
        # Patrones de comportamiento aprendidos
        self.patrones_temporales = self._generar_patrones_temporales()
        self.influencias_sociales = self._generar_influencias_sociales()
        self.sesgos_cognitivos = self._generar_sesgos_cognitivos()
        
        # Métricas de comportamiento
        self.tiempo_promedio_decision = self._calcular_tiempo_base_decision()
        self.tendencia_negociacion = self._calcular_tendencia_negociacion()
        self.factor_lealtad = self._calcular_factor_lealtad()
        self.propension_riesgo_compra = self._calcular_propension_riesgo()
    
    def _determinar_comportamiento_dominante(self) -> TipoComportamientoCompra:
        """Determina el comportamiento de compra dominante"""
        
        rasgos = self.perfil.rasgos_psicologicos
        
        # Calcular puntuaciones para cada tipo
        puntuaciones = {}
        
        # Planificado
        puntuaciones[TipoComportamientoCompra.PLANIFICADO] = (
            rasgos.planificacion * 0.4 +
            rasgos.responsabilidad * 0.3 +
            (1.0 - rasgos.impulsividad) * 0.3
        )
        
        # Impulsivo
        puntuaciones[TipoComportamientoCompra.IMPULSIVO] = (
            rasgos.impulsividad * 0.5 +
            (1.0 - rasgos.planificacion) * 0.3 +
            rasgos.materialismo * 0.2
        )
        
        # Explorador
        puntuaciones[TipoComportamientoCompra.EXPLORADOR] = (
            rasgos.apertura * 0.4 +
            (1.0 - rasgos.aversion_riesgo) * 0.3 +
            rasgos.extraversion * 0.3
        )
        
        # Comparador
        puntuaciones[TipoComportamientoCompra.COMPARADOR] = (
            rasgos.importancia_precio * 0.4 +
            rasgos.planificacion * 0.3 +
            rasgos.responsabilidad * 0.3
        )
        
        # Social
        puntuaciones[TipoComportamientoCompra.SOCIAL] = (
            rasgos.conformidad_social * 0.4 +
            rasgos.extraversion * 0.3 +
            rasgos.amabilidad * 0.3
        )
        
        # Conservador
        puntuaciones[TipoComportamientoCompra.CONSERVADOR] = (
            rasgos.aversion_riesgo * 0.4 +
            (1.0 - rasgos.apertura) * 0.3 +
            rasgos.responsabilidad * 0.3
        )
        
        # Oportunista
        puntuaciones[TipoComportamientoCompra.OPORTUNISTA] = (
            rasgos.importancia_precio * 0.4 +
            (1.0 - rasgos.aversion_riesgo) * 0.3 +
            rasgos.apertura * 0.3
        )
        
        # Minimalista
        puntuaciones[TipoComportamientoCompra.MINIMALISTA] = (
            (1.0 - rasgos.materialismo) * 0.5 +
            rasgos.planificacion * 0.3 +
            rasgos.importancia_sostenibilidad * 0.2
        )
        
        # Seleccionar el mayor
        return max(puntuaciones.items(), key=lambda x: x[1])[0]
    
    def _determinar_comportamientos_secundarios(self) -> List[TipoComportamientoCompra]:
        """Determina comportamientos secundarios"""
        
        # Obtener todos los comportamientos ordenados por puntuación
        rasgos = self.perfil.rasgos_psicologicos
        puntuaciones = {}
        
        for comportamiento in TipoComportamientoCompra:
            if comportamiento != self.comportamiento_dominante:
                # Calcular puntuación simplificada
                if comportamiento == TipoComportamientoCompra.SOCIAL:
                    puntuaciones[comportamiento] = rasgos.conformidad_social
                elif comportamiento == TipoComportamientoCompra.EXPLORADOR:
                    puntuaciones[comportamiento] = rasgos.apertura
                elif comportamiento == TipoComportamientoCompra.COMPARADOR:
                    puntuaciones[comportamiento] = rasgos.importancia_precio
                else:
                    puntuaciones[comportamiento] = random.uniform(0.3, 0.7)
        
        # Ordenar y tomar los 2-3 mejores
        ordenados = sorted(puntuaciones.items(), key=lambda x: x[1], reverse=True)
        num_secundarios = random.randint(1, 3)
        return [comp for comp, _ in ordenados[:num_secundarios]]
    
    def _generar_criterios_decision(self) -> Dict[str, CriterioDecision]:
        """Genera criterios de decisión personalizados"""
        
        criterios = {}
        rasgos = self.perfil.rasgos_psicologicos
        
        # Precio
        peso_precio = rasgos.importancia_precio
        criterios['precio'] = CriterioDecision(
            nombre="precio",
            peso=peso_precio,
            umbral_minimo=0.0,
            preferencia_maxima=100.0 * (1.0 - peso_precio),  # Menos peso = acepta precios más altos
            es_eliminatorio=peso_precio > 0.8
        )
        
        # Calidad
        peso_calidad = rasgos.importancia_calidad
        criterios['calidad'] = CriterioDecision(
            nombre="calidad",
            peso=peso_calidad,
            umbral_minimo=peso_calidad * 0.5,
            preferencia_maxima=1.0,
            es_eliminatorio=peso_calidad > 0.7
        )
        
        # Marca
        peso_marca = rasgos.importancia_marca
        criterios['marca'] = CriterioDecision(
            nombre="marca",
            peso=peso_marca,
            umbral_minimo=peso_marca * 0.3,
            preferencia_maxima=1.0,
            es_eliminatorio=False
        )
        
        # Sostenibilidad
        peso_sostenibilidad = rasgos.importancia_sostenibilidad
        criterios['sostenibilidad'] = CriterioDecision(
            nombre="sostenibilidad",
            peso=peso_sostenibilidad,
            umbral_minimo=peso_sostenibilidad * 0.4,
            preferencia_maxima=1.0,
            es_eliminatorio=peso_sostenibilidad > 0.8
        )
        
        # Conveniencia
        peso_conveniencia = rasgos.importancia_conveniencia
        criterios['conveniencia'] = CriterioDecision(
            nombre="conveniencia",
            peso=peso_conveniencia,
            umbral_minimo=peso_conveniencia * 0.3,
            preferencia_maxima=1.0,
            es_eliminatorio=False
        )
        
        # Criterios específicos por comportamiento dominante
        if self.comportamiento_dominante == TipoComportamientoCompra.SOCIAL:
            criterios['popularidad'] = CriterioDecision(
                nombre="popularidad",
                peso=0.7,
                umbral_minimo=0.5,
                preferencia_maxima=1.0,
                es_eliminatorio=False
            )
        
        elif self.comportamiento_dominante == TipoComportamientoCompra.EXPLORADOR:
            criterios['novedad'] = CriterioDecision(
                nombre="novedad",
                peso=0.6,
                umbral_minimo=0.3,
                preferencia_maxima=1.0,
                es_eliminatorio=False
            )
        
        elif self.comportamiento_dominante == TipoComportamientoCompra.CONSERVADOR:
            criterios['seguridad'] = CriterioDecision(
                nombre="seguridad",
                peso=0.8,
                umbral_minimo=0.6,
                preferencia_maxima=1.0,
                es_eliminatorio=True
            )
        
        return criterios
    
    def _generar_patrones_temporales(self) -> Dict[str, Any]:
        """Genera patrones temporales de compra"""
        
        patrones = {}
        rasgos = self.perfil.rasgos_psicologicos
        
        # Horarios preferidos (0-23)
        if rasgos.responsabilidad > 0.7:
            # Compradores matutinos responsables
            patrones['horas_preferidas'] = list(range(8, 12)) + list(range(14, 18))
        elif rasgos.extraversion > 0.7:
            # Compradores vespertinos sociales
            patrones['horas_preferidas'] = list(range(16, 22))
        else:
            # Horarios mixtos
            patrones['horas_preferidas'] = list(range(10, 20))
        
        # Días de la semana preferidos
        if self.comportamiento_dominante == TipoComportamientoCompra.PLANIFICADO:
            patrones['dias_preferidos'] = ['lunes', 'martes', 'miercoles', 'jueves']
        elif self.comportamiento_dominante == TipoComportamientoCompra.SOCIAL:
            patrones['dias_preferidos'] = ['viernes', 'sabado', 'domingo']
        else:
            patrones['dias_preferidos'] = ['lunes', 'miercoles', 'viernes', 'sabado']
        
        # Frecuencia de compras
        if rasgos.impulsividad > 0.7:
            patrones['frecuencia_base'] = 'alta'  # Compras frecuentes
            patrones['dias_entre_compras'] = random.randint(1, 3)
        elif rasgos.planificacion > 0.7:
            patrones['frecuencia_base'] = 'planificada'
            patrones['dias_entre_compras'] = random.randint(7, 14)
        else:
            patrones['frecuencia_base'] = 'media'
            patrones['dias_entre_compras'] = random.randint(3, 7)
        
        # Estacionalidad personal
        patrones['meses_alta_actividad'] = random.sample(range(1, 13), random.randint(3, 6))
        
        return patrones
    
    def _generar_influencias_sociales(self) -> Dict[str, float]:
        """Genera factores de influencia social"""
        
        influencias = {}
        rasgos = self.perfil.rasgos_psicologicos
        
        # Influencia de familia
        influencias['familia'] = rasgos.amabilidad * 0.7 + random.uniform(0.2, 0.3)
        
        # Influencia de amigos
        influencias['amigos'] = rasgos.extraversion * 0.6 + rasgos.conformidad_social * 0.4
        
        # Influencia de celebridades
        if self.perfil.contexto_socioeconomico.redes_sociales_activo:
            influencias['celebridades'] = rasgos.conformidad_social * 0.5 + random.uniform(0.0, 0.3)
        else:
            influencias['celebridades'] = random.uniform(0.0, 0.2)
        
        # Influencia de expertos/reviews
        influencias['expertos'] = (
            self.perfil.contexto_socioeconomico.conocimiento_financiero * 0.4 +
            rasgos.responsabilidad * 0.3 +
            random.uniform(0.2, 0.3)
        )
        
        # Influencia de tendencias de mercado
        influencias['tendencias'] = rasgos.apertura * 0.5 + rasgos.conformidad_social * 0.3
        
        # Influencia de escasez (FOMO)
        influencias['escasez'] = rasgos.impulsividad * 0.6 + (1.0 - rasgos.aversion_riesgo) * 0.4
        
        # Normalizar valores
        for key in influencias:
            influencias[key] = max(0.0, min(1.0, influencias[key]))
        
        return influencias
    
    def _generar_sesgos_cognitivos(self) -> Dict[str, float]:
        """Genera sesgos cognitivos que afectan decisiones"""
        
        sesgos = {}
        rasgos = self.perfil.rasgos_psicologicos
        
        # Sesgo de anclaje (influencia del primer precio visto)
        sesgos['anclaje'] = rasgos.conformidad_social * 0.6 + random.uniform(0.2, 0.4)
        
        # Sesgo de confirmación (buscar información que confirme decisión)
        sesgos['confirmacion'] = (1.0 - rasgos.apertura) * 0.7 + random.uniform(0.1, 0.3)
        
        # Sesgo de disponibilidad (decisiones basadas en experiencias recientes)
        sesgos['disponibilidad'] = rasgos.neuroticismo * 0.5 + random.uniform(0.3, 0.5)
        
        # Sesgo de pérdida (aversión a perder lo que ya se tiene)
        sesgos['aversion_perdida'] = rasgos.aversion_riesgo * 0.8 + random.uniform(0.1, 0.2)
        
        # Sesgo de reciprocidad (sentirse obligado a devolver favores)
        sesgos['reciprocidad'] = rasgos.amabilidad * 0.7 + random.uniform(0.1, 0.3)
        
        # Sesgo de autoridad (seguir recomendaciones de figuras de autoridad)
        sesgos['autoridad'] = rasgos.conformidad_social * 0.6 + random.uniform(0.2, 0.4)
        
        # Sesgo de escasez (valorar más lo que es limitado)
        sesgos['escasez'] = rasgos.impulsividad * 0.5 + rasgos.materialismo * 0.3 + random.uniform(0.1, 0.2)
        
        return sesgos
    
    def _calcular_tiempo_base_decision(self) -> float:
        """Calcula tiempo base de decisión en minutos"""
        
        rasgos = self.perfil.rasgos_psicologicos
        
        # Tiempo base por comportamiento
        tiempos_base = {
            TipoComportamientoCompra.IMPULSIVO: 2.0,
            TipoComportamientoCompra.PLANIFICADO: 45.0,
            TipoComportamientoCompra.COMPARADOR: 60.0,
            TipoComportamientoCompra.EXPLORADOR: 30.0,
            TipoComportamientoCompra.SOCIAL: 20.0,
            TipoComportamientoCompra.CONSERVADOR: 40.0,
            TipoComportamientoCompra.OPORTUNISTA: 15.0,
            TipoComportamientoCompra.MINIMALISTA: 35.0
        }
        
        tiempo_base = tiempos_base[self.comportamiento_dominante]
        
        # Ajustar por rasgos
        tiempo_base *= (0.5 + rasgos.planificacion * 1.0)
        tiempo_base *= (0.7 + rasgos.responsabilidad * 0.6)
        tiempo_base /= (0.8 + rasgos.impulsividad * 0.4)
        
        return max(1.0, tiempo_base)
    
    def _calcular_tendencia_negociacion(self) -> float:
        """Calcula tendencia a negociar precios"""
        
        rasgos = self.perfil.rasgos_psicologicos
        
        tendencia = (
            rasgos.importancia_precio * 0.4 +
            rasgos.extraversion * 0.3 +
            (1.0 - rasgos.amabilidad) * 0.2 +
            self.perfil.experiencia_mercado * 0.1
        )
        
        # Ajustar por contexto socioeconómico
        if self.perfil.contexto_socioeconomico.nivel_educativo.value in ['universitario', 'postgrado']:
            tendencia += 0.1
        
        if self.perfil.contexto_socioeconomico.conocimiento_financiero > 0.7:
            tendencia += 0.15
        
        return max(0.0, min(1.0, tendencia))
    
    def _calcular_factor_lealtad(self) -> float:
        """Calcula factor de lealtad a marcas/vendedores"""
        
        rasgos = self.perfil.rasgos_psicologicos
        
        lealtad = (
            rasgos.responsabilidad * 0.3 +
            rasgos.importancia_marca * 0.3 +
            (1.0 - rasgos.apertura) * 0.2 +
            rasgos.conformidad_social * 0.2
        )
        
        return max(0.1, min(0.9, lealtad))
    
    def _calcular_propension_riesgo(self) -> float:
        """Calcula propensión al riesgo en compras"""
        
        rasgos = self.perfil.rasgos_psicologicos
        
        propension = (
            (1.0 - rasgos.aversion_riesgo) * 0.4 +
            rasgos.apertura * 0.3 +
            rasgos.impulsividad * 0.2 +
            self.perfil.experiencia_mercado * 0.1
        )
        
        return max(0.0, min(1.0, propension))
    
    def evaluar_opcion_compra(self, bien: BienHiperrealista, precio: float, 
                            vendedor: str, contexto: ContextoCompra) -> Dict[str, Any]:
        """Evalúa una opción de compra y retorna puntuación detallada"""
        
        evaluacion = {
            'puntuacion_total': 0.0,
            'criterios_cumplidos': {},
            'factores_decision': {},
            'tiempo_decision_estimado': 0.0,
            'probabilidad_compra': 0.0,
            'recomendaria_negociar': False
        }
        
        # Evaluar cada criterio
        puntuacion_total = 0.0
        peso_total = 0.0
        
        for nombre_criterio, criterio in self.criterios_decision.items():
            valor_bien = self._obtener_valor_criterio(bien, nombre_criterio, vendedor)
            
            # Verificar si cumple el umbral mínimo
            cumple_minimo = valor_bien >= criterio.umbral_minimo
            
            if criterio.es_eliminatorio and not cumple_minimo:
                evaluacion['puntuacion_total'] = 0.0
                evaluacion['criterios_cumplidos'][nombre_criterio] = False
                return evaluacion
            
            # Calcular puntuación del criterio
            if valor_bien >= criterio.preferencia_maxima:
                puntuacion_criterio = 1.0
            elif valor_bien >= criterio.umbral_minimo:
                rango = criterio.preferencia_maxima - criterio.umbral_minimo
                puntuacion_criterio = (valor_bien - criterio.umbral_minimo) / rango if rango > 0 else 1.0
            else:
                puntuacion_criterio = 0.3  # Penalización pero no eliminatorio
            
            puntuacion_total += puntuacion_criterio * criterio.peso
            peso_total += criterio.peso
            
            evaluacion['criterios_cumplidos'][nombre_criterio] = cumple_minimo
            evaluacion['factores_decision'][nombre_criterio] = {
                'valor': valor_bien,
                'puntuacion': puntuacion_criterio,
                'peso': criterio.peso
            }
        
        # Normalizar puntuación
        if peso_total > 0:
            evaluacion['puntuacion_total'] = puntuacion_total / peso_total
        
        # Aplicar factores contextuales
        evaluacion = self._aplicar_factores_contextuales(evaluacion, bien, contexto)
        
        # Aplicar sesgos cognitivos
        evaluacion = self._aplicar_sesgos_cognitivos(evaluacion, bien, precio)
        
        # Aplicar influencias sociales
        evaluacion = self._aplicar_influencias_sociales(evaluacion, bien)
        
        # Calcular tiempo de decisión
        evaluacion['tiempo_decision_estimado'] = self._calcular_tiempo_decision(contexto, evaluacion['puntuacion_total'])
        
        # Calcular probabilidad final de compra
        evaluacion['probabilidad_compra'] = self._calcular_probabilidad_compra(evaluacion)
        
        # Recomendar negociación
        evaluacion['recomendaria_negociar'] = self._deberia_negociar(precio, bien, evaluacion)
        
        return evaluacion
    
    def _obtener_valor_criterio(self, bien: BienHiperrealista, criterio: str, vendedor: str) -> float:
        """Obtiene el valor de un criterio específico para un bien"""
        
        if criterio == 'precio':
            # Normalizar precio (valor más bajo = mejor puntuación)
            precio_normalizado = min(1.0, 50.0 / max(1.0, bien.precio_base_sugerido))
            return precio_normalizado
        
        elif criterio == 'calidad':
            return bien.factor_calidad_global
        
        elif criterio == 'marca':
            return bien.atributos_calidad.marca_prestigio
        
        elif criterio == 'sostenibilidad':
            return bien.puntuacion_sostenibilidad
        
        elif criterio == 'conveniencia':
            # Basado en transportabilidad y disponibilidad
            return bien.propiedades_fisicas.transportabilidad * 0.7 + 0.3
        
        elif criterio == 'popularidad':
            return bien.factores_sociales.popularidad_general
        
        elif criterio == 'novedad':
            # Basado en tendencia de crecimiento e innovación
            return bien.factores_sociales.tendencia_crecimiento * 0.5 + bien.atributos_calidad.innovacion_tecnologica * 0.5
        
        elif criterio == 'seguridad':
            # Basado en garantía, certificaciones y factor de seguridad emocional
            factor_garantia = min(1.0, bien.atributos_calidad.garantia_meses / 24.0)
            factor_cert = len(bien.atributos_calidad.certificaciones) / 5.0
            return (factor_garantia * 0.4 + factor_cert * 0.3 + bien.impacto_emocional.factor_seguridad * 0.3)
        
        else:
            return 0.5  # Valor neutral por defecto
    
    def _aplicar_factores_contextuales(self, evaluacion: Dict[str, Any], 
                                     bien: BienHiperrealista, contexto: ContextoCompra) -> Dict[str, Any]:
        """Aplica factores contextuales a la evaluación"""
        
        factor_contexto = 1.0
        
        # Factor de urgencia
        if contexto.urgencia > 0.7:
            factor_contexto *= 1.2  # Aumentar probabilidad cuando es urgente
            evaluacion['tiempo_decision_estimado'] *= 0.3  # Reducir tiempo de decisión
        
        # Factor de presupuesto
        if contexto.presupuesto_disponible > 0 and bien.precio_base_sugerido > contexto.presupuesto_disponible:
            factor_contexto *= 0.3  # Penalizar fuertemente si excede presupuesto
        
        # Factor de tiempo disponible
        if contexto.tiempo_disponible < 0.3:
            if self.comportamiento_dominante in [TipoComportamientoCompra.COMPARADOR, TipoComportamientoCompra.PLANIFICADO]:
                factor_contexto *= 0.6  # Penalizar compradores que necesitan tiempo
        
        # Factor de estado emocional
        if contexto.estado_emocional > 0.8:
            if self.comportamiento_dominante == TipoComportamientoCompra.IMPULSIVO:
                factor_contexto *= 1.3  # Compras impulsivas cuando está feliz
        elif contexto.estado_emocional < 0.3:
            factor_contexto *= 0.7  # Reducir compras cuando está mal
        
        # Factor de compañía
        if contexto.compañia == 'familia':
            factor_contexto *= (1.0 + self.influencias_sociales['familia'] * 0.3)
        elif contexto.compañia == 'amigos':
            factor_contexto *= (1.0 + self.influencias_sociales['amigos'] * 0.3)
        
        # Factor de ubicación
        if contexto.ubicacion == 'online':
            if self.perfil.preferencias_consumo.preferencia_compras_online > 0.7:
                factor_contexto *= 1.1
            elif self.perfil.preferencias_consumo.preferencia_compras_online < 0.3:
                factor_contexto *= 0.8
        
        # Aplicar factor a puntuación total
        evaluacion['puntuacion_total'] *= factor_contexto
        evaluacion['puntuacion_total'] = max(0.0, min(1.0, evaluacion['puntuacion_total']))
        
        return evaluacion
    
    def _aplicar_sesgos_cognitivos(self, evaluacion: Dict[str, Any], 
                                 bien: BienHiperrealista, precio: float) -> Dict[str, Any]:
        """Aplica sesgos cognitivos a la evaluación"""
        
        # Sesgo de anclaje
        if hasattr(self, 'precio_ancla') and self.precio_ancla:
            if precio < self.precio_ancla:
                evaluacion['puntuacion_total'] *= (1.0 + self.sesgos_cognitivos['anclaje'] * 0.2)
            else:
                evaluacion['puntuacion_total'] *= (1.0 - self.sesgos_cognitivos['anclaje'] * 0.1)
        
        # Sesgo de disponibilidad (experiencias recientes)
        experiencias_recientes = [exp for exp in self.experiencias_compra[-5:] if exp.bien == bien.nombre]
        if experiencias_recientes:
            satisfaccion_promedio = sum(exp.satisfaccion for exp in experiencias_recientes) / len(experiencias_recientes)
            ajuste = (satisfaccion_promedio - 0.5) * self.sesgos_cognitivos['disponibilidad'] * 0.3
            evaluacion['puntuacion_total'] += ajuste
        
        # Sesgo de escasez
        if bien.factores_sociales.exclusividad > 0.7:
            evaluacion['puntuacion_total'] *= (1.0 + self.sesgos_cognitivos['escasez'] * 0.2)
        
        # Normalizar
        evaluacion['puntuacion_total'] = max(0.0, min(1.0, evaluacion['puntuacion_total']))
        
        return evaluacion
    
    def _aplicar_influencias_sociales(self, evaluacion: Dict[str, Any], bien: BienHiperrealista) -> Dict[str, Any]:
        """Aplica influencias sociales a la evaluación"""
        
        # Influencia de popularidad
        if bien.factores_sociales.popularidad_general > 0.7:
            ajuste_popularidad = self.influencias_sociales['tendencias'] * 0.15
            evaluacion['puntuacion_total'] += ajuste_popularidad
        
        # Influencia de celebridades
        if bien.factores_sociales.influencia_celebridades > 0.5:
            ajuste_celebridades = self.influencias_sociales['celebridades'] * 0.2
            evaluacion['puntuacion_total'] += ajuste_celebridades
        
        # Efecto viral
        if bien.factores_sociales.factor_viral > 0.3:
            ajuste_viral = self.influencias_sociales['amigos'] * 0.1
            evaluacion['puntuacion_total'] += ajuste_viral
        
        # Normalizar
        evaluacion['puntuacion_total'] = max(0.0, min(1.0, evaluacion['puntuacion_total']))
        
        return evaluacion
    
    def _calcular_tiempo_decision(self, contexto: ContextoCompra, puntuacion: float) -> float:
        """Calcula tiempo de decisión en minutos"""
        
        tiempo_base = self.tiempo_promedio_decision
        
        # Ajustar por contexto
        if contexto.urgencia > 0.7:
            tiempo_base *= 0.3
        elif contexto.tiempo_disponible < 0.3:
            tiempo_base *= 0.5
        
        # Ajustar por puntuación (decisiones más fáciles son más rápidas)
        if puntuacion > 0.8:
            tiempo_base *= 0.7
        elif puntuacion < 0.3:
            tiempo_base *= 1.5
        
        # Ajustar por comportamiento
        if self.comportamiento_dominante == TipoComportamientoCompra.IMPULSIVO:
            tiempo_base *= 0.5
        elif self.comportamiento_dominante == TipoComportamientoCompra.COMPARADOR:
            tiempo_base *= 1.5
        
        return max(0.5, tiempo_base)
    
    def _calcular_probabilidad_compra(self, evaluacion: Dict[str, Any]) -> float:
        """Calcula probabilidad final de compra"""
        
        # Base en puntuación
        probabilidad = evaluacion['puntuacion_total']
        
        # Ajustar por comportamiento dominante
        if self.comportamiento_dominante == TipoComportamientoCompra.IMPULSIVO:
            probabilidad = min(0.95, probabilidad * 1.2)
        elif self.comportamiento_dominante == TipoComportamientoCompra.CONSERVADOR:
            probabilidad = probabilidad * 0.8
        
        # Ajustar por estado del perfil
        probabilidad *= (0.8 + self.perfil.satisfaccion_vida * 0.4)
        probabilidad *= (0.9 + self.perfil.confianza_economia * 0.2)
        probabilidad *= (1.1 - self.perfil.stress_financiero * 0.3)
        
        return max(0.0, min(1.0, probabilidad))
    
    def _deberia_negociar(self, precio: float, bien: BienHiperrealista, evaluacion: Dict[str, Any]) -> bool:
        """Determina si debería intentar negociar el precio"""
        
        # No negociar si la puntuación ya es muy alta
        if evaluacion['puntuacion_total'] > 0.9:
            return False
        
        # No negociar si es muy barato
        if precio < bien.economicas.costo_produccion_base * 1.2:
            return False
        
        # Negociar basándose en tendencia personal
        return random.random() < self.tendencia_negociacion
    
    def registrar_experiencia_compra(self, experiencia: ExperienciaCompra):
        """Registra una nueva experiencia de compra"""
        
        self.experiencias_compra.append(experiencia)
        
        # Actualizar listas basándose en la experiencia
        if experiencia.satisfaccion > 0.8:
            # Buena experiencia
            if len(self.marcas_favoritas) < 10:  # Limitar tamaño
                # Agregar marca (simplificado - usamos nombre del bien)
                self.marcas_favoritas.add(experiencia.bien)
        elif experiencia.satisfaccion < 0.3:
            # Mala experiencia
            self.vendedores_bloqueados.add(experiencia.vendedor)
        
        # Actualizar métricas
        self._actualizar_metricas_comportamiento()
        
        # Mantener historial limitado
        if len(self.experiencias_compra) > 100:
            self.experiencias_compra = self.experiencias_compra[-100:]
    
    def _actualizar_metricas_comportamiento(self):
        """Actualiza métricas de comportamiento basándose en experiencias"""
        
        if len(self.experiencias_compra) < 5:
            return
        
        experiencias_recientes = self.experiencias_compra[-20:]
        
        # Actualizar tiempo promedio de decisión
        tiempos = [exp.tiempo_decision for exp in experiencias_recientes]
        self.tiempo_promedio_decision = sum(tiempos) / len(tiempos)
        
        # Actualizar factor de lealtad basándose en repetición de compras
        bienes_comprados = [exp.bien for exp in experiencias_recientes]
        repeticiones = len(bienes_comprados) - len(set(bienes_comprados))
        if len(bienes_comprados) > 0:
            tasa_repeticion = repeticiones / len(bienes_comprados)
            self.factor_lealtad = (self.factor_lealtad * 0.8 + tasa_repeticion * 0.2)
    
    def get_estadisticas_comportamiento(self) -> Dict[str, Any]:
        """Obtiene estadísticas del comportamiento de compra"""
        
        stats = {
            'comportamiento_dominante': self.comportamiento_dominante.value,
            'comportamientos_secundarios': [c.value for c in self.comportamientos_secundarios],
            'tiempo_promedio_decision': self.tiempo_promedio_decision,
            'tendencia_negociacion': self.tendencia_negociacion,
            'factor_lealtad': self.factor_lealtad,
            'propension_riesgo': self.propension_riesgo_compra,
            'experiencias_totales': len(self.experiencias_compra),
            'vendedores_bloqueados': len(self.vendedores_bloqueados),
            'marcas_favoritas': len(self.marcas_favoritas),
            'criterios_principales': list(self.criterios_decision.keys())
        }
        
        # Satisfacción promedio
        if self.experiencias_compra:
            satisfacciones = [exp.satisfaccion for exp in self.experiencias_compra]
            stats['satisfaccion_promedio'] = sum(satisfacciones) / len(satisfacciones)
        else:
            stats['satisfaccion_promedio'] = 0.5
        
        # Tasa de negociación exitosa
        negociaciones = [exp for exp in self.experiencias_compra if exp.resultado_negociacion is not None]
        if negociaciones:
            exitosas = [exp for exp in negociaciones if exp.resultado_negociacion > 0]
            stats['tasa_negociacion_exitosa'] = len(exitosas) / len(negociaciones)
        else:
            stats['tasa_negociacion_exitosa'] = 0.0
        
        return stats
