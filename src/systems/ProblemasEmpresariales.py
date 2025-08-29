"""
Sistema de Problemas Empresariales Realistas
============================================

Simula problemas y desafíos comunes que enfrentan las empresas reales:
- Problemas de cadena de suministro
- Crisis de personal clave
- Problemas regulatorios
- Desafíos tecnológicos
- Crisis de liquidez
- Problemas de calidad
- Competencia desleal
"""

import random
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class ProblemaEmpresarial:
    """Problema empresarial específico"""
    id: str
    tipo: str
    descripcion: str
    severidad: str  # 'leve', 'moderado', 'severo', 'critico'
    impacto_financiero: float
    impacto_operacional: float
    impacto_reputacional: float
    duracion_estimada: int  # días
    probabilidad_escalamiento: float
    solucion_costo: float
    solucion_tiempo: int  # días
    requiere_atencion_inmediata: bool


class GeneradorProblemasEmpresariales:
    """Genera problemas empresariales realistas basados en el contexto de la empresa"""
    
    def __init__(self):
        self.tipos_problemas = {
            'cadena_suministro': {
                'probabilidad_base': 0.15,
                'factores_riesgo': ['tamaño_grande', 'sector_manufacturero', 'muchos_proveedores']
            },
            'personal_clave': {
                'probabilidad_base': 0.08,
                'factores_riesgo': ['pocos_empleados', 'alta_rotacion', 'baja_satisfaccion']
            },
            'regulatorio': {
                'probabilidad_base': 0.06,
                'factores_riesgo': ['sector_regulado', 'expansion_geografica', 'empresa_grande']
            },
            'tecnologico': {
                'probabilidad_base': 0.12,
                'factores_riesgo': ['dependencia_tecnologia', 'sistemas_antiguos', 'falta_id']
            },
            'liquidez': {
                'probabilidad_base': 0.10,
                'factores_riesgo': ['alto_apalancamiento', 'baja_liquidez', 'ventas_bajas']
            },
            'calidad': {
                'probabilidad_base': 0.09,
                'factores_riesgo': ['produccion_alta', 'costos_bajos', 'falta_controles']
            },
            'competencia_desleal': {
                'probabilidad_base': 0.07,
                'factores_riesgo': ['mercado_concentrado', 'competidores_agresivos', 'productos_comoditizados']
            },
            'ciberseguridad': {
                'probabilidad_base': 0.05,
                'factores_riesgo': ['dependencia_digital', 'datos_sensibles', 'falta_protocolos']
            },
            'ambiental': {
                'probabilidad_base': 0.04,
                'factores_riesgo': ['sector_contaminante', 'falta_certificaciones', 'presion_publica']
            },
            'financiero': {
                'probabilidad_base': 0.08,
                'factores_riesgo': ['alta_deuda', 'concentracion_clientes', 'volatilidad_ingresos']
            }
        }
    
    def evaluar_riesgos_empresa(self, empresa) -> Dict[str, float]:
        """Evalúa los riesgos específicos de una empresa"""
        riesgos = {}
        
        for tipo_problema, config in self.tipos_problemas.items():
            probabilidad = config['probabilidad_base']
            
            # Ajustar probabilidad basada en factores de riesgo
            factores_presentes = self._evaluar_factores_riesgo(empresa, config['factores_riesgo'])
            
            # Cada factor de riesgo presente aumenta la probabilidad
            probabilidad += factores_presentes * 0.03
            
            # Ajustar por contexto de mercado
            if hasattr(empresa, 'mercado') and hasattr(empresa.mercado, 'crisis_financiera_activa'):
                if empresa.mercado.crisis_financiera_activa:
                    probabilidad *= 1.5  # Crisis aumenta todos los riesgos
            
            riesgos[tipo_problema] = min(0.4, probabilidad)  # Máximo 40% probabilidad mensual
        
        return riesgos
    
    def _evaluar_factores_riesgo(self, empresa, factores_riesgo: List[str]) -> int:
        """Evalúa cuántos factores de riesgo están presentes"""
        factores_presentes = 0
        
        for factor in factores_riesgo:
            if self._verificar_factor_riesgo(empresa, factor):
                factores_presentes += 1
        
        return factores_presentes
    
    def _verificar_factor_riesgo(self, empresa, factor: str) -> bool:
        """Verifica si un factor de riesgo específico está presente"""
        if factor == 'tamaño_grande':
            return getattr(empresa, 'tamaño_empresa', 'pequeña') in ['mediana', 'grande']
        
        elif factor == 'sector_manufacturero':
            return getattr(empresa, 'sector_principal', 'servicios') in ['manufacturero', 'alimentos', 'textil']
        
        elif factor == 'muchos_proveedores':
            return len(getattr(empresa, 'proveedores_estrategicos', [])) > 5
        
        elif factor == 'pocos_empleados':
            return len(getattr(empresa, 'empleados', [])) < 10
        
        elif factor == 'alta_rotacion':
            if hasattr(empresa, 'gestion_avanzada'):
                return empresa.gestion_avanzada.gestion_rrhh.indicadores_clima['rotacion_mensual'] > 0.05
        
        elif factor == 'baja_satisfaccion':
            if hasattr(empresa, 'gestion_avanzada'):
                return empresa.gestion_avanzada.gestion_rrhh.indicadores_clima['satisfaccion_promedio'] < 0.6
        
        elif factor == 'sector_regulado':
            return getattr(empresa, 'sector_principal', 'servicios') in ['financiero', 'salud', 'energia']
        
        elif factor == 'expansion_geografica':
            return len(getattr(empresa, 'alianzas_comerciales', [])) > 3
        
        elif factor == 'empresa_grande':
            return getattr(empresa, 'tamaño_empresa', 'pequeña') == 'grande'
        
        elif factor == 'dependencia_tecnologia':
            return len(getattr(empresa, 'certificaciones', [])) > 0
        
        elif factor == 'sistemas_antiguos':
            return empresa.fundacion_año < 2015 if hasattr(empresa, 'fundacion_año') else False
        
        elif factor == 'falta_id':
            if hasattr(empresa, 'gestion_avanzada'):
                return len(empresa.gestion_avanzada.gestion_innovacion.proyectos_activos) == 0
        
        elif factor == 'alto_apalancamiento':
            return getattr(empresa, 'deuda_bancaria', 0) > empresa.dinero
        
        elif factor == 'baja_liquidez':
            costos_mensuales = getattr(empresa, 'costos_fijos_mensuales', 1000)
            return empresa.dinero < costos_mensuales * 3
        
        elif factor == 'ventas_bajas':
            return len(getattr(empresa, 'bienes', {})) < 3
        
        elif factor == 'produccion_alta':
            if hasattr(empresa, 'capacidad_produccion'):
                return sum(empresa.capacidad_produccion.values()) > 100
        
        elif factor == 'costos_bajos':
            if hasattr(empresa, 'costos_unitarios'):
                return sum(empresa.costos_unitarios.values()) / len(empresa.costos_unitarios) < 15
        
        elif factor == 'falta_controles':
            return len(getattr(empresa, 'certificaciones', [])) == 0
        
        elif factor == 'mercado_concentrado':
            if hasattr(empresa, 'gestion_avanzada'):
                return len(empresa.gestion_avanzada.analisis_competencia.competidores) > 5
        
        elif factor == 'competidores_agresivos':
            if hasattr(empresa, 'gestion_avanzada'):
                return any(comp.amenaza_nivel > 0.7 for comp in empresa.gestion_avanzada.analisis_competencia.competidores.values())
        
        elif factor == 'productos_comoditizados':
            return len(getattr(empresa, 'bienes', {})) > 5
        
        # Factores adicionales con lógica simplificada
        elif factor in ['dependencia_digital', 'datos_sensibles', 'falta_protocolos', 
                       'sector_contaminante', 'falta_certificaciones', 'presion_publica',
                       'alta_deuda', 'concentracion_clientes', 'volatilidad_ingresos']:
            return random.random() < 0.3  # 30% probabilidad para factores complejos
        
        return False
    
    def generar_problema(self, empresa, tipo_problema: str) -> ProblemaEmpresarial:
        """Genera un problema específico para una empresa"""
        generadores = {
            'cadena_suministro': self._generar_problema_cadena_suministro,
            'personal_clave': self._generar_problema_personal_clave,
            'regulatorio': self._generar_problema_regulatorio,
            'tecnologico': self._generar_problema_tecnologico,
            'liquidez': self._generar_problema_liquidez,
            'calidad': self._generar_problema_calidad,
            'competencia_desleal': self._generar_problema_competencia_desleal,
            'ciberseguridad': self._generar_problema_ciberseguridad,
            'ambiental': self._generar_problema_ambiental,
            'financiero': self._generar_problema_financiero
        }
        
        if tipo_problema in generadores:
            return generadores[tipo_problema](empresa)
        else:
            return self._generar_problema_generico(empresa)
    
    def _generar_problema_cadena_suministro(self, empresa) -> ProblemaEmpresarial:
        """Genera problema de cadena de suministro"""
        problemas_cadena = [
            {
                'descripcion': 'Retraso en entrega de materias primas críticas',
                'severidad': 'moderado',
                'impacto_operacional': 0.3,
                'duracion': random.randint(7, 21),
                'solucion_tiempo': random.randint(3, 10)
            },
            {
                'descripcion': 'Aumento súbito en precios de proveedores principales',
                'severidad': 'severo',
                'impacto_operacional': 0.2,
                'duracion': random.randint(30, 90),
                'solucion_tiempo': random.randint(14, 30)
            },
            {
                'descripcion': 'Proveedor clave declara bancarrota',
                'severidad': 'critico',
                'impacto_operacional': 0.5,
                'duracion': random.randint(14, 45),
                'solucion_tiempo': random.randint(7, 21)
            },
            {
                'descripcion': 'Problemas de calidad en componentes recibidos',
                'severidad': 'moderado',
                'impacto_operacional': 0.25,
                'duracion': random.randint(5, 15),
                'solucion_tiempo': random.randint(2, 7)
            }
        ]
        
        problema_data = random.choice(problemas_cadena)
        
        return ProblemaEmpresarial(
            id=f"cadena_{random.randint(1000, 9999)}",
            tipo='cadena_suministro',
            descripcion=problema_data['descripcion'],
            severidad=problema_data['severidad'],
            impacto_financiero=empresa.dinero * random.uniform(0.05, 0.15),
            impacto_operacional=problema_data['impacto_operacional'],
            impacto_reputacional=random.uniform(0.05, 0.15),
            duracion_estimada=problema_data['duracion'],
            probabilidad_escalamiento=0.3 if problema_data['severidad'] != 'critico' else 0.1,
            solucion_costo=empresa.dinero * random.uniform(0.02, 0.08),
            solucion_tiempo=problema_data['solucion_tiempo'],
            requiere_atencion_inmediata=problema_data['severidad'] in ['severo', 'critico']
        )
    
    def _generar_problema_personal_clave(self, empresa) -> ProblemaEmpresarial:
        """Genera problema de personal clave"""
        problemas_personal = [
            {
                'descripcion': 'Renuncia inesperada de gerente de producción',
                'severidad': 'severo',
                'impacto_operacional': 0.4,
                'duracion': random.randint(30, 60),
                'solucion_tiempo': random.randint(15, 45)
            },
            {
                'descripcion': 'Conflicto laboral por condiciones de trabajo',
                'severidad': 'moderado',
                'impacto_operacional': 0.2,
                'duracion': random.randint(7, 21),
                'solucion_tiempo': random.randint(3, 14)
            },
            {
                'descripcion': 'Huelga del sindicato por aumento salarial',
                'severidad': 'severo',
                'impacto_operacional': 0.6,
                'duracion': random.randint(3, 14),
                'solucion_tiempo': random.randint(1, 7)
            },
            {
                'descripcion': 'Alta rotación de personal especializado',
                'severidad': 'moderado',
                'impacto_operacional': 0.3,
                'duracion': random.randint(60, 120),
                'solucion_tiempo': random.randint(30, 60)
            }
        ]
        
        problema_data = random.choice(problemas_personal)
        
        return ProblemaEmpresarial(
            id=f"personal_{random.randint(1000, 9999)}",
            tipo='personal_clave',
            descripcion=problema_data['descripcion'],
            severidad=problema_data['severidad'],
            impacto_financiero=empresa.dinero * random.uniform(0.03, 0.12),
            impacto_operacional=problema_data['impacto_operacional'],
            impacto_reputacional=random.uniform(0.1, 0.25),
            duracion_estimada=problema_data['duracion'],
            probabilidad_escalamiento=0.4,
            solucion_costo=empresa.dinero * random.uniform(0.05, 0.15),
            solucion_tiempo=problema_data['solucion_tiempo'],
            requiere_atencion_inmediata=problema_data['severidad'] == 'severo'
        )
    
    def _generar_problema_tecnologico(self, empresa) -> ProblemaEmpresarial:
        """Genera problema tecnológico"""
        problemas_tech = [
            {
                'descripcion': 'Falla crítica en sistema de producción',
                'severidad': 'critico',
                'impacto_operacional': 0.8,
                'duracion': random.randint(1, 5),
                'solucion_tiempo': random.randint(1, 3)
            },
            {
                'descripcion': 'Software empresarial obsoleto causa ineficiencias',
                'severidad': 'moderado',
                'impacto_operacional': 0.15,
                'duracion': random.randint(90, 180),
                'solucion_tiempo': random.randint(30, 90)
            },
            {
                'descripcion': 'Pérdida de datos por falta de respaldos',
                'severidad': 'severo',
                'impacto_operacional': 0.3,
                'duracion': random.randint(7, 21),
                'solucion_tiempo': random.randint(7, 14)
            },
            {
                'descripcion': 'Equipos de producción requieren mantenimiento urgente',
                'severidad': 'moderado',
                'impacto_operacional': 0.25,
                'duracion': random.randint(3, 10),
                'solucion_tiempo': random.randint(2, 7)
            }
        ]
        
        problema_data = random.choice(problemas_tech)
        
        return ProblemaEmpresarial(
            id=f"tech_{random.randint(1000, 9999)}",
            tipo='tecnologico',
            descripcion=problema_data['descripcion'],
            severidad=problema_data['severidad'],
            impacto_financiero=empresa.dinero * random.uniform(0.02, 0.10),
            impacto_operacional=problema_data['impacto_operacional'],
            impacto_reputacional=random.uniform(0.02, 0.08),
            duracion_estimada=problema_data['duracion'],
            probabilidad_escalamiento=0.25,
            solucion_costo=empresa.dinero * random.uniform(0.03, 0.12),
            solucion_tiempo=problema_data['solucion_tiempo'],
            requiere_atencion_inmediata=problema_data['severidad'] == 'critico'
        )
    
    def _generar_problema_liquidez(self, empresa) -> ProblemaEmpresarial:
        """Genera problema de liquidez"""
        problemas_liquidez = [
            {
                'descripcion': 'Cliente principal retrasa pago de facturas',
                'severidad': 'severo',
                'impacto_financiero': 0.15,
                'duracion': random.randint(30, 90)
            },
            {
                'descripcion': 'Banco reduce línea de crédito empresarial',
                'severidad': 'severo',
                'impacto_financiero': 0.12,
                'duracion': random.randint(60, 180)
            },
            {
                'descripcion': 'Gastos inesperados por reparaciones de emergencia',
                'severidad': 'moderado',
                'impacto_financiero': 0.08,
                'duracion': random.randint(1, 7)
            },
            {
                'descripcion': 'Disminución estacional de ventas',
                'severidad': 'leve',
                'impacto_financiero': 0.06,
                'duracion': random.randint(60, 120)
            }
        ]
        
        problema_data = random.choice(problemas_liquidez)
        
        return ProblemaEmpresarial(
            id=f"liquidez_{random.randint(1000, 9999)}",
            tipo='liquidez',
            descripcion=problema_data['descripcion'],
            severidad=problema_data['severidad'],
            impacto_financiero=empresa.dinero * problema_data['impacto_financiero'],
            impacto_operacional=random.uniform(0.1, 0.3),
            impacto_reputacional=random.uniform(0.05, 0.15),
            duracion_estimada=problema_data['duracion'],
            probabilidad_escalamiento=0.35,
            solucion_costo=empresa.dinero * random.uniform(0.01, 0.05),
            solucion_tiempo=random.randint(7, 30),
            requiere_atencion_inmediata=problema_data['severidad'] == 'severo'
        )
    
    def _generar_problema_calidad(self, empresa) -> ProblemaEmpresarial:
        """Genera problema de calidad"""
        problemas_calidad = [
            {
                'descripcion': 'Lote de productos defectuosos detectado por clientes',
                'severidad': 'severo',
                'impacto_reputacional': 0.3,
                'duracion': random.randint(14, 45)
            },
            {
                'descripcion': 'Fallas en proceso de control de calidad',
                'severidad': 'moderado',
                'impacto_reputacional': 0.15,
                'duracion': random.randint(7, 21)
            },
            {
                'descripcion': 'Queja formal de cliente corporativo por calidad',
                'severidad': 'moderado',
                'impacto_reputacional': 0.2,
                'duracion': random.randint(21, 60)
            },
            {
                'descripcion': 'Certificación de calidad ISO en riesgo',
                'severidad': 'severo',
                'impacto_reputacional': 0.25,
                'duracion': random.randint(30, 90)
            }
        ]
        
        problema_data = random.choice(problemas_calidad)
        
        return ProblemaEmpresarial(
            id=f"calidad_{random.randint(1000, 9999)}",
            tipo='calidad',
            descripcion=problema_data['descripcion'],
            severidad=problema_data['severidad'],
            impacto_financiero=empresa.dinero * random.uniform(0.04, 0.12),
            impacto_operacional=random.uniform(0.15, 0.35),
            impacto_reputacional=problema_data['impacto_reputacional'],
            duracion_estimada=problema_data['duracion'],
            probabilidad_escalamiento=0.4,
            solucion_costo=empresa.dinero * random.uniform(0.02, 0.08),
            solucion_tiempo=random.randint(7, 30),
            requiere_atencion_inmediata=problema_data['severidad'] == 'severo'
        )
    
    def _generar_problema_competencia_desleal(self, empresa) -> ProblemaEmpresarial:
        """Genera problema de competencia desleal"""
        return ProblemaEmpresarial(
            id=f"competencia_{random.randint(1000, 9999)}",
            tipo='competencia_desleal',
            descripcion='Competidor principal reduce precios agresivamente',
            severidad='moderado',
            impacto_financiero=empresa.dinero * random.uniform(0.05, 0.15),
            impacto_operacional=random.uniform(0.1, 0.25),
            impacto_reputacional=random.uniform(0.02, 0.08),
            duracion_estimada=random.randint(30, 90),
            probabilidad_escalamiento=0.3,
            solucion_costo=empresa.dinero * random.uniform(0.03, 0.10),
            solucion_tiempo=random.randint(14, 60),
            requiere_atencion_inmediata=False
        )
    
    def _generar_problema_ciberseguridad(self, empresa) -> ProblemaEmpresarial:
        """Genera problema de ciberseguridad"""
        return ProblemaEmpresarial(
            id=f"ciber_{random.randint(1000, 9999)}",
            tipo='ciberseguridad',
            descripcion='Intento de acceso no autorizado a sistemas',
            severidad='severo',
            impacto_financiero=empresa.dinero * random.uniform(0.02, 0.08),
            impacto_operacional=random.uniform(0.15, 0.4),
            impacto_reputacional=random.uniform(0.1, 0.3),
            duracion_estimada=random.randint(1, 7),
            probabilidad_escalamiento=0.5,
            solucion_costo=empresa.dinero * random.uniform(0.05, 0.12),
            solucion_tiempo=random.randint(3, 14),
            requiere_atencion_inmediata=True
        )
    
    def _generar_problema_ambiental(self, empresa) -> ProblemaEmpresarial:
        """Genera problema ambiental"""
        return ProblemaEmpresarial(
            id=f"ambiental_{random.randint(1000, 9999)}",
            tipo='ambiental',
            descripcion='Presión regulatoria por impacto ambiental',
            severidad='moderado',
            impacto_financiero=empresa.dinero * random.uniform(0.03, 0.10),
            impacto_operacional=random.uniform(0.05, 0.20),
            impacto_reputacional=random.uniform(0.15, 0.35),
            duracion_estimada=random.randint(60, 180),
            probabilidad_escalamiento=0.25,
            solucion_costo=empresa.dinero * random.uniform(0.08, 0.20),
            solucion_tiempo=random.randint(30, 120),
            requiere_atencion_inmediata=False
        )
    
    def _generar_problema_financiero(self, empresa) -> ProblemaEmpresarial:
        """Genera problema financiero"""
        return ProblemaEmpresarial(
            id=f"financiero_{random.randint(1000, 9999)}",
            tipo='financiero',
            descripcion='Deterioro en calificación crediticia',
            severidad='severo',
            impacto_financiero=empresa.dinero * random.uniform(0.08, 0.20),
            impacto_operacional=random.uniform(0.1, 0.25),
            impacto_reputacional=random.uniform(0.1, 0.25),
            duracion_estimada=random.randint(90, 180),
            probabilidad_escalamiento=0.3,
            solucion_costo=empresa.dinero * random.uniform(0.02, 0.06),
            solucion_tiempo=random.randint(30, 90),
            requiere_atencion_inmediata=True
        )
    
    def _generar_problema_regulatorio(self, empresa) -> ProblemaEmpresarial:
        """Genera problema regulatorio"""
        return ProblemaEmpresarial(
            id=f"regulatorio_{random.randint(1000, 9999)}",
            tipo='regulatorio',
            descripcion='Cambio en regulación sectorial requiere adaptación',
            severidad='moderado',
            impacto_financiero=empresa.dinero * random.uniform(0.05, 0.15),
            impacto_operacional=random.uniform(0.2, 0.4),
            impacto_reputacional=random.uniform(0.05, 0.15),
            duracion_estimada=random.randint(90, 180),
            probabilidad_escalamiento=0.2,
            solucion_costo=empresa.dinero * random.uniform(0.06, 0.15),
            solucion_tiempo=random.randint(45, 120),
            requiere_atencion_inmediata=False
        )
    
    def _generar_problema_generico(self, empresa) -> ProblemaEmpresarial:
        """Genera problema genérico"""
        return ProblemaEmpresarial(
            id=f"generico_{random.randint(1000, 9999)}",
            tipo='operacional',
            descripcion='Problema operacional general',
            severidad='leve',
            impacto_financiero=empresa.dinero * random.uniform(0.01, 0.05),
            impacto_operacional=random.uniform(0.05, 0.15),
            impacto_reputacional=random.uniform(0.01, 0.05),
            duracion_estimada=random.randint(7, 21),
            probabilidad_escalamiento=0.2,
            solucion_costo=empresa.dinero * random.uniform(0.01, 0.03),
            solucion_tiempo=random.randint(3, 14),
            requiere_atencion_inmediata=False
        )


class GestorProblemasEmpresariales:
    """Gestiona los problemas empresariales activos de una empresa"""
    
    def __init__(self, empresa):
        self.empresa = empresa
        self.problemas_activos: Dict[str, ProblemaEmpresarial] = {}
        self.problemas_resueltos: List[ProblemaEmpresarial] = []
        self.generador = GeneradorProblemasEmpresariales()
        
        # Configuración de gestión
        self.revision_frecuencia = 1  # Revisar cada ciclo
        self.limite_problemas_activos = 5
        self.presupuesto_emergencia = 0.05  # 5% del capital para emergencias
    
    def evaluar_nuevos_problemas(self) -> List[ProblemaEmpresarial]:
        """Evalúa y genera nuevos problemas si corresponde"""
        if len(self.problemas_activos) >= self.limite_problemas_activos:
            return []
        
        nuevos_problemas = []
        riesgos = self.generador.evaluar_riesgos_empresa(self.empresa)
        
        for tipo_problema, probabilidad in riesgos.items():
            if random.random() < probabilidad * 0.1:  # 10% de la probabilidad mensual
                problema = self.generador.generar_problema(self.empresa, tipo_problema)
                nuevos_problemas.append(problema)
                self.problemas_activos[problema.id] = problema
                
                logging.warning(f"{self.empresa.nombre}: Nuevo problema {tipo_problema} - {problema.descripcion}")
                
                # Solo uno o dos problemas nuevos por ciclo
                if len(nuevos_problemas) >= 2:
                    break
        
        return nuevos_problemas
    
    def gestionar_problemas_activos(self) -> Dict[str, Any]:
        """Gestiona todos los problemas activos"""
        resultados = {
            'problemas_resueltos': 0,
            'problemas_escalados': 0,
            'costo_total_gestion': 0,
            'impacto_total': {
                'financiero': 0,
                'operacional': 0,
                'reputacional': 0
            }
        }
        
        for problema_id, problema in list(self.problemas_activos.items()):
            resultado_problema = self._gestionar_problema_individual(problema)
            
            if resultado_problema['resuelto']:
                resultados['problemas_resueltos'] += 1
                self.problemas_resueltos.append(problema)
                del self.problemas_activos[problema_id]
            
            elif resultado_problema['escalado']:
                resultados['problemas_escalados'] += 1
                self._escalar_problema(problema)
            
            # Acumular costos e impactos
            resultados['costo_total_gestion'] += resultado_problema['costo']
            
            for tipo_impacto in resultados['impacto_total']:
                resultados['impacto_total'][tipo_impacto] += resultado_problema['impacto'][tipo_impacto]
        
        return resultados
    
    def _gestionar_problema_individual(self, problema: ProblemaEmpresarial) -> Dict[str, Any]:
        """Gestiona un problema individual"""
        resultado = {
            'resuelto': False,
            'escalado': False,
            'costo': 0,
            'impacto': {
                'financiero': 0,
                'operacional': 0,
                'reputacional': 0
            }
        }
        
        # Aplicar impacto del problema
        resultado['impacto']['financiero'] = problema.impacto_financiero * 0.1  # 10% mensual
        resultado['impacto']['operacional'] = problema.impacto_operacional
        resultado['impacto']['reputacional'] = problema.impacto_reputacional * 0.1
        
        # Aplicar impacto financiero
        self.empresa.dinero -= resultado['impacto']['financiero']
        
        # Aplicar impacto operacional
        if hasattr(self.empresa, 'eficiencia_produccion'):
            self.empresa.eficiencia_produccion *= (1 - resultado['impacto']['operacional'] * 0.1)
        
        # Aplicar impacto reputacional
        if hasattr(self.empresa, 'gestion_avanzada'):
            reputacion_actual = self.empresa.gestion_avanzada.responsabilidad_social.reputacion_corporativa
            nueva_reputacion = reputacion_actual - resultado['impacto']['reputacional']
            self.empresa.gestion_avanzada.responsabilidad_social.reputacion_corporativa = max(0, nueva_reputacion)
        
        # Decidir si resolver el problema
        if self._evaluar_resolucion_problema(problema):
            resultado['resuelto'] = True
            resultado['costo'] = problema.solucion_costo
            self.empresa.dinero -= problema.solucion_costo
            
            logging.info(f"{self.empresa.nombre}: Resuelto problema {problema.tipo} - Costo: ${problema.solucion_costo:,.0f}")
        
        # Evaluar escalamiento
        elif random.random() < problema.probabilidad_escalamiento * 0.1:
            resultado['escalado'] = True
        
        return resultado
    
    def _evaluar_resolucion_problema(self, problema: ProblemaEmpresarial) -> bool:
        """Evalúa si resolver un problema específico"""
        # Problemas críticos siempre se resuelven si hay recursos
        if problema.severidad == 'critico' and problema.solucion_costo <= self.empresa.dinero:
            return True
        
        # Evaluar costo-beneficio
        costo_no_resolver = (problema.impacto_financiero + 
                           problema.impacto_operacional * self.empresa.dinero * 0.1 +
                           problema.impacto_reputacional * self.empresa.dinero * 0.05)
        
        if problema.solucion_costo < costo_no_resolver and problema.solucion_costo <= self.empresa.dinero * 0.1:
            return True
        
        # Presupuesto de emergencia
        presupuesto_emergencia = self.empresa.dinero * self.presupuesto_emergencia
        if problema.requiere_atencion_inmediata and problema.solucion_costo <= presupuesto_emergencia:
            return True
        
        return False
    
    def _escalar_problema(self, problema: ProblemaEmpresarial):
        """Escala un problema a mayor severidad"""
        escalamiento = {
            'leve': 'moderado',
            'moderado': 'severo',
            'severo': 'critico'
        }
        
        if problema.severidad in escalamiento:
            problema.severidad = escalamiento[problema.severidad]
            problema.impacto_financiero *= 1.5
            problema.impacto_operacional *= 1.3
            problema.impacto_reputacional *= 1.4
            problema.solucion_costo *= 1.2
            problema.requiere_atencion_inmediata = True
            
            logging.warning(f"{self.empresa.nombre}: Problema {problema.tipo} escaló a {problema.severidad}")
    
    def generar_reporte_problemas(self) -> Dict[str, Any]:
        """Genera un reporte de todos los problemas"""
        problemas_por_tipo = {}
        for problema in self.problemas_activos.values():
            if problema.tipo not in problemas_por_tipo:
                problemas_por_tipo[problema.tipo] = []
            problemas_por_tipo[problema.tipo].append(problema.severidad)
        
        problemas_criticos = [p for p in self.problemas_activos.values() if p.severidad == 'critico']
        costo_resolucion_total = sum(p.solucion_costo for p in self.problemas_activos.values())
        
        return {
            'problemas_activos': len(self.problemas_activos),
            'problemas_por_tipo': problemas_por_tipo,
            'problemas_criticos': len(problemas_criticos),
            'problemas_resueltos_historicos': len(self.problemas_resueltos),
            'costo_resolucion_estimado': costo_resolucion_total,
            'requieren_atencion_inmediata': sum(1 for p in self.problemas_activos.values() 
                                              if p.requiere_atencion_inmediata),
            'problema_mas_critico': max(self.problemas_activos.values(), 
                                      key=lambda x: x.impacto_financiero).descripcion if self.problemas_activos else None
        }
    
    def obtener_recomendaciones_gestion(self) -> List[str]:
        """Obtiene recomendaciones para gestión de problemas"""
        recomendaciones = []
        
        # Recomendaciones basadas en problemas activos
        if len(self.problemas_activos) > 3:
            recomendaciones.append("Considerar contratar consultor externo para gestión de crisis")
        
        problemas_criticos = [p for p in self.problemas_activos.values() if p.severidad == 'critico']
        if problemas_criticos:
            recomendaciones.append("URGENTE: Resolver problemas críticos inmediatamente")
        
        costo_total = sum(p.solucion_costo for p in self.problemas_activos.values())
        if costo_total > self.empresa.dinero * 0.2:
            recomendaciones.append("Buscar financiamiento adicional para resolver problemas")
        
        # Recomendaciones preventivas
        tipos_frecuentes = {}
        for problema in self.problemas_resueltos + list(self.problemas_activos.values()):
            tipos_frecuentes[problema.tipo] = tipos_frecuentes.get(problema.tipo, 0) + 1
        
        if tipos_frecuentes:
            tipo_mas_frecuente = max(tipos_frecuentes, key=tipos_frecuentes.get)
            if tipos_frecuentes[tipo_mas_frecuente] > 2:
                recomendaciones.append(f"Implementar medidas preventivas para problemas de {tipo_mas_frecuente}")
        
        return recomendaciones
