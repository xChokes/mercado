"""
Sistema de Estímulo Económico para activar la economía cuando está estancada
"""
import random


def detectar_estancamiento_economico(mercado):
    """Detecta si la economía está estancada (PIB en 0 por varios ciclos)"""
    if len(mercado.pib_historico) < 3:
        return False

    # Si los últimos 3 ciclos tienen PIB = 0
    ultimos_pibs = mercado.pib_historico[-3:]
    return all(pib == 0 for pib in ultimos_pibs)


def aplicar_estimulo_emergencia(mercado):
    """Aplica estímulos de emergencia para reactivar la economía estancada"""
    print("🚨 ECONOMÍA ESTANCADA - Aplicando estímulos de emergencia...")

    # 1. Compras gubernamentales masivas
    _realizar_compras_gubernamentales(mercado)

    # 2. Subsidios directos a empresas
    _subsidiar_empresas(mercado)

    # 3. Estímulo a consumidores
    _estimular_consumidores(mercado)

    # 4. Forzar producción mínima
    _forzar_produccion_minima(mercado)

    print("✅ Estímulos de emergencia aplicados")


def _realizar_compras_gubernamentales(mercado):
    """El gobierno compra directamente productos para estimular demanda"""
    empresas_productoras = [e for e in mercado.getEmpresas()
                            if hasattr(e, 'bienes') and hasattr(e, 'precios')]

    if not empresas_productoras:
        return

    # Comprar de varias empresas
    for empresa in empresas_productoras[:5]:  # Limitar a 5 empresas
        if not empresa.bienes or not empresa.precios:
            continue

        # Elegir un bien disponible
        bienes_disponibles = [bien for bien, cantidad in empresa.bienes.items()
                              if cantidad and bien in empresa.precios]

        if bienes_disponibles:
            bien_elegido = random.choice(bienes_disponibles)
            cantidad_compra = min(10, len(empresa.bienes[bien_elegido]))
            precio_unitario = empresa.precios[bien_elegido]

            if cantidad_compra > 0 and mercado.gobierno.presupuesto > precio_unitario * cantidad_compra:
                # Realizar transacción gubernamental
                costo_total = precio_unitario * cantidad_compra

                # Transferir dinero y productos
                mercado.gobierno.presupuesto -= costo_total
                empresa.dinero += costo_total

                # Reducir inventario
                for _ in range(cantidad_compra):
                    if empresa.bienes[bien_elegido]:
                        empresa.bienes[bien_elegido].pop()

                # Registrar transacción
                mercado.registrar_transaccion(
                    mercado.gobierno, bien_elegido, cantidad_compra, costo_total, mercado.ciclo_actual
                )

                print(
                    f"  🏛️ Gobierno compró {cantidad_compra} {bien_elegido} de {empresa.nombre}")


def _subsidiar_empresas(mercado):
    """Dar subsidios directos a empresas para capital de trabajo"""
    empresas = mercado.getEmpresas()

    for empresa in empresas[:10]:  # Limitar a 10 empresas
        if hasattr(empresa, 'dinero'):
            # Mínimo $10k o 20% del capital
            subsidio = max(10000, empresa.dinero * 0.2)
            empresa.dinero += subsidio
            mercado.gobierno.presupuesto -= subsidio


def _estimular_consumidores(mercado):
    """Dar estímulo directo a consumidores para aumentar consumo"""
    consumidores = mercado.getConsumidores()

    for consumidor in consumidores:
        if hasattr(consumidor, 'dinero') and hasattr(consumidor, 'ingreso_mensual'):
            estimulo = consumidor.ingreso_mensual * 0.3  # 30% del ingreso mensual
            consumidor.dinero += estimulo
            mercado.gobierno.presupuesto -= estimulo


def _forzar_produccion_minima(mercado):
    """Fuerza a las empresas a producir una cantidad mínima"""
    empresas_productoras = [e for e in mercado.getEmpresas()
                            if hasattr(e, 'producir_bien_mejorado')]

    for empresa in empresas_productoras:
        if not hasattr(empresa, 'bienes') or not empresa.bienes:
            continue

        # Producir al menos 5 unidades de cada bien que puede producir
        for bien in list(empresa.bienes.keys())[:3]:  # Limitar a 3 bienes
            if hasattr(empresa, 'capacidad_produccion') and bien in empresa.capacidad_produccion:
                cantidad_minima = min(
                    5, empresa.capacidad_produccion.get(bien, 0))
                if cantidad_minima > 0:
                    try:
                        empresa.producir_bien_mejorado(
                            bien, cantidad_minima, mercado)
                    except Exception as e:
                        print(
                            f"    ⚠️ Error forzando producción en {empresa.nombre}: {e}")


def ciclo_estimulo_economico(mercado):
    """Ejecuta el ciclo de estímulo económico"""
    # Solo aplicar si la economía está realmente estancada
    if detectar_estancamiento_economico(mercado):
        aplicar_estimulo_emergencia(mercado)

    # Aplicar estímulos menores cada ciclo para mantener actividad
    elif len(mercado.pib_historico) > 0 and mercado.pib_historico[-1] < 1000:
        _aplicar_estimulos_menores(mercado)


def _aplicar_estimulos_menores(mercado):
    """Aplica estímulos menores para mantener actividad económica básica"""
    # Pequeñas compras gubernamentales
    empresas = mercado.getEmpresas()
    if empresas:
        empresa_random = random.choice(empresas)
        if (hasattr(empresa_random, 'bienes') and empresa_random.bienes and
                hasattr(empresa_random, 'precios') and empresa_random.precios):

            bien_random = random.choice(list(empresa_random.precios.keys()))
            if bien_random in empresa_random.bienes and empresa_random.bienes[bien_random]:
                precio = empresa_random.precios[bien_random]
                if mercado.gobierno.presupuesto > precio * 2:
                    mercado.gobierno.presupuesto -= precio * 2
                    empresa_random.dinero += precio * 2

                    # Registrar transacción
                    mercado.registrar_transaccion(
                        mercado.gobierno, bien_random, 2, precio * 2, mercado.ciclo_actual
                    )
