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
from .PerfilPersonalidadIA import GeneradorPerfilesPersonalidad, PerfilPersonalidadCompleto, TipoPersonalidad
from .ComportamientoCompraIA import SistemaComportamientoCompra, ContextoCompra, ExperienciaCompra
from ..models.BienHiperrealista import BienHiperrealista, TipoBien


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
        
        # Generar perfil único de personalidad hiperrealista
        self.perfil_personalidad_completo = GeneradorPerfilesPersonalidad.generar_perfil_unico()
        
        # Sistema de comportamiento de compra personalizado
        self.sistema_comportamiento = SistemaComportamientoCompra(self.perfil_personalidad_completo)
        
        # Componentes IA existentes
        self.ia_engine = IADecisionEngine(f"consumidor_{nombre}")
        self.memoria = AgentMemorySystem(f"consumidor_{nombre}")
        self.comunicacion = AgentCommunicationProtocol(f"consumidor_{nombre}")
        
        # Perfil de aprendizaje IA (mantener compatibilidad)
        self.perfil_aprendizaje = self._convertir_a_perfil_aprendizaje()
        
        # Patrones de consumo aprendidos - ahora más sofisticados
        self.patrones_consumo: Dict[str, PatronConsumo] = {}
        self.preferencias_dinamicas: Dict[str, float] = {}
        
        # Sistema de predicción de necesidades mejorado
        self.calendario_necesidades: Dict[datetime, List[str]] = {}
        self.predicciones_demanda: Dict[str, float] = {}
        
        # Red social y colaboración
        self.red_social: List[str] = []
        self.grupos_compra: List[str] = []
        self.influencers_seguidos: List[str] = []
        
        # Historial de negociaciones
        self.historial_negociaciones: List[Dict[str, Any]] = []
        self.reputacion_vendedores: Dict[str, float] = {}
        
        # Métricas de eficiencia IA
        self.ahorro_obtenido_ia = 0.0
        self.compras_optimizadas = 0
        self.negociaciones_exitosas = 0
        self.utilidad_total_ia = 0.0
        
        # Estado emocional y psicológico - integrado con perfil
        self.estado_emocional = self.perfil_personalidad_completo.satisfaccion_vida
        self.confianza_mercado = self.perfil_personalidad_completo.confianza_economia
        self.stress_financiero = self.perfil_personalidad_completo.stress_financiero
        
        # Características únicas basadas en personalidad
        self._aplicar_caracteristicas_personalidad()
        
        # Inicializar IA
        self._inicializar_sistema_ia()
        
        # Contexto de compra dinámico
        self.contexto_compra_actual = ContextoCompra()
        
        # Precios ancla para sesgos cognitivos
        self.precios_ancla: Dict[str, float] = {}
        
        print(f"[{self.nombre}] Consumidor IA inicializado: {self.perfil_personalidad_completo.get_descripcion_personalidad()}")
    
    def _convertir_a_perfil_aprendizaje(self) -> PerfilAprendizajeIA:
        """Convierte el perfil de personalidad completo al formato de aprendizaje IA anterior"""
        return PerfilAprendizajeIA(
            tipo_personalidad=self.perfil_personalidad_completo.tipo_personalidad.value,
            velocidad_aprendizaje=self.perfil_personalidad_completo.rasgos_psicologicos.apertura * 0.8 + 0.2,
            tolerancia_riesgo=1.0 - self.perfil_personalidad_completo.rasgos_psicologicos.aversion_riesgo,
            influencia_social=self.perfil_personalidad_completo.rasgos_psicologicos.conformidad_social,
            memoria_preferencias=int(50 + self.perfil_personalidad_completo.rasgos_psicologicos.responsabilidad * 50),
            adaptabilidad_crisis=self.perfil_personalidad_completo.rasgos_psicologicos.apertura * 0.6 + 0.4
        )
    
    def _aplicar_caracteristicas_personalidad(self):
        """Aplica características únicas basadas en el perfil de personalidad"""
        
        rasgos = self.perfil_personalidad_completo.rasgos_psicologicos
        prefs = self.perfil_personalidad_completo.preferencias_consumo
        contexto = self.perfil_personalidad_completo.contexto_socioeconomico
        
        # Ajustar propensión al consumo basándose en personalidad
        if self.perfil_personalidad_completo.tipo_personalidad == TipoPersonalidad.HEDONISTA:
            self.propension_consumo = min(0.95, self.propension_consumo * 1.2)
        elif self.perfil_personalidad_completo.tipo_personalidad == TipoPersonalidad.MINIMALISTA:
            self.propension_consumo = max(0.3, self.propension_consumo * 0.7)
        elif self.perfil_personalidad_completo.tipo_personalidad == TipoPersonalidad.CONSERVADOR:
            self.propension_consumo = max(0.4, self.propension_consumo * 0.9)
        
        # Ajustar ingreso mensual basándose en educación y ocupación
        factor_educacion = {
            'basico': 0.8, 'secundario': 1.0, 'tecnico': 1.2, 
            'universitario': 1.5, 'postgrado': 2.0
        }
        factor = factor_educacion.get(contexto.nivel_educativo.value, 1.0)
        
        if self.empleado:
            self.ingreso_mensual = int(self.ingreso_mensual * factor)
        
        # Ajustar aversión al riesgo financiero
        self.aversion_riesgo = rasgos.aversion_riesgo
        
        # Personalizar factor de imitación social
        self.factor_imitacion = rasgos.conformidad_social * 0.8
        
        # Personalizar fidelidad de marca
        self.fidelidad_marca = rasgos.importancia_marca
        
        # Características demográficas únicas adicionales
        if self.perfil_personalidad_completo.estilo_vida.value == 'ecologico':
            # Preferencia por productos sostenibles
            self.preferencia_sostenibilidad = 0.9
        elif self.perfil_personalidad_completo.estilo_vida.value == 'lujoso':
            # Preferencia por productos premium
            self.preferencia_lujo = 0.8
        elif self.perfil_personalidad_completo.estilo_vida.value == 'frugal':
            # Mayor enfoque en precio
            self.sensibilidad_precio = 0.9
        
        # Personalizar tolerancias únicas
        self.tolerancia_espera = rasgos.planificacion * 100 + 10  # minutos
        self.tolerancia_precio_alto = prefs.umbral_precio_alto
        self.umbral_descuento_atractivo = prefs.umbral_descuento_atractivo
    
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
    
    def tomar_decision_compra_hiperrealista(self, bien: str, precio: float, vendedor: str = None, 
                                          contexto_mercado: Dict[str, Any] = None) -> bool:
        """Toma decisión de compra usando el sistema hiperrealista completo"""
        
        # Crear o buscar el bien hiperrealista
        bien_obj = self._obtener_bien_hiperrealista(bien, precio)
        if not bien_obj:
            return False
        
        # Actualizar contexto de compra
        self._actualizar_contexto_compra(precio, contexto_mercado or {})
        
        # Evaluar opción usando sistema de comportamiento
        evaluacion = self.sistema_comportamiento.evaluar_opcion_compra(
            bien_obj, precio, vendedor or "desconocido", self.contexto_compra_actual
        )
        
        # Establecer precio ancla si es la primera vez que ve el bien
        if bien not in self.precios_ancla:
            self.precios_ancla[bien] = precio
            # Aplicar sesgo de anclaje al sistema de comportamiento
            self.sistema_comportamiento.precio_ancla = precio
        
        # Decidir si comprar basándose en probabilidad
        decidir_comprar = random.random() < evaluacion['probabilidad_compra']
        
        # Intentar negociar si es recomendado
        precio_final = precio
        negociacion_exitosa = False
        
        if decidir_comprar and evaluacion['recomendaria_negociar'] and vendedor:
            precio_negociado = self.negociar_precios_inteligente(vendedor, bien, 1, precio)
            if precio_negociado and precio_negociado < precio:
                precio_final = precio_negociado
                negociacion_exitosa = True
                self.negociaciones_exitosas += 1
                self.ahorro_obtenido_ia += precio - precio_final
        
        # Realizar compra si se decidió comprar y hay fondos
        if decidir_comprar and self.dinero >= precio_final:
            # Realizar transacción
            self.dinero -= precio_final
            if bien not in self.bienes:
                self.bienes[bien] = 0
            self.bienes[bien] += 1
            
            # Calcular satisfacción obtenida
            satisfaccion = self._calcular_satisfaccion_compra(bien_obj, precio_final, evaluacion)
            
            # Registrar experiencia
            experiencia = ExperienciaCompra(
                bien=bien,
                vendedor=vendedor or "desconocido",
                precio_pagado=precio_final,
                calidad_percibida=bien_obj.factor_calidad_global,
                satisfaccion=satisfaccion,
                tiempo_decision=evaluacion['tiempo_decision_estimado'],
                fecha=datetime.now(),
                contexto=self.contexto_compra_actual,
                resultado_negociacion=precio - precio_final if negociacion_exitosa else None,
                recomendaria=satisfaccion > 0.6
            )
            
            self.sistema_comportamiento.registrar_experiencia_compra(experiencia)
            
            # Actualizar estado emocional basándose en satisfacción
            self.perfil_personalidad_completo.actualizar_estado_emocional(
                "compra_exitosa", satisfaccion * 0.2
            )
            
            # Actualizar métricas
            self.compras_optimizadas += 1
            utilidad_obtenida = self._calcular_utilidad_real(bien, precio_final)
            self.utilidad_total_ia += utilidad_obtenida
            
            # Registrar decisión para aprendizaje
            decision = Decision(
                agente_id=f"consumidor_{self.nombre}",
                tipo_decision="compra_hiperrealista",
                contexto={
                    'bien': bien,
                    'precio': precio,
                    'precio_final': precio_final,
                    'vendedor': vendedor,
                    'evaluacion': evaluacion
                },
                accion_tomada={
                    'compra_realizada': True,
                    'negociacion': negociacion_exitosa,
                    'satisfaccion': satisfaccion
                },
                resultado={'utilidad_obtenida': utilidad_obtenida},
                recompensa=satisfaccion * 100 - precio_final
            )
            
            self.memoria.agregar_decision(decision)
            
            # Aprender de la experiencia
            self.memoria.aprender_de_experiencia(decision, decision.resultado)
            
            print(f"[{self.nombre}] Compró {bien} por ${precio_final:.2f} (satisfacción: {satisfaccion:.2f})")
            return True
        
        elif decidir_comprar:
            # Quería comprar pero no tenía dinero
            self.perfil_personalidad_completo.actualizar_estado_emocional("compra_fallida", 0.1)
            print(f"[{self.nombre}] Quería comprar {bien} pero no tiene fondos suficientes")
        
        return False
    
    def _obtener_bien_hiperrealista(self, nombre_bien: str, precio: float) -> Optional[BienHiperrealista]:
        """Obtiene o crea un objeto BienHiperrealista"""
        
        # Intentar inferir tipo de bien basándose en el nombre
        tipo_bien = self._inferir_tipo_bien(nombre_bien)
        
        # Crear bien hiperrealista
        try:
            bien = BienHiperrealista(nombre_bien, tipo_bien)
            # Ajustar precio base si es muy diferente al observado
            if abs(bien.precio_base_sugerido - precio) > precio * 0.5:
                bien.economicas.costo_produccion_base = precio * 0.7
                bien._actualizar_valores_derivados()
            return bien
        except Exception as e:
            print(f"[{self.nombre}] Error creando bien hiperrealista para {nombre_bien}: {e}")
            return None
    
    def _inferir_tipo_bien(self, nombre_bien: str) -> TipoBien:
        """Infiere el tipo de bien basándose en su nombre"""
        
        nombre_lower = nombre_bien.lower()
        
        # Mapeo de palabras clave a tipos de bien
        mapeo_tipos = {
            ('arroz', 'papa', 'pan', 'leche', 'sal', 'aceite'): TipoBien.ALIMENTO_BASICO,
            ('carne', 'pollo', 'cafe', 'azucar', 'huevos'): TipoBien.ALIMENTO_PREMIUM,
            ('telefono', 'celular', 'computer', 'laptop'): TipoBien.ELECTRONICO_PREMIUM,
            ('tv', 'television', 'radio'): TipoBien.ELECTRONICO_BASICO,
            ('camisa', 'pantalon', 'zapatos', 'ropa'): TipoBien.ROPA_BASICA,
            ('vestido', 'traje', 'marca'): TipoBien.ROPA_MODA,
            ('casa', 'apartamento', 'hogar'): TipoBien.HOGAR_LUJO,
            ('mueble', 'mesa', 'silla'): TipoBien.HOGAR_BASICO,
            ('medicina', 'medicamento', 'salud'): TipoBien.SALUD,
            ('curso', 'libro', 'educacion'): TipoBien.EDUCACION,
            ('pelicula', 'juego', 'entretenimiento'): TipoBien.ENTRETENIMIENTO
        }
        
        for palabras_clave, tipo_bien in mapeo_tipos.items():
            if any(palabra in nombre_lower for palabra in palabras_clave):
                return tipo_bien
        
        # Tipo por defecto
        return TipoBien.SERVICIO_BASICO
    
    def _actualizar_contexto_compra(self, precio: float, contexto_mercado: Dict[str, Any]):
        """Actualiza el contexto de compra actual"""
        
        # Calcular urgencia basándose en necesidades predichas
        urgencia_base = 0.5
        if self.predicciones_demanda:
            max_demanda = max(self.predicciones_demanda.values())
            urgencia_base = min(1.0, max_demanda)
        
        # Calcular presupuesto disponible
        presupuesto = self.dinero * self.propension_consumo
        
        # Evaluar estado emocional actual
        estado_emocional = (
            self.perfil_personalidad_completo.satisfaccion_vida * 0.4 +
            (1.0 - self.perfil_personalidad_completo.stress_financiero) * 0.3 +
            self.perfil_personalidad_completo.confianza_economia * 0.3
        )
        
        # Determinar tiempo disponible basándose en personalidad
        tiempo_disponible = 1.0
        if self.perfil_personalidad_completo.rasgos_psicologicos.impulsividad > 0.7:
            tiempo_disponible = 0.3  # Impulsivos no dedican mucho tiempo
        elif self.perfil_personalidad_completo.tipo_personalidad == TipoPersonalidad.ESTRATEGICO:
            tiempo_disponible = 1.0  # Estratégicos toman su tiempo
        
        self.contexto_compra_actual = ContextoCompra(
            urgencia=urgencia_base,
            presupuesto_disponible=presupuesto,
            tiempo_disponible=tiempo_disponible,
            compañia=random.choice(['solo', 'familia', 'amigos']) if random.random() < 0.3 else 'solo',
            ubicacion=random.choice(['casa', 'trabajo', 'tienda', 'online']),
            estado_emocional=estado_emocional,
            evento_especial=contexto_mercado.get('evento_actual')
        )
    
    def _calcular_satisfaccion_compra(self, bien: BienHiperrealista, precio_pagado: float, 
                                    evaluacion: Dict[str, Any]) -> float:
        """Calcula la satisfacción obtenida de una compra"""
        
        # Satisfacción base por utilidad vs precio
        utilidad_esperada = bien.atractivo_emocional
        costo_relativo = precio_pagado / max(1.0, self.dinero * 0.1)  # % del dinero gastado
        
        satisfaccion_base = max(0.0, utilidad_esperada - costo_relativo * 0.5)
        
        # Ajustar por compatibilidad con perfil
        compatibilidad = bien.es_compatible_con_perfil(self.perfil_personalidad_completo)
        satisfaccion_base *= (0.7 + compatibilidad * 0.6)
        
        # Ajustar por expectativas vs realidad
        puntuacion_evaluacion = evaluacion['puntuacion_total']
        if satisfaccion_base > puntuacion_evaluacion:
            satisfaccion_final = satisfaccion_base * 1.1  # Superó expectativas
        elif satisfaccion_base < puntuacion_evaluacion * 0.7:
            satisfaccion_final = satisfaccion_base * 0.8  # No cumplió expectativas
        else:
            satisfaccion_final = satisfaccion_base
        
        # Aplicar factores de personalidad
        if self.perfil_personalidad_completo.tipo_personalidad == TipoPersonalidad.HEDONISTA:
            satisfaccion_final *= 1.2  # Los hedonistas disfrutan más las compras
        elif self.perfil_personalidad_completo.tipo_personalidad == TipoPersonalidad.CONSERVADOR:
            satisfaccion_final *= 0.9  # Los conservadores son más críticos
        
        # Agregar variabilidad realista
        variabilidad = random.uniform(0.8, 1.2)
        satisfaccion_final *= variabilidad
        
        return max(0.0, min(1.0, satisfaccion_final))
    
    def explorar_y_aprender_mercado(self, mercado_actual):
        """Explora el mercado activamente y aprende patrones"""
        
        # Solo explorar si la personalidad lo permite
        if self.perfil_personalidad_completo.rasgos_psicologicos.apertura < 0.3:
            return  # Personalidades cerradas no exploran mucho
        
        # Buscar bienes nuevos o con tendencias interesantes
        bienes_explorar = []
        
        if hasattr(mercado_actual, 'bienes'):
            for nombre_bien in mercado_actual.bienes.keys():
                # Explorar bienes que no ha comprado antes
                if nombre_bien not in [exp.bien for exp in self.sistema_comportamiento.experiencias_compra]:
                    bien_obj = self._obtener_bien_hiperrealista(nombre_bien, 50.0)  # Precio estimado
                    if bien_obj and bien_obj.factores_sociales.tendencia_crecimiento > 0.2:
                        bienes_explorar.append(nombre_bien)
        
        # Explorar 1-2 bienes si hay presupuesto y interés
        if bienes_explorar and self.dinero > self.ingreso_mensual * 0.5:
            num_explorar = random.randint(1, min(2, len(bienes_explorar)))
            bienes_a_explorar = random.sample(bienes_explorar, num_explorar)
            
            for bien in bienes_a_explorar:
                # Agregar a lista de deseos para considerar en futuras compras
                self.sistema_comportamiento.productos_lista_deseos.add(bien)
                
                # Pequeña probabilidad de compra exploratoria
                if random.random() < 0.1:  # 10% de probabilidad
                    empresas_disponibles = [e for e in mercado_actual.getEmpresas()
                                          if bien in e.bienes and len(e.bienes[bien]) > 0]
                    if empresas_disponibles:
                        empresa = random.choice(empresas_disponibles)
                        precio = empresa.precios.get(bien, 50.0)
                        self.tomar_decision_compra_hiperrealista(bien, precio, empresa.nombre)
    
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
    
    def procesar_ciclo_ia_hiperrealista(self, mercado_actual):
        """Procesa un ciclo completo de IA hiperrealista del consumidor"""
        try:
            # 1. Actualizar conocimiento del mercado
            self.actualizar_conocimiento_mercado_avanzado(mercado_actual)
            
            # 2. Procesar evolución de personalidad
            self._procesar_evolucion_personalidad()
            
            # 3. Aprender patrones de consumo más sofisticados
            self.aprender_patrones_consumo_avanzados()
            
            # 4. Predecir necesidades futuras con IA
            self.predecir_necesidades_futuras()
            
            # 5. Explorar mercado y aprender
            if random.random() < 0.3:  # 30% probabilidad de exploración
                self.explorar_y_aprender_mercado(mercado_actual)
            
            # 6. Evaluar oportunidades de grupos de compra
            self._evaluar_oportunidades_compra_grupal()
            
            # 7. Actualizar red social
            self._actualizar_red_social_dinamica(mercado_actual)
            
            # 8. Procesar comunicaciones IA
            # (El protocolo de comunicación ya maneja esto automáticamente)
            
            # 9. Tomar decisiones proactivas mejoradas
            self._decisiones_proactivas_avanzadas(mercado_actual)
            
            # 10. Actualizar estado emocional y estrés
            self._actualizar_estado_psicologico()
            
        except Exception as e:
            print(f"[{self.nombre}] Error en ciclo IA hiperrealista: {e}")
    
    def _procesar_evolucion_personalidad(self):
        """Procesa la evolución gradual de la personalidad"""
        
        # La personalidad puede evolucionar lentamente basándose en experiencias
        if len(self.sistema_comportamiento.experiencias_compra) > 20:
            experiencias_recientes = self.sistema_comportamiento.experiencias_compra[-10:]
            satisfaccion_promedio = sum(exp.satisfaccion for exp in experiencias_recientes) / len(experiencias_recientes)
            
            # Si las experiencias han sido muy positivas, aumentar confianza y reducir aversión al riesgo
            if satisfaccion_promedio > 0.8:
                ajuste = 0.001  # Evolución muy lenta
                self.perfil_personalidad_completo.rasgos_psicologicos.aversion_riesgo = max(0.0, 
                    self.perfil_personalidad_completo.rasgos_psicologicos.aversion_riesgo - ajuste)
                self.perfil_personalidad_completo.confianza_economia = min(1.0,
                    self.perfil_personalidad_completo.confianza_economia + ajuste)
            
            # Si han sido muy negativas, aumentar aversión al riesgo
            elif satisfaccion_promedio < 0.3:
                ajuste = 0.002
                self.perfil_personalidad_completo.rasgos_psicologicos.aversion_riesgo = min(1.0,
                    self.perfil_personalidad_completo.rasgos_psicologicos.aversion_riesgo + ajuste)
                self.perfil_personalidad_completo.confianza_economia = max(0.0,
                    self.perfil_personalidad_completo.confianza_economia - ajuste)
    
    def aprender_patrones_consumo_avanzados(self):
        """Versión avanzada del aprendizaje de patrones que usa el comportamiento de compra"""
        
        if not self.sistema_comportamiento.experiencias_compra:
            return
        
        # Agrupar experiencias por bien
        experiencias_por_bien = {}
        for exp in self.sistema_comportamiento.experiencias_compra:
            if exp.bien not in experiencias_por_bien:
                experiencias_por_bien[exp.bien] = []
            experiencias_por_bien[exp.bien].append(exp)
        
        # Actualizar patrones para cada bien
        for bien, experiencias in experiencias_por_bien.items():
            if len(experiencias) >= 2:
                self._actualizar_patron_consumo_avanzado(bien, experiencias)
    
    def _actualizar_patron_consumo_avanzado(self, bien: str, experiencias: List[ExperienciaCompra]):
        """Actualiza patrón de consumo usando experiencias detalladas"""
        
        if bien not in self.patrones_consumo:
            self._inicializar_patron_consumo(bien)
        
        patron = self.patrones_consumo[bien]
        
        # Calcular estadísticas de las experiencias
        precios_pagados = [exp.precio_pagado for exp in experiencias]
        satisfacciones = [exp.satisfaccion for exp in experiencias]
        tiempos_decision = [exp.tiempo_decision for exp in experiencias]
        
        # Actualizar precio máximo aceptable basándose en experiencias reales
        if satisfacciones:
            # Correlacionar precio con satisfacción
            precio_optimo = 0
            mejor_satisfaccion = 0
            
            for precio, satisfaccion in zip(precios_pagados, satisfacciones):
                if satisfaccion > mejor_satisfaccion:
                    mejor_satisfaccion = satisfaccion
                    precio_optimo = precio
            
            if precio_optimo > 0:
                # Actualizar precio máximo con learning rate
                learning_rate = self.perfil_aprendizaje.velocidad_aprendizaje * 0.1
                patron.precio_maximo_aceptable = (
                    patron.precio_maximo_aceptable * (1 - learning_rate) +
                    precio_optimo * 1.2 * learning_rate  # 20% más que el precio óptimo observado
                )
        
        # Actualizar utilidad esperada basándose en satisfacción promedio
        if satisfacciones:
            satisfaccion_promedio = sum(satisfacciones) / len(satisfacciones)
            learning_rate = self.perfil_aprendizaje.velocidad_aprendizaje * 0.05
            patron.utilidad_esperada = (
                patron.utilidad_esperada * (1 - learning_rate) +
                satisfaccion_promedio * learning_rate
            )
        
        # Incrementar confianza en el patrón
        patron.confianza = min(1.0, patron.confianza + 0.05)
        
        # Aprender factores estacionales si hay suficientes datos
        if len(experiencias) >= 6:
            self._aprender_factores_estacionales(bien, experiencias)
    
    def _aprender_factores_estacionales(self, bien: str, experiencias: List[ExperienciaCompra]):
        """Aprende factores estacionales basándose en experiencias históricas"""
        
        # Agrupar por mes
        compras_por_mes = {}
        for exp in experiencias:
            mes = exp.fecha.month
            if mes not in compras_por_mes:
                compras_por_mes[mes] = 0
            compras_por_mes[mes] += 1
        
        if len(compras_por_mes) >= 3:  # Al menos 3 meses diferentes
            # Actualizar factores estacionales del patrón
            promedio_mensual = sum(compras_por_mes.values()) / len(compras_por_mes)
            
            for mes, cantidad in compras_por_mes.items():
                factor_observado = cantidad / promedio_mensual
                mes_nombre = ['ene', 'feb', 'mar', 'abr', 'may', 'jun',
                             'jul', 'ago', 'sep', 'oct', 'nov', 'dic'][mes-1]
                
                # Actualizar con learning rate
                if mes_nombre not in self.patrones_consumo[bien].estacionalidad:
                    self.patrones_consumo[bien].estacionalidad[mes_nombre] = factor_observado
                else:
                    current = self.patrones_consumo[bien].estacionalidad[mes_nombre]
                    self.patrones_consumo[bien].estacionalidad[mes_nombre] = (
                        current * 0.8 + factor_observado * 0.2
                    )
    
    def actualizar_conocimiento_mercado_avanzado(self, mercado_actual):
        """Versión avanzada de actualización de conocimiento de mercado"""
        
        try:
            # Recopilar información del estado del mercado
            estado_mercado = {
                'precios': {},
                'disponibilidad': {},
                'tendencias': {},
                'competencia': {},
                'eventos': {}
            }
            
            # Analizar precios y disponibilidad
            if hasattr(mercado_actual, 'bienes'):
                for bien_nombre in mercado_actual.bienes.keys():
                    empresas_disponibles = [e for e in mercado_actual.getEmpresas()
                                          if bien_nombre in e.bienes and len(e.bienes[bien_nombre]) > 0]
                    
                    if empresas_disponibles:
                        precios = [e.precios.get(bien_nombre, 0) for e in empresas_disponibles]
                        precio_promedio = sum(precios) / len(precios)
                        precio_minimo = min(precios)
                        
                        estado_mercado['precios'][bien_nombre] = {
                            'promedio': precio_promedio,
                            'minimo': precio_minimo,
                            'variabilidad': max(precios) - min(precios) if len(precios) > 1 else 0
                        }
                        
                        estado_mercado['disponibilidad'][bien_nombre] = len(empresas_disponibles)
                        estado_mercado['competencia'][bien_nombre] = len(empresas_disponibles)
            
            # Detectar tendencias de precios
            self._detectar_tendencias_precios(estado_mercado['precios'])
            
            # Actualizar conocimiento sobre crisis económicas
            if hasattr(mercado_actual, 'en_crisis'):
                if mercado_actual.en_crisis:
                    self.perfil_personalidad_completo.actualizar_estado_emocional("crisis_economica", 0.1)
                else:
                    self.perfil_personalidad_completo.actualizar_estado_emocional("recuperacion_economica", 0.05)
            
            # Actualizar predicciones de demanda basándose en conocimiento del mercado
            self._actualizar_predicciones_demanda(estado_mercado)
            
        except Exception as e:
            print(f"[{self.nombre}] Error actualizando conocimiento de mercado: {e}")
    
    def _detectar_tendencias_precios(self, precios_actuales: Dict[str, Dict[str, float]]):
        """Detecta tendencias en precios y actualiza estrategias"""
        
        for bien, info_precio in precios_actuales.items():
            precio_actual = info_precio['promedio']
            
            # Comparar con precio ancla si existe
            if bien in self.precios_ancla:
                cambio_porcentual = (precio_actual - self.precios_ancla[bien]) / self.precios_ancla[bien]
                
                # Si el precio ha subido significativamente, aumentar urgencia
                if cambio_porcentual > 0.15:  # 15% de aumento
                    if bien in self.predicciones_demanda:
                        self.predicciones_demanda[bien] = min(1.0, self.predicciones_demanda[bien] + 0.2)
                
                # Si el precio ha bajado, es oportunidad de compra
                elif cambio_porcentual < -0.10:  # 10% de descuento
                    if bien in self.sistema_comportamiento.productos_lista_deseos:
                        # Aumentar interés en el bien
                        self.predicciones_demanda[bien] = min(1.0, self.predicciones_demanda.get(bien, 0.5) + 0.3)
            
            # Actualizar precio ancla gradualmente
            if bien in self.precios_ancla:
                self.precios_ancla[bien] = self.precios_ancla[bien] * 0.95 + precio_actual * 0.05
            else:
                self.precios_ancla[bien] = precio_actual
    
    def _evaluar_oportunidades_compra_grupal(self):
        """Evalúa oportunidades de compra grupal de manera más sofisticada"""
        
        # Solo evaluar si tiene tendencia social
        if self.perfil_personalidad_completo.rasgos_psicologicos.conformidad_social < 0.4:
            return
        
        # Buscar bienes con alta demanda predicha
        bienes_interes = [bien for bien, demanda in self.predicciones_demanda.items() if demanda > 0.6]
        
        if bienes_interes and len(self.red_social) >= 2:
            # Seleccionar bien con mayor potencial de ahorro
            bien_elegido = random.choice(bienes_interes)
            cantidad_objetivo = random.uniform(3.0, 10.0)  # Cantidad para grupo
            
            alianza_id = self.formar_grupos_compra(bien_elegido, cantidad_objetivo)
            if alianza_id:
                print(f"[{self.nombre}] Formó grupo de compra para {bien_elegido} (ID: {alianza_id})")
    
    def _actualizar_red_social_dinamica(self, mercado_actual):
        """Actualiza la red social de manera dinámica"""
        
        # Buscar otros consumidores IA en el mercado
        if hasattr(mercado_actual, 'consumidores'):
            otros_consumidores = [c for c in mercado_actual.consumidores 
                                if hasattr(c, 'perfil_personalidad_completo') and c.nombre != self.nombre]
            
            # Conectar con consumidores compatibles
            for otro in otros_consumidores[:3]:  # Limitar a 3 por ciclo
                if otro.nombre not in self.red_social:
                    # Calcular compatibilidad social
                    compatibilidad = self._calcular_compatibilidad_social(otro)
                    
                    if compatibilidad > 0.6 and random.random() < 0.1:  # 10% probabilidad si hay compatibilidad
                        self.red_social.append(otro.nombre)
                        print(f"[{self.nombre}] Se conectó socialmente con {otro.nombre}")
        
        # Mantener red social limitada
        if len(self.red_social) > 15:
            # Remover conexiones más débiles (simplificado: aleatorio)
            self.red_social = self.red_social[-15:]
    
    def _calcular_compatibilidad_social(self, otro_consumidor) -> float:
        """Calcula compatibilidad social con otro consumidor"""
        
        if not hasattr(otro_consumidor, 'perfil_personalidad_completo'):
            return 0.0
        
        mi_perfil = self.perfil_personalidad_completo
        otro_perfil = otro_consumidor.perfil_personalidad_completo
        
        # Similitud en tipo de personalidad
        compatibilidad = 0.0
        if mi_perfil.tipo_personalidad == otro_perfil.tipo_personalidad:
            compatibilidad += 0.3
        
        # Similitud en estilo de vida
        if mi_perfil.estilo_vida == otro_perfil.estilo_vida:
            compatibilidad += 0.2
        
        # Similitud en rasgos psicológicos (extraversión más importante para conexiones)
        diff_extraversion = abs(mi_perfil.rasgos_psicologicos.extraversion - 
                               otro_perfil.rasgos_psicologicos.extraversion)
        compatibilidad += (1.0 - diff_extraversion) * 0.3
        
        # Similitud en preferencias de consumo
        mi_prefs = mi_perfil.preferencias_consumo
        otro_prefs = otro_perfil.preferencias_consumo
        
        # Comparar algunas preferencias clave
        prefs_clave = ['preferencia_tecnologia', 'preferencia_alimentacion', 'preferencia_entretenimiento']
        similitud_prefs = 0.0
        
        for pref in prefs_clave:
            if hasattr(mi_prefs, pref) and hasattr(otro_prefs, pref):
                mi_val = getattr(mi_prefs, pref)
                otro_val = getattr(otro_prefs, pref)
                similitud_prefs += (1.0 - abs(mi_val - otro_val)) / len(prefs_clave)
        
        compatibilidad += similitud_prefs * 0.2
        
        return max(0.0, min(1.0, compatibilidad))
    
    def _decisiones_proactivas_avanzadas(self, mercado_actual):
        """Toma decisiones proactivas más sofisticadas"""
        
        # Decisión de cambio de estrategia basándose en rendimiento
        if len(self.sistema_comportamiento.experiencias_compra) >= 10:
            experiencias_recientes = self.sistema_comportamiento.experiencias_compra[-10:]
            satisfaccion_promedio = sum(exp.satisfaccion for exp in experiencias_recientes) / len(experiencias_recientes)
            
            # Si la satisfacción es baja, considerar cambiar estrategia
            if satisfaccion_promedio < 0.4:
                self._ajustar_estrategia_compra()
        
        # Decisión de presupuesto dinámico
        self._ajustar_presupuesto_dinamico()
        
        # Decisión de inversión en educación financiera
        if random.random() < 0.01:  # 1% probabilidad por ciclo
            self._considerar_educacion_financiera()
    
    def _ajustar_estrategia_compra(self):
        """Ajusta la estrategia de compra basándose en experiencias pasadas"""
        
        # Analizar patrones de fallas
        experiencias_malas = [exp for exp in self.sistema_comportamiento.experiencias_compra 
                             if exp.satisfaccion < 0.4]
        
        if experiencias_malas:
            # Identificar problema común
            precios_altos = [exp for exp in experiencias_malas if exp.precio_pagado > exp.precio_pagado * 0.8]
            calidad_baja = [exp for exp in experiencias_malas if exp.calidad_percibida < 0.5]
            
            if len(precios_altos) > len(calidad_baja):
                # Problema de precios - aumentar importancia del precio
                self.perfil_personalidad_completo.rasgos_psicologicos.importancia_precio = min(1.0,
                    self.perfil_personalidad_completo.rasgos_psicologicos.importancia_precio + 0.1)
            else:
                # Problema de calidad - aumentar importancia de la calidad
                self.perfil_personalidad_completo.rasgos_psicologicos.importancia_calidad = min(1.0,
                    self.perfil_personalidad_completo.rasgos_psicologicos.importancia_calidad + 0.1)
        
        # Regenerar criterios de decisión con nuevos valores
        self.sistema_comportamiento.criterios_decision = self.sistema_comportamiento._generar_criterios_decision()
    
    def _ajustar_presupuesto_dinamico(self):
        """Ajusta el presupuesto de consumo dinámicamente"""
        
        # Basándose en estado financiero y experiencias
        if self.dinero > self.ingreso_mensual * 3:  # Tiene buenos ahorros
            if self.perfil_personalidad_completo.satisfaccion_vida > 0.7:
                # Puede permitirse gastar un poco más
                self.propension_consumo = min(0.85, self.propension_consumo + 0.02)
        
        elif self.dinero < self.ingreso_mensual * 0.5:  # Situación ajustada
            # Necesita ahorrar más
            self.propension_consumo = max(0.3, self.propension_consumo - 0.05)
        
        # Ajustar propensión al ahorro
        self.propension_ahorro = 1.0 - self.propension_consumo
    
    def _considerar_educacion_financiera(self):
        """Considera invertir en educación financiera"""
        
        # Solo si tiene recursos y personalidad adecuada
        if (self.dinero > self.ingreso_mensual * 2 and 
            self.perfil_personalidad_completo.rasgos_psicologicos.apertura > 0.6):
            
            # Pequeña mejora en conocimiento financiero
            contexto = self.perfil_personalidad_completo.contexto_socioeconomico
            contexto.conocimiento_financiero = min(1.0, contexto.conocimiento_financiero + 0.05)
            contexto.experiencia_inversiones = min(1.0, contexto.experiencia_inversiones + 0.03)
            
            # Costo de la educación
            costo_educacion = self.ingreso_mensual * 0.1
            if self.dinero >= costo_educacion:
                self.dinero -= costo_educacion
                print(f"[{self.nombre}] Invirtió en educación financiera")
    
    def _actualizar_estado_psicologico(self):
        """Actualiza el estado psicológico de manera más sofisticada"""
        
        # Recuperación gradual basándose en personalidad
        factor_recuperacion = self.perfil_personalidad_completo.rasgos_psicologicos.neuroticismo
        
        # Estrés financiero
        if self.dinero > self.ingreso_mensual * 2:
            self.perfil_personalidad_completo.stress_financiero = max(0.0, 
                self.perfil_personalidad_completo.stress_financiero - 0.02 * (1.0 - factor_recuperacion))
        elif self.dinero < self.ingreso_mensual * 0.5:
            self.perfil_personalidad_completo.stress_financiero = min(1.0,
                self.perfil_personalidad_completo.stress_financiero + 0.05 * (1.0 + factor_recuperacion))
        
        # Satisfacción de vida
        if len(self.sistema_comportamiento.experiencias_compra) >= 5:
            satisfaccion_compras = sum(exp.satisfaccion for exp in self.sistema_comportamiento.experiencias_compra[-5:]) / 5
            ajuste_satisfaccion = (satisfaccion_compras - 0.5) * 0.01
            self.perfil_personalidad_completo.satisfaccion_vida = max(0.0, min(1.0,
                self.perfil_personalidad_completo.satisfaccion_vida + ajuste_satisfaccion))
        
        # Confianza en la economía
        if hasattr(self.mercado, 'en_crisis') and not self.mercado.en_crisis:
            self.perfil_personalidad_completo.confianza_economia = min(1.0,
                self.perfil_personalidad_completo.confianza_economia + 0.01)
        
        # Sincronizar con variables heredadas
        self.estado_emocional = self.perfil_personalidad_completo.satisfaccion_vida
        self.confianza_mercado = self.perfil_personalidad_completo.confianza_economia
        self.stress_financiero = self.perfil_personalidad_completo.stress_financiero
    
    def get_estadisticas_ia_completas(self) -> Dict[str, Any]:
        """Obtiene estadísticas completas del consumidor IA hiperrealista"""
        
        stats_base = {
            'agente_id': f"consumidor_{self.nombre}",
            'dinero_actual': self.dinero,
            'ingreso_mensual': self.ingreso_mensual,
            'empleado': self.empleado,
        }
        
        # Estadísticas de personalidad
        stats_personalidad = {
            'tipo_personalidad': self.perfil_personalidad_completo.tipo_personalidad.value,
            'estilo_vida': self.perfil_personalidad_completo.estilo_vida.value,
            'nivel_educativo': self.perfil_personalidad_completo.contexto_socioeconomico.nivel_educativo.value,
            'ocupacion': self.perfil_personalidad_completo.contexto_socioeconomico.ocupacion,
            'descripcion_personalidad': self.perfil_personalidad_completo.get_descripcion_personalidad(),
        }
        
        # Estadísticas de rasgos psicológicos
        rasgos = self.perfil_personalidad_completo.rasgos_psicologicos
        stats_rasgos = {
            'apertura': rasgos.apertura,
            'responsabilidad': rasgos.responsabilidad,
            'extraversion': rasgos.extraversion,
            'amabilidad': rasgos.amabilidad,
            'neuroticismo': rasgos.neuroticismo,
            'aversion_riesgo': rasgos.aversion_riesgo,
            'materialismo': rasgos.materialismo,
            'impulsividad': rasgos.impulsividad,
            'planificacion': rasgos.planificacion,
            'conformidad_social': rasgos.conformidad_social,
            'importancia_precio': rasgos.importancia_precio,
            'importancia_calidad': rasgos.importancia_calidad,
            'importancia_marca': rasgos.importancia_marca,
            'importancia_sostenibilidad': rasgos.importancia_sostenibilidad,
        }
        
        # Estadísticas de comportamiento de compra
        stats_comportamiento = self.sistema_comportamiento.get_estadisticas_comportamiento()
        
        # Estadísticas de preferencias
        prefs = self.perfil_personalidad_completo.preferencias_consumo
        stats_preferencias = {
            'preferencia_alimentacion': prefs.preferencia_alimentacion,
            'preferencia_tecnologia': prefs.preferencia_tecnologia,
            'preferencia_ropa': prefs.preferencia_ropa,
            'preferencia_entretenimiento': prefs.preferencia_entretenimiento,
            'preferencia_educacion': prefs.preferencia_educacion,
            'preferencia_salud': prefs.preferencia_salud,
            'preferencia_viajes': prefs.preferencia_viajes,
            'preferencia_hogar': prefs.preferencia_hogar,
            'preferencia_compras_online': prefs.preferencia_compras_online,
            'umbral_precio_alto': prefs.umbral_precio_alto,
            'umbral_descuento_atractivo': prefs.umbral_descuento_atractivo,
        }
        
        # Estadísticas de estado psicológico
        stats_psicologico = {
            'satisfaccion_vida': self.perfil_personalidad_completo.satisfaccion_vida,
            'confianza_economia': self.perfil_personalidad_completo.confianza_economia,
            'stress_financiero': self.perfil_personalidad_completo.stress_financiero,
            'experiencia_mercado': self.perfil_personalidad_completo.experiencia_mercado,
        }
        
        # Estadísticas de aprendizaje IA
        stats_ia = {
            'patrones_aprendidos': len(self.patrones_consumo),
            'compras_optimizadas': self.compras_optimizadas,
            'negociaciones_exitosas': self.negociaciones_exitosas,
            'ahorro_total_ia': self.ahorro_obtenido_ia,
            'utilidad_total_ia': self.utilidad_total_ia,
            'predicciones_activas': len(self.predicciones_demanda),
            'vendedores_conocidos': len(self.reputacion_vendedores),
            'memoria_decisiones': self.memoria.experiencia_total,
            'tasa_exito_ia': self.memoria.tasa_exito,
        }
        
        # Estadísticas sociales
        stats_sociales = {
            'red_social_tamaño': len(self.red_social),
            'grupos_compra_activos': len(self.grupos_compra),
            'influencers_seguidos': len(self.influencers_seguidos),
            'redes_sociales_activo': self.perfil_personalidad_completo.contexto_socioeconomico.redes_sociales_activo,
            'usa_comparadores_precios': self.perfil_personalidad_completo.contexto_socioeconomico.usa_comparadores_precios,
        }
        
        # Estadísticas financieras avanzadas
        contexto_financiero = self.perfil_personalidad_completo.contexto_socioeconomico
        stats_financieras = {
            'historial_crediticio': contexto_financiero.historial_crediticio,
            'experiencia_inversiones': contexto_financiero.experiencia_inversiones,
            'conocimiento_financiero': contexto_financiero.conocimiento_financiero,
            'propension_consumo': self.propension_consumo,
            'propension_ahorro': self.propension_ahorro,
            'deuda_actual': getattr(self, 'deuda', 0),
            'ahorros_actuales': getattr(self, 'ahorros', 0),
        }
        
        # Estadísticas de experiencias de compra
        if self.sistema_comportamiento.experiencias_compra:
            experiencias = self.sistema_comportamiento.experiencias_compra
            stats_experiencias = {
                'total_experiencias': len(experiencias),
                'satisfaccion_promedio': sum(exp.satisfaccion for exp in experiencias) / len(experiencias),
                'precio_promedio_pagado': sum(exp.precio_pagado for exp in experiencias) / len(experiencias),
                'tiempo_decision_promedio': sum(exp.tiempo_decision for exp in experiencias) / len(experiencias),
                'tasa_recomendacion': sum(1 for exp in experiencias if exp.recomendaria) / len(experiencias),
                'bienes_unicos_comprados': len(set(exp.bien for exp in experiencias)),
            }
            
            # Análisis de negociaciones
            negociaciones = [exp for exp in experiencias if exp.resultado_negociacion is not None]
            if negociaciones:
                stats_experiencias.update({
                    'negociaciones_intentadas': len(negociaciones),
                    'negociaciones_exitosas': len([exp for exp in negociaciones if exp.resultado_negociacion > 0]),
                    'ahorro_promedio_negociacion': sum(exp.resultado_negociacion for exp in negociaciones) / len(negociaciones),
                })
        else:
            stats_experiencias = {
                'total_experiencias': 0,
                'satisfaccion_promedio': 0.5,
                'precio_promedio_pagado': 0,
                'tiempo_decision_promedio': self.sistema_comportamiento.tiempo_promedio_decision,
                'tasa_recomendacion': 0.5,
                'bienes_unicos_comprados': 0,
                'negociaciones_intentadas': 0,
                'negociaciones_exitosas': 0,
                'ahorro_promedio_negociacion': 0,
            }
        
        # Estadísticas de patrones de consumo aprendidos
        stats_patrones = {}
        if self.patrones_consumo:
            for bien, patron in self.patrones_consumo.items():
                stats_patrones[f'patron_{bien}'] = {
                    'frecuencia_promedio': patron.frecuencia_promedio,
                    'cantidad_promedio': patron.cantidad_promedio,
                    'precio_maximo_aceptable': patron.precio_maximo_aceptable,
                    'utilidad_esperada': patron.utilidad_esperada,
                    'confianza': patron.confianza,
                }
        
        # Combinar todas las estadísticas
        stats_completas = {
            **stats_base,
            'personalidad': stats_personalidad,
            'rasgos_psicologicos': stats_rasgos,
            'comportamiento_compra': stats_comportamiento,
            'preferencias': stats_preferencias,
            'estado_psicologico': stats_psicologico,
            'sistemas_ia': stats_ia,
            'redes_sociales': stats_sociales,
            'finanzas_avanzadas': stats_financieras,
            'experiencias_compra': stats_experiencias,
            'patrones_consumo': stats_patrones,
        }
        
        return stats_completas
    
    def generar_reporte_personalidad(self) -> str:
        """Genera un reporte detallado de la personalidad del consumidor"""
        
        perfil = self.perfil_personalidad_completo
        reporte = []
        
        reporte.append(f"=== REPORTE DE PERSONALIDAD: {self.nombre} ===")
        reporte.append("")
        
        # Información básica
        reporte.append("📊 INFORMACIÓN BÁSICA:")
        reporte.append(f"  • Tipo de Personalidad: {perfil.tipo_personalidad.value.title()}")
        reporte.append(f"  • Estilo de Vida: {perfil.estilo_vida.value.replace('_', ' ').title()}")
        reporte.append(f"  • Nivel Educativo: {perfil.contexto_socioeconomico.nivel_educativo.value.title()}")
        reporte.append(f"  • Ocupación: {perfil.contexto_socioeconomico.ocupacion.title()}")
        reporte.append("")
        
        # Rasgos psicológicos principales
        rasgos = perfil.rasgos_psicologicos
        reporte.append("🧠 RASGOS PSICOLÓGICOS:")
        reporte.append(f"  • Apertura a experiencias: {rasgos.apertura:.2f} ({'Alta' if rasgos.apertura > 0.7 else 'Media' if rasgos.apertura > 0.3 else 'Baja'})")
        reporte.append(f"  • Responsabilidad: {rasgos.responsabilidad:.2f} ({'Alta' if rasgos.responsabilidad > 0.7 else 'Media' if rasgos.responsabilidad > 0.3 else 'Baja'})")
        reporte.append(f"  • Extroversión: {rasgos.extraversion:.2f} ({'Alta' if rasgos.extraversion > 0.7 else 'Media' if rasgos.extraversion > 0.3 else 'Baja'})")
        reporte.append(f"  • Aversión al riesgo: {rasgos.aversion_riesgo:.2f} ({'Alta' if rasgos.aversion_riesgo > 0.7 else 'Media' if rasgos.aversion_riesgo > 0.3 else 'Baja'})")
        reporte.append(f"  • Impulsividad: {rasgos.impulsividad:.2f} ({'Alta' if rasgos.impulsividad > 0.7 else 'Media' if rasgos.impulsividad > 0.3 else 'Baja'})")
        reporte.append("")
        
        # Comportamiento de compra
        comportamiento = self.sistema_comportamiento
        reporte.append("🛒 COMPORTAMIENTO DE COMPRA:")
        reporte.append(f"  • Estilo dominante: {comportamiento.comportamiento_dominante.value.title()}")
        reporte.append(f"  • Tiempo promedio de decisión: {comportamiento.tiempo_promedio_decision:.1f} minutos")
        reporte.append(f"  • Tendencia a negociar: {comportamiento.tendencia_negociacion:.2f}")
        reporte.append(f"  • Factor de lealtad: {comportamiento.factor_lealtad:.2f}")
        reporte.append("")
        
        # Preferencias principales
        prefs = perfil.preferencias_consumo
        reporte.append("❤️ PREFERENCIAS PRINCIPALES:")
        preferencias_ordenadas = [
            ('Alimentación', prefs.preferencia_alimentacion),
            ('Tecnología', prefs.preferencia_tecnologia),
            ('Ropa y moda', prefs.preferencia_ropa),
            ('Entretenimiento', prefs.preferencia_entretenimiento),
            ('Educación', prefs.preferencia_educacion),
            ('Salud', prefs.preferencia_salud),
            ('Viajes', prefs.preferencia_viajes),
            ('Hogar', prefs.preferencia_hogar),
        ]
        preferencias_ordenadas.sort(key=lambda x: x[1], reverse=True)
        
        for i, (categoria, valor) in enumerate(preferencias_ordenadas[:3]):
            reporte.append(f"  {i+1}. {categoria}: {valor:.2f}")
        reporte.append("")
        
        # Estado actual
        reporte.append("📈 ESTADO ACTUAL:")
        reporte.append(f"  • Satisfacción de vida: {perfil.satisfaccion_vida:.2f}")
        reporte.append(f"  • Confianza en economía: {perfil.confianza_economia:.2f}")
        reporte.append(f"  • Estrés financiero: {perfil.stress_financiero:.2f}")
        reporte.append(f"  • Experiencia de mercado: {perfil.experiencia_mercado:.2f}")
        reporte.append("")
        
        # Estadísticas de rendimiento
        stats = self.get_estadisticas_ia_completas()
        reporte.append("🎯 RENDIMIENTO IA:")
        reporte.append(f"  • Compras optimizadas: {stats['sistemas_ia']['compras_optimizadas']}")
        reporte.append(f"  • Ahorro obtenido: ${stats['sistemas_ia']['ahorro_total_ia']:.2f}")
        reporte.append(f"  • Negociaciones exitosas: {stats['sistemas_ia']['negociaciones_exitosas']}")
        reporte.append(f"  • Patrones aprendidos: {stats['sistemas_ia']['patrones_aprendidos']}")
        
        if stats['experiencias_compra']['total_experiencias'] > 0:
            reporte.append(f"  • Satisfacción promedio: {stats['experiencias_compra']['satisfaccion_promedio']:.2f}")
        
        reporte.append("")
        reporte.append("=" * 50)
        
    def validar_perfil_hiperrealista(self) -> Dict[str, bool]:
        """Valida que el perfil hiperrealista esté correctamente configurado"""
        
        validaciones = {}
        
        # Validar personalidad
        try:
            validaciones['personalidad_generada'] = self.perfil_personalidad_completo is not None
            validaciones['tipo_personalidad_valido'] = hasattr(self.perfil_personalidad_completo, 'tipo_personalidad')
            validaciones['rasgos_psicologicos_validos'] = all([
                0 <= self.perfil_personalidad_completo.rasgos_psicologicos.apertura <= 1,
                0 <= self.perfil_personalidad_completo.rasgos_psicologicos.responsabilidad <= 1,
                0 <= self.perfil_personalidad_completo.rasgos_psicologicos.extraversion <= 1,
            ])
        except Exception as e:
            self.logger.error(f"Error validando personalidad: {e}")
            validaciones['personalidad_generada'] = False
            validaciones['tipo_personalidad_valido'] = False
            validaciones['rasgos_psicologicos_validos'] = False
        
        # Validar comportamiento de compra
        try:
            validaciones['comportamiento_configurado'] = self.sistema_comportamiento is not None
            validaciones['criterios_decision_validos'] = len(self.sistema_comportamiento.criterios_decision) > 0
            validaciones['sesgos_cognitivos_validos'] = len(self.sistema_comportamiento.sesgos_cognitivos) > 0
        except Exception as e:
            self.logger.error(f"Error validando comportamiento: {e}")
            validaciones['comportamiento_configurado'] = False
            validaciones['criterios_decision_validos'] = False
            validaciones['sesgos_cognitivos_validos'] = False
        
        # Validar integración con sistemas existentes
        try:
            validaciones['ia_engine_configurado'] = self.ia_engine is not None
            validaciones['memoria_configurada'] = self.memoria is not None
            validaciones['comunicacion_configurada'] = self.comunicacion is not None
        except Exception as e:
            self.logger.error(f"Error validando sistemas IA: {e}")
            validaciones['ia_engine_configurado'] = False
            validaciones['memoria_configurada'] = False
            validaciones['comunicacion_configurada'] = False
        
        # Validar métodos de decisión
        try:
            validaciones['metodo_decision_hiperrealista'] = hasattr(self, 'tomar_decision_compra_hiperrealista')
            validaciones['metodo_exploracion_mercado'] = hasattr(self, 'explorar_mercado_avanzado')
            validaciones['metodo_aprendizaje_social'] = hasattr(self, 'aprender_de_red_social')
        except Exception as e:
            self.logger.error(f"Error validando métodos: {e}")
            validaciones['metodo_decision_hiperrealista'] = False
            validaciones['metodo_exploracion_mercado'] = False
            validaciones['metodo_aprendizaje_social'] = False
        
        # Resumen de validación
        total_validaciones = len(validaciones)
        validaciones_exitosas = sum(validaciones.values())
        
        validaciones['validacion_exitosa'] = validaciones_exitosas == total_validaciones
        validaciones['porcentaje_exito'] = (validaciones_exitosas / total_validaciones) * 100
        
        if not validaciones['validacion_exitosa']:
            self.logger.warning(f"Perfil hiperrealista parcialmente configurado: {validaciones_exitosas}/{total_validaciones} validaciones exitosas")
        else:
            self.logger.info("Perfil hiperrealista completamente configurado y validado")
        
        return validaciones

        return "\n".join(reporte)
    
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
