"""
Consumidor IA Hiperrealista
===========================

Implementa un consumidor con inteligencia artificial que aprende patrones,
adapta comportamientos, negocia precios y forma alianzas estratégicas.
"""

import numpy as np
import random
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta

from ..models.Consumidor import Consumidor
from .AgentMemorySystem import AgentMemorySystem, Decision
from .IADecisionEngine import IADecisionEngine, EstadoMercado, OpcionDecision
from .AgentCommunicationProtocol import AgentCommunicationProtocol, TipoMensaje, PrioridadMensaje


@dataclass
class PatronConsumo:
    """Representa un patrón de consumo aprendido"""
    bien: str
    frecuencia_promedio: float  # días entre compras
    cantidad_promedio: float
    precio_maximo_aceptable: float
    estacionalidad: Dict[str, float]  # factor por mes/estación
    utilidad_esperada: float
    confianza: float


@dataclass
class PerfilAprendizajeIA:
    """Perfil de aprendizaje personalizado del consumidor"""
    tipo_personalidad: str  # 'conservador', 'impulsivo', 'estrategico', 'social'
    velocidad_aprendizaje: float  # 0.0 a 1.0
    tolerancia_riesgo: float  # 0.0 a 1.0
    influencia_social: float  # 0.0 a 1.0
    memoria_preferencias: int  # número de experiencias que recuerda
    adaptabilidad_crisis: float  # qué tan rápido se adapta a crisis


class ConsumidorIA(Consumidor):
    """
    Consumidor con Inteligencia Artificial que aprende y se adapta
    """
    
    def __init__(self, nombre, mercado, bienes={}):
        super().__init__(nombre, mercado, bienes)
        
        # Componentes IA
        self.ia_engine = IADecisionEngine(f"consumidor_{nombre}")
        self.memoria = AgentMemorySystem(f"consumidor_{nombre}")
        self.comunicacion = AgentCommunicationProtocol(f"consumidor_{nombre}")
        
        # Perfil de aprendizaje IA
        self.perfil_aprendizaje = self._generar_perfil_aprendizaje()
        
        # Patrones de consumo aprendidos
        self.patrones_consumo: Dict[str, PatronConsumo] = {}
        self.preferencias_dinamicas: Dict[str, float] = {}
        
        # Sistema de predicción de necesidades
        self.calendario_necesidades: Dict[datetime, List[str]] = {}
        self.predicciones_demanda: Dict[str, float] = {}
        
        # Red social y colaboración
        self.red_social: List[str] = []  # IDs de otros consumidores conocidos
        self.grupos_compra: List[str] = []  # IDs de grupos de compra activos
        self.influencers_seguidos: List[str] = []
        
        # Historial de negociaciones
        self.historial_negociaciones: List[Dict[str, Any]] = []
        self.reputacion_vendedores: Dict[str, float] = {}
        
        # Métricas de eficiencia IA
        self.ahorro_obtenido_ia = 0.0
        self.compras_optimizadas = 0
        self.negociaciones_exitosas = 0
        self.utilidad_total_ia = 0.0
        
        # Estado emocional y psicológico
        self.estado_emocional = 0.5  # 0.0 (triste) a 1.0 (feliz)
        self.confianza_mercado = 0.5  # 0.0 (desconfianza) a 1.0 (confianza total)
        self.stress_financiero = 0.0  # 0.0 (relajado) a 1.0 (muy estresado)
        
        # Inicializar IA
        self._inicializar_sistema_ia()
    
    def _generar_perfil_aprendizaje(self) -> PerfilAprendizajeIA:
        """Genera un perfil de aprendizaje único para el consumidor"""
        tipos_personalidad = ['conservador', 'impulsivo', 'estrategico', 'social']
        
        perfil = PerfilAprendizajeIA(
            tipo_personalidad=random.choice(tipos_personalidad),
            velocidad_aprendizaje=random.uniform(0.3, 0.9),
            tolerancia_riesgo=random.uniform(0.1, 0.8),
            influencia_social=random.uniform(0.2, 0.9),
            memoria_preferencias=random.randint(20, 100),
            adaptabilidad_crisis=random.uniform(0.4, 1.0)
        )
        
        # Ajustar parámetros según personalidad
        if perfil.tipo_personalidad == 'conservador':
            perfil.tolerancia_riesgo *= 0.5
            perfil.velocidad_aprendizaje *= 0.8
        elif perfil.tipo_personalidad == 'impulsivo':
            perfil.tolerancia_riesgo *= 1.5
            perfil.velocidad_aprendizaje *= 1.2
        elif perfil.tipo_personalidad == 'estrategico':
            perfil.memoria_preferencias *= 1.5
        elif perfil.tipo_personalidad == 'social':
            perfil.influencia_social *= 1.3
        
        return perfil
    
    def _inicializar_sistema_ia(self):
        """Inicializa los sistemas de IA del consumidor"""
        # Configurar motor IA según personalidad
        self.ia_engine.modelo_rl.epsilon = 0.2 if self.perfil_aprendizaje.tipo_personalidad == 'impulsivo' else 0.1
        
        # Inicializar patrones básicos para bienes conocidos
        if self.mercado and hasattr(self.mercado, 'bienes'):
            if isinstance(self.mercado.bienes, dict):
                # Mercado con bienes como diccionario
                bienes_nombres = self.mercado.bienes.keys()
            elif isinstance(self.mercado.bienes, list):
                # Mercado con bienes como lista
                bienes_nombres = self.mercado.bienes
            else:
                # Usar los bienes del propio consumidor
                bienes_nombres = self.bienes.keys() if hasattr(self, 'bienes') and isinstance(self.bienes, dict) else []
            
            for nombre_bien in bienes_nombres:
                self._inicializar_patron_consumo(nombre_bien)
    
    def _inicializar_patron_consumo(self, bien: str):
        """Inicializa un patrón de consumo básico para un bien"""
        self.patrones_consumo[bien] = PatronConsumo(
            bien=bien,
            frecuencia_promedio=random.uniform(3, 14),  # 3-14 días
            cantidad_promedio=random.uniform(0.5, 3.0),
            precio_maximo_aceptable=random.uniform(20, 100),
            estacionalidad={},
            utilidad_esperada=random.uniform(0.3, 0.8),
            confianza=0.3  # Baja confianza inicial
        )
    
    def aprender_patrones_consumo(self):
        """Aprende y actualiza patrones de consumo basándose en experiencias"""
        # Analizar historial de compras para identificar patrones
        if not self.historial_compras:
            return
        
        for bien, compras in self.historial_compras.items():
            if len(compras) >= 3:  # Necesario mínimo de datos
                self._actualizar_patron_consumo(bien, compras)
    
    def _actualizar_patron_consumo(self, bien: str, compras: List[Dict[str, Any]]):
        """Actualiza el patrón de consumo para un bien específico"""
        if bien not in self.patrones_consumo:
            self._inicializar_patron_consumo(bien)
        
        patron = self.patrones_consumo[bien]
        
        # Actualizar frecuencia promedio
        if len(compras) > 1:
            intervalos = []
            for i in range(1, len(compras)):
                # Calcular intervalo entre compras (simulado)
                intervalo = random.uniform(1, 20)  # Placeholder
                intervalos.append(intervalo)
            
            if intervalos:
                nueva_frecuencia = np.mean(intervalos)
                patron.frecuencia_promedio = (
                    patron.frecuencia_promedio * 0.7 + nueva_frecuencia * 0.3
                )
        
        # Actualizar cantidad promedio
        cantidades = [compra.get('cantidad', 1) for compra in compras]
        nueva_cantidad = np.mean(cantidades)
        patron.cantidad_promedio = (
            patron.cantidad_promedio * 0.7 + nueva_cantidad * 0.3
        )
        
        # Actualizar precio máximo aceptable
        precios = [compra.get('precio', 0) for compra in compras]
        precio_max_observado = max(precios) if precios else patron.precio_maximo_aceptable
        patron.precio_maximo_aceptable = (
            patron.precio_maximo_aceptable * 0.8 + precio_max_observado * 1.2
        )
        
        # Incrementar confianza en el patrón
        patron.confianza = min(1.0, patron.confianza + 0.1)
    
    def predecir_necesidades_futuras(self, dias_adelante: int = 7) -> Dict[str, float]:
        """Predice necesidades futuras basándose en patrones aprendidos"""
        predicciones = {}
        fecha_actual = datetime.now()
        
        for bien, patron in self.patrones_consumo.items():
            if patron.confianza < 0.3:
                continue  # Skip patrones poco confiables
            
            # Calcular probabilidad de necesidad en los próximos días
            dias_desde_ultima_compra = self._dias_desde_ultima_compra(bien)
            
            if dias_desde_ultima_compra >= patron.frecuencia_promedio * 0.8:
                # Alta probabilidad de necesidad pronto
                urgencia = min(1.0, dias_desde_ultima_compra / patron.frecuencia_promedio)
                
                # Ajustar por factores estacionales (simplificado)
                factor_estacional = self._calcular_factor_estacional(bien, fecha_actual)
                
                # Predicción final
                prediccion = urgencia * patron.utilidad_esperada * factor_estacional
                predicciones[bien] = min(1.0, prediccion)
        
        self.predicciones_demanda = predicciones
        return predicciones
    
    def _dias_desde_ultima_compra(self, bien: str) -> int:
        """Calcula días desde la última compra de un bien"""
        if bien not in self.historial_compras or not self.historial_compras[bien]:
            return 999  # Nunca comprado
        
        # Simulado - en implementación real usaría timestamps reales
        return random.randint(1, 30)
    
    def _calcular_factor_estacional(self, bien: str, fecha: datetime) -> float:
        """Calcula factor estacional para un bien"""
        # Factores estacionales simplificados
        mes = fecha.month
        
        factores_base = {
            'alimentos': {1: 1.1, 2: 1.0, 3: 1.0, 4: 1.0, 5: 1.0, 6: 1.0,
                         7: 1.0, 8: 1.0, 9: 1.0, 10: 1.0, 11: 1.1, 12: 1.2},
            'ropa': {1: 0.8, 2: 0.8, 3: 1.1, 4: 1.2, 5: 1.2, 6: 1.0,
                    7: 0.9, 8: 0.9, 9: 1.1, 10: 1.2, 11: 1.3, 12: 1.3},
            'tecnologia': {1: 1.2, 2: 1.0, 3: 1.0, 4: 1.0, 5: 1.0, 6: 1.0,
                          7: 1.0, 8: 1.0, 9: 1.0, 10: 1.0, 11: 1.3, 12: 1.5}
        }
        
        # Determinar categoría del bien (simplificado)
        categoria = 'alimentos'  # Default
        if 'ropa' in bien.lower() or 'vestido' in bien.lower():
            categoria = 'ropa'
        elif 'tech' in bien.lower() or 'electronico' in bien.lower():
            categoria = 'tecnologia'
        
        return factores_base[categoria].get(mes, 1.0)
    
    def negociar_precios_inteligente(self, vendedor_id: str, bien: str, 
                                   cantidad: float, precio_inicial: float) -> Optional[float]:
        """Negocia precios de manera inteligente basándose en IA"""
        # Evaluar si vale la pena negociar
        if not self._vale_la_pena_negociar(vendedor_id, bien, precio_inicial):
            return None
        
        # Determinar estrategia de negociación basándose en perfil
        estrategia = self._determinar_estrategia_negociacion(vendedor_id, bien, precio_inicial)
        
        # Calcular precio objetivo
        precio_objetivo = self._calcular_precio_objetivo(bien, precio_inicial)
        
        # Iniciar negociación
        negociacion_id = self.comunicacion.negociar_precio(
            vendedor_id, bien, cantidad, precio_objetivo,
            precio_objetivo * 0.8, precio_inicial * 1.1
        )
        
        if negociacion_id:
            # Registrar negociación
            self.historial_negociaciones.append({
                'id': negociacion_id,
                'vendedor': vendedor_id,
                'bien': bien,
                'cantidad': cantidad,
                'precio_inicial': precio_inicial,
                'precio_objetivo': precio_objetivo,
                'estrategia': estrategia,
                'timestamp': datetime.now(),
                'estado': 'activa'
            })
            
            return precio_objetivo
        
        return None
    
    def _vale_la_pena_negociar(self, vendedor_id: str, bien: str, precio: float) -> bool:
        """Determina si vale la pena negociar basándose en múltiples factores"""
        # Factor 1: Precio está por encima del patrón esperado
        if bien in self.patrones_consumo:
            precio_esperado = self.patrones_consumo[bien].precio_maximo_aceptable * 0.8
            if precio <= precio_esperado:
                return False  # Precio ya es bueno
        
        # Factor 2: Reputación del vendedor permite negociación
        reputacion = self.reputacion_vendedores.get(vendedor_id, 0.5)
        if reputacion < 0.3:
            return False  # Vendedor poco confiable
        
        # Factor 3: Personalidad permite negociación
        if self.perfil_aprendizaje.tipo_personalidad == 'conservador' and precio < 50:
            return False  # Conservadores no negocian precios bajos
        
        # Factor 4: Estado emocional
        if self.estado_emocional < 0.3:  # Muy triste/estresado
            return False  # No tiene energía para negociar
        
        return True
    
    def _determinar_estrategia_negociacion(self, vendedor_id: str, bien: str, 
                                         precio: float) -> str:
        """Determina la estrategia de negociación apropiada"""
        reputacion = self.reputacion_vendedores.get(vendedor_id, 0.5)
        
        if self.perfil_aprendizaje.tipo_personalidad == 'agresivo':
            return 'agresiva'
        elif self.perfil_aprendizaje.tipo_personalidad == 'conservador':
            return 'conservadora'
        elif reputacion > 0.7:
            return 'colaborativa'
        else:
            return 'cautelosa'
    
    def _calcular_precio_objetivo(self, bien: str, precio_inicial: float) -> float:
        """Calcula el precio objetivo para la negociación"""
        # Usar patrón aprendido si está disponible
        if bien in self.patrones_consumo:
            precio_esperado = self.patrones_consumo[bien].precio_maximo_aceptable * 0.9
            return min(precio_inicial * 0.9, precio_esperado)
        
        # Fallback: reducir precio inicial basándose en personalidad
        factor_reduccion = {
            'conservador': 0.95,
            'impulsivo': 0.98,
            'estrategico': 0.85,
            'social': 0.92
        }
        
        factor = factor_reduccion.get(self.perfil_aprendizaje.tipo_personalidad, 0.9)
        return precio_inicial * factor
    
    def formar_grupos_compra(self, bien: str, cantidad_total: float) -> Optional[str]:
        """Forma grupos de compra con otros consumidores"""
        # Buscar otros consumidores interesados
        consumidores_interesados = self._buscar_consumidores_interesados(bien)
        
        if len(consumidores_interesados) >= 2:  # Mínimo para grupo
            # Calcular beneficio potencial de compra grupal
            descuento_esperado = self._calcular_descuento_grupal(len(consumidores_interesados), cantidad_total)
            
            if descuento_esperado > 0.05:  # Mínimo 5% de descuento
                # Formar alianza de compra
                alianza_id = self.comunicacion.formar_alianza_temporal(
                    consumidores_interesados,
                    "compra_conjunta",
                    f"Compra grupal de {bien}",
                    duracion_dias=7
                )
                
                if alianza_id:
                    self.grupos_compra.append(alianza_id)
                    
                    # Coordinar compra grupal
                    self.comunicacion.enviar_mensaje(
                        "ALL",
                        TipoMensaje.COORDINACION_COMPRA,
                        {
                            'bien': bien,
                            'cantidad_total': cantidad_total,
                            'precio_objetivo': self._calcular_precio_objetivo(bien, 50),  # Placeholder
                            'participantes': [self.nombre] + consumidores_interesados,
                            'alianza_id': alianza_id
                        },
                        prioridad=PrioridadMensaje.ALTA
                    )
                    
                    return alianza_id
        
        return None
    
    def _buscar_consumidores_interesados(self, bien: str) -> List[str]:
        """Busca otros consumidores que podrían estar interesados en compra grupal"""
        # En implementación real, esto consultaría la red social del consumidor
        # y buscaría patrones de consumo similares
        
        interesados = []
        for contacto in self.red_social:
            # Simular interés basándose en probabilidad
            if random.random() < 0.3:  # 30% probabilidad de interés
                interesados.append(contacto)
        
        return interesados[:5]  # Máximo 5 para mantener grupo manejable
    
    def _calcular_descuento_grupal(self, num_participantes: int, cantidad_total: float) -> float:
        """Calcula el descuento esperado por compra grupal"""
        # Descuento base por volumen
        descuento_base = min(0.15, (num_participantes - 1) * 0.03)
        
        # Bonus por cantidad total
        if cantidad_total > 10:
            descuento_base += 0.05
        elif cantidad_total > 5:
            descuento_base += 0.02
        
        return descuento_base
    
    def adaptarse_a_crisis(self, tipo_crisis: str, severidad: float):
        """Adapta comportamiento durante crisis económicas"""
        print(f"[{self.nombre}] Adaptándose a crisis: {tipo_crisis} (severidad: {severidad:.2f})")
        
        # Ajustar parámetros según tipo de crisis
        if tipo_crisis == "financiera":
            self._adaptarse_crisis_financiera(severidad)
        elif tipo_crisis == "inflacion":
            self._adaptarse_crisis_inflacion(severidad)
        elif tipo_crisis == "desempleo":
            self._adaptarse_crisis_desempleo(severidad)
        elif tipo_crisis == "sanitaria":
            self._adaptarse_crisis_sanitaria(severidad)
        
        # Actualizar estado emocional y estrés
        self.stress_financiero = min(1.0, self.stress_financiero + severidad * 0.5)
        self.estado_emocional = max(0.1, self.estado_emocional - severidad * 0.3)
        self.confianza_mercado = max(0.1, self.confianza_mercado - severidad * 0.4)
        
        # Aprender de la crisis
        decision_crisis = Decision(
            agente_id=f"consumidor_{self.nombre}",
            tipo_decision="adaptacion_crisis",
            contexto={
                'tipo_crisis': tipo_crisis,
                'severidad': severidad,
                'dinero_disponible': self.dinero,
                'empleado': self.empleado
            },
            accion_tomada={
                'estrategia_adaptacion': tipo_crisis,
                'nivel_conservadurismo': severidad
            }
        )
        
        self.memoria.agregar_decision(decision_crisis)
    
    def _adaptarse_crisis_financiera(self, severidad: float):
        """Adaptación específica a crisis financiera"""
        # Reducir propensión al consumo
        factor_reduccion = 1 - severidad * 0.5
        self.propension_consumo = max(0.3, self.propension_consumo * factor_reduccion)
        
        # Aumentar propensión al ahorro
        self.propension_ahorro = min(0.9, 1 - self.propension_consumo)
        
        # Ajustar patrones de consumo - priorizar necesidades básicas
        for bien, patron in self.patrones_consumo.items():
            if self._es_bien_basico(bien):
                patron.utilidad_esperada *= 1.1  # Incrementar utilidad de básicos
            else:
                patron.utilidad_esperada *= (1 - severidad * 0.3)  # Reducir utilidad de lujos
    
    def _adaptarse_crisis_inflacion(self, severidad: float):
        """Adaptación específica a crisis inflacionaria"""
        # Ajustar precios máximos aceptables
        factor_inflacion = 1 + severidad * 0.2
        for patron in self.patrones_consumo.values():
            patron.precio_maximo_aceptable *= factor_inflacion
        
        # Aumentar frecuencia de compras de no perecederos
        for bien, patron in self.patrones_consumo.items():
            if self._es_bien_no_perecedero(bien):
                patron.frecuencia_promedio *= (1 - severidad * 0.2)  # Comprar más frecuentemente
    
    def _adaptarse_crisis_desempleo(self, severidad: float):
        """Adaptación específica a crisis de desempleo"""
        if not self.empleado or severidad > 0.7:
            # Modo supervivencia - solo necesidades básicas
            self.propension_consumo = max(0.2, self.propension_consumo * 0.5)
            
            # Buscar oportunidades de trabajo (simplificado)
            self._buscar_empleo_crisis()
    
    def _adaptarse_crisis_sanitaria(self, severidad: float):
        """Adaptación específica a crisis sanitaria"""
        # Cambiar patrones de consumo hacia productos de salud e higiene
        bienes_salud = ['medicina', 'higiene', 'alimentos_conserva']
        
        for bien in bienes_salud:
            if bien in self.patrones_consumo:
                self.patrones_consumo[bien].utilidad_esperada *= (1 + severidad * 0.3)
                self.patrones_consumo[bien].frecuencia_promedio *= (1 - severidad * 0.2)
    
    def _es_bien_basico(self, bien: str) -> bool:
        """Determina si un bien es básico/necesario"""
        bienes_basicos = ['alimentos', 'agua', 'medicina', 'vivienda', 'energia']
        return any(basico in bien.lower() for basico in bienes_basicos)
    
    def _es_bien_no_perecedero(self, bien: str) -> bool:
        """Determina si un bien es no perecedero"""
        no_perecederos = ['conserva', 'electronico', 'herramienta', 'ropa']
        return any(np in bien.lower() for np in no_perecederos)
    
    def _buscar_empleo_crisis(self):
        """Busca empleo durante crisis (simplificado)"""
        # En implementación real, esto interactuaría con el mercado laboral
        # Por ahora, solo actualizar estado
        print(f"[{self.nombre}] Buscando empleo durante crisis...")
    
    def tomar_decision_compra_ia(self, bien: str, precio: float, vendedor: str = None) -> bool:
        """Toma decisión de compra usando IA"""
        # Crear estado del mercado
        estado_mercado = EstadoMercado(
            precios={bien: precio},
            demanda={bien: self.predicciones_demanda.get(bien, 0.5)},
            oferta={bien: 1.0},  # Simplificado
            competidores=[vendedor] if vendedor else [],
            tendencias={},
            volatilidad={},
            ciclo_economico=getattr(self.mercado, 'ciclo_economico', 'expansion'),
            liquidez_mercado=1.0,
            riesgo_sistemico=0.1
        )
        
        # Crear opciones de decisión
        opcion_comprar = OpcionDecision(
            id="comprar",
            tipo="compra",
            parametros={'bien': bien, 'precio': precio, 'cantidad': 1},
            costo_estimado=precio,
            beneficio_estimado=self._calcular_utilidad_esperada(bien, precio),
            riesgo_estimado=self._calcular_riesgo_compra(bien, precio),
            complejidad=0.3
        )
        
        opcion_no_comprar = OpcionDecision(
            id="no_comprar",
            tipo="abstencion",
            parametros={},
            costo_estimado=0,
            beneficio_estimado=0,
            riesgo_estimado=0.1,  # Riesgo de perder oportunidad
            complejidad=0.1
        )
        
        # Usar IA para decidir
        decision_ia = self.ia_engine.tomar_decision_inteligente(
            estado_mercado, [opcion_comprar, opcion_no_comprar]
        )
        
        # Registrar decisión
        decision = Decision(
            agente_id=f"consumidor_{self.nombre}",
            tipo_decision="compra",
            contexto={
                'bien': bien,
                'precio': precio,
                'vendedor': vendedor,
                'dinero_disponible': self.dinero,
                'utilidad_esperada': opcion_comprar.beneficio_estimado
            },
            accion_tomada={
                'decision': decision_ia.id,
                'precio_pagado': precio if decision_ia.id == "comprar" else 0
            },
            estado_previo={'dinero': self.dinero, 'utilidad': self.utilidad_total_ia}
        )
        
        resultado_compra = decision_ia.id == "comprar"
        
        if resultado_compra:
            # Intentar negociar antes de comprar
            precio_negociado = self.negociar_precios_inteligente(vendedor, bien, 1, precio) if vendedor else None
            precio_final = precio_negociado if precio_negociado else precio
            
            # Realizar compra si hay dinero suficiente
            if self.dinero >= precio_final:
                self.dinero -= precio_final
                self.bienes[bien] = self.bienes.get(bien, 0) + 1
                
                # Actualizar historial
                if bien not in self.historial_compras:
                    self.historial_compras[bien] = []
                
                self.historial_compras[bien].append({
                    'precio': precio_final,
                    'cantidad': 1,
                    'vendedor': vendedor,
                    'timestamp': datetime.now(),
                    'negociado': precio_negociado is not None
                })
                
                # Calcular utilidad obtenida
                utilidad_obtenida = self._calcular_utilidad_real(bien, precio_final)
                self.utilidad_total_ia += utilidad_obtenida
                
                # Actualizar reputación del vendedor
                if vendedor:
                    satisfaccion = utilidad_obtenida / max(precio_final, 1)
                    self._actualizar_reputacion_vendedor(vendedor, satisfaccion)
                
                # Completar decision con resultado
                decision.resultado = {
                    'compra_realizada': True,
                    'precio_final': precio_final,
                    'utilidad_obtenida': utilidad_obtenida,
                    'ahorro_negociacion': precio - precio_final if precio_negociado else 0
                }
                decision.recompensa = utilidad_obtenida - precio_final
                
                # Aprender de la experiencia
                self.memoria.aprender_de_experiencia(decision, decision.resultado)
                
                # Actualizar métricas
                self.compras_optimizadas += 1
                if precio_negociado:
                    self.ahorro_obtenido_ia += precio - precio_final
                    self.negociaciones_exitosas += 1
                
                return True
            else:
                decision.resultado = {'compra_realizada': False, 'razon': 'fondos_insuficientes'}
                decision.recompensa = -10  # Penalización por decisión incorrecta
        else:
            decision.resultado = {'compra_realizada': False, 'razon': 'decision_ia_negativa'}
            decision.recompensa = 0
        
        # Aprender de la experiencia
        self.memoria.aprender_de_experiencia(decision, decision.resultado)
        
        return False
    
    def _calcular_utilidad_esperada(self, bien: str, precio: float) -> float:
        """Calcula la utilidad esperada de comprar un bien"""
        # Usar patrón aprendido si está disponible
        if bien in self.patrones_consumo:
            patron = self.patrones_consumo[bien]
            utilidad_base = patron.utilidad_esperada
            
            # Ajustar por precio vs precio esperado
            if precio <= patron.precio_maximo_aceptable:
                factor_precio = 1.0 + (patron.precio_maximo_aceptable - precio) / patron.precio_maximo_aceptable
            else:
                factor_precio = 0.5  # Penalizar precios altos
            
            return utilidad_base * factor_precio
        
        # Fallback: cálculo básico
        utilidad_base = 50 - precio * 0.5  # Utilidad decrece con precio
        return max(0, utilidad_base)
    
    def _calcular_utilidad_real(self, bien: str, precio: float) -> float:
        """Calcula la utilidad real obtenida después de la compra"""
        # Utilidad base del bien
        utilidad_base = self._calcular_utilidad_esperada(bien, precio)
        
        # Factores que afectan utilidad real
        factor_estado_emocional = 0.8 + self.estado_emocional * 0.4
        factor_necesidad = self._calcular_factor_necesidad(bien)
        factor_calidad = random.uniform(0.8, 1.2)  # Variabilidad de calidad
        
        utilidad_real = utilidad_base * factor_estado_emocional * factor_necesidad * factor_calidad
        
        # Actualizar estado emocional basándose en satisfacción
        satisfaccion = min(1.0, utilidad_real / (precio + 1))
        self.estado_emocional = min(1.0, self.estado_emocional + satisfaccion * 0.1)
        
        return utilidad_real
    
    def _calcular_factor_necesidad(self, bien: str) -> float:
        """Calcula qué tan necesario es el bien actualmente"""
        if bien in self.predicciones_demanda:
            return 0.5 + self.predicciones_demanda[bien] * 0.5
        
        # Si no tenemos el bien, es más necesario
        cantidad_actual = self.bienes.get(bien, 0)
        if cantidad_actual == 0:
            return 1.0
        elif cantidad_actual < 3:
            return 0.8
        else:
            return 0.5
    
    def _calcular_riesgo_compra(self, bien: str, precio: float) -> float:
        """Calcula el riesgo asociado con la compra"""
        riesgo_base = 0.1
        
        # Riesgo por precio alto
        if bien in self.patrones_consumo:
            precio_esperado = self.patrones_consumo[bien].precio_maximo_aceptable
            if precio > precio_esperado:
                riesgo_base += (precio - precio_esperado) / precio_esperado
        
        # Riesgo por situación financiera
        if precio > self.dinero * 0.3:  # Más del 30% del dinero
            riesgo_base += 0.3
        
        # Riesgo por estrés financiero
        riesgo_base += self.stress_financiero * 0.2
        
        return min(1.0, riesgo_base)
    
    def _actualizar_reputacion_vendedor(self, vendedor: str, satisfaccion: float):
        """Actualiza la reputación de un vendedor basándose en la experiencia"""
        if vendedor in self.reputacion_vendedores:
            # Promedio móvil
            self.reputacion_vendedores[vendedor] = (
                self.reputacion_vendedores[vendedor] * 0.8 + satisfaccion * 0.2
            )
        else:
            self.reputacion_vendedores[vendedor] = satisfaccion
    
    def actualizar_red_social(self, nuevos_contactos: List[str]):
        """Actualiza la red social del consumidor"""
        for contacto in nuevos_contactos:
            if contacto not in self.red_social and contacto != self.nombre:
                self.red_social.append(contacto)
        
        # Limitar tamaño de red social
        if len(self.red_social) > 20:
            # Mantener solo los más relevantes (simplificado: aleatorio)
            self.red_social = self.red_social[-20:]
    
    def procesar_ciclo_ia(self):
        """Procesa un ciclo completo de IA del consumidor"""
        try:
            # 1. Aprender patrones de consumo
            self.aprender_patrones_consumo()
            
            # 2. Predecir necesidades futuras
            self.predecir_necesidades_futuras()
            
            # 3. Procesar comunicaciones
            # (El protocolo de comunicación ya maneja esto en su hilo)
            
            # 4. Evaluar oportunidades de grupos de compra
            for bien in self.predicciones_demanda:
                if self.predicciones_demanda[bien] > 0.7:  # Alta necesidad
                    self.formar_grupos_compra(bien, 5.0)  # Cantidad ejemplo
            
            # 5. Actualizar estado emocional
            self._actualizar_estado_emocional()
            
            # 6. Tomar decisiones proactivas
            self._decisiones_proactivas()
            
        except Exception as e:
            print(f"[{self.nombre}] Error en ciclo IA: {e}")
    
    def _actualizar_estado_emocional(self):
        """Actualiza el estado emocional del consumidor"""
        # Recuperación gradual del estrés
        self.stress_financiero = max(0.0, self.stress_financiero - 0.02)
        
        # Mejora gradual del estado emocional
        if self.dinero > 1000:  # Situación financiera estable
            self.estado_emocional = min(1.0, self.estado_emocional + 0.01)
        
        # Recuperación de confianza en el mercado
        if not hasattr(self.mercado, 'en_crisis') or not self.mercado.en_crisis:
            self.confianza_mercado = min(1.0, self.confianza_mercado + 0.02)
    
    def _decisiones_proactivas(self):
        """Toma decisiones proactivas basándose en predicciones"""
        # Decisión de ahorro vs consumo
        if self.predicciones_demanda:
            demanda_total = sum(self.predicciones_demanda.values())
            if demanda_total < 0.3:  # Baja demanda predicha
                # Aumentar ahorro
                self.propension_ahorro = min(0.8, self.propension_ahorro + 0.05)
                self.propension_consumo = 1 - self.propension_ahorro
    
    def get_estadisticas_ia(self) -> Dict[str, Any]:
        """Obtiene estadísticas del sistema IA del consumidor"""
        return {
            'agente_id': f"consumidor_{self.nombre}",
            'perfil_personalidad': self.perfil_aprendizaje.tipo_personalidad,
            'patrones_aprendidos': len(self.patrones_consumo),
            'red_social_tamaño': len(self.red_social),
            'grupos_compra_activos': len(self.grupos_compra),
            'compras_optimizadas': self.compras_optimizadas,
            'negociaciones_exitosas': self.negociaciones_exitosas,
            'ahorro_total_ia': self.ahorro_obtenido_ia,
            'utilidad_total_ia': self.utilidad_total_ia,
            'estado_emocional': self.estado_emocional,
            'confianza_mercado': self.confianza_mercado,
            'stress_financiero': self.stress_financiero,
            'predicciones_activas': len(self.predicciones_demanda),
            'vendedores_conocidos': len(self.reputacion_vendedores),
            'memoria_decisiones': self.memoria.experiencia_total,
            'tasa_exito_ia': self.memoria.tasa_exito,
            'ia_engine_stats': self.ia_engine.get_estadisticas_ia(),
            'comunicacion_stats': self.comunicacion.get_estadisticas_comunicacion()
        }
    
    def actualizar_conocimiento_mercado(self, estado_mercado):
        """Actualiza el conocimiento del mercado del consumidor"""
        try:
            # Convertir EstadoMercado a diccionario si es necesario
            if hasattr(estado_mercado, '__dict__'):
                estado_dict = estado_mercado.__dict__
            elif isinstance(estado_mercado, dict):
                estado_dict = estado_mercado
            else:
                # Si no es convertible, crear un diccionario básico
                estado_dict = {}
            
            # Actualizar información de precios
            if 'precios' in estado_dict:
                for bien, precio in estado_dict['precios'].items():
                    if bien in self.patrones_consumo:
                        patron = self.patrones_consumo[bien]
                        # Actualizar precio máximo aceptable basado en tendencias
                        precio_actual = float(precio)
                        patron.precio_maximo_aceptable = (patron.precio_maximo_aceptable * 0.9 + 
                                                        precio_actual * 1.1 * 0.1)
            
            # Actualizar predicciones de demanda
            if 'demanda_global' in estado_dict:
                self.predicciones_demanda.update(estado_dict['demanda_global'])
            
            # Actualizar conocimiento de crisis
            if 'en_crisis' in estado_dict:
                if estado_dict['en_crisis']:
                    self.confianza_mercado *= 0.95
                    self.stress_financiero = min(1.0, self.stress_financiero + 0.1)
                else:
                    self.confianza_mercado = min(1.0, self.confianza_mercado + 0.02)
            
            # Actualizar estado económico general
            if 'pib' in estado_dict:
                pib_actual = estado_dict['pib']
                if hasattr(self, 'ultimo_pib'):
                    if pib_actual < self.ultimo_pib:
                        # Economía empeorando
                        self.propension_ahorro = min(0.8, self.propension_ahorro + 0.05)
                    else:
                        # Economía mejorando
                        self.propension_consumo = min(0.7, self.propension_consumo + 0.02)
                self.ultimo_pib = pib_actual
            
        except Exception as e:
            print(f"[{self.nombre}] Error actualizando conocimiento de mercado: {e}")

    def finalizar_ia(self):
        """Finaliza todos los componentes IA del consumidor"""
        try:
            self.comunicacion.finalizar()
            print(f"[{self.nombre}] Sistemas IA finalizados")
        except Exception as e:
            print(f"[{self.nombre}] Error finalizando IA: {e}")
