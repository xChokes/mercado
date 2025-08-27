"""
Sistema de Bienes Hiperrealistas con Características Avanzadas
==============================================================

Expande las características de los bienes para hacerlos más realistas:
- Propiedades físicas y de calidad
- Atributos emocionales y sociales
- Ciclo de vida y degradación
- Efectos de red y tendencias
- Impacto ambiental y sostenibilidad
"""

import random
import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
import math
from datetime import datetime, timedelta


class TipoBien(Enum):
    """Clasificación detallada de tipos de bienes"""
    ALIMENTO_BASICO = "alimento_basico"
    ALIMENTO_PREMIUM = "alimento_premium"
    BEBIDA = "bebida"
    ROPA_BASICA = "ropa_basica"
    ROPA_MODA = "ropa_moda"
    ELECTRONICO_BASICO = "electronico_basico"
    ELECTRONICO_PREMIUM = "electronico_premium"
    HOGAR_BASICO = "hogar_basico"
    HOGAR_LUJO = "hogar_lujo"
    TRANSPORTE = "transporte"
    ENTRETENIMIENTO = "entretenimiento"
    EDUCACION = "educacion"
    SALUD = "salud"
    SERVICIO_BASICO = "servicio_basico"
    SERVICIO_PREMIUM = "servicio_premium"


class CalidadBien(Enum):
    """Niveles de calidad de los bienes"""
    MUY_BAJA = 1
    BAJA = 2
    MEDIA = 3
    ALTA = 4
    PREMIUM = 5
    LUJO = 6


class EstadoVida(Enum):
    """Estado en el ciclo de vida del bien"""
    NUEVO = "nuevo"
    USADO_COMO_NUEVO = "usado_como_nuevo"
    USADO_BUENO = "usado_bueno"
    USADO_REGULAR = "usado_regular"
    DETERIORADO = "deteriorado"
    DEFECTUOSO = "defectuoso"


@dataclass
class PropiedadesFisicas:
    """Propiedades físicas del bien"""
    peso: float = 1.0  # kg
    volumen: float = 1.0  # litros
    durabilidad_base: float = 1.0  # años de vida útil
    fragilidad: float = 0.5  # 0.0 (muy robusto) a 1.0 (muy frágil)
    transportabilidad: float = 0.5  # 0.0 (difícil) a 1.0 (fácil)
    
    # Factores ambientales
    sensible_temperatura: bool = False
    sensible_humedad: bool = False
    perecedero: bool = False
    dias_caducidad: Optional[int] = None


@dataclass
class AtributosCalidad:
    """Atributos de calidad del bien"""
    nivel_calidad: CalidadBien = CalidadBien.MEDIA
    marca_prestigio: float = 0.5  # 0.0 a 1.0
    innovacion_tecnologica: float = 0.5  # 0.0 a 1.0
    diseño_estetico: float = 0.5  # 0.0 a 1.0
    funcionalidad: float = 0.5  # 0.0 a 1.0
    
    # Certificaciones y garantías
    certificaciones: Set[str] = field(default_factory=set)
    garantia_meses: int = 12
    servicio_postventa: float = 0.5  # 0.0 a 1.0


@dataclass
class ImpactoEmocional:
    """Impacto emocional y psicológico del bien"""
    factor_estatus: float = 0.5  # Cuánto estatus social confiere
    factor_placer: float = 0.5  # Cuánto placer/satisfacción da
    factor_seguridad: float = 0.5  # Cuánta seguridad/tranquilidad da
    factor_autoestima: float = 0.5  # Impacto en autoestima
    
    # Asociaciones emocionales
    evoca_nostalgia: bool = False
    es_aspiracional: bool = False
    genera_adiccion: bool = False
    es_terapeutico: bool = False


@dataclass
class FactoresSociales:
    """Factores sociales y de red del bien"""
    popularidad_general: float = 0.5  # 0.0 a 1.0
    tendencia_crecimiento: float = 0.0  # -1.0 (decae) a 1.0 (crece)
    factor_viral: float = 0.0  # Potencial de volverse viral
    influencia_celebridades: float = 0.0  # Influencia de celebridades
    
    # Efectos de red
    valor_red_social: float = 0.0  # Valor que aumenta con más usuarios
    exclusividad: float = 0.5  # 0.0 (común) a 1.0 (exclusivo)
    
    # Demografía objetivo
    grupo_edad_objetivo: List[Tuple[int, int]] = field(default_factory=list)
    genero_objetivo: Optional[str] = None
    nivel_socioeconomico_objetivo: List[str] = field(default_factory=list)


@dataclass
class ImpactoAmbiental:
    """Impacto ambiental del bien"""
    huella_carbono: float = 1.0  # kg CO2 equivalente
    recursos_agua: float = 1.0  # litros de agua usados
    materiales_reciclables: float = 0.5  # 0.0 a 1.0
    biodegradable: bool = False
    
    # Sostenibilidad
    origen_sostenible: bool = False
    comercio_justo: bool = False
    produccion_local: bool = False
    empaque_sostenible: bool = False
    
    # Puntuación ESG
    puntuacion_ambiental: float = 0.5  # 0.0 a 1.0
    puntuacion_social: float = 0.5
    puntuacion_gobernanza: float = 0.5


@dataclass
class EconomicasBien:
    """Características económicas del bien"""
    costo_produccion_base: float = 10.0
    margen_minimo: float = 0.1  # 10%
    margen_sugerido: float = 0.3  # 30%
    elasticidad_precio_especifica: float = -1.0
    elasticidad_ingreso_especifica: float = 1.0
    
    # Costos asociados
    costo_almacenamiento: float = 0.1  # por unidad por día
    costo_transporte: float = 1.0  # por unidad
    costo_marketing: float = 0.5  # por unidad
    
    # Economías de escala
    factor_escala: float = 0.9  # Reducción de costos con volumen
    volumen_optimo: int = 1000  # Unidades para economía de escala


class BienHiperrealista:
    """Clase expandida para bienes con características hiperrealistas"""
    
    def __init__(self, nombre: str, tipo_bien: TipoBien, categoria: str = None):
        self.nombre = nombre
        self.tipo_bien = tipo_bien
        self.categoria = categoria or self._inferir_categoria(tipo_bien)
        
        # Características principales
        self.propiedades_fisicas = self._generar_propiedades_fisicas()
        self.atributos_calidad = self._generar_atributos_calidad()
        self.impacto_emocional = self._generar_impacto_emocional()
        self.factores_sociales = self._generar_factores_sociales()
        self.impacto_ambiental = self._generar_impacto_ambiental()
        self.economicas = self._generar_economicas()
        
        # Estado dinámico
        self.estado_vida = EstadoVida.NUEVO
        self.fecha_fabricacion = datetime.now()
        self.fecha_caducidad = self._calcular_fecha_caducidad()
        self.desgaste_actual = 0.0  # 0.0 (nuevo) a 1.0 (totalmente desgastado)
        
        # Historial y métricas
        self.historial_precios: List[Tuple[datetime, float]] = []
        self.ventas_totales = 0
        self.valoraciones_usuarios: List[float] = []
        self.quejas_registradas = 0
        
        # Bienes relacionados
        self.sustitutos: Set[str] = set()
        self.complementos: Set[str] = set()
        self.productos_bundle: Set[str] = set()
        
        # Factores de temporada y eventos
        self.factor_estacional_mensual = self._generar_factores_estacionales()
        self.eventos_especiales = self._generar_eventos_especiales()
        
        # Inicializar valores derivados
        self._actualizar_valores_derivados()
    
    def _inferir_categoria(self, tipo_bien: TipoBien) -> str:
        """Infiere la categoría basándose en el tipo de bien"""
        mapeo_categorias = {
            TipoBien.ALIMENTO_BASICO: "alimentos_basicos",
            TipoBien.ALIMENTO_PREMIUM: "alimentos_lujo",
            TipoBien.BEBIDA: "alimentos_lujo",
            TipoBien.ROPA_BASICA: "servicios",
            TipoBien.ROPA_MODA: "bienes_duraderos",
            TipoBien.ELECTRONICO_BASICO: "bienes_duraderos",
            TipoBien.ELECTRONICO_PREMIUM: "bienes_duraderos",
            TipoBien.HOGAR_BASICO: "servicios",
            TipoBien.HOGAR_LUJO: "bienes_duraderos",
            TipoBien.TRANSPORTE: "servicios",
            TipoBien.ENTRETENIMIENTO: "servicios",
            TipoBien.EDUCACION: "servicios",
            TipoBien.SALUD: "servicios",
            TipoBien.SERVICIO_BASICO: "servicios",
            TipoBien.SERVICIO_PREMIUM: "servicios_lujo"
        }
        return mapeo_categorias.get(tipo_bien, "servicios")
    
    def _generar_propiedades_fisicas(self) -> PropiedadesFisicas:
        """Genera propiedades físicas realistas según el tipo de bien"""
        
        # Plantillas por tipo de bien
        plantillas = {
            TipoBien.ALIMENTO_BASICO: {
                'peso': (0.1, 2.0), 'volumen': (0.1, 2.0),
                'durabilidad_base': (0.01, 2.0), 'fragilidad': (0.3, 0.8),
                'transportabilidad': (0.7, 0.9), 'perecedero': True,
                'sensible_temperatura': True, 'dias_caducidad': (7, 365)
            },
            TipoBien.ALIMENTO_PREMIUM: {
                'peso': (0.1, 1.0), 'volumen': (0.1, 1.0),
                'durabilidad_base': (0.01, 1.0), 'fragilidad': (0.5, 0.9),
                'transportabilidad': (0.5, 0.8), 'perecedero': True,
                'sensible_temperatura': True, 'dias_caducidad': (3, 90)
            },
            TipoBien.ELECTRONICO_BASICO: {
                'peso': (0.5, 5.0), 'volumen': (0.5, 5.0),
                'durabilidad_base': (2.0, 5.0), 'fragilidad': (0.6, 0.8),
                'transportabilidad': (0.6, 0.8), 'perecedero': False,
                'sensible_humedad': True
            },
            TipoBien.ELECTRONICO_PREMIUM: {
                'peso': (0.2, 3.0), 'volumen': (0.2, 3.0),
                'durabilidad_base': (3.0, 8.0), 'fragilidad': (0.7, 0.9),
                'transportabilidad': (0.8, 0.9), 'perecedero': False,
                'sensible_humedad': True
            },
            TipoBien.ROPA_BASICA: {
                'peso': (0.1, 1.0), 'volumen': (0.5, 2.0),
                'durabilidad_base': (1.0, 3.0), 'fragilidad': (0.2, 0.5),
                'transportabilidad': (0.9, 1.0), 'perecedero': False
            },
            TipoBien.ROPA_MODA: {
                'peso': (0.1, 0.8), 'volumen': (0.3, 1.5),
                'durabilidad_base': (0.5, 2.0), 'fragilidad': (0.4, 0.7),
                'transportabilidad': (0.9, 1.0), 'perecedero': False
            }
        }
        
        # Usar plantilla específica o valores por defecto
        plantilla = plantillas.get(self.tipo_bien, {
            'peso': (0.5, 2.0), 'volumen': (0.5, 2.0),
            'durabilidad_base': (1.0, 3.0), 'fragilidad': (0.3, 0.7),
            'transportabilidad': (0.5, 0.8), 'perecedero': False
        })
        
        props = PropiedadesFisicas()
        
        # Generar valores aleatorios dentro de rangos
        props.peso = random.uniform(*plantilla['peso'])
        props.volumen = random.uniform(*plantilla['volumen'])
        props.durabilidad_base = random.uniform(*plantilla['durabilidad_base'])
        props.fragilidad = random.uniform(*plantilla['fragilidad'])
        props.transportabilidad = random.uniform(*plantilla['transportabilidad'])
        
        # Propiedades booleanas
        props.perecedero = plantilla.get('perecedero', False)
        props.sensible_temperatura = plantilla.get('sensible_temperatura', False)
        props.sensible_humedad = plantilla.get('sensible_humedad', False)
        
        # Días de caducidad
        if props.perecedero and 'dias_caducidad' in plantilla:
            min_dias, max_dias = plantilla['dias_caducidad']
            props.dias_caducidad = random.randint(min_dias, max_dias)
        
        return props
    
    def _generar_atributos_calidad(self) -> AtributosCalidad:
        """Genera atributos de calidad según el tipo de bien"""
        
        attrs = AtributosCalidad()
        
        # Mapeo de calidad base por tipo
        calidad_base = {
            TipoBien.ALIMENTO_BASICO: CalidadBien.MEDIA,
            TipoBien.ALIMENTO_PREMIUM: CalidadBien.ALTA,
            TipoBien.ELECTRONICO_BASICO: CalidadBien.MEDIA,
            TipoBien.ELECTRONICO_PREMIUM: CalidadBien.PREMIUM,
            TipoBien.ROPA_BASICA: CalidadBien.MEDIA,
            TipoBien.ROPA_MODA: CalidadBien.ALTA,
            TipoBien.HOGAR_LUJO: CalidadBien.LUJO,
            TipoBien.SERVICIO_PREMIUM: CalidadBien.PREMIUM
        }
        
        attrs.nivel_calidad = calidad_base.get(self.tipo_bien, CalidadBien.MEDIA)
        
        # Ajustar otros atributos según la calidad
        base_quality = attrs.nivel_calidad.value / 6.0  # Normalizar 1-6 a 0-1
        
        attrs.marca_prestigio = min(1.0, base_quality + random.uniform(-0.2, 0.3))
        attrs.innovacion_tecnologica = random.uniform(0.2, 0.8) if self.tipo_bien.name.startswith('ELECTRONICO') else random.uniform(0.1, 0.5)
        attrs.diseño_estetico = random.uniform(0.3, 0.9) if 'MODA' in self.tipo_bien.name or 'LUJO' in self.tipo_bien.name else random.uniform(0.2, 0.6)
        attrs.funcionalidad = min(1.0, base_quality + random.uniform(-0.1, 0.2))
        
        # Certificaciones según tipo
        certificaciones_posibles = {
            TipoBien.ALIMENTO_BASICO: ['FDA', 'ORGANIC', 'NON_GMO'],
            TipoBien.ALIMENTO_PREMIUM: ['ORGANIC', 'GOURMET', 'ARTISANAL'],
            TipoBien.ELECTRONICO_BASICO: ['CE', 'FCC'],
            TipoBien.ELECTRONICO_PREMIUM: ['CE', 'FCC', 'ENERGY_STAR', 'PREMIUM_DESIGN'],
            TipoBien.ROPA_MODA: ['FASHION_FORWARD', 'DESIGNER', 'LIMITED_EDITION'],
            TipoBien.HOGAR_LUJO: ['LUXURY', 'HANDCRAFTED', 'DESIGNER']
        }
        
        if self.tipo_bien in certificaciones_posibles:
            # Seleccionar 1-3 certificaciones aleatoriamente
            certs = certificaciones_posibles[self.tipo_bien]
            num_certs = random.randint(1, min(3, len(certs)))
            attrs.certificaciones = set(random.sample(certs, num_certs))
        
        # Garantía según tipo y calidad
        garantia_base = {
            TipoBien.ALIMENTO_BASICO: 0,
            TipoBien.ALIMENTO_PREMIUM: 0,
            TipoBien.ELECTRONICO_BASICO: 12,
            TipoBien.ELECTRONICO_PREMIUM: 24,
            TipoBien.ROPA_BASICA: 3,
            TipoBien.ROPA_MODA: 6,
            TipoBien.HOGAR_BASICO: 6,
            TipoBien.HOGAR_LUJO: 24
        }
        
        attrs.garantia_meses = garantia_base.get(self.tipo_bien, 12)
        attrs.servicio_postventa = min(1.0, base_quality + random.uniform(0.0, 0.3))
        
        return attrs
    
    def _generar_impacto_emocional(self) -> ImpactoEmocional:
        """Genera impacto emocional según tipo de bien"""
        
        impact = ImpactoEmocional()
        
        # Factores base por tipo
        factores_tipo = {
            TipoBien.ALIMENTO_BASICO: {
                'estatus': 0.2, 'placer': 0.6, 'seguridad': 0.8, 'autoestima': 0.3
            },
            TipoBien.ALIMENTO_PREMIUM: {
                'estatus': 0.6, 'placer': 0.8, 'seguridad': 0.7, 'autoestima': 0.5
            },
            TipoBien.ELECTRONICO_PREMIUM: {
                'estatus': 0.8, 'placer': 0.7, 'seguridad': 0.5, 'autoestima': 0.7
            },
            TipoBien.ROPA_MODA: {
                'estatus': 0.9, 'placer': 0.7, 'seguridad': 0.4, 'autoestima': 0.8
            },
            TipoBien.HOGAR_LUJO: {
                'estatus': 0.9, 'placer': 0.6, 'seguridad': 0.7, 'autoestima': 0.7
            },
            TipoBien.ENTRETENIMIENTO: {
                'estatus': 0.5, 'placer': 0.9, 'seguridad': 0.3, 'autoestima': 0.4
            },
            TipoBien.SALUD: {
                'estatus': 0.3, 'placer': 0.4, 'seguridad': 0.9, 'autoestima': 0.6
            }
        }
        
        factores = factores_tipo.get(self.tipo_bien, {
            'estatus': 0.5, 'placer': 0.5, 'seguridad': 0.5, 'autoestima': 0.5
        })
        
        # Aplicar variación aleatoria
        impact.factor_estatus = max(0.0, min(1.0, factores['estatus'] + random.uniform(-0.2, 0.2)))
        impact.factor_placer = max(0.0, min(1.0, factores['placer'] + random.uniform(-0.2, 0.2)))
        impact.factor_seguridad = max(0.0, min(1.0, factores['seguridad'] + random.uniform(-0.2, 0.2)))
        impact.factor_autoestima = max(0.0, min(1.0, factores['autoestima'] + random.uniform(-0.2, 0.2)))
        
        # Características especiales
        impact.evoca_nostalgia = self.tipo_bien in [TipoBien.ALIMENTO_BASICO, TipoBien.ENTRETENIMIENTO] and random.random() < 0.3
        impact.es_aspiracional = self.tipo_bien in [TipoBien.ELECTRONICO_PREMIUM, TipoBien.ROPA_MODA, TipoBien.HOGAR_LUJO] and random.random() < 0.7
        impact.genera_adiccion = self.tipo_bien in [TipoBien.ENTRETENIMIENTO, TipoBien.ALIMENTO_PREMIUM] and random.random() < 0.2
        impact.es_terapeutico = self.tipo_bien in [TipoBien.SALUD, TipoBien.ENTRETENIMIENTO] and random.random() < 0.4
        
        return impact
    
    def _generar_factores_sociales(self) -> FactoresSociales:
        """Genera factores sociales realistas"""
        
        social = FactoresSociales()
        
        # Popularidad base por tipo
        popularidad_base = {
            TipoBien.ALIMENTO_BASICO: 0.8,
            TipoBien.ELECTRONICO_PREMIUM: 0.6,
            TipoBien.ROPA_MODA: 0.4,
            TipoBien.ENTRETENIMIENTO: 0.7,
            TipoBien.SERVICIO_PREMIUM: 0.3
        }
        
        social.popularidad_general = popularidad_base.get(self.tipo_bien, 0.5) + random.uniform(-0.2, 0.2)
        social.popularidad_general = max(0.1, min(1.0, social.popularidad_general))
        
        # Tendencia de crecimiento
        social.tendencia_crecimiento = random.uniform(-0.1, 0.1)
        if self.tipo_bien in [TipoBien.ELECTRONICO_PREMIUM, TipoBien.ENTRETENIMIENTO]:
            social.tendencia_crecimiento += random.uniform(0.0, 0.3)
        
        # Factor viral
        social.factor_viral = 0.0
        if self.tipo_bien in [TipoBien.ROPA_MODA, TipoBien.ENTRETENIMIENTO, TipoBien.ELECTRONICO_PREMIUM]:
            social.factor_viral = random.uniform(0.0, 0.5)
        
        # Influencia de celebridades
        if self.tipo_bien in [TipoBien.ROPA_MODA, TipoBien.HOGAR_LUJO, TipoBien.ELECTRONICO_PREMIUM]:
            social.influencia_celebridades = random.uniform(0.2, 0.8)
        
        # Efectos de red
        if self.tipo_bien in [TipoBien.ELECTRONICO_PREMIUM, TipoBien.ENTRETENIMIENTO]:
            social.valor_red_social = random.uniform(0.3, 0.8)
        
        # Exclusividad
        exclusividad_tipo = {
            TipoBien.ALIMENTO_BASICO: 0.1,
            TipoBien.ALIMENTO_PREMIUM: 0.6,
            TipoBien.ROPA_MODA: 0.7,
            TipoBien.HOGAR_LUJO: 0.9,
            TipoBien.ELECTRONICO_PREMIUM: 0.5
        }
        
        social.exclusividad = exclusividad_tipo.get(self.tipo_bien, 0.3) + random.uniform(-0.1, 0.1)
        social.exclusividad = max(0.0, min(1.0, social.exclusividad))
        
        # Demografía objetivo
        if self.tipo_bien == TipoBien.ROPA_MODA:
            social.grupo_edad_objetivo = [(16, 35), (25, 45)]
        elif self.tipo_bien == TipoBien.ELECTRONICO_PREMIUM:
            social.grupo_edad_objetivo = [(20, 50)]
        elif self.tipo_bien == TipoBien.HOGAR_LUJO:
            social.grupo_edad_objetivo = [(30, 65)]
        
        # Nivel socioeconómico objetivo
        if 'PREMIUM' in self.tipo_bien.name or 'LUJO' in self.tipo_bien.name:
            social.nivel_socioeconomico_objetivo = ['alto', 'medio_alto']
        elif 'BASICO' in self.tipo_bien.name:
            social.nivel_socioeconomico_objetivo = ['bajo', 'medio_bajo', 'medio']
        else:
            social.nivel_socioeconomico_objetivo = ['medio', 'medio_alto']
        
        return social
    
    def _generar_impacto_ambiental(self) -> ImpactoAmbiental:
        """Genera impacto ambiental realista"""
        
        ambiental = ImpactoAmbiental()
        
        # Huella de carbono por tipo
        huella_base = {
            TipoBien.ALIMENTO_BASICO: (0.5, 3.0),
            TipoBien.ALIMENTO_PREMIUM: (1.0, 5.0),
            TipoBien.ELECTRONICO_BASICO: (10.0, 50.0),
            TipoBien.ELECTRONICO_PREMIUM: (20.0, 100.0),
            TipoBien.ROPA_BASICA: (2.0, 8.0),
            TipoBien.ROPA_MODA: (5.0, 15.0),
            TipoBien.TRANSPORTE: (100.0, 1000.0)
        }
        
        if self.tipo_bien in huella_base:
            min_huella, max_huella = huella_base[self.tipo_bien]
            ambiental.huella_carbono = random.uniform(min_huella, max_huella)
        
        # Recursos de agua
        agua_base = {
            TipoBien.ALIMENTO_BASICO: (10, 100),
            TipoBien.ALIMENTO_PREMIUM: (50, 200),
            TipoBien.ROPA_BASICA: (100, 500),
            TipoBien.ROPA_MODA: (200, 800),
            TipoBien.ELECTRONICO_BASICO: (50, 200),
            TipoBien.ELECTRONICO_PREMIUM: (100, 300)
        }
        
        if self.tipo_bien in agua_base:
            min_agua, max_agua = agua_base[self.tipo_bien]
            ambiental.recursos_agua = random.uniform(min_agua, max_agua)
        
        # Reciclabilidad
        ambiental.materiales_reciclables = random.uniform(0.3, 0.9)
        if self.tipo_bien in [TipoBien.ELECTRONICO_BASICO, TipoBien.ELECTRONICO_PREMIUM]:
            ambiental.materiales_reciclables = random.uniform(0.6, 0.8)
        
        # Biodegradable
        ambiental.biodegradable = self.tipo_bien in [TipoBien.ALIMENTO_BASICO, TipoBien.ALIMENTO_PREMIUM]
        
        # Sostenibilidad
        prob_sostenible = 0.3
        if self.tipo_bien in [TipoBien.ALIMENTO_PREMIUM, TipoBien.ROPA_MODA]:
            prob_sostenible = 0.6
        
        ambiental.origen_sostenible = random.random() < prob_sostenible
        ambiental.comercio_justo = random.random() < (prob_sostenible * 0.7)
        ambiental.produccion_local = random.random() < 0.4
        ambiental.empaque_sostenible = random.random() < 0.5
        
        # Puntuaciones ESG
        base_ambiental = 0.5
        if ambiental.origen_sostenible:
            base_ambiental += 0.2
        if ambiental.empaque_sostenible:
            base_ambiental += 0.1
        if ambiental.biodegradable:
            base_ambiental += 0.2
        
        ambiental.puntuacion_ambiental = min(1.0, base_ambiental)
        ambiental.puntuacion_social = random.uniform(0.3, 0.8)
        ambiental.puntuacion_gobernanza = random.uniform(0.4, 0.9)
        
        return ambiental
    
    def _generar_economicas(self) -> EconomicasBien:
        """Genera características económicas del bien"""
        
        econ = EconomicasBien()
        
        # Costo de producción base por tipo
        costos_base = {
            TipoBien.ALIMENTO_BASICO: (2, 10),
            TipoBien.ALIMENTO_PREMIUM: (5, 25),
            TipoBien.ELECTRONICO_BASICO: (20, 100),
            TipoBien.ELECTRONICO_PREMIUM: (100, 500),
            TipoBien.ROPA_BASICA: (5, 20),
            TipoBien.ROPA_MODA: (15, 80),
            TipoBien.HOGAR_BASICO: (10, 50),
            TipoBien.HOGAR_LUJO: (100, 1000)
        }
        
        if self.tipo_bien in costos_base:
            min_costo, max_costo = costos_base[self.tipo_bien]
            econ.costo_produccion_base = random.uniform(min_costo, max_costo)
        
        # Márgenes por tipo
        margenes = {
            TipoBien.ALIMENTO_BASICO: (0.15, 0.4),
            TipoBien.ALIMENTO_PREMIUM: (0.3, 0.8),
            TipoBien.ELECTRONICO_BASICO: (0.2, 0.5),
            TipoBien.ELECTRONICO_PREMIUM: (0.4, 1.2),
            TipoBien.ROPA_MODA: (0.5, 2.0),
            TipoBien.HOGAR_LUJO: (0.8, 3.0)
        }
        
        if self.tipo_bien in margenes:
            min_margen, max_margen = margenes[self.tipo_bien]
            econ.margen_sugerido = random.uniform(min_margen, max_margen)
            econ.margen_minimo = econ.margen_sugerido * 0.3
        
        # Elasticidades específicas
        elasticidades_precio = {
            TipoBien.ALIMENTO_BASICO: (-0.3, -0.1),
            TipoBien.ALIMENTO_PREMIUM: (-1.5, -0.8),
            TipoBien.ELECTRONICO_PREMIUM: (-2.0, -1.2),
            TipoBien.ROPA_MODA: (-1.8, -1.0),
            TipoBien.HOGAR_LUJO: (-2.5, -1.5)
        }
        
        if self.tipo_bien in elasticidades_precio:
            min_elast, max_elast = elasticidades_precio[self.tipo_bien]
            econ.elasticidad_precio_especifica = random.uniform(min_elast, max_elast)
        
        # Costos operativos
        econ.costo_almacenamiento = econ.costo_produccion_base * 0.001  # 0.1% diario
        econ.costo_transporte = econ.costo_produccion_base * 0.05  # 5%
        econ.costo_marketing = econ.costo_produccion_base * 0.1  # 10%
        
        # Economías de escala
        econ.volumen_optimo = random.randint(100, 10000)
        econ.factor_escala = random.uniform(0.8, 0.95)
        
        return econ
    
    def _calcular_fecha_caducidad(self) -> Optional[datetime]:
        """Calcula la fecha de caducidad si aplica"""
        if self.propiedades_fisicas.perecedero and self.propiedades_fisicas.dias_caducidad:
            return self.fecha_fabricacion + timedelta(days=self.propiedades_fisicas.dias_caducidad)
        return None
    
    def _generar_factores_estacionales(self) -> List[float]:
        """Genera factores estacionales para cada mes"""
        
        # Patrones estacionales por tipo
        patrones_base = {
            TipoBien.ALIMENTO_BASICO: [1.0] * 12,  # Demanda constante
            TipoBien.ROPA_MODA: [0.8, 0.7, 1.1, 1.2, 1.1, 0.9, 0.8, 0.9, 1.1, 1.2, 1.3, 1.4],  # Temporadas
            TipoBien.ELECTRONICO_PREMIUM: [1.2, 1.0, 1.0, 1.0, 1.1, 1.0, 0.9, 0.9, 1.0, 1.1, 1.3, 1.5],  # Navidad
            TipoBien.ENTRETENIMIENTO: [1.1, 1.0, 1.0, 1.0, 1.1, 1.2, 1.3, 1.3, 1.0, 1.0, 1.1, 1.2],  # Vacaciones
            TipoBien.HOGAR_LUJO: [0.9, 0.9, 1.1, 1.2, 1.2, 1.0, 0.9, 0.9, 1.0, 1.1, 1.2, 1.3]  # Renovaciones
        }
        
        patron = patrones_base.get(self.tipo_bien, [1.0] * 12)
        
        # Agregar variación aleatoria
        return [max(0.5, min(1.5, factor + random.uniform(-0.1, 0.1))) for factor in patron]
    
    def _generar_eventos_especiales(self) -> Dict[str, float]:
        """Genera eventos especiales que afectan la demanda"""
        
        eventos = {}
        
        # Eventos comunes
        if random.random() < 0.3:  # 30% probabilidad
            eventos['black_friday'] = random.uniform(1.5, 3.0)
        
        if random.random() < 0.2:  # 20% probabilidad
            eventos['dia_madre'] = random.uniform(1.2, 2.0)
        
        # Eventos específicos por tipo
        if self.tipo_bien == TipoBien.ROPA_MODA:
            if random.random() < 0.4:
                eventos['fashion_week'] = random.uniform(1.3, 2.5)
        
        elif self.tipo_bien == TipoBien.ELECTRONICO_PREMIUM:
            if random.random() < 0.3:
                eventos['lanzamiento_competencia'] = random.uniform(0.7, 0.9)  # Efecto negativo
        
        elif self.tipo_bien in [TipoBien.ALIMENTO_BASICO, TipoBien.ALIMENTO_PREMIUM]:
            if random.random() < 0.2:
                eventos['temporada_cosecha'] = random.uniform(0.8, 1.2)
        
        return eventos
    
    def _actualizar_valores_derivados(self):
        """Actualiza valores calculados basándose en características"""
        
        # Precio base sugerido
        costo = self.economicas.costo_produccion_base
        margen = self.economicas.margen_sugerido
        self.precio_base_sugerido = costo * (1 + margen)
        
        # Factor de calidad global
        calidad_num = self.atributos_calidad.nivel_calidad.value / 6.0
        self.factor_calidad_global = (
            calidad_num * 0.4 +
            self.atributos_calidad.marca_prestigio * 0.3 +
            self.atributos_calidad.funcionalidad * 0.3
        )
        
        # Puntuación de sostenibilidad
        self.puntuacion_sostenibilidad = (
            self.impacto_ambiental.puntuacion_ambiental * 0.5 +
            self.impacto_ambiental.puntuacion_social * 0.3 +
            self.impacto_ambiental.puntuacion_gobernanza * 0.2
        )
        
        # Atractivo emocional total
        self.atractivo_emocional = (
            self.impacto_emocional.factor_estatus * 0.25 +
            self.impacto_emocional.factor_placer * 0.35 +
            self.impacto_emocional.factor_autoestima * 0.25 +
            self.impacto_emocional.factor_seguridad * 0.15
        )
    
    def calcular_desgaste(self, dias_uso: int, intensidad_uso: float = 1.0) -> float:
        """Calcula el desgaste del bien basándose en uso"""
        
        if self.propiedades_fisicas.durabilidad_base <= 0:
            return 1.0  # Completamente desgastado
        
        # Factor de desgaste diario
        desgaste_diario = 1.0 / (self.propiedades_fisicas.durabilidad_base * 365)
        
        # Ajustar por fragilidad
        desgaste_diario *= (1.0 + self.propiedades_fisicas.fragilidad)
        
        # Ajustar por intensidad de uso
        desgaste_diario *= intensidad_uso
        
        # Calcular desgaste acumulado
        nuevo_desgaste = self.desgaste_actual + (desgaste_diario * dias_uso)
        
        # Actualizar estado
        self.desgaste_actual = min(1.0, nuevo_desgaste)
        self._actualizar_estado_vida()
        
        return self.desgaste_actual
    
    def _actualizar_estado_vida(self):
        """Actualiza el estado de vida basándose en el desgaste"""
        
        if self.desgaste_actual < 0.05:
            self.estado_vida = EstadoVida.NUEVO
        elif self.desgaste_actual < 0.15:
            self.estado_vida = EstadoVida.USADO_COMO_NUEVO
        elif self.desgaste_actual < 0.4:
            self.estado_vida = EstadoVida.USADO_BUENO
        elif self.desgaste_actual < 0.7:
            self.estado_vida = EstadoVida.USADO_REGULAR
        elif self.desgaste_actual < 0.9:
            self.estado_vida = EstadoVida.DETERIORADO
        else:
            self.estado_vida = EstadoVida.DEFECTUOSO
    
    def calcular_precio_dinamico(self, precio_base: float, contexto_mercado: Dict[str, Any]) -> float:
        """Calcula precio dinámico basándose en múltiples factores"""
        
        precio = precio_base
        
        # Factor de calidad
        precio *= (0.8 + self.factor_calidad_global * 0.4)
        
        # Factor de estado
        factores_estado = {
            EstadoVida.NUEVO: 1.0,
            EstadoVida.USADO_COMO_NUEVO: 0.9,
            EstadoVida.USADO_BUENO: 0.75,
            EstadoVida.USADO_REGULAR: 0.6,
            EstadoVida.DETERIORADO: 0.4,
            EstadoVida.DEFECTUOSO: 0.2
        }
        precio *= factores_estado[self.estado_vida]
        
        # Factor estacional
        mes_actual = datetime.now().month - 1  # 0-11
        precio *= self.factor_estacional_mensual[mes_actual]
        
        # Factores sociales
        if 'demanda_social' in contexto_mercado:
            demanda = contexto_mercado['demanda_social']
            precio *= (0.8 + demanda * 0.4)
        
        # Factor de exclusividad
        precio *= (1.0 + self.factores_sociales.exclusividad * 0.2)
        
        # Tendencias de crecimiento
        if self.factores_sociales.tendencia_crecimiento > 0:
            precio *= (1.0 + self.factores_sociales.tendencia_crecimiento * 0.1)
        
        # Eventos especiales
        if 'evento_actual' in contexto_mercado:
            evento = contexto_mercado['evento_actual']
            if evento in self.eventos_especiales:
                precio *= self.eventos_especiales[evento]
        
        # Factor de sostenibilidad (premium por productos sostenibles)
        if contexto_mercado.get('valoracion_sostenibilidad', 0.5) > 0.6:
            precio *= (1.0 + self.puntuacion_sostenibilidad * 0.15)
        
        return max(self.economicas.costo_produccion_base * (1 + self.economicas.margen_minimo), precio)
    
    def agregar_valoracion_usuario(self, valoracion: float, comentario: str = ""):
        """Agrega una valoración de usuario"""
        self.valoraciones_usuarios.append(max(0.0, min(5.0, valoracion)))
        
        # Actualizar popularidad basándose en valoraciones
        if len(self.valoraciones_usuarios) > 5:
            promedio = sum(self.valoraciones_usuarios) / len(self.valoraciones_usuarios)
            if promedio > 4.0:
                self.factores_sociales.popularidad_general = min(1.0, 
                    self.factores_sociales.popularidad_general + 0.01)
            elif promedio < 2.0:
                self.factores_sociales.popularidad_general = max(0.1, 
                    self.factores_sociales.popularidad_general - 0.02)
    
    def get_valoracion_promedio(self) -> float:
        """Obtiene la valoración promedio de usuarios"""
        if not self.valoraciones_usuarios:
            return 3.0  # Neutral por defecto
        return sum(self.valoraciones_usuarios) / len(self.valoraciones_usuarios)
    
    def es_compatible_con_perfil(self, perfil_consumidor) -> float:
        """Calcula compatibilidad con perfil de consumidor (0.0 a 1.0)"""
        
        compatibilidad = 0.5  # Base neutral
        
        # Compatibilidad por tipo de personalidad
        if hasattr(perfil_consumidor, 'tipo_personalidad'):
            if perfil_consumidor.tipo_personalidad.value == 'hedonista':
                compatibilidad += self.impacto_emocional.factor_placer * 0.2
            elif perfil_consumidor.tipo_personalidad.value == 'conservador':
                compatibilidad += self.impacto_emocional.factor_seguridad * 0.2
            elif perfil_consumidor.tipo_personalidad.value == 'social':
                compatibilidad += self.factores_sociales.popularidad_general * 0.2
        
        # Compatibilidad por preferencias
        if hasattr(perfil_consumidor, 'preferencias_consumo'):
            prefs = perfil_consumidor.preferencias_consumo
            
            if self.tipo_bien in [TipoBien.ALIMENTO_BASICO, TipoBien.ALIMENTO_PREMIUM]:
                compatibilidad += (prefs.preferencia_alimentacion - 0.5) * 0.3
            elif self.tipo_bien in [TipoBien.ELECTRONICO_BASICO, TipoBien.ELECTRONICO_PREMIUM]:
                compatibilidad += (prefs.preferencia_tecnologia - 0.5) * 0.3
            elif self.tipo_bien in [TipoBien.ROPA_BASICA, TipoBien.ROPA_MODA]:
                compatibilidad += (prefs.preferencia_ropa - 0.5) * 0.3
        
        # Compatibilidad por valores
        if hasattr(perfil_consumidor, 'rasgos_psicologicos'):
            rasgos = perfil_consumidor.rasgos_psicologicos
            
            if rasgos.importancia_sostenibilidad > 0.7:
                compatibilidad += self.puntuacion_sostenibilidad * 0.2
            
            if rasgos.importancia_calidad > 0.7:
                compatibilidad += self.factor_calidad_global * 0.2
            
            if rasgos.materialismo > 0.7:
                compatibilidad += self.impacto_emocional.factor_estatus * 0.2
        
        return max(0.0, min(1.0, compatibilidad))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el bien a diccionario para serialización"""
        return {
            'nombre': self.nombre,
            'tipo_bien': self.tipo_bien.value,
            'categoria': self.categoria,
            'precio_base_sugerido': self.precio_base_sugerido,
            'factor_calidad_global': self.factor_calidad_global,
            'puntuacion_sostenibilidad': self.puntuacion_sostenibilidad,
            'atractivo_emocional': self.atractivo_emocional,
            'popularidad': self.factores_sociales.popularidad_general,
            'exclusividad': self.factores_sociales.exclusividad,
            'valoracion_promedio': self.get_valoracion_promedio(),
            'estado_vida': self.estado_vida.value,
            'desgaste_actual': self.desgaste_actual
        }
    
    def __str__(self) -> str:
        return (f"{self.nombre} ({self.tipo_bien.value}) - "
                f"Calidad: {self.factor_calidad_global:.2f}, "
                f"Precio sugerido: ${self.precio_base_sugerido:.2f}, "
                f"Popularidad: {self.factores_sociales.popularidad_general:.2f}")
