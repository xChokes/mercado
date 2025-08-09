"""Sistema de comercio internacional
====================================

Define estructuras básicas para manejar múltiples economías con
monedas distintas y registrar la balanza comercial entre países.
"""

from dataclasses import dataclass


@dataclass
class Pais:
    """Representa un país dentro del sistema económico"""
    nombre: str
    moneda: str
    arancel_base: float = 0.0

    def __post_init__(self):
        self.aranceles = {}  # {pais: tasa}
        self.balanza_comercial = 0.0
        self.mercado = None

    def establecer_arancel(self, pais, tasa):
        """Define un arancel para comercio con otro país"""
        self.aranceles[pais] = tasa

    def obtener_arancel(self, pais):
        """Retorna el arancel aplicable a un país"""
        return self.aranceles.get(pais, self.arancel_base)


class TipoCambio:
    """Gestiona tipos de cambio entre monedas"""

    def __init__(self, tasas_iniciales):
        # tasas_iniciales: {('USD','EUR'): 0.9, ('EUR','USD'): 1.1}
        self.tasas = dict(tasas_iniciales)

    def convertir(self, monto, moneda_origen, moneda_destino):
        """Convierte un monto entre dos monedas"""
        if moneda_origen == moneda_destino:
            return monto
        tasa = self.tasas.get((moneda_origen, moneda_destino))
        if tasa is None:
            raise ValueError(
                f"Tipo de cambio no definido de {moneda_origen} a {moneda_destino}")
        return monto * tasa

    def actualizar_tasa(self, moneda_origen, moneda_destino, nueva_tasa):
        """Actualiza una tasa de cambio"""
        self.tasas[(moneda_origen, moneda_destino)] = nueva_tasa
