from Empresa import Empresa
import random

from InventarioBien import InventarioBien

class EmpresaProductora(Empresa):
    def __init__(self, nombre,mercado, bienes={}) -> None:
        super().__init__(nombre=nombre, bienes=bienes, mercado=mercado)
        self.costos_unitarios = { bien: random.randint(1, 100) for bien in self.bienes.keys()}
        self.dinero = random.randint(100000, 1000000)

    def ciclo_persona(self, ciclo, mercado):
        print("ESTÁ LLEGANDO")
        self.emitir_acciones(10, mercado.mercado_financiero)
        self.distribuir_dividendos(mercado.mercado_financiero)
        self.actualizar_costos()
        for bien in mercado.bienes:
            
            self.producirBien(bien, 10, mercado)
            self.ajustar_precio_bien(mercado, bien)

    def actualizar_costos(self):
        for bien in self.bienes:
            self.costos_unitarios[bien] = self.costos_unitarios[bien] * random.uniform(0.9, 1.1)

    def ajustar_precio_bien(self, mercado, nombre_bien):
        ventas = sum([venta['cantidad'] for venta in mercado.getRegistroTransacciones() if venta['bien'] == nombre_bien])
        stock_actual = len(self.bienes[nombre_bien])
        elasticidad_demanda = mercado.bienes[nombre_bien].elasticidad_precio

        if nombre_bien not in self.precios:
            self.precios[nombre_bien] = random.randint(1, 100)
            
        precio_actual = self.precios[nombre_bien]
        costo_unitario = self.costos_unitarios[nombre_bien]

        # Calcula el nuevo precio basado en elasticidad de la demanda
        if elasticidad_demanda != 0:
            factor_cambio = 1 - ventas / max(stock_actual, 1)
            cambio_precio = factor_cambio / abs(elasticidad_demanda)
            nuevo_precio = max(precio_actual * (1 + cambio_precio), costo_unitario)
        else:
            print("Elasticidad cero")
            nuevo_precio = precio_actual * (1 + random.uniform(-0.01, 0.01))
        
        self.precios[nombre_bien] = round(nuevo_precio,2)
        print(f"Empresa {self.nombre} ajustó el precio de {nombre_bien} de {precio_actual} a {nuevo_precio}")

    def producirBien(self, bien, cantidad, mercado):
        print(f"Empresa {self.nombre} produjo {cantidad} unidades de {bien}")
        if bien in self.bienes:
            for _ in range(cantidad):
                if bien not in self.costos_unitarios:
                    self.costos_unitarios[bien] = random.randint(1, 100)
                self.bienes[bien].append(InventarioBien(bien, self.costos_unitarios[bien], mercado.bienes))
        else:
            self.bienes[bien] = []
            for _ in range(cantidad):
                if bien not in self.costos_unitarios:
                    self.costos_unitarios[bien] = random.randint(1, 100)
                self.bienes[bien].append(InventarioBien(bien, self.costos_unitarios[bien], mercado.bienes))