from .Empresa import Empresa
from ..config.ConfigEconomica import ConfigEconomica
from .InventarioBien import InventarioBien
import random
import logging


class EmpresaProductora(Empresa):
    def __init__(self, nombre, mercado, bienes={}):
        super().__init__(nombre=nombre, bienes=bienes, mercado=mercado)

        # Características financieras mejoradas
        self.dinero = random.randint(ConfigEconomica.DINERO_INICIAL_EMPRESA_PRODUCTORA_MIN,
                                     ConfigEconomica.DINERO_INICIAL_EMPRESA_PRODUCTORA_MAX)

        # Estado financiero y de quiebra
        self.en_quiebra = False
        self.ciclos_sin_actividad = 0
        self.dinero_minimo_operacion = 5000  # Umbral mínimo para operar

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
        try:
            # Protecciones básicas
            if not mercado or not bien or bien not in mercado.bienes:
                return 1  # Demanda mínima de seguridad

            # Demanda basada en población de consumidores
            consumidores = mercado.getConsumidores()
            if not consumidores:
                return 1  # Demanda mínima si no hay consumidores

            empleados = [c for c in consumidores if c.empleado]
            if empleados:
                ingreso_promedio = sum(
                    [c.ingreso_mensual for c in empleados]) / len(empleados)
            else:
                ingreso_promedio = 5000  # Ingreso promedio de fallback

            # Usar el método del bien para calcular demanda base
            demanda_base = mercado.bienes[bien].calcular_demanda_base(
                len(consumidores), ingreso_promedio)

            # Asegurar demanda base mínima
            demanda_base = max(1, demanda_base)

            # Ajustar por competencia
            competidores = [e for e in mercado.getEmpresas() if e !=
                            self and bien in e.bienes]
            factor_competencia = 1.0 / max(1, len(competidores))

            # Ajustar por precio relativo
            if competidores:
                precios_competencia = [e.precios.get(
                    bien, 0) for e in competidores if e.precios.get(bien, 0) > 0]
                if precios_competencia:
                    precio_promedio_competencia = sum(
                        precios_competencia) / len(precios_competencia)

                    # Obtener precio propio, garantizando que nunca sea cero
                    precio_propio = self.precios.get(bien, 1)
                    if precio_propio <= 0:
                        precio_propio = 1  # Precio mínimo de seguridad

                    # Protección adicional contra división por cero
                    if precio_propio > 0 and precio_promedio_competencia > 0:
                        factor_precio = precio_promedio_competencia / precio_propio
                        # Limitar el efecto
                        factor_precio = min(2.0, max(0.5, factor_precio))
                    else:
                        factor_precio = 1.0
                else:
                    factor_precio = 1.0
            else:
                factor_precio = 1.0

            demanda_estimada = int(
                demanda_base * factor_competencia * factor_precio)
            return max(1, demanda_estimada)

        except (ZeroDivisionError, ValueError, TypeError, AttributeError) as e:
            logging.error(
                f"Error calculando demanda estimada para {bien} en {self.nombre}: {e}")
            return 1  # Demanda mínima de seguridad
        except Exception as e:
            logging.error(
                f"Error inesperado calculando demanda para {bien} en {self.nombre}: {e}")
            return 1

    def planificar_produccion(self, mercado):
        """Planifica la producción basada en demanda estimada y capacidad"""
        plan_produccion = {}

        try:
            for bien in self.capacidad_produccion:
                try:
                    demanda_estimada = self.calcular_demanda_estimada(
                        bien, mercado)
                    stock_actual = len(self.bienes.get(bien, []))

                    # Nivel de stock objetivo (1.5x la demanda estimada)
                    stock_objetivo = int(max(1, demanda_estimada) * 1.5)
                    necesidad_produccion = max(
                        0, stock_objetivo - stock_actual)

                    # Limitar por capacidad de producción
                    capacidad_disponible = max(0, self.capacidad_produccion.get(bien, 0) -
                                               self.produccion_actual.get(bien, 0))
                    produccion_planificada = min(
                        necesidad_produccion, capacidad_disponible)

                    # Considerar restricciones financieras
                    costo_unitario = max(
                        0.01, self.costos_unitarios.get(bien, 1))
                    costo_produccion = produccion_planificada * costo_unitario

                    if costo_produccion > self.dinero * 0.7:  # No usar más del 70% del capital
                        produccion_planificada = int(
                            # Evitar división por cero
                            self.dinero * 0.7 / costo_unitario)

                    plan_produccion[bien] = max(0, produccion_planificada)

                except (ZeroDivisionError, ValueError, TypeError, KeyError) as e:
                    logging.error(
                        f"Error planificando producción de {bien} en {self.nombre}: {e}")
                    plan_produccion[bien] = 0
                except Exception as e:
                    logging.error(
                        f"Error inesperado planificando producción de {bien} en {self.nombre}: {e}")
                    plan_produccion[bien] = 0

        except Exception as e:
            logging.error(
                f"Error general en planificación de producción de {self.nombre}: {e}")
            # Retornar un plan vacío en caso de error
            plan_produccion = {bien: 0 for bien in self.capacidad_produccion}

        return plan_produccion

    def producir_bien_mejorado(self, bien, cantidad, mercado):
        """Versión mejorada del método de producción"""
        try:
            if cantidad <= 0:
                return 0

            costo_unitario = max(0.01, self.costos_unitarios.get(bien, 1))

            # Considerar eficiencia y economías de escala
            cantidad_efectiva = int(
                cantidad * max(0.1, self.eficiencia_produccion))
            if cantidad_efectiva > 50:  # Economías de escala
                factor_escala = getattr(
                    ConfigEconomica, 'FACTOR_ECONOMIA_ESCALA', 1.1)
                cantidad_efectiva = int(cantidad_efectiva * factor_escala)

            # Limitar por disponibilidad de dinero
            # Evitar división por cero
            max_por_dinero = int(max(0, self.dinero) / costo_unitario)
            cantidad_efectiva = max(0, min(cantidad_efectiva, max_por_dinero))
            if cantidad_efectiva <= 0:
                return 0

            # Registrar uso de recursos y emisiones
            try:
                sistema_ambiental = getattr(
                    mercado.gobierno, 'sostenibilidad', None)
                if sistema_ambiental:
                    cantidad_efectiva, _ = sistema_ambiental.registrar_produccion(
                        self.nombre, bien, cantidad_efectiva, self.factor_emisiones
                    )
            except Exception as e:
                logging.warning(
                    f"Error en registro ambiental para {self.nombre}: {e}")

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

        except (ZeroDivisionError, ValueError, TypeError, AttributeError) as e:
            logging.error(f"Error produciendo {bien} en {self.nombre}: {e}")
            return 0
        except Exception as e:
            logging.error(
                f"Error inesperado produciendo {bien} en {self.nombre}: {e}")
            return 0

    def ajustar_precios_dinamico(self, mercado, bien):
        """Ajusta precios basado en múltiples factores económicos mejorados"""
        try:
            logging.debug(
                f"{self.nombre}: INICIO ajuste de precio para {bien}")

            # Validaciones de seguridad más robustas
            if not hasattr(self, 'precios') or bien not in self.precios:
                logging.debug(
                    f"{self.nombre}: No tiene precios para {bien}, saliendo")
                return
            if not hasattr(self, 'costos_unitarios') or bien not in self.costos_unitarios:
                logging.debug(
                    f"{self.nombre}: No tiene costos unitarios para {bien}, saliendo")
                return
            if not hasattr(self, 'bienes'):
                logging.debug(
                    f"{self.nombre}: No tiene atributo bienes, saliendo")
                return

            # Asegurar que el precio actual no sea cero
            if self.precios[bien] <= 0:
                costo_base = self.costos_unitarios.get(bien, 10)
                self.precios[bien] = max(costo_base * 1.2, 1.0)
                logging.warning(
                    f"{self.nombre}: Precio de {bien} era <= 0, ajustado a {self.precios[bien]}")
                return

            precio_actual = self.precios[bien]
            costo_unitario = max(
                0.01, self.costos_unitarios[bien])  # Evitar cero

            logging.debug(
                f"{self.nombre}: Precio actual de {bien}: ${precio_actual:.2f}, Costo: ${costo_unitario:.2f}")

            # Factor 1: Análisis de demanda (ventas recientes)
            try:
                ventas_recientes = self.obtener_ventas_recientes(
                    bien, mercado, 3)  # Últimos 3 ciclos
                demanda_estimada = max(
                    1, self.calcular_demanda_estimada(bien, mercado))

                logging.debug(
                    f"{self.nombre}: Ventas recientes de {bien}: {ventas_recientes}, Demanda estimada: {demanda_estimada}")

                # Protección adicional contra división por cero
                if demanda_estimada == 0:
                    logging.warning(
                        f"{self.nombre}: Demanda estimada es 0 para {bien}, usando 1")
                    demanda_estimada = 1

                ratio_demanda = ventas_recientes / float(demanda_estimada)
                logging.debug(
                    f"{self.nombre}: Ratio demanda para {bien}: {ratio_demanda}")

            except (ZeroDivisionError, ValueError, TypeError) as e:
                logging.error(
                    f"{self.nombre}: Error calculando ratio demanda para {bien}: {e}")
                # En caso de cualquier error numérico, no cambiar precio
                return

            # Factor 2: Nivel de inventario (más sensible)
            stock_actual = len(self.bienes.get(bien, []))
            stock_optimo = max(5, demanda_estimada * 1.5)

            # Evitar división por cero
            if stock_optimo == 0:
                logging.warning(
                    f"{self.nombre}: Stock óptimo es 0 para {bien}, usando 5")
                stock_optimo = 5

            ratio_stock = stock_actual / float(stock_optimo)
            logging.debug(
                f"{self.nombre}: Stock actual de {bien}: {stock_actual}, Óptimo: {stock_optimo}, Ratio: {ratio_stock}")

            # Factor 3: Competencia (más agresiva)
            competidores = [e for e in mercado.getEmpresas(
            ) if e != self and bien in e.precios]
            factor_competencia = 1.0
            if competidores:
                precios_competencia = [e.precios.get(
                    bien, 0) for e in competidores if bien in e.precios and e.precios.get(bien, 0) > 0]
                if precios_competencia:
                    precio_promedio_competencia = sum(
                        precios_competencia) / len(precios_competencia)
                    logging.debug(
                        f"{self.nombre}: Precio promedio competencia para {bien}: ${precio_promedio_competencia:.2f}")

                    if precio_promedio_competencia > 0 and precio_actual > precio_promedio_competencia * 1.1:
                        factor_competencia = 0.95  # Reducir precio para competir
                        logging.debug(
                            f"{self.nombre}: Precio alto vs competencia, factor: {factor_competencia}")
                    elif precio_promedio_competencia > 0 and precio_actual < precio_promedio_competencia * 0.9:
                        factor_competencia = 1.05  # Aumentar precio si somos muy baratos
                        logging.debug(
                            f"{self.nombre}: Precio bajo vs competencia, factor: {factor_competencia}")

            # Factor 4: Condiciones macroeconómicas
            factor_macro = 1.0
            if hasattr(mercado, 'inflacion_historica') and mercado.inflacion_historica:
                inflacion_actual = mercado.inflacion_historica[-1]
                factor_macro += inflacion_actual * 0.5  # Ajustar por inflación
                logging.debug(
                    f"{self.nombre}: Factor macro por inflación: {factor_macro}")

            if hasattr(mercado, 'crisis_financiera_activa') and mercado.crisis_financiera_activa:
                factor_macro *= 0.95  # Reducir precios durante crisis
                logging.debug(
                    f"{self.nombre}: Factor macro por crisis: {factor_macro}")

            # Factor 5: Estacionalidad (nuevo)
            factor_estacional = 1.0
            if hasattr(mercado.bienes[bien], 'obtener_factor_estacional'):
                mes_actual = mercado.ciclo_actual % 12
                factor_estacional = mercado.bienes[bien].obtener_factor_estacional(
                    mes_actual)
                logging.debug(
                    f"{self.nombre}: Factor estacional para {bien}: {factor_estacional}")

            # Calcular ajuste de precio combinado
            ajuste_demanda = - \
                0.1 if ratio_demanda < 0.7 else (
                    0.1 if ratio_demanda > 1.3 else 0)
            ajuste_stock = 0.15 if ratio_stock < 0.5 else (
                -0.1 if ratio_stock > 2.0 else 0)
            # Variabilidad natural
            ajuste_aleatorio = random.uniform(-0.02, 0.02)

            factor_total = (1 + ajuste_demanda + ajuste_stock + ajuste_aleatorio) * \
                factor_competencia * factor_macro * factor_estacional

            logging.debug(
                f"{self.nombre}: Factores para {bien} - demanda: {ajuste_demanda}, stock: {ajuste_stock}, total: {factor_total}")

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
            precio_final = round(max(precio_nuevo, 1.0), 2)

            logging.debug(
                f"{self.nombre}: Precio de {bien} cambiado de ${precio_actual:.2f} a ${precio_final:.2f}")
            self.precios[bien] = precio_final

        except Exception as e:
            logging.error(
                f"{self.nombre}: Error inesperado ajustando precio de {bien}: {e}")
            logging.error(
                f"Estado: precio_actual={self.precios.get(bien, 'N/A')}, costo={self.costos_unitarios.get(bien, 'N/A')}")

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
        try:
            # Validar y corregir valores antes de usar
            if not hasattr(self, 'costos_fijos_mensuales') or self.costos_fijos_mensuales <= 0:
                self.costos_fijos_mensuales = 100.0  # Valor por defecto
            
            if not hasattr(self, 'costo_salarios') or self.costo_salarios < 0:
                self.costo_salarios = 0
                
            costo_total = self.costos_fijos_mensuales + self.costo_salarios

            if self.dinero >= costo_total:
                self.dinero -= costo_total
                return True
            else:
                # Intentar obtener préstamo bancario antes de despedir
                deficit = costo_total - self.dinero
                if hasattr(self.mercado, 'sistema_bancario') and self.mercado.sistema_bancario.bancos:
                    banco = self.mercado.sistema_bancario.bancos[0]
                    
                    # Cálculo seguro del ingreso estimado
                    num_empleados = max(0, len(self.empleados)) if hasattr(self, 'empleados') else 0
                    ingreso_estimado = num_empleados * 3000  # Estimación de ingresos
                    
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
                num_empleados = len(self.empleados) if hasattr(self, 'empleados') and self.empleados else 0
                if num_empleados > 0:
                    # Cálculo seguro para empleados a despedir
                    empleados_a_despedir = min(num_empleados,
                                               max(1, int((costo_total - self.dinero) / 3000)))  # Evitar 0
                    for _ in range(empleados_a_despedir):
                        if self.empleados:
                            empleado = self.empleados.pop()
                            if hasattr(empleado, 'perder_empleo'):
                                empleado.perder_empleo()
                            if hasattr(empleado, 'ingreso_mensual'):
                                self.costo_salarios -= empleado.ingreso_mensual
                return False
                
        except ZeroDivisionError as e:
            logging.error(f"División por cero en pagar_costos_operativos de {self.nombre}: {e}")
            # Aplicar valores de emergencia
            self.costos_fijos_mensuales = max(100.0, getattr(self, 'costos_fijos_mensuales', 100.0))
            self.costo_salarios = max(0, getattr(self, 'costo_salarios', 0))
            return False
        except Exception as e:
            logging.error(f"Error en pagar_costos_operativos de {self.nombre}: {e}")
            return False

    def verificar_estado_financiero(self):
        """Verifica si la empresa está en quiebra o puede seguir operando"""
        costos_totales = self.costos_fijos_mensuales + self.costo_salarios

        # Marcar en quiebra si no puede cubrir costos básicos por 3 ciclos consecutivos
        if self.dinero < costos_totales:
            self.ciclos_sin_actividad += 1
            if self.ciclos_sin_actividad >= 3:
                self.en_quiebra = True
                logging.warning(
                    f"{self.nombre}: EMPRESA EN QUIEBRA - Dinero: ${self.dinero:.2f}, Costos: ${costos_totales:.2f}")
                return False
        else:
            self.ciclos_sin_actividad = 0  # Resetear contador si tiene fondos

        # Verificar si tiene dinero mínimo para operaciones básicas
        if self.dinero < self.dinero_minimo_operacion:
            logging.debug(
                f"{self.nombre}: Fondos insuficientes para operaciones (${self.dinero:.2f} < ${self.dinero_minimo_operacion:.2f})")
            return False

        return True

    def ciclo_persona(self, ciclo, mercado):
        """Ciclo principal de la empresa productora"""
        try:
            logging.debug(
                f"INICIO ciclo {ciclo} para {self.nombre} - Dinero: ${self.dinero:.2f}")

            # Verificar estado financiero antes de cualquier operación
            if not self.verificar_estado_financiero():
                if self.en_quiebra:
                    logging.warning(
                        f"{self.nombre}: EMPRESA EN QUIEBRA - Saltando ciclo")
                    return False
                else:
                    logging.debug(
                        f"{self.nombre}: Fondos insuficientes - Saltando operaciones complejas")
                    return False

            # CORRECCIÓN: Asegurar que la empresa tenga al menos un empleado para operar
            if len(self.empleados) == 0 and self.dinero > 5000:  # Solo si tiene dinero suficiente
                try:
                    logging.debug(f"{self.nombre}: Intentando contratar empleado inicial...")
                    # Contratar directamente un consumidor desempleado
                    consumidores_desempleados = [c for c in mercado.getConsumidores() if not c.empleado]
                    if consumidores_desempleados:
                        consumidor = random.choice(consumidores_desempleados)
                        self.contratar(consumidor)
                        logging.debug(f"{self.nombre}: Empleado inicial contratado")
                except Exception as e:
                    logging.warning(f"{self.nombre}: No pudo contratar empleado inicial: {e}")
            
            # Si aún no tiene empleados, usar modo de operación limitada
            if len(self.empleados) == 0:
                logging.debug(f"{self.nombre}: Operando sin empleados - capacidad limitada")
                # La empresa puede funcionar con capacidad muy reducida pero sin dividir por cero

            # Pagar costos operativos
            try:
                logging.debug(f"{self.nombre}: Pagando costos operativos...")
                resultado_costos = self.pagar_costos_operativos()
                logging.debug(
                    f"{self.nombre}: Costos pagados - Resultado: {resultado_costos}, Dinero restante: ${self.dinero:.2f}")

                # Si no pudo pagar costos, no continuar con operaciones
                if not resultado_costos:
                    logging.warning(
                        f"{self.nombre}: No pudo pagar costos operativos - Saltando producción")
                    return False
            except ZeroDivisionError as e:
                logging.error(f"DIVISIÓN POR CERO en pago de costos de {self.nombre}: {e}")
                self._aplicar_correcciones_division_cero()
                return False

            # Planificar y ejecutar producción
            try:
                logging.debug(f"{self.nombre}: Planificando producción...")
                plan_produccion = self.planificar_produccion(mercado)
                logging.debug(
                    f"{self.nombre}: Plan de producción: {plan_produccion}")
            except ZeroDivisionError as e:
                logging.error(f"DIVISIÓN POR CERO en planificación de {self.nombre}: {e}")
                self._aplicar_correcciones_division_cero()
                plan_produccion = {}  # Plan vacío de emergencia

            for bien, cantidad in plan_produccion.items():
                if cantidad > 0:
                    try:
                        logging.debug(
                            f"{self.nombre}: Produciendo {cantidad} unidades de {bien}")
                        cantidad_producida = self.producir_bien_mejorado(
                            bien, cantidad, mercado)
                        logging.debug(
                            f"{self.nombre}: Producidas {cantidad_producida} unidades de {bien}")
                    except ZeroDivisionError as e:
                        logging.error(
                            f"DIVISION POR CERO en producción de {self.nombre} para {bien}: {e}")
                        logging.error(
                            f"Estado: dinero={self.dinero}, costo_unitario={self.costos_unitarios.get(bien, 'N/A')}")
                        continue
                    except Exception as e:
                        logging.error(
                            f"Error en producción de {self.nombre} para {bien}: {e}")
                        continue

            # Ajustar precios dinámicamente solo si tiene inventario o puede producir
            logging.debug(f"{self.nombre}: Ajustando precios dinámicamente...")
            for bien in list(self.precios.keys()):  # Crear copia de las llaves
                try:
                    precio_anterior = self.precios.get(bien, 0)
                    logging.debug(
                        f"{self.nombre}: Ajustando precio de {bien} (actual: ${precio_anterior:.2f})")
                    self.ajustar_precios_dinamico(mercado, bien)
                    precio_nuevo = self.precios.get(bien, 0)
                    logging.debug(
                        f"{self.nombre}: Precio de {bien} ajustado: ${precio_anterior:.2f} -> ${precio_nuevo:.2f}")
                except ZeroDivisionError as e:
                    logging.error(
                        f"DIVISION POR CERO en ajuste de precios de {self.nombre} para {bien}: {e}")
                    logging.error(
                        f"Estado precio: precio_actual={self.precios.get(bien, 'N/A')}, costo={self.costos_unitarios.get(bien, 'N/A')}")
                    continue
                except Exception as e:
                    logging.error(
                        f"Error en ajuste de precios de {self.nombre} para {bien}: {e}")
                    continue

            # Considerar expansión solo si tiene fondos suficientes
            if ciclo % 5 == 0 and self.dinero > self.costos_fijos_mensuales * 2:  # Cada 5 ciclos y con reservas
                try:
                    logging.debug(f"{self.nombre}: Evaluando expansión...")
                    self.gestionar_expansion()
                    logging.debug(f"{self.nombre}: Expansión evaluada")
                except ZeroDivisionError as e:
                    logging.error(
                        f"DIVISION POR CERO en expansión de {self.nombre}: {e}")
                    logging.error(
                        f"Estado expansión: dinero={self.dinero}, costos_fijos={self.costos_fijos_mensuales}")
                except Exception as e:
                    logging.error(f"Error en expansión de {self.nombre}: {e}")

            # Actividades de empresa base (acciones, dividendos)
            try:
                logging.debug(
                    f"{self.nombre}: Ejecutando actividades financieras...")
                self.emitir_acciones(5, mercado.mercado_financiero)
                self.distribuir_dividendos(mercado.mercado_financiero)
                logging.debug(
                    f"{self.nombre}: Actividades financieras completadas")
            except Exception as e:
                logging.error(
                    f"Error en actividades financieras de {self.nombre}: {e}")

            logging.debug(
                f"FIN ciclo {ciclo} para {self.nombre} - Dinero final: ${self.dinero:.2f}")

        except ZeroDivisionError as e:
            logging.error(f"DIVISIÓN POR CERO en ciclo de {self.nombre}: {e}")
            logging.error(f"Estado: dinero={self.dinero:.2f}, empleados={len(self.empleados)}")
            # Aplicar correcciones de emergencia
            self._aplicar_correcciones_division_cero()
            
        except Exception as e:
            logging.error(f"Error general en ciclo de {self.nombre}: {e}")
            # Agregar más información de debug
            logging.error(f"Estado completo de {self.nombre}:")
            logging.error(f"  - Dinero: ${self.dinero:.2f}")
            logging.error(f"  - Empleados: {len(self.empleados)}")
            logging.error(f"  - Costos fijos: ${self.costos_fijos_mensuales}")
            logging.error(f"  - Costo salarios: ${self.costo_salarios}")
            # Solo mostrar primeros 3
            logging.error(
                f"  - Precios: {dict(list(self.precios.items())[:3])}...")
            logging.error(
                f"  - Costos unitarios: {dict(list(self.costos_unitarios.items())[:3])}...")

        # Reset de producción actual para próximo ciclo
        for bien in self.produccion_actual:
            self.produccion_actual[bien] = 0

    def _aplicar_correcciones_division_cero(self):
        """Aplica correcciones de emergencia para evitar divisiones por cero"""
        try:
            # Corregir precios que sean cero o negativos
            for bien in self.precios:
                if self.precios[bien] <= 0:
                    self.precios[bien] = 1.0  # Precio mínimo de seguridad
                    logging.warning(f"{self.nombre}: Precio de {bien} corregido a $1.00")
            
            # Corregir costos unitarios que sean cero
            for bien in self.costos_unitarios:
                if self.costos_unitarios[bien] <= 0:
                    self.costos_unitarios[bien] = 0.5  # Costo mínimo de seguridad
                    logging.warning(f"{self.nombre}: Costo unitario de {bien} corregido a $0.50")
            
            # Asegurar que acciones_emitidas no sea cero
            if hasattr(self, 'acciones_emitidas') and self.acciones_emitidas <= 0:
                self.acciones_emitidas = 1
                logging.warning(f"{self.nombre}: Acciones emitidas corregidas a 1")
            
            # Asegurar capacidad de producción mínima
            for bien in self.capacidad_produccion:
                if self.capacidad_produccion[bien] <= 0:
                    self.capacidad_produccion[bien] = 1
                    logging.warning(f"{self.nombre}: Capacidad de producción de {bien} corregida a 1")
            
            # Asegurar que los costos fijos no sean cero
            if self.costos_fijos_mensuales <= 0:
                self.costos_fijos_mensuales = 100.0  # Costo fijo mínimo
                logging.warning(f"{self.nombre}: Costos fijos corregidos a $100.00")
                
            logging.info(f"{self.nombre}: Correcciones de división por cero aplicadas")
            
        except Exception as e:
            logging.error(f"{self.nombre}: Error aplicando correcciones: {e}")
