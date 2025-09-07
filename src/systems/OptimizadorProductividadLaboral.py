"""
Módulo de Optimización de Productividad Laboral
Implementa mejoras graduales y sostenibles en la productividad
"""

import logging
import random
from typing import Dict, List, Any, Optional, Tuple
import numpy as np
from dataclasses import dataclass

@dataclass
class ConfigProductividad:
    """Configuración para optimización de productividad"""
    productividad_minima_objetivo: float = 0.90
    productividad_maxima_objetivo: float = 1.10
    tasa_mejora_base: float = 0.003
    factor_experiencia: float = 0.001
    factor_tecnologia: float = 0.002
    factor_capacitacion: float = 0.005
    ciclos_capacitacion: int = 15
    inversion_tecnologia_minima: float = 1000.0

class OptimizadorProductividadLaboral:
    """Sistema avanzado de optimización de productividad laboral"""
    
    def __init__(self, config: ConfigProductividad = None):
        self.config = config or ConfigProductividad()
        self.logger = logging.getLogger(__name__)
        self.historia_productividad = {}
        self.programas_capacitacion = {}
        self.inversiones_tecnologia = {}
        
    def optimizar_productividad_ciclo(self, simulador, ciclo: int) -> Dict[str, Any]:
        """Optimiza la productividad en cada ciclo"""
        resultados = {
            'empresas_mejoradas': 0,
            'mejora_promedio': 0.0,
            'programas_capacitacion': 0,
            'inversiones_tecnologia': 0,
            'productividad_sistema': 0.0
        }
        
        try:
            for empresa in simulador.getEmpresas():
                # Verificar si la empresa está "activa" (no en quiebra y con recursos)
                empresa_activa = True
                if hasattr(empresa, 'en_quiebra') and empresa.en_quiebra:
                    empresa_activa = False
                elif empresa.dinero <= 1000:
                    empresa_activa = False
                
                if not empresa_activa:
                    continue
                    
                mejoras_aplicadas = self._optimizar_empresa(empresa, ciclo)
                
                if mejoras_aplicadas['mejora_aplicada']:
                    resultados['empresas_mejoradas'] += 1
                    resultados['mejora_promedio'] += mejoras_aplicadas['mejora_cantidad']
                    
                if mejoras_aplicadas['capacitacion']:
                    resultados['programas_capacitacion'] += 1
                    
                if mejoras_aplicadas['inversion_tech']:
                    resultados['inversiones_tecnologia'] += 1
            
            # Calcular mejora promedio
            if resultados['empresas_mejoradas'] > 0:
                resultados['mejora_promedio'] /= resultados['empresas_mejoradas']
            
            # Calcular productividad del sistema
            resultados['productividad_sistema'] = self._calcular_productividad_sistema(simulador)
            
            self.logger.info(f"🔧 Productividad optimizada: {resultados['empresas_mejoradas']} empresas, "
                           f"mejora {resultados['mejora_promedio']:.3f}")
            
        except Exception as e:
            self.logger.error(f"Error optimizando productividad: {e}")
            
        return resultados
    
    def _optimizar_empresa(self, empresa, ciclo: int) -> Dict[str, Any]:
        """Optimiza la productividad de una empresa específica"""
        resultado = {
            'mejora_aplicada': False,
            'mejora_cantidad': 0.0,
            'capacitacion': False,
            'inversion_tech': False
        }
        
        try:
            productividad_actual = self._obtener_productividad_empresa(empresa)
            
            if productividad_actual < self.config.productividad_minima_objetivo:
                # Aplicar mejoras múltiples
                mejoras_totales = 0.0
                
                # 1. Mejora base graduales
                mejora_base = self.config.tasa_mejora_base
                mejoras_totales += mejora_base
                
                # 2. Mejora por experiencia (acumulativa)
                experiencia = self._calcular_experiencia_empresa(empresa, ciclo)
                mejora_experiencia = experiencia * self.config.factor_experiencia
                mejoras_totales += mejora_experiencia
                
                # 3. Programas de capacitación
                if ciclo % self.config.ciclos_capacitacion == 0:
                    if self._aplicar_capacitacion(empresa):
                        mejoras_totales += self.config.factor_capacitacion
                        resultado['capacitacion'] = True
                
                # 4. Inversión en tecnología
                if self._aplicar_inversion_tecnologia(empresa):
                    mejoras_totales += self.config.factor_tecnologia
                    resultado['inversion_tech'] = True
                
                # Aplicar mejoras con límite superior
                nueva_productividad = min(
                    productividad_actual + mejoras_totales,
                    self.config.productividad_maxima_objetivo
                )
                
                self._aplicar_productividad_empresa(empresa, nueva_productividad)
                
                resultado['mejora_aplicada'] = True
                resultado['mejora_cantidad'] = nueva_productividad - productividad_actual
                
        except Exception as e:
            self.logger.error(f"Error optimizando empresa {empresa.id}: {e}")
            
        return resultado
    
    def _obtener_productividad_empresa(self, empresa) -> float:
        """Obtiene la productividad actual de una empresa"""
        if hasattr(empresa, 'productividad_laboral'):
            return empresa.productividad_laboral
        elif hasattr(empresa, 'eficiencia'):
            return empresa.eficiencia
        elif hasattr(empresa, 'productividad'):
            return empresa.productividad
        else:
            # Calcular productividad estimada basada en otras métricas
            if hasattr(empresa, 'empleados') and hasattr(empresa, 'produccion'):
                if len(empresa.empleados) > 0:
                    return empresa.produccion / len(empresa.empleados) / 1000  # Normalizar
            return 0.5  # Valor por defecto conservador
    
    def _aplicar_productividad_empresa(self, empresa, nueva_productividad: float):
        """Aplica la nueva productividad a la empresa"""
        if hasattr(empresa, 'productividad_laboral'):
            empresa.productividad_laboral = nueva_productividad
        elif hasattr(empresa, 'eficiencia'):
            empresa.eficiencia = nueva_productividad
        elif hasattr(empresa, 'productividad'):
            empresa.productividad = nueva_productividad
        
        # También mejorar capacidad de producción si aplica
        if hasattr(empresa, 'capacidad_produccion'):
            empresa.capacidad_produccion *= (1 + (nueva_productividad - 0.5) * 0.1)
    
    def _calcular_experiencia_empresa(self, empresa, ciclo: int) -> float:
        """Calcula la experiencia acumulada de la empresa"""
        empresa_id = empresa.id
        
        if empresa_id not in self.historia_productividad:
            self.historia_productividad[empresa_id] = []
        
        # Añadir ciclo actual
        productividad_actual = self._obtener_productividad_empresa(empresa)
        self.historia_productividad[empresa_id].append({
            'ciclo': ciclo,
            'productividad': productividad_actual
        })
        
        # Mantener solo últimos 20 ciclos
        if len(self.historia_productividad[empresa_id]) > 20:
            self.historia_productividad[empresa_id] = self.historia_productividad[empresa_id][-20:]
        
        # Calcular experiencia como número de ciclos activos
        return len(self.historia_productividad[empresa_id]) / 20.0
    
    def _aplicar_capacitacion(self, empresa) -> bool:
        """Aplica programa de capacitación a la empresa"""
        try:
            # Verificar si la empresa puede permitirse capacitación
            costo_capacitacion = 500.0 + (len(getattr(empresa, 'empleados', [])) * 50)
            
            if hasattr(empresa, 'capital') and empresa.capital >= costo_capacitacion:
                empresa.capital -= costo_capacitacion
                
                # Registrar programa de capacitación
                self.programas_capacitacion[empresa.id] = {
                    'costo': costo_capacitacion,
                    'empleados': len(getattr(empresa, 'empleados', [])),
                    'activo': True
                }
                
                return True
        except Exception as e:
            self.logger.error(f"Error aplicando capacitación a {empresa.id}: {e}")
            
        return False
    
    def _aplicar_inversion_tecnologia(self, empresa) -> bool:
        """Aplica inversión en tecnología"""
        try:
            # Calcular inversión proporcional al tamaño de la empresa
            inversion_objetivo = max(
                self.config.inversion_tecnologia_minima,
                getattr(empresa, 'capital', 0) * 0.05
            )
            
            if hasattr(empresa, 'capital') and empresa.capital >= inversion_objetivo:
                # Probabilidad basada en salud financiera
                probabilidad = min(0.3, empresa.capital / (inversion_objetivo * 10))
                
                if random.random() < probabilidad:
                    empresa.capital -= inversion_objetivo
                    
                    # Registrar inversión
                    self.inversiones_tecnologia[empresa.id] = {
                        'inversion': inversion_objetivo,
                        'retorno_esperado': inversion_objetivo * 0.15,
                        'ciclos_retorno': 10
                    }
                    
                    return True
        except Exception as e:
            self.logger.error(f"Error aplicando inversión tecnológica a {empresa.id}: {e}")
            
        return False
    
    def _calcular_productividad_sistema(self, simulador) -> float:
        """Calcula la productividad promedio del sistema"""
        productividades = []
        
        for empresa in simulador.getEmpresas():
            if empresa.activa:
                prod = self._obtener_productividad_empresa(empresa)
                if prod > 0:
                    productividades.append(prod)
        
        return np.mean(productividades) if productividades else 0.0
    
    def obtener_reporte_productividad(self) -> Dict[str, Any]:
        """Genera reporte detallado de productividad"""
        return {
            'programas_capacitacion_activos': len(self.programas_capacitacion),
            'inversiones_tecnologia': len(self.inversiones_tecnologia),
            'empresas_con_historia': len(self.historia_productividad),
            'configuracion': {
                'objetivo_minimo': self.config.productividad_minima_objetivo,
                'objetivo_maximo': self.config.productividad_maxima_objetivo,
                'tasa_mejora': self.config.tasa_mejora_base,
                'ciclos_capacitacion': self.config.ciclos_capacitacion
            },
            'metricas_recientes': {
                empresa_id: historia[-1] if historia else None
                for empresa_id, historia in self.historia_productividad.items()
            }
        }
