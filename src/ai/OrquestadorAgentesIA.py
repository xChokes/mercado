"""
Orquestador de Agentes IA
=========================

Este módulo implementa el sistema central que coordina todos los agentes IA,
gestiona las comunicaciones, facilita las interacciones y mantiene el
ecosistema de mercado funcionando de manera eficiente.
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict, deque
import threading
import time
import json
from datetime import datetime, timedelta
import uuid

from .AgentMemorySystem import AgentMemorySystem, Decision
from .IADecisionEngine import IADecisionEngine, EstadoMercado, OpcionDecision
from .AgentCommunicationProtocol import (
    AgentCommunicationProtocol, Mensaje, TipoMensaje, PrioridadMensaje,
    Negociacion, Alianza, SeñalMercado
)


class RegistroAgente:
    """Información de registro de un agente en el sistema"""
    def __init__(self, agente_id: str, tipo: str, capacidades: List[str]):
        self.agente_id = agente_id
        self.tipo = tipo  # 'consumidor', 'empresa', 'gobierno', etc.
        self.capacidades = capacidades
        self.activo = True
        self.registrado_en = datetime.now()
        self.ultima_actividad = datetime.now()
        self.reputacion = 0.5
        self.metricas_rendimiento = {}
        self.conexiones_red = []


class EstadisticasMercado:
    """Estadísticas agregadas del mercado"""
    def __init__(self):
        self.total_agentes = 0
        self.agentes_por_tipo = defaultdict(int)
        self.transacciones_totales = 0
        self.volumen_negociado = 0.0
        self.precio_promedio_bienes = {}
        self.volatilidad_precios = {}
        self.eficiencia_mercado = 0.0
        self.concentracion_mercado = 0.0
        self.indice_actividad = 0.0


class OrquestadorAgentesIA:
    """
    Sistema central que coordina todos los agentes IA del mercado
    """
    
    def __init__(self, mercado_ref=None):
        self.mercado_ref = mercado_ref
        
        # Registro de agentes
        self.agentes_registrados: Dict[str, RegistroAgente] = {}
        self.agentes_activos: List[str] = []
        
        # Comunicaciones centralizadas
        self.hub_comunicaciones = {}  # agente_id -> protocolo_comunicacion
        self.mensajes_globales = deque(maxlen=10000)
        self.señales_mercado_globales = deque(maxlen=1000)
        
        # Estado del mercado
        self.estado_mercado_actual = EstadoMercado(
            precios={}, demanda={}, oferta={}, competidores=[],
            tendencias={}, volatilidad={}, ciclo_economico='expansion',
            liquidez_mercado=1.0, riesgo_sistemico=0.1
        )
        
        # Estadísticas y métricas
        self.estadisticas = EstadisticasMercado()
        self.historial_estados = deque(maxlen=1000)
        
        # Configuración del orquestador
        self.intervalo_actualizacion = 1.0  # segundos
        self.max_mensajes_por_ciclo = 1000
        self.umbral_eficiencia_minima = 0.3
        
        # Control de hilos
        self.ejecutando = True
        self.hilo_coordinacion = threading.Thread(target=self._ciclo_coordinacion)
        self.hilo_coordinacion.daemon = True
        
        # Métricas de rendimiento del orquestador
        self.ciclos_completados = 0
        self.tiempo_promedio_ciclo = 0.0
        self.mensajes_procesados = 0
        
        # Iniciar coordinación
        self.hilo_coordinacion.start()
    
    def registrar_agente(self, agente_id: str, tipo: str, 
                        capacidades: List[str] = None) -> bool:
        """Registra un nuevo agente en el sistema"""
        if agente_id in self.agentes_registrados:
            return False  # Ya existe
        
        # Crear registro
        registro = RegistroAgente(agente_id, tipo, capacidades or [])
        self.agentes_registrados[agente_id] = registro
        self.agentes_activos.append(agente_id)
        
        # Crear protocolo de comunicación para el agente
        protocolo = AgentCommunicationProtocol(agente_id)
        self.hub_comunicaciones[agente_id] = protocolo
        
        # Actualizar estadísticas
        self.estadisticas.total_agentes += 1
        self.estadisticas.agentes_por_tipo[tipo] += 1
        
        print(f"[ORQUESTADOR] Agente {agente_id} ({tipo}) registrado exitosamente")
        return True
    
    def desregistrar_agente(self, agente_id: str) -> bool:
        """Desregistra un agente del sistema"""
        if agente_id not in self.agentes_registrados:
            return False
        
        # Marcar como inactivo
        registro = self.agentes_registrados[agente_id]
        registro.activo = False
        
        # Remover de lista activa
        if agente_id in self.agentes_activos:
            self.agentes_activos.remove(agente_id)
        
        # Finalizar protocolo de comunicación
        if agente_id in self.hub_comunicaciones:
            self.hub_comunicaciones[agente_id].finalizar()
            del self.hub_comunicaciones[agente_id]
        
        # Actualizar estadísticas
        self.estadisticas.total_agentes -= 1
        self.estadisticas.agentes_por_tipo[registro.tipo] -= 1
        
        print(f"[ORQUESTADOR] Agente {agente_id} desregistrado")
        return True
    
    def coordinar_agentes_ia(self) -> Dict[str, Any]:
        """Coordina las interacciones entre todos los agentes IA"""
        resultado_coordinacion = {
            'agentes_coordinados': 0,
            'mensajes_procesados': 0,
            'negociaciones_facilitadas': 0,
            'alianzas_formadas': 0,
            'señales_propagadas': 0,
            'eficiencia_mercado': 0.0,
            'timestamp': datetime.now()
        }
        
        # 1. Actualizar estado del mercado
        self._actualizar_estado_mercado()
        
        # 2. Procesar comunicaciones entre agentes
        mensajes_procesados = self._procesar_comunicaciones_globales()
        resultado_coordinacion['mensajes_procesados'] = mensajes_procesados
        
        # 3. Facilitar negociaciones activas
        negociaciones = self._facilitar_negociaciones()
        resultado_coordinacion['negociaciones_facilitadas'] = negociaciones
        
        # 4. Promover formación de alianzas
        alianzas = self._promover_alianzas_estrategicas()
        resultado_coordinacion['alianzas_formadas'] = alianzas
        
        # 5. Propagar señales de mercado
        señales = self._propagar_señales_mercado()
        resultado_coordinacion['señales_propagadas'] = señales
        
        # 6. Optimizar eficiencia del mercado
        eficiencia = self._optimizar_eficiencia_mercado()
        resultado_coordinacion['eficiencia_mercado'] = eficiencia
        
        # 7. Detectar y resolver ineficiencias
        self._detectar_resolver_ineficiencias()
        
        resultado_coordinacion['agentes_coordinados'] = len(self.agentes_activos)
        return resultado_coordinacion
    
    def _actualizar_estado_mercado(self):
        """Actualiza el estado global del mercado"""
        nuevo_estado = EstadoMercado(
            precios={}, demanda={}, oferta={}, competidores=self.agentes_activos.copy(),
            tendencias={}, volatilidad={}, ciclo_economico='expansion',
            liquidez_mercado=1.0, riesgo_sistemico=0.1
        )
        
        # Obtener datos del mercado si hay referencia
        if self.mercado_ref:
            try:
                # Extraer precios actuales
                if hasattr(self.mercado_ref, 'bienes'):
                    bienes = self.mercado_ref.bienes
                    
                    # Manejar tanto diccionarios como listas de bienes
                    if isinstance(bienes, dict):
                        for bien_nombre, bien_obj in bienes.items():
                            if hasattr(bien_obj, 'precio'):
                                nuevo_estado.precios[bien_nombre] = bien_obj.precio
                            else:
                                nuevo_estado.precios[bien_nombre] = 50.0  # Precio por defecto
                    elif isinstance(bienes, list):
                        for i, bien_nombre in enumerate(bienes):
                            # Para listas, asignar precios simulados
                            nuevo_estado.precios[bien_nombre] = 30.0 + (i * 10)
                
                # Extraer información de demanda/oferta
                if hasattr(self.mercado_ref, 'obtener_estadisticas_mercado'):
                    stats = self.mercado_ref.obtener_estadisticas_mercado()
                    # Procesar estadísticas...
                
                # Determinar ciclo económico
                if hasattr(self.mercado_ref, 'ciclo_economico'):
                    nuevo_estado.ciclo_economico = self.mercado_ref.ciclo_economico.fase_actual
                
                # Calcular liquidez y riesgo sistémico
                nuevo_estado.liquidez_mercado = self._calcular_liquidez_mercado()
                nuevo_estado.riesgo_sistemico = self._calcular_riesgo_sistemico()
                
            except Exception as e:
                print(f"[ORQUESTADOR] Error actualizando estado: {e}")
        
        # Calcular tendencias y volatilidad
        self._calcular_tendencias_volatilidad(nuevo_estado)
        
        # Guardar estado anterior y actualizar
        self.historial_estados.append(self.estado_mercado_actual)
        self.estado_mercado_actual = nuevo_estado
    
    def _calcular_liquidez_mercado(self) -> float:
        """Calcula la liquidez del mercado"""
        try:
            if not self.mercado_ref or not hasattr(self.mercado_ref, 'personas'):
                return 1.0
            
            # Calcular liquidez basándose en dinero disponible de agentes
            dinero_total = sum(
                getattr(persona, 'dinero', 0) 
                for persona in self.mercado_ref.personas
                if hasattr(persona, 'dinero')
            )
            
            # Normalizar liquidez (arbitrario, pero funcional)
            liquidez = min(1.0, dinero_total / 1000000)  # Normalizar a máximo 1M
            return max(0.1, liquidez)  # Mínimo 0.1
            
        except Exception:
            return 1.0
    
    def _calcular_riesgo_sistemico(self) -> float:
        """Calcula el riesgo sistémico del mercado"""
        try:
            riesgo = 0.1  # Riesgo base
            
            # Incrementar riesgo por concentración de mercado
            if len(self.agentes_activos) < 10:
                riesgo += 0.2
            
            # Incrementar riesgo por volatilidad de precios
            if self.estado_mercado_actual.precios:
                if len(self.historial_estados) > 5:
                    precios_anteriores = [
                        estado.precios for estado in list(self.historial_estados)[-5:]
                        if estado.precios
                    ]
                    if precios_anteriores:
                        # Calcular volatilidad promedio
                        volatilidades = []
                        for bien in self.estado_mercado_actual.precios:
                            precios_bien = [
                                precios.get(bien, 0) for precios in precios_anteriores
                                if bien in precios
                            ]
                            if len(precios_bien) > 1:
                                volatilidad_bien = np.std(precios_bien) / np.mean(precios_bien)
                                volatilidades.append(volatilidad_bien)
                        
                        if volatilidades:
                            volatilidad_promedio = np.mean(volatilidades)
                            riesgo += min(0.5, volatilidad_promedio)
            
            return min(1.0, riesgo)
            
        except Exception:
            return 0.1
    
    def _calcular_tendencias_volatilidad(self, estado: EstadoMercado):
        """Calcula tendencias y volatilidad de precios"""
        if len(self.historial_estados) < 3:
            return
        
        # Obtener últimos estados para calcular tendencias
        estados_recientes = list(self.historial_estados)[-5:]
        
        for bien in estado.precios:
            precios_historicos = []
            for estado_hist in estados_recientes:
                if bien in estado_hist.precios:
                    precios_historicos.append(estado_hist.precios[bien])
            
            if len(precios_historicos) >= 2:
                # Calcular tendencia (pendiente)
                x = np.arange(len(precios_historicos))
                tendencia = np.polyfit(x, precios_historicos, 1)[0]
                estado.tendencias[bien] = tendencia
                
                # Calcular volatilidad
                volatilidad = np.std(precios_historicos) / np.mean(precios_historicos)
                estado.volatilidad[bien] = volatilidad
    
    def _procesar_comunicaciones_globales(self) -> int:
        """Procesa y facilita comunicaciones entre agentes"""
        mensajes_procesados = 0
        
        # Recopilar mensajes de todos los protocolos
        todos_mensajes = []
        for agente_id, protocolo in self.hub_comunicaciones.items():
            while not protocolo.mensajes_salientes.empty():
                try:
                    mensaje = protocolo.mensajes_salientes.get_nowait()
                    todos_mensajes.append(mensaje)
                except:
                    break
        
        # Procesar y enrutar mensajes
        for mensaje in todos_mensajes[:self.max_mensajes_por_ciclo]:
            if mensaje.destinatario == "ALL":
                # Broadcast a todos los agentes
                for agente_id, protocolo in self.hub_comunicaciones.items():
                    if agente_id != mensaje.remitente:
                        protocolo.recibir_mensaje(mensaje)
            elif mensaje.destinatario in self.hub_comunicaciones:
                # Mensaje directo
                self.hub_comunicaciones[mensaje.destinatario].recibir_mensaje(mensaje)
            
            # Guardar en historial global
            self.mensajes_globales.append(mensaje)
            mensajes_procesados += 1
        
        self.mensajes_procesados += mensajes_procesados
        return mensajes_procesados
    
    def _facilitar_negociaciones(self) -> int:
        """Facilita negociaciones activas entre agentes"""
        negociaciones_facilitadas = 0
        
        # Buscar oportunidades de negociación
        for agente_id, protocolo in self.hub_comunicaciones.items():
            for neg_id, negociacion in protocolo.negociaciones_activas.items():
                if negociacion.estado == "activa":
                    # Facilitar progreso de la negociación
                    if self._facilitar_negociacion_especifica(negociacion, protocolo):
                        negociaciones_facilitadas += 1
        
        # Sugerir nuevas negociaciones basándose en estado del mercado
        nuevas_negociaciones = self._sugerir_nuevas_negociaciones()
        negociaciones_facilitadas += nuevas_negociaciones
        
        return negociaciones_facilitadas
    
    def _facilitar_negociacion_especifica(self, negociacion: Negociacion, 
                                        protocolo: AgentCommunicationProtocol) -> bool:
        """Facilita una negociación específica"""
        try:
            # Si la negociación está estancada, sugerir punto medio
            if negociacion.rondas_negociacion > 5:
                precio_sugerido = (negociacion.precio_minimo + negociacion.precio_maximo) / 2
                
                # Enviar sugerencia de mediación
                for participante in negociacion.participantes:
                    if participante != protocolo.agente_id and participante in self.hub_comunicaciones:
                        self.hub_comunicaciones[participante].enviar_mensaje(
                            participante,
                            TipoMensaje.INFORMACION_MERCADO,
                            {
                                'tipo': 'mediacion_orquestador',
                                'negociacion_id': negociacion.id,
                                'precio_sugerido': precio_sugerido,
                                'razon': 'optimizacion_eficiencia'
                            },
                            prioridad=PrioridadMensaje.ALTA
                        )
                
                return True
        
        except Exception as e:
            print(f"[ORQUESTADOR] Error facilitando negociación: {e}")
        
        return False
    
    def _sugerir_nuevas_negociaciones(self) -> int:
        """Sugiere nuevas negociaciones basándose en oportunidades del mercado"""
        sugerencias = 0
        
        try:
            # Identificar agentes con necesidades complementarias
            agentes_vendedores = []
            agentes_compradores = []
            
            for agente_id in self.agentes_activos:
                registro = self.agentes_registrados[agente_id]
                if registro.tipo == "empresa":
                    agentes_vendedores.append(agente_id)
                elif registro.tipo == "consumidor":
                    agentes_compradores.append(agente_id)
            
            # Sugerir negociaciones entre compradores y vendedores
            if agentes_vendedores and agentes_compradores:
                for bien in self.estado_mercado_actual.precios:
                    # Seleccionar agentes aleatorios para sugerencia
                    if len(agentes_vendedores) > 0 and len(agentes_compradores) > 0:
                        vendedor = np.random.choice(agentes_vendedores)
                        comprador = np.random.choice(agentes_compradores)
                        
                        if vendedor in self.hub_comunicaciones and comprador in self.hub_comunicaciones:
                            # Sugerir negociación
                            precio_sugerido = self.estado_mercado_actual.precios[bien]
                            
                            self.hub_comunicaciones[vendedor].enviar_mensaje(
                                comprador,
                                TipoMensaje.PROPUESTA_PRECIO,
                                {
                                    'bien': bien,
                                    'cantidad': 1,
                                    'precio_propuesto': precio_sugerido,
                                    'origen': 'sugerencia_orquestador'
                                },
                                prioridad=PrioridadMensaje.NORMAL
                            )
                            
                            sugerencias += 1
                            
                            # Limitar sugerencias por ciclo
                            if sugerencias >= 5:
                                break
        
        except Exception as e:
            print(f"[ORQUESTADOR] Error sugiriendo negociaciones: {e}")
        
        return sugerencias
    
    def _promover_alianzas_estrategicas(self) -> int:
        """Promueve la formación de alianzas estratégicas"""
        alianzas_promovidas = 0
        
        try:
            # Identificar oportunidades de alianza
            agentes_por_tipo = defaultdict(list)
            for agente_id in self.agentes_activos:
                registro = self.agentes_registrados[agente_id]
                agentes_por_tipo[registro.tipo].append(agente_id)
            
            # Promover alianzas de compra conjunta entre consumidores
            if len(agentes_por_tipo['consumidor']) >= 3:
                consumidores = agentes_por_tipo['consumidor'][:3]
                lider = consumidores[0]
                otros = consumidores[1:]
                
                if lider in self.hub_comunicaciones:
                    self.hub_comunicaciones[lider].formar_alianza_temporal(
                        otros,
                        "compra_conjunta",
                        "Reducir costos mediante compra grupal",
                        duracion_dias=15
                    )
                    alianzas_promovidas += 1
            
            # Promover alianzas de defensa de precios entre empresas
            if len(agentes_por_tipo['empresa']) >= 2:
                empresas = agentes_por_tipo['empresa'][:2]
                if len(empresas) == 2 and all(e in self.hub_comunicaciones for e in empresas):
                    self.hub_comunicaciones[empresas[0]].formar_alianza_temporal(
                        [empresas[1]],
                        "defensa_precios",
                        "Mantener estabilidad de precios",
                        duracion_dias=20
                    )
                    alianzas_promovidas += 1
        
        except Exception as e:
            print(f"[ORQUESTADOR] Error promoviendo alianzas: {e}")
        
        return alianzas_promovidas
    
    def _propagar_señales_mercado(self) -> int:
        """Propaga señales de mercado importantes"""
        señales_propagadas = 0
        
        try:
            # Recopilar señales de todos los agentes
            todas_señales = []
            for agente_id, protocolo in self.hub_comunicaciones.items():
                señales_agente = list(protocolo.señales_mercado)
                todas_señales.extend(señales_agente)
            
            # Filtrar señales importantes
            señales_importantes = [
                señal for señal in todas_señales
                if señal.confianza > 0.6 and señal.intensidad > 0.5
            ]
            
            # Propagar señales importantes a todos los agentes
            for señal in señales_importantes[-10:]:  # Últimas 10 señales importantes
                mensaje_señal = {
                    'tipo': 'propagacion_orquestador',
                    'señal': {
                        'id': señal.id,
                        'emisor': señal.emisor,
                        'tipo_señal': señal.tipo_señal,
                        'bien': señal.bien,
                        'intensidad': señal.intensidad,
                        'confianza': señal.confianza,
                        'alcance': 'global'
                    }
                }
                
                # Enviar a todos los agentes
                for agente_id, protocolo in self.hub_comunicaciones.items():
                    if agente_id != señal.emisor:
                        protocolo.enviar_mensaje(
                            "ALL",
                            TipoMensaje.SEÑAL_MERCADO,
                            mensaje_señal,
                            prioridad=PrioridadMensaje.ALTA,
                            canal="señales_globales"
                        )
                
                self.señales_mercado_globales.append(señal)
                señales_propagadas += 1
        
        except Exception as e:
            print(f"[ORQUESTADOR] Error propagando señales: {e}")
        
        return señales_propagadas
    
    def _optimizar_eficiencia_mercado(self) -> float:
        """Optimiza la eficiencia general del mercado"""
        try:
            # Calcular eficiencia basándose en varios factores
            eficiencia_comunicacion = self._calcular_eficiencia_comunicacion()
            eficiencia_precios = self._calcular_eficiencia_precios()
            eficiencia_transacciones = self._calcular_eficiencia_transacciones()
            
            # Promedio ponderado
            eficiencia_total = (
                eficiencia_comunicacion * 0.3 +
                eficiencia_precios * 0.4 +
                eficiencia_transacciones * 0.3
            )
            
            self.estadisticas.eficiencia_mercado = eficiencia_total
            
            # Si la eficiencia es baja, tomar medidas correctivas
            if eficiencia_total < self.umbral_eficiencia_minima:
                self._aplicar_medidas_correctivas()
            
            return eficiencia_total
        
        except Exception as e:
            print(f"[ORQUESTADOR] Error optimizando eficiencia: {e}")
            return 0.5
    
    def _calcular_eficiencia_comunicacion(self) -> float:
        """Calcula la eficiencia de comunicación entre agentes"""
        if not self.hub_comunicaciones:
            return 0.0
        
        # Métricas de comunicación
        mensajes_totales = sum(
            protocolo.mensajes_enviados + protocolo.mensajes_recibidos
            for protocolo in self.hub_comunicaciones.values()
        )
        
        agentes_comunicando = sum(
            1 for protocolo in self.hub_comunicaciones.values()
            if protocolo.mensajes_enviados > 0 or protocolo.mensajes_recibidos > 0
        )
        
        if len(self.hub_comunicaciones) == 0:
            return 0.0
        
        tasa_participacion = agentes_comunicando / len(self.hub_comunicaciones)
        return min(1.0, tasa_participacion)
    
    def _calcular_eficiencia_precios(self) -> float:
        """Calcula la eficiencia de descubrimiento de precios"""
        if not self.estado_mercado_actual.precios or len(self.historial_estados) < 5:
            return 0.5
        
        # Calcular convergencia de precios (menor volatilidad = mayor eficiencia)
        volatilidades = list(self.estado_mercado_actual.volatilidad.values())
        if volatilidades:
            volatilidad_promedio = np.mean(volatilidades)
            eficiencia = max(0.0, 1.0 - volatilidad_promedio)
            return min(1.0, eficiencia)
        
        return 0.5
    
    def _calcular_eficiencia_transacciones(self) -> float:
        """Calcula la eficiencia de las transacciones"""
        # Basado en negociaciones exitosas vs fallidas
        negociaciones_exitosas = sum(
            protocolo.negociaciones_exitosas
            for protocolo in self.hub_comunicaciones.values()
        )
        
        negociaciones_totales = negociaciones_exitosas + sum(
            len(protocolo.negociaciones_activas)
            for protocolo in self.hub_comunicaciones.values()
        )
        
        if negociaciones_totales == 0:
            return 0.5
        
        return negociaciones_exitosas / negociaciones_totales
    
    def _aplicar_medidas_correctivas(self):
        """Aplica medidas para mejorar la eficiencia del mercado"""
        print("[ORQUESTADOR] Aplicando medidas correctivas para mejorar eficiencia...")
        
        # Incentivar más comunicación
        for agente_id, protocolo in self.hub_comunicaciones.items():
            if protocolo.mensajes_enviados < 5:  # Agentes poco activos
                # Enviar información del mercado para incentivar actividad
                protocolo.enviar_mensaje(
                    "ALL",
                    TipoMensaje.INFORMACION_MERCADO,
                    {
                        'tipo': 'incentivo_actividad',
                        'estado_mercado': {
                            'precios': self.estado_mercado_actual.precios,
                            'oportunidades': 'multiple',
                            'recomendacion': 'aumentar_participacion'
                        }
                    },
                    prioridad=PrioridadMensaje.NORMAL
                )
    
    def _detectar_resolver_ineficiencias(self):
        """Detecta y resuelve ineficiencias específicas del mercado"""
        try:
            # Detectar concentración excesiva
            concentracion = self._calcular_concentracion_mercado()
            if concentracion > 0.7:
                self._resolver_concentracion_excesiva()
            
            # Detectar información asimétrica
            if self._detectar_asimetria_informacion():
                self._resolver_asimetria_informacion()
            
            # Detectar manipulación de precios
            if self._detectar_manipulacion_precios():
                self._resolver_manipulacion_precios()
        
        except Exception as e:
            print(f"[ORQUESTADOR] Error detectando ineficiencias: {e}")
    
    def _calcular_concentracion_mercado(self) -> float:
        """Calcula el índice de concentración del mercado"""
        if not self.agentes_activos:
            return 0.0
        
        # Simplificado: basado en distribución de agentes por tipo
        agentes_por_tipo = defaultdict(int)
        for agente_id in self.agentes_activos:
            tipo = self.agentes_registrados[agente_id].tipo
            agentes_por_tipo[tipo] += 1
        
        # Calcular HHI simplificado
        total = len(self.agentes_activos)
        hhi = sum((count / total) ** 2 for count in agentes_por_tipo.values())
        
        self.estadisticas.concentracion_mercado = hhi
        return hhi
    
    def _detectar_asimetria_informacion(self) -> bool:
        """Detecta si hay asimetría de información significativa"""
        # Verificar si algunos agentes tienen mucha más información que otros
        conocimiento_por_agente = {}
        for agente_id, protocolo in self.hub_comunicaciones.items():
            conocimiento = len(protocolo.contactos_conocidos) + len(protocolo.señales_mercado)
            conocimiento_por_agente[agente_id] = conocimiento
        
        if len(conocimiento_por_agente) < 2:
            return False
        
        valores = list(conocimiento_por_agente.values())
        desviacion = np.std(valores) / (np.mean(valores) + 0.1)
        
        return desviacion > 1.0  # Alta dispersión de conocimiento
    
    def _detectar_manipulacion_precios(self) -> bool:
        """Detecta posible manipulación de precios"""
        if len(self.historial_estados) < 10:
            return False
        
        # Buscar cambios anómalos de precios
        for bien in self.estado_mercado_actual.precios:
            precios_recientes = []
            for estado in list(self.historial_estados)[-10:]:
                if bien in estado.precios:
                    precios_recientes.append(estado.precios[bien])
            
            if len(precios_recientes) >= 5:
                cambios = np.diff(precios_recientes)
                if np.max(np.abs(cambios)) > np.mean(precios_recientes) * 0.5:
                    return True  # Cambio muy grande detectado
        
        return False
    
    def _resolver_concentracion_excesiva(self):
        """Resuelve concentración excesiva promoviendo diversidad"""
        print("[ORQUESTADOR] Resolviendo concentración excesiva...")
        
        # Incentivar entrada de nuevos agentes y diversificar estrategias
        if hasattr(self, 'agentes_registrados') and len(self.agentes_registrados) > 0:
            # Identificar agentes con estrategias similares
            agentes_diversos = []
            for agente_id in list(self.agentes_registrados.keys())[:5]:  # Tomar muestra pequeña
                agente = self.agentes_registrados[agente_id]
                if hasattr(agente, 'diversificar_estrategia'):
                    try:
                        agente.diversificar_estrategia()
                        agentes_diversos.append(agente_id)
                    except AttributeError:
                        # Si no tiene el método, continuar sin error
                        continue
            
            print(f"[ORQUESTADOR] Diversificadas estrategias de {len(agentes_diversos)} agentes")
    
    def _resolver_asimetria_informacion(self):
        """Resuelve asimetría de información promoviendo transparencia"""
        print("[ORQUESTADOR] Resolviendo asimetría de información...")
        
        # Compartir información del mercado de manera más equitativa
        info_mercado = {
            'precios_agregados': self.estado_mercado_actual.precios,
            'tendencias_generales': self.estado_mercado_actual.tendencias,
            'estado_general': {
                'ciclo': self.estado_mercado_actual.ciclo_economico,
                'liquidez': self.estado_mercado_actual.liquidez_mercado,
                'riesgo': self.estado_mercado_actual.riesgo_sistemico
            }
        }
        
        for agente_id, protocolo in self.hub_comunicaciones.items():
            protocolo.enviar_mensaje(
                "ALL",
                TipoMensaje.INFORMACION_MERCADO,
                {
                    'tipo': 'transparencia_mercado',
                    'informacion': info_mercado,
                    'origen': 'orquestador_ia'
                },
                prioridad=PrioridadMensaje.ALTA
            )
    
    def _resolver_manipulacion_precios(self):
        """Resuelve manipulación de precios aplicando regulaciones"""
        print("[ORQUESTADOR] Detectada posible manipulación - aplicando medidas correctivas...")
        
        # Alertar a todos los agentes sobre posible manipulación
        for agente_id, protocolo in self.hub_comunicaciones.items():
            protocolo.enviar_mensaje(
                "ALL",
                TipoMensaje.ALERTA_RIESGO,
                {
                    'tipo': 'manipulacion_precios',
                    'recomendacion': 'verificar_fuentes_precios',
                    'nivel_alerta': 'alto'
                },
                prioridad=PrioridadMensaje.CRITICA
            )
    
    def _ciclo_coordinacion(self):
        """Ciclo principal de coordinación del orquestador"""
        while self.ejecutando:
            inicio_ciclo = time.time()
            
            try:
                # Ejecutar coordinación principal
                resultado = self.coordinar_agentes_ia()
                
                # Actualizar métricas
                self.ciclos_completados += 1
                
                # Calcular tiempo promedio del ciclo
                tiempo_ciclo = time.time() - inicio_ciclo
                self.tiempo_promedio_ciclo = (
                    self.tiempo_promedio_ciclo * 0.9 + tiempo_ciclo * 0.1
                )
                
                # Log periódico de estado
                if self.ciclos_completados % 100 == 0:
                    print(f"[ORQUESTADOR] Ciclo {self.ciclos_completados} - "
                          f"Agentes: {len(self.agentes_activos)}, "
                          f"Eficiencia: {self.estadisticas.eficiencia_mercado:.2f}, "
                          f"Tiempo: {tiempo_ciclo:.3f}s")
                
            except Exception as e:
                print(f"[ORQUESTADOR] Error en ciclo de coordinación: {e}")
            
            # Esperar intervalo de actualización
            time.sleep(max(0, self.intervalo_actualizacion - (time.time() - inicio_ciclo)))
    
    def get_estadisticas_orquestador(self) -> Dict[str, Any]:
        """Obtiene estadísticas completas del orquestador"""
        return {
            'agentes_registrados': len(self.agentes_registrados),
            'agentes_activos': len(self.agentes_activos),
            'agentes_por_tipo': dict(self.estadisticas.agentes_por_tipo),
            'ciclos_completados': self.ciclos_completados,
            'tiempo_promedio_ciclo': self.tiempo_promedio_ciclo,
            'mensajes_procesados': self.mensajes_procesados,
            'eficiencia_mercado': self.estadisticas.eficiencia_mercado,
            'concentracion_mercado': self.estadisticas.concentracion_mercado,
            'estado_mercado_actual': {
                'ciclo_economico': self.estado_mercado_actual.ciclo_economico,
                'liquidez': self.estado_mercado_actual.liquidez_mercado,
                'riesgo_sistemico': self.estado_mercado_actual.riesgo_sistemico,
                'num_precios': len(self.estado_mercado_actual.precios),
                'num_tendencias': len(self.estado_mercado_actual.tendencias)
            },
            'comunicaciones': {
                'protocolos_activos': len(self.hub_comunicaciones),
                'mensajes_globales': len(self.mensajes_globales),
                'señales_globales': len(self.señales_mercado_globales)
            }
        }
    
    def finalizar(self):
        """Finaliza el orquestador y todos sus componentes"""
        print("[ORQUESTADOR] Iniciando finalización...")
        
        self.ejecutando = False
        
        # Esperar a que termine el hilo de coordinación
        if self.hilo_coordinacion.is_alive():
            self.hilo_coordinacion.join(timeout=2.0)
        
        # Finalizar todos los protocolos de comunicación
        for protocolo in self.hub_comunicaciones.values():
            protocolo.finalizar()
        
        print("[ORQUESTADOR] Finalización completada")
