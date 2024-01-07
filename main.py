import random
import time
import matplotlib.pyplot as plt


class Bien:
    def __init__(self, nombre, elasticidad_precio, elasticidad_ingreso):
        self.nombre = nombre
        self.elasticidad_precio = elasticidad_precio
        self.elasticidad_ingreso = elasticidad_ingreso
    
    def __str__(self):
        return f"Nombre: {self.nombre} - Elasticidad precio: {self.elasticidad_precio} - Elasticidad ingreso: {self.elasticidad_ingreso}"

class Persona:
    def __init__(self, mercado) -> None:
        self.dinero = 0
        self.bienes = {}
        self.demanda = []
        self.habilidad_negociacion = random.uniform(0.75,1.25)
        self.cartera_acciones = []
        self.cartera_bienes = []
        self.preferencias = {bien.nombre: random.randint(1, 100) for bien in mercado.bienes}

    def actualizar_ingresos(self):
        self.dinero += random.randint(100, 1000)

    def comprar_bien(self, mercado, bien, cantidad) -> bool:
        precio = mercado.precios[bien]
        if self.dinero < precio * cantidad:
            return False
        self.dinero -= precio * cantidad
        self.bienes[bien.nombre] += cantidad
        mercado.registrar_transaccion(self, bien.nombre, cantidad, precio * cantidad)
        self.preferencias[bien.nombre] *= max(0.1, (1-0.1*cantidad))
        return True
   
class Consumidor(Persona):
    def __init__(self, nombre, bienes, mercado) -> None:
        super().__init__(mercado)
        self.nombre = nombre
        self.bienes = bienes if bienes else {}
        self.dinero = random.randint(100, 1000)

    def ajustar_preferencias(self):
        for bien in self.preferencias:
            if bien not in self.bienes:
                self.preferencias[bien] *= 1.1
            else:
                self.preferencias[bien] /= max(0.1, 1-self.bienes[bien])

    def __str__(self):
        return f"Nombre: {self.nombre} - Dinero: {self.dinero} - Bienes: {self.bienes}"

class Accion(Bien):
    def __init__(self, nombre, elasticidad_precio, elasticidad_ingreso, empresa, nombreAccion):
        super().__init__(nombre, elasticidad_precio, elasticidad_ingreso)
        self.id = nombreAccion
        self.empresa = empresa

    def __str__(self):
        return f"Accion de {self.empresa.nombre}"

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
        self.costos_unitarios = { bien.nombre: random.randint(1, 100) for bien in self.bienes}
        self.demanda = { bien.nombre: random.randint(1, 100) for bien in mercado.bienes}
        self.oferta = { bien.nombre: random.randint(1, 100) for bien in self.bienes}
        self.acciones_emitidas = []
        self.valor_accion = self.dinero / len(self.acciones_emitidas) if len(self.acciones_emitidas) > 0 else 10  # Un valor inicial arbitrario

    def actualizar_oferta(self, bienes, precios):
        oferta_total = 0
        for bien in bienes:
            if bien.nombre not in self.costos_unitarios:
                continue
            precio = precios[bien.nombre]
            oferta_bien = max(0, precio - self.costos_unitarios[bien.nombre])
            self.oferta[bien.nombre] = oferta_bien
            oferta_total += oferta_bien
        return oferta_total
    
    def ajustar_precio_bien(self, mercado, nombre_bien):
        ventas = mercado.ventas_bien(nombre_bien)
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
    
class MercadoFinanciero:
    def __init__(self) -> None:
        self.acciones = {}

    def comprar_acciones(self, accion):
        if accion.id in self.acciones:
            del self.acciones[accion.id]
            return True
        return False

class Mercado:
    def __init__(self, bienes) -> None:
        self.bienes = bienes if bienes else {}
        self.personas = []
        self.precios = { bien.nombre: random.randint(1, 100) for bien in bienes}
        self.mercado_financiero = MercadoFinanciero()
        self.transacciones = []

    def agregar_persona(self, persona):
        self.personas.append(persona)

    def encontrar_equilibrio(self, precio_min, precio_max, tolerancia):
        precios_teoricos = {}
        demanda_teorica_total = {}
        oferta_teorica_total = {}
        exceso_demanda = {}
        exceso_oferta = {}

        for bien in self.bienes:
            precios_teoricos[bien.nombre] = (precio_min + precio_max) / 2
            demanda_teorica_total[bien.nombre] = 0
            oferta_teorica_total[bien.nombre] = 0

            # Calcula demanda teórica y oferta teórica
            for consumidor in self.getConsumidores():
                preferencia = consumidor.preferencias[bien.nombre]
                precio_teorico = precios_teoricos[bien.nombre]
                dinero_disponible = consumidor.dinero
                cantidad_demandada = preferencia * dinero_disponible / max(precio_teorico, 1)  # Evita división por cero
                demanda_teorica_total[bien.nombre] += cantidad_demandada

            # Calcula oferta teórica
            for empresa in self.getEmpresas():
                if bien.nombre in empresa.oferta:
                    oferta_teorica_total[bien.nombre] += empresa.oferta[bien.nombre]

            # Calcula el exceso de demanda
            exceso_demanda[bien.nombre] = demanda_teorica_total[bien.nombre] - oferta_teorica_total[bien.nombre]
            exceso_oferta[bien.nombre] = oferta_teorica_total[bien.nombre] - demanda_teorica_total[bien.nombre]

        return precios_teoricos, demanda_teorica_total, oferta_teorica_total, exceso_demanda, exceso_oferta
        
    def ejecutar_ciclo(self):
        # Actualiza ingresos y preferencias de consumidores
        for consumidor in self.personas:
            if isinstance(consumidor, Empresa):
                continue
            consumidor.actualizar_ingresos()
            consumidor.ajustar_preferencias()
            for bien in mercado.bienes:
                cantidad_compra = consumidor.preferencias[bien.nombre] * consumidor.dinero / self.precios[bien.nombre]
                consumidor.comprar_bien(mercado, bien.nombre, cantidad_compra)

        for empresa in self.personas:
            if isinstance(empresa, Consumidor):
                continue
            empresa.emitir_acciones(10, self.mercado_financiero)
            empresa.actualizar_costos()
            empresa.actualizar_oferta(self.bienes, self.precios)
            print(f"La empresa {empresa.nombre} tiene los siguientes bienes:")
            for bien in empresa.bienes:
                print(f"{bien.nombre}: {empresa.bienes[bien.nombre]}")

        # Encuentra el nuevo equilibrio con los precios actualizados
        # precios, demanda_total, oferta_total = self.encontrar_equilibrio(precio_min=0, precio_max=1000, tolerancia=0.01)

        # return precios, demanda_total, oferta_total

    def getDineroConsumidores(self):
        return [c.dinero for c in self.personas if isinstance(c, Consumidor)]
    
    def getDineroEmpresas(self):
        return [e.dinero for e in self.personas if isinstance(e, Empresa)]
    
    def getConsumidores(self):
        return [c for c in self.personas if isinstance(c, Consumidor)]
    
    def getEmpresas(self):
        return [e for e in self.personas if isinstance(e, Empresa)]
    
    def registrar_transaccion(self, consumidor, nombre_bien, cantidad, costo_total):
        self.transacciones.append({
            'consumidor': consumidor.nombre,
            'bien': nombre_bien,
            'cantidad': cantidad,
            'costo_total': costo_total
        })
    

if __name__ == "__main__":
    bienes = [
        Bien("Arroz", 0.5, 0.5),
        Bien("Carne", 0.5, 0.5),
        Bien("Papa", 0.5, 0.5),
        Bien("Leche", 0.5, 0.5),
        Bien("Huevos", 0.5, 0.5),
        Bien("Pan", 0.5, 0.5),
        Bien("Cerveza", 0.5, 0.5),
        Bien("Cigarrillos", 0.5, 0.5),
        Bien("Computador", 0.5, 0.5),
        Bien("Celular", 0.5, 0.5),
        Bien("Carro", 0.5, 0.5),
        Bien("Moto", 0.5, 0.5),
        Bien("Viaje", 0.5, 0.5),
        Bien("Hotel", 0.5, 0.5),
        Bien("Gimnasio", 0.5, 0.5)]
    
    mercado = Mercado(bienes)
    for _ in range(1000):
        nombre_consumidor = "Consumidor" + str(_)
        mercado.agregar_persona(Consumidor(nombre_consumidor, bienes, mercado))
        print("Agregado consumidor nº ", _)

    for _ in range(100):
        nombre_empresa = "Empresa" + str(_)
        empresa = Empresa.crear_con_acciones(nombre_empresa, bienes, mercado, 10)
        mercado.agregar_persona(empresa)
        print("Agregada empresa nº ", _)


    num_ciclos = 10
    init = time.time()

    # Listas para almacenar totales
    demanda_total_por_ciclo = []
    oferta_total_por_ciclo = []
    exceso_demanda_total_por_ciclo = []
    exceso_oferta_total_por_ciclo = []

    for ciclo in range(num_ciclos):
        print(f"Ciclo {ciclo+1}")
        mercado.ejecutar_ciclo()

        precios_teoricos, demanda_teorica_total, oferta_teorica_total, exceso_demanda, exceso_oferta = mercado.encontrar_equilibrio(precio_min=0, precio_max=1000, tolerancia=0.01)
        
        # Calcular totales para el ciclo actual
        demanda_total_ciclo = sum(demanda_teorica_total.values())
        oferta_total_ciclo = sum(oferta_teorica_total.values())
        exceso_demanda_total_ciclo = sum(exceso_demanda.values())
        exceso_oferta_total_ciclo = sum(exceso_oferta.values())

        # Almacenar los totales en las listas
        demanda_total_por_ciclo.append(demanda_total_ciclo)
        oferta_total_por_ciclo.append(oferta_total_ciclo)
        exceso_demanda_total_por_ciclo.append(exceso_demanda_total_ciclo)
        exceso_oferta_total_por_ciclo.append(exceso_oferta_total_ciclo)

    tiempo_ejecucion = time.time() - init

    # Gráficas
    plt.figure()
    plt.plot(demanda_total_por_ciclo, label='Demanda Total')
    plt.plot(oferta_total_por_ciclo, label='Oferta Total')
    plt.plot(exceso_demanda_total_por_ciclo, label='Exceso de Demanda Total')
    plt.plot(exceso_oferta_total_por_ciclo, label='Exceso de Oferta Total')
    plt.legend()
    plt.show()

    print(f"Tiempo de ejecución: {tiempo_ejecucion} segundos")
    print("Fin del programa")