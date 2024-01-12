import random
from MercadoFinanciero import MercadoFinanciero
from Consumidor import Consumidor
from Empresa import Empresa

class Mercado:
    def __init__(self, bienes) -> None:
        self.bienes = bienes if bienes else {}
        self.personas = []
        self.mercado_financiero = MercadoFinanciero()
        self.transacciones = []
        self.empresaBienes = {}

    def agregar_persona(self, persona):
        self.personas.append(persona)

    def encontrar_equilibrio(self, precio_min, precio_max, tolerancia):
        precios_teoricos = {}
        demanda_teorica_total = {}
        oferta_teorica_total = {}
        exceso_demanda = {}
        exceso_oferta = {}

        for bien in self.bienes:
            precios_teoricos[bien] = (precio_min + precio_max) / 2
            demanda_teorica_total[bien] = 0
            oferta_teorica_total[bien] = 0

            # Calcula demanda teórica y oferta teórica
            for consumidor in self.getConsumidores():
                preferencia = consumidor.preferencias[bien]
                precio_maximo = consumidor.max_precio[bien]
                precio_teorico = precios_teoricos[bien]
                if precio_teorico <= precio_maximo:
                    cantidad_demandada = preferencia * consumidor.dinero / max(precio_teorico, 1)  # Evita división por cero
                    demanda_teorica_total[bien] += cantidad_demandada

            # Calcula oferta teórica
            for empresa in self.getEmpresas():
                if bien in empresa.bienes:
                    oferta_teorica_total[bien] += empresa.bienes[bien]

            # Calcula el exceso de demanda
            exceso_demanda[bien] = demanda_teorica_total[bien] - oferta_teorica_total[bien]
            exceso_oferta[bien] = oferta_teorica_total[bien] - demanda_teorica_total[bien]

        return precios_teoricos, demanda_teorica_total, oferta_teorica_total, exceso_demanda, exceso_oferta
        
    def ejecutar_ciclo(self):
        # Actualiza ingresos y preferencias de consumidores
        for consumidor in self.getConsumidores():
            consumidor.actualizar_ingresos()
            consumidor.ajustar_preferencias()
            # Logica de compra
            preferencias = consumidor.getPreferencias()
            sortedprefdict = {k: v for k, v in sorted(preferencias.items(), key=lambda item: item[1])}
            for bien in sortedprefdict:
                if preferencias[bien] > 0:
                    empresas = [empresa for empresa in self.getEmpresas() if bien in empresa.bienes]
                    empresas.sort(key=lambda empresa: empresa.precios[bien])
                    for empresa in empresas:
                        if empresa.bienes[bien] > 0:
                            if consumidor.comprar_bien(empresa, bien, 1, self):
                                break
        

        for _, empresa in enumerate(self.getEmpresas()):
            empresa.emitir_acciones(10, self.mercado_financiero)
            empresa.actualizar_costos()
            for bien in empresa.bienes:
                empresa.ajustar_precio_bien(self, bien)
                print(f"Empresa {_} actualizando precios")

            # if _%len(self.personas) == 0:
            # print(f"La empresa {empresa.nombre} tiene los siguientes bienes:")
            # for bien in empresa.bienes:
            #     print(f"{bien}: {empresa.bienes[bien]}")

    def getDineroConsumidores(self):
        return [c.dinero for c in self.personas if isinstance(c, Consumidor)]
    
    def getDineroEmpresas(self):
        return [e.dinero for e in self.personas if isinstance(e, Empresa)]
    
    def getConsumidores(self):
        return [c for c in self.personas if isinstance(c, Consumidor)]
    
    def getEmpresas(self):
        return [e for e in self.personas if isinstance(e, Empresa)]
    
    def getPersonas(self):
        return self.personas
    
    def registrar_transaccion(self, consumidor, nombre_bien, cantidad, costo_total):
        self.transacciones.append({
            'consumidor': consumidor.nombre,
            'bien': nombre_bien,
            'cantidad': cantidad,
            'costo_total': costo_total
        })

    def getRegistroTransacciones(self):
        return self.transacciones
    
    def setEmpresaBienes(self, bien, cantidad, empresa):
        if not bien in self.empresaBienes:
            self.empresaBienes[bien] = {}
        if not empresa in self.empresaBienes[bien]:
            self.empresaBienes[bien][empresa] = 0
        self.empresaBienes[bien][empresa] = cantidad