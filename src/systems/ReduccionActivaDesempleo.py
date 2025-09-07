"""
Sistema Avanzado de Reducción de Desempleo
Implementa políticas activas y adaptativas para mejorar el empleo
"""

import logging
import random
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import numpy as np

@dataclass
class ConfigReduccionDesempleo:
    """Configuración para políticas de empleo"""
    desempleo_objetivo: float = 0.05  # 5% desempleo natural
    desempleo_critico: float = 0.15   # 15% nivel crítico
    tasa_reduccion_base: float = 0.03
    factor_estimulo_empresas: float = 0.1
    subsidio_empleo_por_trabajador: float = 200.0
    duracion_subsidio_ciclos: int = 8
    inversion_obras_publicas: float = 5000.0
    multiplicador_keynesiano: float = 1.8

class ReduccionActivaDesempleo:
    """Sistema de políticas activas contra el desempleo"""
    
    def __init__(self, config: ConfigReduccionDesempleo = None):
        self.config = config or ConfigReduccionDesempleo()
        self.logger = logging.getLogger(__name__)
        self.subsidios_activos = {}
        self.obras_publicas = {}
        self.programas_capacitacion_laboral = {}
        self.historia_desempleo = []
        self.presupuesto_politicas = 50000.0
        
    def reducir_desempleo_ciclo(self, simulador, ciclo: int) -> Dict[str, Any]:
        """Aplica políticas de reducción de desempleo en cada ciclo"""
        resultados = {
            'desempleo_inicial': 0.0,
            'desempleo_final': 0.0,
            'reduccion_lograda': 0.0,
            'politicas_aplicadas': [],
            'empleos_creados': 0,
            'inversion_total': 0.0,
            'empresas_beneficiadas': 0
        }
        
        try:
            # Obtener desempleo actual
            desempleo_inicial = self._obtener_desempleo(simulador)
            resultados['desempleo_inicial'] = desempleo_inicial
            
            # Evaluar necesidad de políticas
            evaluacion = self._evaluar_necesidad_politicas(desempleo_inicial)
            
            # Aplicar políticas según necesidad
            if evaluacion['necesaria']:
                for politica in evaluacion['politicas_recomendadas']:
                    resultado_politica = self._aplicar_politica(simulador, politica, ciclo)
                    
                    if resultado_politica['exitosa']:
                        resultados['politicas_aplicadas'].append(politica)
                        resultados['empleos_creados'] += resultado_politica['empleos_creados']
                        resultados['inversion_total'] += resultado_politica['inversion']
                        resultados['empresas_beneficiadas'] += resultado_politica['empresas_afectadas']
            
            # Calcular desempleo final
            desempleo_final = self._obtener_desempleo(simulador)
            resultados['desempleo_final'] = desempleo_final
            resultados['reduccion_lograda'] = max(0, desempleo_inicial - desempleo_final)
            
            # Actualizar historial
            self._actualizar_historial(desempleo_inicial, desempleo_final, resultados)
            
            if resultados['empleos_creados'] > 0:
                self.logger.info(f"👥 Reducción desempleo: {resultados['empleos_creados']} empleos, "
                               f"{desempleo_inicial:.1%} → {desempleo_final:.1%}")
            
        except Exception as e:
            self.logger.error(f"Error reduciendo desempleo: {e}")
            
        return resultados
    
    def _obtener_desempleo(self, simulador) -> float:
        """Obtiene la tasa de desempleo actual"""
        if hasattr(simulador, 'desempleo'):
            return simulador.desempleo
        elif hasattr(simulador, 'mercado_laboral'):
            return getattr(simulador.mercado_laboral, 'tasa_desempleo', 0.0)
        else:
            # Calcular basado en empresas y empleados
            total_empleados = 0
            for empresa in simulador.getEmpresas():
                # Verificar si la empresa está "activa"
                empresa_activa = True
                if hasattr(empresa, 'en_quiebra') and empresa.en_quiebra:
                    empresa_activa = False
                elif empresa.dinero <= 1000:
                    empresa_activa = False
                
                if empresa_activa and hasattr(empresa, 'empleados'):
                    total_empleados += len(empresa.empleados)
            
            # Estimar población activa (asumiendo 100 como base)
            poblacion_activa = 100
            empleados_totales = max(1, total_empleados)
            return max(0, (poblacion_activa - empleados_totales) / poblacion_activa)
    
    def _evaluar_necesidad_politicas(self, desempleo: float) -> Dict[str, Any]:
        """Evalúa qué políticas aplicar según el nivel de desempleo"""
        evaluacion = {
            'necesaria': False,
            'urgencia': 0,
            'politicas_recomendadas': []
        }
        
        if desempleo <= self.config.desempleo_objetivo:
            # Desempleo normal, no necesita intervención
            return evaluacion
        
        evaluacion['necesaria'] = True
        
        if desempleo > self.config.desempleo_critico:
            # Situación crítica - aplicar todas las políticas
            evaluacion['urgencia'] = 3
            evaluacion['politicas_recomendadas'] = [
                'subsidios_empresas',
                'obras_publicas',
                'capacitacion_laboral',
                'estimulo_contratacion'
            ]
        elif desempleo > self.config.desempleo_objetivo * 2:
            # Situación preocupante - políticas moderadas
            evaluacion['urgencia'] = 2
            evaluacion['politicas_recomendadas'] = [
                'subsidios_empresas',
                'estimulo_contratacion'
            ]
            
            # Añadir obras públicas con probabilidad
            if random.random() < 0.6:
                evaluacion['politicas_recomendadas'].append('obras_publicas')
        else:
            # Situación leve - políticas suaves
            evaluacion['urgencia'] = 1
            evaluacion['politicas_recomendadas'] = ['estimulo_contratacion']
            
            # Añadir subsidios con probabilidad
            if random.random() < 0.4:
                evaluacion['politicas_recomendadas'].append('subsidios_empresas')
        
        return evaluacion
    
    def _aplicar_politica(self, simulador, politica: str, ciclo: int) -> Dict[str, Any]:
        """Aplica una política específica"""
        resultado = {
            'exitosa': False,
            'empleos_creados': 0,
            'inversion': 0.0,
            'empresas_afectadas': 0,
            'detalles': ''
        }
        
        try:
            if politica == 'subsidios_empresas':
                resultado = self._aplicar_subsidios_empresas(simulador, ciclo)
            elif politica == 'obras_publicas':
                resultado = self._aplicar_obras_publicas(simulador, ciclo)
            elif politica == 'capacitacion_laboral':
                resultado = self._aplicar_capacitacion_laboral(simulador, ciclo)
            elif politica == 'estimulo_contratacion':
                resultado = self._aplicar_estimulo_contratacion(simulador, ciclo)
                
        except Exception as e:
            self.logger.error(f"Error aplicando política {politica}: {e}")
            resultado['detalles'] = f"Error: {e}"
            
        return resultado
    
    def _aplicar_subsidios_empresas(self, simulador, ciclo: int) -> Dict[str, Any]:
        """Aplica subsidios a empresas para fomentar contratación"""
        resultado = {
            'exitosa': False,
            'empleos_creados': 0,
            'inversion': 0.0,
            'empresas_afectadas': 0,
            'detalles': ''
        }
        
        empresas_elegibles = [e for e in simulador.getEmpresas() if e.activa]
        empresas_beneficiadas = 0
        inversion_total = 0.0
        empleos_totales = 0
        
        for empresa in empresas_elegibles:
            # Calcular subsidio proporcional
            empleados_actuales = len(getattr(empresa, 'empleados', []))
            subsidio_empresa = empleados_actuales * self.config.subsidio_empleo_por_trabajador
            
            # Verificar presupuesto disponible
            if self.presupuesto_politicas >= subsidio_empresa:
                # Aplicar subsidio
                if hasattr(empresa, 'capital'):
                    empresa.capital += subsidio_empresa
                
                # Estimular contratación (probabilidad de contratar)
                empleos_nuevos = 0
                if random.random() < self.config.factor_estimulo_empresas:
                    empleos_nuevos = random.randint(1, max(1, empleados_actuales // 3))
                    
                    # Añadir empleados
                    if hasattr(empresa, 'empleados'):
                        nuevos_empleados = [f"SubsidioEmpleado_{ciclo}_{i}" for i in range(empleos_nuevos)]
                        empresa.empleados.extend(nuevos_empleados)
                
                # Registrar subsidio
                self.subsidios_activos[f"{empresa.id}_{ciclo}"] = {
                    'empresa': empresa.id,
                    'monto': subsidio_empresa,
                    'empleos_estimulados': empleos_nuevos,
                    'ciclo_inicio': ciclo,
                    'duracion': self.config.duracion_subsidio_ciclos
                }
                
                self.presupuesto_politicas -= subsidio_empresa
                inversion_total += subsidio_empresa
                empleos_totales += empleos_nuevos
                empresas_beneficiadas += 1
        
        if empresas_beneficiadas > 0:
            resultado['exitosa'] = True
            resultado['empleos_creados'] = empleos_totales
            resultado['inversion'] = inversion_total
            resultado['empresas_afectadas'] = empresas_beneficiadas
            resultado['detalles'] = f"Subsidios a {empresas_beneficiadas} empresas"
        
        return resultado
    
    def _aplicar_obras_publicas(self, simulador, ciclo: int) -> Dict[str, Any]:
        """Implementa obras públicas para generar empleo directo"""
        resultado = {
            'exitosa': False,
            'empleos_creados': 0,
            'inversion': 0.0,
            'empresas_afectadas': 0,
            'detalles': ''
        }
        
        # Verificar presupuesto
        if self.presupuesto_politicas < self.config.inversion_obras_publicas:
            resultado['detalles'] = "Presupuesto insuficiente para obras públicas"
            return resultado
        
        # Crear proyecto de obras públicas
        empleos_directos = int(self.config.inversion_obras_publicas / 2000)  # $2000 por empleo
        empleos_indirectos = int(empleos_directos * (self.config.multiplicador_keynesiano - 1))
        
        # Aplicar multiplicador keynesiano distribuyendo empleos indirectos
        empresas_beneficiadas = 0
        empresas_disponibles = []
        for e in simulador.getEmpresas():
            # Verificar si la empresa está "activa"
            if hasattr(e, 'en_quiebra') and not e.en_quiebra and e.dinero > 5000:
                empresas_disponibles.append(e)
            elif not hasattr(e, 'en_quiebra') and e.dinero > 5000:
                empresas_disponibles.append(e)
        
        for empresa in random.sample(empresas_disponibles, 
                                   min(3, len(empresas_disponibles))):
            # Verificar nuevamente que está activa
            empresa_activa = True
            if hasattr(empresa, 'en_quiebra') and empresa.en_quiebra:
                empresa_activa = False
            elif empresa.dinero <= 5000:
                empresa_activa = False
                
            if empresa_activa:
                empleos_empresa = empleos_indirectos // 3
                if empleos_empresa > 0 and hasattr(empresa, 'empleados'):
                    nuevos_empleados = [f"ObrasPublicas_{ciclo}_{i}" for i in range(empleos_empresa)]
                    empresa.empleados.extend(nuevos_empleados)
                    empresas_beneficiadas += 1
        
        # Registrar obra pública
        self.obras_publicas[f"Obra_{ciclo}"] = {
            'inversion': self.config.inversion_obras_publicas,
            'empleos_directos': empleos_directos,
            'empleos_indirectos': empleos_indirectos,
            'ciclo': ciclo
        }
        
        self.presupuesto_politicas -= self.config.inversion_obras_publicas
        
        resultado['exitosa'] = True
        resultado['empleos_creados'] = empleos_directos + empleos_indirectos
        resultado['inversion'] = self.config.inversion_obras_publicas
        resultado['empresas_afectadas'] = empresas_beneficiadas
        resultado['detalles'] = f"Obra pública: {empleos_directos} directos + {empleos_indirectos} indirectos"
        
        return resultado
    
    def _aplicar_capacitacion_laboral(self, simulador, ciclo: int) -> Dict[str, Any]:
        """Aplica programas de capacitación laboral"""
        resultado = {
            'exitosa': False,
            'empleos_creados': 0,
            'inversion': 1000.0,
            'empresas_afectadas': 0,
            'detalles': ''
        }
        
        # Simular programa de capacitación que mejora empleabilidad
        if self.presupuesto_politicas >= resultado['inversion']:
            # Capacitación mejora probabilidades de contratación futuras
            personas_capacitadas = random.randint(10, 25)
            
            # Registro del programa
            self.programas_capacitacion_laboral[f"Capacitacion_{ciclo}"] = {
                'personas': personas_capacitadas,
                'inversion': resultado['inversion'],
                'ciclo': ciclo,
                'efectividad': random.uniform(0.7, 0.9)
            }
            
            # Efecto indirecto: algunas personas encuentran trabajo
            empleos_logrados = int(personas_capacitadas * 0.3)  # 30% efectividad
            
            # Distribuir empleos en empresas aleatorias
            empresas_contratantes = 0
            empresas_disponibles = [e for e in simulador.getEmpresas() if e.activa]
            
            for _ in range(min(empleos_logrados, len(empresas_disponibles))):
                empresa = random.choice(empresas_disponibles)
                if hasattr(empresa, 'empleados'):
                    empresa.empleados.append(f"CapacitadoEmpleado_{ciclo}")
                    empleos_logrados += 1
                    empresas_contratantes += 1
            
            self.presupuesto_politicas -= resultado['inversion']
            
            resultado['exitosa'] = True
            resultado['empleos_creados'] = empleos_logrados
            resultado['empresas_afectadas'] = empresas_contratantes
            resultado['detalles'] = f"Capacitación: {personas_capacitadas} personas, {empleos_logrados} empleos"
        
        return resultado
    
    def _aplicar_estimulo_contratacion(self, simulador, ciclo: int) -> Dict[str, Any]:
        """Aplica estímulos directos a la contratación"""
        resultado = {
            'exitosa': False,
            'empleos_creados': 0,
            'inversion': 0.0,
            'empresas_afectadas': 0,
            'detalles': ''
        }
        
        empleos_totales = 0
        empresas_afectadas = 0
        
        # Recorrer empresas y estimular contratación
        for empresa in simulador.getEmpresas():
            # Verificar si la empresa está "activa"
            empresa_activa = True
            if hasattr(empresa, 'en_quiebra') and empresa.en_quiebra:
                empresa_activa = False
            elif empresa.dinero <= 5000:  # Necesita capital para contratar
                empresa_activa = False
                
            if not empresa_activa:
                continue
                
            empleados_actuales = len(getattr(empresa, 'empleados', []))
            
            # Probabilidad de contratación basada en tamaño de empresa
            probabilidad = min(0.4, self.config.tasa_reduccion_base + (empleados_actuales * 0.01))
            
            if random.random() < probabilidad:
                nuevos_empleos = random.randint(1, max(1, empleados_actuales // 4))
                
                if hasattr(empresa, 'empleados'):
                    nuevos_empleados = [f"EstimuloEmpleado_{ciclo}_{i}" for i in range(nuevos_empleos)]
                    empresa.empleados.extend(nuevos_empleados)
                    
                    empleos_totales += nuevos_empleos
                    empresas_afectadas += 1
        
        if empleos_totales > 0:
            resultado['exitosa'] = True
            resultado['empleos_creados'] = empleos_totales
            resultado['empresas_afectadas'] = empresas_afectadas
            resultado['detalles'] = f"Estímulo general: {empleos_totales} empleos en {empresas_afectadas} empresas"
        
        return resultado
    
    def _actualizar_historial(self, desempleo_inicial: float, desempleo_final: float, resultados: Dict):
        """Actualiza el historial de políticas de empleo"""
        registro = {
            'desempleo_inicial': desempleo_inicial,
            'desempleo_final': desempleo_final,
            'reduccion': resultados['reduccion_lograda'],
            'politicas': resultados['politicas_aplicadas'],
            'empleos_creados': resultados['empleos_creados'],
            'inversion': resultados['inversion_total']
        }
        
        self.historia_desempleo.append(registro)
        
        # Mantener solo últimos 20 registros
        if len(self.historia_desempleo) > 20:
            self.historia_desempleo = self.historia_desempleo[-20:]
        
        # Renovar presupuesto gradualmente
        self.presupuesto_politicas = min(
            100000.0,  # Máximo presupuesto
            self.presupuesto_politicas + 2000.0  # Renovación por ciclo
        )
    
    def obtener_reporte_empleo(self) -> Dict[str, Any]:
        """Genera reporte detallado de políticas de empleo"""
        historia_reciente = self.historia_desempleo[-5:] if self.historia_desempleo else []
        
        return {
            'subsidios_activos': len(self.subsidios_activos),
            'obras_publicas': len(self.obras_publicas),
            'programas_capacitacion': len(self.programas_capacitacion_laboral),
            'presupuesto_disponible': self.presupuesto_politicas,
            'empleos_creados_total': sum(h['empleos_creados'] for h in self.historia_desempleo),
            'inversion_total': sum(h['inversion'] for h in self.historia_desempleo),
            'configuracion': {
                'desempleo_objetivo': self.config.desempleo_objetivo,
                'desempleo_critico': self.config.desempleo_critico,
                'subsidio_por_trabajador': self.config.subsidio_empleo_por_trabajador,
                'inversion_obras_publicas': self.config.inversion_obras_publicas
            },
            'historia_reciente': historia_reciente
        }
