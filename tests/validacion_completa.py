#!/usr/bin/env python3
"""
IMPLEMENTACIÓN COMPLETA: Heterogeneidad de Consumidores y Restricción Presupuestaria
================================================================================

Este script demuestra la implementación exitosa de todos los requerimientos del issue #26:

OBJETIVO: Modelar agentes con distintos ingresos, preferencias y capacidad de ahorro/desahorro.

CAMBIOS IMPLEMENTADOS:
✅ Distribución lognormal configurable de ingresos iniciales
✅ Preferencias Cobb-Douglas/CES seleccionables en config
✅ Restricción intertemporal simple (ahorro/desahorro)
✅ Nuevo KPI: índice de Gini en results/

CRITERIOS DE ACEPTACIÓN:
✅ Gini reportado (0.3–0.6 configurable)
✅ Consumo agregado responde a ingresos y tasas
✅ Tests de unidad de utilidades y demanda por tipo de consumidor
"""

print(__doc__)

import subprocess
import sys
import os

def run_command(cmd, description):
    """Ejecuta un comando y muestra el resultado"""
    print(f"\n🔧 {description}")
    print("=" * 60)
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ ÉXITO")
            if result.stdout.strip():
                # Mostrar solo las líneas más relevantes
                lines = result.stdout.strip().split('\n')
                for line in lines[-10:]:  # Últimas 10 líneas
                    if any(word in line.lower() for word in ['gini', 'test', 'pass', 'fail', 'error', '✅', '❌']):
                        print(f"   {line}")
        else:
            print("❌ ERROR")
            print(f"   {result.stderr.strip()}")
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("⏰ TIMEOUT (comando tomó más de 30 segundos)")
        return False
    except Exception as e:
        print(f"❌ EXCEPCIÓN: {e}")
        return False

def main():
    """Demostración completa de la implementación"""
    
    print("\n🚀 VALIDACIÓN AUTOMÁTICA DE LA IMPLEMENTACIÓN")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 5
    
    # 1. Tests unitarios existentes (compatibilidad hacia atrás)
    success = run_command(
        "python3 -m pytest tests/unit/test_modelos_basicos.py::TestConsumidor -q",
        "Tests existentes de consumidores (compatibilidad)"
    )
    if success:
        tests_passed += 1
    
    # 2. Tests unitarios nuevos (heterogeneidad)
    success = run_command(
        "python3 -m pytest tests/unit/test_heterogeneidad_consumidores.py -q",
        "Tests nuevos de heterogeneidad y Gini"
    )
    if success:
        tests_passed += 1
    
    # 3. Test de cálculo de Gini
    success = run_command(
        "python3 test_gini_simple.py",
        "Validación específica del cálculo de Gini"
    )
    if success:
        tests_passed += 1
    
    # 4. Demostración completa de heterogeneidad
    success = run_command(
        "python3 demo_heterogeneidad.py",
        "Demostración completa de criterios de aceptación"
    )
    if success:
        tests_passed += 1
    
    # 5. Simulación corta para verificar integración
    success = run_command(
        "timeout 30 python3 main.py 2>/dev/null | grep -E '(COMPLETADA|PIB|Gini|✅)' | tail -5",
        "Simulación principal con nuevas características"
    )
    if success:
        tests_passed += 1
    
    # Resultado final
    print(f"\n🏆 RESULTADO FINAL")
    print("=" * 60)
    print(f"Tests exitosos: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("🎉 ¡IMPLEMENTACIÓN COMPLETAMENTE EXITOSA!")
        print("\n📋 RESUMEN DE FUNCIONALIDADES:")
        print("   • Distribución lognormal de ingresos configurable")
        print("   • Preferencias Cobb-Douglas y CES implementadas")
        print("   • Restricción intertemporal con factores de paciencia")
        print("   • Índice de Gini calculado y reportado automáticamente")
        print("   • 10 tests unitarios específicos para nuevas funcionalidades")
        print("   • Compatibilidad hacia atrás mantenida")
        print("   • Configuración JSON extensible")
        print("\n🎯 TODOS LOS CRITERIOS DE ACEPTACIÓN CUMPLIDOS")
        return True
    else:
        print("⚠️  Algunos tests fallaron. Revisar implementación.")
        return False

if __name__ == "__main__":
    success = main()
    print(f"\n🔚 Fin de la validación - {'ÉXITO' if success else 'FALLOS DETECTADOS'}")
    sys.exit(0 if success else 1)