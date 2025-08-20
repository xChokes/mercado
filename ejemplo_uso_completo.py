"""
Ejemplo de Uso del Sistema de Agentes IA Hiperrealistas
======================================================

Este ejemplo demuestra cómo usar el sistema completo de agentes IA
para crear un mercado económico con inteligencia artificial avanzada.
"""

import sys
import os
import time
from datetime import datetime

# Agregar el directorio raíz del proyecto al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ai.IntegradorAgentesIA import IntegradorAgentesIA, ConfiguracionSistemaIA
from src.ai.SistemaDeepLearningIA import TipoRedNeural
from src.ai.RedSocialAgentesIA import TipoRelacion


def ejemplo_basico():
    """Ejemplo básico de uso del sistema"""
    print("🚀 EJEMPLO BÁSICO - SISTEMA DE AGENTES IA HIPERREALISTAS")
    print("=" * 60)
    
    # 1. Definir bienes del mercado
    bienes_mercado = ["comida", "tecnologia", "energia", "transporte", "vivienda"]
    
    # 2. Configurar el sistema
    configuracion = ConfiguracionSistemaIA(
        num_consumidores_ia=15,          # 15 consumidores inteligentes
        num_empresas_ia=6,               # 6 empresas inteligentes
        probabilidad_relacion_inicial=0.4,  # 40% probabilidad de relaciones
        activar_formacion_coaliciones=True,
        entrenar_automaticamente=True,
        intervalo_entrenamiento_minutos=10,  # Entrenar cada 10 minutos
        activar_logs_detallados=True
    )
    
    # 3. Inicializar el sistema
    print("\n🔧 Inicializando sistema...")
    sistema_ia = IntegradorAgentesIA(bienes_mercado, configuracion)
    
    try:
        # 4. Ejecutar ciclo de mercado por 30 minutos
        print("\n🏁 Ejecutando simulación por 5 minutos...")
        sistema_ia.ejecutar_ciclo_mercado(duracion_minutos=5)
        
        # 5. Mostrar estado final
        print("\n📊 ESTADO FINAL DEL SISTEMA:")
        estado_final = sistema_ia.obtener_estado_completo()
        
        print(f"   Agentes IA activos: {estado_final['estadisticas']['agentes_activos']}")
        print(f"   Transacciones realizadas: {estado_final['estadisticas']['transacciones_ia']}")
        print(f"   Relaciones sociales: {estado_final['estadisticas']['relaciones_sociales']}")
        print(f"   Coaliciones formadas: {estado_final['estadisticas']['coaliciones_activas']}")
        print(f"   Eficiencia del mercado: {estado_final['estadisticas']['eficiencia_global']:.3f}")
        
    finally:
        # 6. Finalizar sistema ordenadamente
        print("\n🛑 Finalizando sistema...")
        sistema_ia.finalizar_sistema()


def ejemplo_avanzado():
    """Ejemplo avanzado con configuración personalizada"""
    print("🔬 EJEMPLO AVANZADO - CONFIGURACIÓN PERSONALIZADA")
    print("=" * 60)
    
    # Configuración avanzada
    configuracion_avanzada = ConfiguracionSistemaIA(
        num_consumidores_ia=25,
        num_empresas_ia=10,
        probabilidad_relacion_inicial=0.6,
        activar_formacion_coaliciones=True,
        entrenar_automaticamente=True,
        intervalo_entrenamiento_minutos=5,
        activar_detector_crisis=True,
        activar_optimizacion_liquidez=True,
        intervalo_sincronizacion_segundos=5,
        activar_logs_detallados=True
    )
    
    bienes_especializados = [
        "semiconductores", "software", "biotecnologia", 
        "energia_renovable", "inteligencia_artificial"
    ]
    
    sistema_ia = IntegradorAgentesIA(bienes_especializados, configuracion_avanzada)
    
    try:
        print("\n🧪 Realizando experimentos avanzados...")
        
        # Experimento 1: Crear relaciones específicas
        print("\n📋 Experimento 1: Estableciendo relaciones estratégicas")
        empresa_1 = "empresa_ia_1"
        empresa_2 = "empresa_ia_2"
        
        if empresa_1 in sistema_ia.empresas_ia and empresa_2 in sistema_ia.empresas_ia:
            sistema_ia.red_social.establecer_relacion(
                empresa_1, empresa_2, TipoRelacion.ALIANZA_ESTRATEGICA,
                fuerza_inicial=0.9, confianza_inicial=0.8
            )
            print(f"   ✓ Alianza estratégica establecida entre {empresa_1} y {empresa_2}")
        
        # Experimento 2: Compartir información crítica
        print("\n📋 Experimento 2: Propagando información crítica")
        if sistema_ia.empresas_ia:
            primera_empresa = list(sistema_ia.empresas_ia.keys())[0]
            info_critica = {
                "tipo": "innovacion_tecnologica",
                "impacto": "alto",
                "sector": "inteligencia_artificial"
            }
            
            sistema_ia.red_social.compartir_informacion(
                emisor=primera_empresa,
                contenido=info_critica,
                tipo_informacion="tecnologia",
                confiabilidad=0.95
            )
            print(f"   ✓ Información crítica propagada desde {primera_empresa}")
        
        # Experimento 3: Entrenar redes específicas
        print("\n📋 Experimento 3: Entrenamiento especializado de redes")
        
        # Generar datos sintéticos para entrenamiento
        datos_precios = []
        for i in range(50):
            entradas = [
                0.5 + (i % 10) * 0.05,  # Demanda simulada
                0.3 + (i % 8) * 0.08,   # Oferta simulada
                0.7 + (i % 5) * 0.06    # Volatilidad simulada
            ]
            salidas = [0.4 + (i % 12) * 0.05]  # Precio normalizado
            datos_precios.append((entradas, salidas))
        
        resultado_entrenamiento = sistema_ia.sistema_deep_learning.entrenar_red_con_datos(
            TipoRedNeural.PREDICCION_PRECIOS, datos_precios, epocas=30
        )
        print(f"   ✓ Red de predicción entrenada - Precisión: {resultado_entrenamiento['precision_final']:.3f}")
        
        # Experimento 4: Ejecutar ciclo corto intensivo
        print("\n📋 Experimento 4: Ciclo intensivo de mercado")
        sistema_ia.ejecutar_ciclo_mercado(duracion_minutos=3)
        
        # Experimento 5: Análisis de resultados
        print("\n📋 Experimento 5: Análisis detallado de resultados")
        estado_sistema = sistema_ia.obtener_estado_completo()
        
        # Análisis de eficiencia
        eficiencia = estado_sistema['estadisticas']['eficiencia_global']
        if eficiencia > 0.8:
            print("   🏆 EXCELENTE: Eficiencia del mercado superior al 80%")
        elif eficiencia > 0.6:
            print("   ✅ BUENO: Eficiencia del mercado aceptable")
        else:
            print("   ⚠️ MEJORAR: Eficiencia del mercado por debajo del óptimo")
        
        # Análisis de colaboración
        coaliciones = estado_sistema['estadisticas']['coaliciones_activas']
        if coaliciones > 2:
            print("   🤝 EXCELENTE: Múltiples coaliciones activas")
        elif coaliciones > 0:
            print("   👥 BUENO: Colaboración emergente detectada")
        else:
            print("   🔄 EN DESARROLLO: Colaboración aún emergiendo")
        
        # Análisis de aprendizaje
        redes_entrenadas = estado_sistema['deep_learning']['redes_entrenadas']
        if redes_entrenadas > 10:
            print("   🧠 EXCELENTE: Sistema de aprendizaje muy activo")
        elif redes_entrenadas > 5:
            print("   📚 BUENO: Aprendizaje activo")
        else:
            print("   🌱 INICIAL: Aprendizaje en fase temprana")
        
    finally:
        sistema_ia.finalizar_sistema()


def ejemplo_investigacion():
    """Ejemplo para investigación académica"""
    print("🔬 EJEMPLO INVESTIGACIÓN - ANÁLISIS CIENTÍFICO")
    print("=" * 60)
    
    # Configuración para investigación
    config_investigacion = ConfiguracionSistemaIA(
        num_consumidores_ia=30,
        num_empresas_ia=12,
        probabilidad_relacion_inicial=0.5,
        activar_formacion_coaliciones=True,
        entrenar_automaticamente=True,
        intervalo_entrenamiento_minutos=3,
        activar_logs_detallados=False  # Logs menos verbosos para análisis
    )
    
    mercado_investigacion = ["recurso_A", "recurso_B", "recurso_C"]
    sistema = IntegradorAgentesIA(mercado_investigacion, config_investigacion)
    
    try:
        print("\n📊 Recolectando datos experimentales...")
        
        # Ejecutar múltiples ciclos cortos para recolectar datos
        for experimento in range(3):
            print(f"\n🔬 Experimento {experimento + 1}/3")
            
            # Ciclo de 2 minutos
            sistema.ejecutar_ciclo_mercado(duracion_minutos=2)
            
            # Recolectar métricas
            estado = sistema.obtener_estado_completo()
            
            print(f"   Transacciones: {estado['estadisticas']['transacciones_ia']}")
            print(f"   Eficiencia: {estado['estadisticas']['eficiencia_global']:.3f}")
            print(f"   Coaliciones: {estado['estadisticas']['coaliciones_activas']}")
            
            # Pausa entre experimentos
            if experimento < 2:
                print("   ⏳ Pausa entre experimentos...")
                time.sleep(10)
        
        # Análisis final
        print("\n📈 ANÁLISIS FINAL DE INVESTIGACIÓN:")
        estado_final = sistema.obtener_estado_completo()
        
        print(f"   📊 Métricas Cuantitativas:")
        print(f"      - Agentes simulados: {estado_final['estadisticas']['agentes_activos']}")
        print(f"      - Transacciones totales: {estado_final['estadisticas']['transacciones_ia']}")
        print(f"      - Red social formada: {estado_final['estadisticas']['relaciones_sociales']} relaciones")
        print(f"      - Emergencia cooperativa: {estado_final['estadisticas']['coaliciones_activas']} coaliciones")
        print(f"      - Eficiencia del sistema: {estado_final['estadisticas']['eficiencia_global']:.4f}")
        
        print(f"\n   🧠 Métricas de Inteligencia Artificial:")
        dl_stats = estado_final['deep_learning']
        print(f"      - Redes neuronales activas: {dl_stats['redes_creadas']}")
        print(f"      - Ciclos de entrenamiento: {dl_stats['redes_entrenadas']}")
        print(f"      - Datos procesados: {dl_stats['datos_entrenamiento_total']}")
        print(f"      - Optimizaciones evolutivas: {dl_stats['optimizaciones_completadas']}")
        
        print(f"\n   🌐 Métricas de Emergencia Social:")
        red_stats = estado_final['red_social']
        print(f"      - Densidad de red: {red_stats['densidad_red']:.3f}")
        print(f"      - Eficiencia comunicación: {red_stats['eficiencia_comunicacion']:.3f}")
        print(f"      - Comunidades detectadas: {red_stats['comunidades_detectadas']}")
        print(f"      - Reputación promedio: {red_stats['reputacion_promedio']:.3f}")
        
    finally:
        sistema.finalizar_sistema()


def main():
    """Función principal para ejecutar ejemplos"""
    print("🤖 SISTEMA DE AGENTES IA HIPERREALISTAS")
    print("Implementación completa del plan de IA avanzada")
    print("=" * 60)
    
    ejemplos = {
        "1": ("Ejemplo Básico", ejemplo_basico),
        "2": ("Ejemplo Avanzado", ejemplo_avanzado),
        "3": ("Ejemplo Investigación", ejemplo_investigacion)
    }
    
    print("\nSeleccione un ejemplo para ejecutar:")
    for key, (nombre, _) in ejemplos.items():
        print(f"   {key}. {nombre}")
    
    try:
        seleccion = input("\nIngrese su selección (1-3): ").strip()
        
        if seleccion in ejemplos:
            nombre, funcion = ejemplos[seleccion]
            print(f"\n🎯 Ejecutando: {nombre}")
            print("-" * 40)
            funcion()
        else:
            print("❌ Selección inválida. Ejecutando ejemplo básico...")
            ejemplo_basico()
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Ejecución interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante la ejecución: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
