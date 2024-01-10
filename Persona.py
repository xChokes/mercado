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

    def comprar_bien(self, empresa, bien, cantidad, mercado) -> bool:
        precio = empresa.precios[bien]
        if self.dinero < precio * cantidad:
            return False
        self.dinero -= precio * cantidad
        if bien not in self.bienes:
            self.bienes[bien] = 0
        
        self.bienes[bien.nombre] += cantidad
        mercado.registrar_transaccion(self, bien.nombre, cantidad, precio * cantidad)
        self.preferencias[bien.nombre] *= max(0.1, (1-0.1*cantidad))
        return True
    
    def getPreferencias(self):
        return self.preferencias