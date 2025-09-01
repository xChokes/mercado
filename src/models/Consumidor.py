from .Empresa import Empresa
from .Persona import Persona
from ..config.ConfigEconomica import ConfigEconomica
import random
import numpy as np
import math


class Consumidor(Persona):
    def __init__(self, nombre, mercado, bienes={}, config_hetero=None):
        super().__init__(mercado)
        self.nombre = nombre
        self.mercado = mercado  # Referencia al mercado
        self.bienes = bienes if bienes else {}
        
        # Cargar configuración de heterogeneidad
        self.config_hetero = config_hetero or {}
        
        # Distribución heterogénea de ingresos iniciales
        self.dinero = self._generar_dinero_inicial()
        self.historial_compras = {}

        # Características demográficas
        self.edad = random.randint(18, 80)
        self.estado_demografico = self._determinar_estado_demografico()

        # Características laborales
        # 90% empleados inicialmente
        self.empleado = random.choice([True, False])
        if random.random() > 0.1:
            self.empleado = True

        # Ingreso heterogéneo usando distribución lognormal
        self.ingreso_mensual = self._generar_ingreso_inicial() if self.empleado else 0
        self.empleador = None

        # Multiplicador de productividad
        self.habilidades_base = random.uniform(0.5, 1.5)
        self.habilidades = self.habilidades_base

        # Perfil de habilidades por sector y afiliación sindical
        self.habilidades_sectoriales = {}
        self.sindicato = None
        if hasattr(self.mercado, 'mercado_laboral'):
            perfil = self.mercado.mercado_laboral.crear_perfil()
            self.habilidades_sectoriales = perfil.habilidades
            # Asignar sindicato de forma probabilística
            self.sindicato = self.mercado.mercado_laboral.asignar_sindicato(
                self)

        # Características económicas heterogéneas
        self.propension_consumo_base = random.uniform(0.70, 0.95)
        self.propension_consumo = self.propension_consumo_base  # Entre 70% y 95%
        self.propension_ahorro = 1 - self.propension_consumo
        self.ahorros = self.dinero * \
            random.uniform(0.1, 0.3)  # 10-30% en ahorros
        self.deuda = random.uniform(
            0, self.ingreso_mensual * 2) if self.empleado else 0

        # Factor de paciencia para restricción intertemporal
        paciencia_min = self.config_hetero.get('factor_paciencia_min', ConfigEconomica.FACTOR_PACIENCIA_MIN)
        paciencia_max = self.config_hetero.get('factor_paciencia_max', ConfigEconomica.FACTOR_PACIENCIA_MAX)
        self.factor_paciencia = random.uniform(paciencia_min, paciencia_max)
        
        # Tipo de preferencias (Cobb-Douglas o CES)
        self.tipo_preferencias = self.config_hetero.get('tipo_preferencias', ConfigEconomica.TIPO_PREFERENCIAS)
        self.ces_elasticity = self.config_hetero.get('ces_elasticity_substitution', ConfigEconomica.CES_ELASTICITY_SUBSTITUTION)
        
        # Coeficientes de preferencias para Cobb-Douglas
        self.preferencias_cobb_douglas = {}

        # Ajustes por demografía
        self.ajustar_por_demografia()

        # Preferencias de consumo más realistas
        self.utilidad_marginal = {}
        self.cantidad_consumida = {}
        self.satisfaccion_bien = {}

        # Manejar bienes como diccionario o lista
        bienes_lista = mercado.bienes if isinstance(mercado.bienes, list) else list(mercado.bienes.keys())
        
        # Inicializar preferencias de Cobb-Douglas
        self._inicializar_preferencias_cobb_douglas(bienes_lista)
        
        for bien in bienes_lista:
            self.cantidad_consumida[bien] = 0
            self.satisfaccion_bien[bien] = random.uniform(0.3, 1.0)
            # Bienes básicos más importantes
            categorias_map = getattr(ConfigEconomica, 'CATEGORIAS_BIENES_MAP', None)
            if isinstance(categorias_map, dict):
                categoria = categorias_map.get(bien, 'servicios')
            else:
                categoria = 'servicios'
            if categoria == 'alimentos_basicos':
                self.satisfaccion_bien[bien] *= 1.5

        # Factores psicológicos
        self.aversion_riesgo = random.uniform(0.3, 0.9)
        self.factor_imitacion = random.uniform(0.1, 0.4)  # Influencia social
        self.fidelidad_marca = random.uniform(0.2, 0.8)

    def _generar_dinero_inicial(self):
        """Genera dinero inicial usando distribución lognormal o uniforme"""
        distribucion = self.config_hetero.get('distribucion_ingresos', ConfigEconomica.DISTRIBUCION_INGRESOS)
        
        if distribucion == 'lognormal':
            mu = self.config_hetero.get('ingreso_lognormal_mu', ConfigEconomica.INGRESO_LOGNORMAL_MU)
            sigma = self.config_hetero.get('ingreso_lognormal_sigma', ConfigEconomica.INGRESO_LOGNORMAL_SIGMA)
            min_garantizado = self.config_hetero.get('ingreso_min_garantizado', ConfigEconomica.INGRESO_MIN_GARANTIZADO)
            
            # Generar usando distribución lognormal
            dinero = np.random.lognormal(mu, sigma)
            # Aplicar mínimo garantizado y escalar a rango apropiado
            dinero = max(min_garantizado, dinero)
            return int(min(dinero, ConfigEconomica.DINERO_INICIAL_CONSUMIDOR_MAX))
        else:
            # Distribución uniforme tradicional
            return random.randint(
                ConfigEconomica.DINERO_INICIAL_CONSUMIDOR_MIN,
                ConfigEconomica.DINERO_INICIAL_CONSUMIDOR_MAX)
    
    def _generar_ingreso_inicial(self):
        """Genera ingreso inicial usando distribución lognormal o uniforme"""
        distribucion = self.config_hetero.get('distribucion_ingresos', ConfigEconomica.DISTRIBUCION_INGRESOS)
        
        if distribucion == 'lognormal':
            mu = self.config_hetero.get('ingreso_lognormal_mu', ConfigEconomica.INGRESO_LOGNORMAL_MU)
            sigma = self.config_hetero.get('ingreso_lognormal_sigma', ConfigEconomica.INGRESO_LOGNORMAL_SIGMA)
            min_garantizado = self.config_hetero.get('ingreso_min_garantizado', ConfigEconomica.INGRESO_MIN_GARANTIZADO)
            
            # Generar usando distribución lognormal, escalado para ingresos
            ingreso = np.random.lognormal(mu - 1.0, sigma * 0.8)  # Ajustar para ingresos mensuales
            ingreso = max(min_garantizado, ingreso)
            return int(min(ingreso, ConfigEconomica.SALARIO_BASE_MAX))
        else:
            # Distribución uniforme tradicional
            return random.randint(
                ConfigEconomica.SALARIO_BASE_MIN,
                ConfigEconomica.SALARIO_BASE_MAX)

    def _inicializar_preferencias_cobb_douglas(self, bienes_lista):
        """Inicializa coeficientes de preferencias Cobb-Douglas que suman 1"""
        if not bienes_lista:
            return
        
        # Generar coeficientes aleatorios
        coefs_raw = [random.uniform(0.1, 2.0) for _ in bienes_lista]
        suma_coefs = sum(coefs_raw)
        
        # Normalizar para que sumen 1
        for i, bien in enumerate(bienes_lista):
            self.preferencias_cobb_douglas[bien] = coefs_raw[i] / suma_coefs

    def _determinar_estado_demografico(self):
        if self.edad < 25:
            return 'joven'
        elif self.edad < 65:
            return 'adulto'
        else:
            return 'jubilado'

    def ajustar_por_demografia(self):
        if self.estado_demografico == 'joven':
            self.habilidades = self.habilidades_base * 0.8
            self.propension_consumo = min(
                0.95, self.propension_consumo_base * 1.1)
        elif self.estado_demografico == 'adulto':
            self.habilidades = self.habilidades_base
            self.propension_consumo = self.propension_consumo_base
        else:  # jubilado
            self.habilidades = self.habilidades_base * 0.6
            self.propension_consumo = self.propension_consumo_base * 0.8
            self.empleado = False
            self.ingreso_mensual = 0
        self.propension_ahorro = 1 - self.propension_consumo

    def calcular_utilidad_cobb_douglas(self, cantidades):
        """Calcula utilidad usando función Cobb-Douglas: U = ∏(x_i^α_i)"""
        if not cantidades:
            return 0.0
        
        utilidad = 1.0
        for bien, cantidad in cantidades.items():
            if bien in self.preferencias_cobb_douglas and cantidad > 0:
                alpha = self.preferencias_cobb_douglas[bien]
                utilidad *= (cantidad ** alpha)
        
        return utilidad
    
    def calcular_utilidad_ces(self, cantidades):
        """Calcula utilidad usando función CES: U = (∑(α_i * x_i^ρ))^(1/ρ)"""
        if not cantidades:
            return 0.0
        
        rho = (self.ces_elasticity - 1) / self.ces_elasticity
        suma_ces = 0.0
        
        for bien, cantidad in cantidades.items():
            if bien in self.preferencias_cobb_douglas and cantidad >= 0:
                alpha = self.preferencias_cobb_douglas[bien]
                suma_ces += alpha * (cantidad ** rho)
        
        if suma_ces <= 0:
            return 0.0
        
        return suma_ces ** (1 / rho)
    
    def calcular_utilidad_total(self, cantidades):
        """Calcula utilidad total según el tipo de preferencias configurado"""
        if self.tipo_preferencias == 'ces':
            return self.calcular_utilidad_ces(cantidades)
        else:  # Default: cobb_douglas
            return self.calcular_utilidad_cobb_douglas(cantidades)
    
    def calcular_demanda_optima(self, presupuesto, precios):
        """Calcula demanda óptima dada restricción presupuestaria"""
        if not precios or presupuesto <= 0:
            return {}
        
        if self.tipo_preferencias == 'cobb_douglas':
            return self._demanda_cobb_douglas(presupuesto, precios)
        else:  # CES
            return self._demanda_ces(presupuesto, precios)
    
    def _demanda_cobb_douglas(self, presupuesto, precios):
        """Calcula demanda óptima para preferencias Cobb-Douglas"""
        demanda = {}
        
        for bien, precio in precios.items():
            if bien in self.preferencias_cobb_douglas and precio > 0:
                alpha = self.preferencias_cobb_douglas[bien]
                # Demanda marshalliana: x_i = (α_i * M) / p_i
                demanda[bien] = max(0, (alpha * presupuesto) / precio)
            else:
                demanda[bien] = 0
        
        return demanda
    
    def _demanda_ces(self, presupuesto, precios):
        """Calcula demanda óptima para preferencias CES (aproximación)"""
        demanda = {}
        elasticidad = self.ces_elasticity
        
        # Para CES, usamos aproximación basada en elasticidad de sustitución
        total_ponderado = sum(
            self.preferencias_cobb_douglas.get(bien, 0) * (precio ** (1 - elasticidad))
            for bien, precio in precios.items()
        )
        
        if total_ponderado <= 0:
            return {bien: 0 for bien in precios}
        
        for bien, precio in precios.items():
            if bien in self.preferencias_cobb_douglas and precio > 0:
                alpha = self.preferencias_cobb_douglas[bien]
                peso_relativo = alpha * (precio ** (1 - elasticidad)) / total_ponderado
                demanda[bien] = max(0, (peso_relativo * presupuesto) / precio)
            else:
                demanda[bien] = 0
        
        return demanda
    
    def aplicar_restriccion_intertemporal(self, consumo_actual, tasa_interes):
        """Ajusta el consumo considerando restricción intertemporal"""
        # Factor de descuento basado en paciencia y tasa de interés
        factor_descuento = self.factor_paciencia / (1 + tasa_interes)
        
        # Ajustar propensión al consumo basado en la paciencia
        propension_ajustada = self.propension_consumo * factor_descuento
        
        # Los más pacientes tienden a ahorrar más cuando las tasas son altas
        if tasa_interes > 0.05:  # Tasa alta
            propension_ajustada *= (1 - (tasa_interes - 0.05) * self.factor_paciencia)
        
        return max(0.1, min(0.95, propension_ajustada))

    def envejecer(self, anos=1/12):
        self.edad += anos
        nuevo_estado = self._determinar_estado_demografico()
        if nuevo_estado != self.estado_demografico:
            self.estado_demografico = nuevo_estado
            self.ajustar_por_demografia()

    def buscar_empleo(self):
        """Busca empleo mejorado con mayor probabilidad de éxito"""
        if not self.empleado:
            # Incluir empresas con capacidad expandida
            empresas_disponibles = [e for e in self.mercado.getEmpresas()
                                    if hasattr(e, 'empleados')]

            if empresas_disponibles:
                # Seleccionar empresa con mayor compatibilidad de habilidades
                def _compat(e):
                    sector = getattr(e, 'sector', None)
                    nombre_sector = sector.nombre if sector else None
                    return self.habilidades_sectoriales.get(nombre_sector, 0.0)

                # Intentar con múltiples empresas, no solo la mejor
                empresas_candidatas = sorted(
                    empresas_disponibles, key=_compat, reverse=True)[:5]

                for empresa in empresas_candidatas:
                    sector_nombre = getattr(empresa.sector, 'nombre', None) if hasattr(
                        empresa, 'sector') else None
                    nivel = self.habilidades_sectoriales.get(
                        sector_nombre, 0.0)

                    # Aumentar probabilidad base de contratación
                    probabilidad_base = 0.5  # Aumentado de 0.3
                    probabilidad_contratacion = probabilidad_base + 0.4 * nivel

                    # Bonificación por crisis (programas de empleo)
                    if hasattr(self.mercado, 'crisis_financiera_activa') and self.mercado.crisis_financiera_activa:
                        probabilidad_contratacion += 0.2

                    if self.sindicato and sector_nombre in self.sindicato.sectores:
                        probabilidad_contratacion += self.sindicato.poder_negociacion

                    if random.random() < min(0.8, probabilidad_contratacion):  # Máximo 80%
                        resultado = empresa.contratar(self)
                        if resultado:
                            self.empleado = True
                            self.empleador = empresa
                            if isinstance(resultado, (int, float)):
                                self.ingreso_mensual = resultado
                            else:
                                self.ingreso_mensual = int(
                                    ConfigEconomica.SALARIO_BASE_MIN * (0.5 + nivel))
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
        utilidad = satisfaccion_base * \
            (ConfigEconomica.UTILIDAD_MARGINAL_DECRECIENTE ** cantidad_actual)

        # Aumentar utilidad para bienes básicos si no se han consumido
        categorias_map = getattr(ConfigEconomica, 'CATEGORIAS_BIENES_MAP', None)
        categoria = categorias_map.get(bien, 'servicios') if isinstance(categorias_map, dict) else 'servicios'
        if categoria == 'alimentos_basicos' and cantidad_actual == 0:
            utilidad *= 2.0

        return utilidad

    def calcular_precio_reserva(self, bien, precio_mercado):
        """Calcula el precio máximo que estaría dispuesto a pagar"""
        utilidad = self.calcular_utilidad_marginal(bien)
        ingreso_disponible = max(
            0, self.dinero - self.deuda - self.ahorros * 0.8)

        # Precio de reserva basado en utilidad e ingreso
        precio_reserva = utilidad * ingreso_disponible * 0.01  # Factor de escala

        # Ajuste por categoría del bien
        categorias_map = getattr(ConfigEconomica, 'CATEGORIAS_BIENES_MAP', None)
        categoria = categorias_map.get(bien, 'servicios') if isinstance(categorias_map, dict) else 'servicios'
        if categoria == 'alimentos_basicos':
            precio_reserva *= 1.2  # Dispuesto a pagar más por básicos
        elif categoria == 'bienes_duraderos':
            precio_reserva *= 0.8  # Más selectivo con lujos

        # Mínimo 50% del precio de mercado
        return max(precio_reserva, precio_mercado * 0.5)

    def decidir_compra_con_psicologia(self, mercado, ciclo):
        """Decisión de compra considerando factores psicológicos"""
        # Si no tiene perfil psicológico, usar método racional
        if not hasattr(self, 'perfil_psicologico'):
            return self.decidir_compra_racional(mercado, ciclo)

        # Usar sistema de psicología económica para decisiones
        sistema_psicologia = mercado.sistema_psicologia
        perfil = self.perfil_psicologico

        presupuesto_consumo = self.dinero * self.propension_consumo

        # Ajustar presupuesto por estado emocional
        if perfil.estres_financiero > 0.6:
            presupuesto_consumo *= 0.8  # Reducir consumo por estrés
        elif perfil.optimismo > 0.8:
            presupuesto_consumo *= 1.1  # Aumentar consumo por optimismo

        # Crear lista de opciones de compra
        opciones_compra = []

        for bien in mercado.bienes.keys():
            empresas_disponibles = [e for e in mercado.getEmpresas()
                                    if bien in e.bienes and len(e.bienes[bien]) > 0]

            if empresas_disponibles:
                # Encontrar empresa considerando fidelidad de marca
                if hasattr(perfil, 'marcas_confiables') and bien in perfil.marcas_confiables:
                    # Buscar empresa de marca confiable
                    empresas_confiables = [e for e in empresas_disponibles
                                           if e.nombre in perfil.marcas_confiables]
                    if empresas_confiables:
                        empresa_elegida = empresas_confiables[0]
                    else:
                        empresa_elegida = min(
                            empresas_disponibles, key=lambda e: e.precios.get(bien, float('inf')))
                else:
                    # Buscar mejor precio
                    empresa_elegida = min(
                        empresas_disponibles, key=lambda e: e.precios.get(bien, float('inf')))

                precio_original = empresa_elegida.precios.get(bien, 0)

                if precio_original > 0:
                    # Aplicar sesgos psicológicos al precio percibido
                    precio_percibido = sistema_psicologia.aplicar_sesgo_anclaje(
                        self, bien, precio_original)
                    precio_percibido = sistema_psicologia.influencia_social_precios(
                        self, precio_percibido, bien)

                    # Calcular utilidad percibida (no racional)
                    utilidad_percibida = sistema_psicologia.calcular_utilidad_percibida(
                        self, bien, 1, precio_percibido
                    )

                    # Efecto manada
                    factor_manada = sistema_psicologia.aplicar_efecto_manada(
                        self, "compra", bien)
                    utilidad_percibida *= factor_manada

                    # Efecto de tendencias sociales
                    if bien in sistema_psicologia.tendencias_sociales:
                        utilidad_percibida *= (
                            1 + sistema_psicologia.tendencias_sociales[bien] * 0.5)

                    if precio_original <= presupuesto_consumo and utilidad_percibida > 0:
                        opciones_compra.append({
                            'bien': bien,
                            'empresa': empresa_elegida,
                            'precio': precio_original,
                            'precio_percibido': precio_percibido,
                            'utilidad_percibida': utilidad_percibida,
                            'ratio': utilidad_percibida / precio_percibido if precio_percibido > 0 else 0
                        })

        # Ordenar por utilidad percibida (no necesariamente racional)
        opciones_compra.sort(
            key=lambda x: x['utilidad_percibida'], reverse=True)

        # Comprar considerando impulsividad vs racionalidad
        gastado = 0
        compras_realizadas = 0
        # Menos racional = más compras
        max_compras = int(5 * (1 - perfil.racionalidad) +
                          3 * perfil.racionalidad)

        for opcion in opciones_compra[:max_compras]:
            if gastado + opcion['precio'] <= presupuesto_consumo:
                # Probabilidad de compra basada en racionalidad y estado emocional
                prob_compra = 0.8 * (1 - perfil.racionalidad) + \
                    0.5 * perfil.racionalidad

                if perfil.optimismo > 0.7:
                    prob_compra += 0.2
                if perfil.estres_financiero > 0.5:
                    prob_compra -= 0.3

                prob_compra = max(0.1, min(0.9, prob_compra))

                if random.random() < prob_compra:
                    if self.comprar_bien_mejorado(opcion['empresa'], opcion['bien'], 1, mercado, ciclo):
                        gastado += opcion['precio']
                        compras_realizadas += 1

                        # Actualizar estado emocional
                        sistema_psicologia.actualizar_estado_emocional(
                            self, "compra_exitosa")

                        # Marcar empresa como confiable si la compra fue satisfactoria
                        if random.random() < 0.3:  # 30% probabilidad
                            perfil.marcas_confiables.add(
                                opcion['empresa'].nombre)

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
                mejor_empresa = min(
                    empresas_disponibles, key=lambda e: e.precios.get(bien, float('inf')))
                precio_base = mejor_empresa.precios.get(bien, 0)
                
                # Calcular precio final con IVA si existe sistema fiscal
                if hasattr(mercado, 'sistema_fiscal') and bien in mercado.bienes:
                    categoria_bien = mercado.bienes[bien].categoria
                    precio_final = precio_base * (1 + mercado.sistema_fiscal.iva_rates.get(categoria_bien, 0.21))
                else:
                    precio_final = precio_base

                if precio_final > 0 and precio_final <= presupuesto_consumo:
                    utilidad = self.calcular_utilidad_marginal(bien)
                    precio_reserva = self.calcular_precio_reserva(bien, precio_final)

                    if precio_final <= precio_reserva:
                        ratio_utilidad_precio = utilidad / precio_final
                        opciones_compra.append({
                            'bien': bien,
                            'empresa': mejor_empresa,
                            'precio': precio_final,
                            'utilidad': utilidad,
                            'ratio': ratio_utilidad_precio
                        })

        # Ordenar por ratio utilidad/precio
        opciones_compra.sort(key=lambda x: x['ratio'], reverse=True)

        # Comprar en orden de preferencia hasta agotar presupuesto
        gastado = 0
        for opcion in opciones_compra[:5]:  # Máximo 5 compras por ciclo
            if gastado + opcion['precio'] <= presupuesto_consumo:
                if getattr(mercado, 'order_book_habilitado', False):
                    # Enviar orden de compra (bid) al order book
                    try:
                        mercado.enviar_orden('bid', opcion['bien'], opcion['precio'], 1, self.nombre)
                        gastado += opcion['precio']
                    except Exception:
                        pass
                else:
                    if self.comprar_bien_mejorado(opcion['empresa'], opcion['bien'], 1, mercado, ciclo):
                        gastado += opcion['precio']

    def comprar_bien_mejorado(self, empresa, bien, cantidad, mercado, ciclo):
        """Versión mejorada del método de compra con IVA incluido"""
        precio_base = empresa.precios.get(bien, 0)
        
        # Aplicar IVA si existe sistema fiscal
        if hasattr(mercado, 'sistema_fiscal') and bien in mercado.bienes:
            categoria_bien = mercado.bienes[bien].categoria
            precio_final = mercado.sistema_fiscal.aplicar_iva(precio_base, categoria_bien)
        else:
            precio_final = precio_base
            
        costo_total = precio_final * cantidad

        if self.dinero >= costo_total and len(empresa.bienes.get(bien, [])) >= cantidad:
            # Realizar transacción
            self.dinero -= costo_total
            empresa.dinero += precio_base * cantidad  # Empresa recibe precio sin IVA
            
            # El IVA ya fue registrado en el sistema fiscal

            # Actualizar inventarios
            if bien not in self.bienes:
                self.bienes[bien] = 0
            self.bienes[bien] += cantidad

            # Actualizar satisfacción y consumo
            self.cantidad_consumida[bien] = self.cantidad_consumida.get(
                bien, 0) + cantidad

            # Remover del inventario de empresa
            for _ in range(cantidad):
                if empresa.bienes[bien]:
                    empresa.bienes[bien].pop(0)

            # Registrar transacción
            mercado.registrar_transaccion(
                self, bien, cantidad, costo_total, ciclo)

            # Actualizar historial para decisiones futuras
            self.historial_compras[bien] = precio_final

            return True
        return False

    def gestionar_finanzas_personales(self):
        """Gestiona finanzas personales incluyendo interacción bancaria"""
        # Gestión de ahorros mejorada con sistema bancario
        if self.dinero > self.ingreso_mensual * 2 and hasattr(self.mercado, 'sistema_bancario'):
            # Depositar exceso de dinero en banco
            banco_elegido = self.mercado.sistema_bancario.bancos[
                0] if self.mercado.sistema_bancario.bancos else None
            if banco_elegido:
                monto_deposito = self.dinero * 0.3  # Depositar 30% del exceso
                if banco_elegido.recibir_deposito(self, monto_deposito):
                    self.dinero -= monto_deposito
                    self.ahorros += monto_deposito

        # Solicitar préstamo con criterios más flexibles
        deberia_solicitar_prestamo = (
            self.dinero < self.ingreso_mensual * 1.0 and  # Umbral más alto
            self.empleado and
            hasattr(self.mercado, 'sistema_bancario') and
            self.deuda < self.ingreso_mensual * 6  # Límite de endeudamiento
        )

        if deberia_solicitar_prestamo:
            banco_elegido = self.mercado.sistema_bancario.bancos[
                0] if self.mercado.sistema_bancario.bancos else None
            if banco_elegido:
                # Monto más conservador pero más frecuente
                monto_prestamo = max(1000, self.ingreso_mensual * 1.5)

                # Intentar con el plazo adecuado
                resultado_prestamo = banco_elegido.solicitar_prestamo(
                    self, monto_prestamo, 12)

                # Manejo correcto del resultado
                if isinstance(resultado_prestamo, tuple) and resultado_prestamo[0]:
                    # Préstamo aprobado - el dinero ya se agregó automáticamente
                    self.deuda += monto_prestamo * 1.08  # 8% de intereses
                    # print(
                    #     f"💳 {self.nombre} obtuvo préstamo de ${monto_prestamo:,.0f}")
                elif resultado_prestamo is True:  # Por compatibilidad
                    self.deuda += monto_prestamo * 1.08

        # Gestión de deudas
        if self.deuda > 0:
            # Pagar 20% dinero o 10% deuda
            pago_deuda = min(self.dinero * 0.2, self.deuda * 0.1)
            if pago_deuda > 0:
                self.dinero -= pago_deuda
                self.deuda -= pago_deuda
                self.deuda = max(0, self.deuda)

        # Ahorros automáticos para empleados
        if self.empleado and self.dinero > self.ingreso_mensual:
            ahorro_mensual = self.dinero * 0.1
            self.ahorros += ahorro_mensual
            self.dinero -= ahorro_mensual

    def recibir_salario(self):
        """Recibe salario mensual si está empleado"""
        if self.empleado and self.ingreso_mensual > 0:
            # Salario con pequeña variación
            salario_efectivo = self.ingreso_mensual * \
                random.uniform(0.95, 1.05)
            # Aporte sindical si corresponde
            if self.sindicato:
                salario_efectivo -= self.sindicato.calcular_aporte(
                    salario_efectivo)

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
        self.decidir_acciones(mercado.mercado_financiero,
                              mercado.registrar_transaccion, ciclo)

        # Decisión de compra
        if hasattr(self, 'perfil_psicologico') and mercado.sistema_psicologia:
            self.decidir_compra_con_psicologia(mercado, ciclo)
        else:
            self.decidir_compra_racional(mercado, ciclo)

        # Degradar satisfacción con el tiempo (los bienes se consumen)
        for bien in self.cantidad_consumida:
            self.cantidad_consumida[bien] = max(
                0, self.cantidad_consumida[bien] * ConfigEconomica.FACTOR_SACIEDAD)

    def comprar_acciones(self, mercado_financiero, nombre_empresa, cantidad):
        if nombre_empresa in mercado_financiero.acciones:
            total_acciones, precio_actual = mercado_financiero.acciones[nombre_empresa]
            costo_total = precio_actual * cantidad
            if self.dinero >= costo_total and cantidad <= total_acciones:
                self.dinero -= costo_total
                self.cartera_acciones[nombre_empresa] = self.cartera_acciones.get(
                    nombre_empresa, 0) + cantidad
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
                    # Máximo 5% del dinero
                    cantidad_a_comprar = min(
                        5, int(self.dinero * 0.05 / precio_accion))
                    if self.comprar_acciones(mercado_financiero, nombre_empresa, cantidad_a_comprar):
                        nombre_empresa_str = nombre_empresa.nombre if isinstance(
                            nombre_empresa, Empresa) else str(nombre_empresa)
                        registrar(self, 'Accion ' + nombre_empresa_str,
                                  cantidad_a_comprar, precio_accion * cantidad_a_comprar, ciclo)

    def deberia_comprar_acciones(self, acciones):
        # 10% de probabilidad si tiene liquidez
        return self.dinero > self.ingreso_mensual * 3 and random.random() < 0.1

    def comprar(self, producto, cantidad):
        """Método simplificado de compra para compatibilidad con tests"""
        # Buscar empresas que vendan este producto
        empresas_disponibles = []
        for empresa in self.mercado.getEmpresas():
            if producto in empresa.precios and empresa.precios[producto] > 0:
                # Verificar si la empresa tiene stock (si usa inventario)
                if hasattr(empresa, 'bienes') and producto in empresa.bienes:
                    stock = len(empresa.bienes[producto]) if isinstance(empresa.bienes[producto], list) else empresa.bienes[producto]
                    if stock > 0:
                        empresas_disponibles.append(empresa)
                else:
                    # Si no maneja inventario, asumir que puede vender
                    empresas_disponibles.append(empresa)
        
        if not empresas_disponibles:
            return False
        
        # Elegir la empresa con el precio más bajo
        empresa_elegida = min(empresas_disponibles, key=lambda e: e.precios[producto])
        
        # Intentar comprar usando el método mejorado
        return self.comprar_bien_mejorado(empresa_elegida, producto, cantidad, self.mercado, 0)

    def __str__(self):
        empleado_str = "Empleado" if self.empleado else "Desempleado"
        return f"{self.nombre} - Dinero: ${self.dinero:.2f} - {empleado_str} - Ingreso: ${self.ingreso_mensual:.2f}"
