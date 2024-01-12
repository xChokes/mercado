import random
class Persona:
    def __init__(self, mercado) -> None:
        self.dinero = 0
        self.bienes = {}
        self.demanda = []
        self.habilidad_negociacion = random.uniform(0.75,1.25)
        self.cartera_acciones = []
        self.cartera_bienes = []
        self.preferencias = {bien: random.randint(1, 100) for bien in mercado.bienes.keys()}

    def actualizar_ingresos(self):
        self.dinero += random.randint(100, 1000)
    
    def getPreferencias(self):
        return self.preferencias