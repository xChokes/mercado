from Empresa import Empresa
from Persona import Persona
from ConfigEconomica import ConfigEconomica
import random
import math

class Consumidor(Persona):
    def __init__(self, nombre, mercado, bienes={}):
        super().__init__(mercado)
        self.nombre = nombre
        self.mercado = mercado  # Agregar esta línea que faltaba
        self.bienes = bienes if bienes else {}
        self.dinero = random.randint(ConfigEconomica.DINERO_INICIAL_CONSUMIDOR_MIN, 
                                   ConfigEconomica.DINERO_INICIAL_CONSUMIDOR_MAX)
        self.historial_compras = {}
        
        # Características laborales
        self.empleado = random.choice([True, False])  # 90% empleados inicialmente
        if random.random() > 0.1:
            self.empleado = True
            
        self.ingreso_mensual = random.randint(ConfigEconomica.SALARIO_BASE_MIN, 
                                             ConfigEconomica.SALARIO_BASE_MAX) if self.empleado else 0
        self.empleador = None
        self.habilidades = random.uniform(0.5, 1.5)  # Multiplicador de productividad
        
        # Características económicas
        self.propension_consumo = random.uniform(0.70, 0.95)  # Entre 70% y 95%
        self.propension_ahorro = 1 - self.propension_consumo
        self.ahorros = self.dinero * random.uniform(0.1, 0.3)  # 10-30% en ahorros
        self.deuda = random.uniform(0, self.ingreso_mensual * 2) if self.empleado else 0
        
        # Preferencias de consumo más realistas
        self.utilidad_marginal = {}
        self.cantidad_consumida = {}
        self.satisfaccion_bien = {}
        
        for bien in mercado.bienes.keys():
            self.cantidad_consumida[bien] = 0
            self.satisfaccion_bien[bien] = random.uniform(0.3, 1.0)
            # Bienes básicos más importantes
            categoria = ConfigEconomica.CATEGORIAS_BIENES.get(bien, 'servicios')
            if categoria == 'alimentos_basicos':
                self.satisfaccion_bien[bien] *= 1.5
                
        # Factores psicológicos
        self.aversion_riesgo = random.uniform(0.3, 0.9)
        self.factor_imitacion = random.uniform(0.1, 0.4)  # Influencia social
        self.fidelidad_marca = random.uniform(0.2, 0.8)
        
    def buscar_empleo(self):
        """Busca empleo si está desempleado"""
        if not self.empleado:
            empresas_disponibles = [e for e in self.mercado.getEmpresas() 
                                  if hasattr(e, 'empleados') and len(e.empleados) < e.capacidad_empleo]
            
            if empresas_disponibles:
                empresa = random.choice(empresas_disponibles)
                probabilidad_contratacion = self.habilidades * 0.6  # Base 60% si tiene habilidades máximas
                
                if random.random() < probabilidad_contratacion:
                    self.empleado = True
                    self.empleador = empresa
                    self.ingreso_mensual = int(ConfigEconomica.SALARIO_BASE_MIN * self.habilidades)
                    empresa.contratar(self)
                    return True
        return False
        
    def perder_empleo(self):
        """Pierde el empleo (por despidos, etc.)"""
        if self.empleado and self.empleador:
            self.empleado = False
            if hasattr(self.empleador, 'despedir'):
                self.empleador.despedir(self)
            self.empleador = None
            self.ingreso_mensual = 0
            
    def calcular_utilidad_marginal(self, bien):
        """Calcula la utilidad marginal de consumir una unidad adicional del bien"""
        cantidad_actual = self.cantidad_consumida.get(bien, 0)
        satisfaccion_base = self.satisfaccion_bien.get(bien, 0.5)
        
        # Utilidad marginal decreciente
        utilidad = satisfaccion_base * (ConfigEconomica.UTILIDAD_MARGINAL_DECRECIENTE ** cantidad_actual)
        
        # Aumentar utilidad para bienes básicos si no se han consumido
        categoria = ConfigEconomica.CATEGORIAS_BIENES.get(bien, 'servicios')
        if categoria == 'alimentos_basicos' and cantidad_actual == 0:
            utilidad *= 2.0
            
        return utilidad
        
    def calcular_precio_reserva(self, bien, precio_mercado):
        """Calcula el precio máximo que estaría dispuesto a pagar"""
        utilidad = self.calcular_utilidad_marginal(bien)
        ingreso_disponible = max(0, self.dinero - self.deuda - self.ahorros * 0.8)
        
        # Precio de reserva basado en utilidad e ingreso
        precio_reserva = utilidad * ingreso_disponible * 0.01  # Factor de escala
        
        # Ajuste por categoría del bien
        categoria = ConfigEconomica.CATEGORIAS_BIENES.get(bien, 'servicios')
        if categoria == 'alimentos_basicos':
            precio_reserva *= 1.2  # Dispuesto a pagar más por básicos
        elif categoria == 'bienes_duraderos':
            precio_reserva *= 0.8  # Más selectivo con lujos
            
        return max(precio_reserva, precio_mercado * 0.5)  # Mínimo 50% del precio de mercado
        
    def decidir_compra_racional(self, mercado, ciclo):
        """Decisión de compra basada en utilidad marginal y restricción presupuestaria"""
        presupuesto_consumo = self.dinero * self.propension_consumo
        
        # Crear lista de opciones de compra
        opciones_compra = []
        
        for bien in mercado.bienes.keys():
            empresas_disponibles = [e for e in mercado.getEmpresas() 
                                  if bien in e.bienes and len(e.bienes[bien]) > 0]
            
            if empresas_disponibles:
                # Encontrar la empresa con mejor precio
                mejor_empresa = min(empresas_disponibles, key=lambda e: e.precios.get(bien, float('inf')))
                precio = mejor_empresa.precios.get(bien, 0)
                
                if precio > 0 and precio <= presupuesto_consumo:
                    utilidad = self.calcular_utilidad_marginal(bien)
                    precio_reserva = self.calcular_precio_reserva(bien, precio)
                    
                    if precio <= precio_reserva:
                        ratio_utilidad_precio = utilidad / precio
                        opciones_compra.append({
                            'bien': bien,
                            'empresa': mejor_empresa,
                            'precio': precio,
                            'utilidad': utilidad,
                            'ratio': ratio_utilidad_precio
                        })
        
        # Ordenar por ratio utilidad/precio
        opciones_compra.sort(key=lambda x: x['ratio'], reverse=True)
        
        # Comprar en orden de preferencia hasta agotar presupuesto
        gastado = 0
        for opcion in opciones_compra[:5]:  # Máximo 5 compras por ciclo
            if gastado + opcion['precio'] <= presupuesto_consumo:
                if self.comprar_bien_mejorado(opcion['empresa'], opcion['bien'], 1, mercado, ciclo):
                    gastado += opcion['precio']
                    
    def comprar_bien_mejorado(self, empresa, bien, cantidad, mercado, ciclo):
        """Versión mejorada del método de compra"""
        precio = empresa.precios.get(bien, 0)
        costo_total = precio * cantidad
        
        if self.dinero >= costo_total and len(empresa.bienes.get(bien, [])) >= cantidad:
            # Realizar transacción
            self.dinero -= costo_total
            empresa.dinero += costo_total
            
            # Actualizar inventarios
            if bien not in self.bienes:
                self.bienes[bien] = 0
            self.bienes[bien] += cantidad
            
            # Actualizar satisfacción y consumo
            self.cantidad_consumida[bien] = self.cantidad_consumida.get(bien, 0) + cantidad
            
            # Remover del inventario de empresa
            for _ in range(cantidad):
                if empresa.bienes[bien]:
                    empresa.bienes[bien].pop(0)
                    
            # Registrar transacción
            mercado.registrar_transaccion(self, bien, cantidad, costo_total, ciclo)
            
            # Actualizar historial para decisiones futuras
            self.historial_compras[bien] = precio
            
            return True
        return False
        
    def gestionar_finanzas_personales(self):
        """Gestiona ahorros, deudas y decisiones financieras"""
        # Ahorrar si tiene exceso de dinero
        if self.dinero > self.ingreso_mensual * 1.5:
            ahorro_adicional = (self.dinero - self.ingreso_mensual * 1.2) * 0.3
            self.ahorros += ahorro_adicional
            self.dinero -= ahorro_adicional
            
        # Pagar deudas si es posible
        if self.deuda > 0 and self.dinero > self.ingreso_mensual * 0.5:
            pago_deuda = min(self.deuda, self.dinero * 0.1)
            self.deuda -= pago_deuda
            self.dinero -= pago_deuda
            
        # Usar ahorros en emergencias
        if self.dinero < self.ingreso_mensual * 0.2 and self.ahorros > 0:
            retiro = min(self.ahorros, self.ingreso_mensual * 0.3)
            self.ahorros -= retiro
            self.dinero += retiro
            
    def recibir_salario(self):
        """Recibe salario mensual si está empleado"""
        if self.empleado and self.ingreso_mensual > 0:
            # Salario con pequeña variación
            salario_efectivo = self.ingreso_mensual * random.uniform(0.95, 1.05)
            self.dinero += salario_efectivo
            return salario_efectivo
        return 0
        
    def ciclo_persona(self, ciclo, mercado):
        """Ciclo principal del consumidor"""
        # Recibir salario
        self.recibir_salario()
        
        # Buscar empleo si está desempleado
        if not self.empleado:
            self.buscar_empleo()
        
        # Gestionar finanzas
        self.gestionar_finanzas_personales()
        
        # Decisiones de inversión (simplificadas)
        self.decidir_acciones(mercado.mercado_financiero, mercado.registrar_transaccion, ciclo)
        
        # Decisión de compra racional
        self.decidir_compra_racional(mercado, ciclo)
        
        # Degradar satisfacción con el tiempo (los bienes se consumen)
        for bien in self.cantidad_consumida:
            self.cantidad_consumida[bien] = max(0, self.cantidad_consumida[bien] * ConfigEconomica.FACTOR_SACIEDAD)
            
    def comprar_acciones(self, mercado_financiero, nombre_empresa, cantidad):
        if nombre_empresa in mercado_financiero.acciones:
            total_acciones, precio_actual = mercado_financiero.acciones[nombre_empresa]
            costo_total = precio_actual * cantidad
            if self.dinero >= costo_total and cantidad <= total_acciones:
                self.dinero -= costo_total
                self.cartera_acciones[nombre_empresa] = self.cartera_acciones.get(nombre_empresa, 0) + cantidad
                self.historial_compras[nombre_empresa] = precio_actual
                return True
        return False

    def vender_acciones(self, mercado_financiero, nombre_empresa, cantidad):
        if nombre_empresa in self.cartera_acciones:
            if cantidad <= self.cartera_acciones[nombre_empresa]:
                self.cartera_acciones[nombre_empresa] -= cantidad
                self.dinero += mercado_financiero.acciones[nombre_empresa][1] * cantidad
                return True
        return False

    def decidir_acciones(self, mercado_financiero, registrar, ciclo):
        # Lógica simplificada de inversión
        if self.dinero > self.ingreso_mensual * 2:  # Solo invierte si tiene suficiente liquidez
            for nombre_empresa, (cantidad_acciones, precio_accion) in mercado_financiero.acciones.items():
                if self.deberia_comprar_acciones(mercado_financiero.acciones):
                    cantidad_a_comprar = min(5, int(self.dinero * 0.05 / precio_accion))  # Máximo 5% del dinero
                    if self.comprar_acciones(mercado_financiero, nombre_empresa, cantidad_a_comprar):
                        nombre_empresa_str = nombre_empresa.nombre if isinstance(nombre_empresa, Empresa) else str(nombre_empresa)
                        registrar(self, 'Accion ' + nombre_empresa_str, cantidad_a_comprar, precio_accion * cantidad_a_comprar, ciclo)

    def deberia_comprar_acciones(self, acciones):
        return self.dinero > self.ingreso_mensual * 3 and random.random() < 0.1  # 10% de probabilidad si tiene liquidez
        
    def __str__(self):
        empleado_str = "Empleado" if self.empleado else "Desempleado"
        return f"{self.nombre} - Dinero: ${self.dinero:.2f} - {empleado_str} - Ingreso: ${self.ingreso_mensual:.2f}"