"""
Sistema de Banco Central con Regla de Taylor
============================================

Implementa política monetaria profesional basada en la regla de Taylor
para control de inflación y estabilidad económica.

La regla de Taylor: i = r* + π + α(π - π*) + β(y - y*)
Donde:
- i = tasa de interés nominal objetivo
- r* = tasa de interés real neutral
- π = inflación actual  
- π* = meta de inflación
- y - y* = brecha del producto
- α, β = pesos de reacción
"""

import math
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

from ..utils.SimuladorLogger import get_simulador_logger


@dataclass
class TaylorRuleParams:
    """Parámetros para la regla de Taylor"""
    tasa_neutral: float = 0.025          # Tasa de interés real neutral (2.5%)
    meta_inflacion: float = 0.025        # Meta de inflación (2.5% anual)
    peso_inflacion: float = 1.5          # Coeficiente α (reacción a inflación)
    peso_producto: float = 0.5           # Coeficiente β (reacción a brecha PIB)
    suavizamiento: float = 0.8           # Factor de suavizamiento de tasas


@dataclass
class DecisionMonetaria:
    """Registro de una decisión de política monetaria"""
    ciclo: int
    tasa_anterior: float
    tasa_nueva: float
    inflacion_actual: float
    meta_inflacion: float
    brecha_producto: float
    justificacion: str
    accion: str


class CentralBank:
    """
    Banco Central con política monetaria basada en regla de Taylor
    
    Implementa:
    - Regla de Taylor para determinación de tasas
    - Control de inflación hacia meta objetivo
    - Transmisión monetaria via sistema bancario
    - Suavizamiento de cambios de tasas
    """
    
    def __init__(self, mercado, config: Optional[Dict] = None):
        self.mercado = mercado
        self.logger = get_simulador_logger()
        
        # Configuración por defecto o desde config
        taylor_config = config.get('taylor_params', {}) if config else {}
        self.params = TaylorRuleParams(
            tasa_neutral=taylor_config.get('tasa_neutral', 0.025),
            meta_inflacion=taylor_config.get('meta_inflacion', 0.025),
            peso_inflacion=taylor_config.get('peso_inflacion', 1.5), 
            peso_producto=taylor_config.get('peso_producto', 0.5),
            suavizamiento=taylor_config.get('suavizamiento', 0.8)
        )
        
        # Estado del banco central
        self.tasa_actual = self.params.tasa_neutral
        self.tasa_anterior = self.tasa_actual
        
        # Historial para análisis
        self.historial_tasas: List[float] = [self.tasa_actual]
        self.historial_decisiones: List[DecisionMonetaria] = []
        self.historial_inflacion: List[float] = []
        
        # Límites operativos
        self.tasa_minima = 0.0       # 0% piso
        self.tasa_maxima = 0.15      # 15% techo
        
        self.logger.log_sistema(f"🏦 Banco Central inicializado - Meta inflación: {self.params.meta_inflacion:.1%}, Tasa inicial: {self.tasa_actual:.1%}")
    
    def ejecutar_politica_monetaria(self, ciclo: int) -> Dict:
        """
        Ejecuta la política monetaria aplicando la regla de Taylor
        
        Returns:
            Dict con información de la decisión monetaria
        """
        # Obtener datos económicos actuales
        inflacion_actual = self._obtener_inflacion_actual()
        brecha_producto = self._calcular_brecha_producto()
        
        # Aplicar regla de Taylor
        tasa_objetivo = self._calcular_regla_taylor(inflacion_actual, brecha_producto)
        
        # Aplicar suavizamiento
        nueva_tasa = self._aplicar_suavizamiento(tasa_objetivo)
        
        # Aplicar límites
        nueva_tasa = max(self.tasa_minima, min(self.tasa_maxima, nueva_tasa))
        
        # Crear decisión
        decision = self._crear_decision_monetaria(
            ciclo, nueva_tasa, inflacion_actual, brecha_producto
        )
        
        # Implementar decisión
        self._implementar_decision(decision)
        
        # Transmitir a sistema bancario
        self._transmitir_al_sistema_bancario()
        
        # Log de decisión
        self._log_decision(decision)
        
        return self._formatear_resultado(decision)
    
    def _calcular_regla_taylor(self, inflacion_actual: float, brecha_producto: float) -> float:
        """
        Calcula la tasa objetivo usando la regla de Taylor clásica
        
        i = r* + π + α(π - π*) + β(y - y*)
        """
        # Componentes de la regla de Taylor
        tasa_neutral = self.params.tasa_neutral
        brecha_inflacion = inflacion_actual - self.params.meta_inflacion
        
        # Regla de Taylor
        tasa_objetivo = (
            tasa_neutral +                                          # r*
            inflacion_actual +                                      # π
            self.params.peso_inflacion * brecha_inflacion +         # α(π - π*)
            self.params.peso_producto * brecha_producto             # β(y - y*)
        )
        
        return tasa_objetivo
    
    def _obtener_inflacion_actual(self) -> float:
        """Obtiene la inflación actual del mercado"""
        try:
            if hasattr(self.mercado, 'inflacion_historica') and self.mercado.inflacion_historica:
                inflacion = self.mercado.inflacion_historica[-1]
                self.historial_inflacion.append(inflacion)
                return inflacion
            else:
                # Inflación por defecto si no hay datos
                return 0.02
        except Exception as e:
            self.logger.warning(f"Error obteniendo inflación: {e}")
            return 0.02
    
    def _calcular_brecha_producto(self) -> float:
        """Calcula la brecha del producto (PIB actual vs PIB potencial)"""
        try:
            if hasattr(self.mercado, 'pib_historico') and len(self.mercado.pib_historico) > 1:
                pib_actual = self.mercado.pib_historico[-1]
                pib_anterior = self.mercado.pib_historico[-2]
                
                # Crecimiento actual
                crecimiento_actual = (pib_actual - pib_anterior) / pib_anterior if pib_anterior > 0 else 0.0
                
                # Asumimos crecimiento potencial del 2.5% anual (aprox 0.6% por ciclo)
                crecimiento_potencial = 0.006
                
                brecha = crecimiento_actual - crecimiento_potencial
                
                # Limitar brecha a rangos razonables
                return max(-0.1, min(0.1, brecha))
            else:
                return 0.0
        except Exception as e:
            self.logger.warning(f"Error calculando brecha del producto: {e}")
            return 0.0
    
    def _aplicar_suavizamiento(self, tasa_objetivo: float) -> float:
        """Aplica suavizamiento gradual a los cambios de tasa"""
        # Suavizamiento: nueva_tasa = λ * tasa_objetivo + (1-λ) * tasa_actual
        nueva_tasa = (
            (1 - self.params.suavizamiento) * tasa_objetivo +
            self.params.suavizamiento * self.tasa_actual
        )
        return nueva_tasa
    
    def _crear_decision_monetaria(self, ciclo: int, nueva_tasa: float, 
                                inflacion_actual: float, brecha_producto: float) -> DecisionMonetaria:
        """Crea el registro de la decisión monetaria"""
        
        # Determinar tipo de acción
        diferencia_tasa = nueva_tasa - self.tasa_actual
        
        if abs(diferencia_tasa) < 0.0025:  # Menos de 25 puntos básicos
            accion = "MANTENER"
        elif diferencia_tasa > 0:
            accion = "SUBIR" if diferencia_tasa > 0.005 else "SUBIR_LEVE"
        else:
            accion = "BAJAR" if diferencia_tasa < -0.005 else "BAJAR_LEVE"
        
        # Justificación basada en Taylor rule
        brecha_inflacion = inflacion_actual - self.params.meta_inflacion
        justificacion = self._generar_justificacion(brecha_inflacion, brecha_producto, accion)
        
        return DecisionMonetaria(
            ciclo=ciclo,
            tasa_anterior=self.tasa_actual,
            tasa_nueva=nueva_tasa,
            inflacion_actual=inflacion_actual,
            meta_inflacion=self.params.meta_inflacion,
            brecha_producto=brecha_producto,
            justificacion=justificacion,
            accion=accion
        )
    
    def _generar_justificacion(self, brecha_inflacion: float, 
                             brecha_producto: float, accion: str) -> str:
        """Genera justificación técnica para la decisión"""
        componentes = []
        
        if abs(brecha_inflacion) > 0.005:  # > 0.5%
            if brecha_inflacion > 0:
                componentes.append(f"inflación {brecha_inflacion:.1%} sobre meta")
            else:
                componentes.append(f"inflación {abs(brecha_inflacion):.1%} bajo meta")
        
        if abs(brecha_producto) > 0.01:  # > 1%
            if brecha_producto > 0:
                componentes.append("actividad económica robusta")
            else:
                componentes.append("actividad económica débil")
        
        if componentes:
            razon = " y ".join(componentes)
            return f"{accion.lower()} tasa por {razon}"
        else:
            return f"{accion.lower()} tasa por condiciones estables"
    
    def _implementar_decision(self, decision: DecisionMonetaria) -> None:
        """Implementa la decisión actualizando el estado interno"""
        self.tasa_anterior = self.tasa_actual
        self.tasa_actual = decision.tasa_nueva
        
        # Actualizar historiales
        self.historial_tasas.append(self.tasa_actual)
        self.historial_decisiones.append(decision)
    
    def _transmitir_al_sistema_bancario(self) -> None:
        """Transmite el cambio de tasa al sistema bancario"""
        try:
            if hasattr(self.mercado, 'sistema_bancario') and self.mercado.sistema_bancario:
                # Actualizar tasa de referencia del banco central en el sistema bancario
                if hasattr(self.mercado.sistema_bancario, 'banco_central'):
                    self.mercado.sistema_bancario.banco_central.tasa_referencia = self.tasa_actual
                
                # Transmitir a bancos individuales (spread típico de 2-4%)
                for banco in self.mercado.sistema_bancario.bancos:
                    spread_banco = 0.03  # Spread base de 3%
                    banco.tasa_base_prestamos = self.tasa_actual + spread_banco
                    
                    # Ajustar tasa de depósitos (típicamente menor)
                    if hasattr(banco, 'tasa_depositos'):
                        banco.tasa_depositos = max(0.001, self.tasa_actual - 0.01)
                        
        except Exception as e:
            self.logger.warning(f"Error en transmisión a sistema bancario: {e}")
    
    def _log_decision(self, decision: DecisionMonetaria) -> None:
        """Log detallado de la decisión monetaria"""
        cambio_pb = int((decision.tasa_nueva - decision.tasa_anterior) * 10000)
        
        self.logger.log_sistema(
            f"🏦 Banco Central - Ciclo {decision.ciclo}: {decision.accion} "
            f"({cambio_pb:+d} pb) → {decision.tasa_nueva:.2%}"
        )
        self.logger.log_sistema(f"   📊 Inflación: {decision.inflacion_actual:.1%} (meta: {decision.meta_inflacion:.1%})")
        self.logger.log_sistema(f"   📈 Brecha producto: {decision.brecha_producto:.1%}")
        self.logger.log_sistema(f"   💡 {decision.justificacion}")
    
    def _formatear_resultado(self, decision: DecisionMonetaria) -> Dict:
        """Formatea el resultado para compatibilidad con el sistema existente"""
        return {
            'decision_monetaria': decision,
            'tasa_interes': self.tasa_actual,
            'tasa_anterior': self.tasa_anterior,
            'justificacion': decision.justificacion,
            'accion': decision.accion,
            'accion_tomada': True,
            'descripcion': f"Taylor Rule: {decision.accion}",
            'nueva_tasa': self.tasa_actual * 100,  # Porcentaje para compatibilidad
            'inflacion_actual': decision.inflacion_actual,
            'meta_inflacion': decision.meta_inflacion,
            'brecha_producto': decision.brecha_producto
        }
    
    def obtener_estadisticas(self) -> Dict:
        """Retorna estadísticas del desempeño del banco central"""
        if not self.historial_decisiones:
            return {'decisiones_totales': 0}
        
        # Calcular métricas de desempeño
        inflaciones = [d.inflacion_actual for d in self.historial_decisiones]
        brechas_inflacion = [abs(d.inflacion_actual - d.meta_inflacion) for d in self.historial_decisiones]
        
        return {
            'decisiones_totales': len(self.historial_decisiones),
            'tasa_actual': self.tasa_actual,
            'tasa_inicial': self.historial_tasas[0],
            'inflacion_promedio': sum(inflaciones) / len(inflaciones) if inflaciones else 0,
            'brecha_inflacion_promedio': sum(brechas_inflacion) / len(brechas_inflacion) if brechas_inflacion else 0,
            'cambios_tasa_totales': len([d for d in self.historial_decisiones if d.accion != 'MANTENER']),
            'convergencia_inflacion': sum(1 for b in brechas_inflacion if b < 0.005) / len(brechas_inflacion) if brechas_inflacion else 0
        }
    
    def simular_shock_inflacionario(self, magnitud_shock: float = 0.03) -> Dict:
        """
        Simula respuesta a un shock inflacionario para testing
        
        Args:
            magnitud_shock: Magnitud del shock (default 3%)
        
        Returns:
            Respuesta simulada del banco central
        """
        # Simular inflación elevada
        inflacion_con_shock = self.params.meta_inflacion + magnitud_shock
        brecha_producto_normal = 0.0
        
        # Calcular respuesta según Taylor rule
        tasa_respuesta = self._calcular_regla_taylor(inflacion_con_shock, brecha_producto_normal)
        
        # Sin suavizamiento para shock (respuesta inmediata)
        diferencia_tasa = tasa_respuesta - self.tasa_actual
        
        return {
            'shock_inflacion': magnitud_shock,
            'inflacion_resultante': inflacion_con_shock,
            'tasa_respuesta': tasa_respuesta,
            'cambio_tasa': diferencia_tasa,
            'cambio_puntos_basicos': int(diferencia_tasa * 10000),
            'respuesta_adecuada': diferencia_tasa > 0 and diferencia_tasa > magnitud_shock * self.params.peso_inflacion
        }