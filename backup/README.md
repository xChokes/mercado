# 🏛️ SIMULADOR ECONÓMICO AVANZADO v2.0

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production-brightgreen.svg)]()

## 🎯 Descripción

Simulación económica avanzada que modela un ecosistema de mercado completo con múltiples agentes económicos, implementando leyes económicas realistas y dinámicas macroeconómicas sofisticadas.

## ✨ Sistemas Implementados

### 🏦 Sistema Bancario

- Bancos comerciales con intermediación financiera
- Sistema de crédito con evaluación de riesgo
- Banco Central con política monetaria
- Tasas de interés diferenciadas

### 🏭 Sectores Económicos

- Sectores primario, secundario y terciario
- Matriz insumo-producto
- Cadenas de suministro
- Shocks sectoriales con propagación

### 🔬 Innovación y Tecnología

- I+D empresarial
- Ciclos de vida de productos
- Adopción tecnológica
- Spillovers tecnológicos

### 🧠 Psicología Económica

- Sesgos cognitivos (anclaje, aversión pérdidas, etc.)
- Decisiones irracionales
- Influencia social
- Perfiles psicológicos individualizados

### 🤖 Analytics y Machine Learning

- Predicción de demanda
- Optimización de precios
- Clusterización de agentes
- Análisis predictivo

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
└── requirements.txt       # 📋 Dependencias
```

## 🚀 Instalación y Uso

### Prerrequisitos

```bash
Python 3.8+
pip (gestor de paquetes)
```

### Instalación

```bash
# Clonar repositorio
git clone https://github.com/xChokes/mercado.git
cd mercado

# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### Ejecución

```bash
# Ejecutar simulación principal
python main.py
```

## 📊 Salidas del Simulador

### Análisis Generados

- **Reporte económico completo** con indicadores macroeconómicos
- **Gráficos multi-panel** con 9 métricas principales
- **Análisis sectorial** detallado
- **Estadísticas de sistemas avanzados**
- **Ranking empresarial** por capital

### Archivos de Salida

- `results/simulacion_economica_avanzada_[timestamp].png` - Gráficos de análisis
- Logs detallados en consola
- Estadísticas de performance del sistema

## 🎮 Personalización

### Parámetros Configurables

- **Número de ciclos**: Duración de la simulación
- **Cantidad de agentes**: Consumidores y empresas
- **Tipos de bienes**: Productos y servicios
- **Políticas gubernamentales**: Impuestos, gasto público
- **Parámetros ML**: Configuración de algoritmos

### Extensiones Disponibles

- Nuevos tipos de agentes económicos
- Sistemas sectoriales adicionales
- Algoritmos de ML más sofisticados
- Visualizaciones personalizadas

## 📈 Características Técnicas

### Modelado Económico

- **Elasticidades realistas** por tipo de bien
- **Ciclos económicos** dinámicos
- **Shocks económicos** aleatorios
- **Políticas contracíclicas** automáticas

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
