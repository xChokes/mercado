"""
Sistema de Gestión Empresarial Avanzada
=======================================

Proporciona funcionalidades realistas para la gestión empresarial:
- Gestión de recursos humanos avanzada
- Análisis de competencia
- Innovación y desarrollo de productos
- Gestión de riesgos operacionales
- Responsabilidad social corporativa
- Gestión de la cadena de suministro
- Análisis financiero avanzado
"""

import random
import logging
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from collections import defaultdict


@dataclass
class EmpleadoPerfil:
    """Perfil detallado de empleado"""
    id: str
    nombre: str
    experiencia_años: int
    especializacion: str  # 'produccion', 'ventas', 'administracion', 'investigacion'
    productividad: float  # 0.5 - 1.5
    salario_base: float
    satisfaccion: float  # 0.0 - 1.0
    fecha_contratacion: datetime
    capacitacion_recibida: List[str]
    evaluacion_desempeño: float  # 0.0 - 1.0


@dataclass
class ProyectoID:
    """Proyecto de Investigación y Desarrollo"""
    id: str
    nombre: str
    tipo: str  # 'producto_nuevo', 'mejora_proceso', 'tecnologia_limpia'
    inversion_total: float
    inversion_actual: float
    progreso: float  # 0.0 - 1.0
    riesgo_tecnico: float
    tiempo_estimado: int  # días
    dias_transcurridos: int
    equipo_asignado: List[str]  # IDs de empleados
    beneficio_esperado: float


@dataclass
class RiesgoOperacional:
    """Riesgo operacional de la empresa"""
    tipo: str  # 'tecnologico', 'regulatorio', 'mercado', 'reputacional'
    probabilidad: float  # 0.0 - 1.0
    impacto_estimado: float  # en dinero
    medidas_mitigacion: List[str]
    costo_mitigacion: float
    estado: str  # 'identificado', 'en_tratamiento', 'mitigado'


@dataclass
class CompetidorAnalisis:
    """Análisis detallado de competidor"""
    nombre: str
    fortalezas: List[str]
    debilidades: List[str]
    participacion_mercado: float
    estrategia_precios: str
    productos_estrella: List[str]
    amenaza_nivel: float  # 0.0 - 1.0
    ultimas_acciones: List[str]


class GestionRRHH:
    """Sistema de gestión de recursos humanos avanzado"""
    
    def __init__(self, empresa):
        self.empresa = empresa
        self.empleados: Dict[str, EmpleadoPerfil] = {}
        self.politicas_rrhh = {
            'rotacion_aceptable': 0.15,  # 15% anual
            'presupuesto_capacitacion': 0.03,  # 3% de masa salarial
            'evaluacion_frecuencia': 6,  # cada 6 meses
            'bonus_productividad': 0.1  # 10% extra por alta productividad
        }
        self.programas_capacitacion = [
            'liderazgo', 'tecnologia', 'calidad', 'innovacion', 'idiomas'
        ]
        self.indicadores_clima = {
            'satisfaccion_promedio': 0.7,
            'rotacion_mensual': 0.02,
            'ausentismo': 0.05,
            'productividad_promedio': 0.8
        }
    
    def contratar_empleado(self, especialidad: str = None) -> Optional[EmpleadoPerfil]:
        """Contrata un nuevo empleado con perfil específico"""
        if len(self.empleados) >= self.empresa.capacidad_empleo:
            return None
        
        especialidades = ['produccion', 'ventas', 'administracion', 'investigacion']
        especialidad = especialidad or random.choice(especialidades)
        
        # Generar perfil basado en presupuesto disponible
        salario_base = self._calcular_salario_mercado(especialidad)
        if salario_base * 12 > self.empresa.dinero * 0.1:  # No más del 10% del capital
            return None
        
        empleado = EmpleadoPerfil(
            id=f"emp_{len(self.empleados) + 1}",
            nombre=f"Empleado_{len(self.empleados) + 1}",
            experiencia_años=random.randint(1, 15),
            especializacion=especialidad,
            productividad=random.uniform(0.6, 1.2),
            salario_base=salario_base,
            satisfaccion=random.uniform(0.6, 0.9),
            fecha_contratacion=datetime.now(),
            capacitacion_recibida=[],
            evaluacion_desempeño=random.uniform(0.6, 0.9)
        )
        
        self.empleados[empleado.id] = empleado
        self.empresa.dinero -= salario_base  # Costo de contratación
        
        logging.info(f"{self.empresa.nombre}: Contratado {empleado.nombre} ({especialidad}) - ${salario_base:,.0f}/mes")
        return empleado
    
    def _calcular_salario_mercado(self, especialidad: str) -> float:
        """Calcula salario de mercado según especialidad"""
        salarios_base = {
            'produccion': random.uniform(2500, 4000),
            'ventas': random.uniform(3000, 5000),
            'administracion': random.uniform(3500, 6000),
            'investigacion': random.uniform(4000, 7000)
        }
        return salarios_base.get(especialidad, 3000)
    
    def evaluar_desempeño(self) -> Dict[str, float]:
        """Evalúa el desempeño de todos los empleados"""
        evaluaciones = {}
        
        for emp_id, empleado in self.empleados.items():
            # Factores de evaluación
            factor_experiencia = min(1.0, empleado.experiencia_años / 10)
            factor_satisfaccion = empleado.satisfaccion
            factor_capacitacion = len(empleado.capacitacion_recibida) * 0.05
            
            # Variabilidad individual
            variacion = random.uniform(-0.1, 0.1)
            
            evaluacion = (factor_experiencia * 0.4 + 
                         factor_satisfaccion * 0.4 + 
                         factor_capacitacion * 0.2 + 
                         variacion)
            
            evaluacion = max(0.0, min(1.0, evaluacion))
            empleado.evaluacion_desempeño = evaluacion
            evaluaciones[emp_id] = evaluacion
        
        return evaluaciones
    
    def gestionar_capacitacion(self) -> int:
        """Gestiona programas de capacitación"""
        presupuesto_disponible = sum(emp.salario_base for emp in self.empleados.values()) * \
                                self.politicas_rrhh['presupuesto_capacitacion']
        
        if presupuesto_disponible > self.empresa.dinero * 0.05:
            return 0
        
        capacitaciones_realizadas = 0
        
        for empleado in self.empleados.values():
            if empleado.evaluacion_desempeño < 0.7 and random.random() < 0.3:
                programa = random.choice(self.programas_capacitacion)
                costo_capacitacion = random.uniform(500, 2000)
                
                if costo_capacitacion <= presupuesto_disponible:
                    empleado.capacitacion_recibida.append(programa)
                    empleado.productividad = min(1.5, empleado.productividad + 0.1)
                    empleado.satisfaccion = min(1.0, empleado.satisfaccion + 0.05)
                    
                    presupuesto_disponible -= costo_capacitacion
                    self.empresa.dinero -= costo_capacitacion
                    capacitaciones_realizadas += 1
        
        return capacitaciones_realizadas
    
    def gestionar_rotacion(self) -> List[str]:
        """Gestiona la rotación de personal"""
        empleados_salientes = []
        
        for emp_id, empleado in list(self.empleados.items()):
            # Probabilidad de salida basada en satisfacción
            prob_salida = (1.0 - empleado.satisfaccion) * 0.1  # Máximo 10% mensual
            
            if random.random() < prob_salida:
                empleados_salientes.append(emp_id)
                del self.empleados[emp_id]
                logging.info(f"{self.empresa.nombre}: {empleado.nombre} renunció (satisfacción: {empleado.satisfaccion:.2f})")
        
        return empleados_salientes
    
    def calcular_productividad_total(self) -> float:
        """Calcula la productividad total del equipo"""
        if not self.empleados:
            return 0.5  # Productividad mínima sin empleados
        
        productividad_total = sum(emp.productividad for emp in self.empleados.values())
        productividad_promedio = productividad_total / len(self.empleados)
        
        # Bonus por trabajo en equipo
        if len(self.empleados) > 3:
            bonus_equipo = min(0.2, len(self.empleados) * 0.02)
            productividad_promedio += bonus_equipo
        
        return min(1.5, productividad_promedio)


class GestionInnovacion:
    """Sistema de gestión de innovación y desarrollo"""
    
    def __init__(self, empresa):
        self.empresa = empresa
        self.proyectos_activos: Dict[str, ProyectoID] = {}
        self.proyectos_completados: List[ProyectoID] = []
        self.presupuesto_id = 0.05  # 5% de ingresos
        self.capacidad_maxima_proyectos = 3
        
    def evaluar_oportunidades_innovacion(self) -> List[Dict[str, Any]]:
        """Evalúa oportunidades de innovación"""
        oportunidades = []
        
        # Innovación en productos existentes
        for producto in self.empresa.bienes.keys():
            if random.random() < 0.2:  # 20% probabilidad por producto
                oportunidad = {
                    'tipo': 'mejora_producto',
                    'objetivo': producto,
                    'inversion_estimada': random.uniform(5000, 25000),
                    'beneficio_esperado': random.uniform(10000, 50000),
                    'riesgo_tecnico': random.uniform(0.2, 0.6),
                    'tiempo_desarrollo': random.randint(30, 90)
                }
                oportunidades.append(oportunidad)
        
        # Nuevos productos basados en competencia
        if hasattr(self.empresa, 'competidores_analizados'):
            productos_competencia = set()
            for comp in getattr(self.empresa, 'competidores_analizados', {}).values():
                if hasattr(comp, 'productos_estrella'):
                    productos_competencia.update(comp.productos_estrella)
            
            productos_propios = set(self.empresa.bienes.keys())
            gaps = productos_competencia - productos_propios
            
            for gap in list(gaps)[:2]:  # Máximo 2 gaps
                oportunidad = {
                    'tipo': 'producto_nuevo',
                    'objetivo': gap,
                    'inversion_estimada': random.uniform(15000, 50000),
                    'beneficio_esperado': random.uniform(25000, 100000),
                    'riesgo_tecnico': random.uniform(0.4, 0.8),
                    'tiempo_desarrollo': random.randint(60, 180)
                }
                oportunidades.append(oportunidad)
        
        # Innovación en procesos
        if random.random() < 0.15:  # 15% probabilidad
            oportunidad = {
                'tipo': 'mejora_proceso',
                'objetivo': 'eficiencia_operativa',
                'inversion_estimada': random.uniform(10000, 30000),
                'beneficio_esperado': random.uniform(20000, 60000),
                'riesgo_tecnico': random.uniform(0.1, 0.4),
                'tiempo_desarrollo': random.randint(45, 120)
            }
            oportunidades.append(oportunidad)
        
        return oportunidades
    
    def iniciar_proyecto_id(self, oportunidad: Dict[str, Any]) -> Optional[ProyectoID]:
        """Inicia un nuevo proyecto de I+D"""
        if len(self.proyectos_activos) >= self.capacidad_maxima_proyectos:
            return None
        
        if oportunidad['inversion_estimada'] > self.empresa.dinero * 0.2:
            return None
        
        proyecto = ProyectoID(
            id=f"id_{len(self.proyectos_activos) + 1}",
            nombre=f"Proyecto {oportunidad['tipo']} - {oportunidad['objetivo']}",
            tipo=oportunidad['tipo'],
            inversion_total=oportunidad['inversion_estimada'],
            inversion_actual=0,
            progreso=0.0,
            riesgo_tecnico=oportunidad['riesgo_tecnico'],
            tiempo_estimado=oportunidad['tiempo_desarrollo'],
            dias_transcurridos=0,
            equipo_asignado=[],
            beneficio_esperado=oportunidad['beneficio_esperado']
        )
        
        # Asignar equipo de investigación
        if hasattr(self.empresa, 'empleados'):
            investigadores = [emp for emp in self.empresa.empleados 
                            if hasattr(emp, 'especializacion') and emp.especializacion == 'investigacion']
            if investigadores:
                proyecto.equipo_asignado = [inv.id for inv in investigadores[:2]]
        
        self.proyectos_activos[proyecto.id] = proyecto
        logging.info(f"{self.empresa.nombre}: Iniciado {proyecto.nombre} - ${proyecto.inversion_total:,.0f}")
        
        return proyecto
    
    def avanzar_proyectos(self) -> List[ProyectoID]:
        """Avanza el progreso de todos los proyectos activos"""
        proyectos_completados = []
        
        for proyecto in list(self.proyectos_activos.values()):
            # Calcular inversión mensual
            inversion_mensual = proyecto.inversion_total / (proyecto.tiempo_estimado / 30)
            
            if inversion_mensual <= self.empresa.dinero:
                self.empresa.dinero -= inversion_mensual
                proyecto.inversion_actual += inversion_mensual
                
                # Progreso basado en equipo asignado
                factor_equipo = len(proyecto.equipo_asignado) * 0.3 + 0.4
                progreso_base = (1 / (proyecto.tiempo_estimado / 30)) * factor_equipo
                
                # Riesgo técnico puede ralentizar el proyecto
                if random.random() < proyecto.riesgo_tecnico * 0.1:
                    progreso_base *= 0.5  # Complicación técnica
                
                proyecto.progreso = min(1.0, proyecto.progreso + progreso_base)
                proyecto.dias_transcurridos += 30
                
                # Completar proyecto
                if proyecto.progreso >= 1.0:
                    self._completar_proyecto(proyecto)
                    proyectos_completados.append(proyecto)
                    del self.proyectos_activos[proyecto.id]
        
        return proyectos_completados
    
    def _completar_proyecto(self, proyecto: ProyectoID):
        """Completa un proyecto y aplica sus beneficios"""
        self.proyectos_completados.append(proyecto)
        
        if proyecto.tipo == 'mejora_producto':
            # Mejorar calidad/reducir costos del producto
            if proyecto.objetivo in self.empresa.costos_unitarios:
                reduccion_costo = random.uniform(0.05, 0.15)
                self.empresa.costos_unitarios[proyecto.objetivo] *= (1 - reduccion_costo)
                logging.info(f"{self.empresa.nombre}: Reducidos costos de {proyecto.objetivo} en {reduccion_costo:.1%}")
        
        elif proyecto.tipo == 'producto_nuevo':
            # Agregar nuevo producto
            nuevo_costo = random.uniform(10, 30)
            nuevo_precio = nuevo_costo * random.uniform(1.3, 2.0)
            
            self.empresa.costos_unitarios[proyecto.objetivo] = nuevo_costo
            self.empresa.precios[proyecto.objetivo] = nuevo_precio
            self.empresa.bienes[proyecto.objetivo] = []
            
            logging.info(f"{self.empresa.nombre}: Lanzado nuevo producto {proyecto.objetivo}")
        
        elif proyecto.tipo == 'mejora_proceso':
            # Mejorar eficiencia general
            if hasattr(self.empresa, 'eficiencia_produccion'):
                mejora = random.uniform(0.02, 0.08)
                self.empresa.eficiencia_produccion = min(1.2, self.empresa.eficiencia_produccion + mejora)
                logging.info(f"{self.empresa.nombre}: Mejorada eficiencia en {mejora:.1%}")


class GestionRiesgos:
    """Sistema de gestión de riesgos operacionales"""
    
    def __init__(self, empresa):
        self.empresa = empresa
        self.riesgos_identificados: Dict[str, RiesgoOperacional] = {}
        self.matriz_riesgos = {
            'tecnologico': {'prob_base': 0.1, 'impacto_base': 0.15},
            'regulatorio': {'prob_base': 0.05, 'impacto_base': 0.20},
            'mercado': {'prob_base': 0.20, 'impacto_base': 0.10},
            'reputacional': {'prob_base': 0.08, 'impacto_base': 0.25},
            'operacional': {'prob_base': 0.15, 'impacto_base': 0.12}
        }
    
    def identificar_riesgos(self) -> List[RiesgoOperacional]:
        """Identifica nuevos riesgos operacionales"""
        nuevos_riesgos = []
        
        for tipo_riesgo, parametros in self.matriz_riesgos.items():
            if random.random() < parametros['prob_base'] * 0.1:  # 10% de la probabilidad base mensual
                impacto = self.empresa.dinero * parametros['impacto_base'] * random.uniform(0.5, 1.5)
                
                riesgo = RiesgoOperacional(
                    tipo=tipo_riesgo,
                    probabilidad=random.uniform(0.1, 0.6),
                    impacto_estimado=impacto,
                    medidas_mitigacion=self._generar_medidas_mitigacion(tipo_riesgo),
                    costo_mitigacion=impacto * random.uniform(0.1, 0.3),
                    estado='identificado'
                )
                
                riesgo_id = f"riesgo_{tipo_riesgo}_{len(self.riesgos_identificados)}"
                self.riesgos_identificados[riesgo_id] = riesgo
                nuevos_riesgos.append(riesgo)
        
        return nuevos_riesgos
    
    def _generar_medidas_mitigacion(self, tipo_riesgo: str) -> List[str]:
        """Genera medidas de mitigación según el tipo de riesgo"""
        medidas = {
            'tecnologico': ['backup_sistemas', 'actualizacion_equipos', 'capacitacion_tecnica'],
            'regulatorio': ['auditoria_legal', 'actualizacion_politicas', 'consultor_externo'],
            'mercado': ['diversificacion_productos', 'analisis_competencia', 'seguro_comercial'],
            'reputacional': ['plan_comunicacion', 'monitoreo_medios', 'programa_rsc'],
            'operacional': ['procedimientos_emergencia', 'seguro_operacional', 'redundancia_procesos']
        }
        
        medidas_tipo = medidas.get(tipo_riesgo, ['medida_generica'])
        return random.sample(medidas_tipo, min(2, len(medidas_tipo)))
    
    def evaluar_mitigacion_riesgos(self) -> Dict[str, bool]:
        """Evalúa y aplica medidas de mitigación de riesgos"""
        decisiones = {}
        
        for riesgo_id, riesgo in self.riesgos_identificados.items():
            if riesgo.estado == 'identificado':
                # Evaluar si vale la pena mitigar
                costo_beneficio = riesgo.impacto_estimado * riesgo.probabilidad
                
                if costo_beneficio > riesgo.costo_mitigacion and \
                   riesgo.costo_mitigacion <= self.empresa.dinero * 0.05:
                    
                    self.empresa.dinero -= riesgo.costo_mitigacion
                    riesgo.estado = 'en_tratamiento'
                    riesgo.probabilidad *= 0.3  # Reducir probabilidad significativamente
                    decisiones[riesgo_id] = True
                    
                    logging.info(f"{self.empresa.nombre}: Mitigando riesgo {riesgo.tipo} - ${riesgo.costo_mitigacion:,.0f}")
                else:
                    decisiones[riesgo_id] = False
        
        return decisiones
    
    def materializar_riesgos(self) -> List[Tuple[str, float]]:
        """Evalúa si algún riesgo se materializa"""
        riesgos_materializados = []
        
        for riesgo_id, riesgo in list(self.riesgos_identificados.items()):
            if random.random() < riesgo.probabilidad * 0.1:  # 10% de la probabilidad mensual
                # El riesgo se materializa
                impacto_real = riesgo.impacto_estimado * random.uniform(0.7, 1.3)
                self.empresa.dinero -= impacto_real
                
                riesgos_materializados.append((riesgo.tipo, impacto_real))
                del self.riesgos_identificados[riesgo_id]
                
                logging.warning(f"{self.empresa.nombre}: Riesgo {riesgo.tipo} materializado - Pérdida: ${impacto_real:,.0f}")
        
        return riesgos_materializados


class ResponsabilidadSocial:
    """Sistema de responsabilidad social corporativa"""
    
    def __init__(self, empresa):
        self.empresa = empresa
        self.programas_rsc = {
            'medio_ambiente': {'activo': False, 'inversion': 0, 'beneficio_reputacion': 0.1},
            'comunidad': {'activo': False, 'inversion': 0, 'beneficio_reputacion': 0.08},
            'empleados': {'activo': False, 'inversion': 0, 'beneficio_reputacion': 0.06},
            'proveedores': {'activo': False, 'inversion': 0, 'beneficio_reputacion': 0.05}
        }
        self.reputacion_corporativa = 0.5  # 0.0 - 1.0
        self.presupuesto_rsc = 0.02  # 2% de ingresos
    
    def evaluar_programas_rsc(self) -> Dict[str, bool]:
        """Evalúa qué programas de RSC implementar"""
        presupuesto_disponible = self.empresa.dinero * self.presupuesto_rsc
        decisiones = {}
        
        for programa, config in self.programas_rsc.items():
            if not config['activo']:
                costo_anual = random.uniform(5000, 15000)
                beneficio_esperado = config['beneficio_reputacion'] * self.empresa.dinero * 0.05
                
                if costo_anual <= presupuesto_disponible and beneficio_esperado > costo_anual:
                    config['activo'] = True
                    config['inversion'] = costo_anual
                    self.empresa.dinero -= costo_anual
                    presupuesto_disponible -= costo_anual
                    decisiones[programa] = True
                    
                    logging.info(f"{self.empresa.nombre}: Implementado programa RSC {programa} - ${costo_anual:,.0f}")
                else:
                    decisiones[programa] = False
        
        return decisiones
    
    def calcular_impacto_reputacion(self) -> float:
        """Calcula el impacto de la reputación en el negocio"""
        # Beneficios por programas activos
        for programa, config in self.programas_rsc.items():
            if config['activo']:
                self.reputacion_corporativa = min(1.0, 
                    self.reputacion_corporativa + config['beneficio_reputacion'] * 0.01)
        
        # La buena reputación puede aumentar demanda y permitir precios premium
        factor_reputacion = 1.0 + (self.reputacion_corporativa - 0.5) * 0.2
        
        return factor_reputacion


class AnalisisCompetencia:
    """Sistema de análisis de competencia"""
    
    def __init__(self, empresa):
        self.empresa = empresa
        self.competidores: Dict[str, CompetidorAnalisis] = {}
        self.frecuencia_analisis = 3  # cada 3 ciclos
        self.ultimo_analisis = 0
    
    def actualizar_analisis_competencia(self, mercado) -> Dict[str, CompetidorAnalisis]:
        """Actualiza el análisis de todos los competidores"""
        if not hasattr(mercado, 'personas'):
            return {}
        
        competidores_actuales = {}
        
        for persona in mercado.personas:
            if (hasattr(persona, 'nombre') and persona.nombre != self.empresa.nombre and
                hasattr(persona, 'precios') and hasattr(persona, 'dinero')):
                
                analisis = self._analizar_competidor(persona, mercado)
                competidores_actuales[persona.nombre] = analisis
        
        self.competidores = competidores_actuales
        return competidores_actuales
    
    def _analizar_competidor(self, competidor, mercado) -> CompetidorAnalisis:
        """Analiza un competidor específico"""
        # Identificar fortalezas y debilidades
        fortalezas = []
        debilidades = []
        
        # Análisis financiero
        if competidor.dinero > self.empresa.dinero * 1.2:
            fortalezas.append("recursos_financieros")
        elif competidor.dinero < self.empresa.dinero * 0.5:
            debilidades.append("limitaciones_financieras")
        
        # Análisis de precios
        precios_competidor = []
        precios_propios = []
        productos_comunes = set(competidor.precios.keys()) & set(self.empresa.precios.keys())
        
        for producto in productos_comunes:
            precios_competidor.append(competidor.precios[producto])
            precios_propios.append(self.empresa.precios[producto])
        
        estrategia_precios = "indefinida"
        if precios_competidor and precios_propios:
            precio_prom_comp = sum(precios_competidor) / len(precios_competidor)
            precio_prom_propio = sum(precios_propios) / len(precios_propios)
            
            if precio_prom_comp < precio_prom_propio * 0.9:
                estrategia_precios = "precios_bajos"
                fortalezas.append("competitividad_precios")
            elif precio_prom_comp > precio_prom_propio * 1.1:
                estrategia_precios = "premium"
                fortalezas.append("productos_premium")
            else:
                estrategia_precios = "paridad"
        
        # Análisis de diversificación
        if len(competidor.precios) > len(self.empresa.precios):
            fortalezas.append("diversificacion_productos")
        elif len(competidor.precios) < len(self.empresa.precios) * 0.7:
            debilidades.append("productos_limitados")
        
        # Calcular nivel de amenaza
        amenaza = self._calcular_nivel_amenaza(competidor, productos_comunes)
        
        # Identificar productos estrella (los más caros, asumiendo calidad premium)
        productos_estrella = []
        if hasattr(competidor, 'precios'):
            productos_ordenados = sorted(competidor.precios.items(), key=lambda x: x[1], reverse=True)
            productos_estrella = [p[0] for p in productos_ordenados[:3]]
        
        return CompetidorAnalisis(
            nombre=competidor.nombre,
            fortalezas=fortalezas,
            debilidades=debilidades,
            participacion_mercado=random.uniform(0.05, 0.25),  # Simplificado
            estrategia_precios=estrategia_precios,
            productos_estrella=productos_estrella,
            amenaza_nivel=amenaza,
            ultimas_acciones=self._detectar_acciones_recientes(competidor)
        )
    
    def _calcular_nivel_amenaza(self, competidor, productos_comunes: set) -> float:
        """Calcula el nivel de amenaza de un competidor"""
        amenaza_base = 0.3
        
        # Factor financiero
        if competidor.dinero > self.empresa.dinero:
            amenaza_base += 0.2
        
        # Factor de competencia directa
        if len(productos_comunes) > len(self.empresa.precios) * 0.5:
            amenaza_base += 0.3
        
        # Factor de empleados (si tiene más empleados)
        if hasattr(competidor, 'empleados') and hasattr(self.empresa, 'empleados'):
            if len(competidor.empleados) > len(self.empresa.empleados):
                amenaza_base += 0.2
        
        return min(1.0, amenaza_base)
    
    def _detectar_acciones_recientes(self, competidor) -> List[str]:
        """Detecta acciones recientes del competidor"""
        acciones = []
        
        # Simplificado: acciones basadas en probabilidades
        if random.random() < 0.2:
            acciones.append("reduccion_precios")
        if random.random() < 0.15:
            acciones.append("lanzamiento_producto")
        if random.random() < 0.1:
            acciones.append("expansion_capacidad")
        if random.random() < 0.08:
            acciones.append("campaña_marketing")
        
        return acciones
    
    def generar_recomendaciones_estrategicas(self) -> List[str]:
        """Genera recomendaciones estratégicas basadas en análisis de competencia"""
        recomendaciones = []
        
        # Analizar amenazas principales
        amenazas_altas = [comp for comp in self.competidores.values() if comp.amenaza_nivel > 0.6]
        
        if amenazas_altas:
            # Estrategias defensivas
            for amenaza in amenazas_altas:
                if "competitividad_precios" in amenaza.fortalezas:
                    recomendaciones.append("Considerar reducción de precios o mejora de valor")
                if "diversificacion_productos" in amenaza.fortalezas:
                    recomendaciones.append("Evaluar expansión de línea de productos")
                if "recursos_financieros" in amenaza.fortalezas:
                    recomendaciones.append("Buscar financiamiento o alianzas estratégicas")
        
        # Identificar oportunidades
        competidores_debiles = [comp for comp in self.competidores.values() 
                              if "limitaciones_financieras" in comp.debilidades]
        
        if competidores_debiles:
            recomendaciones.append("Oportunidad de ganar market share con estrategia agresiva")
        
        # Análisis de gaps de productos
        todos_productos = set()
        for comp in self.competidores.values():
            todos_productos.update(comp.productos_estrella)
        
        productos_propios = set(self.empresa.precios.keys())
        gaps = todos_productos - productos_propios
        
        if gaps:
            recomendaciones.append(f"Considerar desarrollo de: {', '.join(list(gaps)[:3])}")
        
        return recomendaciones


class GestionEmpresarialAvanzada:
    """Sistema integrado de gestión empresarial avanzada"""
    
    def __init__(self, empresa):
        self.empresa = empresa
        
        # Subsistemas de gestión
        self.gestion_rrhh = GestionRRHH(empresa)
        self.gestion_innovacion = GestionInnovacion(empresa)
        self.gestion_riesgos = GestionRiesgos(empresa)
        self.responsabilidad_social = ResponsabilidadSocial(empresa)
        self.analisis_competencia = AnalisisCompetencia(empresa)
        
        # KPIs empresariales
        self.kpis = {
            'roi': 0.0,
            'margen_operativo': 0.0,
            'satisfaccion_empleados': 0.7,
            'cuota_mercado': 0.0,
            'nivel_innovacion': 0.0,
            'reputacion_corporativa': 0.5,
            'eficiencia_operativa': 0.7
        }
        
        # Historial de decisiones para aprendizaje
        self.historial_decisiones = []
        
    def ciclo_gestion_avanzada(self, mercado) -> Dict[str, Any]:
        """Ejecuta un ciclo completo de gestión empresarial avanzada"""
        resultados = {
            'rrhh': {},
            'innovacion': {},
            'riesgos': {},
            'rsc': {},
            'competencia': {},
            'kpis': {}
        }
        
        try:
            # 1. Gestión de Recursos Humanos
            resultados['rrhh'] = self._ciclo_rrhh()
            
            # 2. Gestión de Innovación
            resultados['innovacion'] = self._ciclo_innovacion()
            
            # 3. Gestión de Riesgos
            resultados['riesgos'] = self._ciclo_riesgos()
            
            # 4. Responsabilidad Social
            resultados['rsc'] = self._ciclo_rsc()
            
            # 5. Análisis de Competencia
            resultados['competencia'] = self._ciclo_competencia(mercado)
            
            # 6. Actualizar KPIs
            resultados['kpis'] = self._actualizar_kpis()
            
            # 7. Generar reporte ejecutivo
            reporte = self._generar_reporte_ejecutivo(resultados)
            resultados['reporte_ejecutivo'] = reporte
            
        except Exception as e:
            logging.error(f"Error en ciclo de gestión avanzada de {self.empresa.nombre}: {e}")
            
        return resultados
    
    def _ciclo_rrhh(self) -> Dict[str, Any]:
        """Ciclo de gestión de recursos humanos"""
        # Evaluar desempeño
        evaluaciones = self.gestion_rrhh.evaluar_desempeño()
        
        # Gestionar capacitación
        capacitaciones = self.gestion_rrhh.gestionar_capacitacion()
        
        # Gestionar rotación
        salidas = self.gestion_rrhh.gestionar_rotacion()
        
        # Contrataciones necesarias
        contrataciones = 0
        if len(self.gestion_rrhh.empleados) < self.empresa.capacidad_empleo * 0.8:
            if random.random() < 0.3:  # 30% probabilidad de contratar
                nuevo_empleado = self.gestion_rrhh.contratar_empleado()
                if nuevo_empleado:
                    contrataciones = 1
        
        # Calcular productividad total
        productividad_total = self.gestion_rrhh.calcular_productividad_total()
        
        return {
            'empleados_actuales': len(self.gestion_rrhh.empleados),
            'evaluaciones_realizadas': len(evaluaciones),
            'capacitaciones_realizadas': capacitaciones,
            'rotacion_empleados': len(salidas),
            'nuevas_contrataciones': contrataciones,
            'productividad_total': productividad_total
        }
    
    def _ciclo_innovacion(self) -> Dict[str, Any]:
        """Ciclo de gestión de innovación"""
        # Evaluar oportunidades
        oportunidades = self.gestion_innovacion.evaluar_oportunidades_innovacion()
        
        # Iniciar nuevos proyectos
        nuevos_proyectos = 0
        for oportunidad in oportunidades[:2]:  # Máximo 2 nuevos proyectos
            if self.gestion_innovacion.iniciar_proyecto_id(oportunidad):
                nuevos_proyectos += 1
        
        # Avanzar proyectos existentes
        proyectos_completados = self.gestion_innovacion.avanzar_proyectos()
        
        return {
            'oportunidades_identificadas': len(oportunidades),
            'proyectos_iniciados': nuevos_proyectos,
            'proyectos_activos': len(self.gestion_innovacion.proyectos_activos),
            'proyectos_completados': len(proyectos_completados),
            'inversion_total_id': sum(p.inversion_actual for p in self.gestion_innovacion.proyectos_activos.values())
        }
    
    def _ciclo_riesgos(self) -> Dict[str, Any]:
        """Ciclo de gestión de riesgos"""
        # Identificar nuevos riesgos
        nuevos_riesgos = self.gestion_riesgos.identificar_riesgos()
        
        # Evaluar mitigación
        mitigaciones = self.gestion_riesgos.evaluar_mitigacion_riesgos()
        
        # Materialización de riesgos
        riesgos_materializados = self.gestion_riesgos.materializar_riesgos()
        
        return {
            'riesgos_identificados': len(nuevos_riesgos),
            'riesgos_activos': len(self.gestion_riesgos.riesgos_identificados),
            'mitigaciones_implementadas': sum(mitigaciones.values()),
            'riesgos_materializados': len(riesgos_materializados),
            'impacto_riesgos': sum(impacto for _, impacto in riesgos_materializados)
        }
    
    def _ciclo_rsc(self) -> Dict[str, Any]:
        """Ciclo de responsabilidad social corporativa"""
        # Evaluar programas RSC
        decisiones_rsc = self.responsabilidad_social.evaluar_programas_rsc()
        
        # Calcular impacto en reputación
        factor_reputacion = self.responsabilidad_social.calcular_impacto_reputacion()
        
        return {
            'programas_implementados': sum(decisiones_rsc.values()),
            'programas_activos': sum(1 for p in self.responsabilidad_social.programas_rsc.values() if p['activo']),
            'reputacion_corporativa': self.responsabilidad_social.reputacion_corporativa,
            'factor_reputacion': factor_reputacion
        }
    
    def _ciclo_competencia(self, mercado) -> Dict[str, Any]:
        """Ciclo de análisis de competencia"""
        # Actualizar análisis
        competidores_analizados = self.analisis_competencia.actualizar_analisis_competencia(mercado)
        
        # Generar recomendaciones
        recomendaciones = self.analisis_competencia.generar_recomendaciones_estrategicas()
        
        return {
            'competidores_analizados': len(competidores_analizados),
            'amenazas_altas': sum(1 for c in competidores_analizados.values() if c.amenaza_nivel > 0.6),
            'recomendaciones_estrategicas': recomendaciones,
            'principales_competidores': [c.nombre for c in competidores_analizados.values() 
                                       if c.amenaza_nivel > 0.5]
        }
    
    def _actualizar_kpis(self) -> Dict[str, float]:
        """Actualiza los KPIs empresariales"""
        # ROI simplificado
        ingresos_estimados = sum(self.empresa.precios.values()) * 10  # Simplificado
        costos_estimados = sum(self.empresa.costos_unitarios.values()) * 10
        if costos_estimados > 0:
            self.kpis['roi'] = (ingresos_estimados - costos_estimados) / costos_estimados
        
        # Margen operativo
        if ingresos_estimados > 0:
            self.kpis['margen_operativo'] = (ingresos_estimados - costos_estimados) / ingresos_estimados
        
        # Satisfacción de empleados
        if self.gestion_rrhh.empleados:
            satisfacciones = [emp.satisfaccion for emp in self.gestion_rrhh.empleados.values()]
            self.kpis['satisfaccion_empleados'] = sum(satisfacciones) / len(satisfacciones)
        
        # Nivel de innovación
        proyectos_activos = len(self.gestion_innovacion.proyectos_activos)
        proyectos_completados = len(self.gestion_innovacion.proyectos_completados)
        self.kpis['nivel_innovacion'] = min(1.0, (proyectos_activos + proyectos_completados) / 10)
        
        # Reputación corporativa
        self.kpis['reputacion_corporativa'] = self.responsabilidad_social.reputacion_corporativa
        
        # Eficiencia operativa (basada en productividad de empleados)
        productividad = self.gestion_rrhh.calcular_productividad_total()
        self.kpis['eficiencia_operativa'] = min(1.0, productividad)
        
        return self.kpis.copy()
    
    def _generar_reporte_ejecutivo(self, resultados: Dict[str, Any]) -> List[str]:
        """Genera un reporte ejecutivo con los puntos clave"""
        reporte = []
        
        # Situación de RRHH
        rrhh = resultados['rrhh']
        reporte.append(f"Personal: {rrhh['empleados_actuales']} empleados, productividad {rrhh['productividad_total']:.2f}")
        
        # Situación de innovación
        innovacion = resultados['innovacion']
        if innovacion['proyectos_activos'] > 0:
            reporte.append(f"I+D: {innovacion['proyectos_activos']} proyectos activos, inversión ${innovacion['inversion_total_id']:,.0f}")
        
        # Situación de riesgos
        riesgos = resultados['riesgos']
        if riesgos['riesgos_activos'] > 0:
            reporte.append(f"Riesgos: {riesgos['riesgos_activos']} identificados, {riesgos['mitigaciones_implementadas']} mitigados")
        
        # Situación competitiva
        competencia = resultados['competencia']
        if competencia['amenazas_altas'] > 0:
            reporte.append(f"Competencia: {competencia['amenazas_altas']} amenazas significativas detectadas")
        
        # KPIs clave
        kpis = resultados['kpis']
        reporte.append(f"KPIs: ROI {kpis['roi']:.1%}, Margen {kpis['margen_operativo']:.1%}, Reputación {kpis['reputacion_corporativa']:.2f}")
        
        return reporte
    
    def obtener_estadisticas_completas(self) -> Dict[str, Any]:
        """Obtiene estadísticas completas del sistema de gestión"""
        return {
            'empleados': {
                'total': len(self.gestion_rrhh.empleados),
                'por_especializacion': self._contar_por_especializacion(),
                'productividad_promedio': self.gestion_rrhh.calcular_productividad_total(),
                'satisfaccion_promedio': self.kpis['satisfaccion_empleados']
            },
            'innovacion': {
                'proyectos_activos': len(self.gestion_innovacion.proyectos_activos),
                'proyectos_completados': len(self.gestion_innovacion.proyectos_completados),
                'inversion_total': sum(p.inversion_actual for p in self.gestion_innovacion.proyectos_activos.values())
            },
            'riesgos': {
                'riesgos_identificados': len(self.gestion_riesgos.riesgos_identificados),
                'riesgos_por_tipo': self._contar_riesgos_por_tipo()
            },
            'competencia': {
                'competidores_monitoreados': len(self.analisis_competencia.competidores),
                'amenazas_principales': [c.nombre for c in self.analisis_competencia.competidores.values() 
                                       if c.amenaza_nivel > 0.6]
            },
            'kpis': self.kpis.copy()
        }
    
    def _contar_por_especializacion(self) -> Dict[str, int]:
        """Cuenta empleados por especialización"""
        conteo = defaultdict(int)
        for empleado in self.gestion_rrhh.empleados.values():
            conteo[empleado.especializacion] += 1
        return dict(conteo)
    
    def _contar_riesgos_por_tipo(self) -> Dict[str, int]:
        """Cuenta riesgos por tipo"""
        conteo = defaultdict(int)
        for riesgo in self.gestion_riesgos.riesgos_identificados.values():
            conteo[riesgo.tipo] += 1
        return dict(conteo)
