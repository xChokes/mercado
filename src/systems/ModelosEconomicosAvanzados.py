"""
Modelos Económicos Avanzados para el Simulador
=============================================

Implementa modelos económicos estándar de la literatura académica:
- Modelo DSGE (Dynamic Stochastic General Equilibrium)
- Modelo IS-LM (Investment-Saving / Liquidity preference-Money supply)
- Curva de Phillips
- Funciones de Producción Cobb-Douglas
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
import logging
from abc import ABC, abstractmethod


@dataclass
class ParametrosEconomicos:
    """Parámetros calibrados para modelos económicos"""
    
    # PARÁMETROS DSGE
    beta: float = 0.99          # Factor de descuento temporal
    sigma: float = 2.0          # Aversión al riesgo relativo
    phi: float = 1.0            # Elasticidad Frisch del trabajo
    alpha: float = 0.33         # Participación del capital en producción
    delta: float = 0.025        # Tasa de depreciación del capital
    rho_a: float = 0.95         # Persistencia del shock tecnológico
    sigma_a: float = 0.007      # Volatilidad del shock tecnológico
    
    # PARÁMETROS IS-LM
    sensibilidad_inversion: float = 0.5    # Sensibilidad inversión a tasas
    sensibilidad_consumo: float = 0.8      # Propensión marginal a consumir
    sensibilidad_demanda_dinero: float = 1.5  # Elasticidad demanda dinero
    
    # PARÁMETROS CURVA DE PHILLIPS
    coeficiente_phillips: float = 0.1      # Sensibilidad inflación-desempleo
    inflacion_esperada_peso: float = 0.6   # Peso expectativas inflación
    
    # PARÁMETROS FUNCIÓN PRODUCCIÓN
    productividad_total: float = 1.0       # Factor productividad total
    elasticidad_sustitucion: float = 0.7   # Elasticidad capital-trabajo


class ModeloEconomicoBase(ABC):
    """Clase base para modelos económicos"""
    
    def __init__(self, parametros: ParametrosEconomicos):
        self.parametros = parametros
        self.logger = logging.getLogger(self.__class__.__name__)
        self.estado_anterior = {}
        
    @abstractmethod
    def calcular_equilibrio(self, estado_actual: Dict) -> Dict:
        """Calcula el equilibrio del modelo"""
        pass
    
    @abstractmethod
    def predecir_proximo_periodo(self, estado_actual: Dict) -> Dict:
        """Predice variables para el próximo período"""
        pass


class ModeloDSGE(ModeloEconomicoBase):
    """
    Modelo DSGE (Dynamic Stochastic General Equilibrium)
    
    Modelo estándar de equilibrio general dinámico estocástico
    usado por bancos centrales para política económica.
    """
    
    def __init__(self, parametros: ParametrosEconomicos):
        super().__init__(parametros)
        self.shock_tecnologico = 0.0
        self.capital_acumulado = 1.0
        self.trabajo_ofrecido = 1.0
        
    def calcular_equilibrio(self, estado_actual: Dict) -> Dict:
        """Calcula equilibrio DSGE"""
        
        # Variables exógenas
        productividad = estado_actual.get('productividad', 1.0)
        oferta_monetaria = estado_actual.get('oferta_monetaria', 1.0)
        
        # Actualizar shock tecnológico (proceso AR(1))
        self.shock_tecnologico = (self.parametros.rho_a * self.shock_tecnologico + 
                                 np.random.normal(0, self.parametros.sigma_a))
        
        # Función de producción Cobb-Douglas
        produccion = (productividad * np.exp(self.shock_tecnologico) * 
                     (self.capital_acumulado ** self.parametros.alpha) * 
                     (self.trabajo_ofrecido ** (1 - self.parametros.alpha)))
        
        # Condiciones de primer orden
        
        # 1. Productividad marginal del trabajo = salario real
        salario_real = ((1 - self.parametros.alpha) * produccion / 
                       max(self.trabajo_ofrecido, 0.01))
        
        # 2. Productividad marginal del capital = tasa real + depreciación
        tasa_real_equilibrio = (self.parametros.alpha * produccion / 
                               max(self.capital_acumulado, 0.01) - self.parametros.delta)
        
        # 3. Ecuación de Euler para consumo
        consumo_optimo = (produccion - self.parametros.delta * self.capital_acumulado -
                         self._calcular_inversion_optima(tasa_real_equilibrio))
        
        # 4. Oferta de trabajo (trade-off consumo-ocio)
        trabajo_optimo = self._calcular_trabajo_optimo(salario_real, consumo_optimo)
        
        return {
            'produccion': max(produccion, 0.01),
            'consumo': max(consumo_optimo, 0.01),
            'inversion': self._calcular_inversion_optima(tasa_real_equilibrio),
            'salario_real': salario_real,
            'tasa_real': tasa_real_equilibrio,
            'trabajo': trabajo_optimo,
            'capital': self.capital_acumulado,
            'productividad_efectiva': productividad * np.exp(self.shock_tecnologico)
        }
    
    def predecir_proximo_periodo(self, estado_actual: Dict) -> Dict:
        """Predice variables del próximo período usando transiciones DSGE"""
        
        equilibrio_actual = self.calcular_equilibrio(estado_actual)
        
        # Actualizar capital (ecuación de acumulación)
        capital_proximo = ((1 - self.parametros.delta) * self.capital_acumulado + 
                          equilibrio_actual['inversion'])
        
        # Predicción de trabajo (ajuste gradual)
        trabajo_proximo = (0.8 * self.trabajo_ofrecido + 
                          0.2 * equilibrio_actual['trabajo'])
        
        # Actualizar estados
        self.capital_acumulado = capital_proximo
        self.trabajo_ofrecido = trabajo_proximo
        
        return {
            'capital_esperado': capital_proximo,
            'trabajo_esperado': trabajo_proximo,
            'produccion_esperada': equilibrio_actual['produccion'] * 1.02,  # Crecimiento tendencial
            'inflacion_esperada': self._calcular_inflacion_esperada(estado_actual)
        }
    
    def _calcular_inversion_optima(self, tasa_real: float) -> float:
        """Calcula inversión óptima dado tasa real"""
        # Función de inversión sensible a la tasa real
        inversion_base = 0.2 * self.capital_acumulado  # 20% depreciación base
        sensibilidad = -0.5  # Elasticidad inversión-tasa
        return max(inversion_base * (1 + sensibilidad * tasa_real), 0.01)
    
    def _calcular_trabajo_optimo(self, salario_real: float, consumo: float) -> float:
        """Calcula oferta óptima de trabajo"""
        # Condición de primer orden: TMS = salario real
        # Función utilidad: log(C) - (L^(1+1/φ))/(1+1/φ)
        if consumo <= 0:
            return 0.01
        
        trabajo_optimo = ((salario_real * consumo) ** self.parametros.phi)
        return min(max(trabajo_optimo, 0.01), 1.0)  # Entre 1% y 100%
    
    def _calcular_inflacion_esperada(self, estado_actual: Dict) -> float:
        """Calcula inflación esperada usando curva de Phillips"""
        desempleo = estado_actual.get('desempleo', 0.05)
        inflacion_anterior = estado_actual.get('inflacion', 0.02)
        
        # NAIRU (tasa natural de desempleo)
        nairu = 0.045
        
        # Curva de Phillips: π = πₑ - α(u - u*)
        inflacion_esperada = (self.parametros.inflacion_esperada_peso * inflacion_anterior - 
                            self.parametros.coeficiente_phillips * (desempleo - nairu))
        
        return inflacion_esperada


class ModeloISLM(ModeloEconomicoBase):
    """
    Modelo IS-LM (Investment-Saving / Liquidity preference-Money supply)
    
    Modelo macroeconómico clásico para equilibrio en mercados
    de bienes y dinero en el corto plazo.
    """
    
    def __init__(self, parametros: ParametrosEconomicos):
        super().__init__(parametros)
        self.pib_potencial = 1.0
        
    def calcular_equilibrio(self, estado_actual: Dict) -> Dict:
        """Calcula equilibrio IS-LM simultáneo"""
        
        # Variables exógenas
        gasto_gobierno = estado_actual.get('gasto_gobierno', 0.2)
        oferta_monetaria = estado_actual.get('oferta_monetaria', 1.0)
        nivel_precios = estado_actual.get('nivel_precios', 1.0)
        
        # Resolver sistema IS-LM
        try:
            tasa_equilibrio, pib_equilibrio = self._resolver_sistema_islm(
                gasto_gobierno, oferta_monetaria, nivel_precios
            )
        except:
            # Fallback en caso de no convergencia
            tasa_equilibrio = 0.03
            pib_equilibrio = self.pib_potencial
        
        # Calcular variables derivadas
        consumo = self._calcular_consumo(pib_equilibrio, tasa_equilibrio)
        inversion = self._calcular_inversion(tasa_equilibrio)
        demanda_dinero = self._calcular_demanda_dinero(pib_equilibrio, tasa_equilibrio)
        
        return {
            'pib_equilibrio': pib_equilibrio,
            'tasa_interes': tasa_equilibrio,
            'consumo': consumo,
            'inversion': inversion,
            'demanda_dinero': demanda_dinero,
            'brecha_producto': (pib_equilibrio - self.pib_potencial) / self.pib_potencial,
            'multiplicador_fiscal': self._calcular_multiplicador_fiscal()
        }
    
    def predecir_proximo_periodo(self, estado_actual: Dict) -> Dict:
        """Predice ajustes IS-LM para próximo período"""
        
        equilibrio_actual = self.calcular_equilibrio(estado_actual)
        
        # Ajuste gradual hacia equilibrio (rigideces nominales)
        pib_actual = estado_actual.get('pib', self.pib_potencial)
        tasa_actual = estado_actual.get('tasa_interes', 0.03)
        
        # Velocidad de ajuste
        velocidad_pib = 0.3
        velocidad_tasa = 0.5
        
        pib_proximo = (pib_actual + velocidad_pib * 
                      (equilibrio_actual['pib_equilibrio'] - pib_actual))
        
        tasa_proxima = (tasa_actual + velocidad_tasa * 
                       (equilibrio_actual['tasa_interes'] - tasa_actual))
        
        return {
            'pib_predicho': pib_proximo,
            'tasa_predicha': tasa_proxima,
            'ajuste_necesario': abs(equilibrio_actual['pib_equilibrio'] - pib_actual),
            'presion_inflacionaria': equilibrio_actual['brecha_producto']
        }
    
    def _resolver_sistema_islm(self, G: float, M: float, P: float) -> Tuple[float, float]:
        """Resuelve sistema IS-LM por método iterativo"""
        
        # Parámetros del modelo
        c = self.parametros.sensibilidad_consumo        # Propensión marginal a consumir
        d = self.parametros.sensibilidad_inversion      # Sensibilidad inversión a tasa
        k = self.parametros.sensibilidad_demanda_dinero # Sensibilidad demanda dinero a PIB
        h = 1.0                                         # Sensibilidad demanda dinero a tasa
        
        # Método de Newton-Raphson para sistema no lineal
        r = 0.03  # Guess inicial tasa
        
        for i in range(20):  # Máximo 20 iteraciones
            
            # Ecuación IS: Y = C + I + G = c*Y + I₀ - d*r + G
            # Despejando: Y = (I₀ + G) / (1 - c + d*r/(1-c))
            autonomo = 0.3 + G  # Inversión autónoma + gasto gobierno
            Y_is = autonomo / (1 - c + d * r / (1 - c))
            
            # Ecuación LM: M/P = L(Y,r) = k*Y - h*r
            # Despejando: r = (k*Y - M/P) / h
            r_lm = (k * Y_is - M / P) / h
            
            # Comprobar convergencia
            if abs(r_lm - r) < 1e-6:
                return r, Y_is
            
            # Actualizar guess
            r = 0.5 * r + 0.5 * r_lm
        
        # Si no converge, retornar último valor
        return r, Y_is
    
    def _calcular_consumo(self, pib: float, tasa: float) -> float:
        """Calcula consumo óptimo"""
        c = self.parametros.sensibilidad_consumo
        consumo_autonomo = 0.1
        return consumo_autonomo + c * pib
    
    def _calcular_inversion(self, tasa: float) -> float:
        """Calcula inversión óptima"""
        inversion_autonoma = 0.3
        d = self.parametros.sensibilidad_inversion
        return max(inversion_autonoma - d * tasa, 0.01)
    
    def _calcular_demanda_dinero(self, pib: float, tasa: float) -> float:
        """Calcula demanda de dinero"""
        k = self.parametros.sensibilidad_demanda_dinero
        h = 1.0
        return k * pib - h * tasa
    
    def _calcular_multiplicador_fiscal(self) -> float:
        """Calcula multiplicador del gasto fiscal"""
        c = self.parametros.sensibilidad_consumo
        return 1 / (1 - c)


class ModeloCurvaPhillips:
    """
    Curva de Phillips con expectativas racionales
    
    Modela la relación entre inflación y desempleo
    incorporando expectativas de inflación.
    """
    
    def __init__(self, parametros: ParametrosEconomicos):
        self.parametros = parametros
        self.nairu = 0.045  # 4.5% desempleo natural
        self.expectativas_inflacion = 0.02
        
    def calcular_inflacion(self, desempleo: float, shock_oferta: float = 0.0) -> float:
        """
        Calcula inflación usando curva de Phillips aumentada por expectativas
        
        π = πₑ - α(u - u*) + ε
        
        Donde:
        π = inflación actual
        πₑ = inflación esperada
        α = coeficiente de Phillips
        u = tasa de desempleo
        u* = NAIRU (tasa natural)
        ε = shock de oferta
        """
        
        brecha_desempleo = desempleo - self.nairu
        
        inflacion = (self.expectativas_inflacion - 
                    self.parametros.coeficiente_phillips * brecha_desempleo + 
                    shock_oferta)
        
        return inflacion
    
    def actualizar_expectativas(self, inflacion_observada: float):
        """Actualiza expectativas de inflación (formación adaptativa)"""
        peso_nuevo = 0.3
        self.expectativas_inflacion = ((1 - peso_nuevo) * self.expectativas_inflacion + 
                                      peso_nuevo * inflacion_observada)
    
    def calcular_nairu_dinamica(self, historico_desempleo: List[float]) -> float:
        """Calcula NAIRU dinámicamente basado en tendencias"""
        if len(historico_desempleo) < 10:
            return self.nairu
        
        # Promedio móvil de largo plazo como proxy de NAIRU
        ventana = min(20, len(historico_desempleo))
        nairu_estimada = sum(historico_desempleo[-ventana:]) / ventana
        
        # Suavizar cambios en NAIRU
        self.nairu = 0.9 * self.nairu + 0.1 * nairu_estimada
        return self.nairu


class FuncionProduccionCobbDouglas:
    """
    Función de producción Cobb-Douglas con progreso tecnológico
    
    Y = A * K^α * L^(1-α)
    
    Donde:
    Y = Producto
    A = Productividad total de factores
    K = Capital
    L = Trabajo
    α = Elasticidad del capital
    """
    
    def __init__(self, parametros: ParametrosEconomicos):
        self.parametros = parametros
        self.productividad_tfp = parametros.productividad_total
        self.tendencia_tecnologica = 0.015  # 1.5% anual
        
    def calcular_produccion(self, capital: float, trabajo: float) -> float:
        """Calcula producción dado capital y trabajo"""
        return (self.productividad_tfp * 
               (capital ** self.parametros.alpha) * 
               (trabajo ** (1 - self.parametros.alpha)))
    
    def calcular_productividad_marginal_capital(self, capital: float, trabajo: float) -> float:
        """Calcula productividad marginal del capital"""
        return (self.parametros.alpha * self.productividad_tfp * 
               (trabajo ** (1 - self.parametros.alpha)) * 
               (capital ** (self.parametros.alpha - 1)))
    
    def calcular_productividad_marginal_trabajo(self, capital: float, trabajo: float) -> float:
        """Calcula productividad marginal del trabajo"""
        return ((1 - self.parametros.alpha) * self.productividad_tfp * 
               (capital ** self.parametros.alpha) * 
               (trabajo ** (-self.parametros.alpha)))
    
    def actualizar_tecnologia(self, shock_tecnologico: float = 0.0):
        """Actualiza productividad total con progreso tecnológico"""
        crecimiento = self.tendencia_tecnologica / 12 + shock_tecnologico  # Mensual
        self.productividad_tfp *= (1 + crecimiento)
    
    def calcular_elasticidad_sustitucion(self, capital: float, trabajo: float) -> float:
        """Calcula elasticidad de sustitución capital-trabajo"""
        # Para Cobb-Douglas es siempre 1, pero permitimos variación
        return self.parametros.elasticidad_sustitucion


class IntegradorModelosEconomicos:
    """
    Integra múltiples modelos económicos para análisis comprehensivo
    """
    
    def __init__(self, parametros: Optional[ParametrosEconomicos] = None):
        if parametros is None:
            parametros = ParametrosEconomicos()
        
        self.dsge = ModeloDSGE(parametros)
        self.islm = ModeloISLM(parametros)
        self.phillips = ModeloCurvaPhillips(parametros)
        self.cobb_douglas = FuncionProduccionCobbDouglas(parametros)
        
        self.logger = logging.getLogger('IntegradorModelos')
        
    def analisis_completo(self, estado_economico: Dict) -> Dict:
        """Ejecuta análisis usando todos los modelos disponibles"""
        
        resultados = {}
        
        try:
            # Análisis DSGE
            resultados['dsge'] = self.dsge.calcular_equilibrio(estado_economico)
            resultados['dsge_prediccion'] = self.dsge.predecir_proximo_periodo(estado_economico)
            
            # Análisis IS-LM
            resultados['islm'] = self.islm.calcular_equilibrio(estado_economico)
            resultados['islm_prediccion'] = self.islm.predecir_proximo_periodo(estado_economico)
            
            # Análisis Curva de Phillips
            desempleo = estado_economico.get('desempleo', 0.05)
            resultados['phillips_inflacion'] = self.phillips.calcular_inflacion(desempleo)
            
            # Análisis función de producción
            capital = estado_economico.get('capital', 1.0)
            trabajo = estado_economico.get('trabajo', 1.0)
            resultados['produccion_teorica'] = self.cobb_douglas.calcular_produccion(capital, trabajo)
            
            # Síntesis de resultados
            resultados['sintesis'] = self._sintetizar_resultados(resultados)
            
        except Exception as e:
            self.logger.error(f"Error en análisis completo: {e}")
            resultados['error'] = str(e)
        
        return resultados
    
    def _sintetizar_resultados(self, resultados: Dict) -> Dict:
        """Sintetiza resultados de múltiples modelos"""
        
        sintesis = {}
        
        # Promedio ponderado de predicciones PIB
        if 'dsge' in resultados and 'islm' in resultados:
            pib_dsge = resultados['dsge'].get('produccion', 1.0)
            pib_islm = resultados['islm'].get('pib_equilibrio', 1.0)
            sintesis['pib_consenso'] = 0.6 * pib_dsge + 0.4 * pib_islm
        
        # Tasa de interés consenso
        if 'dsge' in resultados and 'islm' in resultados:
            tasa_dsge = resultados['dsge'].get('tasa_real', 0.03)
            tasa_islm = resultados['islm'].get('tasa_interes', 0.03)
            sintesis['tasa_consenso'] = 0.5 * tasa_dsge + 0.5 * tasa_islm
        
        # Inflación esperada
        if 'phillips_inflacion' in resultados:
            sintesis['inflacion_consenso'] = resultados['phillips_inflacion']
        
        # Evaluación de consistencia entre modelos
        sintesis['consistencia_modelos'] = self._evaluar_consistencia(resultados)
        
        return sintesis
    
    def _evaluar_consistencia(self, resultados: Dict) -> float:
        """Evalúa consistencia entre predicciones de diferentes modelos"""
        
        if 'dsge' not in resultados or 'islm' not in resultados:
            return 0.5
        
        # Comparar predicciones de PIB
        pib_dsge = resultados['dsge'].get('produccion', 1.0)
        pib_islm = resultados['islm'].get('pib_equilibrio', 1.0)
        
        diferencia_relativa = abs(pib_dsge - pib_islm) / max(pib_dsge, pib_islm, 0.01)
        
        # Consistencia inversamente proporcional a la diferencia
        consistencia = max(0, 1 - diferencia_relativa * 2)
        
        return consistencia
