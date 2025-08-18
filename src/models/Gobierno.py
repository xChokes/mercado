"""
Sistema de Gobierno que implementa políticas económicas, regulación y servicios públicos
"""
import random
from ..config.ConfigEconomica import ConfigEconomica
from ..systems.SostenibilidadAmbiental import SostenibilidadAmbiental


class Gobierno:
    def __init__(self, mercado):
        self.nombre = "Gobierno Nacional"  # Agregar nombre para transacciones
        self.mercado = mercado
        self.presupuesto = 0
        self.deuda_publica = 0
        self.tasa_impuestos = ConfigEconomica.TASA_IMPUESTOS
        self.tasa_interes_referencia = ConfigEconomica.TASA_INTERES_BASE
        self.gasto_publico_objetivo = 0
        self.politicas_activas = []
        self.reservas_monetarias = 1000000  # Capacidad de intervención
        # Sistema ambiental
        self.sostenibilidad = SostenibilidadAmbiental()
        self.tasa_impuesto_carbono = ConfigEconomica.IMPUESTO_CARBONO
        # Indicadores macroeconómicos
        self.inflacion_mensual = 0
        self.tasa_desempleo = 0
        self.pib_real = 0
        self.pib_nominal = 0
        self.deficit_fiscal = 0
        self.poblacion = len(mercado.getConsumidores()) if mercado else 0
        self.desempleo_sectorial = {}

    def calcular_indicadores_macroeconomicos(self):
        """Calcula indicadores económicos principales"""
        # PIB como suma de toda la actividad económica
        transacciones_ciclo = [t for t in self.mercado.transacciones if t['ciclo'] == len(
            self.mercado.transacciones)]
        self.pib_nominal = sum([t['costo_total'] for t in transacciones_ciclo])

        # Población y tasa de desempleo
        self.poblacion = len(self.mercado.getConsumidores())
        desempleados = len(
            [c for c in self.mercado.getConsumidores() if not c.empleado])
        self.tasa_desempleo = desempleados / self.poblacion if self.poblacion > 0 else 0

        # Desempleo por sector
        self.desempleo_sectorial = {}
        if hasattr(self.mercado, 'economia_sectorial'):
            sectores = self.mercado.economia_sectorial.sectores
            consumidores = self.mercado.getConsumidores()
            for nombre in sectores.keys():
                potenciales = [
                    c for c in consumidores if c.habilidades_sectoriales.get(nombre, 0) > 0]
                empleados_sector = [c for c in potenciales if c.empleado and getattr(
                    c.empleador, 'sector', None) and c.empleador.sector.nombre == nombre]
                total = len(potenciales)
                if total > 0:
                    self.desempleo_sectorial[nombre] = 1 - \
                        len(empleados_sector) / total
                else:
                    self.desempleo_sectorial[nombre] = 0

        # Inflación basada en cambios de precios
        precios_actuales = []
        for empresa in self.mercado.getEmpresas():
            precios_actuales.extend(empresa.precios.values())

        if hasattr(self, 'precios_ciclo_anterior') and precios_actuales:

            inflacion = (sum(precios_actuales) / len(precios_actuales) if len(precios_actuales) > 0 else 0) / \
                (sum(self.precios_ciclo_anterior) /
                 len(self.precios_ciclo_anterior) if len(self.precios_ciclo_anterior) > 0 else 1) - 1
            # Limitar entre -5% y 10%
            self.inflacion_mensual = max(-0.05, min(0.10, inflacion))

        self.precios_ciclo_anterior = precios_actuales[:]

    def recaudar_impuestos(self):
        """Recauda impuestos de empresas y personas con ingresos altos"""
        recaudacion = 0

        # Impuesto a empresas
        for empresa in self.mercado.getEmpresas():
            ganancia_ciclo = max(0, empresa.dinero - empresa.dinero_ciclo_anterior) if hasattr(
                empresa, 'dinero_ciclo_anterior') else 0
            impuesto = ganancia_ciclo * self.tasa_impuestos
            empresa.dinero -= impuesto
            recaudacion += impuesto
            empresa.dinero_ciclo_anterior = empresa.dinero

        # Impuesto a consumidores con ingresos altos
        for consumidor in self.mercado.getConsumidores():
            if consumidor.ingreso_mensual > ConfigEconomica.SALARIO_BASE_MAX:
                impuesto = (consumidor.ingreso_mensual -
                            ConfigEconomica.SALARIO_BASE_MAX) * 0.15
                consumidor.dinero -= impuesto
                recaudacion += impuesto

        self.presupuesto += recaudacion
        return recaudacion

    def ejecutar_gasto_publico(self):
        """Ejecuta gasto público para estimular la economía"""
        self.gasto_publico_objetivo = self.pib_nominal * ConfigEconomica.GASTO_PUBLICO_PIB
        gasto_efectivo = min(self.presupuesto, self.gasto_publico_objetivo)

        if gasto_efectivo > 0 and self.poblacion > 0:
            # Distribuir gasto público
            # 60% a subsidios de desempleo diferenciados por sector
            subsidios = gasto_efectivo * 0.6
            desempleados = [
                c for c in self.mercado.getConsumidores() if not c.empleado]
            if desempleados:
                agrupados = {}
                for d in desempleados:
                    if d.habilidades_sectoriales:
                        sector_principal = max(
                            d.habilidades_sectoriales, key=d.habilidades_sectoriales.get)
                    else:
                        sector_principal = 'general'
                    agrupados.setdefault(sector_principal, []).append(d)

                total_ratio = sum(self.desempleo_sectorial.get(s, 0)
                                  for s in agrupados)
                for sector, lista in agrupados.items():
                    if total_ratio > 0:
                        fondo_sector = subsidios * \
                            (self.desempleo_sectorial.get(sector, 0) / total_ratio)
                    else:
                        if len(agrupados) > 0:
                            fondo_sector = subsidios / len(agrupados)
                        else:
                            fondo_sector = 0
                    if len(lista) > 0:
                        subsidio_individual = fondo_sector / len(lista)
                    else:
                        subsidio_individual = 0
                    for desempleado in lista:
                        desempleado.dinero += subsidio_individual

            # 40% a compras gubernamentales (estimula demanda)
            compras_gobierno = gasto_efectivo * 0.4
            empresas = self.mercado.getEmpresas()
            if empresas and len(empresas) > 0:
                compra_por_empresa = compras_gobierno / len(empresas)
                for empresa in empresas:
                    empresa.dinero += compra_por_empresa

            self.presupuesto -= gasto_efectivo

        self.deficit_fiscal = self.gasto_publico_objetivo - self.presupuesto
        if self.deficit_fiscal > 0:
            self.deuda_publica += self.deficit_fiscal

    def politica_monetaria(self):
        """Implementa política monetaria basada en condiciones económicas"""
        # Política anti-inflacionaria
        if self.inflacion_mensual > ConfigEconomica.INFLACION_MENSUAL_OBJETIVO * 1.5:
            # Aumentar tasa de interés para reducir inflación
            self.tasa_interes_referencia = min(
                0.15, self.tasa_interes_referencia * 1.1)
            self.politicas_activas.append("Política monetaria restrictiva")

        # Política expansiva contra recesión
        elif self.tasa_desempleo > ConfigEconomica.TASA_DESEMPLEO_OBJETIVO * 2:
            # Reducir tasa de interés para estimular la economía
            self.tasa_interes_referencia = max(
                0.01, self.tasa_interes_referencia * 0.9)
            self.politicas_activas.append("Política monetaria expansiva")

        # Inyección de liquidez en crisis
        if self.tasa_desempleo > 0.15 and self.reservas_monetarias > 100000:
            inyeccion = min(100000, self.reservas_monetarias * 0.1)
            # Distribuir entre bancos/empresas
            empresas = self.mercado.getEmpresas()
            if empresas and len(empresas) > 0:
                inyeccion_empresa = inyeccion / len(empresas)
                for empresa in empresas:
                    empresa.dinero += inyeccion_empresa
                self.reservas_monetarias -= inyeccion
                self.politicas_activas.append("Inyección de liquidez")

    def regular_precios(self):
        """Implementa regulación de precios para bienes esenciales"""
        for empresa in self.mercado.getEmpresas():
            for bien, precio in empresa.precios.items():
                if bien in ConfigEconomica.CATEGORIAS_BIENES:
                    categoria = ConfigEconomica.CATEGORIAS_BIENES[bien]

                    # Controlar precios de alimentos básicos en crisis
                    if categoria == 'alimentos_basicos' and self.inflacion_mensual > 0.05:
                        precio_maximo = empresa.costos_unitarios.get(
                            bien, precio * 0.8) * 1.3  # 30% margen máximo
                        if precio > precio_maximo:
                            empresa.precios[bien] = precio_maximo
                            self.politicas_activas.append(
                                f"Regulación precio {bien}")

    def rescatar_banco(self, banco, monto):
        """Inyecta capital a un banco en dificultades"""
        if self.reservas_monetarias >= monto:
            banco.capital += monto
            banco.reservas += monto * 0.5
            self.reservas_monetarias -= monto
            self.politicas_activas.append(f"Rescate a {banco.nombre}")
            return True
        return False

    def regulacion_prudencial(self):
        """Aplica regulación prudencial al sistema bancario"""
        sistema = self.mercado.sistema_bancario
        for banco in sistema.bancos:
            ratio = banco.calcular_ratio_solvencia()
            if ratio < banco.ratio_capital:
                deficit = banco.ratio_capital * \
                    sum(banco.depositos.values()) - \
                    (banco.capital + banco.reservas)
                if deficit > 0:
                    self.rescatar_banco(banco, min(
                        deficit, self.reservas_monetarias))

    def aplicar_politicas_ambientales(self):
        """Aplica impuestos al carbono y límites de extracción"""
        impuestos_carbono = 0

        for empresa in self.mercado.getEmpresas():
            emisiones = self.sostenibilidad.emisiones_empresas.get(
                empresa.nombre, 0)
            if emisiones > 0:
                impuesto = emisiones * self.tasa_impuesto_carbono
                empresa.dinero -= impuesto
                impuestos_carbono += impuesto

        self.presupuesto += impuestos_carbono

        # Limitar extracción si recursos bajos
        limite = ConfigEconomica.RECURSOS_NATURALES_INICIALES * \
            ConfigEconomica.LIMITE_EXTRACCION_RECURSOS
        if self.sostenibilidad.recursos_disponibles < limite:
            for empresa in self.mercado.getEmpresas():
                if hasattr(empresa, 'capacidad_produccion'):
                    for bien in empresa.capacidad_produccion:
                        empresa.capacidad_produccion[bien] = int(
                            empresa.capacidad_produccion[bien] * 0.9)
            self.politicas_activas.append("Límite de extracción de recursos")

        return impuestos_carbono

    def calcular_indicadores_ecologicos(self):
        """Calcula indicadores ambientales agregados"""
        return self.sostenibilidad.obtener_indicadores()

    def ciclo_gobierno(self, ciclo):
        """Ejecuta un ciclo completo de políticas gubernamentales"""
        self.politicas_activas = []

        # Calcular indicadores
        self.calcular_indicadores_macroeconomicos()

        # Recaudar impuestos
        recaudacion = self.recaudar_impuestos()

        # Ejecutar gasto público
        self.ejecutar_gasto_publico()

        # Implementar políticas
        self.politica_monetaria()
        self.regular_precios()
        self.regulacion_prudencial()
        impuestos_carbono = self.aplicar_politicas_ambientales()
        indicadores_ecologicos = self.calcular_indicadores_ecologicos()

        return {
            'pib_nominal': self.pib_nominal,
            'inflacion': self.inflacion_mensual,
            'desempleo': self.tasa_desempleo,
            'desempleo_sectorial': self.desempleo_sectorial,
            'recaudacion': recaudacion,
            'deficit': self.deficit_fiscal,
            'tasa_interes': self.tasa_interes_referencia,
            'politicas': self.politicas_activas[:],
            'impuestos_carbono': impuestos_carbono,
            'indicadores_ecologicos': indicadores_ecologicos
        }
