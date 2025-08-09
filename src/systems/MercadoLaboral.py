"""Sistema de mercado laboral con perfiles de habilidades, sindicatos y movilidad"""
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class PerfilHabilidadesSectoriales:
    """Perfil de habilidades por sector para un trabajador"""
    habilidades: Dict[str, float] = field(default_factory=dict)

    def obtener_nivel(self, sector: str) -> float:
        """Obtiene el nivel de habilidad para un sector dado"""
        return self.habilidades.get(sector, 0.0)

    def sector_principal(self) -> Optional[str]:
        """Devuelve el sector donde el trabajador es más competente"""
        if not self.habilidades:
            return None
        return max(self.habilidades, key=self.habilidades.get)


@dataclass
class Sindicato:
    """Representa un sindicato laboral"""
    nombre: str
    sectores: List[str]
    cuota: float = 0.01  # 1% de aporte sindical
    poder_negociacion: float = 0.05  # Aumento salarial negociado
    miembros: List["Consumidor"] = field(default_factory=list)

    def afiliar(self, trabajador: "Consumidor") -> None:
        """Afiliar un trabajador al sindicato"""
        if trabajador not in self.miembros:
            self.miembros.append(trabajador)
            trabajador.sindicato = self

    def calcular_aporte(self, salario: float) -> float:
        """Calcula el aporte sindical sobre el salario"""
        return salario * self.cuota


class MercadoLaboral:
    """Coordinador del mercado laboral"""

    def __init__(self, mercado):
        self.mercado = mercado
        self.sectores = list(mercado.economia_sectorial.sectores.keys()) if hasattr(mercado, "economia_sectorial") else []
        # Crear sindicatos básicos por sector
        self.sindicatos = [Sindicato(f"Sindicato_{s}", [s]) for s in self.sectores]

    def crear_perfil(self) -> PerfilHabilidadesSectoriales:
        """Genera un perfil de habilidades aleatorio por sector"""
        habilidades = {sector: random.uniform(0.0, 1.0) for sector in self.sectores}
        return PerfilHabilidadesSectoriales(habilidades)

    def asignar_sindicato(self, trabajador: "Consumidor") -> Optional[Sindicato]:
        """Asigna aleatoriamente un sindicato al trabajador"""
        if self.sindicatos and random.random() < 0.5:  # 50% tasa de sindicalización
            sindicato = random.choice(self.sindicatos)
            sindicato.afiliar(trabajador)
            return sindicato
        return None

    def compatibilidad(self, perfil: PerfilHabilidadesSectoriales, sector: str) -> float:
        """Calcula la compatibilidad de un perfil con un sector"""
        return perfil.obtener_nivel(sector)

    def probabilidad_movilidad(self, origen: str, destino: str) -> float:
        """Probabilidad base de moverse entre sectores"""
        if origen == destino:
            return 1.0
        return 0.1  # movilidad simple entre sectores distintos
