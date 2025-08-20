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
    
    # Inflación y precios - CONFIGURACIÓN MEJORADA PARA CONTROL FINO
    INFLACION_OBJETIVO_ANUAL = 0.03    # 3% anual (target central)
    INFLACION_OBJETIVO_CICLO = 0.0025  # ~3% anual / 12 ciclos = 0.25% por ciclo
    INFLACION_TOLERANCIA = 0.01        # ±1% de tolerancia (banda 2-4%)
    FACTOR_AJUSTE_PRECIO_MAX = 0.015   # Máximo 1.5% de cambio por ciclo (más restrictivo)
    PRECIO_BASE_MIN = 5.0
    PRECIO_BASE_MAX = 50.0
    
    # NUEVO: Parámetros para política monetaria óptima
    TASA_INTERES_NEUTRAL = 0.03        # 3% tasa neutral real
    TASA_INTERES_MINIMA = 0.001        # 0.1% mínimo (ZLB)
    TASA_INTERES_MAXIMA = 0.25         # 25% máximo de emergencia
    TRANSMISION_MONETARIA_NORMAL = 0.7  # 70% de transmisión normal
    TRANSMISION_MONETARIA_EMERGENCIA = 0.9  # 90% en emergencias
    
    # Elasticidades por tipo de bien
    ELASTICIDADES_PRECIO = {
        'alimentos_basicos': -0.3,  # Inelástico (necesidades básicas)
        'alimentos_lujo': -1.2,    # Elástico
        'servicios': -0.8,
        'servicios_lujo': -1.5,
        'bienes_duraderos': -1.5,
        'combustibles': -0.2,
        'tecnologia': -1.8,        # Muy elástico
        'capital': -0.5,           # Poco elástico
        'intermedio': -0.4,        # Poco elástico
        'financiero': -1.0         # Moderadamente elástico
    }
    
    ELASTICIDADES_INGRESO = {
        'alimentos_basicos': 0.5,   # Bien normal inferior
        'alimentos_lujo': 1.5,     # Bien normal superior
        'servicios': 1.2,
        'servicios_lujo': 2.2,     # Bien de lujo
        'bienes_duraderos': 2.0,   # Bien de lujo
        'combustibles': 0.8,
        'tecnologia': 2.5,         # Bien de lujo alto
        'capital': 1.5,            # Bien de inversión
        'intermedio': 1.0,         # Neutral
        'financiero': 1.8          # Bien superior
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
    # Sostenibilidad ambiental
    RECURSOS_NATURALES_INICIALES = 1000000
    FACTORES_AGOTAMIENTO_RECURSOS = {
        'alimentos_basicos': 1.0,
        'alimentos_lujo': 1.5,
        'servicios': 0.5,
        'bienes_duraderos': 2.0,
        'combustibles': 2.5
    }
    COEFICIENTES_CONTAMINACION = {
        'alimentos_basicos': 0.3,
        'alimentos_lujo': 0.7,
        'servicios': 0.2,
        'bienes_duraderos': 1.0,
        'combustibles': 1.8
    }
    IMPUESTO_CARBONO = 5  # Unidad monetaria por unidad de emisión
    LIMITE_EXTRACCION_RECURSOS = 0.1  # 10% de recursos restantes como umbral crítico