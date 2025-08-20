from .Persona import Persona
from ..config.ConfigEconomica import ConfigEconomica
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
        # Manejar bienes como diccionario o lista
        bienes_lista = mercado.bienes if isinstance(mercado.bienes, list) else list(mercado.bienes.keys())
        
        for bien in bienes_lista:
            if bien not in self.precios:
                self.precios[bien] = random.randint(10, 50)
            if bien not in self.costos_unitarios:
                self.costos_unitarios[bien] = self.precios[bien] * \
                    random.uniform(0.6, 0.8)
            self.ventasPorBienPorCiclo[bien] = {}

    def contratar(self, consumidor):
        """Contrata a un consumidor como empleado con lógica mejorada"""
        if len(self.empleados) < self.capacidad_empleo and self.dinero > 10000:
            self.empleados.append(consumidor)
            consumidor.empleado = True
            consumidor.empleador = self
            # Asignar salario basado en capacidad de la empresa
            salario_base = max(2000, min(8000, self.dinero / 100))
            consumidor.ingreso_mensual = salario_base * \
                random.uniform(0.8, 1.2)
            return True
        return False

    def despedir(self, consumidor):
        """Despide a un empleado con lógica mejorada"""
        if consumidor in self.empleados:
            self.empleados.remove(consumidor)
            consumidor.empleado = False
            consumidor.empleador = None
            consumidor.ingreso_mensual = 0
            return True
        return False

    def ajustar_precio_bien(self, mercado, nombre_bien):
        if nombre_bien not in self.precios:
            self.precios[nombre_bien] = random.randint(10, 50)

        # Asegurar que el precio nunca sea cero
        if self.precios[nombre_bien] <= 0:
            self.precios[nombre_bien] = random.randint(10, 50)

        ventas = sum([t['cantidad'] for t in mercado.getRegistroTransacciones()
                     if t['bien'] == nombre_bien])
        stock_actual = len(self.bienes.get(nombre_bien, []))

        # Verificar que elasticidad existe y es válida
        if hasattr(mercado.bienes[nombre_bien], 'elasticidad_precio'):
            elasticidad_demanda = mercado.bienes[nombre_bien].elasticidad_precio
        else:
            elasticidad_demanda = 1.0  # Valor por defecto

        precio_actual = self.precios[nombre_bien]

        # Asegurar que costos_unitarios esté inicializado
        if not hasattr(self, 'costos_unitarios'):
            self.costos_unitarios = {}
        if nombre_bien not in self.costos_unitarios or self.costos_unitarios[nombre_bien] <= 0:
            self.costos_unitarios[nombre_bien] = precio_actual * 0.7

        costo_unitario = self.costos_unitarios.get(
            nombre_bien, precio_actual * 0.7)

        # Calcula el nuevo precio basado en elasticidad de la demanda
        # Evitar divisiones por números muy pequeños
        if elasticidad_demanda != 0 and abs(elasticidad_demanda) > 0.001:
            factor_cambio = 1 - ventas / max(stock_actual, 1)
            cambio_precio = factor_cambio / \
                max(abs(elasticidad_demanda), 0.001)  # Protección adicional
            nuevo_precio = max(
                precio_actual * (1 + cambio_precio * 0.1), costo_unitario * 1.1)
        else:
            nuevo_precio = precio_actual * (1 + random.uniform(-0.02, 0.02))

        # Asegurar que el nuevo precio nunca sea cero o negativo
        self.precios[nombre_bien] = round(max(nuevo_precio, 1.0), 2)

    def emitir_acciones(self, cantidad, mercado_financiero):
        if self.acciones_emitidas == 0:
            self.valor_accion = max(10, int(self.dinero / 1000))
        else:
            # Protección contra división por cero en acciones emitidas
            if self.acciones_emitidas > 0:
                self.valor_accion = max(
                    1, int(self.dinero / self.acciones_emitidas))
            else:
                self.valor_accion = max(10, int(self.dinero / 1000))

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
        """Calcula dividendo por acción con protección contra división por cero"""
        if self.acciones_emitidas > 0 and self.dinero > 0:
            # 2% del capital dividido entre acciones
            return max(0, self.dinero * 0.02 / self.acciones_emitidas)
        return 0

    def ciclo_persona(self, ciclo, mercado):
        """Ciclo básico de empresa (las empresas productoras sobrescriben esto)"""
        # Emitir algunas acciones
        if random.random() < 0.3:  # 30% probabilidad
            self.emitir_acciones(random.randint(
                1, 10), mercado.mercado_financiero)

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
