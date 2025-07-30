from Persona import Persona
from ConfigEconomica import ConfigEconomica
import random

class Empresa(Persona):
    def __init__(self, nombre, mercado, bienes={}):
        super().__init__(mercado=mercado)
        self.nombre = nombre
        self.bienes = bienes if bienes else {}
        self.dinero = random.randint(ConfigEconomica.DINERO_INICIAL_EMPRESA_MIN, 
                                   ConfigEconomica.DINERO_INICIAL_EMPRESA_MAX)
        self.acciones_emitidas = 0
        self.valor_accion = 0
        self.umbral_alto = random.randint(80, 120)
        self.umbral_bajo = random.randint(30, 70)
        self.factor_incremento = random.uniform(0.1, 0.25)
        self.factor_decremento = random.uniform(0.1, 0.25)
        self.precios = {}
        self.costos_unitarios = {}
        self.ventasPorBienPorCiclo = {}
        
        # Nuevos atributos para manejo de empleados
        self.empleados = []
        self.capacidad_empleo = random.randint(5, 30)
        
        # Inicializar precios y costos básicos
        for bien in mercado.bienes.keys():
            if bien not in self.precios:
                self.precios[bien] = random.randint(10, 50)
            if bien not in self.costos_unitarios:
                self.costos_unitarios[bien] = self.precios[bien] * random.uniform(0.6, 0.8)
            self.ventasPorBienPorCiclo[bien] = {}
            
    def contratar(self, consumidor):
        """Contrata a un consumidor como empleado"""
        if len(self.empleados) < self.capacidad_empleo:
            self.empleados.append(consumidor)
            return True
        return False
        
    def despedir(self, consumidor):
        """Despide a un empleado"""
        if consumidor in self.empleados:
            self.empleados.remove(consumidor)
            
    def ajustar_precio_bien(self, mercado, nombre_bien):
        if nombre_bien not in self.precios:
            self.precios[nombre_bien] = random.randint(10, 50)
            
        ventas = sum([t['cantidad'] for t in mercado.getRegistroTransacciones() 
                     if t['bien'] == nombre_bien])
        stock_actual = len(self.bienes.get(nombre_bien, []))
        elasticidad_demanda = mercado.bienes[nombre_bien].elasticidad_precio

        precio_actual = self.precios[nombre_bien]
        costo_unitario = self.costos_unitarios.get(nombre_bien, precio_actual * 0.7)

        # Calcula el nuevo precio basado en elasticidad de la demanda
        if elasticidad_demanda != 0:
            factor_cambio = 1 - ventas / max(stock_actual, 1)
            cambio_precio = factor_cambio / abs(elasticidad_demanda)
            nuevo_precio = max(precio_actual * (1 + cambio_precio * 0.1), costo_unitario * 1.1)
        else:
            nuevo_precio = precio_actual * (1 + random.uniform(-0.02, 0.02))

        self.precios[nombre_bien] = round(nuevo_precio, 2)
    
    def emitir_acciones(self, cantidad, mercado_financiero):
        if self.acciones_emitidas == 0:
            self.valor_accion = max(10, int(self.dinero / 1000))
        else:
            self.valor_accion = max(1, int(self.dinero / self.acciones_emitidas))
            
        mercado_financiero.emitir_acciones(self.nombre, cantidad)
        self.acciones_emitidas += cantidad

    def distribuir_dividendos(self, mercado_financiero):
        if self.nombre in mercado_financiero.acciones:
            total_acciones, _ = mercado_financiero.acciones[self.nombre]
            if total_acciones > 0 and self.dinero > 1000:  # Solo si hay liquidez
                dividendo_por_accion = self.calcular_dividendo()
                dividendo_total = dividendo_por_accion * total_acciones
                if dividendo_total <= self.dinero * 0.1:  # Máximo 10% en dividendos
                    self.dinero -= dividendo_total

    def calcular_dividendo(self):
        if self.acciones_emitidas > 0:
            return max(0, self.dinero * 0.02 / self.acciones_emitidas)  # 2% del capital
        return 0
    
    def ciclo_persona(self, ciclo, mercado):
        """Ciclo básico de empresa (las empresas productoras sobrescriben esto)"""
        # Emitir algunas acciones
        if random.random() < 0.3:  # 30% probabilidad
            self.emitir_acciones(random.randint(1, 10), mercado.mercado_financiero)
        
        # Distribuir dividendos
        self.distribuir_dividendos(mercado.mercado_financiero)
        
        # Ajustar precios si tiene bienes
        for bien in self.bienes:
            if bien in mercado.bienes:
                self.ajustar_precio_bien(mercado, bien)
            
    @classmethod
    def crear_con_acciones(cls, nombre, mercado, cantidad_acciones, bienes={}):
        empresa = cls(nombre, mercado, bienes=bienes)
        empresa.emitir_acciones(cantidad_acciones, mercado.mercado_financiero)
        return empresa

    def __str__(self):
        return f"Empresa {self.nombre} - Capital: ${self.dinero:,.2f} - Acciones: {self.acciones_emitidas}"