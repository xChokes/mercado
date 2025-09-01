# Pipeline de Calibración Automática y Análisis de Sensibilidad

## Descripción

Sistema avanzado de calibración automática que optimiza parámetros del simulador económico para lograr métricas macroeconómicas realistas y reproducibles. Incluye optimización Bayesiana con Optuna y grid search para análisis de sensibilidad.

## Características Principales

### 🎯 Métodos de Optimización
- **Optimización Bayesiana**: Usando TPE (Tree-structured Parzen Estimator) con Optuna
- **Grid Search**: Búsqueda exhaustiva en grid de parámetros para análisis de sensibilidad
- **Pruning**: Eliminación temprana de trials no prometedores con MedianPruner

### 📊 Parámetros Clave Calibrados
- **PIB inicial**: Valor base de la economía
- **Elasticidades**: Precio-demanda e ingreso-demanda  
- **Rigidez de precios**: Velocidad de ajuste y sensibilidad a competencia
- **Meta de inflación**: Objetivo del banco central
- **Intensidad búsqueda laboral**: Probabilidades de contratación y habilidades mínimas
- **Sistema bancario**: Tasas de interés y ratios de préstamos

### 🎯 Métricas Objetivo
- **PIB final**: Valor y crecimiento económico
- **Inflación promedio**: Estabilidad de precios
- **Desempleo promedio**: Mercado laboral saludable
- **Volatilidad**: Estabilidad macroeconómica
- **Actividad económica**: Transacciones y empresas activas

## Instalación y Configuración

### Dependencias
```bash
pip install optuna pandas numpy scikit-learn matplotlib
```

### Estructura de Archivos
```
src/utils/calibration_runner.py    # Pipeline principal
config/presets/                    # Configuraciones predefinidas
├── basic_economic.json            # Calibración económica básica
├── pricing_sensitivity.json       # Análisis sensibilidad precios
└── banking_system.json           # Sistema bancario
results/calibrations/              # Resultados de calibración
```

## Uso

### 1. Calibración Básica

```bash
# Optimización Bayesiana con configuración por defecto
python3 -m src.utils.calibration_runner --method bayesian --trials 50

# Especificar número de ciclos de simulación
python3 -m src.utils.calibration_runner --trials 25 --cycles 10
```

### 2. Usar Configuraciones Preset

```bash
# Calibración económica básica
python3 -m src.utils.calibration_runner --preset basic_economic --trials 30

# Análisis de sensibilidad de precios
python3 -m src.utils.calibration_runner --preset pricing_sensitivity --method grid

# Calibración sistema bancario
python3 -m src.utils.calibration_runner --preset banking_system --trials 40
```

### 3. Grid Search para Análisis de Sensibilidad

```bash
# Grid search con límite de trials
python3 -m src.utils.calibration_runner --method grid --trials 100

# Grid search con timeout
python3 -m src.utils.calibration_runner --method grid --timeout 3600
```

### 4. Crear Configuraciones Preset

```bash
# Generar archivos de configuración predefinidos
python3 -m src.utils.calibration_runner --create-presets
```

## Configuración Personalizada

### Archivo JSON de Configuración

```json
{
  "parameters": {
    "pib_inicial": [80000, 150000],
    "tasa_inflacion_objetivo": [0.015, 0.035],
    "ajuste_maximo_por_ciclo": [0.10, 0.25],
    "probabilidad_contratacion_base": [0.3, 0.7]
  },
  "optimization_method": "bayesian",
  "n_trials": 50,
  "simulation_cycles": 15,
  "target_metrics": {
    "pib_final": [100000.0, 1.0],
    "inflacion_promedio": [0.02, 2.0],
    "desempleo_promedio": [0.06, 1.5]
  },
  "results_dir": "results/calibrations"
}
```

### Usar Configuración Personalizada

```bash
python3 -m src.utils.calibration_runner --config mi_configuracion.json
```

## Resultados y Análisis

### Archivos Generados

1. **`calibration_results_TIMESTAMP.csv`**: Resultados completos de todos los trials
2. **`calibration_best_TIMESTAMP.csv`**: Top 10 mejores resultados
3. **`calibration_summary_TIMESTAMP.json`**: Resumen con estadísticas y mejor configuración
4. **`calibration_TIMESTAMP.log`**: Log detallado del proceso

### Estructura de Resultados CSV

| Columna | Descripción |
|---------|-------------|
| `pib_inicial` | Parámetro: PIB inicial |
| `tasa_inflacion_objetivo` | Parámetro: Meta de inflación |
| `ajuste_maximo_por_ciclo` | Parámetro: Rigidez de precios |
| `pib_final` | Métrica: PIB final alcanzado |
| `inflacion_promedio` | Métrica: Inflación promedio |
| `desempleo_promedio` | Métrica: Desempleo promedio |
| `score` | Score objetivo (0-1, mayor es mejor) |
| `execution_time` | Tiempo de ejecución en segundos |
| `trial_number` | Número de trial |

### Análisis de Sensibilidad

Los resultados permiten analizar:
- **Correlaciones**: Entre parámetros y métricas objetivo
- **Rangos óptimos**: Valores de parámetros que producen mejores scores
- **Trade-offs**: Compensaciones entre diferentes objetivos económicos
- **Robustez**: Estabilidad de resultados ante variaciones paramétricas

## Ejemplos de Uso Avanzado

### 1. Calibración para Economía Estable

```bash
# Enfoque en estabilidad económica
python3 -m src.utils.calibration_runner \
  --preset basic_economic \
  --trials 100 \
  --cycles 20 \
  --timeout 7200
```

### 2. Análisis de Políticas de Precios

```bash
# Sensibilidad de políticas de precios
python3 -m src.utils.calibration_runner \
  --preset pricing_sensitivity \
  --method grid \
  --trials 200
```

### 3. Optimización del Sistema Bancario

```bash
# Calibración del sistema financiero
python3 -m src.utils.calibration_runner \
  --preset banking_system \
  --trials 75 \
  --cycles 25
```

## Métricas y Scoring

### Función Objetivo

El sistema utiliza una función objetivo multi-criterio que:

1. **Normaliza métricas**: Convierte a scores 0-1 según targets
2. **Aplica pesos**: Prioriza métricas más importantes
3. **Penaliza extremos**: Evita colapsos económicos
4. **Premia estabilidad**: Bonus por economías funcionales

### Targets por Defecto

| Métrica | Target | Peso | Descripción |
|---------|--------|------|-------------|
| PIB final | $100,000 | 1.0 | Tamaño económico objetivo |
| Inflación promedio | 2% | 2.0 | Estabilidad de precios (peso alto) |
| Desempleo promedio | 6% | 1.5 | Mercado laboral saludable |
| Crecimiento PIB | 2% | 1.0 | Dinamismo económico |
| Volatilidad inflación | 1% | 0.5 | Previsibilidad económica |

## Solución de Problemas

### Error: "Configuración no encontrada"
- Verificar que el archivo de configuración existe
- Usar rutas absolutas o relativas correctas
- Revisar formato JSON válido

### Simulaciones muy lentas
- Reducir `simulation_cycles` (mínimo 5)
- Limitar `n_trials` para tests rápidos
- Usar `timeout` para evitar ejecuciones muy largas

### Scores muy bajos
- Ajustar `target_metrics` a valores más realistas
- Revisar rangos de `parameters` muy extremos
- Verificar que la economía se inicializa correctamente

### Grid search muy lento
- Reducir número de parámetros en configuración
- Usar menos puntos por parámetro (el sistema usa 5 por defecto)
- Limitar con `--trials` el número máximo de combinaciones

## API Programática

### Uso desde Python

```python
from src.utils.calibration_runner import CalibrationRunner, CalibrationConfig

# Configurar calibración
config = CalibrationConfig(
    parameters={
        'pib_inicial': (80000, 120000),
        'tasa_inflacion_objetivo': (0.015, 0.025),
    },
    optimization_method="bayesian",
    n_trials=30,
    simulation_cycles=10
)

# Ejecutar calibración
runner = CalibrationRunner(config)
results = runner.run_calibration()

# Análizar resultados
best_result = max(results, key=lambda r: r.score)
print(f"Mejor score: {best_result.score:.4f}")
print(f"Mejores parámetros: {best_result.parameters}")
```

## Contribuir

Para contribuir al sistema de calibración:

1. **Tests**: Agregar tests en `tests/unit/test_calibration_runner.py`
2. **Presets**: Crear nuevas configuraciones en `config/presets/`
3. **Métricas**: Extender métricas objetivo en `extract_metrics_from_mercado()`
4. **Optimizadores**: Agregar nuevos métodos de optimización

## Changelog

### v1.0.0
- ✅ Optimización Bayesiana con Optuna
- ✅ Grid search para análisis de sensibilidad  
- ✅ Configuraciones preset predefinidas
- ✅ Exportación completa de resultados
- ✅ Función objetivo multi-criterio robusta
- ✅ Tests automatizados
- ✅ CLI completo con argumentos
- ✅ Documentación completa