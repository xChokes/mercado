from .Empresa import Empresa
from ..config.ConfigEconomica import ConfigEconomica
from .InventarioBien import InventarioBien
import random
import logging
import math


class EmpresaProductora(Empresa):
    def __init__(self, nombre, mercado, bienes={}):
        super().__init__(nombre=nombre, bienes=bienes, mercado=mercado)

                # INICIALIZACIÓN MÁS ROBUSTA: 5x capital anterior
        capital_base = random.randint(50000, 120000)  # 5x anterior (era 10K-24K)
        capital_adicional = random.randint(30000, 80000)  # Buffer adicional
        self.dinero = capital_base + capital_adicional  # Total: 80K-200K
        
        # Dinero mínimo para operaciones más realista
        self.dinero_minimo_operacion = 15000  # 3x anterior (era 5K)
        
        # Costos más balanceados y realistas
        self.costos_fijos_mensuales = random.randint(2000, 6000)  # Más bajo que antes (era 3K-8K)
        self.costo_salarios = random.randint(8000, 18000)  # Rango más amplio pero controlado
        
        # ATRIBUTOS FALTANTES PARA MANEJO DE CRISIS
        self.ciclos_sin_actividad = 0  # Contador de ciclos sin actividad económica
        self.ciclos_crisis_financiera = 0  # Contador de ciclos en crisis financiera
        self.en_quiebra = False  # Estado de quiebra
        self.costos_fijos_originales = None  # Para guardar costos originales durante crisis

        # Capacidades de producción con límites realistas más estrictos
        self.capacidad_produccion = {}
        self.produccion_actual = {}
        self.eficiencia_produccion = random.uniform(0.95, 1.0)  # Eficiencia base ultra conservadora
        self.eficiencia_maxima = 1.05  # Límite superior ultra estricto (era 1.15)
        self.eficiencia_minima = 0.85  # Límite inferior ultra conservador (era 0.80)
        self.degeneracion_factor = 0.995  # Factor de degeneración más agresivo (era 0.999)

        # Tecnología limpia
        self.factor_emisiones = 1.0  # 1.0 sin mejoras

        # MEJORA: Costos de producción más realistas y escalables
        self.costos_unitarios = {}
        base_costos_fijos = random.randint(5000, 15000)  # Costos más moderados
        self.costos_fijos_mensuales = base_costos_fijos
        self.costos_fijos_originales = base_costos_fijos  # Para recuperación
        self.costos_variables = {}

        # Empleados y recursos humanos
        self.empleados = []
        self.capacidad_empleo = random.randint(5, 25)  # Capacidad más realista
        self.costo_salarios = 0

        # MEJORA: Estrategia empresarial más balanceada
        self.estrategia_precios = random.choice(
            ['lider_costos', 'diferenciacion', 'nicho'])
        self.aversion_riesgo_empresa = random.uniform(0.4, 0.7)  # Riesgo más balanceado
        self.factor_expansion = random.uniform(0.03, 0.15)  # Expansión más conservadora

        # Inicializar capacidades para todos los bienes del mercado
        for bien in mercado.bienes.keys():
            base_capacity = random.randint(ConfigEconomica.PRODUCCION_BASE_MIN,
                                           ConfigEconomica.PRODUCCION_BASE_MAX)
            self.capacidad_produccion[bien] = base_capacity
            self.produccion_actual[bien] = 0

            # Costos basados en categoría del bien
            categorias_map = getattr(ConfigEconomica, 'CATEGORIAS_BIENES_MAP', None)
            if isinstance(categorias_map, dict):
                categoria = categorias_map.get(bien, 'servicios')
            else:
                categoria = 'servicios'
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

            # CORRECCIÓN CRÍTICA: Evitar división por cero
            costo_unitario = max(1.0, self.costos_unitarios.get(bien, 10.0))  # Mínimo más alto

            # Considerar eficiencia y economías de escala
            cantidad_efectiva = int(
                cantidad * max(0.1, self.eficiencia_produccion))
                
            # NUEVA: Aplicar degeneración por sobreproducción
            if cantidad_efectiva > 30:  # Umbral de sobreproducción
                self.eficiencia_produccion *= self.degeneracion_factor
                # Aplicar límites de eficiencia
                self.eficiencia_produccion = max(self.eficiencia_minima, 
                                               min(self.eficiencia_maxima, self.eficiencia_produccion))
                
            if cantidad_efectiva > 50:  # Economías de escala
                factor_escala = getattr(
                    ConfigEconomica, 'FACTOR_ECONOMIA_ESCALA', 1.1)
                cantidad_efectiva = int(cantidad_efectiva * factor_escala)

            # NUEVO: Limitar por disponibilidad de INSUMOS (si existe cadena de suministro)
            try:
                cantidad_efectiva = self._aplicar_consumo_insumos(cantidad_efectiva)
            except Exception as _:
                # Si hay cualquier problema, continuar sin consumo de insumos
                pass

            # CORRECCIÓN: Limitar por disponibilidad de dinero de forma segura
            dinero_disponible = max(0, self.dinero)
            if dinero_disponible < costo_unitario:
                # No hay suficiente dinero para producir ni una unidad
                return 0
            
            max_por_dinero = int(dinero_disponible / costo_unitario)
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

    # --- Cadena de suministro: consumo de insumos ---
    def _aplicar_consumo_insumos(self, cantidad_deseada: int) -> int:
        """Reduce inventario de insumos en proporción a la producción deseada.
        Devuelve la cantidad efectiva que se puede producir dados los insumos.
        Si no existen estructuras de insumos, retorna cantidad_deseada sin cambios.
        """
        if cantidad_deseada <= 0:
            return 0
        # Si la empresa no está integrada con el sistema de insumos, no limitar
        if not hasattr(self, 'insumos_requeridos') or not isinstance(getattr(self, 'insumos_requeridos'), dict):
            return cantidad_deseada
        if not hasattr(self, 'inventario_insumos') or not isinstance(getattr(self, 'inventario_insumos'), dict):
            return cantidad_deseada

        # Calcular máximo producible por cada insumo
        max_por_insumo = []
        for insumo, meta in self.insumos_requeridos.items():
            consumo_u = float(meta.get('consumo_por_unidad', 0))
            if consumo_u <= 0:
                continue
            stock = int(self.inventario_insumos.get(insumo, 0))
            producible = int(stock // consumo_u) if consumo_u > 0 else cantidad_deseada
            max_por_insumo.append(producible)

        if max_por_insumo:
            cantidad_posible = max(0, min(min(max_por_insumo), int(cantidad_deseada)))
        else:
            cantidad_posible = int(cantidad_deseada)

        if cantidad_posible <= 0:
            return 0

        # Consumir insumos requeridos para la cantidad posible
        for insumo, meta in self.insumos_requeridos.items():
            consumo_u = float(meta.get('consumo_por_unidad', 0))
            if consumo_u <= 0:
                continue
            requerido = int(math.ceil(consumo_u * cantidad_posible))
            stock = int(self.inventario_insumos.get(insumo, 0))
            self.inventario_insumos[insumo] = max(0, stock - requerido)

        return cantidad_posible

    def ajustar_precios_dinamico(self, mercado, bien):
        """Ajusta precios basado en múltiples factores económicos mejorados"""
        try:
            logging.debug(
                f"{self.nombre}: INICIO ajuste de precio para {bien}")

            # NUEVA VALIDACIÓN: Verificar que el bien existe en el mercado
            if not hasattr(mercado, 'bienes') or bien not in mercado.bienes:
                logging.debug(
                    f"{self.nombre}: Bien {bien} no existe en el mercado, omitiendo ajuste de precio")
                return

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
        """Paga los costos operativos con sistema de crisis progresiva mejorado"""
        try:
            costo_total = self._calcular_costos_operativos()
            
            # Validación de rango numérico para evitar overflow
            if costo_total <= 0 or costo_total > 1e9:
                logging.warning(f"{self.nombre}: Costo operativo inválido: {costo_total}")
                costo_total = max(1000, min(costo_total, 50000))  # Normalizar entre límites seguros
            
            # Crisis progresiva: Intentar pagos múltiples antes de fallar
            if self.dinero >= costo_total:
                self.dinero = max(0, self.dinero - costo_total)  # Evitar valores negativos
                self.ciclos_crisis_financiera = 0  # Reset crisis
                return True
            
            # NIVEL 1: Préstamo de emergencia
            if self.ciclos_crisis_financiera <= 1:
                prestamo_necesario = min(costo_total - self.dinero + 5000, 100000)  # Limitar préstamo máximo
                if self._solicitar_prestamo_emergencia(prestamo_necesario):
                    self.dinero = max(0, self.dinero - costo_total)
                    return True
            
            # NIVEL 2: Reducción de costos operativos (30% vs 20% anterior)
            if self.ciclos_crisis_financiera <= 3:
                costo_reducido = costo_total * 0.7  # Más agresivo: 30% reducción
                if self.dinero >= costo_reducido:
                    self.dinero = max(0, self.dinero - costo_reducido)
                    self.eficiencia_produccion *= 0.97  # Menor penalización (0.97 vs 0.95)
                    # Aplicar límites de eficiencia
                    self.eficiencia_produccion = max(self.eficiencia_minima, 
                                                   min(self.eficiencia_maxima, self.eficiencia_produccion))
                    return True
            
            # NIVEL 3: Despidos graduales (reducir costos 40%)
            if self.ciclos_crisis_financiera <= 4:
                if len(self.empleados) > 1:  # CORREGIDO: usar len() para obtener el número de empleados
                    empleados_despedir = min(2, len(self.empleados) // 3)  # CORREGIDO: usar len()
                    self._despedir_empleados(empleados_despedir)
                    costo_total = self._calcular_costos_operativos()  # Recalcular
                    
                    if self.dinero >= costo_total:
                        self.dinero = max(0, self.dinero - costo_total)
                        return True
            
            # NIVEL 4: Pago parcial como último recurso (más generoso)
            if self.dinero > 0:
                pago_parcial = min(self.dinero, costo_total * 0.7)  # 70% vs 60% anterior
                self.dinero = max(0, self.dinero - pago_parcial)
                self.eficiencia_produccion *= 0.95  # Menor penalización (0.95 vs 0.90)
                # Aplicar límites de eficiencia
                self.eficiencia_produccion = max(self.eficiencia_minima, 
                                               min(self.eficiencia_maxima, self.eficiencia_produccion))
                return True
            
            return False
            
        except (OverflowError, ValueError, ArithmeticError) as e:
            logging.error(f"Error numérico en pagar_costos_operativos de {self.nombre}: {e}")
            # Fallback seguro: reset básico
            self.dinero = max(0, self.dinero)
            return False
        except Exception as e:
            logging.error(f"Error general en pagar_costos_operativos de {self.nombre}: {e}")
            return False

    def _calcular_costos_operativos(self):
        """Calcula costos operativos totales con protecciones contra overflow"""
        try:
            # Costos fijos básicos (rentas, servicios, etc.)
            costos_fijos = max(100, min(self.costos_fijos_mensuales, 10000))  # Limitar entre 100-10K
            
            # Costos de salarios con protección contra números negativos
            costo_salarios = 0
            if hasattr(self, 'empleados') and self.empleados:
                salario_promedio = max(800, min(3000, getattr(self, 'costo_salarios', 1500) / max(1, len(self.empleados))))
                costo_salarios = len(self.empleados) * salario_promedio
                costo_salarios = min(costo_salarios, 50000)  # Máximo 50K en salarios
            
            # Costos de mantenimiento (5% de capacidad de producción total)
            mantenimiento = 0
            if hasattr(self, 'capacidad_produccion'):
                capacidad_total = sum(self.capacidad_produccion.values())
                mantenimiento = max(50, min(capacidad_total * 0.05, 2000))  # Entre 50-2K
            
            # Costos de inventario (2% del valor del inventario)
            costo_inventario = 0
            if hasattr(self, 'bienes'):
                for bien, items in self.bienes.items():
                    if items:
                        costo_promedio = self.costos_unitarios.get(bien, 10)
                        costo_inventario += len(items) * costo_promedio * 0.02
                costo_inventario = min(costo_inventario, 5000)  # Máximo 5K
            
            # Sumar todos los costos con límites de seguridad
            total = costos_fijos + costo_salarios + mantenimiento + costo_inventario
            
            # Protección final contra overflow y valores extremos
            total = max(200, min(total, 100000))  # Entre 200 y 100K
            
            return total
            
        except (OverflowError, ValueError, ArithmeticError) as e:
            logging.error(f"Error numérico calculando costos operativos en {self.nombre}: {e}")
            return 1000  # Costo de seguridad básico
        except Exception as e:
            logging.error(f"Error general calculando costos operativos en {self.nombre}: {e}")
            return 1000

    def verificar_estado_financiero(self):
        """Verifica si la empresa está en quiebra o puede seguir operando"""
        costos_totales = max(100.0, self.costos_fijos_mensuales + self.costo_salarios)

        # MEJORA: Sistema más resiliente para evitar quiebras inmediatas
        if self.dinero < costos_totales:
            self.ciclos_sin_actividad += 1
            
            # Sistema de ayuda progresiva antes de la quiebra
            if self.ciclos_sin_actividad == 1:
                # Primer ciclo: Reducir costos operativos
                if not hasattr(self, 'costos_fijos_originales'):
                    self.costos_fijos_originales = self.costos_fijos_mensuales
                self.costos_fijos_mensuales *= 0.8
                logging.info(f"{self.nombre}: Reduciendo costos operativos por dificultades financieras")
            
            elif self.ciclos_sin_actividad == 2:
                # Segundo ciclo: Buscar financiamiento de emergencia
                if hasattr(self.mercado, 'sistema_bancario') and self.mercado.sistema_bancario.bancos:
                    banco = self.mercado.sistema_bancario.bancos[0]
                    prestamo_emergencia = costos_totales * 3  # 3 meses de supervivencia
                    
                    # Solicitar préstamo de emergencia con condiciones flexibles
                    resultado = banco.otorgar_prestamo(self, prestamo_emergencia, self.dinero + 1000)
                    if isinstance(resultado, tuple) and resultado[0]:
                        self.dinero += prestamo_emergencia
                        if not hasattr(self, 'deuda_bancaria'):
                            self.deuda_bancaria = 0
                        self.deuda_bancaria += prestamo_emergencia * 1.1
                        self.ciclos_sin_actividad = 0  # Reset contador
                        logging.info(f"{self.nombre}: Préstamo de emergencia obtenido - ${prestamo_emergencia:.2f}")
                        return True
            
            elif self.ciclos_sin_actividad >= 5:  # Aumentado de 3 a 5 ciclos
                # Última oportunidad: Rescate gubernamental o fusión
                if hasattr(self.mercado, 'rescate_empresarial'):
                    rescate_exitoso = self.mercado.rescate_empresarial.evaluar_rescate(self)
                    if rescate_exitoso:
                        self.ciclos_sin_actividad = 0
                        logging.info(f"{self.nombre}: Rescatada por el gobierno")
                        return True
                
                # Si no hay rescate, entonces quiebra
                self.en_quiebra = True
                logging.warning(
                    f"{self.nombre}: EMPRESA EN QUIEBRA después de 5 ciclos - Dinero: ${self.dinero:.2f}, Costos: ${costos_totales:.2f}")
                return False
        else:
            # Empresa estable, reset contador
            self.ciclos_sin_actividad = max(0, self.ciclos_sin_actividad - 1)
            
            # MEJORA: Recuperación gradual de costos si la empresa se estabiliza
            if self.ciclos_sin_actividad == 0 and hasattr(self, 'costos_fijos_originales'):
                self.costos_fijos_mensuales = min(
                    self.costos_fijos_originales,
                    self.costos_fijos_mensuales * 1.05  # Recuperación gradual del 5%
                )

        return True

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
            
            # MEJORADO: Filtrar solo bienes válidos que existen en el mercado
            bienes_validos = [bien for bien in self.precios.keys() 
                             if hasattr(mercado, 'bienes') and bien in mercado.bienes]
            
            for bien in bienes_validos:
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

    def _despedir_empleados(self, cantidad):
        """Despide una cantidad específica de empleados para reducir costos"""
        try:
            if not hasattr(self, 'empleados') or not self.empleados:
                return 0
            
            empleados_despedidos = 0
            empleados_a_despedir = min(cantidad, len(self.empleados))
            
            for _ in range(empleados_a_despedir):
                if self.empleados:
                    empleado = self.empleados.pop()
                    empleado.empleado = False  # Marcar como desempleado
                    empleado.empresa = None
                    empleados_despedidos += 1
            
            # Recalcular costo de salarios
            if hasattr(self, 'costo_salarios') and len(self.empleados) > 0:
                salario_promedio = self.costo_salarios / max(1, len(self.empleados) + empleados_despedidos)
                self.costo_salarios = len(self.empleados) * salario_promedio
            else:
                self.costo_salarios = 0
            
            logging.info(f"{self.nombre}: Despidió {empleados_despedidos} empleados por crisis financiera")
            return empleados_despedidos
            
        except Exception as e:
            logging.error(f"Error despidiendo empleados en {self.nombre}: {e}")
            return 0

    def _solicitar_prestamo_emergencia(self, monto):
        """Solicita un préstamo de emergencia al sistema bancario"""
        try:
            if not hasattr(self.mercado, 'sistema_bancario') or not self.mercado.sistema_bancario.bancos:
                return False
            
            # Intentar con cada banco
            for banco in self.mercado.sistema_bancario.bancos:
                try:
                    resultado = banco.solicitar_prestamo(self, monto, 24)  # 24 meses
                    if isinstance(resultado, tuple) and resultado[0]:
                        logging.info(f"{self.nombre}: Préstamo de emergencia aprobado - ${monto:,.2f}")
                        return True
                except Exception as e:
                    logging.debug(f"Banco {banco.nombre} rechazó préstamo para {self.nombre}: {e}")
                    continue
            
            return False
            
        except Exception as e:
            logging.error(f"Error solicitando préstamo de emergencia para {self.nombre}: {e}")
            return False
