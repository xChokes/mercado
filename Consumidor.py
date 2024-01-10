from Persona import Persona
import random
class Consumidor(Persona):
    def __init__(self, nombre, bienes, mercado) -> None:
        super().__init__(mercado)
        self.nombre = nombre
        self.bienes = bienes if bienes else {}
        self.dinero = random.randint(100, 1000)

    def ajustar_preferencias(self):
        for bien in self.preferencias:
            if bien not in self.bienes:
                self.preferencias[bien] *= 1.1
            else:
                self.preferencias[bien] /= max(0.1, 1-self.bienes[bien])

    def __str__(self):
        return f"Nombre: {self.nombre} - Dinero: {self.dinero} - Bienes: {self.bienes}"