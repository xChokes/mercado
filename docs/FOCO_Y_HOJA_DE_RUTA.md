# Foco propuesto y hoja de ruta

Este documento sintetiza un foco claro para el simulador y un plan corto para ejecutarlo.

## Objetivo 2025 Q3: PriceLab-Mercado (enfoque comercial)

Construir un simulador ligero de estrategia de precios y shocks macro que, en 30–120 s, permita estimar impactos en demanda, ingresos y márgenes bajo distintos escenarios y genere un informe automático en `results/`.

- Usuarios: analistas de pricing/BI en retail/servicios, PMs de producto, docentes.
- Por qué ahora: ya existen ciclos rápidos (~30 s), agentes IA, manejo de crisis y dashboards; sólo falta empaquetar escenarios y reportes comparables.

## Alcance MVP

- 3 escenarios predefinidos (archivos JSON o perfiles):
  1) Base estable, 2) Shock de inflación + política monetaria, 3) Subsidio a demanda + restricción de oferta.
- Salida: CSV comparables y un dashboard/resumen por escenario (PNG + TXT/JSON con KPIs).
- Uso: 1 comando por escenario o un batch que ejecute todos y cree un reporte comparativo.

## KPIs de éxito (medibles con el código actual)

- Tiempo de simulación (50 ciclos): < 60 s en equipo estándar.
- Estabilidad económica: PIB en 100k–1M; inflación -10% a +20% (según "Validación").
- Sensibilidad a políticas: variación de demanda/PIB consistente ante ±5% en tasas o precios.
- Reproducibilidad: semillas y configs versionadas; resultados deterministas bajo misma semilla.
- Experiencia: 3 escenarios ejecutables sin editar código, con outputs claros en `results/`.

## Hoja de ruta de 4 semanas

### ✅ Semana 1 – Empaquetado de escenarios (COMPLETADO)
- ✅ Definir carpeta `escenarios/` con 3 presets (JSON) y semilla fija.
- ✅ Cargar perfiles desde CLI o variable de entorno (sin romper `main.py`).
- ✅ Registrar metadatos de ejecución en cada archivo de salida.

### ✅ Semana 2 – Reportes y comparables (COMPLETADO)
- ✅ Agregar un agregador de resultados: resumen consolidado (CSV + TXT) por batch.
- ✅ Etiquetar dashboards con nombre del escenario y semilla.

### ✅ Semana 3 – Validación y pruebas (COMPLETADO)
- ✅ Scripts de validación automática de KPIs (rangos PIB/inflación, tiempos, integridad de archivos).
- ✅ Pruebas de humo en CI (opcional) y `./run_tests.sh` extendido para escenarios.

### ✅ Semana 4 – Documentación y demo (COMPLETADO)
- ✅ Guía de uso con los 3 escenarios y ejemplos de interpretación.
- ✅ Caso demo: comparar Base vs Shock inflación (gráficas + conclusiones).

## Estado de Implementación

### ✅ Funcionalidades Implementadas
- [x] 3 escenarios predefinidos en `escenarios/` (base, shock_inflacion, subsidio_y_restriccion_oferta)
- [x] Selector de escenarios en `main.py` con flag `--escenario`
- [x] Script batch `run_escenarios.py` para ejecución múltiple
- [x] Generación automática de reportes comparativos (CSV + TXT)
- [x] Validación automática de KPIs con `scripts/validar_kpis.py`
- [x] Extensión de `run_tests.sh` para incluir validación de escenarios
- [x] Documentación completa de usuario en `docs/GUIA_USUARIO.md`
- [x] Demo comparativo interactivo con `demo_comparativo.py`
- [x] Archivos etiquetados con nombre de escenario y timestamp
- [x] Sistema de semillas para reproducibilidad

### 📁 Archivos Creados/Modificados
- `escenarios/base.json` - Escenario estable base
- `escenarios/shock_inflacion.json` - Escenario con presiones inflacionarias  
- `escenarios/subsidio_y_restriccion_oferta.json` - Escenario con políticas públicas
- `run_escenarios.py` - Ejecutor batch de escenarios
- `scripts/validar_kpis.py` - Validador automático de KPIs
- `docs/GUIA_USUARIO.md` - Guía completa de uso
- `demo_comparativo.py` - Demo interactivo Base vs Shock
- `run_tests.sh` - Extendido con validación de escenarios

### 🎯 Objetivos MVP Alcanzados
- ✅ Tiempo de simulación < 60s (típicamente ~30s para 50 ciclos)
- ✅ 3 escenarios predefinidos ejecutables sin editar código
- ✅ Outputs claros y comparables en `results/`
- ✅ Validación automática de rangos PIB/inflación
- ✅ Reproducibilidad con semillas fijas
- ✅ Experiencia de usuario simplificada

## Extensión de investigación (en paralelo, opcional)

Benchmark de coordinación multiagente en mercados:
- Tareas: formación de coaliciones, respuesta a shocks, dinámica de precios.
- Métricas: bienestar social, volatilidad de precios, velocidad de convergencia.
- Entregable: informe replicable y, si procede, preprint.

## Monetización posible

- Core OSS + presets básicos; paquete pro con escenarios sectoriales y soporte.
- Servicio: consultoría de calibración y análisis ad hoc.
- SaaS mínimo (FastAPI): ejecución remota de escenarios y descarga de reportes.

## Próximos pasos inmediatos

### ✅ COMPLETADO - Estado MVP Alcanzado

1. ✅ **Crear `escenarios/` y 3 presets JSON** - Implementado con:
   - `escenarios/base.json` - Escenario estable de referencia
   - `escenarios/shock_inflacion.json` - Presiones inflacionarias
   - `escenarios/subsidio_y_restriccion_oferta.json` - Políticas públicas

2. ✅ **Añadir selector de escenarios sin romper compatibilidad** - Implementado:
   - Flag `--escenario` en `main.py` 
   - Retrocompatibilidad con `config_simulacion.json`
   - Semillas fijas para reproducibilidad

3. ✅ **Generar reporte comparativo en `results/`** - Implementado:
   - `run_escenarios.py` para ejecución batch
   - Archivos CSV consolidados con KPIs
   - Reportes de texto con resúmenes ejecutivos
   - Dashboards etiquetados por escenario

### ✅ FUNCIONALIDADES ADICIONALES IMPLEMENTADAS

4. ✅ **Validación automática de KPIs** - `scripts/validar_kpis.py`:
   - Validación de rangos PIB, inflación, desempleo
   - Verificación de tiempos de ejecución
   - Integridad de archivos de salida
   - Reportes automáticos de validación

5. ✅ **Extensión de tests para escenarios** - `run_tests.sh` mejorado:
   - Validación de escenarios en CI
   - Pruebas de humo automatizadas
   - Integración con suite de tests existente

6. ✅ **Documentación completa de usuario** - `docs/GUIA_USUARIO.md`:
   - Manual de uso con ejemplos prácticos
   - Casos de uso por sector (retail, finanzas, manufactura)
   - Solución de problemas comunes
   - Interpretación de resultados

7. ✅ **Demo comparativo interactivo** - `demo_comparativo.py`:
   - Análisis automático Base vs Shock de Inflación
   - Gráficas comparativas de evolución de precios
   - Insights automáticos generados por IA
   - Reportes completos con recomendaciones

### 🎯 Objetivos MVP 100% Cumplidos

- ✅ **Tiempo < 60s**: Simulaciones optimizadas (~30-50s para 50 ciclos sin IA intensiva)
- ✅ **3 escenarios predefinidos**: Base, Shock Inflación, Subsidio+Restricción
- ✅ **Outputs claros en results/**: CSV, PNG, TXT, JSON automáticos
- ✅ **Uso sin editar código**: Scripts ejecutables con argumentos
- ✅ **Reproducibilidad**: Sistema de semillas implementado
- ✅ **Validación automática**: Rangos PIB/inflación verificados
- ✅ **Experiencia de usuario**: Documentación y ejemplos completos
