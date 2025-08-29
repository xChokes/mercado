"""
Empresa Productora Hiperrealista
================================

Extensión de la EmpresaProductora que integra automáticamente todas las
características hiperrealistas para mayor realismo empresarial.
"""

import random
import logging
from typing import Dict, List, Any, Optional
from .EmpresaProductora import EmpresaProductora
from ..ai.EmpresaIA import EmpresaIA
from ..config.ConfigEconomica import ConfigEconomica


class EmpresaProductoraHiperrealista(EmpresaProductora):
    """
    Empresa Productora con características hiperrealistas integradas
    """
    
    def __init__(self, nombre, mercado, bienes={}):
        super().__init__(nombre, mercado, bienes)
        
        # Características hiperrealistas básicas
        self.nivel_tecnologico = random.uniform(0.6, 0.95)
        self.reputacion_mercado = random.uniform(0.5, 0.8)
        self.experiencia_sectorial = random.uniform(0.3, 0.8)
        
        # Gestión de stakeholders
        self.satisfaccion_accionistas = random.uniform(0.6, 0.9)
        self.relaciones_gobierno = random.uniform(0.4, 0.7)
        self.responsabilidad_social = random.uniform(0.3, 0.7)
        
        # Sistemas de gestión avanzada
        self.gestion_calidad = SistemaGestionCalidad(self)
        self.gestion_riesgos_operativos = SistemaRiesgosOperativos(self)
        self.gestion_marca = SistemaGestionMarca(self)
        self.analisis_competitivo = SistemaAnalisisCompetitivo(self, mercado)
        
        # Métricas de rendimiento empresarial
        self.roi_historico = []
        self.margen_bruto_historico = []
        self.rotacion_inventario = 0.8
        self.ciclo_conversion_efectivo = 30  # días
        
        # Planificación estratégica
        self.vision_empresa = self._generar_vision_empresa()
        self.objetivos_estrategicos = self._definir_objetivos_estrategicos()
        self.horizonte_planificacion = random.randint(12, 36)  # meses
        
        # Crisis y contingencias
        self.plan_contingencia = PlanContingencia(self)
        self.reservas_emergencia = self.dinero * random.uniform(0.05, 0.15)
        self.seguros_contratados = self._contratar_seguros_basicos()
        
        # Innovación y desarrollo
        self.centro_innovacion = CentroInnovacionEmpresarial(self)
        self.alianzas_tecnologicas = []
        self.patentes_registradas = []
        
        # Responsabilidad corporativa
        self.programa_sostenibilidad = ProgramaSostenibilidad(self)
        self.certificaciones_obtenidas = []
        self.inversion_comunidad = 0
        
        # Inteligencia empresarial integrada
        if random.random() < 0.7:  # 70% de empresas tendrán IA
            self.sistema_ia = EmpresaIA(nombre + "_IA", mercado, bienes)
            self.ia_habilitada = True
        else:
            self.sistema_ia = None
            self.ia_habilitada = False
        
        logging.info(f"Empresa hiperrealista {nombre} inicializada con nivel tecnológico {self.nivel_tecnologico:.2f}")
    
    def _generar_vision_empresa(self) -> str:
        """Genera visión empresarial basada en características"""
        visiones_base = [
            "Liderar el mercado con productos innovadores y sostenibles",
            "Ser la empresa preferida por clientes y empleados",
            "Transformar la industria mediante tecnología avanzada",
            "Crear valor a largo plazo para todos los stakeholders",
            "Ser reconocidos por excelencia operacional y calidad"
        ]
        
        return random.choice(visiones_base)
    
    def _definir_objetivos_estrategicos(self) -> List[Dict]:
        """Define objetivos estratégicos específicos"""
        objetivos = []
        
        # Objetivo financiero
        crecimiento_objetivo = random.uniform(0.1, 0.3)
        objetivos.append({
            'tipo': 'financiero',
            'descripcion': f'Crecer {crecimiento_objetivo:.1%} anualmente',
            'metrica': 'crecimiento_ingresos',
            'objetivo': crecimiento_objetivo,
            'plazo': 12
        })
        
        # Objetivo operacional
        eficiencia_objetivo = random.uniform(0.85, 0.95)
        objetivos.append({
            'tipo': 'operacional',
            'descripcion': f'Alcanzar {eficiencia_objetivo:.1%} de eficiencia',
            'metrica': 'eficiencia_produccion',
            'objetivo': eficiencia_objetivo,
            'plazo': 6
        })
        
        # Objetivo de mercado
        if random.random() < 0.8:
            market_share_objetivo = random.uniform(0.15, 0.4)
            objetivos.append({
                'tipo': 'mercado',
                'descripcion': f'Capturar {market_share_objetivo:.1%} del mercado',
                'metrica': 'market_share',
                'objetivo': market_share_objetivo,
                'plazo': 18
            })
        
        return objetivos
    
    def _contratar_seguros_basicos(self) -> List[str]:
        """Contrata seguros empresariales básicos"""
        seguros = []
        
        # Seguro obligatorio
        seguros.append('responsabilidad_civil')
        
        # Seguros opcionales según capacidad financiera
        if self.dinero > 50000:
            seguros.append('incendio_robo')
        
        if len(self.empleados) > 10:
            seguros.append('accidentes_trabajo')
        
        if random.random() < 0.6:
            seguros.append('seguro_credito')
        
        return seguros
    
    def ciclo_empresa_hiperrealista(self):
        """Ciclo principal con características hiperrealistas"""
        try:
            # 0. Limpiar productos inválidos antes de cualquier procesamiento
            self._limpiar_productos_invalidos()
            
            # 1. Evaluación estratégica
            self._evaluar_cumplimiento_objetivos()
            
            # 2. Gestión de calidad y procesos
            self.gestion_calidad.ciclo_calidad()
            
            # 3. Gestión de riesgos operativos
            self.gestion_riesgos_operativos.evaluar_riesgos()
            
            # 4. Gestión de marca y reputación
            self.gestion_marca.gestionar_reputacion()
            
            # 5. Análisis competitivo continuo
            self.analisis_competitivo.actualizar_analisis()
            
            # 6. Innovación empresarial
            self.centro_innovacion.ciclo_innovacion()
            
            # 7. Sostenibilidad corporativa
            self.programa_sostenibilidad.ciclo_sostenibilidad()
            
            # 8. Planificación táctica
            self._planificacion_tactica()
            
            # 9. IA empresarial si está habilitada
            if self.ia_habilitada and self.sistema_ia:
                self.sistema_ia.procesar_ciclo_empresarial_ia()
            
            # 10. Actualizar métricas de rendimiento
            self._actualizar_metricas_rendimiento()
            
        except Exception as e:
            logging.error(f"Error en ciclo hiperrealista de {self.nombre}: {e}")
    
    def _evaluar_cumplimiento_objetivos(self):
        """Evalúa el cumplimiento de objetivos estratégicos"""
        for objetivo in self.objetivos_estrategicos:
            progreso = self._medir_progreso_objetivo(objetivo)
            objetivo['progreso_actual'] = progreso
            
            # Ajustar estrategia si el progreso es bajo
            if progreso < 0.3 and objetivo['plazo'] <= 6:
                self._ajustar_estrategia_objetivo(objetivo)
    
    def _medir_progreso_objetivo(self, objetivo: Dict) -> float:
        """Mide el progreso hacia un objetivo específico"""
        if objetivo['metrica'] == 'crecimiento_ingresos':
            # Aproximar crecimiento basado en dinero actual vs inicial
            if hasattr(self, 'dinero_inicial'):
                crecimiento_actual = (self.dinero - self.dinero_inicial) / max(self.dinero_inicial, 1)
                return min(1.0, crecimiento_actual / objetivo['objetivo'])
            return 0.5  # Progreso neutro
        
        elif objetivo['metrica'] == 'eficiencia_produccion':
            eficiencia_actual = getattr(self, 'eficiencia_produccion', 0.8)
            return eficiencia_actual / objetivo['objetivo']
        
        elif objetivo['metrica'] == 'market_share':
            # Aproximar market share basado en volumen de ventas
            return random.uniform(0.3, 0.8)  # Simulado
        
        return 0.5
    
    def _ajustar_estrategia_objetivo(self, objetivo: Dict):
        """Ajusta estrategia para objetivos con bajo rendimiento"""
        if objetivo['tipo'] == 'financiero':
            # Aumentar margen de precios para mejorar ingresos
            for bien in self.precios:
                self.precios[bien] *= 1.05
        
        elif objetivo['tipo'] == 'operacional':
            # Invertir en mejoras de eficiencia
            if self.dinero > 10000:
                inversion_eficiencia = min(self.dinero * 0.1, 15000)
                self.dinero -= inversion_eficiencia
                self.eficiencia_produccion = min(1.0, self.eficiencia_produccion * 1.1)
        
        elif objetivo['tipo'] == 'mercado':
            # Estrategia más agresiva de precios
            for bien in self.precios:
                costo = self.costos_unitarios.get(bien, 10)
                precio_competitivo = costo * 1.15  # Margen reducido
                self.precios[bien] = min(self.precios[bien], precio_competitivo)
    
    def _planificacion_tactica(self):
        """Realiza planificación táctica a corto plazo"""
        # Ajustar niveles de inventario basándose en análisis de demanda
        self._optimizar_inventario_tactico()
        
        # Revisar estructura de costos
        self._optimizar_estructura_costos()
        
        # Evaluar oportunidades de expansion
        self._evaluar_expansion_tactica()
    
    def _optimizar_inventario_tactico(self):
        """Optimiza inventario desde perspectiva táctica"""
        for bien, inventario in self.bienes.items():
            if isinstance(inventario, list):
                stock_actual = len(inventario)
                demanda_esperada = self.analisis_competitivo.proyectar_demanda(bien)
                
                # Determinar inventario óptimo (1.2x demanda esperada)
                inventario_optimo = int(demanda_esperada * 1.2)
                
                if stock_actual > inventario_optimo * 2:
                    # Exceso de inventario: promociones especiales
                    self._activar_promocion_liquidacion(bien)
                elif stock_actual < inventario_optimo * 0.5:
                    # Falta de inventario: aumentar producción
                    self._aumentar_produccion_urgente(bien)
    
    def _activar_promocion_liquidacion(self, bien: str):
        """Activa promoción para liquidar exceso de inventario"""
        descuento = random.uniform(0.1, 0.25)  # 10-25% descuento
        precio_original = self.precios.get(bien, 50)
        precio_promocional = precio_original * (1 - descuento)
        
        # Aplicar precio promocional temporalmente
        self.precios[bien] = max(precio_promocional, self.costos_unitarios.get(bien, 1) * 1.05)
        
        logging.info(f"{self.nombre}: Promoción de liquidación en {bien} - {descuento:.1%} descuento")
    
    def _aumentar_produccion_urgente(self, bien: str):
        """Aumenta producción urgente para bien con faltante"""
        if hasattr(self, 'capacidad_produccion') and bien in self.capacidad_produccion:
            # Trabajar horas extra (costo adicional)
            capacidad_adicional = int(self.capacidad_produccion[bien] * 0.3)
            costo_horas_extra = capacidad_adicional * self.costos_unitarios.get(bien, 10) * 1.2
            
            if self.dinero > costo_horas_extra:
                # Producir unidades adicionales
                for _ in range(capacidad_adicional):
                    resultado = self.producir_bien_mejorado(bien, 1, self.mercado)
                    if resultado == 0:  # No se pudo producir
                        break
    
    def _optimizar_estructura_costos(self):
        """Optimiza estructura de costos operativos"""
        # Revisar costos fijos
        if hasattr(self, 'costos_fijos_mensuales'):
            # Buscar oportunidades de reducción
            if random.random() < 0.1:  # 10% probabilidad de encontrar ahorro
                ahorro = random.uniform(0.02, 0.08)  # 2-8% ahorro
                self.costos_fijos_mensuales *= (1 - ahorro)
                logging.info(f"{self.nombre}: Optimización de costos fijos - {ahorro:.1%} reducción")
        
        # Revisar costos variables por economías de escala
        for bien in self.costos_unitarios:
            volumen_produccion = getattr(self, 'produccion_actual', {}).get(bien, 0)
            if volumen_produccion > 20:  # Economías de escala
                factor_economia = min(0.95, 1 - volumen_produccion / 1000)
                self.costos_unitarios[bien] *= factor_economia
    
    def _evaluar_expansion_tactica(self):
        """Evalúa oportunidades de expansión táctica"""
        # Expansión de capacidad si hay alta demanda sostenida
        bienes_alta_demanda = []
        
        for bien in self.bienes:
            demanda_proyectada = self.analisis_competitivo.proyectar_demanda(bien)
            capacidad_actual = self.capacidad_produccion.get(bien, 10)
            
            if demanda_proyectada > capacidad_actual * 0.8:  # 80% de utilización
                bienes_alta_demanda.append((bien, demanda_proyectada))
        
        # Expandir capacidad del bien más prometedor
        if bienes_alta_demanda and self.dinero > 30000:
            bien_expandir, demanda = max(bienes_alta_demanda, key=lambda x: x[1])
            costo_expansion = self.capacidad_produccion.get(bien_expandir, 10) * 500
            
            if self.dinero > costo_expansion:
                expansion = int(self.capacidad_produccion.get(bien_expandir, 10) * 0.2)
                self.capacidad_produccion[bien_expandir] += expansion
                self.dinero -= costo_expansion
                
                logging.info(f"{self.nombre}: Expansión de capacidad en {bien_expandir} - +{expansion} unidades")
    
    def _actualizar_metricas_rendimiento(self):
        """Actualiza métricas de rendimiento empresarial"""
        # ROI aproximado
        if hasattr(self, 'dinero_inicial') and self.dinero_inicial > 0:
            roi = (self.dinero - self.dinero_inicial) / self.dinero_inicial
            self.roi_historico.append(roi)
        
        # Margen bruto por bien
        margenes = []
        for bien in self.precios:
            precio = self.precios[bien]
            costo = self.costos_unitarios.get(bien, precio * 0.7)
            margen = (precio - costo) / precio if precio > 0 else 0
            margenes.append(margen)
        
        if margenes:
            margen_promedio = sum(margenes) / len(margenes)
            self.margen_bruto_historico.append(margen_promedio)
        
        # Rotación de inventario (simplificado)
        inventario_total = sum(len(inv) if isinstance(inv, list) else inv for inv in self.bienes.values())
        if inventario_total > 0:
            # Aproximar rotación basada en volumen de ventas vs inventario
            self.rotacion_inventario = min(2.0, random.uniform(0.5, 1.5))
        
        # Actualizar reputación basada en rendimiento
        if self.roi_historico and len(self.roi_historico) >= 3:
            roi_promedio = sum(self.roi_historico[-3:]) / 3
            if roi_promedio > 0.1:  # 10% ROI
                self.reputacion_mercado = min(1.0, self.reputacion_mercado * 1.02)
            elif roi_promedio < 0:
                self.reputacion_mercado = max(0.1, self.reputacion_mercado * 0.98)
    
    def ciclo_persona(self, ciclo, mercado):
        """Ciclo principal que integra funcionalidad hiperrealista"""
        # Ejecutar ciclo base de empresa productora
        super().ciclo_persona(ciclo, mercado)
        
        # Ejecutar extensiones hiperrealistas
        self.ciclo_empresa_hiperrealista()
    
    def obtener_reporte_hiperrealista(self) -> Dict[str, Any]:
        """Genera reporte completo de la empresa hiperrealista"""
        reporte = {
            'nombre': self.nombre,
            'nivel_tecnologico': self.nivel_tecnologico,
            'reputacion_mercado': self.reputacion_mercado,
            'vision_empresa': self.vision_empresa,
            'objetivos_cumplimiento': [
                {
                    'descripcion': obj['descripcion'],
                    'progreso': obj.get('progreso_actual', 0),
                    'tipo': obj['tipo']
                }
                for obj in self.objetivos_estrategicos
            ],
            'roi_promedio': sum(self.roi_historico[-5:]) / min(len(self.roi_historico), 5) if self.roi_historico else 0,
            'margen_bruto_promedio': sum(self.margen_bruto_historico[-5:]) / min(len(self.margen_bruto_historico), 5) if self.margen_bruto_historico else 0,
            'rotacion_inventario': self.rotacion_inventario,
            'satisfaccion_accionistas': self.satisfaccion_accionistas,
            'responsabilidad_social': self.responsabilidad_social,
            'certificaciones': len(self.certificaciones_obtenidas),
            'patentes': len(self.patentes_registradas),
            'alianzas_tecnologicas': len(self.alianzas_tecnologicas),
            'seguros_contratados': len(self.seguros_contratados),
            'ia_habilitada': self.ia_habilitada,
            'calidad_promedio': self.gestion_calidad.nivel_calidad_promedio,
            'riesgo_operativo': self.gestion_riesgos_operativos.nivel_riesgo_actual,
            'sostenibilidad_score': self.programa_sostenibilidad.score_sostenibilidad
        }
        
        # Añadir estadísticas de IA si está habilitada
        if self.ia_habilitada and self.sistema_ia:
            reporte['estadisticas_ia'] = self.sistema_ia.get_estadisticas_empresariales_ia()
        
        return reporte
    
    def _limpiar_productos_invalidos(self):
        """Limpia productos que no existen en el mercado"""
        if not hasattr(self.mercado, 'bienes'):
            return
        
        # Lista de productos válidos en el mercado
        productos_validos = set(self.mercado.bienes.keys())
        
        # Limpiar precios de productos inválidos
        if hasattr(self, 'precios'):
            productos_a_eliminar = [p for p in self.precios.keys() if p not in productos_validos]
            for producto in productos_a_eliminar:
                del self.precios[producto]
                logging.debug(f"{self.nombre}: Eliminado precio de producto inválido - {producto}")
        
        # Limpiar costos de productos inválidos
        if hasattr(self, 'costos_unitarios'):
            productos_a_eliminar = [p for p in self.costos_unitarios.keys() if p not in productos_validos]
            for producto in productos_a_eliminar:
                del self.costos_unitarios[producto]
                logging.debug(f"{self.nombre}: Eliminado costo de producto inválido - {producto}")
        
        # Limpiar inventario de productos inválidos
        if hasattr(self, 'bienes'):
            productos_a_eliminar = [p for p in self.bienes.keys() if p not in productos_validos]
            for producto in productos_a_eliminar:
                del self.bienes[producto]
                logging.debug(f"{self.nombre}: Eliminado inventario de producto inválido - {producto}")
        
        # Limpiar capacidad de producción de productos inválidos
        if hasattr(self, 'capacidad_produccion'):
            productos_a_eliminar = [p for p in self.capacidad_produccion.keys() if p not in productos_validos]
            for producto in productos_a_eliminar:
                del self.capacidad_produccion[producto]
                logging.debug(f"{self.nombre}: Eliminada capacidad de producto inválido - {producto}")


# Sistemas de gestión especializados

class SistemaGestionCalidad:
    """Sistema de gestión de calidad empresarial"""
    
    def __init__(self, empresa):
        self.empresa = empresa
        self.nivel_calidad_promedio = random.uniform(0.7, 0.9)
        self.certificaciones_iso = []
        self.controles_calidad = 0
        self.defectos_detectados = 0
    
    def ciclo_calidad(self):
        """Ejecuta ciclo de gestión de calidad"""
        self._realizar_controles_calidad()
        self._implementar_mejoras_continuas()
        self._evaluar_certificaciones()
    
    def _realizar_controles_calidad(self):
        """Realiza controles de calidad en producción"""
        self.controles_calidad += 1
        
        # Detectar defectos basándose en nivel de calidad
        probabilidad_defecto = 1 - self.nivel_calidad_promedio
        
        for bien in self.empresa.bienes:
            if isinstance(self.empresa.bienes[bien], list):
                unidades_producidas = len(self.empresa.bienes[bien])
                defectos = sum(1 for _ in range(unidades_producidas) if random.random() < probabilidad_defecto)
                
                if defectos > 0:
                    self.defectos_detectados += defectos
                    # Retirar productos defectuosos
                    for _ in range(min(defectos, len(self.empresa.bienes[bien]))):
                        if self.empresa.bienes[bien]:
                            self.empresa.bienes[bien].pop()
    
    def _implementar_mejoras_continuas(self):
        """Implementa mejoras continuas de calidad"""
        if self.controles_calidad > 0:
            tasa_defectos = self.defectos_detectados / max(self.controles_calidad, 1)
            
            if tasa_defectos > 0.05:  # Si más del 5% son defectos
                # Invertir en mejoras de calidad
                if self.empresa.dinero > 5000:
                    inversion_calidad = min(10000, self.empresa.dinero * 0.05)
                    self.empresa.dinero -= inversion_calidad
                    
                    # Mejorar nivel de calidad
                    mejora = inversion_calidad / 20000  # Factor de conversión
                    self.nivel_calidad_promedio = min(0.98, self.nivel_calidad_promedio + mejora)
    
    def _evaluar_certificaciones(self):
        """Evalúa oportunidades de certificaciones de calidad"""
        if self.nivel_calidad_promedio > 0.85 and 'iso_9001' not in self.certificaciones_iso:
            if random.random() < 0.1:  # 10% probabilidad
                costo_certificacion = 8000
                if self.empresa.dinero > costo_certificacion:
                    self.empresa.dinero -= costo_certificacion
                    self.certificaciones_iso.append('iso_9001')
                    self.empresa.certificaciones_obtenidas.append('ISO 9001')
                    
                    # Beneficio en reputación y precios
                    self.empresa.reputacion_mercado = min(1.0, self.empresa.reputacion_mercado * 1.05)


class SistemaRiesgosOperativos:
    """Sistema de gestión de riesgos operativos"""
    
    def __init__(self, empresa):
        self.empresa = empresa
        self.nivel_riesgo_actual = random.uniform(0.2, 0.5)
        self.planes_mitigacion = []
        self.incidentes_registrados = 0
    
    def evaluar_riesgos(self):
        """Evalúa riesgos operativos actuales"""
        self._identificar_riesgos_criticos()
        self._aplicar_medidas_mitigacion()
        self._monitorear_incidentes()
    
    def _identificar_riesgos_criticos(self):
        """Identifica riesgos críticos operativos"""
        riesgos = []
        
        # Riesgo de personal
        if len(self.empresa.empleados) < 3:
            riesgos.append('personal_insuficiente')
        
        # Riesgo financiero
        ratio_liquidez = self.empresa.dinero / max(getattr(self.empresa, 'costos_fijos_mensuales', 1000), 1)
        if ratio_liquidez < 2:
            riesgos.append('liquidez_baja')
        
        # Riesgo de inventario
        inventario_total = sum(len(inv) if isinstance(inv, list) else inv for inv in self.empresa.bienes.values())
        capacidad_total = sum(getattr(self.empresa, 'capacidad_produccion', {}).values())
        if inventario_total > capacidad_total * 3:
            riesgos.append('exceso_inventario')
        
        # Actualizar nivel de riesgo
        self.nivel_riesgo_actual = min(0.9, len(riesgos) * 0.2 + 0.1)
    
    def _aplicar_medidas_mitigacion(self):
        """Aplica medidas de mitigación de riesgos"""
        if self.nivel_riesgo_actual > 0.6:
            # Activar protocolos de emergencia
            self.empresa.plan_contingencia.activar_plan()
        elif self.nivel_riesgo_actual > 0.4:
            # Medidas preventivas
            self._implementar_medidas_preventivas()
    
    def _implementar_medidas_preventivas(self):
        """Implementa medidas preventivas básicas"""
        # Aumentar reservas de emergencia
        if self.empresa.dinero > 20000:
            aumento_reservas = self.empresa.dinero * 0.02
            self.empresa.reservas_emergencia += aumento_reservas
            self.empresa.dinero -= aumento_reservas
    
    def _monitorear_incidentes(self):
        """Monitorea y registra incidentes operativos"""
        if random.random() < self.nivel_riesgo_actual * 0.1:  # Probabilidad de incidente
            self.incidentes_registrados += 1
            
            # Costo del incidente
            costo_incidente = random.uniform(1000, 5000)
            self.empresa.dinero = max(0, self.empresa.dinero - costo_incidente)
            
            logging.warning(f"{self.empresa.nombre}: Incidente operativo - Costo: ${costo_incidente:.2f}")


class SistemaGestionMarca:
    """Sistema de gestión de marca y reputación"""
    
    def __init__(self, empresa):
        self.empresa = empresa
        self.valor_marca = random.uniform(0.4, 0.8)
        self.inversion_marketing = 0
        self.campañas_activas = []
    
    def gestionar_reputacion(self):
        """Gestiona reputación y valor de marca"""
        self._evaluar_percepcion_mercado()
        self._planificar_marketing()
        self._gestionar_crisis_reputacion()
    
    def _evaluar_percepcion_mercado(self):
        """Evalúa percepción del mercado sobre la empresa"""
        # Factores que afectan la percepción
        factor_calidad = getattr(self.empresa.gestion_calidad, 'nivel_calidad_promedio', 0.7)
        factor_precios = self._evaluar_competitividad_precios()
        factor_innovacion = getattr(self.empresa, 'innovaciones_exitosas', 0) / 10
        
        percepcion_mercado = (factor_calidad * 0.4 + factor_precios * 0.3 + factor_innovacion * 0.3)
        
        # Actualizar reputación gradualmente
        self.empresa.reputacion_mercado = (
            self.empresa.reputacion_mercado * 0.8 + percepcion_mercado * 0.2
        )
    
    def _evaluar_competitividad_precios(self) -> float:
        """Evalúa competitividad de precios vs mercado"""
        if not self.empresa.precios:
            return 0.5
        
        # Comparar con precios promedio del mercado
        precio_promedio_empresa = sum(self.empresa.precios.values()) / len(self.empresa.precios)
        
        # Obtener precios de competidores (simplificado)
        competidores = [e for e in self.empresa.mercado.getEmpresas() if e != self.empresa]
        if competidores:
            precios_competencia = []
            for comp in competidores:
                if hasattr(comp, 'precios') and comp.precios:
                    precio_comp = sum(comp.precios.values()) / len(comp.precios)
                    precios_competencia.append(precio_comp)
            
            if precios_competencia:
                precio_mercado = sum(precios_competencia) / len(precios_competencia)
                # Retornar 1.0 si es 10% más barato, 0.5 si igual, 0.0 si es 50% más caro
                ratio = precio_promedio_empresa / precio_mercado
                return max(0, min(1, 1.5 - ratio))
        
        return 0.5
    
    def _planificar_marketing(self):
        """Planifica actividades de marketing"""
        # Presupuesto de marketing (2-5% de ingresos)
        presupuesto_marketing = self.empresa.dinero * random.uniform(0.02, 0.05)
        
        if presupuesto_marketing > 2000 and self.empresa.dinero > presupuesto_marketing:
            self.empresa.dinero -= presupuesto_marketing
            self.inversion_marketing += presupuesto_marketing
            
            # Beneficio en reputación y ventas
            mejora_reputacion = presupuesto_marketing / 50000  # Factor de conversión
            self.empresa.reputacion_mercado = min(1.0, self.empresa.reputacion_mercado + mejora_reputacion)
            
            # Crear campaña
            campaña = {
                'tipo': random.choice(['digital', 'tradicional', 'eventos']),
                'presupuesto': presupuesto_marketing,
                'duracion': random.randint(1, 3),
                'objetivo': random.choice(['awareness', 'ventas', 'reputacion'])
            }
            self.campañas_activas.append(campaña)
    
    def _gestionar_crisis_reputacion(self):
        """Gestiona crisis de reputación"""
        if self.empresa.reputacion_mercado < 0.4:
            # Crisis de reputación - inversión de emergencia en PR
            if self.empresa.dinero > 10000:
                inversion_crisis = min(15000, self.empresa.dinero * 0.1)
                self.empresa.dinero -= inversion_crisis
                
                # Mejora inmediata pero limitada de reputación
                mejora = inversion_crisis / 30000
                self.empresa.reputacion_mercado = min(0.6, self.empresa.reputacion_mercado + mejora)


class SistemaAnalisisCompetitivo:
    """Sistema de análisis competitivo continuo"""
    
    def __init__(self, empresa, mercado):
        self.empresa = empresa
        self.mercado = mercado
        self.competidores_monitoreados = {}
        self.tendencias_mercado = {}
    
    def actualizar_analisis(self):
        """Actualiza análisis competitivo"""
        self._monitorear_competidores()
        self._analizar_tendencias_mercado()
        self._identificar_oportunidades()
    
    def _monitorear_competidores(self):
        """Monitorea actividad de competidores"""
        competidores = [e for e in self.mercado.getEmpresas() if e != self.empresa]
        
        for comp in competidores:
            if hasattr(comp, 'nombre'):
                analisis = {
                    'precios_promedio': sum(comp.precios.values()) / len(comp.precios) if comp.precios else 0,
                    'capital': comp.dinero,
                    'empleados': len(getattr(comp, 'empleados', [])),
                    'productos': len(comp.bienes),
                    'ultima_actualizacion': self.mercado.ciclo_actual
                }
                self.competidores_monitoreados[comp.nombre] = analisis
    
    def _analizar_tendencias_mercado(self):
        """Analiza tendencias del mercado"""
        for bien in self.mercado.bienes:
            # Analizar tendencia de precios
            if bien in self.mercado.precios_historicos and len(self.mercado.precios_historicos[bien]) >= 3:
                precios = self.mercado.precios_historicos[bien][-3:]
                tendencia = (precios[-1] - precios[0]) / max(precios[0], 1)
                self.tendencias_mercado[bien] = tendencia
    
    def _identificar_oportunidades(self):
        """Identifica oportunidades competitivas"""
        oportunidades = []
        
        # Oportunidad 1: Bienes con tendencia alcista de precios
        for bien, tendencia in self.tendencias_mercado.items():
            if tendencia > 0.1 and bien in self.empresa.bienes:
                oportunidades.append({
                    'tipo': 'expansion_capacidad',
                    'bien': bien,
                    'razon': f'Tendencia alcista de precios: {tendencia:.1%}'
                })
        
        # Oportunidad 2: Nichos con pocos competidores
        for bien in self.mercado.bienes:
            competidores_bien = sum(1 for comp in self.competidores_monitoreados.values() 
                                  if comp.get('productos', 0) > 0)
            if competidores_bien < 3 and bien not in self.empresa.bienes:
                oportunidades.append({
                    'tipo': 'nuevo_producto',
                    'bien': bien,
                    'razon': f'Pocos competidores: {competidores_bien}'
                })
        
        return oportunidades
    
    def proyectar_demanda(self, bien: str) -> int:
        """Proyecta demanda futura para un bien"""
        # Demanda base
        demanda_base = 10
        
        # Ajustar por tendencias
        if bien in self.tendencias_mercado:
            factor_tendencia = 1 + self.tendencias_mercado[bien]
            demanda_base *= factor_tendencia
        
        # Ajustar por competencia
        competidores = len([c for c in self.competidores_monitoreados.values() if c.get('productos', 0) > 0])
        factor_competencia = max(0.5, 1 - competidores * 0.1)
        demanda_base *= factor_competencia
        
        return max(1, int(demanda_base))


class PlanContingencia:
    """Plan de contingencia empresarial"""
    
    def __init__(self, empresa):
        self.empresa = empresa
        self.plan_activo = False
        self.medidas_implementadas = []
    
    def activar_plan(self):
        """Activa plan de contingencia"""
        if not self.plan_activo:
            self.plan_activo = True
            self._implementar_medidas_emergencia()
    
    def _implementar_medidas_emergencia(self):
        """Implementa medidas de emergencia"""
        # Reducir costos no esenciales
        if hasattr(self.empresa, 'costos_fijos_mensuales'):
            self.empresa.costos_fijos_mensuales *= 0.8
            self.medidas_implementadas.append('reduccion_costos_fijos')
        
        # Usar reservas de emergencia
        if self.empresa.reservas_emergencia > 0:
            self.empresa.dinero += self.empresa.reservas_emergencia
            self.empresa.reservas_emergencia = 0
            self.medidas_implementadas.append('uso_reservas_emergencia')
        
        # Liquidar inventario no crítico
        self._liquidar_inventario_no_critico()
    
    def _liquidar_inventario_no_critico(self):
        """Liquida inventario no crítico para generar efectivo"""
        for bien, inventario in self.empresa.bienes.items():
            if isinstance(inventario, list) and len(inventario) > 5:
                # Liquidar 40% del inventario excesivo
                cantidad_liquidar = int(len(inventario) * 0.4)
                precio_liquidacion = self.empresa.precios.get(bien, 10) * 0.7  # 30% descuento
                
                for _ in range(cantidad_liquidar):
                    if inventario:
                        inventario.pop()
                        self.empresa.dinero += precio_liquidacion
                
                self.medidas_implementadas.append(f'liquidacion_inventario_{bien}')


class CentroInnovacionEmpresarial:
    """Centro de innovación empresarial avanzado"""
    
    def __init__(self, empresa):
        self.empresa = empresa
        self.proyectos_innovacion = []
        self.patentes_pendientes = []
        self.colaboraciones_externas = []
    
    def ciclo_innovacion(self):
        """Ejecuta ciclo de innovación empresarial"""
        self._gestionar_proyectos_existentes()
        self._evaluar_nuevos_proyectos()
        self._gestionar_patentes()
        self._explorar_colaboraciones()
    
    def _gestionar_proyectos_existentes(self):
        """Gestiona proyectos de innovación existentes"""
        for proyecto in self.proyectos_innovacion[:]:
            proyecto['progreso'] += random.uniform(0.1, 0.3)
            
            if proyecto['progreso'] >= 1.0:
                self._completar_proyecto_innovacion(proyecto)
                self.proyectos_innovacion.remove(proyecto)
    
    def _completar_proyecto_innovacion(self, proyecto):
        """Completa proyecto de innovación"""
        if proyecto['tipo'] == 'proceso':
            # Mejora de proceso
            self.empresa.eficiencia_produccion = min(1.0, self.empresa.eficiencia_produccion * 1.15)
        elif proyecto['tipo'] == 'producto':
            # Nuevo producto
            self._lanzar_producto_innovador(proyecto)
        elif proyecto['tipo'] == 'tecnologia':
            # Nueva tecnología
            self.empresa.nivel_tecnologico = min(1.0, self.empresa.nivel_tecnologico * 1.1)
        
        # Incrementar contador
        if not hasattr(self.empresa, 'innovaciones_exitosas'):
            self.empresa.innovaciones_exitosas = 0
        self.empresa.innovaciones_exitosas += 1
        
        # Aplicar para patente
        if random.random() < 0.6:
            self.patentes_pendientes.append({
                'proyecto': proyecto['nombre'],
                'tipo': proyecto['tipo'],
                'fecha_solicitud': self.empresa.mercado.ciclo_actual
            })
    
    def _lanzar_producto_innovador(self, proyecto):
        """Lanza producto innovador al mercado"""
        # CORRECCIÓN: Solo usar productos existentes en el mercado
        productos_existentes = list(self.empresa.mercado.bienes.keys())
        if not productos_existentes:
            return  # No hay productos para mejorar
        
        # Mejorar un producto existente en lugar de crear uno nuevo
        producto_base = random.choice(productos_existentes)
        
        # Aplicar mejora al producto existente
        if producto_base in self.empresa.costos_unitarios:
            # Reducir costos por innovación (5-15%)
            factor_mejora = random.uniform(0.85, 0.95)
            self.empresa.costos_unitarios[producto_base] *= factor_mejora
            
            # Mejorar calidad (reflejado en precio potencial)
            if hasattr(self.empresa, 'calidad_productos'):
                if producto_base not in self.empresa.calidad_productos:
                    self.empresa.calidad_productos = {}
                self.empresa.calidad_productos[producto_base] = min(1.0, 
                    self.empresa.calidad_productos.get(producto_base, 0.5) + 0.1)
        
        logging.info(f"{self.empresa.nombre}: Innovación aplicada a producto existente - {producto_base}")
    
    def _evaluar_nuevos_proyectos(self):
        """Evalúa oportunidades de nuevos proyectos"""
        if len(self.proyectos_innovacion) < 2 and self.empresa.dinero > 20000:
            if random.random() < 0.15:  # 15% probabilidad
                self._iniciar_proyecto_innovacion()
    
    def _iniciar_proyecto_innovacion(self):
        """Inicia nuevo proyecto de innovación"""
        tipos_proyecto = ['proceso', 'producto', 'tecnologia']
        tipo = random.choice(tipos_proyecto)
        
        proyecto = {
            'nombre': f"proyecto_{tipo}_{len(self.proyectos_innovacion)}",
            'tipo': tipo,
            'progreso': 0.0,
            'inversion_total': random.uniform(5000, 25000),
            'riesgo': random.uniform(0.3, 0.7),
            'impacto_esperado': random.uniform(0.1, 0.4)
        }
        
        if self.empresa.dinero > proyecto['inversion_total']:
            self.empresa.dinero -= proyecto['inversion_total']
            self.proyectos_innovacion.append(proyecto)
    
    def _gestionar_patentes(self):
        """Gestiona proceso de patentes"""
        for patente in self.patentes_pendientes[:]:
            # Proceso de patente toma tiempo
            if self.empresa.mercado.ciclo_actual - patente['fecha_solicitud'] > 5:
                if random.random() < 0.8:  # 80% éxito
                    self.empresa.patentes_registradas.append(patente)
                    
                    # Beneficio económico de la patente
                    valor_patente = random.uniform(5000, 20000)
                    self.empresa.dinero += valor_patente
                
                self.patentes_pendientes.remove(patente)
    
    def _explorar_colaboraciones(self):
        """Explora colaboraciones tecnológicas"""
        if random.random() < 0.05:  # 5% probabilidad
            # Colaboración con universidad o centro de investigación
            colaboracion = {
                'tipo': random.choice(['universidad', 'centro_investigacion', 'startup']),
                'area': random.choice(['tecnologia', 'sostenibilidad', 'digitalizacion']),
                'duracion': random.randint(6, 18),
                'costo': random.uniform(3000, 12000)
            }
            
            if self.empresa.dinero > colaboracion['costo']:
                self.empresa.dinero -= colaboracion['costo']
                self.colaboraciones_externas.append(colaboracion)
                self.empresa.alianzas_tecnologicas.append(colaboracion['tipo'])


class ProgramaSostenibilidad:
    """Programa integral de sostenibilidad corporativa"""
    
    def __init__(self, empresa):
        self.empresa = empresa
        self.score_sostenibilidad = random.uniform(0.3, 0.6)
        self.iniciativas_activas = []
        self.reportes_sostenibilidad = []
    
    def ciclo_sostenibilidad(self):
        """Ejecuta ciclo de sostenibilidad"""
        self._evaluar_impacto_actual()
        self._implementar_iniciativas()
        self._generar_reporte_sostenibilidad()
    
    def _evaluar_impacto_actual(self):
        """Evalúa impacto ambiental y social actual"""
        # Impacto ambiental basado en producción
        factor_produccion = sum(getattr(self.empresa, 'produccion_actual', {}).values())
        impacto_ambiental = factor_produccion * getattr(self.empresa, 'factor_emisiones', 1.0)
        
        # Impacto social basado en empleados
        impacto_social = len(self.empresa.empleados) * 0.1  # Contribución positiva al empleo
        
        # Actualizar score
        self.score_sostenibilidad = (
            self.score_sostenibilidad * 0.9 + 
            (impacto_social - impacto_ambiental * 0.01) * 0.1
        )
        self.score_sostenibilidad = max(0.1, min(1.0, self.score_sostenibilidad))
    
    def _implementar_iniciativas(self):
        """Implementa iniciativas de sostenibilidad"""
        if self.empresa.dinero > 15000 and len(self.iniciativas_activas) < 3:
            if random.random() < 0.2:  # 20% probabilidad
                self._lanzar_nueva_iniciativa()
    
    def _lanzar_nueva_iniciativa(self):
        """Lanza nueva iniciativa de sostenibilidad"""
        tipos_iniciativa = [
            'energia_renovable', 'reduccion_residuos', 'agua_limpia',
            'transporte_sostenible', 'cadena_suministro_verde'
        ]
        
        iniciativa = {
            'tipo': random.choice(tipos_iniciativa),
            'inversion': random.uniform(5000, 20000),
            'impacto_esperado': random.uniform(0.1, 0.3),
            'duracion': random.randint(6, 24),
            'progreso': 0.0
        }
        
        if self.empresa.dinero > iniciativa['inversion']:
            self.empresa.dinero -= iniciativa['inversion']
            self.iniciativas_activas.append(iniciativa)
            
            # Beneficio inmediato en score
            self.score_sostenibilidad = min(1.0, self.score_sostenibilidad + 0.05)
    
    def _generar_reporte_sostenibilidad(self):
        """Genera reporte de sostenibilidad periódico"""
        if self.empresa.mercado.ciclo_actual % 12 == 0:  # Anual
            reporte = {
                'ciclo': self.empresa.mercado.ciclo_actual,
                'score_sostenibilidad': self.score_sostenibilidad,
                'iniciativas_completadas': len([i for i in self.iniciativas_activas if i['progreso'] >= 1.0]),
                'inversion_total': sum(i['inversion'] for i in self.iniciativas_activas),
                'impacto_comunidad': self.empresa.inversion_comunidad
            }
            
            self.reportes_sostenibilidad.append(reporte)
            
            # Beneficio en reputación por transparencia
            self.empresa.reputacion_mercado = min(1.0, self.empresa.reputacion_mercado * 1.02)
