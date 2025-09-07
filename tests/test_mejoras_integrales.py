#!/usr/bin/env python3
"""
Script de Prueba de Mejoras Integrales
Valida que todos los sistemas de mejora funcionen correctamente
"""

import sys
import os
import traceback

# Añadir el directorio raíz al path
sys.path.append('/workspaces/mercado')

def test_imports():
    """Prueba que todos los imports necesarios funcionen"""
    print("🔍 Probando imports de sistemas de mejora...")
    
    try:
        from src.systems.SistemaIntegracionMejoras import SistemaIntegracionMejoras, ConfiguracionMejoras
        print("✅ SistemaIntegracionMejoras importado correctamente")
        
        from src.systems.OptimizadorProductividadLaboral import OptimizadorProductividadLaboral, ConfigProductividad
        print("✅ OptimizadorProductividadLaboral importado correctamente")
        
        from src.systems.ControladorConcentracionEmpresarial import ControladorConcentracionEmpresarial, ConfigCreacionEmpresas
        print("✅ ControladorConcentracionEmpresarial importado correctamente")
        
        from src.systems.ReduccionActivaDesempleo import ReduccionActivaDesempleo, ConfigReduccionDesempleo
        print("✅ ReduccionActivaDesempleo importado correctamente")
        
        from src.systems.EstabilizadorAutomaticoPIB import EstabilizadorAutomaticoPIB, ConfigEstabilizacionPIB
        print("✅ EstabilizadorAutomaticoPIB importado correctamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en imports: {e}")
        traceback.print_exc()
        return False

def test_configuracion():
    """Prueba que las configuraciones se puedan crear correctamente"""
    print("\n🔧 Probando configuraciones...")
    
    try:
        from src.systems.SistemaIntegracionMejoras import ConfiguracionMejoras
        from src.systems.OptimizadorProductividadLaboral import ConfigProductividad
        from src.systems.ControladorConcentracionEmpresarial import ConfigCreacionEmpresas
        from src.systems.ReduccionActivaDesempleo import ConfigReduccionDesempleo
        from src.systems.EstabilizadorAutomaticoPIB import ConfigEstabilizacionPIB
        
        config_mejoras = ConfiguracionMejoras()
        print(f"✅ ConfiguracionMejoras creada: productividad_base {config_mejoras.productividad_base_minima}-{config_mejoras.productividad_base_maxima}")
        
        config_prod = ConfigProductividad()
        print(f"✅ ConfigProductividad creada: objetivo {config_prod.productividad_minima_objetivo}-{config_prod.productividad_maxima_objetivo}")
        
        config_empresas = ConfigCreacionEmpresas()
        print(f"✅ ConfigCreacionEmpresas creada: {config_empresas.empresas_minimas}-{config_empresas.empresas_optimas} empresas")
        
        config_desempleo = ConfigReduccionDesempleo()
        print(f"✅ ConfigReduccionDesempleo creada: objetivo {config_desempleo.desempleo_objetivo:.1%}")
        
        config_pib = ConfigEstabilizacionPIB()
        print(f"✅ ConfigEstabilizacionPIB creada: umbral {config_pib.umbral_volatilidad:.1%}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en configuraciones: {e}")
        traceback.print_exc()
        return False

def test_inicializacion_sistemas():
    """Prueba que los sistemas se puedan inicializar"""
    print("\n🚀 Probando inicialización de sistemas...")
    
    try:
        from src.systems.SistemaIntegracionMejoras import SistemaIntegracionMejoras, ConfiguracionMejoras
        from src.systems.OptimizadorProductividadLaboral import OptimizadorProductividadLaboral
        from src.systems.ControladorConcentracionEmpresarial import ControladorConcentracionEmpresarial
        from src.systems.ReduccionActivaDesempleo import ReduccionActivaDesempleo
        from src.systems.EstabilizadorAutomaticoPIB import EstabilizadorAutomaticoPIB
        
        # Crear sistemas
        sistema_mejoras = SistemaIntegracionMejoras()
        print("✅ SistemaIntegracionMejoras inicializado")
        
        optimizador = OptimizadorProductividadLaboral()
        print("✅ OptimizadorProductividadLaboral inicializado")
        
        controlador = ControladorConcentracionEmpresarial()
        print("✅ ControladorConcentracionEmpresarial inicializado")
        
        reductor = ReduccionActivaDesempleo()
        print("✅ ReduccionActivaDesempleo inicializado")
        
        estabilizador = EstabilizadorAutomaticoPIB()
        print("✅ EstabilizadorAutomaticoPIB inicializado")
        
        # Probar métodos básicos
        reporte = sistema_mejoras.obtener_reporte_mejoras()
        print(f"✅ Reporte de mejoras generado: {len(reporte)} secciones")
        
        return True
        
    except Exception as e:
        print(f"❌ Error inicializando sistemas: {e}")
        traceback.print_exc()
        return False

def test_config_json():
    """Prueba que el archivo de configuración sea válido"""
    print("\n📋 Probando configuración JSON...")
    
    try:
        import json
        
        with open('/workspaces/mercado/config_simulacion.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print("✅ Archivo JSON válido")
        
        # Verificar sección de mejoras
        if 'mejoras_integrales' in config:
            mejoras = config['mejoras_integrales']
            print(f"✅ Sección mejoras_integrales encontrada con {len(mejoras)} subsecciones")
            
            required_sections = ['productividad_laboral', 'control_concentracion', 'reduccion_desempleo', 'estabilizacion_pib']
            for section in required_sections:
                if section in mejoras:
                    print(f"✅ Subsección '{section}' encontrada")
                else:
                    print(f"⚠️  Subsección '{section}' faltante")
        else:
            print("⚠️  Sección 'mejoras_integrales' no encontrada en configuración")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en configuración JSON: {e}")
        traceback.print_exc()
        return False

def test_simulacion_simple():
    """Prueba una mini simulación para verificar integración"""
    print("\n🎯 Probando mini simulación...")
    
    try:
        # Crear simulador mock simple
        class MockSimulador:
            def __init__(self):
                self.pib = 100000
                self.desempleo = 0.15
                self.mercado = MockMercado()
        
        class MockMercado:
            def __init__(self):
                self.empresas = [MockEmpresa(f"Empresa_{i}") for i in range(2)]
        
        class MockEmpresa:
            def __init__(self, id):
                self.id = id
                self.activa = True
                self.capital = 50000
                self.empleados = [f"empleado_{i}" for i in range(10)]
                self.productividad_laboral = 0.3
        
        # Crear sistema de mejoras
        from src.systems.SistemaIntegracionMejoras import SistemaIntegracionMejoras
        sistema = SistemaIntegracionMejoras()
        
        # Simular mock
        simulador = MockSimulador()
        
        # Aplicar mejoras
        resultados = sistema.aplicar_mejoras_ciclo(simulador, 1)
        
        print(f"✅ Mini simulación ejecutada:")
        print(f"   - Productividad mejorada: {resultados['productividad_mejorada']}")
        print(f"   - Empresas creadas: {resultados['empresas_creadas']}")
        print(f"   - Desempleo reducido: {resultados['desempleo_reducido']:.3f}")
        print(f"   - PIB estabilizado: {resultados['pib_estabilizado']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en mini simulación: {e}")
        traceback.print_exc()
        return False

def main():
    """Función principal de pruebas"""
    print("🚀 PRUEBAS DE MEJORAS INTEGRALES v3.2")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Configuraciones", test_configuracion),
        ("Inicialización", test_inicializacion_sistemas),
        ("Config JSON", test_config_json),
        ("Mini Simulación", test_simulacion_simple)
    ]
    
    resultados = []
    
    for nombre, test_func in tests:
        try:
            resultado = test_func()
            resultados.append((nombre, resultado))
        except Exception as e:
            print(f"❌ Error en prueba {nombre}: {e}")
            resultados.append((nombre, False))
    
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE PRUEBAS:")
    print("=" * 50)
    
    exitosos = 0
    for nombre, resultado in resultados:
        status = "✅ EXITOSO" if resultado else "❌ FALLIDO"
        print(f"{nombre}: {status}")
        if resultado:
            exitosos += 1
    
    print(f"\n🎯 RESULTADO FINAL: {exitosos}/{len(tests)} pruebas exitosas")
    
    if exitosos == len(tests):
        print("🎉 ¡TODAS LAS MEJORAS ESTÁN LISTAS PARA USAR!")
        return True
    else:
        print("⚠️  Algunas mejoras necesitan atención")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
