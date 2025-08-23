"""
Sistema de Memoria y Aprendizaje para Agentes IA
================================================

Este módulo implementa un sistema avanzado de memoria que permite
a los agentes aprender de sus experiencias y mejorar sus decisiones.
"""

import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from collections import deque
import pickle
import json
from datetime import datetime
import uuid


@dataclass
class Decision:
    """Representa una decisión tomada por un agente"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    agente_id: str = ""
    tipo_decision: str = ""  # 'compra', 'venta', 'contratacion', 'precio', etc.
    contexto: Dict[str, Any] = field(default_factory=dict)
    accion_tomada: Dict[str, Any] = field(default_factory=dict)
    resultado: Optional[Dict[str, Any]] = None
    recompensa: float = 0.0
    estado_previo: Dict[str, Any] = field(default_factory=dict)
    estado_posterior: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Strategy:
    """Representa una estrategia aprendida por un agente"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    nombre: str = ""
    tipo: str = ""  # 'precio', 'compra', 'produccion', etc.
    condiciones: Dict[str, Any] = field(default_factory=dict)
    acciones: Dict[str, Any] = field(default_factory=dict)
    exito_rate: float = 0.0
    veces_usado: int = 0
    recompensa_promedio: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    last_used: Optional[datetime] = None


@dataclass
class MarketKnowledge:
    """Conocimiento del mercado acumulado por el agente"""
    precios_historicos: Dict[str, List[float]] = field(default_factory=dict)
    tendencias_demanda: Dict[str, float] = field(default_factory=dict)
    competidores_conocidos: List[str] = field(default_factory=list)
    oportunidades_detectadas: List[Dict[str, Any]] = field(default_factory=list)
    riesgos_identificados: List[Dict[str, Any]] = field(default_factory=list)
    correlaciones_mercado: Dict[str, float] = field(default_factory=dict)


class AgentMemorySystem:
    """
    Sistema avanzado de memoria para agentes IA que incluye:
    - Memoria a corto plazo (decisiones recientes)
    - Memoria a largo plazo (patrones aprendidos)
    - Sistema de recompensas
    - Conocimiento del mercado
    """
    
    def __init__(self, agente_id: str, capacidad_memoria_corta: int = 1000):
        self.agente_id = agente_id
        self.capacidad_memoria_corta = capacidad_memoria_corta

        # Memoria a corto plazo - decisiones recientes
        self.memoria_corta = deque(maxlen=self.capacidad_memoria_corta)
        # Alias solicitado por tests: memoria de trabajo (temporal)
        self.memoria_trabajo = {}

        # Memoria a largo plazo - patrones y estrategias
        self.historial_decisiones = []
        # Alias solicitado por tests para memoria a largo plazo
        self.memoria_largo_plazo = {}
        self.matriz_recompensas = {}
        self.estrategias_exitosas = {}
        self.conocimiento_mercado = MarketKnowledge()

        # Métricas de aprendizaje
        self.experiencia_total = 0
        self.tasa_exito = 0.0
        self.recompensa_total = 0.0
        self.decision_count_by_type = {}

        # Configuración de aprendizaje
        self.factor_descuento = 0.95  # Gamma para recompensas futuras
        self.tasa_aprendizaje = 0.1   # Alpha para actualización
        self.exploracion_rate = 0.1   # Epsilon para exploración vs explotación
        
    def agregar_decision(self, decision: Decision):
        """Agrega una nueva decisión al sistema de memoria"""
        # Añadir a memoria corta
        self.memoria_corta.append(decision)
        
        # Añadir a historial completo
        self.historial_decisiones.append(decision)
        
        # Actualizar métricas
        self.experiencia_total += 1
        tipo = decision.tipo_decision
        self.decision_count_by_type[tipo] = self.decision_count_by_type.get(tipo, 0) + 1
        
        # Si hay resultado, actualizar recompensas
        if decision.resultado is not None:
            self._actualizar_sistema_recompensas(decision)

    # Métodos y alias mínimos esperados por tests
    def almacenar_decision(self, decision: Decision):
        """Alias para agregar_decision, usado por tests."""
        return self.agregar_decision(decision)

    @property
    def decisiones_historicas(self) -> List[Decision]:
        """Alias a historial_decisiones solicitado por tests."""
        return self.historial_decisiones

    def obtener_decisiones_por_tipo(self, tipo: str) -> List[Decision]:
        """Devuelve decisiones del histórico filtradas por tipo."""
        return [d for d in self.historial_decisiones if d.tipo_decision == tipo]

    def calcular_rendimiento_promedio(self, tipo: str) -> float:
        """Calcula el promedio de recompensas para un tipo de decisión."""
        decisiones = [d for d in self.historial_decisiones if d.tipo_decision == tipo]
        if not decisiones:
            return 0.0
        return float(sum(d.recompensa for d in decisiones) / len(decisiones))
    
    def _actualizar_sistema_recompensas(self, decision: Decision):
        """Actualiza el sistema de recompensas basado en el resultado"""
        clave_decision = f"{decision.tipo_decision}_{hash(str(decision.contexto))}"
        
        # Actualizar matriz de recompensas
        if clave_decision in self.matriz_recompensas:
            # Promedio móvil de recompensas
            self.matriz_recompensas[clave_decision] = (
                self.matriz_recompensas[clave_decision] * 0.9 + 
                decision.recompensa * 0.1
            )
        else:
            self.matriz_recompensas[clave_decision] = decision.recompensa
        
        # Actualizar recompensa total
        self.recompensa_total += decision.recompensa
        
        # Actualizar tasa de éxito (recompensa positiva = éxito)
        decisiones_con_resultado = [d for d in self.historial_decisiones if d.resultado is not None]
        if decisiones_con_resultado:
            exitos = sum(1 for d in decisiones_con_resultado if d.recompensa > 0)
            self.tasa_exito = exitos / len(decisiones_con_resultado)
    
    def aprender_de_experiencia(self, decision: Decision, resultado: Dict[str, Any]):
        """Aprende de una experiencia específica y actualiza estrategias"""
        # Actualizar la decisión con el resultado
        decision.resultado = resultado
        decision.recompensa = self._calcular_recompensa(decision, resultado)
        
        # Agregar a memoria
        self.agregar_decision(decision)
        
        # Intentar crear o mejorar estrategias
        self._actualizar_estrategias(decision)
        
        # Actualizar conocimiento del mercado
        self._actualizar_conocimiento_mercado(decision, resultado)
    
    def _calcular_recompensa(self, decision: Decision, resultado: Dict[str, Any]) -> float:
        """Calcula la recompensa basada en el resultado de la decisión"""
        recompensa = 0.0
        
        # Recompensas básicas según tipo de decisión
        if decision.tipo_decision == "compra":
            # Recompensa basada en utilidad obtenida vs precio pagado
            precio_pagado = decision.accion_tomada.get('precio', 0)
            utilidad_obtenida = resultado.get('utilidad', 0)
            recompensa = utilidad_obtenida - precio_pagado * 0.1
            
        elif decision.tipo_decision == "venta":
            # Recompensa basada en beneficio obtenido
            precio_venta = resultado.get('precio_vendido', 0)
            costo_produccion = decision.contexto.get('costo_produccion', 0)
            recompensa = precio_venta - costo_produccion
            
        elif decision.tipo_decision == "precio":
            # Recompensa basada en ventas vs margen de beneficio
            ventas = resultado.get('ventas', 0)
            margen = resultado.get('margen_beneficio', 0)
            recompensa = ventas * margen
            
        elif decision.tipo_decision == "contratacion":
            # Recompensa basada en productividad del empleado
            productividad = resultado.get('productividad', 0)
            salario = decision.accion_tomada.get('salario', 0)
            recompensa = productividad - salario * 0.1
        
        # Aplicar factor de descuento temporal
        tiempo_transcurrido = (datetime.now() - decision.timestamp).days
        factor_temporal = self.factor_descuento ** tiempo_transcurrido
        
        return recompensa * factor_temporal
    
    def _actualizar_estrategias(self, decision: Decision):
        """Actualiza las estrategias basándose en nuevas experiencias"""
        if decision.recompensa <= 0:
            return  # Solo aprender de experiencias exitosas
        
        # Crear clave de estrategia
        clave_estrategia = f"{decision.tipo_decision}_{self._contexto_a_clave(decision.contexto)}"
        
        if clave_estrategia in self.estrategias_exitosas:
            # Actualizar estrategia existente
            estrategia = self.estrategias_exitosas[clave_estrategia]
            estrategia.veces_usado += 1
            estrategia.recompensa_promedio = (
                estrategia.recompensa_promedio * 0.9 + 
                decision.recompensa * 0.1
            )
            estrategia.exito_rate = min(1.0, estrategia.exito_rate + 0.1)
            estrategia.last_used = datetime.now()
        else:
            # Crear nueva estrategia
            estrategia = Strategy(
                nombre=f"Estrategia_{decision.tipo_decision}_{len(self.estrategias_exitosas)}",
                tipo=decision.tipo_decision,
                condiciones=decision.contexto.copy(),
                acciones=decision.accion_tomada.copy(),
                exito_rate=0.7,  # Empezar con confianza moderada
                veces_usado=1,
                recompensa_promedio=decision.recompensa
            )
            self.estrategias_exitosas[clave_estrategia] = estrategia
    
    def _contexto_a_clave(self, contexto: Dict[str, Any]) -> str:
        """Convierte el contexto en una clave para indexar estrategias"""
        # Simplificar contexto a elementos clave
        elementos_clave = ['precio_mercado', 'demanda', 'competencia', 'temporada']
        clave_elementos = []
        
        for elemento in elementos_clave:
            if elemento in contexto:
                valor = contexto[elemento]
                if isinstance(valor, (int, float)):
                    # Discretizar valores numéricos
                    if valor < 10:
                        clave_elementos.append(f"{elemento}_bajo")
                    elif valor < 50:
                        clave_elementos.append(f"{elemento}_medio")
                    else:
                        clave_elementos.append(f"{elemento}_alto")
                else:
                    clave_elementos.append(f"{elemento}_{valor}")
        
        return "_".join(clave_elementos)
    
    def _actualizar_conocimiento_mercado(self, decision: Decision, resultado: Dict[str, Any]):
        """Actualiza el conocimiento del mercado basado en observaciones"""
        # Actualizar precios históricos
        if 'precio' in resultado:
            bien = decision.contexto.get('bien', 'general')
            if bien not in self.conocimiento_mercado.precios_historicos:
                self.conocimiento_mercado.precios_historicos[bien] = []
            
            precios = self.conocimiento_mercado.precios_historicos[bien]
            precios.append(resultado['precio'])
            
            # Mantener solo últimos 100 precios
            if len(precios) > 100:
                precios.pop(0)
        
        # Detectar tendencias de demanda
        if 'demanda' in resultado:
            bien = decision.contexto.get('bien', 'general')
            demanda_actual = resultado['demanda']
            
            if bien in self.conocimiento_mercado.tendencias_demanda:
                # Calcular tendencia como promedio móvil
                tendencia_anterior = self.conocimiento_mercado.tendencias_demanda[bien]
                self.conocimiento_mercado.tendencias_demanda[bien] = (
                    tendencia_anterior * 0.8 + demanda_actual * 0.2
                )
            else:
                self.conocimiento_mercado.tendencias_demanda[bien] = demanda_actual
        
        # Identificar competidores
        if 'competidores' in resultado:
            for competidor in resultado['competidores']:
                if competidor not in self.conocimiento_mercado.competidores_conocidos:
                    self.conocimiento_mercado.competidores_conocidos.append(competidor)
    
    def actualizar_estrategia(self, nueva_info: Dict[str, Any]):
        """Actualiza estrategias basándose en nueva información del mercado"""
        # Adaptar tasa de exploración basada en experiencia
        if self.experiencia_total > 100:
            self.exploracion_rate = max(0.05, self.exploracion_rate * 0.99)
        
        # Detectar oportunidades basadas en nueva información
        self._detectar_oportunidades(nueva_info)
        
        # Evaluar riesgos
        self._evaluar_riesgos(nueva_info)
    
    def _detectar_oportunidades(self, info: Dict[str, Any]):
        """Detecta oportunidades de mercado basándose en información disponible"""
        # Oportunidad de precio bajo
        if 'precios_mercado' in info:
            for bien, precio in info['precios_mercado'].items():
                if bien in self.conocimiento_mercado.precios_historicos:
                    precios_hist = self.conocimiento_mercado.precios_historicos[bien]
                    if precios_hist and precio < np.mean(precios_hist) * 0.8:
                        oportunidad = {
                            'tipo': 'precio_bajo',
                            'bien': bien,
                            'precio_actual': precio,
                            'precio_promedio': np.mean(precios_hist),
                            'potencial_beneficio': np.mean(precios_hist) - precio,
                            'timestamp': datetime.now()
                        }
                        self.conocimiento_mercado.oportunidades_detectadas.append(oportunidad)
        
        # Mantener solo últimas 50 oportunidades
        if len(self.conocimiento_mercado.oportunidades_detectadas) > 50:
            self.conocimiento_mercado.oportunidades_detectadas = (
                self.conocimiento_mercado.oportunidades_detectadas[-50:]
            )
    
    def _evaluar_riesgos(self, info: Dict[str, Any]):
        """Evalúa riesgos potenciales basándose en información del mercado"""
        # Riesgo de volatilidad de precios
        if 'precios_mercado' in info:
            for bien, precio in info['precios_mercado'].items():
                if bien in self.conocimiento_mercado.precios_historicos:
                    precios_hist = self.conocimiento_mercado.precios_historicos[bien]
                    if len(precios_hist) > 10:
                        volatilidad = np.std(precios_hist) / np.mean(precios_hist)
                        if volatilidad > 0.3:  # Alta volatilidad
                            riesgo = {
                                'tipo': 'alta_volatilidad',
                                'bien': bien,
                                'volatilidad': volatilidad,
                                'recomendacion': 'reducir_exposicion',
                                'timestamp': datetime.now()
                            }
                            self.conocimiento_mercado.riesgos_identificados.append(riesgo)
        
        # Mantener solo últimos 50 riesgos
        if len(self.conocimiento_mercado.riesgos_identificados) > 50:
            self.conocimiento_mercado.riesgos_identificados = (
                self.conocimiento_mercado.riesgos_identificados[-50:]
            )
    
    def predecir_mejor_accion(self, estado_actual: Dict[str, Any]) -> Dict[str, Any]:
        """Predice la mejor acción basándose en experiencias pasadas"""
        # Buscar estrategias similares al estado actual
        estrategias_aplicables = []
        
        for clave, estrategia in self.estrategias_exitosas.items():
            similitud = self._calcular_similitud_contexto(
                estrategia.condiciones, 
                estado_actual
            )
            
            if similitud > 0.6:  # Umbral de similitud
                score = similitud * estrategia.exito_rate * estrategia.recompensa_promedio
                estrategias_aplicables.append((estrategia, score))
        
        if estrategias_aplicables:
            # Ordenar por score y seleccionar la mejor
            estrategias_aplicables.sort(key=lambda x: x[1], reverse=True)
            mejor_estrategia = estrategias_aplicables[0][0]
            
            # Aplicar exploración vs explotación
            if np.random.random() < self.exploracion_rate:
                # Explorar: modificar ligeramente la estrategia
                accion = self._explorar_variacion(mejor_estrategia.acciones)
            else:
                # Explotar: usar la estrategia conocida
                accion = mejor_estrategia.acciones.copy()
            
            return {
                'accion_recomendada': accion,
                'confianza': mejor_estrategia.exito_rate,
                'estrategia_base': mejor_estrategia.nombre,
                'explorar': np.random.random() < self.exploracion_rate
            }
        else:
            # Sin estrategias aplicables, usar decisión aleatoria informada
            return self._decision_aleatoria_informada(estado_actual)
    
    def _calcular_similitud_contexto(self, contexto1: Dict[str, Any], 
                                   contexto2: Dict[str, Any]) -> float:
        """Calcula la similitud entre dos contextos"""
        claves_comunes = set(contexto1.keys()) & set(contexto2.keys())
        if not claves_comunes:
            return 0.0
        
        similitudes = []
        for clave in claves_comunes:
            val1, val2 = contexto1[clave], contexto2[clave]
            
            if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                # Similitud numérica
                max_val = max(abs(val1), abs(val2), 1)
                similitud = 1 - abs(val1 - val2) / max_val
            elif val1 == val2:
                # Similitud exacta
                similitud = 1.0
            else:
                # Sin similitud
                similitud = 0.0
            
            similitudes.append(similitud)
        
        return np.mean(similitudes)
    
    def _explorar_variacion(self, accion_base: Dict[str, Any]) -> Dict[str, Any]:
        """Explora variaciones de una acción base"""
        accion_explorada = accion_base.copy()
        
        for clave, valor in accion_explorada.items():
            if isinstance(valor, (int, float)):
                # Añadir ruido aleatorio
                factor_ruido = np.random.uniform(0.9, 1.1)
                accion_explorada[clave] = valor * factor_ruido
        
        return accion_explorada
    
    def _decision_aleatoria_informada(self, estado_actual: Dict[str, Any]) -> Dict[str, Any]:
        """Toma una decisión aleatoria pero informada por el conocimiento del mercado"""
        # Basarse en conocimiento general del mercado
        accion = {'tipo': 'exploracion'}
        
        # Si hay información de precios, usar tendencias
        if 'bien' in estado_actual and estado_actual['bien'] in self.conocimiento_mercado.tendencias_demanda:
            tendencia = self.conocimiento_mercado.tendencias_demanda[estado_actual['bien']]
            if tendencia > 50:  # Alta demanda
                accion['agresividad'] = 'alta'
            else:
                accion['agresividad'] = 'baja'
        
        return {
            'accion_recomendada': accion,
            'confianza': 0.3,  # Baja confianza en decisiones aleatorias
            'estrategia_base': 'exploracion_aleatoria',
            'explorar': True
        }
    
    def get_estadisticas(self) -> Dict[str, Any]:
        """Obtiene estadísticas del sistema de memoria"""
        return {
            'experiencia_total': self.experiencia_total,
            'tasa_exito': self.tasa_exito,
            'recompensa_total': self.recompensa_total,
            'recompensa_promedio': self.recompensa_total / max(self.experiencia_total, 1),
            'estrategias_aprendidas': len(self.estrategias_exitosas),
            'decisiones_por_tipo': self.decision_count_by_type,
            'tasa_exploracion': self.exploracion_rate,
            'oportunidades_detectadas': len(self.conocimiento_mercado.oportunidades_detectadas),
            'riesgos_identificados': len(self.conocimiento_mercado.riesgos_identificados),
            'competidores_conocidos': len(self.conocimiento_mercado.competidores_conocidos)
        }
    
    def guardar_memoria(self, filepath: str):
        """Guarda el estado de la memoria en un archivo"""
        estado = {
            'agente_id': self.agente_id,
            'historial_decisiones': [vars(d) for d in self.historial_decisiones],
            'matriz_recompensas': self.matriz_recompensas,
            'estrategias_exitosas': {k: vars(v) for k, v in self.estrategias_exitosas.items()},
            'conocimiento_mercado': vars(self.conocimiento_mercado),
            'experiencia_total': self.experiencia_total,
            'tasa_exito': self.tasa_exito,
            'recompensa_total': self.recompensa_total
        }
        
        with open(filepath, 'w') as f:
            json.dump(estado, f, default=str, indent=2)
    
    def cargar_memoria(self, filepath: str):
        """Carga el estado de la memoria desde un archivo"""
        try:
            with open(filepath, 'r') as f:
                estado = json.load(f)
            
            self.agente_id = estado['agente_id']
            self.matriz_recompensas = estado['matriz_recompensas']
            self.experiencia_total = estado['experiencia_total']
            self.tasa_exito = estado['tasa_exito']
            self.recompensa_total = estado['recompensa_total']
            
            # Reconstruir objetos complejos
            # ... (implementar reconstrucción completa si es necesario)
            
        except Exception as e:
            print(f"Error cargando memoria: {e}")
