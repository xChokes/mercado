"""
Contrato unificado para Agentes IA del simulador.

Define un protocolo mínimo para que consumidores, empresas,
gobierno, banco central y otros actores puedan interoperar
con los sistemas del mercado sin acoplarse a implementaciones concretas.
"""

from __future__ import annotations

from typing import Any, Dict, Protocol, runtime_checkable, Optional
from enum import Enum


class AgentType(str, Enum):
    CONSUMIDOR = "consumidor"
    EMPRESA = "empresa"
    GOBIERNO = "gobierno"
    BANCO_CENTRAL = "banco_central"
    INTERMEDIARIO_FINANCIERO = "intermediario_financiero"


@runtime_checkable
class IAgent(Protocol):
    """Interfaz mínima para agentes IA"""

    @property
    def agent_id(self) -> str:  # noqa: D401
        """Identificador único del agente"""

    @property
    def agent_type(self) -> AgentType:  # noqa: D401
        """Tipo de agente (consumidor, empresa, etc.)"""

    def observe(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Construye una observación a partir del contexto/mercado."""

    def decide(self, observation: Dict[str, Any]) -> Dict[str, Any]:
        """Devuelve una acción (diccionario) basada en la observación."""

    def act(self, action: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Efectúa la acción en el entorno/mercado y devuelve efectos/resultados."""

    def learn(self, feedback: Dict[str, Any]) -> None:
        """Actualiza la política/memoria con feedback (recompensa, next_obs, etc.)."""

    def save_state(self, path: str) -> None:
        """Persiste el estado del agente (pesos, buffers, etc.)."""

    def load_state(self, path: str) -> None:
        """Carga el estado previamente guardado."""


__all__ = ["IAgent", "AgentType"]
