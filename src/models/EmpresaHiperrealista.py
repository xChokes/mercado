"""
Empresa Hiperrfrom src.systems.GestionEmpresarialAvanzada import GestionEmpresarialAvanzada
from src.systems.ProblemasEmpresariales import GestorProblemasEmpresariales
from src.config.ConfigEmpresaHiperrealista import ConfigEmpresaHiperrealistalista con Gestión Avanzada
==========================================

Implementa una empresa con todas las funcionalidades del mundo real:
- Gestión de recursos humanos profesional
- Análisis de competencia
- Gestión de riesgos operacionales
- Innovación y desarrollo
- Responsabilidad social corporativa
- Análisis financiero avanzado
- Cadena de suministro
"""

import random
import logging
from typing import Dict, List, Any, Optional
from .EmpresaProductora import EmpresaProductora
from ..systems.GestionEmpresarialAvanzada import GestionEmpresarialAvanzada
from ..systems.ProblemasEmpresariales import GestorProblemasEmpresariales


class EmpresaHiperrealista(EmpresaProductora):
    """
    Empresa con gestión empresarial hiperrealista que incorpora
    todas las funcionalidades de una empresa moderna real
    """
    
    def __init__(self, nombre, mercado, bienes={}):
        super().__init__(nombre, mercado, bienes)
        
        # Sistema de gestión empresarial avanzada
        self.gestion_avanzada = GestionEmpresarialAvanzada(self)
        
        # Sistema de gestión de problemas empresariales
        self.gestor_problemas = GestorProblemasEmpresariales(self)
        
        # Atributos adicionales para realismo
        self.fundacion_año = 2020 + random.randint(-10, 0)  # Empresa fundada en los últimos 10 años
        self.sector_principal = self._determinar_sector_principal()
        self.mision_corporativa = self._generar_mision()
        self.vision_corporativa = self._generar_vision()
        
        # Estructura organizacional
        self.estructura_organizacional = {
            'direccion_general': True,
            'finanzas': len(self.empleados) > 5,
            'recursos_humanos': len(self.empleados) > 10,
            'marketing': len(self.empleados) > 8,
            'operaciones': True,
            'investigacion_desarrollo': len(self.empleados) > 15
        }
        
        # Métricas empresariales avanzadas
        self.metricas_financieras = {
            'ebitda': 0.0,
            'flujo_caja_libre': 0.0,
            'apalancamiento': 0.0,
            'liquidez_corriente': 0.0,
            'rentabilidad_activos': 0.0,
            'crecimiento_ventas': 0.0
        }
        
        # Histórico de decisiones estratégicas
        self.decisiones_estrategicas = []
        self.crisis_superadas = []
        self.logros_empresariales = []
        
        # Relaciones externas
        self.alianzas_comerciales = []
        self.proveedores_estrategicos = []
        self.clientes_corporativos = []
        
        # Certificaciones y reconocimientos
        self.certificaciones = []
        self.premios_recibidos = []
        
        # Inicializar según tamaño de empresa
        self._clasificar_empresa()
        self._inicializar_por_tamaño()
        
    def _determinar_sector_principal(self) -> str:
        """Determina el sector principal de la empresa"""
        if not self.bienes:
            return "servicios"
        
        # Analizar tipos de productos
        productos = list(self.bienes.keys())
        sectores = {
            'alimentos': ['pan', 'leche', 'carne', 'vegetales', 'frutas'],
            'tecnologia': ['electronica', 'software', 'computadoras'],
            'textil': ['ropa', 'textiles', 'calzado'],
            'construccion': ['cemento', 'acero', 'madera'],
            'energia': ['petroleo', 'gas', 'electricidad'],
            'servicios': ['servicios', 'consultoria', 'educacion']
        }
        
        for sector, palabras_clave in sectores.items():
            if any(palabra in producto.lower() for producto in productos for palabra in palabras_clave):
                return sector
        
        return "manufacturero"
    
    def _generar_mision(self) -> str:
        """Genera una misión corporativa realista"""
        misiones_base = [
            f"Liderar el sector {self.sector_principal} mediante la innovación y calidad excepcional",
            f"Proporcionar soluciones de {self.sector_principal} que transformen vidas",
            f"Ser el socio estratégico preferido en {self.sector_principal}",
            f"Crear valor sostenible en {self.sector_principal} para todos nuestros stakeholders"
        ]
        return random.choice(misiones_base)
    
    def _generar_vision(self) -> str:
        """Genera una visión corporativa realista"""
        visiones_base = [
            f"Ser la empresa líder en {self.sector_principal} a nivel nacional",
            f"Transformar el sector {self.sector_principal} mediante la innovación",
            f"Expandir globalmente manteniendo nuestros valores en {self.sector_principal}",
            f"Ser reconocidos como la empresa más sostenible en {self.sector_principal}"
        ]
        return random.choice(visiones_base)
    
    def _clasificar_empresa(self):
        """Clasifica la empresa por tamaño"""
        num_empleados = len(self.empleados)
        
        if num_empleados < 10:
            self.tamaño_empresa = "microempresa"
        elif num_empleados < 50:
            self.tamaño_empresa = "pequeña"
        elif num_empleados < 250:
            self.tamaño_empresa = "mediana"
        else:
            self.tamaño_empresa = "grande"
    
    def _inicializar_por_tamaño(self):
        """Inicializa características según el tamaño de empresa"""
        if self.tamaño_empresa == "microempresa":
            self.presupuesto_marketing = self.dinero * 0.02
            self.presupuesto_id = self.dinero * 0.01
            self.estructura_organizacional = {k: False for k in self.estructura_organizacional}
            self.estructura_organizacional['direccion_general'] = True
            
        elif self.tamaño_empresa == "pequeña":
            self.presupuesto_marketing = self.dinero * 0.03
            self.presupuesto_id = self.dinero * 0.02
            
        elif self.tamaño_empresa == "mediana":
            self.presupuesto_marketing = self.dinero * 0.05
            self.presupuesto_id = self.dinero * 0.04
            
        else:  # grande
            self.presupuesto_marketing = self.dinero * 0.07
            self.presupuesto_id = self.dinero * 0.06
    
    def ejecutar_plan_estrategico(self, mercado) -> Dict[str, Any]:
        """Ejecuta el plan estratégico anual de la empresa"""
        plan_resultados = {
            'objetivos_cumplidos': 0,
            'inversion_estrategica': 0,
            'nuevas_iniciativas': [],
            'kpis_mejorados': []
        }
        
        # Definir objetivos estratégicos basados en análisis FODA
        objetivos = self._definir_objetivos_estrategicos(mercado)
        
        for objetivo in objetivos:
            resultado = self._ejecutar_objetivo_estrategico(objetivo, mercado)
            if resultado['exito']:
                plan_resultados['objetivos_cumplidos'] += 1
                plan_resultados['inversion_estrategica'] += resultado['inversion']
                plan_resultados['nuevas_iniciativas'].extend(resultado['iniciativas'])
        
        # Registrar decisión estratégica
        self.decisiones_estrategicas.append({
            'año': 2024,  # Simplificado
            'plan': objetivos,
            'resultados': plan_resultados,
            'inversion_total': plan_resultados['inversion_estrategica']
        })
        
        return plan_resultados
    
    def _definir_objetivos_estrategicos(self, mercado) -> List[Dict[str, Any]]:
        """Define objetivos estratégicos basados en análisis de situación"""
        objetivos = []
        
        # Objetivo 1: Crecimiento en ventas
        if len(self.bienes) > 0:
            objetivos.append({
                'tipo': 'crecimiento_ventas',
                'meta': 'Aumentar ventas 15% anual',
                'inversion_requerida': self.dinero * 0.1,
                'plazo_meses': 12,
                'probabilidad_exito': 0.7
            })
        
        # Objetivo 2: Expansión de productos
        if self.dinero > 50000:
            objetivos.append({
                'tipo': 'expansion_productos',
                'meta': 'Lanzar 2 nuevos productos',
                'inversion_requerida': self.dinero * 0.15,
                'plazo_meses': 18,
                'probabilidad_exito': 0.6
            })
        
        # Objetivo 3: Mejora operacional
        objetivos.append({
            'tipo': 'mejora_operacional',
            'meta': 'Reducir costos operativos 10%',
            'inversion_requerida': self.dinero * 0.05,
            'plazo_meses': 6,
            'probabilidad_exito': 0.8
        })
        
        # Objetivo 4: Expansión geográfica (solo empresas grandes)
        if self.tamaño_empresa in ["mediana", "grande"]:
            objetivos.append({
                'tipo': 'expansion_geografica',
                'meta': 'Entrar en 2 nuevos mercados',
                'inversion_requerida': self.dinero * 0.2,
                'plazo_meses': 24,
                'probabilidad_exito': 0.5
            })
        
        # Objetivo 5: Sostenibilidad
        if self.gestion_avanzada.responsabilidad_social.reputacion_corporativa > 0.6:
            objetivos.append({
                'tipo': 'sostenibilidad',
                'meta': 'Certificación ambiental ISO 14001',
                'inversion_requerida': self.dinero * 0.03,
                'plazo_meses': 12,
                'probabilidad_exito': 0.7
            })
        
        return objetivos
    
    def _ejecutar_objetivo_estrategico(self, objetivo: Dict[str, Any], mercado) -> Dict[str, Any]:
        """Ejecuta un objetivo estratégico específico"""
        if objetivo['inversion_requerida'] > self.dinero:
            return {'exito': False, 'razon': 'Fondos insuficientes', 'inversion': 0, 'iniciativas': []}
        
        # Evaluar probabilidad de éxito
        if random.random() > objetivo['probabilidad_exito']:
            # Inversión parcial incluso si falla
            inversion_parcial = objetivo['inversion_requerida'] * 0.3
            self.dinero -= inversion_parcial
            return {'exito': False, 'razon': 'Ejecución fallida', 'inversion': inversion_parcial, 'iniciativas': []}
        
        # Ejecutar objetivo exitosamente
        self.dinero -= objetivo['inversion_requerida']
        iniciativas = self._generar_iniciativas_objetivo(objetivo, mercado)
        
        return {
            'exito': True,
            'inversion': objetivo['inversion_requerida'],
            'iniciativas': iniciativas
        }
    
    def _generar_iniciativas_objetivo(self, objetivo: Dict[str, Any], mercado) -> List[str]:
        """Genera iniciativas específicas para cada tipo de objetivo"""
        iniciativas = []
        
        if objetivo['tipo'] == 'crecimiento_ventas':
            iniciativas = [
                'Campaña de marketing digital',
                'Programa de fidelización de clientes',
                'Expansión del equipo de ventas'
            ]
            # Aplicar efectos
            for producto in self.precios:
                self.precios[producto] *= random.uniform(1.02, 1.08)  # Incremento de precios premium
        
        elif objetivo['tipo'] == 'expansion_productos':
            iniciativas = [
                'Investigación de mercado para nuevos productos',
                'Desarrollo de prototipos',
                'Pruebas de mercado'
            ]
            # Iniciar proyectos de I+D
            for _ in range(2):
                oportunidades = self.gestion_avanzada.gestion_innovacion.evaluar_oportunidades_innovacion()
                if oportunidades:
                    self.gestion_avanzada.gestion_innovacion.iniciar_proyecto_id(oportunidades[0])
        
        elif objetivo['tipo'] == 'mejora_operacional':
            iniciativas = [
                'Automatización de procesos',
                'Capacitación en lean manufacturing',
                'Optimización de la cadena de suministro'
            ]
            # Reducir costos operativos
            for producto in self.costos_unitarios:
                self.costos_unitarios[producto] *= random.uniform(0.9, 0.95)
        
        elif objetivo['tipo'] == 'expansion_geografica':
            iniciativas = [
                'Apertura de nueva sucursal',
                'Alianzas comerciales regionales',
                'Contratación de equipo local'
            ]
            # Aumentar capacidad
            for producto in self.capacidad_produccion:
                self.capacidad_produccion[producto] *= random.uniform(1.2, 1.5)
        
        elif objetivo['tipo'] == 'sostenibilidad':
            iniciativas = [
                'Auditoría ambiental',
                'Implementación de procesos verdes',
                'Certificación ISO 14001'
            ]
            # Mejorar reputación
            self.gestion_avanzada.responsabilidad_social.reputacion_corporativa = min(1.0,
                self.gestion_avanzada.responsabilidad_social.reputacion_corporativa + 0.1)
            self.certificaciones.append('ISO 14001')
        
        return iniciativas
    
    def analizar_performance_empresarial(self) -> Dict[str, Any]:
        """Analiza la performance integral de la empresa"""
        analisis = {
            'salud_financiera': self._evaluar_salud_financiera(),
            'posicion_competitiva': self._evaluar_posicion_competitiva(),
            'eficiencia_operacional': self._evaluar_eficiencia_operacional(),
            'innovacion_y_crecimiento': self._evaluar_innovacion_crecimiento(),
            'responsabilidad_social': self._evaluar_responsabilidad_social(),
            'calificacion_general': 0.0
        }
        
        # Calcular calificación general (0-100)
        pesos = {
            'salud_financiera': 0.3,
            'posicion_competitiva': 0.25,
            'eficiencia_operacional': 0.2,
            'innovacion_y_crecimiento': 0.15,
            'responsabilidad_social': 0.1
        }
        
        calificacion_total = sum(analisis[categoria]['score'] * peso 
                               for categoria, peso in pesos.items())
        analisis['calificacion_general'] = calificacion_total
        
        # Generar recomendaciones
        analisis['recomendaciones'] = self._generar_recomendaciones_performance(analisis)
        
        return analisis
    
    def _evaluar_salud_financiera(self) -> Dict[str, Any]:
        """Evalúa la salud financiera de la empresa"""
        # Cálculos financieros básicos
        activos_totales = self.dinero + sum(len(inventario) * self.costos_unitarios.get(bien, 0) 
                                          for bien, inventario in self.bienes.items())
        
        pasivos_totales = getattr(self, 'deuda_bancaria', 0) + (self.costo_salarios * 12)
        patrimonio = activos_totales - pasivos_totales
        
        # Métricas financieras
        liquidez = self.dinero / max(1, self.costos_fijos_mensuales) if hasattr(self, 'costos_fijos_mensuales') else 1.0
        solvencia = patrimonio / max(1, activos_totales)
        apalancamiento = pasivos_totales / max(1, patrimonio) if patrimonio > 0 else 0
        
        # Score de salud financiera (0-100)
        score_liquidez = min(100, liquidez * 20)  # 5 meses de operación = 100 puntos
        score_solvencia = solvencia * 100
        score_apalancamiento = max(0, 100 - apalancamiento * 50)
        
        score_final = (score_liquidez * 0.4 + score_solvencia * 0.4 + score_apalancamiento * 0.2)
        
        return {
            'score': score_final,
            'liquidez_meses': liquidez,
            'solvencia_ratio': solvencia,
            'apalancamiento_ratio': apalancamiento,
            'activos_totales': activos_totales,
            'patrimonio': patrimonio,
            'estado': 'excelente' if score_final > 80 else 'bueno' if score_final > 60 else 'regular' if score_final > 40 else 'preocupante'
        }
    
    def _evaluar_posicion_competitiva(self) -> Dict[str, Any]:
        """Evalúa la posición competitiva"""
        competidores = self.gestion_avanzada.analisis_competencia.competidores
        
        if not competidores:
            return {'score': 70, 'posicion': 'indefinida', 'amenazas': 0, 'ventajas': []}
        
        # Analizar amenazas
        amenazas_altas = sum(1 for comp in competidores.values() if comp.amenaza_nivel > 0.6)
        
        # Analizar ventajas competitivas
        ventajas = []
        if self.dinero > sum(getattr(comp, 'dinero', 0) for comp in competidores.values()) / len(competidores):
            ventajas.append('recursos_financieros')
        
        if len(self.empleados) > sum(len(getattr(comp, 'empleados', [])) for comp in competidores.values()) / len(competidores):
            ventajas.append('recursos_humanos')
        
        if len(self.bienes) > sum(len(getattr(comp, 'bienes', {})) for comp in competidores.values()) / len(competidores):
            ventajas.append('diversificacion_productos')
        
        # Score competitivo
        score = 50  # Base
        score -= amenazas_altas * 15  # Penalizar amenazas
        score += len(ventajas) * 10   # Premiar ventajas
        score = max(0, min(100, score))
        
        return {
            'score': score,
            'posicion': 'lider' if score > 80 else 'fuerte' if score > 60 else 'promedio' if score > 40 else 'debil',
            'amenazas': amenazas_altas,
            'ventajas': ventajas,
            'competidores_monitoreados': len(competidores)
        }
    
    def _evaluar_eficiencia_operacional(self) -> Dict[str, Any]:
        """Evalúa la eficiencia operacional"""
        productividad = self.gestion_avanzada.gestion_rrhh.calcular_productividad_total()
        
        # Eficiencia de producción
        eficiencia_produccion = getattr(self, 'eficiencia_produccion', 0.8)
        
        # Utilización de capacidad
        capacidad_total = sum(self.capacidad_produccion.values()) if hasattr(self, 'capacidad_produccion') else 1
        produccion_actual = sum(self.produccion_actual.values()) if hasattr(self, 'produccion_actual') else 0
        utilizacion_capacidad = produccion_actual / max(1, capacidad_total)
        
        # Score operacional
        score_productividad = min(100, productividad * 70)  # Productividad 1.4 = 98 puntos
        score_eficiencia = eficiencia_produccion * 100
        score_utilizacion = utilizacion_capacidad * 100
        
        score_final = (score_productividad * 0.4 + score_eficiencia * 0.4 + score_utilizacion * 0.2)
        
        return {
            'score': score_final,
            'productividad': productividad,
            'eficiencia_produccion': eficiencia_produccion,
            'utilizacion_capacidad': utilizacion_capacidad,
            'estado': 'optima' if score_final > 85 else 'buena' if score_final > 70 else 'mejorable' if score_final > 50 else 'deficiente'
        }
    
    def _evaluar_innovacion_crecimiento(self) -> Dict[str, Any]:
        """Evalúa capacidad de innovación y crecimiento"""
        proyectos_activos = len(self.gestion_avanzada.gestion_innovacion.proyectos_activos)
        proyectos_completados = len(self.gestion_avanzada.gestion_innovacion.proyectos_completados)
        
        # Inversión en I+D como % de ingresos
        inversion_id = sum(p.inversion_actual for p in self.gestion_avanzada.gestion_innovacion.proyectos_activos.values())
        ratio_id = inversion_id / max(1, self.dinero)
        
        # Score de innovación
        score_proyectos = min(100, (proyectos_activos + proyectos_completados) * 20)
        score_inversion = min(100, ratio_id * 1000)  # 10% inversión = 100 puntos
        
        score_final = (score_proyectos * 0.6 + score_inversion * 0.4)
        
        return {
            'score': score_final,
            'proyectos_activos': proyectos_activos,
            'proyectos_completados': proyectos_completados,
            'inversion_id': inversion_id,
            'ratio_id': ratio_id,
            'capacidad': 'alta' if score_final > 75 else 'media' if score_final > 45 else 'baja'
        }
    
    def _evaluar_responsabilidad_social(self) -> Dict[str, Any]:
        """Evalúa responsabilidad social corporativa"""
        reputacion = self.gestion_avanzada.responsabilidad_social.reputacion_corporativa
        programas_activos = sum(1 for p in self.gestion_avanzada.responsabilidad_social.programas_rsc.values() if p['activo'])
        
        score = reputacion * 70 + programas_activos * 7.5  # 4 programas = 30 puntos adicionales
        
        return {
            'score': min(100, score),
            'reputacion': reputacion,
            'programas_activos': programas_activos,
            'certificaciones': len(self.certificaciones),
            'nivel': 'ejemplar' if score > 80 else 'responsable' if score > 60 else 'basico' if score > 40 else 'deficiente'
        }
    
    def _generar_recomendaciones_performance(self, analisis: Dict[str, Any]) -> List[str]:
        """Genera recomendaciones basadas en el análisis de performance"""
        recomendaciones = []
        
        # Recomendaciones financieras
        if analisis['salud_financiera']['score'] < 60:
            if analisis['salud_financiera']['liquidez_meses'] < 3:
                recomendaciones.append("URGENTE: Mejorar liquidez - buscar financiamiento o reducir costos")
            if analisis['salud_financiera']['apalancamiento_ratio'] > 2:
                recomendaciones.append("Reducir apalancamiento - pagar deuda o aumentar capital")
        
        # Recomendaciones competitivas
        if analisis['posicion_competitiva']['score'] < 50:
            recomendaciones.append("Desarrollar ventajas competitivas - innovación o diferenciación")
            if analisis['posicion_competitiva']['amenazas'] > 2:
                recomendaciones.append("Estrategia defensiva contra competidores fuertes")
        
        # Recomendaciones operacionales
        if analisis['eficiencia_operacional']['score'] < 70:
            if analisis['eficiencia_operacional']['productividad'] < 1.0:
                recomendaciones.append("Mejorar productividad - capacitación y motivación del personal")
            if analisis['eficiencia_operacional']['utilizacion_capacidad'] < 0.6:
                recomendaciones.append("Optimizar utilización de capacidad instalada")
        
        # Recomendaciones de innovación
        if analisis['innovacion_y_crecimiento']['score'] < 40:
            recomendaciones.append("Aumentar inversión en I+D para competitividad futura")
            if analisis['innovacion_y_crecimiento']['proyectos_activos'] == 0:
                recomendaciones.append("Iniciar proyectos de innovación inmediatamente")
        
        # Recomendaciones de RSC
        if analisis['responsabilidad_social']['score'] < 50:
            recomendaciones.append("Implementar programas de responsabilidad social")
        
        return recomendaciones
    
    def gestionar_crisis_empresarial(self, tipo_crisis: str) -> Dict[str, Any]:
        """Gestiona diferentes tipos de crisis empresariales"""
        planes_crisis = {
            'financiera': self._plan_crisis_financiera,
            'reputacional': self._plan_crisis_reputacional,
            'operacional': self._plan_crisis_operacional,
            'competitiva': self._plan_crisis_competitiva,
            'regulatoria': self._plan_crisis_regulatoria
        }
        
        if tipo_crisis not in planes_crisis:
            return {'exito': False, 'mensaje': 'Tipo de crisis no reconocido'}
        
        plan_resultado = planes_crisis[tipo_crisis]()
        
        # Registrar crisis superada si fue exitosa
        if plan_resultado['exito']:
            self.crisis_superadas.append({
                'tipo': tipo_crisis,
                'año': 2024,
                'costo': plan_resultado.get('costo', 0),
                'duracion_meses': random.randint(3, 12),
                'lecciones_aprendidas': plan_resultado.get('lecciones', [])
            })
        
        return plan_resultado
    
    def _plan_crisis_financiera(self) -> Dict[str, Any]:
        """Plan de manejo de crisis financiera"""
        acciones = []
        costo_total = 0
        
        # 1. Reducción de costos inmediata
        reduccion_costos = self.costos_fijos_mensuales * 0.3
        self.costos_fijos_mensuales *= 0.7
        acciones.append(f"Reducción costos fijos: ${reduccion_costos:,.0f}")
        
        # 2. Renegociación con proveedores
        if random.random() < 0.7:  # 70% éxito
            ahorro_proveedores = sum(self.costos_unitarios.values()) * 0.1
            for bien in self.costos_unitarios:
                self.costos_unitarios[bien] *= 0.9
            acciones.append(f"Renegociación proveedores: ${ahorro_proveedores:,.0f} ahorro")
        
        # 3. Búsqueda de financiamiento de emergencia
        financiamiento_necesario = self.costos_fijos_mensuales * 6
        if hasattr(self.mercado, 'sistema_bancario'):
            for banco in self.mercado.sistema_bancario.bancos:
                aprobado, mensaje = banco.solicitar_prestamo(self, financiamiento_necesario, 36)
                if aprobado:
                    acciones.append(f"Préstamo emergencia obtenido: ${financiamiento_necesario:,.0f}")
                    break
        
        # 4. Reestructuración organizacional
        if len(self.empleados) > 5:
            empleados_despedir = len(self.empleados) // 4  # 25% de reducción
            for _ in range(empleados_despedir):
                if self.empleados:
                    empleado = self.empleados.pop()
                    self.costo_salarios -= getattr(empleado, 'ingreso_mensual', 0)
            acciones.append(f"Reestructuración: {empleados_despedir} empleados")
            costo_total += empleados_despedir * 2000  # Costo de indemnizaciones
        
        return {
            'exito': len(acciones) >= 3,
            'acciones': acciones,
            'costo': costo_total,
            'lecciones': ['Mantener mayor liquidez', 'Diversificar fuentes de ingresos', 'Plan de contingencia financiera']
        }
    
    def _plan_crisis_reputacional(self) -> Dict[str, Any]:
        """Plan de manejo de crisis reputacional"""
        acciones = []
        costo_total = 0
        
        # 1. Plan de comunicación de crisis
        costo_comunicacion = self.dinero * 0.02
        if costo_comunicacion <= self.dinero:
            self.dinero -= costo_comunicacion
            costo_total += costo_comunicacion
            acciones.append("Plan de comunicación implementado")
        
        # 2. Acciones correctivas
        costo_correctivas = self.dinero * 0.05
        if costo_correctivas <= self.dinero:
            self.dinero -= costo_correctivas
            costo_total += costo_correctivas
            # Recuperar parte de la reputación
            self.gestion_avanzada.responsabilidad_social.reputacion_corporativa = max(0.3,
                self.gestion_avanzada.responsabilidad_social.reputacion_corporativa + 0.1)
            acciones.append("Acciones correctivas implementadas")
        
        # 3. Programa de responsabilidad social intensivo
        for programa in self.gestion_avanzada.responsabilidad_social.programas_rsc:
            if not self.gestion_avanzada.responsabilidad_social.programas_rsc[programa]['activo']:
                self.gestion_avanzada.responsabilidad_social.programas_rsc[programa]['activo'] = True
                acciones.append(f"Programa RSC {programa} activado")
        
        return {
            'exito': len(acciones) >= 2,
            'acciones': acciones,
            'costo': costo_total,
            'lecciones': ['Monitoreo continuo de reputación', 'Comunicación transparente', 'Programas RSC preventivos']
        }
    
    def _plan_crisis_operacional(self) -> Dict[str, Any]:
        """Plan de manejo de crisis operacional"""
        acciones = []
        costo_total = 0
        
        # 1. Implementar procedimientos de emergencia
        if hasattr(self, 'eficiencia_produccion'):
            self.eficiencia_produccion = max(0.5, self.eficiencia_produccion - 0.2)
            acciones.append("Procedimientos de emergencia activados")
        
        # 2. Buscar proveedores alternativos
        costo_nuevos_proveedores = self.dinero * 0.03
        if costo_nuevos_proveedores <= self.dinero:
            self.dinero -= costo_nuevos_proveedores
            costo_total += costo_nuevos_proveedores
            acciones.append("Proveedores alternativos contratados")
        
        # 3. Aumentar inventarios de seguridad
        for bien in self.bienes:
            if self.costos_unitarios.get(bien, 0) > 0:
                unidades_seguridad = 10
                costo_inventario = unidades_seguridad * self.costos_unitarios[bien]
                if costo_inventario <= self.dinero:
                    self.dinero -= costo_inventario
                    costo_total += costo_inventario
                    # Agregar inventario (simplificado)
                    break
        
        acciones.append("Inventarios de seguridad aumentados")
        
        return {
            'exito': len(acciones) >= 2,
            'acciones': acciones,
            'costo': costo_total,
            'lecciones': ['Redundancia en proveedores', 'Inventarios de seguridad', 'Planes de contingencia operativa']
        }
    
    def _plan_crisis_competitiva(self) -> Dict[str, Any]:
        """Plan de manejo de crisis competitiva"""
        acciones = []
        costo_total = 0
        
        # 1. Análisis competitivo intensivo
        self.gestion_avanzada.analisis_competencia.actualizar_analisis_competencia(self.mercado)
        acciones.append("Análisis competitivo actualizado")
        
        # 2. Estrategia de diferenciación
        if len(self.gestion_avanzada.gestion_innovacion.proyectos_activos) < 2:
            oportunidades = self.gestion_avanzada.gestion_innovacion.evaluar_oportunidades_innovacion()
            if oportunidades:
                proyecto = self.gestion_avanzada.gestion_innovacion.iniciar_proyecto_id(oportunidades[0])
                if proyecto:
                    costo_total += proyecto.inversion_total
                    acciones.append("Proyecto de diferenciación iniciado")
        
        # 3. Ajuste de precios estratégico
        for bien in self.precios:
            # Estrategia agresiva de precios
            self.precios[bien] *= random.uniform(0.9, 0.95)
        acciones.append("Estrategia de precios competitivos implementada")
        
        return {
            'exito': len(acciones) >= 2,
            'acciones': acciones,
            'costo': costo_total,
            'lecciones': ['Monitoreo continuo de competencia', 'Diferenciación constante', 'Flexibilidad estratégica']
        }
    
    def _plan_crisis_regulatoria(self) -> Dict[str, Any]:
        """Plan de manejo de crisis regulatoria"""
        acciones = []
        costo_total = 0
        
        # 1. Auditoría legal completa
        costo_auditoria = self.dinero * 0.02
        if costo_auditoria <= self.dinero:
            self.dinero -= costo_auditoria
            costo_total += costo_auditoria
            acciones.append("Auditoría legal completada")
        
        # 2. Actualización de políticas y procedimientos
        costo_actualizacion = self.dinero * 0.01
        if costo_actualizacion <= self.dinero:
            self.dinero -= costo_actualizacion
            costo_total += costo_actualizacion
            acciones.append("Políticas actualizadas")
        
        # 3. Capacitación en cumplimiento
        if self.gestion_avanzada.gestion_rrhh.empleados:
            costo_capacitacion = len(self.gestion_avanzada.gestion_rrhh.empleados) * 500
            if costo_capacitacion <= self.dinero:
                self.dinero -= costo_capacitacion
                costo_total += costo_capacitacion
                acciones.append("Personal capacitado en cumplimiento")
        
        return {
            'exito': len(acciones) >= 2,
            'acciones': acciones,
            'costo': costo_total,
            'lecciones': ['Monitoreo regulatorio continuo', 'Cumplimiento proactivo', 'Relaciones con reguladores']
        }
    
    def ciclo_empresa_hiperrealista(self, ciclo, mercado):
        """Ciclo principal de la empresa hiperrealista"""
        try:
            # Ejecutar ciclo de empresa productora base
            resultado_base = super().ciclo_persona(ciclo, mercado)
            
            # Si la empresa base falló, intentar recuperación
            if resultado_base is False:
                logging.warning(f"{self.nombre}: Ciclo base falló, iniciando recuperación de crisis")
                crisis_resultado = self.gestionar_crisis_empresarial('financiera')
                if not crisis_resultado['exito']:
                    return False
            
            # Ejecutar gestión avanzada cada ciclo
            resultados_gestion = self.gestion_avanzada.ciclo_gestion_avanzada(mercado)
            
            # Gestionar problemas empresariales
            nuevos_problemas = self.gestor_problemas.evaluar_nuevos_problemas()
            resultados_problemas = self.gestor_problemas.gestionar_problemas_activos()
            
            # Log problemas críticos
            if resultados_problemas['problemas_escalados'] > 0:
                logging.warning(f"{self.nombre}: {resultados_problemas['problemas_escalados']} problemas escalaron")
            if resultados_problemas['problemas_resueltos'] > 0:
                logging.info(f"{self.nombre}: {resultados_problemas['problemas_resueltos']} problemas resueltos")
            
            # Ejecutar plan estratégico cada 12 ciclos (anual)
            if ciclo % 12 == 0:
                plan_estrategico = self.ejecutar_plan_estrategico(mercado)
                logging.info(f"{self.nombre}: Plan estratégico ejecutado - {plan_estrategico['objetivos_cumplidos']} objetivos cumplidos")
            
            # Análisis de performance cada 6 ciclos (semestral)
            if ciclo % 6 == 0:
                performance = self.analizar_performance_empresarial()
                logging.info(f"{self.nombre}: Performance empresarial - {performance['calificacion_general']:.1f}/100")
                
                # Implementar recomendaciones automáticamente si performance es baja
                if performance['calificacion_general'] < 60:
                    self._implementar_mejoras_automaticas(performance['recomendaciones'])
            
            # Actualizar clasificación de empresa
            self._clasificar_empresa()
            
            # Log de estado empresarial
            if ciclo % 3 == 0:  # Cada 3 ciclos
                self._log_estado_empresarial(resultados_gestion)
            
            return True
            
        except Exception as e:
            logging.error(f"Error en ciclo hiperrealista de {self.nombre}: {e}")
            return False
    
    def _implementar_mejoras_automaticas(self, recomendaciones: List[str]):
        """Implementa mejoras automáticas basadas en recomendaciones"""
        for recomendacion in recomendaciones[:3]:  # Máximo 3 mejoras por ciclo
            if "liquidez" in recomendacion.lower() and self.dinero > 1000:
                # Buscar financiamiento de emergencia
                if hasattr(self.mercado, 'sistema_bancario'):
                    banco = self.mercado.sistema_bancario.bancos[0] if self.mercado.sistema_bancario.bancos else None
                    if banco:
                        banco.solicitar_prestamo(self, self.costos_fijos_mensuales * 3, 24)
            
            elif "productividad" in recomendacion.lower():
                # Implementar programa de capacitación automático
                self.gestion_avanzada.gestion_rrhh.gestionar_capacitacion()
            
            elif "innovación" in recomendacion.lower() or "i+d" in recomendacion.lower():
                # Iniciar proyecto de I+D automáticamente
                oportunidades = self.gestion_avanzada.gestion_innovacion.evaluar_oportunidades_innovacion()
                if oportunidades:
                    self.gestion_avanzada.gestion_innovacion.iniciar_proyecto_id(oportunidades[0])
    
    def _log_estado_empresarial(self, resultados_gestion: Dict[str, Any]):
        """Log del estado empresarial"""
        empleados = resultados_gestion['rrhh']['empleados_actuales']
        productividad = resultados_gestion['rrhh']['productividad_total']
        proyectos_id = resultados_gestion['innovacion']['proyectos_activos']
        reputacion = resultados_gestion['rsc']['reputacion_corporativa']
        
        logging.info(f"{self.nombre} [{self.tamaño_empresa}]: ${self.dinero:,.0f} | "
                    f"{empleados} empleados (prod: {productividad:.2f}) | "
                    f"{proyectos_id} proyectos I+D | "
                    f"Reputación: {reputacion:.2f}")
    
    def obtener_reporte_empresarial_completo(self) -> Dict[str, Any]:
        """Obtiene un reporte empresarial completo"""
        performance = self.analizar_performance_empresarial()
        estadisticas_gestion = self.gestion_avanzada.obtener_estadisticas_completas()
        
        return {
            'informacion_general': {
                'nombre': self.nombre,
                'sector': self.sector_principal,
                'tamaño': self.tamaño_empresa,
                'fundacion': self.fundacion_año,
                'mision': self.mision_corporativa,
                'vision': self.vision_corporativa
            },
            'situacion_financiera': {
                'capital_actual': self.dinero,
                'metricas': self.metricas_financieras,
                'evaluacion': performance['salud_financiera']
            },
            'recursos_humanos': estadisticas_gestion['empleados'],
            'innovacion_desarrollo': estadisticas_gestion['innovacion'],
            'gestion_riesgos': estadisticas_gestion['riesgos'],
            'competencia': estadisticas_gestion['competencia'],
            'responsabilidad_social': {
                'reputacion': self.gestion_avanzada.responsabilidad_social.reputacion_corporativa,
                'programas_activos': sum(1 for p in self.gestion_avanzada.responsabilidad_social.programas_rsc.values() if p['activo']),
                'certificaciones': self.certificaciones
            },
            'performance_integral': {
                'calificacion_general': performance['calificacion_general'],
                'areas_evaluadas': {k: v['score'] for k, v in performance.items() if isinstance(v, dict) and 'score' in v},
                'recomendaciones': performance['recomendaciones']
            },
            'logros_historicos': {
                'decisiones_estrategicas': len(self.decisiones_estrategicas),
                'crisis_superadas': len(self.crisis_superadas),
                'proyectos_completados': len(self.gestion_avanzada.gestion_innovacion.proyectos_completados)
            },
            'estructura_organizacional': self.estructura_organizacional,
            'kpis_actuales': estadisticas_gestion['kpis']
        }

    def __str__(self):
        return (f"EmpresaHiperrealista {self.nombre} [{self.tamaño_empresa}] - "
                f"Capital: ${self.dinero:,.2f} - Sector: {self.sector_principal} - "
                f"Empleados: {len(self.empleados)} - "
                f"Reputación: {self.gestion_avanzada.responsabilidad_social.reputacion_corporativa:.2f}")
