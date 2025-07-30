"""
Sistema de Innovación y Tecnología para la Simulación Económica
Implementa I+D, adopción tecnológica y ciclos de vida de productos
"""
import random
import math
from enum import Enum
from dataclasses import dataclass
from typing import Dict, List


class TipoInnovacion(Enum):
    PRODUCTO = "producto"      # Nuevos productos
    PROCESO = "proceso"        # Mejores métodos de producción
    ORGANIZACIONAL = "organizacional"  # Nuevas formas de organización
    MARKETING = "marketing"    # Nuevas estrategias de mercado


class FaseVidaProducto(Enum):
    INTRODUCCION = "introduccion"
    CRECIMIENTO = "crecimiento"
    MADUREZ = "madurez"
    DECLIVE = "declive"


@dataclass
class Tecnologia:
    nombre: str
    tipo: TipoInnovacion
    mejora_productividad: float  # Factor multiplicativo
    reduccion_costos: float     # Porcentaje de reducción
    costo_adopcion: int        # Costo inicial de adopción
    difusion_actual: float = 0.0  # % de empresas que la han adoptado
    ciclo_vida: int = 0        # Ciclos desde introducción


class ProductoInnovador:
    def __init__(self, nombre, categoria, innovacion_base):
        self.nombre = nombre
        self.categoria = categoria
        self.innovacion_base = innovacion_base
        self.fase_vida = FaseVidaProducto.INTRODUCCION
        self.ciclos_en_fase = 0
        self.demanda_acumulada = 0
        self.precio_inicial = 0
        self.factor_novedad = 1.0  # Premium por novedad

        # Características del ciclo de vida
        self.duracion_fases = {
            FaseVidaProducto.INTRODUCCION: random.randint(3, 8),
            FaseVidaProducto.CRECIMIENTO: random.randint(8, 15),
            FaseVidaProducto.MADUREZ: random.randint(15, 30),
            FaseVidaProducto.DECLIVE: random.randint(10, 20)
        }


class SistemaInnovacion:
    """Sistema de gestión de innovación tecnológica"""

    def __init__(self, mercado):
        self.mercado = mercado
        self.tecnologias_disponibles = []
        self.productos_innovadores = []
        self.inversion_id_total = 0
        self.spillovers_tecnologicos = {}  # Externalidades tecnológicas

        # Inicializar tecnologías base
        self._crear_tecnologias_iniciales()

    def _crear_tecnologias_iniciales(self):
        """Crea un conjunto inicial de tecnologías disponibles"""
        tecnologias_base = [
            Tecnologia("Automatización Básica",
                       TipoInnovacion.PROCESO, 1.15, 0.10, 50000),
            Tecnologia("Gestión de Calidad",
                       TipoInnovacion.ORGANIZACIONAL, 1.10, 0.05, 30000),
            Tecnologia("Marketing Digital",
                       TipoInnovacion.MARKETING, 1.05, 0.02, 20000),
            Tecnologia("Sistemas ERP", TipoInnovacion.ORGANIZACIONAL,
                       1.20, 0.15, 80000),
            Tecnologia("Robótica Industrial",
                       TipoInnovacion.PROCESO, 1.30, 0.25, 150000),
            Tecnologia("Inteligencia Artificial",
                       TipoInnovacion.PROCESO, 1.40, 0.30, 200000),
            Tecnologia("Biotecnología", TipoInnovacion.PRODUCTO,
                       1.25, 0.20, 120000),
            Tecnologia("Nanotecnología", TipoInnovacion.PRODUCTO,
                       1.35, 0.25, 180000)
        ]

        self.tecnologias_disponibles = tecnologias_base

    def empresa_invierte_id(self, empresa, monto_inversion):
        """Una empresa invierte en I+D"""
        if empresa.dinero >= monto_inversion:
            empresa.dinero -= monto_inversion
            self.inversion_id_total += monto_inversion

            # Probabilidad de breakthrough basada en inversión
            prob_breakthrough = min(0.15, monto_inversion / 100000 * 0.05)

            if random.random() < prob_breakthrough:
                return self._generar_innovacion(empresa, monto_inversion)
            else:
                # Mejora gradual de productividad
                if hasattr(empresa, 'eficiencia_produccion'):
                    mejora = monto_inversion / 1000000  # Mejora proporcional
                    empresa.eficiencia_produccion += mejora
                return None, "Mejora gradual en procesos"

        return None, "Fondos insuficientes"

    def _generar_innovacion(self, empresa, inversion):
        """Genera una nueva innovación"""
        tipo_innovacion = random.choice(list(TipoInnovacion))

        if tipo_innovacion == TipoInnovacion.PRODUCTO:
            return self._crear_producto_innovador(empresa, inversion)
        else:
            return self._crear_tecnologia_proceso(empresa, tipo_innovacion, inversion)

    def _crear_producto_innovador(self, empresa, inversion):
        """Crea un nuevo producto innovador"""
        # Generar nombre único del producto
        base_productos = list(self.mercado.bienes.keys())
        nombre_base = random.choice(base_productos)
        nombre_nuevo = f"{nombre_base}_Pro"

        # Evitar duplicados
        contador = 1
        while nombre_nuevo in [p.nombre for p in self.productos_innovadores]:
            nombre_nuevo = f"{nombre_base}_Pro_{contador}"
            contador += 1

        categoria = self.mercado.bienes[nombre_base].categoria
        innovacion_base = inversion / 100000  # Factor de innovación

        producto = ProductoInnovador(nombre_nuevo, categoria, innovacion_base)
        producto.precio_inicial = empresa.precios.get(
            nombre_base, 50) * (1 + innovacion_base)

        self.productos_innovadores.append(producto)

        # Agregar producto al mercado
        from Bien import Bien
        nuevo_bien = Bien(nombre_nuevo, categoria)
        self.mercado.bienes[nombre_nuevo] = nuevo_bien

        # Agregar a empresa
        empresa.bienes[nombre_nuevo] = []
        empresa.precios[nombre_nuevo] = producto.precio_inicial

        # Inicializar capacidad de producción
        if hasattr(empresa, 'capacidad_produccion'):
            empresa.capacidad_produccion[nombre_nuevo] = max(
                10, int(inversion / 10000))

        return producto, f"Nuevo producto innovador: {nombre_nuevo}"

    def _crear_tecnologia_proceso(self, empresa, tipo, inversion):
        """Crea una nueva tecnología de proceso"""
        mejora_productividad = 1 + \
            (inversion / 200000)  # Mejora basada en inversión
        reduccion_costos = min(0.5, inversion / 500000)  # Hasta 50% reducción

        nombre_tech = f"Tech_{tipo.value}_{len(self.tecnologias_disponibles)}"

        nueva_tech = Tecnologia(
            nombre_tech, tipo, mejora_productividad,
            reduccion_costos, int(inversion * 0.8)
        )

        self.tecnologias_disponibles.append(nueva_tech)

        # La empresa que la desarrolló la adopta automáticamente
        self.adoptar_tecnologia(empresa, nueva_tech)

        return nueva_tech, f"Nueva tecnología desarrollada: {nombre_tech}"

    def adoptar_tecnologia(self, empresa, tecnologia):
        """Una empresa adopta una tecnología existente"""
        if empresa.dinero >= tecnologia.costo_adopcion:
            empresa.dinero -= tecnologia.costo_adopcion

            # Aplicar beneficios de la tecnología
            if tecnologia.tipo == TipoInnovacion.PROCESO:
                if hasattr(empresa, 'eficiencia_produccion'):
                    empresa.eficiencia_produccion *= tecnologia.mejora_productividad

                # Reducir costos unitarios
                for bien in empresa.costos_unitarios:
                    empresa.costos_unitarios[bien] *= (
                        1 - tecnologia.reduccion_costos)

            elif tecnologia.tipo == TipoInnovacion.ORGANIZACIONAL:
                # Mejorar gestión (reducir costos fijos)
                if hasattr(empresa, 'costos_fijos_mensuales'):
                    empresa.costos_fijos_mensuales *= (
                        1 - tecnologia.reduccion_costos)

            elif tecnologia.tipo == TipoInnovacion.MARKETING:
                # Mejorar capacidad de venta (aumentar demanda)
                if hasattr(empresa, 'factor_marketing'):
                    empresa.factor_marketing = getattr(
                        empresa, 'factor_marketing', 1.0) * tecnologia.mejora_productividad

            # Marcar como adoptada
            if not hasattr(empresa, 'tecnologias_adoptadas'):
                empresa.tecnologias_adoptadas = []
            empresa.tecnologias_adoptadas.append(tecnologia.nombre)

            # Actualizar difusión
            empresas_totales = len(self.mercado.getEmpresas())
            empresas_con_tech = sum([1 for e in self.mercado.getEmpresas()
                                     if hasattr(e, 'tecnologias_adoptadas') and
                                     tecnologia.nombre in e.tecnologias_adoptadas])

            tecnologia.difusion_actual = empresas_con_tech / \
                max(1, empresas_totales)

            return True

        return False

    def calcular_spillovers(self):
        """Calcula spillovers tecnológicos entre sectores"""
        if hasattr(self.mercado, 'economia_sectorial'):
            sectores = self.mercado.economia_sectorial.sectores

            for sector_nombre, sector in sectores.items():
                spillover = 0

                # Spillover basado en tecnologías adoptadas en el sector
                for empresa in sector.empresas:
                    if hasattr(empresa, 'tecnologias_adoptadas'):
                        spillover += len(empresa.tecnologias_adoptadas) * 0.02

                # Aplicar spillover a empresas del sector
                for empresa in sector.empresas:
                    if hasattr(empresa, 'eficiencia_produccion'):
                        empresa.eficiencia_produccion *= (1 + spillover * 0.1)

                self.spillovers_tecnologicos[sector_nombre] = spillover

    def evolucionar_productos_innovadores(self):
        """Evoluciona el ciclo de vida de productos innovadores"""
        for producto in self.productos_innovadores[:]:
            producto.ciclos_en_fase += 1

            # Verificar transición de fase
            if producto.ciclos_en_fase >= producto.duracion_fases[producto.fase_vida]:
                self._transicionar_fase_producto(producto)

            # Aplicar efectos de la fase actual
            self._aplicar_efectos_fase(producto)

    def _transicionar_fase_producto(self, producto):
        """Transiciona un producto a la siguiente fase de vida"""
        fases_orden = [FaseVidaProducto.INTRODUCCION, FaseVidaProducto.CRECIMIENTO,
                       FaseVidaProducto.MADUREZ, FaseVidaProducto.DECLIVE]

        indice_actual = fases_orden.index(producto.fase_vida)

        if indice_actual < len(fases_orden) - 1:
            producto.fase_vida = fases_orden[indice_actual + 1]
            producto.ciclos_en_fase = 0
        else:
            # Producto llega al final de su ciclo
            self._retirar_producto(producto)

    def _aplicar_efectos_fase(self, producto):
        """Aplica efectos específicos de cada fase del ciclo de vida"""
        # Encontrar empresas que producen este producto
        empresas_productoras = [e for e in self.mercado.getEmpresas()
                                if producto.nombre in e.bienes]

        for empresa in empresas_productoras:
            if producto.fase_vida == FaseVidaProducto.INTRODUCCION:
                # Fase de introducción: pocos compradores, precios altos
                empresa.precios[producto.nombre] = producto.precio_inicial * \
                    producto.factor_novedad

            elif producto.fase_vida == FaseVidaProducto.CRECIMIENTO:
                # Fase de crecimiento: demanda aumenta, precios se estabilizan
                empresa.precios[producto.nombre] *= 0.95  # Reducción gradual

                # Aumentar capacidad de producción
                if hasattr(empresa, 'capacidad_produccion'):
                    empresa.capacidad_produccion[producto.nombre] = int(
                        empresa.capacidad_produccion[producto.nombre] * 1.1
                    )

            elif producto.fase_vida == FaseVidaProducto.MADUREZ:
                # Fase de madurez: competencia de precios
                empresa.precios[producto.nombre] *= 0.98

            elif producto.fase_vida == FaseVidaProducto.DECLIVE:
                # Fase de declive: reducir producción
                if hasattr(empresa, 'capacidad_produccion'):
                    empresa.capacidad_produccion[producto.nombre] = int(
                        empresa.capacidad_produccion[producto.nombre] * 0.9
                    )

    def _retirar_producto(self, producto):
        """Retira un producto del mercado al final de su ciclo"""
        # Remover de empresas
        for empresa in self.mercado.getEmpresas():
            if producto.nombre in empresa.bienes:
                del empresa.bienes[producto.nombre]
            if producto.nombre in empresa.precios:
                del empresa.precios[producto.nombre]
            if hasattr(empresa, 'capacidad_produccion') and producto.nombre in empresa.capacidad_produccion:
                del empresa.capacidad_produccion[producto.nombre]

        # Remover del mercado
        if producto.nombre in self.mercado.bienes:
            del self.mercado.bienes[producto.nombre]

        # Remover de lista de productos innovadores
        self.productos_innovadores.remove(producto)

    def ciclo_innovacion(self):
        """Ejecuta el ciclo de innovación tecnológica"""
        # Empresas deciden invertir en I+D
        for empresa in self.mercado.getEmpresas():
            if hasattr(empresa, 'factor_expansion') and empresa.dinero > 100000:
                # Probabilidad de inversión en I+D basada en capacidad financiera
                prob_id = min(0.3, empresa.dinero / 1000000 * 0.1)

                if random.random() < prob_id:
                    # Monto de inversión entre 5% y 15% del capital
                    monto = empresa.dinero * random.uniform(0.05, 0.15)
                    self.empresa_invierte_id(empresa, monto)

        # Adopción de tecnologías existentes
        for empresa in self.mercado.getEmpresas():
            tecnologias_no_adoptadas = [t for t in self.tecnologias_disponibles
                                        if not hasattr(empresa, 'tecnologias_adoptadas') or
                                        t.nombre not in empresa.tecnologias_adoptadas]

            if tecnologias_no_adoptadas and empresa.dinero > 50000:
                # Probabilidad de adopción basada en difusión actual
                tech_candidata = random.choice(tecnologias_no_adoptadas)
                prob_adopcion = 0.1 + tech_candidata.difusion_actual * 0.2

                if random.random() < prob_adopcion:
                    self.adoptar_tecnologia(empresa, tech_candidata)

        # Evolucionar productos innovadores
        self.evolucionar_productos_innovadores()

        # Calcular spillovers tecnológicos
        self.calcular_spillovers()

        # Evolucionar tecnologías (aumentar ciclo de vida)
        for tech in self.tecnologias_disponibles:
            tech.ciclo_vida += 1

    def obtener_estadisticas_innovacion(self):
        """Retorna estadísticas del sistema de innovación"""
        stats = {
            'inversion_id_total': self.inversion_id_total,
            'tecnologias_disponibles': len(self.tecnologias_disponibles),
            'productos_innovadores': len(self.productos_innovadores),
            'spillovers_sectoriales': dict(self.spillovers_tecnologicos)
        }

        # Estadísticas por tipo de innovación
        for tipo in TipoInnovacion:
            techs_tipo = [
                t for t in self.tecnologias_disponibles if t.tipo == tipo]
            stats[f'tecnologias_{tipo.value}'] = len(techs_tipo)

            if techs_tipo:
                difusion_promedio = sum(
                    [t.difusion_actual for t in techs_tipo]) / len(techs_tipo)
                stats[f'difusion_{tipo.value}'] = difusion_promedio

        # Estadísticas de adopción empresarial
        empresas_innovadoras = sum([1 for e in self.mercado.getEmpresas()
                                    if hasattr(e, 'tecnologias_adoptadas') and
                                    len(e.tecnologias_adoptadas) > 0])

        stats['empresas_innovadoras'] = empresas_innovadoras
        stats['porcentaje_empresas_innovadoras'] = empresas_innovadoras / \
            max(1, len(self.mercado.getEmpresas()))

        return stats
