"""
SIMULADOR ECONÓMICO AVANZADO v2.1 - INTEGRACIÓN COMPLETA
========================================================

Simulación económica realista con todas las mejoras implementadas:
- ✅ Sistema ML con datos sintéticos garantizados
- ✅ Sistema de precios dinámicos 
- ✅ Configuración externa via JSON
- ✅ Dashboard avanzado con múltiples métricas
- ✅ Sistema de crisis mejorado
- ✅ Tests automatizados
- ✅ Mercado laboral activado
- ✅ Sistema bancario completamente funcional

Autor: Simulador Económico Team
Versión: 2.1 - Mejoras Críticas Implementadas
"""

from src.config.ConfiguradorSimulacion import ConfiguradorSimulacion
from src.systems.PreciosDinamicos import integrar_sistema_precios_dinamicos, actualizar_precios_mercado
from src.systems.VisualizacionAvanzada import DashboardEconomico, VisualizadorTiempoReal, exportar_resultados_completos
from src.systems.EstimuloEconomico import detectar_estancamiento_economico, aplicar_estimulo_emergencia
from src.systems.CrisisFinanciera import evaluar_recuperacion_crisis, aplicar_medidas_recuperacion
from src.systems.MercadoLaboral import MercadoLaboral
from src.systems.AnalyticsML import SistemaAnalyticsML
from src.systems.SistemaBancario import SistemaBancario, Banco
from src.models.Gobierno import Gobierno
from src.models.EmpresaProductora import EmpresaProductora
from src.models.Empresa import Empresa
from src.models.Consumidor import Consumidor
from src.models.Bien import Bien
from src.models.Mercado import Mercado
import sys
import os
import time
import random
import matplotlib.pyplot as plt

# Añadir src al path de Python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Importaciones principales

# Sistemas avanzados

# Configuración


def crear_bienes_expandidos():
    """Crea catálogo expandido de 45+ bienes en múltiples categorías"""
    bienes = {}

    print("📦 Creando catálogo expandido de bienes...")

    # ALIMENTOS BÁSICOS (10 bienes)
    alimentos_basicos = [
        'Arroz', 'Papa', 'Pan', 'Leche', 'Sal', 'Aceite', 'Azucar',
        'Agua', 'Harina', 'Frijoles'
    ]
    for nombre in alimentos_basicos:
        bienes[nombre] = Bien(nombre, 'alimentos_basicos')

    # ALIMENTOS DE LUJO (10 bienes)
    alimentos_lujo = [
        'Carne', 'Pollo', 'Huevos', 'Cafe', 'Pescado', 'Queso',
        'Chocolate', 'Vino', 'Frutas', 'Verduras'
    ]
    for nombre in alimentos_lujo:
        bienes[nombre] = Bien(nombre, 'alimentos_lujo')

    # BIENES MANUFACTURADOS (8 bienes)
    manufacturados = [
        'Ropa', 'Calzado', 'Muebles', 'Electrodomesticos',
        'Libros', 'Herramientas', 'Juguetes', 'Medicinas'
    ]
    for nombre in manufacturados:
        bienes[nombre] = Bien(nombre, 'bienes_duraderos')

    # TECNOLOGÍA (7 bienes)
    tecnologia = [
        'Computadora', 'Telefono', 'Television', 'Internet',
        'Software', 'Videojuegos', 'Electronica'
    ]
    for nombre in tecnologia:
        bienes[nombre] = Bien(nombre, 'tecnologia')

    # SERVICIOS BÁSICOS (8 bienes)
    servicios = [
        'Transporte', 'Educacion', 'Salud', 'Vivienda',
        'Electricidad', 'Gas', 'Seguridad', 'Comunicaciones'
    ]
    for nombre in servicios:
        bienes[nombre] = Bien(nombre, 'servicios')

    # SERVICIOS DE LUJO (6 bienes)
    servicios_lujo = [
        'Entretenimiento', 'Turismo', 'Restaurante',
        'Gimnasio', 'Spa', 'Arte'
    ]
    for nombre in servicios_lujo:
        bienes[nombre] = Bien(nombre, 'servicios_lujo')

    # BIENES DE CAPITAL E INTERMEDIOS (6 bienes)
    capital_intermedio = [
        ('Maquinaria', 'capital'),
        ('Materias_Primas', 'intermedio'),
        ('Energia', 'intermedio'),
        ('Acero', 'intermedio'),
        ('Cemento', 'intermedio'),
        ('Combustible', 'intermedio')
    ]
    for nombre, categoria in capital_intermedio:
        bienes[nombre] = Bien(nombre, categoria)

    print(
        f"✅ Catálogo creado: {len(bienes)} bienes en {len(set(b.categoria for b in bienes.values()))} categorías")
    return bienes


def configurar_economia_avanzada(mercado, config):
    """Configura la economía con parámetros del archivo de configuración"""
    print("🏗️ Configurando economía avanzada...")

    # Obtener configuración
    sim_config = config.obtener_seccion('simulacion')
    eco_config = config.obtener_seccion('economia')
    banco_config = config.obtener_seccion('sistema_bancario')

    # === CONSUMIDORES ===
    num_consumidores = sim_config.get('num_consumidores', 250)
    dinero_config = eco_config.get('dinero_inicial_consumidores', {
                                   'min': 5000, 'max': 15000})

    print(f"👥 Creando {num_consumidores} consumidores...")
    for i in range(num_consumidores):
        consumidor = Consumidor(f'Consumidor_{i+1}', mercado)
        # Dinero inicial aleatorio en el rango configurado
        consumidor.dinero = random.uniform(
            dinero_config['min'], dinero_config['max'])
        consumidor.ingreso_mensual = random.uniform(2000, 8000)
        mercado.agregar_persona(consumidor)

    # === EMPRESAS PRODUCTORAS ===
    num_empresas_prod = sim_config.get('num_empresas_productoras', 5)
    capital_config = eco_config.get('capital_inicial_empresas', {
                                    'min': 100000, 'max': 1500000})

    print(f"🏭 Creando {num_empresas_prod} empresas productoras...")
    empresas = []
    for i in range(num_empresas_prod):
        empresa = EmpresaProductora(f'Productora_{i+1}', mercado)
        empresa.dinero = random.uniform(
            capital_config['min'], capital_config['max'])
        mercado.agregar_persona(empresa)
        empresas.append(empresa)

    # === EMPRESAS COMERCIALES ===
    num_empresas_com = sim_config.get('num_empresas_comerciales', 8)

    print(f"🏢 Creando {num_empresas_com} empresas comerciales...")
    for i in range(num_empresas_com):
        # Seleccionar algunos bienes aleatorios para vender
        bienes_empresa = random.sample(list(mercado.bienes.keys()),
                                       random.randint(3, 8))
        bienes_dict = {bien: [] for bien in bienes_empresa}

        empresa = Empresa.crear_con_acciones(
            f'Comercial_{i+1}', mercado, 1000, bienes_dict
        )
        empresa.dinero = random.uniform(50000, 300000)
        mercado.agregar_persona(empresa)
        empresas.append(empresa)

    # === SISTEMA BANCARIO ===
    if banco_config.get('activar', True):
        print("🏦 Configurando sistema bancario...")
        mercado.sistema_bancario = SistemaBancario()

        num_bancos = banco_config.get('num_bancos', 3)
        capital_bancos = banco_config.get('capital_inicial_bancos', 3000000)

        for i in range(num_bancos):
            banco = Banco(f'Banco_{i+1}', capital_bancos)
            banco.tasa_base_prestamos = banco_config.get(
                'tasa_interes_base', 0.05)
            mercado.sistema_bancario.agregar_banco(banco)

        print(
            f"✅ {num_bancos} bancos creados con capital total ${num_bancos * capital_bancos:,}")

    # === GOBIERNO ===
    print("🏛️ Configurando gobierno...")
    mercado.gobierno = Gobierno(mercado)
    mercado.gobierno.presupuesto = eco_config.get(
        'pib_inicial', 100000) * 0.3  # 30% del PIB inicial

    # === CONTRATACIONES INICIALES ===
    print("👔 Ejecutando contrataciones iniciales...")
    tasa_empleo_objetivo = 1 - eco_config.get('tasa_desempleo_inicial', 0.15)
    empleos_objetivo = int(num_consumidores * tasa_empleo_objetivo)

    consumidores_desempleados = [
        c for c in mercado.getConsumidores() if not c.empleado]
    empleos_creados = 0

    for empresa in empresas:
        if empleos_creados >= empleos_objetivo:
            break

        # Cada empresa contrata entre 5-20 empleados
        contrataciones_empresa = min(
            random.randint(5, 20),
            len(consumidores_desempleados),
            empleos_objetivo - empleos_creados
        )

        for _ in range(contrataciones_empresa):
            if consumidores_desempleados:
                trabajador = consumidores_desempleados.pop(0)
                if empresa.contratar(trabajador):
                    empleos_creados += 1

    tasa_desempleo_real = (
        len(consumidores_desempleados) / num_consumidores) * 100
    print(f"✅ Tasa de desempleo inicial: {tasa_desempleo_real:.1f}%")

    return empresas


def integrar_sistemas_avanzados(mercado, config):
    """Integra todos los sistemas avanzados"""
    print("🔗 Integrando sistemas avanzados...")

    # === MACHINE LEARNING ===
    ml_config = config.obtener_seccion('machine_learning')
    if ml_config.get('activar', True):
        print("🤖 Activando sistema de Machine Learning...")
        mercado.analytics_ml = SistemaAnalyticsML(mercado)

        # Entrenar modelos iniciales con datos sintéticos
        print("📊 Entrenando modelos ML iniciales...")
        modelos_entrenados = 0
        # Entrenar primeros 10 bienes
        for bien_nombre in list(mercado.bienes.keys())[:10]:
            if mercado.analytics_ml.predictor_demanda.get(bien_nombre) is None:
                from src.systems.AnalyticsML import PredictorDemanda
                mercado.analytics_ml.predictor_demanda[bien_nombre] = PredictorDemanda(
                )

            if mercado.analytics_ml.predictor_demanda[bien_nombre].entrenar(mercado, bien_nombre):
                modelos_entrenados += 1

        print(f"✅ {modelos_entrenados} modelos ML entrenados exitosamente")

    # === MERCADO LABORAL ===
    print("👷 Activando mercado laboral avanzado...")
    mercado.mercado_laboral = MercadoLaboral(mercado)

    # Asignar perfiles de habilidades a consumidores
    for consumidor in mercado.getConsumidores():
        if not hasattr(consumidor, 'perfil_habilidades'):
            consumidor.perfil_habilidades = mercado.mercado_laboral.crear_perfil()
            # 50% probabilidad de afiliación sindical
            mercado.mercado_laboral.asignar_sindicato(consumidor)

    # === SISTEMA DE PRECIOS DINÁMICOS ===
    print("💰 Configurando sistema de precios dinámicos...")
    sistema_precios = integrar_sistema_precios_dinamicos(mercado)

    # Asignar precios iniciales a todas las empresas
    precios_asignados = 0
    for empresa in mercado.getEmpresas():
        if hasattr(empresa, 'bienes') and empresa.bienes:
            for bien_nombre in empresa.bienes.keys():
                if bien_nombre in mercado.bienes:
                    precio_base = sistema_precios.precios_base.get(
                        bien_nombre, 10)
                    empresa.precios[bien_nombre] = precio_base * \
                        random.uniform(0.8, 1.2)
                    precios_asignados += 1

    print(f"✅ {precios_asignados} precios dinámicos asignados")

    # === DASHBOARD ===
    print("📊 Configurando dashboard avanzado...")
    mercado.dashboard = DashboardEconomico(mercado)

    print("✅ Todos los sistemas avanzados integrados")


def ejecutar_simulacion_completa(config):
    """Ejecuta la simulación completa con todas las mejoras"""
    print("🚀 INICIANDO SIMULACIÓN ECONÓMICA AVANZADA v2.1")
    print("=" * 60)

    tiempo_inicio = time.time()

    # === CONFIGURACIÓN INICIAL ===
    # Crear bienes expandidos primero
    bienes = crear_bienes_expandidos()

    # Crear mercado con bienes
    mercado = Mercado(bienes)

    # Configurar economía
    empresas = configurar_economia_avanzada(mercado, config)

    # Integrar sistemas avanzados
    integrar_sistemas_avanzados(mercado, config)

    # === CONFIGURACIÓN DE SIMULACIÓN ===
    sim_config = config.obtener_seccion('simulacion')
    num_ciclos = sim_config.get('num_ciclos', 50)
    frecuencia_reportes = sim_config.get('frecuencia_reportes', 5)

    # Visualizador en tiempo real (opcional)
    usar_tiempo_real = False  # Cambiar a True para gráficos en tiempo real
    if usar_tiempo_real:
        visualizador_tiempo_real = VisualizadorTiempoReal()

    print(f"🔄 Ejecutando {num_ciclos} ciclos económicos...")
    print("=" * 60)

    # === EJECUCIÓN PRINCIPAL ===
    for ciclo in range(1, num_ciclos + 1):
        # Actualizar dashboard antes del ciclo
        mercado.dashboard.actualizar_metricas(ciclo)

        # === SISTEMAS AUTOMÁTICOS ===

        # 1. Verificar crisis financiera
        if mercado.crisis_financiera_activa:
            if evaluar_recuperacion_crisis(mercado):
                print(
                    f"📈 Ciclo {ciclo}: Crisis financiera resuelta - Economía recuperándose")
                mercado.crisis_financiera_activa = False
                mercado.ciclos_en_crisis = 0
            else:
                aplicar_medidas_recuperacion(mercado)
                mercado.ciclos_en_crisis = getattr(
                    mercado, 'ciclos_en_crisis', 0) + 1

        # 2. Detectar estancamiento económico
        if detectar_estancamiento_economico(mercado):
            aplicar_estimulo_emergencia(mercado)

        # 3. Mercado laboral - contrataciones masivas si es necesario
        if hasattr(mercado, 'mercado_laboral'):
            mercado.mercado_laboral.facilitar_contrataciones_masivas()

        # 4. Analytics ML cada 5 ciclos
        if hasattr(mercado, 'analytics_ml') and ciclo % 5 == 0:
            mercado.analytics_ml.ciclo_analytics()

        # 5. Actualizar precios dinámicos cada 3 ciclos
        if ciclo % 3 == 0:
            actualizar_precios_mercado(mercado)

        # === CICLO ECONÓMICO PRINCIPAL ===
        mercado.ejecutar_ciclo()

        # === REPORTES PERIÓDICOS ===
        if ciclo % frecuencia_reportes == 0 or ciclo == num_ciclos:
            # Calcular métricas actuales
            consumidores_totales = len(mercado.getConsumidores())
            desempleados = len(
                [c for c in mercado.getConsumidores() if not c.empleado])
            tasa_desempleo = (
                desempleados / max(1, consumidores_totales)) * 100

            pib_actual = mercado.pib_historico[-1] if mercado.pib_historico else 0
            inflacion_actual = mercado.inflacion_historica[-1] if mercado.inflacion_historica else 0

            transacciones_ciclo = len(
                [t for t in mercado.transacciones if t.get('ciclo', 0) == ciclo])
            empresas_activas = len(
                [e for e in mercado.getEmpresas() if hasattr(e, 'dinero') and e.dinero > 0])

            # Métricas ML
            modelos_entrenados = 0
            if hasattr(mercado, 'analytics_ml'):
                stats_ml = mercado.analytics_ml.obtener_estadisticas_analytics()
                modelos_entrenados = stats_ml.get('modelos_entrenados', 0)

            # Métricas bancarias
            depositos_totales = prestamos_totales = 0
            if hasattr(mercado, 'sistema_bancario') and mercado.sistema_bancario.bancos:
                for banco in mercado.sistema_bancario.bancos:
                    depositos_totales += sum(banco.depositos.values())
                    prestamos_totales += sum([p['monto']
                                             for p in banco.prestamos.values()])

            print(f"""
📊 REPORTE CICLO {ciclo}/{num_ciclos}:
   💰 PIB: ${pib_actual:,.2f} | 📈 Inflación: {inflacion_actual*100:.2f}%
   👥 Desempleo: {tasa_desempleo:.1f}% | 🏢 Empresas Activas: {empresas_activas}
   💼 Transacciones: {transacciones_ciclo} | 🤖 Modelos ML: {modelos_entrenados}
   🏦 Depósitos: ${depositos_totales:,.0f} | 💳 Préstamos: ${prestamos_totales:,.0f}
   🚨 Crisis: {'Activa' if mercado.crisis_financiera_activa else 'Inactiva'}""")

        # Actualizar gráfico en tiempo real
        if usar_tiempo_real and ciclo % 2 == 0:
            visualizador_tiempo_real.actualizar_grafico_tiempo_real(
                mercado.dashboard)

    # === FINALIZACIÓN ===
    tiempo_total = time.time() - tiempo_inicio

    if usar_tiempo_real:
        visualizador_tiempo_real.cerrar()

    print("\n" + "=" * 60)
    print("🎉 SIMULACIÓN COMPLETADA")
    print("=" * 60)
    print(f"⏱️ Tiempo total: {tiempo_total:.2f} segundos")
    print(f"🔄 Velocidad: {tiempo_total/num_ciclos:.3f} segundos/ciclo")

    # === RESULTADOS FINALES ===
    generar_resultados_finales(mercado, tiempo_total, num_ciclos)

    return mercado


def generar_resultados_finales(mercado, tiempo_total, num_ciclos):
    """Genera y guarda todos los resultados finales"""
    print("\n📊 GENERANDO RESULTADOS FINALES...")

    # === DASHBOARD COMPLETO ===
    mercado.dashboard.crear_dashboard_completo(
        num_ciclos, guardar_archivo=True)

    # === REPORTE TEXTUAL ===
    print("\n" + mercado.dashboard.generar_reporte_textual())

    # === EXPORTAR DATOS ===
    csv_file, json_file, reporte_file = exportar_resultados_completos(
        mercado.dashboard, prefijo="simulacion_v2_1"
    )

    # === ESTADÍSTICAS ADICIONALES ===
    print(f"\n🔧 ESTADÍSTICAS TÉCNICAS:")
    print(f"   ⏱️ Tiempo total: {tiempo_total:.2f}s")
    print(f"   🔄 Velocidad promedio: {tiempo_total/num_ciclos:.3f}s/ciclo")
    print(f"   👥 Agentes totales: {len(mercado.personas)}")
    print(f"   📦 Tipos de bienes: {len(mercado.bienes)}")
    print(f"   💼 Transacciones totales: {len(mercado.transacciones)}")

    if hasattr(mercado, 'sistema_precios'):
        stats_precios = mercado.sistema_precios.obtener_estadisticas_precios()
        if stats_precios:
            print(
                f"   💰 Precio promedio: ${stats_precios['precio_promedio']:.2f}")
            print(
                f"   📊 Dispersión precios: ${stats_precios['dispersion_precios']:.2f}")

    print(f"\n📁 Archivos generados:")
    print(f"   📄 Datos CSV: {csv_file}")
    print(f"   ⚙️ Configuración JSON: {json_file}")
    print(f"   📝 Reporte: {reporte_file}")


def main():
    """Función principal mejorada"""
    print("🏛️ SIMULADOR ECONÓMICO AVANZADO v2.1")
    print("=====================================")
    print("✅ Sistema ML con garantía de entrenamiento")
    print("✅ Precios dinámicos implementados")
    print("✅ Dashboard avanzado con múltiples métricas")
    print("✅ Configuración externa JSON")
    print("✅ Crisis financiera mejorada")
    print("✅ Mercado laboral activado")
    print("✅ Sistema bancario completamente funcional")
    print("=" * 60)

    try:
        # Cargar configuración
        print("⚙️ Cargando configuración...")
        configurador = ConfiguradorSimulacion()

        # Ejecutar simulación
        mercado = ejecutar_simulacion_completa(configurador)

        print("\n✅ SIMULACIÓN EXITOSA - Todas las mejoras funcionando correctamente")

        # Opción de ejecutar tests
        respuesta = input(
            "\n🧪 ¿Ejecutar tests automatizados? (s/n): ").lower().strip()
        if respuesta in ['s', 'si', 'y', 'yes']:
            print("\n🧪 Ejecutando tests automatizados...")
            try:
                from tests.test_completo_sistema import ejecutar_tests_completos
                tests_exitosos = ejecutar_tests_completos()
                if tests_exitosos:
                    print("✅ Todos los tests pasaron correctamente")
                else:
                    print("❌ Algunos tests fallaron - revisar logs")
            except ImportError:
                print("⚠️ Módulo de tests no disponible")

        print("\n🎯 SIMULACIÓN ECONÓMICA AVANZADA v2.1 COMPLETADA EXITOSAMENTE")

    except KeyboardInterrupt:
        print("\n\n⏹️ Simulación interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante la simulación: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
