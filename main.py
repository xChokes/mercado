"""
SIMULADOR ECONÓMICO AVANZADO
============================

Simulación económica realista con sistemas integrados:
- Sistema Bancario y Crédito
- Sectores Económicos Multi-sectoriales  
- Innovación y Tecnología
- Psicología Económica (Behavioral Economics)
- Analytics y Machine Learning

Autor: Simulador Económico Team
Versión: 2.0 - Sistemas Avanzados Integrados
"""

import sys
import os
import random
import time
import matplotlib.pyplot as plt
import numpy as np

# Añadir src al path de Python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.models.Mercado import Mercado
from src.models.Bien import Bien
from src.models.Consumidor import Consumidor
from src.models.Empresa import Empresa
from src.models.EmpresaProductora import EmpresaProductora
from src.config.ConfigEconomica import ConfigEconomica
from src.config.ConfiguradorSimulacion import configurador
from src.systems.PsicologiaEconomica import inicializar_perfiles_psicologicos
from src.systems.ComercioInternacional import Pais, TipoCambio


def crear_bienes_realistas():
    """Crea bienes con características económicas realistas - CATÁLOGO EXPANDIDO"""
    bienes = {}
    
    # Bienes básicos (necesidades)
    bienes['Arroz'] = Bien('Arroz', 'alimentos_basicos')
    bienes['Papa'] = Bien('Papa', 'alimentos_basicos')
    bienes['Pan'] = Bien('Pan', 'alimentos_basicos')
    bienes['Leche'] = Bien('Leche', 'alimentos_basicos')
    bienes['Sal'] = Bien('Sal', 'alimentos_basicos')
    bienes['Aceite'] = Bien('Aceite', 'alimentos_basicos')
    bienes['Azucar'] = Bien('Azucar', 'alimentos_basicos')
    bienes['Agua'] = Bien('Agua', 'alimentos_basicos')
    bienes['Harina'] = Bien('Harina', 'alimentos_basicos')
    bienes['Frijoles'] = Bien('Frijoles', 'alimentos_basicos')
    
    # Bienes de lujo alimentarios
    bienes['Carne'] = Bien('Carne', 'alimentos_lujo')
    bienes['Pollo'] = Bien('Pollo', 'alimentos_lujo')
    bienes['Huevos'] = Bien('Huevos', 'alimentos_lujo')
    bienes['Cafe'] = Bien('Cafe', 'alimentos_lujo')
    bienes['Pescado'] = Bien('Pescado', 'alimentos_lujo')
    bienes['Queso'] = Bien('Queso', 'alimentos_lujo')
    bienes['Chocolate'] = Bien('Chocolate', 'alimentos_lujo')
    bienes['Vino'] = Bien('Vino', 'alimentos_lujo')
    bienes['Frutas'] = Bien('Frutas', 'alimentos_lujo')
    bienes['Verduras'] = Bien('Verduras', 'alimentos_lujo')
    
    # Bienes manufacturados básicos
    bienes['Ropa'] = Bien('Ropa', 'bienes_duraderos')
    bienes['Calzado'] = Bien('Calzado', 'bienes_duraderos')
    bienes['Muebles'] = Bien('Muebles', 'bienes_duraderos')
    bienes['Electrodomesticos'] = Bien('Electrodomesticos', 'bienes_duraderos')
    bienes['Libros'] = Bien('Libros', 'bienes_duraderos')
    bienes['Herramientas'] = Bien('Herramientas', 'bienes_duraderos')
    
    # Bienes tecnológicos
    bienes['Computadora'] = Bien('Computadora', 'tecnologia')
    bienes['Telefono'] = Bien('Telefono', 'tecnologia')
    bienes['Television'] = Bien('Television', 'tecnologia')
    bienes['Internet'] = Bien('Internet', 'tecnologia')
    bienes['Software'] = Bien('Software', 'tecnologia')
    
    # Servicios básicos
    bienes['Transporte'] = Bien('Transporte', 'servicios')
    bienes['Educacion'] = Bien('Educacion', 'servicios')
    bienes['Salud'] = Bien('Salud', 'servicios')
    bienes['Vivienda'] = Bien('Vivienda', 'servicios')
    bienes['Electricidad'] = Bien('Electricidad', 'servicios')
    bienes['Gas'] = Bien('Gas', 'servicios')
    bienes['Seguridad'] = Bien('Seguridad', 'servicios')
    
    # Servicios de lujo
    bienes['Entretenimiento'] = Bien('Entretenimiento', 'servicios_lujo')
    bienes['Turismo'] = Bien('Turismo', 'servicios_lujo')
    bienes['Restaurante'] = Bien('Restaurante', 'servicios_lujo')
    bienes['Gimnasio'] = Bien('Gimnasio', 'servicios_lujo')
    bienes['Spa'] = Bien('Spa', 'servicios_lujo')
    
    # Bienes de capital e intermedios
    bienes['Maquinaria'] = Bien('Maquinaria', 'capital')
    bienes['Materias_Primas'] = Bien('Materias_Primas', 'intermedio')
    bienes['Energia'] = Bien('Energia', 'intermedio')
    bienes['Acero'] = Bien('Acero', 'intermedio')
    bienes['Cemento'] = Bien('Cemento', 'intermedio')
    bienes['Plastico'] = Bien('Plastico', 'intermedio')
    
    # Bienes financieros
    bienes['Seguros'] = Bien('Seguros', 'financiero')
    bienes['Credito'] = Bien('Credito', 'financiero')
    bienes['Inversion'] = Bien('Inversion', 'financiero')
    
    return bienes


def configurar_economia_inicial(mercado):
    """Configura el estado inicial de la economía con parámetros configurables"""
    print("🏗️  Configurando economía inicial...")
    
    # Obtener configuración
    config_sim = configurador.obtener_seccion('simulacion')
    config_econ = configurador.obtener_seccion('economia')
    
    num_productoras = config_sim.get('num_empresas_productoras', 5)
    num_comerciales = config_sim.get('num_empresas_comerciales', 8)
    num_consumidores = config_sim.get('num_consumidores', 250)
    
    # Actualizar configuración económica global
    configurador.actualizar_configuracion_economica(ConfigEconomica)
    
    # Crear empresas productoras especializadas
    empresas_productoras = []
    nombres_productoras = [
        "AgroIndustrias SA", "AlimentosPro Ltd", "ManufacturaMax Corp",
        "ProduccionTotal Inc", "IndustriasPrima SA", "TecnoFabrik SA",
        "ProcessingCorp Ltd", "MaterialesPro Inc"
    ]
    
    
    for i, nombre in enumerate(nombres_productoras):
        empresa = EmpresaProductora(nombre, mercado)
        mercado.agregar_persona(empresa)
        empresas_productoras.append(empresa)
        print(f"   ✅ Creada {nombre} con capital inicial ${empresa.dinero:,.2f}")
    
    # Crear consumidores con características diversas
    consumidores = []
    for i in range(250):  # 250 consumidores para mayor realismo
        nombre = f"Consumidor{i+1:03d}"
        consumidor = Consumidor(nombre, mercado)
        mercado.agregar_persona(consumidor)
        consumidores.append(consumidor)
        
        # Asignar empleos iniciales (75% empleados)
        if consumidor.empleado and empresas_productoras and random.random() < 0.75:
            empleador = random.choice(empresas_productoras)
            if empleador.contratar(consumidor):
                consumidor.empleador = empleador
                
    # Crear empresas de servicios/comercio
    nombres_comerciales = [
        "ComercioLocal SA", "ServiciosPlus Ltd", "RetailMax Corp",
        "DistribucionTotal Inc", "ComercialCenter SA", "MarketPlace Ltd",
        "ServiceHub Corp", "TradingPro Inc"
    ]
    
    for nombre in nombres_comerciales:
        empresa = Empresa.crear_con_acciones(
            nombre=nombre, 
            mercado=mercado, 
            cantidad_acciones=1000, 
            bienes={}
        )
        mercado.agregar_persona(empresa)
        print(f"   ✅ Creada {nombre} con capital inicial ${empresa.dinero:,.2f}")
    
    print(f"   📊 Total: {len(empresas_productoras)} productoras, {len(consumidores)} consumidores, {len(nombres_comerciales)} comerciales")
    print("   🎯 Economía inicial configurada correctamente")
    
    return empresas_productoras, consumidores


def ejecutar_simulacion(mercado, num_ciclos=50):
    """Ejecuta la simulación económica completa"""
    print(f"\n🚀 Iniciando simulación económica de {num_ciclos} ciclos...")
    inicio = time.time()
    
    # Almacenar métricas expandidas
    metricas = {
        'pib': [],
        'inflacion': [],
        'desempleo': [],
        'dinero_consumidores': [],
        'dinero_empresas': [],
        'precios_promedio': [],
        'transacciones_totales': [],
        'sistema_bancario': [],
        'sectores_economicos': [],
        'innovacion': [],
        'psicologia': [],
        'analytics': []
    }
    
    for ciclo in range(num_ciclos):
        print(f"\n📅 Ejecutando ciclo {ciclo + 1}/{num_ciclos}")

        try:
            mercado.actualizar_demografia()
            mercado.ejecutar_ciclo(ciclo)
            
            # Recopilar métricas básicas
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
            
            # Sistemas avanzados
            try:
                # Sistema bancario
                stats_bancario = mercado.sistema_bancario.obtener_estadisticas_sistema()
                metricas['sistema_bancario'].append(stats_bancario)
                
                # Sectores económicos
                stats_sectores = mercado.economia_sectorial.obtener_estadisticas_sectoriales()
                metricas['sectores_economicos'].append(stats_sectores)
                
                # Sistema de innovación
                stats_innovacion = mercado.sistema_innovacion.obtener_estadisticas_innovacion()
                metricas['innovacion'].append(stats_innovacion)
                
                # Analytics y ML
                stats_analytics = mercado.sistema_analytics.obtener_estadisticas_analytics()
                metricas['analytics'].append(stats_analytics)
                
                # Psicología económica
                if hasattr(mercado, 'sistema_psicologia') and mercado.sistema_psicologia:
                    stats_psicologia = mercado.sistema_psicologia.obtener_estadisticas_psicologicas()
                    metricas['psicologia'].append(stats_psicologia)
                else:
                    metricas['psicologia'].append({})
                    
            except Exception as e:
                print(f"   ⚠️  Error recopilando métricas avanzadas: {e}")
                # Agregar valores vacíos para mantener consistencia
                for key in ['sistema_bancario', 'sectores_economicos', 'innovacion', 'analytics', 'psicologia']:
                    metricas[key].append({})
            
            # Progreso cada 10 ciclos
            if (ciclo + 1) % 10 == 0:
                porcentaje = ((ciclo + 1) / num_ciclos) * 100
                print(f"   ⏱️  Progreso: {porcentaje:.1f}% completado")
                
                # Mini-reporte intermedio
                pib_actual = metricas['pib'][-1] if metricas['pib'] else 0
                desempleo_actual = metricas['desempleo'][-1] if metricas['desempleo'] else 0
                print(f"   📊 PIB: ${pib_actual:,.0f} | Desempleo: {desempleo_actual:.1%} | Fase: {mercado.fase_ciclo_economico}")
                
        except Exception as e:
            print(f"   ❌ Error en ciclo {ciclo + 1}: {e}")
            continue
    
    tiempo_total = time.time() - inicio
    print(f"\n✅ Simulación completada en {tiempo_total:.2f} segundos")
    
    return metricas


def generar_analisis_economico(mercado, metricas):
    """Genera análisis económico detallado"""
    print("\n" + "="*80)
    print("📊 ANÁLISIS ECONÓMICO FINAL - SIMULADOR AVANZADO")
    print("="*80)
    
    # === INDICADORES MACROECONÓMICOS ===
    print("\n🎯 INDICADORES MACROECONÓMICOS:")
    print("-" * 50)
    
    pib_final = metricas['pib'][-1] if metricas['pib'] else 0
    pib_inicial = metricas['pib'][0] if metricas['pib'] else 0
    crecimiento_pib = ((pib_final - pib_inicial) / pib_inicial * 100) if pib_inicial > 0 else 0
    
    inflacion_promedio = sum(metricas['inflacion']) / len(metricas['inflacion']) if metricas['inflacion'] else 0
    desempleo_promedio = sum(metricas['desempleo']) / len(metricas['desempleo']) if metricas['desempleo'] else 0
    
    print(f"📈 PIB Final: ${pib_final:,.2f}")
    print(f"📊 Crecimiento PIB: {crecimiento_pib:+.2f}%")
    print(f"💰 Inflación Promedio: {inflacion_promedio:.2%}")
    print(f"👥 Desempleo Promedio: {desempleo_promedio:.2%}")
    
    # Estado del mercado laboral
    empleados = sum([1 for c in mercado.getConsumidores() if c.empleado])
    total_consumidores = len(mercado.getConsumidores())
    tasa_empleo = empleados / total_consumidores if total_consumidores > 0 else 0
    
    print(f"💼 Tasa de Empleo Final: {tasa_empleo:.2%}")
    print(f"🏢 Empresas Activas: {len(mercado.getEmpresas())}")
    
    # === ANÁLISIS DE COMPETENCIA ===
    print(f"\n🏆 ANÁLISIS DE COMPETENCIA:")
    print("-" * 50)
    for bien, nivel in mercado.nivel_competencia.items():
        estado = "🔴 Baja" if nivel < 0.4 else "🟡 Media" if nivel < 0.7 else "🟢 Alta"
        print(f"   {bien}: {estado} competencia (índice: {nivel:.2f})")
    
    # === CICLO ECONÓMICO ===
    print(f"\n🔄 ESTADO MACROECONÓMICO:")
    print("-" * 50)
    print(f"Fase Económica: {mercado.fase_ciclo_economico.upper()}")
    if mercado.shock_economico_activo:
        print("⚠️  SHOCK ECONÓMICO ACTIVO")
    
    # === SISTEMAS AVANZADOS ===
    print(f"\n🏦 SISTEMA BANCARIO:")
    print("-" * 50)
    if metricas['sistema_bancario']:
        stats_bancario = metricas['sistema_bancario'][-1]
        print(f"Capital Total: ${stats_bancario.get('capital_total', 0):,.2f}")
        print(f"Préstamos Totales: ${stats_bancario.get('prestamos_totales', 0):,.2f}")
        print(f"Depósitos Totales: ${stats_bancario.get('depositos_totales', 0):,.2f}")
        print(f"Tasa de Referencia: {stats_bancario.get('tasa_referencia', 0):.2%}")
        print(f"Bancos Operando: {stats_bancario.get('bancos_operando', 0)}")
    
    print(f"\n🏭 ANÁLISIS SECTORIAL:")
    print("-" * 50)
    if metricas['sectores_economicos']:
        stats_sectores = metricas['sectores_economicos'][-1]
        for sector, datos in stats_sectores.items():
            if isinstance(datos, dict) and 'pib' in datos:
                participacion = datos.get('participacion_pib', 0) * 100
                print(f"{sector.capitalize()}: PIB ${datos['pib']:,.0f} ({participacion:.1f}%) - {datos['empresas']} empresas - {datos['empleo']} empleos")
    
    print(f"\n🔬 SISTEMA DE INNOVACIÓN:")
    print("-" * 50)
    if metricas['innovacion']:
        stats_innovacion = metricas['innovacion'][-1]
        print(f"Inversión I+D Total: ${stats_innovacion.get('inversion_id_total', 0):,.2f}")
        print(f"Tecnologías Disponibles: {stats_innovacion.get('tecnologias_disponibles', 0)}")
        print(f"Productos Innovadores: {stats_innovacion.get('productos_innovadores', 0)}")
        print(f"Empresas Innovadoras: {stats_innovacion.get('empresas_innovadoras', 0)} ({stats_innovacion.get('porcentaje_empresas_innovadoras', 0):.1%})")
    
    print(f"\n🤖 SISTEMA DE ANALYTICS Y ML:")
    print("-" * 50)
    if metricas['analytics']:
        stats_analytics = metricas['analytics'][-1]
        print(f"Modelos Entrenados: {stats_analytics.get('modelos_entrenados', 0)}")
        print(f"Predictores Disponibles: {stats_analytics.get('predictores_disponibles', 0)}")
        if 'clusters_identificados' in stats_analytics:
            print(f"Clusters de Consumidores: {stats_analytics.get('clusters_identificados', 0)}")
            if 'perfiles_consumidor' in stats_analytics:
                print("Perfiles Identificados:")
                for cluster, perfil in stats_analytics['perfiles_consumidor'].items():
                    print(f"  • {cluster}: {perfil}")
    
    print(f"\n🧠 PERFIL PSICOLÓGICO ECONÓMICO:")
    print("-" * 50)
    if metricas['psicologia'] and any(metricas['psicologia']):
        stats_psicologia = next((p for p in reversed(metricas['psicologia']) if p), {})
        print(f"Confianza del Consumidor: {stats_psicologia.get('confianza_promedio', 0.5):.1%}")
        print(f"Aversión al Riesgo Promedio: {stats_psicologia.get('aversion_riesgo_promedio', 0.5):.1%}")
        print(f"Optimismo General: {stats_psicologia.get('optimismo_promedio', 0.5):.1%}")
    
    # === RANKING EMPRESARIAL ===
    print(f"\n🥇 TOP 5 EMPRESAS POR CAPITAL:")
    print("-" * 50)
    empresas_ordenadas = sorted(mercado.getEmpresas(), 
                               key=lambda e: e.dinero, reverse=True)[:5]
    for i, empresa in enumerate(empresas_ordenadas, 1):
        emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "🏅"
        print(f"{emoji} {i}. {empresa.nombre}: ${empresa.dinero:,.2f}")
    
    # === ACTIVIDAD ECONÓMICA ===
    print(f"\n💵 ACTIVIDAD ECONÓMICA:")
    print("-" * 50)
    total_transacciones = len(mercado.transacciones)
    volumen_total = sum([t.get('costo_total', 0) for t in mercado.transacciones])
    print(f"Total Transacciones: {total_transacciones:,}")
    print(f"Volumen Total: ${volumen_total:,.2f}")
    print(f"Transacción Promedio: ${volumen_total/max(1, total_transacciones):,.2f}")


def crear_visualizaciones_avanzadas(metricas):
    """Crea gráficos de análisis económico avanzados"""
    print("\n📊 Generando visualizaciones avanzadas...")
    
    # Configurar estilo profesional
    plt.style.use('default')
    plt.rcParams.update({
        'font.size': 10,
        'axes.titlesize': 12,
        'axes.labelsize': 10,
        'xtick.labelsize': 9,
        'ytick.labelsize': 9,
        'legend.fontsize': 9
    })
    
    # Crear figura principal con 8 subplots
    fig = plt.figure(figsize=(20, 16))
    fig.suptitle('🏛️ SIMULADOR ECONÓMICO AVANZADO - ANÁLISIS INTEGRAL', 
                 fontsize=18, fontweight='bold', y=0.95)
    
    ciclos = range(len(metricas['pib']))
    
    # 1. PIB y Crecimiento
    ax1 = plt.subplot(3, 3, 1)
    ax1.plot(ciclos, metricas['pib'], 'b-', linewidth=2, marker='o', markersize=2)
    ax1.set_title('📈 Evolución del PIB', fontweight='bold')
    ax1.set_xlabel('Ciclos')
    ax1.set_ylabel('PIB ($)')
    ax1.grid(True, alpha=0.3)
    ax1.ticklabel_format(style='plain', axis='y')
    
    # 2. Inflación vs Objetivo
    ax2 = plt.subplot(3, 3, 2)
    ax2.plot(ciclos, [i*100 for i in metricas['inflacion']], 'r-', linewidth=2, marker='s', markersize=2)
    ax2.axhline(y=2, color='g', linestyle='--', alpha=0.7, label='Objetivo 2%')
    ax2.axhline(y=-2, color='orange', linestyle='--', alpha=0.7, label='Deflación -2%')
    ax2.set_title('🔥 Tasa de Inflación', fontweight='bold')
    ax2.set_xlabel('Ciclos')
    ax2.set_ylabel('Inflación (%)')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    # 3. Desempleo
    ax3 = plt.subplot(3, 3, 3)
    ax3.plot(ciclos, [d*100 for d in metricas['desempleo']], 'orange', linewidth=2, marker='^', markersize=2)
    ax3.axhline(y=5, color='g', linestyle='--', alpha=0.7, label='Objetivo 5%')
    ax3.set_title('👥 Tasa de Desempleo', fontweight='bold')
    ax3.set_xlabel('Ciclos')
    ax3.set_ylabel('Desempleo (%)')
    ax3.grid(True, alpha=0.3)
    ax3.legend()
    
    # 4. Distribución de Riqueza
    ax4 = plt.subplot(3, 3, 4)
    ax4.plot(ciclos, metricas['dinero_consumidores'], 'g-', linewidth=2, label='Consumidores', marker='o', markersize=2)
    ax4.plot(ciclos, metricas['dinero_empresas'], 'purple', linewidth=2, label='Empresas', marker='s', markersize=2)
    ax4.set_title('💰 Dinero Promedio por Agente', fontweight='bold')
    ax4.set_xlabel('Ciclos')
    ax4.set_ylabel('Dinero Promedio ($)')
    ax4.grid(True, alpha=0.3)
    ax4.legend()
    ax4.ticklabel_format(style='plain', axis='y')
    
    # 5. Precios y Actividad
    ax5 = plt.subplot(3, 3, 5)
    ax5.plot(ciclos, metricas['precios_promedio'], 'brown', linewidth=2, marker='d', markersize=2)
    ax5.set_title('💲 Precios Promedio', fontweight='bold')
    ax5.set_xlabel('Ciclos')
    ax5.set_ylabel('Precio Promedio ($)')
    ax5.grid(True, alpha=0.3)
    
    # 6. Volumen de Transacciones
    ax6 = plt.subplot(3, 3, 6)
    ax6.bar(ciclos[::5], metricas['transacciones_totales'][::5], alpha=0.7, color='teal', width=1.5)
    ax6.set_title('📊 Volumen de Transacciones', fontweight='bold')
    ax6.set_xlabel('Ciclos (cada 5)')
    ax6.set_ylabel('Número de Transacciones')
    ax6.grid(True, alpha=0.3)
    
    # 7. Sistema Bancario
    ax7 = plt.subplot(3, 3, 7)
    if metricas['sistema_bancario']:
        capital_bancario = [s.get('capital_total', 0) for s in metricas['sistema_bancario']]
        ax7.plot(ciclos, capital_bancario, 'darkblue', linewidth=2, marker='x', markersize=3)
        ax7.set_title('🏦 Capital Bancario Total', fontweight='bold')
        ax7.set_xlabel('Ciclos')
        ax7.set_ylabel('Capital ($)')
        ax7.grid(True, alpha=0.3)
        ax7.ticklabel_format(style='plain', axis='y')
    
    # 8. Innovación
    ax8 = plt.subplot(3, 3, 8)
    if metricas['innovacion']:
        inversion_id = [s.get('inversion_id_total', 0) for s in metricas['innovacion']]
        ax8.plot(ciclos, inversion_id, 'darkgreen', linewidth=2, marker='*', markersize=3)
        ax8.set_title('🔬 Inversión en I+D Acumulada', fontweight='bold')
        ax8.set_xlabel('Ciclos')
        ax8.set_ylabel('Inversión I+D ($)')
        ax8.grid(True, alpha=0.3)
        ax8.ticklabel_format(style='plain', axis='y')
    
    # 9. Indicador Compuesto
    ax9 = plt.subplot(3, 3, 9)
    if len(metricas['pib']) > 0 and len(metricas['desempleo']) > 0:
        # Crear índice de bienestar económico
        pib_norm = np.array(metricas['pib']) / max(metricas['pib']) if max(metricas['pib']) > 0 else np.zeros(len(metricas['pib']))
        desempleo_norm = 1 - np.array(metricas['desempleo'])  # Invertir desempleo
        indice_bienestar = (pib_norm + desempleo_norm) / 2
        
        ax9.plot(ciclos, indice_bienestar, 'darkred', linewidth=3, marker='o', markersize=2)
        ax9.axhline(y=0.7, color='g', linestyle='--', alpha=0.7, label='Bienestar Alto')
        ax9.set_title('📈 Índice de Bienestar Económico', fontweight='bold')
        ax9.set_xlabel('Ciclos')
        ax9.set_ylabel('Índice (0-1)')
        ax9.grid(True, alpha=0.3)
        ax9.legend()
    
    plt.tight_layout()
    timestamp = int(time.time())
    filename = f'results/simulacion_economica_avanzada_{timestamp}.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"   📊 Análisis completo guardado: {filename}")
    plt.show()
    
    print("   ✅ Visualizaciones avanzadas generadas correctamente")


def mostrar_resumen_inicial():
    """Muestra información del simulador al inicio"""
    print("="*80)
    print("🌟 SIMULADOR ECONÓMICO AVANZADO v2.0")
    print("="*80)
    print("🎯 SISTEMAS INTEGRADOS:")
    print("   🏦 Sistema Bancario y Crédito")
    print("   🏭 Sectores Económicos Multi-sectoriales") 
    print("   🔬 Innovación y Tecnología")
    print("   🧠 Psicología Económica (Behavioral Economics)")
    print("   🤖 Analytics y Machine Learning")
    print("="*80)


def main():
    """Función principal del simulador económico avanzado"""
    mostrar_resumen_inicial()
    
    # 1. Crear bienes realistas ampliados
    bienes = crear_bienes_realistas()
    print(f"✅ Creados {len(bienes)} tipos de bienes con características económicas realistas")
    
    # 2. Inicializar mercado con sistemas avanzados
    mercado = Mercado(bienes)
    print("✅ Mercado inicializado con sistemas avanzados integrados")

    # 3. Configurar comercio internacional
    tipo_cambio = TipoCambio(ConfigEconomica.TIPOS_CAMBIO_INICIALES)
    pais_a = Pais("PaisA", "USD")
    pais_b = Pais("PaisB", "EUR")
    pais_a.establecer_arancel(pais_b.nombre, ConfigEconomica.ARANCEL_BASE)
    pais_b.establecer_arancel(pais_a.nombre, ConfigEconomica.ARANCEL_BASE)
    mercado.tipo_cambio = tipo_cambio
    mercado.agregar_pais(pais_a)
    mercado.agregar_pais(pais_b)
    print("✅ Sistema de comercio internacional inicializado")

    # 4. Configurar economía inicial
    empresas_productoras, consumidores = configurar_economia_inicial(mercado)
    
    # 5. Activar sistemas de psicología económica
    inicializar_perfiles_psicologicos(mercado)
    print("✅ Sistema de psicología económica activado con perfiles individualizados")

    # 6. Asignar empresas a sectores económicos
    mercado.economia_sectorial.asignar_empresas_a_sectores()
    print("✅ Sistema sectorial configurado con especialización productiva")

    # 7. Ejemplo de transacción internacional
    exportador = random.choice(mercado.getEmpresas())
    importador = random.choice([e for e in mercado.getEmpresas() if e != exportador])
    mercado.realizar_transaccion_internacional(exportador, importador,
                                               'Arroz', 10, 5,
                                               pais_a, pais_b)
    print("✅ Transacción internacional de ejemplo registrada")

    # 8. Ejecutar simulación principal con configuración
    num_ciclos = configurador.obtener('simulacion', 'num_ciclos', 50)
    metricas = ejecutar_simulacion(mercado, num_ciclos)

    # 9. Análisis económico integral
    generar_analisis_economico(mercado, metricas)

    # 10. Crear visualizaciones avanzadas
    crear_visualizaciones_avanzadas(metricas)

    # 11. Estadísticas finales comprehensivas
    print("\n" + "="*80)
    print("📋 ESTADÍSTICAS FINALES DEL SISTEMA")
    print("="*80)
    stats = mercado.obtener_estadisticas_completas()
    
    print(f"🔄 Ciclos simulados: {num_ciclos}")
    print(f"👥 Agentes económicos totales: {len(mercado.personas)}")
    print(f"   └─ Consumidores: {len([p for p in mercado.personas if p.__class__.__name__ == 'Consumidor'])}")
    print(f"   └─ Empresas: {len([p for p in mercado.personas if 'Empresa' in p.__class__.__name__])}")
    print(f"🏪 Bienes en el mercado: {len(bienes)}")
    print(f"📊 Transacciones registradas: {len(mercado.transacciones):,}")
    print(f"🏦 Reservas gubernamentales: ${mercado.gobierno.presupuesto:,.2f}")
    print(f"📈 Tasa de interés gubernamental: {mercado.gobierno.tasa_interes_referencia:.2%}")
    
    # Estado final de sistemas
    print(f"\n🔧 ESTADO DE SISTEMAS AVANZADOS:")
    print(f"   🏦 Bancos operando: {len(mercado.sistema_bancario.bancos)}")
    print(f"   🏭 Sectores activos: {len([s for s in mercado.economia_sectorial.sectores.values() if s.empresas])}")
    print(f"   🔬 Tecnologías disponibles: {len(mercado.sistema_innovacion.tecnologias_disponibles)}")
    print(f"   🤖 Modelos ML entrenados: {len([p for p in mercado.sistema_analytics.predictor_demanda.values() if p.caracteristicas_entrenadas])}")
    
    print(f"\n🎉 ¡SIMULACIÓN ECONÓMICA AVANZADA COMPLETADA EXITOSAMENTE!")
    print(f"    ✨ Ecosistema económico complejo funcionando con {len(mercado.personas)} agentes")
    print(f"    🎯 Sistemas realistas implementados y coordinados")
    print(f"    📊 Análisis multi-dimensional disponible en /results/")
    print("="*80)


if __name__ == "__main__":
    main()
