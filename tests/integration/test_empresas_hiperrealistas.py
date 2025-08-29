#!/usr/bin/env python3
"""
Script de prueba para empresas hiperrealistas
=============================================

Este script verifica que todas las nuevas características empresariales
funcionen correctamente en integración con el sistema existente.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.models.EmpresaProductoraHiperrealista import EmpresaProductoraHiperrealista
from src.models.Mercado import Mercado
from src.models.Bien import Bien
from src.models.Consumidor import Consumidor
import random
import json

def crear_mercado_prueba():
    """Crea un mercado pequeño para pruebas"""
    print("🔧 Creando mercado de prueba...")
    
    # Crear bienes básicos
    bienes = {
        'Pan': Bien('Pan', 'alimentos_basicos'),
        'Leche': Bien('Leche', 'alimentos_basicos'),
        'Ropa': Bien('Ropa', 'bienes_duraderos'),
        'Telefono': Bien('Telefono', 'tecnologia')
    }
    
    # Crear mercado
    mercado = Mercado(bienes)
    
    # Agregar algunos consumidores
    for i in range(10):
        consumidor = Consumidor(f'Consumidor_{i+1}', mercado)
        consumidor.dinero = random.uniform(5000, 15000)
        consumidor.ingreso_mensual = random.uniform(2000, 6000)
        mercado.agregar_persona(consumidor)
    
    print(f"✅ Mercado creado con {len(bienes)} bienes y {len(mercado.getConsumidores())} consumidores")
    return mercado

def probar_empresa_hiperrealista(mercado):
    """Prueba las características de empresa hiperrealista"""
    print("\n🚀 Probando empresa hiperrealista...")
    
    try:
        # Crear empresa hiperrealista
        empresa = EmpresaProductoraHiperrealista('EmpresaPrueba_Hiper', mercado)
        empresa.dinero = 150000  # Capital inicial generoso
        
        print(f"✅ Empresa creada: {empresa.nombre}")
        print(f"   💰 Capital inicial: ${empresa.dinero:,.2f}")
        print(f"   🔬 Nivel tecnológico: {empresa.nivel_tecnologico:.2f}")
        print(f"   ⭐ Reputación: {empresa.reputacion_mercado:.2f}")
        print(f"   🤖 IA habilitada: {empresa.ia_habilitada}")
        print(f"   🎯 Visión: {empresa.vision_empresa}")
        
        # Verificar sistemas de gestión
        print(f"   📊 Gestión de calidad: {'✅' if hasattr(empresa, 'gestion_calidad') else '❌'}")
        print(f"   ⚠️  Gestión de riesgos: {'✅' if hasattr(empresa, 'gestion_riesgos_operativos') else '❌'}")
        print(f"   🏷️  Gestión de marca: {'✅' if hasattr(empresa, 'gestion_marca') else '❌'}")
        print(f"   🔍 Análisis competitivo: {'✅' if hasattr(empresa, 'analisis_competitivo') else '❌'}")
        print(f"   🔬 Centro innovación: {'✅' if hasattr(empresa, 'centro_innovacion') else '❌'}")
        print(f"   🌱 Sostenibilidad: {'✅' if hasattr(empresa, 'programa_sostenibilidad') else '❌'}")
        
        # Agregar empresa al mercado
        mercado.agregar_persona(empresa)
        
        return empresa
        
    except Exception as e:
        print(f"❌ Error creando empresa hiperrealista: {e}")
        return None

def probar_ciclo_completo(mercado):
    """Prueba un ciclo completo de simulación"""
    print("\n🔄 Probando ciclo completo...")
    
    try:
        # Ejecutar algunos ciclos
        for ciclo in range(3):
            print(f"   Ejecutando ciclo {ciclo + 1}...")
            mercado.ejecutar_ciclo(ciclo)
        
        # Mostrar estadísticas
        stats = mercado.obtener_estadisticas_completas()
        
        print("✅ Ciclos completados exitosamente")
        print(f"   📈 PIB final: ${stats['pib_historico'][-1]:,.2f}")
        print(f"   📊 Inflación: {stats['inflacion_historica'][-1]:.2%}")
        print(f"   💼 Desempleo: {stats['desempleo_historico'][-1]:.2%}")
        
        # Estadísticas del sistema hiperrealista
        if 'empresas_hiperrealistas' in stats:
            hiper_stats = stats['empresas_hiperrealistas']
            print(f"   🚀 Empresas mejoradas: {hiper_stats.get('empresas_totales_mejoradas', 0)}")
            print(f"   💊 Empresas rescatadas: {hiper_stats.get('empresas_rescatadas_total', 0)}")
            print(f"   🔬 Innovaciones exitosas: {hiper_stats.get('innovaciones_exitosas_total', 0)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en ciclo completo: {e}")
        import traceback
        traceback.print_exc()
        return False

def probar_reporte_hiperrealista(empresa):
    """Prueba el reporte hiperrealista de empresa"""
    print("\n📊 Probando reporte hiperrealista...")
    
    try:
        reporte = empresa.obtener_reporte_hiperrealista()
        
        print("✅ Reporte generado exitosamente:")
        print(f"   🏢 Empresa: {reporte['nombre']}")
        print(f"   🔬 Nivel tecnológico: {reporte['nivel_tecnologico']:.2f}")
        print(f"   ⭐ Reputación: {reporte['reputacion_mercado']:.2f}")
        print(f"   📈 ROI promedio: {reporte['roi_promedio']:.2%}")
        print(f"   💰 Margen bruto: {reporte['margen_bruto_promedio']:.2%}")
        print(f"   🏆 Certificaciones: {reporte['certificaciones']}")
        print(f"   🔬 Patentes: {reporte['patentes']}")
        print(f"   🤝 Alianzas: {reporte['alianzas_tecnologicas']}")
        print(f"   🛡️  Seguros: {reporte['seguros_contratados']}")
        print(f"   🌱 Score sostenibilidad: {reporte['sostenibilidad_score']:.2f}")
        
        # Objetivos estratégicos
        print("\n   🎯 Objetivos estratégicos:")
        for obj in reporte['objetivos_cumplimiento']:
            progreso = obj['progreso'] * 100
            print(f"      • {obj['descripcion']} ({obj['tipo']}): {progreso:.1f}%")
        
        return True
        
    except Exception as e:
        print(f"❌ Error generando reporte: {e}")
        import traceback
        traceback.print_exc()
        return False

def verificar_integracion_sistema():
    """Verifica la integración con el sistema existente"""
    print("\n🔗 Verificando integración con sistema existente...")
    
    try:
        # Cargar configuración real
        with open('config_simulacion.json', 'r') as f:
            config = json.load(f)
        
        print("✅ Configuración cargada:")
        empresas_hiper = config.get('empresas_hiperrealistas', {})
        print(f"   🚀 Sistema activado: {empresas_hiper.get('activar', False)}")
        print(f"   🤖 IA empresarial: {empresas_hiper.get('habilitado_ia_empresarial', False)}")
        print(f"   🔧 Gestión avanzada: {empresas_hiper.get('sistemas_gestion_avanzada', False)}")
        print(f"   🔬 Innovación continua: {empresas_hiper.get('innovacion_continua', False)}")
        
        # Verificar import del main
        try:
            from main import crear_bienes_expandidos
            bienes = crear_bienes_expandidos()
            print(f"✅ Integración con main.py verificada - {len(bienes)} bienes disponibles")
        except Exception as e:
            print(f"⚠️  Advertencia en integración main.py: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando integración: {e}")
        return False

def main():
    """Función principal de prueba"""
    print("=" * 60)
    print("🧪 PRUEBA DE EMPRESAS HIPERREALISTAS")
    print("=" * 60)
    
    resultados = {
        'mercado_creado': False,
        'empresa_creada': False,
        'ciclo_completo': False,
        'reporte_generado': False,
        'integracion_verificada': False
    }
    
    try:
        # 1. Crear mercado de prueba
        mercado = crear_mercado_prueba()
        if mercado:
            resultados['mercado_creado'] = True
        
        # 2. Probar empresa hiperrealista
        empresa = probar_empresa_hiperrealista(mercado)
        if empresa:
            resultados['empresa_creada'] = True
        
        # 3. Probar ciclo completo
        if empresa and probar_ciclo_completo(mercado):
            resultados['ciclo_completo'] = True
        
        # 4. Probar reporte hiperrealista
        if empresa and probar_reporte_hiperrealista(empresa):
            resultados['reporte_generado'] = True
        
        # 5. Verificar integración
        if verificar_integracion_sistema():
            resultados['integracion_verificada'] = True
        
    except Exception as e:
        print(f"❌ Error general en pruebas: {e}")
        import traceback
        traceback.print_exc()
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📋 RESUMEN DE RESULTADOS")
    print("=" * 60)
    
    total_pruebas = len(resultados)
    pruebas_exitosas = sum(resultados.values())
    
    for prueba, resultado in resultados.items():
        estado = "✅ EXITOSA" if resultado else "❌ FALLIDA"
        print(f"{prueba:25} {estado}")
    
    print(f"\n🎯 RESULTADO FINAL: {pruebas_exitosas}/{total_pruebas} pruebas exitosas")
    
    if pruebas_exitosas == total_pruebas:
        print("🎉 ¡TODAS LAS PRUEBAS EXITOSAS! Sistema hiperrealista listo.")
        return 0
    elif pruebas_exitosas >= total_pruebas * 0.8:
        print("⚠️  Sistema mayormente funcional con algunas advertencias.")
        return 1
    else:
        print("❌ Sistema requiere correcciones antes del uso.")
        return 2

if __name__ == '__main__':
    exit(main())
