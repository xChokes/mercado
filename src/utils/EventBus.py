from dataclasses import dataclass, asdict
from typing import List, Dict, Any
import time


@dataclass
class Evento:
    tipo: str
    data: Dict[str, Any]
    ts: float


class EventBus:
    """Registro centralizado de eventos (en memoria).

    Se puede exportar como lista de dicts para DF.
    """

    def __init__(self):
        self.eventos: List[Evento] = []

    def publish(self, tipo: str, **data):
        self.eventos.append(Evento(tipo=tipo, data=data, ts=time.time()))

    def all(self) -> List[Dict[str, Any]]:
        return [
            {
                'tipo': e.tipo,
                'ts': e.ts,
                **e.data
            } for e in self.eventos
        ]
