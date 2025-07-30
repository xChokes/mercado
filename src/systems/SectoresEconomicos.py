"""
Sistema de Sectores Económicos para mayor realismo en la simulación
Implementa sectores primario, secundario y terciario con cadenas productivas
"""
import random
from enum import Enum
from ..config.ConfigEconomica import ConfigEconomica


class TipoSector(Enum):
    PRIMARIO = "primario"      # Agricultura, minería, pesca
    SECUNDARIO = "secundario"  # Manufactura, construcción
    TERCIARIO = "terciario"    # Servicios, comercio


class Sector:
    def __init__(self, nombre, tipo_sector, productividad_base=1.0):
        self.nombre = nombre
        self.tipo = tipo_sector
        self.productividad_base = productividad_base
        self.empresas = []
        self.empleo_total = 0
        self.pib_sectorial = 0

        # Características sectoriales
        self.intensidad_capital = self._calcular_intensidad_capital()
        self.volatilidad = self._calcular_volatilidad()
        self.elasticidad_empleo = self._calcular_elasticidad_empleo()

        # Insumos requeridos (inputs de otros sectores)
        self.inputs_requeridos = self._definir_inputs()

        # Factores de competitividad
        self.nivel_tecnologico = random.uniform(0.5, 1.0)
        self.especializacion = random.uniform(0.3, 0.9)

    def _calcular_intensidad_capital(self):
        """Calcula qué tan intensivo en capital es el sector"""
        intensidades = {
            TipoSector.PRIMARIO: random.uniform(0.3, 0.6),    # Moderada
            TipoSector.SECUNDARIO: random.uniform(0.7, 0.9),  # Alta
            TipoSector.TERCIARIO: random.uniform(0.2, 0.5)    # Baja
        }
        return intensidades[self.tipo]

    def _calcular_volatilidad(self):
        """Volatilidad típica del sector"""
        volatilidades = {
            # Alta (clima, precios commodities)
            TipoSector.PRIMARIO: random.uniform(0.15, 0.30),
            TipoSector.SECUNDARIO: random.uniform(0.10, 0.20),  # Media
            TipoSector.TERCIARIO: random.uniform(
                0.05, 0.15)    # Baja (más estable)
        }
        return volatilidades[self.tipo]

    def _calcular_elasticidad_empleo(self):
        """Qué tan sensible es el empleo a cambios en producción"""
        elasticidades = {
            TipoSector.PRIMARIO: random.uniform(0.4, 0.7),    # Media
            TipoSector.SECUNDARIO: random.uniform(0.6, 1.2),  # Alta
            TipoSector.TERCIARIO: random.uniform(0.8, 1.4)    # Muy alta
        }
        return elasticidades[self.tipo]

    def _definir_inputs(self):
        """Define qué inputs necesita cada sector"""
        if self.tipo == TipoSector.PRIMARIO:
            return {
                'energia': 0.15,
                'combustibles': 0.10,
                'maquinaria': 0.05
            }
        elif self.tipo == TipoSector.SECUNDARIO:
            return {
                'materias_primas': 0.40,
                'energia': 0.20,
                'servicios_empresariales': 0.10
            }
        else:  # TERCIARIO
            return {
                'bienes_intermedios': 0.20,
                'energia': 0.10,
                'servicios_especializados': 0.15
            }

    def agregar_empresa(self, empresa):
        """Agrega una empresa al sector"""
        self.empresas.append(empresa)
        empresa.sector = self

    def calcular_pib_sectorial(self):
        """Calcula el PIB del sector"""
        pib = 0
        empleo = 0

        for empresa in self.empresas:
            # PIB como valor agregado basado en dinero de la empresa
            # Usamos una estimación del valor agregado basada en el capital
            if hasattr(empresa, 'dinero'):
                # Estimación: el valor agregado es proporcional al capital de la empresa
                valor_base = empresa.dinero * 0.1  # 10% del capital como valor agregado mensual
                
                # Si tiene ventas por bien, sumarlas
                if hasattr(empresa, 'ventasPorBienPorCiclo'):
                    ventas_totales = 0
                    for bien_ventas in empresa.ventasPorBienPorCiclo.values():
                        if isinstance(bien_ventas, dict):
                            ventas_totales += sum(bien_ventas.values())
                    
                    # Si hay ventas, usar eso como base
                    if ventas_totales > 0:
                        valor_base = ventas_totales * 0.3  # 30% como valor agregado
                
                pib += valor_base

            # Empleo
            if hasattr(empresa, 'empleados'):
                empleo += len(empresa.empleados)

        self.pib_sectorial = pib
        self.empleo_total = empleo
        return pib

    def aplicar_shock_sectorial(self, tipo_shock, intensidad):
        """Aplica un shock específico al sector"""
        for empresa in self.empresas:
            if tipo_shock == 'productividad':
                if hasattr(empresa, 'eficiencia_produccion'):
                    empresa.eficiencia_produccion *= intensidad
            elif tipo_shock == 'demanda':
                # Afectar demanda de los bienes del sector
                pass  # Implementar lógica específica
            elif tipo_shock == 'costos':
                if hasattr(empresa, 'costos_unitarios'):
                    for bien in empresa.costos_unitarios:
                        empresa.costos_unitarios[bien] *= intensidad


class EconomiaMultisectorial:
    """Coordinador de la economía multi-sectorial"""

    def __init__(self, mercado):
        self.mercado = mercado
        self.sectores = {}
        self.matriz_insumo_producto = {}
        self.ciclo_sectorial = 0

        # Crear sectores principales
        self._crear_sectores()
        self._construir_matriz_insumo_producto()

    def _crear_sectores(self):
        """Crea los sectores económicos principales"""
        # Sector primario
        self.sectores['agricultura'] = Sector(
            'Agricultura', TipoSector.PRIMARIO, 0.8)
        self.sectores['mineria'] = Sector('Minería', TipoSector.PRIMARIO, 1.2)

        # Sector secundario
        self.sectores['manufactura'] = Sector(
            'Manufactura', TipoSector.SECUNDARIO, 1.0)
        self.sectores['construccion'] = Sector(
            'Construcción', TipoSector.SECUNDARIO, 0.9)

        # Sector terciario
        self.sectores['comercio'] = Sector(
            'Comercio', TipoSector.TERCIARIO, 0.9)
        self.sectores['servicios'] = Sector(
            'Servicios', TipoSector.TERCIARIO, 1.1)
        self.sectores['finanzas'] = Sector(
            'Finanzas', TipoSector.TERCIARIO, 1.3)

    def _construir_matriz_insumo_producto(self):
        """Construye la matriz de relaciones entre sectores"""
        # Simplificada: qué porcentaje de cada sector compra de otros
        self.matriz_insumo_producto = {
            'agricultura': {'mineria': 0.05, 'manufactura': 0.10, 'servicios': 0.15},
            'mineria': {'manufactura': 0.20, 'construccion': 0.15, 'servicios': 0.10},
            'manufactura': {'agricultura': 0.30, 'mineria': 0.25, 'servicios': 0.20},
            'construccion': {'manufactura': 0.40, 'mineria': 0.30, 'servicios': 0.15},
            'comercio': {'manufactura': 0.50, 'agricultura': 0.20, 'servicios': 0.10},
            'servicios': {'manufactura': 0.15, 'finanzas': 0.25, 'comercio': 0.10},
            'finanzas': {'servicios': 0.30, 'manufactura': 0.10, 'comercio': 0.05}
        }

    def asignar_empresas_a_sectores(self):
        """Asigna las empresas existentes a sectores apropiados"""
        empresas = self.mercado.getEmpresas()

        for empresa in empresas:
            # Asignación basada en los bienes que produce
            sector_asignado = self._determinar_sector_empresa(empresa)
            if sector_asignado:
                self.sectores[sector_asignado].agregar_empresa(empresa)

    def _determinar_sector_empresa(self, empresa):
        """Determina a qué sector pertenece una empresa"""
        # Primero verificar si es EmpresaProductora
        if empresa.__class__.__name__ == 'EmpresaProductora':
            # Las empresas productoras van principalmente a agricultura o manufactura
            if any(word in empresa.nombre.lower() for word in ['agro', 'agri', 'alimento']):
                return 'agricultura'
            elif any(word in empresa.nombre.lower() for word in ['manufactura', 'industria', 'prod']):
                return 'manufactura'
            else:
                # Por defecto las productoras van a agricultura
                return 'agricultura'
        else:
            # Empresas normales van a servicios o comercio
            if any(word in empresa.nombre.lower() for word in ['comercio', 'retail', 'market', 'trading']):
                return 'comercio'
            elif any(word in empresa.nombre.lower() for word in ['servicio', 'service', 'hub']):
                return 'servicios'
            else:
                return 'servicios'  # Por defecto

    def calcular_efectos_intersectoriales(self):
        """Calcula efectos de propagación entre sectores"""
        efectos = {}

        for sector_origen, compras in self.matriz_insumo_producto.items():
            if sector_origen in self.sectores:
                pib_origen = self.sectores[sector_origen].pib_sectorial

                for sector_destino, coeficiente in compras.items():
                    if sector_destino in self.sectores:
                        efecto = pib_origen * coeficiente

                        if sector_destino not in efectos:
                            efectos[sector_destino] = 0
                        efectos[sector_destino] += efecto

        return efectos

    def simular_shock_sectorial(self, sector_afectado, tipo_shock, intensidad, duracion=3):
        """Simula un shock que afecta a un sector específico"""
        if sector_afectado in self.sectores:
            sector = self.sectores[sector_afectado]
            sector.aplicar_shock_sectorial(tipo_shock, intensidad)

            # Efectos de propagación
            if tipo_shock == 'productividad' and intensidad < 1.0:
                # Shock negativo se propaga a sectores dependientes
                efectos = self.calcular_efectos_intersectoriales()

                for sector_nombre, efecto_size in efectos.items():
                    if efecto_size > 0:  # Solo si hay dependencia
                        factor_propagacion = 1.0 - (1.0 - intensidad) * 0.3
                        self.sectores[sector_nombre].aplicar_shock_sectorial(
                            tipo_shock, factor_propagacion
                        )

    def ciclo_economico_sectorial(self):
        """Ejecuta el ciclo económico desde perspectiva sectorial"""
        self.ciclo_sectorial += 1

        # Calcular PIB sectorial
        pib_total = 0
        for sector in self.sectores.values():
            pib_sectorial = sector.calcular_pib_sectorial()
            pib_total += pib_sectorial

        # Efectos intersectoriales
        efectos = self.calcular_efectos_intersectoriales()

        # Aplicar efectos de productividad sectorial
        for sector in self.sectores.values():
            factor_productividad = 1.0 + random.gauss(0, sector.volatilidad)
            factor_productividad = max(0.8, min(1.2, factor_productividad))

            for empresa in sector.empresas:
                if hasattr(empresa, 'eficiencia_produccion'):
                    empresa.eficiencia_produccion *= factor_productividad
                    # Mantener en rangos razonables
                    empresa.eficiencia_produccion = max(
                        0.5, min(1.5, empresa.eficiencia_produccion))

        # Shocks sectoriales aleatorios
        if random.random() < 0.05:  # 5% probabilidad por ciclo
            sector_afectado = random.choice(list(self.sectores.keys()))
            tipo_shock = random.choice(['productividad', 'demanda', 'costos'])
            intensidad = random.uniform(0.8, 1.2)

            self.simular_shock_sectorial(
                sector_afectado, tipo_shock, intensidad)

    def obtener_estadisticas_sectoriales(self):
        """Retorna estadísticas detalladas por sector"""
        stats = {}

        for nombre, sector in self.sectores.items():
            stats[nombre] = {
                'pib': sector.pib_sectorial,
                'empleo': sector.empleo_total,
                'empresas': len(sector.empresas),
                'productividad_promedio': sector.productividad_base,
                'nivel_tecnologico': sector.nivel_tecnologico,
                'tipo': sector.tipo.value
            }

        # Calcular participaciones
        pib_total = sum([s['pib'] for s in stats.values()])
        empleo_total = sum([s['empleo'] for s in stats.values()])

        for nombre in stats:
            if pib_total > 0:
                stats[nombre]['participacion_pib'] = stats[nombre]['pib'] / pib_total
            else:
                stats[nombre]['participacion_pib'] = 0
            if empleo_total > 0:
                stats[nombre]['participacion_empleo'] = stats[nombre]['empleo'] / empleo_total
            else:
                stats[nombre]['participacion_empleo'] = 0

        return stats

    def obtener_resumen_estructural(self):
        """Resumen de la estructura económica"""
        stats = self.obtener_estadisticas_sectoriales()

        # Participación por tipo de sector
        participacion_primario = sum([s.get('participacion_pib', 0) for s in stats.values()
                                      if s.get('tipo') == 'primario'])
        participacion_secundario = sum([s.get('participacion_pib', 0) for s in stats.values()
                                        if s.get('tipo') == 'secundario'])
        participacion_terciario = sum([s.get('participacion_pib', 0) for s in stats.values()
                                       if s.get('tipo') == 'terciario'])

        return {
            'estructura_pib': {
                'primario': participacion_primario,
                'secundario': participacion_secundario,
                'terciario': participacion_terciario
            },
            'nivel_desarrollo': self._calcular_nivel_desarrollo(
                participacion_primario, participacion_secundario, participacion_terciario
            ),
            'diversificacion': self._calcular_diversificacion(stats)
        }

    def _calcular_nivel_desarrollo(self, primario, secundario, terciario):
        """Calcula nivel de desarrollo basado en estructura sectorial"""
        if terciario > 0.6:
            return "Economía de servicios avanzada"
        elif secundario > 0.4:
            return "Economía industrializada"
        elif primario > 0.4:
            return "Economía primario-exportadora"
        else:
            return "Economía en transición"

    def _calcular_diversificacion(self, stats):
        """Calcula índice de diversificación económica"""
        participaciones = [s.get('participacion_pib', 0)
                           for s in stats.values()]

        # Índice de Herfindahl inverso
        hhi = sum([p**2 for p in participaciones])
        diversificacion = 1 / hhi if hhi > 0 else 1

        return min(1.0, diversificacion / len(stats))  # Normalizado
