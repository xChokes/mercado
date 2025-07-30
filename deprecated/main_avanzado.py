"""
Simulación económica avanzada con sistemas integrados
Incluye: Sistema bancario, sectores económicos, psicología económica e innovación
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


def crear_bienes_avanzados():
    """Crea bienes con mayor variedad y características económicas realistas"""
    bienes = {}

    # Bienes básicos alimentarios
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
    bienes['Chocolate'] = Bien('Chocolate', 'alimentos_lujo')

    # Servicios básicos
    bienes['Electricidad'] = Bien('Electricidad', 'servicios')
    bienes['Agua'] = Bien('Agua', 'servicios')
    bienes['Internet'] = Bien('Internet', 'servicios')
    bienes['Transporte'] = Bien('Transporte', 'servicios')

    # Bienes duraderos
    bienes['Telefono'] = Bien('Telefono', 'bienes_duraderos')
    bienes['Computadora'] = Bien('Computadora', 'bienes_duraderos')
    bienes['Refrigerador'] = Bien('Refrigerador', 'bienes_duraderos')

    return bienes


def configurar_economia_avanzada(mercado):
    """Configura una economía más sofisticada con diferentes tipos de empresas"""
    print("🏗️  Configurando economía avanzada...")

    # Crear empresas productoras especializadas por sector
    empresas_agricultura = []
    for i in range(3):  # 3 empresas agrícolas
        nombre = f"AgroEmpresa{i+1}"
        empresa = EmpresaProductora(nombre, mercado)
        # Especializar en productos agrícolas
        productos_agricolas = ['Arroz', 'Papa', 'Cafe', 'Azucar']
        for producto in productos_agricolas:
            if producto in empresa.bienes:
                # Mayor capacidad en especialización
                empresa.capacidad_produccion[producto] *= 2
        mercado.agregar_persona(empresa)
        empresas_agricultura.append(empresa)
        print(f"   🌾 Creada {nombre} especializada en agricultura")

    # Empresas ganaderas
    empresas_ganaderia = []
    for i in range(2):
        nombre = f"Ganadera{i+1}"
        empresa = EmpresaProductora(nombre, mercado)
        productos_ganaderos = ['Carne', 'Pollo', 'Leche', 'Huevos']
        for producto in productos_ganaderos:
            if producto in empresa.bienes:
                empresa.capacidad_produccion[producto] *= 2
        mercado.agregar_persona(empresa)
        empresas_ganaderia.append(empresa)
        print(f"   🐄 Creada {nombre} especializada en ganadería")

    # Empresas de servicios
    empresas_servicios = []
    for i in range(4):
        nombre = f"ServiciosEmpresa{i+1}"
        empresa = Empresa.crear_con_acciones(
            nombre=nombre,
            mercado=mercado,
            cantidad_acciones=1000,
            bienes={}
        )
        mercado.agregar_persona(empresa)
        empresas_servicios.append(empresa)
        print(f"   🏢 Creada {nombre} de servicios")

    # Empresas tecnológicas (innovadoras)
    empresas_tech = []
    for i in range(2):
        nombre = f"TechCorp{i+1}"
        empresa = EmpresaProductora(nombre, mercado)
        # Mayor capital para I+D
        empresa.dinero *= 1.5
        productos_tech = ['Telefono', 'Computadora', 'Internet']
        for producto in productos_tech:
            if producto in empresa.bienes:
                empresa.capacidad_produccion[producto] *= 1.5
        mercado.agregar_persona(empresa)
        empresas_tech.append(empresa)
        print(f"   💻 Creada {nombre} especializada en tecnología")

    # Crear consumidores con perfiles diversos
    consumidores = []
    for i in range(300):  # Mayor población para mejor simulación
        nombre = f"Consumidor{i+1}"
        consumidor = Consumidor(nombre, mercado)
        mercado.agregar_persona(consumidor)
        consumidores.append(consumidor)

        # Asignar empleos con preferencia sectorial
        if consumidor.empleado:
            todas_empresas = empresas_agricultura + \
                empresas_ganaderia + empresas_servicios + empresas_tech
            if todas_empresas:
                empleador = random.choice(todas_empresas)
                if empleador.contratar(consumidor):
                    consumidor.empleador = empleador

    total_empresas = len(empresas_agricultura) + len(empresas_ganaderia) + \
        len(empresas_servicios) + len(empresas_tech)
    print(
        f"   📊 Total: {total_empresas} empresas, {len(consumidores)} consumidores")
    print("   🎯 Economía avanzada configurada correctamente")


def ejecutar_simulacion_avanzada(mercado, num_ciclos=60):
    """Ejecuta simulación económica con sistemas avanzados"""
    print(
        f"\n🚀 Iniciando simulación económica avanzada de {num_ciclos} ciclos...")
    print("   🏦 Sistema bancario activo")
    print("   🏭 Sectores económicos diferenciados")
    print("   🧠 Psicología económica implementada")
    print("   🔬 Sistema de innovación y tecnología")

    inicio = time.time()

    # Almacenar métricas expandidas
    metricas = {
        # Métricas tradicionales
        'pib': [],
        'inflacion': [],
        'desempleo': [],
        'dinero_consumidores': [],
        'dinero_empresas': [],
        'precios_promedio': [],
        'transacciones_totales': [],

        # Métricas del sistema bancario
        'credito_total': [],
        'depositos_totales': [],
        'morosidad': [],

        # Métricas sectoriales
        'pib_primario': [],
        'pib_secundario': [],
        'pib_terciario': [],

        # Métricas psicológicas
        'optimismo_promedio': [],
        'estres_financiero': [],
        'confianza_consumidor': [],

        # Métricas de innovación
        'inversion_id': [],
        'productos_innovadores': [],
        'tecnologias_adoptadas': []
    }

    for ciclo in range(num_ciclos):
        print(f"\n📅 Ejecutando ciclo {ciclo + 1}/{num_ciclos}")

        try:
            mercado.ejecutar_ciclo(ciclo)

            # Recopilar métricas tradicionales
            stats = mercado.obtener_estadisticas_completas()
            metricas['pib'].append(stats['pib_historico']
                                   [-1] if stats['pib_historico'] else 0)
            metricas['inflacion'].append(
                stats['inflacion_historica'][-1] if stats['inflacion_historica'] else 0)
            metricas['desempleo'].append(
                stats['desempleo_historico'][-1] if stats['desempleo_historico'] else 0)

            # Dinero por tipo de agente
            dinero_cons = [c.dinero for c in mercado.getConsumidores()]
            dinero_emp = [e.dinero for e in mercado.getEmpresas()]
            metricas['dinero_consumidores'].append(
                sum(dinero_cons) / len(dinero_cons) if dinero_cons else 0)
            metricas['dinero_empresas'].append(
                sum(dinero_emp) / len(dinero_emp) if dinero_emp else 0)

            # Precio promedio
            precios_todos = []
            for empresa in mercado.getEmpresas():
                precios_todos.extend(empresa.precios.values())
            metricas['precios_promedio'].append(
                sum(precios_todos) / len(precios_todos) if precios_todos else 0)

            # Transacciones
            trans_ciclo = len(
                [t for t in mercado.transacciones if t.get('ciclo') == ciclo])
            metricas['transacciones_totales'].append(trans_ciclo)

            # Métricas del sistema bancario
            if 'sistema_bancario' in stats:
                sb_stats = stats['sistema_bancario']
                metricas['credito_total'].append(
                    sb_stats.get('prestamos_totales', 0))
                metricas['depositos_totales'].append(
                    sb_stats.get('depositos_totales', 0))
                # Morosidad promedio de todos los bancos
                morosidad_promedio = 0
                if hasattr(mercado.sistema_bancario, 'bancos'):
                    morosidades = [b.morosidad_historica[-1] if b.morosidad_historica else 0
                                   for b in mercado.sistema_bancario.bancos]
                    morosidad_promedio = sum(
                        morosidades) / len(morosidades) if morosidades else 0
                metricas['morosidad'].append(morosidad_promedio)
            else:
                metricas['credito_total'].append(0)
                metricas['depositos_totales'].append(0)
                metricas['morosidad'].append(0)

            # Métricas sectoriales
            if 'sectores_economicos' in stats:
                sectores = stats['sectores_economicos']
                pib_primario = sum(
                    [s['pib'] for s in sectores.values() if s.get('tipo') == 'primario'])
                pib_secundario = sum(
                    [s['pib'] for s in sectores.values() if s.get('tipo') == 'secundario'])
                pib_terciario = sum(
                    [s['pib'] for s in sectores.values() if s.get('tipo') == 'terciario'])

                metricas['pib_primario'].append(pib_primario)
                metricas['pib_secundario'].append(pib_secundario)
                metricas['pib_terciario'].append(pib_terciario)
            else:
                metricas['pib_primario'].append(0)
                metricas['pib_secundario'].append(0)
                metricas['pib_terciario'].append(0)

            # Métricas psicológicas
            if 'psicologia_economica' in stats:
                psico_stats = stats['psicologia_economica']
                metricas['optimismo_promedio'].append(
                    psico_stats.get('optimismo_promedio', 0.5))
                metricas['estres_financiero'].append(
                    psico_stats.get('estres_promedio', 0))
                metricas['confianza_consumidor'].append(
                    psico_stats.get('indice_confianza', 0.5))
            else:
                metricas['optimismo_promedio'].append(0.5)
                metricas['estres_financiero'].append(0)
                metricas['confianza_consumidor'].append(0.5)

            # Métricas de innovación
            if 'innovacion' in stats:
                innov_stats = stats['innovacion']
                metricas['inversion_id'].append(
                    innov_stats.get('inversion_id_total', 0))
                metricas['productos_innovadores'].append(
                    innov_stats.get('productos_innovadores', 0))
                metricas['tecnologias_adoptadas'].append(
                    innov_stats.get('tecnologias_disponibles', 0))
            else:
                metricas['inversion_id'].append(0)
                metricas['productos_innovadores'].append(0)
                metricas['tecnologias_adoptadas'].append(0)

            # Progreso cada 10 ciclos
            if (ciclo + 1) % 10 == 0:
                porcentaje = ((ciclo + 1) / num_ciclos) * 100
                print(f"   ⏱️  Progreso: {porcentaje:.1f}% completado")

                # Mostrar métricas clave
                pib_actual = metricas['pib'][-1] if metricas['pib'] else 0
                optimismo = metricas['optimismo_promedio'][-1] if metricas['optimismo_promedio'] else 0
                credito = metricas['credito_total'][-1] if metricas['credito_total'] else 0

                print(
                    f"   📊 PIB: ${pib_actual:,.0f} | Optimismo: {optimismo:.2f} | Crédito: ${credito:,.0f}")

        except Exception as e:
            print(f"   ❌ Error en ciclo {ciclo + 1}: {e}")
            continue

    tiempo_total = time.time() - inicio
    print(f"\n✅ Simulación avanzada completada en {tiempo_total:.2f} segundos")

    return metricas


def generar_analisis_avanzado(mercado, metricas):
    """Genera análisis económico con sistemas avanzados"""
    print("\n📊 ANÁLISIS ECONÓMICO AVANZADO")
    print("=" * 70)

    # Estadísticas básicas
    pib_final = metricas['pib'][-1] if metricas['pib'] else 0
    pib_inicial = metricas['pib'][0] if metricas['pib'] else 0
    crecimiento_pib = ((pib_final - pib_inicial) /
                       pib_inicial * 100) if pib_inicial > 0 else 0

    inflacion_promedio = sum(
        metricas['inflacion']) / len(metricas['inflacion']) if metricas['inflacion'] else 0
    desempleo_promedio = sum(
        metricas['desempleo']) / len(metricas['desempleo']) if metricas['desempleo'] else 0

    print(f"📈 PIB Final: ${pib_final:,.2f}")
    print(f"📊 Crecimiento PIB: {crecimiento_pib:+.2f}%")
    print(f"💰 Inflación Promedio: {inflacion_promedio:.2%}")
    print(f"👥 Desempleo Promedio: {desempleo_promedio:.2%}")

    # Análisis del sistema bancario
    print(f"\n🏦 SISTEMA BANCARIO:")
    credito_final = metricas['credito_total'][-1] if metricas['credito_total'] else 0
    depositos_final = metricas['depositos_totales'][-1] if metricas['depositos_totales'] else 0
    morosidad_promedio = sum(
        metricas['morosidad']) / len(metricas['morosidad']) if metricas['morosidad'] else 0

    print(f"   💳 Crédito Total: ${credito_final:,.2f}")
    print(f"   🏛️ Depósitos Totales: ${depositos_final:,.2f}")
    print(f"   ⚠️ Morosidad Promedio: {morosidad_promedio:.2%}")

    if credito_final > 0 and depositos_final > 0:
        ratio_credito_depositos = credito_final / depositos_final
        print(f"   📊 Ratio Crédito/Depósitos: {ratio_credito_depositos:.2f}")

    # Análisis sectorial
    print(f"\n🏭 ESTRUCTURA ECONÓMICA SECTORIAL:")
    pib_sectores = {
        'Primario': metricas['pib_primario'][-1] if metricas['pib_primario'] else 0,
        'Secundario': metricas['pib_secundario'][-1] if metricas['pib_secundario'] else 0,
        'Terciario': metricas['pib_terciario'][-1] if metricas['pib_terciario'] else 0
    }

    pib_total_sectores = sum(pib_sectores.values())
    if pib_total_sectores > 0:
        for sector, pib_sector in pib_sectores.items():
            participacion = pib_sector / pib_total_sectores * 100
            print(f"   {sector}: {participacion:.1f}% (${pib_sector:,.0f})")

    # Análisis psicológico
    print(f"\n🧠 ESTADO PSICOLÓGICO DEL MERCADO:")
    optimismo_promedio = sum(metricas['optimismo_promedio']) / len(
        metricas['optimismo_promedio']) if metricas['optimismo_promedio'] else 0
    estres_promedio = sum(metricas['estres_financiero']) / len(
        metricas['estres_financiero']) if metricas['estres_financiero'] else 0
    confianza_promedio = sum(metricas['confianza_consumidor']) / len(
        metricas['confianza_consumidor']) if metricas['confianza_consumidor'] else 0

    print(f"   😊 Optimismo Promedio: {optimismo_promedio:.2f}")
    print(f"   😰 Estrés Financiero: {estres_promedio:.2f}")
    print(f"   🤝 Confianza del Consumidor: {confianza_promedio:.2f}")

    # Análisis de innovación
    print(f"\n🔬 INNOVACIÓN Y TECNOLOGÍA:")
    inversion_id_total = metricas['inversion_id'][-1] if metricas['inversion_id'] else 0
    productos_innovadores = metricas['productos_innovadores'][-1] if metricas['productos_innovadores'] else 0
    tecnologias_disponibles = metricas['tecnologias_adoptadas'][-1] if metricas['tecnologias_adoptadas'] else 0

    print(f"   💰 Inversión I+D Total: ${inversion_id_total:,.2f}")
    print(f"   🆕 Productos Innovadores: {productos_innovadores}")
    print(f"   ⚙️ Tecnologías Disponibles: {tecnologias_disponibles}")

    if pib_final > 0:
        intensidad_id = inversion_id_total / pib_final * 100
        print(f"   📊 Intensidad I+D: {intensidad_id:.2f}% del PIB")

    # Análisis de competencia
    stats = mercado.obtener_estadisticas_completas()
    print("\n🏆 ANÁLISIS DE COMPETENCIA:")
    for bien, nivel in mercado.nivel_competencia.items():
        estado = "Alta" if nivel > 0.7 else "Media" if nivel > 0.4 else "Baja"
        print(f"   {bien}: {estado} competencia (índice: {nivel:.2f})")

    # Resumen ejecutivo
    print(f"\n📋 RESUMEN EJECUTIVO:")
    print(
        f"   🎯 La economía simulada muestra características de una economía {determinar_tipo_economia(pib_sectores, optimismo_promedio, inversion_id_total/pib_final if pib_final > 0 else 0)}")
    print(
        f"   📈 Tendencia general: {'Expansiva' if crecimiento_pib > 0 else 'Contractiva'}")
    print(
        f"   🏦 Sistema financiero: {'Estable' if morosidad_promedio < 0.1 else 'En riesgo'}")
    print(
        f"   🧠 Sentimiento del mercado: {'Positivo' if optimismo_promedio > 0.6 else 'Neutro' if optimismo_promedio > 0.4 else 'Negativo'}")


def determinar_tipo_economia(pib_sectores, optimismo, intensidad_id):
    """Determina el tipo de economía basado en indicadores"""
    total_pib = sum(pib_sectores.values())
    if total_pib == 0:
        return "en desarrollo inicial"

    participacion_terciario = pib_sectores['Terciario'] / total_pib
    participacion_secundario = pib_sectores['Secundario'] / total_pib

    if participacion_terciario > 0.6 and intensidad_id > 0.02:
        return "post-industrial innovadora"
    elif participacion_terciario > 0.5:
        return "de servicios desarrollada"
    elif participacion_secundario > 0.4:
        return "industrial en crecimiento"
    else:
        return "primario-exportadora"


def crear_visualizaciones_avanzadas(metricas):
    """Crea gráficos avanzados de análisis económico"""
    print("\n📊 Generando visualizaciones avanzadas...")

    # Configurar estilo
    plt.style.use('default')
    fig = plt.figure(figsize=(20, 16))

    # Layout de gráficos 3x4
    gs = fig.add_gridspec(4, 3, hspace=0.3, wspace=0.3)

    ciclos = range(len(metricas['pib']))

    # 1. PIB y crecimiento
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(ciclos, metricas['pib'], 'b-',
             linewidth=2, marker='o', markersize=3)
    ax1.set_title('📈 Evolución del PIB', fontweight='bold')
    ax1.set_ylabel('PIB ($)')
    ax1.grid(True, alpha=0.3)
    ax1.ticklabel_format(style='plain', axis='y')

    # 2. Inflación vs Desempleo (Curva de Phillips)
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.scatter([i*100 for i in metricas['inflacion']], [d*100 for d in metricas['desempleo']],
                alpha=0.6, c=range(len(ciclos)), cmap='viridis')
    ax2.set_title('📊 Curva de Phillips', fontweight='bold')
    ax2.set_xlabel('Inflación (%)')
    ax2.set_ylabel('Desempleo (%)')
    ax2.grid(True, alpha=0.3)

    # 3. Sistema bancario
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.plot(ciclos, metricas['credito_total'], 'g-',
             linewidth=2, label='Crédito Total')
    ax3.plot(ciclos, metricas['depositos_totales'],
             'orange', linewidth=2, label='Depósitos')
    ax3.set_title('🏦 Sistema Bancario', fontweight='bold')
    ax3.set_ylabel('Monto ($)')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    ax3.ticklabel_format(style='plain', axis='y')

    # 4. Estructura sectorial
    ax4 = fig.add_subplot(gs[1, 0])
    ax4.plot(ciclos, metricas['pib_primario'],
             'brown', linewidth=2, label='Primario')
    ax4.plot(ciclos, metricas['pib_secundario'],
             'gray', linewidth=2, label='Secundario')
    ax4.plot(ciclos, metricas['pib_terciario'],
             'purple', linewidth=2, label='Terciario')
    ax4.set_title('🏭 PIB Sectorial', fontweight='bold')
    ax4.set_ylabel('PIB Sectorial ($)')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    # 5. Psicología del mercado
    ax5 = fig.add_subplot(gs[1, 1])
    ax5.plot(ciclos, metricas['optimismo_promedio'],
             'green', linewidth=2, label='Optimismo')
    ax5.plot(ciclos, metricas['estres_financiero'],
             'red', linewidth=2, label='Estrés')
    ax5.plot(ciclos, metricas['confianza_consumidor'],
             'blue', linewidth=2, label='Confianza')
    ax5.set_title('🧠 Psicología Económica', fontweight='bold')
    ax5.set_ylabel('Índice (0-1)')
    ax5.legend()
    ax5.grid(True, alpha=0.3)

    # 6. Innovación
    ax6 = fig.add_subplot(gs[1, 2])
    ax6.bar(ciclos[::5], [metricas['inversion_id'][i] for i in range(0, len(ciclos), 5)],
            alpha=0.7, color='cyan', label='Inversión I+D')
    ax6_twin = ax6.twinx()
    ax6_twin.plot(ciclos, metricas['productos_innovadores'], 'red', linewidth=2, marker='s',
                  markersize=3, label='Productos Nuevos')
    ax6.set_title('🔬 Innovación', fontweight='bold')
    ax6.set_ylabel('Inversión I+D ($)')
    ax6_twin.set_ylabel('Productos Innovadores')
    ax6.grid(True, alpha=0.3)

    # 7. Distribución de riqueza
    ax7 = fig.add_subplot(gs[2, 0])
    ax7.plot(ciclos, metricas['dinero_consumidores'],
             'g-', linewidth=2, label='Consumidores')
    ax7.plot(ciclos, metricas['dinero_empresas'],
             'purple', linewidth=2, label='Empresas')
    ax7.set_title('💰 Distribución de Riqueza', fontweight='bold')
    ax7.set_ylabel('Dinero Promedio ($)')
    ax7.legend()
    ax7.grid(True, alpha=0.3)

    # 8. Morosidad bancaria
    ax8 = fig.add_subplot(gs[2, 1])
    ax8.plot(ciclos, [m*100 for m in metricas['morosidad']],
             'red', linewidth=2, marker='^', markersize=3)
    ax8.set_title('⚠️ Morosidad Bancaria', fontweight='bold')
    ax8.set_ylabel('Morosidad (%)')
    ax8.axhline(y=5, color='orange', linestyle='--',
                alpha=0.7, label='Umbral Alerta 5%')
    ax8.axhline(y=10, color='red', linestyle='--',
                alpha=0.7, label='Umbral Crisis 10%')
    ax8.legend()
    ax8.grid(True, alpha=0.3)

    # 9. Actividad económica total
    ax9 = fig.add_subplot(gs[2, 2])
    ax9.plot(ciclos, metricas['transacciones_totales'],
             'teal', linewidth=2, marker='d', markersize=3)
    ax9.set_title('📊 Actividad Económica', fontweight='bold')
    ax9.set_ylabel('Transacciones por Ciclo')
    ax9.grid(True, alpha=0.3)

    # 10. Análisis de correlación PIB vs Factores
    ax10 = fig.add_subplot(gs[3, :])

    # Normalizar datos para comparación
    pib_norm = np.array(metricas['pib'])
    pib_norm = (pib_norm - np.min(pib_norm)) / (np.max(pib_norm) -
                                                np.min(pib_norm)) if np.max(pib_norm) > np.min(pib_norm) else pib_norm

    confianza_norm = np.array(metricas['confianza_consumidor'])
    credito_norm = np.array(metricas['credito_total'])
    credito_norm = (credito_norm - np.min(credito_norm)) / (np.max(credito_norm) -
                                                            np.min(credito_norm)) if np.max(credito_norm) > np.min(credito_norm) else credito_norm

    ax10.plot(ciclos, pib_norm, 'blue', linewidth=3, label='PIB (normalizado)')
    ax10.plot(ciclos, confianza_norm, 'green',
              linewidth=2, label='Confianza Consumidor')
    ax10.plot(ciclos, credito_norm, 'orange',
              linewidth=2, label='Crédito (normalizado)')
    ax10.set_title('🔗 Correlaciones Macroeconómicas',
                   fontweight='bold', size=14)
    ax10.set_xlabel('Ciclos')
    ax10.set_ylabel('Valores Normalizados (0-1)')
    ax10.legend()
    ax10.grid(True, alpha=0.3)

    plt.suptitle('ANÁLISIS ECONÓMICO AVANZADO - SIMULACIÓN MULTISISTEMA',
                 fontsize=18, fontweight='bold')

    # Guardar gráfico
    filename = f'economia_avanzada_{time.time():.0f}.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"   📊 Gráfico guardado como {filename}")
    plt.show()

    print("   ✅ Visualizaciones avanzadas generadas correctamente")


def main():
    """Función principal de la simulación avanzada"""
    print("🌟 SIMULADOR ECONÓMICO AVANZADO - VERSIÓN MULTISISTEMA 🌟")
    print("=" * 80)
    print("📋 Sistemas integrados:")
    print("   🏦 Sistema bancario con crédito y política monetaria")
    print("   🏭 Sectores económicos diferenciados (primario, secundario, terciario)")
    print("   🧠 Psicología económica con sesgos cognitivos")
    print("   🔬 Sistema de innovación y desarrollo tecnológico")
    print("   📊 Análisis macroeconómico avanzado")
    print()

    # 1. Crear bienes avanzados
    bienes = crear_bienes_avanzados()
    print(
        f"✅ Creados {len(bienes)} tipos de bienes con características económicas realistas")

    # 2. Inicializar mercado
    mercado = Mercado(bienes)
    print("✅ Mercado inicializado con sistemas avanzados integrados")

    # 3. Configurar economía avanzada
    configurar_economia_avanzada(mercado)

    # 4. Ejecutar simulación avanzada
    num_ciclos = 50  # Simulación para observar efectos de largo plazo
    metricas = ejecutar_simulacion_avanzada(mercado, num_ciclos)

    # 5. Análisis avanzado
    generar_analisis_avanzado(mercado, metricas)

    # 6. Crear visualizaciones avanzadas
    crear_visualizaciones_avanzadas(metricas)

    # 7. Estadísticas finales detalladas
    print("\n📋 ESTADÍSTICAS FINALES DETALLADAS:")
    print("-" * 50)
    stats = mercado.obtener_estadisticas_completas()

    print(f"🔄 Ciclos simulados: {num_ciclos}")
    print(f"👥 Agentes económicos totales: {len(mercado.personas)}")
    print(f"🏪 Bienes en el mercado: {len(bienes)}")
    print(f"📊 Transacciones registradas: {len(mercado.transacciones):,}")
    print(
        f"🏦 Sistema bancario: {stats['sistema_bancario']['bancos_operando']} bancos activos")
    print(
        f"🏭 Sectores económicos: {len(stats['sectores_economicos'])} sectores diferenciados")
    print(
        f"🔬 Tecnologías disponibles: {stats['innovacion']['tecnologias_disponibles']}")

    if 'psicologia_economica' in stats:
        print(
            f"🧠 Estado psicológico promedio: Optimismo {stats['psicologia_economica']['optimismo_promedio']:.2f}")

    print(f"🏛️ Reservas gubernamentales: ${mercado.gobierno.presupuesto:,.2f}")
    print(
        f"📈 Tasa de interés actual: {mercado.gobierno.tasa_interes_referencia:.2%}")

    print("\n🎉 ¡Simulación económica avanzada completada exitosamente!")
    print("    Los resultados muestran un ecosistema económico multisistema")
    print("    con interacciones complejas entre agentes, psicología, sectores,")
    print("    sistema financiero e innovación tecnológica.")


if __name__ == "__main__":
    main()
