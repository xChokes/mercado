import random
from InventarioBien import InventarioBien
class Persona:
    def __init__(self, mercado) -> None:
        self.dinero = 0
        self.bienes = {} # Bienes en posesion, formato: {'NombreBien': cantidad}
        self.demanda = [] # Bienes que se desean comprar, formato: [{'NombreBien': cantidad}]
        self.habilidad_negociacion = random.uniform(0.75,1.25)  # Habilidad de negociación aleatoria
        self.cartera_acciones = {} # Cartera de acciones, formato: {'NombreEmpresa': cantidad_acciones}
        print(mercado)
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
        # Usar agregarBien
        self.agregarBien(bien, precio, mercado)
        
        mercado.registrar_transaccion(self, bien, cantidad, precio * cantidad, ciclo)
        self.preferencias[bien] *= max(0.1, (1 - 0.1 * cantidad))
        empresa.dinero += precio * cantidad
        for _ in range(cantidad):
            sortedbienes = {k: v for k, v in sorted(empresa.bienes.items(), key=lambda item: item[1])}
            print(sortedbienes)
        print(f"Consumidor {self.nombre} comprando {cantidad} {bien} de {empresa.nombre} a {precio} cada uno")
        return True
    
    def agregarBien(self, nombre, costo, mercado):
        if not self.bienes[nombre]:
            self.bienes[nombre] = []

        self.bienes[nombre].append(InventarioBien(nombre, costo, mercado.bienes))

    def eliminarBien(self, nombre, id):
        if self.bienes[nombre]:
            for bien in self.bienes[nombre]:
                if bien.id == id:
                    self.bienes[nombre].remove(bien)
                    break

    def actualizar_ingresos(self):
        self.dinero += random.randint(500, 2000)
        pass
    
    def getPreferencias(self):
        return self.preferencias