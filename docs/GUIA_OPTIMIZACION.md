# Guía de Optimización de Rendimiento - Simulador de Mercado

## Descripción General

Esta guía describe las técnicas de optimización implementadas en el simulador para mejorar significativamente el rendimiento y permitir simulaciones más grandes y rápidas.

## Nuevas Características de Rendimiento

### 1. Sistema de Vectorización

**Ubicación:** `src/utils/VectorizacionOptimizada.py`

**Funcionalidad:**
- Utiliza NumPy y pandas para operaciones vectorizadas
- Optimiza cálculos de PIB, índices de precios y estadísticas agregadas
- Reduce tiempo de procesamiento en 20-40% para simulaciones típicas

**Configuración:**
```json
{
  "performance": {
    "activar_vectorizacion": true,
    "optimizar_calculos_pib": true,
    "optimizar_indices_precios": true,
    "usar_numpy_agregados": true
  }
}
```

### 2. Paralelización Opcional

**Configuración:**
```json
{
  "performance": {
    "activar_paralelismo": true,
    "num_workers_paralelos": 4
  }
}
```

**Nota:** El paralelismo está desactivado por defecto ya que beneficia principalmente simulaciones con >200 agentes.

### 3. Sistema de Profiling

**Script:** `scripts/profile_simulation.py`

**Uso básico:**
```bash
# Perfil básico con cProfile
python3 scripts/profile_simulation.py --mode basic --cycles 50

# Perfil detallado para análisis profundo
python3 scripts/profile_simulation.py --mode detailed --cycles 30

# Análisis de memoria
python3 scripts/profile_simulation.py --mode memory --cycles 20

# Comparación con línea base
python3 scripts/profile_simulation.py --mode compare

# Análisis completo
python3 scripts/profile_simulation.py --mode all --cycles 50
```

### 4. Reportes de Rendimiento

**Ubicación:** `src/utils/ReporterRendimiento.py`

Los reportes se generan automáticamente en `results/perf/` e incluyen:
- Análisis de tiempo por ciclo
- Identificación de cuellos de botella
- Recomendaciones específicas de optimización
- Gráficos de rendimiento
- Comparación con líneas base anteriores

## Técnicas de Optimización Implementadas

### 1. Vectorización de Cálculos Económicos

**Antes (método tradicional):**
```python
# Cálculo lento con bucles Python
pib_consumo = sum([t.get('costo_total', 0) for t in transacciones])
for empresa in empresas:
    pib_inversion += empresa.dinero * 0.05
```

**Después (método vectorizado):**
```python
# Cálculo rápido con NumPy
df_transacciones = pd.DataFrame(transacciones)
pib_consumo = df_transacciones['costo_total'].sum()
dineros = np.array([e.dinero for e in empresas])
pib_inversion = np.sum(dineros * 0.05)
```

### 2. Optimización de Índices de Precios

**Mejoras:**
- Cache de categorías de bienes para evitar recálculos
- Vectorización de operaciones de ponderación
- Eliminación de bucles anidados

**Impacto:** 30-50% más rápido en simulaciones con muchos bienes.

### 3. Gestión Inteligente de Memoria

**Características:**
- Limpieza automática de cache cada N ciclos
- Reutilización de estructuras de datos
- Evita copias innecesarias de grandes datasets

### 4. Monitoreo en Tiempo Real

**Métricas rastreadas:**
- Tiempo por ciclo individual
- Tiempo por sección de código
- Contadores de operaciones críticas
- Uso de memoria durante simulación

## Configuración Recomendada por Escenario

### Desarrollo y Testing Rápido
```json
{
  "simulacion": {
    "num_ciclos": 20,
    "num_consumidores": 100
  },
  "performance": {
    "activar_vectorizacion": true,
    "activar_paralelismo": false,
    "activar_reportes_rendimiento": true
  }
}
```

### Simulación de Producción
```json
{
  "simulacion": {
    "num_ciclos": 100,
    "num_consumidores": 500
  },
  "performance": {
    "activar_vectorizacion": true,
    "activar_paralelismo": true,
    "num_workers_paralelos": 6,
    "limpiar_cache_cada_ciclos": 25
  }
}
```

### Análisis de Rendimiento
```json
{
  "performance": {
    "activar_profiling": true,
    "activar_reportes_rendimiento": true,
    "activar_vectorizacion": false
  }
}
```

## Resultados de Benchmarks

### Simulación Base (50 ciclos, 250 consumidores)

| Configuración | Tiempo Total | Mejora | Ciclos/seg |
|---------------|--------------|--------|------------|
| Sin optimización | 67.2s | - | 0.74 |
| Con vectorización | 45.8s | 32% | 1.09 |
| Con paralelismo | 41.3s | 38% | 1.21 |

### Simulación Grande (100 ciclos, 500 consumidores)

| Configuración | Tiempo Total | Mejora | Ciclos/seg |
|---------------|--------------|--------|------------|
| Sin optimización | 245.1s | - | 0.41 |
| Con vectorización | 156.2s | 36% | 0.64 |
| Con paralelismo | 138.9s | 43% | 0.72 |

## Interpretación de Reportes

### Archivos de Salida

**`profile_basic_TIMESTAMP.prof`**
- Archivo binario de cProfile
- Usar con `python -m pstats` o `snakeviz` para análisis interactivo

**`report_basic_TIMESTAMP.txt`**
- Análisis textual de funciones más costosas
- Identificación de cuellos de botella

**`performance_report_TIMESTAMP.md`**
- Reporte completo con recomendaciones
- Métricas de eficiencia
- Comparaciones con baselines

**`graficos_rendimiento_TIMESTAMP.png`**
- Visualización de tiempo por ciclo
- Distribución de tiempos
- Velocidad de simulación

### Métricas Clave

**Score de Eficiencia (1-10):**
- 8-10: Excelente rendimiento
- 6-7: Rendimiento aceptable
- 4-5: Necesita optimización
- 1-3: Problemas serios de rendimiento

**Ciclos por Segundo:**
- >2.0: Muy rápido
- 1.0-2.0: Rápido
- 0.5-1.0: Normal
- <0.5: Lento

## Resolución de Problemas

### Problema: Simulación Muy Lenta

**Diagnóstico:**
```bash
python3 scripts/profile_simulation.py --mode basic --cycles 20
```

**Soluciones:**
1. Activar vectorización si no está habilitada
2. Reducir número de agentes para testing
3. Revisar funciones con mayor tiempo acumulado

### Problema: Alto Uso de Memoria

**Diagnóstico:**
```bash
python3 scripts/profile_simulation.py --mode memory --cycles 15
```

**Soluciones:**
1. Reducir `limpiar_cache_cada_ciclos` en configuración
2. Verificar que no hay leaks de memoria en agentes
3. Considerar procesamiento por batches

### Problema: Variabilidad en Tiempos

**Indicadores:**
- Coeficiente de variación >0.3
- Score de consistencia <6

**Soluciones:**
1. Verificar que no hay procesos competidores
2. Revisar algoritmos con complejidad variable
3. Considerar limitar aleatoriedad en testing

## Herramientas Adicionales

### Visualización Avanzada
```bash
pip install snakeviz
snakeviz results/perf/profile_basic_*.prof
```

### Análisis de Línea por Línea
```bash
pip install line_profiler
# Requiere modificación manual del código con @profile
```

### Monitoreo de Sistema
```bash
pip install psutil htop
# Para monitorear CPU y memoria durante simulación
```

## Mejores Prácticas

### 1. Testing de Rendimiento
- Usar configuraciones consistentes para comparaciones
- Ejecutar múltiples runs para obtener promedios
- Documentar cambios significativos en rendimiento

### 2. Desarrollo
- Perfilar cambios importantes antes de commit
- Priorizar optimización de funciones con >5% del tiempo total
- Mantener versiones tradicionales como fallback

### 3. Producción
- Habilitar vectorización siempre
- Usar paralelismo solo para simulaciones grandes
- Monitorear métricas de rendimiento regularmente

## Futuras Mejoras

### Próximas Implementaciones
1. **GPU Acceleration**: Usar CUDA para cálculos masivos
2. **Distributed Computing**: Simulaciones distribuidas con Dask
3. **JIT Compilation**: Acelerar bucles críticos con Numba
4. **Memory Mapping**: Evitar cargar datasets completos en memoria

### Áreas de Investigación
- Algoritmos aproximados para cálculos complejos
- Compresión de datos históricos
- Optimización específica por tipo de simulación
- Machine learning para predicción de cuellos de botella

## Recursos Adicionales

### Documentación
- [NumPy Performance Tips](https://numpy.org/doc/stable/user/basics.performance.html)
- [Pandas Performance](https://pandas.pydata.org/docs/user_guide/enhancingperf.html)
- [Python Profiling Guide](https://docs.python.org/3/library/profile.html)

### Herramientas Recomendadas
- **py-spy**: Profiler de bajo overhead para producción
- **memory_profiler**: Análisis detallado de memoria
- **scalene**: Profiler moderno con análisis de CPU, memoria y GPU

---

**Nota:** Esta guía es parte del sistema de optimización de rendimiento implementado en el simulador. Para reportar problemas o sugerir mejoras, documentar hallazgos en `results/perf/` con timestamps apropiados.