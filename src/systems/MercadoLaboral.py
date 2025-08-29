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
        """Facilita contrataciones masivas con lógica más agresiva"""
        desempleados = [c for c in self.mercado.getConsumidores()
                        if not c.empleado]
        empresas = [e for e in self.mercado.getEmpresas()
                    if hasattr(e, 'dinero')]

        # Calcular tasa de desempleo actual
        tasa_desempleo = len(desempleados) / \
            max(1, len(self.mercado.getConsumidores()))

        if tasa_desempleo > 0.10:  # Si desempleo > 10%
            print(
                f"🔄 Facilitando contrataciones masivas (desempleo: {tasa_desempleo:.1%})")

            contrataciones_exitosas = 0
            objetivo_contrataciones = min(
                len(desempleados), 20)  # Máximo 20 por ciclo

            # Ordenar empresas por capacidad financiera
            empresas_viables = [
                e for e in empresas if e.dinero > 20000]  # Capital mínimo
            empresas_viables.sort(key=lambda x: x.dinero, reverse=True)

            for empresa in empresas_viables:
                if contrataciones_exitosas >= objetivo_contrataciones:
                    break

                # Cada empresa puede contratar hasta 3 empleados por ciclo
                max_contrataciones_empresa = min(
                    3, int(empresa.dinero / 30000))
                contrataciones_empresa = 0

                # Seleccionar candidatos aleatorios
                candidatos_disponibles = [
                    d for d in desempleados if not d.empleado]
                random.shuffle(candidatos_disponibles)

                for candidato in candidatos_disponibles[:max_contrataciones_empresa]:
                    if contrataciones_empresa >= max_contrataciones_empresa:
                        break

                    if empresa.contratar(candidato):
                        contrataciones_exitosas += 1
                        contrataciones_empresa += 1

                        # Subsidio gubernamental por contratación de emergencia
                        if hasattr(self.mercado, 'gobierno'):
                            subsidio = candidato.ingreso_mensual * 0.5  # 50% del salario
                            empresa.dinero += subsidio
                            self.mercado.gobierno.presupuesto -= subsidio

            if contrataciones_exitosas > 0:
                print(
                    f"✅ {contrataciones_exitosas} contrataciones de emergencia realizadas")

    def ciclo_mercado_laboral(self):
        """Ciclo principal del mercado laboral con contrataciones y despidos dinámicos"""
        # 1. Facilitar contrataciones si hay alto desempleo
        self.facilitar_contrataciones_masivas()

        # 2. Gestionar despidos por crisis económica
        if hasattr(self.mercado, 'fase_ciclo_economico'):
            if self.mercado.fase_ciclo_economico in ['recesion', 'depresion']:
                self._gestionar_despidos_por_crisis()
            elif self.mercado.fase_ciclo_economico in ['expansion', 'recuperacion']:
                self._gestionar_contrataciones_por_crecimiento()

        # 3. Movilidad laboral básica
        self._procesar_movilidad_laboral()

    def _gestionar_despidos_por_crisis(self):
        """Gestiona despidos durante crisis económica"""
        for empresa in self.mercado.getEmpresas():
            if hasattr(empresa, 'empleados') and hasattr(empresa, 'dinero'):
                # Si la empresa está en problemas financieros
                if empresa.dinero < 10000:  # Umbral de crisis
                    empleados_actuales = [
                        e for e in empresa.empleados if e.empleado]
                    # Despedir hasta 20% de empleados
                    despidos = min(len(empleados_actuales), max(
                        1, len(empleados_actuales) // 5))

                    for _ in range(despidos):
                        if empleados_actuales:
                            empleado = random.choice(empleados_actuales)
                            empresa.despedir(empleado)
                            empleados_actuales.remove(empleado)

    def _gestionar_contrataciones_por_crecimiento(self):
        """Gestiona contrataciones durante crecimiento económico"""
        desempleados = [c for c in self.mercado.getConsumidores()
                        if not c.empleado]

        for empresa in self.mercado.getEmpresas():
            if hasattr(empresa, 'dinero') and empresa.dinero > 100000:  # Empresas prósperas
                # Probabilidad de contratar durante crecimiento
                if random.random() < 0.3 and desempleados:  # 30% probabilidad
                    candidato = random.choice(desempleados)
                    if empresa.contratar(candidato):
                        desempleados.remove(candidato)

    def _procesar_movilidad_laboral(self):
        """Procesa movilidad laboral básica entre sectores"""
        empleados = [c for c in self.mercado.getConsumidores() if c.empleado]

        # 5% de empleados pueden cambiar de trabajo cada ciclo
        empleados_moviles = random.sample(
            empleados, min(len(empleados), len(empleados) // 20))

        for empleado in empleados_moviles:
            if random.random() < 0.1:  # 10% probabilidad de cambio
                # Buscar mejor oportunidad
                empresas_alternativas = [e for e in self.mercado.getEmpresas()
                                         if e != empleado.empleador and hasattr(e, 'dinero')
                                         and e.dinero > 50000]

                if empresas_alternativas:
                    nueva_empresa = random.choice(empresas_alternativas)
                    salario_actual = empleado.ingreso_mensual

                    # Intentar obtener mejor salario
                    nuevo_salario = salario_actual * \
                        random.uniform(1.05, 1.15)  # 5-15% aumento

                    if nueva_empresa.dinero > nuevo_salario * 12:  # Puede pagar el salario anual
                        empleado.empleador.despedir(empleado)
                        empleado.ingreso_mensual = nuevo_salario
                        nueva_empresa.contratar(empleado)

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

    def priorizar_empresa_contratacion(self, empresa_nombre: str, prioridad: float = 1.5):
        """
        Prioriza una empresa para contrataciones en el mercado laboral
        
        Args:
            empresa_nombre: Nombre de la empresa a priorizar
            prioridad: Multiplicador de prioridad (1.5 = 50% más probabilidad)
        """
        if not hasattr(self, 'prioridades_contratacion'):
            self.prioridades_contratacion = {}
        
        self.prioridades_contratacion[empresa_nombre] = prioridad
        
        # Facilitar contrataciones para esta empresa específica
        empresa_objetivo = None
        for empresa in self.mercado.getEmpresas():
            if hasattr(empresa, 'nombre') and empresa.nombre == empresa_nombre:
                empresa_objetivo = empresa
                break
        
        if empresa_objetivo and hasattr(empresa_objetivo, 'dinero'):
            desempleados = [c for c in self.mercado.getConsumidores() if not c.empleado]
            
            # Intentar contratar hasta 3 empleados adicionales
            max_contrataciones = min(3, len(desempleados), int(empresa_objetivo.dinero / 25000))
            contrataciones_realizadas = 0
            
            # Seleccionar candidatos con mejor compatibilidad
            candidatos_ordenados = desempleados.copy()
            random.shuffle(candidatos_ordenados)  # Aleatorizar para diversidad
            
            for candidato in candidatos_ordenados[:max_contrataciones]:
                if contrataciones_realizadas >= max_contrataciones:
                    break
                    
                # Aumentar probabilidad de contratación por prioridad
                probabilidad_base = 0.6  # 60% base
                probabilidad_ajustada = min(0.95, probabilidad_base * prioridad)
                
                if random.random() < probabilidad_ajustada:
                    if empresa_objetivo.contratar(candidato):
                        contrataciones_realizadas += 1
                        print(f"📋 {empresa_nombre} contrató a {candidato.nombre} (prioridad activada)")
            
            if contrataciones_realizadas > 0:
                print(f"✅ Empresa {empresa_nombre} completó {contrataciones_realizadas} contrataciones prioritarias")

    def obtener_empresas_mejor_reputacion(self, limite: int = 5) -> List[str]:
        """
        Obtiene las empresas con mejor reputación para contratación
        
        Args:
            limite: Número máximo de empresas a retornar
            
        Returns:
            Lista de nombres de empresas ordenadas por reputación
        """
        empresas_con_reputacion = []
        
        for empresa in self.mercado.getEmpresas():
            if hasattr(empresa, 'nombre'):
                # Calcular score de reputación basado en múltiples factores
                score_reputacion = 0.5  # Base
                
                # Factor financiero
                if hasattr(empresa, 'dinero'):
                    if empresa.dinero > 100000:
                        score_reputacion += 0.2
                    elif empresa.dinero > 50000:
                        score_reputacion += 0.1
                
                # Factor de empleados (estabilidad)
                if hasattr(empresa, 'empleados'):
                    if len(empresa.empleados) > 10:
                        score_reputacion += 0.2
                    elif len(empresa.empleados) > 5:
                        score_reputacion += 0.1
                
                # Factor reputación específica (si existe)
                if hasattr(empresa, 'reputacion_mercado'):
                    score_reputacion += empresa.reputacion_mercado * 0.3
                
                # Factor de innovación
                if hasattr(empresa, 'nivel_tecnologico'):
                    score_reputacion += empresa.nivel_tecnologico * 0.1
                
                empresas_con_reputacion.append((empresa.nombre, score_reputacion))
        
        # Ordenar por reputación descendente
        empresas_con_reputacion.sort(key=lambda x: x[1], reverse=True)
        
        # Retornar solo los nombres de las mejores empresas
        return [nombre for nombre, _ in empresas_con_reputacion[:limite]]

    def aplicar_incentivos_contratacion(self, sector: str = None, multiplicador: float = 1.3):
        """
        Aplica incentivos temporales para contratación en un sector específico
        
        Args:
            sector: Sector económico a incentivar (None para todos)
            multiplicador: Multiplicador de incentivo de contratación
        """
        if not hasattr(self, 'incentivos_activos'):
            self.incentivos_activos = {}
        
        if sector:
            self.incentivos_activos[sector] = multiplicador
        else:
            self.incentivos_activos['general'] = multiplicador
        
        print(f"💰 Incentivos de contratación aplicados - Sector: {sector or 'General'}, Multiplicador: {multiplicador}x")
        
        # Procesar contrataciones con incentivos
        desempleados = [c for c in self.mercado.getConsumidores() if not c.empleado]
        empresas_elegibles = []
        
        for empresa in self.mercado.getEmpresas():
            if hasattr(empresa, 'dinero') and empresa.dinero > 30000:
                # Verificar si empresa es elegible según sector
                elegible = True
                if sector and hasattr(empresa, 'sector_principal'):
                    elegible = empresa.sector_principal == sector
                
                if elegible:
                    empresas_elegibles.append(empresa)
        
        # Facilitar contrataciones con incentivos
        contrataciones_incentivadas = 0
        objetivo_contrataciones = min(len(desempleados), len(empresas_elegibles) * 2)
        
        for empresa in empresas_elegibles:
            if contrataciones_incentivadas >= objetivo_contrataciones:
                break
            
            candidatos_disponibles = [d for d in desempleados if not d.empleado]
            max_contrataciones_empresa = min(2, int(empresa.dinero / 20000))
            
            for _ in range(max_contrataciones_empresa):
                if candidatos_disponibles and contrataciones_incentivadas < objetivo_contrataciones:
                    candidato = random.choice(candidatos_disponibles)
                    
                    # Aplicar incentivo gubernamental
                    salario_incentivado = getattr(candidato, 'ingreso_mensual', 2000) * 0.3
                    empresa.dinero += salario_incentivado  # Subsidio gubernamental
                    
                    if empresa.contratar(candidato):
                        candidatos_disponibles.remove(candidato)
                        contrataciones_incentivadas += 1
        
        if contrataciones_incentivadas > 0:
            print(f"✅ {contrataciones_incentivadas} contrataciones incentivadas realizadas")
