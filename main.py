import random
import time
import matplotlib.pyplot as plt
from Mercado import Mercado
from Bien import Bien
from Consumidor import Consumidor
from Empresa import Empresa


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
    for _ in range(1000):
        nombre_consumidor = "Consumidor" + str(_)
        bienescons = {bien: random.randint(1, 100) for bien in bienes.keys()}
        mercado.agregar_persona(Consumidor(nombre_consumidor, bienescons, mercado))
        print("Agregado consumidor nº ", _)

    for _ in range(100):
        nombre_empresa = "Empresa" + str(_)
        bienesempres = {bien: random.randint(1, 100) for bien in bienes.keys()}
        empresa = Empresa.crear_con_acciones(nombre_empresa, bienesempres, mercado, 10)
        mercado.agregar_persona(empresa)
        print("Agregada empresa nº ", _)


    num_ciclos = 10
    init = time.time()

    # Listas para almacenar totales
    demanda_total_por_ciclo = []
    oferta_total_por_ciclo = []
    exceso_demanda_total_por_ciclo = []
    exceso_oferta_total_por_ciclo = []
    dinero_consumidores_por_ciclo = {}
    dinero_empresas_por_ciclo = {}
    precios_por_ciclo = {}

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

    # Gráficas
    plt.figure()
    plt.plot(demanda_total_por_ciclo, label='Demanda Total')
    plt.plot(oferta_total_por_ciclo, label='Oferta Total')
    plt.plot(exceso_demanda_total_por_ciclo, label='Exceso de Demanda Total')
    plt.plot(exceso_oferta_total_por_ciclo, label='Exceso de Oferta Total')
    plt.legend()
    plt.show()
    
    #Dinero personas
    plt.figure()
    for _,persona in enumerate(dinero_consumidores_por_ciclo):
        # if _==2 or _ % len(dinero_consumidores_por_ciclo) == 0:
        if _%5 == 0:
            plt.plot(dinero_consumidores_por_ciclo[persona], label=persona)
    plt.legend()
    plt.show()

    #Dinero empresas
    plt.figure()
    for _,persona in enumerate(dinero_empresas_por_ciclo):
        # if _==2 or _ % len(dinero_empresas_por_ciclo) == 0:
        if _%5 == 0:
            plt.plot(dinero_empresas_por_ciclo[persona], label=persona)
    plt.legend()
    plt.show()

    # Transacciones
    transacciones = mercado.getRegistroTransacciones()
    print("Transacciones:")
    # print(transacciones)
    for transaccion in transacciones:
        print(transaccion)

    print(f"Tiempo de ejecución: {tiempo_ejecucion} segundos")
    print("Fin del programa")