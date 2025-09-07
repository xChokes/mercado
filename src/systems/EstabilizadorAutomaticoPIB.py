"""
Sistema de Estabilización Automática del PIB
Implementa amortiguadores automáticos para reducir volatilidad económica
"""

import logging
import random
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import numpy as np
from collections import deque

@dataclass
class ConfigEstabilizacionPIB:
    """Configuración para estabilización del PIB"""
    ventana_memoria: int = 8
    umbral_volatilidad: float = 0.20  # 20% de desviación estándar
    factor_amortiguacion: float = 0.25
    umbral_caida_critica: float = 0.15  # 15% caída
    umbral_crecimiento_excesivo: float = 0.25  # 25% crecimiento
    reserva_estabilizacion: float = 10000.0
    multiplicador_fiscal: float = 1.5

class EstabilizadorAutomaticoPIB:
    """Sistema de estabilización automática del PIB"""
    
    def __init__(self, config: ConfigEstabilizacionPIB = None):
        self.config = config or ConfigEstabilizacionPIB()
        self.logger = logging.getLogger(__name__)
        self.historia_pib = deque(maxlen=self.config.ventana_memoria)
        self.intervenciones = {}
        self.reserva_actual = self.config.reserva_estabilizacion
        self.contador_intervenciones = 0
        
    def estabilizar_pib_ciclo(self, simulador, ciclo: int) -> Dict[str, Any]:
        """Estabiliza el PIB en cada ciclo"""
        resultados = {
            'pib_original': 0.0,
            'pib_estabilizado': 0.0,
            'volatilidad_detectada': 0.0,
            'intervencion_aplicada': False,
            'tipo_intervencion': '',
            'magnitud_ajuste': 0.0,
            'reserva_utilizada': 0.0
        }
        
        try:
            # Obtener PIB actual
            pib_actual = self._obtener_pib(simulador)
            resultados['pib_original'] = pib_actual
            
            # Actualizar historia
            self.historia_pib.append(pib_actual)
            
            # Analizar necesidad de estabilización
            analisis = self._analizar_volatilidad()
            resultados['volatilidad_detectada'] = analisis['volatilidad']
            
            # Aplicar estabilización si es necesaria
            if analisis['necesita_estabilizacion']:
                intervencion = self._aplicar_estabilizacion(simulador, pib_actual, analisis, ciclo)
                
                resultados.update(intervencion)
                
                if intervencion['intervencion_aplicada']:
                    # Actualizar PIB en el simulador
                    self._aplicar_pib_ajustado(simulador, intervencion['pib_estabilizado'])
                    
            else:
                resultados['pib_estabilizado'] = pib_actual
            
            # Regenerar reservas gradualmente
            self._regenerar_reservas()
            
            if resultados['intervencion_aplicada']:
                self.logger.info(f"📊 PIB estabilizado: {resultados['pib_original']:.0f} → {resultados['pib_estabilizado']:.0f} "
                               f"({resultados['tipo_intervencion']})")
            
        except Exception as e:
            self.logger.error(f"Error estabilizando PIB: {e}")
            resultados['pib_estabilizado'] = resultados['pib_original']
            
        return resultados
    
    def _obtener_pib(self, simulador) -> float:
        """Obtiene el PIB actual del simulador"""
        if hasattr(simulador, 'pib'):
            return float(simulador.pib)
        elif hasattr(simulador, 'calcular_pib'):
            return float(simulador.calcular_pib())
        else:
            # Estimar PIB basado en actividad económica
            pib_estimado = 0.0
            for empresa in simulador.getEmpresas():
                # Verificar si la empresa está "activa"
                empresa_activa = True
                if hasattr(empresa, 'en_quiebra') and empresa.en_quiebra:
                    empresa_activa = False
                elif empresa.dinero <= 1000:
                    empresa_activa = False
                
                if empresa_activa:
                    if hasattr(empresa, 'produccion'):
                        pib_estimado += empresa.produccion
                    elif hasattr(empresa, 'capital'):
                        pib_estimado += empresa.capital * 0.1  # Proxy de actividad
            return pib_estimado
    
    def _analizar_volatilidad(self) -> Dict[str, Any]:
        """Analiza la volatilidad del PIB y determina necesidad de intervención"""
        analisis = {
            'volatilidad': 0.0,
            'necesita_estabilizacion': False,
            'tipo_problema': '',
            'magnitud_problema': 0.0,
            'direccion_ajuste': 0  # -1: reducir, 0: mantener, 1: aumentar
        }
        
        if len(self.historia_pib) < 3:
            return analisis
        
        pibs = np.array(self.historia_pib)
        
        # Calcular volatilidad (desviación estándar relativa)
        pib_promedio = np.mean(pibs)
        if pib_promedio > 0:
            analisis['volatilidad'] = np.std(pibs) / pib_promedio
        
        # Verificar si excede umbral de volatilidad
        if analisis['volatilidad'] > self.config.umbral_volatilidad:
            analisis['necesita_estabilizacion'] = True
            analisis['tipo_problema'] = 'volatilidad_excesiva'
            analisis['magnitud_problema'] = analisis['volatilidad']
        
        # Verificar caídas o crecimientos excesivos
        if len(pibs) >= 2:
            cambio_reciente = (pibs[-1] - pibs[-2]) / pibs[-2] if pibs[-2] > 0 else 0
            
            if cambio_reciente < -self.config.umbral_caida_critica:
                analisis['necesita_estabilizacion'] = True
                analisis['tipo_problema'] = 'caida_critica'
                analisis['magnitud_problema'] = abs(cambio_reciente)
                analisis['direccion_ajuste'] = 1  # Aumentar PIB
                
            elif cambio_reciente > self.config.umbral_crecimiento_excesivo:
                analisis['necesita_estabilizacion'] = True
                analisis['tipo_problema'] = 'crecimiento_excesivo'
                analisis['magnitud_problema'] = cambio_reciente
                analisis['direccion_ajuste'] = -1  # Reducir PIB
        
        return analisis
    
    def _aplicar_estabilizacion(self, simulador, pib_actual: float, analisis: Dict, ciclo: int) -> Dict[str, Any]:
        """Aplica medidas de estabilización específicas"""
        resultado = {
            'intervencion_aplicada': False,
            'tipo_intervencion': '',
            'pib_estabilizado': pib_actual,
            'magnitud_ajuste': 0.0,
            'reserva_utilizada': 0.0
        }
        
        try:
            if analisis['tipo_problema'] == 'caida_critica':
                resultado = self._aplicar_estimulo_economico(simulador, pib_actual, analisis, ciclo)
                
            elif analisis['tipo_problema'] == 'crecimiento_excesivo':
                resultado = self._aplicar_enfriamiento_economico(simulador, pib_actual, analisis, ciclo)
                
            elif analisis['tipo_problema'] == 'volatilidad_excesiva':
                resultado = self._aplicar_suavizamiento(simulador, pib_actual, analisis, ciclo)
            
            # Registrar intervención
            if resultado['intervencion_aplicada']:
                self.intervenciones[ciclo] = {
                    'tipo': resultado['tipo_intervencion'],
                    'pib_original': pib_actual,
                    'pib_ajustado': resultado['pib_estabilizado'],
                    'problema': analisis['tipo_problema'],
                    'magnitud': analisis['magnitud_problema']
                }
                self.contador_intervenciones += 1
                
        except Exception as e:
            self.logger.error(f"Error aplicando estabilización: {e}")
            
        return resultado
    
    def _aplicar_estimulo_economico(self, simulador, pib_actual: float, analisis: Dict, ciclo: int) -> Dict[str, Any]:
        """Aplica estímulo económico para contrarrestar caída del PIB"""
        resultado = {
            'intervencion_aplicada': False,
            'tipo_intervencion': 'estimulo_economico',
            'pib_estabilizado': pib_actual,
            'magnitud_ajuste': 0.0,
            'reserva_utilizada': 0.0
        }
        
        # Calcular magnitud del estímulo necesario
        estimulo_necesario = pib_actual * analisis['magnitud_problema'] * self.config.multiplicador_fiscal
        
        if self.reserva_actual >= estimulo_necesario:
            # Aplicar estímulo mediante:
            # 1. Inyección de capital a empresas
            empresas_activas = [e for e in simulador.getEmpresas() if e.activa]
            if empresas_activas:
                estimulo_por_empresa = estimulo_necesario / len(empresas_activas)
                
                for empresa in empresas_activas:
                    if hasattr(empresa, 'capital'):
                        empresa.capital += estimulo_por_empresa * 0.5  # 50% como capital
                    
                    # Incrementar capacidad temporal
                    if hasattr(empresa, 'capacidad_produccion'):
                        empresa.capacidad_produccion *= 1.1
                    
                    # Estimular contratación
                    if hasattr(empresa, 'empleados') and random.random() < 0.3:
                        nuevos_empleados = random.randint(1, 3)
                        empresa.empleados.extend([f"EstimuloEmp_{ciclo}_{i}" for i in range(nuevos_empleados)])
            
            # 2. Incremento directo del PIB ajustado
            factor_multiplicador = 1.0 + (analisis['magnitud_problema'] * self.config.factor_amortiguacion)
            pib_estimulado = pib_actual * factor_multiplicador
            
            # Actualizar estado
            self.reserva_actual -= estimulo_necesario
            
            resultado['intervencion_aplicada'] = True
            resultado['pib_estabilizado'] = pib_estimulado
            resultado['magnitud_ajuste'] = pib_estimulado - pib_actual
            resultado['reserva_utilizada'] = estimulo_necesario
        
        return resultado
    
    def _aplicar_enfriamiento_economico(self, simulador, pib_actual: float, analisis: Dict, ciclo: int) -> Dict[str, Any]:
        """Aplica medidas de enfriamiento para controlar crecimiento excesivo"""
        resultado = {
            'intervencion_aplicada': False,
            'tipo_intervencion': 'enfriamiento_economico',
            'pib_estabilizado': pib_actual,
            'magnitud_ajuste': 0.0,
            'reserva_utilizada': 0.0
        }
        
        # Aplicar medidas de enfriamiento:
        # 1. Reducir capacidades de producción temporalmente
        for empresa in simulador.getEmpresas():
            # Verificar si la empresa está "activa"
            empresa_activa = True
            if hasattr(empresa, 'en_quiebra') and empresa.en_quiebra:
                empresa_activa = False
            elif empresa.dinero <= 1000:
                empresa_activa = False
                
            if empresa_activa:
                if hasattr(empresa, 'capacidad_produccion'):
                    empresa.capacidad_produccion *= 0.95  # Reducir 5%
                
                # Incrementar costos operativos (simulando regulación)
                if hasattr(empresa, 'costos_operativos'):
                    empresa.costos_operativos *= 1.05
        
        # 2. Ajustar PIB hacia abajo
        factor_enfriamiento = 1.0 - (analisis['magnitud_problema'] * self.config.factor_amortiguacion * 0.5)
        pib_enfriado = pib_actual * factor_enfriamiento
        
        # Acumular reservas del "enfriamiento"
        diferencia = pib_actual - pib_enfriado
        self.reserva_actual += diferencia * 0.3  # 30% a reservas
        
        resultado['intervencion_aplicada'] = True
        resultado['pib_estabilizado'] = pib_enfriado
        resultado['magnitud_ajuste'] = pib_enfriado - pib_actual
        
        return resultado
    
    def _aplicar_suavizamiento(self, simulador, pib_actual: float, analisis: Dict, ciclo: int) -> Dict[str, Any]:
        """Aplica suavizamiento general para reducir volatilidad"""
        resultado = {
            'intervencion_aplicada': False,
            'tipo_intervencion': 'suavizamiento',
            'pib_estabilizado': pib_actual,
            'magnitud_ajuste': 0.0,
            'reserva_utilizada': 0.0
        }
        
        if len(self.historia_pib) >= 3:
            # Calcular PIB objetivo como promedio móvil suavizado
            pibs_recientes = list(self.historia_pib)[-3:]
            pib_objetivo = np.mean(pibs_recientes)
            
            # Aplicar suavizamiento gradual hacia el objetivo
            factor_suavizado = self.config.factor_amortiguacion
            pib_suavizado = (pib_actual * (1 - factor_suavizado)) + (pib_objetivo * factor_suavizado)
            
            # Aplicar ajustes graduales a empresas
            if abs(pib_suavizado - pib_actual) > pib_actual * 0.02:  # Solo si ajuste > 2%
                ratio_ajuste = pib_suavizado / pib_actual if pib_actual > 0 else 1.0
                
                for empresa in simulador.getEmpresas():
                    # Verificar si la empresa está "activa"
                    empresa_activa = True
                    if hasattr(empresa, 'en_quiebra') and empresa.en_quiebra:
                        empresa_activa = False
                    elif empresa.dinero <= 1000:
                        empresa_activa = False
                        
                    if empresa_activa:
                        # Ajustar producción proporcionalmente
                        if hasattr(empresa, 'produccion'):
                            empresa.produccion *= ratio_ajuste
                        
                        # Ajustar capacidad ligeramente
                        if hasattr(empresa, 'capacidad_produccion'):
                            nueva_capacidad = empresa.capacidad_produccion * (0.95 + ratio_ajuste * 0.05)
                            empresa.capacidad_produccion = nueva_capacidad
                
                resultado['intervencion_aplicada'] = True
                resultado['pib_estabilizado'] = pib_suavizado
                resultado['magnitud_ajuste'] = pib_suavizado - pib_actual
        
        return resultado
    
    def _aplicar_pib_ajustado(self, simulador, pib_ajustado: float):
        """Aplica el PIB ajustado al simulador"""
        if hasattr(simulador, 'pib'):
            simulador.pib = pib_ajustado
        
        # También ajustar métricas relacionadas si existen
        if hasattr(simulador, 'metricas_economicas'):
            simulador.metricas_economicas['pib'] = pib_ajustado
    
    def _regenerar_reservas(self):
        """Regenera gradualmente las reservas de estabilización"""
        # Regeneración del 2% por ciclo hasta el máximo
        regeneracion = self.config.reserva_estabilizacion * 0.02
        self.reserva_actual = min(
            self.config.reserva_estabilizacion * 2,  # Máximo 2x la reserva base
            self.reserva_actual + regeneracion
        )
    
    def obtener_metricas_estabilizacion(self) -> Dict[str, Any]:
        """Obtiene métricas del sistema de estabilización"""
        if len(self.historia_pib) < 2:
            return {'historia_insuficiente': True}
        
        pibs = np.array(self.historia_pib)
        volatilidad_actual = np.std(pibs) / np.mean(pibs) if np.mean(pibs) > 0 else 0
        
        return {
            'volatilidad_actual': volatilidad_actual,
            'pib_promedio': float(np.mean(pibs)),
            'pib_actual': float(pibs[-1]) if len(pibs) > 0 else 0.0,
            'intervenciones_totales': self.contador_intervenciones,
            'reserva_disponible': self.reserva_actual,
            'historia_pib': list(pibs),
            'configuracion': {
                'umbral_volatilidad': self.config.umbral_volatilidad,
                'factor_amortiguacion': self.config.factor_amortiguacion,
                'ventana_memoria': self.config.ventana_memoria
            },
            'intervenciones_recientes': dict(list(self.intervenciones.items())[-5:]) if self.intervenciones else {}
        }
