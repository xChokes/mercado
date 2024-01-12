from Persona import Persona
import random
class Consumidor(Persona):
    def __init__(self, nombre, mercado, bienes = {}) -> None:
        super().__init__(mercado)
        self.nombre = nombre
        self.bienes = bienes if bienes else {}
        self.dinero = random.randint(100, 1000)
        self.max_precio = {bien: random.uniform(0.5, 1.5) * self.dinero / 100 for bien in mercado.bienes.keys()}  # Nuevo

    def ajustar_preferencias(self):
        for bien in self.preferencias:
            if bien in self.bienes:
                self.preferencias[bien] *= max(0.1, (1 - 0.1 * self.bienes[bien]))  # Ajustado para disminuir con la cantidad comprada
            elif bien not in self.bienes:
                self.preferencias[bien] *= 1.1

    def comprar_bien(self, empresa, bien, cantidad, mercado) -> bool:
        precio = empresa.precios[bien]
        if self.dinero < precio * cantidad or precio > self.max_precio[bien]:  # Nuevo: revisa el precio máximo que el consumidor está dispuesto a pagar
            return False
        
        self.dinero -= precio * cantidad
        empresa.dinero += precio * cantidad
        if bien not in self.bienes:
            self.bienes[bien] = 0

        self.bienes[bien] += cantidad
        mercado.registrar_transaccion(self, bien, cantidad, precio * cantidad)
        self.preferencias[bien] *= max(0.1, (1 - 0.1 * cantidad))
        empresa.dinero += precio * cantidad
        empresa.bienes[bien] -= cantidad
        print(f"Consumidor {self.nombre} comprando {cantidad} {bien} de {empresa.nombre} a {precio} cada uno")
        return True

    def __str__(self):
        return f"Nombre: {self.nombre} - Dinero: {self.dinero} - Bienes: {self.bienes}"