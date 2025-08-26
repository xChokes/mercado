# Guía Técnica - Comportamientos y Decisiones de Agentes IA

## Tabla de Contenidos
1. [Sistema de Decisiones IA](#sistema-de-decisiones-ia)
2. [Comportamientos de Agentes Especializados](#comportamientos-de-agentes-especializados)
3. [Protocolos de Interacción](#protocolos-de-interacción)
4. [Aprendizaje y Adaptación](#aprendizaje-y-adaptación)
5. [Emergencia y Comportamientos Complejos](#emergencia-y-comportamientos-complejos)

---

## Sistema de Decisiones IA

### Motor de Decisión Central (IADecisionEngine)

El `IADecisionEngine` es el núcleo del sistema de toma de decisiones para todos los agentes IA. Implementa un modelo híbrido que combina lógica programada, aprendizaje por refuerzo y redes neuronales.

#### Estructura del Estado de Mercado

```python
@dataclass
class EstadoMercado:
    """Estado completo del mercado para decisiones IA"""
    # Métricas económicas
    pib_actual: float
    inflacion: float
    desempleo: float
    liquidez_total: float
    
    # Precios por categoría
    precios_por_categoria: Dict[str, float]
    tendencias_precios: Dict[str, List[float]]  # Histórico
    
    # Estado de la competencia
    num_competidores: Dict[str, int]
    market_share: Dict[str, float]
    
    # Información social
    sentimiento_mercado: float  # -1.0 a 1.0
    nivel_cooperacion: float
    coaliciones_activas: List[str]
    
    # Señales de alerta
    crisis_detectada: bool
    oportunidades_emergentes: List[Dict]
```

#### Proceso de Toma de Decisiones

```python
class IADecisionEngine:
    def __init__(self):
        self.modelos_decision = {
            'utilidad_esperada': ModeloUtilidadEsperada(),
            'teoria_juegos': ModeloTeoriaJuegos(),
            'heuristicas': ModeloHeuristicas(),
            'red_neuronal': RedNeuronalDecision()
        }
        self.pesos_modelos = {'utilidad': 0.4, 'juegos': 0.3, 'heuristic': 0.2, 'neural': 0.1}
    
    def tomar_decision(self, opciones: List[OpcionDecision], 
                      estado: EstadoMercado, 
                      contexto_agente: Dict) -> DecisionIA:
        """
        Proceso de decisión multi-modelo:
        
        1. Evaluación por Utilidad Esperada
        2. Análisis de Teoría de Juegos
        3. Aplicación de Heurísticas
        4. Predicción de Red Neuronal
        5. Combinación ponderada
        6. Selección final con incertidumbre
        """
        evaluaciones = {}
        
        # 1. Modelo de Utilidad Esperada
        evaluaciones['utilidad'] = self.modelos_decision['utilidad_esperada'].evaluar(
            opciones, estado, contexto_agente
        )
        
        # 2. Análisis de Teoría de Juegos
        evaluaciones['juegos'] = self.modelos_decision['teoria_juegos'].evaluar(
            opciones, estado, contexto_agente
        )
        
        # 3. Heurísticas basadas en experiencia
        evaluaciones['heuristicas'] = self.modelos_decision['heuristicas'].evaluar(
            opciones, estado, contexto_agente
        )
        
        # 4. Red neuronal predictiva
        evaluaciones['neural'] = self.modelos_decision['red_neuronal'].predecir(
            opciones, estado, contexto_agente
        )
        
        # 5. Combinación ponderada
        decision_final = self._combinar_evaluaciones(evaluaciones)
        
        return decision_final
```

### Modelos de Decisión Especializados

#### 1. Modelo de Utilidad Esperada
```python
class ModeloUtilidadEsperada:
    """Evaluación basada en maximización de utilidad"""
    
    def evaluar(self, opciones, estado, contexto):
        utilidades = []
        
        for opcion in opciones:
            # Calcular utilidad esperada
            beneficio_esperado = self._calcular_beneficio(opcion, estado)
            riesgo = self._evaluar_riesgo(opcion, estado)
            incertidumbre = self._medir_incertidumbre(opcion, estado)
            
            # Función de utilidad con aversión al riesgo
            utilidad = beneficio_esperado - (riesgo * contexto['aversion_riesgo']) - incertidumbre
            utilidades.append(utilidad)
        
        return utilidades
```

#### 2. Modelo de Teoría de Juegos
```python
class ModeloTeoriaJuegos:
    """Análisis estratégico considerando otros agentes"""
    
    def evaluar(self, opciones, estado, contexto):
        evaluaciones = []
        
        for opcion in opciones:
            # Predecir respuestas de otros agentes
            respuestas_esperadas = self._predecir_respuestas_competidores(opcion, estado)
            
            # Calcular equilibrio de Nash aproximado
            payoff_nash = self._calcular_equilibrio_nash(opcion, respuestas_esperadas)
            
            # Evaluar estabilidad de la estrategia
            estabilidad = self._evaluar_estabilidad_estrategia(opcion, estado)
            
            evaluacion = payoff_nash * estabilidad
            evaluaciones.append(evaluacion)
        
        return evaluaciones
```

#### 3. Modelo de Heurísticas
```python
class ModeloHeuristicas:
    """Reglas de decisión basadas en experiencia"""
    
    def __init__(self):
        self.heuristicas = [
            HeuristicaSeguridad(),      # Evitar decisiones muy arriesgadas
            HeuristicaTendencia(),      # Seguir tendencias del mercado
            HeuristicaDiversificacion(),  # Diversificar riesgos
            HeuristicaOportunidad(),    # Aprovechar oportunidades
        ]
    
    def evaluar(self, opciones, estado, contexto):
        evaluaciones_finales = []
        
        for opcion in opciones:
            evaluacion_total = 0
            
            for heuristica in self.heuristicas:
                peso = heuristica.peso
                evaluacion = heuristica.aplicar(opcion, estado, contexto)
                evaluacion_total += peso * evaluacion
            
            evaluaciones_finales.append(evaluacion_total)
        
        return evaluaciones_finales
```

---

## Comportamientos de Agentes Especializados

### ConsumidorIA - Comportamientos de Consumo Inteligente

#### Proceso de Decisión de Compra

```python
class ConsumidorIA:
    def __init__(self, perfil_consumo):
        self.perfil = perfil_consumo
        self.memoria_episodica = AgentMemorySystem()
        self.preferencias_aprendidas = {}
        self.red_social = None
        self.presupuesto_disponible = 0
        
    def tomar_decision_compra(self, estado_mercado):
        """
        Proceso de decisión de compra multi-fase:
        
        1. Análisis de necesidades
        2. Evaluación de opciones
        3. Consulta de experiencia
        4. Influencia social
        5. Decisión final
        """
        
        # Fase 1: Análisis de necesidades
        necesidades = self._analizar_necesidades_actuales()
        
        # Fase 2: Evaluación de opciones disponibles
        opciones_compra = self._evaluar_opciones_mercado(estado_mercado, necesidades)
        
        # Fase 3: Consulta de memoria y experiencia
        experiencias_relevantes = self.memoria_episodica.recuperar_experiencias_similares(
            opciones_compra
        )
        
        # Fase 4: Influencia de la red social
        influencia_social = self._consultar_red_social(opciones_compra)
        
        # Fase 5: Decisión final integrada
        decision = self.motor_decision.tomar_decision(
            opciones_compra, estado_mercado, {
                'necesidades': necesidades,
                'experiencias': experiencias_relevantes,
                'influencia_social': influencia_social,
                'presupuesto': self.presupuesto_disponible
            }
        )
        
        return decision
```

#### Aprendizaje de Preferencias

```python
def actualizar_preferencias_por_experiencia(self, transaccion_realizada):
    """
    Actualización de preferencias basada en satisfacción:
    - Calidad vs Precio
    - Marca vs Genérico  
    - Novedad vs Familiar
    """
    satisfaccion = self._evaluar_satisfaccion_transaccion(transaccion_realizada)
    
    # Actualizar preferencias con algoritmo de aprendizaje
    caracteristicas = transaccion_realizada.caracteristicas_producto
    
    for caracteristica, valor in caracteristicas.items():
        preferencia_actual = self.preferencias_aprendidas.get(caracteristica, 0.5)
        
        # Aprendizaje con tasa adaptativa
        tasa_aprendizaje = 0.1 if satisfaccion > 0.7 else 0.05
        nueva_preferencia = preferencia_actual + tasa_aprendizaje * (satisfaccion - 0.5)
        
        self.preferencias_aprendidas[caracteristica] = np.clip(nueva_preferencia, 0, 1)
```

#### Comportamientos Sociales

```python
def formar_grupo_compra(self, otros_consumidores, objetivo_compra):
    """
    Formación de grupos de compra para mayor poder de negociación:
    1. Identificar consumidores con necesidades similares
    2. Evaluar beneficios de compra grupal
    3. Negociar términos del grupo
    4. Coordinar compra colectiva
    """
    candidatos_compatibles = []
    
    for otro_consumidor in otros_consumidores:
        compatibilidad = self._evaluar_compatibilidad_compra(
            otro_consumidor, objetivo_compra
        )
        
        if compatibilidad > 0.7:
            candidatos_compatibles.append((otro_consumidor, compatibilidad))
    
    if len(candidatos_compatibles) >= 2:
        grupo = self._formar_coalicion_compra(candidatos_compatibles, objetivo_compra)
        return grupo
    
    return None
```

### EmpresaIA - Estrategias Empresariales Inteligentes

#### Sistema de Estrategia Competitiva

```python
class EmpresaIA:
    def __init__(self, sector_industrial, recursos_iniciales):
        self.sector = sector_industrial
        self.recursos = recursos_iniciales
        self.estrategia_actual = EstrategiaEmpresarial()
        self.inteligencia_competitiva = SistemaInteligenciaCompetitiva()
        self.cartera_productos = {}
        
    def generar_estrategia_ciclo(self, ciclo):
        """
        Generación de estrategia empresarial integral:
        
        1. Análisis de mercado y competencia
        2. Optimización de pricing
        3. Planificación de producción
        4. Estrategia de marketing
        5. Decisiones de I+D
        6. Gestión de alianzas
        """
        
        # 1. Análisis de mercado
        analisis_mercado = self._analizar_mercado_competitivo()
        
        # 2. Optimización de precios
        estrategia_precios = self._optimizar_precios_dinamicos(analisis_mercado)
        
        # 3. Planificación de producción
        plan_produccion = self._planificar_produccion_inteligente(analisis_mercado)
        
        # 4. Marketing y posicionamiento
        estrategia_marketing = self._desarrollar_estrategia_marketing()
        
        # 5. Innovación y desarrollo
        plan_innovacion = self._planificar_innovacion()
        
        # 6. Alianzas estratégicas
        oportunidades_alianza = self._identificar_oportunidades_alianza()
        
        return EstrategiaEmpresarial(
            precios=estrategia_precios,
            produccion=plan_produccion,
            marketing=estrategia_marketing,
            innovacion=plan_innovacion,
            alianzas=oportunidades_alianza
        )
```

#### Inteligencia Competitiva

```python
class SistemaInteligenciaCompetitiva:
    """Sistema de análisis competitivo continuo"""
    
    def analizar_competidores(self, mercado_estado):
        """
        Análisis multi-dimensional de competidores:
        - Precios y posicionamiento
        - Cuota de mercado y tendencias
        - Fortalezas y debilidades
        - Movimientos estratégicos
        """
        competidores = mercado_estado.obtener_competidores(self.sector)
        analisis = {}
        
        for competidor in competidores:
            analisis[competidor.id] = {
                'market_share': self._calcular_market_share(competidor),
                'posicionamiento_precios': self._analizar_precios(competidor),
                'fortalezas': self._identificar_fortalezas(competidor),
                'vulnerabilidades': self._detectar_vulnerabilidades(competidor),
                'tendencia_estrategica': self._predecir_movimientos(competidor)
            }
        
        return analisis
    
    def detectar_oportunidades_mercado(self, analisis_competidores):
        """
        Detección de oportunidades estratégicas:
        - Nichos desatendidos
        - Debilidades de competidores
        - Tendencias emergentes
        - Cambios regulatorios
        """
        oportunidades = []
        
        # Analizar nichos de mercado
        nichos = self._detectar_nichos_desatendidos(analisis_competidores)
        oportunidades.extend(nichos)
        
        # Vulnerabilidades competitivas
        vulnerabilidades = self._mapear_vulnerabilidades_competitivas(analisis_competidores)
        oportunidades.extend(vulnerabilidades)
        
        # Tendencias de mercado
        tendencias = self._identificar_tendencias_emergentes()
        oportunidades.extend(tendencias)
        
        return sorted(oportunidades, key=lambda x: x.potencial, reverse=True)
```

#### Optimización de Precios ML

```python
def optimizar_precios_ml(self, producto, estado_mercado):
    """
    Optimización de precios usando machine learning:
    1. Predicción de elasticidad de demanda
    2. Análisis de sensibilidad al precio
    3. Optimización de margen vs volumen
    4. Consideración de competencia
    """
    
    # Modelo de elasticidad de demanda
    elasticidad_predicha = self.modelo_elasticidad.predecir(
        producto, estado_mercado
    )
    
    # Modelo de respuesta competitiva
    respuesta_competidores = self.modelo_competencia.predecir_respuesta(
        producto, estado_mercado
    )
    
    # Optimización multi-objetivo
    precio_optimo = self._optimizar_precio_multiobjetivo(
        producto=producto,
        elasticidad=elasticidad_predicha,
        respuesta_competidores=respuesta_competidores,
        objetivos=['margen', 'volumen', 'market_share']
    )
    
    return precio_optimo
```

---

## Protocolos de Interacción

### Protocolos de Negociación

#### Negociación Bilateral

```python
class ProtocoloNegociacionBilateral:
    """Protocolo estándar para negociaciones entre dos agentes"""
    
    def __init__(self, agente_a, agente_b, objeto_negociacion):
        self.participantes = [agente_a, agente_b]
        self.objeto = objeto_negociacion
        self.estado = EstadoNegociacion.INICIANDO
        self.historial_ofertas = []
        self.acuerdo_final = None
    
    def ejecutar_negociacion(self, max_rondas=10):
        """
        Proceso de negociación multi-ronda:
        
        1. Ofertas iniciales
        2. Contra-ofertas iterativas
        3. Evaluación de convergencia
        4. Acuerdo o ruptura
        """
        
        for ronda in range(max_rondas):
            # Turno del agente A
            oferta_a = self.participantes[0].generar_oferta(
                self.objeto, self.historial_ofertas
            )
            
            # Evaluación del agente B
            respuesta_b = self.participantes[1].evaluar_oferta(oferta_a)
            
            if respuesta_b.tipo == TipoRespuesta.ACEPTAR:
                self.acuerdo_final = oferta_a
                self.estado = EstadoNegociacion.ACUERDO
                break
            elif respuesta_b.tipo == TipoRespuesta.RECHAZAR:
                self.estado = EstadoNegociacion.RUPTURA
                break
            else:  # CONTRA_OFERTA
                # Intercambiar roles y continuar
                oferta_b = respuesta_b.contra_oferta
                self.historial_ofertas.append((oferta_a, oferta_b))
                
                # Evaluar convergencia
                if self._detectar_convergencia(oferta_a, oferta_b):
                    punto_medio = self._calcular_punto_medio(oferta_a, oferta_b)
                    self.acuerdo_final = punto_medio
                    self.estado = EstadoNegociacion.ACUERDO
                    break
        
        return self.acuerdo_final
```

#### Subastas Inteligentes

```python
class SubastaInteligente:
    """Sistema de subastas con agentes IA"""
    
    def __init__(self, tipo_subasta='vickrey'):
        self.tipo = tipo_subasta
        self.participantes = []
        self.ofertas = []
        self.ganador = None
    
    def ejecutar_subasta(self, objeto_subasta):
        """
        Proceso de subasta automatizada:
        1. Registro de participantes
        2. Recolección de ofertas
        3. Evaluación de ofertas
        4. Determinación de ganador
        """
        
        # Notificar oportunidad de subasta
        self._notificar_oportunidad_subasta(objeto_subasta)
        
        # Recopilar ofertas de agentes interesados
        for agente in self.participantes:
            oferta = agente.generar_oferta_subasta(objeto_subasta)
            if oferta:
                self.ofertas.append(oferta)
        
        # Evaluar ofertas según el tipo de subasta
        if self.tipo == 'vickrey':
            self.ganador = self._evaluar_subasta_vickrey()
        elif self.tipo == 'ingles':
            self.ganador = self._ejecutar_subasta_inglesa()
        
        return self.ganador
```

### Protocolos de Coalición

#### Formación de Alianzas

```python
class ProtocoloFormacionAlianza:
    """Protocolo para formación de alianzas estratégicas"""
    
    def detectar_oportunidad_alianza(self, agentes_mercado):
        """
        Detección automática de oportunidades de alianza:
        1. Análisis de complementariedad
        2. Evaluación de beneficios mutuos
        3. Compatibilidad estratégica
        """
        oportunidades = []
        
        for i, agente_a in enumerate(agentes_mercado):
            for j, agente_b in enumerate(agentes_mercado[i+1:], i+1):
                
                # Evaluar complementariedad
                complementariedad = self._evaluar_complementariedad(agente_a, agente_b)
                
                # Calcular beneficios mutuos
                beneficios = self._calcular_beneficios_mutuos(agente_a, agente_b)
                
                # Verificar compatibilidad
                compatibilidad = self._verificar_compatibilidad(agente_a, agente_b)
                
                if (complementariedad > 0.7 and 
                    beneficios['a'] > 0 and beneficios['b'] > 0 and
                    compatibilidad > 0.6):
                    
                    oportunidades.append(
                        OportunidadAlianza(agente_a, agente_b, beneficios, complementariedad)
                    )
        
        return sorted(oportunidades, key=lambda x: x.valor_total, reverse=True)
```

---

## Aprendizaje y Adaptación

### Sistema de Memoria de Agentes

#### Memoria Episódica

```python
class MemoriaEpisodica:
    """Sistema de memoria para experiencias específicas"""
    
    def __init__(self, capacidad_maxima=1000):
        self.episodios = deque(maxlen=capacidad_maxima)
        self.indice_semantico = {}
        
    def registrar_episodio(self, situacion, accion, resultado, satisfaccion):
        """Registra una experiencia completa"""
        episodio = Episodio(
            timestamp=datetime.now(),
            situacion=situacion,
            accion=accion,
            resultado=resultado,
            satisfaccion=satisfaccion,
            contexto=self._capturar_contexto()
        )
        
        self.episodios.append(episodio)
        self._actualizar_indice_semantico(episodio)
    
    def recuperar_experiencias_similares(self, situacion_actual, k=5):
        """Recupera experiencias similares para informar decisiones"""
        similitudes = []
        
        for episodio in self.episodios:
            similaridad = self._calcular_similaridad(
                situacion_actual, episodio.situacion
            )
            similitudes.append((episodio, similaridad))
        
        # Ordenar por similaridad y retornar top-k
        similitudes.sort(key=lambda x: x[1], reverse=True)
        return [episodio for episodio, _ in similitudes[:k]]
```

#### Memoria Semántica

```python
class MemoriaSemantica:
    """Conocimiento general sobre el mercado y patrones"""
    
    def __init__(self):
        self.conocimiento_general = {
            'patrones_mercado': {},
            'relaciones_causales': {},
            'reglas_generales': {},
            'conceptos_aprendidos': {}
        }
    
    def actualizar_conocimiento(self, nuevas_observaciones):
        """Actualiza conocimiento general basado en patrones observados"""
        
        # Detectar nuevos patrones
        patrones = self._detectar_patrones(nuevas_observaciones)
        
        for patron in patrones:
            if patron.confianza > 0.8:
                self.conocimiento_general['patrones_mercado'][patron.id] = patron
        
        # Actualizar relaciones causales
        relaciones = self._identificar_relaciones_causales(nuevas_observaciones)
        self.conocimiento_general['relaciones_causales'].update(relaciones)
        
        # Generalizar reglas
        reglas = self._generalizar_reglas(nuevas_observaciones)
        self.conocimiento_general['reglas_generales'].update(reglas)
```

### Aprendizaje por Refuerzo

#### Q-Learning para Estrategias

```python
class QlearningAgente:
    """Implementación de Q-Learning para aprendizaje de estrategias"""
    
    def __init__(self, acciones_posibles, tasa_aprendizaje=0.1, factor_descuento=0.9):
        self.q_table = defaultdict(lambda: defaultdict(float))
        self.acciones = acciones_posibles
        self.alpha = tasa_aprendizaje
        self.gamma = factor_descuento
        self.epsilon = 0.1  # Exploración
    
    def seleccionar_accion(self, estado):
        """Selección de acción con estrategia epsilon-greedy"""
        if random.random() < self.epsilon:
            # Exploración: acción aleatoria
            return random.choice(self.acciones)
        else:
            # Explotación: mejor acción conocida
            valores_q = {accion: self.q_table[estado][accion] for accion in self.acciones}
            return max(valores_q, key=valores_q.get)
    
    def actualizar_q_valor(self, estado, accion, recompensa, nuevo_estado):
        """Actualización de valores Q basada en experiencia"""
        mejor_q_futuro = max([self.q_table[nuevo_estado][a] for a in self.acciones])
        
        valor_actual = self.q_table[estado][accion]
        nuevo_valor = valor_actual + self.alpha * (
            recompensa + self.gamma * mejor_q_futuro - valor_actual
        )
        
        self.q_table[estado][accion] = nuevo_valor
```

### Adaptación de Estrategias

#### Algoritmo Genético para Evolución de Estrategias

```python
class EvolucionEstrategias:
    """Evolución de estrategias mediante algoritmos genéticos"""
    
    def __init__(self, tamaño_poblacion=50, tasa_mutacion=0.1):
        self.poblacion = []
        self.tamaño_poblacion = tamaño_poblacion
        self.tasa_mutacion = tasa_mutacion
        self.generacion_actual = 0
    
    def evolucionar_estrategias(self, resultados_actuales):
        """
        Proceso de evolución de estrategias:
        1. Evaluación de fitness
        2. Selección de padres
        3. Cruzamiento
        4. Mutación
        5. Reemplazo generacional
        """
        
        # 1. Evaluación de fitness
        fitness_poblacion = self._evaluar_fitness(self.poblacion, resultados_actuales)
        
        # 2. Selección de padres (torneo)
        padres = self._seleccion_torneo(self.poblacion, fitness_poblacion)
        
        # 3. Cruzamiento para crear descendencia
        descendencia = []
        for i in range(0, len(padres), 2):
            if i + 1 < len(padres):
                hijo1, hijo2 = self._cruzar_estrategias(padres[i], padres[i+1])
                descendencia.extend([hijo1, hijo2])
        
        # 4. Mutación
        descendencia_mutada = [
            self._mutar_estrategia(individuo) for individuo in descendencia
        ]
        
        # 5. Reemplazo (mantener mejores)
        poblacion_combinada = self.poblacion + descendencia_mutada
        fitness_combinado = self._evaluar_fitness(poblacion_combinada, resultados_actuales)
        
        indices_mejores = sorted(
            range(len(fitness_combinado)), 
            key=lambda i: fitness_combinado[i], 
            reverse=True
        )[:self.tamaño_poblacion]
        
        self.poblacion = [poblacion_combinada[i] for i in indices_mejores]
        self.generacion_actual += 1
        
        return self.poblacion[0]  # Mejor estrategia
```

---

## Emergencia y Comportamientos Complejos

### Detección de Comportamientos Emergentes

#### Sistema de Detección de Patrones

```python
class DetectorComportamientosEmergentes:
    """Detecta comportamientos complejos que emergen de interacciones simples"""
    
    def __init__(self):
        self.patrones_conocidos = {}
        self.ventana_observacion = 50  # Ciclos
        self.historial_comportamientos = deque(maxlen=1000)
    
    def detectar_emergencia(self, estado_sistema):
        """
        Detección de emergencia de comportamientos complejos:
        1. Análisis de correlaciones no lineales
        2. Detección de sincronización
        3. Identificación de bucles de retroalimentación
        4. Análisis de auto-organización
        """
        
        # 1. Correlaciones no lineales
        correlaciones = self._detectar_correlaciones_no_lineales(estado_sistema)
        
        # 2. Sincronización de agentes
        sincronizacion = self._medir_sincronizacion_agentes(estado_sistema)
        
        # 3. Bucles de retroalimentación
        bucles = self._identificar_bucles_retroalimentacion(estado_sistema)
        
        # 4. Auto-organización
        auto_organizacion = self._detectar_auto_organizacion(estado_sistema)
        
        comportamientos_emergentes = []
        
        if sincronizacion > 0.8:
            comportamientos_emergentes.append(
                ComportamientoEmergente(
                    tipo='sincronizacion_masiva',
                    intensidad=sincronizacion,
                    agentes_involucrados=estado_sistema.agentes_activos
                )
            )
        
        if len(bucles) > 3:
            comportamientos_emergentes.append(
                ComportamientoEmergente(
                    tipo='cascada_retroalimentacion',
                    intensidad=len(bucles) / 10,
                    bucles=bucles
                )
            )
        
        return comportamientos_emergentes
```

#### Análisis de Redes Complejas

```python
class AnalizadorRedesComplejas:
    """Análisis de propiedades emergentes en redes de agentes"""
    
    def analizar_propiedades_red(self, red_agentes):
        """
        Análisis de propiedades de red:
        - Centralidad y nodos críticos
        - Comunidades y clustering
        - Pequeño mundo
        - Robustez y vulnerabilidades
        """
        
        propiedades = {}
        
        # Centralidad de agentes
        propiedades['centralidad'] = self._calcular_centralidad(red_agentes)
        
        # Detección de comunidades
        propiedades['comunidades'] = self._detectar_comunidades(red_agentes)
        
        # Análisis de mundo pequeño
        propiedades['mundo_pequeño'] = self._analizar_mundo_pequeño(red_agentes)
        
        # Vulnerabilidades de red
        propiedades['vulnerabilidades'] = self._identificar_vulnerabilidades(red_agentes)
        
        return propiedades
    
    def predecir_cascadas(self, red_agentes, perturbacion_inicial):
        """Predicción de cascadas de efectos en la red"""
        
        simulador_cascada = SimuladorCascadas(red_agentes)
        
        # Simular propagación de perturbación
        resultado_cascada = simulador_cascada.simular_propagacion(
            perturbacion_inicial
        )
        
        return {
            'agentes_afectados': resultado_cascada.agentes_afectados,
            'intensidad_maxima': resultado_cascada.intensidad_maxima,
            'tiempo_propagacion': resultado_cascada.tiempo_propagacion,
            'nodos_criticos': resultado_cascada.nodos_criticos
        }
```

### Auto-Organización del Mercado

#### Formación Espontánea de Estructuras

```python
class SistemaAutoOrganizacion:
    """Detección y análisis de auto-organización en el mercado"""
    
    def detectar_estructuras_emergentes(self, agentes_mercado):
        """
        Detección de estructuras que emergen espontáneamente:
        - Clusters de especialización
        - Cadenas de suministro auto-organizadas
        - Nichos de mercado emergentes
        - Jerarquías espontáneas
        """
        
        estructuras = []
        
        # 1. Clusters de especialización
        clusters = self._detectar_clusters_especializacion(agentes_mercado)
        for cluster in clusters:
            if cluster.cohesion > 0.7:
                estructuras.append(
                    EstructuraEmergente(
                        tipo='cluster_especializacion',
                        agentes=cluster.miembros,
                        propiedades=cluster.caracteristicas
                    )
                )
        
        # 2. Cadenas de suministro
        cadenas = self._identificar_cadenas_suministro(agentes_mercado)
        for cadena in cadenas:
            if len(cadena.eslabones) >= 3:
                estructuras.append(
                    EstructuraEmergente(
                        tipo='cadena_suministro',
                        agentes=cadena.participantes,
                        propiedades={'eficiencia': cadena.eficiencia}
                    )
                )
        
        # 3. Nichos emergentes
        nichos = self._detectar_nichos_emergentes(agentes_mercado)
        estructuras.extend(nichos)
        
        return estructuras
```

### Inteligencia Colectiva

#### Sabiduría de Multitudes

```python
class SistemaInteligenciaColectiva:
    """Aprovechamiento de inteligencia colectiva de agentes"""
    
    def agregar_predicciones(self, predicciones_agentes, pesos_confianza=None):
        """
        Agregación inteligente de predicciones de múltiples agentes:
        1. Ponderación por confianza histórica
        2. Detección de sesgos sistemáticos
        3. Eliminación de outliers
        4. Combinación óptima
        """
        
        if pesos_confianza is None:
            pesos_confianza = [1.0] * len(predicciones_agentes)
        
        # 1. Ponderación por confianza
        predicciones_ponderadas = [
            pred * peso for pred, peso in zip(predicciones_agentes, pesos_confianza)
        ]
        
        # 2. Detección de outliers
        predicciones_filtradas = self._filtrar_outliers(predicciones_ponderadas)
        
        # 3. Agregación final
        if len(predicciones_filtradas) > 0:
            prediccion_colectiva = np.mean(predicciones_filtradas)
            confianza_colectiva = self._calcular_confianza_agregada(predicciones_filtradas)
        else:
            prediccion_colectiva = np.mean(predicciones_agentes)
            confianza_colectiva = 0.5
        
        return {
            'prediccion': prediccion_colectiva,
            'confianza': confianza_colectiva,
            'num_agentes_contribuyeron': len(predicciones_filtradas)
        }
```

---

## Conclusión

Los agentes IA en este simulador implementan un sistema sofisticado de toma de decisiones que combina múltiples paradigmas: utilidad esperada, teoría de juegos, heurísticas y aprendizaje automático. Estos agentes no solo toman decisiones individuales óptimas, sino que también desarrollan comportamientos sociales complejos, forman alianzas estratégicas y generan inteligencia colectiva.

El sistema está diseñado para que emerjan comportamientos complejos de las interacciones simples entre agentes, simulando de manera realista la complejidad de los mercados económicos reales. Los protocolos de comunicación permiten coordinación sofisticada, mientras que los sistemas de aprendizaje aseguran que los agentes se adapten y evolucionen a lo largo del tiempo.

Esta arquitectura proporciona una base sólida para la investigación en economía computacional, sistemas multi-agente y comportamientos emergentes en mercados artificiales.