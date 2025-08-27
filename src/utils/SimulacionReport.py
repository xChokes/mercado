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

    def snapshot(self) -> Dict[str, Any]:
        return {
            'inflacion_ultima': self.inflacion[-1] if self.inflacion else 0.0,
            'pib_ultimo': self.pib[-1] if self.pib else 0.0,
            'desempleo_ultimo': self.desempleo[-1] if self.desempleo else 0.0,
            'gini_ultimo': self.gini[-1] if self.gini else 0.0,
            'transacciones_totales': self.transacciones_totales,
            'spread_promedio': self.spread_promedio,
            'profundidad_promedio': self.profundidad_promedio,
        }
