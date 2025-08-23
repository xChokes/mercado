"""
Sistema de Validación Económica Profesional
==========================================

Valida que el simulador produzca resultados económicamente realistas
comparando con rangos y ratios estándar de la literatura económica.
"""

import math
import logging
import sys
import os
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

try:
    from src.config.DatosEconomicosReales import CalibradorEconomicoRealista
except ImportError:
    CalibradorEconomicoRealista = None

class TipoAlerta(Enum):
    """Tipos de alertas económicas"""
    CRITICA = "CRITICA"
    ADVERTENCIA = "ADVERTENCIA"
    INFO = "INFO"


@dataclass
class AlertaEconomica:
    """Alerta del sistema de validación"""
    tipo: TipoAlerta
    indicador: str
    valor_actual: float
    rango_normal: Tuple[float, float]
    mensaje: str
    ciclo: int


class ValidadorEconomico:
    """
    Sistema de validación que monitorea indicadores económicos
    y alerta sobre comportamientos no realistas.
    """
    
    def __init__(self):
        self.logger = logging.getLogger('ValidadorEconomico')
        # Compatibilidad con tests básicos
        self.alertas: List[AlertaEconomica] = []
        self.indicadores: Dict[str, List[float]] = {}
        self.alertas_historicas = []
        
        # Inicializar calibrador si está disponible
        if CalibradorEconomicoRealista:
            self.calibrador = CalibradorEconomicoRealista()
            self.rangos_normales = self.calibrador.generar_rangos_validacion_estrictos()
        else:
            self.calibrador = None
            self.rangos_normales = self._definir_rangos_normales()
        
        # Histórico para análisis de tendencias
        self.historico_indicadores = []
        self.regimen_economico_actual = "NORMAL"

    # --- Métodos de compatibilidad con tests unitarios básicos ---
    def validar_inflacion(self, inflacion: float) -> Dict:
        """Valida inflación simple para tests básicos.
        Retorna {'estado': 'normal'|'alerta', 'alertas': [...?]}
        """
        estado = 'normal'
        alertas = []
        # Rango razonable de inflación anual (0% - 10%)
        if inflacion < -0.01 or inflacion > 0.10:
            estado = 'alerta'
            alertas.append(f"Inflación fuera de rango: {inflacion:.3f}")
        return {'estado': estado, 'alertas': alertas}

    def validar_desempleo(self, desempleo: float) -> Dict:
        """Valida desempleo simple para tests básicos.
        Estados: normal (<10%), alerta (10-15%), critico (>=15%).
        """
        if desempleo >= 0.15:
            estado = 'critico'
        elif desempleo >= 0.10:
            estado = 'alerta'
        else:
            estado = 'normal'
        alertas = [] if estado == 'normal' else [f"Desempleo elevado: {desempleo:.3f}"]
        return {'estado': estado, 'alertas': alertas}

    def generar_reporte_estabilidad(self) -> Dict:
        """Genera reporte mínimo de estabilidad para tests básicos.
        Usa self.indicadores si están disponibles.
        """
        resumen = {}
        if self.indicadores:
            try:
                inflaciones = self.indicadores.get('inflacion', [])
                desempleos = self.indicadores.get('desempleo', [])
                pib = self.indicadores.get('pib', [])
                resumen = {
                    'inflacion_promedio': sum(inflaciones)/len(inflaciones) if inflaciones else 0.0,
                    'desempleo_promedio': sum(desempleos)/len(desempleos) if desempleos else 0.0,
                    'crecimiento_pib': ((pib[-1]-pib[0])/pib[0]) if pib and len(pib) > 1 else 0.0
                }
            except Exception:
                resumen = {}
        return {'resumen': resumen, 'indicadores': self.indicadores}
        
    def _definir_rangos_normales(self) -> Dict[str, Tuple[float, float]]:
        """Define rangos normales para indicadores económicos clave (fallback)"""
        return {
            # Rangos basados en datos del FMI y OCDE
            'inflacion_anual': (-0.02, 0.08),        # -2% a 8%
            'crecimiento_pib': (-0.05, 0.06),        # -5% a 6%
            'desempleo': (0.02, 0.15),               # 2% a 15%
            'ratio_deuda_pib': (0.20, 1.20),         # 20% a 120%
            'gini_desigualdad': (0.25, 0.65),        # 0.25 a 0.65
            'ratio_ahorro_pib': (0.10, 0.35),        # 10% a 35%
            'tasa_interes_real': (-0.02, 0.08),      # -2% a 8%
            'productividad_laboral': (0.95, 1.10),   # 95% a 110% de baseline
            'participacion_laboral': (0.55, 0.80),   # 55% a 80%
            'balanza_comercial_pib': (-0.10, 0.10),  # -10% a 10% del PIB
        }
    
    def validar_indicadores_macroeconomicos(self, mercado, ciclo: int) -> List[AlertaEconomica]:
        """Valida indicadores macroeconómicos clave"""
        alertas = []
        
        # 1. Validar inflación
        if hasattr(mercado, 'inflacion_historica') and mercado.inflacion_historica:
            inflacion_actual = mercado.inflacion_historica[-1]
            alerta = self._validar_indicador('inflacion_anual', inflacion_actual, ciclo)
            if alerta:
                alertas.append(alerta)
        
        # 2. Validar crecimiento del PIB
        if len(mercado.pib_historico) >= 2:
            crecimiento = (mercado.pib_historico[-1] - mercado.pib_historico[-2]) / mercado.pib_historico[-2]
            alerta = self._validar_indicador('crecimiento_pib', crecimiento, ciclo)
            if alerta:
                alertas.append(alerta)
        
        # 3. Validar desempleo
        if hasattr(mercado, 'desempleo_historico') and mercado.desempleo_historico:
            desempleo_actual = mercado.desempleo_historico[-1]
            alerta = self._validar_indicador('desempleo', desempleo_actual, ciclo)
            if alerta:
                alertas.append(alerta)
        
        # 4. Validar productividad laboral
        productividad = self._calcular_productividad_laboral(mercado)
        if productividad is not None:
            alerta = self._validar_indicador('productividad_laboral', productividad, ciclo)
            if alerta:
                alertas.append(alerta)
        
        # Guardar alertas
        self.alertas_historicas.extend(alertas)
        
        return alertas
    
    def _validar_indicador(self, nombre: str, valor: float, ciclo: int) -> Optional[AlertaEconomica]:
        """Valida un indicador específico contra su rango normal"""
        if nombre not in self.rangos_normales:
            return None
            
        rango_min, rango_max = self.rangos_normales[nombre]
        
        if valor < rango_min:
            tipo = TipoAlerta.CRITICA if valor < rango_min * 0.5 else TipoAlerta.ADVERTENCIA
            mensaje = f"{nombre} muy bajo: {valor:.4f} (normal: {rango_min:.4f} - {rango_max:.4f})"
            
        elif valor > rango_max:
            tipo = TipoAlerta.CRITICA if valor > rango_max * 2.0 else TipoAlerta.ADVERTENCIA
            mensaje = f"{nombre} muy alto: {valor:.4f} (normal: {rango_min:.4f} - {rango_max:.4f})"
            
        else:
            return None  # Valor dentro del rango normal
        
        return AlertaEconomica(tipo, nombre, valor, (rango_min, rango_max), mensaje, ciclo)
    
    def _calcular_productividad_laboral(self, mercado) -> Optional[float]:
        """Calcula la productividad laboral (PIB por trabajador)"""
        try:
            if not mercado.pib_historico:
                return None
                
            pib_actual = mercado.pib_historico[-1]
            
            # Contar empleados
            empleados_totales = 0
            for persona in mercado.personas:
                if hasattr(persona, 'empleado') and persona.empleado:
                    empleados_totales += 1
            
            if empleados_totales == 0:
                return None
                
            # Productividad = PIB / Número de empleados (normalizada)
            productividad_baseline = 100000 / max(1, len(mercado.personas) * 0.7)  # 70% empleo baseline
            productividad_actual = pib_actual / empleados_totales
            
            return productividad_actual / productividad_baseline
            
        except Exception as e:
            self.logger.warning(f"Error calculando productividad laboral: {e}")
            return None
    
    def detectar_anomalias_precios(self, mercado, ciclo: int) -> List[AlertaEconomica]:
        """Detecta anomalías en el sistema de precios"""
        alertas = []
        
        try:
            # Verificar precios negativos o extremos
            for persona in mercado.personas:
                if hasattr(persona, 'precios'):
                    for bien, precio in persona.precios.items():
                        if precio <= 0:
                            alerta = AlertaEconomica(
                                TipoAlerta.CRITICA,
                                f"precio_{bien}",
                                precio,
                                (0.1, 1000.0),
                                f"Precio no válido para {bien}: {precio}",
                                ciclo
                            )
                            alertas.append(alerta)
                        
                        elif precio > 10000:  # Precio extremadamente alto
                            alerta = AlertaEconomica(
                                TipoAlerta.ADVERTENCIA,
                                f"precio_{bien}",
                                precio,
                                (1.0, 1000.0),
                                f"Precio extremo para {bien}: {precio}",
                                ciclo
                            )
                            alertas.append(alerta)
        
        except Exception as e:
            self.logger.warning(f"Error detectando anomalías de precios: {e}")
        
        return alertas
    
    def calcular_indice_estabilidad(self, datos, ventana_ciclos: int = 10) -> float:
        """
        Calcula un índice de estabilidad económica (0-1)
        1 = Muy estable, 0 = Muy inestable
        """
        try:
            # Compatibilidad: si se pasa un dict de métricas simples
            if isinstance(datos, dict):
                inflacion = float(datos.get('inflacion', 0.02))
                desempleo = float(datos.get('desempleo', 0.06))
                crecimiento = float(datos.get('crecimiento_pib', 0.02))
                # Índice heurístico: penaliza alta inflación y desempleo, premia crecimiento
                score = 1.0
                score -= max(0.0, inflacion) * 2.0  # penalización
                score -= max(0.0, desempleo - 0.04) * 2.5
                score += max(0.0, crecimiento) * 1.5
                return max(0.0, min(1.0, score))

            mercado = datos
            factores_estabilidad = []
            
            # 1. Estabilidad de inflación
            if len(mercado.inflacion_historica) >= ventana_ciclos:
                inflacion_reciente = mercado.inflacion_historica[-ventana_ciclos:]
                volatilidad_inflacion = self._calcular_volatilidad(inflacion_reciente)
                estabilidad_inflacion = max(0, 1 - volatilidad_inflacion * 10)
                factores_estabilidad.append(estabilidad_inflacion)
            
            # 2. Estabilidad de crecimiento PIB
            if len(mercado.pib_historico) >= ventana_ciclos + 1:
                crecimientos = []
                for i in range(len(mercado.pib_historico) - ventana_ciclos, len(mercado.pib_historico)):
                    if i > 0:
                        crecimiento = (mercado.pib_historico[i] - mercado.pib_historico[i-1]) / mercado.pib_historico[i-1]
                        crecimientos.append(crecimiento)
                
                if crecimientos:
                    volatilidad_pib = self._calcular_volatilidad(crecimientos)
                    estabilidad_pib = max(0, 1 - volatilidad_pib * 5)
                    factores_estabilidad.append(estabilidad_pib)
            
            # 3. Estabilidad de desempleo
            if hasattr(mercado, 'desempleo_historico') and len(mercado.desempleo_historico) >= ventana_ciclos:
                desempleo_reciente = mercado.desempleo_historico[-ventana_ciclos:]
                volatilidad_desempleo = self._calcular_volatilidad(desempleo_reciente)
                estabilidad_desempleo = max(0, 1 - volatilidad_desempleo * 8)
                factores_estabilidad.append(estabilidad_desempleo)
            
            # Promedio ponderado
            if factores_estabilidad:
                return sum(factores_estabilidad) / len(factores_estabilidad)
            else:
                return 0.5  # Neutro si no hay suficientes datos
                
        except Exception as e:
            self.logger.warning(f"Error calculando índice de estabilidad: {e}")
            return 0.5
    
    def _calcular_volatilidad(self, serie: List[float]) -> float:
        """Calcula la volatilidad (desviación estándar) de una serie"""
        if len(serie) < 2:
            return 0.0
            
        media = sum(serie) / len(serie)
        varianza = sum((x - media) ** 2 for x in serie) / len(serie)
        return math.sqrt(varianza)
    
    def generar_reporte_validacion(self, mercado, ciclo: int) -> str:
        """Genera un reporte completo de validación económica"""
        alertas_actuales = self.validar_indicadores_macroeconomicos(mercado, ciclo)
        alertas_precios = self.detectar_anomalias_precios(mercado, ciclo)
        indice_estabilidad = self.calcular_indice_estabilidad(mercado)
        
        reporte = []
        reporte.append("="*60)
        reporte.append("📊 REPORTE DE VALIDACIÓN ECONÓMICA")
        reporte.append("="*60)
        reporte.append(f"Ciclo: {ciclo}")
        reporte.append(f"Índice de Estabilidad: {indice_estabilidad:.3f}")
        reporte.append("")
        
        # Alertas críticas
        alertas_criticas = [a for a in alertas_actuales + alertas_precios if a.tipo == TipoAlerta.CRITICA]
        if alertas_criticas:
            reporte.append("🚨 ALERTAS CRÍTICAS:")
            for alerta in alertas_criticas:
                reporte.append(f"  • {alerta.mensaje}")
            reporte.append("")
        
        # Advertencias
        advertencias = [a for a in alertas_actuales + alertas_precios if a.tipo == TipoAlerta.ADVERTENCIA]
        if advertencias:
            reporte.append("⚠️  ADVERTENCIAS:")
            for alerta in advertencias:
                reporte.append(f"  • {alerta.mensaje}")
            reporte.append("")
        
        # Resumen de estabilidad
        if indice_estabilidad >= 0.8:
            reporte.append("✅ Estado económico: ESTABLE")
        elif indice_estabilidad >= 0.6:
            reporte.append("⚠️  Estado económico: MODERADAMENTE ESTABLE")
        elif indice_estabilidad >= 0.4:
            reporte.append("🔶 Estado económico: INESTABLE")
        else:
            reporte.append("🚨 Estado económico: MUY INESTABLE")
        
        reporte.append("="*60)
        
        return "\n".join(reporte)
    
    def obtener_alertas_recientes(self, ultimos_ciclos: int = 5) -> List[AlertaEconomica]:
        """Obtiene las alertas de los últimos ciclos"""
        alertas_recientes = []
        for alerta in self.alertas_historicas:
            if hasattr(alerta, 'ciclo') and alerta.ciclo >= (len(self.historico_indicadores) - ultimos_ciclos):
                alertas_recientes.append(alerta)
        return alertas_recientes
    
    def analizar_regimen_economico(self, mercado) -> str:
        """Analiza y determina el régimen económico actual"""
        if not self.calibrador:
            return "NORMAL"
        
        try:
            # Calcular indicadores clave
            indicadores = {
                'inflacion': getattr(mercado, 'inflacion_anual', 0.02),
                'desempleo': getattr(mercado, 'tasa_desempleo', 0.05),
                'crecimiento_pib': getattr(mercado, 'crecimiento_pib', 0.02)
            }
            
            # Detectar régimen con el calibrador
            regimen = self.calibrador.detectar_regimen_economico(indicadores)
            self.regimen_economico_actual = regimen
            
            # Log del cambio de régimen
            if hasattr(self, '_regimen_anterior') and self._regimen_anterior != regimen:
                self.logger.info(f"📊 Cambio de régimen económico: {self._regimen_anterior} → {regimen}")
            
            self._regimen_anterior = regimen
            return regimen
            
        except Exception as e:
            self.logger.warning(f"Error analizando régimen económico: {e}")
            return "NORMAL"
    
    def sugerir_politicas_economicas(self, mercado) -> Dict:
        """Sugiere políticas económicas basadas en el régimen actual"""
        if not self.calibrador:
            return {"mensaje": "Calibrador no disponible"}
        
        try:
            regimen = self.analizar_regimen_economico(mercado)
            politicas = self.calibrador.sugerir_politicas_por_regimen(regimen)
            
            return {
                'regimen_detectado': regimen,
                'politicas_sugeridas': politicas,
                'timestamp': len(self.historico_indicadores)
            }
            
        except Exception as e:
            self.logger.warning(f"Error sugiriendo políticas: {e}")
            return {"error": str(e)}
    
    def calcular_metricas_avanzadas(self, mercado) -> Dict:
        """Calcula métricas económicas avanzadas"""
        try:
            metricas = {}
            
            # Velocidad del dinero (aproximación)
            if hasattr(mercado, 'pib_total') and hasattr(mercado, 'masa_monetaria'):
                metricas['velocidad_dinero'] = mercado.pib_total / max(mercado.masa_monetaria, 1)
            
            # Ratio deuda/PIB (aproximación)
            if hasattr(mercado, 'deuda_total') and hasattr(mercado, 'pib_total'):
                metricas['ratio_deuda_pib'] = mercado.deuda_total / max(mercado.pib_total, 1)
            
            # Concentración de mercado (Índice Herfindahl)
            if hasattr(mercado, 'empresas'):
                participaciones = []
                ingresos_total = sum(getattr(emp, 'ingresos_totales', 0) for emp in mercado.empresas)
                if ingresos_total > 0:
                    for empresa in mercado.empresas:
                        participacion = getattr(empresa, 'ingresos_totales', 0) / ingresos_total
                        participaciones.append(participacion)
                    metricas['indice_herfindahl'] = sum(p**2 for p in participaciones)
                else:
                    metricas['indice_herfindahl'] = 0
            
            # Índice de desigualdad (Gini aproximado)
            if hasattr(mercado, 'consumidores'):
                ingresos = [getattr(cons, 'dinero', 0) for cons in mercado.consumidores]
                if ingresos:
                    metricas['indice_gini'] = self._calcular_gini(ingresos)
            
            return metricas
            
        except Exception as e:
            self.logger.warning(f"Error calculando métricas avanzadas: {e}")
            return {}
    
    def _calcular_gini(self, ingresos: List[float]) -> float:
        """Calcula el coeficiente de Gini para medir desigualdad"""
        if not ingresos or len(ingresos) < 2:
            return 0.0
        
        # Ordenar ingresos
        ingresos_ordenados = sorted(ingresos)
        n = len(ingresos_ordenados)
        
        # Calcular Gini
        suma_diferencias = 0
        for i in range(n):
            for j in range(n):
                suma_diferencias += abs(ingresos_ordenados[i] - ingresos_ordenados[j])
        
        media_ingresos = sum(ingresos_ordenados) / n
        if media_ingresos == 0:
            return 0.0
        
        return suma_diferencias / (2 * n * n * media_ingresos)
    
    def generar_reporte_avanzado(self, mercado, ciclo: int) -> str:
        """Genera un reporte avanzado con análisis económico profundo"""
        # Análisis básico
        reporte_basico = self.generar_reporte_validacion(mercado, ciclo)
        
        # Análisis avanzado
        regimen = self.analizar_regimen_economico(mercado)
        politicas = self.sugerir_politicas_economicas(mercado)
        metricas = self.calcular_metricas_avanzadas(mercado)
        
        reporte_avanzado = []
        reporte_avanzado.append("📊 ANÁLISIS ECONÓMICO AVANZADO")
        reporte_avanzado.append("="*60)
        reporte_avanzado.append(f"📈 Régimen Económico: {regimen}")
        
        if 'politicas_sugeridas' in politicas:
            pol = politicas['politicas_sugeridas']
            reporte_avanzado.append(f"💰 Política Monetaria Sugerida: {pol.get('politica_monetaria', 'N/A')}")
            reporte_avanzado.append(f"🏛️  Política Fiscal Sugerida: {pol.get('politica_fiscal', 'N/A')}")
            
            if 'prioridades' in pol:
                reporte_avanzado.append(f"🎯 Prioridades: {', '.join(pol['prioridades'])}")
        
        if metricas:
            reporte_avanzado.append("\n📊 MÉTRICAS AVANZADAS:")
            for metrica, valor in metricas.items():
                reporte_avanzado.append(f"  • {metrica.replace('_', ' ').title()}: {valor:.3f}")
        
        reporte_avanzado.append("="*60)
        
        return reporte_basico + "\n\n" + "\n".join(reporte_avanzado)
        if not self.alertas_historicas:
            return []
            
        ciclo_limite = max(alerta.ciclo for alerta in self.alertas_historicas) - ultimos_ciclos
        return [alerta for alerta in self.alertas_historicas if alerta.ciclo > ciclo_limite]
