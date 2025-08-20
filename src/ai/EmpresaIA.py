"""
Empresa IA Hiperrealista
========================

Implementa una empresa con inteligencia artificial que desarrolla estrategias
competitivas, optimiza operaciones, innova productos y gestiona recursos.
"""

import numpy as np
import random
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from collections import defaultdict

from ..models.Empresa import Empresa
from .AgentMemorySystem import AgentMemorySystem, Decision
from .IADecisionEngine import IADecisionEngine, EstadoMercado, OpcionDecision
from .AgentCommunicationProtocol import AgentCommunicationProtocol, TipoMensaje, PrioridadMensaje


@dataclass
class EstrategiaCompetitiva:
    """Estrategia competitiva de la empresa"""
    nombre: str
    tipo: str  # 'diferenciacion', 'liderazgo_costos', 'nicho', 'innovacion'
    parametros: Dict[str, float]
    efectividad: float
    riesgo: float
    recursos_requeridos: float
    tiempo_implementacion: int  # días


@dataclass
class ProductoIA:
    """Producto con características de IA"""
    nombre: str
    categoria: str
    costo_produccion: float
    precio_sugerido: float
    calidad: float
    innovacion_level: float
    demanda_predicha: float
    ciclo_vida: str  # 'introduccion', 'crecimiento', 'madurez', 'declive'
    competitividad: float


@dataclass
class CompetidorAnalisis:
    """Análisis de competidor"""
    empresa_id: str
    fortalezas: List[str]
    debilidades: List[str]
    estrategia_percibida: str
    nivel_amenaza: float
    oportunidades_colaboracion: float
    precios_observados: Dict[str, float]
    market_share_estimado: float


class EmpresaIA(Empresa):
    """
    Empresa con Inteligencia Artificial Estratégica
    """
    
    def __init__(self, nombre, mercado, bienes={}):
        super().__init__(nombre, mercado, bienes)
        
        # Componentes IA
        self.ia_engine = IADecisionEngine(f"empresa_{nombre}")
        self.memoria = AgentMemorySystem(f"empresa_{nombre}")
        self.comunicacion = AgentCommunicationProtocol(f"empresa_{nombre}")
        
        # Estrategia empresarial IA
        self.estrategia_actual: Optional[EstrategiaCompetitiva] = None
        self.cartera_estrategias: List[EstrategiaCompetitiva] = []
        
        # Análisis de competencia
        self.competidores_analizados: Dict[str, CompetidorAnalisis] = {}
        self.market_share: Dict[str, float] = {}
        self.posicion_competitiva: Dict[str, str] = {}  # 'lider', 'retador', 'seguidor', 'nicho'
        
        # Gestión de productos IA
        self.productos_ia: Dict[str, ProductoIA] = {}
        self.pipeline_innovacion: List[Dict[str, Any]] = []
        self.inversiones_id: Dict[str, float] = {}
        
        # Gestión de recursos humanos IA
        self.perfiles_empleados: Dict[str, Dict[str, float]] = {}
        self.necesidades_contratacion: Dict[str, int] = {}
        self.productividad_promedio: float = 1.0
        
        # Gestión financiera IA
        self.flujo_caja_predicho: List[float] = []
        self.inversiones_planificadas: Dict[str, float] = {}
        self.riesgo_financiero: float = 0.3
        
        # Cadena de suministro IA
        self.proveedores_evaluados: Dict[str, float] = {}
        self.inventario_optimo: Dict[str, float] = {}
        self.costos_logisticos: Dict[str, float] = {}
        
        # Métricas de rendimiento IA
        self.roi_estrategias: Dict[str, float] = {}
        self.eficiencia_operacional: float = 0.7
        self.satisfaccion_clientes: float = 0.6
        self.innovaciones_exitosas: int = 0
        
        # Alianzas estratégicas
        self.alianzas_activas: List[str] = []
        self.partnerships_tecnologicos: List[str] = []
        
        # Inicializar IA empresarial
        self._inicializar_sistema_empresarial_ia()
    
    def _inicializar_sistema_empresarial_ia(self):
        """Inicializa todos los sistemas IA de la empresa"""
        # Generar estrategia inicial
        self._generar_estrategias_base()
        self._seleccionar_estrategia_inicial()
        
        # Inicializar análisis de productos
        self._inicializar_productos_ia()
        
        # Configurar objetivos iniciales
        self._establecer_objetivos_ia()
    
    def _generar_estrategias_base(self):
        """Genera estrategias competitivas base"""
        estrategias_base = [
            EstrategiaCompetitiva(
                nombre="Liderazgo en Costos",
                tipo="liderazgo_costos",
                parametros={
                    'reduccion_costos': 0.15,
                    'eficiencia_operativa': 0.2,
                    'margen_objetivo': 0.1
                },
                efectividad=0.7,
                riesgo=0.4,
                recursos_requeridos=0.6,
                tiempo_implementacion=30
            ),
            EstrategiaCompetitiva(
                nombre="Diferenciación Premium",
                tipo="diferenciacion",
                parametros={
                    'calidad_premium': 0.3,
                    'innovacion_producto': 0.25,
                    'servicio_cliente': 0.2
                },
                efectividad=0.8,
                riesgo=0.6,
                recursos_requeridos=0.8,
                tiempo_implementacion=45
            ),
            EstrategiaCompetitiva(
                nombre="Innovación Disruptiva",
                tipo="innovacion",
                parametros={
                    'inversion_id': 0.15,
                    'velocidad_lanzamiento': 0.3,
                    'riesgo_tecnologico': 0.7
                },
                efectividad=0.9,
                riesgo=0.8,
                recursos_requeridos=0.9,
                tiempo_implementacion=60
            ),
            EstrategiaCompetitiva(
                nombre="Nicho Especializado",
                tipo="nicho",
                parametros={
                    'especializacion': 0.8,
                    'lealtad_cliente': 0.6,
                    'barreras_entrada': 0.5
                },
                efectividad=0.6,
                riesgo=0.3,
                recursos_requeridos=0.4,
                tiempo_implementacion=20
            )
        ]
        
        self.cartera_estrategias = estrategias_base
    
    def _seleccionar_estrategia_inicial(self):
        """Selecciona la estrategia inicial basándose en recursos y mercado"""
        # Evaluar capacidades actuales
        recursos_disponibles = self.dinero / 100000  # Normalizar
        capacidad_innovacion = random.uniform(0.3, 0.8)
        
        mejor_estrategia = None
        mejor_score = 0
        
        for estrategia in self.cartera_estrategias:
            # Calcular score de viabilidad
            score = estrategia.efectividad
            
            # Penalizar si no tenemos recursos suficientes
            if recursos_disponibles < estrategia.recursos_requeridos:
                score *= 0.5
            
            # Ajustar por tolerancia al riesgo
            tolerancia_riesgo = 0.6  # Empresa promedio
            if estrategia.riesgo > tolerancia_riesgo:
                score *= 0.8
            
            if score > mejor_score:
                mejor_score = score
                mejor_estrategia = estrategia
        
        self.estrategia_actual = mejor_estrategia
        print(f"[{self.nombre}] Estrategia inicial: {mejor_estrategia.nombre}")
    
    def _inicializar_productos_ia(self):
        """Inicializa análisis IA de productos"""
        # Determinar la lista de bienes según el tipo de estructura
        if hasattr(self.mercado, 'bienes'):
            if isinstance(self.mercado.bienes, dict):
                bienes_nombres = self.mercado.bienes.keys()
            elif isinstance(self.mercado.bienes, list):
                bienes_nombres = self.mercado.bienes
            else:
                bienes_nombres = self.bienes.keys() if hasattr(self, 'bienes') and isinstance(self.bienes, dict) else []
        else:
            bienes_nombres = self.bienes.keys() if hasattr(self, 'bienes') and isinstance(self.bienes, dict) else []
        
        for bien in bienes_nombres:
            producto_ia = ProductoIA(
                nombre=bien,
                categoria="general",
                costo_produccion=self.costos_unitarios.get(bien, 20),
                precio_sugerido=self.precios.get(bien, 30),
                calidad=random.uniform(0.5, 0.9),
                innovacion_level=random.uniform(0.1, 0.6),
                demanda_predicha=random.uniform(0.3, 0.8),
                ciclo_vida="introduccion",
                competitividad=random.uniform(0.4, 0.7)
            )
            
            self.productos_ia[bien] = producto_ia
    
    def _establecer_objetivos_ia(self):
        """Establece objetivos estratégicos de IA"""
        # Objetivos base según estrategia actual
        if self.estrategia_actual:
            if self.estrategia_actual.tipo == "liderazgo_costos":
                self.inversiones_planificadas["eficiencia_operativa"] = self.dinero * 0.1
            elif self.estrategia_actual.tipo == "diferenciacion":
                self.inversiones_planificadas["calidad_producto"] = self.dinero * 0.15
            elif self.estrategia_actual.tipo == "innovacion":
                self.inversiones_planificadas["investigacion_desarrollo"] = self.dinero * 0.2
    
    def desarrollar_estrategia_competitiva(self) -> Dict[str, Any]:
        """Desarrolla y actualiza estrategia competitiva"""
        # Analizar competencia actual
        analisis_competencia = self._analizar_competidores()
        
        # Evaluar efectividad de estrategia actual
        efectividad_actual = self._evaluar_estrategia_actual()
        
        # Determinar si cambiar estrategia
        if efectividad_actual < 0.4 or random.random() < 0.05:  # 5% probabilidad de cambio
            nueva_estrategia = self._desarrollar_nueva_estrategia(analisis_competencia)
            if nueva_estrategia:
                self._implementar_cambio_estrategia(nueva_estrategia)
        
        # Ajustar táctica actual
        ajustes_tacticos = self._ajustar_tacticas_estrategia()
        
        return {
            'estrategia_actual': self.estrategia_actual.nombre if self.estrategia_actual else None,
            'efectividad': efectividad_actual,
            'competidores_analizados': len(self.competidores_analizados),
            'ajustes_tacticos': ajustes_tacticos,
            'market_share_promedio': np.mean(list(self.market_share.values())) if self.market_share else 0
        }
    
    def _analizar_competidores(self) -> Dict[str, Any]:
        """Analiza competidores en el mercado"""
        if not self.mercado or not hasattr(self.mercado, 'personas'):
            return {}
        
        # Identificar empresas competidoras
        competidores = [
            persona for persona in self.mercado.personas
            if isinstance(persona, Empresa) and persona.nombre != self.nombre
        ]
        
        analisis_total = {}
        
        for competidor in competidores:
            if hasattr(competidor, 'nombre'):
                analisis = self._analizar_competidor_especifico(competidor)
                self.competidores_analizados[competidor.nombre] = analisis
                analisis_total[competidor.nombre] = analisis
        
        return analisis_total
    
    def _analizar_competidor_especifico(self, competidor) -> CompetidorAnalisis:
        """Analiza un competidor específico"""
        # Observar precios del competidor
        precios_observados = {}
        for bien in self.productos_ia.keys():
            if hasattr(competidor, 'precios') and bien in competidor.precios:
                precios_observados[bien] = competidor.precios[bien]
        
        # Estimar fortalezas y debilidades
        fortalezas = []
        debilidades = []
        
        if hasattr(competidor, 'dinero'):
            if competidor.dinero > self.dinero * 1.5:
                fortalezas.append("recursos_financieros")
            elif competidor.dinero < self.dinero * 0.5:
                debilidades.append("recursos_limitados")
        
        if hasattr(competidor, 'empleados'):
            if len(competidor.empleados) > len(self.empleados) * 1.2:
                fortalezas.append("recursos_humanos")
            elif len(competidor.empleados) < len(self.empleados) * 0.8:
                debilidades.append("personal_limitado")
        
        # Calcular nivel de amenaza
        nivel_amenaza = 0.5  # Base
        if precios_observados:
            precios_propios = [self.precios.get(bien, 100) for bien in precios_observados.keys()]
            precios_competidor = list(precios_observados.values())
            
            if precios_propios and precios_competidor:
                precio_promedio_propio = np.mean(precios_propios)
                precio_promedio_competidor = np.mean(precios_competidor)
                
                if precio_promedio_competidor < precio_promedio_propio * 0.9:
                    nivel_amenaza += 0.3  # Competidor más barato
        
        # Determinar estrategia percibida
        estrategia_percibida = "desconocida"
        if precios_observados:
            precios_bajos = sum(1 for p in precios_observados.values() if p < 30)
            if precios_bajos / len(precios_observados) > 0.7:
                estrategia_percibida = "liderazgo_costos"
            elif any(p > 80 for p in precios_observados.values()):
                estrategia_percibida = "diferenciacion"
        
        return CompetidorAnalisis(
            empresa_id=competidor.nombre,
            fortalezas=fortalezas,
            debilidades=debilidades,
            estrategia_percibida=estrategia_percibida,
            nivel_amenaza=min(1.0, nivel_amenaza),
            oportunidades_colaboracion=random.uniform(0.1, 0.6),
            precios_observados=precios_observados,
            market_share_estimado=random.uniform(0.05, 0.3)
        )
    
    def _evaluar_estrategia_actual(self) -> float:
        """Evalúa la efectividad de la estrategia actual"""
        if not self.estrategia_actual:
            return 0.0
        
        # Métricas de efectividad
        efectividad = 0.5  # Base
        
        # Factor 1: Rendimiento financiero
        if hasattr(self, 'dinero_inicial'):
            crecimiento = (self.dinero - self.dinero_inicial) / max(self.dinero_inicial, 1)
            efectividad += min(0.3, crecimiento)
        
        # Factor 2: Market share
        if self.market_share:
            share_promedio = np.mean(list(self.market_share.values()))
            efectividad += share_promedio * 0.2
        
        # Factor 3: Competitividad de productos
        if self.productos_ia:
            competitividad_promedio = np.mean([p.competitividad for p in self.productos_ia.values()])
            efectividad += competitividad_promedio * 0.2
        
        # Factor 4: Eficiencia operacional
        efectividad += self.eficiencia_operacional * 0.1
        
        return min(1.0, efectividad)
    
    def _desarrollar_nueva_estrategia(self, analisis_competencia: Dict[str, Any]) -> Optional[EstrategiaCompetitiva]:
        """Desarrolla una nueva estrategia basándose en análisis de competencia"""
        # Identificar gaps en el mercado
        estrategias_competidores = [
            analisis.estrategia_percibida for analisis in self.competidores_analizados.values()
        ]
        
        # Buscar estrategia menos usada por competidores
        estrategias_disponibles = [e for e in self.cartera_estrategias if e.tipo not in estrategias_competidores]
        
        if estrategias_disponibles:
            # Seleccionar la más prometedora
            mejor_estrategia = max(estrategias_disponibles, key=lambda x: x.efectividad - x.riesgo)
            return mejor_estrategia
        
        # Si no hay gaps claros, mejorar estrategia actual
        if self.estrategia_actual:
            estrategia_mejorada = self._mejorar_estrategia_actual()
            return estrategia_mejorada
        
        return None
    
    def _mejorar_estrategia_actual(self) -> EstrategiaCompetitiva:
        """Mejora la estrategia actual con pequeños ajustes"""
        estrategia_mejorada = EstrategiaCompetitiva(
            nombre=f"{self.estrategia_actual.nombre} v2.0",
            tipo=self.estrategia_actual.tipo,
            parametros=self.estrategia_actual.parametros.copy(),
            efectividad=min(1.0, self.estrategia_actual.efectividad * 1.1),
            riesgo=max(0.1, self.estrategia_actual.riesgo * 0.9),
            recursos_requeridos=self.estrategia_actual.recursos_requeridos,
            tiempo_implementacion=self.estrategia_actual.tiempo_implementacion
        )
        
        # Ajustar parámetros basándose en aprendizaje
        for param in estrategia_mejorada.parametros:
            ajuste = random.uniform(0.95, 1.05)
            estrategia_mejorada.parametros[param] *= ajuste
        
        return estrategia_mejorada
    
    def _implementar_cambio_estrategia(self, nueva_estrategia: EstrategiaCompetitiva):
        """Implementa un cambio de estrategia"""
        estrategia_anterior = self.estrategia_actual
        self.estrategia_actual = nueva_estrategia
        
        print(f"[{self.nombre}] Cambio de estrategia: {estrategia_anterior.nombre if estrategia_anterior else 'Ninguna'} → {nueva_estrategia.nombre}")
        
        # Registrar decisión estratégica
        decision = Decision(
            agente_id=f"empresa_{self.nombre}",
            tipo_decision="cambio_estrategia",
            contexto={
                'estrategia_anterior': estrategia_anterior.nombre if estrategia_anterior else None,
                'competidores_activos': len(self.competidores_analizados),
                'recursos_disponibles': self.dinero
            },
            accion_tomada={
                'nueva_estrategia': nueva_estrategia.nombre,
                'tipo_estrategia': nueva_estrategia.tipo,
                'recursos_comprometidos': nueva_estrategia.recursos_requeridos * self.dinero
            }
        )
        
        self.memoria.agregar_decision(decision)
        
        # Ajustar operaciones según nueva estrategia
        self._ajustar_operaciones_nueva_estrategia(nueva_estrategia)
    
    def _ajustar_operaciones_nueva_estrategia(self, estrategia: EstrategiaCompetitiva):
        """Ajusta operaciones según la nueva estrategia"""
        if estrategia.tipo == "liderazgo_costos":
            # Reducir costos de producción
            for bien in self.costos_unitarios:
                reduccion = estrategia.parametros.get('reduccion_costos', 0.1)
                self.costos_unitarios[bien] *= (1 - reduccion)
            
            # Ajustar precios para ser competitivos
            for bien in self.precios:
                self.precios[bien] *= 0.95
        
        elif estrategia.tipo == "diferenciacion":
            # Aumentar calidad e innovación
            for producto in self.productos_ia.values():
                mejora_calidad = estrategia.parametros.get('calidad_premium', 0.2)
                producto.calidad = min(1.0, producto.calidad + mejora_calidad)
                producto.innovacion_level = min(1.0, producto.innovacion_level + 0.1)
            
            # Ajustar precios al alza
            for bien in self.precios:
                self.precios[bien] *= 1.1
        
        elif estrategia.tipo == "innovacion":
            # Aumentar inversión en I+D
            inversion_id = estrategia.parametros.get('inversion_id', 0.15)
            self.inversiones_planificadas["investigacion_desarrollo"] = self.dinero * inversion_id
        
        elif estrategia.tipo == "nicho":
            # Especializarse en productos específicos
            productos_nicho = list(self.productos_ia.keys())[:2]  # Enfocar en 2 productos
            for bien in productos_nicho:
                if bien in self.productos_ia:
                    self.productos_ia[bien].competitividad *= 1.2
    
    def _ajustar_tacticas_estrategia(self) -> List[str]:
        """Ajusta tácticas específicas de la estrategia actual"""
        ajustes = []
        
        if not self.estrategia_actual:
            return ajustes
        
        # Ajustes basados en rendimiento reciente
        efectividad = self._evaluar_estrategia_actual()
        
        if efectividad < 0.5:
            # Estrategia no está funcionando bien
            if self.estrategia_actual.tipo == "liderazgo_costos":
                # Reducir más los costos
                for bien in self.costos_unitarios:
                    self.costos_unitarios[bien] *= 0.98
                ajustes.append("reduccion_costos_adicional")
            
            elif self.estrategia_actual.tipo == "diferenciacion":
                # Mejorar servicio al cliente
                self.satisfaccion_clientes = min(1.0, self.satisfaccion_clientes + 0.05)
                ajustes.append("mejora_servicio_cliente")
        
        return ajustes
    
    def optimizar_cartera_productos(self) -> Dict[str, Any]:
        """Optimiza la cartera de productos usando IA"""
        optimizaciones = {
            'productos_analizados': len(self.productos_ia),
            'productos_descontinuados': 0,
            'productos_mejorados': 0,
            'nuevos_productos': 0
        }
        
        # Analizar ciclo de vida de productos
        for nombre_producto, producto in self.productos_ia.items():
            # Actualizar ciclo de vida
            self._actualizar_ciclo_vida_producto(producto)
            
            # Decisiones basadas en ciclo de vida
            if producto.ciclo_vida == "declive" and producto.competitividad < 0.3:
                # Considerar descontinuar
                if self._evaluar_descontinuacion_producto(producto):
                    optimizaciones['productos_descontinuados'] += 1
            
            elif producto.ciclo_vida in ["introduccion", "crecimiento"]:
                # Optimizar producto
                if self._optimizar_producto_existente(producto):
                    optimizaciones['productos_mejorados'] += 1
        
        # Evaluar desarrollo de nuevos productos
        nuevos_productos = self._evaluar_nuevos_productos()
        optimizaciones['nuevos_productos'] = len(nuevos_productos)
        
        # Actualizar pipeline de innovación
        self._actualizar_pipeline_innovacion(nuevos_productos)
        
        return optimizaciones
    
    def _actualizar_ciclo_vida_producto(self, producto: ProductoIA):
        """Actualiza el ciclo de vida del producto"""
        # Lógica simplificada de transición de ciclo de vida
        if producto.ciclo_vida == "introduccion":
            if producto.demanda_predicha > 0.6:
                producto.ciclo_vida = "crecimiento"
        elif producto.ciclo_vida == "crecimiento":
            if producto.competitividad < 0.5:
                producto.ciclo_vida = "madurez"
        elif producto.ciclo_vida == "madurez":
            if producto.demanda_predicha < 0.3:
                producto.ciclo_vida = "declive"
    
    def _evaluar_descontinuacion_producto(self, producto: ProductoIA) -> bool:
        """Evalúa si descontinuar un producto"""
        # Criterios para descontinuación
        margen = producto.precio_sugerido - producto.costo_produccion
        
        if margen < 5 and producto.demanda_predicha < 0.2:
            return True
        
        return False
    
    def _optimizar_producto_existente(self, producto: ProductoIA) -> bool:
        """Optimiza un producto existente"""
        optimizado = False
        
        # Optimización de costos
        if producto.costo_produccion > producto.precio_sugerido * 0.7:
            # Reducir costos si son muy altos
            reduccion = random.uniform(0.05, 0.15)
            producto.costo_produccion *= (1 - reduccion)
            optimizado = True
        
        # Mejora de calidad
        if producto.calidad < 0.8 and self.dinero > 10000:
            inversion_calidad = min(5000, self.dinero * 0.05)
            mejora_calidad = inversion_calidad / 10000  # Factor de conversión
            producto.calidad = min(1.0, producto.calidad + mejora_calidad)
            self.dinero -= inversion_calidad
            optimizado = True
        
        return optimizado
    
    def _evaluar_nuevos_productos(self) -> List[Dict[str, Any]]:
        """Evalúa oportunidades de nuevos productos"""
        nuevos_productos = []
        
        # Analizar gaps en el mercado
        productos_competencia = set()
        for analisis in self.competidores_analizados.values():
            productos_competencia.update(analisis.precios_observados.keys())
        
        productos_propios = set(self.productos_ia.keys())
        gaps_mercado = productos_competencia - productos_propios
        
        # Evaluar cada gap
        for gap in list(gaps_mercado)[:3]:  # Máximo 3 nuevos productos
            if self._es_viable_nuevo_producto(gap):
                nuevo_producto = {
                    'nombre': gap,
                    'viabilidad': random.uniform(0.5, 0.9),
                    'inversion_requerida': random.uniform(5000, 20000),
                    'tiempo_desarrollo': random.randint(15, 60)
                }
                nuevos_productos.append(nuevo_producto)
        
        return nuevos_productos
    
    def _es_viable_nuevo_producto(self, nombre_producto: str) -> bool:
        """Evalúa si es viable desarrollar un nuevo producto"""
        # Recursos financieros suficientes
        if self.dinero < 10000:
            return False
        
        # Capacidad de desarrollo (simplificado)
        if len(self.pipeline_innovacion) > 5:  # Ya muchos proyectos
            return False
        
        # Estrategia permite innovación
        if self.estrategia_actual and self.estrategia_actual.tipo == "innovacion":
            return True
        
        return random.random() < 0.3  # 30% probabilidad base
    
    def _actualizar_pipeline_innovacion(self, nuevos_productos: List[Dict[str, Any]]):
        """Actualiza el pipeline de innovación"""
        # Agregar nuevos productos al pipeline
        for producto in nuevos_productos:
            if len(self.pipeline_innovacion) < 10:  # Límite del pipeline
                proyecto = {
                    'id': f"proyecto_{len(self.pipeline_innovacion)}",
                    'producto': producto,
                    'etapa': 'concepto',
                    'progreso': 0.0,
                    'inversion_actual': 0.0,
                    'fecha_inicio': datetime.now()
                }
                self.pipeline_innovacion.append(proyecto)
        
        # Actualizar progreso de proyectos existentes
        for proyecto in self.pipeline_innovacion:
            if random.random() < 0.3:  # 30% probabilidad de progreso
                proyecto['progreso'] = min(1.0, proyecto['progreso'] + random.uniform(0.1, 0.3))
                
                if proyecto['progreso'] >= 1.0 and proyecto['etapa'] != 'completado':
                    self._completar_proyecto_innovacion(proyecto)
    
    def _completar_proyecto_innovacion(self, proyecto: Dict[str, Any]):
        """Completa un proyecto de innovación"""
        proyecto['etapa'] = 'completado'
        
        # Crear nuevo producto
        producto_info = proyecto['producto']
        nuevo_producto = ProductoIA(
            nombre=producto_info['nombre'],
            categoria="nuevo",
            costo_produccion=random.uniform(15, 35),
            precio_sugerido=random.uniform(40, 80),
            calidad=random.uniform(0.6, 0.9),
            innovacion_level=random.uniform(0.7, 1.0),
            demanda_predicha=producto_info['viabilidad'],
            ciclo_vida="introduccion",
            competitividad=random.uniform(0.6, 0.9)
        )
        
        self.productos_ia[producto_info['nombre']] = nuevo_producto
        self.precios[producto_info['nombre']] = nuevo_producto.precio_sugerido
        self.costos_unitarios[producto_info['nombre']] = nuevo_producto.costo_produccion
        
        self.innovaciones_exitosas += 1
        print(f"[{self.nombre}] Nuevo producto lanzado: {producto_info['nombre']}")
    
    def gestionar_cadena_suministro_ia(self) -> Dict[str, Any]:
        """Gestiona la cadena de suministro con IA"""
        gestion = {
            'proveedores_evaluados': 0,
            'costos_optimizados': 0,
            'inventario_ajustado': 0,
            'eficiencia_logistica': self.eficiencia_operacional
        }
        
        # Evaluar proveedores (simulado)
        self._evaluar_proveedores()
        gestion['proveedores_evaluados'] = len(self.proveedores_evaluados)
        
        # Optimizar inventario
        optimizaciones_inventario = self._optimizar_inventario()
        gestion['inventario_ajustado'] = optimizaciones_inventario
        
        # Reducir costos logísticos
        reducciones_costo = self._optimizar_costos_logisticos()
        gestion['costos_optimizados'] = reducciones_costo
        
        return gestion
    
    def _evaluar_proveedores(self):
        """Evalúa y califica proveedores"""
        # Simulación de evaluación de proveedores
        proveedores_potenciales = [f"proveedor_{i}" for i in range(1, 6)]
        
        for proveedor in proveedores_potenciales:
            calificacion = random.uniform(0.3, 0.9)
            
            # Factores de evaluación
            factores = {
                'precio': random.uniform(0.4, 0.9),
                'calidad': random.uniform(0.5, 0.9),
                'confiabilidad': random.uniform(0.6, 0.9),
                'tiempo_entrega': random.uniform(0.5, 0.8)
            }
            
            # Calificación ponderada
            calificacion_final = (
                factores['precio'] * 0.3 +
                factores['calidad'] * 0.3 +
                factores['confiabilidad'] * 0.25 +
                factores['tiempo_entrega'] * 0.15
            )
            
            self.proveedores_evaluados[proveedor] = calificacion_final
    
    def _optimizar_inventario(self) -> int:
        """Optimiza niveles de inventario"""
        optimizaciones = 0
        
        for producto_nombre, producto in self.productos_ia.items():
            # Calcular inventario óptimo basándose en demanda predicha
            demanda_mensual = producto.demanda_predicha * 100  # Escalar
            inventario_optimo = demanda_mensual * 1.5  # 1.5 meses de stock
            
            inventario_actual = self.bienes.get(producto_nombre, 0)
            
            if abs(inventario_actual - inventario_optimo) > inventario_optimo * 0.2:
                self.inventario_optimo[producto_nombre] = inventario_optimo
                optimizaciones += 1
        
        return optimizaciones
    
    def _optimizar_costos_logisticos(self) -> int:
        """Optimiza costos logísticos"""
        reducciones = 0
        
        for producto_nombre in self.productos_ia.keys():
            costo_actual = self.costos_logisticos.get(producto_nombre, 5.0)
            
            # Buscar oportunidades de reducción
            if random.random() < 0.3:  # 30% probabilidad de encontrar mejora
                reduccion = random.uniform(0.05, 0.15)
                nuevo_costo = costo_actual * (1 - reduccion)
                self.costos_logisticos[producto_nombre] = nuevo_costo
                reducciones += 1
        
        return reducciones
    
    def formar_alianzas_estrategicas(self) -> List[str]:
        """Forma alianzas estratégicas con otras empresas"""
        nuevas_alianzas = []
        
        # Identificar candidatos para alianzas
        candidatos = self._identificar_candidatos_alianza()
        
        for candidato in candidatos[:2]:  # Máximo 2 alianzas nuevas por ciclo
            tipo_alianza = self._determinar_tipo_alianza(candidato)
            
            if tipo_alianza:
                alianza_id = self.comunicacion.formar_alianza_temporal(
                    [candidato],
                    tipo_alianza,
                    f"Alianza estratégica {tipo_alianza}",
                    duracion_dias=90
                )
                
                if alianza_id:
                    self.alianzas_activas.append(alianza_id)
                    nuevas_alianzas.append(alianza_id)
                    print(f"[{self.nombre}] Nueva alianza {tipo_alianza} con {candidato}")
        
        return nuevas_alianzas
    
    def _identificar_candidatos_alianza(self) -> List[str]:
        """Identifica candidatos potenciales para alianzas"""
        candidatos = []
        
        for empresa_id, analisis in self.competidores_analizados.items():
            # Criterios para alianza
            if (analisis.oportunidades_colaboracion > 0.5 and 
                analisis.nivel_amenaza < 0.7 and 
                empresa_id not in self.alianzas_activas):
                candidatos.append(empresa_id)
        
        return candidatos
    
    def _determinar_tipo_alianza(self, candidato: str) -> Optional[str]:
        """Determina el tipo de alianza más apropiado"""
        if candidato in self.competidores_analizados:
            analisis = self.competidores_analizados[candidato]
            
            # Alianza tecnológica si ambos innovan
            if (self.estrategia_actual and 
                self.estrategia_actual.tipo == "innovacion" and
                analisis.estrategia_percibida == "innovacion"):
                return "tecnologica"
            
            # Alianza de distribución si tienen fortalezas complementarias
            if "recursos_humanos" in analisis.fortalezas and "recursos_financieros" in analisis.debilidades:
                return "distribucion"
            
            # Alianza de compras para reducir costos
            if self.estrategia_actual and self.estrategia_actual.tipo == "liderazgo_costos":
                return "compras_conjuntas"
        
        return None
    
    def procesar_ciclo_empresarial_ia(self):
        """Procesa un ciclo completo de IA empresarial"""
        try:
            # 1. Desarrollar estrategia competitiva
            resultado_estrategia = self.desarrollar_estrategia_competitiva()
            
            # 2. Optimizar cartera de productos
            resultado_productos = self.optimizar_cartera_productos()
            
            # 3. Gestionar cadena de suministro
            resultado_suministro = self.gestionar_cadena_suministro_ia()
            
            # 4. Formar alianzas estratégicas
            nuevas_alianzas = self.formar_alianzas_estrategicas()
            
            # 5. Tomar decisiones operativas
            self._decisiones_operativas_ia()
            
            # 6. Actualizar métricas de rendimiento
            self._actualizar_metricas_rendimiento()
            
            # 7. Aprender de resultados
            self._aprender_de_resultados_ciclo()
            
        except Exception as e:
            print(f"[{self.nombre}] Error en ciclo empresarial IA: {e}")
    
    def _decisiones_operativas_ia(self):
        """Toma decisiones operativas usando IA"""
        # Decisión de precios
        self._ajustar_precios_ia()
        
        # Decisión de producción
        self._ajustar_produccion_ia()
        
        # Decisión de contratación
        self._evaluar_contratacion_ia()
    
    def _ajustar_precios_ia(self):
        """Ajusta precios usando IA"""
        for producto_nombre, producto in self.productos_ia.items():
            # Crear estado del mercado para decisión de precio
            estado_mercado = EstadoMercado(
                precios={producto_nombre: self.precios.get(producto_nombre, 50)},
                demanda={producto_nombre: producto.demanda_predicha},
                oferta={producto_nombre: 1.0},
                competidores=list(self.competidores_analizados.keys()),
                tendencias={},
                volatilidad={},
                ciclo_economico=getattr(self.mercado, 'ciclo_economico', 'expansion'),
                liquidez_mercado=1.0,
                riesgo_sistemico=0.1
            )
            
            # Crear opciones de precio
            precio_actual = self.precios.get(producto_nombre, 50)
            opciones_precio = [
                OpcionDecision(
                    id="mantener_precio",
                    tipo="precio",
                    parametros={'precio': precio_actual},
                    costo_estimado=0,
                    beneficio_estimado=precio_actual * producto.demanda_predicha,
                    riesgo_estimado=0.2,
                    complejidad=0.1
                ),
                OpcionDecision(
                    id="aumentar_precio",
                    tipo="precio",
                    parametros={'precio': precio_actual * 1.05},
                    costo_estimado=0,
                    beneficio_estimado=precio_actual * 1.05 * producto.demanda_predicha * 0.9,
                    riesgo_estimado=0.4,
                    complejidad=0.2
                ),
                OpcionDecision(
                    id="reducir_precio",
                    tipo="precio",
                    parametros={'precio': precio_actual * 0.95},
                    costo_estimado=0,
                    beneficio_estimado=precio_actual * 0.95 * producto.demanda_predicha * 1.1,
                    riesgo_estimado=0.3,
                    complejidad=0.2
                )
            ]
            
            # Decidir con IA
            decision_precio = self.ia_engine.tomar_decision_inteligente(estado_mercado, opciones_precio)
            
            # Aplicar decisión
            nuevo_precio = decision_precio.parametros['precio']
            self.precios[producto_nombre] = nuevo_precio
            producto.precio_sugerido = nuevo_precio
    
    def _ajustar_produccion_ia(self):
        """Ajusta niveles de producción usando IA"""
        for producto_nombre, producto in self.productos_ia.items():
            # Decisión de producción basada en demanda predicha
            produccion_objetivo = producto.demanda_predicha * 100  # Escalar
            
            # Ajustar por estrategia
            if self.estrategia_actual:
                if self.estrategia_actual.tipo == "liderazgo_costos":
                    produccion_objetivo *= 1.2  # Producir más para economías de escala
                elif self.estrategia_actual.tipo == "diferenciacion":
                    produccion_objetivo *= 0.8  # Producir menos, enfoque en calidad
    
    def _evaluar_contratacion_ia(self):
        """Evalúa necesidades de contratación usando IA"""
        # Calcular carga de trabajo actual
        empleados_actuales = len(self.empleados)
        carga_trabajo = sum(producto.demanda_predicha for producto in self.productos_ia.values())
        
        # Determinar si necesita más empleados
        empleados_necesarios = int(carga_trabajo / 2)  # 2 unidades de demanda por empleado
        
        if empleados_necesarios > empleados_actuales and self.dinero > 50000:
            # Intentar contratar
            empleados_a_contratar = min(3, empleados_necesarios - empleados_actuales)
            self.necesidades_contratacion['general'] = empleados_a_contratar
    
    def _actualizar_metricas_rendimiento(self):
        """Actualiza métricas de rendimiento empresarial"""
        # Calcular eficiencia operacional
        if self.productos_ia:
            competitividad_promedio = np.mean([p.competitividad for p in self.productos_ia.values()])
            self.eficiencia_operacional = (self.eficiencia_operacional * 0.9 + competitividad_promedio * 0.1)
        
        # Actualizar satisfacción de clientes (simulado)
        if self.estrategia_actual and self.estrategia_actual.tipo == "diferenciacion":
            self.satisfaccion_clientes = min(1.0, self.satisfaccion_clientes + 0.02)
        
        # Calcular ROI de estrategias
        if self.estrategia_actual:
            # Simplificado: ROI basado en efectividad
            efectividad = self._evaluar_estrategia_actual()
            self.roi_estrategias[self.estrategia_actual.nombre] = efectividad * 100
    
    def _aprender_de_resultados_ciclo(self):
        """Aprende de los resultados del ciclo actual"""
        # Crear decisión de ciclo completo
        decision_ciclo = Decision(
            agente_id=f"empresa_{self.nombre}",
            tipo_decision="ciclo_empresarial",
            contexto={
                'estrategia_actual': self.estrategia_actual.nombre if self.estrategia_actual else None,
                'productos_activos': len(self.productos_ia),
                'competidores_activos': len(self.competidores_analizados),
                'recursos_disponibles': self.dinero
            },
            accion_tomada={
                'ciclo_completado': True,
                'eficiencia_alcanzada': self.eficiencia_operacional,
                'satisfaccion_clientes': self.satisfaccion_clientes
            }
        )
        
        # Calcular recompensa del ciclo
        recompensa = (
            self.eficiencia_operacional * 50 +
            self.satisfaccion_clientes * 30 +
            len(self.alianzas_activas) * 10
        )
        
        decision_ciclo.recompensa = recompensa
        decision_ciclo.resultado = {
            'exito_ciclo': recompensa > 60,
            'metricas_finales': {
                'eficiencia': self.eficiencia_operacional,
                'satisfaccion': self.satisfaccion_clientes,
                'alianzas': len(self.alianzas_activas)
            }
        }
        
        # Aprender de la experiencia
        self.memoria.aprender_de_experiencia(decision_ciclo, decision_ciclo.resultado)
    
    def actualizar_conocimiento_mercado(self, estado_mercado):
        """Actualiza el conocimiento del mercado de la empresa"""
        try:
            # Convertir EstadoMercado a diccionario si es necesario
            if hasattr(estado_mercado, '__dict__'):
                estado_dict = estado_mercado.__dict__
            elif isinstance(estado_mercado, dict):
                estado_dict = estado_mercado
            else:
                # Si no es convertible, crear un diccionario básico
                estado_dict = {}
            
            # Actualizar análisis de mercado
            if 'precios' in estado_dict:
                # Analizar precios de competidores
                for bien, precio in estado_dict['precios'].items():
                    if bien in self.market_share:
                        precio_actual = float(precio)
                        # Ajustar estrategia de precios
                        if hasattr(self, 'precio_productos'):
                            if bien in self.precio_productos:
                                precio_empresa = self.precio_productos[bien]
                                if precio_actual < precio_empresa * 0.9:
                                    # Competidores más baratos, considerar ajuste
                                    self.precio_productos[bien] = precio_empresa * 0.95
            
            # Actualizar análisis de demanda
            if 'demanda_global' in estado_dict:
                for bien, demanda in estado_dict['demanda_global'].items():
                    if bien in self.productos_ia:
                        producto = self.productos_ia[bien]
                        producto.demanda_predicha = demanda
            
            # Actualizar información de crisis
            if 'en_crisis' in estado_dict:
                if estado_dict['en_crisis']:
                    # Activar estrategias de crisis
                    self.eficiencia_operacional = min(1.0, self.eficiencia_operacional * 1.1)
                    # Reducir inversión en riesgo
                    if self.estrategia_actual:
                        self.estrategia_actual.riesgo *= 0.8
                else:
                    # Normalizar operaciones
                    self.eficiencia_operacional = max(0.7, self.eficiencia_operacional * 0.98)
            
            # Actualizar market share basado en PIB
            if 'pib' in estado_dict:
                pib_actual = estado_dict['pib']
                if hasattr(self, 'ultimo_pib_empresa'):
                    if pib_actual > self.ultimo_pib_empresa:
                        # Economía creciendo, expandir market share
                        for bien in self.market_share:
                            self.market_share[bien] = min(1.0, self.market_share[bien] * 1.02)
                    else:
                        # Economía decreciendo, ser más conservador
                        for bien in self.market_share:
                            self.market_share[bien] = max(0.01, self.market_share[bien] * 0.98)
                self.ultimo_pib_empresa = pib_actual
            
        except Exception as e:
            print(f"[{self.nombre}] Error actualizando conocimiento de mercado: {e}")

    def get_estadisticas_empresariales_ia(self) -> Dict[str, Any]:
        """Obtiene estadísticas completas de la empresa IA"""
        return {
            'agente_id': f"empresa_{self.nombre}",
            'estrategia_actual': self.estrategia_actual.nombre if self.estrategia_actual else None,
            'productos_ia': len(self.productos_ia),
            'competidores_analizados': len(self.competidores_analizados),
            'alianzas_activas': len(self.alianzas_activas),
            'pipeline_innovacion': len(self.pipeline_innovacion),
            'innovaciones_exitosas': self.innovaciones_exitosas,
            'eficiencia_operacional': self.eficiencia_operacional,
            'satisfaccion_clientes': self.satisfaccion_clientes,
            'proveedores_evaluados': len(self.proveedores_evaluados),
            'market_share_promedio': np.mean(list(self.market_share.values())) if self.market_share else 0,
            'roi_estrategias': self.roi_estrategias,
            'memoria_decisiones': self.memoria.experiencia_total,
            'tasa_exito_ia': self.memoria.tasa_exito,
            'ia_engine_stats': self.ia_engine.get_estadisticas_ia(),
            'comunicacion_stats': self.comunicacion.get_estadisticas_comunicacion()
        }
    
    def finalizar_ia(self):
        """Finaliza todos los componentes IA de la empresa"""
        try:
            self.comunicacion.finalizar()
            print(f"[{self.nombre}] Sistemas empresariales IA finalizados")
        except Exception as e:
            print(f"[{self.nombre}] Error finalizando IA empresarial: {e}")
