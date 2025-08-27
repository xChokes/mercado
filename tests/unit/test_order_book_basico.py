import pytest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.systems.OrderBook import OrderBook


def test_spread_positivo_y_profundidad():
    ob = OrderBook('Arroz')
    ob.submit('bid', price=9.0, qty=10, agent='C1')
    ob.submit('ask', price=10.0, qty=5, agent='E1')

    assert ob.best_bid().price == 9.0
    assert ob.best_ask().price == 10.0
    assert ob.spread() > 0
    assert ob.depth('bid') == 10
    assert ob.depth('ask') == 5

    # Al aumentar volumen en un lado, la profundidad debe aumentar
    ob.submit('bid', price=8.5, qty=20, agent='C2')
    assert ob.depth('bid') == 30

    # Si agregamos una ask que cruza el mercado, se ejecuta y reduce profundidad
    ob.submit('ask', price=8.0, qty=7, agent='E2')
    trades = ob.match()
    assert sum(t['qty'] for t in trades) == 7
    assert ob.depth('bid') == 23