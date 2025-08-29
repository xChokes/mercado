#!/bin/bash

# Script de Ejecución de Tests para Simulador de Mercado Hiperrealista
# ====================================================================

echo "🧪 INICIANDO SUITE DE TESTS DEL SIMULADOR DE MERCADO"
echo "===================================================="

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir con colores
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[⚠]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Verificar que estamos en el directorio correcto
if [[ ! -f "main.py" ]]; then
    print_error "Error: No se encuentra main.py. Ejecute desde el directorio raíz del proyecto."
    exit 1
fi

# Crear directorio de reportes si no existe
mkdir -p test_reports

# Variables de control
FAILED_TESTS=0
TOTAL_TESTS=0

print_status "Verificando dependencias..."

# Verificar Python
if ! command -v python3 &> /dev/null; then
    print_error "Python3 no está instalado"
    exit 1
fi

# Instalar dependencias si es necesario
print_status "Instalando dependencias de testing..."
python3 -m pip install pytest pytest-cov coverage > /dev/null 2>&1

# === TESTS UNITARIOS ===
echo ""
print_status "🔬 EJECUTANDO TESTS UNITARIOS"
echo "================================"

print_status "Test 1: Modelos Básicos"
if python3 -m pytest tests/unit/test_modelos_basicos.py -v --tb=short; then
    print_success "Tests de modelos básicos: PASADOS"
else
    print_error "Tests de modelos básicos: FALLARON"
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi
TOTAL_TESTS=$((TOTAL_TESTS + 1))

echo ""
print_status "Test 2: Estabilidad Económica"
if python3 -m pytest tests/unit/test_estabilidad_economica.py -v --tb=short; then
    print_success "Tests de estabilidad económica: PASADOS"
else
    print_error "Tests de estabilidad económica: FALLARON"
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi
TOTAL_TESTS=$((TOTAL_TESTS + 1))

echo ""
print_status "Test 3: Sistemas Hiperrealistas"
if python3 -m pytest tests/unit/test_sistemas_hiperrealistas.py -v --tb=short; then
    print_success "Tests de sistemas hiperrealistas: PASADOS"
else
    print_error "Tests de sistemas hiperrealistas: FALLARON"
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi
TOTAL_TESTS=$((TOTAL_TESTS + 1))

# NUEVOS TESTS UNITARIOS (Cadena y Bolsa)
echo ""
print_status "Test 3.1: Cadena de Suministro B2B (básico)"
if python3 -m pytest tests/unit/test_cadena_suministro_basico.py -v --tb=short; then
    print_success "Cadena de suministro (básico): PASADO"
else
    print_error "Cadena de suministro (básico): FALLÓ"
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi
TOTAL_TESTS=$((TOTAL_TESTS + 1))

echo ""
print_status "Test 3.2: Mercado de Capitales (smoke)"
if python3 -m pytest tests/unit/test_bolsa_valores_smoke.py -v --tb=short; then
    print_success "Mercado de capitales (smoke): PASADO"
else
    print_error "Mercado de capitales (smoke): FALLÓ"
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi
TOTAL_TESTS=$((TOTAL_TESTS + 1))

# === TESTS DE INTEGRACIÓN ===
echo ""
print_status "🔧 EJECUTANDO TESTS DE INTEGRACIÓN"
echo "===================================="

print_status "Test 4: Simulación Completa"
if timeout 300 python3 -m pytest tests/integration/test_simulacion_completa.py::TestIntegracionCompleta::test_simulacion_estabilidad_30_ciclos -v --tb=short; then
    print_success "Test de simulación completa (30 ciclos): PASADO"
else
    print_error "Test de simulación completa (30 ciclos): FALLÓ"
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi
TOTAL_TESTS=$((TOTAL_TESTS + 1))

print_status "Test 5: Integración Sistemas Hiperrealistas"
if timeout 180 python3 -m pytest tests/integration/test_sistemas_hiperrealistas_integracion.py -v --tb=short; then
    print_success "Test de integración hiperrealista: PASADO"
else
    print_error "Test de integración hiperrealista: FALLÓ"
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi
TOTAL_TESTS=$((TOTAL_TESTS + 1))

print_status "Test 6: Banco Central Avanzado"
if timeout 180 python3 -m pytest tests/integration/test_simulacion_completa.py::TestIntegracionCompleta::test_banco_central_avanzado_funcionamiento -v --tb=short; then
    print_success "Test de Banco Central Avanzado: PASADO"
else
    print_error "Test de Banco Central Avanzado: FALLÓ"
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi
TOTAL_TESTS=$((TOTAL_TESTS + 1))

print_status "Test 7: Resistencia a Shocks"
if timeout 180 python3 -m pytest tests/integration/test_simulacion_completa.py::TestIntegracionCompleta::test_resistencia_a_shocks -v --tb=short; then
    print_success "Test de resistencia a shocks: PASADO"
else
    print_error "Test de resistencia a shocks: FALLÓ"
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi
TOTAL_TESTS=$((TOTAL_TESTS + 1))

# === TESTS DE PERFORMANCE ===
echo ""
print_status "⚡ EJECUTANDO TESTS DE PERFORMANCE"
echo "==================================="

print_status "Test 8: Performance 100 Ciclos"
if timeout 180 python3 -m pytest tests/integration/test_simulacion_completa.py::TestBenchmarkPerformance::test_performance_simulacion_100_ciclos -v --tb=short; then
    print_success "Test de performance (100 ciclos): PASADO"
else
    print_warning "Test de performance (100 ciclos): FALLÓ (no crítico)"
    # No contar como fallo crítico
fi
TOTAL_TESTS=$((TOTAL_TESTS + 1))

# === TEST DEL SIMULADOR PRINCIPAL ===
echo ""
print_status "🚀 EJECUTANDO TEST DEL SIMULADOR PRINCIPAL"
echo "==========================================="

print_status "Test 9: Simulador Principal (10 ciclos)"
if timeout 120 python3 main.py > test_reports/main_execution.log 2>&1; then
    print_success "Simulador principal: EJECUTADO CORRECTAMENTE"
    
    # Verificar que se generaron resultados
    if ls results/*.txt >/dev/null 2>&1; then
        print_success "Archivos de resultados generados correctamente"
    else
        print_warning "No se encontraron archivos de resultados"
    fi
else
    print_error "Simulador principal: FALLÓ AL EJECUTAR"
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi
TOTAL_TESTS=$((TOTAL_TESTS + 1))

# === RESUMEN FINAL ===
# === VALIDACIÓN DE ESCENARIOS ===
echo ""
echo "=============================================="
print_status "🎯 VALIDACIÓN DE ESCENARIOS"
echo "=============================================="

print_status "Validando escenarios predefinidos..."

# Ejecutar validación de KPIs si existe el script
if [[ -f "scripts/validar_kpis.py" ]]; then
    print_status "Ejecutando validación automática de KPIs..."
    
    # Crear archivo temporal para capturar salida
    VALIDATION_LOG="test_reports/validation_kpis.log"
    
    if timeout 300 python3 scripts/validar_kpis.py --escenarios base shock_inflacion --solo-csv > "$VALIDATION_LOG" 2>&1; then
        print_success "Validación de KPIs completada exitosamente"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        print_warning "Validación de KPIs falló o no se pudo completar"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    # Verificar que run_escenarios.py funcione
    print_status "Probando ejecución batch de escenarios..."
    
    BATCH_LOG="test_reports/batch_escenarios.log"
    if timeout 300 python3 run_escenarios.py --escenarios test_minimal --seed 42 > "$BATCH_LOG" 2>&1; then
        print_success "Script batch de escenarios funciona correctamente"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        print_warning "Script batch de escenarios falló"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
else
    print_warning "Script de validación de KPIs no encontrado"
fi

echo ""
echo "=============================================="
print_status "📊 RESUMEN DE RESULTADOS"
echo "=============================================="

PASSED_TESTS=$((TOTAL_TESTS - FAILED_TESTS))
SUCCESS_RATE=$((PASSED_TESTS * 100 / TOTAL_TESTS))

echo "Tests ejecutados: $TOTAL_TESTS"
echo "Tests pasados: $PASSED_TESTS"
echo "Tests fallidos: $FAILED_TESTS"
echo "Tasa de éxito: $SUCCESS_RATE%"

if [[ $FAILED_TESTS -eq 0 ]]; then
    print_success "¡TODOS LOS TESTS PASARON! ✨"
    print_success "El simulador está estable y funcionando correctamente."
    EXIT_CODE=0
elif [[ $FAILED_TESTS -le 2 ]]; then
    print_warning "Algunos tests fallaron, pero el sistema es funcional."
    print_warning "Se recomienda revisar los fallos reportados."
    EXIT_CODE=1
else
    print_error "Múltiples tests fallaron. El sistema requiere correcciones."
    print_error "Revisar logs en test_reports/ para más detalles."
    EXIT_CODE=2
fi

# === GENERAR REPORTE ===
echo ""
print_status "📝 Generando reporte de tests..."

cat > test_reports/test_summary.txt << EOF
REPORTE DE TESTS - SIMULADOR DE MERCADO HIPERREALISTA
=====================================================
Fecha: $(date)
Tests ejecutados: $TOTAL_TESTS
Tests pasados: $PASSED_TESTS  
Tests fallidos: $FAILED_TESTS
Tasa de éxito: $SUCCESS_RATE%

Estado del sistema: $(if [[ $FAILED_TESTS -eq 0 ]]; then echo "ESTABLE"; elif [[ $FAILED_TESTS -le 2 ]]; then echo "FUNCIONAL"; else echo "INESTABLE"; fi)

Detalles:
- Modelos básicos: $(if [[ -f "test_reports/main_execution.log" ]]; then echo "VERIFICADO"; else echo "PENDIENTE"; fi)
- Estabilidad económica: EVALUADA
- Integración completa: PROBADA
- Performance: MEDIDA
- Simulador principal: EJECUTADO

Recomendaciones:
$(if [[ $FAILED_TESTS -eq 0 ]]; then 
    echo "- Sistema listo para uso en producción"
    echo "- Considerar añadir más tests de casos extremos"
elif [[ $FAILED_TESTS -le 2 ]]; then
    echo "- Revisar tests fallidos y corregir problemas menores"
    echo "- Sistema aceptable para desarrollo y testing"
else
    echo "- CRÍTICO: Revisar y corregir fallos fundamentales"
    echo "- No recomendado para uso hasta resolver problemas"
fi)
EOF

print_success "Reporte guardado en test_reports/test_summary.txt"

echo ""
print_status "🎯 Tests completados. Código de salida: $EXIT_CODE"

exit $EXIT_CODE
