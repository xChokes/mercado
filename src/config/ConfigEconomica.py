"""
Configuración económica global para el ecosistema de mercado
Contiene constantes económicas fundamentales y parámetros de simulación
"""

class ConfigEconomica:
    # Parámetros monetarios
    DINERO_INICIAL_CONSUMIDOR_MIN = 10000
    DINERO_INICIAL_CONSUMIDOR_MAX = 50000
    DINERO_INICIAL_EMPRESA_MIN = 100000
    DINERO_INICIAL_EMPRESA_MAX = 500000
    DINERO_INICIAL_EMPRESA_PRODUCTORA_MIN = 500000
    DINERO_INICIAL_EMPRESA_PRODUCTORA_MAX = 2000000
    
    # Salarios y empleo
    SALARIO_BASE_MIN = 2000
    SALARIO_BASE_MAX = 8000
    TASA_DESEMPLEO_OBJETIVO = 0.05  # 5%
    SUBSIDIO_DESEMPLEO = 1500
    
    # Inflación y precios
    INFLACION_MENSUAL_OBJETIVO = 0.02  # 2% mensual
    FACTOR_AJUSTE_PRECIO_MAX = 0.10  # Máximo 10% de cambio por ciclo
    PRECIO_BASE_MIN = 5.0
    PRECIO_BASE_MAX = 50.0
    
    # Elasticidades por tipo de bien
    ELASTICIDADES_PRECIO = {
        'alimentos_basicos': -0.3,  # Inelástico (necesidades básicas)
        'alimentos_lujo': -1.2,    # Elástico
        'servicios': -0.8,
        'bienes_duraderos': -1.5,
        'combustibles': -0.2
    }
    
    ELASTICIDADES_INGRESO = {
        'alimentos_basicos': 0.5,   # Bien normal inferior
        'alimentos_lujo': 1.5,     # Bien normal superior
        'servicios': 1.2,
        'bienes_duraderos': 2.0,   # Bien de lujo
        'combustibles': 0.8
    }
    
    # Tipos de bienes por categoría
    CATEGORIAS_BIENES = {
        'Arroz': 'alimentos_basicos',
        'Papa': 'alimentos_basicos', 
        'Pan': 'alimentos_basicos',
        'Leche': 'alimentos_basicos',
        'Sal': 'alimentos_basicos',
        'Carne': 'alimentos_lujo',
        'Pollo': 'alimentos_lujo',
        'Huevos': 'alimentos_lujo',
        'Cafe': 'alimentos_lujo',
        'Aceite': 'alimentos_basicos',
        'Azucar': 'alimentos_basicos'
    }
    
    # Factores de producción
    COSTO_PRODUCCION_BASE_MIN = 5.0
    COSTO_PRODUCCION_BASE_MAX = 25.0
    MARGEN_GANANCIA_MIN = 0.20  # 20%
    MARGEN_GANANCIA_MAX = 0.80  # 80%
    
    # Capacidad de producción
    PRODUCCION_BASE_MIN = 50
    PRODUCCION_BASE_MAX = 200
    FACTOR_ECONOMIA_ESCALA = 0.85  # Costos reducen con mayor producción
    
    # Mercado financiero
    DIVIDEND_YIELD_MIN = 0.02   # 2%
    DIVIDEND_YIELD_MAX = 0.08   # 8%
    VOLATILIDAD_ACCIONES = 0.15  # 15%
    TASA_INTERES_BASE = 0.05    # 5%
    
    # Factores macroeconómicos
    CICLO_ECONOMICO_DURACION = 40  # ciclos
    AMPLITUD_CICLO_ECONOMICO = 0.20  # 20% de variación
    CRECIMIENTO_POBLACION_ANUAL = 0.02  # 2%
    
    # Preferencias de consumo
    UTILIDAD_MARGINAL_DECRECIENTE = 0.85
    FACTOR_SACIEDAD = 0.90
    PREFERENCIA_VARIEDAD = 0.15  # Tendencia a diversificar compras
    
    # Comportamiento empresarial
    FACTOR_REINVERSION = 0.30    # 30% de ganancias se reinvierten
    UMBRAL_EXPANSION = 0.80      # Expande si utiliza >80% de capacidad
    UMBRAL_CONTRACCION = 0.30    # Contrae si utiliza <30% de capacidad
    
    # Gobierno y regulación
    TASA_IMPUESTOS = 0.25        # 25% de impuestos sobre ganancias
    GASTO_PUBLICO_PIB = 0.20     # Gasto público como % del PIB
    POLITICA_MONETARIA_AGRESIVA = False

    # Comercio internacional
    ARANCEL_BASE = 0.05  # Arancel general del 5%
    TIPOS_CAMBIO_INICIALES = {
        ('USD', 'EUR'): 0.90,
        ('EUR', 'USD'): 1.10
    }
    COSTO_TRANSPORTE_BASE = 0.02  # 2% del valor comerciado
