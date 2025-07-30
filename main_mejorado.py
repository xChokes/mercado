"""
Simulación económica realista con leyes económicas implementadas
"""
import random
import time
import matplotlib.pyplot as plt
import numpy as np
from Mercado import Mercado
from Bien import Bien
from Consumidor import Consumidor
from Empresa import Empresa
from EmpresaProductora import EmpresaProductora
from ConfigEconomica import ConfigEconomica

def crear_bienes_realistas():
    """Crea bienes con características económicas realistas"""
    bienes = {}
    
    # Bienes básicos
    bienes['Arroz'] = Bien('Arroz', 'alimentos_basicos')
    bienes['Papa'] = Bien('Papa', 'alimentos_basicos')
    bienes['Pan'] = Bien('Pan', 'alimentos_basicos')
    bienes['Leche'] = Bien('Leche', 'alimentos_basicos')
    bienes['Sal'] = Bien('Sal', 'alimentos_basicos')
    bienes['Aceite'] = Bien('Aceite', 'alimentos_basicos')
    bienes['Azucar'] = Bien('Azucar', 'alimentos_basicos')
    
    # Bienes de lujo alimentarios
    bienes['Carne'] = Bien('Carne', 'alimentos_lujo')
    bienes['Pollo'] = Bien('Pollo', 'alimentos_lujo')
    bienes['Huevos'] = Bien('Huevos', 'alimentos_lujo')
    bienes['Cafe'] = Bien('Cafe', 'alimentos_lujo')
    
    return bienes

def configurar_economia_inicial(mercado):
    """Configura el estado inicial de la economía"""
    print("🏗️  Configurando economía inicial...")
    
    # Crear empresas productoras especializadas
    empresas_productoras = []
    for i in range(5):  # 5 empresas productoras
        nombre = f"ProductoraMega{i+1}"
        empresa = EmpresaProductora(nombre, mercado)
        mercado.agregar_persona(empresa)
        empresas_productoras.append(empresa)
        print(f"   ✅ Creada {nombre} con capital inicial ${empresa.dinero:,.2f}")
    
    # Crear consumidores con características diversas
    consumidores = []
    for i in range(200):  # 200 consumidores para mayor realismo
        nombre = f"Consumidor{i+1}"
        consumidor = Consumidor(nombre, mercado)
        mercado.agregar_persona(consumidor)
        consumidores.append(consumidor)
        
        # Asignar empleos iniciales (80% empleados)
        if consumidor.empleado and empresas_productoras:
            empleador = random.choice(empresas_productoras)
            if empleador.contratar(consumidor):
                consumidor.empleador = empleador
                
    # Crear empresas de servicios/comercio
    for i in range(8):  # 8 empresas de servicios
        nombre = f"EmpresaComercial{i+1}"
        empresa = Empresa.crear_con_acciones(
            nombre=nombre, 
            mercado=mercado, 
            cantidad_acciones=1000, 
            bienes={}
        )
        mercado.agregar_persona(empresa)
        print(f"   ✅ Creada {nombre} con capital inicial ${empresa.dinero:,.2f}")
    
    print(f"   📊 Total: {len(empresas_productoras)} productoras, {len(consumidores)} consumidores, 8 comerciales")
    print("   🎯 Economía inicial configurada correctamente")

def ejecutar_simulacion(mercado, num_ciclos=50):
    """Ejecuta la simulación económica completa"""
    print(f"\n🚀 Iniciando simulación económica de {num_ciclos} ciclos...")
    inicio = time.time()
    
    # Almacenar métricas
    metricas = {
        'pib': [],
        'inflacion': [],
        'desempleo': [],
        'dinero_consumidores': [],
        'dinero_empresas': [],
        'precios_promedio': [],
        'transacciones_totales': []
    }
    
    for ciclo in range(num_ciclos):
        print(f"\n📅 Ejecutando ciclo {ciclo + 1}/{num_ciclos}")
        
        try:
            mercado.ejecutar_ciclo(ciclo)
            
            # Recopilar métricas
            stats = mercado.obtener_estadisticas_completas()
            metricas['pib'].append(stats['pib_historico'][-1] if stats['pib_historico'] else 0)
            metricas['inflacion'].append(stats['inflacion_historica'][-1] if stats['inflacion_historica'] else 0)
            metricas['desempleo'].append(stats['desempleo_historico'][-1] if stats['desempleo_historico'] else 0)
            
            # Dinero por tipo de agente
            dinero_cons = [c.dinero for c in mercado.getConsumidores()]
            dinero_emp = [e.dinero for e in mercado.getEmpresas()]
            metricas['dinero_consumidores'].append(sum(dinero_cons) / len(dinero_cons) if dinero_cons else 0)
            metricas['dinero_empresas'].append(sum(dinero_emp) / len(dinero_emp) if dinero_emp else 0)
            
            # Precio promedio
            precios_todos = []
            for empresa in mercado.getEmpresas():
                precios_todos.extend(empresa.precios.values())
            metricas['precios_promedio'].append(sum(precios_todos) / len(precios_todos) if precios_todos else 0)
            
            # Transacciones
            trans_ciclo = len([t for t in mercado.transacciones if t.get('ciclo') == ciclo])
            metricas['transacciones_totales'].append(trans_ciclo)
            
            # Progreso cada 10 ciclos
            if (ciclo + 1) % 10 == 0:
                porcentaje = ((ciclo + 1) / num_ciclos) * 100
                print(f"   ⏱️  Progreso: {porcentaje:.1f}% completado")
                
        except Exception as e:
            print(f"   ❌ Error en ciclo {ciclo + 1}: {e}")
            continue
    
    tiempo_total = time.time() - inicio
    print(f"\n✅ Simulación completada en {tiempo_total:.2f} segundos")
    
    return metricas

def generar_analisis_economico(mercado, metricas):
    """Genera análisis económico detallado"""
    print("\n📊 ANÁLISIS ECONÓMICO FINAL")
    print("=" * 60)
    
    # Estadísticas básicas
    pib_final = metricas['pib'][-1] if metricas['pib'] else 0
    pib_inicial = metricas['pib'][0] if metricas['pib'] else 0
    crecimiento_pib = ((pib_final - pib_inicial) / pib_inicial * 100) if pib_inicial > 0 else 0
    
    inflacion_promedio = sum(metricas['inflacion']) / len(metricas['inflacion']) if metricas['inflacion'] else 0
    desempleo_promedio = sum(metricas['desempleo']) / len(metricas['desempleo']) if metricas['desempleo'] else 0
    
    print(f"📈 PIB Final: ${pib_final:,.2f}")
    print(f"📊 Crecimiento PIB: {crecimiento_pib:+.2f}%")
    print(f"💰 Inflación Promedio: {inflacion_promedio:.2%}")
    print(f"👥 Desempleo Promedio: {desempleo_promedio:.2%}")
    
    # Análisis del mercado laboral
    empleados = sum([1 for c in mercado.getConsumidores() if c.empleado])
    total_consumidores = len(mercado.getConsumidores())
    tasa_empleo = empleados / total_consumidores if total_consumidores > 0 else 0
    
    print(f"💼 Tasa de Empleo Final: {tasa_empleo:.2%}")
    print(f"🏢 Empresas Activas: {len(mercado.getEmpresas())}")
    
    # Análisis de competencia
    print("\n🏆 ANÁLISIS DE COMPETENCIA:")
    for bien, nivel in mercado.nivel_competencia.items():
        estado = "Alta" if nivel > 0.7 else "Media" if nivel > 0.4 else "Baja"
        print(f"   {bien}: {estado} competencia (índice: {nivel:.2f})")
    
    # Análisis de ciclo económico
    print(f"\n🔄 FASE ECONÓMICA ACTUAL: {mercado.fase_ciclo_economico.upper()}")
    if mercado.shock_economico_activo:
        print("⚠️  SHOCK ECONÓMICO EN CURSO")
    
    # Top empresas por capital
    empresas_ordenadas = sorted(mercado.getEmpresas(), 
                               key=lambda e: e.dinero, reverse=True)[:5]
    print("\n🥇 TOP 5 EMPRESAS POR CAPITAL:")
    for i, empresa in enumerate(empresas_ordenadas, 1):
        print(f"   {i}. {empresa.nombre}: ${empresa.dinero:,.2f}")
    
    # Transacciones totales
    total_transacciones = len(mercado.transacciones)
    volumen_total = sum([t['costo_total'] for t in mercado.transacciones])
    print(f"\n💵 Total Transacciones: {total_transacciones:,}")
    print(f"💰 Volumen Total: ${volumen_total:,.2f}")

def crear_visualizaciones(metricas):
    """Crea gráficos de análisis económico"""
    print("\n📊 Generando visualizaciones...")
    
    # Configurar estilo
    plt.style.use('default')
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('ANÁLISIS ECONÓMICO COMPLETO', fontsize=16, fontweight='bold')
    
    ciclos = range(len(metricas['pib']))
    
    # 1. PIB
    axes[0, 0].plot(ciclos, metricas['pib'], 'b-', linewidth=2, marker='o', markersize=3)
    axes[0, 0].set_title('📈 Evolución del PIB', fontweight='bold')
    axes[0, 0].set_xlabel('Ciclos')
    axes[0, 0].set_ylabel('PIB ($)')
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].ticklabel_format(style='plain', axis='y')
    
    # 2. Inflación
    axes[0, 1].plot(ciclos, [i*100 for i in metricas['inflacion']], 'r-', linewidth=2, marker='s', markersize=3)
    axes[0, 1].set_title('🔥 Tasa de Inflación', fontweight='bold')
    axes[0, 1].set_xlabel('Ciclos')
    axes[0, 1].set_ylabel('Inflación (%)')
    axes[0, 1].grid(True, alpha=0.3)
    axes[0, 1].axhline(y=2, color='g', linestyle='--', alpha=0.7, label='Objetivo 2%')
    axes[0, 1].legend()
    
    # 3. Desempleo
    axes[0, 2].plot(ciclos, [d*100 for d in metricas['desempleo']], 'orange', linewidth=2, marker='^', markersize=3)
    axes[0, 2].set_title('👥 Tasa de Desempleo', fontweight='bold')
    axes[0, 2].set_xlabel('Ciclos')
    axes[0, 2].set_ylabel('Desempleo (%)')
    axes[0, 2].grid(True, alpha=0.3)
    axes[0, 2].axhline(y=5, color='g', linestyle='--', alpha=0.7, label='Objetivo 5%')
    axes[0, 2].legend()
    
    # 4. Dinero por agente
    axes[1, 0].plot(ciclos, metricas['dinero_consumidores'], 'g-', linewidth=2, label='Consumidores')
    axes[1, 0].plot(ciclos, metricas['dinero_empresas'], 'purple', linewidth=2, label='Empresas')
    axes[1, 0].set_title('💰 Dinero Promedio por Agente', fontweight='bold')
    axes[1, 0].set_xlabel('Ciclos')
    axes[1, 0].set_ylabel('Dinero Promedio ($)')
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].legend()
    axes[1, 0].ticklabel_format(style='plain', axis='y')
    
    # 5. Precios promedio
    axes[1, 1].plot(ciclos, metricas['precios_promedio'], 'brown', linewidth=2, marker='d', markersize=3)
    axes[1, 1].set_title('💲 Precios Promedio', fontweight='bold')
    axes[1, 1].set_xlabel('Ciclos')
    axes[1, 1].set_ylabel('Precio Promedio ($)')
    axes[1, 1].grid(True, alpha=0.3)
    
    # 6. Actividad económica (transacciones)
    axes[1, 2].bar(ciclos[::5], metricas['transacciones_totales'][::5], alpha=0.7, color='teal')
    axes[1, 2].set_title('📊 Volumen de Transacciones', fontweight='bold')
    axes[1, 2].set_xlabel('Ciclos (cada 5)')
    axes[1, 2].set_ylabel('Número de Transacciones')
    axes[1, 2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'economia_simulacion_{time.time():.0f}.png', dpi=300, bbox_inches='tight')
    print("   📊 Gráfico guardado como economia_simulacion_[timestamp].png")
    plt.show()
    
    print("   ✅ Visualizaciones generadas correctamente")

def main():
    """Función principal de la simulación"""
    print("🌟 SIMULADOR ECONÓMICO AVANZADO 🌟")
    print("=" * 50)
    
    # 1. Crear bienes realistas
    bienes = crear_bienes_realistas()
    print(f"✅ Creados {len(bienes)} tipos de bienes con características económicas realistas")
    
    # 2. Inicializar mercado
    mercado = Mercado(bienes)
    print("✅ Mercado inicializado con gobierno y políticas económicas")
    
    # 3. Configurar economía inicial
    configurar_economia_inicial(mercado)
    
    # 4. Ejecutar simulación
    num_ciclos = 40  # Simulación más larga para ver efectos
    metricas = ejecutar_simulacion(mercado, num_ciclos)
    
    # 5. Análisis final
    generar_analisis_economico(mercado, metricas)
    
    # 6. Crear visualizaciones
    crear_visualizaciones(metricas)
    
    # 7. Estadísticas finales detalladas
    print("\n📋 ESTADÍSTICAS DETALLADAS:")
    print("-" * 40)
    stats = mercado.obtener_estadisticas_completas()
    
    print(f"🔄 Ciclos simulados: {num_ciclos}")
    print(f"👥 Agentes económicos totales: {len(mercado.personas)}")
    print(f"🏪 Bienes en el mercado: {len(bienes)}")
    print(f"📊 Transacciones registradas: {len(mercado.transacciones):,}")
    print(f"🏦 Reservas gubernamentales: ${mercado.gobierno.presupuesto:,.2f}")
    print(f"📈 Tasa de interés actual: {mercado.gobierno.tasa_interes_referencia:.2%}")
    
    print("\n🎉 ¡Simulación económica completada exitosamente!")
    print("    Los resultados muestran un ecosistema económico funcional")
    print("    con leyes económicas realistas implementadas.")

if __name__ == "__main__":
    main()
