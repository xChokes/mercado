# 📊 SIMULADOR ECONÓMICO AVANZADO - DOCUMENTACIÓN TÉCNICA

## 🎯 VISIÓN GENERAL DEL PROYECTO

Esta es una simulación económica completa que modela un ecosistema de mercado con múltiples agentes económicos, implementando leyes económicas realistas y dinámicas macroeconómicas.

## 📚 ARQUITECTURA DEL SISTEMA

### Componentes Principales

1. **🏪 Mercado** (`Mercado.py`) - Sistema central que coordina todas las interacciones
2. **👥 Agentes Económicos:**
   - **Consumidores** (`Consumidor.py`) - Individuos que compran bienes y servicios
   - **Empresas** (`Empresa.py`) - Entidades comerciales básicas
   - **Empresas Productoras** (`EmpresaProductora.py`) - Manufacturas especializadas
3. **🏛️ Gobierno** (`Gobierno.py`) - Política fiscal y monetaria
4. **📈 Mercado Financiero** (`MercadoFinanciero.py`) - Sistema de acciones y inversiones
5. **🛍️ Bienes** (`Bien.py`) - Productos con características económicas específicas

### Arquitectura de Clases

```
Persona (Base)
├── Consumidor
├── Empresa
│   └── EmpresaProductora
└── Gobierno

Mercado (Coordinador Central)
├── MercadoFinanciero
├── ConfigEconomica
└── Bien
```

## 🔧 CARACTERÍSTICAS TÉCNICAS IMPLEMENTADAS

### Modelado Económico Realista

#### 1. **Elasticidades de Demanda**

- **Precio**: Respuesta de la demanda a cambios de precios
- **Ingreso**: Respuesta de la demanda a cambios de ingresos
- **Categorización por tipo de bien** (básicos, lujo, duraderos)

#### 2. **Ciclos Económicos**

- **Fases**: Expansión → Recesión → Depresión → Recuperación
- **Detección automática** basada en indicadores PIB y desempleo
- **Efectos diferenciados** por fase en todos los agentes

#### 3. **Shocks Económicos**

- **Tipos**: Inflacionarios, deflacionarios, financieros, de oferta
- **Ocurrencia aleatoria** con efectos temporales
- **Impacto sistémico** en toda la economía

#### 4. **Indicadores Macroeconómicos**

- **PIB** (Producto Interno Bruto)
- **Inflación** basada en índice de precios ponderado
- **Desempleo** dinámico con contrataciones/despidos
- **Competencia** medida por índice Herfindahl-Hirschman

### Agentes Económicos Sofisticados

#### Consumidores

- **Características laborales**: Empleado/desempleado, habilidades, ingresos
- **Comportamiento económico**: Propensión al consumo/ahorro, aversión al riesgo
- **Factores psicológicos**: Imitación social, fidelidad de marca
- **Utilidad marginal decreciente**: Satisfacción decrece con más consumo

#### Empresas Productoras

- **Estrategias de precios**: Líder en costos, diferenciación, nicho
- **Capacidades de producción**: Dinámicas con economías de escala
- **Gestión de empleados**: Contratación/despido basado en demanda
- **Reinversión inteligente**: Expansión basada en utilización de capacidad

#### Gobierno

- **Política fiscal**: Impuestos progresivos, gasto público contracíclico
- **Política monetaria**: Tasa de interés de referencia
- **Servicios públicos**: Subsidios de desempleo, compras gubernamentales
- **Indicadores macroeconómicos**: Cálculo y monitoreo continuo

## 📊 MÉTRICAS Y ANÁLISIS

### Estadísticas Implementadas

1. **PIB histórico** con cálculo de crecimiento
2. **Inflación mensual** y promedio
3. **Tasa de desempleo** dinámica
4. **Distribución de dinero** por tipo de agente
5. **Precios promedio** por categoría de bien
6. **Volumen de transacciones** por ciclo
7. **Nivel de competencia** por mercado

### Visualizaciones Generadas

- **Evolución del PIB** con tendencias
- **Tasa de inflación** vs objetivo gubernamental
- **Desempleo** vs tasa natural
- **Distribución de riqueza** (consumidores vs empresas)
- **Evolución de precios** promedio
- **Actividad económica** (transacciones)

## ⚙️ CONFIGURACIÓN ECONÓMICA

### Parámetros Clave (`ConfigEconomica.py`)

#### Monetarios

- Dinero inicial: Consumidores (10K-50K), Empresas (100K-500K), Productoras (500K-2M)
- Salarios: 2,000-8,000 con variabilidad por habilidades

#### Elasticidades por Categoría

```python
ELASTICIDADES_PRECIO = {
    'alimentos_basicos': -0.3,  # Inelásticos
    'alimentos_lujo': -1.2,     # Elásticos
    'servicios': -0.8,
    'bienes_duraderos': -1.5,
    'combustibles': -0.2
}
```

#### Márgenes y Costos

- Márgenes de ganancia: 20%-80%
- Producción base: 50-200 unidades
- Factor de reinversión: 30% de ganancias

## 🚀 PROCESO DE SIMULACIÓN

### Flujo por Ciclo

1. **Detección de fase económica** y aplicación de efectos
2. **Simulación de shocks** económicos aleatorios
3. **Ciclo gubernamental** (políticas, impuestos, gasto)
4. **Actualización de competencia** por mercado
5. **Ciclos individuales** de cada agente económico
6. **Registro de estadísticas** y métricas
7. **Reporte periódico** del estado económico

### Ciclo Individual por Agente

#### Consumidores

- Cálculo de ingreso disponible
- Decisiones de consumo basadas en utilidad marginal
- Búsqueda de mejores precios con fidelidad de marca
- Compras con efectos de red social
- Actualización de satisfacción y preferencias

#### Empresas Productoras

- Estimación de demanda por bien
- Decisiones de producción óptima
- Ajuste dinámico de precios
- Gestión de inventarios
- Contratación/despido de empleados
- Estrategias de expansión/contracción

#### Gobierno

- Recaudación de impuestos progresivos
- Ejecución de gasto público contracíclico
- Política monetaria basada en inflación
- Monitoreo de indicadores macroeconómicos

## 📈 RESULTADOS Y ANÁLISIS

### Métricas de Evaluación

- **Estabilidad macroeconómica**: Volatilidad de PIB, inflación, desempleo
- **Eficiencia de mercado**: Nivel de competencia, formación de precios
- **Distribución de riqueza**: Gini implícito, movilidad económica
- **Ciclos económicos**: Duración, amplitud, transiciones de fase
- **Efectividad de políticas**: Respuesta a intervenciones gubernamentales

### Outputs Generados

1. **Reporte económico detallado** con análisis final
2. **Gráficos multi-panel** con 6 métricas principales
3. **Ranking de empresas** por capital acumulado
4. **Estadísticas de transacciones** y volumen comercial
5. **Estado del ciclo económico** y competencia por mercado

## 🎯 CASOS DE USO

1. **Investigación económica**: Testeo de teorías macroeconómicas
2. **Educación**: Visualización de conceptos económicos complejos
3. **Análisis de políticas**: Simulación de impacto de medidas gubernamentales
4. **Modelado predictivo**: Entendimiento de dinámicas de mercado
5. **Análisis de crisis**: Estudio de efectos de shocks económicos

## 📋 LIMITACIONES ACTUALES

1. **Mercado internacional**: No considera comercio exterior
2. **Sistema bancario**: Ausencia de intermediarios financieros
3. **Innovación tecnológica**: No modela cambio tecnológico
4. **Geografía económica**: Mercado único sin regiones
5. **Complejidad sectorial**: Sectores económicos simplificados

## 🔧 ESTRUCTURA DE CÓDIGO

### Archivos Principales

- `main_mejorado.py` - Orquestador principal de simulación
- `Mercado.py` - Coordinador central con lógica macroeconómica
- `ConfigEconomica.py` - Parámetros y constantes económicas
- `Consumidor.py` - Comportamiento de agentes consumidores
- `EmpresaProductora.py` - Lógica empresarial y producción
- `Gobierno.py` - Políticas fiscales y monetarias
- `Bien.py` - Características de productos y elasticidades

### Patrones de Diseño Utilizados

- **Strategy Pattern**: Diferentes estrategias de precios empresariales
- **Observer Pattern**: Gobierno observa indicadores económicos
- **Factory Pattern**: Creación de bienes con características específicas
- **Singleton Pattern**: Configuración económica global

Este simulador representa un ecosistema económico funcional con características realistas que permite experimentar con diferentes escenarios y políticas económicas.
