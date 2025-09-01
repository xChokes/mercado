from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class SimulacionReport:
    inflacion: List[float] = field(default_factory=list)
    pib: List[float] = field(default_factory=list)
    desempleo: List[float] = field(default_factory=list)
    gini: List[float] = field(default_factory=list)
    transacciones_totales: int = 0
    spread_promedio: Dict[str, float] = field(default_factory=dict)
    profundidad_promedio: Dict[str, Dict[str, float]] = field(default_factory=dict)
    
    # NUEVOS KPIs para dinámicas empresariales
    tasa_quiebra: List[float] = field(default_factory=list)  # % empresas que quiebran por ciclo
    rotacion_empresas: List[float] = field(default_factory=list)  # Entrada + salida empresas
    rigidez_precios: List[float] = field(default_factory=list)  # % precios sin cambio
    empresas_activas: List[int] = field(default_factory=list)  # Número total de empresas
    empresas_entrantes: List[int] = field(default_factory=list)  # Nuevas empresas por período
    
    # Métricas de inventarios S,s
    inventario_promedio_ratio: List[float] = field(default_factory=list)  # Stock/Objetivo promedio
    costos_ajuste_precio_totales: List[float] = field(default_factory=list)  # Costos totales de cambio precio

    def snapshot(self) -> Dict[str, Any]:
        return {
            'inflacion_ultima': self.inflacion[-1] if self.inflacion else 0.0,
            'pib_ultimo': self.pib[-1] if self.pib else 0.0,
            'desempleo_ultimo': self.desempleo[-1] if self.desempleo else 0.0,
            'gini_ultimo': self.gini[-1] if self.gini else 0.0,
            'transacciones_totales': self.transacciones_totales,
            'spread_promedio': self.spread_promedio,
            'profundidad_promedio': self.profundidad_promedio,
            
            # NUEVOS KPIs empresariales
            'tasa_quiebra_ultima': self.tasa_quiebra[-1] if self.tasa_quiebra else 0.0,
            'rotacion_empresas_ultima': self.rotacion_empresas[-1] if self.rotacion_empresas else 0.0,
            'rigidez_precios_ultima': self.rigidez_precios[-1] if self.rigidez_precios else 0.0,
            'empresas_activas_actual': self.empresas_activas[-1] if self.empresas_activas else 0,
            'empresas_entrantes_ultima': self.empresas_entrantes[-1] if self.empresas_entrantes else 0,
            'inventario_ratio_ultimo': self.inventario_promedio_ratio[-1] if self.inventario_promedio_ratio else 0.0,
            'costos_ajuste_totales': self.costos_ajuste_precio_totales[-1] if self.costos_ajuste_precio_totales else 0.0,
        }
