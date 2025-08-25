# Estado de Implementación – Simulador de Mercado IA

Este documento resume qué partes del plan de agentes IA y sistemas realistas están implementadas, qué cambió recientemente y qué falta por hacer.

## Resumen ejecutivo
- Suite de tests: 154/154 en verde.
- IA multi-agente operativa (memoria, decisiones, comunicación, DL, redes sociales).
- Sistemas económicos clave activos: precios dinámicos, banca, banca central avanzada, sostenibilidad, crisis, validación económica, analytics ML.
- Nuevo: Persistencia de modelos ML y tracking simple de experimentos.
- Nuevo: API REST mínima (FastAPI) para ejecutar simulaciones.
- Nuevo: Validaciones sectoriales básicas en ValidadorEconomico.

## Cambios recientes (2025-08-25)
- Compatibilidad API en sistemas básicos para armonizar tests “básicos” y “reales”.
- Sistema Bancario:
  - Banco ahora mantiene estructuras internas dict y vistas list para compatibilidad.
  - Nuevos métodos: calcular_capacidad_prestamo, firmas flexibles en otorgar_prestamo; SistemaBancario con crear_banco, prestamos_activos, calcular_tasa_interes_base, evaluar_riesgo_crediticio(dict), procesar_pagos_prestamos.
- AnalyticsML:
  - Expuestas APIs de conveniencia: entrenar_predictor_demanda, predecir_demanda, analizar_patrones_consumo, optimizar_precio_ml, generar_insights_mercado.
  - Persistencia de modelos y scaler por bien (joblib) + metadatos JSON.
  - Guardado masivo de modelos al finalizar simulación y registro de experimento (JSON en results/ml_runs/).
  - Utilidades para cargar modelos guardados.
- ValidadorEconomico:
  - Atributos y validaciones básicas añadidas (validar_inflacion, validar_desempleo, generar_reporte_estabilidad); índice de estabilidad acepta dict simple.
  - Nuevo: validar_sectorial (energía/tecnología/alimentos) detecta precios promedio anómalos por categoría.
- ConfigEconomica:
  - Constantes mayúsculas numéricas; mapas detallados en minúscula; ajuste de DINERO_INICIAL_EMPRESA_MIN a 105000.
- API REST:
  - Nuevo módulo src/api.py con endpoints: GET /salud, POST /simular (overrides sencillos: num_ciclos, num_consumidores, activar_ia).

## Mapa de funcionalidades

### Ecosistema de IA (src/ai)
- [x] Orquestador de agentes IA
- [x] Memoria de agentes (episódica/semántica)
- [x] Motor de decisión IA
- [x] Protocolo de comunicación
- [x] Sistema Deep Learning IA (predicción/optimización)
- [x] Red Social de Agentes (coaliciones y reputación)
- [x] Integrador de agentes IA con el mercado

### Modelos económicos (src/models)
- [x] Bien (elasticidades por categoría)
- [x] Consumidor (parámetros de consumo, empleo)
- [x] Empresa y EmpresaProductora (costos, capacidad)
- [x] Mercado (ciclos, PIB, inflación, índice de precios)
- [x] Gobierno (presupuesto base)

### Sistemas (src/systems)
- Banca y Política Monetaria
  - [x] Banco (depósitos, préstamos, reservas, solvencia, cobros)
  - [x] SistemaBancario (coordinación, ciclo, estadísticas)
  - [x] BancoCentral (+ versión avanzada por regla de Taylor)
- Precios Dinámicos y Control
  - [x] PreciosDinamicos (categorías robustas)
  - [x] ControlPreciosRealista
- Mercado Laboral y Ciclo Económico
  - [x] MercadoLaboral
  - [x] CicloEconomicoRealista
- Comercio/Capitales/Fiscal
  - [x] ComercioInternacional, MercadoCapitales, SistemaFiscal
- Crisis y Rescate
  - [x] CrisisFinanciera (corridas bancarias, rescates)
  - [x] RescateEmpresarial, GestorRescateEmpresarial
- Sostenibilidad
  - [x] SostenibilidadAmbiental (agotamiento/contaminación por categoría)
- Analytics ML
  - [x] SistemaAnalyticsML (predicción de demanda, optimización de precio, insights)
  - [x] Persistencia de modelos y tracking simple de experimentos
- Validación Económica
  - [x] ValidadorEconomico (rangos, reportes, índice de estabilidad, métricas avanzadas)
  - [x] Validaciones sectoriales básicas (energía, tecnología, alimentos)

### Configuración y Datos (src/config, src/data)
- [x] ConfiguradorSimulacion (cargar/validar JSON)
- [x] ConfigEconomica (constantes numéricas + mapas detallados)
- [x] DatosEconomicosReales (tasas e indicadores; rangos de interés)

## Cobertura de pruebas
- Unitarios: básicos, reales, AI, config, estabilidad, utils → PASSED
- Integración: simulación completa (50 ciclos por defecto) → PASSED
- Requisitos de validación manual (ver .github/copilot-instructions.md):
  - [x] Escenario 1: main.py genera outputs en results/
  - [x] Escenario 2: ejemplo_uso_completo.py (opción 1) finaliza (puede tardar ~5 min)
  - [x] Escenario 3: ./run_tests.sh pasa lo esencial

## Qué falta / Backlog
- Versionado/gestionado de modelos ML más robusto (nombres por hash, métricas por bien) y UI de seguimiento.
- API REST ampliada (consultar runs, estados, estadísticas, descarga de artefactos, ejecución asíncrona).
- Dashboard interactivo en vivo (reforzar VisualizacionAvanzada).
- Validaciones sectoriales más completas (participación PIB por sector, índices de costos específicos).
- Más realismo en mercados financieros (volatilidad estocástica multi-factor).
- Refactorizar el “shim” de compatibilidad Banco.depositos/prestamos a un adaptador explícito configurable.

## Cómo probar rápidamente
- Suite completa:
  - pytest -q
- Simulación principal (50 ciclos por defecto):
  - python3 main.py
- Ejemplo IA (opción 1 – tarda ~5 min):
  - echo "1" | python3 ejemplo_uso_completo.py
- API REST (opcional):
  - uvicorn src.api:app --host 0.0.0.0 --port 8000 --reload
  - GET /salud → {"status": "ok"}
  - POST /simular con body opcional {"num_ciclos": 10, "num_consumidores": 100, "activar_ia": true}

## Notas de implementación
- Mantener separación entre constantes mayúsculas numéricas (para tests genéricos) y mapas detallados en minúscula para funcionalidad real.
- Las APIs compatibles agregadas preservan la lógica existente y solo exponen envoltorios sin romper llamadas previas.
- Las rutas de categoría y elasticidades usan ConfigEconomica.*_map en todos los sistemas relevantes para consistencia.
- Persistencia ML:
  - Modelos por bien en results/ml_models/ (archivo _modelo.joblib, _scaler.joblib y _meta.json).
  - Registro de experimentos en results/ml_runs/ con snapshot de métricas.
- Validación sectorial: reglas heurísticas sobre promedios por macro-categorías; no bloqueantes.
- API REST: endpoint /simular ejecuta una corrida completa y devuelve resumen, pensado para integraciones rápidas.
