from EmpresaProductora import EmpresaProductora
from MercadoFinanciero import MercadoFinanciero
from Consumidor import Consumidor
from Empresa import Empresa

class Mercado:
    def __init__(self, bienes) -> None:
        self.bienes = bienes if bienes else {} # Nuevo: bienes disponibles en el mercado
        self.personas = [] 
        self.mercado_financiero = MercadoFinanciero()
        self.transacciones = []
        self.empresaBienes = {}

    def agregar_persona(self, persona):
        self.personas.append(persona)

    def ejecutar_ciclo(self, ciclo):
        for persona in self.getPersonas():
            if isinstance(persona, Consumidor):
                persona.actualizar_ingresos()
                persona.ajustar_preferencias()
                persona.decidir_acciones(self.mercado_financiero, self.registrar_transaccion, ciclo)
                # Logica de compra
                preferencias = persona.getPreferencias()
                sortedprefdict = {k: v for k, v in sorted(preferencias.items(), key=lambda item: item[1])}
                for bien in sortedprefdict:
                    if preferencias[bien] > 0:
                        empresas = [empresa for empresa in self.getEmpresas() if bien in empresa.bienes]
                        empresas.sort(key=lambda empresa: empresa.precios[bien])
                        for empresa in empresas:
                            cantidad = persona.preferencias[bien] * persona.dinero / (2 * empresa.precios[bien])
                            if cantidad > 0:
                                if empresa.bienes[bien] > 0:
                                    dineroAntes = persona.dinero
                                    dineroAntes2 = empresa.dinero
                                    if persona.comprar_bien(empresa, bien, 1, self, ciclo):
                                        dineroDespues = persona.dinero
                                        dineroDespues2 = empresa.dinero
                                        print(f"La empresa {empresa.nombre} ha pasado de tener {dineroAntes2} a {dineroDespues2} y el consumidor {persona.nombre} ha pasado de tener {dineroAntes} a {dineroDespues}")
                                        break
            else:
                persona.emitir_acciones(10, self.mercado_financiero)
                if isinstance(persona, EmpresaProductora):
                    persona.actualizar_costos()
                persona.distribuir_dividendos(self.mercado_financiero)
                for bien in persona.bienes:
                    persona.ajustar_precio_bien(self, bien)

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
    
    def registrar_transaccion(self, consumidor, nombre_bien, cantidad, costo_total, ciclo):
        self.transacciones.append({
            'consumidor': consumidor.nombre,
            'bien': nombre_bien,
            'cantidad': cantidad,
            'costo_total': costo_total,
            'ciclo': ciclo
        })

    def getRegistroTransacciones(self):
        return self.transacciones
    
    def setEmpresaBienes(self, bien, cantidad, empresa):
        if not bien in self.empresaBienes:
            self.empresaBienes[bien] = {}
        if not empresa in self.empresaBienes[bien]:
            self.empresaBienes[bien][empresa] = 0
        self.empresaBienes[bien][empresa] = cantidad

    