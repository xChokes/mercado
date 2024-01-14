from Persona import Persona
import random

class Empresa(Persona):
    def __init__(self, nombre, bienes, mercado) -> None:
        super().__init__(mercado)
        self.nombre = nombre
        self.bienes = bienes if bienes else {}
        self.dinero = random.randint(9000, 10000)
        self.costos_unitarios = { bien: random.randint(1, 100) for bien in self.bienes.keys()}
        self.acciones_emitidas = 0
        self.valor_accion = 0
        self.umbral_alto = random.randint(80, 120)  # Umbral alto dinámico
        self.umbral_bajo = random.randint(30, 70)   # Umbral bajo dinámico
        self.factor_incremento = random.uniform(0.1, 0.25)  # Factor de incremento aleatorio
        self.factor_decremento = random.uniform(0.1, 0.25)  # Factor de decremento aleatorio
        self.precios = {bien: random.randint(1, 100) for bien in self.bienes.keys()}
    
    def ajustar_precio_bien(self, mercado, nombre_bien):
        ventas = sum([venta['cantidad'] for venta in mercado.getRegistroTransacciones() if venta['bien'] == nombre_bien])
        stock_actual = self.bienes[nombre_bien]
        elasticidad_demanda = mercado.bienes[nombre_bien].elasticidad_precio

        precio_actual = self.precios[nombre_bien]
        costo_unitario = self.costos_unitarios[nombre_bien]

        # Calcula el nuevo precio basado en elasticidad de la demanda
        if elasticidad_demanda != 0:
            factor_cambio = 1 - ventas / max(stock_actual, 1)  # Evita división por cero
            cambio_precio = factor_cambio / abs(elasticidad_demanda)
            nuevo_precio = max(precio_actual * (1 + cambio_precio), costo_unitario)  # Asegura que el precio no caiga por debajo del costo
        else:
            print("Elasticidad cero")
            nuevo_precio = precio_actual * (1 + random.uniform(-0.01, 0.01))  # Ajuste de precios aleatorio en caso de elasticidad cero

        self.precios[nombre_bien] = round(nuevo_precio,2)
        print(f"Empresa {self.nombre} ajustó el precio de {nombre_bien} de {precio_actual} a {nuevo_precio}")
    
    def emitir_acciones(self, cantidad, mercado_financiero):
        # Determinar el precio por acción basado en el capital y las acciones emitidas
        self.valor_accion = round(self.dinero /self.acciones_emitidas) if self.acciones_emitidas > 0 else 10
        # Emitir acciones
        mercado_financiero.emitir_acciones(self, cantidad)
        self.acciones_emitidas += cantidad
        print(f"Empresa {self.nombre} emitió {cantidad} acciones a un valor de {self.valor_accion} cada una")
    
    def actualizar_costos(self):
        # Las empresas ajustan sus costos, por ejemplo, debido a la tecnología o la eficiencia
        for bien in self.costos_unitarios:
            self.costos_unitarios[bien] *= 1 + random.uniform(-0.01, 0.01)  # Ajuste de costos aleatorio

    def distribuir_dividendos(self, mercado_financiero):
        if self.nombre in mercado_financiero.acciones:
            total_acciones, _ = mercado_financiero.acciones[self.nombre]
            if total_acciones > 0:
                dividendo_por_accion = self.calcular_dividendo()  # Suponiendo que existe este método
                for consumidor in mercado_financiero.consumidores_con_acciones(self.nombre):
                    cantidad_acciones = consumidor.cartera_acciones[self.nombre]
                    dividendo_total = dividendo_por_accion * cantidad_acciones
                    consumidor.dinero += dividendo_total
                    print(f"{consumidor.nombre} recibió ${dividendo_total} en dividendos de {self.nombre}")

    def calcular_dividendo(self):
        # Calcula el dividendo por acción
        return 0.1 * self.dinero / self.acciones_emitidas if self.acciones_emitidas > 0 else 0
    
    @classmethod
    def crear_con_acciones(cls, nombre, bienes, mercado, cantidad_acciones):
        empresa = cls(nombre, bienes, mercado)
        empresa.actualizar_costos()
        empresa.emitir_acciones(cantidad_acciones, mercado.mercado_financiero)
        return empresa

    def __str__(self) -> str:
        return f"Empresa {self.nombre} con bienes {self.bienes}, dinero {self.dinero}, costos unitarios {self.costos_unitarios}, precios {self.precios} acciones emitidas {self.acciones_emitidas}, valor accion {self.valor_accion}, umbral alto {self.umbral_alto}, umbral bajo {self.umbral_bajo}, factor incremento {self.factor_incremento}, factor decremento {self.factor_decremento}"