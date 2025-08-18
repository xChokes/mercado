"""
SIMULADOR ECONÓMICO AVANZADO v2.2 - CON SISTEMA DE LOGGING
===========================================================

Simulación económica realista con todas las mejoras implementadas:
- ✅ Sistema ML con datos sintéticos garantizados
- ✅ Sistema de precios dinámicos 
- ✅ Configuración externa via JSON
- ✅ Dashboard avanzado con múltiples métricas
- ✅ Sistema de crisis mejorado
- ✅ Mercado laboral activado
- ✅ Sistema bancario completamente funcional
- ✅ Sistema de logging avanzado

Autor: Simulador Económico Team
Versión: 2.2 - Sistema de Logging Implementado
"""

from src.config.ConfiguradorSimulacion import ConfiguradorSimulacion
from src.utils.SimuladorLogger import SimuladorLogger
from src.systems.PreciosDinamicos import integrar_sistema_precios_dinamicos, actualizar_precios_mercado
from src.systems.VisualizacionAvanzada import DashboardEconomico, VisualizadorTiempoReal, exportar_resultados_completos
from src.systems.EstimuloEconomico import detectar_estancamiento_economico, aplicar_estimulo_emergencia
from src.systems.CrisisFinanciera import evaluar_recuperacion_crisis, aplicar_medidas_recuperacion, evaluar_riesgo_sistemico
from src.systems.MercadoLaboral import MercadoLaboral
from src.systems.AnalyticsML import SistemaAnalyticsML
from src.systems.SistemaBancario import SistemaBancario, Banco
from src.models.Gobierno import Gobierno
from src.models.EmpresaProductora import EmpresaProductora
from src.models.Empresa import Empresa
from src.models.Consumidor import Consumidor
from src.models.Bien import Bien
from src.models.Mercado import Mercado
from src.utils.SimuladorLogger import init_logging, get_simulador_logger, close_logging
import sys
import os
import time
import random
import logging
import matplotlib.pyplot as plt

# Añadir src al path de Python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Inicializar logger global
logger = SimuladorLogger()

# Importaciones principales

# Sistemas avanzados

# Configuración


def crear_bienes_expandidos():
    """Crea catálogo expandido de 45+ bienes en múltiples categorías"""
    bienes = {}

    logger.log_configuracion("Creando catálogo expandido de bienes...")

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

    logger.log_configuracion(
        f"Catálogo creado: {len(bienes)} bienes en {len(set(b.categoria for b in bienes.values()))} categorías")
    return bienes


def configurar_economia_avanzada(mercado, config):
    """Configura la economía con parámetros del archivo de configuración"""
    logger.log_configuracion("Configurando economía avanzada...")

    # Obtener configuración
    sim_config = config.obtener_seccion('simulacion')
    eco_config = config.obtener_seccion('economia')
    banco_config = config.obtener_seccion('sistema_bancario')

    # === CONSUMIDORES ===
    num_consumidores = sim_config.get('num_consumidores', 250)
    dinero_config = eco_config.get('dinero_inicial_consumidores', {
                                   'min': 5000, 'max': 15000})

    logger.log_configuracion(f"Creando {num_consumidores} consumidores...")
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

    logger.log_configuracion(
        f"Creando {num_empresas_prod} empresas productoras...")
    empresas = []
    for i in range(num_empresas_prod):
        empresa = EmpresaProductora(f'Productora_{i+1}', mercado)
        empresa.dinero = random.uniform(
            capital_config['min'], capital_config['max'])
        mercado.agregar_persona(empresa)
        empresas.append(empresa)

    # === EMPRESAS COMERCIALES ===
    num_empresas_com = sim_config.get('num_empresas_comerciales', 8)

    logger.log_configuracion(
        f"Creando {num_empresas_com} empresas comerciales...")
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
        logger.log_configuracion("Configurando sistema bancario...")
        mercado.sistema_bancario = SistemaBancario(mercado)

        # El SistemaBancario ya crea los bancos automáticamente
        num_bancos = len(mercado.sistema_bancario.bancos)
        capital_total = sum(
            banco.capital for banco in mercado.sistema_bancario.bancos)

        logger.log_configuracion(
            f"{num_bancos} bancos creados con capital total ${capital_total:,}")

    # === GOBIERNO ===
    logger.log_configuracion("Configurando gobierno...")
    mercado.gobierno = Gobierno(mercado)
    mercado.gobierno.presupuesto = eco_config.get(
        'pib_inicial', 100000) * 0.3  # 30% del PIB inicial

    # === CONTRATACIONES INICIALES ===
    logger.log_configuracion("Ejecutando contrataciones iniciales...")
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
    logger.log_configuracion(
        f"Tasa de desempleo inicial: {tasa_desempleo_real:.1f}%")

    return empresas


def integrar_sistemas_avanzados(mercado, config):
    """Integra todos los sistemas avanzados"""
    logger.log_configuracion("Integrando sistemas avanzados...")

    # === MACHINE LEARNING ===
    ml_config = config.obtener_seccion('machine_learning')
    if ml_config.get('activar', True):
        logger.log_configuracion("Activando sistema de Machine Learning...")
        mercado.analytics_ml = SistemaAnalyticsML(mercado)

        # Entrenar modelos iniciales con datos sintéticos
        logger.log_configuracion("Entrenando modelos ML iniciales...")
        modelos_entrenados = 0
        # Entrenar primeros 10 bienes
        for bien_nombre in list(mercado.bienes.keys())[:10]:
            if mercado.analytics_ml.predictor_demanda.get(bien_nombre) is None:
                from src.systems.AnalyticsML import PredictorDemanda
                mercado.analytics_ml.predictor_demanda[bien_nombre] = PredictorDemanda(
                )

            if mercado.analytics_ml.predictor_demanda[bien_nombre].entrenar(mercado, bien_nombre):
                modelos_entrenados += 1

        logger.log_configuracion(
            f"{modelos_entrenados} modelos ML entrenados exitosamente")

    # === MERCADO LABORAL ===
    logger.log_configuracion("Activando mercado laboral avanzado...")
    mercado.mercado_laboral = MercadoLaboral(mercado)

    # Asignar perfiles de habilidades a consumidores
    for consumidor in mercado.getConsumidores():
        if not hasattr(consumidor, 'perfil_habilidades'):
            consumidor.perfil_habilidades = mercado.mercado_laboral.crear_perfil()
            # 50% probabilidad de afiliación sindical
            mercado.mercado_laboral.asignar_sindicato(consumidor)

    # === SISTEMA DE PRECIOS DINÁMICOS ===
    logger.log_configuracion("Configurando sistema de precios dinámicos...")
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

    logger.log_configuracion(
        f"{precios_asignados} precios dinámicos asignados")

    # === DASHBOARD ===
    logger.log_configuracion("Configurando dashboard avanzado...")
    mercado.dashboard = DashboardEconomico(mercado)

    logger.log_configuracion("Todos los sistemas avanzados integrados")


def ejecutar_simulacion_completa(config):
    """Ejecuta la simulación completa con todas las mejoras"""
    logger.log_inicio("INICIANDO SIMULACIÓN ECONÓMICA AVANZADA v2.2")
    logger.log_inicio("=" * 60)

    # Inicializar sistema de logging (ya tenemos uno global, pero mantenemos el local para compatibilidad)
    local_logger = SimuladorLogger()
    local_logger.log_inicio("Simulación Económica Avanzada v2.2 iniciada")

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

    logger.log_configuracion(f"Ejecutando {num_ciclos} ciclos económicos...")
    logger.log_configuracion("=" * 60)

    # Logging inicial de configuración
    local_logger.log_configuracion(
        f"Simulación configurada con {num_ciclos} ciclos")
    local_logger.log_configuracion(
        f"Empresas creadas: {len(mercado.getEmpresas())}")
    local_logger.log_configuracion(
        f"Consumidores creados: {len(mercado.getConsumidores())}")
    local_logger.log_configuracion(
        f"Bienes disponibles: {len(mercado.bienes)}")

    # === EJECUCIÓN PRINCIPAL ===
    for ciclo in range(1, num_ciclos + 1):
        # Log inicio de ciclo
        local_logger.log_ciclo(f"=== INICIANDO CICLO {ciclo}/{num_ciclos} ===")

        # Actualizar dashboard antes del ciclo
        mercado.dashboard.actualizar_metricas(ciclo)

        # === SISTEMAS AUTOMÁTICOS ===

        # 1. Verificar y gestionar crisis financiera (una sola vez por ciclo)
        if mercado.crisis_financiera_activa:
            local_logger.log_crisis(
                f"Ciclo {ciclo}: Crisis financiera activa - ciclos en crisis: {getattr(mercado, 'ciclos_en_crisis', 0)}")
            if evaluar_recuperacion_crisis(mercado):
                local_logger.log_crisis(
                    f"Ciclo {ciclo}: Crisis financiera resuelta - Economía recuperándose")
                local_logger.log_crisis(
                    f"Ciclo {ciclo}: Crisis financiera RESUELTA - Economía recuperándose")
                mercado.crisis_financiera_activa = False
                mercado.ciclos_en_crisis = 0
            else:
                # Solo aplicar medidas cada 3 ciclos para evitar spam
                if getattr(mercado, 'ciclos_en_crisis', 0) % 3 == 0:
                    local_logger.log_crisis(
                        f"Ciclo {ciclo}: Aplicando medidas de recuperación de crisis")
                    aplicar_medidas_recuperacion(mercado)
                mercado.ciclos_en_crisis = getattr(
                    mercado, 'ciclos_en_crisis', 0) + 1
        else:
            # Evaluar si iniciar nueva crisis
            riesgo = evaluar_riesgo_sistemico(mercado.sistema_bancario) if hasattr(
                mercado, 'sistema_bancario') else 0
            if riesgo > 0.7:  # Umbral más alto para evitar crisis constantes
                mercado.crisis_financiera_activa = True
                mercado.ciclos_en_crisis = 0
                local_logger.log_crisis(
                    f"Ciclo {ciclo}: Crisis financiera detectada (riesgo: {riesgo:.2f})")
                local_logger.log_crisis(
                    f"Ciclo {ciclo}: Crisis financiera DETECTADA (riesgo: {riesgo:.2f})")
            elif riesgo > 0.4:  # Log niveles de riesgo elevados
                local_logger.log_crisis(
                    f"Ciclo {ciclo}: Riesgo sistémico elevado: {riesgo:.2f}")

        # 2. Detectar estancamiento económico (solo si no hay crisis activa)
        if not mercado.crisis_financiera_activa and detectar_estancamiento_economico(mercado):
            local_logger.log_sistema(
                f"Ciclo {ciclo}: Estancamiento económico detectado - aplicando estímulo de emergencia")
            aplicar_estimulo_emergencia(mercado)

        # 3. Mercado laboral - contrataciones masivas si es necesario
        if hasattr(mercado, 'mercado_laboral'):
            mercado.mercado_laboral.facilitar_contrataciones_masivas()
            # Log que se ejecutó la función (no devuelve un valor específico)
            local_logger.log_sistema(
                f"Ciclo {ciclo}: Proceso de contrataciones masivas ejecutado")

        # 4. Analytics ML cada 5 ciclos
        if hasattr(mercado, 'analytics_ml') and ciclo % 5 == 0:
            local_logger.log_ml(
                f"Ciclo {ciclo}: Ejecutando ciclo de Analytics ML")
            mercado.analytics_ml.ciclo_analytics()

        # 5. Actualizar precios dinámicos cada 3 ciclos
        if ciclo % 3 == 0:
            local_logger.log_precios(
                f"Ciclo {ciclo}: Actualizando precios dinámicos del mercado")
            actualizar_precios_mercado(mercado)

        # === CICLO ECONÓMICO PRINCIPAL ===
        local_logger.log_ciclo(
            f"Ciclo {ciclo}: Ejecutando ciclo económico principal")
        mercado.ejecutar_ciclo(ciclo)

        # Log métricas básicas del ciclo
        pib_actual = mercado.pib_historico[-1] if mercado.pib_historico else 0
        inflacion_actual = mercado.inflacion_historica[-1] if mercado.inflacion_historica else 0
        local_logger.log_metricas(
            f"Ciclo {ciclo}: PIB=${pib_actual:,.2f}, Inflación={inflacion_actual*100:.2f}%")

        # === REPORTES PERIÓDICOS ===
        if ciclo % frecuencia_reportes == 0 or ciclo == num_ciclos:
            local_logger.log_sistema(
                f"Generando reporte periódico para ciclo {ciclo}")
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

            local_logger.log_reporte(f"""
REPORTE CICLO {ciclo}/{num_ciclos}:
   PIB: ${pib_actual:,.2f} | Inflación: {inflacion_actual*100:.2f}%
   Desempleo: {tasa_desempleo:.1f}% | Empresas Activas: {empresas_activas}
   Transacciones: {transacciones_ciclo} | Modelos ML: {modelos_entrenados}
   Depósitos: ${depositos_totales:,.0f} | Préstamos: ${prestamos_totales:,.0f}
   Crisis: {'Activa' if mercado.crisis_financiera_activa else 'Inactiva'}""")

            # Log reporte detallado
            local_logger.log_reporte(
                f"REPORTE CICLO {ciclo}: PIB=${pib_actual:,.2f}, Inflación={inflacion_actual*100:.2f}%, Desempleo={tasa_desempleo:.1f}%, Empresas={empresas_activas}, Transacciones={transacciones_ciclo}")
            local_logger.log_reporte(
                f"REPORTE CICLO {ciclo}: Depósitos=${depositos_totales:,.0f}, Préstamos=${prestamos_totales:,.0f}, Crisis={'Activa' if mercado.crisis_financiera_activa else 'Inactiva'}")

        # Actualizar gráfico en tiempo real
        if usar_tiempo_real and ciclo % 2 == 0:
            visualizador_tiempo_real.actualizar_grafico_tiempo_real(
                mercado.dashboard)

    # === FINALIZACIÓN ===
    tiempo_total = time.time() - tiempo_inicio
    local_logger.log_sistema(
        f"Simulación completada - Tiempo total: {tiempo_total:.2f} segundos")
    local_logger.log_metricas(
        f"Velocidad promedio: {tiempo_total/num_ciclos:.3f} segundos/ciclo")

    if usar_tiempo_real:
        visualizador_tiempo_real.cerrar()

    logger.log_fin("=" * 60)
    logger.log_fin("SIMULACIÓN COMPLETADA")
    logger.log_fin("=" * 60)
    logger.log_fin(f"Tiempo total: {tiempo_total:.2f} segundos")
    logger.log_fin(f"Velocidad: {tiempo_total/num_ciclos:.3f} segundos/ciclo")

    # === RESULTADOS FINALES ===
    local_logger.log_sistema("Generando resultados finales de la simulación")
    generar_resultados_finales(mercado, tiempo_total, num_ciclos)

    # Log final de cierre
    local_logger.log_fin(
        "Simulación Económica Avanzada v2.2 completada exitosamente")

    return mercado


def generar_resultados_finales(mercado, tiempo_total, num_ciclos):
    """Genera y guarda todos los resultados finales"""
    logger.log_sistema("GENERANDO RESULTADOS FINALES...")

    # === DASHBOARD COMPLETO ===
    mercado.dashboard.crear_dashboard_completo(
        num_ciclos, guardar_archivo=True)

    # === REPORTE TEXTUAL ===
    logger.log_reporte("Reporte textual generado:")
    logger.log_reporte(mercado.dashboard.generar_reporte_textual())

    # === EXPORTAR DATOS ===
    csv_file, json_file, reporte_file = exportar_resultados_completos(
        mercado.dashboard, prefijo="simulacion_v2_1"
    )

    # === ESTADÍSTICAS ADICIONALES ===
    logger.log_sistema("ESTADÍSTICAS TÉCNICAS:")
    logger.log_sistema(f"   Tiempo total: {tiempo_total:.2f}s")
    logger.log_sistema(
        f"   Velocidad promedio: {tiempo_total/num_ciclos:.3f}s/ciclo")
    logger.log_sistema(f"   Agentes totales: {len(mercado.personas)}")
    logger.log_sistema(f"   Tipos de bienes: {len(mercado.bienes)}")
    logger.log_sistema(
        f"   Transacciones totales: {len(mercado.transacciones)}")

    if hasattr(mercado, 'sistema_precios'):
        stats_precios = mercado.sistema_precios.obtener_estadisticas_precios()
        if stats_precios:
            logger.log_sistema(
                f"   Precio promedio: ${stats_precios['precio_promedio']:.2f}")
            logger.log_sistema(
                f"   Dispersión precios: ${stats_precios['dispersion_precios']:.2f}")

    logger.log_sistema("Archivos generados:")
    logger.log_sistema(f"   Datos CSV: {csv_file}")
    logger.log_sistema(f"   Configuración JSON: {json_file}")
    logger.log_sistema(f"   Reporte: {reporte_file}")


def main():
    """Función principal mejorada"""
    logger.log_inicio("SIMULADOR ECONÓMICO AVANZADO v2.2")
    logger.log_inicio("=====================================")
    logger.log_inicio("✅ Sistema ML con garantía de entrenamiento")
    logger.log_inicio("✅ Precios dinámicos implementados")
    logger.log_inicio("✅ Dashboard avanzado con múltiples métricas")
    logger.log_inicio("✅ Configuración externa JSON")
    logger.log_inicio("✅ Crisis financiera mejorada")
    logger.log_inicio("✅ Mercado laboral activado")
    logger.log_inicio("✅ Sistema bancario completamente funcional")
    logger.log_inicio("✅ Sistema de logging avanzado implementado")
    logger.log_inicio("=" * 60)

    # Inicializar logger para la función main (usar el global)
    main_logger = logger

    try:
        # Cargar configuración
        logger.log_configuracion("Cargando configuración...")
        main_logger.log_inicio("Cargando configuración del simulador")
        configurador = ConfiguradorSimulacion()

        # Ejecutar simulación
        main_logger.log_inicio("Iniciando ejecución de simulación completa")
        mercado = ejecutar_simulacion_completa(configurador)

        main_logger.log_fin(
            "Simulación exitosa - todas las mejoras funcionando correctamente")

        logger.log_fin(
            "SIMULACIÓN ECONÓMICA AVANZADA v2.2 COMPLETADA EXITOSAMENTE")
        main_logger.log_fin(
            "SIMULACIÓN ECONÓMICA AVANZADA v2.2 COMPLETADA EXITOSAMENTE")

    except KeyboardInterrupt:
        main_logger.log_error(
            "Simulación interrumpida por el usuario (KeyboardInterrupt)")
    except Exception as e:
        main_logger.log_error(f"Error durante la simulación: {e}")
        import traceback
        main_logger.log_error(f"Traceback completo: {traceback.format_exc()}")
        # Mantenemos el traceback para debug si es necesario
        traceback.print_exc()


if __name__ == "__main__":
    main()
