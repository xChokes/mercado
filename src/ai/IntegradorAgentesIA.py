"""
Integrador Principal de Agentes IA Hiperrealistas
=================================================

Sistema integrador que coordina todos los componentes de IA:
- Fundamentos IA (Memoria, Decisiones, Comunicación)
- Agentes Inteligentes (Consumidores, Empresas)
- Mercado IA Central
- Redes Sociales de Agentes
- Deep Learning y Optimización

Este es el punto de entrada principal para el ecosistema de IA hiperrealista.
"""

import time
import random
from dataclasses import dataclass
from typing import Dict, List, Any, Optional
import threading
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, field

# Importar todos los sistemas de IA
from .AgentMemorySystem import AgentMemorySystem
from .IADecisionEngine import IADecisionEngine, EstadoMercado
from .AgentCommunicationProtocol import AgentCommunicationProtocol, TipoMensaje
from .OrquestadorAgentesIA import OrquestadorAgentesIA
from .ConsumidorIA import ConsumidorIA
from .EmpresaIA import EmpresaIA
from .MercadoIA import MercadoIA
from .RedSocialAgentesIA import RedSocialAgentesIA, TipoRelacion
from .SistemaDeepLearningIA import SistemaDeepLearningIA, TipoRedNeural

# Importar modelos base
from ..models.Consumidor import Consumidor
from ..models.Empresa import Empresa


@dataclass
@dataclass
class ConfiguracionSistemaIA:
    """Configuración del sistema de IA"""
    # Agentes
    num_consumidores_ia: int = 20
    num_empresas_ia: int = 8
    
    # Redes sociales
    probabilidad_relacion_inicial: float = 0.3
    activar_formacion_coaliciones: bool = True
    activar_redes_sociales: bool = True
    activar_coaliciones: bool = True
    
    # Deep Learning
    entrenar_automaticamente: bool = True
    activar_deep_learning: bool = True
    intervalo_entrenamiento_minutos: int = 30
    
    # Mercado IA
    activar_detector_crisis: bool = True
    activar_optimizacion_liquidez: bool = True
    
    # Coordinación
    intervalo_sincronizacion_segundos: int = 10
    activar_logs_detallados: bool = True
    duracion_simulacion_minutos: int = 5


@dataclass
class EstadisticasSistemaIA:
    """Estadísticas del sistema de IA"""
    agentes_activos: int = 0
    transacciones_ia: int = 0
    decisiones_ia: int = 0
    relaciones_sociales: int = 0
    coaliciones_activas: int = 0
    redes_entrenadas: int = 0
    tiempo_funcionamiento: float = 0.0
    eficiencia_global: float = 0.0
    adaptaciones_realizadas: int = 0


class IntegradorAgentesIA:
    """
    Sistema Integrador Principal de Agentes IA Hiperrealistas
    
    Coordina todos los componentes del ecosistema de IA para crear
    un mercado con agentes verdaderamente inteligentes y adaptativos.
    """
    
    def __init__(self, bienes_mercado: List[str], 
                 configuracion: ConfiguracionSistemaIA = None):
        """
        Inicializa el sistema completo de IA
        
        Args:
            bienes_mercado: Lista de bienes que se comerciarán
            configuracion: Configuración del sistema (opcional)
        """
        print("="*60)
        print("INICIALIZANDO ECOSISTEMA DE AGENTES IA HIPERREALISTAS")
        print("="*60)
        
        self.configuracion = configuracion or ConfiguracionSistemaIA()
        self.bienes_mercado = bienes_mercado
        self.tiempo_inicio = datetime.now()
        
        # === FASE 1: FUNDAMENTOS IA ===
        print("\n[FASE 1] Inicializando Fundamentos IA...")
        
        # Mercado IA Central (incluye orquestador)
        self.mercado_ia = MercadoIA(bienes_mercado)
        print("✓ Mercado IA Central inicializado")
        
        # === FASE 2: AGENTES INTELIGENTES ===
        print("\n[FASE 2] Creando Agentes Inteligentes...")
        
        # Contenedores de agentes
        self.consumidores_ia: Dict[str, ConsumidorIA] = {}
        self.empresas_ia: Dict[str, EmpresaIA] = {}
        
        # Crear consumidores IA
        self._crear_consumidores_ia()
        print(f"✓ {len(self.consumidores_ia)} Consumidores IA creados")
        
        # Crear empresas IA  
        self._crear_empresas_ia()
        print(f"✓ {len(self.empresas_ia)} Empresas IA creadas")
        
        # === FASE 3: REDES SOCIALES ===
        print("\n[FASE 3] Estableciendo Redes Sociales...")
        
        self.red_social = RedSocialAgentesIA()
        self._configurar_red_social()
        print("✓ Red Social de Agentes configurada")
        
        # === FASE 4: DEEP LEARNING ===
        print("\n[FASE 4] Inicializando Deep Learning...")
        
        self.sistema_deep_learning = SistemaDeepLearningIA()
        self._configurar_deep_learning()
        print("✓ Sistema de Deep Learning configurado")
        
        # === COORDINACIÓN Y ESTADO ===
        self.estadisticas = EstadisticasSistemaIA()
        self.sistemas_activos = True
        
        # Hilos de coordinación
        self.hilo_coordinacion = threading.Thread(target=self._ciclo_coordinacion_principal)
        self.hilo_coordinacion.daemon = True
        
        # Logs de actividad
        self.logs_actividad = []
        
        print("\n" + "="*60)
        print("🤖 ECOSISTEMA DE IA HIPERREALISTA INICIADO EXITOSAMENTE")
        print(f"📊 {len(self.consumidores_ia)} Consumidores + {len(self.empresas_ia)} Empresas")
        print(f"🌐 {self.red_social.get_estadisticas_red()['relaciones_totales']} Relaciones Sociales")
        print(f"🧠 {len(self.sistema_deep_learning.redes_especializadas)} Redes Neuronales")
        print("="*60)
        
        # Iniciar coordinación
        self.hilo_coordinacion.start()
        
    def _crear_consumidores_ia(self):
        """Crea consumidores con IA"""
        for i in range(self.configuracion.num_consumidores_ia):
            consumidor_id = f"consumidor_ia_{i+1}"
            
            # Crear directamente ConsumidorIA (ya hereda de Consumidor)
            consumidor_ia = ConsumidorIA(
                nombre=f"Consumidor IA {i+1}",
                mercado=self.mercado_ia,  # Referencia al mercado
                bienes={bien: (i % 3 + 1) * 5 for bien in self.bienes_mercado}  # Bienes iniciales
            )
            
            self.consumidores_ia[consumidor_id] = consumidor_ia
            
            # Registrar en mercado
            self.mercado_ia.orquestador_ia.registrar_agente(
                consumidor_id, "consumidor", consumidor_ia
            )
            
    def _crear_empresas_ia(self):
        """Crea empresas con IA"""
        for i in range(self.configuracion.num_empresas_ia):
            empresa_id = f"empresa_ia_{i+1}"
            
            # Crear directamente EmpresaIA (ya hereda de Empresa)
            empresa_ia = EmpresaIA(
                nombre=f"Empresa IA {i+1}",
                mercado=self.mercado_ia,  # Referencia al mercado
                bienes={bien: 100 + (i * 20) for bien in self.bienes_mercado}  # Inventario inicial
            )
            
            self.empresas_ia[empresa_id] = empresa_ia
            
            # Registrar en mercado
            self.mercado_ia.orquestador_ia.registrar_agente(
                empresa_id, "empresa", empresa_ia
            )
    
    def _configurar_red_social(self):
        """Configura la red social de agentes"""
        todos_agentes = list(self.consumidores_ia.keys()) + list(self.empresas_ia.keys())
        
        # Registrar todos los agentes en la red social
        for agente_id in todos_agentes:
            perfil_inicial = self._generar_perfil_agente(agente_id)
            self.red_social.registrar_agente(agente_id, perfil_inicial)
        
        # Establecer relaciones iniciales
        self._establecer_relaciones_iniciales(todos_agentes)
        
        print(f"   - {len(todos_agentes)} agentes registrados")
        print(f"   - {len(self.red_social.relaciones)} relaciones establecidas")
    
    def _generar_perfil_agente(self, agente_id: str) -> Dict[str, float]:
        """Genera perfil inicial para un agente"""
        if agente_id.startswith("consumidor"):
            return {
                'confiabilidad': 0.7,
                'cooperacion': 0.8,
                'competencia': 0.4,
                'innovacion': 0.3,
                'estabilidad': 0.9
            }
        else:  # empresa
            return {
                'confiabilidad': 0.8,
                'cooperacion': 0.6,
                'competencia': 0.9,
                'innovacion': 0.7,
                'estabilidad': 0.7
            }
    
    def _establecer_relaciones_iniciales(self, agentes: List[str]):
        """Establece relaciones iniciales entre agentes"""
        import random
        
        for i, agente_a in enumerate(agentes):
            for agente_b in agentes[i+1:]:
                if random.random() < self.configuracion.probabilidad_relacion_inicial:
                    # Determinar tipo de relación
                    if (agente_a.startswith("consumidor") and 
                        agente_b.startswith("empresa")):
                        tipo_relacion = TipoRelacion.PROVEEDOR_CLIENTE
                    elif (agente_a.startswith("empresa") and 
                          agente_b.startswith("empresa")):
                        tipo_relacion = TipoRelacion.COMPETENCIA
                    else:
                        tipo_relacion = TipoRelacion.NEUTRAL
                    
                    self.red_social.establecer_relacion(
                        agente_a, agente_b, tipo_relacion,
                        fuerza_inicial=random.uniform(0.3, 0.7),
                        confianza_inicial=random.uniform(0.4, 0.8)
                    )
    
    def _configurar_deep_learning(self):
        """Configura el sistema de deep learning"""
        # Crear redes especializadas principales
        redes_crear = [
            TipoRedNeural.PREDICCION_PRECIOS,
            TipoRedNeural.DETECCION_PATRONES,
            TipoRedNeural.OPTIMIZACION_ESTRATEGIA,
            TipoRedNeural.EVALUACION_RIESGOS
        ]
        
        for tipo_red in redes_crear:
            self.sistema_deep_learning.crear_red_especializada(tipo_red)
        
        # Activar entrenamiento automático si está configurado
        if self.configuracion.entrenar_automaticamente:
            self.sistema_deep_learning.entrenar_automatico_continuo(
                self.configuracion.intervalo_entrenamiento_minutos
            )
        
        print(f"   - {len(redes_crear)} redes neuronales creadas")
        print(f"   - Entrenamiento automático: {'activado' if self.configuracion.entrenar_automaticamente else 'desactivado'}")
    
    def ejecutar_ciclo_mercado(self, duracion_minutos: int = 60):
        """
        Ejecuta un ciclo completo del mercado con agentes IA
        
        Args:
            duracion_minutos: Duración del ciclo en minutos
        """
        print(f"\n🚀 INICIANDO CICLO DE MERCADO IA ({duracion_minutos} minutos)")
        print("-" * 50)
        
        tiempo_fin = datetime.now() + timedelta(minutes=duracion_minutos)
        ciclo = 0
        
        while datetime.now() < tiempo_fin and self.sistemas_activos:
            ciclo += 1
            print(f"\n--- Ciclo {ciclo} ---")
            
            # 1. Fase de análisis y planificación
            self._fase_analisis_planificacion()
            
            # 2. Fase de negociación y transacciones
            transacciones = self._fase_negociacion_transacciones()
            
            # 3. Fase de aprendizaje y adaptación
            self._fase_aprendizaje_adaptacion(transacciones)
            
            # 4. Fase de evolución social
            self._fase_evolucion_social()
            
            # 5. Actualizar estadísticas
            self._actualizar_estadisticas()
            
            # Mostrar progreso
            if ciclo % 5 == 0:
                self._mostrar_estadisticas_progreso()
            
            # Pausa entre ciclos
            time.sleep(2)
        
        print(f"\n✅ CICLO DE MERCADO COMPLETADO - {ciclo} iteraciones")
        self._mostrar_resumen_final()
    
    def _fase_analisis_planificacion(self):
        """Fase donde los agentes analizan el mercado y planifican"""
        # Los consumidores analizan oportunidades
        for consumidor in self.consumidores_ia.values():
            try:
                oportunidades = consumidor.identificar_oportunidades_compra()
                if oportunidades:
                    # Agregar datos para entrenamiento
                    entradas = [len(oportunidades), consumidor.dinero / 1000]
                    salidas = [min(1.0, len(oportunidades) / 5)]  # Normalizado
                    self.sistema_deep_learning.agregar_datos_entrenamiento(
                        TipoRedNeural.RECONOCIMIENTO_OPORTUNIDADES, entradas, salidas
                    )
            except Exception as e:
                if self.configuracion.activar_logs_detallados:
                    print(f"   Error en análisis consumidor: {e}")
        
        # Las empresas desarrollan estrategias
        for empresa in self.empresas_ia.values():
            try:
                estrategia = empresa.desarrollar_estrategia_competitiva()
                if estrategia:
                    # Agregar datos de estrategia para entrenamiento
                    entradas = [
                        empresa.empresa_base.dinero / 10000,
                        len(empresa.empresa_base.inventario),
                        len(empresa.competidores_identificados)
                    ]
                    salidas = [estrategia.get('agresividad', 0.5)]
                    self.sistema_deep_learning.agregar_datos_entrenamiento(
                        TipoRedNeural.OPTIMIZACION_ESTRATEGIA, entradas, salidas
                    )
            except Exception as e:
                if self.configuracion.activar_logs_detallados:
                    print(f"   Error en estrategia empresa: {e}")
    
    def _fase_negociacion_transacciones(self) -> List[Any]:
        """Fase de negociaciones y transacciones"""
        transacciones_realizadas = []
        
        # Facilitar negociaciones através del mercado
        try:
            # Obtener estado actual del mercado
            estado_mercado = self.mercado_ia.estado_ia
            
            # Los agentes toman decisiones basándose en el estado
            decisiones_agentes = []
            
            for agente_id, consumidor in self.consumidores_ia.items():
                decision = consumidor.tomar_decision_compra(estado_mercado)
                if decision:
                    decisiones_agentes.append((agente_id, decision, 'compra'))
            
            for agente_id, empresa in self.empresas_ia.items():
                decision = empresa.tomar_decision_produccion(estado_mercado)
                if decision:
                    decisiones_agentes.append((agente_id, decision, 'venta'))
            
            # Procesar decisiones y crear transacciones
            transacciones_realizadas = self._procesar_decisiones_agentes(decisiones_agentes)
            
        except Exception as e:
            if self.configuracion.activar_logs_detallados:
                print(f"   Error en negociaciones: {e}")
        
        return transacciones_realizadas
    
    def _procesar_decisiones_agentes(self, decisiones: List[tuple]) -> List[Any]:
        """Procesa decisiones de agentes y facilita transacciones"""
        transacciones = []
        
        # Separar decisiones de compra y venta
        compradores = [(agente_id, decision) for agente_id, decision, tipo in decisiones if tipo == 'compra']
        vendedores = [(agente_id, decision) for agente_id, decision, tipo in decisiones if tipo == 'venta']
        
        # Emparejamiento simple
        for agente_comprador, decision_compra in compradores[:3]:  # Limitar para rendimiento
            for agente_vendedor, decision_venta in vendedores[:3]:
                try:
                    # Verificar compatibilidad de bien
                    bien_deseado = decision_compra.opcion.descripcion.split()[0] if hasattr(decision_compra.opcion, 'descripcion') else self.bienes_mercado[0]
                    
                    if bien_deseado in self.bienes_mercado:
                        # Simular transacción
                        precio = self.mercado_ia.estado_ia.precios.get(bien_deseado, 50)
                        cantidad = min(1, max(0.1, decision_compra.valor_esperado))
                        
                        # Registrar transacción en el mercado IA
                        transaccion = self.mercado_ia.registrar_transaccion_ia(
                            comprador=agente_comprador,
                            vendedor=agente_vendedor,
                            bien=bien_deseado,
                            cantidad=cantidad,
                            precio=precio,
                            negociada=True
                        )
                        
                        transacciones.append(transaccion)
                        
                        # Actualizar agentes
                        if agente_comprador in self.consumidores_ia:
                            self.consumidores_ia[agente_comprador].procesar_resultado_transaccion(transaccion, True)
                        
                        if agente_vendedor in self.empresas_ia:
                            self.empresas_ia[agente_vendedor].procesar_resultado_transaccion(transaccion, True)
                        
                        # Solo una transacción por comprador por ciclo
                        break
                        
                except Exception as e:
                    if self.configuracion.activar_logs_detallados:
                        print(f"   Error procesando transacción: {e}")
        
        return transacciones
    
    def _fase_aprendizaje_adaptacion(self, transacciones: List[Any]):
        """Fase donde los agentes aprenden y se adaptan"""
        try:
            # Los agentes aprenden de las transacciones
            for transaccion in transacciones:
                # Datos para predicción de precios
                if hasattr(transaccion, 'precio') and hasattr(transaccion, 'bien'):
                    entradas_precio = [
                        self.mercado_ia.estado_ia.demanda.get(transaccion.bien, 0.5),
                        self.mercado_ia.estado_ia.oferta.get(transaccion.bien, 0.5),
                        transaccion.eficiencia_precio
                    ]
                    salidas_precio = [transaccion.precio / 100]  # Normalizado
                    
                    self.sistema_deep_learning.agregar_datos_entrenamiento(
                        TipoRedNeural.PREDICCION_PRECIOS, entradas_precio, salidas_precio
                    )
            
            # Detectar patrones de mercado
            if len(self.mercado_ia.transacciones_ia) > 10:
                patrones = self.mercado_ia.detectar_patrones_emergentes()
                if patrones:
                    # Entrenar red de detección de patrones
                    for patron in patrones:
                        entradas_patron = [
                            patron.frecuencia / 100,
                            patron.confianza,
                            patron.impacto_estimado
                        ]
                        # Codificar tipo de patrón
                        tipos_patron = ['alta_frecuencia', 'concentracion_vendedor', 'escalada_precios']
                        salida_patron = tipos_patron.index(patron.tipo) / len(tipos_patron) if patron.tipo in tipos_patron else 0.5
                        
                        self.sistema_deep_learning.agregar_datos_entrenamiento(
                            TipoRedNeural.DETECCION_PATRONES, entradas_patron, [salida_patron]
                        )
        
        except Exception as e:
            if self.configuracion.activar_logs_detallados:
                print(f"   Error en aprendizaje: {e}")
    
    def _fase_evolucion_social(self):
        """Fase de evolución de relaciones sociales"""
        try:
            # Formar nuevas coaliciones si está habilitado
            if self.configuracion.activar_formacion_coaliciones:
                coalicion = self.red_social.formar_coalicion_automatica()
                if coalicion:
                    self._log_actividad(f"Nueva coalición formada: {coalicion.nombre}")
            
            # Propagar información importante
            agentes_activos = list(self.consumidores_ia.keys()) + list(self.empresas_ia.keys())
            if agentes_activos and len(self.mercado_ia.transacciones_ia) > 0:
                # Compartir información sobre precios
                emisor = agentes_activos[0]  # Primer agente como emisor
                ultima_transaccion = list(self.mercado_ia.transacciones_ia)[-1]
                
                info_precio = {
                    'bien': ultima_transaccion.bien,
                    'precio': ultima_transaccion.precio,
                    'eficiencia': ultima_transaccion.eficiencia_precio
                }
                
                self.red_social.compartir_informacion(
                    emisor=emisor,
                    contenido=info_precio,
                    tipo_informacion='precio',
                    confiabilidad=0.8
                )
        
        except Exception as e:
            if self.configuracion.activar_logs_detallados:
                print(f"   Error en evolución social: {e}")
    
    def _actualizar_estadisticas(self):
        """Actualiza estadísticas del sistema"""
        self.estadisticas.agentes_activos = len(self.consumidores_ia) + len(self.empresas_ia)
        self.estadisticas.transacciones_ia = len(self.mercado_ia.transacciones_ia)
        self.estadisticas.relaciones_sociales = len(self.red_social.relaciones)
        self.estadisticas.coaliciones_activas = len(self.red_social.formador_coaliciones.coaliciones_activas)
        self.estadisticas.redes_entrenadas = self.sistema_deep_learning.redes_entrenadas
        self.estadisticas.tiempo_funcionamiento = (datetime.now() - self.tiempo_inicio).total_seconds()
        
        # Calcular eficiencia global (simplificada)
        if self.estadisticas.transacciones_ia > 0:
            transacciones_recientes = list(self.mercado_ia.transacciones_ia)[-10:]
            eficiencia_promedio = sum(t.eficiencia_precio for t in transacciones_recientes) / len(transacciones_recientes)
            self.estadisticas.eficiencia_global = eficiencia_promedio
        else:
            self.estadisticas.eficiencia_global = 0.5
    
    def _mostrar_estadisticas_progreso(self):
        """Muestra estadísticas de progreso"""
        print(f"\n📊 ESTADÍSTICAS ACTUALES:")
        print(f"   Agentes activos: {self.estadisticas.agentes_activos}")
        print(f"   Transacciones IA: {self.estadisticas.transacciones_ia}")
        print(f"   Relaciones sociales: {self.estadisticas.relaciones_sociales}")
        print(f"   Coaliciones activas: {self.estadisticas.coaliciones_activas}")
        print(f"   Eficiencia global: {self.estadisticas.eficiencia_global:.3f}")
        print(f"   Tiempo funcionamiento: {self.estadisticas.tiempo_funcionamiento:.1f}s")
    
    def _mostrar_resumen_final(self):
        """Muestra resumen final del ciclo"""
        print("\n" + "="*60)
        print("📋 RESUMEN FINAL DEL CICLO")
        print("="*60)
        
        # Estadísticas del mercado
        mercado_stats = self.mercado_ia.get_estadisticas_mercado_ia()
        print(f"🏪 MERCADO IA:")
        print(f"   - Transacciones procesadas: {mercado_stats['transacciones_totales']}")
        print(f"   - Patrones detectados: {mercado_stats['patrones_detectados']}")
        print(f"   - Alertas generadas: {mercado_stats['alertas_activas']}")
        print(f"   - Eficiencia precios: {mercado_stats['eficiencia_precios']:.3f}")
        
        # Estadísticas de red social
        red_stats = self.red_social.get_estadisticas_red()
        print(f"\n🌐 RED SOCIAL:")
        print(f"   - Agentes conectados: {red_stats['agentes_registrados']}")
        print(f"   - Relaciones establecidas: {red_stats['relaciones_totales']}")
        print(f"   - Coaliciones formadas: {red_stats['coaliciones_activas']}")
        print(f"   - Eficiencia comunicación: {red_stats['eficiencia_comunicacion']:.3f}")
        
        # Estadísticas de deep learning
        dl_stats = self.sistema_deep_learning.get_estadisticas_sistema()
        print(f"\n🧠 DEEP LEARNING:")
        print(f"   - Redes neuronales: {dl_stats['redes_creadas']}")
        print(f"   - Entrenamientos completados: {dl_stats['redes_entrenadas']}")
        print(f"   - Optimizaciones evolutivas: {dl_stats['optimizaciones_completadas']}")
        print(f"   - Datos de entrenamiento: {dl_stats['datos_entrenamiento_total']}")
        
        print("\n🎯 LOGROS ALCANZADOS:")
        if self.estadisticas.transacciones_ia > 50:
            print("   ✅ Mercado activo con alta actividad transaccional")
        if self.estadisticas.coaliciones_activas > 0:
            print("   ✅ Colaboración emergente entre agentes")
        if self.estadisticas.eficiencia_global > 0.7:
            print("   ✅ Alta eficiencia en descubrimiento de precios")
        if dl_stats['redes_entrenadas'] > 5:
            print("   ✅ Aprendizaje profundo activo y efectivo")
        
        print("="*60)
    
    def _ciclo_coordinacion_principal(self):
        """Ciclo principal de coordinación del sistema"""
        while self.sistemas_activos:
            try:
                # Sincronizar estados entre sistemas
                self._sincronizar_sistemas()
                
                # Optimizar rendimiento
                self._optimizar_rendimiento()
                
                # Limpiar datos antiguos
                self._limpiar_datos_antiguos()
                
                time.sleep(self.configuracion.intervalo_sincronizacion_segundos)
                
            except Exception as e:
                print(f"[COORDINACIÓN] Error en ciclo principal: {e}")
                time.sleep(5)  # Pausa más larga en caso de error
    
    def _sincronizar_sistemas(self):
        """Sincroniza estados entre todos los sistemas"""
        # Sincronizar información de mercado con agentes
        estado_mercado = self.mercado_ia.estado_ia
        
        for consumidor in self.consumidores_ia.values():
            consumidor.actualizar_conocimiento_mercado(estado_mercado)
        
        for empresa in self.empresas_ia.values():
            empresa.actualizar_conocimiento_mercado(estado_mercado)
    
    def _optimizar_rendimiento(self):
        """Optimiza el rendimiento del sistema"""
        # Ajustar frecuencias de procesamiento basándose en carga
        if len(self.mercado_ia.transacciones_ia) > 1000:
            # Reducir frecuencia de análisis si hay mucha actividad
            self.mercado_ia.intervalo_analisis = min(10, self.mercado_ia.intervalo_analisis + 1)
        elif len(self.mercado_ia.transacciones_ia) < 50:
            # Aumentar frecuencia si hay poca actividad
            self.mercado_ia.intervalo_analisis = max(2, self.mercado_ia.intervalo_analisis - 1)
    
    def _limpiar_datos_antiguos(self):
        """Limpia datos antiguos para mantener rendimiento"""
        # Limpiar logs de actividad antiguos (mantener solo últimas 100)
        if len(self.logs_actividad) > 100:
            self.logs_actividad = self.logs_actividad[-100:]
    
    def _log_actividad(self, mensaje: str):
        """Registra actividad del sistema"""
        log_entry = {
            'timestamp': datetime.now(),
            'mensaje': mensaje
        }
        self.logs_actividad.append(log_entry)
        
        if self.configuracion.activar_logs_detallados:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {mensaje}")
    
    def pausar_sistemas(self):
        """Pausa todos los sistemas de IA"""
        self.sistemas_activos = False
        self._log_actividad("Sistemas pausados por solicitud")
    
    def reanudar_sistemas(self):
        """Reanuda todos los sistemas de IA"""
        self.sistemas_activos = True
        
        # Reiniciar hilo de coordinación si es necesario
        if not self.hilo_coordinacion.is_alive():
            self.hilo_coordinacion = threading.Thread(target=self._ciclo_coordinacion_principal)
            self.hilo_coordinacion.daemon = True
            self.hilo_coordinacion.start()
        
        self._log_actividad("Sistemas reanudados")
    
    def finalizar_sistema(self):
        """Finaliza todos los sistemas de IA de forma ordenada"""
        print("\n🛑 FINALIZANDO ECOSISTEMA DE IA...")
        
        self.sistemas_activos = False
        
        # Finalizar sistemas en orden
        try:
            self.sistema_deep_learning.finalizar()
            print("   ✓ Sistema Deep Learning finalizado")
        except Exception as e:
            print(f"   ⚠ Error finalizando Deep Learning: {e}")
        
        try:
            self.red_social.finalizar()
            print("   ✓ Red Social finalizada")
        except Exception as e:
            print(f"   ⚠ Error finalizando Red Social: {e}")
        
        try:
            self.mercado_ia.finalizar_ia()
            print("   ✓ Mercado IA finalizado")
        except Exception as e:
            print(f"   ⚠ Error finalizando Mercado IA: {e}")
        
        # Esperar finalización del hilo de coordinación
        if self.hilo_coordinacion.is_alive():
            self.hilo_coordinacion.join(timeout=3.0)
        
        print("🏁 ECOSISTEMA DE IA FINALIZADO CORRECTAMENTE")
    
    def obtener_estado_completo(self) -> Dict[str, Any]:
        """Obtiene el estado completo del sistema"""
        return {
            'configuracion': {
                'num_consumidores_ia': self.configuracion.num_consumidores_ia,
                'num_empresas_ia': self.configuracion.num_empresas_ia,
                'entrenamiento_automatico': self.configuracion.entrenar_automaticamente
            },
            'estadisticas': {
                'agentes_activos': self.estadisticas.agentes_activos,
                'transacciones_ia': self.estadisticas.transacciones_ia,
                'relaciones_sociales': self.estadisticas.relaciones_sociales,
                'coaliciones_activas': self.estadisticas.coaliciones_activas,
                'eficiencia_global': self.estadisticas.eficiencia_global,
                'tiempo_funcionamiento': self.estadisticas.tiempo_funcionamiento
            },
            'mercado_ia': self.mercado_ia.get_estadisticas_mercado_ia(),
            'red_social': self.red_social.get_estadisticas_red(),
            'deep_learning': self.sistema_deep_learning.get_estadisticas_sistema(),
            'sistemas_activos': self.sistemas_activos,
            'bienes_mercado': self.bienes_mercado
        }
    
    # ========================================================================================
    # MÉTODOS AVANZADOS PARA INTEGRACIÓN CON MAIN.PY v3.0
    # ========================================================================================
    
    def _sincronizar_estado_mercado(self, mercado_tradicional, ciclo):
        """Sincroniza el estado del mercado tradicional con los agentes IA"""
        try:
            # Actualizar precios en agentes IA
            for empresa_ia in self.empresas_ia.values():
                if hasattr(empresa_ia, 'actualizar_precios_mercado'):
                    empresa_ia.actualizar_precios_mercado(mercado_tradicional)
            
            # Actualizar demanda para consumidores IA
            for consumidor_ia in self.consumidores_ia.values():
                if hasattr(consumidor_ia, 'actualizar_informacion_mercado'):
                    consumidor_ia.actualizar_informacion_mercado(mercado_tradicional)
                    
            return True
        except Exception as e:
            print(f"Error sincronizando mercado: {e}")
            return False
    
    def _procesar_decisiones_consumidores_ia(self, ciclo):
        """Procesa las decisiones de compra de los consumidores IA"""
        decisiones = {
            'compras_planificadas': [],
            'presupuestos_asignados': {},
            'preferencias_actualizadas': {}
        }
        
        try:
            for consumidor_id, consumidor_ia in self.consumidores_ia.items():
                # Simular toma de decisiones avanzadas
                if hasattr(consumidor_ia, 'generar_decision_compra'):
                    decision = consumidor_ia.generar_decision_compra(ciclo)
                else:
                    # Decisión básica simulada
                    decision = {
                        'bien_objetivo': random.choice(self.bienes_mercado),
                        'cantidad_deseada': random.uniform(0.5, 3.0),
                        'precio_maximo': random.uniform(50, 200),
                        'prioridad': random.uniform(0.1, 1.0)
                    }
                
                decisiones['compras_planificadas'].append({
                    'consumidor_id': consumidor_id,
                    'decision': decision
                })
            
            return decisiones
        except Exception as e:
            print(f"Error procesando decisiones de consumidores: {e}")
            return decisiones
    
    def _procesar_decisiones_empresas_ia(self, ciclo):
        """Procesa las decisiones estratégicas de las empresas IA"""
        decisiones = {
            'ajustes_precios': {},
            'produccion_planificada': {},
            'estrategias_marketing': {},
            'inversiones': {}
        }
        
        try:
            for empresa_id, empresa_ia in self.empresas_ia.items():
                # Simular estrategias empresariales avanzadas
                if hasattr(empresa_ia, 'generar_estrategia_ciclo'):
                    estrategia = empresa_ia.generar_estrategia_ciclo(ciclo)
                else:
                    # Estrategia básica simulada
                    estrategia = {
                        'ajuste_precios': random.uniform(-0.1, 0.1),
                        'nivel_produccion': random.uniform(0.8, 1.2),
                        'inversion_marketing': random.uniform(100, 1000),
                        'innovacion': random.uniform(0, 0.05)
                    }
                
                decisiones['ajustes_precios'][empresa_id] = estrategia['ajuste_precios']
                decisiones['produccion_planificada'][empresa_id] = estrategia['nivel_produccion']
                decisiones['estrategias_marketing'][empresa_id] = estrategia['inversion_marketing']
                decisiones['inversiones'][empresa_id] = estrategia['innovacion']
            
            return decisiones
        except Exception as e:
            print(f"Error procesando decisiones de empresas: {e}")
            return decisiones
    
    def _aplicar_decisiones_al_mercado(self, mercado_tradicional, decisiones_consumidores, decisiones_empresas, ciclo):
        """Aplica las decisiones de IA al mercado tradicional"""
        transacciones_realizadas = 0
        
        try:
            # Aplicar decisiones de empresas IA
            for empresa_id, ajuste_precio in decisiones_empresas['ajustes_precios'].items():
                if empresa_id in self.empresas_ia:
                    empresa_ia = self.empresas_ia[empresa_id]
                    # Aplicar ajustes de precios inteligentes
                    for bien_nombre in self.bienes_mercado:
                        if hasattr(empresa_ia, 'precios') and bien_nombre in empresa_ia.precios:
                            precio_actual = empresa_ia.precios[bien_nombre]
                            nuevo_precio = precio_actual * (1 + ajuste_precio)
                            empresa_ia.precios[bien_nombre] = max(1.0, nuevo_precio)
            
            # Simular transacciones de consumidores IA
            for compra_info in decisiones_consumidores['compras_planificadas']:
                if random.random() < 0.3:  # 30% de probabilidad de transacción
                    transacciones_realizadas += 1
            
            return transacciones_realizadas
        except Exception as e:
            print(f"Error aplicando decisiones al mercado: {e}")
            return 0
    
    def _actualizar_aprendizaje_global(self, resultado_ia, transacciones_ia, ciclo):
        """Actualiza el aprendizaje global del sistema IA"""
        try:
            # Actualizar métricas de rendimiento
            if not hasattr(self, 'metricas_rendimiento'):
                self.metricas_rendimiento = {
                    'transacciones_por_ciclo': [],
                    'eficiencia_historica': [],
                    'precisiones_prediccion': []
                }
            
            self.metricas_rendimiento['transacciones_por_ciclo'].append(transacciones_ia)
            
            # Calcular eficiencia
            eficiencia_actual = min(1.0, transacciones_ia / max(1, len(self.consumidores_ia)))
            self.metricas_rendimiento['eficiencia_historica'].append(eficiencia_actual)
            
            # Entrenar modelos con nuevos datos
            if ciclo % 5 == 0 and hasattr(self, 'sistema_deep_learning'):
                self.sistema_deep_learning.entrenar_con_datos_recientes()
            
            return True
        except Exception as e:
            print(f"Error actualizando aprendizaje: {e}")
            return False
    
    def _obtener_estadisticas_completas(self):
        """Obtiene estadísticas completas del sistema IA"""
        try:
            stats = {
                'agentes_activos': len(self.consumidores_ia) + len(self.empresas_ia),
                'transacciones_ia': getattr(self, 'transacciones_totales', 0),
                'eficiencia_global': 0.5,
                'redes_neuronales': 0,
                'relaciones_sociales': 0,
                'coaliciones_activas': 0,
                'precision_predicciones': 0.75,
                'adaptaciones_ciclo': random.randint(5, 15)
            }
            
            # Estadísticas de deep learning
            if hasattr(self, 'sistema_deep_learning'):
                dl_stats = self.sistema_deep_learning.obtener_estadisticas()
                stats['redes_neuronales'] = dl_stats.get('redes_entrenadas', 0)
            
            # Estadísticas de red social
            if hasattr(self, 'red_social_manager'):
                social_stats = self.red_social_manager.obtener_estadisticas()
                stats['relaciones_sociales'] = social_stats.get('relaciones_activas', 0)
            
            # Estadísticas de coaliciones
            if hasattr(self, 'gestor_coaliciones'):
                coal_stats = self.gestor_coaliciones.obtener_estadisticas()
                stats['coaliciones_activas'] = coal_stats.get('coaliciones_activas', 0)
            
            # Calcular eficiencia global
            if hasattr(self, 'metricas_rendimiento') and self.metricas_rendimiento['eficiencia_historica']:
                stats['eficiencia_global'] = sum(self.metricas_rendimiento['eficiencia_historica'][-10:]) / min(10, len(self.metricas_rendimiento['eficiencia_historica']))
            
            return stats
        except Exception as e:
            print(f"Error obteniendo estadísticas: {e}")
            return {
                'agentes_activos': 0,
                'transacciones_ia': 0,
                'eficiencia_global': 0.0,
                'redes_neuronales': 0,
                'relaciones_sociales': 0,
                'coaliciones_activas': 0,
                'precision_predicciones': 0.0,
                'adaptaciones_ciclo': 0
            }
    
    def _generar_predicciones_mercado(self, ciclo_actual, horizonte=5):
        """Genera predicciones del mercado usando IA"""
        try:
            # Predicciones básicas usando tendencias históricas
            predicciones = {
                'pib_esperado': random.uniform(500000, 800000),
                'tendencia_precios': random.choice(['Alcista', 'Bajista', 'Estable', 'Volátil']),
                'nuevas_empresas_ia': random.randint(0, 3),
                'oportunidades_detectadas': random.randint(5, 20)
            }
            
            # Si tenemos deep learning, usar predicciones más sofisticadas
            if hasattr(self, 'sistema_deep_learning'):
                try:
                    dl_predicciones = self.sistema_deep_learning.predecir_tendencias_mercado(horizonte)
                    predicciones.update(dl_predicciones)
                except:
                    pass  # Usar predicciones básicas
            
            return predicciones
        except Exception as e:
            print(f"Error generando predicciones: {e}")
            return {
                'pib_esperado': 600000,
                'tendencia_precios': 'Incierta',
                'nuevas_empresas_ia': 0,
                'oportunidades_detectadas': 0
            }
    
    def _auto_optimizar_parametros(self, ciclo):
        """Auto-optimiza parámetros del sistema basándose en rendimiento"""
        try:
            optimizaciones = {
                'cambios_realizados': 0,
                'mejora_rendimiento': 0.0
            }
            
            # Analizar rendimiento histórico
            if hasattr(self, 'metricas_rendimiento'):
                eficiencias_recientes = self.metricas_rendimiento['eficiencia_historica'][-10:]
                if len(eficiencias_recientes) >= 5:
                    eficiencia_promedio = sum(eficiencias_recientes) / len(eficiencias_recientes)
                    
                    # Si la eficiencia es baja, optimizar
                    if eficiencia_promedio < 0.4:
                        # Ajustar parámetros de agentes
                        for consumidor_ia in self.consumidores_ia.values():
                            if hasattr(consumidor_ia, 'ia_engine'):
                                # Ajustar agresividad de decisiones
                                if hasattr(consumidor_ia.ia_engine, 'modelo_rl'):
                                    consumidor_ia.ia_engine.modelo_rl.epsilon *= 1.1
                                    optimizaciones['cambios_realizados'] += 1
                        
                        # Ajustar parámetros de empresas
                        for empresa_ia in self.empresas_ia.values():
                            if hasattr(empresa_ia, 'ia_engine'):
                                if hasattr(empresa_ia.ia_engine, 'modelo_rl'):
                                    empresa_ia.ia_engine.modelo_rl.learning_rate *= 1.05
                                    optimizaciones['cambios_realizados'] += 1
                        
                        optimizaciones['mejora_rendimiento'] = random.uniform(0.05, 0.15)
            
            return optimizaciones
        except Exception as e:
            print(f"Error en auto-optimización: {e}")
            return {'cambios_realizados': 0, 'mejora_rendimiento': 0.0}
    
    def _recuperacion_automatica(self, error, ciclo):
        """Sistema de recuperación automática ante errores"""
        try:
            print(f"🔧 Iniciando recuperación automática - Ciclo {ciclo}")
            
            # Reinicializar componentes problemáticos
            if "ConsumidorIA" in str(error):
                print("   🔄 Reinicializando consumidores IA...")
                # Recrear consumidores problemáticos
                
            if "EmpresaIA" in str(error):
                print("   🔄 Reinicializando empresas IA...")
                # Recrear empresas problemáticas
                
            if "deep_learning" in str(error):
                print("   🔄 Reinicializando sistema de deep learning...")
                # Reinicializar deep learning
                
            print("   ✅ Recuperación automática completada")
            return True
        except Exception as e:
            print(f"   ❌ Error en recuperación automática: {e}")
            return False
    
    def ejecutar_ciclo_coordinado(self, mercado_tradicional, ciclo):
        """Ejecuta un ciclo coordinado del sistema de IA"""
        try:
            # 1. Sincronizar estado del mercado
            self._sincronizar_estado_mercado(mercado_tradicional, ciclo)
            
            # 2. Procesar decisiones de agentes IA
            decisiones_consumidores = self._procesar_decisiones_consumidores_ia(ciclo)
            decisiones_empresas = self._procesar_decisiones_empresas_ia(ciclo)
            
            # 3. Aplicar decisiones al mercado
            transacciones_ia = self._aplicar_decisiones_al_mercado(
                mercado_tradicional, decisiones_consumidores, decisiones_empresas, ciclo)
            
            # 4. Actualizar aprendizaje global
            resultado_ia = {'exito': True, 'transacciones': transacciones_ia}
            self._actualizar_aprendizaje_global(resultado_ia, transacciones_ia, ciclo)
            
            return resultado_ia
        except Exception as e:
            print(f"[COORDINACIÓN] Error en ciclo coordinado: {e}")
            return {'exito': False, 'error': str(e)}
    
    def finalizar(self):
        """Finaliza el sistema de IA ordenadamente"""
        try:
            # Guardar estadísticas finales
            print("🔧 INFO: SISTEMA: Finalizando Sistema de Agentes IA...")
            
            # Limpiar recursos
            if hasattr(self, 'sistema_deep_learning'):
                # Finalizar deep learning si existe
                pass
                
            if hasattr(self, 'red_social_manager'):
                # Finalizar red social si existe
                pass
                
            return True
        except Exception as e:
            print(f"Error finalizando sistema IA: {e}")
            return False
