# Dinámicas Empresariales Avanzadas

Este documento describe las nuevas características implementadas para mejorar el realismo de las dinámicas empresariales en el simulador económico.

## Características Implementadas

### 1. Política de Inventarios S,s

**Descripción:**
Implementación de la política (s,S) estándar en teoría de inventarios, donde:
- `s` = punto de reorden (reorder point)
- `S` = nivel objetivo de inventario (target stock level)

**Funcionamiento:**
- Las empresas solo producen cuando el inventario actual ≤ punto de reorden
- Cuando se activa la producción, se produce hasta alcanzar el nivel objetivo S
- Los parámetros se ajustan dinámicamente basado en la volatilidad de la demanda

**Atributos añadidos a EmpresaProductora:**
```python
self.inventario_objetivo = {}      # S: nivel objetivo por bien
self.punto_reorden = {}           # s: punto de reorden por bien
self.costo_almacenamiento = 0.01-0.03  # % del valor por ciclo
self.costo_faltante = 0.05-0.10        # Costo por unidad faltante
```

**Costos asociados:**
- **Costo de almacenamiento:** % del valor del inventario por ciclo
- **Costo de faltante:** Penalización cuando stock < punto de reorden

### 2. Costos de Ajuste de Precios (Menu Costs)

**Descripción:**
Implementación de costos de ajuste de precios que crean rigidez realista según la literatura económica.

**Funcionamiento:**
- Las empresas pagan un costo fijo cada vez que cambian precios
- Solo cambian precios cuando el beneficio esperado supera el costo de ajuste
- Existe un umbral mínimo de cambio para justificar el costo

**Atributos añadidos:**
```python
self.costo_ajuste_precio = 100-500        # Costo fijo por cambio
self.historial_cambios_precio = {}        # Registro de cambios
self.ciclos_sin_cambio_precio = {}        # Contador por bien
self.umbral_cambio_precio = 0.03-0.08     # Cambio mínimo requerido
```

**Lógica de decisión:**
1. Calcular cambio de precio propuesto
2. Si cambio < umbral → No cambiar (rigidez)
3. Si beneficio esperado > costo ajuste → Cambiar y pagar costo
4. Si muchos ciclos sin cambio (>10) → Forzar ajuste

### 3. Sistema de Rotación Empresarial

**Descripción:**
Proceso realista de entrada y salida de empresas del mercado.

**Quiebra empresarial:**
- Sistema progresivo de ayuda antes de la quiebra:
  1. Ciclo 1: Reducir costos operativos (20%)
  2. Ciclo 2: Buscar préstamo de emergencia
  3. Ciclo 5+: Rescate gubernamental o quiebra definitiva

**Entrada de empresas:**
- Proceso Poisson con probabilidad base de 0.1% por ciclo
- Factores que afectan la entrada:
  - Crecimiento PIB > 2% → Probabilidad × 1.5
  - Crisis financiera activa → Probabilidad × 0.3

**Métodos clave:**
```python
mercado.gestionar_rotacion_empresas(ciclo)  # Gestión automática
mercado.crear_nueva_empresa(ciclo)          # Crear empresa entrante
empresa.verificar_estado_financiero()       # Detección de quiebra
```

### 4. Nuevos KPIs de Dinámicas Empresariales

**KPIs implementados:**
- **Tasa de quiebra:** % empresas que fallan por ciclo
- **Rotación empresarial:** (Entradas + Salidas) / Total empresas
- **Rigidez de precios:** % bienes sin cambio de precio por 3+ ciclos
- **Ratio de inventario:** Stock actual / Objetivo promedio
- **Costos de ajuste:** Total gastos en cambios de precio

**Reporte en simulación:**
```
🏢 DINÁMICAS EMPRESARIALES:
   Tasa Quiebra: 2.1% | Rotación: 4.5%
   Rigidez Precios: 65.3% | Empresas Nuevas: 1
   Ratio Inventario: 0.85 | Costos Ajuste: $2,340
```

## Configuración

### Parámetros en config_simulacion.json

No se requieren nuevos parámetros de configuración. El sistema usa los existentes:

```json
{
  "empresas_hiperrealistas": {
    "activar": true,
    "probabilidad_crisis_empresa": 0.02
  },
  "precios": {
    "ajuste_maximo_por_ciclo": 0.15,
    "sensibilidad_stock": 0.15
  }
}
```

### Parámetros automáticos inicializados

Los parámetros S,s se calculan automáticamente para cada empresa:
- **S (objetivo):** 2-4 veces la capacidad de producción base
- **s (reorden):** 20-40% del objetivo
- **Costos ajuste:** 100-500 unidades monetarias
- **Umbral cambio:** 3-8% del precio actual

## Impacto Económico

### Efectos esperados:

1. **Mayor realismo:** Comportamiento empresarial más cercano a la realidad
2. **Rigidez de precios:** Fluctuaciones menos frecuentes y más suaves
3. **Gestión de inventarios:** Optimización de costos de almacenamiento
4. **Rotación natural:** Mercados más dinámicos con entrada/salida constante
5. **Ciclos económicos:** Amplificación de fluctuaciones por inventarios

### Métricas de validación:

- **Rigidez de precios:** 50-80% típico en economías desarrolladas
- **Rotación empresarial:** 5-15% anual dependiendo del sector
- **Ratio inventario:** 0.8-1.2 para gestión eficiente

## Tests Implementados

### Suite de testing (tests/unit/test_dinamicas_empresariales.py):

1. **TestInventariosSs:** Política S,s
   - Inicialización de parámetros
   - Lógica de producción S,s
   - Ajuste dinámico de parámetros

2. **TestCostosAjustePrecios:** Rigidez de precios
   - Inicialización de costos
   - Rigidez por cambios pequeños
   - Aplicación de costos de ajuste

3. **TestRotacionEmpresarial:** Entrada/salida
   - Detección de quiebra
   - Entrada de nuevas empresas
   - Proceso completo de rotación

4. **TestKPIsEmpresariales:** Métricas
   - Cálculo básico de KPIs
   - KPI de rigidez de precios

**Ejecución:**
```bash
python3 -m pytest tests/unit/test_dinamicas_empresariales.py -v
```

## Integración con el Sistema

### Modificaciones realizadas:

1. **EmpresaProductora.py:** Core de las nuevas funcionalidades
2. **Mercado.py:** Gestión de rotación y cálculo de KPIs
3. **main.py:** Integración en el ciclo principal
4. **SimulacionReport.py:** Nuevos campos de reporte

### Compatibilidad:

- ✅ Compatible con sistemas existentes
- ✅ No afecta simulaciones existentes
- ✅ Activación automática sin configuración adicional
- ✅ Métricas adicionales en reportes

## Uso Avanzado

### Personalización de parámetros S,s:
```python
empresa.inventario_objetivo['bien'] = 150
empresa.punto_reorden['bien'] = 50
empresa.ajustar_politica_inventarios(mercado)
```

### Análisis de rigidez por sector:
```python
kpis = mercado.calcular_kpis_empresariales(ciclo)
rigidez = kpis['rigidez_precios']
```

### Simulación de crisis empresarial:
```python
empresa.dinero = 0
empresa.costos_fijos_mensuales = 10000
for _ in range(6):
    empresa.verificar_estado_financiero()
# empresa.en_quiebra será True
```