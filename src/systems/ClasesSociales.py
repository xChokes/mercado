"""
Sistema de Clases Sociales Dinámicas para Simulación Económica Hiperrealista
Implementa estratificación social, movilidad social y desigualdad endógena
"""

import random
import math
from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional
from ..utils.SimuladorLogger import get_simulador_logger


class ClaseSocial(Enum):
    BAJA = "baja"
    MEDIA_BAJA = "media_baja"
    MEDIA = "media"
    MEDIA_ALTA = "media_alta"
    ALTA = "alta"


class TipoMovilidad(Enum):
    ASCENDENTE = "ascendente"
    DESCENDENTE = "descendente"
    ESTABLE = "estable"


@dataclass
class PerfilClaseSocial:
    """Perfil de comportamiento por clase social"""
    clase: ClaseSocial
    percentil_riqueza: tuple  # (min, max) percentil
    propension_consumo: float
    propension_ahorro: float
    propension_inversion: float
    acceso_credito: float     # Facilidad de obtener crédito
    educacion_promedio: float # Nivel educativo (0-1)
    capital_social: float     # Redes y conexiones (0-1)
    
    # Patrones de consumo específicos
    bienes_preferidos: List[str]
    sensibilidad_precio: float
    lealtad_marca: float


class SistemaClasesSociales:
    """Sistema que gestiona la estratificación y movilidad social"""
    
    def __init__(self, mercado):
        self.mercado = mercado
        self.logger = get_simulador_logger()
        
        # Perfiles de clase social
        self.perfiles_clase = self._crear_perfiles_clase()
        
        # Distribución de clases (basada en datos reales)
        self.distribucion_clases = {
            ClaseSocial.BAJA: 0.25,      # 25%
            ClaseSocial.MEDIA_BAJA: 0.30, # 30%
            ClaseSocial.MEDIA: 0.25,      # 25%
            ClaseSocial.MEDIA_ALTA: 0.15, # 15%
            ClaseSocial.ALTA: 0.05        # 5%
        }
        
        # Factores de movilidad social
        self.factores_movilidad = {
            'educacion': 0.30,      # 30% del peso
            'empleo': 0.25,         # 25% del peso
            'inversion': 0.20,      # 20% del peso
            'suerte': 0.15,         # 15% del peso
            'herencia': 0.10        # 10% del peso
        }
        
        # Métricas de desigualdad
        self.coeficiente_gini = 0.0
        self.ratio_90_10 = 0.0  # Ratio entre percentil 90 y 10
        self.movilidad_intergeneracional = 0.3  # Qué tan móvil es la sociedad
        
        # Historial de movilidad
        self.historial_movilidad = []
        self.matriz_transicion = self._crear_matriz_transicion()
        
        self.logger.log_configuracion("Sistema de Clases Sociales inicializado")
        
    def _crear_perfiles_clase(self):
        """Crea perfiles de comportamiento por clase social"""
        perfiles = {}
        
        # CLASE BAJA
        perfiles[ClaseSocial.BAJA] = PerfilClaseSocial(
            clase=ClaseSocial.BAJA,
            percentil_riqueza=(0, 25),
            propension_consumo=0.95,    # Gastan casi todo
            propension_ahorro=0.03,     # Muy poco ahorro
            propension_inversion=0.02,  # Casi nula inversión
            acceso_credito=0.20,        # Difícil acceso al crédito
            educacion_promedio=0.30,    # Educación básica
            capital_social=0.25,        # Pocas conexiones
            bienes_preferidos=['alimentos_basicos', 'servicios', 'transporte'],
            sensibilidad_precio=0.90,   # Muy sensibles al precio
            lealtad_marca=0.20          # Baja lealtad (compran lo más barato)
        )
        
        # CLASE MEDIA BAJA
        perfiles[ClaseSocial.MEDIA_BAJA] = PerfilClaseSocial(
            clase=ClaseSocial.MEDIA_BAJA,
            percentil_riqueza=(25, 45),
            propension_consumo=0.85,
            propension_ahorro=0.10,
            propension_inversion=0.05,
            acceso_credito=0.40,
            educacion_promedio=0.50,
            capital_social=0.40,
            bienes_preferidos=['alimentos_basicos', 'alimentos_lujo', 'ropa', 'educacion'],
            sensibilidad_precio=0.75,
            lealtad_marca=0.35
        )
        
        # CLASE MEDIA
        perfiles[ClaseSocial.MEDIA] = PerfilClaseSocial(
            clase=ClaseSocial.MEDIA,
            percentil_riqueza=(45, 70),
            propension_consumo=0.75,
            propension_ahorro=0.15,
            propension_inversion=0.10,
            acceso_credito=0.65,
            educacion_promedio=0.70,
            capital_social=0.60,
            bienes_preferidos=['bienes_duraderos', 'tecnologia', 'vivienda', 'entretenimiento'],
            sensibilidad_precio=0.55,
            lealtad_marca=0.50
        )
        
        # CLASE MEDIA ALTA
        perfiles[ClaseSocial.MEDIA_ALTA] = PerfilClaseSocial(
            clase=ClaseSocial.MEDIA_ALTA,
            percentil_riqueza=(70, 90),
            propension_consumo=0.65,
            propension_ahorro=0.20,
            propension_inversion=0.15,
            acceso_credito=0.80,
            educacion_promedio=0.85,
            capital_social=0.75,
            bienes_preferidos=['tecnologia', 'servicios_lujo', 'vivienda', 'inversion'],
            sensibilidad_precio=0.35,
            lealtad_marca=0.65
        )
        
        # CLASE ALTA
        perfiles[ClaseSocial.ALTA] = PerfilClaseSocial(
            clase=ClaseSocial.ALTA,
            percentil_riqueza=(90, 100),
            propension_consumo=0.45,
            propension_ahorro=0.25,
            propension_inversion=0.30,
            acceso_credito=0.95,
            educacion_promedio=0.95,
            capital_social=0.90,
            bienes_preferidos=['servicios_lujo', 'arte', 'inversion', 'tecnologia'],
            sensibilidad_precio=0.15,
            lealtad_marca=0.80
        )
        
        return perfiles
    
    def _crear_matriz_transicion(self):
        """Crea matriz de transición entre clases sociales"""
        # Matriz simplificada - probabilidades de moverse entre clases en un período
        return {
            ClaseSocial.BAJA: {
                ClaseSocial.BAJA: 0.80,
                ClaseSocial.MEDIA_BAJA: 0.15,
                ClaseSocial.MEDIA: 0.04,
                ClaseSocial.MEDIA_ALTA: 0.01,
                ClaseSocial.ALTA: 0.00
            },
            ClaseSocial.MEDIA_BAJA: {
                ClaseSocial.BAJA: 0.15,
                ClaseSocial.MEDIA_BAJA: 0.60,
                ClaseSocial.MEDIA: 0.20,
                ClaseSocial.MEDIA_ALTA: 0.04,
                ClaseSocial.ALTA: 0.01
            },
            ClaseSocial.MEDIA: {
                ClaseSocial.BAJA: 0.05,
                ClaseSocial.MEDIA_BAJA: 0.20,
                ClaseSocial.MEDIA: 0.50,
                ClaseSocial.MEDIA_ALTA: 0.20,
                ClaseSocial.ALTA: 0.05
            },
            ClaseSocial.MEDIA_ALTA: {
                ClaseSocial.BAJA: 0.01,
                ClaseSocial.MEDIA_BAJA: 0.04,
                ClaseSocial.MEDIA: 0.20,
                ClaseSocial.MEDIA_ALTA: 0.60,
                ClaseSocial.ALTA: 0.15
            },
            ClaseSocial.ALTA: {
                ClaseSocial.BAJA: 0.00,
                ClaseSocial.MEDIA_BAJA: 0.01,
                ClaseSocial.MEDIA: 0.04,
                ClaseSocial.MEDIA_ALTA: 0.15,
                ClaseSocial.ALTA: 0.80
            }
        }
    
    def asignar_clases_sociales(self):
        """Asigna clase social inicial a todos los consumidores"""
        consumidores = self.mercado.getConsumidores()
        
        # Ordenar por riqueza inicial
        consumidores_ordenados = sorted(consumidores, key=lambda c: getattr(c, 'dinero', 0))
        
        clases_asignadas = 0
        for clase, porcentaje in self.distribucion_clases.items():
            num_clase = int(len(consumidores) * porcentaje)
            
            for i in range(clases_asignadas, min(clases_asignadas + num_clase, len(consumidores_ordenados))):
                consumidor = consumidores_ordenados[i]
                self._asignar_clase_social(consumidor, clase)
            
            clases_asignadas += num_clase
        
        # Asignar clase media a cualquier consumidor sin clase
        for consumidor in consumidores:
            if not hasattr(consumidor, 'clase_social'):
                self._asignar_clase_social(consumidor, ClaseSocial.MEDIA)
        
        self.logger.log_configuracion(f"   Clases sociales asignadas a {len(consumidores)} consumidores")
        self._log_distribucion_clases()
    
    def _asignar_clase_social(self, consumidor, clase: ClaseSocial):
        """Asigna clase social específica a un consumidor"""
        consumidor.clase_social = clase
        perfil = self.perfiles_clase[clase]
        
        # Ajustar comportamiento económico según la clase
        consumidor.propension_consumo_base = perfil.propension_consumo
        consumidor.propension_consumo = perfil.propension_consumo
        consumidor.propension_ahorro = perfil.propension_ahorro
        
        # Crear atributos específicos de clase
        consumidor.acceso_credito = perfil.acceso_credito
        consumidor.educacion = perfil.educacion_promedio * random.uniform(0.8, 1.2)
        consumidor.capital_social = perfil.capital_social * random.uniform(0.7, 1.3)
        consumidor.sensibilidad_precio = perfil.sensibilidad_precio
        consumidor.bienes_preferidos = perfil.bienes_preferidos.copy()
        
        # Historial de movilidad
        consumidor.historial_clases = [clase]
        consumidor.clase_social_anterior = None
    
    def ejecutar_ciclo_movilidad_social(self, ciclo):
        """Ejecuta ciclo de movilidad social"""
        # Solo evaluar movilidad cada 12 ciclos (anual)
        if ciclo % 12 != 0:
            return
            
        movimientos = self._evaluar_movilidad_social()
        self._aplicar_cambios_clase(movimientos)
        self._actualizar_metricas_desigualdad()
        
        return self._generar_reporte_movilidad(ciclo, movimientos)
    
    def _evaluar_movilidad_social(self):
        """Evalúa qué consumidores cambian de clase social"""
        movimientos = []
        
        for consumidor in self.mercado.getConsumidores():
            if not hasattr(consumidor, 'clase_social'):
                continue
                
            # Calcular score de movilidad
            score_movilidad = self._calcular_score_movilidad(consumidor)
            
            # Determinar nueva clase potencial
            clase_actual = consumidor.clase_social
            nueva_clase = self._determinar_nueva_clase(consumidor, score_movilidad)
            
            if nueva_clase != clase_actual:
                movimientos.append({
                    'consumidor': consumidor,
                    'clase_anterior': clase_actual,
                    'nueva_clase': nueva_clase,
                    'score': score_movilidad,
                    'tipo': TipoMovilidad.ASCENDENTE if self._es_ascendente(clase_actual, nueva_clase) else TipoMovilidad.DESCENDENTE
                })
        
        return movimientos
    
    def _calcular_score_movilidad(self, consumidor):
        """Calcula score que determina movilidad social potencial"""
        score = 0.0
        
        # Factor educación
        educacion_score = getattr(consumidor, 'educacion', 0.5)
        score += educacion_score * self.factores_movilidad['educacion']
        
        # Factor empleo/ingresos
        if hasattr(consumidor, 'empleado') and consumidor.empleado:
            ingreso_relativo = getattr(consumidor, 'ingreso_mensual', 0) / 5000  # Normalizar
            empleo_score = min(1.0, ingreso_relativo)
        else:
            empleo_score = 0.1  # Penalización por desempleo
        score += empleo_score * self.factores_movilidad['empleo']
        
        # Factor inversión/ahorro
        if hasattr(consumidor, 'dinero'):
            riqueza_relativa = consumidor.dinero / 50000  # Normalizar
            inversion_score = min(1.0, riqueza_relativa)
        else:
            inversion_score = 0.0
        score += inversion_score * self.factores_movilidad['inversion']
        
        # Factor suerte (eventos aleatorios)
        suerte_score = random.uniform(0.0, 1.0)
        score += suerte_score * self.factores_movilidad['suerte']
        
        # Factor herencia/familia (basado en clase de origen)
        if hasattr(consumidor, 'historial_clases') and consumidor.historial_clases:
            clase_origen = consumidor.historial_clases[0]
            herencia_score = self.perfiles_clase[clase_origen].capital_social
        else:
            herencia_score = 0.5
        score += herencia_score * self.factores_movilidad['herencia']
        
        return min(1.0, score)  # Normalizar a [0,1]
    
    def _determinar_nueva_clase(self, consumidor, score_movilidad):
        """Determina nueva clase social basada en score de movilidad"""
        clase_actual = consumidor.clase_social
        
        # Obtener probabilidades de transición
        prob_transicion = self.matriz_transicion[clase_actual].copy()
        
        # Ajustar probabilidades basado en score de movilidad
        if score_movilidad > 0.7:  # Score alto = más probable ascender
            self._aumentar_prob_ascenso(prob_transicion, clase_actual)
        elif score_movilidad < 0.3:  # Score bajo = más probable descender
            self._aumentar_prob_descenso(prob_transicion, clase_actual)
        
        # Seleccionar nueva clase
        rand = random.random()
        acumulado = 0.0
        
        for nueva_clase, probabilidad in prob_transicion.items():
            acumulado += probabilidad
            if rand <= acumulado:
                return nueva_clase
        
        return clase_actual  # Fallback
    
    def _aumentar_prob_ascenso(self, prob_transicion, clase_actual):
        """Aumenta probabilidades de ascenso social"""
        clases_ordenadas = list(ClaseSocial)
        idx_actual = clases_ordenadas.index(clase_actual)
        
        # Redistribuir probabilidad hacia clases superiores
        for i, clase in enumerate(clases_ordenadas):
            if i > idx_actual:  # Clases superiores
                prob_transicion[clase] *= 2.0
            elif i < idx_actual:  # Clases inferiores
                prob_transicion[clase] *= 0.5
        
        # Renormalizar
        total = sum(prob_transicion.values())
        for clase in prob_transicion:
            prob_transicion[clase] /= total
    
    def _aumentar_prob_descenso(self, prob_transicion, clase_actual):
        """Aumenta probabilidades de descenso social"""
        clases_ordenadas = list(ClaseSocial)
        idx_actual = clases_ordenadas.index(clase_actual)
        
        # Redistribuir probabilidad hacia clases inferiores
        for i, clase in enumerate(clases_ordenadas):
            if i < idx_actual:  # Clases inferiores
                prob_transicion[clase] *= 2.0
            elif i > idx_actual:  # Clases superiores
                prob_transicion[clase] *= 0.5
        
        # Renormalizar
        total = sum(prob_transicion.values())
        for clase in prob_transicion:
            prob_transicion[clase] /= total
    
    def _es_ascendente(self, clase_anterior, nueva_clase):
        """Determina si el movimiento es ascendente"""
        clases_ordenadas = list(ClaseSocial)
        return clases_ordenadas.index(nueva_clase) > clases_ordenadas.index(clase_anterior)
    
    def _aplicar_cambios_clase(self, movimientos):
        """Aplica cambios de clase social"""
        for movimiento in movimientos:
            consumidor = movimiento['consumidor']
            nueva_clase = movimiento['nueva_clase']
            
            # Actualizar clase
            consumidor.clase_social_anterior = consumidor.clase_social
            consumidor.clase_social = nueva_clase
            
            # Agregar a historial
            if hasattr(consumidor, 'historial_clases'):
                consumidor.historial_clases.append(nueva_clase)
            else:
                consumidor.historial_clases = [nueva_clase]
            
            # Aplicar nuevo perfil de clase
            self._aplicar_nuevo_perfil_clase(consumidor, nueva_clase)
        
        # Registrar en historial global
        self.historial_movilidad.extend(movimientos)
    
    def _aplicar_nuevo_perfil_clase(self, consumidor, nueva_clase):
        """Aplica nuevo perfil de comportamiento según nueva clase"""
        perfil = self.perfiles_clase[nueva_clase]
        
        # Ajustar comportamiento gradualmente (no instantáneo)
        factor_ajuste = 0.3  # 30% de ajuste por período
        
        # Propensiones de gasto
        propension_objetivo = perfil.propension_consumo
        consumidor.propension_consumo = (
            consumidor.propension_consumo * (1 - factor_ajuste) +
            propension_objetivo * factor_ajuste
        )
        
        # Acceso al crédito
        acceso_objetivo = perfil.acceso_credito
        consumidor.acceso_credito = (
            getattr(consumidor, 'acceso_credito', 0.5) * (1 - factor_ajuste) +
            acceso_objetivo * factor_ajuste
        )
        
        # Actualizar preferencias de consumo gradualmente
        consumidor.bienes_preferidos = perfil.bienes_preferidos.copy()
        consumidor.sensibilidad_precio = (
            getattr(consumidor, 'sensibilidad_precio', 0.5) * (1 - factor_ajuste) +
            perfil.sensibilidad_precio * factor_ajuste
        )
    
    def _actualizar_metricas_desigualdad(self):
        """Actualiza métricas de desigualdad social"""
        consumidores = self.mercado.getConsumidores()
        
        if not consumidores:
            return
            
        # Obtener riquezas
        riquezas = [getattr(c, 'dinero', 0) for c in consumidores]
        riquezas.sort()
        
        # Calcular Gini
        self.coeficiente_gini = self._calcular_gini(riquezas)
        
        # Calcular ratio 90/10
        n = len(riquezas)
        p90 = riquezas[int(n * 0.9)] if n > 10 else riquezas[-1]
        p10 = riquezas[int(n * 0.1)] if n > 10 else riquezas[0]
        self.ratio_90_10 = p90 / max(1, p10)
    
    def _calcular_gini(self, riquezas):
        """Calcula coeficiente de Gini"""
        if not riquezas or len(riquezas) < 2:
            return 0.0
            
        n = len(riquezas)
        total_riqueza = sum(riquezas)
        
        if total_riqueza == 0:
            return 0.0
        
        # Fórmula del Gini
        suma_diferencias = 0
        for i in range(n):
            for j in range(n):
                suma_diferencias += abs(riquezas[i] - riquezas[j])
        
        gini = suma_diferencias / (2 * n * total_riqueza)
        return min(1.0, gini)
    
    def _log_distribucion_clases(self):
        """Log de distribución actual de clases"""
        consumidores = self.mercado.getConsumidores()
        distribucion = {clase: 0 for clase in ClaseSocial}
        
        for consumidor in consumidores:
            if hasattr(consumidor, 'clase_social'):
                distribucion[consumidor.clase_social] += 1
        
        total = len(consumidores)
        for clase, cantidad in distribucion.items():
            porcentaje = (cantidad / total) * 100 if total > 0 else 0
            self.logger.log_configuracion(f"      {clase.value}: {cantidad} ({porcentaje:.1f}%)")
    
    def _generar_reporte_movilidad(self, ciclo, movimientos):
        """Genera reporte de movilidad social"""
        ascendentes = len([m for m in movimientos if m['tipo'] == TipoMovilidad.ASCENDENTE])
        descendentes = len([m for m in movimientos if m['tipo'] == TipoMovilidad.DESCENDENTE])
        
        return {
            'ciclo': ciclo,
            'movimientos_totales': len(movimientos),
            'movilidad_ascendente': ascendentes,
            'movilidad_descendente': descendentes,
            'coeficiente_gini': self.coeficiente_gini,
            'ratio_90_10': self.ratio_90_10,
            'tasa_movilidad': len(movimientos) / len(self.mercado.getConsumidores()) if self.mercado.getConsumidores() else 0
        }
    
    def obtener_estadisticas_sociales(self):
        """Obtiene estadísticas consolidadas del sistema social"""
        consumidores = self.mercado.getConsumidores()
        
        # Distribución por clase
        distribucion = {clase: 0 for clase in ClaseSocial}
        for consumidor in consumidores:
            if hasattr(consumidor, 'clase_social'):
                distribucion[consumidor.clase_social] += 1
        
        # Movilidad histórica
        movimientos_historicos = len(self.historial_movilidad)
        ascensos_historicos = len([m for m in self.historial_movilidad if m['tipo'] == TipoMovilidad.ASCENDENTE])
        
        return {
            'distribucion_clases': distribucion,
            'coeficiente_gini': self.coeficiente_gini,
            'ratio_90_10': self.ratio_90_10,
            'movilidad_intergeneracional': self.movilidad_intergeneracional,
            'movimientos_historicos_total': movimientos_historicos,
            'ascensos_historicos': ascensos_historicos,
            'tasa_ascenso_historica': ascensos_historicos / max(1, movimientos_historicos)
        }
