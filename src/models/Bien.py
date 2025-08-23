import random
from ..config.ConfigEconomica import ConfigEconomica

class Bien:
    def __init__(self, nombre, categoria=None):
        self.nombre = nombre
        categorias_map = (
            getattr(ConfigEconomica, 'CATEGORIAS_BIENES_MAP', None)
            or getattr(ConfigEconomica, 'categorias_bienes_map', None)
        )
        if not categoria and isinstance(categorias_map, dict):
            categoria = categorias_map.get(nombre, 'servicios')
        self.categoria = categoria or 'servicios'
        
        # Elasticidades basadas en la categoría del bien
        mapa_precio = getattr(ConfigEconomica, 'elasticidades_precio_map', {})
        mapa_ingreso = getattr(ConfigEconomica, 'elasticidades_ingreso_map', {})
        self.elasticidad_precio = mapa_precio.get(self.categoria, -0.8)
        self.elasticidad_ingreso = mapa_ingreso.get(self.categoria, 1.0)
        
        # Características del bien
        self.es_bien_basico = self.categoria in ['alimentos_basicos', 'combustibles']
        self.es_bien_lujo = self.categoria in ['alimentos_lujo', 'bienes_duraderos']
        self.es_duradero = self.categoria == 'bienes_duraderos'
        self.perecedero = self.categoria.startswith('alimentos')
        
        # Factores de temporada y estacionalidad
        self.factor_estacional = self._calcular_estacionalidad()
        
        # Sustitos y complementos (simplificado)
        self.sustitutos = self._definir_sustitutos()
        self.complementos = self._definir_complementos()
        
    def _calcular_estacionalidad(self):
        """Calcula factores estacionales para ciertos bienes"""
        factores_estacionales = {
            'Cafe': [1.2, 1.1, 1.0, 0.9, 0.8, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4],  # Mayor demanda en invierno
            'Carne': [1.3, 1.1, 1.0, 1.0, 1.1, 1.2, 1.3, 1.2, 1.0, 1.0, 1.2, 1.4],  # Fiestas y asados
            'Aceite': [1.0] * 12,  # Demanda constante
        }
        return factores_estacionales.get(self.nombre, [1.0] * 12)
        
    def _definir_sustitutos(self):
        """Define bienes sustitutos"""
        sustitutos = {
            'Arroz': ['Papa', 'Pan'],
            'Papa': ['Arroz', 'Pan'], 
            'Pan': ['Arroz', 'Papa'],
            'Carne': ['Pollo'],
            'Pollo': ['Carne', 'Huevos'],
            'Cafe': ['Azucar'],  # Simplificado
            'Leche': [],
            'Huevos': ['Pollo'],
            'Aceite': [],
            'Sal': [],
            'Azucar': ['Cafe']
        }
        return sustitutos.get(self.nombre, [])
        
    def _definir_complementos(self):
        """Define bienes complementarios"""
        complementos = {
            'Pan': ['Aceite'],
            'Arroz': ['Aceite', 'Sal'],
            'Papa': ['Aceite', 'Sal'],
            'Carne': ['Sal'],
            'Pollo': ['Sal'],
            'Cafe': ['Azucar'],  
            'Huevos': ['Aceite', 'Sal']
        }
        return complementos.get(self.nombre, [])
        
    def calcular_demanda_base(self, poblacion, ingreso_promedio):
        """Calcula demanda base considerando elasticidades"""
        # Demanda base por población
        demanda_poblacional = poblacion * random.uniform(0.8, 1.2)
        
        # Efecto del ingreso
        if self.elasticidad_ingreso > 0:
            factor_ingreso = (ingreso_promedio / 5000) ** self.elasticidad_ingreso
        else:
            factor_ingreso = 1
            
        return max(1, int(demanda_poblacional * factor_ingreso))
        
    def calcular_factor_precio(self, precio_actual, precio_referencia):
        """Calcula el factor de demanda basado en cambio de precios"""
        if precio_referencia <= 0:
            return 1.0
            
        cambio_precio = (precio_actual - precio_referencia) / precio_referencia
        factor_precio = (1 + cambio_precio) ** self.elasticidad_precio
        
        return max(0.1, min(3.0, factor_precio))  # Limitar entre 0.1 y 3.0
        
    def obtener_factor_estacional(self, mes):
        """Obtiene el factor estacional para un mes dado (0-11)"""
        mes_idx = mes % 12
        return self.factor_estacional[mes_idx]
    
    def __str__(self):
        return f"{self.nombre} (Categoría: {self.categoria}, Elast.Precio: {self.elasticidad_precio:.2f}, Elast.Ingreso: {self.elasticidad_ingreso:.2f})"