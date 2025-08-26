# 🤖 Simulación de Mercado con Agentes IA Hiperrealistas

Este proyecto implementa una simulación avanzada de mercado económico con **agentes de inteligencia artificial hiperrealistas** que aprenden, se adaptan, forman coaliciones y evolución estratégicamente.

> **🎯 MVP Actual: PriceLab-Mercado** - Simulador ligero de estrategia de precios y shocks macro optimizado para análisis comercial (consulta `docs/FOCO_Y_HOJA_DE_RUTA.md`)

## 🚀 Inicio Rápido - PriceLab

### Instalación y Configuración
```bash
# 1. Verificar Python 3.12+
python3 --version

# 2. Instalar dependencias (5-10 minutos)
python3 -m pip install -r requirements.txt

# 3. Ejecutar simulación base
python3 main.py --escenario base --seed 42
```

### Escenarios Predefinidos para Análisis de Pricing
```bash
# Escenario Base (línea base estable)
python3 main.py --escenario base --seed 42

# Shock de Inflación + Política Monetaria  
python3 main.py --escenario shock_inflacion --seed 42

# Subsidio a Demanda + Restricción de Oferta
python3 main.py --escenario subsidio_y_restriccion_oferta --seed 42

# Ejecutar todos los escenarios y generar reporte comparativo
python3 run_escenarios.py --escenarios base shock_inflacion subsidio_y_restriccion_oferta --seed 42
```

### Demo Comparativo Interactivo
```bash
# Análisis completo Base vs Shock de Inflación con gráficas
python3 demo_comparativo.py --seed 42

# Versión rápida (25 ciclos)
python3 demo_comparativo.py --ciclos 25 --seed 42
```

### Validación y Quality Assurance
```bash
# Validar KPIs automáticamente
python3 scripts/validar_kpis.py --escenarios base shock_inflacion

# Suite completa de tests (incluye validación de escenarios)
./run_tests.sh

# Solo validar archivos CSV existentes
python3 scripts/validar_kpis.py --solo-csv
```

### Resultados Generados
Cada ejecución crea automáticamente en `results/`:
- 📊 **Dashboard visual** con gráficas de PIB, inflación, precios por categoría
- 📈 **Datos CSV** con series temporales completas 
- 📋 **Reporte ejecutivo** con KPIs y insights automáticos
- ⚙️ **Configuración** usada para reproducibilidad
- 📊 **Reportes comparativos** entre escenarios (batch)

### 📚 Documentación Completa

#### 📖 **Documentación de Usuario**
- **Guía de Usuario**: `docs/GUIA_USUARIO.md` - Manual completo con casos de uso
- **Foco y Hoja de Ruta**: `docs/FOCO_Y_HOJA_DE_RUTA.md` - Objetivos y estado del MVP
- **Estado de Implementación**: `docs/ESTADO_IMPLEMENTACION.md` - Funcionalidades y cobertura

#### 🔧 **Documentación Técnica**
- **📋 Índice de Documentación**: `docs/INDICE_DOCUMENTACION.md` - Guía completa de documentación técnica
- **🏗️ Documentación Técnica Principal**: `docs/DOCUMENTACION_TECNICA.md` - Arquitectura y sistemas
- **🤖 Guía de Agentes IA**: `docs/GUIA_AGENTES_IA.md` - Comportamientos y decisiones de agentes
- **🔗 Patrones de Integración**: `docs/PATRONES_INTEGRACION.md` - Comunicación y flujos de datos

---

## 🚀 Características Revolucionarias

### 🧠 **Inteligencia Artificial Avanzada**
- **Agentes con Memoria**: Sistema de memoria episódica y semántica
- **Aprendizaje por Refuerzo**: Decisiones adaptativas basadas en experiencia
- **Redes Neuronales Especializadas**: Deep Learning para predicción y optimización
- **Algoritmos Evolutivos**: Optimización automática de estrategias

### 🌐 **Redes Sociales Emergentes**
- **Relaciones Dinámicas**: Competencia, colaboración y alianzas estratégicas
- **Propagación de Información**: Difusión inteligente de datos de mercado
- **Formación de Coaliciones**: Agrupaciones automáticas para objetivos comunes
- **Reputación y Confianza**: Sistema de evaluación social entre agentes

### 🏪 **Mercado IA Central**
- **Detección de Crisis**: Predicción y prevención de burbujas y crashes
- **Optimización de Liquidez**: Gestión inteligente de recursos
- **Negociación Automática**: Plataforma de negociación multi-agente
- **Análisis de Patrones**: Identificación de tendencias emergentes

### 🎯 **Agentes Especializados**
- **Consumidores IA**: Aprenden patrones de compra, negocian precios, forman grupos
- **Empresas IA**: Estrategia competitiva, innovación, gestión de cadena de suministro
- **Meta-Aprendizaje**: Adaptación automática de parámetros de aprendizaje

## 🏗️ Arquitectura del Sistema

```
src/ai/                          # 🤖 ECOSISTEMA DE IA
├── AgentMemorySystem.py         # Memoria y aprendizaje de agentes
├── IADecisionEngine.py          # Motor de decisiones IA
├── AgentCommunicationProtocol.py # Comunicación entre agentes
├── OrquestadorAgentesIA.py      # Coordinador central
├── ConsumidorIA.py              # Consumidores inteligentes
├── EmpresaIA.py                 # Empresas estratégicas
├── MercadoIA.py                 # Mercado con IA central
├── RedSocialAgentesIA.py        # Redes sociales emergentes
├── SistemaDeepLearningIA.py     # Deep Learning y optimización
└── IntegradorAgentesIA.py       # 🎯 INTEGRADOR PRINCIPAL

src/models/                      # Modelos base
├── Consumidor.py
├── Empresa.py
├── Gobierno.py
└── Mercado.py

src/systems/                     # Sistemas económicos
├── SistemaBancario.py
├── MercadoTrabajo.py
└── GestorCrisis.py
```

## 🎮 Uso Rápido

### Ejecutar Ejemplo Completo
```bash
python ejemplo_uso_completo.py
```

### Ejecutar escenarios (MVP PriceLab)
```bash
python main.py --escenario base --seed 42
python main.py --escenario shock_inflacion --seed 42
python main.py --escenario subsidio_y_restriccion_oferta --seed 42

# Batch y comparativo
python run_escenarios.py --escenarios base shock_inflacion subsidio_y_restriccion_oferta --seed 42
```

### Implementación Básica
```python
from src.ai.IntegradorAgentesIA import IntegradorAgentesIA, ConfiguracionSistemaIA

# Configurar sistema
config = ConfiguracionSistemaIA(
    num_consumidores_ia=20,
    num_empresas_ia=8,
    entrenar_automaticamente=True
)

# Crear mercado con IA
bienes = ["comida", "tecnologia", "energia"]
sistema_ia = IntegradorAgentesIA(bienes, config)

# Ejecutar simulación
sistema_ia.ejecutar_ciclo_mercado(duracion_minutos=30)

# Obtener resultados
estado = sistema_ia.obtener_estado_completo()
print(f"Eficiencia: {estado['estadisticas']['eficiencia_global']}")
print(f"Transacciones IA: {estado['estadisticas']['transacciones_ia']}")
```

## 📊 Capacidades Demostradas

### ✅ **Emergencia de Comportamientos Complejos**
- Formación espontánea de alianzas comerciales
- Desarrollo de estrategias competitivas adaptativas
- Propagación viral de información de mercado
- Auto-organización de redes de suministro

### ✅ **Aprendizaje y Adaptación**
- Mejora continua de decisiones de compra/venta
- Adaptación a crisis económicas
- Optimización automática de precios
- Evolución de estrategias de negociación

### ✅ **Inteligencia Colectiva**
- Detección colaborativa de oportunidades
- Prevención distribuida de riesgos
- Optimización global a través de decisiones locales
- Emergencia de especialización sectorial

## 🔬 Para Investigadores

El sistema está diseñado para investigación en:
- **Economía Computacional**: Mercados artificiales complejos
- **Inteligencia Artificial Multi-Agente**: Coordinación y competencia
- **Sistemas Adaptativos Complejos**: Emergencia y auto-organización
- **Redes Sociales**: Formación y evolución de relaciones

### Métricas de Investigación
- Eficiencia de descubrimiento de precios
- Velocidad de propagación de información
- Estabilidad sistémica bajo perturbaciones
- Tasa de formación/disolución de coaliciones

## 🛠️ Instalación

```bash
# Clonar repositorio
git clone [repository_url]
cd mercado

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar ejemplo
python ejemplo_uso_completo.py
```

## 📈 Resultados Típicos

En simulaciones de 30 minutos con 20 consumidores y 8 empresas:
- **Transacciones**: 100-300 operaciones automáticas
- **Eficiencia**: 70-85% de eficiencia de mercado
- **Coaliciones**: 2-5 alianzas estratégicas emergentes
- **Aprendizaje**: 15-25 ciclos de entrenamiento de redes neuronales

## 🎯 Casos de Uso

1. **Simulación Económica**: Modelado de mercados complejos
2. **Investigación IA**: Desarrollo de agentes inteligentes
3. **Análisis de Políticas**: Impacto de regulaciones
4. **Educación**: Comprensión de dinámicas económicas
5. **Optimización**: Estrategias de trading automático

## 🤝 Contribuciones

Este proyecto implementa el **Plan de Agentes IA Hiperrealistas** completo, incluyendo:
- ✅ Fase 1: Fundamentos IA
- ✅ Fase 2: Agentes Consumidores IA  
- ✅ Fase 3: Agentes Empresariales IA
- ✅ Fase 4: Ecosistema de Mercado IA
- ✅ Fase 5: Redes Sociales y Colaboración
- ✅ Fase 6: Deep Learning y Optimización

## 📜 Licencia

MIT License - Ver archivo LICENSE para detalles.

---

**🎖️ Sistema de IA Económica de Última Generación**  
*Donde la inteligencia artificial encuentra la economía para crear el futuro de los mercados digitales*
│   │   ├── MercadoFinanciero.py # Sistema financiero
│   │   └── InventarioBien.py # Gestión inventarios
│   ├── systems/           # ⚙️ Sistemas avanzados
│   │   ├── SistemaBancario.py # Sistema bancario
│   │   ├── SectoresEconomicos.py # Sectores económicos
│   │   ├── SistemaInnovacion.py # I+D y tecnología
│   │   ├── PsicologiaEconomica.py # Behavioral economics
│   │   └── AnalyticsML.py # Machine learning
│   └── config/            # ⚙️ Configuración
│       └── ConfigEconomica.py # Parámetros económicos
├── docs/                  # 📚 Documentación
│   ├── DOCUMENTACION_COMPLETA.md
│   ├── PLAN_MEJORAS.md
│   └── RESUMEN_MEJORAS_IMPLEMENTADAS.md
├── tests/                 # 🧪 Tests
│   ├── test_sistemas_avanzados.py
│   └── test_visualizacion.py
├── results/               # 📊 Resultados de simulaciones
├── deprecated/            # 🗄️ Archivos antiguos
```

mercado/
├── main.py # 🚀 Archivo principal - ejecuta toda la simulación
├── config_simulacion.json # ⚙️ Configuración de parámetros
├── requirements.txt # � Dependencias
└── src/ # 📂 Código fuente modular
├── models/ # 🎭 Modelos de agentes económicos
├── systems/ # ⚡ Sistemas económicos avanzados
└── config/ # ⚙️ Configuración y gestión

````

## 🚀 Uso Rápido

### 1. Instalación

```bash
pip install -r requirements.txt
````

### 2. Ejecución

```bash
python main.py
```

## ⚙️ Configuración

Edita `config_simulacion.json` para personalizar:

- **Número de agentes económicos**
- **Duración de la simulación**
- **Parámetros económicos iniciales**
- **Activación de sistemas específicos**

## 📊 Resultados

La simulación genera automáticamente:

- **Gráficos interactivos** de métricas económicas
- **Datos CSV** para análisis posterior
- **Reportes textuales** con estadísticas detalladas
- **Archivos JSON** con configuración utilizada

## 🔧 Sistemas Integrados

### 🏦 Sistema Bancario

- Múltiples bancos comerciales
- Evaluación de riesgo crediticio
- Política monetaria del banco central

### 👷 Mercado Laboral

- Perfiles de habilidades individualizados
- Sindicatos y negociación colectiva
- Facilitación de contrataciones masivas

### 🤖 Machine Learning

- Predicción automática de demanda
- Optimización dinámica de precios
- Análisis de patrones de consumo

### 💰 Precios Dinámicos

- Ajuste automático por oferta/demanda
- Elasticidad diferenciada por categoría
- Competencia entre empresas

### 🚨 Crisis y Estímulos

- Detección automática de crisis financieras
- Medidas de recuperación económica
- Estímulos gubernamentales de emergencia

## 📈 Métricas Monitoreadas

- **PIB y crecimiento económico**
- **Inflación y deflación**
- **Tasa de desempleo**
- **Volumen de transacciones**
- **Salud del sistema bancario**
- **Distribución de la riqueza**

## 💡 Ejemplos de Uso

### Análisis de Crisis Económicas

```json
{
  "simulacion": {
    "activar_crisis": true,
    "tiempo_maximo_crisis": 15
  }
}
```

### Economía de Alto Empleo

```json
{
  "economia": {
    "tasa_desempleo_inicial": 0.05,
    "salario_base_minimo": 3000
  }
}
```

## 🔍 Monitoreo en Tiempo Real

El dashboard muestra en tiempo real:

- Evolución del PIB
- Fluctuaciones de precios
- Movimientos en el mercado laboral
- Actividad bancaria
- Indicadores de crisis

## 🎯 Casos de Uso

- **Investigación Económica**: Análisis de políticas macroeconómicas
- **Educación**: Enseñanza de principios económicos
- **Planificación**: Simulación de escenarios económicos
- **Validación**: Testing de teorías económicas

## 📝 Licencia

MIT License - Libre para uso académico y comercial

---

**¡Ejecuta `python main.py` y observa una economía completa en acción! 🚀**

### Agentes Inteligentes

- **Decisiones optimizadas** por ML
- **Comportamiento psicológico** realista
- **Aprendizaje adaptativo** durante simulación
- **Interacciones complejas** entre agentes

### Performance

- **Simulaciones rápidas** (50 ciclos en ~5 segundos)
- **Escalabilidad** para 1000+ agentes
- **Memoria eficiente** con garbage collection
- **Paralelización** disponible para análisis

## 🤝 Contribución

### Cómo Contribuir

1. Fork del repositorio
2. Crear rama de feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

### Áreas de Mejora

- [ ] Comercio internacional
- [ ] Sostenibilidad ambiental
- [ ] Crisis financieras
- [ ] Dashboard interactivo
- [ ] API REST para simulaciones

## � Estado de Implementación

- Resumen actualizado del avance, cambios recientes y backlog: ver `docs/ESTADO_IMPLEMENTACION.md`.
- Objetivo, KPIs y hoja de ruta: ver `docs/FOCO_Y_HOJA_DE_RUTA.md`.

## �📚 Casos de Uso

### Investigación Académica

- Testeo de teorías macroeconómicas
- Análisis de políticas públicas
- Modelado de crisis económicas
- Estudios de behavioral economics

### Educación

- Enseñanza de conceptos económicos
- Simulaciones interactivas para estudiantes
- Demostración de efectos de políticas
- Laboratorio virtual de economía

### Consultoría

- Modelado de escenarios económicos
- Análisis de impacto de regulaciones
- Forecasting económico
- Optimización de estrategias empresariales

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 👥 Autores

- **Simulador Económico Team** - _Desarrollo inicial_ - [xChokes](https://github.com/xChokes)

## 🙏 Agradecimientos

- Comunidad de Python científico
- Librerías scikit-learn, matplotlib, numpy
- Investigadores en economía computacional
- Beta testers y contributors

---

⭐ **¡Dale una estrella al proyecto si te resulta útil!** ⭐
