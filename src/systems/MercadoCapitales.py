"""
Mercado de Capitales Sofisticado para Simulación Económica Hiperrealista
Implementa bolsa de valores, derivados, análisis fundamental/técnico y burbujas especulativas
"""

import random
import math
from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional
from ..utils.SimuladorLogger import get_simulador_logger


class TipoInstrumento(Enum):
    ACCION = "accion"
    BONO = "bono"
    DERIVADO = "derivado"
    ETF = "etf"
    COMMODITY = "commodity"


class TipoInversor(Enum):
    RETAIL = "retail"           # Inversores minoristas
    INSTITUCIONAL = "institucional"  # Fondos, pensiones
    ESPECULATIVO = "especulativo"    # Hedge funds, day traders
    BANCO_CENTRAL = "banco_central"  # Autoridad monetaria


@dataclass
class Instrumento:
    """Instrumento financiero genérico"""
    ticker: str
    nombre: str
    tipo: TipoInstrumento
    precio_actual: float
    precio_inicial: float
    volumen_diario: int = 0
    capitalizacion: float = 0.0
    
    # Métricas fundamentales (solo para acciones)
    pe_ratio: Optional[float] = None
    dividend_yield: Optional[float] = None
    roe: Optional[float] = None
    debt_to_equity: Optional[float] = None
    
    # Historia de precios (últimos 20 períodos)
    historia_precios: List[float] = None
    
    def __post_init__(self):
        if self.historia_precios is None:
            self.historia_precios = [self.precio_inicial]


class Accion(Instrumento):
    """Acción de empresa con métricas fundamentales"""
    
    def __init__(self, empresa, ticker: str):
        self.empresa = empresa
        precio_inicial = self.calcular_precio_teorico(empresa)
        
        super().__init__(
            ticker=ticker,
            nombre=empresa.nombre,
            tipo=TipoInstrumento.ACCION,
            precio_actual=precio_inicial,
            precio_inicial=precio_inicial
        )
        
        self.acciones_circulacion = 1000000  # 1M acciones
        self.capitalizacion = self.precio_actual * self.acciones_circulacion
        
        # Actualizar métricas fundamentales
        self.actualizar_metricas_fundamentales()
    
    def calcular_precio_teorico(self, empresa):
        """Calcula precio teórico basado en fundamentales de la empresa"""
        if not hasattr(empresa, 'dinero') or empresa.dinero <= 0:
            return 10.0
            
        # Valor libro por acción (simplificado)
        valor_libro = empresa.dinero / 1000000  # 1M acciones
        
        # Múltiplo P/B basado en crecimiento esperado
        multiplo_pb = random.uniform(1.2, 3.5)
        
        return max(1.0, valor_libro * multiplo_pb)
    
    def actualizar_metricas_fundamentales(self):
        """Actualiza métricas fundamentales de la acción"""
        if not hasattr(self.empresa, 'dinero'):
            return
            
        # P/E Ratio (simplificado)
        utilidades_estimadas = max(1, self.empresa.dinero * 0.05)  # 5% ROA
        self.pe_ratio = (self.precio_actual * self.acciones_circulacion) / utilidades_estimadas
        
        # ROE (Return on Equity)
        self.roe = utilidades_estimadas / max(1, self.empresa.dinero)
        
        # Dividend Yield (simplificado)
        self.dividend_yield = random.uniform(0.02, 0.06) if self.pe_ratio < 25 else 0.01
        
        # Debt to Equity (simplificado)
        self.debt_to_equity = random.uniform(0.2, 1.5)


class FondoInversion:
    """Fondo de inversión institucional"""
    
    def __init__(self, nombre: str, tipo_inversor: TipoInversor, capital_inicial: float):
        self.nombre = nombre
        self.tipo = tipo_inversor
        self.capital = capital_inicial
        self.cartera = {}  # {ticker: cantidad}
        self.valor_cartera = capital_inicial
        
        # Estrategia de inversión
        self.tolerancia_riesgo = random.uniform(0.3, 0.8)
        self.horizonte_inversion = random.randint(12, 60)  # 1-5 años en ciclos
        self.sesgo_momentum = random.uniform(0.1, 0.6)
        
        # Performance tracking
        self.rendimiento_acumulado = 0.0
        self.volatilidad = 0.0


class BolsaValores:
    """Bolsa de valores completa con múltiples instrumentos"""
    
    def __init__(self, mercado):
        self.mercado = mercado
        self.logger = get_simulador_logger()
        
        # Instrumentos listados
        self.instrumentos = {}  # {ticker: Instrumento}
        self.acciones = {}      # {ticker: Accion}
        
        # Índices bursátiles
        self.indices = {
            "GENERAL": [],      # Índice general
            "TECH": [],         # Tecnología
            "BANKING": [],      # Financiero
            "INDUSTRIAL": []    # Industrial
        }
        
        # Participantes del mercado
        self.fondos_inversion = []
        self.inversores_retail = []
        
        # Estado del mercado
        self.sentimiento_mercado = 0.5  # 0=bearish, 1=bullish
        self.volatilidad_mercado = 0.15  # 15% volatilidad base
        self.volumen_total_diario = 0
        
        # Burbujas y crashes
        self.en_burbuja = False
        self.probabilidad_crash = 0.02  # 2% por ciclo
        self.factor_burbuja = 1.0
        
        self.logger.log_configuracion("Bolsa de Valores inicializada")
        
    def listar_empresas(self):
        """Lista todas las empresas del mercado en la bolsa"""
        empresas_listadas = 0
        
        for empresa in self.mercado.getEmpresas():
            if hasattr(empresa, 'nombre') and hasattr(empresa, 'dinero'):
                # Crear ticker
                ticker = empresa.nombre.upper().replace('_', '').replace(' ', '')[:4]
                
                # Crear acción
                accion = Accion(empresa, ticker)
                self.acciones[ticker] = accion
                self.instrumentos[ticker] = accion
                
                # Asignar a índice sectorial
                self._asignar_a_indice(accion)
                
                empresas_listadas += 1
        
        # Crear fondos de inversión
        self._crear_fondos_inversion()
        
        self.logger.log_configuracion(f"   Empresas listadas: {empresas_listadas}")
        self.logger.log_configuración(f"   Fondos creados: {len(self.fondos_inversion)}")
        
    def _asignar_a_indice(self, accion: Accion):
        """Asigna acción a índices apropiados"""
        # Todos van al índice general
        self.indices["GENERAL"].append(accion.ticker)
        
        # Clasificar por sector (simplificado)
        nombre = accion.nombre.lower()
        if any(word in nombre for word in ['tech', 'computadora', 'software', 'internet']):
            self.indices["TECH"].append(accion.ticker)
        elif any(word in nombre for word in ['banco', 'financ', 'credit']):
            self.indices["BANKING"].append(accion.ticker)
        else:
            self.indices["INDUSTRIAL"].append(accion.ticker)
    
    def _crear_fondos_inversion(self):
        """Crea fondos de inversión institucionales"""
        # Fondo de pensiones (conservador)
        fondo_pensiones = FondoInversion("Fondo Pensiones", TipoInversor.INSTITUCIONAL, 5000000)
        fondo_pensiones.tolerancia_riesgo = 0.3
        
        # Fondo mutuo (balanceado)
        fondo_mutuo = FondoInversion("Fondo Mutuo", TipoInversor.INSTITUCIONAL, 2000000)
        fondo_mutuo.tolerancia_riesgo = 0.5
        
        # Hedge fund (agresivo)
        hedge_fund = FondoInversion("Hedge Fund", TipoInversor.ESPECULATIVO, 1000000)
        hedge_fund.tolerancia_riesgo = 0.8
        
        self.fondos_inversion = [fondo_pensiones, fondo_mutuo, hedge_fund]
        
        # Invertir capital inicial
        for fondo in self.fondos_inversion:
            self._diversificar_cartera_inicial(fondo)
    
    def _diversificar_cartera_inicial(self, fondo: FondoInversion):
        """Diversifica cartera inicial del fondo"""
        capital_disponible = fondo.capital * 0.8  # 80% invertido, 20% cash
        acciones_disponibles = list(self.acciones.keys())
        
        if not acciones_disponibles:
            return
            
        # Invertir en 3-8 acciones diferentes
        num_acciones = min(random.randint(3, 8), len(acciones_disponibles))
        acciones_elegidas = random.sample(acciones_disponibles, num_acciones)
        
        for ticker in acciones_elegidas:
            accion = self.acciones[ticker]
            peso_cartera = random.uniform(0.05, 0.25)  # 5-25% por acción
            inversion = capital_disponible * peso_cartera
            cantidad = int(inversion / accion.precio_actual)
            
            if cantidad > 0:
                fondo.cartera[ticker] = cantidad
                fondo.capital -= cantidad * accion.precio_actual
    
    def ejecutar_ciclo_bursatil(self, ciclo):
        """Ejecuta un día de trading en la bolsa"""
        # 1. Actualizar sentimiento del mercado
        self._actualizar_sentimiento_mercado()
        
        # 2. Detectar/gestionar burbujas
        self._gestionar_burbujas_y_crashes(ciclo)
        
        # 3. Actualizar precios de acciones
        self._actualizar_precios_acciones()
        
        # 4. Trading institucional
        self._ejecutar_trading_institucional()
        
        # 5. Trading retail (consumidores ricos)
        self._ejecutar_trading_retail()
        
        # 6. Actualizar métricas de mercado
        self._actualizar_metricas_mercado()
        
        # 7. Calcular índices
        indices_valores = self._calcular_indices()
        
        return self._generar_reporte_bursatil(ciclo, indices_valores)
    
    def _actualizar_sentimiento_mercado(self):
        """Actualiza sentimiento basado en indicadores económicos"""
        if len(self.mercado.pib_historico) < 2:
            return
            
        # Factores que afectan sentimiento
        pib_actual = self.mercado.pib_historico[-1]
        pib_anterior = self.mercado.pib_historico[-2]
        crecimiento_pib = (pib_actual - pib_anterior) / pib_anterior if pib_anterior > 0 else 0
        
        inflacion = self.mercado.inflacion_historica[-1] if self.mercado.inflacion_historica else 0
        crisis_activa = getattr(self.mercado, 'crisis_financiera_activa', False)
        
        # Calcular nuevo sentimiento
        delta_sentimiento = 0
        delta_sentimiento += crecimiento_pib * 2.0  # PIB tiene peso 2x
        delta_sentimiento -= abs(inflacion) * 0.5   # Inflación moderada es buena
        delta_sentimiento -= 0.3 if crisis_activa else 0
        
        # Agregar ruido aleatorio
        delta_sentimiento += random.gauss(0, 0.05)
        
        # Actualizar con inercia
        self.sentimiento_mercado = max(0, min(1, 
            self.sentimiento_mercado * 0.7 + (0.5 + delta_sentimiento) * 0.3
        ))
        
        # Volatilidad inversa al sentimiento
        self.volatilidad_mercado = 0.05 + (1 - self.sentimiento_mercado) * 0.25
    
    def _gestionar_burbujas_y_crashes(self, ciclo):
        """Detecta y gestiona burbujas especulativas y crashes"""
        indices_actual = self._calcular_indices()
        general_index = indices_actual.get("GENERAL", 100)
        
        # Detectar burbuja: índice >50% por encima de fundamentales
        if not self.en_burbuja and general_index > 150:
            if random.random() < 0.1:  # 10% probabilidad de iniciar burbuja
                self.en_burbuja = True
                self.factor_burbuja = 1.2
                self.logger.log_sistema(f"🎈 BURBUJA BURSÁTIL iniciada - Ciclo {ciclo}")
        
        # Gestionar burbuja activa
        if self.en_burbuja:
            self.factor_burbuja *= random.uniform(1.02, 1.08)  # Crecimiento 2-8%
            
            # Probabilidad creciente de crash
            self.probabilidad_crash = min(0.15, 0.02 + (self.factor_burbuja - 1.2) * 0.1)
            
            # Ejecutar crash
            if random.random() < self.probabilidad_crash:
                self._ejecutar_crash_bursatil(ciclo)
    
    def _ejecutar_crash_bursatil(self, ciclo):
        """Ejecuta un crash bursátil"""
        self.en_burbuja = False
        self.factor_burbuja = 1.0
        self.probabilidad_crash = 0.02
        
        # Caída entre 20-50%
        factor_crash = random.uniform(0.5, 0.8)
        
        for ticker, accion in self.acciones.items():
            accion.precio_actual *= factor_crash
            accion.historia_precios.append(accion.precio_actual)
        
        # Pánico: vender todo
        for fondo in self.fondos_inversion:
            self._liquidar_cartera_panico(fondo, factor_crash)
        
        self.sentimiento_mercado = 0.1  # Extremo pesimismo
        self.volatilidad_mercado = 0.4   # Alta volatilidad
        
        self.logger.log_sistema(f"💥 CRASH BURSÁTIL - Ciclo {ciclo}: Caída {(1-factor_crash)*100:.0f}%")
    
    def _liquidar_cartera_panico(self, fondo: FondoInversion, factor_crash: float):
        """Liquida cartera en pánico durante crash"""
        for ticker, cantidad in list(fondo.cartera.items()):
            if random.random() < 0.7:  # 70% probabilidad de vender
                accion = self.acciones[ticker]
                valor_venta = cantidad * accion.precio_actual
                fondo.capital += valor_venta
                del fondo.cartera[ticker]
    
    def _actualizar_precios_acciones(self):
        """Actualiza precios de todas las acciones"""
        for ticker, accion in self.acciones.items():
            # Precio fundamental
            precio_fundamental = accion.calcular_precio_teorico(accion.empresa)
            
            # Factors de precio
            factor_sentimiento = 0.8 + (self.sentimiento_mercado * 0.4)
            factor_volatilidad = random.gauss(1.0, self.volatilidad_mercado)
            factor_burbuja = self.factor_burbuja if self.en_burbuja else 1.0
            
            # Momentum (análisis técnico básico)
            if len(accion.historia_precios) >= 5:
                precios_recientes = accion.historia_precios[-5:]
                tendencia = (precios_recientes[-1] - precios_recientes[0]) / precios_recientes[0]
                factor_momentum = 1 + (tendencia * 0.1)  # 10% del momentum
            else:
                factor_momentum = 1.0
            
            # Calcular nuevo precio
            nuevo_precio = precio_fundamental * factor_sentimiento * factor_volatilidad * factor_burbuja * factor_momentum
            
            # Límites de variación diaria
            max_cambio = accion.precio_actual * 0.15  # ±15% máximo por día
            nuevo_precio = max(accion.precio_actual - max_cambio, 
                             min(accion.precio_actual + max_cambio, nuevo_precio))
            
            accion.precio_actual = max(0.1, nuevo_precio)  # Precio mínimo $0.1
            accion.historia_precios.append(accion.precio_actual)
            
            # Mantener solo últimos 20 precios
            if len(accion.historia_precios) > 20:
                accion.historia_precios.pop(0)
            
            # Actualizar métricas fundamentales
            accion.actualizar_metricas_fundamentales()
    
    def _ejecutar_trading_institucional(self):
        """Ejecuta trading de fondos institucionales"""
        for fondo in self.fondos_inversion:
            self._trading_fondo(fondo)
    
    def _trading_fondo(self, fondo: FondoInversion):
        """Ejecuta estrategia de trading de un fondo específico"""
        # Decidir si comprar o vender
        if random.random() < 0.3:  # 30% probabilidad de trading activo
            if random.random() < 0.6:  # 60% compra, 40% venta
                self._comprar_accion_fondo(fondo)
            else:
                self._vender_accion_fondo(fondo)
    
    def _comprar_accion_fondo(self, fondo: FondoInversion):
        """Fondo compra acciones"""
        if fondo.capital < 1000:  # Capital mínimo para operar
            return
            
        # Seleccionar acción basada en estrategia
        ticker_objetivo = self._seleccionar_accion_compra(fondo)
        if not ticker_objetivo:
            return
            
        accion = self.acciones[ticker_objetivo]
        
        # Determinar cantidad a comprar
        inversion_max = min(fondo.capital * 0.1, fondo.capital - 1000)  # Máximo 10% del capital
        cantidad = int(inversion_max / accion.precio_actual)
        
        if cantidad > 0:
            costo_total = cantidad * accion.precio_actual
            fondo.capital -= costo_total
            fondo.cartera[ticker_objetivo] = fondo.cartera.get(ticker_objetivo, 0) + cantidad
            accion.volumen_diario += cantidad
    
    def _vender_accion_fondo(self, fondo: FondoInversion):
        """Fondo vende acciones"""
        if not fondo.cartera:
            return
            
        # Seleccionar acción a vender
        ticker_venta = random.choice(list(fondo.cartera.keys()))
        accion = self.acciones[ticker_venta]
        
        # Vender hasta 50% de la posición
        cantidad_actual = fondo.cartera[ticker_venta]
        cantidad_venta = random.randint(1, max(1, cantidad_actual // 2))
        
        valor_venta = cantidad_venta * accion.precio_actual
        fondo.capital += valor_venta
        fondo.cartera[ticker_venta] -= cantidad_venta
        
        if fondo.cartera[ticker_venta] == 0:
            del fondo.cartera[ticker_venta]
            
        accion.volumen_diario += cantidad_venta
    
    def _seleccionar_accion_compra(self, fondo: FondoInversion) -> str:
        """Selecciona acción para comprar basada en estrategia del fondo"""
        acciones_disponibles = list(self.acciones.keys())
        
        if not acciones_disponibles:
            return None
            
        if fondo.tipo == TipoInversor.INSTITUCIONAL:
            # Conservador: buscar P/E bajo y dividend yield alto
            mejor_accion = None
            mejor_score = -1
            
            for ticker in acciones_disponibles:
                accion = self.acciones[ticker]
                if accion.pe_ratio and accion.dividend_yield:
                    score = (1 / accion.pe_ratio) + accion.dividend_yield
                    if score > mejor_score:
                        mejor_score = score
                        mejor_accion = ticker
            
            return mejor_accion or random.choice(acciones_disponibles)
            
        elif fondo.tipo == TipoInversor.ESPECULATIVO:
            # Agresivo: buscar momentum y volatilidad
            acciones_momentum = []
            
            for ticker in acciones_disponibles:
                accion = self.acciones[ticker]
                if len(accion.historia_precios) >= 3:
                    cambio_reciente = (accion.precio_actual - accion.historia_precios[-3]) / accion.historia_precios[-3]
                    if cambio_reciente > 0.05:  # Subió >5% en últimos 3 períodos
                        acciones_momentum.append(ticker)
            
            return random.choice(acciones_momentum) if acciones_momentum else random.choice(acciones_disponibles)
        
        else:
            return random.choice(acciones_disponibles)
    
    def _ejecutar_trading_retail(self):
        """Simula trading de inversores retail (consumidores ricos)"""
        # Solo consumidores con más de $50K pueden invertir
        inversores_potenciales = [c for c in self.mercado.getConsumidores() 
                                if hasattr(c, 'dinero') and c.dinero > 50000]
        
        # 5% de los consumidores ricos hacen trading
        num_traders = max(1, len(inversores_potenciales) // 20)
        traders = random.sample(inversores_potenciales, min(num_traders, len(inversores_potenciales)))
        
        for trader in traders:
            if random.random() < 0.1:  # 10% probabilidad de trading
                self._trading_retail_individual(trader)
    
    def _trading_retail_individual(self, consumidor):
        """Trading individual de consumidor retail"""
        capital_inversion = min(consumidor.dinero * 0.05, 10000)  # Máximo 5% del capital o $10K
        
        if capital_inversion < 100:  # Mínimo $100 para invertir
            return
            
        # Retail tiende a ser más emocional
        if self.sentimiento_mercado > 0.7 and random.random() < 0.8:  # Comprar en euforia
            ticker_compra = random.choice(list(self.acciones.keys()))
            accion = self.acciones[ticker_compra]
            cantidad = int(capital_inversion / accion.precio_actual)
            
            if cantidad > 0:
                costo = cantidad * accion.precio_actual
                consumidor.dinero -= costo
                accion.volumen_diario += cantidad
                
        elif self.sentimiento_mercado < 0.3 and random.random() < 0.6:  # Vender en pánico
            # Simular venta durante pánico del mercado
            acciones_para_vender = [a for a in self.acciones.values() if a.precio > a.precio_inicial * 0.5]
            if acciones_para_vender:
                accion_venta = random.choice(acciones_para_vender)
                cantidad_venta = random.randint(1, 20)
                
                # Reducir precio por presión de venta
                factor_venta = 0.98  # 2% reducción por venta
                accion_venta.precio *= factor_venta
                accion_venta.volumen_diario += cantidad_venta
    
    def _actualizar_metricas_mercado(self):
        """Actualiza métricas generales del mercado"""
        self.volumen_total_diario = sum(accion.volumen_diario for accion in self.acciones.values())
        
        # Reset volumen diario
        for accion in self.acciones.values():
            accion.volumen_diario = 0
    
    def _calcular_indices(self):
        """Calcula valores de índices bursátiles"""
        indices_valores = {}
        
        for nombre_indice, tickers in self.indices.items():
            if not tickers:
                indices_valores[nombre_indice] = 100
                continue
                
            # Promedio ponderado por capitalización
            valor_total = 0
            cap_total = 0
            
            for ticker in tickers:
                if ticker in self.acciones:
                    accion = self.acciones[ticker]
                    cap = accion.precio_actual * accion.acciones_circulacion
                    valor_total += cap
                    cap_total += accion.acciones_circulacion
            
            if cap_total > 0:
                precio_promedio = valor_total / cap_total
                indices_valores[nombre_indice] = precio_promedio
            else:
                indices_valores[nombre_indice] = 100
        
        return indices_valores
    
    def _generar_reporte_bursatil(self, ciclo, indices_valores):
        """Genera reporte del ciclo bursátil"""
        return {
            'ciclo': ciclo,
            'sentimiento_mercado': self.sentimiento_mercado,
            'volatilidad_mercado': self.volatilidad_mercado,
            'volumen_total': self.volumen_total_diario,
            'en_burbuja': self.en_burbuja,
            'indices': indices_valores,
            'num_acciones_listadas': len(self.acciones),
            'capitalizacion_total': sum(a.precio_actual * a.acciones_circulacion for a in self.acciones.values())
        }
    
    def obtener_estadisticas_mercado(self):
        """Obtiene estadísticas consolidadas del mercado"""
        if not self.acciones:
            return {}
            
        precios_actuales = [a.precio_actual for a in self.acciones.values()]
        precios_iniciales = [a.precio_inicial for a in self.acciones.values()]
        
        rendimiento_promedio = sum((pa/pi - 1) for pa, pi in zip(precios_actuales, precios_iniciales)) / len(precios_actuales)
        
        return {
            'sentimiento_mercado': self.sentimiento_mercado,
            'volatilidad_mercado': self.volatilidad_mercado,
            'acciones_listadas': len(self.acciones),
            'capitalizacion_total': sum(a.precio_actual * a.acciones_circulacion for a in self.acciones.values()),
            'rendimiento_promedio': rendimiento_promedio,
            'volumen_promedio_diario': self.volumen_total_diario,
            'en_burbuja': self.en_burbuja,
            'fondos_activos': len(self.fondos_inversion)
        }
