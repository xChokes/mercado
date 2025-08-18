# 🏛️ SIMULADOR ECONÓMICO AVANZADO

## 🎯 Descripción

Simulación económica completa que modela un ecosistema de mercado realista con múltiples agentes económicos, implementando dinámicas macroeconómicas avanzadas.

## ✨ Características Principales

- **Sistema Bancario Completo**: Bancos, créditos, política monetaria
- **Mercado Laboral**: Contrataciones, sindicatos, perfiles de habilidades
- **Machine Learning**: Predicción de demanda y optimización de precios
- **Crisis Financieras**: Detección automática y medidas de recuperación
- **Dashboard Avanzado**: Visualización en tiempo real de múltiples métricas
- **Precios Dinámicos**: Ajuste automático basado en oferta y demanda
- **Psicología Económica**: Sesgos cognitivos y decisiones irracionales

## 📁 Estructura del Proyecto

```
simulador-economico/
├── main.py                 # 🚀 Archivo principal de ejecución
├── src/                    # 📦 Código fuente
│   ├── models/            # 🏗️ Modelos económicos
│   │   ├── Mercado.py     # Coordinador central
│   │   ├── Bien.py        # Productos y servicios
│   │   ├── Persona.py     # Clase base agentes
│   │   ├── Consumidor.py  # Agentes consumidores
│   │   ├── Empresa.py     # Empresas básicas
│   │   ├── EmpresaProductora.py # Empresas manufactureras
│   │   ├── Gobierno.py    # Políticas públicas
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

## 📚 Casos de Uso

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
