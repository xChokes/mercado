"""
Sistema de Precios Dinámicos para el Simulador Económico
Implementa ajustes de precios realistas basados en oferta, demanda y competencia
"""

import random
import math
from collections import defaultdict


class SistemaPreciosDinamicos:
    """Maneja ajustes dinámicos de precios basados en condiciones de mercado"""

    def __init__(self, mercado):
        self.mercado = mercado
        self.precios_base = {}  # Precios de referencia inicial
        self.elasticidades = {}  # Elasticidad precio-demanda por bien
        self.competencia_cache = {}  # Cache de análisis de competencia
        self.volatilidad_mercado = 0.1  # Factor de volatilidad base

        # Inicializar elasticidades por categoría
        self.elasticidades_categoria = {
            'alimentos_basicos': -0.3,  # Inelásticos (necesidades)
            'alimentos_lujo': -0.8,    # Más elásticos
            'bienes_duraderos': -1.2,  # Muy elásticos
            'servicios': -0.6,         # Moderadamente elásticos
            'tecnologia': -1.5,        # Muy elásticos
            'servicios_lujo': -1.8,    # Altamente elásticos
            'capital': -0.9,           # Elásticos
            'intermedio': -0.5         # Moderadamente inelásticos
        }

    def inicializar_precios_base(self):
        """Establece precios base para todos los bienes"""
        for bien_nombre, bien in self.mercado.bienes.items():
            # Precio base según categoría
            precios_categoria = {
                'alimentos_basicos': (5, 20),
                'alimentos_lujo': (15, 50),
                'bienes_duraderos': (100, 1000),
                'servicios': (20, 200),
                'tecnologia': (200, 2000),
                'servicios_lujo': (50, 500),
                'capital': (1000, 10000),
                'intermedio': (10, 100)
            }

            categoria = bien.categoria
            rango = precios_categoria.get(categoria, (10, 50))
            precio_base = random.uniform(rango[0], rango[1])

            self.precios_base[bien_nombre] = precio_base
            self.elasticidades[bien_nombre] = self.elasticidades_categoria.get(
                categoria, -0.8)

    def calcular_precio_dinamico(self, empresa, bien_nombre, inventario_actual, demanda_reciente):
        """Calcula el precio dinámico con control de inflación mejorado"""
        if bien_nombre not in self.precios_base:
            self.precios_base[bien_nombre] = random.uniform(10, 50)

        precio_base = self.precios_base[bien_nombre]
        precio_actual = empresa.precios.get(bien_nombre, precio_base)

        # Factor 1: Oferta y demanda básica (moderado)
        factor_stock = self._calcular_factor_stock_moderado(inventario_actual)
        factor_demanda = self._calcular_factor_demanda_moderado(
            demanda_reciente)

        # Factor 2: Competencia
        factor_competencia = self._calcular_factor_competencia(
            empresa, bien_nombre)

        # Factor 3: Condiciones macroeconómicas
        factor_macro = self._calcular_factor_macroeconomico()

        # Factor 4: Control de inflación
        factor_control_inflacion = self._calcular_control_inflacion(
            self.mercado)

        # Factor 5: Volatilidad reducida
        factor_volatilidad = random.uniform(
            0.98, 1.02)  # ±2% de ruido (reducido)

        # Combinar todos los factores con pesos balanceados
        multiplicador_total = (
            factor_stock * 0.25 +
            factor_demanda * 0.25 +
            factor_competencia * 0.20 +
            factor_macro * 0.10 +
            factor_control_inflacion * 0.15 +
            factor_volatilidad * 0.05
        )

        # Aplicar cambio controlado (máximo 8% por ciclo para controlar inflación)
        max_cambio = 0.08  # Reducido de 25% a 8%
        cambio_propuesto = (multiplicador_total - 1.0)
        cambio_final = max(-max_cambio, min(max_cambio, cambio_propuesto))

        nuevo_precio = precio_actual * (1 + cambio_final)

        # Asegurar precio mínimo viable
        precio_minimo = self._calcular_precio_minimo(empresa, bien_nombre)
        nuevo_precio = max(nuevo_precio, precio_minimo)

        return nuevo_precio

    def _calcular_factor_stock_agresivo(self, inventario_actual):
        """Factor de stock más agresivo para crear volatilidad"""
        if inventario_actual == 0:
            return 1.3  # Subir precio 30% si no hay stock
        elif inventario_actual < 5:
            return 1.15  # Subir precio 15% si stock bajo
        elif inventario_actual > 20:
            return 0.85  # Bajar precio 15% si mucho stock
        else:
            return 1.0

    def _calcular_factor_demanda_agresivo(self, demanda_reciente):
        """Factor de demanda más sensible"""
        if demanda_reciente > 15:
            return 1.2  # Alta demanda: subir precio 20%
        elif demanda_reciente > 10:
            return 1.1  # Demanda media-alta: subir precio 10%
        elif demanda_reciente < 3:
            return 0.9  # Baja demanda: bajar precio 10%
        else:
            return 1.0

    def _calcular_factor_inflacionario(self):
        """Nuevo factor que añade presión inflacionaria"""
        # Presión inflacionaria base del 2% anual (aproximadamente 0.15% por ciclo)
        if hasattr(self.mercado, 'fase_ciclo_economico'):
            if self.mercado.fase_ciclo_economico == 'expansion':
                return 1.003  # 0.3% por ciclo durante expansión
            elif self.mercado.fase_ciclo_economico == 'recesion':
                return 0.998  # -0.2% por ciclo durante recesión

        return 1.001  # 0.1% base

        # Agregar volatilidad aleatoria
        volatilidad = random.uniform(-self.volatilidad_mercado,
                                     self.volatilidad_mercado)
        nuevo_precio *= (1 + volatilidad)

        return round(nuevo_precio, 2)

    def _calcular_factor_stock(self, inventario_actual):
        """Factor basado en nivel de inventario"""
        if inventario_actual == 0:
            return 1.3  # Subir precios si no hay stock
        elif inventario_actual > 50:
            return 0.85  # Bajar precios si hay exceso
        elif inventario_actual > 20:
            return 0.95  # Ligera reducción
        else:
            return 1.1  # Ligero aumento si stock bajo

    def _calcular_factor_demanda(self, demanda_reciente):
        """Factor basado en demanda reciente"""
        if demanda_reciente == 0:
            return 0.8  # Reducir precios si no hay demanda
        elif demanda_reciente > 20:
            return 1.2  # Aumentar si alta demanda
        elif demanda_reciente > 10:
            return 1.1  # Ligero aumento
        else:
            return 0.95  # Ligera reducción

    def _calcular_factor_competencia(self, empresa, bien_nombre):
        """Factor basado en competencia de precios"""
        # Encontrar otras empresas que venden el mismo bien
        competidores = []
        for otra_empresa in self.mercado.getEmpresas():
            if otra_empresa != empresa and hasattr(otra_empresa, 'precios'):
                if bien_nombre in otra_empresa.precios:
                    competidores.append(otra_empresa.precios[bien_nombre])

        if not competidores:
            return 1.0  # Sin competencia, mantener precio

        precio_actual = empresa.precios.get(
            bien_nombre, self.precios_base.get(bien_nombre, 10))
        precio_promedio_competencia = sum(competidores) / len(competidores)

        # Si estoy por encima del promedio, presión para bajar
        ratio = precio_actual / precio_promedio_competencia

        if ratio > 1.2:  # 20% más caro que competencia
            return 0.9  # Presión para bajar
        elif ratio < 0.8:  # 20% más barato
            return 1.1  # Puede subir precio
        else:
            return 1.0  # Precio competitivo

    def _calcular_factor_macroeconomico(self):
        """Factor basado en condiciones macroeconómicas"""
        factor = 1.0

        # Inflación
        if self.mercado.inflacion_historica:
            inflacion_actual = self.mercado.inflacion_historica[-1]
            factor *= (1 + inflacion_actual * 0.5)  # 50% de pass-through

        # Crisis financiera
        if self.mercado.crisis_financiera_activa:
            factor *= 0.95  # Presión deflacionaria

        # Fase del ciclo económico
        if hasattr(self.mercado, 'fase_ciclo_economico'):
            if self.mercado.fase_ciclo_economico == 'expansion':
                factor *= 1.02
            elif self.mercado.fase_ciclo_economico == 'recesion':
                factor *= 0.98
            elif self.mercado.fase_ciclo_economico == 'depresion':
                factor *= 0.95

        return factor

    def _calcular_factor_costos(self, empresa, bien_nombre):
        """Factor basado en costos de producción"""
        if hasattr(empresa, 'costos_unitarios') and bien_nombre in empresa.costos_unitarios:
            costo_unitario = empresa.costos_unitarios[bien_nombre]
            precio_actual = empresa.precios.get(bien_nombre, 10)

            # Mantener margen mínimo del 20%
            precio_minimo_margen = costo_unitario * 1.2

            if precio_actual < precio_minimo_margen:
                return 1.15  # Necesita subir para mantener margen
            elif precio_actual > costo_unitario * 3:
                return 0.95  # Margen muy alto, puede reducir

        return 1.0

    def _calcular_factor_estacional(self, bien_nombre):
        """Factor estacional simplificado"""
        ciclo_actual = self.mercado.ciclo_actual

        # Diferentes bienes tienen diferentes patrones estacionales
        if bien_nombre in ['Cafe', 'Chocolate', 'Vino']:
            # Productos de temporada navideña (ciclo 12 = diciembre)
            if (ciclo_actual % 12) in [11, 0, 1]:  # Nov, Dic, Ene
                return 1.1
        elif bien_nombre in ['Ropa', 'Calzado']:
            # Temporada de cambio de estación
            if (ciclo_actual % 12) in [3, 4, 9, 10]:  # Primavera y otoño
                return 1.05

        return 1.0

    def _calcular_precio_minimo(self, empresa, bien_nombre):
        """Calcula el precio mínimo viable"""
        if hasattr(empresa, 'costos_unitarios') and bien_nombre in empresa.costos_unitarios:
            # 5% margen mínimo
            return empresa.costos_unitarios[bien_nombre] * 1.05
        else:
            # 50% del precio base
            return self.precios_base.get(bien_nombre, 1) * 0.5

    def ajustar_volatilidad_mercado(self):
        """Ajusta la volatilidad del mercado basada en condiciones"""
        volatilidad_base = 0.05

        # Aumentar volatilidad durante crisis
        if self.mercado.crisis_financiera_activa:
            volatilidad_base *= 2

        # Aumentar volatilidad si hay muchas transacciones (mercado activo)
        transacciones_recientes = len([t for t in self.mercado.transacciones
                                       if t.get('ciclo', 0) >= self.mercado.ciclo_actual - 5])

        if transacciones_recientes > 100:
            volatilidad_base *= 1.5
        elif transacciones_recientes < 20:
            volatilidad_base *= 0.7

        self.volatilidad_mercado = min(
            0.25, volatilidad_base)  # Máximo 25% volatilidad

    def aplicar_shock_precios(self, tipo_shock='aleatorio', intensidad=0.2):
        """Aplica un shock de precios al mercado"""
        print(
            f"💥 Aplicando shock de precios: {tipo_shock} (intensidad: {intensidad})")

        if tipo_shock == 'materias_primas':
            # Shock en bienes intermedios y básicos
            categorias_afectadas = ['intermedio', 'alimentos_basicos']
        elif tipo_shock == 'tecnologico':
            # Shock en tecnología (deflacionario)
            categorias_afectadas = ['tecnologia']
            intensidad = -abs(intensidad)  # Siempre negativo
        elif tipo_shock == 'energia':
            # Shock energético (afecta costos de transporte)
            categorias_afectadas = ['servicios', 'intermedio']
        else:
            # Shock aleatorio
            categorias_afectadas = list(self.elasticidades_categoria.keys())

        # Aplicar shock a precios base
        for bien_nombre, bien in self.mercado.bienes.items():
            if bien.categoria in categorias_afectadas:
                factor_shock = 1 + \
                    random.uniform(-abs(intensidad), abs(intensidad))
                self.precios_base[bien_nombre] *= factor_shock

                # Aplicar inmediatamente a empresas
                for empresa in self.mercado.getEmpresas():
                    if hasattr(empresa, 'precios') and bien_nombre in empresa.precios:
                        empresa.precios[bien_nombre] *= factor_shock

    def obtener_estadisticas_precios(self):
        """Retorna estadísticas del sistema de precios"""
        todos_precios = []
        cambios_precios = []

        for empresa in self.mercado.getEmpresas():
            if hasattr(empresa, 'precios'):
                todos_precios.extend(empresa.precios.values())

        if not todos_precios:
            return {}

        return {
            'precio_promedio': sum(todos_precios) / len(todos_precios),
            'precio_minimo': min(todos_precios),
            'precio_maximo': max(todos_precios),
            'num_productos_precios': len(todos_precios),
            'volatilidad_actual': self.volatilidad_mercado,
            'dispersion_precios': max(todos_precios) - min(todos_precios)
        }


def integrar_sistema_precios_dinamicos(mercado):
    """Función para integrar el sistema de precios dinámicos al mercado"""
    if not hasattr(mercado, 'sistema_precios'):
        mercado.sistema_precios = SistemaPreciosDinamicos(mercado)
        mercado.sistema_precios.inicializar_precios_base()
        print("✅ Sistema de precios dinámicos integrado")

    return mercado.sistema_precios


def actualizar_precios_mercado(mercado):
    """Actualiza todos los precios del mercado usando el sistema dinámico"""
    if not hasattr(mercado, 'sistema_precios'):
        integrar_sistema_precios_dinamicos(mercado)

    sistema = mercado.sistema_precios
    sistema.ajustar_volatilidad_mercado()

    precios_actualizados = 0

    for empresa in mercado.getEmpresas():
        if not hasattr(empresa, 'precios') or not hasattr(empresa, 'bienes'):
            continue

        for bien_nombre in empresa.precios.keys():
            # Obtener inventario actual
            inventario_actual = len(empresa.bienes.get(bien_nombre, []))

            # Calcular demanda reciente (simplificado)
            transacciones_bien = [t for t in mercado.transacciones[-20:]
                                  if t.get('bien') == bien_nombre and t.get('vendedor') == empresa.nombre]
            demanda_reciente = sum([t.get('cantidad', 0)
                                   for t in transacciones_bien])

            # Calcular nuevo precio
            nuevo_precio = sistema.calcular_precio_dinamico(
                empresa, bien_nombre, inventario_actual, demanda_reciente
            )

            empresa.precios[bien_nombre] = nuevo_precio
            precios_actualizados += 1

    return precios_actualizados


# Métodos auxiliares adicionales para SistemaPreciosDinamicos
def _calcular_factor_stock_moderado(self, inventario_actual):
    """Factor basado en stock con cambios moderados"""
    if inventario_actual > 50:
        return 0.96  # Reducción suave
    elif inventario_actual > 20:
        return 0.98  # Reducción mínima
    elif inventario_actual < 5:
        return 1.04  # Aumento moderado si stock muy bajo
    elif inventario_actual < 10:
        return 1.02  # Aumento suave
    else:
        return 1.0  # Precio estable


def _calcular_factor_demanda_moderado(self, demanda_reciente):
    """Factor basado en demanda con cambios moderados"""
    if demanda_reciente == 0:
        return 0.96  # Reducción suave si no hay demanda
    elif demanda_reciente > 20:
        return 1.04  # Aumento moderado si alta demanda
    elif demanda_reciente > 10:
        return 1.02  # Aumento suave
    else:
        return 0.99  # Reducción mínima


def _calcular_control_inflacion(self, mercado):
    """Factor para controlar inflación excesiva"""
    if not mercado.inflacion_historica:
        return 1.0

    inflacion_reciente = mercado.inflacion_historica[-1]

    # Si inflación es muy alta, aplicar presión deflacionaria
    if inflacion_reciente > 0.15:  # Más de 15%
        return 0.95  # Presión para bajar precios
    elif inflacion_reciente > 0.08:  # Más de 8%
        return 0.98  # Presión suave para bajar
    elif inflacion_reciente < -0.02:  # Deflación
        return 1.02  # Presión suave para subir
    else:
        return 1.0  # Estable


# Agregar métodos a la clase
SistemaPreciosDinamicos._calcular_factor_stock_moderado = _calcular_factor_stock_moderado
SistemaPreciosDinamicos._calcular_factor_demanda_moderado = _calcular_factor_demanda_moderado
SistemaPreciosDinamicos._calcular_control_inflacion = _calcular_control_inflacion
