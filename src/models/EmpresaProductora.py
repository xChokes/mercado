from .Empresa import Empresa
from ..config.ConfigEconomica import ConfigEconomica
from .InventarioBien import InventarioBien
import random


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

        # Tecnología limpia
        self.factor_emisiones = 1.0  # 1.0 sin mejoras

        # Costos de producción más realistas
        self.costos_unitarios = {}
        self.costos_fijos_mensuales = random.randint(10000, 50000)
        self.costos_variables = {}

        # Empleados y recursos humanos
        self.empleados = []
        self.capacidad_empleo = random.randint(20, 100)
        self.costo_salarios = 0

        # Estrategia empresarial
        self.estrategia_precios = random.choice(
            ['lider_costos', 'diferenciacion', 'nicho'])
        self.aversion_riesgo_empresa = random.uniform(0.3, 0.8)
        self.factor_expansion = random.uniform(0.05, 0.20)

        # Inicializar capacidades para todos los bienes del mercado
        for bien in mercado.bienes.keys():
            base_capacity = random.randint(ConfigEconomica.PRODUCCION_BASE_MIN,
                                           ConfigEconomica.PRODUCCION_BASE_MAX)
            self.capacidad_produccion[bien] = base_capacity
            self.produccion_actual[bien] = 0

            # Costos basados en categoría del bien
            categoria = ConfigEconomica.CATEGORIAS_BIENES.get(
                bien, 'servicios')
            if categoria == 'alimentos_basicos':
                costo_base = random.uniform(3, 15)
            elif categoria == 'alimentos_lujo':
                costo_base = random.uniform(8, 25)
            else:
                costo_base = random.uniform(10, 30)

            self.costos_unitarios[bien] = costo_base
            self.costos_variables[bien] = costo_base * \
                random.uniform(0.3, 0.7)  # Costos variables

            # Inicializar inventario vacío
            self.bienes[bien] = []

        # Precios iniciales con márgenes realistas
        self.establecer_precios_iniciales()

    def establecer_precios_iniciales(self):
        """Establece precios iniciales basados en costos y estrategia"""
        # Validación de seguridad
        if not hasattr(self, 'costos_unitarios') or not self.costos_unitarios:
            return

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

            self.precios[bien] = round(
                max(costo * (1 + margen), 1), 2)  # Precio mínimo de 1

    def contratar(self, consumidor):
        """Contrata evaluando habilidades sectoriales y negociando salario mejorado"""
        # Aumentar capacidad de empleo dinámicamente
        capacidad_dinamica = max(
            self.capacidad_empleo, len(self.empleados) + 5)

        if len(self.empleados) >= capacidad_dinamica:
            return 0

        # Flexibilizar requisitos de habilidades durante alta desempleo
        sector_nombre = getattr(getattr(self, 'sector', None), 'nombre', None)
        nivel = consumidor.habilidades_sectoriales.get(sector_nombre, 0.0)

        # Ajustar requisitos según desempleo
        desempleo = self.mercado.gobierno.tasa_desempleo if hasattr(
            self.mercado, 'gobierno') else 0.1
        # Menor requisito con alto desempleo
        habilidad_minima = max(0.1, 0.3 - desempleo)

        if nivel < habilidad_minima:
            return 0

        # Negociación salarial mejorada
        if ConfigEconomica.TASA_DESEMPLEO_OBJETIVO > 0:
            factor_phillips = 1 + 0.5 * \
                (1 - desempleo / max(0.01, ConfigEconomica.TASA_DESEMPLEO_OBJETIVO)
                 )  # Evitar división por cero
        else:
            factor_phillips = 1.0

        # Incentivos gubernamentales para contratación
        subsidio_contratacion = 1.0
        if hasattr(self.mercado, 'crisis_financiera_activa') and self.mercado.crisis_financiera_activa:
            subsidio_contratacion = 1.2  # 20% de incentivo durante crisis

        salario_base = ConfigEconomica.SALARIO_BASE_MIN * (0.5 + nivel)
        salario = int(salario_base * factor_phillips * subsidio_contratacion)

        # Ajuste por poder sindical
        if consumidor.sindicato and sector_nombre in consumidor.sindicato.sectores:
            salario = int(
                salario * (1 + consumidor.sindicato.poder_negociacion))

        consumidor.ingreso_mensual = salario
        self.empleados.append(consumidor)
        self.costo_salarios += salario
        return salario

    def despedir(self, consumidor):
        """Despide a un empleado"""
        if consumidor in self.empleados:
            self.empleados.remove(consumidor)
            self.costo_salarios -= consumidor.ingreso_mensual

    def calcular_demanda_estimada(self, bien, mercado):
        """Estima la demanda del bien basada en el mercado"""
        # Demanda basada en población de consumidores
        consumidores = mercado.getConsumidores()
        ingreso_promedio = sum(
            [c.ingreso_mensual for c in consumidores if c.empleado]) / max(1, len(consumidores))

        # Usar el método del bien para calcular demanda base
        demanda_base = mercado.bienes[bien].calcular_demanda_base(
            len(consumidores), ingreso_promedio)

        # Ajustar por competencia
        competidores = [e for e in mercado.getEmpresas() if e !=
                        self and bien in e.bienes]
        factor_competencia = 1.0 / max(1, len(competidores))

        # Ajustar por precio relativo
        if competidores:
            precio_promedio_competencia = sum(
                # Evitar división por cero
                [e.precios.get(bien, 0) for e in competidores]) / max(1, len(competidores))
            if precio_promedio_competencia > 0:
                # Obtener precio propio, garantizando que nunca sea cero
                precio_propio = self.precios.get(bien, 1)
                if precio_propio <= 0:
                    precio_propio = 1  # Precio mínimo de seguridad
                factor_precio = precio_promedio_competencia / precio_propio
                # Limitar el efecto
                factor_precio = min(2.0, max(0.5, factor_precio))
            else:
                factor_precio = 1.0
        else:
            factor_precio = 1.0

        demanda_estimada = int(
            demanda_base * factor_competencia * factor_precio)
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
            capacidad_disponible = self.capacidad_produccion[bien] - \
                self.produccion_actual.get(bien, 0)
            produccion_planificada = min(
                necesidad_produccion, capacidad_disponible)

            # Considerar restricciones financieras
            costo_produccion = produccion_planificada * \
                self.costos_unitarios[bien]
            if costo_produccion > self.dinero * 0.7:  # No usar más del 70% del capital
                produccion_planificada = int(
                    # Evitar división por cero
                    self.dinero * 0.7 / max(1, self.costos_unitarios[bien]))

            plan_produccion[bien] = max(0, produccion_planificada)

        return plan_produccion

    def producir_bien_mejorado(self, bien, cantidad, mercado):
        """Versión mejorada del método de producción"""
        if cantidad <= 0:
            return 0

        costo_unitario = self.costos_unitarios[bien]

        # Considerar eficiencia y economías de escala
        cantidad_efectiva = int(cantidad * self.eficiencia_produccion)
        if cantidad_efectiva > 50:  # Economías de escala
            cantidad_efectiva = int(
                cantidad_efectiva * ConfigEconomica.FACTOR_ECONOMIA_ESCALA)

        # Limitar por disponibilidad de dinero
        # Evitar división por cero
        max_por_dinero = int(self.dinero / max(1, costo_unitario))
        cantidad_efectiva = max(0, min(cantidad_efectiva, max_por_dinero))
        if cantidad_efectiva <= 0:
            return 0

        # Registrar uso de recursos y emisiones
        sistema_ambiental = getattr(mercado.gobierno, 'sostenibilidad', None)
        if sistema_ambiental:
            cantidad_efectiva, _ = sistema_ambiental.registrar_produccion(
                self.nombre, bien, cantidad_efectiva, self.factor_emisiones
            )
        if cantidad_efectiva <= 0:
            return 0

        costo_total = cantidad_efectiva * costo_unitario
        self.dinero -= costo_total

        # Añadir al inventario
        if bien not in self.bienes:
            self.bienes[bien] = []

        for _ in range(cantidad_efectiva):
            costo_unitario_efectivo = costo_unitario * \
                random.uniform(0.95, 1.05)
            self.bienes[bien].append(InventarioBien(
                bien, costo_unitario_efectivo, mercado.bienes))

        self.produccion_actual[bien] = self.produccion_actual.get(
            bien, 0) + cantidad_efectiva
        return cantidad_efectiva

    def ajustar_precios_dinamico(self, mercado, bien):
        """Ajusta precios basado en múltiples factores económicos mejorados"""
        # Validaciones de seguridad más robustas
        if not hasattr(self, 'precios') or bien not in self.precios:
            return
        if not hasattr(self, 'costos_unitarios') or bien not in self.costos_unitarios:
            return
        if not hasattr(self, 'bienes'):
            return

        # Asegurar que el precio actual no sea cero
        if self.precios[bien] <= 0:
            costo_base = self.costos_unitarios.get(bien, 10)
            self.precios[bien] = max(costo_base * 1.2, 1.0)
            return

        try:
            precio_actual = self.precios[bien]
            costo_unitario = max(
                0.01, self.costos_unitarios[bien])  # Evitar cero

            # Factor 1: Análisis de demanda (ventas recientes)
            ventas_recientes = self.obtener_ventas_recientes(
                bien, mercado, 3)  # Últimos 3 ciclos
            demanda_estimada = max(
                1, self.calcular_demanda_estimada(bien, mercado))

            # Protección adicional contra división por cero
            ratio_demanda = ventas_recientes / \
                max(1.0, float(demanda_estimada))

        except (ZeroDivisionError, ValueError, TypeError) as e:
            # En caso de cualquier error numérico, no cambiar precio
            return

        # Factor 2: Nivel de inventario (más sensible)
        stock_actual = len(self.bienes.get(bien, []))
        stock_optimo = max(5, demanda_estimada * 1.5)

        # Evitar división por cero
        ratio_stock = stock_actual / max(1.0, float(stock_optimo))

        # Factor 3: Competencia (más agresiva)
        competidores = [e for e in mercado.getEmpresas() if e !=
                        self and bien in e.precios]
        factor_competencia = 1.0
        if competidores:
            precios_competencia = [e.precios.get(
                bien, 0) for e in competidores if bien in e.precios and e.precios.get(bien, 0) > 0]
            if precios_competencia:
                precio_promedio_competencia = sum(
                    precios_competencia) / max(1, len(precios_competencia))
                if precio_promedio_competencia > 0 and precio_actual > precio_promedio_competencia * 1.1:
                    factor_competencia = 0.95  # Reducir precio para competir
                elif precio_promedio_competencia > 0 and precio_actual < precio_promedio_competencia * 0.9:
                    factor_competencia = 1.05  # Aumentar precio si somos muy baratos

        # Factor 4: Condiciones macroeconómicas
        factor_macro = 1.0
        if hasattr(mercado, 'inflacion_historica') and mercado.inflacion_historica:
            inflacion_actual = mercado.inflacion_historica[-1]
            factor_macro += inflacion_actual * 0.5  # Ajustar por inflación

        if hasattr(mercado, 'crisis_financiera_activa') and mercado.crisis_financiera_activa:
            factor_macro *= 0.95  # Reducir precios durante crisis

        # Factor 5: Estacionalidad (nuevo)
        factor_estacional = 1.0
        if hasattr(mercado.bienes[bien], 'obtener_factor_estacional'):
            mes_actual = mercado.ciclo_actual % 12
            factor_estacional = mercado.bienes[bien].obtener_factor_estacional(
                mes_actual)

        # Calcular ajuste de precio combinado
        ajuste_demanda = - \
            0.1 if ratio_demanda < 0.7 else (0.1 if ratio_demanda > 1.3 else 0)
        ajuste_stock = 0.15 if ratio_stock < 0.5 else (
            -0.1 if ratio_stock > 2.0 else 0)
        ajuste_aleatorio = random.uniform(-0.02, 0.02)  # Variabilidad natural

        factor_total = (1 + ajuste_demanda + ajuste_stock + ajuste_aleatorio) * \
            factor_competencia * factor_macro * factor_estacional

        # Aplicar ajuste con límites
        precio_nuevo = precio_actual * factor_total
        precio_minimo = costo_unitario * 1.05  # Mínimo 5% margen
        precio_maximo = costo_unitario * 4.0   # Máximo 300% margen

        precio_nuevo = max(precio_minimo, min(precio_maximo, precio_nuevo))

        # Limitar cambios drásticos (máximo ±15% por ciclo)
        cambio_maximo = precio_actual * 0.15
        if abs(precio_nuevo - precio_actual) > cambio_maximo:
            if precio_nuevo > precio_actual:
                precio_nuevo = precio_actual + cambio_maximo
            else:
                precio_nuevo = precio_actual - cambio_maximo

        # Asegurar que el precio final nunca sea cero o negativo
        self.precios[bien] = round(max(precio_nuevo, 1.0), 2)

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

    def invertir_tecnologia_limpia(self, monto):
        """Invierte en mejoras para reducir emisiones"""
        if monto <= 0 or self.dinero < monto:
            return False
        self.dinero -= monto
        reduccion = monto / 100000  # Escala de mejora
        self.factor_emisiones = max(
            0.1, self.factor_emisiones * (1 - reduccion))
        return True

    def gestionar_expansion(self):
        """Decide si expandir capacidad basado en rentabilidad"""
        if self.dinero > self.costos_fijos_mensuales * 6:  # 6 meses de reserva
            # Identificar bienes más rentables
            rentabilidades = {}
            for bien in self.precios:
                precio = self.precios[bien]
                costo = self.costos_unitarios[bien]
                # Evitar división por cero más robusta
                rentabilidad = (precio - costo) / \
                    max(0.01, costo) if costo > 0.01 else 0
                rentabilidades[bien] = rentabilidad

            # Expandir capacidad del bien más rentable
            if rentabilidades:
                mejor_bien = max(rentabilidades, key=rentabilidades.get)
                if rentabilidades[mejor_bien] > 0.3:  # 30% de margen mínimo
                    # Costo por unidad de capacidad
                    costo_expansion = self.capacidad_produccion[mejor_bien] * 100
                    if self.dinero > costo_expansion:
                        expansion = int(
                            self.capacidad_produccion[mejor_bien] * self.factor_expansion)
                        self.capacidad_produccion[mejor_bien] += expansion
                        self.dinero -= costo_expansion

    def pagar_costos_operativos(self):
        """Paga costos fijos y salarios con opción de financiamiento bancario"""
        costo_total = self.costos_fijos_mensuales + self.costo_salarios

        if self.dinero >= costo_total:
            self.dinero -= costo_total
            return True
        else:
            # Intentar obtener préstamo bancario antes de despedir
            deficit = costo_total - self.dinero
            if hasattr(self.mercado, 'sistema_bancario') and self.mercado.sistema_bancario.bancos:
                banco = self.mercado.sistema_bancario.bancos[0]
                ingreso_estimado = len(self.empleados) * \
                    3000  # Estimación de ingresos
                prestamo_resultado = banco.otorgar_prestamo(
                    self, deficit * 2, ingreso_estimado)

                # Corregir manejo del resultado (es una tupla)
                prestamo_aprobado = False
                if isinstance(prestamo_resultado, tuple) and prestamo_resultado[0]:
                    prestamo_aprobado = True
                elif prestamo_resultado is True:  # Por compatibilidad
                    prestamo_aprobado = True
                    self.dinero += deficit * 2

                if prestamo_aprobado:
                    # Registrar deuda (simplificado)
                    if not hasattr(self, 'deuda_bancaria'):
                        self.deuda_bancaria = 0
                    self.deuda_bancaria += deficit * 2.2  # Con intereses
                    return True

            # Crisis financiera - despedir empleados como último recurso
            empleados_a_despedir = min(len(self.empleados),
                                       # Asumir salario promedio 3000
                                       int((costo_total - self.dinero) / 3000))
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
                cantidad_producida = self.producir_bien_mejorado(
                    bien, cantidad, mercado)

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
