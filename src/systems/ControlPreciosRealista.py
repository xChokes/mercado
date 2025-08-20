"""
Control de Precios con Inercia Realista
Sistema que evita cambios de precios abruptos y hiperinflación
"""

import random
import math
from collections import defaultdict

class ControladorPreciosRealista:
    """Controla los precios para mantener realismo económico"""
    
    def __init__(self, mercado):
        self.mercado = mercado
        self.inercia_precios = 0.98  # 98% de inercia (MÁS estable)
        self.cambio_maximo_ciclo = 0.008  # Máximo 0.8% por ciclo (MÁS restrictivo)
        self.factor_monetario = 1.0  # Factor del banco central
        
        # Cache de precios para cálculo de inercia
        self.precios_anteriores = {}
        self.presion_inflacionaria = 0.0
        
        # CONTROLES ANTI-HIPERINFLACIÓN MÁS ESTRICTOS
        self.inflacion_acumulada_periodo = 0.0
        self.ciclos_inflacion_alta = 0
        self.limite_inflacion_emergencia = 0.04  # 4% máximo por ciclo (MÁS estricto)
        self.activar_controles_emergencia = False
        
        # NUEVO: Control de precios extremos
        self.precio_maximo_permitido = 10000.0  # Límite absoluto de precios
        self.precio_minimo_permitido = 0.1      # Límite mínimo
        
    def aplicar_control_precios(self, empresa, bien_nombre, precio_propuesto):
        """Aplica control de precios con inercia realista y controles anti-hiperinflación"""
        
        # Obtener precio anterior
        precio_anterior = empresa.precios.get(bien_nombre, precio_propuesto)
        if bien_nombre not in self.precios_anteriores:
            self.precios_anteriores[bien_nombre] = precio_anterior
        
        # CONTROL DE EMERGENCIA: Si hay hiperinflación, aplicar controles extremos
        if self._detectar_hiperinflacion():
            self.activar_controles_emergencia = True
            return self._aplicar_controles_emergencia(precio_anterior, precio_propuesto)
        
        # Calcular precio objetivo con factores económicos
        precio_objetivo = self._calcular_precio_objetivo(
            empresa, bien_nombre, precio_propuesto, precio_anterior
        )
        
        # Aplicar inercia (los precios no cambian instantáneamente)
        precio_con_inercia = (
            precio_anterior * self.inercia_precios + 
            precio_objetivo * (1 - self.inercia_precios)
        )
        
        # Aplicar límites de variación más estrictos
        precio_final = self._aplicar_limites_variacion_mejorados(
            precio_con_inercia, precio_anterior
        )
        
        # Aplicar factor monetario del banco central (con límites)
        precio_final *= max(0.95, min(1.05, self.factor_monetario))  # Limitar impacto
        
        # NUEVO: Control absoluto de precios extremos
        precio_final = self._aplicar_limites_absolutos(precio_final)
        
        # Actualizar caché
        self.precios_anteriores[bien_nombre] = precio_final
        
        return precio_final
    
    def _calcular_precio_objetivo(self, empresa, bien_nombre, precio_propuesto, precio_anterior):
        """Calcula precio objetivo considerando factores macroeconómicos"""
        
        # Base: precio propuesto por el sistema de precios dinámicos
        precio_base = precio_propuesto
        
        # Factor 1: Expectativas de inflación
        factor_expectativas = self._calcular_factor_expectativas()
        
        # Factor 2: Presión de costos (salarios, energía)
        factor_costos = self._calcular_factor_costos(empresa)
        
        # Factor 3: Competencia en el mercado
        factor_competencia = self._calcular_factor_competencia(bien_nombre)
        
        # Factor 4: Ciclo económico
        factor_ciclo = self._calcular_factor_ciclo_economico()
        
        # Combinar factores
        precio_objetivo = precio_base * factor_expectativas * factor_costos * factor_competencia * factor_ciclo
        
        return precio_objetivo
    
    def _calcular_factor_expectativas(self):
        """Factor basado en expectativas de inflación"""
        inflacion_esperada = self._estimar_inflacion_esperada()
        
        # Las empresas ajustan precios por inflación esperada
        return 1 + (inflacion_esperada * 0.8)  # 80% de pass-through
    
    def _calcular_factor_costos(self, empresa):
        """Factor basado en presión de costos"""
        # Presión salarial
        if hasattr(empresa, 'empleados') and empresa.empleados:
            crecimiento_salarios = self._estimar_crecimiento_salarios()
            factor_salarios = 1 + (crecimiento_salarios * 0.6)  # 60% de traspaso
        else:
            factor_salarios = 1.0
        
        # Presión de materias primas (simplificado)
        factor_materias_primas = 1 + random.uniform(-0.02, 0.02)
        
        return factor_salarios * factor_materias_primas
    
    def _calcular_factor_competencia(self, bien_nombre):
        """Factor basado en nivel de competencia"""
        empresas_con_bien = len([
            e for e in self.mercado.getEmpresas() 
            if hasattr(e, 'bienes') and bien_nombre in e.bienes
        ])
        
        if empresas_con_bien <= 1:
            return 1.05  # Monopolio: +5% poder de pricing
        elif empresas_con_bien <= 3:
            return 1.02  # Oligopolio: +2% poder de pricing
        else:
            return 0.98  # Competencia: -2% presión de precios
    
    def _calcular_factor_ciclo_economico(self):
        """Factor basado en fase del ciclo económico"""
        if hasattr(self.mercado, 'fase_ciclo_economico'):
            if self.mercado.fase_ciclo_economico == 'expansion':
                return 1.01  # Presión al alza en expansión
            elif self.mercado.fase_ciclo_economico == 'recesion':
                return 0.99  # Presión a la baja en recesión
            elif self.mercado.fase_ciclo_economico == 'depresion':
                return 0.97  # Fuerte presión a la baja
        
        return 1.0  # Neutral
    
    def _detectar_hiperinflacion(self):
        """Detecta condiciones de hiperinflación para activar controles de emergencia"""
        if len(self.mercado.inflacion_historica) < 2:
            return False
        
        # CONTROLES MÁS ESTRICTOS
        # Hiperinflación: inflación > 4% en un ciclo o > 10% acumulada en 3 ciclos
        inflacion_actual = self.mercado.inflacion_historica[-1]
        
        # Verificar también precios extremos
        precio_promedio_actual = self._calcular_precio_promedio_actual()
        if precio_promedio_actual > 1000:  # Precios muy altos
            return True
        
        if len(self.mercado.inflacion_historica) >= 3:
            inflaciones_recientes = self.mercado.inflacion_historica[-3:]
            inflacion_acumulada = sum(inflaciones_recientes)
            return inflacion_actual > self.limite_inflacion_emergencia or inflacion_acumulada > 0.10
        
        return inflacion_actual > self.limite_inflacion_emergencia
    
    def _aplicar_controles_emergencia(self, precio_anterior, precio_propuesto):
        """Aplica controles de emergencia anti-hiperinflación"""
        # En emergencia: congelar precios o permitir solo deflación
        if precio_propuesto > precio_anterior:
            # No permitir subidas de precios
            return precio_anterior * 0.999  # Pequeña deflación forzada
        else:
            # Permitir deflación limitada
            return max(precio_propuesto, precio_anterior * 0.95)  # Máximo 5% deflación
    
    def _aplicar_limites_variacion_mejorados(self, precio_nuevo, precio_anterior):
        """Aplica límites más estrictos de variación de precios"""
        if precio_anterior <= 0:
            return precio_nuevo
        
        ratio_cambio = precio_nuevo / precio_anterior
        
        # Límites MUCHO más estrictos para simulaciones largas
        cambio_maximo = self.cambio_maximo_ciclo  # 0.8% base
        
        # Si hay inflación alta, reducir límites drásticamente
        if len(self.mercado.inflacion_historica) > 0:
            inflacion_actual = self.mercado.inflacion_historica[-1]
            if inflacion_actual > 0.03:  # Si inflación > 3%
                cambio_maximo *= 0.25  # Reducir límites al 25%
            elif inflacion_actual > 0.02:  # Si inflación > 2%
                cambio_maximo *= 0.5   # Reducir límites al 50%
        
        limite_superior = 1 + cambio_maximo
        limite_inferior = 1 - cambio_maximo
        
        if ratio_cambio > limite_superior:
            return precio_anterior * limite_superior
        elif ratio_cambio < limite_inferior:
            return precio_anterior * limite_inferior
        else:
            return precio_nuevo
    
    def _aplicar_limites_variacion(self, precio_nuevo, precio_anterior):
        """Aplica límites realistas de variación de precios"""
        if precio_anterior <= 0:
            return precio_nuevo
        
        ratio_cambio = precio_nuevo / precio_anterior
        
        # Límites realistas: máximo 3% por ciclo (36% anual)
        limite_superior = 1 + self.cambio_maximo_ciclo
        limite_inferior = 1 - self.cambio_maximo_ciclo
        
        if ratio_cambio > limite_superior:
            return precio_anterior * limite_superior
        elif ratio_cambio < limite_inferior:
            return precio_anterior * limite_inferior
        else:
            return precio_nuevo
    
    def _estimar_inflacion_esperada(self):
        """Estima expectativas de inflación basada en historial"""
        if len(self.mercado.inflacion_historica) < 3:
            return 0.02  # 2% por defecto
        
        # Promedio de últimas 3 observaciones con peso decreciente
        inflaciones_recientes = self.mercado.inflacion_historica[-3:]
        pesos = [0.5, 0.3, 0.2]  # Más peso a observaciones recientes
        
        inflacion_esperada = sum(
            inf * peso for inf, peso in zip(inflaciones_recientes, pesos)
        )
        
        # Suavizar expectativas (no cambian abruptamente)
        return max(-0.02, min(0.10, inflacion_esperada))  # Entre -2% y 10%
    
    def _estimar_crecimiento_salarios(self):
        """Estima crecimiento de salarios"""
        # En economías reales, salarios siguen inflación con lag
        inflacion_esperada = self._estimar_inflacion_esperada()
        productividad = 0.02  # Asumimos 2% de crecimiento de productividad
        
        return inflacion_esperada + productividad * 0.5
    
    def aplicar_factor_monetario(self, factor):
        """Aplica factor monetario del banco central con mayor efectividad"""
        # Transmisión más agresiva de política monetaria
        cambio = (factor - 1.0) * 0.7  # 70% de transmisión inmediata (más que antes)
        self.factor_monetario = 1.0 + cambio
        
        # Límites más amplios del factor monetario para mayor efectividad
        self.factor_monetario = max(0.7, min(1.3, self.factor_monetario))
        
        # Si hay hiperinflación, hacer la política contractiva aún más agresiva
        if hasattr(self.mercado, 'inflacion_historica') and len(self.mercado.inflacion_historica) > 0:
            inflacion_actual = self.mercado.inflacion_historica[-1]
            if inflacion_actual > 0.10:  # Si inflación > 10%
                # Política contractiva extrema
                if factor < 1.0:
                    self.factor_monetario = max(0.5, self.factor_monetario * 0.8)
    
    def calcular_inflacion_core(self):
        """Calcula inflación subyacente (sin alimentos y energía)"""
        bienes_core = [
            bien for bien in self.mercado.bienes.keys()
            if not any(keyword in bien.lower() 
                      for keyword in ['energia', 'combustible', 'agua', 'gas'])
        ]
        
        if not bienes_core or len(self.mercado.precios_historicos) < 2:
            return 0.0
        
        cambios_precios = []
        for bien in bienes_core:
            if bien in self.mercado.precios_historicos:
                historial = self.mercado.precios_historicos[bien]
                if len(historial) >= 2:
                    cambio = (historial[-1] - historial[-2]) / historial[-2]
                    cambios_precios.append(cambio)
        
        if cambios_precios:
            return sum(cambios_precios) / len(cambios_precios)
        
        return 0.0
    
    def obtener_estadisticas_precios(self):
        """Obtiene estadísticas del control de precios"""
        return {
            'inercia_precios': self.inercia_precios,
            'cambio_maximo_ciclo': self.cambio_maximo_ciclo,
            'factor_monetario': self.factor_monetario,
            'inflacion_core': self.calcular_inflacion_core(),
            'expectativas_inflacion': self._estimar_inflacion_esperada()
        }
    
    def aplicar_control_masivo_precios(self, ciclo):
        """Aplica control de precios a todas las empresas del mercado"""
        cambios_aplicados = 0
        
        # Aplicar control a todas las empresas
        for empresa in self.mercado.getEmpresas():
            if hasattr(empresa, 'precios') and empresa.precios:
                for bien_nombre, precio_actual in empresa.precios.items():
                    # Aplicar control de precios
                    precio_controlado = self.aplicar_control_precios(empresa, bien_nombre, precio_actual)
                    
                    # Si hay cambio significativo, aplicar
                    if abs(precio_controlado - precio_actual) / precio_actual > 0.001:  # >0.1% de cambio
                        empresa.precios[bien_nombre] = precio_controlado
                        cambios_aplicados += 1
        
        return cambios_aplicados
    
    def obtener_estadisticas_control(self):
        """Obtiene estadísticas específicas del control de precios"""
        total_empresas = len(self.mercado.getEmpresas())
        total_precios = 0
        precio_promedio = 0
        
        for empresa in self.mercado.getEmpresas():
            if hasattr(empresa, 'precios') and empresa.precios:
                total_precios += len(empresa.precios)
                precio_promedio += sum(empresa.precios.values())
        
        if total_precios > 0:
            precio_promedio /= total_precios
        
        return {
            'cambios_aplicados': getattr(self, '_cambios_aplicados_total', 0),
            'empresas_monitoreadas': total_empresas,
            'precios_controlados': total_precios,
            'precio_promedio_actual': precio_promedio,
            'factor_monetario_actual': self.factor_monetario
        }
    
    def monitorear_y_responder_hiperinflacion(self, ciclo):
        """Monitorea y responde automáticamente a condiciones de hiperinflación"""
        if len(self.mercado.inflacion_historica) < 1:
            return False
        
        inflacion_actual = self.mercado.inflacion_historica[-1]
        
        # RESPUESTA AUTOMÁTICA A HIPERINFLACIÓN
        if inflacion_actual > 0.10:  # Inflación > 10%
            print(f"⚠️  ALERTA HIPERINFLACIÓN DETECTADA: {inflacion_actual:.1%}")
            
            # Activar controles de emergencia
            self.activar_controles_emergencia = True
            self.inercia_precios = 0.98  # Aumentar inercia al 98%
            self.cambio_maximo_ciclo = 0.005  # Reducir a 0.5% máximo por ciclo
            
            # Aplicar deflación forzada en mercado
            self._aplicar_deflacion_emergencia()
            
            return True
        
        elif inflacion_actual > 0.05:  # Inflación > 5%
            print(f"⚠️  ALERTA INFLACIÓN ALTA: {inflacion_actual:.1%}")
            
            # Ajustes moderados
            self.inercia_precios = min(0.97, self.inercia_precios + 0.02)
            self.cambio_maximo_ciclo = max(0.01, self.cambio_maximo_ciclo * 0.8)
            
            return True
        
        elif self.activar_controles_emergencia and inflacion_actual < 0.03:
            # Desactivar controles de emergencia si inflación baja
            print(f"✅ INFLACIÓN CONTROLADA: {inflacion_actual:.1%} - Desactivando emergencia")
            self.activar_controles_emergencia = False
            self.inercia_precios = 0.95  # Volver a normal
            self.cambio_maximo_ciclo = 0.015  # Volver a normal
        
        return False
    
    def activar_deflacion_emergencia(self, intensidad=0.5):
        """NUEVO: Método para deflación de emergencia llamado por el Banco Central"""
        factor_deflacion = 1.0 - (0.02 * intensidad)  # Base 2% * intensidad
        
        bienes_deflacionados = 0
        for empresa in self.mercado.getEmpresas():
            if hasattr(empresa, 'precios') and empresa.precios:
                for bien_nombre in empresa.precios.keys():
                    precio_actual = empresa.precios[bien_nombre]
                    empresa.precios[bien_nombre] = precio_actual * factor_deflacion
                    bienes_deflacionados += 1
        
        self.activar_controles_emergencia = True  # Activar controles
        print(f"🏛️ BANCO CENTRAL: Deflación de emergencia aplicada a {bienes_deflacionados} bienes ({(1-factor_deflacion)*100:.1f}%)")
    
    def _aplicar_deflacion_emergencia(self):
        """Aplica deflación forzada de emergencia en todos los precios"""
        factor_deflacion = 0.98  # 2% de deflación forzada
        
        for empresa in self.mercado.getEmpresas():
            if hasattr(empresa, 'precios') and empresa.precios:
                for bien_nombre, precio_actual in empresa.precios.items():
                    empresa.precios[bien_nombre] = precio_actual * factor_deflacion
    
    def _aplicar_limites_absolutos(self, precio):
        """Aplica límites absolutos para evitar precios extremos"""
        # Limitar precio máximo
        if precio > self.precio_maximo_permitido:
            return self.precio_maximo_permitido
        
        # Limitar precio mínimo
        if precio < self.precio_minimo_permitido:
            return self.precio_minimo_permitido
        
        return precio
    
    def _calcular_precio_promedio_actual(self):
        """Calcula el precio promedio actual de todos los bienes"""
        total_precios = 0
        count_precios = 0
        
        for empresa in self.mercado.getEmpresas():
            if hasattr(empresa, 'precios') and empresa.precios:
                for precio in empresa.precios.values():
                    total_precios += precio
                    count_precios += 1
        
        return total_precios / max(1, count_precios)
        
        for empresa in self.mercado.getEmpresas():
            if hasattr(empresa, 'precios') and empresa.precios:
                for bien_nombre in empresa.precios.keys():
                    precio_actual = empresa.precios[bien_nombre]
                    empresa.precios[bien_nombre] = precio_actual * factor_deflacion
        
        print(f"🚨 DEFLACIÓN DE EMERGENCIA APLICADA: {(1-factor_deflacion)*100:.1f}%")
