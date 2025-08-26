# Guía de Uso - PriceLab-Mercado

Esta guía detalla cómo usar el simulador de mercado con agentes IA para análisis de estrategias de precios y escenarios macroeconómicos.

## Inicio Rápido

### Instalación y Configuración

1. **Verificar Python 3.12+**
   ```bash
   python3 --version
   ```

2. **Instalar dependencias** (toma ~5 minutos)
   ```bash
   python3 -m pip install -r requirements.txt
   ```

3. **Ejecutar simulación básica**
   ```bash
   python3 main.py
   ```

### Ejecución de Escenarios Predefinidos

El simulador incluye 3 escenarios predefinidos optimizados para análisis de pricing:

#### 1. Escenario Base (Estable)
```bash
python3 main.py --escenario base --seed 42
```
- **Propósito**: Línea base para comparaciones
- **Características**: Economía estable, inflación ~2%, desempleo ~12%
- **Duración**: ~30 segundos (50 ciclos)

#### 2. Shock de Inflación + Política Monetaria
```bash
python3 main.py --escenario shock_inflacion --seed 42
```
- **Propósito**: Analizar impacto de presiones inflacionarias
- **Características**: Inflación objetivo 3%, mayor volatilidad, tasas de interés elevadas
- **Use Cases**: Estrategias de precios en entornos inflacionarios

#### 3. Subsidio a Demanda + Restricción de Oferta
```bash
python3 main.py --escenario subsidio_y_restriccion_oferta --seed 42
```
- **Propósito**: Evaluar efectos de políticas públicas en mercados
- **Características**: Subsidio del 5% a demanda, oferta reducida al 85%
- **Use Cases**: Impacto de regulaciones y subsidios en pricing

### Ejecución Batch y Análisis Comparativo

#### Ejecutar Todos los Escenarios
```bash
python3 run_escenarios.py --escenarios base shock_inflacion subsidio_y_restriccion_oferta --seed 42
```

#### Ejecutar Escenarios Específicos
```bash
python3 run_escenarios.py --escenarios base shock_inflacion --seed 42
```

### Resultados y Outputs

Cada ejecución genera automáticamente en `results/`:

1. **Dashboard Visual** (`esc_[nombre]_dashboard_economico_completo_[timestamp].png`)
   - Gráficas de PIB, inflación, desempleo
   - Evolución de precios por categoría
   - Métricas de estabilidad económica

2. **Datos Detallados** (`esc_[nombre]_datos_[timestamp].csv`)
   - Serie temporal completa de todas las variables
   - Compatible con análisis adicional en Excel/Python

3. **Reporte Ejecutivo** (`esc_[nombre]_reporte_[timestamp].txt`)
   - Resumen de KPIs clave
   - Insights automáticos sobre tendencias

4. **Configuración Usada** (`esc_[nombre]_config_[timestamp].json`)
   - Parámetros exactos para reproducibilidad

#### Resultados Comparativos Batch
- **KPIs Consolidados**: `escenarios_kpis_[timestamp].csv`
- **Resumen Ejecutivo**: `escenarios_resumen_[timestamp].txt`

## Interpretación de Resultados

### KPIs Principales

| KPI | Rango Normal | Significado |
|-----|--------------|-------------|
| **PIB** | $100K - $1M | Tamaño total de la economía simulada |
| **Inflación** | -10% a +20% | Presión de precios general |
| **Desempleo** | 5% - 25% | Tensión en mercado laboral |
| **Empresas Activas** | 8-15 | Nivel de competencia |
| **Transacciones** | 1K - 50K | Actividad económica |

### Análisis de Sensibilidad de Precios

#### Elasticidades por Categoría
- **Alimentos**: Demanda inelástica (-0.3), esencial
- **Tecnología**: Demanda elástica (-1.2), discrecional  
- **Servicios**: Elasticidad media (-0.8), mixto
- **Manufacturados**: Elasticidad alta (-1.0), sustituibles

#### Indicadores de Estabilidad
- **Volatilidad de Precios**: < 15% considerado estable
- **Convergencia PIB**: Crecimiento sostenido > 5 ciclos
- **Solvencia Bancaria**: Ratio capital/activos > 8%

## Casos de Uso por Sector

### Retail y E-commerce
```bash
# Análisis de estrategia de precios estacional
python3 run_escenarios.py --escenarios base subsidio_y_restriccion_oferta --seed 42

# Evaluar:
# - Elasticidad de demanda por categoría
# - Impacto de promociones (subsidio)
# - Respuesta a escasez (restricción oferta)
```

### Servicios Financieros
```bash
# Análisis de riesgo crediticio en diferentes escenarios
python3 run_escenarios.py --escenarios base shock_inflacion --seed 42

# Evaluar:
# - Capacidad de pago en entornos inflacionarios
# - Demanda de crédito por tasas de interés
# - Riesgo de default sectorial
```

### Manufactura y Supply Chain
```bash
# Análisis de pricing bajo restricciones de oferta
python3 main.py --escenario subsidio_y_restriccion_oferta --seed 42

# Evaluar:
# - Márgenes óptimos con oferta limitada
# - Estrategias de pricing premium
# - Impacto en inventarios y producción
```

## Personalización Avanzada

### Crear Escenarios Personalizados

1. **Copiar escenario base**
   ```bash
   cp escenarios/base.json escenarios/mi_escenario.json
   ```

2. **Modificar parámetros clave**
   ```json
   {
     "economia": {
       "tasa_inflacion_objetivo": 0.05,  // 5% inflación
       "subsidio_demanda": 0.10          // 10% subsidio
     },
     "precios": {
       "ajuste_maximo_por_ciclo": 0.20   // 20% ajuste máximo
     }
   }
   ```

3. **Ejecutar escenario personalizado**
   ```bash
   python3 main.py --escenario mi_escenario --seed 42
   ```

### Parámetros Clave para Pricing

| Parámetro | Ubicación | Efecto |
|-----------|-----------|--------|
| `ajuste_maximo_por_ciclo` | precios | Velocidad de ajuste de precios |
| `sensibilidad_competencia` | precios | Respuesta a precios competidores |
| `subsidio_demanda` | economia | Boost artificial a demanda |
| `restriccion_oferta_factor` | economia | Limitación de capacidad |
| `tasa_interes_base` | sistema_bancario | Costo de capital |

## Validación y Quality Assurance

### Validación Automática de Resultados
```bash
python3 scripts/validar_kpis.py --escenarios base shock_inflacion subsidio_y_restriccion_oferta
```

### Suite Completa de Tests
```bash
./run_tests.sh
```

### Verificación Manual Rápida
```bash
# Verificar que main.py genera outputs
ls results/esc_*_dashboard_*.png

# Verificar contenido de reporte más reciente
cat results/esc_*_reporte_*.txt | tail -20
```

## Solución de Problemas Comunes

### Error: "ModuleNotFoundError"
```bash
# Reinstalar dependencias
python3 -m pip install -r requirements.txt --force-reinstall
```

### Error: "Escenario no encontrado"
```bash
# Verificar escenarios disponibles
ls escenarios/*.json

# Usar ruta completa si es necesario
python3 main.py --escenario escenarios/base.json
```

### Simulación muy lenta
```bash
# Reducir número de ciclos para testing
python3 main.py --escenario base --seed 42
# Editar config: "num_ciclos": 25
```

### Resultados inconsistentes
```bash
# Usar siempre la misma semilla para reproducibilidad
python3 main.py --escenario base --seed 42
```

## Contacto y Soporte

Para reportar problemas o solicitar nuevas funcionalidades:
- **Issues**: Usar el sistema de issues del repositorio
- **Documentación**: Revisar `/docs/` para información técnica detallada
- **Tests**: Ejecutar `./run_tests.sh` antes de reportar problemas

---

> **Nota**: Este simulador está optimizado para análisis de pricing y estrategia comercial. Para casos de uso en investigación académica, revisar `/docs/plan_todos_agentes_ia.md` para funcionalidades avanzadas de IA multiagente.
