# 🌟 SIMULADOR ECONÓMICO AVANZADO

## 🎯 Visión General

Este es un simulador económico completo que modela un ecosistema de mercado con múltiples agentes económicos, implementando leyes económicas realistas, dinámicas macroeconómicas y sistemas avanzados de comportamiento económico.

## 🆕 MEJORAS IMPLEMENTADAS

### 🏦 Sistema Bancario Completo

- **Intermediación financiera** con bancos que ofrecen créditos y depósitos
- **Evaluación de riesgo crediticio** basada en ingresos, empleo y historial
- **Tasas de interés diferenciadas** según el perfil de riesgo
- **Política monetaria** del banco central con regla de Taylor
- **Morosidad y gestión de riesgos** bancarios

### 🏭 Sectores Económicos Diferenciados

- **Tres sectores económicos**: Primario, Secundario y Terciario
- **Matriz insumo-producto** que modela interdependencias sectoriales
- **Especialización empresarial** por sector productivo
- **Spillovers tecnológicos** entre sectores
- **Shocks sectoriales** con efectos de propagación

### 🧠 Psicología Económica y Behavioral Economics

- **Sesgos cognitivos** implementados:
  - Sesgo de anclaje en precios
  - Aversión a las pérdidas
  - Efecto manada
  - Sesgo de confirmación
  - Sesgo del presente
  - Efecto dotación
- **Estados emocionales** que afectan decisiones económicas
- **Influencia social** y tendencias de mercado
- **Decisiones no racionales** basadas en psicología

### 🔬 Sistema de Innovación y Tecnología

- **Inversión en I+D** empresarial con probabilidades de breakthrough
- **Adopción tecnológica** con difusión gradual
- **Productos innovadores** con ciclos de vida realistas
- **Spillovers tecnológicos** que benefician a todo el sector
- **Mejoras de productividad** basadas en tecnología

## 📊 Métricas y Análisis Avanzados

### Nuevos Indicadores Implementados

- **Sistema Bancario**: Crédito total, depósitos, morosidad, ratios de liquidez
- **Sectores**: PIB sectorial, participación por sector, nivel de desarrollo
- **Psicología**: Optimismo, estrés financiero, confianza del consumidor
- **Innovación**: Inversión I+D, productos nuevos, adopción tecnológica

### Visualizaciones Mejoradas

- **12 gráficos especializados** que muestran diferentes aspectos de la economía
- **Curva de Phillips** (inflación vs desempleo)
- **Análisis de correlaciones** macroeconómicas
- **Tendencias sectoriales** y estructurales
- **Indicadores psicológicos** del mercado

## 🚀 Cómo Usar el Simulador

### Requisitos

```bash
pip install matplotlib numpy
```

### Ejecución Básica

```bash
python main_avanzado.py
```

### Ejecución de Tests

```bash
python test_sistemas_avanzados.py
```

### Configuración Original

```bash
python main_mejorado.py
```

## 📁 Estructura de Archivos

### Archivos Principales

- `main_avanzado.py` - **NUEVO**: Simulador con todos los sistemas integrados
- `main_mejorado.py` - Simulador original mejorado
- `test_sistemas_avanzados.py` - **NUEVO**: Tests de funcionalidad

### Sistemas Nuevos

- `SistemaBancario.py` - **NUEVO**: Sistema bancario completo
- `SectoresEconomicos.py` - **NUEVO**: Sectores económicos diferenciados
- `PsicologiaEconomica.py` - **NUEVO**: Behavioral economics
- `SistemaInnovacion.py` - **NUEVO**: I+D y tecnología

### Documentación

- `DOCUMENTACION_COMPLETA.md` - **NUEVO**: Documentación técnica completa
- `PLAN_MEJORAS.md` - **NUEVO**: Plan de mejoras implementadas
- `README.md` - **ACTUALIZADO**: Este archivo

### Archivos Core (Mejorados)

- `Mercado.py` - **MEJORADO**: Integra todos los sistemas nuevos
- `Consumidor.py` - **MEJORADO**: Decisiones con psicología económica
- `ConfigEconomica.py` - Configuración económica base
- `Empresa.py`, `EmpresaProductora.py` - Lógica empresarial
- `Gobierno.py` - Políticas fiscales y monetarias
- `Bien.py` - Características de productos

## 🎮 Características Únicas del Simulador

### 1. **Realismo Económico**

- Elasticidades de demanda diferenciadas por categoría
- Ciclos económicos endógenos (expansión, recesión, depresión, recuperación)
- Shocks económicos aleatorios con efectos sistémicos
- Política fiscal y monetaria responsiva

### 2. **Complejidad Comportamental**

- Agentes con perfiles psicológicos únicos
- Decisiones influenciadas por emociones y sesgos
- Efectos de red social y tendencias de mercado
- Aprendizaje y adaptación de comportamientos

### 3. **Innovación Tecnológica**

- Empresas invierten en I+D para desarrollar nuevas tecnologías
- Productos con ciclos de vida realistas
- Adopción tecnológica gradual con efectos de red
- Spillovers que benefician a sectores completos

### 4. **Sistema Financiero Sofisticado**

- Bancos que evalúan riesgo crediticio
- Política monetaria del banco central
- Creación de dinero mediante crédito
- Gestión de morosidad y crisis bancarias

## 📈 Resultados y Análisis

### Métricas Tradicionales

- **PIB**: Crecimiento económico agregado
- **Inflación**: Basada en índice de precios ponderado
- **Desempleo**: Dinámico con contrataciones/despidos
- **Distribución de riqueza**: Entre consumidores y empresas

### Métricas Avanzadas

- **Estructura económica**: Participación sectorial en PIB
- **Estabilidad financiera**: Ratios bancarios y morosidad
- **Innovación**: Intensidad I+D y adopción tecnológica
- **Bienestar social**: Indicadores psicológicos agregados

### Análisis Automático

- **Clasificación económica**: Determina tipo de economía (industrial, servicios, etc.)
- **Fases del ciclo**: Identificación automática de recesiones/expansiones
- **Alertas de riesgo**: Sistemas de early warning para crisis
- **Correlaciones**: Análisis de relaciones entre variables

## 🔧 Personalización y Extensión

### Parámetros Configurables (`ConfigEconomica.py`)

- Dinero inicial por tipo de agente
- Elasticidades de demanda por categoría
- Márgenes de ganancia empresariales
- Tasas de impuestos y gasto público
- Intensidad de sesgos psicológicos

### Nuevos Tipos de Bienes

```python
# Agregar en crear_bienes_avanzados()
bienes['NuevoProducto'] = Bien('NuevoProducto', 'categoria')
```

### Nuevas Tecnologías

```python
# Agregar en SistemaInnovacion._crear_tecnologias_iniciales()
nueva_tech = Tecnologia("Nueva Tech", TipoInnovacion.PROCESO, 1.25, 0.15, 75000)
```

## 🎯 Casos de Uso

1. **Investigación Económica**: Testeo de teorías macroeconómicas
2. **Educación**: Visualización de conceptos económicos complejos
3. **Análisis de Políticas**: Simulación de impacto de medidas gubernamentales
4. **Behavioral Economics**: Estudio de sesgos en decisiones económicas
5. **Innovación**: Análisis de difusión tecnológica
6. **Sistema Financiero**: Modelado de crisis y estabilidad bancaria

## 📊 Outputs Generados

### Gráficos

- `economia_avanzada_[timestamp].png` - Análisis completo de 12 paneles
- Gráficos individuales de métricas específicas

### Reportes en Consola

- Análisis económico detallado
- Estado de todos los sistemas
- Ranking de empresas por desempeño
- Indicadores de desarrollo económico

## 🔬 Testing y Validación

### Tests Automatizados

```bash
python test_sistemas_avanzados.py
```

### Tests Incluidos

- ✅ Sistema bancario (préstamos, depósitos, morosidad)
- ✅ Sectores económicos (asignación, estadísticas)
- ✅ Psicología económica (perfiles, sesgos)
- ✅ Sistema de innovación (I+D, adopción)
- ✅ Integración completa (todos los sistemas)

## 🚧 Limitaciones y Trabajo Futuro

### Limitaciones Actuales

- No incluye comercio internacional ni divisas
- Sector público simplificado
- Sin modelado de recursos naturales
- Geografía económica no implementada

### Expansiones Futuras Planeadas

- **Comercio Internacional**: Países, divisas, balanza comercial
- **Recursos Naturales**: Sostenibilidad ambiental
- **Machine Learning**: Predicción inteligente de demanda
- **Redes Sociales**: Modelado de influencia más sofisticado

## 👨‍💻 Contribución

Para contribuir al proyecto:

1. Fork el repositorio
2. Crear branch de feature
3. Implementar mejoras con tests
4. Documentar cambios
5. Submit pull request

## 📄 Licencia

MIT License - Ver archivo LICENSE para detalles

## 🙏 Reconocimientos

Inspirado en:

- Modelos macroeconómicos DSGE
- Literatura de behavioral economics
- Sistemas multi-agente económicos
- Teorías de innovación y difusión tecnológica

---

**🎉 ¡Disfruta explorando la complejidad de la economía simulada!**
