"""
Banco Central Avanzado con Política Monetaria Profesional
========================================================

Implementa la regla de Taylor y otros instrumentos de política monetaria
para mantener estabilidad de precios y pleno empleo.
Integra modelos económicos avanzados para pronósticos.
"""

import math
import logging
import sys
import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

# Agregar path para importar módulos avanzados
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

try:
    from src.systems.ModelosEconomicosAvanzados import (
        IntegradorModelosEconomicos, ParametrosEconomicos
    )
    from src.config.DatosEconomicosReales import CalibradorEconomicoRealista
    MODELOS_DISPONIBLES = True
except ImportError:
    IntegradorModelosEconomicos = None
    ParametrosEconomicos = None
    CalibradorEconomicoRealista = None
    MODELOS_DISPONIBLES = False


class EstadoEconomico(Enum):
    """Estados de la economía para política monetaria"""
    EXPANSION = "expansion"
    RECESION = "recesion"
    ESTANFLACION = "estanflacion"
    RECUPERACION = "recuperacion"
    CRISIS = "crisis"
    SOBRECALENTAMIENTO = "sobrecalentamiento"


@dataclass
class DecisionMonetaria:
    """Registro de una decisión de política monetaria"""
    ciclo: int
    tasa_anterior: float
    tasa_nueva: float
    inflacion_objetivo: float
    inflacion_actual: float
    brecha_producto: float
    justificacion: str


class BancoCentralAvanzado:
    """
    Banco Central con política monetaria sofisticada basada en:
    - Regla de Taylor aumentada
    - Modelos DSGE y IS-LM para pronósticos
    - Targeting de inflación con expectativas
    - Comunicación forward guidance profesional
    """
    
    def __init__(self, mercado):
        self.mercado = mercado
        self.logger = logging.getLogger('BancoCentral')
        
        # Parámetros de política monetaria
        self.tasa_neutral = 0.025       # Tasa de interés neutral (2.5%)
        self.inflacion_objetivo = 0.025  # Meta de inflación (2.5%)
        self.tolerancia_inflacion = 0.005  # Banda de tolerancia (±0.5%)
        
        # Parámetros de la regla de Taylor
        self.peso_inflacion = 1.2       # Reacción a desviación de inflación (más conservador)
        self.peso_producto = 0.3        # Reacción a brecha del producto (más conservador)
        self.suavizamiento = 0.85       # Mayor suavizamiento de tasas
        
        # Estado del banco central
        self.tasa_actual = self.tasa_neutral
        self.decisiones_historicas = []
        self.forward_guidance = ""
        self.reunion_cada_ciclos = 3    # Reuniones cada 3 ciclos
        
        # Estimaciones económicas
        self.pib_potencial_estimado = None
        self.tendencia_inflacion = []
        
        # Modelos económicos avanzados
        if MODELOS_DISPONIBLES:
            self.integrador_modelos = IntegradorModelosEconomicos()
            self.calibrador = CalibradorEconomicoRealista()
            self.usar_modelos_avanzados = True
            self.logger.info("🧮 Modelos económicos avanzados ACTIVADOS")
        else:
            self.integrador_modelos = None
            self.calibrador = None
            self.usar_modelos_avanzados = False
            self.logger.warning("⚠️  Modelos económicos avanzados NO DISPONIBLES")
        
        # Análisis de expectativas
        self.expectativas_inflacion = self.inflacion_objetivo
        self.confianza_expectativas = 0.8
        
    def ejecutar_politica_monetaria(self, ciclo: int) -> Optional[DecisionMonetaria]:
        """
        Ejecuta la política monetaria si corresponde una reunión
        """
        if ciclo % self.reunion_cada_ciclos != 0:
            return None
            
        # Actualizar estimaciones
        self._actualizar_estimaciones()
        
        # Evaluar estado económico
        estado_economico = self._evaluar_estado_economico()
        
        # Calcular nueva tasa usando modelos integrados o Taylor Rule
        if self.usar_modelos_avanzados:
            nueva_tasa = self._calcular_tasa_con_modelos_avanzados(estado_economico)
        else:
            nueva_tasa = self._calcular_regla_taylor()
        
        # Aplicar suavizamiento
        nueva_tasa = self._aplicar_suavizamiento(nueva_tasa)
        
        # Aplicar límites realistas
        nueva_tasa = max(0.0, min(0.15, nueva_tasa))  # Entre 0% y 15%
        
        # Crear decisión
        decision = self._crear_decision_monetaria(ciclo, nueva_tasa, estado_economico)
        
        # Implementar decisión
        self._implementar_decision(decision)
        
        # Log de la decisión con modelos
        if self.usar_modelos_avanzados:
            puntos_base = int((nueva_tasa - self.tasa_actual) * 10000)
            self.logger.info(f"💰 DECISIÓN MONETARIA (Modelos): {puntos_base:+d} pb → {nueva_tasa:.3f}% | {estado_economico.value}")
        
        return decision
    
    def _calcular_regla_taylor(self) -> float:
        """
        Implementa la regla de Taylor:
        i = r* + π + α(π - π*) + β(y - y*)
        
        Donde:
        i = tasa de interés nominal
        r* = tasa de interés real neutral
        π = inflación actual
        π* = meta de inflación
        y - y* = brecha del producto
        α, β = pesos de reacción
        """
        try:
            # Obtener inflación actual
            inflacion_actual = self._obtener_inflacion_actual()
            
            # Calcular brecha del producto
            brecha_producto = self._calcular_brecha_producto()
            
            # Calcular tasa según Taylor Rule
            tasa_taylor = (
                self.tasa_neutral +                                    # r*
                inflacion_actual +                                     # π
                self.peso_inflacion * (inflacion_actual - self.inflacion_objetivo) +  # α(π - π*)
                self.peso_producto * brecha_producto                   # β(y - y*)
            )
            
            return tasa_taylor
            
        except Exception as e:
            self.logger.warning(f"Error en cálculo de regla de Taylor: {e}")
            return self.tasa_actual
        
        return decision
    
    def _calcular_tasa_con_modelos_avanzados(self, estado_economico: EstadoEconomico) -> float:
        """Calcula tasa óptima usando modelos económicos avanzados"""
        try:
            # Preparar estado económico para los modelos
            estado_actual = self._preparar_estado_para_modelos()
            
            # Ejecutar análisis completo
            analisis = self.integrador_modelos.analisis_completo(estado_actual)
            
            # Extraer recomendaciones de tasas
            if 'sintesis' in analisis and 'tasa_consenso' in analisis['sintesis']:
                tasa_consenso = analisis['sintesis']['tasa_consenso']
                
                # Ajustar según estado económico detectado por calibrador
                if self.calibrador:
                    regimen = self.calibrador.detectar_regimen_economico(estado_actual)
                    politicas = self.calibrador.sugerir_politicas_por_regimen(regimen)
                    
                    if 'tasas_sugeridas' in politicas:
                        rango_min, rango_max = politicas['tasas_sugeridas']
                        tasa_consenso = max(rango_min, min(rango_max, tasa_consenso))
                
                self.logger.info(f"🧮 Tasa consenso de modelos: {tasa_consenso:.3f}%")
                return tasa_consenso
            
            # Fallback a Taylor Rule si modelos fallan
            return self._calcular_regla_taylor()
            
        except Exception as e:
            self.logger.warning(f"Error en modelos avanzados, usando Taylor Rule: {e}")
            return self._calcular_regla_taylor()
    
    def _preparar_estado_para_modelos(self) -> Dict:
        """Prepara el estado económico para análisis de modelos"""
        
        estado = {
            'inflacion': self._obtener_inflacion_actual(),
            'desempleo': getattr(self.mercado, 'tasa_desempleo', 0.05),
            'crecimiento_pib': self._calcular_crecimiento_pib(),
            'productividad': getattr(self.mercado, 'productividad_promedio', 1.0),
            'oferta_monetaria': getattr(self.mercado, 'masa_monetaria', 1000000),
            'nivel_precios': getattr(self.mercado, 'nivel_precios_promedio', 100),
            'gasto_gobierno': getattr(self.mercado, 'gasto_publico', 0.2),
            'capital': self._estimar_stock_capital(),
            'trabajo': self._estimar_empleo_total(),
            'pib': self._obtener_pib_actual(),
            'tasa_interes': self.tasa_actual
        }
        
        return estado
    
    def _calcular_crecimiento_pib(self) -> float:
        """Calcula tasa de crecimiento del PIB"""
        if hasattr(self.mercado, 'pib_historico') and len(self.mercado.pib_historico) >= 2:
            pib_actual = self.mercado.pib_historico[-1]
            pib_anterior = self.mercado.pib_historico[-2]
            if pib_anterior > 0:
                return (pib_actual - pib_anterior) / pib_anterior
        return 0.02  # 2% default
    
    def _estimar_stock_capital(self) -> float:
        """Estima el stock de capital total de la economía"""
        if hasattr(self.mercado, 'empresas'):
            capital_total = sum(getattr(emp, 'capital', 0) for emp in self.mercado.empresas)
            return max(capital_total, 1.0)
        return 1000000  # Default
    
    def _estimar_empleo_total(self) -> float:
        """Estima el empleo total de la economía"""
        if hasattr(self.mercado, 'consumidores'):
            empleados = sum(1 for cons in self.mercado.getConsumidores() 
                          if getattr(cons, 'empleado', False))
            return max(empleados / len(self.mercado.getConsumidores()), 0.01)
        return 0.95  # 95% empleo default
    
    def _obtener_pib_actual(self) -> float:
        """Obtiene PIB actual"""
        if hasattr(self.mercado, 'pib_historico') and self.mercado.pib_historico:
            return self.mercado.pib_historico[-1]
        return 1000000  # Default
        
    def _calcular_regla_taylor(self) -> float:
        """
        Calcula la tasa de interés usando la Regla de Taylor:
        i = r* + π + α(π - π*) + β(y - y*)
        """
        try:
            inflacion_actual = self._obtener_inflacion_actual()
            
            # Calcular brecha del producto
            brecha_producto = self._calcular_brecha_producto()
            
            # Calcular tasa según Taylor Rule
            tasa_taylor = (
                self.tasa_neutral +                                    # r*
                inflacion_actual +                                     # π
                self.peso_inflacion * (inflacion_actual - self.inflacion_objetivo) +  # α(π - π*)
                self.peso_producto * brecha_producto                   # β(y - y*)
            )
            
            return tasa_taylor
            
        except Exception as e:
            self.logger.warning(f"Error en cálculo de regla de Taylor: {e}")
            return self.tasa_actual
    
    def _obtener_inflacion_actual(self) -> float:
        """Obtiene la inflación actual o estimada"""
        if hasattr(self.mercado, 'inflacion_historica') and self.mercado.inflacion_historica:
            # Usar promedio de últimos 3 períodos para suavizar
            inflacion_reciente = self.mercado.inflacion_historica[-3:]
            return sum(inflacion_reciente) / len(inflacion_reciente)
        else:
            return self.inflacion_objetivo  # Asumir meta si no hay datos
    
    def _calcular_brecha_producto(self) -> float:
        """
        Calcula la brecha del producto (output gap):
        (PIB actual - PIB potencial) / PIB potencial
        """
        try:
            if not self.mercado.pib_historico:
                return 0.0
                
            pib_actual = self.mercado.pib_historico[-1]
            
            # Estimar PIB potencial usando tendencia
            if self.pib_potencial_estimado is None:
                self._estimar_pib_potencial()
            
            if self.pib_potencial_estimado is None:
                return 0.0
                
            brecha = (pib_actual - self.pib_potencial_estimado) / self.pib_potencial_estimado
            
            # Limitar la brecha a rangos realistas (-20% a +20%)
            return max(-0.20, min(0.20, brecha))
            
        except Exception as e:
            self.logger.warning(f"Error calculando brecha del producto: {e}")
            return 0.0
    
    def _estimar_pib_potencial(self):
        """Estima el PIB potencial usando tendencia de crecimiento"""
        try:
            if len(self.mercado.pib_historico) < 5:
                # Si hay pocos datos, usar el PIB inicial como potencial
                self.pib_potencial_estimado = self.mercado.pib_historico[0] if self.mercado.pib_historico else 100000
                return
            
            # Usar regresión simple para estimar tendencia
            n = len(self.mercado.pib_historico)
            x_sum = sum(range(n))
            y_sum = sum(self.mercado.pib_historico)
            xy_sum = sum(i * pib for i, pib in enumerate(self.mercado.pib_historico))
            x2_sum = sum(i**2 for i in range(n))
            
            # Calcular pendiente de la tendencia
            pendiente = (n * xy_sum - x_sum * y_sum) / (n * x2_sum - x_sum**2)
            intercepto = (y_sum - pendiente * x_sum) / n
            
            # PIB potencial = tendencia en el período actual
            self.pib_potencial_estimado = intercepto + pendiente * (n - 1)
            
        except Exception as e:
            self.logger.warning(f"Error estimando PIB potencial: {e}")
            self.pib_potencial_estimado = self.mercado.pib_historico[-1] if self.mercado.pib_historico else 100000
    
    def _aplicar_suavizamiento(self, nueva_tasa: float) -> float:
        """Aplica suavizamiento para evitar cambios bruscos de tasas"""
        return self.suavizamiento * self.tasa_actual + (1 - self.suavizamiento) * nueva_tasa
    
    def _evaluar_estado_economico(self) -> EstadoEconomico:
        """Evalúa el estado actual de la economía"""
        try:
            inflacion = self._obtener_inflacion_actual()
            brecha_producto = self._calcular_brecha_producto()
            
            # Lógica de clasificación del estado económico
            if inflacion > self.inflacion_objetivo + 0.02 and brecha_producto < -0.02:
                return EstadoEconomico.ESTANFLACION
            elif brecha_producto < -0.03:
                return EstadoEconomico.RECESION
            elif brecha_producto > 0.03:
                return EstadoEconomico.EXPANSION
            else:
                return EstadoEconomico.RECUPERACION
                
        except Exception:
            return EstadoEconomico.RECUPERACION
    
    def _crear_decision_monetaria(self, ciclo: int, nueva_tasa: float, estado: EstadoEconomico) -> DecisionMonetaria:
        """Crea el registro de la decisión monetaria"""
        inflacion_actual = self._obtener_inflacion_actual()
        brecha_producto = self._calcular_brecha_producto()
        
        # Generar justificación
        cambio_tasa = nueva_tasa - self.tasa_actual
        
        if abs(cambio_tasa) < 0.001:
            justificacion = f"Mantener tasa en {self.tasa_actual:.3f}% - Condiciones estables"
        elif cambio_tasa > 0:
            if inflacion_actual > self.inflacion_objetivo:
                justificacion = f"Subir tasa +{cambio_tasa:.3f}% - Controlar inflación ({inflacion_actual:.3f}%)"
            else:
                justificacion = f"Subir tasa +{cambio_tasa:.3f}% - Enfriar economía sobrecalentada"
        else:
            if brecha_producto < 0:
                justificacion = f"Bajar tasa {cambio_tasa:.3f}% - Estimular crecimiento (brecha: {brecha_producto:.3f})"
            else:
                justificacion = f"Bajar tasa {cambio_tasa:.3f}% - Apoyar inflación baja"
        
        return DecisionMonetaria(
            ciclo=ciclo,
            tasa_anterior=self.tasa_actual,
            tasa_nueva=nueva_tasa,
            inflacion_objetivo=self.inflacion_objetivo,
            inflacion_actual=inflacion_actual,
            brecha_producto=brecha_producto,
            justificacion=justificacion
        )
    
    def _implementar_decision(self, decision: DecisionMonetaria):
        """Implementa la decisión monetaria en el sistema"""
        # Actualizar tasa del banco central
        self.tasa_actual = decision.tasa_nueva
        
        # Propagar a sistema bancario
        if hasattr(self.mercado, 'sistema_bancario'):
            self._actualizar_tasas_sistema_bancario()
        
        # Guardar en historial
        self.decisiones_historicas.append(decision)
        
        # Log de la decisión
        self.logger.info(f"DECISIÓN MONETARIA - Ciclo {decision.ciclo}: {decision.justificacion}")
    
    def _actualizar_tasas_sistema_bancario(self):
        """Actualiza las tasas del sistema bancario"""
        try:
            for banco in self.mercado.sistema_bancario.bancos:
                # Las tasas de los bancos siguen la tasa del banco central con spread
                spread_depositos = 0.01  # 1% menos para depósitos
                spread_prestamos = 0.03  # 3% más para préstamos
                
                banco.tasa_depositos = max(0.001, self.tasa_actual - spread_depositos)
                banco.tasa_base_prestamos = self.tasa_actual + spread_prestamos
                
        except Exception as e:
            self.logger.warning(f"Error actualizando tasas bancarias: {e}")
    
    def _actualizar_estimaciones(self):
        """Actualiza las estimaciones económicas del banco central"""
        # Reestimar PIB potencial cada cierto número de ciclos
        if len(self.mercado.pib_historico) % 10 == 0:
            self._estimar_pib_potencial()
        
        # Actualizar tendencia de inflación
        if hasattr(self.mercado, 'inflacion_historica') and self.mercado.inflacion_historica:
            self.tendencia_inflacion = self.mercado.inflacion_historica[-12:]  # Últimos 12 ciclos
    
    def generar_comunicado_monetario(self, decision: DecisionMonetaria) -> str:
        """Genera un comunicado oficial de política monetaria"""
        comunicado = []
        comunicado.append("="*50)
        comunicado.append("📈 COMUNICADO DE POLÍTICA MONETARIA")
        comunicado.append("="*50)
        comunicado.append(f"Ciclo: {decision.ciclo}")
        comunicado.append(f"Decisión: Tasa de interés {decision.tasa_anterior:.3f}% → {decision.tasa_nueva:.3f}%")
        comunicado.append("")
        comunicado.append("ANÁLISIS ECONÓMICO:")
        comunicado.append(f"• Inflación actual: {decision.inflacion_actual:.3f}% (objetivo: {decision.inflacion_objetivo:.3f}%)")
        comunicado.append(f"• Brecha del producto: {decision.brecha_producto:.3f}%")
        comunicado.append("")
        comunicado.append("JUSTIFICACIÓN:")
        comunicado.append(f"• {decision.justificacion}")
        comunicado.append("")
        
        if hasattr(self, 'forward_guidance') and self.forward_guidance:
            comunicado.append("ORIENTACIÓN FUTURA:")
            comunicado.append(f"• {self.forward_guidance}")
        
        comunicado.append("="*50)
        
        return "\n".join(comunicado)
    
    def obtener_efectividad_politica(self) -> Dict[str, float]:
        """Calcula métricas de efectividad de la política monetaria"""
        try:
            if len(self.decisiones_historicas) < 3:
                return {"efectividad_inflacion": 0.5, "efectividad_producto": 0.5}
            
            # Calcular qué tan cerca se ha mantenido la inflación del objetivo
            inflaciones_post_decision = []
            for i, decision in enumerate(self.decisiones_historicas[-5:]):  # Últimas 5 decisiones
                ciclo_decision = decision.ciclo
                # Buscar inflación 3 ciclos después de la decisión
                idx_futuro = None
                for j, inf in enumerate(self.mercado.inflacion_historica):
                    if j >= ciclo_decision + 3:
                        idx_futuro = j
                        break
                
                if idx_futuro and idx_futuro < len(self.mercado.inflacion_historica):
                    inflaciones_post_decision.append(self.mercado.inflacion_historica[idx_futuro])
            
            # Efectividad inflación: qué tan cerca del objetivo
            if inflaciones_post_decision:
                desviaciones_inflacion = [abs(inf - self.inflacion_objetivo) for inf in inflaciones_post_decision]
                # Menos punitivo: factor 8 en lugar de 10 para mapear a [0,1]
                efectividad_inflacion = max(0, 1 - (sum(desviaciones_inflacion) / len(desviaciones_inflacion)) * 8)
            else:
                efectividad_inflacion = 0.5
            
            # Efectividad producto: reducción de volatilidad
            if len(self.mercado.pib_historico) >= 10:
                volatilidad_pib = self._calcular_volatilidad_pib()
                efectividad_producto = max(0, 1 - volatilidad_pib * 5)
            else:
                efectividad_producto = 0.5
            
            return {
                "efectividad_inflacion": efectividad_inflacion,
                "efectividad_producto": efectividad_producto
            }
            
        except Exception as e:
            self.logger.warning(f"Error calculando efectividad: {e}")
            return {"efectividad_inflacion": 0.5, "efectividad_producto": 0.5}
    
    def _calcular_volatilidad_pib(self) -> float:
        """Calcula la volatilidad del crecimiento del PIB"""
        if len(self.mercado.pib_historico) < 5:
            return 0.1
            
        crecimientos = []
        for i in range(1, len(self.mercado.pib_historico)):
            crecimiento = (self.mercado.pib_historico[i] - self.mercado.pib_historico[i-1]) / self.mercado.pib_historico[i-1]
            crecimientos.append(crecimiento)
        
        if len(crecimientos) < 2:
            return 0.1
            
        media = sum(crecimientos) / len(crecimientos)
        varianza = sum((x - media)**2 for x in crecimientos) / len(crecimientos)
        return math.sqrt(varianza)
    
    def _calcular_tasa_con_modelos_avanzados(self, estado_economico: EstadoEconomico) -> float:
        """Calcula tasa óptima usando modelos económicos avanzados"""
        try:
            # Preparar estado económico para los modelos
            estado_actual = self._preparar_estado_para_modelos()
            
            # Ejecutar análisis completo
            analisis = self.integrador_modelos.analisis_completo(estado_actual)
            
            # Extraer recomendaciones de tasas
            if 'sintesis' in analisis and 'tasa_consenso' in analisis['sintesis']:
                tasa_consenso = analisis['sintesis']['tasa_consenso']
                
                # Ajustar según estado económico detectado por calibrador
                if self.calibrador:
                    regimen = self.calibrador.detectar_regimen_economico(estado_actual)
                    politicas = self.calibrador.sugerir_politicas_por_regimen(regimen)
                    
                    if 'tasas_sugeridas' in politicas:
                        rango_min, rango_max = politicas['tasas_sugeridas']
                        tasa_consenso = max(rango_min, min(rango_max, tasa_consenso))
                
                self.logger.info(f"🧮 Tasa consenso de modelos: {tasa_consenso:.3f}%")
                return tasa_consenso
            
            # Fallback a Taylor Rule si modelos fallan
            return self._calcular_regla_taylor()
            
        except Exception as e:
            self.logger.warning(f"Error en modelos avanzados, usando Taylor Rule: {e}")
            return self._calcular_regla_taylor()
    
    def _preparar_estado_para_modelos(self) -> Dict:
        """Prepara el estado económico para análisis de modelos"""
        
        estado = {
            'inflacion': self._obtener_inflacion_actual(),
            'desempleo': getattr(self.mercado, 'tasa_desempleo', 0.05),
            'crecimiento_pib': self._calcular_crecimiento_pib(),
            'productividad': getattr(self.mercado, 'productividad_promedio', 1.0),
            'oferta_monetaria': getattr(self.mercado, 'masa_monetaria', 1000000),
            'nivel_precios': getattr(self.mercado, 'nivel_precios_promedio', 100),
            'gasto_gobierno': getattr(self.mercado, 'gasto_publico', 0.2),
            'capital': self._estimar_stock_capital(),
            'trabajo': self._estimar_empleo_total(),
            'pib': self._obtener_pib_actual(),
            'tasa_interes': self.tasa_actual
        }
        
        return estado
    
    def _calcular_crecimiento_pib(self) -> float:
        """Calcula tasa de crecimiento del PIB"""
        if hasattr(self.mercado, 'pib_historico') and len(self.mercado.pib_historico) >= 2:
            pib_actual = self.mercado.pib_historico[-1]
            pib_anterior = self.mercado.pib_historico[-2]
            if pib_anterior > 0:
                return (pib_actual - pib_anterior) / pib_anterior
        return 0.02  # 2% default
    
    def _estimar_stock_capital(self) -> float:
        """Estima el stock de capital total de la economía"""
        if hasattr(self.mercado, 'empresas'):
            capital_total = sum(getattr(emp, 'capital', 0) for emp in self.mercado.empresas)
            return max(capital_total, 1.0)
        return 1000000  # Default
    
    def _estimar_empleo_total(self) -> float:
        """Estima el empleo total de la economía"""
        if hasattr(self.mercado, 'consumidores'):
            empleados = sum(1 for cons in self.mercado.getConsumidores() 
                          if getattr(cons, 'empleado', False))
            total_consumidores = len(self.mercado.getConsumidores())
            if total_consumidores > 0:
                return max(empleados / total_consumidores, 0.01)
        return 0.95  # 95% empleo default
    
    def _obtener_pib_actual(self) -> float:
        """Obtiene PIB actual"""
        if hasattr(self.mercado, 'pib_historico') and self.mercado.pib_historico:
            return self.mercado.pib_historico[-1]
        return 1000000  # Default
    
    def generar_reporte_avanzado(self) -> str:
        """Genera reporte avanzado de política monetaria con modelos económicos"""
        reporte = []
        reporte.append("="*60)
        reporte.append("🏦 REPORTE AVANZADO BANCO CENTRAL")
        reporte.append("="*60)
        
        # Estado actual
        reporte.append(f"Tasa de Interés Actual: {self.tasa_actual:.3f}%")
        reporte.append(f"Inflación Objetivo: {self.inflacion_objetivo:.1%}")
        reporte.append(f"Tasa Neutral Estimada: {self.tasa_neutral:.3f}%")
        
        # Integración de modelos avanzados
        if self.usar_modelos_avanzados:
            reporte.append("\n🧮 ANÁLISIS CON MODELOS AVANZADOS:")
            try:
                estado_actual = self._preparar_estado_para_modelos()
                analisis = self.integrador_modelos.analisis_completo(estado_actual)
                
                if 'sintesis' in analisis:
                    sintesis = analisis['sintesis']
                    reporte.append(f"  • PIB Consenso: {sintesis.get('pib_consenso', 'N/A')}")
                    reporte.append(f"  • Tasa Consenso: {sintesis.get('tasa_consenso', 'N/A'):.3f}%")
                    reporte.append(f"  • Consistencia Modelos: {sintesis.get('consistencia_modelos', 'N/A'):.1%}")
                
                # Régimen económico
                if self.calibrador:
                    regimen = self.calibrador.detectar_regimen_economico(estado_actual)
                    reporte.append(f"  • Régimen Detectado: {regimen}")
                    
            except Exception as e:
                reporte.append(f"  • Error en análisis: {e}")
        else:
            reporte.append("\n⚠️  Modelos avanzados NO DISPONIBLES")
        
        # Efectividad de políticas
        efectividad = self.evaluar_efectividad_politica()
        reporte.append(f"\n📊 EFECTIVIDAD DE POLÍTICA:")
        reporte.append(f"  • Control Inflación: {efectividad['efectividad_inflacion']:.1%}")
        reporte.append(f"  • Estabilidad Producto: {efectividad['efectividad_producto']:.1%}")
        
        # Decisiones recientes
        if self.decisiones_historicas:
            reporte.append(f"\n📈 ÚLTIMAS DECISIONES:")
            for decision in self.decisiones_historicas[-3:]:
                cambio_pb = int((decision.tasa_nueva - decision.tasa_anterior) * 10000)
                reporte.append(f"  • Ciclo {decision.ciclo}: {cambio_pb:+d} pb")
        
        reporte.append("="*60)
        return "\n".join(reporte)
