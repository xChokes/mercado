"""
Mercado IA Inteligente
======================

Implementa un mercado con inteligencia artificial central que coordina
transacciones, optimiza eficiencia, detecta patrones y previene crisis.
"""

import numpy as np
import random
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict, deque
import threading
import time

from ..models.Mercado import Mercado
from .OrquestadorAgentesIA import OrquestadorAgentesIA
from .AgentMemorySystem import AgentMemorySystem, Decision
from .IADecisionEngine import IADecisionEngine, EstadoMercado, OpcionDecision
from .AgentCommunicationProtocol import TipoMensaje, PrioridadMensaje


@dataclass
class TransaccionIA:
    """Transacción inteligente con metadatos de IA"""
    id: str
    comprador: str
    vendedor: str
    bien: str
    cantidad: float
    precio: float
    precio_mercado: float
    eficiencia_precio: float
    timestamp: datetime
    negociada: bool = False
    tiempo_resolucion: float = 0.0
    satisfaccion_comprador: float = 0.0
    satisfaccion_vendedor: float = 0.0


@dataclass
class PatronMercado:
    """Patrón identificado en el mercado"""
    tipo: str
    descripcion: str
    confianza: float
    frecuencia: int
    impacto_estimado: float
    detectado_en: datetime
    variables_asociadas: List[str]


@dataclass
class AlertaRiesgo:
    """Alerta de riesgo del mercado"""
    nivel: str  # 'bajo', 'medio', 'alto', 'critico'
    tipo: str
    descripcion: str
    probabilidad: float
    impacto_estimado: float
    recomendaciones: List[str]
    timestamp: datetime


class DetectorCrisisIA:
    """Detector avanzado de crisis usando IA"""
    
    def __init__(self):
        self.indicadores_riesgo = {}
        self.umbrales_alerta = {
            'volatilidad_precios': 0.3,
            'concentracion_mercado': 0.7,
            'liquidez_baja': 0.2,
            'caida_transacciones': 0.5,
            'diferencial_precios': 0.4
        }
        self.historial_alertas = deque(maxlen=1000)
        self.patrones_crisis = []
    
    def monitorear_indicadores_riesgo(self, estado_mercado: EstadoMercado,
                                    transacciones_recientes: List[TransaccionIA]) -> Dict[str, float]:
        """Monitorea indicadores de riesgo en tiempo real"""
        indicadores = {}
        
        # 1. Volatilidad de precios
        indicadores['volatilidad_precios'] = self._calcular_volatilidad_precios(estado_mercado)
        
        # 2. Concentración de mercado
        indicadores['concentracion_mercado'] = self._calcular_concentracion_transacciones(transacciones_recientes)
        
        # 3. Liquidez del mercado
        indicadores['liquidez_mercado'] = estado_mercado.liquidez_mercado
        
        # 4. Volumen de transacciones
        indicadores['volumen_transacciones'] = len(transacciones_recientes)
        
        # 5. Diferencial de precios
        indicadores['diferencial_precios'] = self._calcular_diferencial_precios(estado_mercado)
        
        # 6. Riesgo sistémico
        indicadores['riesgo_sistemico'] = estado_mercado.riesgo_sistemico
        
        self.indicadores_riesgo = indicadores
        return indicadores
    
    def _calcular_volatilidad_precios(self, estado: EstadoMercado) -> float:
        """Calcula volatilidad promedio de precios"""
        if not estado.volatilidad:
            return 0.0
        return np.mean(list(estado.volatilidad.values()))
    
    def _calcular_concentracion_transacciones(self, transacciones: List[TransaccionIA]) -> float:
        """Calcula concentración de transacciones por agente"""
        if not transacciones:
            return 0.0
        
        agentes_transacciones = defaultdict(int)
        for transaccion in transacciones:
            agentes_transacciones[transaccion.vendedor] += 1
            agentes_transacciones[transaccion.comprador] += 1
        
        if not agentes_transacciones:
            return 0.0
        
        total_transacciones = sum(agentes_transacciones.values())
        proporciones = [count / total_transacciones for count in agentes_transacciones.values()]
        
        # Calcular índice HHI
        hhi = sum(p ** 2 for p in proporciones)
        return hhi
    
    def _calcular_diferencial_precios(self, estado: EstadoMercado) -> float:
        """Calcula diferencial entre precios máximos y mínimos"""
        if not estado.precios or len(estado.precios) < 2:
            return 0.0
        
        precios = list(estado.precios.values())
        precio_max = max(precios)
        precio_min = min(precios)
        precio_promedio = np.mean(precios)
        
        if precio_promedio == 0:
            return 0.0
        
        return (precio_max - precio_min) / precio_promedio
    
    def predecir_contagio_crisis(self, tipo_crisis: str, epicentro: str) -> Dict[str, float]:
        """Predice cómo se propagará una crisis"""
        propagacion = {}
        
        # Modelos simplificados de contagio
        if tipo_crisis == "liquidez":
            # Crisis de liquidez se propaga rápidamente
            propagacion['velocidad'] = 0.8
            propagacion['amplitud'] = 0.7
            propagacion['sectores_afectados'] = 0.9
        elif tipo_crisis == "crediticia":
            # Crisis crediticia afecta especialmente empresas
            propagacion['velocidad'] = 0.6
            propagacion['amplitud'] = 0.8
            propagacion['sectores_afectados'] = 0.6
        elif tipo_crisis == "demanda":
            # Crisis de demanda se propaga gradualmente
            propagacion['velocidad'] = 0.4
            propagacion['amplitud'] = 0.6
            propagacion['sectores_afectados'] = 0.7
        
        return propagacion
    
    def activar_medidas_preventivas(self, alertas: List[AlertaRiesgo]) -> List[Dict[str, Any]]:
        """Activa medidas preventivas basándose en alertas"""
        medidas = []
        
        for alerta in alertas:
            if alerta.nivel in ['alto', 'critico']:
                medida = self._generar_medida_preventiva(alerta)
                if medida:
                    medidas.append(medida)
        
        return medidas
    
    def _generar_medida_preventiva(self, alerta: AlertaRiesgo) -> Optional[Dict[str, Any]]:
        """Genera medida preventiva específica para un tipo de alerta"""
        if alerta.tipo == "volatilidad_extrema":
            return {
                'tipo': 'estabilizacion_precios',
                'accion': 'suspender_negociacion_volatil',
                'parametros': {'umbral_suspension': 0.5},
                'duracion_horas': 2
            }
        elif alerta.tipo == "concentracion_excesiva":
            return {
                'tipo': 'diversificacion_forzada',
                'accion': 'limitar_transacciones_grandes',
                'parametros': {'limite_porcentaje': 0.1},
                'duracion_horas': 24
            }
        elif alerta.tipo == "caida_liquidez":
            return {
                'tipo': 'inyeccion_liquidez',
                'accion': 'facilitar_credito',
                'parametros': {'tasa_interes': 0.02},
                'duracion_horas': 72
            }
        
        return None
    
    def generar_alerta(self, indicadores: Dict[str, float]) -> Optional[AlertaRiesgo]:
        """Genera alerta basándose en indicadores"""
        alertas_detectadas = []
        
        for indicador, valor in indicadores.items():
            if indicador in self.umbrales_alerta:
                umbral = self.umbrales_alerta[indicador]
                
                if valor > umbral:
                    nivel = self._determinar_nivel_alerta(valor, umbral)
                    alerta = AlertaRiesgo(
                        nivel=nivel,
                        tipo=indicador,
                        descripcion=f"Valor anómalo detectado: {indicador} = {valor:.3f}",
                        probabilidad=min(1.0, (valor - umbral) / umbral),
                        impacto_estimado=valor,
                        recomendaciones=self._generar_recomendaciones(indicador),
                        timestamp=datetime.now()
                    )
                    alertas_detectadas.append(alerta)
        
        if alertas_detectadas:
            # Devolver la alerta más severa
            alerta_principal = max(alertas_detectadas, 
                                 key=lambda x: self._severidad_alerta(x.nivel))
            self.historial_alertas.append(alerta_principal)
            return alerta_principal
        
        return None
    
    def _determinar_nivel_alerta(self, valor: float, umbral: float) -> str:
        """Determina nivel de alerta basándose en qué tanto excede el umbral"""
        exceso = (valor - umbral) / umbral
        
        if exceso > 1.0:
            return 'critico'
        elif exceso > 0.5:
            return 'alto'
        elif exceso > 0.2:
            return 'medio'
        else:
            return 'bajo'
    
    def _severidad_alerta(self, nivel: str) -> int:
        """Convierte nivel de alerta a valor numérico"""
        niveles = {'bajo': 1, 'medio': 2, 'alto': 3, 'critico': 4}
        return niveles.get(nivel, 0)
    
    def _generar_recomendaciones(self, tipo_indicador: str) -> List[str]:
        """Genera recomendaciones para un tipo de indicador"""
        recomendaciones_base = {
            'volatilidad_precios': [
                'Suspender temporalmente negociaciones de alta frecuencia',
                'Activar mecanismos de estabilización',
                'Incrementar transparencia de información'
            ],
            'concentracion_mercado': [
                'Promover entrada de nuevos participantes',
                'Limitar operaciones de agentes dominantes',
                'Facilitar competencia'
            ],
            'liquidez_mercado': [
                'Inyectar liquidez al sistema',
                'Reducir requisitos de garantías',
                'Facilitar acceso a crédito'
            ]
        }
        
        return recomendaciones_base.get(tipo_indicador, ['Monitorear situación'])


class PlatformaNegociacionIA:
    """Plataforma inteligente de negociación"""
    
    def __init__(self):
        self.negociaciones_activas = {}
        self.algoritmos_matching = {}
        self.optimizador_clearing = None
        self.motor_contratos = None
        self.arbitro_disputas = None
    
    def facilitar_negociaciones_complejas(self, participantes: List[str], 
                                        bienes: List[str]) -> str:
        """Facilita negociaciones complejas multi-parte"""
        negociacion_id = f"negociacion_compleja_{int(time.time())}"
        
        # Configurar negociación
        negociacion = {
            'id': negociacion_id,
            'participantes': participantes,
            'bienes': bienes,
            'tipo': 'multi_parte',
            'estado': 'configuracion',
            'rondas_maximas': 10,
            'tiempo_limite': datetime.now() + timedelta(hours=2),
            'ofertas': defaultdict(list),
            'matriz_utilidad': {},
            'solucion_optima': None
        }
        
        # Calcular matriz de utilidad para optimización
        self._calcular_matriz_utilidad(negociacion)
        
        # Encontrar solución óptima inicial
        self._encontrar_solucion_optima(negociacion)
        
        self.negociaciones_activas[negociacion_id] = negociacion
        return negociacion_id
    
    def _calcular_matriz_utilidad(self, negociacion: Dict[str, Any]):
        """Calcula matriz de utilidad para optimización"""
        # Simulación de cálculo de utilidad
        participantes = negociacion['participantes']
        bienes = negociacion['bienes']
        
        for participante in participantes:
            negociacion['matriz_utilidad'][participante] = {}
            for bien in bienes:
                # Utilidad simulada
                utilidad = random.uniform(0.1, 1.0)
                negociacion['matriz_utilidad'][participante][bien] = utilidad
    
    def _encontrar_solucion_optima(self, negociacion: Dict[str, Any]):
        """Encuentra solución óptima usando algoritmos de optimización"""
        # Algoritmo simplificado de optimización
        participantes = negociacion['participantes']
        bienes = negociacion['bienes']
        matriz_utilidad = negociacion['matriz_utilidad']
        
        mejor_asignacion = {}
        mejor_utilidad_total = 0
        
        # Probar diferentes asignaciones (simplificado)
        for _ in range(100):  # Monte Carlo simple
            asignacion = {}
            utilidad_total = 0
            
            bienes_disponibles = bienes.copy()
            random.shuffle(bienes_disponibles)
            
            for i, participante in enumerate(participantes):
                if i < len(bienes_disponibles):
                    bien_asignado = bienes_disponibles[i]
                    asignacion[participante] = bien_asignado
                    utilidad_total += matriz_utilidad[participante].get(bien_asignado, 0)
            
            if utilidad_total > mejor_utilidad_total:
                mejor_utilidad_total = utilidad_total
                mejor_asignacion = asignacion
        
        negociacion['solucion_optima'] = {
            'asignacion': mejor_asignacion,
            'utilidad_total': mejor_utilidad_total,
            'eficiencia': mejor_utilidad_total / len(participantes)
        }
    
    def optimizar_clearing_settlement(self, transacciones: List[TransaccionIA]) -> Dict[str, Any]:
        """Optimiza el proceso de clearing y settlement"""
        optimizacion = {
            'transacciones_procesadas': len(transacciones),
            'tiempo_promedio_clearing': 0.0,
            'eficiencia_netting': 0.0,
            'costos_reducidos': 0.0,
            'riesgos_mitigados': 0
        }
        
        if not transacciones:
            return optimizacion
        
        # 1. Netting multilateral
        netting_result = self._realizar_netting_multilateral(transacciones)
        optimizacion['eficiencia_netting'] = netting_result['eficiencia']
        
        # 2. Optimización temporal
        scheduling_result = self._optimizar_scheduling(transacciones)
        optimizacion['tiempo_promedio_clearing'] = scheduling_result['tiempo_promedio']
        
        # 3. Reducción de costos
        costos_result = self._reducir_costos_transaccion(transacciones)
        optimizacion['costos_reducidos'] = costos_result['ahorro_total']
        
        return optimizacion
    
    def _realizar_netting_multilateral(self, transacciones: List[TransaccionIA]) -> Dict[str, Any]:
        """Realiza netting multilateral para reducir exposiciones"""
        # Construir matriz de exposiciones
        exposiciones = defaultdict(lambda: defaultdict(float))
        
        for transaccion in transacciones:
            exposiciones[transaccion.comprador][transaccion.vendedor] += transaccion.precio
            exposiciones[transaccion.vendedor][transaccion.comprador] -= transaccion.precio
        
        # Calcular netting
        exposiciones_netas = {}
        transacciones_originales = len(transacciones)
        transacciones_netas = 0
        
        for agente1 in exposiciones:
            exposicion_neta = sum(exposiciones[agente1].values())
            if abs(exposicion_neta) > 0.01:  # Umbral mínimo
                exposiciones_netas[agente1] = exposicion_neta
                transacciones_netas += 1
        
        eficiencia = 1 - (transacciones_netas / max(transacciones_originales, 1))
        
        return {
            'exposiciones_netas': exposiciones_netas,
            'transacciones_reducidas': transacciones_originales - transacciones_netas,
            'eficiencia': eficiencia
        }
    
    def _optimizar_scheduling(self, transacciones: List[TransaccionIA]) -> Dict[str, Any]:
        """Optimiza el scheduling de transacciones"""
        # Algoritmo simple de scheduling por prioridad
        transacciones_priorizadas = sorted(
            transacciones,
            key=lambda t: (t.precio, -t.cantidad),  # Priorizar por valor
            reverse=True
        )
        
        tiempo_acumulado = 0
        tiempos_proceso = []
        
        for i, transaccion in enumerate(transacciones_priorizadas):
            tiempo_proceso = 0.1 + random.uniform(0, 0.2)  # Simulado
            tiempo_acumulado += tiempo_proceso
            tiempos_proceso.append(tiempo_proceso)
        
        tiempo_promedio = np.mean(tiempos_proceso) if tiempos_proceso else 0
        
        return {
            'tiempo_promedio': tiempo_promedio,
            'tiempo_total': tiempo_acumulado,
            'transacciones_optimizadas': len(transacciones_priorizadas)
        }
    
    def _reducir_costos_transaccion(self, transacciones: List[TransaccionIA]) -> Dict[str, Any]:
        """Reduce costos de transacción mediante optimización"""
        costo_base_por_transaccion = 1.0
        
        # Descuentos por volumen
        volumen_total = sum(t.cantidad * t.precio for t in transacciones)
        if volumen_total > 1000:
            descuento_volumen = 0.1
        elif volumen_total > 500:
            descuento_volumen = 0.05
        else:
            descuento_volumen = 0.0
        
        # Descuentos por netting
        if len(transacciones) > 10:
            descuento_netting = 0.15
        elif len(transacciones) > 5:
            descuento_netting = 0.1
        else:
            descuento_netting = 0.0
        
        costo_total_original = len(transacciones) * costo_base_por_transaccion
        costo_total_optimizado = costo_total_original * (1 - descuento_volumen - descuento_netting)
        ahorro_total = costo_total_original - costo_total_optimizado
        
        return {
            'costo_original': costo_total_original,
            'costo_optimizado': costo_total_optimizado,
            'ahorro_total': ahorro_total,
            'porcentaje_ahorro': (ahorro_total / costo_total_original) if costo_total_original > 0 else 0
        }


class MercadoIA(Mercado):
    """
    Mercado con Inteligencia Artificial Central
    """
    
    def __init__(self, bienes):
        super().__init__(bienes)
        
        # Componentes IA del mercado
        self.orquestador_ia = OrquestadorAgentesIA(mercado_ref=self)
        self.detector_crisis = DetectorCrisisIA()
        self.plataforma_negociacion = PlatformaNegociacionIA()
        
        # Sistema de memoria del mercado
        self.memoria_mercado = AgentMemorySystem("mercado_central")
        self.ia_engine = IADecisionEngine("mercado_central")
        
        # Estado del mercado IA
        self.estado_ia = EstadoMercado(
            precios={}, demanda={}, oferta={}, competidores=[],
            tendencias={}, volatilidad={}, ciclo_economico='expansion',
            liquidez_mercado=1.0, riesgo_sistemico=0.1
        )
        
        # Transacciones y análisis
        self.transacciones_ia: deque = deque(maxlen=10000)
        self.patrones_detectados: List[PatronMercado] = []
        self.alertas_activas: List[AlertaRiesgo] = []
        
        # Métricas de eficiencia IA
        self.eficiencia_descubrimiento_precios = 0.7
        self.eficiencia_asignacion_recursos = 0.6
        self.estabilidad_sistemica = 0.8
        self.transparencia_mercado = 0.7
        
        # Configuración
        self.intervalo_analisis = 5  # segundos
        self.umbral_intervencion = 0.7
        
        # Control de hilos
        self.procesando_ia = True
        self.hilo_analisis = threading.Thread(target=self._ciclo_analisis_continuo)
        self.hilo_analisis.daemon = True
        self.hilo_analisis.start()
        
        print("[MERCADO IA] Sistema de IA del mercado inicializado")
    
    def registrar_transaccion_ia(self, comprador: str, vendedor: str, bien: str,
                               cantidad: float, precio: float, negociada: bool = False) -> TransaccionIA:
        """Registra una transacción con análisis IA"""
        # Crear transacción IA
        transaccion = TransaccionIA(
            id=f"tx_{int(time.time())}_{len(self.transacciones_ia)}",
            comprador=comprador,
            vendedor=vendedor,
            bien=bien,
            cantidad=cantidad,
            precio=precio,
            precio_mercado=self.estado_ia.precios.get(bien, precio),
            eficiencia_precio=self._calcular_eficiencia_precio(bien, precio),
            timestamp=datetime.now(),
            negociada=negociada
        )
        
        # Calcular satisfacción (simulado)
        transaccion.satisfaccion_comprador = self._calcular_satisfaccion_comprador(transaccion)
        transaccion.satisfaccion_vendedor = self._calcular_satisfaccion_vendedor(transaccion)
        
        # Registrar en historial
        self.transacciones_ia.append(transaccion)
        
        # Actualizar estado del mercado
        self._actualizar_estado_por_transaccion(transaccion)
        
        # Analizar patrones en tiempo real
        self._analizar_patrones_transaccion(transaccion)
        
        return transaccion
    
    def _calcular_eficiencia_precio(self, bien: str, precio: float) -> float:
        """Calcula la eficiencia del precio vs precio de mercado"""
        precio_mercado = self.estado_ia.precios.get(bien, precio)
        if precio_mercado == 0:
            return 1.0
        
        diferencia = abs(precio - precio_mercado) / precio_mercado
        eficiencia = max(0.0, 1.0 - diferencia)
        return eficiencia
    
    def _calcular_satisfaccion_comprador(self, transaccion: TransaccionIA) -> float:
        """Calcula satisfacción del comprador"""
        # Satisfacción basada en eficiencia del precio
        satisfaccion_base = transaccion.eficiencia_precio
        
        # Bonus si el precio fue negociado (mejor para comprador)
        if transaccion.negociada:
            satisfaccion_base += 0.1
        
        # Ajuste por disponibilidad del bien
        disponibilidad = self.estado_ia.oferta.get(transaccion.bien, 1.0)
        if disponibilidad < 0.5:  # Bien escaso
            satisfaccion_base += 0.2  # Satisfecho de conseguirlo
        
        return min(1.0, satisfaccion_base)
    
    def _calcular_satisfaccion_vendedor(self, transaccion: TransaccionIA) -> float:
        """Calcula satisfacción del vendedor"""
        # Satisfacción basada en margen vs precio de mercado
        precio_mercado = self.estado_ia.precios.get(transaccion.bien, transaccion.precio)
        if precio_mercado > 0:
            margen = (transaccion.precio - precio_mercado) / precio_mercado
            satisfaccion_base = 0.5 + margen  # Neutral + margen
        else:
            satisfaccion_base = 0.7
        
        # Penalización si fue muy negociado
        if transaccion.negociada and transaccion.precio < precio_mercado * 0.9:
            satisfaccion_base -= 0.1
        
        return max(0.0, min(1.0, satisfaccion_base))
    
    def _actualizar_estado_por_transaccion(self, transaccion: TransaccionIA):
        """Actualiza el estado del mercado basándose en nueva transacción"""
        bien = transaccion.bien
        
        # Actualizar precio promedio ponderado
        if bien in self.estado_ia.precios:
            # Promedio móvil exponencial
            self.estado_ia.precios[bien] = (
                self.estado_ia.precios[bien] * 0.9 + transaccion.precio * 0.1
            )
        else:
            self.estado_ia.precios[bien] = transaccion.precio
        
        # Actualizar indicadores de demanda/oferta
        self.estado_ia.demanda[bien] = self.estado_ia.demanda.get(bien, 0.5) + 0.05
        self.estado_ia.oferta[bien] = max(0.1, self.estado_ia.oferta.get(bien, 1.0) - 0.02)
        
        # Actualizar competidores activos
        if transaccion.vendedor not in self.estado_ia.competidores:
            self.estado_ia.competidores.append(transaccion.vendedor)
        if transaccion.comprador not in self.estado_ia.competidores:
            self.estado_ia.competidores.append(transaccion.comprador)
    
    def _analizar_patrones_transaccion(self, transaccion: TransaccionIA):
        """Analiza patrones en tiempo real basándose en nueva transacción"""
        # Detectar patrón de alta frecuencia
        transacciones_recientes = [
            t for t in self.transacciones_ia 
            if (datetime.now() - t.timestamp).total_seconds() < 60
        ]
        
        if len(transacciones_recientes) > 10:
            patron = PatronMercado(
                tipo="alta_frecuencia",
                descripcion=f"Actividad alta detectada: {len(transacciones_recientes)} transacciones en 1 minuto",
                confianza=0.8,
                frecuencia=len(transacciones_recientes),
                impacto_estimado=0.3,
                detectado_en=datetime.now(),
                variables_asociadas=['volumen', 'frecuencia']
            )
            
            if not any(p.tipo == "alta_frecuencia" for p in self.patrones_detectados[-5:]):
                self.patrones_detectados.append(patron)
    
    def detectar_patrones_emergentes(self) -> List[PatronMercado]:
        """Detecta patrones emergentes en el mercado"""
        nuevos_patrones = []
        
        if len(self.transacciones_ia) < 20:
            return nuevos_patrones
        
        transacciones_recientes = list(self.transacciones_ia)[-100:]  # Últimas 100
        
        # 1. Patrón de concentración de vendedor
        vendedores = defaultdict(int)
        for tx in transacciones_recientes:
            vendedores[tx.vendedor] += 1
        
        if vendedores:
            max_vendedor = max(vendedores.values())
            if max_vendedor > len(transacciones_recientes) * 0.4:  # Más del 40%
                patron = PatronMercado(
                    tipo="concentracion_vendedor",
                    descripcion=f"Concentración alta detectada: un vendedor con {max_vendedor} transacciones",
                    confianza=0.9,
                    frecuencia=max_vendedor,
                    impacto_estimado=0.6,
                    detectado_en=datetime.now(),
                    variables_asociadas=['vendedor', 'concentracion']
                )
                nuevos_patrones.append(patron)
        
        # 2. Patrón de precios sincronizados
        if len(set(tx.precio for tx in transacciones_recientes[-10:])) <= 2:
            patron = PatronMercado(
                tipo="precios_sincronizados",
                descripcion="Precios muy similares en transacciones recientes",
                confianza=0.7,
                frecuencia=10,
                impacto_estimado=0.4,
                detectado_en=datetime.now(),
                variables_asociadas=['precio', 'sincronizacion']
            )
            nuevos_patrones.append(patron)
        
        # 3. Patrón de escalada de precios
        precios_cronologicos = [tx.precio for tx in transacciones_recientes[-20:]]
        if len(precios_cronologicos) >= 10:
            tendencia = np.polyfit(range(len(precios_cronologicos)), precios_cronologicos, 1)[0]
            if tendencia > np.mean(precios_cronologicos) * 0.05:  # Escalada > 5%
                patron = PatronMercado(
                    tipo="escalada_precios",
                    descripcion=f"Escalada de precios detectada: tendencia {tendencia:.2f}",
                    confianza=0.8,
                    frecuencia=len(precios_cronologicos),
                    impacto_estimado=0.7,
                    detectado_en=datetime.now(),
                    variables_asociadas=['precio', 'tendencia']
                )
                nuevos_patrones.append(patron)
        
        # Agregar a lista total
        self.patrones_detectados.extend(nuevos_patrones)
        
        # Mantener solo últimos 100 patrones
        if len(self.patrones_detectados) > 100:
            self.patrones_detectados = self.patrones_detectados[-100:]
        
        return nuevos_patrones
    
    def optimizar_liquidez_mercado(self) -> Dict[str, Any]:
        """Optimiza la liquidez del mercado"""
        optimizacion = {
            'liquidez_inicial': self.estado_ia.liquidez_mercado,
            'medidas_aplicadas': [],
            'mejora_liquidez': 0.0,
            'transacciones_facilitadas': 0
        }
        
        # Identificar problemas de liquidez
        if self.estado_ia.liquidez_mercado < 0.3:
            # Crisis de liquidez - medidas agresivas
            medidas = self._aplicar_medidas_liquidez_crisis()
            optimizacion['medidas_aplicadas'].extend(medidas)
        elif self.estado_ia.liquidez_mercado < 0.6:
            # Liquidez baja - medidas moderadas
            medidas = self._aplicar_medidas_liquidez_baja()
            optimizacion['medidas_aplicadas'].extend(medidas)
        
        # Facilitar emparejamiento de órdenes
        emparejamientos = self._facilitar_emparejamiento_ordenes()
        optimizacion['transacciones_facilitadas'] = emparejamientos
        
        # Calcular mejora
        liquidez_final = self._recalcular_liquidez()
        optimizacion['mejora_liquidez'] = liquidez_final - optimizacion['liquidez_inicial']
        self.estado_ia.liquidez_mercado = liquidez_final
        
        return optimizacion
    
    def _aplicar_medidas_liquidez_crisis(self) -> List[str]:
        """Aplica medidas agresivas para crisis de liquidez"""
        medidas = []
        
        # Reducir spreads bid-ask
        medidas.append("reduccion_spreads")
        
        # Facilitar acceso a crédito
        medidas.append("facilitacion_credito")
        
        # Suspender algunos requisitos regulatorios temporalmente
        medidas.append("suspension_requisitos")
        
        # Incrementar liquidez artificialmente
        self.estado_ia.liquidez_mercado += 0.2
        medidas.append("inyeccion_liquidez_emergencia")
        
        return medidas
    
    def _aplicar_medidas_liquidez_baja(self) -> List[str]:
        """Aplica medidas moderadas para liquidez baja"""
        medidas = []
        
        # Incentivar market makers
        medidas.append("incentivos_market_makers")
        
        # Mejorar transparencia
        medidas.append("mejora_transparencia")
        
        # Incrementar liquidez moderadamente
        self.estado_ia.liquidez_mercado += 0.1
        medidas.append("inyeccion_liquidez_moderada")
        
        return medidas
    
    def _facilitar_emparejamiento_ordenes(self) -> int:
        """Facilita emparejamiento de órdenes pendientes"""
        # Simulación de emparejamiento de órdenes
        transacciones_recientes = list(self.transacciones_ia)[-50:]
        
        # Identificar oportunidades de emparejamiento
        compradores = set(tx.comprador for tx in transacciones_recientes)
        vendedores = set(tx.vendedor for tx in transacciones_recientes)
        
        # Facilitar nuevos emparejamientos (simulado)
        nuevos_emparejamientos = min(5, len(compradores), len(vendedores))
        
        return nuevos_emparejamientos
    
    def _recalcular_liquidez(self) -> float:
        """Recalcula liquidez basándose en estado actual"""
        # Factores que afectan liquidez
        factor_volumen = min(1.0, len(self.transacciones_ia) / 100)
        factor_diversidad = min(1.0, len(self.estado_ia.competidores) / 20)
        factor_volatilidad = 1.0 - np.mean(list(self.estado_ia.volatilidad.values())) if self.estado_ia.volatilidad else 1.0
        
        liquidez_calculada = (factor_volumen * 0.4 + factor_diversidad * 0.3 + factor_volatilidad * 0.3)
        
        return min(1.0, liquidez_calculada)
    
    def prevenir_burbujas_crashes(self) -> Dict[str, Any]:
        """Previene burbujas especulativas y crashes"""
        prevencion = {
            'burbujas_detectadas': 0,
            'riesgo_crash_detectado': False,
            'medidas_preventivas': [],
            'eficacia_prevencion': 0.0
        }
        
        # Detectar burbujas
        burbujas = self._detectar_burbujas_especulativas()
        prevencion['burbujas_detectadas'] = len(burbujas)
        
        if burbujas:
            medidas_burbuja = self._aplicar_medidas_anti_burbuja(burbujas)
            prevencion['medidas_preventivas'].extend(medidas_burbuja)
        
        # Detectar riesgo de crash
        riesgo_crash = self._evaluar_riesgo_crash()
        prevencion['riesgo_crash_detectado'] = riesgo_crash > 0.7
        
        if prevencion['riesgo_crash_detectado']:
            medidas_crash = self._aplicar_medidas_anti_crash()
            prevencion['medidas_preventivas'].extend(medidas_crash)
        
        # Evaluar eficacia
        prevencion['eficacia_prevencion'] = self._evaluar_eficacia_prevencion()
        
        return prevencion
    
    def _detectar_burbujas_especulativas(self) -> List[str]:
        """Detecta burbujas especulativas en bienes específicos"""
        burbujas = []
        
        for bien, precio_actual in self.estado_ia.precios.items():
            # Calcular precio histórico promedio
            precios_historicos = [
                tx.precio for tx in self.transacciones_ia 
                if tx.bien == bien and (datetime.now() - tx.timestamp).days <= 30
            ]
            
            if len(precios_historicos) >= 5:
                precio_promedio = np.mean(precios_historicos)
                
                # Detectar burbuja si precio actual es > 150% del promedio
                if precio_actual > precio_promedio * 1.5:
                    burbujas.append(bien)
        
        return burbujas
    
    def _evaluar_riesgo_crash(self) -> float:
        """Evalúa riesgo de crash del mercado"""
        factores_riesgo = []
        
        # Factor 1: Volatilidad extrema
        if self.estado_ia.volatilidad:
            volatilidad_promedio = np.mean(list(self.estado_ia.volatilidad.values()))
            if volatilidad_promedio > 0.5:
                factores_riesgo.append(0.3)
        
        # Factor 2: Concentración alta
        if len(self.transacciones_ia) > 20:
            vendedores = defaultdict(int)
            for tx in list(self.transacciones_ia)[-50:]:
                vendedores[tx.vendedor] += 1
            
            if vendedores:
                concentracion = max(vendedores.values()) / len(vendedores)
                if concentracion > 0.4:
                    factores_riesgo.append(0.4)
        
        # Factor 3: Liquidez muy baja
        if self.estado_ia.liquidez_mercado < 0.2:
            factores_riesgo.append(0.5)
        
        # Factor 4: Riesgo sistémico alto
        if self.estado_ia.riesgo_sistemico > 0.7:
            factores_riesgo.append(0.6)
        
        return min(1.0, sum(factores_riesgo))
    
    def _aplicar_medidas_anti_burbuja(self, burbujas: List[str]) -> List[str]:
        """Aplica medidas para prevenir burbujas"""
        medidas = []
        
        for bien in burbujas:
            # Aumentar transparencia sobre el bien
            medidas.append(f"transparencia_aumentada_{bien}")
            
            # Alertar a participantes
            medidas.append(f"alerta_burbuja_{bien}")
            
            # Aplicar cooldown en negociaciones del bien
            medidas.append(f"cooldown_negociacion_{bien}")
        
        return medidas
    
    def _aplicar_medidas_anti_crash(self) -> List[str]:
        """Aplica medidas para prevenir crash"""
        medidas = []
        
        # Suspender negociación de alta frecuencia
        medidas.append("suspension_alta_frecuencia")
        
        # Activar circuit breakers
        medidas.append("activacion_circuit_breakers")
        
        # Incrementar liquidez de emergencia
        self.estado_ia.liquidez_mercado += 0.3
        medidas.append("liquidez_emergencia")
        
        # Reducir riesgo sistémico
        self.estado_ia.riesgo_sistemico *= 0.8
        medidas.append("reduccion_riesgo_sistemico")
        
        return medidas
    
    def _evaluar_eficacia_prevencion(self) -> float:
        """Evalúa eficacia de medidas preventivas"""
        # Métricas de eficacia simplificadas
        eficacia = 0.5  # Base
        
        # Incrementar por liquidez estable
        if self.estado_ia.liquidez_mercado > 0.6:
            eficacia += 0.2
        
        # Incrementar por baja volatilidad
        if self.estado_ia.volatilidad:
            volatilidad_promedio = np.mean(list(self.estado_ia.volatilidad.values()))
            if volatilidad_promedio < 0.3:
                eficacia += 0.2
        
        # Incrementar por riesgo sistémico bajo
        if self.estado_ia.riesgo_sistemico < 0.5:
            eficacia += 0.1
        
        return min(1.0, eficacia)
    
    def _ciclo_analisis_continuo(self):
        """Ciclo continuo de análisis del mercado IA"""
        while self.procesando_ia:
            try:
                # Monitorear indicadores de riesgo
                if len(self.transacciones_ia) > 0:
                    indicadores = self.detector_crisis.monitorear_indicadores_riesgo(
                        self.estado_ia, list(self.transacciones_ia)[-100:]
                    )
                    
                    # Generar alertas si es necesario
                    alerta = self.detector_crisis.generar_alerta(indicadores)
                    if alerta:
                        self.alertas_activas.append(alerta)
                        print(f"[MERCADO IA] Alerta {alerta.nivel}: {alerta.descripcion}")
                
                # Detectar patrones emergentes
                nuevos_patrones = self.detectar_patrones_emergentes()
                if nuevos_patrones:
                    print(f"[MERCADO IA] {len(nuevos_patrones)} nuevos patrones detectados")
                
                # Optimizar liquidez si es necesario
                if self.estado_ia.liquidez_mercado < 0.5:
                    self.optimizar_liquidez_mercado()
                
                # Prevenir burbujas y crashes
                self.prevenir_burbujas_crashes()
                
                # Limpiar alertas antiguas
                self._limpiar_alertas_antigas()
                
            except Exception as e:
                print(f"[MERCADO IA] Error en análisis continuo: {e}")
            
            time.sleep(self.intervalo_analisis)
    
    def _limpiar_alertas_antigas(self):
        """Limpia alertas antiguas (más de 1 hora)"""
        ahora = datetime.now()
        self.alertas_activas = [
            alerta for alerta in self.alertas_activas
            if (ahora - alerta.timestamp).total_seconds() < 3600
        ]
    
    def get_estadisticas_mercado_ia(self) -> Dict[str, Any]:
        """Obtiene estadísticas completas del mercado IA"""
        return {
            'transacciones_totales': len(self.transacciones_ia),
            'patrones_detectados': len(self.patrones_detectados),
            'alertas_activas': len(self.alertas_activas),
            'eficiencia_precios': self.eficiencia_descubrimiento_precios,
            'eficiencia_asignacion': self.eficiencia_asignacion_recursos,
            'estabilidad_sistemica': self.estabilidad_sistemica,
            'transparencia': self.transparencia_mercado,
            'estado_actual': {
                'liquidez': self.estado_ia.liquidez_mercado,
                'riesgo_sistemico': self.estado_ia.riesgo_sistemico,
                'ciclo_economico': self.estado_ia.ciclo_economico,
                'competidores_activos': len(self.estado_ia.competidores),
                'bienes_comerciados': len(self.estado_ia.precios)
            },
            'orquestador_stats': self.orquestador_ia.get_estadisticas_orquestador(),
            'detector_crisis_stats': {
                'indicadores_monitoreados': len(self.detector_crisis.indicadores_riesgo),
                'alertas_historicas': len(self.detector_crisis.historial_alertas),
                'umbrales_configurados': len(self.detector_crisis.umbrales_alerta)
            }
        }
    
    def finalizar_ia(self):
        """Finaliza todos los componentes IA del mercado"""
        print("[MERCADO IA] Iniciando finalización...")
        
        self.procesando_ia = False
        
        # Esperar a que termine el hilo de análisis
        if self.hilo_analisis.is_alive():
            self.hilo_analisis.join(timeout=2.0)
        
        # Finalizar orquestador
        self.orquestador_ia.finalizar()
        
        print("[MERCADO IA] Finalización completada")
