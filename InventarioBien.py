class InventarioBien:
    def __init__(self, nombre, costo, bienesmercado) -> None:
        if nombre not in bienesmercado:
            return
        self.id = id(self)
        self.nombre = nombre
        self.costo = costo