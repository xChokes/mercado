import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.models.Mercado import Mercado
from src.models.Bien import Bien
from src.models.Empresa import Empresa
from src.models.Consumidor import Consumidor


def _setup_mercado_simple():
    bienes = { 'Arroz': Bien('Arroz', 'alimentos_basicos') }
    m = Mercado(bienes)
    e = Empresa('E1', m, bienes={'Arroz': [1]*20})
    c = Consumidor('C1', m)
    c.dinero = 1000
    m.agregar_persona(e)
    m.agregar_persona(c)
    e.precios['Arroz'] = 10.0
    return m, e, c


def test_spread_y_ejecucion_matching():
    m, e, c = _setup_mercado_simple()
    # empresa publica ask, consumidor publica bid
    m.enviar_orden('ask', 'Arroz', 10.0, 5, e.nombre)
    m.enviar_orden('bid', 'Arroz', 9.0, 5, c.nombre)
    ob = m.order_books.get('Arroz')
    assert ob.spread() == 1.0

    # Ahora consumidor mejora bid y cruza
    m.enviar_orden('bid', 'Arroz', 10.0, 3, c.nombre)
    m.ejecutar_matching()

    # Debe haberse ejecutado al menos 3 unidades
    assert c.bienes.get('Arroz', 0) >= 3
    assert c.dinero <= 1000 - 3*10.0