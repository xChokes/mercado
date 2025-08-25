"""
API mínima (FastAPI) para interactuar con el simulador.
- POST /simular: Ejecuta una simulación con parámetros opcionales.
- GET /salud: Chequeo simple de salud.
"""
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Dict, Any

from src.config.ConfiguradorSimulacion import ConfiguradorSimulacion
from src.main import ejecutar_simulacion_completa

app = FastAPI(title="Simulador de Mercado IA - API")

class SimulacionRequest(BaseModel):
    num_ciclos: Optional[int] = None
    num_consumidores: Optional[int] = None
    activar_ia: Optional[bool] = None

@app.get("/salud")
async def salud():
    return {"status": "ok"}

@app.post("/simular")
async def simular(req: SimulacionRequest):
    # Cargar configuración por defecto y aplicar overrides sencillos
    config = ConfiguradorSimulacion()
    cfg = config.config
    if req.num_ciclos is not None:
        cfg.setdefault('simulacion', {})['num_ciclos'] = int(req.num_ciclos)
    if req.num_consumidores is not None:
        cfg.setdefault('simulacion', {})['num_consumidores'] = int(req.num_consumidores)
    if req.activar_ia is not None:
        cfg.setdefault('agentes_ia', {})['activar'] = bool(req.activar_ia)
    # Ejecutar simulación (sin bloquear indefinidamente en casos largos)
    mercado = ejecutar_simulacion_completa(config)
    # Resumen ligero
    resumen = {
        'ciclos': cfg['simulacion'].get('num_ciclos'),
        'pib_final': mercado.pib_historico[-1] if mercado.pib_historico else 0,
        'inflacion_final': mercado.inflacion_historica[-1] if mercado.inflacion_historica else 0,
        'consumidores': len(mercado.getConsumidores()),
        'empresas': len(mercado.getEmpresas()),
    }
    return {'resultado': 'ok', 'resumen': resumen}
