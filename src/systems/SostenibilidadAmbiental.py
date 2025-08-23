"""\
Sistema de sostenibilidad ambiental para el simulador económico.
Lleva registro de recursos naturales disponibles y de las emisiones
asociadas a la producción de cada empresa.
"""

from ..config.ConfigEconomica import ConfigEconomica


class SostenibilidadAmbiental:
    """Gestiona recursos y contaminación ambiental"""

    def __init__(self):
        # Recursos naturales globales disponibles
        self.recursos_disponibles = ConfigEconomica.RECURSOS_NATURALES_INICIALES

        # Registros de impacto por empresa
        self.emisiones_empresas = {}
        self.contaminacion_empresas = {}

    def registrar_produccion(self, empresa, bien, cantidad, factor_emision=1.0):
        """Registra el uso de recursos y emisiones generadas por una producción.

        Parameters
        ----------
        empresa: str
            Nombre de la empresa que produce.
        bien: str
            Bien producido.
        cantidad: int
            Cantidad producida.
        factor_emision: float
            Factor multiplicador de emisiones (tecnología limpia).

        Returns
        -------
        tuple (cantidad_aceptada, emisiones_generadas)
        """
        categorias_map = getattr(ConfigEconomica, 'CATEGORIAS_BIENES_MAP', None)
        if isinstance(categorias_map, dict):
            categoria = categorias_map.get(bien, 'servicios')
        else:
            categoria = 'servicios'
        factores_map = getattr(ConfigEconomica, 'factores_agotamiento_recursos_map', {})
        consumo_unitario = factores_map.get(categoria, 0)

        # Determinar la cantidad que puede producirse con los recursos restantes
        max_producible = cantidad
        if consumo_unitario > 0:
            max_producible = min(cantidad, int(self.recursos_disponibles / consumo_unitario))

        if max_producible <= 0:
            return 0, 0

        # Consumir recursos
        consumo_total = consumo_unitario * max_producible
        self.recursos_disponibles = max(0, self.recursos_disponibles - consumo_total)

        # Calcular emisiones y contaminación
        coef_map = getattr(ConfigEconomica, 'coeficientes_contaminacion_map', {})
        coeficiente = coef_map.get(categoria, 0)
        emisiones = coeficiente * max_producible * factor_emision
        self.emisiones_empresas[empresa] = self.emisiones_empresas.get(empresa, 0) + emisiones
        self.contaminacion_empresas[empresa] = self.contaminacion_empresas.get(empresa, 0) + (
            coeficiente * max_producible
        )
        return max_producible, emisiones

    def obtener_indicadores(self):
        """Devuelve indicadores agregados del estado ambiental"""
        emisiones_totales = sum(self.emisiones_empresas.values())
        contaminacion_total = sum(self.contaminacion_empresas.values())
        return {
            'recursos_disponibles': self.recursos_disponibles,
            'emisiones_totales': emisiones_totales,
            'contaminacion_total': contaminacion_total,
        }
