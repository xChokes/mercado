from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
import time


@dataclass(order=True)
class Order:
    sort_index: Tuple[float, float, int] = field(init=False, repr=False)
    id: int
    side: str  # 'bid' or 'ask'
    bien: str
    price: float
    qty: int
    agent: str  # nombre del agente (consumidor o empresa)
    ts: float = field(default_factory=lambda: time.time())

    def __post_init__(self):
        # price-time priority; for bids: higher price first; for asks: lower price first
        # sort_index se establecerá dinámicamente por el order book al insertar
        self.sort_index = (0.0, self.ts, self.id)


class OrderBook:
    """Libro de órdenes simple con prioridad precio-tiempo.

    - Mantiene dos listas: bids (desc) y asks (asc)
    - Inserta órdenes manteniendo estabilidad temporal para mismo precio
    - Matching por límite: ejecuta mientras mejor bid >= mejor ask
    """

    def __init__(self, bien: str):
        self.bien = bien
        self.bids: List[Order] = []
        self.asks: List[Order] = []
        self._oid_seq = 0

    def _next_id(self) -> int:
        self._oid_seq += 1
        return self._oid_seq

    def best_bid(self) -> Optional[Order]:
        return self.bids[0] if self.bids else None

    def best_ask(self) -> Optional[Order]:
        return self.asks[0] if self.asks else None

    def spread(self) -> Optional[float]:
        bb = self.best_bid()
        ba = self.best_ask()
        if bb and ba:
            return max(0.0, ba.price - bb.price)
        return None

    def depth(self, side: str) -> int:
        """Devuelve profundidad total (suma de cantidades) para un lado."""
        if side == 'bid':
            return sum(o.qty for o in self.bids)
        return sum(o.qty for o in self.asks)

    def submit(self, side: str, price: float, qty: int, agent: str) -> Order:
        assert side in ('bid', 'ask')
        if qty <= 0 or price <= 0:
            raise ValueError("Orden inválida: qty y price deben ser > 0")
        oid = self._next_id()
        order = Order(id=oid, side=side, bien=self.bien, price=float(price), qty=int(qty), agent=agent)

        # definir sort_index según lado
        if side == 'bid':
            # mayor precio primero -> usar negativo para ordenar ascendente
            order.sort_index = (-order.price, order.ts, order.id)
            self._insert_order(order, self.bids)
        else:
            # menor precio primero
            order.sort_index = (order.price, order.ts, order.id)
            self._insert_order(order, self.asks)
        return order

    def _insert_order(self, order: Order, book_side: List[Order]):
        # inserción ordenada por sort_index (lista pequeña -> búsqueda lineal suficiente)
        idx = 0
        n = len(book_side)
        while idx < n and book_side[idx].sort_index <= order.sort_index:
            idx += 1
        book_side.insert(idx, order)

    def match(self) -> List[Dict]:
        """Ejecuta matching y devuelve lista de trades ejecutados.

        Cada trade: {
            'bien', 'price', 'qty', 'buyer', 'seller', 'ts'
        }
        El ajuste de balances/inventarios debe ocurrir fuera (Mercado.execute_trade).
        """
        trades: List[Dict] = []
        while self.bids and self.asks:
            bid = self.bids[0]
            ask = self.asks[0]
            if bid.price < ask.price:
                break  # no hay cruce de precios

            # Ejecutar al precio del ask (price-time priority típica)
            qty = min(bid.qty, ask.qty)
            trade_price = ask.price
            trades.append({
                'bien': self.bien,
                'price': trade_price,
                'qty': qty,
                'buyer': bid.agent,
                'seller': ask.agent,
                'ts': time.time()
            })

            bid.qty -= qty
            ask.qty -= qty
            if bid.qty == 0:
                self.bids.pop(0)
            if ask.qty == 0:
                self.asks.pop(0)

        return trades


class OrderBookManager:
    """Gestor de libros por bien."""

    def __init__(self):
        self.books: Dict[str, OrderBook] = {}

    def get(self, bien: str) -> OrderBook:
        if bien not in self.books:
            self.books[bien] = OrderBook(bien)
        return self.books[bien]

    def submit(self, bien: str, side: str, price: float, qty: int, agent: str):
        return self.get(bien).submit(side, price, qty, agent)

    def match_all(self) -> Dict[str, List[Dict]]:
        resultados: Dict[str, List[Dict]] = {}
        for bien, ob in self.books.items():
            trades = ob.match()
            if trades:
                resultados[bien] = trades
        return resultados
