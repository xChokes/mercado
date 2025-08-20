"""
Sistema de Banco Central para Control Monetario Realista MEJORADO
Implementa política monetaria automática tipo Fed/BCE con Taylor Rule
"""

import random
import math
from ..utils.SimuladorLogger import get_simulador_logger

class BancoCentral:
    """Banco Central con política monetaria automática MEJORADA"""
    
    def __init__(self, mercado):
        self.mercado = mercado
        
        # CONFIGURACIÓN MEJORADA basada en ConfigEconomica
        from src.config.ConfigEconomica import ConfigEconomica
        
        self.tasa_interes_base = ConfigEconomica.TASA_INTERES_NEUTRAL  # 3% inicial
        self.meta_inflacion = ConfigEconomica.INFLACION_OBJETIVO_CICLO  # 0.25% por ciclo
        self.tolerancia_inflacion = ConfigEconomica.INFLACION_TOLERANCIA / 12  # Tolerancia por ciclo
        
        # Límites de tasa de interés
        self.tasa_minima = ConfigEconomica.TASA_INTERES_MINIMA  # 0.1%
        self.tasa_maxima = ConfigEconomica.TASA_INTERES_MAXIMA  # 25%
        
        # Herramientas de política monetaria
        self.multiplicador_monetario = 1.0
        self.reservas_obligatorias = 0.1  # 10%
        
        # NUEVOS: Parámetros de Taylor Rule refinada
        self.peso_inflacion = 2.0      # Peso alta para inflación
        self.peso_pib = 0.3           # Peso moderado para PIB
        self.suavizado_tasa = 0.3     # Suavizado de cambios (30% por ciclo)
        
        # Logger y historial
        self.logger = get_simulador_logger()
        self.historial_tasas = [self.tasa_interes_base]
        self.historial_decisiones = []
        
        self.logger.log_sistema(f"Banco Central creado - Tasa inicial: {self.tasa_interes_base:.2%}")
    
    def ejecutar_politica_monetaria(self, ciclo):
        """Ejecuta política monetaria basada en condiciones económicas"""
        
        # Obtener métricas económicas actuales
        inflacion = self.calcular_inflacion()
        crecimiento_pib = self.calcular_crecimiento_pib()
        desempleo = self.calcular_tasa_desempleo()
        
        # Tomar decisión de política monetaria
        decision = self.tomar_decision_monetaria(inflacion, crecimiento_pib, desempleo)
        
        # Aplicar medidas
        self.aplicar_medidas_monetarias(decision, ciclo)
        
        # Log de la decisión
        self.logger.log_sistema(f"🏦 Banco Central - Ciclo {ciclo}: Política {decision['accion']}: {decision['justificacion']}")
        self.logger.log_sistema(f"   Nueva tasa: {self.tasa_interes_base:.2%}, Justificación: {decision['justificacion']}")
        
        return {
            'decision_monetaria': decision,
            'tasa_interes': self.tasa_interes_base,
            'justificacion': decision['justificacion'],
            'accion': decision['accion']
        }
        
    def tomar_decision_monetaria(self, inflacion, crecimiento_pib, desempleo):
        """Toma decisiones de política monetaria tipo regla de Taylor MEJORADA"""
        
        # Regla de Taylor avanzada para control fino
        brecha_inflacion = inflacion - self.meta_inflacion
        brecha_pib = max(-0.05, min(0.05, crecimiento_pib - 0.025))  # PIB potencial 2.5%
        
        # NUEVA: Cálculo de tasa objetivo con Taylor Rule refinada
        tasa_neutral = 0.03  # Tasa neutral real del 3%
        peso_inflacion = 2.0  # Peso para inflación (más agresivo)
        peso_pib = 0.3  # Peso para brecha PIB (menos peso)
        
        tasa_objetivo = (
            tasa_neutral +
            peso_inflacion * brecha_inflacion +
            peso_pib * brecha_pib
        )
        
        # Límites de la tasa objetivo
        tasa_objetivo = max(0.001, min(0.25, tasa_objetivo))
        
        # NUEVO: Bandas de inflación más estrictas para control fino
        if inflacion > 0.04:  # Inflación > 4% = acción inmediata (antes 5%)
            if inflacion > 0.08:  # > 8% = emergencia total (antes 10%)
                return self._decision_antiinflacionaria_emergencia(inflacion, tasa_objetivo)
            elif inflacion > 0.05:  # 5-8% = agresiva
                return self._decision_antiinflacionaria_agresiva(inflacion)
            else:  # 4-5% = moderada pero inmediata
                return self._decision_antiinflacionaria_moderada(inflacion)
                
        elif inflacion < 0.02:  # Deflación o inflación muy baja
            if desempleo > 0.08:  # Desempleo > 8% = problema
                return self._decision_expansiva(inflacion, desempleo)
            else:
                return self._decision_neutral()
        else:
            # 2-4% = zona objetivo, política neutral con ajustes finos
            return self._decision_ajuste_fino(inflacion, tasa_objetivo)
    
    def _decision_antiinflacionaria_emergencia(self, inflacion, tasa_objetivo):
        """NUEVA: Política de emergencia para inflación > 8%"""
        # Respuesta ultra-agresiva: aumentar tasa inmediatamente al máximo necesario
        nueva_tasa = min(0.25, max(tasa_objetivo, inflacion * 1.5))
        
        return {
            'tasa_interes': nueva_tasa,
            'accion': 'EMERGENCIA_ANTIINFLACION',
            'justificacion': f'EMERGENCIA: Inflación {inflacion:.1%} requiere máxima contracción',
            'transmision_inmediata': True  # Aplicar efecto inmediato
        }
    
    def _decision_ajuste_fino(self, inflacion, tasa_objetivo):
        """NUEVA: Ajustes finos dentro de la banda objetivo (2-4%)"""
        # Movimientos graduales hacia la tasa objetivo
        diferencia = tasa_objetivo - self.tasa_interes_base
        ajuste = diferencia * 0.3  # Ajuste gradual del 30%
        nueva_tasa = self.tasa_interes_base + ajuste
        
        if abs(ajuste) < 0.0025:  # Cambio menor a 0.25%
            accion = 'MANTENIMIENTO'
            justificacion = f'Inflación {inflacion:.1%} dentro del target, mantener política'
        elif ajuste > 0:
            accion = 'AJUSTE_CONTRACTIVO'
            justificacion = f'Ajuste gradual hacia target: inflación {inflacion:.1%}'
        else:
            accion = 'AJUSTE_EXPANSIVO'
            justificacion = f'Ajuste gradual hacia target: inflación {inflacion:.1%}'
        
        return {
            'tasa_interes': nueva_tasa,
            'accion': accion,
            'justificacion': justificacion,
            'transmision_inmediata': False
        }

    def _decision_antiinflacionaria_agresiva(self, inflacion):
        """Política contractiva agresiva para hiperinflación MEJORADA"""
        # Política más agresiva: respuesta de 2x la inflación
        aumento_tasa = min(0.10, inflacion * 2.0)  # Máximo 10% de aumento
        nueva_tasa = min(0.25, self.tasa_interes_base + aumento_tasa)  # Máximo 25%
        
        return {
            'accion': 'CONTRACCION_AGRESIVA',
            'tasa_interes': nueva_tasa,
            'reservas': min(0.30, self.reservas_obligatorias + 0.10),  # Aumentar reservas
            'multiplicador': max(0.3, self.multiplicador_monetario - 0.5),  # Más contractivo
            'justificacion': f'Combatir hiperinflación del {inflacion:.1%}'
        }
    
    def _decision_antiinflacionaria_moderada(self, inflacion):
        """Política contractiva moderada"""
        aumento_tasa = min(0.02, (inflacion - self.meta_inflacion) * 2)
        nueva_tasa = min(0.15, self.tasa_interes_base + aumento_tasa)
        
        return {
            'accion': 'CONTRACCION_MODERADA',
            'tasa_interes': nueva_tasa,
            'reservas': min(0.20, self.reservas_obligatorias + 0.05),
            'multiplicador': max(0.5, self.multiplicador_monetario - 0.3),
            'justificacion': f'Controlar inflación del {inflacion:.1%}'
        }
    
    def _decision_expansiva(self, inflacion, desempleo):
        """Política expansiva para estimular crecimiento"""
        reduccion_tasa = min(0.02, (self.meta_inflacion - inflacion) * 1.5)
        nueva_tasa = max(0.01, self.tasa_interes_base - reduccion_tasa)
        
        return {
            'accion': 'EXPANSION',
            'tasa_interes': nueva_tasa,
            'reservas': max(0.05, self.reservas_obligatorias - 0.05),
            'multiplicador': min(2.0, self.multiplicador_monetario + 0.5),
            'justificacion': f'Estimular economía (desempleo: {desempleo:.1%})'
        }
    
    def _decision_neutral(self):
        """Política neutral - mantener"""
        return {
            'accion': 'MANTENER',
            'tasa_interes': self.tasa_interes_base,
            'reservas': self.reservas_obligatorias,
            'multiplicador': self.multiplicador_monetario,
            'justificacion': 'Mantener estabilidad'
        }
    
    def aplicar_medidas_monetarias(self, decision, ciclo):
        """Aplica las medidas de política monetaria con mayor efectividad"""
        
        # CORRECCIÓN: Usar la key correcta según el tipo de decisión
        nueva_tasa = decision.get('tasa_interes', decision.get('nueva_tasa', self.tasa_interes_base))
        
        # Actualizar tasa de interés con menos inercia para mayor efectividad
        if decision['accion'] in ['EMERGENCIA_ANTIINFLACION', 'CONTRACCION_AGRESIVA']:
            # En crisis de inflación, cambios más rápidos
            factor_suavizado = decision.get('transmision_inmediata', False) and 1.0 or 0.9
            cambio_tasa = (nueva_tasa - self.tasa_interes_base) * factor_suavizado
        else:
            # Cambio normal con algo de inercia
            cambio_tasa = (nueva_tasa - self.tasa_interes_base) * self.suavizado_tasa
        
        self.tasa_interes_base += cambio_tasa
        self.tasa_interes_base = max(self.tasa_minima, min(self.tasa_maxima, self.tasa_interes_base))
        
        # Aplicar efectos a precios (canal de transmisión MEJORADO)
        self._aplicar_efectos_precios_mejorados(decision)
        
        # Registrar decisión
        self.historial_tasas.append(self.tasa_interes_base)
        self.historial_decisiones.append({
            'ciclo': ciclo,
            'decision': decision['accion'],
            'tasa': self.tasa_interes_base,
            'justificacion': decision['justificacion']
        })
    
    def _aplicar_efectos_precios_mejorados(self, decision):
        """Aplica efectos de política monetaria a la formación de precios MEJORADO"""
        # Aplicar efectos a través del controlador de precios realista si existe
        if hasattr(self.mercado, 'controlador_precios'):
            
            # NUEVO: Transmisión inmediata para decisiones de emergencia
            transmision_inmediata = decision.get('transmision_inmediata', False)
            factor_transmision = 0.9 if transmision_inmediata else 0.7  # 90% vs 70%
            
            # Política contractiva reduce presión inflacionaria - MÁS AGRESIVA
            if decision['accion'] in ['EMERGENCIA_ANTIINFLACION', 'CONTRACCION_AGRESIVA', 'CONTRACCION_MODERADA', 'AJUSTE_CONTRACTIVO']:
                # Efecto más fuerte: usar tasa real vs neutral
                diferencia_tasa = self.tasa_interes_base - 0.03  # vs tasa neutral 3%
                efecto_contractivo = diferencia_tasa * factor_transmision
                factor_deflacionario = 1 - efecto_contractivo
                factor_deflacionario = max(0.3, min(1.0, factor_deflacionario))  # Entre 30% y 100%
                
                # Aplicar factor + llamar método de control de inflación
                self.mercado.controlador_precios.factor_monetario = factor_deflacionario
                
                # NUEVO: Para emergencias, aplicar presión deflacionaria adicional
                if decision['accion'] == 'EMERGENCIA_ANTIINFLACION':
                    if hasattr(self.mercado.controlador_precios, 'activar_deflacion_emergencia'):
                        self.mercado.controlador_precios.activar_deflacion_emergencia(0.5)  # 50% de fuerza
                    
            # Política expansiva aumenta presión inflacionaria  
            elif decision['accion'] in ['EXPANSION_AGRESIVA', 'EXPANSION_MODERADA', 'EXPANSION', 'AJUSTE_EXPANSIVO']:
                diferencia_tasa = 0.03 - self.tasa_interes_base  # Cuanto más baja la tasa
                factor_inflacionario = 1 + (diferencia_tasa * factor_transmision * 0.3)
                factor_inflacionario = max(1.0, min(1.3, factor_inflacionario))  # Entre 100% y 130%
                self.mercado.controlador_precios.factor_monetario = factor_inflacionario
            else:
                # Política neutral o mantenimiento
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

    def calcular_inflacion(self):
        """Calcula inflación actual"""
        if len(self.mercado.precio_historico) < 2:
            return 0.0
        
        precio_actual = self.mercado.precio_historico[-1]
        precio_anterior = self.mercado.precio_historico[-2]
        
        if precio_anterior > 0:
            return (precio_actual - precio_anterior) / precio_anterior
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
