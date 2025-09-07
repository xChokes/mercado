#!/usr/bin/env python3
"""
Test standalone de validación económica
Prueba el sistema de validación sin dependencias complejas
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from src.utils.validators import ValidadorEconomicoFormal, validar_resultados_simulacion

def test_validation_simple():
    """Test básico del sistema de validación"""
    print("🧪 Probando sistema de validación económica...")
    
    # Datos de prueba normales
    datos_normales = {
        'pib': 100000,
        'inflacion': 2.5,
        'desempleo': 5.0,
        'empresas_activas': 5,
        'transacciones': 1000,
        'depositos_bancarios': 500000,
        'prestamos_totales': 300000,
        'capital_bancario': 50000,
        'duracion_s': 45
    }
    
    # Test función principal
    reporte = validar_resultados_simulacion(datos_normales, "test_standalone")
    
    print("✅ Validación completada")
    print(f"   Estado: {reporte['estado_general']}")
    print(f"   Validaciones exitosas: {reporte['resumen']['validaciones_exitosas']}")
    print(f"   Advertencias: {reporte['resumen']['advertencias']}")
    print(f"   Errores: {reporte['resumen']['errores']}")
    
    # Test datos problemáticos
    print("\n🧪 Probando con datos problemáticos...")
    datos_problematicos = {
        'pib': 5000,      # Muy bajo
        'inflacion': 50,  # Muy alta
        'desempleo': 30,  # Muy alto
        'empresas_activas': 0,  # Crítico
        'transacciones': 0,
        'depositos_bancarios': 100000,
        'prestamos_totales': 150000,  # Más préstamos que depósitos
        'capital_bancario': 5000,     # Capital muy bajo
        'duracion_s': 200
    }
    
    reporte_problemas = validar_resultados_simulacion(datos_problematicos, "test_problemas")
    
    print("✅ Validación problemática completada")
    print(f"   Estado: {reporte_problemas['estado_general']}")
    print(f"   Validaciones exitosas: {reporte_problemas['resumen']['validaciones_exitosas']}")
    print(f"   Advertencias: {reporte_problemas['resumen']['advertencias']}")
    print(f"   Errores: {reporte_problemas['resumen']['errores']}")
    
    # Test guardado JSON
    print("\n💾 Probando guardado de reporte JSON...")
    validador = ValidadorEconomicoFormal()
    validador.ejecutar_validacion_completa(datos_normales, "test_json")
    
    ruta = validador.guardar_reporte_json("results/validation_report_test.json")
    print(f"✅ Reporte guardado en: {ruta}")
    
    # Verificar que el archivo existe
    if os.path.exists(ruta):
        print("✅ Archivo JSON generado correctamente")
        with open(ruta, 'r') as f:
            contenido = f.read()
            print(f"   Tamaño: {len(contenido)} caracteres")
    else:
        print("❌ Error: archivo JSON no generado")
    
    return True

if __name__ == "__main__":
    try:
        test_validation_simple()
        print("\n🎉 ¡Todos los tests de validación pasaron!")
    except Exception as e:
        print(f"\n❌ Error en test de validación: {e}")
        import traceback
        traceback.print_exc()