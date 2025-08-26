# Documentación Técnica - Simulador de Mercado con Agentes IA Hiperrealistas

## Tabla de Contenidos
1. [Arquitectura General del Sistema](#arquitectura-general-del-sistema)
2. [Ecosistema de Agentes IA](#ecosistema-de-agentes-ia)
3. [Sistemas Económicos](#sistemas-económicos)
4. [Protocolos de Comunicación](#protocolos-de-comunicación)
5. [Flujos de Datos](#flujos-de-datos)
6. [Patrones de Integración](#patrones-de-integración)
7. [Guía para Desarrolladores](#guía-para-desarrolladores)

---

## Arquitectura General del Sistema

### Visión General
El simulador implementa una arquitectura de microservicios centrada en agentes inteligentes que interactúan en un mercado económico simulado. La arquitectura se divide en cuatro capas principales:

```
┌─────────────────────────────────────────────────────────────┐
│                    CAPA DE PRESENTACIÓN                     │
│  Dashboard, API REST, Reportes, Visualizaciones            │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                  CAPA DE AGENTES IA                        │
│  IntegradorAgentesIA, OrquestadorAgentesIA,                │
│  ConsumidorIA, EmpresaIA, RedSocialAgentesIA               │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                 CAPA DE SISTEMAS ECONÓMICOS                │
│  SistemaBancario, MercadoTrabajo, GestorCrisis,           │
│  BancoCentralAvanzado, PreciosDinámicos                    │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                   CAPA DE MODELOS BASE                     │
│  Consumidor, Empresa, Mercado, Gobierno, Bien             │
└─────────────────────────────────────────────────────────────┘
```

### Componentes Principales

#### 1. Punto de Entrada (main.py)
- **Función**: Coordinador principal de la simulación
- **Responsabilidades**:
  - Carga de configuración desde JSON
  - Inicialización de todos los sistemas
  - Orquestación del ciclo de simulación
  - Integración de sistemas de IA, económicos y de monitoreo

#### 2. Configuración (src/config/)
- **ConfiguradorSimulacion.py**: Gestión centralizada de parámetros
- **ConfigEconomica.py**: Constantes y valores económicos realistas
- **DatosEconomicosReales.py**: Calibración con datos económicos reales

#### 3. Modelos Base (src/models/)
- **Bien**: Entidades económicas básicas con elasticidades por categoría
- **Consumidor**: Agentes económicos con comportamiento de consumo
- **Empresa/EmpresaProductora**: Entidades productivas con costos y capacidades
- **Mercado**: Coordinador de transacciones y métricas económicas
- **Gobierno**: Entidad reguladora con políticas fiscales

---

## Ecosistema de Agentes IA

### Arquitectura de IA Multi-Agente

El sistema de IA está diseñado como una red de agentes autónomos que aprenden, se comunican y colaboran:

```
┌─────────────────────────────────────────────────────────────┐
│                IntegradorAgentesIA                          │
│              (Coordinador Principal)                        │
│  ┌─────────────────────────────────────────────────────┐   │
│  │            OrquestadorAgentesIA                     │   │
│  │          (Registro y Coordinación)                  │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────┐ ┌─────────────────┐ ┌──────────────┐   │
│  │  ConsumidorIA   │ │   EmpresaIA     │ │ MercadoIA    │   │
│  │   (Agentes      │ │   (Agentes      │ │ (Central     │   │
│  │   Consumo)      │ │ Empresariales)  │ │ Inteligente) │   │
│  └─────────────────┘ └─────────────────┘ └──────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │            RedSocialAgentesIA                       │   │
│  │        (Relaciones y Coaliciones)                  │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │         SistemaDeepLearningIA                       │   │
│  │       (Redes Neuronales Especializadas)            │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### 1. IntegradorAgentesIA
**Ubicación**: `src/ai/IntegradorAgentesIA.py`
**Función**: Coordinador maestro del ecosistema de IA

**Responsabilidades principales**:
- Inicialización y configuración de todos los componentes de IA
- Coordinación de ciclos de mercado con IA
- Gestión de fases: comunicación, negociación, aprendizaje
- Integración con el mercado económico principal

**Ciclo de Ejecución**:
```python
def ejecutar_ciclo_mercado(self, duracion_minutos=5):
    """
    Fases del ciclo IA:
    1. Comunicación entre agentes
    2. Negociación y transacciones  
    3. Aprendizaje y adaptación
    4. Actualización de estado
    """
    for ciclo in range(self.num_ciclos):
        # Fase 1: Comunicación
        self._fase_comunicacion_agentes()
        
        # Fase 2: Negociaciones 
        transacciones = self._fase_negociacion_transacciones()
        
        # Fase 3: Aprendizaje
        self._fase_aprendizaje_adaptacion(transacciones)
        
        # Fase 4: Coordinación
        self.orquestador_ia.coordinar_agentes_ia()
```

### 2. OrquestadorAgentesIA
**Ubicación**: `src/ai/OrquestadorAgentesIA.py`
**Función**: Registro, coordinación y monitoreo de agentes

**Características clave**:
- **Registro de Agentes**: Sistema de registro centralizado con capacidades
- **Hub de Comunicaciones**: Gestión de protocolos de comunicación por agente
- **Estadísticas de Sistema**: Monitoreo de rendimiento y actividad
- **Detección de Patrones**: Identificación de comportamientos emergentes

**Estructura de Registro de Agente**:
```python
class RegistroAgente:
    def __init__(self, agente_id: str, tipo: str, capacidades: List[str]):
        self.agente_id = agente_id
        self.tipo = tipo  # 'consumidor', 'empresa', 'gobierno'
        self.capacidades = capacidades
        self.activo = True
        self.registrado_en = datetime.now()
        self.reputacion = 0.5
        self.metricas_rendimiento = {}
        self.conexiones_red = []
```

**Coordinación Inteligente**:
- Detección de asimetrías de información
- Cálculo de riesgo sistémico
- Gestión de liquidez del mercado
- Coordinación de decisiones distribuidas

### 3. Agentes Especializados

#### ConsumidorIA
**Ubicación**: `src/ai/ConsumidorIA.py`
**Función**: Agentes consumidores con comportamiento inteligente

**Capacidades**:
- **Toma de Decisiones Adaptativa**: Basada en experiencia y preferencias aprendidas
- **Memoria de Transacciones**: Sistema de memoria episódica para decisiones futuras
- **Negociación Inteligente**: Capacidad de negociar precios y condiciones
- **Formación de Grupos**: Colaboración con otros consumidores para poder de compra

**Proceso de Decisión**:
```python
def tomar_decision_compra(self, estado_mercado):
    """
    Proceso de decisión multi-factor:
    1. Análisis de necesidades actuales
    2. Evaluación de precios y calidad
    3. Consulta de memoria histórica
    4. Consideración de relaciones sociales
    5. Decisión final con incertidumbre
    """
    necesidades = self.analizar_necesidades()
    opciones = self.evaluar_opciones_mercado(estado_mercado)
    experiencia = self.consultar_memoria_episodica()
    contexto_social = self.analizar_red_social()
    
    return self.motor_decision.decidir(
        necesidades, opciones, experiencia, contexto_social
    )
```

#### EmpresaIA  
**Ubicación**: `src/ai/EmpresaIA.py`
**Función**: Agentes empresariales con estrategia competitiva

**Capacidades Estratégicas**:
- **Optimización de Precios**: ML para encontrar precios óptimos
- **Gestión de Inventario**: Predicción de demanda y optimización de stock
- **Análisis Competitivo**: Monitoreo y respuesta a competidores
- **Innovación Estratégica**: Desarrollo de nuevos productos/servicios

**Estrategias Empresariales**:
```python
def generar_estrategia_ciclo(self, ciclo):
    """
    Estrategia empresarial integrada:
    1. Análisis de mercado y competencia
    2. Optimización de pricing dinámico
    3. Planificación de producción
    4. Estrategias de marketing
    5. Decisiones de inversión
    """
    return {
        'ajuste_precios': self.optimizar_precios_ml(),
        'nivel_produccion': self.planificar_produccion(),
        'inversion_marketing': self.calcular_inversion_marketing(),
        'estrategia_competitiva': self.analizar_competencia()
    }
```

### 4. Sistemas de Soporte IA

#### AgentMemorySystem
**Ubicación**: `src/ai/AgentMemorySystem.py`
**Función**: Sistema de memoria avanzado para agentes

**Tipos de Memoria**:
- **Memoria Episódica**: Experiencias específicas de transacciones
- **Memoria Semántica**: Conocimiento general sobre el mercado
- **Memoria de Trabajo**: Información temporal para decisiones inmediatas

#### IADecisionEngine
**Ubicación**: `src/ai/IADecisionEngine.py`
**Función**: Motor de decisiones basado en IA

**Componentes**:
- Análisis de estado del mercado
- Evaluación de opciones múltiples
- Cálculo de utilidad esperada
- Gestión de incertidumbre

#### SistemaDeepLearningIA
**Ubicación**: `src/ai/SistemaDeepLearningIA.py`
**Función**: Redes neuronales especializadas

**Redes Especializadas**:
- **Predicción de Precios**: Forecasting de tendencias de precios
- **Detección de Patrones**: Identificación de comportamientos emergentes
- **Optimización de Estrategia**: Mejora continua de decisiones
- **Evaluación de Riesgos**: Análisis de riesgos sistémicos

---

## Sistemas Económicos

### Arquitectura de Sistemas Económicos

Los sistemas económicos proporcionan la infraestructura realista sobre la cual operan los agentes IA:

```
┌─────────────────────────────────────────────────────────────┐
│                    SISTEMAS ECONÓMICOS                      │
│                                                             │
│  ┌─────────────────┐ ┌─────────────────┐ ┌──────────────┐   │
│  │ BancoCentral    │ │ SistemaBancario │ │ MercadoTrabajo│   │
│  │ Avanzado        │ │                 │ │               │   │
│  └─────────────────┘ └─────────────────┘ └──────────────┘   │
│  ┌─────────────────┐ ┌─────────────────┐ ┌──────────────┐   │
│  │ PreciosDinámicos│ │ GestorCrisis    │ │ AnalyticsML  │   │
│  │                 │ │                 │ │               │   │
│  └─────────────────┘ └─────────────────┘ └──────────────┘   │
│  ┌─────────────────┐ ┌─────────────────┐                   │
│  │ValidadorEconomico│ │ModelosEconomicos│                   │
│  │                 │ │ Avanzados       │                   │
│  └─────────────────┘ └─────────────────┘                   │
└─────────────────────────────────────────────────────────────┘
```

### 1. Sistema Bancario y Monetario

#### BancoCentralAvanzado
**Ubicación**: `src/systems/BancoCentralAvanzado.py`
**Función**: Política monetaria automática con Taylor Rule

**Políticas Implementadas**:
- **Regla de Taylor**: Ajuste automático de tasas de interés
- **Control de Inflación**: Medidas anti-inflacionarias de emergencia
- **Estímulo Económico**: Respuesta a recesiones y crisis
- **Estabilización de Mercados**: Intervención en crisis sistémicas

**Proceso de Decisión Monetaria**:
```python
def ejecutar_politica_monetaria(self, estado_economia):
    """
    Proceso de política monetaria:
    1. Análisis de indicadores clave (inflación, desempleo, PIB)
    2. Aplicación de Regla de Taylor
    3. Detección de condiciones de emergencia
    4. Implementación de medidas correctivas
    """
    inflacion = estado_economia['inflacion']
    desempleo = estado_economia['desempleo']
    
    if inflacion > self.umbral_emergencia_inflacion:
        return self.politica_emergencia_antiinflacion()
    elif desempleo > self.umbral_emergencia_desempleo:
        return self.politica_estimulo_economico()
    else:
        return self.aplicar_regla_taylor(inflacion, desempleo)
```

#### SistemaBancario
**Ubicación**: `src/systems/SistemaBancario.py`
**Función**: Sistema bancario comercial completo

**Características**:
- **Múltiples Bancos**: Competencia entre instituciones financieras
- **Evaluación de Riesgo**: Algoritmos de scoring crediticio
- **Gestión de Liquidez**: Manejo de reservas y capital
- **Productos Financieros**: Préstamos, depósitos, inversiones

### 2. Mercado Laboral Avanzado

#### MercadoTrabajo  
**Ubicación**: `src/systems/MercadoTrabajo.py`
**Función**: Simulación realista del mercado laboral

**Componentes**:
- **Perfiles de Habilidades**: Trabajadores con competencias específicas
- **Proceso de Contratación**: Matching entre ofertas y demandas
- **Negociación Salarial**: Determinación de salarios por competencia
- **Sindicalización**: Representación colectiva de trabajadores

### 3. Sistema de Precios Dinámicos

#### PreciosDinámicos
**Ubicación**: `src/systems/PreciosDinamicos.py`
**Función**: Mecanismo de formación de precios realista

**Algoritmos**:
- **Oferta y Demanda**: Equilibrio automático por categoría de bien
- **Elasticidad Diferenciada**: Respuesta específica por tipo de producto
- **Inercia de Precios**: Resistencia al cambio para realismo
- **Shock de Mercado**: Respuesta a crisis y eventos externos

### 4. Sistemas de Crisis y Estabilidad

#### GestorCrisis
**Ubicación**: `src/systems/GestorCrisis.py`
**Función**: Detección y gestión de crisis económicas

**Tipos de Crisis Detectadas**:
- Crisis bancarias (insolvencia, corridas bancarias)
- Crisis de demanda (caída del consumo)
- Crisis de oferta (disrupciones de producción)
- Crisis sistémicas (colapso general)

#### ValidadorEconomico
**Ubicación**: `src/systems/ValidadorEconomico.py`
**Función**: Validación de estabilidad económica

**Validaciones**:
- Rangos normales de inflación y desempleo
- Estabilidad de precios por sector
- Coherencia de métricas macroeconómicas
- Alertas de anomalías sistémicas

---

## Protocolos de Comunicación

### Sistema de Comunicación Multi-Agente

#### AgentCommunicationProtocol
**Ubicación**: `src/ai/AgentCommunicationProtocol.py`
**Función**: Protocolo estándar de comunicación entre agentes

**Arquitectura de Comunicación**:
```
┌─────────────────────────────────────────────────────────────┐
│                 PROTOCOLOS DE COMUNICACIÓN                  │
│                                                             │
│  ┌─────────────────┐ ┌─────────────────┐ ┌──────────────┐   │
│  │   Mensajería    │ │   Negociación   │ │   Broadcast  │   │
│  │   Punto-a-Punto │ │   Estructurada  │ │   Mercado    │   │
│  └─────────────────┘ └─────────────────┘ └──────────────┘   │
│  ┌─────────────────┐ ┌─────────────────┐ ┌──────────────┐   │
│  │   Alianzas      │ │ Señales Mercado │ │  Reputación  │   │
│  │   Estratégicas  │ │                 │ │              │   │
│  └─────────────────┘ └─────────────────┘ └──────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

**Tipos de Mensajes**:
```python
class TipoMensaje(Enum):
    OFERTA_COMPRA = "oferta_compra"
    OFERTA_VENTA = "oferta_venta"
    NEGOCIACION = "negociacion"
    ALIANZA = "alianza"
    INFORMACION_MERCADO = "info_mercado"
    REPUTACION = "reputacion"
    EMERGENCIA = "emergencia"
```

**Estructura de Mensaje**:
```python
@dataclass
class Mensaje:
    id: str
    remitente: str
    destinatario: str
    tipo: TipoMensaje
    contenido: Dict[str, Any]
    prioridad: int
    timestamp: datetime
    requiere_respuesta: bool
    canal: str = "default"
```

**Proceso de Comunicación**:
1. **Envío**: Agente crea mensaje y lo envía via protocolo
2. **Enrutamiento**: Hub de comunicaciones dirige el mensaje
3. **Cola de Prioridad**: Mensajes ordenados por importancia
4. **Procesamiento**: Agente destinatario procesa en orden
5. **Respuesta**: Respuesta automática si es requerida

### Negociación Inteligente

**Proceso de Negociación**:
```python
def iniciar_negociacion(self, contraparte: str, objeto: str, términos_iniciales: Dict):
    """
    Proceso de negociación multi-ronda:
    1. Propuesta inicial
    2. Contra-propuestas iterativas
    3. Evaluación de utilidad mutua
    4. Convergencia o ruptura
    """
    negociacion = Negociacion(
        participantes=[self.agente_id, contraparte],
        objeto=objeto,
        terminos_iniciales=términos_iniciales
    )
    
    return self.gestionar_negociacion(negociacion)
```

### Red Social de Agentes

#### RedSocialAgentesIA
**Ubicación**: `src/ai/RedSocialAgentesIA.py`
**Función**: Gestión de relaciones sociales entre agentes

**Tipos de Relaciones**:
- **Competencia**: Rivalidad por recursos/mercados
- **Colaboración**: Alianzas mutuamente beneficiosas
- **Neutralidad**: Sin relación especial
- **Dependencia**: Relaciones proveedor-cliente

**Formación de Coaliciones**:
```python
def formar_coalicion_automatica(self) -> Optional[CoalicionAgentes]:
    """
    Algoritmo de formación de coaliciones:
    1. Identificar oportunidades de colaboración
    2. Evaluar compatibilidad entre agentes
    3. Calcular beneficios esperados
    4. Establecer términos y duración
    """
    oportunidades = self.detectar_oportunidades_coalicion()
    agentes_compatibles = self.evaluar_compatibilidad()
    
    if self.beneficio_mutuo_suficiente(oportunidades, agentes_compatibles):
        return self.crear_coalicion(agentes_compatibles)
    
    return None
```

---

## Flujos de Datos

### Ciclo Principal de Simulación

El flujo de datos sigue un patrón cíclico donde cada componente procesa y enriquece la información:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   INICIALIZACIÓN │───▶│ CONFIGURACIÓN   │───▶│ CREACIÓN AGENTES │
│   - main.py     │    │ - JSON configs  │    │ - Consumidores   │
│   - Logging     │    │ - Validaciones  │    │ - Empresas       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ REPORTE FINAL   │◀───│ ANÁLISIS CICLO  │◀───│ SISTEMAS ACTIVOS │
│ - Dashboard     │    │ - Métricas      │    │ - Banking       │
│ - Exportación   │    │ - ML Analytics  │    │ - Trabajo       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ ACTUALIZACIÓN   │◀───│ PROCESAMIENTO   │◀───│ CICLO ECONÓMICO │
│ - Estado Global │    │ - Transacciones │    │ - Precios       │
│ - Métricas      │    │ - Decisiones IA │    │ - Demanda       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Flujo de Datos de Agentes IA

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ ESTADO MERCADO  │───▶│ ANÁLISIS AGENTE │───▶│ DECISIÓN IA     │
│ - Precios       │    │ - Memoria       │    │ - Compra/Venta  │
│ - Inventarios   │    │ - Preferencias  │    │ - Negociación   │
│ - Competencia   │    │ - Red Social    │    │ - Alianzas      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ ACTUALIZACIÓN   │◀───│ EJECUCIÓN       │◀───│ COMUNICACIÓN    │
│ - Memoria       │    │ - Transacciones │    │ - Mensajes      │
│ - Reputación    │    │ - Contratos     │    │ - Coordinación  │
│ - Aprendizaje   │    │ - Relaciones    │    │ - Sincronización│
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Integración de Datos Cross-Sistema

**Puntos de Integración Clave**:
1. **Mercado ↔ Agentes IA**: Estado de mercado → Decisiones inteligentes
2. **Sistema Bancario ↔ Agentes**: Crédito y liquidez → Capacidad de compra
3. **Precios Dinámicos ↔ IA**: Demanda IA → Ajustes de precios
4. **Analytics ML ↔ Todo**: Datos históricos → Predicciones y optimizaciones

---

## Patrones de Integración

### Patrón Observer para Estado de Mercado

Los agentes IA se suscriben a cambios en el estado del mercado:

```python
class EstadoMercadoObservable:
    def __init__(self):
        self.observadores = []
        self.estado_actual = {}
    
    def agregar_observador(self, agente_ia):
        self.observadores.append(agente_ia)
    
    def notificar_cambio_estado(self, nuevo_estado):
        for observador in self.observadores:
            observador.actualizar_estado_mercado(nuevo_estado)
```

### Patrón Strategy para Decisiones IA

Diferentes estrategias de decisión según el contexto:

```python
class EstrategiaDecision:
    def decidir(self, contexto):
        raise NotImplementedError

class EstrategiaConservadora(EstrategiaDecision):
    def decidir(self, contexto):
        # Lógica conservadora
        pass

class EstrategiaAgresiva(EstrategiaDecision):
    def decidir(self, contexto):
        # Lógica agresiva
        pass
```

### Patrón Command para Transacciones

Encapsulación de operaciones económicas:

```python
class ComandoTransaccion:
    def __init__(self, comprador, vendedor, bien, cantidad, precio):
        self.comprador = comprador
        self.vendedor = vendedor
        self.bien = bien
        self.cantidad = cantidad
        self.precio = precio
    
    def ejecutar(self):
        # Lógica de transacción
        pass
    
    def deshacer(self):
        # Rollback si es necesario
        pass
```

### Patrón Factory para Creación de Agentes

Creación flexible de diferentes tipos de agentes:

```python
class FactoriaAgentesIA:
    @staticmethod
    def crear_agente(tipo: str, configuracion: Dict) -> AgenteIA:
        if tipo == "consumidor":
            return ConsumidorIA(configuracion)
        elif tipo == "empresa":
            return EmpresaIA(configuracion)
        elif tipo == "gobierno":
            return GobiernoIA(configuracion)
        else:
            raise ValueError(f"Tipo de agente desconocido: {tipo}")
```

---

## Guía para Desarrolladores

### Configuración del Entorno de Desarrollo

1. **Requisitos del Sistema**:
   ```bash
   # Python 3.12+
   python3 --version
   
   # Dependencias
   python3 -m pip install -r requirements.txt
   ```

2. **Estructura del Proyecto**:
   ```
   mercado/
   ├── main.py                    # Punto de entrada principal
   ├── config_simulacion.json    # Configuración principal
   ├── src/
   │   ├── ai/                   # Sistema de agentes IA
   │   ├── models/               # Modelos económicos base
   │   ├── systems/              # Sistemas económicos avanzados
   │   ├── config/               # Gestión de configuración
   │   └── utils/                # Utilidades y logging
   ├── tests/                    # Suite de tests
   └── docs/                     # Documentación
   ```

### Extensión del Sistema

#### Agregar Nuevo Tipo de Agente IA

1. **Crear clase del agente**:
   ```python
   # src/ai/NuevoAgenteIA.py
   from .IADecisionEngine import IADecisionEngine
   from .AgentMemorySystem import AgentMemorySystem
   
   class NuevoAgenteIA:
       def __init__(self, configuracion):
           self.motor_decision = IADecisionEngine()
           self.memoria = AgentMemorySystem()
           # Inicialización específica
   ```

2. **Registrar en el sistema**:
   ```python
   # En IntegradorAgentesIA.py
   def _crear_nuevos_agentes_ia(self):
       for i in range(self.configuracion.num_nuevos_agentes):
           agente = NuevoAgenteIA(configuracion)
           self.nuevos_agentes[f"nuevo_{i}"] = agente
   ```

3. **Actualizar factory**:
   ```python
   # En FactoriaAgentesIA.py
   elif tipo == "nuevo_tipo":
       return NuevoAgenteIA(configuracion)
   ```

#### Agregar Nuevo Sistema Económico

1. **Crear sistema**:
   ```python
   # src/systems/NuevoSistema.py
   class NuevoSistema:
       def __init__(self, mercado):
           self.mercado = mercado
           self.activo = True
       
       def procesar_ciclo(self, ciclo):
           # Lógica del sistema
           pass
   ```

2. **Integrar en main.py**:
   ```python
   # En función de configuración
   if config.get('activar_nuevo_sistema'):
       nuevo_sistema = NuevoSistema(mercado)
       mercado.integrar_sistema(nuevo_sistema)
   ```

### Debugging y Monitoreo

#### Sistema de Logging

```python
# Uso del logger
from src.utils.SimuladorLogger import SimuladorLogger

logger = SimuladorLogger()
logger.info("SISTEMA", "Información del sistema")
logger.warning("AGENTE", "Advertencia de agente")
logger.error("ERROR", "Error crítico")
```

#### Métricas y Analytics

```python
# Acceso a métricas del sistema
estado = integrador_ia.obtener_estado_completo()
print(f"Eficiencia: {estado['estadisticas']['eficiencia_global']}")
print(f"Agentes activos: {estado['estadisticas']['agentes_activos']}")
```

### Testing

#### Tests Unitarios
```bash
# Ejecutar tests específicos
python3 -m pytest tests/unit/test_modelos_basicos.py -v

# Tests de agentes IA
python3 -m pytest tests/unit/test_agentes_ia.py -v
```

#### Tests de Integración
```bash
# Test completo del sistema
python3 -m pytest tests/integration/test_simulacion_completa.py -v
```

#### Validación Manual
```bash
# Simulación rápida para validación
python3 main.py --escenario base --seed 42

# Con agentes IA
echo "1" | python3 ejemplo_uso_completo.py
```

### Configuración Avanzada

#### Configuración de Agentes IA

```json
{
  "agentes_ia": {
    "activar": true,
    "num_consumidores_ia": 15,
    "num_empresas_ia": 6,
    "entrenar_automaticamente": true,
    "activar_logs_detallados": true,
    "duracion_simulacion_minutos": 5
  }
}
```

#### Configuración de Sistemas Económicos

```json
{
  "sistemas_avanzados": {
    "activar_banco_central": true,
    "activar_precios_dinamicos": true,
    "activar_sistema_bancario": true,
    "activar_mercado_trabajo": true,
    "activar_validador_economico": true
  }
}
```

### Mejores Prácticas

1. **Separación de Responsabilidades**: Cada sistema debe tener una responsabilidad clara
2. **Inyección de Dependencias**: Usar configuración para controlar dependencias
3. **Logging Estructurado**: Usar categorías consistentes para logging
4. **Testing Exhaustivo**: Cubrir tanto unidades como integración
5. **Configuración Externa**: Parametrizar todo via JSON/configuración
6. **Documentación del Código**: Docstrings detallados para APIs públicas

---

## Conclusión

Este simulador representa un sistema complejo de agentes IA que interactúan en un entorno económico realista. La arquitectura modular permite extensibilidad mientras mantiene la coherencia del sistema. Los patrones de integración facilitan la comunicación entre componentes, y los flujos de datos aseguran que la información fluya correctamente a través de todo el sistema.

Para desarrolladores que quieran contribuir o extender el sistema, esta documentación proporciona la base técnica necesaria para entender las interacciones complejas entre agentes inteligentes, sistemas económicos y protocolos de comunicación.