class MercadoFinanciero:
    def __init__(self) -> None:
        self.acciones = {}

    def comprar_acciones(self, accion):
        if accion.id in self.acciones:
            del self.acciones[accion.id]
            return True
        return False