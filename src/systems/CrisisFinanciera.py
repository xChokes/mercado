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
    riesgo_total = max(
        0.0, min(1.0, (riesgo_solvencia + riesgo_exposicion) / 2))
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


def evaluar_recuperacion_crisis(mercado) -> bool:
    """Evalúa si la economía ha cumplido condiciones para salir de crisis.

    Condiciones de recuperación (más flexibles):
    - Crisis activa por más de 10 ciclos (reducido de 15)
    - PIB mayor que cero por 2+ ciclos consecutivos
    - Desempleo no empeorando dramáticamente
    - Al menos alguna actividad económica presente
    """
    if not mercado.crisis_financiera_activa:
        return False

    # Condición 1: Crisis prolongada (recuperación forzada más temprana)
    if hasattr(mercado, 'ciclos_en_crisis') and mercado.ciclos_en_crisis > 10:
        return True

    # Condición 2: PIB positivo por 2+ ciclos (más flexible)
    if len(mercado.pib_historico) >= 3:
        ultimos_pibs = mercado.pib_historico[-3:]
        # Al menos uno positivo
        pib_positivo = any(pib > 0 for pib in ultimos_pibs[-2:])
        # No caída dramática
        pib_estable = ultimos_pibs[-1] >= ultimos_pibs[-2] * 0.9

        if pib_positivo and pib_estable:
            return True

    # Condición 3: Actividad económica mínima (nueva condición)
    if len(mercado.transacciones) > 0:
        transacciones_recientes = [
            t for t in mercado.transacciones
            if t.get('ciclo', 0) >= len(mercado.pib_historico) - 5
        ]
        if len(transacciones_recientes) > 10:  # Al menos 10 transacciones en últimos 5 ciclos
            return True

    # Condición 4: Desempleo estabilizado o mejorando ligeramente
    if (len(mercado.desempleo_historico) >= 3):
        desempleo_actual = mercado.desempleo_historico[-1]
        desempleo_anterior = mercado.desempleo_historico[-3]

        # Si el desempleo no está empeorando mucho, permitir recuperación
        if desempleo_actual <= desempleo_anterior * 1.1:  # Máximo 10% de empeoramiento
            return True

    return False


def aplicar_medidas_recuperacion(mercado):
    """Aplica medidas automáticas de recuperación económica más agresivas.

    Simula intervenciones gubernamentales y bancarias para estabilizar la economía.
    """
    if not mercado.crisis_financiera_activa:
        return

    # Medida 1: Reducir tasa de interés del gobierno más agresivamente
    mercado.gobierno.tasa_interes_referencia = max(
        0.001, mercado.gobierno.tasa_interes_referencia * 0.7
    )

    # Medida 2: Inyección de liquidez más grande al sistema bancario
    for banco in mercado.sistema_bancario.bancos:
        inyeccion = banco.capital * 0.2  # Aumentado de 0.1 a 0.2
        banco.reservas += inyeccion
        banco.capital += inyeccion * 0.8  # Aumentado de 0.5 a 0.8

    # Medida 3: Estímulo fiscal más agresivo
    mercado.gobierno.presupuesto += mercado.gobierno.presupuesto * \
        0.1  # Aumentado de 0.05 a 0.1

    # Medida 4: Incentivos de contratación más fuertes para empresas
    for empresa in mercado.getEmpresas():
        if hasattr(empresa, 'dinero'):
            subsidio = empresa.dinero * 0.05  # Aumentado de 0.02 a 0.05
            empresa.dinero += subsidio

    # Medida 5: NUEVA - Estímulo directo a consumidores
    for consumidor in mercado.getConsumidores():
        if hasattr(consumidor, 'dinero'):
            subsidio = consumidor.ingreso_mensual * 0.5  # Medio salario de estímulo
            consumidor.dinero += subsidio

    # Medida 6: NUEVA - Reducir costos de producción temporalmente
    for empresa in mercado.getEmpresas():
        if hasattr(empresa, 'costos_unitarios'):
            for bien in empresa.costos_unitarios:
                empresa.costos_unitarios[bien] *= 0.9  # Reducir costos 10%
