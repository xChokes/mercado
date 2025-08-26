"""
Adaptadores de modelos clásicos a la interfaz IAgent para migración progresiva.
"""
from __future__ import annotations

from typing import Any, Dict, Optional
from .IAgent import IAgent, AgentType
from .BaseAgent import BaseAgent


class ConsumidorAdapter(BaseAgent, IAgent):
    def __init__(self, consumidor, agent_id: Optional[str] = None, seed: Optional[int] = None) -> None:
        super().__init__(agent_id or f"consumidor_{getattr(consumidor, 'nombre', 'anon')}", seed)
        self._wrapped = consumidor

    @property
    def agent_type(self) -> AgentType:
        return AgentType.CONSUMIDOR

    def observe(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        # Construir observación simple desde atributos del consumidor
        obs = {
            "dinero": getattr(self._wrapped, "dinero", 0.0),
            "ingreso_mensual": getattr(self._wrapped, "ingreso_mensual", 0.0),
            "empleado": getattr(self._wrapped, "empleado", False),
        }
        if context:
            obs.update(context)
        return obs

    def decide(self, observation: Dict[str, Any]) -> Dict[str, Any]:
        # Política heurística: proporción de gasto basada en propensión de consumo
        prop = getattr(self._wrapped, "propension_consumo", 0.8)
        return {"tasa_gasto": self.clamp(prop, 0.0, 1.0)}

    def act(self, action: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        # Delegar al ciclo de persona existente como acción
        mercado = getattr(self._wrapped, "mercado", None)
        ciclo = context.get("ciclo") if context else 0
        if hasattr(self._wrapped, "ciclo_persona") and mercado is not None:
            try:
                self._wrapped.ciclo_persona(ciclo, mercado)
            except Exception as e:
                # Log del error pero no interrumpir el flujo del agente
                import logging
                logging.getLogger(__name__).debug(f"Error en ciclo_persona de {self.agent_id}: {e}")
        return {"status": "ok"}

    def learn(self, feedback: Dict[str, Any]) -> None:
        # No-Op para el adaptador
        return


class EmpresaAdapter(BaseAgent, IAgent):
    def __init__(self, empresa, agent_id: Optional[str] = None, seed: Optional[int] = None) -> None:
        super().__init__(agent_id or f"empresa_{getattr(empresa, 'nombre', 'anon')}", seed)
        self._wrapped = empresa

    @property
    def agent_type(self) -> AgentType:
        return AgentType.EMPRESA

    def observe(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        obs = {
            "dinero": getattr(self._wrapped, "dinero", 0.0),
            "empleados": len(getattr(self._wrapped, "empleados", []) or []),
        }
        if context:
            obs.update(context)
        return obs

    def decide(self, observation: Dict[str, Any]) -> Dict[str, Any]:
        # Heurística simple: mantener precios
        return {"policy": "mantener"}

    def act(self, action: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        mercado = getattr(self._wrapped, "mercado", None)
        ciclo = context.get("ciclo") if context else 0
        if hasattr(self._wrapped, "ciclo_persona") and mercado is not None:
            try:
                self._wrapped.ciclo_persona(ciclo, mercado)
            except Exception as e:
                # Log del error pero no interrumpir el flujo del agente
                import logging
                logging.getLogger(__name__).debug(f"Error en ciclo_persona empresa de {self.agent_id}: {e}")
        return {"status": "ok"}

    def learn(self, feedback: Dict[str, Any]) -> None:
        return


__all__ = ["ConsumidorAdapter", "EmpresaAdapter"]
