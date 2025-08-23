# Plan para convertir todos los agentes en IA y aumentar el realismo del simulador

> Objetivo: Migrar hacia un simulador donde todos los agentes (consumidores, empresas, gobierno, banco central y actores del sistema financiero/laboral) sean agentes de IA coherentes entre sí, manteniendo estabilidad macro, reproducibilidad y rendimiento aceptable.

## Resumen ejecutivo
- Alcance: Reemplazar/encapsular los agentes actuales por implementaciones IA con memoria, comunicación, aprendizaje y coordinación social.
- Estrategia: API unificada de agente, envoltorios de compatibilidad, despliegue gradual por tipos de agente, recompensas económicas calibradas, validación económica continua.
- Entregables clave: Nueva interfaz `IAgent`, refactor de sistemas para consumir `IAgent`, políticas IA por tipo de agente, scripts de entrenamiento/evaluación, dashboards y tests reforzados.
- Riesgos: Inestabilidad macro por malas recompensas, coste de entrenamiento, no determinismo. Mitigación: toggles por feature, semillas fijas, pruebas de regresión y límites de acción.

---

## Estado actual (alto nivel)
Estructura relevante:
- `src/ai/`: componentes IA existentes (p. ej. `ConsumidorIA.py`, `EmpresaIA.py`, memoria, red social, orquestador y deep learning)
- `src/models/`: modelos clásicos (`Consumidor`, `Empresa`, `Mercado`, etc.)
- `src/systems/`: sistemas macro (Banco Central, Precios Dinámicos, Mercado Laboral, etc.)
- `main.py` y `config_simulacion.json`: punto de entrada y configuración
- Tests en `tests/` y ejemplos en `ejemplo_uso_completo.py`

Se observa coexistencia IA + modelos clásicos. El objetivo es consolidar una API común y usar IA end-to-end (con opción para retroceder).

---

## Principios de diseño
1. API única de agentes: todos los sistemas interactúan con `IAgent` sin conocer la implementación interna.
2. Compatibilidad progresiva: adaptadores para mantener ejecuciones existentes mientras migramos.
3. Reproducibilidad y estabilidad: semillas fijas, límites de acción y validadores económicos (`ValidadorEconomico`).
4. Métricas y trazabilidad: logging estructurado, KPIs económicos y métricas de decisiones por agente.
5. Rendimiento: decisiones vectorizadas, caching, lotes de inferencia, y configuración para desactivar partes costosas.

---

## Arquitectura propuesta
Componentes por agente:
- `IAgent` (contrato): perceive(observación), decide(acción), act(contexto/mercado), learn(feedback), persist/load(estado), id/tipo.
- `DecisionEngine` (regla/ML/RL): `IADecisionEngine.py` extendido por tipo de agente.
- `AgentMemorySystem`: memoria a corto/largo plazo, embedding opcional.
- `AgentCommunicationProtocol`: mensajería P2P y difusión; integración con `RedSocialAgentesIA`.
- `Reward & Constraints`: funciones objetivo por tipo (consumo/utilidad, beneficio, inflación/desempleo, estabilidad financiera), con límites regulatorios.
- `Event Bus` ligero: para publicar decisiones/eventos clave hacia sistemas (o usar logger + hooks existentes).

Interacción con sistemas:
- Sistemas (precios, laboral, bancario, fiscal) consumen `IAgent` vía métodos neutrales. Implementar adaptadores Mercado<->Agente donde sea necesario.

---

## Roadmap por fases (entregas incrementales)

### Fase 0 — Línea base y métricas (1-2 días)
- Fijar semillas y parámetros para tener baseline estable (50 ciclos por defecto).
- Registrar KPIs: PIB, inflación, desempleo, salario medio, beneficios medios, tasa de quiebras, distribución de precios.
- Verificar escenarios del README (ver validaciones al final).

### Fase 1 — API unificada de agentes (2-3 días)
- Crear interfaz `IAgent` y `BaseAgent` en `src/ai/` con métodos mínimos:
  - `observe(contexto) -> obs`
  - `decide(obs) -> action`
  - `act(action, mercado/sistema) -> efectos`
  - `learn(feedback)`
  - `save_state(path)` / `load_state(path)`
  - `agent_id`, `agent_type`
- Añadir adaptador para que `Consumidor` y `Empresa` clásicos implementen el contrato vía wrapper (compatibilidad temporal).
- Actualizar `IntegradorAgentesIA`/`OrquestadorAgentesIA` para operar sobre `IAgent`.

### Fase 2 — Consumidores IA al 100% (3-5 días)
- Completar `ConsumidorIA` para cubrir todas las interacciones que `Consumidor` tenía con Mercado y Sistemas.
- Definir acción: cesta de demanda, ahorro, oferta laboral (horas), preferencia temporal.
- Recompensa: utilidad esperada (consumo ajustado por variedad), suavidad intertemporal, restricción presupuestaria, penalización por endeudamiento excesivo.
- Integración con `MercadoLaboral` (oferta laboral) y `SistemaBancario` (depósitos/crédito sencillo).
- Toggle en `config_simulacion.json`: `agentes_ia.consumidores: {proporcion: 1.0, politica: "rl|heuristica"}`.

### Fase 3 — Empresas IA al 100% (4-7 días)
- Completar `EmpresaIA` para producción, precios, inversión y contratación.
- Acción: precio, cantidad objetivo, inversión, contratación/despidos, I+D (si aplica).
- Recompensa: beneficio esperado + cuota de mercado + penalización por volatilidad de inventario/precio.
- Integración con `PreciosDinamicos`, `MercadoLaboral`, `SistemaBancario` (crédito) y `SostenibilidadAmbiental` (costes externos si se activa).
- Añadir límites regulatorios desde `SistemaFiscal`/`ControlPreciosRealista`.

### Fase 4 — Gobierno y Banco Central IA (5-8 días, opcional por lotes)
- Agente Gobierno: decide gasto, impuestos marginales, transferencias.
- Agente Banco Central: fija tasa de interés/objetivo monetario.
- Política por etapas: empezar con política parametrizada con ML (supervisado) y luego RL conservador.
- Recompensa: estabilidad macro (inflación cercana a objetivo, desempleo bajo), penalizaciones por shocks extremos.

### Fase 5 — Sistema financiero y laboral IA (3-5 días)
- Bancos/Intermediarios IA para provisión de crédito simple (scoring básico con ML supervisado sobre series simuladas).
- Empleadores/Trabajadores ya cubiertos parcialmente por Empresas/Consumidores IA; afinar matching y salarios con políticas IA.

### Fase 6 — Entrenamiento y currículo (continuo)
- Dataset offline: volcar observaciones/acciones/recompensas a `results/datasets/`.
- Entrenamiento offline (imitation/BC) y online fine-tuning (RL) con `scripts/train_agents.py`.
- Semillas y checkpoints en `models/` con `save_state`.

### Fase 7 — Coordinación social y coaliciones (2-4 días)
- Activar `RedSocialAgentesIA`: difusión de señales, reputación simple.
- Coaliciones: compartir información de precios y ofertas laborales (sin colusión perfecta; añadir ruído/regulación).

### Fase 8 — Validación económica y calibración (2-3 días por iteración)
- Usar `ValidadorEconomico` con reglas adicionales: stickiness de precios, ley de Okun cualitativa, curva de Phillips simple.
- Ajustar recompensas y límites hasta que KPIs estén en rangos realistas.

### Fase 9 — Rendimiento y reproducibilidad (1-2 días)
- Batching de inferencias por tipo de agente.
- Vectorización crítica (pandas/numpy) y caching de features.
- Semillas globales y por agente, modo determinista opcional.

### Fase 10 — Visualización y reporting (1-2 días)
- Extender `VisualizacionAvanzada` con panel de decisiones IA: histogramas de precios-acción, tasas de ahorro, volúmenes de crédito, series de recompensas.

### Fase 11 — Configuración y toggles (0.5-1 día)
- Claves nuevas en `config_simulacion.json`:
  ```json
  {
    "agentes_ia": {
      "activar": true,
      "consumidores": { "proporcion": 1.0, "politica": "rl", "logs_detallados": false },
      "empresas": { "proporcion": 1.0, "politica": "rl" },
      "gobierno": { "activar": true, "politica": "ml-param" },
      "banco_central": { "activar": true, "objetivo_inflacion": 0.03 }
    }
  }
  ```
- Mantener compatibilidad: si `activar=false`, usar agentes clásicos/wrappers heurísticos.

### Fase 12 — Pruebas y CI (1-2 días)
- Unit tests: `tests/unit/test_agents_api.py`, `test_rewards.py`.
- Integración: `tests/integration/test_end_to_end_ia.py` con 50 ciclos y KPIs en rango.
- Rendimiento: test con 250 consumidores/100 ciclos en <2m (ajustable a hardware).

---

## Cambios propuestos por archivo/carpeta
- `src/ai/IAgent.py` (nuevo): contrato del agente + enums de tipos.
- `src/ai/BaseAgent.py` (nuevo): utilidades comunes (semillas, normalización, clamps, logs).
- `src/ai/DecisionPolicies/` (nuevo): políticas concretas por agente (heurística, supervised, rl).
- `src/ai/RewardFunctions/` (nuevo): recompensas por tipo con parámetros en config.
- `src/ai/Adapters/` (nuevo): wrappers para `Consumidor`/`Empresa` clásicos a `IAgent`.
- `src/ai/Batching.py` (nuevo): lotes de inferencia por tipo de agente.
- `src/systems/*`: puntos de integración reciben `IAgent` o adaptadores; evitar dependencia de clases concretas.
- `src/utils/SimuladorLogger.py`: añadir canal `agent_decisions` y opción JSONL.
- `config_simulacion.json`: nuevas claves en `agentes_ia` (ver Fase 11).
- `scripts/train_agents.py` (nuevo): entrenamiento offline/online.
- `results/datasets/` (nuevo): dumps para entrenamiento.

---

## Contratos y formas de datos (borrador)
- Observación por consumidor:
  - precios[bienes_k], ingreso_disponible, ahorro_actual, salarios, desempleo, señales_red_social (opc), expectativas simples.
- Acción por consumidor:
  - demandas[bienes_k] (no negativa), tasa_ahorro [0,1], oferta_laboral [0,1].
- Observación por empresa:
  - demanda_hist, inventario, coste_unitario, salario_medio, tipo_interes, competencia_local.
- Acción por empresa:
  - precio>=0, produccion>=0, contrataciones_int, inversion>=0.

Clamps y normalización definidos en `BaseAgent`.

---

## Recompensas por tipo (resumen)
- Consumidor: utilidad CES del consumo + bonus por suavidad del consumo − penalización por endeudamiento/situaciones de liquidez.
- Empresa: beneficio neto + cuota mercado − penalización por stockouts/inventario extremo − volatilidad de precios.
- Gobierno: bienestar social (ponderación de utilidad agregada) con penalización por desigualdad alta.
- Banco Central: pérdida cuadrática tipo Taylor (inflación/objetivo + desempleo/desempleo_natural).

Parámetros en `config_simulacion.json` para facilitar calibración.

---

## Validación y aceptación
Usar SIEMPRE las validaciones del proyecto tras cambios (ver `.github/copilot-instructions.md`):
1) Simulación básica: `python3 main.py` debe completar con mensaje “SIMULACIÓN ECONÓMICA HIPERREALISTA v3.0 COMPLETADA EXITOSAMENTE” y generar dashboard/CSV/JSON/report.
2) Ejemplo interactivo: `echo "1" | python3 ejemplo_uso_completo.py` con 15 consumidores y 6 empresas; 150 ciclos sin errores críticos; agentes IA activos.
3) Test suite: `./run_tests.sh` con pruebas básicas pasando (fallos de performance no críticos). Añadir nuevos tests IA sin romper los existentes.

KPIs esperados (rangos orientativos):
- PIB: 100.000 – 1.000.000
- Inflación: -10% a +20% (preferible 0–8%)
- Desempleo: 2% – 20%
- Cuota de quiebras empresariales: 0% – 15% por 100 ciclos

Criterio de aceptación por fase: KPIs dentro de rango + tests verdes + artefactos generados.

---

## Riesgos y mitigaciones
- Desalineación de recompensas: usar validadores macro y pruebas A/B con baseline heurístico.
- No determinismo/ruido: fijar semillas y ofrecer modo determinista; logs JSONL para reproducir episodios.
- Coste de cómputo: políticas heurísticas iniciales + RL opcional; batching y vectorización; toggles de detalle.
- Colusión empresarial: regular mediante límites y ruido en comunicación social.

---

## Plan de entregas y estimación
- Sprint 1: Fase 0-1 (API, wrappers, baseline) — 1 semana
- Sprint 2: Fase 2 (Consumidores IA 100%) — 1 semana
- Sprint 3: Fase 3 (Empresas IA 100%) — 1-2 semanas
- Sprint 4: Fases 4-5 (Gobierno/BC y financiero/laboral IA) — 1-2 semanas
- Sprint 5: Fases 6-12 (entrenamiento, coordinación, validación, rendimiento, visualización, tests) — 2+ semanas iterativas

---

## Próximos pasos inmediatos
1) Añadir `src/ai/IAgent.py` y `src/ai/BaseAgent.py` + toggles en `config_simulacion.json`.
2) Implementar wrappers para Consumidor/Empresa clásicos a `IAgent`.
3) Actualizar `IntegradorAgentesIA`/`OrquestadorAgentesIA` para operar con la nueva API.
4) Ejecutar validaciones baseline y fijar KPIs objetivo por escenario.

---

> Nota: Este plan respeta la guía operativa del repo (no cancelar instalaciones ni simulaciones largas) y usa los escenarios de validación como criterio de éxito continuo.
