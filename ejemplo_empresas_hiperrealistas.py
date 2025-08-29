"""
Ejemplo de Empresas Hiperrealistas
=================================

Demuestra las nuevas funcionalidades empresariales realistas:
- Gestión de recursos humanos avanzada
- Análisis de competencia
- Gestión de riesgos y problemas operacionales
- Innovación y desarrollo
- Responsabilidad social corporativa
- Planes estratégicos
- Crisis empresariales
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.models.EmpresaHiperrealista import EmpresaHiperrealista
from src.models.Mercado import Mercado
from src.models.Bien import Bien
from src.models.Consumidor import Consumidor
from src.config.ConfigEconomica import ConfigEconomica
import logging

# Configurar logging para ver las actividades empresariales
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('empresa_hiperrealista_demo.log')
    ]
)

def crear_mercado_demo():
    """Crea un mercado de demostración con bienes variados"""
    print("🏭 Creando mercado de demostración...")
    
    # Crear mercado
    mercado = Mercado()
    
    # Definir bienes diversos para diferentes sectores
    bienes_config = {
        'pan': {'precio_base': 3.5, 'categoria': 'alimentos_basicos'},
        'leche': {'precio_base': 2.8, 'categoria': 'alimentos_basicos'},
        'carne': {'precio_base': 15.0, 'categoria': 'alimentos_lujo'},
        'electronica': {'precio_base': 250.0, 'categoria': 'tecnologia'},
        'ropa': {'precio_base': 45.0, 'categoria': 'textil'},
        'cemento': {'precio_base': 80.0, 'categoria': 'construccion'},
        'servicios_consultoria': {'precio_base': 120.0, 'categoria': 'servicios'},
        'medicamentos': {'precio_base': 35.0, 'categoria': 'salud'}
    }
    
    # Crear bienes
    for nombre, config in bienes_config.items():
        bien = Bien(
            nombre=nombre, 
            categoria=config['categoria'],
            precio_base=config['precio_base']
        )
        mercado.agregar_bien(bien)
    
    # Crear consumidores
    for i in range(30):
        consumidor = Consumidor(mercado=mercado)
        consumidor.dinero = ConfigEconomica.DINERO_INICIAL_CONSUMIDOR_MAX
        consumidor.ingreso_mensual = 3000 + (i * 100)  # Ingresos variados
        mercado.agregar_persona(consumidor)
    
    print(f"✅ Mercado creado con {len(mercado.bienes)} bienes y {len(mercado.getConsumidores())} consumidores")
    return mercado

def crear_empresas_hiperrealistas(mercado):
    """Crea empresas hiperrealistas de diferentes sectores"""
    print("\n🏢 Creando empresas hiperrealistas...")
    
    empresas = []
    
    # Empresa de alimentos (sector tradicional)
    empresa_alimentos = EmpresaHiperrealista(
        nombre="AlimentosCorp",
        mercado=mercado,
        bienes=['pan', 'leche', 'carne']
    )
    empresa_alimentos.dinero = 150000  # Capital sustancial
    empresas.append(empresa_alimentos)
    
    # Empresa de tecnología (sector innovador)
    empresa_tech = EmpresaHiperrealista(
        nombre="TechSolutions",
        mercado=mercado,
        bienes=['electronica', 'servicios_consultoria']
    )
    empresa_tech.dinero = 200000  # Más capital para I+D
    empresas.append(empresa_tech)
    
    # Empresa textil (sector competitivo)
    empresa_textil = EmpresaHiperrealista(
        nombre="ModaIndustrial",
        mercado=mercado,
        bienes=['ropa']
    )
    empresa_textil.dinero = 100000
    empresas.append(empresa_textil)
    
    # Empresa de construcción (sector cíclico)
    empresa_construccion = EmpresaHiperrealista(
        nombre="ConstruyeFacil",
        mercado=mercado,
        bienes=['cemento']
    )
    empresa_construccion.dinero = 180000
    empresas.append(empresa_construccion)
    
    # Empresa farmacéutica (sector regulado)
    empresa_pharma = EmpresaHiperrealista(
        nombre="FarmaSalud",
        mercado=mercado,
        bienes=['medicamentos']
    )
    empresa_pharma.dinero = 250000  # Sector con altos márgenes
    empresas.append(empresa_pharma)
    
    # Agregar todas las empresas al mercado
    for empresa in empresas:
        mercado.agregar_persona(empresa)
        
        # Contratar empleados iniciales
        consumidores_disponibles = [c for c in mercado.getConsumidores() if not c.empleado]
        empleados_a_contratar = min(8, len(consumidores_disponibles))
        
        for i in range(empleados_a_contratar):
            if consumidores_disponibles:
                consumidor = consumidores_disponibles.pop(0)
                empresa.contratar(consumidor)
    
    print(f"✅ Creadas {len(empresas)} empresas hiperrealistas")
    for empresa in empresas:
        print(f"   • {empresa.nombre} [{empresa.sector_principal}] - ${empresa.dinero:,.0f} - {len(empresa.empleados)} empleados")
    
    return empresas

def simular_ciclos_empresariales(mercado, empresas, num_ciclos=12):
    """Simula ciclos empresariales con análisis detallado"""
    print(f"\n🔄 Iniciando simulación de {num_ciclos} ciclos empresariales...")
    
    resultados_simulacion = {
        'empresas': {},
        'eventos_importantes': [],
        'metricas_por_ciclo': []
    }
    
    # Inicializar datos de seguimiento
    for empresa in empresas:
        resultados_simulacion['empresas'][empresa.nombre] = {
            'capital_inicial': empresa.dinero,
            'empleados_inicial': len(empresa.empleados),
            'performance_historica': [],
            'problemas_enfrentados': [],
            'decisiones_estrategicas': []
        }
    
    for ciclo in range(1, num_ciclos + 1):
        print(f"\n--- CICLO {ciclo} ---")
        
        metricas_ciclo = {
            'ciclo': ciclo,
            'empresas_activas': 0,
            'empleos_totales': 0,
            'capital_total': 0,
            'proyectos_id': 0,
            'problemas_criticos': 0
        }
        
        # Ejecutar ciclo para cada empresa
        for empresa in empresas[:]:  # Copia de la lista por si alguna empresa sale
            try:
                resultado_ciclo = empresa.ciclo_empresa_hiperrealista(ciclo, mercado)
                
                if resultado_ciclo:
                    metricas_ciclo['empresas_activas'] += 1
                    metricas_ciclo['empleos_totales'] += len(empresa.empleados)
                    metricas_ciclo['capital_total'] += empresa.dinero
                    
                    # Contar proyectos I+D
                    proyectos_id = len(empresa.gestion_avanzada.gestion_innovacion.proyectos_activos)
                    metricas_ciclo['proyectos_id'] += proyectos_id
                    
                    # Contar problemas críticos
                    problemas_criticos = len([p for p in empresa.gestor_problemas.problemas_activos.values() 
                                            if p.severidad == 'critico'])
                    metricas_ciclo['problemas_criticos'] += problemas_criticos
                    
                    # Análisis de performance cada 3 ciclos
                    if ciclo % 3 == 0:
                        performance = empresa.analizar_performance_empresarial()
                        resultados_simulacion['empresas'][empresa.nombre]['performance_historica'].append({
                            'ciclo': ciclo,
                            'calificacion': performance['calificacion_general'],
                            'salud_financiera': performance['salud_financiera']['score'],
                            'competitividad': performance['posicion_competitiva']['score']
                        })
                        
                        # Eventos importantes
                        if performance['calificacion_general'] < 40:
                            evento = f"CRISIS: {empresa.nombre} en dificultades (Score: {performance['calificacion_general']:.1f})"
                            resultados_simulacion['eventos_importantes'].append((ciclo, evento))
                            print(f"⚠️  {evento}")
                        
                        elif performance['calificacion_general'] > 85:
                            evento = f"EXITO: {empresa.nombre} excelente performance (Score: {performance['calificacion_general']:.1f})"
                            resultados_simulacion['eventos_importantes'].append((ciclo, evento))
                            print(f"🎉 {evento}")
                    
                    # Registrar problemas importantes
                    reporte_problemas = empresa.gestor_problemas.generar_reporte_problemas()
                    if reporte_problemas['problemas_criticos'] > 0:
                        evento = f"PROBLEMA: {empresa.nombre} enfrenta {reporte_problemas['problemas_criticos']} problemas críticos"
                        resultados_simulacion['eventos_importantes'].append((ciclo, evento))
                        print(f"🚨 {evento}")
                
                else:
                    # Empresa en quiebra o problemas graves
                    evento = f"QUIEBRA: {empresa.nombre} cesó operaciones"
                    resultados_simulacion['eventos_importantes'].append((ciclo, evento))
                    print(f"💀 {evento}")
                    empresas.remove(empresa)
            
            except Exception as e:
                print(f"❌ Error en {empresa.nombre}: {e}")
                logging.error(f"Error en ciclo {ciclo} para {empresa.nombre}: {e}")
        
        # Ejecutar ciclo del mercado
        mercado.ciclo_mercado()
        
        # Registrar métricas del ciclo
        resultados_simulacion['metricas_por_ciclo'].append(metricas_ciclo)
        
        # Resumen del ciclo
        print(f"📊 Resumen Ciclo {ciclo}:")
        print(f"   • Empresas activas: {metricas_ciclo['empresas_activas']}")
        print(f"   • Empleos totales: {metricas_ciclo['empleos_totales']}")
        print(f"   • Capital total: ${metricas_ciclo['capital_total']:,.0f}")
        print(f"   • Proyectos I+D: {metricas_ciclo['proyectos_id']}")
        print(f"   • Problemas críticos: {metricas_ciclo['problemas_criticos']}")
    
    return resultados_simulacion

def generar_reporte_final(empresas, resultados_simulacion):
    """Genera un reporte final detallado de la simulación"""
    print("\n" + "="*60)
    print("📋 REPORTE FINAL DE SIMULACIÓN EMPRESARIAL")
    print("="*60)
    
    # Resumen general
    print(f"\n🏢 EMPRESAS SUPERVIVIENTES: {len(empresas)}")
    for empresa in empresas:
        reporte = empresa.obtener_reporte_empresarial_completo()
        
        print(f"\n▶️  {empresa.nombre.upper()}")
        print(f"   Sector: {reporte['informacion_general']['sector']}")
        print(f"   Tamaño: {reporte['informacion_general']['tamaño']}")
        print(f"   Capital Final: ${reporte['situacion_financiera']['capital_actual']:,.0f}")
        print(f"   Empleados: {reporte['recursos_humanos']['total']}")
        print(f"   Performance General: {reporte['performance_integral']['calificacion_general']:.1f}/100")
        
        # Situación financiera
        salud_fin = reporte['situacion_financiera']['evaluacion']
        print(f"   💰 Salud Financiera: {salud_fin['estado'].upper()} ({salud_fin['score']:.1f}/100)")
        print(f"      - Liquidez: {salud_fin['liquidez_meses']:.1f} meses")
        print(f"      - Solvencia: {salud_fin['solvencia_ratio']:.2f}")
        
        # Innovación
        innovacion = reporte['innovacion_desarrollo']
        print(f"   🔬 Innovación:")
        print(f"      - Proyectos activos: {innovacion['proyectos_activos']}")
        print(f"      - Proyectos completados: {innovacion['proyectos_completados']}")
        print(f"      - Inversión I+D: ${innovacion['inversion_total']:,.0f}")
        
        # Recursos humanos
        rrhh = reporte['recursos_humanos']
        print(f"   👥 Recursos Humanos:")
        print(f"      - Productividad promedio: {rrhh['productividad_promedio']:.2f}")
        print(f"      - Satisfacción: {rrhh['satisfaccion_promedio']:.2f}")
        
        # Responsabilidad social
        rsc = reporte['responsabilidad_social']
        print(f"   🌱 Responsabilidad Social:")
        print(f"      - Reputación: {rsc['reputacion']:.2f}")
        print(f"      - Programas activos: {rsc['programas_activos']}")
        print(f"      - Certificaciones: {len(rsc['certificaciones'])}")
        
        # Gestión de riesgos
        riesgos = reporte['gestion_riesgos']
        print(f"   ⚠️  Gestión de Riesgos:")
        print(f"      - Riesgos identificados: {riesgos['riesgos_identificados']}")
        
        # Logros históricos
        logros = reporte['logros_historicos']
        print(f"   🏆 Logros:")
        print(f"      - Decisiones estratégicas: {logros['decisiones_estrategicas']}")
        print(f"      - Crisis superadas: {logros['crisis_superadas']}")
        print(f"      - Proyectos completados: {logros['proyectos_completados']}")
        
        # Top recomendaciones
        recomendaciones = reporte['performance_integral']['recomendaciones'][:3]
        if recomendaciones:
            print(f"   💡 Principales Recomendaciones:")
            for i, rec in enumerate(recomendaciones, 1):
                print(f"      {i}. {rec}")
    
    # Eventos más importantes
    print(f"\n📈 EVENTOS MÁS IMPORTANTES:")
    eventos_importantes = resultados_simulacion['eventos_importantes']
    for ciclo, evento in eventos_importantes[-10:]:  # Últimos 10 eventos
        print(f"   Ciclo {ciclo}: {evento}")
    
    # Análisis de tendencias
    print(f"\n📊 ANÁLISIS DE TENDENCIAS:")
    metricas = resultados_simulacion['metricas_por_ciclo']
    if len(metricas) > 3:
        capital_inicial = metricas[0]['capital_total']
        capital_final = metricas[-1]['capital_total']
        empleos_inicial = metricas[0]['empleos_totales']
        empleos_final = metricas[-1]['empleos_totales']
        
        crecimiento_capital = ((capital_final - capital_inicial) / capital_inicial * 100) if capital_inicial > 0 else 0
        crecimiento_empleos = ((empleos_final - empleos_inicial) / empleos_inicial * 100) if empleos_inicial > 0 else 0
        
        print(f"   • Crecimiento de capital: {crecimiento_capital:+.1f}%")
        print(f"   • Crecimiento de empleos: {crecimiento_empleos:+.1f}%")
        print(f"   • Proyectos I+D promedio: {sum(m['proyectos_id'] for m in metricas) / len(metricas):.1f}")
        print(f"   • Problemas críticos promedio: {sum(m['problemas_criticos'] for m in metricas) / len(metricas):.1f}")
    
    print("\n✅ SIMULACIÓN COMPLETADA CON ÉXITO")
    print("="*60)

def demostrar_funcionalidades_especificas(empresas):
    """Demuestra funcionalidades específicas de las empresas hiperrealistas"""
    print("\n" + "="*50)
    print("🎯 DEMOSTRACIÓN DE FUNCIONALIDADES ESPECÍFICAS")
    print("="*50)
    
    empresa_demo = empresas[0]  # Usar la primera empresa para demos
    
    # 1. Plan estratégico
    print(f"\n1️⃣  PLAN ESTRATÉGICO - {empresa_demo.nombre}")
    plan_resultado = empresa_demo.ejecutar_plan_estrategico(empresa_demo.mercado)
    print(f"   ✅ Objetivos cumplidos: {plan_resultado['objetivos_cumplidos']}")
    print(f"   💰 Inversión estratégica: ${plan_resultado['inversion_estrategica']:,.0f}")
    print(f"   🚀 Nuevas iniciativas: {len(plan_resultado['nuevas_iniciativas'])}")
    for iniciativa in plan_resultado['nuevas_iniciativas'][:3]:
        print(f"      • {iniciativa}")
    
    # 2. Gestión de crisis
    print(f"\n2️⃣  GESTIÓN DE CRISIS - {empresa_demo.nombre}")
    crisis_resultado = empresa_demo.gestionar_crisis_empresarial('financiera')
    print(f"   📊 Crisis resuelta: {'✅ SÍ' if crisis_resultado['exito'] else '❌ NO'}")
    print(f"   💸 Costo total: ${crisis_resultado.get('costo', 0):,.0f}")
    print(f"   📋 Acciones tomadas: {len(crisis_resultado.get('acciones', []))}")
    for accion in crisis_resultado.get('acciones', [])[:3]:
        print(f"      • {accion}")
    
    # 3. Análisis de performance
    print(f"\n3️⃣  ANÁLISIS DE PERFORMANCE - {empresa_demo.nombre}")
    performance = empresa_demo.analizar_performance_empresarial()
    print(f"   🎯 Calificación general: {performance['calificacion_general']:.1f}/100")
    
    areas = ['salud_financiera', 'posicion_competitiva', 'eficiencia_operacional', 
             'innovacion_y_crecimiento', 'responsabilidad_social']
    for area in areas:
        if area in performance:
            score = performance[area]['score']
            estado = performance[area].get('estado', performance[area].get('posicion', 'N/A'))
            print(f"      • {area.replace('_', ' ').title()}: {score:.1f}/100 ({estado})")
    
    # 4. Reporte de problemas empresariales
    print(f"\n4️⃣  PROBLEMAS EMPRESARIALES - {empresa_demo.nombre}")
    reporte_problemas = empresa_demo.gestor_problemas.generar_reporte_problemas()
    print(f"   🚨 Problemas activos: {reporte_problemas['problemas_activos']}")
    print(f"   ⚠️  Problemas críticos: {reporte_problemas['problemas_criticos']}")
    print(f"   💰 Costo resolución: ${reporte_problemas['costo_resolucion_estimado']:,.0f}")
    print(f"   ⏰ Requieren atención inmediata: {reporte_problemas['requieren_atencion_inmediata']}")
    
    if reporte_problemas['problema_mas_critico']:
        print(f"   🔥 Problema más crítico: {reporte_problemas['problema_mas_critico']}")
    
    # 5. Recomendaciones de gestión
    recomendaciones = empresa_demo.gestor_problemas.obtener_recomendaciones_gestion()
    if recomendaciones:
        print(f"   💡 Recomendaciones:")
        for rec in recomendaciones[:3]:
            print(f"      • {rec}")

def main():
    """Función principal del ejemplo"""
    print("🎬 INICIANDO DEMO DE EMPRESAS HIPERREALISTAS")
    print("=" * 60)
    
    try:
        # 1. Crear mercado
        mercado = crear_mercado_demo()
        
        # 2. Crear empresas hiperrealistas
        empresas = crear_empresas_hiperrealistas(mercado)
        
        # 3. Demostrar funcionalidades específicas
        demostrar_funcionalidades_especificas(empresas)
        
        # 4. Simular ciclos empresariales
        resultados = simular_ciclos_empresariales(mercado, empresas, num_ciclos=12)
        
        # 5. Generar reporte final
        generar_reporte_final(empresas, resultados)
        
        print(f"\n📄 Log detallado guardado en: empresa_hiperrealista_demo.log")
        
    except Exception as e:
        print(f"❌ Error en la simulación: {e}")
        logging.error(f"Error en simulación principal: {e}")
        raise

if __name__ == "__main__":
    main()
