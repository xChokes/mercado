from Empresa import Empresa
import random

class EmpresaProductora(Empresa):
    def __init__(self, nombre,mercado, bienes={}) -> None:
        print(mercado.bienes)
        super().__init__(nombre=nombre, bienes=bienes, mercado=mercado)

    def actualizar_costos(self):
        for bien in self.bienes:
            self.costos[bien] = self.costos[bien] * random.uniform(0.9, 1.1)

    def producirBien(self, bien, cantidad):
        if bien in self.bienes:
            self.bienes[bien] += cantidad
            self.dinero -= self.costos[bien] * cantidad
            return True
        else:
            return False