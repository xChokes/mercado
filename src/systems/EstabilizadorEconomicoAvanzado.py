"""
Sistema de Estabilización Económica y Amortiguadores PIB
=======================================================

Previene volatilidad extrema del PIB y mantiene crecimiento sostenible
"""

import logging
import random
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from collections import deque

class EstabilizadorEconomicoAvanzado:
    """Sistema avanzado de estabilización económica con múltiples amortiguadores"""
    
    def __init__(self, mercado):
        self.mercado = mercado
        self.logger = logging.getLogger(__name__)
        
        # Histórico para análisis de tendencias
        self.pib_historico = deque(maxlen=10)  # Últimos 10 ciclos
        self.inflacion_historico = deque(maxlen=10)
        self.desempleo_historico = deque(maxlen=10)
        
        # Parámetros de estabilización
        self.volatilidad_maxima_pib = 0.25  # ±25% máximo por ciclo
        self.crecimiento_objetivo_anual = 0.03  # 3% anual
        self.banda_estabilidad = 0.15  # ±15% banda de estabilidad
        
        # Mecanismos de estabilización
        self.fondo_estabilizacion = 0.0
        self.multiplicador_fiscal = 1.0
        self.politicas_activas = {}
        
        # Contadores
        self.intervenciones_realizadas = 0
        self.ciclos_estables = 0
        
    def aplicar_estabilizacion(self, ciclo: int, pib_actual: float, pib_anterior: float = None):
        """Aplica mecanismos de estabilización económica"""
        try:
            # Registrar datos históricos
            self._registrar_datos_historicos(pib_actual)
            
            # Detectar volatilidad extrema
            volatilidad = self._calcular_volatilidad(pib_actual, pib_anterior)
            
            # Aplicar amortiguadores si es necesario
            pib_estabilizado = pib_actual
            if self._requiere_intervencion(volatilidad, pib_actual):
                pib_estabilizado = self._aplicar_amortiguadores(pib_actual, volatilidad, ciclo)
                self.intervenciones_realizadas += 1
                self.logger.info(f"Estabilización aplicada - PIB: ${pib_actual:.0f} → ${pib_estabilizado:.0f}")
            else:
                self.ciclos_estables += 1
            
            # Actualizar políticas automáticas
            self._actualizar_politicas_automaticas(pib_estabilizado, ciclo)
            
            return pib_estabilizado
            
        except Exception as e:
            self.logger.error(f"Error en estabilización económica: {e}")
            return pib_actual
    
    def _registrar_datos_historicos(self, pib_actual: float):
        """Registra datos históricos para análisis"""
        self.pib_historico.append(pib_actual)
        
        # Registrar inflación y desempleo del mercado
        inflacion_actual = getattr(self.mercado, 'tasa_inflacion', 0.0)
        desempleo_actual = self._calcular_desempleo_actual()
        
        self.inflacion_historico.append(inflacion_actual)
        self.desempleo_historico.append(desempleo_actual)
    
    def _calcular_volatilidad(self, pib_actual: float, pib_anterior: float = None) -> float:
        """Calcula la volatilidad actual del PIB"""
        if pib_anterior is None or pib_anterior == 0:
            if len(self.pib_historico) >= 2:
                pib_anterior = self.pib_historico[-2]
            else:
                return 0.0
        
        return abs(pib_actual - pib_anterior) / max(1, pib_anterior)
    
    def _calcular_desempleo_actual(self) -> float:
        """Calcula tasa de desempleo actual"""
        consumidores = self.mercado.getConsumidores()
        if not consumidores:
            return 0.0
        
        desempleados = len([c for c in consumidores if not getattr(c, 'empleado', False)])
        return desempleados / len(consumidores)
    
    def _requiere_intervencion(self, volatilidad: float, pib_actual: float) -> bool:
        """Determina si se requiere intervención estabilizadora"""
        # Criterio 1: Volatilidad extrema
        if volatilidad > self.volatilidad_maxima_pib:
            return True
        
        # Criterio 2: PIB fuera de banda de estabilidad
        if len(self.pib_historico) >= 3:
            pib_promedio_3m = np.mean(list(self.pib_historico)[-3:])
            desviacion = abs(pib_actual - pib_promedio_3m) / max(1, pib_promedio_3m)
            if desviacion > self.banda_estabilidad:
                return True
        
        # Criterio 3: Tendencia negativa sostenida
        if len(self.pib_historico) >= 4:
            tendencia = self._calcular_tendencia()
            if tendencia < -0.1:  # Caída sostenida > 10%
                return True
        
        return False
    
    def _calcular_tendencia(self) -> float:
        """Calcula tendencia promedio de crecimiento"""
        if len(self.pib_historico) < 3:
            return 0.0
        
        valores = list(self.pib_historico)[-4:]  # Últimos 4 valores
        crecimientos = []
        
        for i in range(1, len(valores)):
            crecimiento = (valores[i] - valores[i-1]) / max(1, valores[i-1])
            crecimientos.append(crecimiento)
        
        return np.mean(crecimientos) if crecimientos else 0.0
    
    def _aplicar_amortiguadores(self, pib_actual: float, volatilidad: float, ciclo: int) -> float:
        """Aplica diferentes tipos de amortiguadores económicos"""
        pib_ajustado = pib_actual
        
        # Amortiguador 1: Estabilización fiscal
        pib_ajustado = self._aplicar_estabilizacion_fiscal(pib_ajustado, volatilidad)
        
        # Amortiguador 2: Suavizado por inventarios
        pib_ajustado = self._aplicar_amortiguador_inventarios(pib_ajustado)
        
        # Amortiguador 3: Intervención del gobierno
        pib_ajustado = self._aplicar_intervencion_gubernamental(pib_ajustado, ciclo)
        
        # Amortiguador 4: Ajuste gradual (evitar shocks)
        pib_ajustado = self._aplicar_suavizado_gradual(pib_actual, pib_ajustado)
        
        return pib_ajustado
    
    def _aplicar_estabilizacion_fiscal(self, pib: float, volatilidad: float) -> float:
        """Aplica política fiscal contracíclica"""
        if len(self.pib_historico) < 2:
            return pib
        
        pib_anterior = self.pib_historico[-2]
        crecimiento = (pib - pib_anterior) / max(1, pib_anterior)
        
        # Política contracíclica
        if crecimiento < -0.1:  # Recesión
            # Estímulo fiscal
            estimulo = min(pib * 0.05, self.fondo_estabilizacion * 0.3)  # Máximo 5% PIB o 30% del fondo
            pib_ajustado = pib + estimulo
            self.fondo_estabilizacion -= estimulo
            self.politicas_activas[f'estimulo_fiscal'] = estimulo
            
        elif crecimiento > 0.15:  # Crecimiento muy alto
            # Enfriamiento fiscal
            retiro = min(pib * 0.03, pib * 0.1)  # Entre 3-10% según intensidad
            pib_ajustado = pib - retiro
            self.fondo_estabilizacion += retiro
            self.politicas_activas[f'enfriamiento_fiscal'] = retiro
            
        else:
            pib_ajustado = pib
        
        return pib_ajustado
    
    def _aplicar_amortiguador_inventarios(self, pib: float) -> float:
        """Aplica suavizado basado en inventarios empresariales"""
        empresas = self.mercado.getEmpresas()
        if not empresas:
            return pib
        
        # Calcular nivel promedio de inventarios
        inventarios_totales = 0
        inventarios_objetivo = 0
        
        for empresa in empresas:
            if hasattr(empresa, 'bienes'):
                for bien, stock in empresa.bienes.items():
                    if isinstance(stock, list):
                        inventarios_totales += len(stock)
                        inventarios_objetivo += getattr(empresa, f'objetivo_{bien}', 10)
        
        # Si inventarios están muy por encima/debajo del objetivo, ajustar PIB
        if inventarios_objetivo > 0:
            ratio_inventario = inventarios_totales / inventarios_objetivo
            
            if ratio_inventario > 1.5:  # Exceso de inventario
                # Reducir PIB por acumulación no deseada
                ajuste = pib * -0.02 * (ratio_inventario - 1.5)
                pib = pib + ajuste
                
            elif ratio_inventario < 0.5:  # Inventarios bajos
                # Aumentar PIB por reposición
                ajuste = pib * 0.03 * (0.5 - ratio_inventario)
                pib = pib + ajuste
        
        return pib
    
    def _aplicar_intervencion_gubernamental(self, pib: float, ciclo: int) -> float:
        """Aplica intervenciones gubernamentales estabilizadoras"""
        # Programa de obras públicas en recesión
        if len(self.pib_historico) >= 2:
            tendencia = self._calcular_tendencia()
            
            if tendencia < -0.08:  # Recesión sostenida
                # Programa de obras públicas
                inversion_publica = pib * random.uniform(0.02, 0.04)  # 2-4% PIB
                pib += inversion_publica
                self.politicas_activas['obras_publicas'] = inversion_publica
                
                # Subsidios de emergencia
                if self._calcular_desempleo_actual() > 0.15:
                    subsidio_emergencia = pib * 0.015  # 1.5% PIB
                    pib += subsidio_emergencia
                    self.politicas_activas['subsidios_emergencia'] = subsidio_emergencia
        
        return pib
    
    def _aplicar_suavizado_gradual(self, pib_original: float, pib_con_politicas: float) -> float:
        """Aplica suavizado gradual para evitar cambios abruptos"""
        cambio_total = pib_con_politicas - pib_original
        cambio_maximo_permitido = pib_original * self.volatilidad_maxima_pib
        
        # Limitar el cambio total
        if abs(cambio_total) > cambio_maximo_permitido:
            factor_limitacion = cambio_maximo_permitido / abs(cambio_total)
            cambio_limitado = cambio_total * factor_limitacion
            pib_final = pib_original + cambio_limitado
        else:
            pib_final = pib_con_politicas
        
        return pib_final
    
    def _actualizar_politicas_automaticas(self, pib: float, ciclo: int):
        """Actualiza políticas automáticas como multiplicador fiscal"""
        # Actualizar fondo de estabilización (acumula en tiempos buenos)
        if len(self.pib_historico) >= 2:
            crecimiento = (pib - self.pib_historico[-2]) / max(1, self.pib_historico[-2])
            
            if crecimiento > 0.05:  # Crecimiento sólido
                contribucion = pib * 0.01  # 1% PIB al fondo
                self.fondo_estabilizacion += contribucion
                
        # Límite máximo del fondo (no más de 20% PIB promedio)
        if len(self.pib_historico) >= 3:
            pib_promedio = np.mean(list(self.pib_historico))
            limite_fondo = pib_promedio * 0.2
            self.fondo_estabilizacion = min(self.fondo_estabilizacion, limite_fondo)
        
        # Actualizar multiplicador fiscal según condiciones
        desempleo = self._calcular_desempleo_actual()
        if desempleo > 0.1:
            self.multiplicador_fiscal = min(1.5, self.multiplicador_fiscal + 0.05)
        else:
            self.multiplicador_fiscal = max(0.8, self.multiplicador_fiscal - 0.02)
    
    def aplicar_politicas_macroeconomicas(self, ciclo: int):
        """Aplica políticas macroeconómicas automáticas"""
        try:
            # Política de empleo
            self._aplicar_politica_empleo()
            
            # Política de competencia
            self._aplicar_politica_competencia()
            
            # Política de innovación
            self._aplicar_politica_innovacion(ciclo)
            
        except Exception as e:
            self.logger.error(f"Error aplicando políticas macroeconómicas: {e}")
    
    def _aplicar_politica_empleo(self):
        """Aplica política activa de empleo"""
        desempleo = self._calcular_desempleo_actual()
        
        if desempleo > 0.12:
            # Crear empleos públicos temporales
            consumidores_desempleados = [c for c in self.mercado.getConsumidores() 
                                       if not getattr(c, 'empleado', False)]
            
            empleos_a_crear = min(len(consumidores_desempleados) // 5, 10)  # Máximo 10 empleos públicos
            
            for i, consumidor in enumerate(consumidores_desempleados[:empleos_a_crear]):
                # Simular empleo público temporal
                consumidor.empleado = True
                consumidor.empleador_publico = True
                consumidor.ingreso_mensual = random.uniform(2200, 2800)  # Salario público
    
    def _aplicar_politica_competencia(self):
        """Aplica política de competencia y antimonopolio"""
        empresas = [e for e in self.mercado.getEmpresas() if not getattr(e, 'en_quiebra', False)]
        
        if len(empresas) <= 2:  # Muy pocas empresas
            # Incentivos para nuevos entrantes
            for empresa in empresas:
                if hasattr(empresa, 'dinero'):
                    # Reducir barreras de entrada (simulado como capital adicional para competidores)
                    incentivo_competencia = empresa.dinero * 0.05
                    empresa.competencia_incentivo = incentivo_competencia
    
    def _aplicar_politica_innovacion(self, ciclo: int):
        """Aplica política de fomento a la innovación"""
        if ciclo % 15 == 0:  # Cada 15 ciclos
            # Subsidios de I+D
            empresas = [e for e in self.mercado.getEmpresas() if not getattr(e, 'en_quiebra', False)]
            
            for empresa in empresas:
                if hasattr(empresa, 'dinero') and empresa.dinero > 50000:
                    subsidio_id = random.uniform(5000, 15000)
                    empresa.dinero += subsidio_id
                    empresa.subsidio_innovacion = subsidio_id
    
    def obtener_estadisticas(self) -> Dict[str, Any]:
        """Retorna estadísticas del sistema de estabilización"""
        volatilidad_promedio = 0.0
        if len(self.pib_historico) >= 2:
            volatilidades = []
            valores_pib = list(self.pib_historico)
            
            for i in range(1, len(valores_pib)):
                vol = abs(valores_pib[i] - valores_pib[i-1]) / max(1, valores_pib[i-1])
                volatilidades.append(vol)
            
            volatilidad_promedio = np.mean(volatilidades) if volatilidades else 0.0
        
        tendencia_actual = self._calcular_tendencia()
        
        return {
            'intervenciones_realizadas': self.intervenciones_realizadas,
            'ciclos_estables': self.ciclos_estables,
            'fondo_estabilizacion': self.fondo_estabilizacion,
            'volatilidad_promedio': volatilidad_promedio,
            'tendencia_crecimiento': tendencia_actual,
            'politicas_activas': len(self.politicas_activas),
            'multiplicador_fiscal': self.multiplicador_fiscal,
            'sistema_estable': volatilidad_promedio < self.volatilidad_maxima_pib * 0.5
        }
