import random
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
            persona.ciclo_persona(ciclo, self)

    def getDineroConsumidores(self):
        return [c.dinero for c in self.personas if isinstance(c, Consumidor)]
    
    def getDineroEmpresas(self):
        return [e.dinero for e in self.personas if isinstance(e, Empresa)]
    
    def getConsumidores(self):
        return [c for c in self.personas if isinstance(c, Consumidor)]
    
    def getEmpresas(self):
        return [e for e in self.personas if isinstance(e, Empresa) or isinstance(e, EmpresaProductora)]
    
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

    