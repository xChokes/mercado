import pytest

from src.models.Mercado import Mercado
from src.models.Empresa import Empresa
from src.systems.MercadoCapitales import BolsaValores


def test_bolsa_inicializa_y_lista_empresas():
    bienes = { 'Arroz': object(), 'Energia': object() }
    mercado = Mercado(bienes)

    e1 = Empresa('Comercial_1', mercado, bienes={'Arroz': []})
    e2 = Empresa('Productora_1', mercado, bienes={'Arroz': []})
    mercado.agregar_persona(e1)
    mercado.agregar_persona(e2)

    bolsa = BolsaValores(mercado)
    bolsa.listar_empresas()

    assert len(bolsa.acciones) >= 2
    reporte = bolsa.ejecutar_ciclo_bursatil(1)
    assert 'indices' in reporte
