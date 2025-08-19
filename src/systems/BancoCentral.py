"""
Sistema de Banco Central para Control Monetario Realista
Implementa política monetaria automática tipo Fed/BCE
"""

import random
import math
from ..utils.SimuladorLogger import get_simulador_logger

class BancoCentral:
    """Banco Central con política monetaria automática"""
    
    def __init__(self, mercado):
        self.mercado = mercado
        self.tasa_interes_base = 0.05  # 5% inicial
        self.meta_inflacion = 0.02     # 2% objetivo
        self.tolerancia_inflacion = 0.01  # ±1% de tolerancia
        
        # Herramientas de política monetaria
        self.multiplicador_monetario = 1.0
        self.reservas_obligatorias = 0.1  # 10%
        
        # Historial para decisiones
        self.historial_tasas = [self.tasa_interes_base]
        self.historial_decisiones = []
        
        self.logger = get_simulador_logger()
        
    def ejecutar_politica_monetaria(self, ciclo):
        """Ejecuta política monetaria basada en indicadores económicos"""
        
        # Obtener indicadores actuales
        inflacion_actual = self.mercado.inflacion_historica[-1] if self.mercado.inflacion_historica else 0
        pib_crecimiento = self.calcular_crecimiento_pib()
        desempleo = self.calcular_tasa_desempleo()
        
        # Decisión de política monetaria
        decision = self.tomar_decision_monetaria(inflacion_actual, pib_crecimiento, desempleo)
        
        # Aplicar medidas
        self.aplicar_medidas_monetarias(decision, ciclo)
        
        # Log de la decisión
        self.logger.log_sistema(f"Banco Central - Ciclo {ciclo}: {decision['accion']} - Tasa: {self.tasa_interes_base:.2%}")
        
        # Devolver información de la decisión
        return {
            'accion_tomada': True,
            'descripcion': f"Política {decision['accion']}: {decision['justificacion']}",
            'nueva_tasa': self.tasa_interes_base,
            'justificacion': decision['justificacion'],
            'accion': decision['accion']
        }
        
    def tomar_decision_monetaria(self, inflacion, crecimiento_pib, desempleo):
        """Toma decisiones de política monetaria tipo regla de Taylor"""
        
        # Regla de Taylor modificada
        brecha_inflacion = inflacion - self.meta_inflacion
        brecha_pib = max(-0.05, min(0.05, crecimiento_pib - 0.025))  # PIB potencial 2.5%
        
        # Cálculo de tasa objetivo
        tasa_objetivo = (
            self.meta_inflacion +  # Tasa real neutral
            1.5 * brecha_inflacion +  # Respuesta a inflación
            0.5 * brecha_pib  # Respuesta a ciclo económico
        )
        
        # Decisión basada en prioridades
        if inflacion > self.meta_inflacion + self.tolerancia_inflacion:
            if inflacion > 0.10:  # Inflación > 10% = emergencia
                return self._decision_antiinflacionaria_agresiva(inflacion)
            else:
                return self._decision_antiinflacionaria_moderada(inflacion)
                
        elif inflacion < self.meta_inflacion - self.tolerancia_inflacion:
            if desempleo > 0.08:  # Desempleo > 8% = problema
                return self._decision_expansiva(inflacion, desempleo)
            else:
                return self._decision_neutral()
        else:
            return self._decision_neutral()
    
    def _decision_antiinflacionaria_agresiva(self, inflacion):
        """Política contractiva agresiva para hiperinflación"""
        aumento_tasa = min(0.05, inflacion * 0.5)  # Máximo 5% de aumento
        nueva_tasa = min(0.20, self.tasa_interes_base + aumento_tasa)  # Máximo 20%
        
        return {
            'accion': 'CONTRACCION_AGRESIVA',
            'nueva_tasa': nueva_tasa,
            'reservas': min(0.25, self.reservas_obligatorias + 0.05),
            'multiplicador': max(0.5, self.multiplicador_monetario - 0.3),
            'justificacion': f'Combatir hiperinflación del {inflacion:.1%}'
        }
    
    def _decision_antiinflacionaria_moderada(self, inflacion):
        """Política contractiva moderada"""
        aumento_tasa = min(0.02, (inflacion - self.meta_inflacion) * 2)
        nueva_tasa = min(0.15, self.tasa_interes_base + aumento_tasa)
        
        return {
            'accion': 'CONTRACCION_MODERADA',
            'nueva_tasa': nueva_tasa,
            'reservas': min(0.20, self.reservas_obligatorias + 0.02),
            'multiplicador': max(0.7, self.multiplicador_monetario - 0.1),
            'justificacion': f'Controlar inflación del {inflacion:.1%}'
        }
    
    def _decision_expansiva(self, inflacion, desempleo):
        """Política expansiva para estimular economía"""
        reduccion_tasa = min(0.02, (self.meta_inflacion - inflacion) * 1.5)
        nueva_tasa = max(0.01, self.tasa_interes_base - reduccion_tasa)
        
        return {
            'accion': 'EXPANSION',
            'nueva_tasa': nueva_tasa,
            'reservas': max(0.05, self.reservas_obligatorias - 0.02),
            'multiplicador': min(1.5, self.multiplicador_monetario + 0.1),
            'justificacion': f'Estimular economía (desempleo: {desempleo:.1%})'
        }
    
    def _decision_neutral(self):
        """Mantener política actual"""
        return {
            'accion': 'MANTENER',
            'nueva_tasa': self.tasa_interes_base,
            'reservas': self.reservas_obligatorias,
            'multiplicador': self.multiplicador_monetario,
            'justificacion': 'Mantener estabilidad'
        }
    
    def aplicar_medidas_monetarias(self, decision, ciclo):
        """Aplica las medidas de política monetaria"""
        
        # Actualizar tasa de interés gradualmente (inercia realista)
        cambio_tasa = (decision['nueva_tasa'] - self.tasa_interes_base) * 0.7
        self.tasa_interes_base += cambio_tasa
        
        # Actualizar otras herramientas
        self.reservas_obligatorias = decision['reservas']
        self.multiplicador_monetario = decision['multiplicador']
        
        # Aplicar efectos al sistema bancario
        if hasattr(self.mercado, 'sistema_bancario'):
            self._aplicar_efectos_bancarios(decision)
        
        # Aplicar efectos a precios (canal de transmisión)
        self._aplicar_efectos_precios(decision)
        
        # Registrar decisión
        self.historial_tasas.append(self.tasa_interes_base)
        self.historial_decisiones.append({
            'ciclo': ciclo,
            'decision': decision['accion'],
            'tasa': self.tasa_interes_base,
            'justificacion': decision['justificacion']
        })
    
    def _aplicar_efectos_bancarios(self, decision):
        """Aplica efectos de política monetaria al sistema bancario"""
        for banco in self.mercado.sistema_bancario.bancos:
            # Ajustar tasas de préstamos (usar spread de 3% como margen bancario estándar)
            margen_bancario = 0.03  # 3% de margen bancario estándar
            banco.tasa_base_prestamos = self.tasa_interes_base + margen_bancario
            
            # Ajustar reservas obligatorias
            depositos_totales = sum(banco.depositos.values())
            reservas_requeridas = depositos_totales * self.reservas_obligatorias
            if banco.reservas < reservas_requeridas:
                # Banco debe aumentar reservas
                deficit_reservas = reservas_requeridas - banco.reservas
                # Simplificación: ajustar capital en lugar de reducir préstamos
                banco.capital -= deficit_reservas * 0.1  # Costo de ajuste
    
    def _aplicar_efectos_precios(self, decision):
        """Aplica efectos de política monetaria a la formación de precios"""
        # Aplicar efectos a través del controlador de precios realista si existe
        if hasattr(self.mercado, 'controlador_precios'):
            # Política contractiva reduce presión inflacionaria
            if decision['accion'] in ['CONTRACCION_AGRESIVA', 'CONTRACCION_MODERADA']:
                factor_deflacionario = 1 - (self.tasa_interes_base - 0.05) * 0.3
                self.mercado.controlador_precios.factor_monetario = factor_deflacionario
            # Política expansiva aumenta presión inflacionaria  
            elif decision['accion'] in ['EXPANSION_AGRESIVA', 'EXPANSION_MODERADA', 'EXPANSION']:
                factor_inflacionario = 1 + (0.05 - self.tasa_interes_base) * 0.3
                self.mercado.controlador_precios.factor_monetario = factor_inflacionario
            else:
                # Política neutral
                self.mercado.controlador_precios.factor_monetario = 1.0
    
    def calcular_crecimiento_pib(self):
        """Calcula tasa de crecimiento del PIB"""
        if len(self.mercado.pib_historico) < 2:
            return 0.0
        
        pib_actual = self.mercado.pib_historico[-1]
        pib_anterior = self.mercado.pib_historico[-2]
        
        if pib_anterior > 0:
            return (pib_actual - pib_anterior) / pib_anterior
        return 0.0
    
    def calcular_tasa_desempleo(self):
        """Calcula tasa de desempleo actual"""
        total_consumidores = len([p for p in self.mercado.personas 
                                if hasattr(p, 'empleado')])
        if total_consumidores == 0:
            return 0.0
        
        desempleados = len([p for p in self.mercado.personas 
                          if hasattr(p, 'empleado') and not p.empleado])
        return desempleados / total_consumidores
    
    def obtener_reporte_monetario(self):
        """Genera reporte del estado de la política monetaria"""
        inflacion_actual = self.mercado.inflacion_historica[-1] if self.mercado.inflacion_historica else 0
        
        return {
            'tasa_interes': self.tasa_interes_base,
            'meta_inflacion': self.meta_inflacion,
            'inflacion_actual': inflacion_actual,
            'brecha_inflacion': inflacion_actual - self.meta_inflacion,
            'stance_monetario': self._evaluar_stance_monetario(),
            'ultima_decision': self.historial_decisiones[-1] if self.historial_decisiones else None
        }
    
    def _evaluar_stance_monetario(self):
        """Evalúa si la política es expansiva, neutral o contractiva"""
        if self.tasa_interes_base > 0.07:
            return 'CONTRACTIVA'
        elif self.tasa_interes_base < 0.03:
            return 'EXPANSIVA'
        else:
            return 'NEUTRAL'
