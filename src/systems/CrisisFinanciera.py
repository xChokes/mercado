"""
Herramientas para analizar y simular crisis financieras.
Incluye detección de burbujas de precios, evaluación de riesgo sistémico
y simulación de corridas bancarias.
"""

from typing import Dict, List


def detectar_burbuja_precios(mercado, bien: str = None, ventana: int = 5, umbral: float = 0.5) -> bool:
    """Detecta si existe una burbuja de precios en un bien o en el mercado.

    Una burbuja se identifica cuando el precio ha crecido más del ``umbral``
    respecto a hace ``ventana`` ciclos.
    """
    bienes_a_evaluar: List[str]
    if bien:
        bienes_a_evaluar = [bien]
    else:
        bienes_a_evaluar = list(mercado.precios_historicos.keys())

    for nombre in bienes_a_evaluar:
        historial = mercado.precios_historicos.get(nombre, [])
        if len(historial) > ventana:
            precio_reciente = historial[-1]
            precio_pasado = historial[-ventana]
            if precio_pasado > 0 and (precio_reciente / precio_pasado - 1) > umbral:
                return True
    return False


def evaluar_riesgo_sistemico(sistema_bancario) -> float:
    """Evalúa un índice de riesgo sistémico del sistema bancario.

    Se basa en la solvencia promedio y las exposiciones interbancarias.
    """
    if not sistema_bancario.bancos:
        return 0.0

    ratios = []
    exposicion_total = 0.0
    capital_total = 0.0
    for banco in sistema_bancario.bancos:
        ratios.append(banco.calcular_ratio_solvencia())
        exposicion_total += sum(banco.exposiciones_interbancarias.values())
        capital_total += banco.capital

    riesgo_solvencia = 1 - (sum(ratios) / len(ratios))
    if capital_total > 0:
        riesgo_exposicion = exposicion_total / capital_total
    else:
        riesgo_exposicion = 0

    # Índice final entre 0 y 1
    riesgo_total = max(0.0, min(1.0, (riesgo_solvencia + riesgo_exposicion) / 2))
    return riesgo_total


def simular_corrida_bancaria(sistema_bancario, intensidad: float = 0.3) -> Dict[str, float]:
    """Simula retiros masivos de depósitos en todos los bancos.

    ``intensidad`` determina el porcentaje de depósitos retirados.
    Retorna un diccionario con los retiros totales por banco.
    """
    retiros = {}
    for banco in sistema_bancario.bancos:
        retiro_total = 0.0
        for persona_id, saldo in list(banco.depositos.items()):
            retiro = saldo * intensidad
            banco.depositos[persona_id] -= retiro
            retiro_total += retiro
            banco.reservas = max(0, banco.reservas - retiro * 0.1)
            banco.capital -= retiro * 0.05  # costo de liquidez de emergencia
        retiros[banco.nombre] = retiro_total
    return retiros

