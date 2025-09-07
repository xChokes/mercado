"""
Sistema de Control de Concentración Empresarial
Previene monopolización mediante creación dinámica de empresas
"""

import logging
import random
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import numpy as np

@dataclass
class ConfigCreacionEmpresas:
    """Configuración para creación dinámica de empresas"""
    empresas_minimas: int = 3
    empresas_optimas: int = 8
    probabilidad_base_creacion: float = 0.20
    capital_inicial_minimo: float = 25000.0
    capital_inicial_maximo: float = 100000.0
    factor_mercado: float = 0.1
    umbral_concentracion_hhi: float = 0.6
    cooldown_creacion_ciclos: int = 5

class ControladorConcentracionEmpresarial:
    """Sistema que previene monopolización y fomenta competencia"""
    
    def __init__(self, config: ConfigCreacionEmpresas = None):
        self.config = config or ConfigCreacionEmpresas()
        self.logger = logging.getLogger(__name__)
        self.empresas_creadas = {}
        self.ultimo_ciclo_creacion = {}
        self.contador_empresas_globales = 0
        self.historia_concentracion = []
        
    def controlar_concentracion_ciclo(self, simulador, ciclo: int) -> Dict[str, Any]:
        """Controla la concentración empresarial en cada ciclo"""
        resultados = {
            'empresas_creadas': 0,
            'empresas_activas': 0,
            'hhi_actual': 0.0,
            'necesidad_intervencion': False,
            'razon_intervencion': '',
            'detalles_empresas': []
        }
        
        try:
            # Analizar estado actual
            analisis = self._analizar_concentracion(simulador)
            resultados.update(analisis)
            
            # Determinar necesidad de intervención
            necesidad = self._evaluar_necesidad_intervencion(analisis, ciclo)
            resultados['necesidad_intervencion'] = necesidad['necesaria']
            resultados['razon_intervencion'] = necesidad['razon']
            
            # Crear empresas si es necesario
            if necesidad['necesaria']:
                empresas_nuevas = self._crear_empresas_estrategicas(simulador, necesidad, ciclo)
                resultados['empresas_creadas'] = len(empresas_nuevas)
                resultados['detalles_empresas'] = empresas_nuevas
                
            # Actualizar historial
            self._actualizar_historial(analisis)
            
            if resultados['empresas_creadas'] > 0:
                self.logger.info(f"🏢 Control concentración: {resultados['empresas_creadas']} empresas creadas, "
                               f"HHI: {resultados['hhi_actual']:.3f}")
            
        except Exception as e:
            self.logger.error(f"Error controlando concentración empresarial: {e}")
            
        return resultados
    
    def _analizar_concentracion(self, simulador) -> Dict[str, Any]:
        """Analiza el nivel actual de concentración del mercado"""
        # Obtener empresas activas (no en quiebra y con dinero suficiente)
        empresas = simulador.getEmpresas()
        empresas_activas = []
        for e in empresas:
            # Una empresa está "activa" si no está en quiebra y tiene recursos mínimos
            if hasattr(e, 'en_quiebra') and not e.en_quiebra and e.dinero > 1000:
                empresas_activas.append(e)
            elif not hasattr(e, 'en_quiebra') and e.dinero > 1000:
                empresas_activas.append(e)
        
        if len(empresas_activas) < 2:
            return analisis  # No hay suficientes empresas para analizar concentración
        
        analisis = {
            'empresas_activas': len(empresas_activas),
            'hhi_actual': 0.0,
            'empresa_dominante_cuota': 0.0,
            'distribucion_tamanos': [],
            'mercado_total': 0.0
        }
        
        if not empresas_activas:
            return analisis
        
        # Calcular cuotas de mercado (basado en capital o empleados)
        tamanos_empresas = []
        for empresa in empresas_activas:
            tamano = self._calcular_tamano_empresa(empresa)
            tamanos_empresas.append(tamano)
        
        analisis['mercado_total'] = sum(tamanos_empresas)
        
        if analisis['mercado_total'] > 0:
            # Calcular cuotas de mercado
            cuotas = [tamano / analisis['mercado_total'] for tamano in tamanos_empresas]
            analisis['distribucion_tamanos'] = cuotas
            
            # Calcular Índice Herfindahl-Hirschman (HHI)
            analisis['hhi_actual'] = sum(cuota ** 2 for cuota in cuotas)
            
            # Empresa dominante
            analisis['empresa_dominante_cuota'] = max(cuotas) if cuotas else 0.0
        
        return analisis
    
    def _calcular_tamano_empresa(self, empresa) -> float:
        """Calcula el tamaño relativo de una empresa"""
        # Priorizar diferentes métricas según disponibilidad
        if hasattr(empresa, 'empleados') and empresa.empleados:
            return len(empresa.empleados) * 1000  # Factor de escala
        elif hasattr(empresa, 'capital'):
            return empresa.capital
        elif hasattr(empresa, 'produccion'):
            return empresa.produccion
        elif hasattr(empresa, 'capacidad_produccion'):
            return empresa.capacidad_produccion
        else:
            return 1000.0  # Valor por defecto
    
    def _evaluar_necesidad_intervencion(self, analisis: Dict, ciclo: int) -> Dict[str, Any]:
        """Evalúa si se necesita intervención anti-monopolio"""
        evaluacion = {
            'necesaria': False,
            'razon': '',
            'urgencia': 0,
            'empresas_a_crear': 0
        }
        
        # Criterio 1: Muy pocas empresas activas
        if analisis['empresas_activas'] < self.config.empresas_minimas:
            evaluacion['necesaria'] = True
            evaluacion['razon'] = f"Muy pocas empresas ({analisis['empresas_activas']} < {self.config.empresas_minimas})"
            evaluacion['urgencia'] = 3
            evaluacion['empresas_a_crear'] = self.config.empresas_minimas - analisis['empresas_activas']
        
        # Criterio 2: Alto índice de concentración HHI
        elif analisis['hhi_actual'] > self.config.umbral_concentracion_hhi:
            evaluacion['necesaria'] = True
            evaluacion['razon'] = f"Alta concentración HHI ({analisis['hhi_actual']:.3f} > {self.config.umbral_concentracion_hhi})"
            evaluacion['urgencia'] = 2
            evaluacion['empresas_a_crear'] = min(3, self.config.empresas_optimas - analisis['empresas_activas'])
        
        # Criterio 3: Empresa dominante con cuota muy alta
        elif analisis['empresa_dominante_cuota'] > 0.7:
            evaluacion['necesaria'] = True
            evaluacion['razon'] = f"Empresa dominante ({analisis['empresa_dominante_cuota']:.1%} cuota)"
            evaluacion['urgencia'] = 2
            evaluacion['empresas_a_crear'] = 2
        
        # Criterio 4: Oportunidad de mercado (pocas empresas pero no crítico)
        elif analisis['empresas_activas'] < self.config.empresas_optimas:
            # Probabilidad basada en condiciones de mercado
            probabilidad_mercado = self.config.probabilidad_base_creacion * (
                1 + (self.config.empresas_optimas - analisis['empresas_activas']) * self.config.factor_mercado
            )
            
            if random.random() < probabilidad_mercado:
                evaluacion['necesaria'] = True
                evaluacion['razon'] = "Oportunidad de mercado"
                evaluacion['urgencia'] = 1
                evaluacion['empresas_a_crear'] = 1
        
        # Verificar cooldown
        if evaluacion['necesaria']:
            tiempo_desde_ultima = ciclo - self.ultimo_ciclo_creacion.get('global', 0)
            if tiempo_desde_ultima < self.config.cooldown_creacion_ciclos:
                evaluacion['necesaria'] = False
                evaluacion['razon'] += " (cooldown activo)"
        
        return evaluacion
    
    def _crear_empresas_estrategicas(self, simulador, necesidad: Dict, ciclo: int) -> List[Dict]:
        """Crea nuevas empresas de manera estratégica"""
        empresas_creadas = []
        
        for i in range(necesidad['empresas_a_crear']):
            try:
                nueva_empresa = self._crear_empresa_individual(simulador, i, ciclo, necesidad['urgencia'])
                if nueva_empresa:
                    empresas_creadas.append(nueva_empresa)
                    
            except Exception as e:
                self.logger.error(f"Error creando empresa {i}: {e}")
        
        # Actualizar cooldown
        if empresas_creadas:
            self.ultimo_ciclo_creacion['global'] = ciclo
            
        return empresas_creadas
    
    def _crear_empresa_individual(self, simulador, indice: int, ciclo: int, urgencia: int) -> Optional[Dict]:
        """Crea una empresa individual optimizada"""
        try:
            from src.models.Empresa import Empresa
            
            # Generar parámetros de la empresa
            empresa_id = f"Antimonopolio_{ciclo}_{indice}"
            
            # Capital inicial basado en urgencia y mercado
            capital_base = random.uniform(
                self.config.capital_inicial_minimo,
                self.config.capital_inicial_maximo
            )
            
            # Ajustar capital según urgencia
            multiplicador_urgencia = {1: 1.0, 2: 1.3, 3: 1.6}.get(urgencia, 1.0)
            capital_inicial = capital_base * multiplicador_urgencia
            
            # Crear empresa
            nueva_empresa = Empresa(
                id=empresa_id,
                capital=capital_inicial,
                capacidad_produccion=random.randint(100, 300)
            )
            
            # Configurar parámetros optimizados
            self._configurar_empresa_competitiva(nueva_empresa, simulador, urgencia)
            
            # Añadir al mercado
            simulador.agregar_persona(nueva_empresa)
            
            # Registrar creación
            detalles = {
                'id': empresa_id,
                'capital': capital_inicial,
                'capacidad': nueva_empresa.capacidad_produccion,
                'urgencia': urgencia,
                'ciclo_creacion': ciclo
            }
            
            self.empresas_creadas[empresa_id] = detalles
            self.contador_empresas_globales += 1
            
            return detalles
            
        except Exception as e:
            self.logger.error(f"Error creando empresa individual: {e}")
            return None
    
    def _configurar_empresa_competitiva(self, empresa, simulador, urgencia: int):
        """Configura una empresa para ser competitiva"""
        # Configuración básica
        empresa.activa = True
        
        # Eficiencia basada en análisis del mercado
        if hasattr(empresa, 'eficiencia'):
            # Eficiencia ligeramente superior para compensar desventaja inicial
            empresa.eficiencia = random.uniform(0.75, 0.95)
        
        # Productividad laboral competitiva
        if hasattr(empresa, 'productividad_laboral'):
            empresa.productividad_laboral = random.uniform(0.85, 1.05)
        
        # Empleados iniciales
        if hasattr(empresa, 'empleados'):
            num_empleados_inicial = random.randint(5, 20)
            empresa.empleados = [f"Empleado_{i}" for i in range(num_empleados_inicial)]
        
        # Estrategia inicial de precios (ligeramente competitiva)
        if hasattr(empresa, 'factor_precio'):
            empresa.factor_precio = random.uniform(0.9, 1.1)
        
        # Especialización en productos menos saturados
        if hasattr(simulador, 'bienes') and simulador.bienes:
            # Seleccionar productos con menor competencia
            productos_disponibles = []
            for bien_nombre in simulador.bienes.keys():
                # Contar productores existentes
                productores = sum(1 for e in simulador.getEmpresas() 
                                if hasattr(e, 'productos_fabricados') and bien_nombre in e.productos_fabricados)
                productos_disponibles.append((bien_nombre, productores))
            
            # Ordenar por menor competencia
            productos_disponibles.sort(key=lambda x: x[1])
            
            # Asignar productos menos competidos
            if productos_disponibles and hasattr(empresa, 'productos_fabricados'):
                productos_a_fabricar = [p[0] for p in productos_disponibles[:random.randint(1, 3)]]
                empresa.productos_fabricados = productos_a_fabricar
    
    def _actualizar_historial(self, analisis: Dict):
        """Actualiza el historial de concentración"""
        self.historia_concentracion.append({
            'empresas_activas': analisis['empresas_activas'],
            'hhi': analisis['hhi_actual'],
            'cuota_dominante': analisis['empresa_dominante_cuota']
        })
        
        # Mantener solo últimos 30 registros
        if len(self.historia_concentracion) > 30:
            self.historia_concentracion = self.historia_concentracion[-30:]
    
    def obtener_reporte_concentracion(self) -> Dict[str, Any]:
        """Genera reporte detallado de concentración"""
        historia_reciente = self.historia_concentracion[-10:] if self.historia_concentracion else []
        
        return {
            'empresas_creadas_total': len(self.empresas_creadas),
            'empresas_activas_promedio': np.mean([h['empresas_activas'] for h in historia_reciente]) if historia_reciente else 0,
            'hhi_promedio': np.mean([h['hhi'] for h in historia_reciente]) if historia_reciente else 0,
            'configuracion': {
                'empresas_minimas': self.config.empresas_minimas,
                'empresas_optimas': self.config.empresas_optimas,
                'umbral_hhi': self.config.umbral_concentracion_hhi,
                'cooldown_ciclos': self.config.cooldown_creacion_ciclos
            },
            'historia_reciente': historia_reciente,
            'empresas_creadas_detalles': list(self.empresas_creadas.values())[-5:]
        }
