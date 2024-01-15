import random
import time
import matplotlib.pyplot as plt
from Mercado import Mercado
from Bien import Bien
from Consumidor import Consumidor
from Empresa import Empresa
from EmpresaProductora import EmpresaProductora

if __name__ == "__main__":
    bienes = {
        'Arroz': Bien('Arroz', 0.5, 0.5),
        'Carne': Bien('Carne', 0.5, 0.5),
        'Papa': Bien('Papa', 0.5, 0.5),
        'Leche': Bien('Leche', 0.5, 0.5),
        'Pan': Bien('Pan', 0.5, 0.5),
        'Huevos': Bien('Huevos', 0.5, 0.5),
        'Pollo': Bien('Pollo', 0.5, 0.5),
        'Azucar': Bien('Azucar', 0.5, 0.5),
        'Sal': Bien('Sal', 0.5, 0.5),
        'Aceite': Bien('Aceite', 0.5, 0.5),
        'Cafe': Bien('Cafe', 0.5, 0.5),
    }
    
    mercado = Mercado(bienes)

    for _ in range(3):
        nombre_empresa_productora = "EmpresaProductora" + str(_)
        empresa = EmpresaProductora(nombre_empresa_productora, mercado=mercado)
        mercado.agregar_persona(empresa)
        print("Agregada empresa productora nº ", _)

    for _ in range(100):
        nombre_consumidor = "Consumidor" + str(_)
        mercado.agregar_persona(Consumidor(nombre_consumidor, mercado))
        print("Agregado consumidor nº ", _)

    for _ in range(5):
        nombre_empresa = "Empresa" + str(_)
        empresa = Empresa.crear_con_acciones(nombre=nombre_empresa, mercado=mercado, cantidad_acciones=100, bienes={})
        mercado.agregar_persona(empresa)
        print("Agregada empresa nº ", _)

    num_ciclos = 20
    init = time.time()

    dinero_consumidores_por_ciclo = {}
    dinero_empresas_por_ciclo = {}
    precios_por_ciclo = {}

    empresaAleatoria = random.choice(mercado.getEmpresas())
    print(f"Dinero de {empresaAleatoria.nombre} aleatoria: {empresaAleatoria.dinero}")
    for ciclo in range(num_ciclos):
        print(f"Ciclo {ciclo+1}")
        mercado.ejecutar_ciclo(ciclo)
        empresaAleatoria2 = None
        for empresa in mercado.getEmpresas():
            if empresa.nombre == empresaAleatoria.nombre:
                empresaAleatoria2 = empresa
                break

        print(f"Dinero de {empresaAleatoria2.nombre} aleatoria en el ciclo {ciclo+1}: {empresaAleatoria2.dinero}")

        for persona in mercado.getPersonas():
            if isinstance(persona, Consumidor):
                if persona.nombre not in dinero_consumidores_por_ciclo:
                    dinero_consumidores_por_ciclo[persona.nombre] = []
                dinero_consumidores_por_ciclo[persona.nombre].append(persona.dinero)
            else:
                if persona.nombre not in dinero_empresas_por_ciclo:
                    dinero_empresas_por_ciclo[persona.nombre] = []
                dinero_empresas_por_ciclo[persona.nombre].append(persona.dinero)

    tiempo_ejecucion = time.time() - init
    
    print("Transacciones:")
    for transaccion in mercado.getRegistroTransacciones():
        print(transaccion)

    #Dinero personas
    plt.figure()
    for _,persona in enumerate(dinero_consumidores_por_ciclo):
        plt.plot(dinero_consumidores_por_ciclo[persona], label=persona)
    plt.legend()
    plt.show()

    #Dinero empresas
    print(dinero_empresas_por_ciclo)
    plt.figure()
    for _,persona in enumerate(dinero_empresas_por_ciclo):
        plt.plot(dinero_empresas_por_ciclo[persona], label=persona)
    plt.legend()
    plt.show()

    print("Información de empresa aleatoria:")
    empresa = random.choice(mercado.getEmpresas())
    print(f"Nombre: {empresa}")

    print(f"Tiempo de ejecución: {tiempo_ejecucion} segundos")
    print("Fin del programa")