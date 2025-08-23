"""
BaseAgent proporciona utilidades comunes para agentes IA:
- gestión de semillas
- clamps/normalización
- logging ligero de decisiones
"""

from __future__ import annotations

from typing import Any, Dict, Optional
import json
import random
import numpy as np
from datetime import datetime


class BaseAgent:
    def __init__(self, agent_id: str, seed: Optional[int] = None) -> None:
        self._agent_id = agent_id
        self._rng = np.random.default_rng(seed)
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
        self._decision_log_enabled = False
        self._decision_log_path = None

    # --- utilidades ---
    @property
    def agent_id(self) -> str:
        return self._agent_id

    def enable_decision_log(self, path: str) -> None:
        self._decision_log_enabled = True
        self._decision_log_path = path

    def log_decision(self, observation: Dict[str, Any], action: Dict[str, Any], extra: Optional[Dict[str, Any]] = None) -> None:
        if not self._decision_log_enabled or not self._decision_log_path:
            return
        record = {
            "ts": datetime.utcnow().isoformat(),
            "agent_id": self._agent_id,
            "observation": observation,
            "action": action,
        }
        if extra:
            record.update(extra)
        try:
            with open(self._decision_log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        except Exception:
            # Logging best-effort, no romper simulación
            pass

    # Normalización y clamps
    @staticmethod
    def clamp(x: float, lo: float, hi: float) -> float:
        return max(lo, min(hi, x))

    @staticmethod
    def safe_div(a: float, b: float, default: float = 0.0) -> float:
        return a / b if b else default

    @staticmethod
    def norm(x: float, lo: float, hi: float) -> float:
        if hi == lo:
            return 0.0
        x = BaseAgent.clamp(x, lo, hi)
        return (x - lo) / (hi - lo)

    # Persistencia (stubs)
    def save_state(self, path: str) -> None:
        # implementaciones concretas pueden sobrescribir
        pass

    def load_state(self, path: str) -> None:
        # implementaciones concretas pueden sobrescribir
        pass
