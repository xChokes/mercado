from Persona import Persona
import random
from Accion import Accion

class Empresa(Persona):
    def __init__(self, nombre, bienes, mercado) -> None:
        super().__init__(mercado)
        self.nombre = nombre
        self.bienes = bienes if bienes else {}
        self.dinero = random.randint(1000, 10000)
        self.costos_unitarios = { bien: random.randint(1, 100) for bien in self.bienes.keys()}
        self.demanda = { bien: random.randint(1, 100) for bien in mercado.bienes.keys()}
        self.acciones_emitidas = []
        self.valor_accion = self.dinero / len(self.acciones_emitidas) if len(self.acciones_emitidas) > 0 else 10  # Un valor inicial arbitrario
        self.umbral_alto = random.randint(80, 120)  # Umbral alto dinámico
        self.umbral_bajo = random.randint(30, 70)   # Umbral bajo dinámico
        self.factor_incremento = random.uniform(0.1, 0.25)  # Factor de incremento aleatorio
        self.factor_decremento = random.uniform(0.1, 0.25)  # Factor de decremento aleatorio
        self.precios = {bien: random.randint(1, 100) for bien in self.bienes.keys()}
    
    def ajustar_precio_bien(self, mercado, nombre_bien):
        ventas = mercado.getRegistroTransacciones()
        if len(ventas) == 0:
            self.precios[nombre_bien] *= (1 + random.uniform(-0.01, 0.01))  # Ajuste de precios aleatorio
            return
        ventas = sum([venta['cantidad'] for venta in ventas if venta['bien'] == nombre_bien])

        stock_actual = self.bienes[nombre_bien]  # Asumiendo que 'bienes' representa el stock disponible

        costo_unitario = self.costos_unitarios[nombre_bien]
        antiguoprecio = self.precios[nombre_bien]
        # Ajusta el precio sobre el coste unitario
        self.precios[nombre_bien] = costo_unitario * (1 + random.uniform(0.05, 0.15))

        # Reemplaza Empresa.umbral_alto/bajo y Empresa.factor_incremento/decremento por los atributos de la instancia
        if ventas > self.umbral_alto and stock_actual > 0:
            self.precios[nombre_bien] *= (1 + self.factor_incremento)
        elif ventas < self.umbral_bajo:
            self.precios[nombre_bien] *= (1 - self.factor_decremento)
        else:
            self.precios[nombre_bien] *= (1 + random.uniform(-0.01, 0.01))  # Ajuste de precios aleatorio

        print(f"Empresa {self.nombre} ajustando precio de {nombre_bien} de {antiguoprecio} a {self.precios[nombre_bien]}, diferencia: {self.precios[nombre_bien] - antiguoprecio}")
    
    def emitir_acciones(self, cantidad, mercado_financiero):
        # Determinar el precio por acción basado en el capital y las acciones emitidas
        if len(self.acciones_emitidas) > 0:
            self.valor_accion = self.dinero / max(len(self.acciones_emitidas), 1) 
        else:
            self.valor_accion = 10

        for _ in range(cantidad):
            accion = Accion(self.nombre, 1, 1, self.nombre, len(mercado_financiero.acciones)+1)
            self.acciones_emitidas.append(accion)
            mercado_financiero.acciones[accion.id] = accion
    
    def actualizar_costos(self):
        # Las empresas ajustan sus costos, por ejemplo, debido a la tecnología o la eficiencia
        for bien in self.costos_unitarios:
            self.costos_unitarios[bien] *= 1 + random.uniform(-0.01, 0.01)  # Ajuste de costos aleatorio

    @classmethod
    def crear_con_acciones(cls, nombre, bienes, mercado, cantidad_acciones):
        empresa = cls(nombre, bienes, mercado)
        empresa.actualizar_costos()
        empresa.emitir_acciones(cantidad_acciones, mercado.mercado_financiero)
        return empresa

    def __str__(self) -> str:
        return f"Empresa {self.nombre} con bienes {self.bienes}, dinero {self.dinero}, costos unitarios {self.costos_unitarios}, demanda {self.demanda}, acciones emitidas {len(self.acciones_emitidas)}, valor accion {self.valor_accion}, umbral alto {self.umbral_alto}, umbral bajo {self.umbral_bajo}, factor incremento {self.factor_incremento}, factor decremento {self.factor_decremento}"