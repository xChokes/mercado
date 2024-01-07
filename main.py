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
    def __init__(self) -> None:
        self.dinero = 0
        self.bienes = {}
        self.demanda = []
        self.habilidad_negociacion = random.uniform(0.75,1.25)
        self.cartera_acciones = []
        self.cartera_bienes = []

    def actualizar_ingresos(self):
        self.dinero += random.randint(100, 1000)

    def comprar_bien(self, mercado, bien, cantidad) -> bool:
        precio = mercado.precios[bien.nombre]
        if self.dinero < precio * cantidad:
            return False
        self.dinero -= precio * cantidad
        if bien.nombre not in self.bienes:
            self.bienes[bien.nombre] = 0
        self.bienes[bien.nombre] += cantidad
        mercado.registrar_transaccion(self, bien.nombre, cantidad, precio * cantidad)
        return True
    
class Consumidor(Persona):
    def __init__(self, nombre, bienes, mercado) -> None:
        super().__init__()  # Inicializa la clase base
        self.nombre = nombre
        self.bienes = bienes if bienes else {}
        self.dinero = random.randint(100, 1000)
        self.preferencias = {bien.nombre: random.randint(1, 100) for bien in self.bienes}
        self.demanda = {bien.nombre: random.randint(1, 100) for bien in mercado.bienes}
        self.oferta = {bien.nombre: random.randint(1, 100) for bien in self.bienes}

    def actualizar_demanda(self, bienes, precios):
        demanda_total = 0
        for bien in bienes:
            if bien.nombre not in self.preferencias:
                continue
            precio = precios[bien.nombre]
            demanda_bien = self.preferencias[bien.nombre] * (1 - bien.elasticidad_precio * precio)
            demanda_total += demanda_bien
            self.demanda[bien.nombre] = demanda_bien
        return demanda_total

    def ajustar_preferencias(self):
        for bien in self.preferencias:
            self.preferencias[bien] *= 1 + random.uniform(-0.01, 0.01)  # Ajuste de preferencias aleatorio

    def __str__(self):
        return f"Nombre: {self.nombre} - Dinero: {self.dinero} - Bienes: {self.bienes} - Preferencias: {self.preferencias}"
    

class Accion(Bien):
    def __init__(self, nombre, elasticidad_precio, elasticidad_ingreso, empresa, nombreAccion):
        super().__init__(nombre, elasticidad_precio, elasticidad_ingreso)
        self.id = nombreAccion
        self.empresa = empresa

    def __str__(self):
        return f"Accion de {self.empresa.nombre}"

class Empresa(Persona):
    def __init__(self, nombre, bienes, mercado) -> None:
        super().__init__()
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

    def encontrar_equilibrio(self, precio_min, precio_max, tolerancia): # Algoritmo de bisección
        for bien in self.bienes:
            min_precio, max_precio = precio_min, precio_max
            while max_precio - min_precio > tolerancia:
                precio_medio = (max_precio + min_precio) / 2
                self.precios[bien.nombre] = precio_medio

                # Calcular demanda y oferta totales en el precio medio
                demanda_total = sum(map(lambda c: c.actualizar_demanda(self.bienes, self.precios), filter(lambda p: isinstance(p, Consumidor), self.personas)))
                oferta_total = sum(map(lambda e: e.actualizar_oferta(self.bienes, self.precios), filter(lambda p: isinstance(p, Empresa), self.personas)))

                if demanda_total > oferta_total:
                    min_precio = precio_medio
                else:
                    max_precio = precio_medio

            self.precios[bien.nombre] = (max_precio + min_precio) / 2

        return self.precios, demanda_total, oferta_total
        
    def ejecutar_ciclo(self):
        # Actualiza ingresos y preferencias de consumidores
        for persona in self.personas:
            if isinstance(persona, Empresa):
                continue
            persona.actualizar_ingresos()
            persona.ajustar_preferencias()

        # Actualiza costos de empresas
        for empresa in self.personas:
            if isinstance(empresa, Consumidor):
                continue
            empresa.actualizar_costos()

        # Encuentra el nuevo equilibrio con los precios actualizados
        precios, demanda_total, oferta_total = self.encontrar_equilibrio(precio_min=0, precio_max=1000, tolerancia=0.01)

        return precios, demanda_total, oferta_total

    def getDineroConsumidores(self):
        return [c.dinero for c in self.personas if isinstance(c, Consumidor)]
    
    def getDineroEmpresas(self):
        return [e.dinero for e in self.personas if isinstance(e, Empresa)]
    
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
        nombreconsumidor = "Consumidor" + str(_)
        mercado.agregar_persona(Consumidor(nombreconsumidor, bienes, mercado))
        print("Agregado consumidor nº ", _)

    for _ in range(100):
        nombreempresa = "Empresa" + str(_)
        empresa = Empresa.crear_con_acciones(nombreempresa, bienes, mercado, 10)
        mercado.agregar_persona(empresa)
        print("Agregada empresa nº ", _)

    num_ciclos = 10
    init = time.time()

    # Listas para almacenar datos
    precios_bienes = {}
    demanda_total_list = []
    exceso_demanda_list = []
    exceso_oferta_list = []
    dinero_medio_consumidores_list = []
    dinero_medio_empresas_list = []
    acciones_emitidas_empresas = {}
    acciones_consumidores = {}

    for ciclo in range(num_ciclos):
        print(f"Ciclo {ciclo}")
        precios, demanda_total, oferta_total = mercado.ejecutar_ciclo()
        for persona in mercado.personas:
            if isinstance(persona, Empresa):
                persona.emitir_acciones(10, mercado.mercado_financiero)

        for bien in mercado.bienes:
            if bien.nombre not in precios_bienes:
                precios_bienes[bien.nombre] = []
            precios_bienes[bien.nombre].append(precios[bien.nombre])

        demanda_total_list.append(demanda_total)
        exceso_demanda_list.append(demanda_total - oferta_total)
        exceso_oferta_list.append(oferta_total - demanda_total)

        dineromedio = mercado.getDineroConsumidores()
        dinero_medio_consumidores_list.append(sum(dineromedio) / len(dineromedio))

        dineromedioempresas = mercado.getDineroEmpresas()
        dinero_medio_empresas_list.append(sum(dineromedioempresas) / len(dineromedioempresas))

        for persona in mercado.personas:
            if isinstance(persona, Empresa):
                if persona.nombre not in acciones_emitidas_empresas:
                    acciones_emitidas_empresas[persona.nombre] = []
                acciones_emitidas_empresas[persona.nombre].append(len(persona.acciones_emitidas))
            else:
                if persona.nombre not in acciones_consumidores:
                    acciones_consumidores[persona.nombre] = []
                acciones_consumidores[persona.nombre].append(len(persona.cartera_acciones))

    tiempo_ejecucion = time.time() - init

    # Ahora puedes usar matplotlib para graficar los datos
    for bien, precios in precios_bienes.items():
        plt.figure()
        plt.plot(precios)
        plt.title(f"Precios de {bien}")
        plt.show()

    plt.figure()
    plt.plot(demanda_total_list)
    plt.title("Demanda total")
    plt.show()

    plt.figure()
    plt.plot(exceso_demanda_list)
    plt.title("Exceso de demanda")
    plt.show()

    plt.figure()
    plt.plot(exceso_oferta_list)
    plt.title("Exceso de oferta")
    plt.show()

    plt.figure()
    plt.plot(dinero_medio_consumidores_list)
    plt.title("Dinero medio de los consumidores")
    plt.show()

    plt.figure()
    plt.plot(dinero_medio_empresas_list)
    plt.title("Dinero medio de las empresas")
    plt.show()

    # Acciones emitidas por la empresa 1 y 99 y la media de acciones
    plt.figure()
    plt.plot(acciones_emitidas_empresas["Empresa1"])
    plt.plot(acciones_emitidas_empresas["Empresa99"])
    plt.plot([sum(acciones_emitidas_empresas[e]) / len(acciones_emitidas_empresas[e]) for e in acciones_emitidas_empresas])
    plt.title("Acciones emitidas por empresas")
    plt.show()

    print(f"Tiempo de ejecución: {tiempo_ejecucion} segundos")
    print("Fin del programa")