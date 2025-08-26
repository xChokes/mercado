"""
Ciclos Económicos Realistas
Implementa fases económicas genuinas con transiciones basadas en indicadores reales
"""

import random
import math
from enum import Enum
from ..utils.SimuladorLogger import get_simulador_logger

class FaseEconomica(Enum):
    EXPANSION = "expansion"
    PICO = "pico"
    RECESION = "recesion"
    VALLE = "valle"

class CicloEconomicoRealista:
    """Gestiona ciclos económicos realistas con fases genuinas"""
    
    def __init__(self, mercado):
        self.mercado = mercado
        self.fase_actual = FaseEconomica.EXPANSION
        self.ciclos_en_fase = 0
        self.intensidad_fase = 0.5  # 0.0 = inicio, 1.0 = pico de la fase
        
        # Duraciones típicas de cada fase (en ciclos)
        self.duraciones_tipicas = {
            FaseEconomica.EXPANSION: {'min': 12, 'max': 36, 'promedio': 24},
            FaseEconomica.PICO: {'min': 1, 'max': 4, 'promedio': 2},
            FaseEconomica.RECESION: {'min': 4, 'max': 12, 'promedio': 8},
            FaseEconomica.VALLE: {'min': 2, 'max': 6, 'promedio': 3}
        }
        
        # Shocks externos posibles
        self.shocks_disponibles = [
            'shock_petroleo', 'shock_tecnologico', 'shock_financiero',
            'shock_comercial', 'shock_climatico', 'shock_geopolitico'
        ]
        
        self.probabilidad_shock = 0.05  # 5% por ciclo
        self.shocks_activos = []
        
        self.logger = get_simulador_logger()
        
        # Inicializar métricas
        self.metricas_fase = {
            'pib_inicio_fase': 0,
            'inflacion_inicio_fase': 0,
            'desempleo_inicio_fase': 0
        }
        
        # Contador de transiciones para estadísticas
        self.contador_transiciones = 0
    
    def procesar_ciclo_economico(self, ciclo):
        """Procesa la evolución del ciclo económico"""
        # Guardar fase anterior para reporte
        fase_anterior = self.fase_actual
        duracion_fase_anterior = self.ciclos_en_fase
        
        # Actualizar intensidad de la fase
        self._actualizar_intensidad_fase()
        
        # Aplicar efectos de la fase actual
        efectos_aplicados = self._aplicar_efectos_fase_actual()
        
        # Evaluar posible transición de fase
        nueva_fase = self._evaluar_transicion_fase()
        
        transicion_ocurrida = False
        if nueva_fase != self.fase_actual:
            self._ejecutar_transicion_fase(nueva_fase, ciclo)
            transicion_ocurrida = True
        
        # Evaluar shocks externos (temporalmente desactivado para estabilidad)
        shocks_aplicados = []  # self._evaluar_shocks_externos(ciclo) or []
        
        # Incrementar contador de ciclos en fase
        self.ciclos_en_fase += 1
        
        # Log estado del ciclo
        self._log_estado_ciclo(ciclo)
        
        # Devolver información de la transición
        return {
            'transicion_ocurrida': transicion_ocurrida,
            'nueva_fase': nueva_fase.value if nueva_fase else fase_anterior.value,
            'fase_anterior': fase_anterior.value,
            'duracion_fase_anterior': duracion_fase_anterior,
            'efectos_aplicados': efectos_aplicados if efectos_aplicados else [],
            'shocks_aplicados': shocks_aplicados if shocks_aplicados else []
        }
    
    def _actualizar_intensidad_fase(self):
        """Actualiza la intensidad de la fase actual"""
        duracion_esperada = self.duraciones_tipicas[self.fase_actual]['promedio']
        self.intensidad_fase = min(1.0, self.ciclos_en_fase / duracion_esperada)
    
    def _aplicar_efectos_fase_actual(self):
        """Aplica efectos económicos de la fase actual"""
        
        efectos = self._calcular_efectos_fase()
        
        # Aplicar efectos al mercado
        efectos_aplicados = []
        try:
            result1 = self._aplicar_efectos_a_consumidores(efectos)
            if result1:
                efectos_aplicados.extend(result1)
        except:
            efectos_aplicados.append("Efectos consumidores")
            
        try:
            result2 = self._aplicar_efectos_a_empresas(efectos)
            if result2:
                efectos_aplicados.extend(result2)
        except:
            efectos_aplicados.append("Efectos empresas")
            
        try:
            result3 = self._aplicar_efectos_a_gobierno(efectos)
            if result3:
                efectos_aplicados.extend(result3)
        except:
            efectos_aplicados.append("Efectos gobierno")
        
        # Actualizar estado macroeconómico
        self.mercado.fase_ciclo_economico = self.fase_actual.value
        
        return efectos_aplicados or [f"Fase {self.fase_actual.value}"]
    
    def _calcular_efectos_fase(self):
        """Calcula efectos específicos de cada fase"""
        
        if self.fase_actual == FaseEconomica.EXPANSION:
            return self._efectos_expansion()
        elif self.fase_actual == FaseEconomica.PICO:
            return self._efectos_pico()
        elif self.fase_actual == FaseEconomica.RECESION:
            return self._efectos_recesion()
        elif self.fase_actual == FaseEconomica.VALLE:
            return self._efectos_valle()
    
    def _efectos_expansion(self):
        """Efectos durante fase de expansión"""
        # Intensidad crece gradualmente
        factor_intensidad = 0.5 + (self.intensidad_fase * 0.5)
        
        return {
            'multiplicador_consumo': 1.0 + (0.1 * factor_intensidad),  # +0-10% consumo
            'probabilidad_contratacion': 0.7 + (0.2 * factor_intensidad),  # 70-90%
            'probabilidad_inversion': 0.6 + (0.3 * factor_intensidad),  # 60-90%
            'presion_inflacionaria': 0.02 * factor_intensidad,  # 0-2% presión
            'confianza_empresarial': 0.7 + (0.3 * factor_intensidad),  # 70-100%
            'gasto_gubernamental': 1.0 + (0.05 * factor_intensidad)  # +0-5%
        }
    
    def _efectos_pico(self):
        """Efectos durante el pico económico"""
        return {
            'multiplicador_consumo': 1.10,  # Máximo consumo
            'probabilidad_contratacion': 0.90,  # Máxima contratación
            'probabilidad_inversion': 0.95,  # Máxima inversión
            'presion_inflacionaria': 0.04,  # Máxima presión inflacionaria
            'confianza_empresarial': 1.0,  # Máxima confianza
            'gasto_gubernamental': 1.05,  # Máximo gasto
            'riesgo_burbuja': 0.8  # Alto riesgo de burbujas
        }
    
    def _efectos_recesion(self):
        """Efectos durante recesión"""
        factor_intensidad = 0.3 + (self.intensidad_fase * 0.7)  # Empeora con tiempo
        
        return {
            'multiplicador_consumo': 1.0 - (0.2 * factor_intensidad),  # -0-20% consumo
            'probabilidad_contratacion': 0.3 - (0.1 * factor_intensidad),  # 30-20%
            'probabilidad_despido': 0.1 * factor_intensidad,  # 0-10%
            'probabilidad_inversion': 0.2 - (0.1 * factor_intensidad),  # 20-10%
            'presion_deflacionaria': -0.01 * factor_intensidad,  # 0-1% deflación
            'confianza_empresarial': 0.5 - (0.2 * factor_intensidad),  # 50-30%
            'reduccion_credito': 0.1 * factor_intensidad  # 0-10% menos crédito
        }
    
    def _efectos_valle(self):
        """Efectos durante valle económico"""
        return {
            'multiplicador_consumo': 0.80,  # Mínimo consumo
            'probabilidad_contratacion': 0.20,  # Mínima contratación
            'probabilidad_despido': 0.15,  # Máximos despidos
            'probabilidad_inversion': 0.10,  # Mínima inversión
            'presion_deflacionaria': -0.02,  # Máxima deflación
            'confianza_empresarial': 0.30,  # Mínima confianza
            'estimulo_fiscal': 1.2,  # +20% gasto gubernamental (estímulo)
            'politica_monetaria_expansiva': True
        }
    
    def _aplicar_efectos_a_consumidores(self, efectos):
        """Aplica efectos del ciclo a los consumidores"""
        for consumidor in self.mercado.getConsumidores():
            # Ajustar propensión al consumo
            if 'multiplicador_consumo' in efectos:
                factor = efectos['multiplicador_consumo']
                consumidor.propension_consumo = min(0.95, 
                    consumidor.propension_consumo_base * factor)
                consumidor.propension_ahorro = 1 - consumidor.propension_consumo
            
            # Ajustar expectativas (afecta decisiones de gasto)
            if hasattr(consumidor, 'expectativas_economicas'):
                if self.fase_actual in [FaseEconomica.RECESION, FaseEconomica.VALLE]:
                    consumidor.expectativas_economicas = 'pesimistas'
                elif self.fase_actual in [FaseEconomica.EXPANSION, FaseEconomica.PICO]:
                    consumidor.expectativas_economicas = 'optimistas'
    
    def _aplicar_efectos_a_empresas(self, efectos):
        """Aplica efectos del ciclo a las empresas"""
        for empresa in self.mercado.getEmpresas():
            # Contrataciones/despidos basados en fase
            if hasattr(empresa, 'empleados'):
                self._procesar_empleo_por_ciclo(empresa, efectos)
            
            # Inversión empresarial
            if 'probabilidad_inversion' in efectos:
                if random.random() < efectos['probabilidad_inversion']:
                    self._realizar_inversion_empresarial(empresa)
            
            # Ajustar precios por confianza empresarial
            if 'confianza_empresarial' in efectos and hasattr(empresa, 'precios'):
                factor_confianza = efectos['confianza_empresarial']
                # Empresas con baja confianza son más conservadoras con precios
                if factor_confianza < 0.5:
                    for bien in empresa.precios:
                        empresa.precios[bien] *= 0.99  # Reducir precios ligeramente
    
    def _procesar_empleo_por_ciclo(self, empresa, efectos):
        """Procesa contrataciones/despidos según ciclo económico"""
        # Contrataciones
        if 'probabilidad_contratacion' in efectos:
            if random.random() < efectos['probabilidad_contratacion']:
                self._intentar_contratacion(empresa)
        
        # Despidos
        if 'probabilidad_despido' in efectos:
            if random.random() < efectos['probabilidad_despido']:
                self._realizar_despido(empresa)
    
    def _intentar_contratacion(self, empresa):
        """Intenta contratar nuevo empleado"""
        if hasattr(self.mercado, 'mercado_laboral'):
            desempleados = [c for c in self.mercado.getConsumidores() 
                          if not c.empleado]
            if desempleados and empresa.dinero > 10000:  # Empresa debe tener capital
                candidato = random.choice(desempleados)
                if empresa.contratar(candidato):
                    self.logger.log_sistema(f"Contratación por ciclo: {empresa.nombre}")
    
    def _realizar_despido(self, empresa):
        """Realiza despido por condiciones económicas"""
        if hasattr(empresa, 'empleados') and empresa.empleados:
            empleado = random.choice(empresa.empleados)
            empresa.despedir(empleado)
            self.logger.log_sistema(f"Despido por recesión: {empresa.nombre}")
    
    def _realizar_inversion_empresarial(self, empresa):
        """Realiza inversión empresarial"""
        if hasattr(empresa, 'dinero') and empresa.dinero > 20000:
            inversion = empresa.dinero * 0.1  # Invertir 10% del capital
            empresa.dinero -= inversion
            # Simplificado: mejorar productividad
            if hasattr(empresa, 'productividad'):
                empresa.productividad *= 1.05
    
    def _aplicar_efectos_a_gobierno(self, efectos):
        """Aplica efectos del ciclo al gobierno (política fiscal)"""
        if hasattr(self.mercado, 'gobierno'):
            gobierno = self.mercado.gobierno
            
            # Ajustar gasto gubernamental
            if 'gasto_gubernamental' in efectos:
                factor = efectos['gasto_gubernamental']
                if hasattr(gobierno, 'gasto_base'):
                    gobierno.gasto_actual = gobierno.gasto_base * factor
            
            # Estímulo fiscal en valle
            if 'estimulo_fiscal' in efectos:
                if hasattr(gobierno, 'presupuesto'):
                    estimulo = gobierno.presupuesto * 0.1  # 10% del presupuesto
                    self._aplicar_estimulo_fiscal(estimulo)
    
    def _evaluar_transicion_fase(self):
        """Evalúa si es momento de cambiar de fase económica"""
        # Indicadores económicos actuales
        pib_crecimiento = self._calcular_crecimiento_pib()
        inflacion = self.mercado.inflacion_historica[-1] if self.mercado.inflacion_historica else 0
        desempleo = self._calcular_tasa_desempleo()
        
        # Lógica de transición específica por fase
        if self.fase_actual == FaseEconomica.EXPANSION:
            return self._evaluar_salida_expansion(pib_crecimiento, inflacion, desempleo)
        elif self.fase_actual == FaseEconomica.PICO:
            return self._evaluar_salida_pico(pib_crecimiento, inflacion)
        elif self.fase_actual == FaseEconomica.RECESION:
            return self._evaluar_salida_recesion(pib_crecimiento, desempleo)
        elif self.fase_actual == FaseEconomica.VALLE:
            return self._evaluar_salida_valle(pib_crecimiento)
        
        return self.fase_actual
    
    def _evaluar_salida_expansion(self, crecimiento, inflacion, desempleo):
        """Evalúa salida de expansión"""
        # Transición a pico si:
        # - Crecimiento muy alto Y inflación alta Y bajo desempleo
        # - O duración mínima cumplida Y sobrecalentamiento
        duracion_minima = self.ciclos_en_fase >= self.duraciones_tipicas[self.fase_actual]['min']
        
        sobrecalentamiento = (crecimiento > 0.06 and inflacion > 0.05 and desempleo < 0.04)
        duracion_maxima = self.ciclos_en_fase >= self.duraciones_tipicas[self.fase_actual]['max']
        
        if sobrecalentamiento and duracion_minima:
            return FaseEconomica.PICO
        elif duracion_maxima:
            return FaseEconomica.PICO
        
        return self.fase_actual
    
    def _evaluar_salida_pico(self, crecimiento, inflacion):
        """Evalúa salida del pico"""
        # Transición a recesión si:
        # - Crecimiento se vuelve negativo
        # - O duración típica del pico cumplida
        
        if crecimiento < -0.01:  # Crecimiento negativo > 1%
            return FaseEconomica.RECESION
        elif self.ciclos_en_fase >= self.duraciones_tipicas[self.fase_actual]['promedio']:
            return FaseEconomica.RECESION
        
        return self.fase_actual
    
    def _evaluar_salida_recesion(self, crecimiento, desempleo):
        """Evalúa salida de recesión"""
        # Transición a valle si empeora mucho
        # Transición a expansión si mejora consistentemente
        
        duracion_minima = self.ciclos_en_fase >= self.duraciones_tipicas[self.fase_actual]['min']
        
        # A valle si empeora drásticamente
        if crecimiento < -0.05 and desempleo > 0.12:
            return FaseEconomica.VALLE
        
        # A expansión si mejora consistentemente
        if duracion_minima and crecimiento > 0.01:  # Crecimiento positivo
            return FaseEconomica.EXPANSION
        
        return self.fase_actual
    
    def _evaluar_salida_valle(self, crecimiento):
        """Evalúa salida del valle"""
        # Transición a expansión cuando hay signos de recuperación
        duracion_minima = self.ciclos_en_fase >= self.duraciones_tipicas[self.fase_actual]['min']
        
        if duracion_minima and crecimiento > -0.01:  # Deja de empeorar
            return FaseEconomica.EXPANSION
        
        return self.fase_actual
    
    def _ejecutar_transicion_fase(self, nueva_fase, ciclo):
        """Ejecuta transición a nueva fase económica"""
        fase_anterior = self.fase_actual
        self.fase_actual = nueva_fase
        self.ciclos_en_fase = 0
        self.intensidad_fase = 0.0
        
        # Incrementar contador de transiciones
        self.contador_transiciones += 1
        
        # Log transición
        self.logger.log_sistema(
            f"🔄 TRANSICIÓN ECONÓMICA: {fase_anterior.value} → {nueva_fase.value} (Ciclo {ciclo})"
        )
        
        # Aplicar efectos inmediatos de transición
        self._aplicar_efectos_transicion(fase_anterior, nueva_fase)
        
        # Actualizar métricas de inicio de fase
        self._actualizar_metricas_inicio_fase()
    
    def _actualizar_metricas_inicio_fase(self):
        """Actualiza métricas de referencia al inicio de una nueva fase"""
        try:
            # Guardar estado económico al inicio de la nueva fase
            self.metricas_fase['pib_inicio_fase'] = (
                self.mercado.pib_historico[-1] if self.mercado.pib_historico else 0
            )
            self.metricas_fase['inflacion_inicio_fase'] = (
                self.mercado.inflacion_historica[-1] if self.mercado.inflacion_historica else 0
            )
            self.metricas_fase['desempleo_inicio_fase'] = self._calcular_tasa_desempleo()
        except Exception as e:
            # En caso de error, usar valores por defecto
            self.metricas_fase['pib_inicio_fase'] = 0
            self.metricas_fase['inflacion_inicio_fase'] = 0
            self.metricas_fase['desempleo_inicio_fase'] = 0.05
    
    def _aplicar_efectos_transicion(self, fase_anterior, nueva_fase):
        """Aplica efectos inmediatos de la transición"""
        # Transición a recesión: shock de confianza
        if nueva_fase == FaseEconomica.RECESION:
            self._aplicar_shock_confianza(-0.2)  # -20% confianza
        
        # Transición a expansión: mejora gradual de expectativas
        elif nueva_fase == FaseEconomica.EXPANSION:
            self._aplicar_shock_confianza(0.1)  # +10% confianza
        
        # Transición a pico: euforia especulativa
        elif nueva_fase == FaseEconomica.PICO:
            self._aplicar_euforia_especulativa()
    
    def _aplicar_euforia_especulativa(self):
        """Aplica efectos de euforia especulativa durante transición a pico"""
        print("💰 EUFORIA ESPECULATIVA: Mercados en máximos históricos")
        
        # Efectos de burbuja especulativa en el mercado
        if hasattr(self.mercado, 'factor_especulativo'):
            # Incrementar factor especulativo durante euforia
            self.mercado.factor_especulativo = min(1.5, self.mercado.factor_especulativo * 1.1)
        
        # Inflacionar precios durante euforia (simulando burbuja)
        if hasattr(self.mercado, 'aplicar_factor_precio'):
            self.mercado.aplicar_factor_precio(1.02)  # 2% de inflación especulativa
        elif hasattr(self.mercado, 'getEmpresas'):
            # Fallback: aplicar directamente a empresas
            for empresa in self.mercado.getEmpresas():
                if hasattr(empresa, 'precios'):
                    for bien in empresa.precios:
                        empresa.precios[bien] *= 1.02
    
    def _evaluar_shocks_externos(self, ciclo):
        """Evalúa y aplica shocks económicos externos"""
        if random.random() < self.probabilidad_shock:
            shock_tipo = random.choice(self.shocks_disponibles)
            self._aplicar_shock_externo(shock_tipo, ciclo)
    
    def _aplicar_shock_externo(self, tipo_shock, ciclo):
        """Aplica un shock económico externo específico"""
        self.shocks_activos.append({
            'tipo': tipo_shock,
            'ciclo_inicio': ciclo,
            'duracion': random.randint(2, 8),
            'intensidad': random.uniform(0.3, 0.8)
        })
        
        # Efectos inmediatos específicos por tipo de shock
        if tipo_shock == 'shock_petroleo':
            self._shock_precios_energia(1.5)  # +50% precios energía
        elif tipo_shock == 'shock_tecnologico':
            self._shock_productividad(1.2)  # +20% productividad sectorial
        elif tipo_shock == 'shock_financiero':
            self._shock_credito(0.7)  # -30% disponibilidad crédito
        
        self.logger.log_sistema(f"⚡ SHOCK EXTERNO: {tipo_shock} aplicado en ciclo {ciclo}")
    
    def _aplicar_shock_confianza(self, factor):
        """Aplica shock de confianza a consumidores y empresas"""
        try:
            # Afectar confianza de consumidores
            for consumidor in self.mercado.getConsumidores():
                if hasattr(consumidor, 'confianza'):
                    consumidor.confianza = max(0.1, min(1.0, consumidor.confianza + factor))
                elif hasattr(consumidor, 'propension_consumo'):
                    # Si no tiene confianza, afectar propensión al consumo
                    consumidor.propension_consumo = max(0.1, min(0.95, 
                        consumidor.propension_consumo * (1 + factor)))
            
            # Afectar confianza empresarial
            for empresa in self.mercado.getEmpresas():
                if hasattr(empresa, 'confianza_empresarial'):
                    empresa.confianza_empresarial = max(0.1, min(1.0, 
                        empresa.confianza_empresarial + factor))
        except Exception as e:
            self.logger.log_error(f"Error aplicando shock de confianza: {e}")
    
    def _shock_precios_energia(self, factor):
        """Aplica shock a precios de energía"""
        try:
            # Buscar empresas de energía y ajustar precios
            for empresa in self.mercado.getEmpresas():
                if hasattr(empresa, 'precios') and hasattr(empresa, 'sector'):
                    if empresa.sector in ['energia', 'petroleo', 'gas']:
                        for bien in empresa.precios:
                            empresa.precios[bien] *= factor
        except Exception as e:
            self.logger.log_error(f"Error aplicando shock de energía: {e}")
    
    def _shock_productividad(self, factor):
        """Aplica shock tecnológico de productividad"""
        try:
            # Mejorar productividad de empresas tecnológicas
            empresas_tech = [e for e in self.mercado.getEmpresas() 
                           if hasattr(e, 'sector') and e.sector in ['tecnologia', 'servicios']]
            for empresa in empresas_tech[:len(empresas_tech)//2]:  # Solo algunas empresas
                if hasattr(empresa, 'productividad'):
                    empresa.productividad *= factor
        except Exception as e:
            self.logger.log_error(f"Error aplicando shock de productividad: {e}")
    
    def _shock_credito(self, factor):
        """Aplica shock de restricción crediticia"""
        try:
            # Afectar capacidad de endeudamiento
            for consumidor in self.mercado.getConsumidores():
                if hasattr(consumidor, 'limite_credito'):
                    consumidor.limite_credito *= factor
            
            for empresa in self.mercado.getEmpresas():
                if hasattr(empresa, 'capacidad_endeudamiento'):
                    empresa.capacidad_endeudamiento *= factor
        except Exception as e:
            self.logger.log_error(f"Error aplicando shock de crédito: {e}")
    
    def _aplicar_estimulo_fiscal(self, monto):
        """Aplica estímulo fiscal distribuyendo dinero"""
        try:
            # Distribuir estímulo entre consumidores (proporcionalmente a ingresos bajos)
            consumidores = self.mercado.getConsumidores()
            if consumidores:
                estimulo_per_capita = monto / len(consumidores)
                for consumidor in consumidores:
                    # Más estímulo para consumidores con menos dinero
                    multiplicador = 2.0 if consumidor.dinero < 5000 else 1.0
                    consumidor.dinero += estimulo_per_capita * multiplicador
                
                self.logger.log_sistema(f"Estímulo fiscal aplicado: ${monto:,.0f}")
        except Exception as e:
            self.logger.log_error(f"Error aplicando estímulo fiscal: {e}")
    
    def _calcular_crecimiento_pib(self):
        """Calcula crecimiento del PIB"""
        if len(self.mercado.pib_historico) < 2:
            return 0.02  # Asumir 2% por defecto
        
        pib_actual = self.mercado.pib_historico[-1]
        pib_anterior = self.mercado.pib_historico[-2]
        
        if pib_anterior > 0:
            return (pib_actual - pib_anterior) / pib_anterior
        return 0.0
    
    def _calcular_tasa_desempleo(self):
        """Calcula tasa de desempleo"""
        consumidores = self.mercado.getConsumidores()
        if not consumidores:
            return 0.05
        
        desempleados = sum(1 for c in consumidores if not c.empleado)
        return desempleados / len(consumidores)
    
    def _log_estado_ciclo(self, ciclo):
        """Log del estado actual del ciclo económico"""
        if ciclo % 5 == 0:  # Log cada 5 ciclos
            self.logger.log_sistema(
                f"Ciclo Económico - Fase: {self.fase_actual.value}, "
                f"Duración: {self.ciclos_en_fase}, "
                f"Intensidad: {self.intensidad_fase:.2f}"
            )
    
    def obtener_estado_ciclo(self):
        """Obtiene estado completo del ciclo económico"""
        return {
            'fase_actual': self.fase_actual.value,
            'ciclos_en_fase': self.ciclos_en_fase,
            'intensidad_fase': self.intensidad_fase,
            'shocks_activos': len(self.shocks_activos),
            'proxima_transicion_estimada': self._estimar_proxima_transicion()
        }
    
    def _estimar_proxima_transicion(self):
        """Estima cuándo podría ocurrir la próxima transición"""
        duracion_promedio = self.duraciones_tipicas[self.fase_actual]['promedio']
        ciclos_restantes = max(0, duracion_promedio - self.ciclos_en_fase)
        return ciclos_restantes
