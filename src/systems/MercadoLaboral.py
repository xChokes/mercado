"""Sistema de mercado laboral con perfiles de habilidades, sindicatos y movilidad"""
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class PerfilHabilidadesSectoriales:
    """Perfil de habilidades por sector para un trabajador"""
    habilidades: Dict[str, float] = field(default_factory=dict)

    def obtener_nivel(self, sector: str) -> float:
        """Obtiene el nivel de habilidad para un sector dado"""
        return self.habilidades.get(sector, 0.0)

    def sector_principal(self) -> Optional[str]:
        """Devuelve el sector donde el trabajador es más competente"""
        if not self.habilidades:
            return None
        return max(self.habilidades, key=self.habilidades.get)


@dataclass
class Sindicato:
    """Representa un sindicato laboral"""
    nombre: str
    sectores: List[str]
    cuota: float = 0.01  # 1% de aporte sindical
    poder_negociacion: float = 0.05  # Aumento salarial negociado
    miembros: List["Consumidor"] = field(default_factory=list)

    def afiliar(self, trabajador: "Consumidor") -> None:
        """Afiliar un trabajador al sindicato"""
        if trabajador not in self.miembros:
            self.miembros.append(trabajador)
            trabajador.sindicato = self

    def calcular_aporte(self, salario: float) -> float:
        """Calcula el aporte sindical sobre el salario"""
        return salario * self.cuota


class MercadoLaboral:
    """Coordinador del mercado laboral"""

    def __init__(self, mercado):
        self.mercado = mercado
        self.sectores = list(mercado.economia_sectorial.sectores.keys()) if hasattr(
            mercado, "economia_sectorial") else []
        # Crear sindicatos básicos por sector
        self.sindicatos = [
            Sindicato(f"Sindicato_{s}", [s]) for s in self.sectores]

    def crear_perfil(self) -> PerfilHabilidadesSectoriales:
        """Genera un perfil de habilidades aleatorio por sector"""
        habilidades = {sector: random.uniform(
            0.0, 1.0) for sector in self.sectores}
        return PerfilHabilidadesSectoriales(habilidades)

    def asignar_sindicato(self, trabajador: "Consumidor") -> Optional[Sindicato]:
        """Asigna aleatoriamente un sindicato al trabajador"""
        if self.sindicatos and random.random() < 0.5:  # 50% tasa de sindicalización
            sindicato = random.choice(self.sindicatos)
            sindicato.afiliar(trabajador)
            return sindicato
        return None

    def compatibilidad(self, perfil: PerfilHabilidadesSectoriales, sector: str) -> float:
        """Calcula la compatibilidad de un perfil con un sector"""
        return perfil.obtener_nivel(sector)

    def probabilidad_movilidad(self, origen: str, destino: str) -> float:
        """Probabilidad base de moverse entre sectores"""
        if origen == destino:
            return 1.0
        return 0.1  # movilidad simple entre sectores distintos

    def facilitar_contrataciones_masivas(self):
        """Facilita contrataciones masivas durante crisis de desempleo"""
        desempleados = [c for c in self.mercado.getConsumidores()
                        if not c.empleado]
        empresas_contratando = [e for e in self.mercado.getEmpresas()
                                if hasattr(e, 'empleados') and hasattr(e, 'dinero')]

        # Incentivar contratación si hay alto desempleo
        tasa_desempleo = len(desempleados) / \
            max(1, len(self.mercado.getConsumidores()))

        if tasa_desempleo > 0.25:  # Si desempleo > 25%
            # Programa de subsidios de contratación
            # Limitar a 10 empresas por ciclo
            for empresa in empresas_contratando[:10]:
                if empresa.dinero > 50000:  # Solo empresas con capital suficiente
                    # Max 5 por empresa
                    candidatos = [
                        d for d in desempleados if not d.empleado][:5]

                    for candidato in candidatos:
                        if empresa.contratar(candidato):
                            # Subsidio gubernamental por contratación
                            subsidio = candidato.ingreso_mensual * 0.5
                            empresa.dinero += subsidio
                            candidato.empleador = empresa
                            candidato.empleado = True

                            # Remover de lista de desempleados
                            if candidato in desempleados:
                                desempleados.remove(candidato)

    def crear_empresas_emergentes(self):
        """Crea nuevas empresas pequeñas para absorber desempleo"""
        from ..models.Empresa import Empresa
        from ..models.EmpresaProductora import EmpresaProductora

        desempleados = [c for c in self.mercado.getConsumidores()
                        if not c.empleado]

        # Si hay muchos desempleados, crear empresas emergentes
        if len(desempleados) > 50:
            # 1 empresa por cada 20 desempleados
            for i in range(min(3, len(desempleados) // 20)):
                # Crear empresa emergente
                if random.random() < 0.7:  # 70% productoras, 30% comerciales
                    nueva_empresa = EmpresaProductora(
                        f"StartUp{i+1}", self.mercado)

                    # Asegurar inicialización completa para evitar errores
                    if not hasattr(nueva_empresa, 'costos_unitarios') or not nueva_empresa.costos_unitarios:
                        # Inicializar con costos básicos para todos los bienes del mercado
                        nueva_empresa.costos_unitarios = {}
                        for bien in self.mercado.bienes.keys():
                            nueva_empresa.costos_unitarios[bien] = max(
                                1, random.randint(5, 20))

                    if not hasattr(nueva_empresa, 'precios') or not nueva_empresa.precios:
                        # Inicializar con precios básicos para todos los bienes
                        nueva_empresa.precios = {}
                        for bien in self.mercado.bienes.keys():
                            costo = nueva_empresa.costos_unitarios.get(
                                bien, 10)
                            # Asegurar que el precio nunca sea cero
                            nueva_empresa.precios[bien] = max(costo * 1.2, 1)

                    if not hasattr(nueva_empresa, 'capacidad_produccion') or not nueva_empresa.capacidad_produccion:
                        # Inicializar capacidad básica para todos los bienes
                        nueva_empresa.capacidad_produccion = {}
                        for bien in self.mercado.bienes.keys():
                            nueva_empresa.capacidad_produccion[bien] = random.randint(
                                5, 20)

                    # Asegurar otros atributos necesarios
                    if not hasattr(nueva_empresa, 'produccion_actual'):
                        nueva_empresa.produccion_actual = {}
                        for bien in self.mercado.bienes.keys():
                            nueva_empresa.produccion_actual[bien] = 0

                    if not hasattr(nueva_empresa, 'bienes'):
                        nueva_empresa.bienes = {}

                    # Asegurar que el sistema de acciones esté inicializado correctamente
                    if not hasattr(nueva_empresa, 'acciones_emitidas'):
                        nueva_empresa.acciones_emitidas = 0
                    if not hasattr(nueva_empresa, 'valor_accion'):
                        nueva_empresa.valor_accion = 10

                else:
                    nueva_empresa = Empresa.crear_con_acciones(
                        f"Comercio{i+1}", self.mercado, 500, {}
                    )

                    # Asegurar que el sistema de acciones esté inicializado correctamente para empresas comerciales
                    if not hasattr(nueva_empresa, 'acciones_emitidas'):
                        nueva_empresa.acciones_emitidas = 0
                    if not hasattr(nueva_empresa, 'valor_accion'):
                        nueva_empresa.valor_accion = 10

                    # Asegurar precios no vacíos
                    if not hasattr(nueva_empresa, 'precios') or not nueva_empresa.precios:
                        nueva_empresa.precios = {}
                        for bien in self.mercado.bienes.keys():
                            nueva_empresa.precios[bien] = random.randint(
                                10, 50)

                    # Verificar que no haya precios en cero
                    for bien, precio in nueva_empresa.precios.items():
                        if precio <= 0:
                            nueva_empresa.precios[bien] = random.randint(
                                10, 50)

                # Dar capital inicial gubernamental
                nueva_empresa.dinero = random.randint(50000, 150000)
                self.mercado.agregar_persona(nueva_empresa)

                # Contratar algunos desempleados inmediatamente
                candidatos = [
                    d for d in desempleados if not d.empleado][:random.randint(3, 8)]
                for candidato in candidatos:
                    if nueva_empresa.contratar(candidato):
                        candidato.empleador = nueva_empresa
                        candidato.empleado = True
                        if candidato in desempleados:
                            desempleados.remove(candidato)

    def ciclo_mercado_laboral(self):
        """Ejecuta el ciclo completo del mercado laboral"""
        # 1. Facilitar contrataciones masivas si hay alto desempleo
        self.facilitar_contrataciones_masivas()

        # 2. Crear empresas emergentes si es necesario
        self.crear_empresas_emergentes()

        # 3. Procesar aportes sindicales
        for sindicato in self.sindicatos:
            for miembro in sindicato.miembros:
                if miembro.empleado and hasattr(miembro, 'ingreso_mensual'):
                    aporte = sindicato.calcular_aporte(miembro.ingreso_mensual)
                    if miembro.dinero >= aporte:
                        miembro.dinero -= aporte

        # 4. Reasignar trabajadores con perfiles incompatibles
        self.reasignar_trabajadores_incompatibles()

    def reasignar_trabajadores_incompatibles(self):
        """Reasigna trabajadores que no están en su sector óptimo"""
        empleados = [c for c in self.mercado.getConsumidores(
        ) if c.empleado and hasattr(c, 'empleador')]

        for empleado in empleados[:10]:  # Limitar reasignaciones por ciclo
            if hasattr(empleado, 'perfil_habilidades') and empleado.empleador:
                # Encontrar mejor sector para este empleado
                mejor_sector = empleado.perfil_habilidades.sector_principal()

                if mejor_sector and random.random() < 0.1:  # 10% probabilidad de cambio
                    # Buscar empresas en el sector óptimo
                    empresas_sector = []
                    for empresa in self.mercado.getEmpresas():
                        if (hasattr(empresa, 'sector_principal') and
                            empresa.sector_principal == mejor_sector and
                            hasattr(empresa, 'empleados') and
                                len(empresa.empleados) < 20):  # No sobrepoblar empresas
                            empresas_sector.append(empresa)

                    if empresas_sector:
                        nueva_empresa = random.choice(empresas_sector)
                        if nueva_empresa.contratar(empleado):
                            # Renunciar a empresa anterior
                            empleado.empleador.despedir(empleado)
                            empleado.empleador = nueva_empresa
