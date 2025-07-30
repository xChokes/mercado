from .Empresa import Empresa
from ..config.ConfigEconomica import ConfigEconomica
from .InventarioBien import InventarioBien
import random
import math

class EmpresaProductora(Empresa):
    def __init__(self, nombre, mercado, bienes={}):
        super().__init__(nombre=nombre, bienes=bienes, mercado=mercado)
        
        # Características financieras mejoradas
        self.dinero = random.randint(ConfigEconomica.DINERO_INICIAL_EMPRESA_PRODUCTORA_MIN,
                                   ConfigEconomica.DINERO_INICIAL_EMPRESA_PRODUCTORA_MAX)
        
        # Capacidades de producción
        self.capacidad_produccion = {}
        self.produccion_actual = {}
        self.eficiencia_produccion = random.uniform(0.7, 1.0)
        
        # Costos de producción más realistas
        self.costos_unitarios = {}
        self.costos_fijos_mensuales = random.randint(10000, 50000)
        self.costos_variables = {}
        
        # Empleados y recursos humanos
        self.empleados = []
        self.capacidad_empleo = random.randint(20, 100)
        self.costo_salarios = 0
        
        # Estrategia empresarial
        self.estrategia_precios = random.choice(['lider_costos', 'diferenciacion', 'nicho'])
        self.aversion_riesgo_empresa = random.uniform(0.3, 0.8)
        self.factor_expansion = random.uniform(0.05, 0.20)
        
        # Inicializar capacidades para todos los bienes del mercado
        for bien in mercado.bienes.keys():
            base_capacity = random.randint(ConfigEconomica.PRODUCCION_BASE_MIN,
                                         ConfigEconomica.PRODUCCION_BASE_MAX)
            self.capacidad_produccion[bien] = base_capacity
            self.produccion_actual[bien] = 0
            
            # Costos basados en categoría del bien
            categoria = ConfigEconomica.CATEGORIAS_BIENES.get(bien, 'servicios')
            if categoria == 'alimentos_basicos':
                costo_base = random.uniform(3, 15)
            elif categoria == 'alimentos_lujo':
                costo_base = random.uniform(8, 25)
            else:
                costo_base = random.uniform(10, 30)
                
            self.costos_unitarios[bien] = costo_base
            self.costos_variables[bien] = costo_base * random.uniform(0.3, 0.7)  # Costos variables
            
            # Inicializar inventario vacío
            self.bienes[bien] = []
            
        # Precios iniciales con márgenes realistas
        self.establecer_precios_iniciales()
        
    def establecer_precios_iniciales(self):
        """Establece precios iniciales basados en costos y estrategia"""
        for bien in self.costos_unitarios:
            costo = self.costos_unitarios[bien]
            
            if self.estrategia_precios == 'lider_costos':
                margen = random.uniform(ConfigEconomica.MARGEN_GANANCIA_MIN, 
                                      ConfigEconomica.MARGEN_GANANCIA_MIN + 0.2)
            elif self.estrategia_precios == 'diferenciacion':
                margen = random.uniform(ConfigEconomica.MARGEN_GANANCIA_MIN + 0.3,
                                      ConfigEconomica.MARGEN_GANANCIA_MAX)
            else:  # nicho
                margen = random.uniform(ConfigEconomica.MARGEN_GANANCIA_MIN + 0.1,
                                      ConfigEconomica.MARGEN_GANANCIA_MAX - 0.1)
                
            self.precios[bien] = round(costo * (1 + margen), 2)
            
    def contratar(self, consumidor):
        """Contrata a un consumidor como empleado"""
        if len(self.empleados) < self.capacidad_empleo:
            self.empleados.append(consumidor)
            self.costo_salarios += consumidor.ingreso_mensual
            return True
        return False
        
    def despedir(self, consumidor):
        """Despide a un empleado"""
        if consumidor in self.empleados:
            self.empleados.remove(consumidor)
            self.costo_salarios -= consumidor.ingreso_mensual
            
    def calcular_demanda_estimada(self, bien, mercado):
        """Estima la demanda del bien basada en el mercado"""
        # Demanda basada en población de consumidores
        consumidores = mercado.getConsumidores()
        ingreso_promedio = sum([c.ingreso_mensual for c in consumidores if c.empleado]) / max(1, len(consumidores))
        
        # Usar el método del bien para calcular demanda base
        demanda_base = mercado.bienes[bien].calcular_demanda_base(len(consumidores), ingreso_promedio)
        
        # Ajustar por competencia
        competidores = [e for e in mercado.getEmpresas() if e != self and bien in e.bienes]
        factor_competencia = 1.0 / max(1, len(competidores))
        
        # Ajustar por precio relativo
        if competidores:
            precio_promedio_competencia = sum([e.precios.get(bien, 0) for e in competidores]) / len(competidores)
            if precio_promedio_competencia > 0:
                factor_precio = precio_promedio_competencia / max(self.precios.get(bien, 1), 1)
                factor_precio = min(2.0, max(0.5, factor_precio))  # Limitar el efecto
            else:
                factor_precio = 1.0
        else:
            factor_precio = 1.0
            
        demanda_estimada = int(demanda_base * factor_competencia * factor_precio)
        return max(1, demanda_estimada)
        
    def planificar_produccion(self, mercado):
        """Planifica la producción basada en demanda estimada y capacidad"""
        plan_produccion = {}
        
        for bien in self.capacidad_produccion:
            demanda_estimada = self.calcular_demanda_estimada(bien, mercado)
            stock_actual = len(self.bienes.get(bien, []))
            
            # Nivel de stock objetivo (1.5x la demanda estimada)
            stock_objetivo = int(demanda_estimada * 1.5)
            necesidad_produccion = max(0, stock_objetivo - stock_actual)
            
            # Limitar por capacidad de producción
            capacidad_disponible = self.capacidad_produccion[bien] - self.produccion_actual.get(bien, 0)
            produccion_planificada = min(necesidad_produccion, capacidad_disponible)
            
            # Considerar restricciones financieras
            costo_produccion = produccion_planificada * self.costos_unitarios[bien]
            if costo_produccion > self.dinero * 0.7:  # No usar más del 70% del capital
                produccion_planificada = int(self.dinero * 0.7 / self.costos_unitarios[bien])
                
            plan_produccion[bien] = max(0, produccion_planificada)
            
        return plan_produccion
        
    def producir_bien_mejorado(self, bien, cantidad, mercado):
        """Versión mejorada del método de producción"""
        if cantidad <= 0:
            return 0
            
        costo_total = cantidad * self.costos_unitarios[bien]
        
        if self.dinero >= costo_total:
            self.dinero -= costo_total
            
            # Considerar eficiencia y economías de escala
            cantidad_efectiva = int(cantidad * self.eficiencia_produccion)
            if cantidad_efectiva > 50:  # Economías de escala
                cantidad_efectiva = int(cantidad_efectiva * ConfigEconomica.FACTOR_ECONOMIA_ESCALA)
                
            # Añadir al inventario
            if bien not in self.bienes:
                self.bienes[bien] = []
                
            for _ in range(cantidad_efectiva):
                costo_unitario_efectivo = self.costos_unitarios[bien] * random.uniform(0.95, 1.05)
                self.bienes[bien].append(InventarioBien(bien, costo_unitario_efectivo, mercado.bienes))
                
            self.produccion_actual[bien] = self.produccion_actual.get(bien, 0) + cantidad_efectiva
            return cantidad_efectiva
            
        return 0
        
    def ajustar_precios_dinamico(self, mercado, bien):
        """Ajusta precios basado en múltiples factores económicos"""
        if bien not in self.precios:
            return
            
        precio_actual = self.precios[bien]
        costo_unitario = self.costos_unitarios[bien]
        
        # Factor 1: Análisis de demanda (ventas recientes)
        ventas_recientes = self.obtener_ventas_recientes(bien, mercado, 3)  # Últimos 3 ciclos
        demanda_estimada = self.calcular_demanda_estimada(bien, mercado)
        
        if demanda_estimada > 0:
            ratio_demanda = ventas_recientes / demanda_estimada
        else:
            ratio_demanda = 0.5
            
        # Factor 2: Nivel de inventario
        stock_actual = len(self.bienes.get(bien, []))
        stock_optimo = demanda_estimada * 1.5
        
        if stock_optimo > 0:
            ratio_stock = stock_actual / stock_optimo
        else:
            ratio_stock = 1.0
            
        # Factor 3: Competencia
        competidores = [e for e in mercado.getEmpresas() if e != self and bien in e.precios]
        if competidores:
            precio_promedio_competencia = sum([e.precios[bien] for e in competidores]) / len(competidores)
            factor_competencia = precio_promedio_competencia / precio_actual if precio_actual > 0 else 1.0
        else:
            factor_competencia = 1.0
            
        # Calcular ajuste de precio
        ajuste = 0
        
        # Si demanda > oferta, subir precios
        if ratio_demanda > 1.2:
            ajuste += 0.05
        elif ratio_demanda < 0.8:
            ajuste -= 0.03
            
        # Si hay exceso de inventario, bajar precios
        if ratio_stock > 2.0:
            ajuste -= 0.04
        elif ratio_stock < 0.5:
            ajuste += 0.03
            
        # Ajuste por competencia
        if factor_competencia > 1.1:  # Competencia más cara
            ajuste += 0.02
        elif factor_competencia < 0.9:  # Competencia más barata
            ajuste -= 0.02
            
        # Limitar el ajuste máximo por ciclo
        ajuste = max(-ConfigEconomica.FACTOR_AJUSTE_PRECIO_MAX, 
                    min(ConfigEconomica.FACTOR_AJUSTE_PRECIO_MAX, ajuste))
        
        # Aplicar ajuste
        nuevo_precio = precio_actual * (1 + ajuste)
        
        # Asegurar margen mínimo
        precio_minimo = costo_unitario * (1 + ConfigEconomica.MARGEN_GANANCIA_MIN)
        nuevo_precio = max(nuevo_precio, precio_minimo)
        
        self.precios[bien] = round(nuevo_precio, 2)
        
    def obtener_ventas_recientes(self, bien, mercado, num_ciclos):
        """Obtiene las ventas de los últimos N ciclos"""
        ciclo_actual = len(mercado.transacciones)
        ventas_totales = 0
        
        for transaccion in mercado.transacciones:
            if (transaccion.get('bien') == bien and 
                hasattr(transaccion, 'empresa') and 
                transaccion['empresa'] == self.nombre and
                transaccion.get('ciclo', 0) >= ciclo_actual - num_ciclos):
                ventas_totales += transaccion.get('cantidad', 0)
                
        return ventas_totales
        
    def gestionar_expansion(self):
        """Decide si expandir capacidad basado en rentabilidad"""
        if self.dinero > self.costos_fijos_mensuales * 6:  # 6 meses de reserva
            # Identificar bienes más rentables
            rentabilidades = {}
            for bien in self.precios:
                precio = self.precios[bien]
                costo = self.costos_unitarios[bien]
                rentabilidad = (precio - costo) / costo if costo > 0 else 0
                rentabilidades[bien] = rentabilidad
                
            # Expandir capacidad del bien más rentable
            if rentabilidades:
                mejor_bien = max(rentabilidades, key=rentabilidades.get)
                if rentabilidades[mejor_bien] > 0.3:  # 30% de margen mínimo
                    costo_expansion = self.capacidad_produccion[mejor_bien] * 100  # Costo por unidad de capacidad
                    if self.dinero > costo_expansion:
                        expansion = int(self.capacidad_produccion[mejor_bien] * self.factor_expansion)
                        self.capacidad_produccion[mejor_bien] += expansion
                        self.dinero -= costo_expansion
                        
    def pagar_costos_operativos(self):
        """Paga costos fijos y salarios"""
        costo_total = self.costos_fijos_mensuales + self.costo_salarios
        
        if self.dinero >= costo_total:
            self.dinero -= costo_total
            return True
        else:
            # Crisis financiera - despedir empleados
            empleados_a_despedir = min(len(self.empleados), 
                                     int((costo_total - self.dinero) / 3000))  # Asumir salario promedio 3000
            for _ in range(empleados_a_despedir):
                if self.empleados:
                    empleado = self.empleados.pop()
                    empleado.perder_empleo()
                    self.costo_salarios -= empleado.ingreso_mensual
            return False
            
    def ciclo_persona(self, ciclo, mercado):
        """Ciclo principal de la empresa productora"""
        # Pagar costos operativos
        self.pagar_costos_operativos()
        
        # Planificar y ejecutar producción
        plan_produccion = self.planificar_produccion(mercado)
        
        for bien, cantidad in plan_produccion.items():
            if cantidad > 0:
                cantidad_producida = self.producir_bien_mejorado(bien, cantidad, mercado)
                
        # Ajustar precios dinámicamente
        for bien in self.precios:
            self.ajustar_precios_dinamico(mercado, bien)
            
        # Considerar expansión
        if ciclo % 5 == 0:  # Cada 5 ciclos evaluar expansión
            self.gestionar_expansion()
            
        # Actividades de empresa base (acciones, dividendos)
        self.emitir_acciones(5, mercado.mercado_financiero)
        self.distribuir_dividendos(mercado.mercado_financiero)
        
        # Reset de producción actual para próximo ciclo
        for bien in self.produccion_actual:
            self.produccion_actual[bien] = 0