from Persona import Persona
import random
from Accion import Accion

class Empresa(Persona):
    umbral_alto = 100  # Ejemplo de umbral
    umbral_bajo = 50   # Ejemplo de umbral
    factor_incremento = 0.05  # 5% de incremento
    factor_decremento = 0.05  # 5% de decremento
    def __init__(self, nombre, bienes, mercado) -> None:
        super().__init__(mercado)
        self.nombre = nombre
        self.bienes = bienes if bienes else {}
        self.dinero = random.randint(100000, 1000000)
        self.costos_unitarios = { bien: random.randint(1, 100) for bien in self.bienes.keys()}
        self.demanda = { bien: random.randint(1, 100) for bien in mercado.bienes.keys()}
        self.oferta = { bien: random.randint(1, 100) for bien in self.bienes.keys()}
        self.acciones_emitidas = []
        self.valor_accion = self.dinero / len(self.acciones_emitidas) if len(self.acciones_emitidas) > 0 else 10  # Un valor inicial arbitrario
    
    def ajustar_precio_bien(self, mercado, nombre_bien):
        ventas = mercado.getRegistroTransacciones()
        ventas = sum([venta for venta in ventas if venta[0] == self.nombre and venta[1] == nombre_bien])
        costo_unitario = self.costos_unitarios[nombre_bien]

        if ventas > Empresa.umbral_alto and mercado.precios[nombre_bien] > costo_unitario:
            mercado.precios[nombre_bien] *= (1 + Empresa.factor_incremento)
        elif ventas < Empresa.umbral_bajo and mercado.precios[nombre_bien] > costo_unitario:
            mercado.precios[nombre_bien] *= (1 - Empresa.factor_decremento)
    
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

    def __str__(self):
        return f"Nombre: {self.nombre} - Dinero: {self.dinero} - Bienes: {self.bienes} - Costos unitarios: {self.costos_unitarios}"