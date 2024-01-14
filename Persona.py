import random
class Persona:
    def __init__(self, mercado) -> None:
        self.dinero = 0
        self.bienes = {} # Bienes en posesion, formato: {'NombreBien': cantidad}
        self.demanda = [] # Bienes que se desean comprar, formato: [{'NombreBien': cantidad}]
        self.habilidad_negociacion = random.uniform(0.75,1.25)  # Habilidad de negociación aleatoria
        self.cartera_acciones = {} # Cartera de acciones, formato: {'NombreEmpresa': cantidad_acciones}
        self.preferencias = {bien: random.randint(1, 100) for bien in mercado.bienes.keys()} # Preferencias de compra, formato: {'NombreBien': preferencia}
        self.riesgoCompra = random.uniform(0, 1) # Riesgo de compra aleatorio POR IMPLEMENTAR #############################################################
        self.riesgoVenta = random.uniform(0, 1) # Riesgo de venta aleatorio POR IMPLEMENTAR #############################################################

    def comprar_bien(self, empresa, bien, cantidad, mercado, ciclo) -> bool:
        precio = empresa.precios[bien]
        if self.dinero < precio * cantidad or precio > self.max_precio[bien]:  # Nuevo: revisa el precio máximo que el consumidor está dispuesto a pagar
            return False
        
        self.dinero -= precio * cantidad
        if bien not in self.bienes:
            self.bienes[bien] = 0

        self.bienes[bien] += cantidad
        mercado.registrar_transaccion(self, bien, cantidad, precio * cantidad, ciclo)
        self.preferencias[bien] *= max(0.1, (1 - 0.1 * cantidad))
        empresa.dinero += precio * cantidad
        empresa.bienes[bien] -= cantidad
        print(f"Consumidor {self.nombre} comprando {cantidad} {bien} de {empresa.nombre} a {precio} cada uno")
        return True

    def actualizar_ingresos(self):
        self.dinero += random.randint(500, 2000)
        pass
    
    def getPreferencias(self):
        return self.preferencias