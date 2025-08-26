# Guía Técnica - Patrones de Integración y Flujos de Comunicación

## Tabla de Contenidos
1. [Arquitectura de Integración](#arquitectura-de-integración)
2. [Patrones de Comunicación](#patrones-de-comunicación)
3. [Flujos de Datos](#flujos-de-datos)
4. [Sincronización y Coordinación](#sincronización-y-coordinación)
5. [Gestión de Estado](#gestión-de-estado)
6. [APIs y Interfaces](#apis-y-interfaces)

---

## Arquitectura de Integración

### Modelo de Capas de Integración

El sistema utiliza un modelo de integración en capas que permite la comunicación fluida entre componentes mientras mantiene la separación de responsabilidades:

```
┌─────────────────────────────────────────────────────────────┐
│                    CAPA DE ORQUESTACIÓN                     │
│                                                             │
│  ┌─────────────────┐ ┌─────────────────┐ ┌──────────────┐   │
│  │ IntegradorIA    │ │ Coordinador     │ │ EventBus     │   │
│  │                 │ │ Principal       │ │ Global       │   │
│  └─────────────────┘ └─────────────────┘ └──────────────┘   │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                  CAPA DE COORDINACIÓN                       │
│                                                             │
│  ┌─────────────────┐ ┌─────────────────┐ ┌──────────────┐   │
│  │ OrquestadorIA   │ │ Hub Mensajes    │ │ Sincronizador│   │
│  │                 │ │                 │ │              │   │
│  └─────────────────┘ └─────────────────┘ └──────────────┘   │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                   CAPA DE SERVICIOS                        │
│                                                             │
│  ┌─────────────────┐ ┌─────────────────┐ ┌──────────────┐   │
│  │ ServiciosIA     │ │ ServiciosEcon.  │ │ ServiciosDatos│   │
│  │                 │ │                 │ │              │   │
│  └─────────────────┘ └─────────────────┘ └──────────────┘   │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                   CAPA DE ENTIDADES                        │
│                                                             │
│  ┌─────────────────┐ ┌─────────────────┐ ┌──────────────┐   │
│  │ Agentes IA      │ │ Modelos Econ.   │ │ Sistemas     │   │
│  │                 │ │                 │ │ Base         │   │
│  └─────────────────┘ └─────────────────┘ └──────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Puntos de Integración Principales

#### 1. Integrador Principal (main.py)

El `main.py` actúa como el coordinador maestro que orquesta todos los sistemas:

```python
class CoordinadorPrincipal:
    """Coordinador maestro del sistema completo"""
    
    def __init__(self):
        self.sistemas_activos = {}
        self.integradores = {}
        self.event_bus = EventBusGlobal()
        
    def inicializar_sistema_completo(self):
        """
        Inicialización ordenada de todos los sistemas:
        1. Configuración y validación
        2. Sistemas base (modelos económicos)
        3. Sistemas avanzados (banking, trabajo, etc.)
        4. Sistema de IA
        5. Monitoreo y analytics
        """
        
        # Fase 1: Configuración
        self.configuracion = self._cargar_y_validar_configuracion()
        
        # Fase 2: Sistemas base
        self.mercado = self._inicializar_mercado_base()
        self._crear_agentes_economicos_base()
        
        # Fase 3: Sistemas avanzados
        self._integrar_sistema_bancario()
        self._integrar_mercado_trabajo()
        self._integrar_precios_dinamicos()
        self._integrar_banco_central()
        
        # Fase 4: Sistema de IA
        if self.configuracion.get('agentes_ia', {}).get('activar', False):
            self.integrador_ia = self._inicializar_sistema_ia()
            self._integrar_ia_con_economia()
        
        # Fase 5: Monitoreo
        self._configurar_monitoreo_y_analytics()
        
        # Fase 6: Event Bus
        self._configurar_event_bus()
    
    def _integrar_ia_con_economia(self):
        """Integración bidireccional entre IA y economía"""
        
        # IA → Economía: Decisiones de agentes afectan el mercado
        self.integrador_ia.registrar_callback_decisiones(
            self.mercado.procesar_decisiones_ia
        )
        
        # Economía → IA: Estado del mercado informa decisiones
        self.mercado.registrar_observer_estado(
            self.integrador_ia.actualizar_estado_mercado
        )
        
        # Coordinación de ciclos
        self.coordinador_ciclos = CoordinadorCiclos(
            self.mercado, self.integrador_ia
        )
```

#### 2. Coordinador de Ciclos

```python
class CoordinadorCiclos:
    """Coordinación de ciclos entre IA y economía"""
    
    def __init__(self, mercado, integrador_ia):
        self.mercado = mercado
        self.integrador_ia = integrador_ia
        self.sincronizador = SincronizadorCiclos()
        
    def ejecutar_ciclo_integrado(self, numero_ciclo):
        """
        Ejecución coordinada de un ciclo completo:
        1. Pre-procesamiento
        2. Fase económica
        3. Fase IA
        4. Sincronización
        5. Post-procesamiento
        """
        
        # 1. Pre-procesamiento
        estado_inicial = self._capturar_estado_inicial()
        
        # 2. Fase económica (sistemas tradicionales)
        resultados_economicos = self.mercado.ejecutar_ciclo_economico(numero_ciclo)
        
        # 3. Fase IA (agentes inteligentes)
        if self.integrador_ia:
            decisiones_ia = self.integrador_ia.ejecutar_ciclo_ia(numero_ciclo)
            
            # Aplicar decisiones IA al mercado
            self.mercado.aplicar_decisiones_ia(decisiones_ia)
        
        # 4. Sincronización
        self.sincronizador.sincronizar_estado(
            self.mercado, self.integrador_ia
        )
        
        # 5. Post-procesamiento
        self._procesar_resultados_ciclo(
            estado_inicial, resultados_economicos, decisiones_ia
        )
        
        return {
            'ciclo': numero_ciclo,
            'resultados_economicos': resultados_economicos,
            'decisiones_ia': decisiones_ia,
            'estado_final': self._capturar_estado_final()
        }
```

---

## Patrones de Comunicación

### Patrón Observer para Estado de Mercado

El sistema utiliza el patrón Observer para propagar cambios de estado del mercado a todos los componentes interesados:

```python
class EstadoMercadoObservable:
    """Observable para cambios en el estado del mercado"""
    
    def __init__(self):
        self.observadores = {
            'agentes_ia': [],
            'sistemas_economicos': [],
            'analytics': [],
            'monitoreo': []
        }
        self.estado_actual = EstadoMercado()
        
    def agregar_observador(self, observador, categoria='general'):
        """Registro de observadores por categoría"""
        if categoria not in self.observadores:
            self.observadores[categoria] = []
        
        self.observadores[categoria].append(observador)
    
    def notificar_cambio_estado(self, nuevo_estado, tipo_cambio='general'):
        """
        Notificación inteligente basada en tipo de cambio:
        - Solo notifica a observadores relevantes
        - Incluye diff del estado para eficiencia
        """
        
        # Calcular diferencias
        diff_estado = self._calcular_diff_estado(self.estado_actual, nuevo_estado)
        
        # Notificar según relevancia
        if tipo_cambio in ['precios', 'general']:
            self._notificar_categoria('agentes_ia', nuevo_estado, diff_estado)
        
        if tipo_cambio in ['economia', 'general']:
            self._notificar_categoria('sistemas_economicos', nuevo_estado, diff_estado)
        
        if tipo_cambio in ['metricas', 'general']:
            self._notificar_categoria('analytics', nuevo_estado, diff_estado)
        
        # Siempre notificar monitoreo
        self._notificar_categoria('monitoreo', nuevo_estado, diff_estado)
        
        self.estado_actual = nuevo_estado
```

### Patrón Mediator para Comunicación Cross-Sistema

```python
class MediadorSistemas:
    """Mediador central para comunicación entre sistemas"""
    
    def __init__(self):
        self.sistemas_registrados = {}
        self.canales_comunicacion = {}
        self.cola_mensajes = queue.PriorityQueue()
        
    def registrar_sistema(self, sistema_id, sistema, interfaces):
        """Registro de sistemas con sus interfaces de comunicación"""
        self.sistemas_registrados[sistema_id] = {
            'instancia': sistema,
            'interfaces': interfaces,
            'estado': 'activo'
        }
        
        # Configurar canales
        for interface in interfaces:
            if interface not in self.canales_comunicacion:
                self.canales_comunicacion[interface] = []
            
            self.canales_comunicacion[interface].append(sistema_id)
    
    def enviar_mensaje_sistema(self, remitente, destinatario, mensaje, prioridad=1):
        """Envío de mensajes entre sistemas"""
        
        mensaje_completo = MensajeSistema(
            remitente=remitente,
            destinatario=destinatario,
            contenido=mensaje,
            timestamp=datetime.now(),
            prioridad=prioridad
        )
        
        self.cola_mensajes.put((prioridad, mensaje_completo))
    
    def procesar_mensajes(self):
        """Procesamiento de cola de mensajes"""
        while not self.cola_mensajes.empty():
            prioridad, mensaje = self.cola_mensajes.get()
            
            # Verificar destinatario activo
            if mensaje.destinatario in self.sistemas_registrados:
                sistema_destino = self.sistemas_registrados[mensaje.destinatario]['instancia']
                
                # Entregar mensaje
                if hasattr(sistema_destino, 'recibir_mensaje_sistema'):
                    sistema_destino.recibir_mensaje_sistema(mensaje)
```

### Patrón Publish-Subscribe para Eventos

```python
class EventBusGlobal:
    """Bus de eventos global del sistema"""
    
    def __init__(self):
        self.suscriptores = defaultdict(list)
        self.filtros_eventos = {}
        self.historial_eventos = deque(maxlen=1000)
        
    def suscribir(self, evento_tipo, callback, filtros=None):
        """Suscripción a tipos de eventos específicos"""
        suscriptor = Suscriptor(
            callback=callback,
            filtros=filtros or {},
            timestamp_suscripcion=datetime.now()
        )
        
        self.suscriptores[evento_tipo].append(suscriptor)
    
    def publicar_evento(self, evento):
        """Publicación de eventos con filtrado inteligente"""
        
        # Registrar en historial
        self.historial_eventos.append(evento)
        
        # Notificar suscriptores
        for suscriptor in self.suscriptores[evento.tipo]:
            if self._aplicar_filtros(evento, suscriptor.filtros):
                try:
                    suscriptor.callback(evento)
                except Exception as e:
                    # Log error pero continúa procesamiento
                    print(f"Error en suscriptor de evento {evento.tipo}: {e}")

# Eventos específicos del sistema
class EventoEconomico:
    """Eventos relacionados con cambios económicos"""
    
    CAMBIO_PRECIO = "cambio_precio"
    TRANSACCION_COMPLETADA = "transaccion_completada"
    CRISIS_DETECTADA = "crisis_detectada"
    POLITICA_MONETARIA = "politica_monetaria"

class EventoIA:
    """Eventos relacionados con agentes IA"""
    
    DECISION_AGENTE = "decision_agente"
    FORMACION_COALICION = "formacion_coalicion"
    APRENDIZAJE_COMPLETADO = "aprendizaje_completado"
    COMPORTAMIENTO_EMERGENTE = "comportamiento_emergente"
```

---

## Flujos de Datos

### Flujo de Datos Principal del Sistema

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  CONFIGURACIÓN  │───▶│  INICIALIZACIÓN │───▶│ CREACIÓN AGENTES│
│                 │    │                 │    │                 │
│ • config.json   │    │ • Validación    │    │ • Consumidores  │
│ • Parámetros    │    │ • Sistemas base │    │ • Empresas      │
│ • Escenarios    │    │ • Logging       │    │ • Gobierno      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
                                                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ ANÁLISIS FINAL  │◀───│ MÉTRICAS/LOGS   │◀───│ SISTEMAS ACTIVOS│
│                 │    │                 │    │                 │
│ • Dashboard     │    │ • ML Analytics  │    │ • Banking       │
│ • Reportes      │    │ • Validación    │    │ • Mercado Labor │
│ • Exportación   │    │ • Monitoreo     │    │ • Precios Dinám.│
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
                                                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ ESTADO GLOBAL   │◀───│ PROCESAMIENTO   │◀───│ CICLO ECONÓMICO │
│                 │    │                 │    │                 │
│ • Sincronización│    │ • Transacciones │    │ • Oferta/Demanda│
│ • Consistencia  │    │ • Decisiones IA │    │ • Ajuste Precios│
│ • Persistencia  │    │ • Comunicación  │    │ • Política Econ.│
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Flujo de Decisiones IA

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ ESTADO MERCADO  │───▶│ ANÁLISIS AGENTE │───▶│ GENERACIÓN      │
│                 │    │                 │    │ OPCIONES        │
│ • Precios       │    │ • Memoria       │    │                 │
│ • Inventarios   │    │ • Preferencias  │    │ • Compra/Venta  │
│ • Competencia   │    │ • Red Social    │    │ • Negociación   │
│ • Tendencias    │    │ • Experiencia   │    │ • Alianzas      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
                                                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ ACTUALIZACIÓN   │◀───│ EJECUCIÓN       │◀───│ TOMA DECISIÓN   │
│ ESTADO          │    │ ACCIÓN          │    │                 │
│                 │    │                 │    │ • Motor IA      │
│ • Memoria       │    │ • Transacciones │    │ • Evaluación    │
│ • Reputación    │    │ • Comunicación  │    │ • Selección     │
│ • Aprendizaje   │    │ • Coordinación  │    │ • Incertidumbre │
│ • Red Social    │    │ • Sincronización│    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Flujo de Datos Cross-Sistema

#### Integración Mercado ↔ IA

```python
class IntegradorMercadoIA:
    """Integración bidireccional entre mercado y sistema de IA"""
    
    def __init__(self, mercado, sistema_ia):
        self.mercado = mercado
        self.sistema_ia = sistema_ia
        self.mapeador_datos = MapeadorDatos()
        
    def mercado_a_ia(self):
        """Transformación de datos del mercado para agentes IA"""
        
        # Capturar estado del mercado
        estado_economico = self.mercado.obtener_estado_completo()
        
        # Transformar a formato IA
        estado_ia = self.mapeador_datos.transformar_estado_para_ia(
            estado_economico
        )
        
        # Agregar contexto específico para IA
        estado_ia['señales_mercado'] = self._generar_señales_mercado(estado_economico)
        estado_ia['oportunidades'] = self._detectar_oportunidades(estado_economico)
        estado_ia['amenazas'] = self._detectar_amenazas(estado_economico)
        
        return estado_ia
    
    def ia_a_mercado(self, decisiones_ia):
        """Transformación de decisiones IA para el mercado"""
        
        # Validar decisiones
        decisiones_validadas = self._validar_decisiones_ia(decisiones_ia)
        
        # Transformar a formato de mercado
        transacciones_mercado = []
        
        for decision in decisiones_validadas:
            if decision.tipo == TipoDecision.COMPRA:
                transaccion = self._crear_transaccion_compra(decision)
                transacciones_mercado.append(transaccion)
            
            elif decision.tipo == TipoDecision.VENTA:
                transaccion = self._crear_transaccion_venta(decision)
                transacciones_mercado.append(transaccion)
            
            elif decision.tipo == TipoDecision.NEGOCIACION:
                negociacion = self._iniciar_negociacion_mercado(decision)
                transacciones_mercado.append(negociacion)
        
        return transacciones_mercado
```

#### Integración Sistema Bancario ↔ Agentes

```python
class IntegradorBancoAgentes:
    """Integración entre sistema bancario y agentes IA"""
    
    def procesar_solicitud_credito_ia(self, agente_ia, solicitud):
        """Procesamiento de solicitudes de crédito de agentes IA"""
        
        # Evaluar perfil crediticio del agente IA
        perfil_crediticio = self._evaluar_perfil_agente_ia(agente_ia)
        
        # Determinar capacidad de pago basada en comportamiento IA
        capacidad_pago = self._calcular_capacidad_pago_ia(
            agente_ia, solicitud
        )
        
        # Aplicar algoritmo de scoring considerando IA
        score_final = self.sistema_bancario.calcular_score_crediticio({
            'perfil_tradicional': perfil_crediticio,
            'comportamiento_ia': agente_ia.obtener_metricas_comportamiento(),
            'historial_decisiones': agente_ia.obtener_historial_decisiones(),
            'red_social': agente_ia.obtener_métricas_red_social()
        })
        
        # Tomar decisión de crédito
        decision_credito = self.sistema_bancario.evaluar_solicitud_credito(
            solicitud, score_final
        )
        
        return decision_credito
```

---

## Sincronización y Coordinación

### Sincronizador de Ciclos

```python
class SincronizadorCiclos:
    """Sincronización de ciclos entre diferentes sistemas"""
    
    def __init__(self):
        self.sistemas_sincronizados = {}
        self.barreras_sincronizacion = {}
        self.estado_ciclo_actual = {}
        
    def registrar_sistema_para_sincronizacion(self, sistema_id, sistema):
        """Registro de sistemas que requieren sincronización"""
        self.sistemas_sincronizados[sistema_id] = {
            'instancia': sistema,
            'fase_actual': 'idle',
            'listo_para_siguiente_fase': False,
            'tiempo_ultima_sincronizacion': datetime.now()
        }
    
    def sincronizar_fase_ciclo(self, fase, timeout_segundos=30):
        """
        Sincronización de una fase específica del ciclo:
        1. Verificar que todos los sistemas estén listos
        2. Coordinar inicio simultáneo
        3. Monitorear progreso
        4. Confirmar finalización
        """
        
        # 1. Verificar preparación
        sistemas_listos = self._verificar_sistemas_listos_para_fase(fase)
        
        if not sistemas_listos:
            # Esperar con timeout
            tiempo_inicio = time.time()
            while time.time() - tiempo_inicio < timeout_segundos:
                if self._verificar_sistemas_listos_para_fase(fase):
                    sistemas_listos = True
                    break
                time.sleep(0.1)
        
        if not sistemas_listos:
            raise TimeoutError(f"Timeout en sincronización de fase {fase}")
        
        # 2. Coordinar inicio
        self._señalizar_inicio_fase(fase)
        
        # 3. Monitorear progreso
        self._monitorear_progreso_fase(fase)
        
        # 4. Confirmar finalización
        self._confirmar_finalizacion_fase(fase)
    
    def _verificar_sistemas_listos_para_fase(self, fase):
        """Verificación de que todos los sistemas están listos"""
        for sistema_id, info in self.sistemas_sincronizados.items():
            if not info['listo_para_siguiente_fase']:
                return False
        return True
```

### Coordinador de Estado Global

```python
class CoordinadorEstadoGlobal:
    """Coordinación del estado global del sistema"""
    
    def __init__(self):
        self.estado_global = EstadoGlobalSistema()
        self.gestores_estado = {}
        self.validadores_consistencia = []
        
    def actualizar_estado_componente(self, componente_id, nuevo_estado):
        """Actualización coordinada del estado de un componente"""
        
        # 1. Validar cambio de estado
        if not self._validar_cambio_estado(componente_id, nuevo_estado):
            raise ValueError(f"Cambio de estado inválido para {componente_id}")
        
        # 2. Calcular impactos en otros componentes
        impactos = self._calcular_impactos_cruzados(componente_id, nuevo_estado)
        
        # 3. Aplicar cambios de forma atómica
        with self.estado_global.lock:
            # Actualizar componente principal
            self.estado_global.componentes[componente_id] = nuevo_estado
            
            # Aplicar impactos calculados
            for componente_impactado, cambio in impactos.items():
                self._aplicar_cambio_impacto(componente_impactado, cambio)
            
            # Validar consistencia global
            if not self._validar_consistencia_global():
                # Rollback si hay inconsistencias
                self._rollback_cambios(componente_id, impactos)
                raise ValueError("Cambio causaría inconsistencia global")
        
        # 4. Notificar cambios
        self._notificar_cambios_estado(componente_id, impactos)
```

---

## Gestión de Estado

### Estado Global del Sistema

```python
@dataclass
class EstadoGlobalSistema:
    """Estado global centralizado del sistema"""
    
    # Estados de componentes principales
    mercado: EstadoMercado
    agentes_ia: EstadoAgentesIA
    sistema_bancario: EstadoBancario
    mercado_trabajo: EstadoMercadoTrabajo
    
    # Métricas globales
    metricas_rendimiento: Dict[str, float]
    metricas_estabilidad: Dict[str, float]
    
    # Control de sincronización
    ciclo_actual: int
    timestamp_ultima_actualizacion: datetime
    lock: threading.RLock = field(default_factory=threading.RLock)
    
    # Validadores de consistencia
    validadores_activos: List[str] = field(default_factory=list)
    
    def obtener_snapshot(self):
        """Obtiene snapshot inmutable del estado actual"""
        with self.lock:
            return copy.deepcopy(self)
    
    def validar_consistencia(self):
        """Validación de consistencia del estado global"""
        inconsistencias = []
        
        # Validar conservación de dinero
        dinero_total_calculado = (
            self.mercado.dinero_circulacion +
            self.sistema_bancario.dinero_en_bancos +
            sum(agente.dinero for agente in self.agentes_ia.agentes_activos)
        )
        
        if abs(dinero_total_calculado - self.mercado.dinero_total_inicial) > 0.01:
            inconsistencias.append("Violación de conservación de dinero")
        
        # Validar balances de inventario
        for bien in self.mercado.bienes_disponibles:
            inventario_total = self._calcular_inventario_total(bien)
            if inventario_total < 0:
                inconsistencias.append(f"Inventario negativo para {bien}")
        
        return len(inconsistencias) == 0, inconsistencias
```

### Gestión de Transacciones

```python
class GestorTransacciones:
    """Gestión de transacciones con garantías ACID"""
    
    def __init__(self, coordinador_estado):
        self.coordinador_estado = coordinador_estado
        self.transacciones_activas = {}
        self.log_transacciones = []
        
    def iniciar_transaccion(self, transaccion_id, componentes_involucrados):
        """Inicio de transacción distribuida"""
        
        transaccion = TransaccionDistribuida(
            id=transaccion_id,
            componentes=componentes_involucrados,
            estado=EstadoTransaccion.INICIADA,
            timestamp_inicio=datetime.now(),
            snapshots_iniciales={}
        )
        
        # Capturar snapshots de estado inicial
        for componente in componentes_involucrados:
            transaccion.snapshots_iniciales[componente] = (
                self.coordinador_estado.obtener_snapshot_componente(componente)
            )
        
        self.transacciones_activas[transaccion_id] = transaccion
        return transaccion
    
    def ejecutar_transaccion(self, transaccion_id, operaciones):
        """Ejecución de transacción con protocolo 2PC"""
        
        transaccion = self.transacciones_activas[transaccion_id]
        
        # Fase 1: Preparar (2PC - Phase 1)
        preparacion_exitosa = True
        for componente in transaccion.componentes:
            if not self._preparar_componente(componente, operaciones):
                preparacion_exitosa = False
                break
        
        if preparacion_exitosa:
            # Fase 2: Confirmar (2PC - Phase 2)
            for componente in transaccion.componentes:
                self._confirmar_componente(componente, operaciones)
            
            transaccion.estado = EstadoTransaccion.CONFIRMADA
            self._log_transaccion_exitosa(transaccion)
        else:
            # Rollback
            self._rollback_transaccion(transaccion)
            transaccion.estado = EstadoTransaccion.ABORTADA
        
        # Limpiar transacción activa
        del self.transacciones_activas[transaccion_id]
        
        return transaccion.estado == EstadoTransaccion.CONFIRMADA
```

---

## APIs y Interfaces

### API REST para Control Externo

```python
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel

class ControladorSimulacion:
    """Controlador REST para el simulador"""
    
    def __init__(self):
        self.app = FastAPI(title="Simulador Mercado IA API", version="3.0")
        self.simulacion_activa = None
        self.configurar_rutas()
    
    def configurar_rutas(self):
        """Configuración de endpoints REST"""
        
        @self.app.post("/simulacion/iniciar")
        async def iniciar_simulacion(
            configuracion: ConfiguracionSimulacion,
            background_tasks: BackgroundTasks
        ):
            """Inicia una nueva simulación"""
            
            if self.simulacion_activa:
                raise HTTPException(400, "Simulación ya activa")
            
            # Validar configuración
            if not self._validar_configuracion(configuracion):
                raise HTTPException(400, "Configuración inválida")
            
            # Iniciar en background
            background_tasks.add_task(
                self._ejecutar_simulacion_background, configuracion
            )
            
            return {"status": "iniciada", "id": configuracion.id}
        
        @self.app.get("/simulacion/estado")
        async def obtener_estado_simulacion():
            """Obtiene el estado actual de la simulación"""
            
            if not self.simulacion_activa:
                raise HTTPException(404, "No hay simulación activa")
            
            return {
                "id": self.simulacion_activa.id,
                "ciclo_actual": self.simulacion_activa.ciclo_actual,
                "estado": self.simulacion_activa.estado,
                "metricas": self.simulacion_activa.obtener_metricas(),
                "agentes_activos": len(self.simulacion_activa.agentes_ia),
                "timestamp": datetime.now()
            }
        
        @self.app.post("/simulacion/intervenir")
        async def intervenir_simulacion(intervencion: IntervencionSimulacion):
            """Permite intervenciones en tiempo real"""
            
            if not self.simulacion_activa:
                raise HTTPException(404, "No hay simulación activa")
            
            resultado = self.simulacion_activa.aplicar_intervencion(intervencion)
            
            return {
                "intervencion_aplicada": intervencion.tipo,
                "resultado": resultado,
                "timestamp": datetime.now()
            }
```

### Interface de Plugin para Extensiones

```python
class InterfacePlugin:
    """Interface base para plugins del sistema"""
    
    def __init__(self, nombre: str, version: str):
        self.nombre = nombre
        self.version = version
        self.activo = False
        
    def inicializar(self, contexto_sistema):
        """Inicialización del plugin"""
        raise NotImplementedError
    
    def procesar_ciclo(self, ciclo: int, estado_sistema):
        """Procesamiento en cada ciclo"""
        raise NotImplementedError
    
    def finalizar(self):
        """Finalización y limpieza del plugin"""
        raise NotImplementedError

class GestorPlugins:
    """Gestor de plugins del sistema"""
    
    def __init__(self):
        self.plugins_registrados = {}
        self.plugins_activos = {}
        
    def registrar_plugin(self, plugin: InterfacePlugin):
        """Registro de un nuevo plugin"""
        
        # Validar plugin
        if not self._validar_plugin(plugin):
            raise ValueError(f"Plugin {plugin.nombre} no es válido")
        
        self.plugins_registrados[plugin.nombre] = plugin
    
    def activar_plugin(self, nombre_plugin, contexto_sistema):
        """Activación de un plugin registrado"""
        
        if nombre_plugin not in self.plugins_registrados:
            raise ValueError(f"Plugin {nombre_plugin} no registrado")
        
        plugin = self.plugins_registrados[nombre_plugin]
        
        try:
            plugin.inicializar(contexto_sistema)
            plugin.activo = True
            self.plugins_activos[nombre_plugin] = plugin
            
        except Exception as e:
            raise RuntimeError(f"Error activando plugin {nombre_plugin}: {e}")
    
    def ejecutar_plugins_ciclo(self, ciclo, estado_sistema):
        """Ejecución de todos los plugins activos en un ciclo"""
        
        resultados = {}
        
        for nombre, plugin in self.plugins_activos.items():
            try:
                resultado = plugin.procesar_ciclo(ciclo, estado_sistema)
                resultados[nombre] = resultado
                
            except Exception as e:
                print(f"Error en plugin {nombre}: {e}")
                resultados[nombre] = {"error": str(e)}
        
        return resultados
```

### Interface de Datos para Analytics

```python
class InterfaceDatosAnalytics:
    """Interface unificada para acceso a datos de analytics"""
    
    def __init__(self, coordinador_estado):
        self.coordinador_estado = coordinador_estado
        self.cache_consultas = {}
        
    def obtener_serie_temporal(self, metrica: str, ventana_ciclos: int = 50):
        """Obtiene serie temporal de una métrica específica"""
        
        cache_key = f"{metrica}_{ventana_ciclos}"
        
        if cache_key in self.cache_consultas:
            if self._cache_valido(cache_key):
                return self.cache_consultas[cache_key]
        
        # Construir serie temporal
        serie = self._construir_serie_temporal(metrica, ventana_ciclos)
        
        # Cachear resultado
        self.cache_consultas[cache_key] = {
            'data': serie,
            'timestamp': datetime.now()
        }
        
        return serie
    
    def obtener_metricas_agentes(self, filtros: Dict = None):
        """Obtiene métricas de agentes con filtros opcionales"""
        
        agentes = self.coordinador_estado.estado_global.agentes_ia.agentes_activos
        
        metricas = []
        for agente in agentes:
            metricas_agente = {
                'id': agente.id,
                'tipo': agente.tipo,
                'rendimiento': agente.calcular_rendimiento(),
                'decisiones_ciclo': len(agente.decisiones_recientes),
                'reputacion': agente.reputacion_actual,
                'conexiones_red': len(agente.conexiones_red_social)
            }
            
            # Aplicar filtros
            if not filtros or self._aplicar_filtros_agente(metricas_agente, filtros):
                metricas.append(metricas_agente)
        
        return metricas
    
    def generar_reporte_completo(self, formato='json'):
        """Genera reporte completo del estado del sistema"""
        
        estado = self.coordinador_estado.estado_global
        
        reporte = {
            'timestamp': datetime.now(),
            'ciclo_actual': estado.ciclo_actual,
            'metricas_economicas': {
                'pib': estado.mercado.pib_actual,
                'inflacion': estado.mercado.inflacion_actual,
                'desempleo': estado.mercado_trabajo.tasa_desempleo,
                'liquidez': estado.sistema_bancario.liquidez_total
            },
            'metricas_ia': {
                'agentes_activos': len(estado.agentes_ia.agentes_activos),
                'transacciones_ia': estado.agentes_ia.transacciones_totales,
                'coaliciones_activas': len(estado.agentes_ia.coaliciones_activas),
                'eficiencia_global': estado.agentes_ia.eficiencia_global
            },
            'metricas_sistema': {
                'tiempo_ciclo_promedio': estado.metricas_rendimiento['tiempo_ciclo'],
                'uso_memoria': estado.metricas_rendimiento['memoria_mb'],
                'eventos_procesados': estado.metricas_rendimiento['eventos_totales']
            }
        }
        
        if formato == 'json':
            return reporte
        elif formato == 'csv':
            return self._convertir_a_csv(reporte)
        elif formato == 'html':
            return self._generar_html_reporte(reporte)
        else:
            raise ValueError(f"Formato {formato} no soportado")
```

---

## Conclusión

Los patrones de integración implementados en este simulador proporcionan una base robusta para la comunicación y coordinación entre sistemas complejos. La arquitectura de capas permite extensibilidad mientras mantiene la separación de responsabilidades, y los patrones de comunicación aseguran que la información fluya de manera eficiente y consistente.

El sistema de sincronización garantiza que todos los componentes operen de manera coordinada, mientras que la gestión de estado centralizada mantiene la consistencia global. Las APIs y interfaces proporcionan puntos de extensión claros para desarrolladores que quieran agregar funcionalidad o integrar sistemas externos.

Esta arquitectura ha sido diseñada específicamente para soportar la complejidad emergente de un sistema multi-agente mientras proporciona las garantías de consistencia y rendimiento necesarias para una simulación económica realista.