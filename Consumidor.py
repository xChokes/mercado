from Empresa import Empresa
from Persona import Persona
import random
class Consumidor(Persona):
    def __init__(self, nombre, mercado, bienes = {}) -> None:
        super().__init__(mercado)
        self.nombre = nombre # Nuevo: nombre del consumidor
        self.bienes = bienes if bienes else {} # Nuevo: bienes en posesión
        self.dinero = random.randint(1000, 10000) # Nuevo: dinero inicial
        self.max_precio = {bien: random.uniform(0.5, 1.5) * self.dinero / 100 for bien in mercado.bienes.keys()}  # Nuevo: precio máximo que el consumidor está dispuesto a pagar
        self.historial_compras = {} # Nuevo: historial de precios de compra de acciones

    def ajustar_preferencias(self):
        for bien in self.preferencias:
            if bien in self.bienes:
                self.preferencias[bien] *= max(0.1, (1 - 0.1 * self.bienes[bien]))  # Ajustado para disminuir con la cantidad comprada
            elif bien not in self.bienes:
                self.preferencias[bien] *= 1.1
    
    def comprar_acciones(self, mercado_financiero, nombre_empresa, cantidad):
        if nombre_empresa in mercado_financiero.acciones:
            total_acciones, precio_actual = mercado_financiero.acciones[nombre_empresa]
            costo_total = precio_actual * cantidad
            if self.dinero >= costo_total and cantidad <= total_acciones:
                self.dinero -= costo_total
                self.cartera_acciones[nombre_empresa] = self.cartera_acciones.get(nombre_empresa, 0) + cantidad
                self.historial_compras[nombre_empresa] = precio_actual
                # Actualizar el mercado financiero según sea necesario
                print(f"{self.nombre} compró {cantidad} acciones de {nombre_empresa.nombre}")
                return True
            else:
                print(f"No es posible realizar la compra")
                return False
        else:
            print(f"Acciones de {nombre_empresa} no disponibles en el mercado")
            return False

    def vender_acciones(self, mercado_financiero, nombre_empresa, cantidad):
        if nombre_empresa in self.cartera_acciones:
            if cantidad <= self.cartera_acciones[nombre_empresa]:
                self.cartera_acciones[nombre_empresa] -= cantidad
                self.dinero += mercado_financiero.acciones[nombre_empresa][1] * cantidad
                # Actualizar el mercado financiero según sea necesario
                print(f"{self.nombre} vendió {cantidad} acciones de {nombre_empresa}")
                return True
            else:
                print(f"No es posible realizar la venta")
                return False
        else:
            print(f"No se poseen acciones de {nombre_empresa}")
            return False

    def __str__(self):
        return f"Nombre: {self.nombre} - Dinero: {self.dinero} - Bienes: {self.bienes}"
    
    def decidir_acciones(self, mercado_financiero, registrar, ciclo):
        # Ejemplo: Decidir comprar acciones basado en alguna lógica
        for nombre_empresa, (cantidad_acciones, precio_accion) in mercado_financiero.acciones.items():
            if self.deberia_comprar_acciones(mercado_financiero.acciones):
                cantidad_a_comprar = self.calcular_cantidad_compra(precio_accion)
                if self.comprar_acciones(mercado_financiero, nombre_empresa, cantidad_a_comprar):
                    nombre_empresa_str = nombre_empresa.nombre if isinstance(nombre_empresa, Empresa) else nombre_empresa
                    registrar(self, 'Accion ' + nombre_empresa_str, cantidad_a_comprar, precio_accion * cantidad_a_comprar, ciclo)

        # Similarmente, decidir vender acciones
        for nombre_empresa, cantidad_acciones in self.cartera_acciones.items():
            if self.deberia_vender_acciones(nombre_empresa, mercado_financiero.acciones):
                cantidad_a_vender = self.calcular_cantidad_venta(cantidad_acciones)
                if self.vender_acciones(mercado_financiero, nombre_empresa, cantidad_a_vender):
                    registrar(self, 'Vender Accion ' + nombre_empresa, -cantidad_a_vender, mercado_financiero.acciones[nombre_empresa][1] * cantidad_a_vender, ciclo)

    def deberia_comprar_acciones(self, acciones):
        # Ejemplo de lógica: comprar si tiene suficiente liquidez y desea diversificar
        umbral_liquidez = random.uniform(100, 500)  # Ejemplo: umbral entre 100 y 500
        liquidez = self.dinero
        empresas_interes = [nombre for nombre, _ in acciones.items() if nombre not in self.cartera_acciones]
        return liquidez > umbral_liquidez and len(empresas_interes) > 0

    def calcular_cantidad_compra(self, precio_accion):
        # Ejemplo: compra una cantidad que no supere un porcentaje de su liquidez
        porcentaje_inversion = random.uniform(0.05, 0.15)  # Ejemplo: invertir entre 5% y 15% de la liquidez
        cantidad_maxima = self.dinero * porcentaje_inversion / precio_accion
        cantidad_a_comprar = random.randint(1, max(1, int(cantidad_maxima)))  # Asegura al menos comprar 1 acción
        return cantidad_a_comprar

    def deberia_vender_acciones(self, nombre_empresa, acciones):
        # Ejemplo: vender si el precio de la acción ha aumentado significativamente
        umbral_incremento = random.uniform(1.1, 1.5)  # Ejemplo: incremento del 10% al 50%
        precio_compra = self.historial_compras[nombre_empresa]  # Supone un registro de precios de compra
        precio_actual = acciones[nombre_empresa][1]
        return precio_actual > precio_compra * umbral_incremento
    
    def calcular_cantidad_venta(self, cantidad_acciones):
        # Ejemplo: vender un porcentaje de las acciones en posesión
        porcentaje_venta = random.uniform(0.2, 0.5)  # Ejemplo: vender entre el 20% y el 50% de las acciones
        cantidad_a_vender = max(1, int(cantidad_acciones * porcentaje_venta))  # Asegura vender al menos 1 acción
        return cantidad_a_vender