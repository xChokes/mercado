import random
from InventarioBien import InventarioBien
class Persona:
    def __init__(self, mercado) -> None:
        self.dinero = 0
        self.bienes = {} # Bienes en posesion, formato: {'NombreBien': cantidad}
        self.demanda = [] # Bienes que se desean comprar, formato: [{'NombreBien': cantidad}]
        self.habilidad_negociacion = random.uniform(0.75,1.25)  # Habilidad de negociación aleatoria
        self.cartera_acciones = {} # Cartera de acciones, formato: {'NombreEmpresa': cantidad_acciones}
        self.max_precio = {bien: random.uniform(0.5, 1.5) * self.dinero / 100 for bien in mercado.bienes.keys()}  # Nuevo: precio máximo que el consumidor está dispuesto a pagar
        self.preferencias = {bien: random.randint(1, 100) for bien in mercado.bienes.keys()} # Preferencias de compra, formato: {'NombreBien': preferencia}
        self.riesgoCompra = random.uniform(0, 1) # Riesgo de compra aleatorio POR IMPLEMENTAR #############################################################
        self.riesgoVenta = random.uniform(0, 1) # Riesgo de venta aleatorio POR IMPLEMENTAR #############################################################
        
    def decidir_compra(self, mercado, ciclo):
        preferencias = self.getPreferencias()
        sortedprefdict = {k: v for k, v in sorted(preferencias.items(), key=lambda item: item[1])}
        for bien in sortedprefdict:
            if preferencias[bien] > 0:
                empresas = [empresa for empresa in mercado.getEmpresas() if bien in empresa.bienes]
                empresas.sort(key=lambda empresa: empresa.precios[bien])
                for empresa in empresas:
                    cantidad = self.preferencias[bien] * self.dinero / (2 * empresa.precios[bien])
                    if cantidad > 0:
                        if len(empresa.bienes[bien]) > 0:
                            dineroAntes = self.dinero
                            dineroAntes2 = empresa.dinero
                            if self.comprar_bien(empresa=empresa, bien=bien, cantidad=1, mercado=mercado, ciclo=ciclo):
                                dineroDespues = self.dinero
                                dineroDespues2 = empresa.dinero
                                print(f"La empresa {empresa.nombre} ha pasado de tener {dineroAntes2} a {dineroDespues2} y el consumidor {self.nombre} ha pasado de tener {dineroAntes} a {dineroDespues}")
                                break
                            else:
                                print(f"La empresa {empresa.nombre} no ha podido venderle al consumidor {self.nombre}")
                        else:
                            print(f"La empresa {empresa.nombre} no tiene stock de {bien}")
                    else:
                        print(f"El consumidor {self.nombre} no tiene dinero para comprar {bien}")
                else:
                    print(f"Ninguna empresa vende {bien}")
            else:
                print(f"El consumidor {self.nombre} no quiere comprar {bien}")

    def comprar_bien(self, empresa, bien, cantidad, mercado, ciclo) -> bool:
        precio = empresa.precios[bien]
        print(f"El consumidor {self.nombre} está dispuesto a pagar {self.max_precio[bien]} por {bien}")
        print(self.max_precio)
        if self.dinero < precio * cantidad :  # Nuevo: revisa el precio máximo que el consumidor está dispuesto a pagar
            return False
        
        self.dinero -= precio * cantidad
        if bien not in self.bienes:
            self.bienes[bien] = 0
        # Usar agregarBien
        self.agregarBien(bien, precio, mercado)
        
        mercado.registrar_transaccion(self, bien, cantidad, precio * cantidad, ciclo)
        self.preferencias[bien] *= max(0.1, (1 - 0.1 * cantidad))
        empresa.dinero += precio * cantidad
        if bien not in empresa.ventasPorBienPorCiclo:
            empresa.ventasPorBienPorCiclo[bien] = {}
        if ciclo not in empresa.ventasPorBienPorCiclo[bien]:
            empresa.ventasPorBienPorCiclo[bien][ciclo] = 0
        empresa.ventasPorBienPorCiclo[bien][ciclo] += cantidad
        for _ in range(cantidad):
            sortedbienes = {k: v for k, v in sorted(empresa.bienes.items(), key=lambda item: item[1])}
            for bien in sortedbienes:
                if len(sortedbienes[bien]) > 0:
                    empresa.eliminarBien(bien, sortedbienes[bien][0].id)
                    break
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