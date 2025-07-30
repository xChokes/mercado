class InventarioBien:
    def __init__(self, nombre, costo, bienesmercado) -> None:
        if nombre not in bienesmercado:
            return
        self.id = id(self)
        self.nombre = nombre
        self.costo = costo

    def __eq__(self, __value: object) -> bool:
        return self.id == __value.id
    
    def __ne__(self, __value: object) -> bool:
        return self.id != __value.id
    
    def __gt__(self, __value: object) -> bool:
        return self.costo > __value.costo
    
    def __lt__(self, __value: object) -> bool:
        return self.costo < __value.costo
    
    def __ge__(self, __value: object) -> bool:
        return self.costo >= __value.costo
    
    def __le__(self, __value: object) -> bool:
        return self.costo <= __value.costo
    
    def __str__(self) -> str:
        return f"Nombre: {self.nombre}, Costo: {self.costo} ID: {self.id}"