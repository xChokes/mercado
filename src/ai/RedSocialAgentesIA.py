"""
Redes Sociales de Agentes IA
============================

Implementa redes sociales inteligentes entre agentes, propagación de información,
formación de coaliciones y inteligencia colectiva emergente.
"""

import numpy as np
import random
from typing import Dict, List, Set, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict, deque
import threading
import time
import math
from enum import Enum

from .AgentMemorySystem import AgentMemorySystem, Decision
from .AgentCommunicationProtocol import TipoMensaje, PrioridadMensaje


class TipoRelacion(Enum):
    """Tipos de relaciones entre agentes"""
    COMPETENCIA = "competencia"
    COLABORACION = "colaboracion"
    PROVEEDOR_CLIENTE = "proveedor_cliente"
    ALIANZA_ESTRATEGICA = "alianza_estrategica"
    NEUTRAL = "neutral"
    CONFLICTO = "conflicto"


class TipoRed(Enum):
    """Tipos de redes sociales"""
    COMERCIAL = "comercial"
    INFORMACION = "informacion"
    CONFIANZA = "confianza"
    COLABORACION = "colaboracion"
    COMPETENCIA = "competencia"


@dataclass
class RelacionAgente:
    """Relación entre dos agentes"""
    agente_a: str
    agente_b: str
    tipo: TipoRelacion
    fuerza: float  # 0.0 a 1.0
    confianza: float  # 0.0 a 1.0
    historial_interacciones: int
    ultima_interaccion: datetime
    beneficio_mutuo: float
    reputacion_cruzada: float
    
    def actualizar_por_interaccion(self, resultado_positivo: bool, impacto: float = 0.1):
        """Actualiza la relación basándose en una interacción"""
        self.historial_interacciones += 1
        self.ultima_interaccion = datetime.now()
        
        if resultado_positivo:
            self.fuerza = min(1.0, self.fuerza + impacto)
            self.confianza = min(1.0, self.confianza + impacto * 0.5)
            self.beneficio_mutuo += impacto
        else:
            self.fuerza = max(0.0, self.fuerza - impacto)
            self.confianza = max(0.0, self.confianza - impacto * 0.7)
            self.beneficio_mutuo -= impacto * 0.5
        
        # Actualizar tipo de relación basándose en métricas
        self._actualizar_tipo_relacion()
    
    def _actualizar_tipo_relacion(self):
        """Actualiza el tipo de relación basándose en métricas actuales"""
        if self.confianza > 0.8 and self.beneficio_mutuo > 0.5:
            self.tipo = TipoRelacion.ALIANZA_ESTRATEGICA
        elif self.confianza > 0.6 and self.beneficio_mutuo > 0.2:
            self.tipo = TipoRelacion.COLABORACION
        elif self.confianza < 0.3 or self.beneficio_mutuo < -0.3:
            self.tipo = TipoRelacion.CONFLICTO
        elif abs(self.beneficio_mutuo) < 0.1:
            self.tipo = TipoRelacion.NEUTRAL
        else:
            # Mantener tipo actual o asignar por contexto
            # Si no hay cambios significativos, mantener relación existente
            return


@dataclass
class InformacionCompartida:
    """Información compartida en la red social"""
    id: str
    emisor: str
    contenido: Dict[str, Any]
    tipo_informacion: str  # 'precio', 'demanda', 'oportunidad', 'riesgo', etc.
    confiabilidad: float
    timestamp: datetime
    propagaciones: int = 0
    agentes_informados: Set[str] = field(default_factory=set)
    verificada: bool = False
    impacto_estimado: float = 0.0


@dataclass
class CoalicionAgentes:
    """Coalición de agentes trabajando juntos"""
    id: str
    nombre: str
    miembros: Set[str]
    lider: str
    objetivo: str
    beneficio_esperado: float
    recursos_compartidos: Dict[str, float]
    duracion_estimada: timedelta
    creada_en: datetime
    activa: bool = True
    progreso: float = 0.0
    decisiones_conjuntas: List[Dict[str, Any]] = field(default_factory=list)


class AnalyzadorReputacion:
    """Analizador de reputación de agentes en la red"""
    
    def __init__(self):
        self.reputaciones = defaultdict(lambda: {
            'confiabilidad': 0.5,
            'cooperacion': 0.5,
            'competencia': 0.5,
            'innovacion': 0.5,
            'estabilidad': 0.5
        })
        self.historial_evaluaciones = defaultdict(list)
    
    def evaluar_reputacion(self, agente: str, categoria: str, 
                          evaluador: str, puntuacion: float):
        """Evalúa la reputación de un agente en una categoría"""
        if categoria not in self.reputaciones[agente]:
            self.reputaciones[agente][categoria] = 0.5
        
        # Promedio ponderado con evaluación anterior
        peso_nuevo = 0.3
        puntuacion_anterior = self.reputaciones[agente][categoria]
        nueva_puntuacion = (puntuacion_anterior * (1 - peso_nuevo) + 
                           puntuacion * peso_nuevo)
        
        self.reputaciones[agente][categoria] = max(0.0, min(1.0, nueva_puntuacion))
        
        # Registrar evaluación
        self.historial_evaluaciones[agente].append({
            'categoria': categoria,
            'evaluador': evaluador,
            'puntuacion': puntuacion,
            'timestamp': datetime.now()
        })
    
    def get_reputacion_global(self, agente: str) -> float:
        """Obtiene reputación global del agente"""
        if agente not in self.reputaciones:
            return 0.5
        
        reputacion = self.reputaciones[agente]
        # Promedio ponderado de todas las categorías
        return (reputacion['confiabilidad'] * 0.3 +
                reputacion['cooperacion'] * 0.25 +
                reputacion['competencia'] * 0.2 +
                reputacion['innovacion'] * 0.15 +
                reputacion['estabilidad'] * 0.1)
    
    def get_agentes_por_reputacion(self, categoria: str = None, 
                                  min_reputacion: float = 0.0) -> List[Tuple[str, float]]:
        """Obtiene agentes ordenados por reputación"""
        agentes_reputacion = []
        
        for agente in self.reputaciones:
            if categoria:
                reputacion = self.reputaciones[agente].get(categoria, 0.5)
            else:
                reputacion = self.get_reputacion_global(agente)
            
            if reputacion >= min_reputacion:
                agentes_reputacion.append((agente, reputacion))
        
        return sorted(agentes_reputacion, key=lambda x: x[1], reverse=True)


class PropagadorInformacion:
    """Sistema de propagación de información en la red"""
    
    def __init__(self, red_social):
        self.red_social = red_social
        self.velocidad_propagacion = {}  # Por tipo de información
        self.filtros_propagacion = {}
        self.modelo_contagio = "epidemiologico"
    
    def propagar_informacion(self, informacion: InformacionCompartida, 
                           agentes_iniciales: List[str]) -> Dict[str, Any]:
        """Propaga información através de la red social"""
        resultado_propagacion = {
            'informacion_id': informacion.id,
            'agentes_alcanzados': set(agentes_iniciales),
            'rondas_propagacion': 0,
            'velocidad_promedio': 0.0,
            'distorsion_informacion': 0.0,
            'agentes_por_ronda': [len(agentes_iniciales)]
        }
        
        # Configurar parámetros de propagación
        probabilidad_base = self._calcular_probabilidad_base(informacion)
        resistencia_red = self._calcular_resistencia_red(informacion.tipo_informacion)
        
        # Inicializar agentes informados
        agentes_actuales = set(agentes_iniciales)
        informacion.agentes_informados.update(agentes_iniciales)
        
        # Propagación iterativa
        max_rondas = 10
        for ronda in range(max_rondas):
            nuevos_agentes = set()
            
            for agente_emisor in agentes_actuales:
                # Obtener vecinos del agente
                vecinos = self.red_social.get_vecinos_agente(agente_emisor)
                
                for vecino in vecinos:
                    if vecino not in informacion.agentes_informados:
                        # Calcular probabilidad de transmisión
                        prob_transmision = self._calcular_probabilidad_transmision(
                            agente_emisor, vecino, informacion, probabilidad_base
                        )
                        
                        if random.random() < prob_transmision:
                            nuevos_agentes.add(vecino)
                            informacion.agentes_informados.add(vecino)
            
            if not nuevos_agentes:
                break  # No hay más propagación
            
            agentes_actuales = nuevos_agentes
            resultado_propagacion['agentes_alcanzados'].update(nuevos_agentes)
            resultado_propagacion['agentes_por_ronda'].append(len(nuevos_agentes))
            resultado_propagacion['rondas_propagacion'] += 1
            
            # Aplicar distorsión de información
            informacion.confiabilidad *= 0.95  # Ligera degradación
        
        # Calcular métricas finales
        resultado_propagacion['velocidad_promedio'] = (
            len(resultado_propagacion['agentes_alcanzados']) / 
            max(1, resultado_propagacion['rondas_propagacion'])
        )
        resultado_propagacion['distorsion_informacion'] = 1.0 - informacion.confiabilidad
        
        informacion.propagaciones += 1
        
        return resultado_propagacion
    
    def _calcular_probabilidad_base(self, informacion: InformacionCompartida) -> float:
        """Calcula probabilidad base de propagación"""
        # Factores que afectan propagación
        factor_confiabilidad = informacion.confiabilidad
        factor_urgencia = 1.0 if informacion.tipo_informacion in ['riesgo', 'oportunidad'] else 0.7
        factor_novedad = max(0.3, 1.0 - informacion.propagaciones * 0.1)
        
        return factor_confiabilidad * factor_urgencia * factor_novedad * 0.3
    
    def _calcular_resistencia_red(self, tipo_informacion: str) -> float:
        """Calcula resistencia de la red a cierto tipo de información"""
        resistencias = {
            'precio': 0.1,  # Información de precios se propaga fácil
            'riesgo': 0.2,  # Información de riesgo encuentra más resistencia
            'oportunidad': 0.15,
            'tecnologia': 0.25,
            'regulacion': 0.3
        }
        return resistencias.get(tipo_informacion, 0.2)
    
    def _calcular_probabilidad_transmision(self, emisor: str, receptor: str,
                                         informacion: InformacionCompartida,
                                         prob_base: float) -> float:
        """Calcula probabilidad de transmisión entre dos agentes específicos"""
        # Obtener relación entre agentes
        relacion = self.red_social.get_relacion_agentes(emisor, receptor)
        
        if not relacion:
            return prob_base * 0.3  # Transmisión débil sin relación
        
        # Factores de la relación
        factor_confianza = relacion.confianza
        factor_fuerza = relacion.fuerza
        factor_tipo_relacion = self._factor_tipo_relacion(relacion.tipo, informacion.tipo_informacion)
        
        # Reputación del emisor
        reputacion_emisor = self.red_social.analizador_reputacion.get_reputacion_global(emisor)
        
        probabilidad = (prob_base * factor_confianza * factor_fuerza * 
                       factor_tipo_relacion * reputacion_emisor)
        
        return min(1.0, probabilidad)
    
    def _factor_tipo_relacion(self, tipo_relacion: TipoRelacion, tipo_informacion: str) -> float:
        """Factor basado en tipo de relación y tipo de información"""
        factores = {
            TipoRelacion.ALIANZA_ESTRATEGICA: {
                'precio': 0.9, 'riesgo': 0.95, 'oportunidad': 0.9
            },
            TipoRelacion.COLABORACION: {
                'precio': 0.8, 'riesgo': 0.85, 'oportunidad': 0.8
            },
            TipoRelacion.COMPETENCIA: {
                'precio': 0.3, 'riesgo': 0.6, 'oportunidad': 0.2
            },
            TipoRelacion.CONFLICTO: {
                'precio': 0.1, 'riesgo': 0.3, 'oportunidad': 0.1
            },
            TipoRelacion.NEUTRAL: {
                'precio': 0.5, 'riesgo': 0.5, 'oportunidad': 0.4
            }
        }
        
        return factores.get(tipo_relacion, {}).get(tipo_informacion, 0.5)


class FormadorCoaliciones:
    """Sistema de formación y gestión de coaliciones"""
    
    def __init__(self, red_social):
        self.red_social = red_social
        self.coaliciones_activas: Dict[str, CoalicionAgentes] = {}
        self.algoritmo_formacion = "estabilidad_core"
        self.historial_coaliciones = []
    
    def identificar_oportunidades_coalicion(self) -> List[Dict[str, Any]]:
        """Identifica oportunidades para formar coaliciones"""
        oportunidades = []
        
        # 1. Coaliciones por complementariedad de recursos
        oportunidades.extend(self._identificar_coaliciones_recursos())
        
        # 2. Coaliciones por objetivos comunes
        oportunidades.extend(self._identificar_coaliciones_objetivos())
        
        # 3. Coaliciones defensivas contra competencia
        oportunidades.extend(self._identificar_coaliciones_defensivas())
        
        # 4. Coaliciones de innovación
        oportunidades.extend(self._identificar_coaliciones_innovacion())
        
        return sorted(oportunidades, key=lambda x: x['beneficio_estimado'], reverse=True)
    
    def _identificar_coaliciones_recursos(self) -> List[Dict[str, Any]]:
        """Identifica coaliciones basadas en complementariedad de recursos"""
        oportunidades = []
        
        agentes = list(self.red_social.agentes_registrados)
        
        # Analizar pares de agentes
        for i in range(len(agentes)):
            for j in range(i + 1, len(agentes)):
                agente_a, agente_b = agentes[i], agentes[j]
                
                # Evaluar complementariedad (simulado)
                complementariedad = self._evaluar_complementariedad_recursos(agente_a, agente_b)
                
                if complementariedad > 0.6:
                    oportunidad = {
                        'tipo': 'recursos',
                        'agentes': [agente_a, agente_b],
                        'objetivo': 'complementariedad_recursos',
                        'beneficio_estimado': complementariedad,
                        'duracion_estimada': timedelta(days=90),
                        'recursos_necesarios': {'coordinacion': 0.2, 'inversion': 0.1}
                    }
                    oportunidades.append(oportunidad)
        
        return oportunidades
    
    def _evaluar_complementariedad_recursos(self, agente_a: str, agente_b: str) -> float:
        """Evalúa complementariedad de recursos entre dos agentes"""
        # Simulación de evaluación de recursos
        # En implementación real, consultaría perfiles de agentes
        
        # Factores simulados
        diferencia_especialidades = random.uniform(0.3, 0.9)
        sinergias_potenciales = random.uniform(0.2, 0.8)
        compatibilidad_operacional = random.uniform(0.4, 0.9)
        
        # Evaluar relación existente
        relacion = self.red_social.get_relacion_agentes(agente_a, agente_b)
        factor_relacion = relacion.confianza if relacion else 0.5
        
        complementariedad = (diferencia_especialidades * 0.4 +
                           sinergias_potenciales * 0.3 +
                           compatibilidad_operacional * 0.2 +
                           factor_relacion * 0.1)
        
        return complementariedad
    
    def _identificar_coaliciones_objetivos(self) -> List[Dict[str, Any]]:
        """Identifica coaliciones basadas en objetivos comunes"""
        oportunidades = []
        
        # Agrupar agentes por objetivos similares (simulado)
        objetivos_comunes = {
            'expansion_mercado': random.sample(list(self.red_social.agentes_registrados), 
                                             min(4, len(self.red_social.agentes_registrados))),
            'reduccion_costos': random.sample(list(self.red_social.agentes_registrados), 
                                            min(3, len(self.red_social.agentes_registrados))),
            'innovacion_tecnologica': random.sample(list(self.red_social.agentes_registrados), 
                                                   min(5, len(self.red_social.agentes_registrados)))
        }
        
        for objetivo, agentes_objetivo in objetivos_comunes.items():
            if len(agentes_objetivo) >= 2:
                beneficio_estimado = min(0.9, len(agentes_objetivo) * 0.15)
                
                oportunidad = {
                    'tipo': 'objetivos',
                    'agentes': agentes_objetivo,
                    'objetivo': objetivo,
                    'beneficio_estimado': beneficio_estimado,
                    'duracion_estimada': timedelta(days=120),
                    'recursos_necesarios': {'coordinacion': 0.3, 'inversion': 0.2}
                }
                oportunidades.append(oportunidad)
        
        return oportunidades
    
    def _identificar_coaliciones_defensivas(self) -> List[Dict[str, Any]]:
        """Identifica coaliciones defensivas contra amenazas comunes"""
        oportunidades = []
        
        # Identificar agentes bajo presión competitiva similar
        agentes_vulnerables = []
        for agente in self.red_social.agentes_registrados:
            reputacion = self.red_social.analizador_reputacion.get_reputacion_global(agente)
            if reputacion < 0.6:  # Agentes con reputación baja
                agentes_vulnerables.append(agente)
        
        if len(agentes_vulnerables) >= 2:
            oportunidad = {
                'tipo': 'defensiva',
                'agentes': agentes_vulnerables[:4],  # Máximo 4 agentes
                'objetivo': 'defensa_competitiva',
                'beneficio_estimado': 0.7,
                'duracion_estimada': timedelta(days=60),
                'recursos_necesarios': {'coordinacion': 0.4, 'inversion': 0.1}
            }
            oportunidades.append(oportunidad)
        
        return oportunidades
    
    def _identificar_coaliciones_innovacion(self) -> List[Dict[str, Any]]:
        """Identifica coaliciones para proyectos de innovación"""
        oportunidades = []
        
        # Identificar agentes con alta reputación en innovación
        agentes_innovadores = []
        for agente in self.red_social.agentes_registrados:
            reputacion_innovacion = self.red_social.analizador_reputacion.reputaciones[agente].get('innovacion', 0.5)
            if reputacion_innovacion > 0.7:
                agentes_innovadores.append(agente)
        
        if len(agentes_innovadores) >= 2:
            oportunidad = {
                'tipo': 'innovacion',
                'agentes': agentes_innovadores[:3],  # Coaliciones pequeñas para innovación
                'objetivo': 'proyecto_innovacion',
                'beneficio_estimado': 0.8,
                'duracion_estimada': timedelta(days=180),
                'recursos_necesarios': {'coordinacion': 0.3, 'inversion': 0.4}
            }
            oportunidades.append(oportunidad)
        
        return oportunidades
    
    def formar_coalicion(self, oportunidad: Dict[str, Any]) -> Optional[CoalicionAgentes]:
        """Forma una coalición basándose en una oportunidad identificada"""
        
        # Verificar disponibilidad de agentes
        agentes_disponibles = [
            agente for agente in oportunidad['agentes']
            if not self._agente_en_coalicion_activa(agente)
        ]
        
        if len(agentes_disponibles) < 2:
            return None
        
        # Seleccionar líder (agente con mejor reputación)
        lider = max(agentes_disponibles, 
                   key=lambda a: self.red_social.analizador_reputacion.get_reputacion_global(a))
        
        # Crear coalición
        coalicion_id = f"coalicion_{int(time.time())}"
        coalicion = CoalicionAgentes(
            id=coalicion_id,
            nombre=f"Coalición {oportunidad['objetivo']}",
            miembros=set(agentes_disponibles),
            lider=lider,
            objetivo=oportunidad['objetivo'],
            beneficio_esperado=oportunidad['beneficio_estimado'],
            recursos_compartidos=oportunidad['recursos_necesarios'],
            duracion_estimada=oportunidad['duracion_estimada'],
            creada_en=datetime.now()
        )
        
        # Registrar coalición
        self.coaliciones_activas[coalicion_id] = coalicion
        
        # Notificar a agentes miembros
        self._notificar_formacion_coalicion(coalicion)
        
        print(f"[COALICIONES] Formada coalición {coalicion.nombre} con {len(coalicion.miembros)} miembros")
        
        return coalicion
    
    def _agente_en_coalicion_activa(self, agente: str) -> bool:
        """Verifica si un agente está en una coalición activa"""
        for coalicion in self.coaliciones_activas.values():
            if coalicion.activa and agente in coalicion.miembros:
                return True
        return False
    
    def _notificar_formacion_coalicion(self, coalicion: CoalicionAgentes):
        """Notifica a los miembros sobre la formación de la coalición"""
        for miembro in coalicion.miembros:
            # En implementación real, enviaría mensaje al agente
            print(f"[COALICIONES] Notificando a {miembro} sobre coalición {coalicion.nombre}")
    
    def gestionar_coaliciones_activas(self) -> Dict[str, Any]:
        """Gestiona coaliciones activas, evalúa progreso y toma decisiones"""
        gestion = {
            'coaliciones_evaluadas': 0,
            'coaliciones_renovadas': 0,
            'coaliciones_disueltas': 0,
            'nuevas_decisiones': 0
        }
        
        for coalicion_id, coalicion in list(self.coaliciones_activas.items()):
            if not coalicion.activa:
                continue
            
            # Evaluar progreso
            progreso_anterior = coalicion.progreso
            coalicion.progreso = self._evaluar_progreso_coalicion(coalicion)
            gestion['coaliciones_evaluadas'] += 1
            
            # Tomar decisiones de gestión
            decision_gestion = self._decidir_gestion_coalicion(coalicion)
            
            if decision_gestion == 'renovar':
                self._renovar_coalicion(coalicion)
                gestion['coaliciones_renovadas'] += 1
            elif decision_gestion == 'disolver':
                self._disolver_coalicion(coalicion_id, coalicion)
                gestion['coaliciones_disueltas'] += 1
            elif decision_gestion == 'nueva_decision':
                self._facilitar_decision_conjunta(coalicion)
                gestion['nuevas_decisiones'] += 1
        
        return gestion
    
    def _evaluar_progreso_coalicion(self, coalicion: CoalicionAgentes) -> float:
        """Evalúa el progreso de una coalición"""
        # Factores de progreso
        tiempo_transcurrido = (datetime.now() - coalicion.creada_en).total_seconds()
        tiempo_esperado = coalicion.duracion_estimada.total_seconds()
        factor_tiempo = min(1.0, tiempo_transcurrido / tiempo_esperado)
        
        # Evaluar cumplimiento de objetivos (simulado)
        factor_objetivos = random.uniform(0.3, 0.9)
        
        # Evaluar cohesión del grupo
        factor_cohesion = self._evaluar_cohesion_coalicion(coalicion)
        
        progreso = factor_tiempo * 0.3 + factor_objetivos * 0.5 + factor_cohesion * 0.2
        return min(1.0, progreso)
    
    def _evaluar_cohesion_coalicion(self, coalicion: CoalicionAgentes) -> float:
        """Evalúa la cohesión interna de la coalición"""
        if len(coalicion.miembros) < 2:
            return 1.0
        
        # Evaluar relaciones entre miembros
        relaciones_internas = []
        miembros = list(coalicion.miembros)
        
        for i in range(len(miembros)):
            for j in range(i + 1, len(miembros)):
                relacion = self.red_social.get_relacion_agentes(miembros[i], miembros[j])
                if relacion:
                    relaciones_internas.append(relacion.fuerza * relacion.confianza)
                else:
                    relaciones_internas.append(0.3)  # Relación débil por defecto
        
        cohesion = np.mean(relaciones_internas) if relaciones_internas else 0.5
        return cohesion
    
    def _decidir_gestion_coalicion(self, coalicion: CoalicionAgentes) -> str:
        """Decide qué acción tomar con una coalición"""
        # Evaluar tiempo restante
        tiempo_transcurrido = datetime.now() - coalicion.creada_en
        tiempo_restante = coalicion.duracion_estimada - tiempo_transcurrido
        
        if tiempo_restante.total_seconds() <= 0:
            if coalicion.progreso > 0.8:
                return 'renovar'  # Coalición exitosa, renovar
            else:
                return 'disolver'  # No tuvo éxito, disolver
        
        # Evaluar si necesita nuevas decisiones
        if len(coalicion.decisiones_conjuntas) == 0 or coalicion.progreso > 0.3:
            return 'nueva_decision'
        
        return 'continuar'  # Mantener como está
    
    def _renovar_coalicion(self, coalicion: CoalicionAgentes):
        """Renueva una coalición exitosa"""
        coalicion.duracion_estimada = timedelta(days=90)  # Extensión estándar
        coalicion.creada_en = datetime.now()  # Reiniciar cronómetro
        coalicion.progreso = 0.0
        print(f"[COALICIONES] Renovada coalición {coalicion.nombre}")
    
    def _disolver_coalicion(self, coalicion_id: str, coalicion: CoalicionAgentes):
        """Disuelve una coalición"""
        coalicion.activa = False
        self.historial_coaliciones.append(coalicion)
        del self.coaliciones_activas[coalicion_id]
        print(f"[COALICIONES] Disuelta coalición {coalicion.nombre}")
    
    def _facilitar_decision_conjunta(self, coalicion: CoalicionAgentes):
        """Facilita una decisión conjunta de la coalición"""
        # Generar decisión simulada
        decision = {
            'tipo': random.choice(['inversion', 'expansion', 'estrategia', 'operacion']),
            'descripcion': f"Decisión conjunta para {coalicion.objetivo}",
            'beneficio_estimado': random.uniform(0.1, 0.5),
            'riesgo_estimado': random.uniform(0.1, 0.3),
            'timestamp': datetime.now(),
            'consenso': random.uniform(0.6, 0.95)
        }
        
        coalicion.decisiones_conjuntas.append(decision)
        print(f"[COALICIONES] Nueva decisión conjunta en {coalicion.nombre}: {decision['tipo']}")


class RedSocialAgentesIA:
    """
    Red Social de Agentes con Inteligencia Artificial
    """
    
    def __init__(self):
        # Componentes principales
        self.agentes_registrados: Set[str] = set()
        self.relaciones: Dict[Tuple[str, str], RelacionAgente] = {}
        self.redes_especializadas: Dict[TipoRed, Dict] = {
            tipo: {} for tipo in TipoRed
        }
        
        # Sistemas especializados
        self.analizador_reputacion = AnalyzadorReputacion()
        self.propagador_informacion = PropagadorInformacion(self)
        self.formador_coaliciones = FormadorCoaliciones(self)
        
        # Información y comunicación
        self.informaciones_activas: Dict[str, InformacionCompartida] = {}
        self.canales_comunicacion: Dict[str, List[str]] = defaultdict(list)
        
        # Métricas de red
        self.centralidad_agentes: Dict[str, float] = {}
        self.clusters_detectados: List[Set[str]] = []
        self.densidad_red = 0.0
        self.eficiencia_comunicacion = 0.0
        
        # Control de procesamiento
        self.procesando = True
        self.intervalo_analisis = 30  # segundos
        
        # Hilo de análisis continuo
        self.hilo_analisis = threading.Thread(target=self._ciclo_analisis_red)
        self.hilo_analisis.daemon = True
        self.hilo_analisis.start()
        
        print("[RED SOCIAL IA] Sistema de red social de agentes inicializado")
    
    def registrar_agente(self, agente_id: str, perfil_inicial: Dict[str, Any] = None):
        """Registra un nuevo agente en la red social"""
        self.agentes_registrados.add(agente_id)
        
        # Inicializar reputación
        if perfil_inicial:
            for categoria, valor in perfil_inicial.items():
                if categoria in ['confiabilidad', 'cooperacion', 'competencia', 'innovacion', 'estabilidad']:
                    self.analizador_reputacion.reputaciones[agente_id][categoria] = valor
        
        # Recalcular métricas de red
        self._recalcular_metricas_red()
        
        print(f"[RED SOCIAL] Agente {agente_id} registrado en la red")
    
    def establecer_relacion(self, agente_a: str, agente_b: str,
                          tipo_relacion: TipoRelacion, fuerza_inicial: float = 0.5,
                          confianza_inicial: float = 0.5) -> RelacionAgente:
        """Establece una relación entre dos agentes"""
        # Asegurar orden consistente para la clave
        clave_relacion = tuple(sorted([agente_a, agente_b]))
        
        relacion = RelacionAgente(
            agente_a=clave_relacion[0],
            agente_b=clave_relacion[1],
            tipo=tipo_relacion,
            fuerza=fuerza_inicial,
            confianza=confianza_inicial,
            historial_interacciones=0,
            ultima_interaccion=datetime.now(),
            beneficio_mutuo=0.0,
            reputacion_cruzada=0.5
        )
        
        self.relaciones[clave_relacion] = relacion
        
        # Agregar a redes especializadas
        self._agregar_a_redes_especializadas(relacion)
        
        # Recalcular métricas
        self._recalcular_metricas_red()
        
        return relacion
    
    def get_relacion_agentes(self, agente_a: str, agente_b: str) -> Optional[RelacionAgente]:
        """Obtiene la relación entre dos agentes"""
        clave_relacion = tuple(sorted([agente_a, agente_b]))
        return self.relaciones.get(clave_relacion)
    
    def get_vecinos_agente(self, agente: str) -> List[str]:
        """Obtiene los vecinos (agentes conectados) de un agente"""
        vecinos = []
        for (agente_a, agente_b), relacion in self.relaciones.items():
            if agente_a == agente:
                vecinos.append(agente_b)
            elif agente_b == agente:
                vecinos.append(agente_a)
        return vecinos
    
    def _agregar_a_redes_especializadas(self, relacion: RelacionAgente):
        """Agrega relación a redes especializadas según su tipo"""
        # Red comercial
        if relacion.tipo in [TipoRelacion.PROVEEDOR_CLIENTE, TipoRelacion.COLABORACION]:
            if 'comercial' not in self.redes_especializadas[TipoRed.COMERCIAL]:
                self.redes_especializadas[TipoRed.COMERCIAL] = {}
            
            clave = (relacion.agente_a, relacion.agente_b)
            self.redes_especializadas[TipoRed.COMERCIAL][clave] = relacion
        
        # Red de confianza
        if relacion.confianza > 0.7:
            if 'confianza' not in self.redes_especializadas[TipoRed.CONFIANZA]:
                self.redes_especializadas[TipoRed.CONFIANZA] = {}
            
            clave = (relacion.agente_a, relacion.agente_b)
            self.redes_especializadas[TipoRed.CONFIANZA][clave] = relacion
        
        # Red de competencia
        if relacion.tipo == TipoRelacion.COMPETENCIA:
            if 'competencia' not in self.redes_especializadas[TipoRed.COMPETENCIA]:
                self.redes_especializadas[TipoRed.COMPETENCIA] = {}
            
            clave = (relacion.agente_a, relacion.agente_b)
            self.redes_especializadas[TipoRed.COMPETENCIA][clave] = relacion
    
    def compartir_informacion(self, emisor: str, contenido: Dict[str, Any],
                            tipo_informacion: str, confiabilidad: float = 0.8,
                            agentes_destino: List[str] = None) -> InformacionCompartida:
        """Comparte información en la red social"""
        informacion_id = f"info_{int(time.time())}_{emisor}"
        
        informacion = InformacionCompartida(
            id=informacion_id,
            emisor=emisor,
            contenido=contenido,
            tipo_informacion=tipo_informacion,
            confiabilidad=confiabilidad,
            timestamp=datetime.now()
        )
        
        # Determinar agentes iniciales para propagación
        if agentes_destino:
            agentes_iniciales = agentes_destino
        else:
            # Propagar a vecinos directos
            agentes_iniciales = self.get_vecinos_agente(emisor)
        
        # Propagar información
        resultado_propagacion = self.propagador_informacion.propagar_informacion(
            informacion, agentes_iniciales
        )
        
        # Registrar información
        self.informaciones_activas[informacion_id] = informacion
        
        print(f"[RED SOCIAL] Información compartida por {emisor}, alcanzó {len(resultado_propagacion['agentes_alcanzados'])} agentes")
        
        return informacion
    
    def formar_coalicion_automatica(self) -> Optional[CoalicionAgentes]:
        """Forma una coalición automáticamente basándose en oportunidades"""
        oportunidades = self.formador_coaliciones.identificar_oportunidades_coalicion()
        
        if oportunidades:
            mejor_oportunidad = oportunidades[0]  # Ya están ordenadas por beneficio
            coalicion = self.formador_coaliciones.formar_coalicion(mejor_oportunidad)
            return coalicion
        
        return None
    
    def detectar_comunidades(self) -> List[Set[str]]:
        """Detecta comunidades de agentes en la red"""
        if len(self.agentes_registrados) < 3:
            return [self.agentes_registrados.copy()] if self.agentes_registrados else []
        
        # Algoritmo simple de detección de comunidades
        comunidades = []
        agentes_procesados = set()
        
        for agente in self.agentes_registrados:
            if agente in agentes_procesados:
                continue
            
            # Construir comunidad desde este agente
            comunidad = {agente}
            vecinos = set(self.get_vecinos_agente(agente))
            
            # Agregar vecinos fuertemente conectados
            for vecino in vecinos:
                if vecino not in agentes_procesados:
                    relacion = self.get_relacion_agentes(agente, vecino)
                    if relacion and relacion.fuerza > 0.6 and relacion.confianza > 0.6:
                        comunidad.add(vecino)
            
            if len(comunidad) >= 2:
                comunidades.append(comunidad)
                agentes_procesados.update(comunidad)
        
        # Agentes aislados forman comunidades individuales
        agentes_aislados = self.agentes_registrados - agentes_procesados
        for agente_aislado in agentes_aislados:
            comunidades.append({agente_aislado})
        
        self.clusters_detectados = comunidades
        return comunidades
    
    def _recalcular_metricas_red(self):
        """Recalcula métricas importantes de la red"""
        if not self.agentes_registrados:
            return
        
        # Densidad de la red
        n_agentes = len(self.agentes_registrados)
        max_conexiones = n_agentes * (n_agentes - 1) // 2
        conexiones_actuales = len(self.relaciones)
        self.densidad_red = conexiones_actuales / max(1, max_conexiones)
        
        # Centralidad de agentes (grado)
        for agente in self.agentes_registrados:
            grado = len(self.get_vecinos_agente(agente))
            self.centralidad_agentes[agente] = grado / max(1, n_agentes - 1)
        
        # Eficiencia de comunicación (simplificada)
        if conexiones_actuales > 0:
            self.eficiencia_comunicacion = self.densidad_red * 0.7 + np.mean(list(self.centralidad_agentes.values())) * 0.3
        else:
            self.eficiencia_comunicacion = 0.0
    
    def _ciclo_analisis_red(self):
        """Ciclo continuo de análisis de la red social"""
        while self.procesando:
            try:
                # Gestionar coaliciones activas
                if hasattr(self.formador_coaliciones, 'coaliciones_activas'):
                    self.formador_coaliciones.gestionar_coaliciones_activas()
                
                # Detectar nuevas comunidades
                if len(self.agentes_registrados) > 2:
                    self.detectar_comunidades()
                
                # Formar coaliciones automáticas (ocasionalmente)
                if random.random() < 0.1:  # 10% de probabilidad cada ciclo
                    self.formar_coalicion_automatica()
                
                # Limpiar información antigua
                self._limpiar_informacion_antigua()
                
                # Recalcular métricas
                self._recalcular_metricas_red()
                
            except Exception as e:
                print(f"[RED SOCIAL] Error en análisis de red: {e}")
            
            time.sleep(self.intervalo_analisis)
    
    def _limpiar_informacion_antigua(self):
        """Limpia información más antigua de 24 horas"""
        ahora = datetime.now()
        informaciones_a_eliminar = []
        
        for info_id, informacion in self.informaciones_activas.items():
            if (ahora - informacion.timestamp).total_seconds() > 86400:  # 24 horas
                informaciones_a_eliminar.append(info_id)
        
        for info_id in informaciones_a_eliminar:
            del self.informaciones_activas[info_id]
    
    def get_estadisticas_red(self) -> Dict[str, Any]:
        """Obtiene estadísticas completas de la red social"""
        return {
            'agentes_registrados': len(self.agentes_registrados),
            'relaciones_totales': len(self.relaciones),
            'densidad_red': self.densidad_red,
            'eficiencia_comunicacion': self.eficiencia_comunicacion,
            'comunidades_detectadas': len(self.clusters_detectados),
            'informaciones_activas': len(self.informaciones_activas),
            'coaliciones_activas': len(self.formador_coaliciones.coaliciones_activas),
            'centralidad_promedio': np.mean(list(self.centralidad_agentes.values())) if self.centralidad_agentes else 0,
            'reputacion_promedio': np.mean([
                self.analizador_reputacion.get_reputacion_global(agente)
                for agente in self.agentes_registrados
            ]) if self.agentes_registrados else 0,
            'tipos_relacion_distribucion': self._get_distribucion_tipos_relacion(),
            'redes_especializadas': {
                tipo.value: len(redes) for tipo, redes in self.redes_especializadas.items()
            }
        }
    
    def _get_distribucion_tipos_relacion(self) -> Dict[str, int]:
        """Obtiene distribución de tipos de relación"""
        distribucion = defaultdict(int)
        for relacion in self.relaciones.values():
            distribucion[relacion.tipo.value] += 1
        return dict(distribucion)
    
    def finalizar(self):
        """Finaliza la red social de agentes"""
        print("[RED SOCIAL] Finalizando red social...")
        self.procesando = False
        
        if self.hilo_analisis.is_alive():
            self.hilo_analisis.join(timeout=2.0)
        
        print("[RED SOCIAL] Finalización completada")
