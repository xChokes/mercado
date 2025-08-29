"""
Integrador de Empresas Hiperrealistas
=====================================

Este módulo integra las características hiperrealistas de las empresas
con el sistema de simulación existente, proporcionando mayor realismo
en el comportamiento empresarial.
"""

import random
import logging
from typing import Dict, List, Any, Optional
from ..models.EmpresaProductora import EmpresaProductora
from ..ai.EmpresaIA import EmpresaIA
from ..config.ConfigEconomica import ConfigEconomica


class GestorEmpresasHiperrealistas:
    """
    Gestor que administra y coordina todas las mejoras empresariales hiperrealistas
    """
    
    def __init__(self, mercado):
        self.mercado = mercado
        self.empresas_mejoradas = {}
        self.sistema_activo = False
        
        # Configuraciones del sistema
        self.probabilidad_crisis_empresa = 0.02  # 2% por ciclo
        self.factor_competencia_intensidad = 1.0
        self.habilitado_ia_empresarial = True
        
        # Métricas del sistema
        self.empresas_rescatadas = 0
        self.fusiones_realizadas = 0
        self.innovaciones_exitosas = 0
        self.crisis_empresariales_resueltas = 0
        
    def inicializar_sistema(self):
        """Inicializa el sistema de empresas hiperrealistas"""
        try:
            logging.info("Inicializando sistema de empresas hiperrealistas...")
            
            # Mejorar empresas existentes
            self._mejorar_empresas_existentes()
            
            # Configurar sistemas de apoyo
            self._configurar_sistemas_apoyo()
            
            # Activar monitoring empresarial
            self._activar_monitoring_empresarial()
            
            self.sistema_activo = True
            logging.info(f"Sistema hiperrealista inicializado con {len(self.empresas_mejoradas)} empresas mejoradas")
            
        except Exception as e:
            logging.error(f"Error inicializando sistema hiperrealista: {e}")
    
    def _mejorar_empresas_existentes(self):
        """Aplica mejoras hiperrealistas a empresas existentes"""
        empresas = self.mercado.getEmpresas()
        
        for empresa in empresas:
            try:
                # Aplicar mejoras según tipo de empresa
                if isinstance(empresa, EmpresaProductora):
                    self._aplicar_mejoras_productora(empresa)
                else:
                    self._aplicar_mejoras_basicas(empresa)
                
                # Registrar empresa mejorada
                self.empresas_mejoradas[empresa.nombre] = {
                    'tipo': type(empresa).__name__,
                    'mejoras_aplicadas': [],
                    'estado_financiero': 'estable',
                    'ciclos_monitoreados': 0
                }
                
            except Exception as e:
                logging.warning(f"No se pudo mejorar empresa {empresa.nombre}: {e}")
    
    def _aplicar_mejoras_productora(self, empresa: EmpresaProductora):
        """Aplica mejoras específicas a empresas productoras"""
        mejoras = []
        
        # 1. Sistema de gestión de riesgos financieros
        if not hasattr(empresa, 'sistema_riesgos'):
            empresa.sistema_riesgos = SistemaGestionRiesgos(empresa)
            mejoras.append('gestion_riesgos')
        
        # 2. Optimización de cadena de suministro
        if not hasattr(empresa, 'cadena_suministro'):
            empresa.cadena_suministro = CadenasuministroOptimizada(empresa)
            mejoras.append('cadena_suministro')
        
        # 3. Sistema de innovación continua
        if not hasattr(empresa, 'laboratorio_id'):
            empresa.laboratorio_id = LaboratorioID(empresa)
            mejoras.append('laboratorio_id')
        
        # 4. Gestión avanzada de recursos humanos
        if not hasattr(empresa, 'gestion_rrhh'):
            empresa.gestion_rrhh = GestionRecursosHumanos(empresa)
            mejoras.append('gestion_rrhh')
        
        # 5. Sistema de inteligencia de mercado
        if not hasattr(empresa, 'inteligencia_mercado'):
            empresa.inteligencia_mercado = InteligenciaMercado(empresa, self.mercado)
            mejoras.append('inteligencia_mercado')
        
        # 6. Gestión de sostenibilidad
        if not hasattr(empresa, 'gestion_sostenibilidad'):
            empresa.gestion_sostenibilidad = GestionSostenibilidad(empresa)
            mejoras.append('gestion_sostenibilidad')
        
        # Registrar mejoras aplicadas
        if empresa.nombre in self.empresas_mejoradas:
            self.empresas_mejoradas[empresa.nombre]['mejoras_aplicadas'] = mejoras
    
    def _aplicar_mejoras_basicas(self, empresa):
        """Aplica mejoras básicas a empresas regulares"""
        mejoras = []
        
        # Sistema básico de gestión de riesgos
        if not hasattr(empresa, 'nivel_riesgo'):
            empresa.nivel_riesgo = random.uniform(0.2, 0.8)
            empresa.tolerancia_riesgo = random.uniform(0.3, 0.7)
            mejoras.append('gestion_riesgo_basica')
        
        # Sistema de fidelización de clientes
        if not hasattr(empresa, 'satisfaccion_cliente'):
            empresa.satisfaccion_cliente = random.uniform(0.5, 0.9)
            empresa.programa_fidelizacion = random.choice([True, False])
            mejoras.append('fidelizacion_clientes')
        
        # Gestión de marca
        if not hasattr(empresa, 'valor_marca'):
            empresa.valor_marca = random.uniform(0.3, 0.8)
            empresa.inversion_marketing = empresa.dinero * random.uniform(0.02, 0.08)
            mejoras.append('gestion_marca')
        
        if empresa.nombre in self.empresas_mejoradas:
            self.empresas_mejoradas[empresa.nombre]['mejoras_aplicadas'] = mejoras
    
    def _configurar_sistemas_apoyo(self):
        """Configura sistemas de apoyo empresarial"""
        # Sistema de rescate empresarial mejorado
        if not hasattr(self.mercado, 'rescate_empresarial_avanzado'):
            self.mercado.rescate_empresarial_avanzado = SistemaRescateAvanzado(self.mercado)
        
        # Sistema de fusiones y adquisiciones
        if not hasattr(self.mercado, 'sistema_fusiones'):
            self.mercado.sistema_fusiones = SistemaFusionesAdquisiciones(self.mercado)
        
        # Observatorio empresarial
        if not hasattr(self.mercado, 'observatorio_empresarial'):
            self.mercado.observatorio_empresarial = ObservatorioEmpresarial(self.mercado)
    
    def _activar_monitoring_empresarial(self):
        """Activa el sistema de monitoreo empresarial continuo"""
        self.monitoring_activo = True
        logging.info("Sistema de monitoreo empresarial activado")
    
    def ciclo_empresas_hiperrealistas(self):
        """Ejecuta un ciclo del sistema de empresas hiperrealistas"""
        if not self.sistema_activo:
            return
        
        try:
            # 1. Monitorear estado financiero de todas las empresas
            self._monitorear_estado_financiero()
            
            # 2. Aplicar sistemas de gestión avanzada
            self._ejecutar_sistemas_gestion()
            
            # 3. Gestionar crisis empresariales
            self._gestionar_crisis_empresariales()
            
            # 4. Facilitar innovación y mejora continua
            self._facilitar_innovacion_continua()
            
            # 5. Gestionar competencia empresarial
            self._gestionar_competencia_empresarial()
            
            # 6. Evaluar oportunidades de fusiones
            self._evaluar_fusiones_adquisiciones()
            
            # 7. Actualizar métricas del sistema
            self._actualizar_metricas_sistema()
            
        except Exception as e:
            logging.error(f"Error en ciclo empresas hiperrealistas: {e}")
    
    def _monitorear_estado_financiero(self):
        """Monitorea el estado financiero de todas las empresas"""
        for empresa in self.mercado.getEmpresas():
            if empresa.nombre not in self.empresas_mejoradas:
                continue
                
            estado_anterior = self.empresas_mejoradas[empresa.nombre]['estado_financiero']
            estado_actual = self._evaluar_estado_financiero(empresa)
            
            # Detectar cambios críticos
            if estado_anterior != estado_actual:
                self._notificar_cambio_estado(empresa, estado_anterior, estado_actual)
            
            self.empresas_mejoradas[empresa.nombre]['estado_financiero'] = estado_actual
            self.empresas_mejoradas[empresa.nombre]['ciclos_monitoreados'] += 1
    
    def _evaluar_estado_financiero(self, empresa) -> str:
        """Evalúa el estado financiero actual de una empresa"""
        if hasattr(empresa, 'en_quiebra') and empresa.en_quiebra:
            return 'quiebra'
        
        if hasattr(empresa, 'costos_fijos_mensuales'):
            ratio_liquidez = empresa.dinero / max(empresa.costos_fijos_mensuales, 1)
            
            if ratio_liquidez < 1:
                return 'crisis'
            elif ratio_liquidez < 3:
                return 'riesgo'
            elif ratio_liquidez < 8:
                return 'estable'
            else:
                return 'prospero'
        
        # Evaluación básica para empresas sin costos_fijos_mensuales
        if empresa.dinero < 1000:
            return 'crisis'
        elif empresa.dinero < 10000:
            return 'riesgo'
        elif empresa.dinero < 50000:
            return 'estable'
        else:
            return 'prospero'
    
    def _notificar_cambio_estado(self, empresa, estado_anterior: str, estado_actual: str):
        """Notifica cambios significativos en el estado empresarial"""
        cambios_criticos = [
            ('estable', 'crisis'), ('prospero', 'crisis'),
            ('estable', 'quiebra'), ('riesgo', 'quiebra')
        ]
        
        if (estado_anterior, estado_actual) in cambios_criticos:
            logging.warning(f"ALERTA: {empresa.nombre} cambió de {estado_anterior} a {estado_actual}")
            
            # Activar medidas de emergencia
            if hasattr(empresa, 'sistema_riesgos'):
                empresa.sistema_riesgos.activar_protocolo_emergencia()
    
    def _ejecutar_sistemas_gestion(self):
        """Ejecuta todos los sistemas de gestión empresarial"""
        for empresa in self.mercado.getEmpresas():
            try:
                # Sistema de gestión de riesgos
                if hasattr(empresa, 'sistema_riesgos'):
                    empresa.sistema_riesgos.ciclo_gestion_riesgos()
                
                # Cadena de suministro
                if hasattr(empresa, 'cadena_suministro'):
                    empresa.cadena_suministro.optimizar_cadena()
                
                # Laboratorio I+D
                if hasattr(empresa, 'laboratorio_id'):
                    empresa.laboratorio_id.ciclo_investigacion()
                
                # Gestión RRHH
                if hasattr(empresa, 'gestion_rrhh'):
                    empresa.gestion_rrhh.ciclo_recursos_humanos()
                
                # Inteligencia de mercado
                if hasattr(empresa, 'inteligencia_mercado'):
                    empresa.inteligencia_mercado.actualizar_inteligencia()
                
                # Gestión de sostenibilidad
                if hasattr(empresa, 'gestion_sostenibilidad'):
                    empresa.gestion_sostenibilidad.ciclo_sostenibilidad()
                
            except Exception as e:
                logging.warning(f"Error ejecutando sistemas de gestión para {empresa.nombre}: {e}")
    
    def _gestionar_crisis_empresariales(self):
        """Gestiona crisis empresariales con medidas de rescate avanzadas"""
        empresas_en_crisis = [
            empresa for empresa in self.mercado.getEmpresas()
            if empresa.nombre in self.empresas_mejoradas and 
            self.empresas_mejoradas[empresa.nombre]['estado_financiero'] in ['crisis', 'quiebra']
        ]
        
        for empresa in empresas_en_crisis:
            exito_rescate = self._intentar_rescate_empresarial(empresa)
            if exito_rescate:
                self.crisis_empresariales_resueltas += 1
                logging.info(f"Crisis empresarial resuelta para {empresa.nombre}")
    
    def _intentar_rescate_empresarial(self, empresa) -> bool:
        """Intenta rescatar una empresa en crisis"""
        if hasattr(self.mercado, 'rescate_empresarial_avanzado'):
            return self.mercado.rescate_empresarial_avanzado.evaluar_rescate(empresa)
        
        # Rescate básico si no hay sistema avanzado
        if empresa.dinero < 1000 and len(empresa.empleados) > 5:
            # Empresa sistemáticamente importante
            rescate = min(50000, empresa.costos_fijos_mensuales * 6)
            empresa.dinero += rescate
            self.empresas_rescatadas += 1
            return True
        
        return False
    
    def _facilitar_innovacion_continua(self):
        """Facilita procesos de innovación continua en las empresas"""
        for empresa in self.mercado.getEmpresas():
            if hasattr(empresa, 'laboratorio_id'):
                # Incentivar innovación según estado financiero
                estado = self.empresas_mejoradas.get(empresa.nombre, {}).get('estado_financiero', 'estable')
                
                if estado == 'prospero':
                    # Empresas prósperas pueden innovar más
                    empresa.laboratorio_id.aumentar_capacidad_investigacion(0.1)
                elif estado == 'crisis':
                    # Empresas en crisis se enfocan en innovación de supervivencia
                    empresa.laboratorio_id.priorizar_innovacion_supervivencia()
    
    def _gestionar_competencia_empresarial(self):
        """Gestiona la competencia empresarial intensificada"""
        # Identificar mercados altamente competitivos
        mercados_competitivos = {}
        
        for bien in self.mercado.bienes:
            empresas_competidoras = [
                e for e in self.mercado.getEmpresas()
                if bien in e.precios and len(e.bienes.get(bien, [])) > 0
            ]
            
            if len(empresas_competidoras) > 2:
                mercados_competitivos[bien] = empresas_competidoras
        
        # Intensificar competencia en mercados saturados
        for bien, empresas in mercados_competitivos.items():
            self._intensificar_competencia_mercado(bien, empresas)
    
    def _intensificar_competencia_mercado(self, bien: str, empresas: List):
        """Intensifica la competencia en un mercado específico"""
        for empresa in empresas:
            if hasattr(empresa, 'inteligencia_mercado'):
                # Empresas con inteligencia de mercado responden más agresivamente
                empresa.inteligencia_mercado.activar_modo_competencia_intensiva(bien)
            else:
                # Respuesta básica de competencia
                if random.random() < 0.3:  # 30% probabilidad
                    # Reducir precio para ser más competitivo
                    precio_actual = empresa.precios.get(bien, 0)
                    if precio_actual > 5:  # No reducir por debajo de 5
                        empresa.precios[bien] = precio_actual * random.uniform(0.95, 0.98)
    
    def _evaluar_fusiones_adquisiciones(self):
        """Evalúa oportunidades de fusiones y adquisiciones"""
        if hasattr(self.mercado, 'sistema_fusiones'):
            oportunidades = self.mercado.sistema_fusiones.identificar_oportunidades()
            
            for oportunidad in oportunidades[:2]:  # Máximo 2 fusiones por ciclo
                if self.mercado.sistema_fusiones.ejecutar_fusion(oportunidad):
                    self.fusiones_realizadas += 1
                    logging.info(f"Fusión ejecutada: {oportunidad}")
    
    def _actualizar_metricas_sistema(self):
        """Actualiza las métricas del sistema hiperrealista"""
        # Contar innovaciones exitosas
        self.innovaciones_exitosas = sum(
            getattr(empresa, 'innovaciones_exitosas', 0)
            for empresa in self.mercado.getEmpresas()
            if hasattr(empresa, 'innovaciones_exitosas')
        )
        
        # Actualizar estadísticas en el reporte del mercado
        if hasattr(self.mercado, 'reporte'):
            self.mercado.reporte.sistema_hiperrealista = {
                'empresas_mejoradas': len(self.empresas_mejoradas),
                'empresas_rescatadas': self.empresas_rescatadas,
                'fusiones_realizadas': self.fusiones_realizadas,
                'innovaciones_exitosas': self.innovaciones_exitosas,
                'crisis_resueltas': self.crisis_empresariales_resueltas
            }
    
    def obtener_estadisticas_sistema(self) -> Dict[str, Any]:
        """Retorna estadísticas completas del sistema hiperrealista"""
        # Calcular distribución de estados financieros
        distribucion_estados = {}
        for empresa_info in self.empresas_mejoradas.values():
            estado = empresa_info['estado_financiero']
            distribucion_estados[estado] = distribucion_estados.get(estado, 0) + 1
        
        return {
            'sistema_activo': self.sistema_activo,
            'empresas_totales_mejoradas': len(self.empresas_mejoradas),
            'distribucion_estados_financieros': distribucion_estados,
            'empresas_rescatadas_total': self.empresas_rescatadas,
            'fusiones_realizadas_total': self.fusiones_realizadas,
            'innovaciones_exitosas_total': self.innovaciones_exitosas,
            'crisis_empresariales_resueltas': self.crisis_empresariales_resueltas,
            'factor_competencia_actual': self.factor_competencia_intensidad
        }


class SistemaGestionRiesgos:
    """Sistema de gestión de riesgos empresariales"""
    
    def __init__(self, empresa):
        self.empresa = empresa
        self.nivel_riesgo_actual = 0.3
        self.protocolo_emergencia_activo = False
        self.medidas_riesgo = []
    
    def ciclo_gestion_riesgos(self):
        """Ejecuta ciclo de gestión de riesgos"""
        self._evaluar_riesgos_actuales()
        self._aplicar_medidas_mitigacion()
        self._actualizar_nivel_riesgo()
    
    def _evaluar_riesgos_actuales(self):
        """Evalúa riesgos financieros, operativos y de mercado"""
        # Riesgo financiero
        ratio_liquidez = self.empresa.dinero / max(getattr(self.empresa, 'costos_fijos_mensuales', 1000), 1)
        riesgo_financiero = max(0, 1 - ratio_liquidez / 5)
        
        # Riesgo operativo (basado en eficiencia)
        eficiencia = getattr(self.empresa, 'eficiencia_produccion', 0.8)
        riesgo_operativo = 1 - eficiencia
        
        # Riesgo de mercado (basado en competencia)
        riesgo_mercado = random.uniform(0.1, 0.4)
        
        self.nivel_riesgo_actual = (riesgo_financiero * 0.5 + riesgo_operativo * 0.3 + riesgo_mercado * 0.2)
    
    def _aplicar_medidas_mitigacion(self):
        """Aplica medidas de mitigación de riesgos"""
        if self.nivel_riesgo_actual > 0.7:
            self.activar_protocolo_emergencia()
        elif self.nivel_riesgo_actual > 0.5:
            self._aplicar_medidas_preventivas()
    
    def _aplicar_medidas_preventivas(self):
        """Aplica medidas preventivas de riesgo"""
        # Reducir costos no esenciales
        if hasattr(self.empresa, 'costos_fijos_mensuales'):
            self.empresa.costos_fijos_mensuales *= 0.98
        
        # Aumentar márgenes de seguridad
        for bien in self.empresa.precios:
            costo = self.empresa.costos_unitarios.get(bien, 10)
            margen_seguridad = costo * 0.1
            self.empresa.precios[bien] = max(self.empresa.precios[bien], costo + margen_seguridad)
    
    def activar_protocolo_emergencia(self):
        """Activa protocolo de emergencia empresarial"""
        if not self.protocolo_emergencia_activo:
            self.protocolo_emergencia_activo = True
            
            # Medidas de emergencia
            # 1. Reducir costos operativos drásticamente
            if hasattr(self.empresa, 'costos_fijos_mensuales'):
                self.empresa.costos_fijos_mensuales *= 0.8
            
            # 2. Liquidar inventario excesivo
            self._liquidar_inventario_exceso()
            
            # 3. Buscar financiamiento de emergencia
            self._buscar_financiamiento_emergencia()
    
    def _liquidar_inventario_exceso(self):
        """Liquida inventario excesivo para generar efectivo"""
        for bien, inventario in self.empresa.bienes.items():
            if isinstance(inventario, list) and len(inventario) > 10:
                # Liquidar 30% del exceso de inventario
                cantidad_liquidar = min(len(inventario) // 3, 5)
                precio_liquidacion = self.empresa.precios.get(bien, 10) * 0.8
                
                for _ in range(cantidad_liquidar):
                    if inventario:
                        inventario.pop()
                        self.empresa.dinero += precio_liquidacion
    
    def _buscar_financiamiento_emergencia(self):
        """Busca financiamiento de emergencia"""
        if hasattr(self.empresa.mercado, 'sistema_bancario'):
            # Intentar préstamo de emergencia
            bancos = self.empresa.mercado.sistema_bancario.bancos
            for banco in bancos:
                monto_necesario = getattr(self.empresa, 'costos_fijos_mensuales', 5000) * 3
                try:
                    resultado = banco.otorgar_prestamo(self.empresa, monto_necesario, self.empresa.dinero + 1000)
                    if isinstance(resultado, tuple) and resultado[0]:
                        break
                except:
                    continue
    
    def _actualizar_nivel_riesgo(self):
        """Actualiza nivel de riesgo después de medidas"""
        if self.protocolo_emergencia_activo and self.nivel_riesgo_actual < 0.4:
            self.protocolo_emergencia_activo = False


class CadenasuministroOptimizada:
    """Sistema de optimización de cadena de suministro"""
    
    def __init__(self, empresa):
        self.empresa = empresa
        self.proveedores = {}
        self.eficiencia_cadena = 0.8
        self.costos_logisticos = {}
    
    def optimizar_cadena(self):
        """Optimiza la cadena de suministro"""
        self._evaluar_proveedores()
        self._optimizar_inventarios()
        self._reducir_costos_logisticos()
    
    def _evaluar_proveedores(self):
        """Evalúa y optimiza relaciones con proveedores"""
        # Simulación de evaluación de proveedores
        for bien in self.empresa.costos_unitarios:
            if random.random() < 0.1:  # 10% probabilidad de encontrar mejor proveedor
                reduccion_costo = random.uniform(0.02, 0.08)
                self.empresa.costos_unitarios[bien] *= (1 - reduccion_costo)
    
    def _optimizar_inventarios(self):
        """Optimiza niveles de inventario"""
        for bien, inventario in self.empresa.bienes.items():
            if isinstance(inventario, list):
                stock_actual = len(inventario)
                stock_optimo = self._calcular_stock_optimo(bien)
                
                if stock_actual > stock_optimo * 1.5:
                    # Reducir producción futura
                    if hasattr(self.empresa, 'capacidad_produccion'):
                        self.empresa.capacidad_produccion[bien] = int(
                            self.empresa.capacidad_produccion.get(bien, 10) * 0.95
                        )
    
    def _calcular_stock_optimo(self, bien: str) -> int:
        """Calcula el stock óptimo para un bien"""
        # Demanda histórica simulada
        demanda_base = 10
        return max(5, int(demanda_base * 1.2))  # 20% buffer
    
    def _reducir_costos_logisticos(self):
        """Reduce costos logísticos mediante optimización"""
        if random.random() < 0.2:  # 20% probabilidad de mejora
            # Mejora en eficiencia logística
            self.eficiencia_cadena = min(1.0, self.eficiencia_cadena * 1.02)
            
            # Aplicar eficiencia a costos de producción
            for bien in self.empresa.costos_unitarios:
                self.empresa.costos_unitarios[bien] *= (2 - self.eficiencia_cadena)


class LaboratorioID:
    """Laboratorio de Investigación y Desarrollo empresarial"""
    
    def __init__(self, empresa):
        self.empresa = empresa
        self.proyectos_activos = []
        self.presupuesto_id = 0
        self.capacidad_investigacion = 1.0
    
    def ciclo_investigacion(self):
        """Ejecuta ciclo de investigación y desarrollo"""
        self._asignar_presupuesto_id()
        self._gestionar_proyectos_activos()
        self._evaluar_nuevos_proyectos()
    
    def _asignar_presupuesto_id(self):
        """Asigna presupuesto para I+D"""
        # 3-8% de ingresos para I+D
        porcentaje_id = random.uniform(0.03, 0.08)
        self.presupuesto_id = self.empresa.dinero * porcentaje_id
    
    def _gestionar_proyectos_activos(self):
        """Gestiona proyectos de I+D activos"""
        for proyecto in self.proyectos_activos[:]:
            proyecto['progreso'] += random.uniform(0.1, 0.3) * self.capacidad_investigacion
            
            if proyecto['progreso'] >= 1.0:
                self._completar_proyecto(proyecto)
                self.proyectos_activos.remove(proyecto)
    
    def _completar_proyecto(self, proyecto):
        """Completa un proyecto de I+D"""
        tipo_innovacion = proyecto['tipo']
        
        if tipo_innovacion == 'reduccion_costos':
            # Reducir costos de producción
            bien = proyecto['bien_objetivo']
            if bien in self.empresa.costos_unitarios:
                reduccion = proyecto['impacto_esperado']
                self.empresa.costos_unitarios[bien] *= (1 - reduccion)
        
        elif tipo_innovacion == 'mejora_calidad':
            # Mejorar calidad del producto
            bien = proyecto['bien_objetivo']
            if hasattr(self.empresa, 'productos_ia') and bien in self.empresa.productos_ia:
                self.empresa.productos_ia[bien].calidad += proyecto['impacto_esperado']
        
        elif tipo_innovacion == 'nuevo_producto':
            # Desarrollar nuevo producto
            self._lanzar_nuevo_producto(proyecto)
        
        # Incrementar contador de innovaciones
        if not hasattr(self.empresa, 'innovaciones_exitosas'):
            self.empresa.innovaciones_exitosas = 0
        self.empresa.innovaciones_exitosas += 1
    
    def _lanzar_nuevo_producto(self, proyecto):
        """Lanza un nuevo producto al mercado"""
        nuevo_bien = f"producto_innovador_{len(self.empresa.bienes) + 1}"
        
        # Agregar al inventario de la empresa
        self.empresa.bienes[nuevo_bien] = []
        
        # Establecer precio y costo
        costo_base = random.uniform(15, 30)
        self.empresa.costos_unitarios[nuevo_bien] = costo_base
        self.empresa.precios[nuevo_bien] = costo_base * random.uniform(1.5, 2.5)
        
        # Agregar capacidad de producción si es empresa productora
        if hasattr(self.empresa, 'capacidad_produccion'):
            self.empresa.capacidad_produccion[nuevo_bien] = random.randint(5, 15)
    
    def _evaluar_nuevos_proyectos(self):
        """Evalúa oportunidades de nuevos proyectos I+D"""
        if len(self.proyectos_activos) < 3 and self.presupuesto_id > 5000:
            if random.random() < 0.3:  # 30% probabilidad
                self._iniciar_nuevo_proyecto()
    
    def _iniciar_nuevo_proyecto(self):
        """Inicia un nuevo proyecto de I+D"""
        tipos_proyecto = ['reduccion_costos', 'mejora_calidad', 'nuevo_producto']
        tipo = random.choice(tipos_proyecto)
        
        proyecto = {
            'tipo': tipo,
            'bien_objetivo': random.choice(list(self.empresa.bienes.keys())),
            'progreso': 0.0,
            'costo_total': random.uniform(3000, 15000),
            'impacto_esperado': random.uniform(0.05, 0.20),
            'duracion_estimada': random.randint(3, 8)
        }
        
        self.proyectos_activos.append(proyecto)
    
    def aumentar_capacidad_investigacion(self, factor: float):
        """Aumenta la capacidad de investigación"""
        self.capacidad_investigacion = min(2.0, self.capacidad_investigacion * (1 + factor))
    
    def priorizar_innovacion_supervivencia(self):
        """Prioriza innovaciones críticas para supervivencia"""
        # Enfocar en reducción de costos para empresas en crisis
        for proyecto in self.proyectos_activos:
            if proyecto['tipo'] != 'reduccion_costos':
                proyecto['tipo'] = 'reduccion_costos'
                proyecto['impacto_esperado'] *= 1.5  # Mayor impacto


class GestionRecursosHumanos:
    """Sistema avanzado de gestión de recursos humanos"""
    
    def __init__(self, empresa):
        self.empresa = empresa
        self.productividad_empleados = {}
        self.programa_capacitacion = False
        self.satisfaccion_laboral = 0.7
    
    def ciclo_recursos_humanos(self):
        """Ejecuta ciclo de gestión de RRHH"""
        self._evaluar_productividad()
        self._gestionar_capacitacion()
        self._optimizar_contratacion()
        self._mantener_satisfaccion_laboral()
    
    def _evaluar_productividad(self):
        """Evalúa productividad de empleados"""
        for empleado in self.empresa.empleados:
            if empleado not in self.productividad_empleados:
                self.productividad_empleados[empleado] = random.uniform(0.7, 1.2)
            
            # La productividad puede variar
            variacion = random.uniform(-0.05, 0.05)
            self.productividad_empleados[empleado] += variacion
            self.productividad_empleados[empleado] = max(0.5, min(1.5, self.productividad_empleados[empleado]))
    
    def _gestionar_capacitacion(self):
        """Gestiona programas de capacitación"""
        if self.empresa.dinero > 20000 and not self.programa_capacitacion:
            if random.random() < 0.2:  # 20% probabilidad
                self.programa_capacitacion = True
                costo_capacitacion = len(self.empresa.empleados) * 500
                self.empresa.dinero -= costo_capacitacion
                
                # Mejorar productividad de empleados
                for empleado in self.productividad_empleados:
                    self.productividad_empleados[empleado] *= 1.1
    
    def _optimizar_contratacion(self):
        """Optimiza procesos de contratación"""
        # Evaluar necesidades de personal basadas en productividad
        productividad_promedio = sum(self.productividad_empleados.values()) / max(len(self.productividad_empleados), 1)
        
        if productividad_promedio < 0.8 and len(self.empresa.empleados) < self.empresa.capacidad_empleo:
            # Necesita contratar personal más productivo
            if hasattr(self.empresa.mercado, 'mercado_laboral'):
                self.empresa.mercado.mercado_laboral.priorizar_empresa_contratacion(self.empresa)
    
    def _mantener_satisfaccion_laboral(self):
        """Mantiene niveles adecuados de satisfacción laboral"""
        # La satisfacción afecta la productividad
        if self.satisfaccion_laboral < 0.6:
            # Implementar mejoras laborales
            if self.empresa.dinero > 10000:
                inversion_bienestar = len(self.empresa.empleados) * 200
                self.empresa.dinero -= inversion_bienestar
                self.satisfaccion_laboral += 0.1
        
        # Aplicar efectos de satisfacción en productividad
        factor_satisfaccion = 0.5 + self.satisfaccion_laboral * 0.5
        for empleado in self.productividad_empleados:
            self.productividad_empleados[empleado] *= factor_satisfaccion


class InteligenciaMercado:
    """Sistema de inteligencia de mercado empresarial"""
    
    def __init__(self, empresa, mercado):
        self.empresa = empresa
        self.mercado = mercado
        self.inteligencia_competidores = {}
        self.tendencias_mercado = {}
        self.oportunidades_identificadas = []
    
    def actualizar_inteligencia(self):
        """Actualiza inteligencia de mercado"""
        self._analizar_competidores()
        self._identificar_tendencias()
        self._buscar_oportunidades()
    
    def _analizar_competidores(self):
        """Analiza comportamiento de competidores"""
        competidores = [e for e in self.mercado.getEmpresas() if e != self.empresa]
        
        for competidor in competidores:
            analisis = {
                'precios_promedio': sum(competidor.precios.values()) / max(len(competidor.precios), 1),
                'nivel_inventario': sum(len(inv) if isinstance(inv, list) else inv for inv in competidor.bienes.values()),
                'fortaleza_financiera': competidor.dinero,
                'ultima_actualizacion': self.mercado.ciclo_actual
            }
            
            self.inteligencia_competidores[competidor.nombre] = analisis
    
    def _identificar_tendencias(self):
        """Identifica tendencias del mercado"""
        # Analizar tendencias de precios
        for bien in self.mercado.precios_historicos:
            if len(self.mercado.precios_historicos[bien]) >= 3:
                precios_recientes = self.mercado.precios_historicos[bien][-3:]
                tendencia = (precios_recientes[-1] - precios_recientes[0]) / max(precios_recientes[0], 1)
                self.tendencias_mercado[bien] = tendencia
    
    def _buscar_oportunidades(self):
        """Busca oportunidades de mercado"""
        self.oportunidades_identificadas = []
        
        # Oportunidad 1: Bienes con alta demanda y pocos competidores
        for bien in self.mercado.bienes:
            competidores_bien = [e for e in self.mercado.getEmpresas() if bien in e.bienes and len(e.bienes[bien]) > 0]
            
            if len(competidores_bien) < 3 and bien not in self.empresa.bienes:
                self.oportunidades_identificadas.append({
                    'tipo': 'expansion_producto',
                    'bien': bien,
                    'competidores': len(competidores_bien),
                    'prioridad': 'alta' if len(competidores_bien) < 2 else 'media'
                })
        
        # Oportunidad 2: Nichos de precio
        for bien in self.empresa.bienes:
            if bien in self.tendencias_mercado and self.tendencias_mercado[bien] > 0.1:
                self.oportunidades_identificadas.append({
                    'tipo': 'ajuste_precio_alza',
                    'bien': bien,
                    'tendencia': self.tendencias_mercado[bien],
                    'prioridad': 'media'
                })
    
    def activar_modo_competencia_intensiva(self, bien: str):
        """Activa modo de competencia intensiva para un bien específico"""
        if bien in self.empresa.precios:
            # Analizar precios de competidores para ese bien
            precios_competidores = [
                e.precios.get(bien, float('inf'))
                for e in self.mercado.getEmpresas()
                if e != self.empresa and bien in e.precios
            ]
            
            if precios_competidores:
                precio_minimo_competencia = min(precios_competidores)
                precio_actual = self.empresa.precios[bien]
                
                # Ser 5% más barato que el competidor más barato
                if precio_actual > precio_minimo_competencia:
                    nuevo_precio = precio_minimo_competencia * 0.95
                    costo_unitario = self.empresa.costos_unitarios.get(bien, 1)
                    
                    # No vender por debajo del costo
                    if nuevo_precio > costo_unitario * 1.05:
                        self.empresa.precios[bien] = nuevo_precio


class GestionSostenibilidad:
    """Sistema de gestión de sostenibilidad empresarial"""
    
    def __init__(self, empresa):
        self.empresa = empresa
        self.nivel_sostenibilidad = random.uniform(0.3, 0.7)
        self.inversiones_verdes = 0
        self.certificaciones = []
    
    def ciclo_sostenibilidad(self):
        """Ejecuta ciclo de gestión de sostenibilidad"""
        self._evaluar_impacto_ambiental()
        self._implementar_mejoras_sostenibles()
        self._buscar_certificaciones()
    
    def _evaluar_impacto_ambiental(self):
        """Evalúa el impacto ambiental actual"""
        # El impacto depende del volumen de producción
        volumen_produccion = sum(getattr(self.empresa, 'produccion_actual', {}).values())
        
        # Factor de emisiones (menor es mejor)
        factor_emisiones = getattr(self.empresa, 'factor_emisiones', 1.0)
        impacto_total = volumen_produccion * factor_emisiones
        
        # Evaluar si necesita mejoras
        if impacto_total > 100 and self.nivel_sostenibilidad < 0.8:
            self._planificar_mejoras_ambientales()
    
    def _planificar_mejoras_ambientales(self):
        """Planifica mejoras ambientales"""
        if self.empresa.dinero > 15000:
            # Invertir en tecnología limpia
            inversion = min(self.empresa.dinero * 0.1, 20000)
            self.empresa.dinero -= inversion
            self.inversiones_verdes += inversion
            
            # Mejorar factor de emisiones
            if hasattr(self.empresa, 'factor_emisiones'):
                mejora = inversion / 50000  # Factor de conversión
                self.empresa.factor_emisiones = max(0.1, self.empresa.factor_emisiones - mejora)
            
            # Aumentar nivel de sostenibilidad
            self.nivel_sostenibilidad = min(1.0, self.nivel_sostenibilidad + 0.1)
    
    def _implementar_mejoras_sostenibles(self):
        """Implementa mejoras sostenibles operativas"""
        if random.random() < 0.1:  # 10% probabilidad
            # Optimización de recursos
            for bien in self.empresa.costos_unitarios:
                # Reducir desperdicio = menor costo
                if self.nivel_sostenibilidad > 0.7:
                    self.empresa.costos_unitarios[bien] *= 0.98
    
    def _buscar_certificaciones(self):
        """Busca certificaciones de sostenibilidad"""
        if self.nivel_sostenibilidad > 0.8 and 'iso_14001' not in self.certificaciones:
            if random.random() < 0.05:  # 5% probabilidad
                self.certificaciones.append('iso_14001')
                # Beneficio en reputación (simulado como precio premium)
                for bien in self.empresa.precios:
                    self.empresa.precios[bien] *= 1.05


# Sistemas de apoyo adicionales

class SistemaRescateAvanzado:
    """Sistema avanzado de rescate empresarial"""
    
    def __init__(self, mercado):
        self.mercado = mercado
        self.criterios_rescate = {
            'empleados_minimos': 10,
            'impacto_economico': 0.05,  # 5% del PIB
            'sector_estrategico': True
        }
    
    def evaluar_rescate(self, empresa) -> bool:
        """Evalúa si una empresa califica para rescate"""
        # Criterio 1: Número de empleados
        if len(empresa.empleados) >= self.criterios_rescate['empleados_minimos']:
            return self._ejecutar_rescate(empresa, 'importancia_laboral')
        
        # Criterio 2: Impacto económico
        pib_actual = self.mercado.calcular_pib_total()
        impacto_empresa = empresa.dinero / max(pib_actual, 1)
        if impacto_empresa >= self.criterios_rescate['impacto_economico']:
            return self._ejecutar_rescate(empresa, 'impacto_sistemico')
        
        # Criterio 3: Sector estratégico (simplificado)
        if hasattr(empresa, 'sector') and empresa.sector in ['alimentos', 'energia', 'salud']:
            return self._ejecutar_rescate(empresa, 'sector_estrategico')
        
        return False
    
    def _ejecutar_rescate(self, empresa, motivo: str) -> bool:
        """Ejecuta el rescate empresarial"""
        # Calcular monto de rescate
        monto_rescate = self._calcular_monto_rescate(empresa, motivo)
        
        if monto_rescate > 0:
            empresa.dinero += monto_rescate
            
            # Aplicar condiciones del rescate
            self._aplicar_condiciones_rescate(empresa)
            
            logging.info(f"Rescate ejecutado para {empresa.nombre}: ${monto_rescate:,.2f} por {motivo}")
            return True
        
        return False
    
    def _calcular_monto_rescate(self, empresa, motivo: str) -> float:
        """Calcula el monto del rescate"""
        if motivo == 'importancia_laboral':
            return len(empresa.empleados) * 2000  # $2000 por empleado
        elif motivo == 'impacto_sistemico':
            return min(100000, empresa.dinero * 0.5)  # Hasta 50% del capital o $100K
        elif motivo == 'sector_estrategico':
            costos_operativos = getattr(empresa, 'costos_fijos_mensuales', 5000)
            return costos_operativos * 6  # 6 meses de operación
        
        return 0
    
    def _aplicar_condiciones_rescate(self, empresa):
        """Aplica condiciones post-rescate"""
        # Reducir costos operativos por 3 ciclos
        if hasattr(empresa, 'costos_fijos_mensuales'):
            empresa.costos_fijos_mensuales *= 0.85
        
        # Limitar dividendos si es empresa que emite acciones
        if hasattr(empresa, 'valor_accion'):
            empresa.rescate_activo = 3  # 3 ciclos de restricciones


class SistemaFusionesAdquisiciones:
    """Sistema de fusiones y adquisiciones"""
    
    def __init__(self, mercado):
        self.mercado = mercado
        self.fusiones_completadas = []
    
    def identificar_oportunidades(self) -> List[Dict]:
        """Identifica oportunidades de fusiones"""
        empresas = self.mercado.getEmpresas()
        oportunidades = []
        
        for i, empresa1 in enumerate(empresas):
            for empresa2 in empresas[i+1:]:
                sinergia = self._evaluar_sinergia(empresa1, empresa2)
                
                if sinergia > 0.6:  # Umbral de sinergia
                    oportunidades.append({
                        'empresa_adquirente': empresa1.nombre,
                        'empresa_objetivo': empresa2.nombre,
                        'sinergia': sinergia,
                        'tipo': self._determinar_tipo_fusion(empresa1, empresa2)
                    })
        
        return sorted(oportunidades, key=lambda x: x['sinergia'], reverse=True)[:3]
    
    def _evaluar_sinergia(self, empresa1, empresa2) -> float:
        """Evalúa sinergia potencial entre dos empresas"""
        sinergia = 0.0
        
        # Sinergia por productos complementarios
        productos_comunes = set(empresa1.bienes.keys()) & set(empresa2.bienes.keys())
        sinergia += len(productos_comunes) * 0.1
        
        # Sinergia por fortaleza financiera complementaria
        if empresa1.dinero > empresa2.dinero * 2:
            sinergia += 0.3  # Empresa fuerte puede rescatar débil
        
        # Sinergia por recursos humanos
        if len(empresa1.empleados) + len(empresa2.empleados) < max(empresa1.capacidad_empleo, empresa2.capacidad_empleo):
            sinergia += 0.2  # No hay sobreempleo
        
        # Sinergia por eficiencia operativa
        if hasattr(empresa1, 'eficiencia_produccion') and hasattr(empresa2, 'eficiencia_produccion'):
            eficiencia_promedio = (empresa1.eficiencia_produccion + empresa2.eficiencia_produccion) / 2
            if eficiencia_promedio > 0.8:
                sinergia += 0.2
        
        return min(1.0, sinergia)
    
    def _determinar_tipo_fusion(self, empresa1, empresa2) -> str:
        """Determina el tipo de fusión"""
        # Fusión horizontal: mismos productos
        productos_comunes = set(empresa1.bienes.keys()) & set(empresa2.bienes.keys())
        if len(productos_comunes) > len(empresa1.bienes) * 0.5:
            return 'horizontal'
        
        # Fusión vertical: cadena de suministro
        # (simplificado: empresas de diferentes tamaños)
        if abs(len(empresa1.empleados) - len(empresa2.empleados)) > 10:
            return 'vertical'
        
        return 'conglomerado'
    
    def ejecutar_fusion(self, oportunidad: Dict) -> bool:
        """Ejecuta una fusión específica"""
        empresa_adquirente = self._buscar_empresa_por_nombre(oportunidad['empresa_adquirente'])
        empresa_objetivo = self._buscar_empresa_por_nombre(oportunidad['empresa_objetivo'])
        
        if not empresa_adquirente or not empresa_objetivo:
            return False
        
        # Verificar capacidad financiera
        valor_objetivo = empresa_objetivo.dinero * 1.2  # Prima de 20%
        if empresa_adquirente.dinero < valor_objetivo:
            return False
        
        # Ejecutar la fusión
        self._transferir_activos(empresa_adquirente, empresa_objetivo)
        self._integrar_operaciones(empresa_adquirente, empresa_objetivo)
        self._remover_empresa_objetivo(empresa_objetivo)
        
        self.fusiones_completadas.append({
            'adquirente': oportunidad['empresa_adquirente'],
            'objetivo': oportunidad['empresa_objetivo'],
            'tipo': oportunidad['tipo'],
            'ciclo': self.mercado.ciclo_actual
        })
        
        return True
    
    def _buscar_empresa_por_nombre(self, nombre: str):
        """Busca empresa por nombre"""
        for empresa in self.mercado.getEmpresas():
            if empresa.nombre == nombre:
                return empresa
        return None
    
    def _transferir_activos(self, adquirente, objetivo):
        """Transfiere activos de empresa objetivo a adquirente"""
        # Transferir dinero (descontando prima)
        prima = objetivo.dinero * 0.2
        adquirente.dinero -= (objetivo.dinero + prima)
        adquirente.dinero += objetivo.dinero
        
        # Transferir inventarios
        for bien, inventario in objetivo.bienes.items():
            if bien not in adquirente.bienes:
                adquirente.bienes[bien] = []
            if isinstance(inventario, list):
                adquirente.bienes[bien].extend(inventario)
            else:
                adquirente.bienes[bien] = adquirente.bienes.get(bien, 0) + inventario
        
        # Transferir empleados
        adquirente.empleados.extend(objetivo.empleados)
        adquirente.capacidad_empleo += objetivo.capacidad_empleo
        
        # Transferir capacidades de producción
        if hasattr(objetivo, 'capacidad_produccion'):
            for bien, capacidad in objetivo.capacidad_produccion.items():
                if bien in adquirente.capacidad_produccion:
                    adquirente.capacidad_produccion[bien] += capacidad
                else:
                    adquirente.capacidad_produccion[bien] = capacidad
    
    def _integrar_operaciones(self, adquirente, objetivo):
        """Integra operaciones de ambas empresas"""
        # Integrar precios (tomar el más competitivo)
        for bien in objetivo.precios:
            if bien in adquirente.precios:
                # Tomar el menor precio para ser más competitivo
                adquirente.precios[bien] = min(adquirente.precios[bien], objetivo.precios[bien])
            else:
                adquirente.precios[bien] = objetivo.precios[bien]
        
        # Integrar costos (tomar el más eficiente)
        for bien in objetivo.costos_unitarios:
            if bien in adquirente.costos_unitarios:
                # Promedio ponderado de costos
                adquirente.costos_unitarios[bien] = (
                    adquirente.costos_unitarios[bien] * 0.7 + objetivo.costos_unitarios[bien] * 0.3
                )
            else:
                adquirente.costos_unitarios[bien] = objetivo.costos_unitarios[bien]
        
        # Beneficios de sinergia
        if hasattr(adquirente, 'eficiencia_produccion'):
            adquirente.eficiencia_produccion = min(1.2, adquirente.eficiencia_produccion * 1.1)
    
    def _remover_empresa_objetivo(self, empresa_objetivo):
        """Remueve la empresa objetivo del mercado"""
        if empresa_objetivo in self.mercado.personas:
            self.mercado.personas.remove(empresa_objetivo)


class ObservatorioEmpresarial:
    """Observatorio para monitoreo del ecosistema empresarial"""
    
    def __init__(self, mercado):
        self.mercado = mercado
        self.metricas_ecosistema = {}
        self.alertas_activas = []
    
    def monitorear_ecosistema(self):
        """Monitorea el ecosistema empresarial completo"""
        self._calcular_metricas_ecosistema()
        self._detectar_alertas_sistema()
        self._generar_recomendaciones()
    
    def _calcular_metricas_ecosistema(self):
        """Calcula métricas clave del ecosistema"""
        empresas = self.mercado.getEmpresas()
        
        if not empresas:
            return
        
        # Distribución de tamaños empresariales
        tamaños = [len(e.empleados) for e in empresas]
        self.metricas_ecosistema['empresas_pequeñas'] = sum(1 for t in tamaños if t <= 5)
        self.metricas_ecosistema['empresas_medianas'] = sum(1 for t in tamaños if 5 < t <= 20)
        self.metricas_ecosistema['empresas_grandes'] = sum(1 for t in tamaños if t > 20)
        
        # Concentración de mercado
        capitals = [e.dinero for e in empresas]
        capital_total = sum(capitals)
        if capital_total > 0:
            # Índice de concentración (% del capital en top 3 empresas)
            capitals_sorted = sorted(capitals, reverse=True)
            top3_capital = sum(capitals_sorted[:3])
            self.metricas_ecosistema['concentracion_capital'] = top3_capital / capital_total
        
        # Nivel de innovación
        innovaciones_total = sum(getattr(e, 'innovaciones_exitosas', 0) for e in empresas)
        self.metricas_ecosistema['innovaciones_por_empresa'] = innovaciones_total / len(empresas)
        
        # Nivel de sostenibilidad promedio
        sostenibilidad_total = sum(
            getattr(e.gestion_sostenibilidad, 'nivel_sostenibilidad', 0.5)
            for e in empresas if hasattr(e, 'gestion_sostenibilidad')
        )
        empresas_con_sostenibilidad = sum(1 for e in empresas if hasattr(e, 'gestion_sostenibilidad'))
        if empresas_con_sostenibilidad > 0:
            self.metricas_ecosistema['sostenibilidad_promedio'] = sostenibilidad_total / empresas_con_sostenibilidad
    
    def _detectar_alertas_sistema(self):
        """Detecta alertas del sistema empresarial"""
        self.alertas_activas = []
        
        # Alerta: Alta concentración de capital
        if self.metricas_ecosistema.get('concentracion_capital', 0) > 0.7:
            self.alertas_activas.append({
                'tipo': 'concentracion_excesiva',
                'descripcion': 'Alta concentración de capital empresarial',
                'nivel': 'medio'
            })
        
        # Alerta: Baja innovación
        if self.metricas_ecosistema.get('innovaciones_por_empresa', 0) < 0.1:
            self.alertas_activas.append({
                'tipo': 'baja_innovacion',
                'descripcion': 'Nivel de innovación por debajo del óptimo',
                'nivel': 'alto'
            })
        
        # Alerta: Muchas empresas pequeñas (posible fragmentación)
        total_empresas = sum([
            self.metricas_ecosistema.get('empresas_pequeñas', 0),
            self.metricas_ecosistema.get('empresas_medianas', 0),
            self.metricas_ecosistema.get('empresas_grandes', 0)
        ])
        
        if total_empresas > 0:
            ratio_pequeñas = self.metricas_ecosistema.get('empresas_pequeñas', 0) / total_empresas
            if ratio_pequeñas > 0.8:
                self.alertas_activas.append({
                    'tipo': 'fragmentacion_mercado',
                    'descripcion': 'Exceso de empresas pequeñas puede indicar fragmentación',
                    'nivel': 'bajo'
                })
    
    def _generar_recomendaciones(self):
        """Genera recomendaciones basadas en el análisis"""
        recomendaciones = []
        
        for alerta in self.alertas_activas:
            if alerta['tipo'] == 'concentracion_excesiva':
                recomendaciones.append("Considerar políticas antimonopolio")
            elif alerta['tipo'] == 'baja_innovacion':
                recomendaciones.append("Incentivar inversión en I+D empresarial")
            elif alerta['tipo'] == 'fragmentacion_mercado':
                recomendaciones.append("Facilitar fusiones de empresas pequeñas")
        
        self.metricas_ecosistema['recomendaciones'] = recomendaciones
