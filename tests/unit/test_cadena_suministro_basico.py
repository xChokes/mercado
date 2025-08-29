import pytest

from src.models.Mercado import Mercado
from src.models.Empresa import Empresa
from src.systems.CadenaSuministro import GestorCadenaSuministro


def test_cadena_inicializa_y_abastece_minimo():
    bienes = { 'Materias_Primas': object(), 'Energia': object(), 'Arroz': object() }
    mercado = Mercado(bienes)

    # Crear dos empresas: proveedor con stock y comprador sin stock
    proveedor = Empresa('Proveedor', mercado, bienes={'Materias_Primas': []})
    proveedor.dinero = 100000
    # stock del proveedor
    proveedor.bienes['Materias_Primas'] = [1]*50
    proveedor.precios['Materias_Primas'] = 10

    comprador = Empresa('Comprador', mercado, bienes={'Materias_Primas': []})
    comprador.dinero = 1000

    mercado.agregar_persona(proveedor)
    mercado.agregar_persona(comprador)

    cadena = GestorCadenaSuministro(mercado)
    cadena.inicializar_red()

    # Forzar umbral bajo para que compre
    cadena.umbral_reabastecimiento = 5
    cadena.nivel_objetivo_insumo = 10
    cadena.max_compra_por_ciclo = 5

    # Asegurar que el comprador tenga declarado el insumo
    comprador.insumos_requeridos['Materias_Primas'] = {'consumo_por_unidad': 1}
    comprador.inventario_insumos['Materias_Primas'] = 0

    mercado.ciclo_actual = 1
    cadena.ciclo_cadena()

    assert comprador.inventario_insumos['Materias_Primas'] > 0
    assert cadena.pedidos_realizados >= 1
    assert cadena.unidades_abastecidas > 0
