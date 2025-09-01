"""
SIMULADOR ECONÓMICO AVANZADO v3.0 - SISTEMA DE AGENTES IA HIPERREALISTAS
=========================================================================

Simulación económica hiperrealista con todas las mejoras implementadas:
- ✅ Sistema ML con datos sintéticos garantizados
- ✅ Sistema de precios dinámicos 
- ✅ Configuración externa via JSON
- ✅ Dashboard avanzado con múltiples métricas
- ✅ Sistema de crisis mejorado
- ✅ Mercado laboral activado
- ✅ Sistema bancario completamente funcional
- ✅ Sistema de logging avanzado
- 🚀 NUEVO: Banco Central con política monetaria automática
- 🚀 NUEVO: Control de precios realista con inercia
- 🚀 NUEVO: Ciclos económicos genuinos (4 fases)
- 🚀 NUEVO: Sistema de rescate empresarial
- 🤖 NUEVO v3.0: SISTEMA DE AGENTES IA HIPERREALISTAS
  - 🧠 Motor de decisiones con redes neuronales
  - 💾 Sistema de memoria avanzado para agentes
  - 🌐 Protocolos de comunicación entre agentes
  - 📱 Redes sociales virtuales y formación de coaliciones
  - 🎯 Deep Learning para predicción y adaptación
  - ⚡ Coordinación inteligente de mercado en tiempo real

Autor: Simulador Económico Team
Versión: 3.0 - Agentes IA Hiperrealistas
"""

from src.config.ConfiguradorSimulacion import ConfiguradorSimulacion
from src.utils.SimuladorLogger import SimuladorLogger
from src.systems.PreciosDinamicos import integrar_sistema_precios_dinamicos, actualizar_precios_mercado
from src.systems.VisualizacionAvanzada import DashboardEconomico, VisualizadorTiempoReal, exportar_resultados_completos
from src.systems.EstimuloEconomico import detectar_estancamiento_economico, aplicar_estimulo_emergencia
from src.systems.CrisisFinanciera import evaluar_recuperacion_crisis, aplicar_medidas_recuperacion, evaluar_riesgo_sistemico
from src.systems.MercadoLaboral import MercadoLaboral
from src.systems.labor_market import EnhancedLaborMarket
from src.systems.AnalyticsML import SistemaAnalyticsML
from src.systems.SistemaBancario import SistemaBancario, Banco
# NUEVOS SISTEMAS HIPERREALISTAS v3.0
from src.systems.BancoCentral import BancoCentral
from src.systems.ControlPreciosRealista import ControladorPreciosRealista
from src.systems.CicloEconomicoRealista import CicloEconomicoRealista
from src.systems.GestorRescateEmpresarial import GestorRescateEmpresarial
from src.systems.SistemaFiscal import SistemaFiscal
from src.systems.MercadoCapitales import BolsaValores
from src.systems.ClasesSociales import SistemaClasesSociales
# NUEVOS SISTEMAS DE VALIDACIÓN Y ESTABILIZACIÓN v3.1
from src.systems.ValidadorEconomico import ValidadorEconomico
from src.systems.BancoCentralAvanzado import BancoCentralAvanzado
# NUEVOS SISTEMAS ECONÓMICOS AVANZADOS v3.2 - FASE 2
try:
    from src.systems.ModelosEconomicosAvanzados import IntegradorModelosEconomicos, ParametrosEconomicos
    from src.config.DatosEconomicosReales import CalibradorEconomicoRealista
    MODELOS_ECONOMICOS_DISPONIBLES = True
except ImportError:
    MODELOS_ECONOMICOS_DISPONIBLES = False
# SISTEMA DE AGENTES IA HIPERREALISTAS v3.0
from src.ai.IntegradorAgentesIA import IntegradorAgentesIA, ConfiguracionSistemaIA
from src.models.Gobierno import Gobierno
from src.models.EmpresaProductora import EmpresaProductora
from src.models.EmpresaProductoraHiperrealista import EmpresaProductoraHiperrealista
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
import argparse
import json

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

    # === EMPRESAS PRODUCTORAS HIPERREALISTAS ===
    num_empresas_prod = sim_config.get('num_empresas_productoras', 5)
    capital_config = eco_config.get('capital_inicial_empresas', {
                                    'min': 100000, 'max': 1500000})

    logger.log_configuracion(
        f"Creando {num_empresas_prod} empresas productoras hiperrealistas...")
    empresas = []
    for i in range(num_empresas_prod):
        # Usar empresas hiperrealistas por defecto
        if sim_config.get('usar_empresas_hiperrealistas', True):
            empresa = EmpresaProductoraHiperrealista(f'Productora_Hiperrealista_{i+1}', mercado)
        else:
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

    # === NUEVO: SISTEMA DE VALIDACIÓN ECONÓMICA ===
    logger.log_configuracion("Activando sistema de validación económica...")
    mercado.validador_economico = ValidadorEconomico()
    
    # === NUEVO: BANCO CENTRAL AVANZADO ===
    logger.log_configuracion("Activando Banco Central Avanzado con Taylor Rule...")
    mercado.banco_central_avanzado = BancoCentralAvanzado(mercado)
    
    # === NUEVOS: MODELOS ECONÓMICOS AVANZADOS - FASE 2 ===
    if MODELOS_ECONOMICOS_DISPONIBLES:
        logger.log_configuracion("🧮 Activando modelos económicos avanzados (DSGE, IS-LM)...")
        mercado.integrador_modelos = IntegradorModelosEconomicos()
        mercado.calibrador_economico = CalibradorEconomicoRealista()
        
        # Calibrar configuración con datos reales
        config_dict = config.config
        config_calibrada = mercado.calibrador_economico.calibrar_configuracion_base(config_dict)
        
        # Actualizar configuración del mercado con parámetros calibrados
        if 'economia' in config_calibrada:
            eco_config = config_calibrada['economia']
            mercado.tasa_inflacion_objetivo = eco_config.get('tasa_inflacion_objetivo', 0.025)
            mercado.crecimiento_pib_objetivo = eco_config.get('crecimiento_pib_objetivo', 0.025)
            mercado.volatilidad_economica = eco_config.get('volatilidad_economica', 0.15)
        
        logger.log_configuracion("✅ Modelos económicos profesionales ACTIVADOS")
    else:
        logger.log_configuracion("⚠️  Modelos económicos avanzados NO DISPONIBLES")

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

    # === ENHANCED LABOR MARKET with DMP-style matching ===
    logger.log_configuracion("Activando sistema de mercado laboral mejorado con emparejamiento DMP...")
    mercado.enhanced_labor_market = EnhancedLaborMarket(mercado)

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

    # === SISTEMAS HIPERREALISTAS v3.0 ===
    logger.log_configuracion("🚀 INTEGRANDO SISTEMAS HIPERREALISTAS v3.0...")
    
    # 1. BANCO CENTRAL - Política monetaria automática
    logger.log_configuracion("🏦 Configurando Banco Central...")
    mercado.banco_central = BancoCentral(mercado)
    logger.log_configuracion(f"   Banco Central creado - Tasa inicial: {mercado.banco_central.tasa_interes_base:.2%}")
    
    # 2. CONTROLADOR DE PRECIOS REALISTA - Inercia y límites
    logger.log_configuracion("💰 Configurando Control de Precios Realista...")
    mercado.controlador_precios = ControladorPreciosRealista(mercado)
    logger.log_configuracion(f"   Control activado - Inercia: {mercado.controlador_precios.inercia_precios:.1%}")
    
    # 3. GESTOR DE CICLO ECONÓMICO - 4 fases reales
    logger.log_configuracion("📊 Configurando Ciclo Económico Realista...")
    mercado.gestor_ciclo = CicloEconomicoRealista(mercado)
    logger.log_configuracion(f"   Fase inicial: {mercado.gestor_ciclo.fase_actual.value}")
    
    # 4. GESTOR DE RESCATE EMPRESARIAL - Prevenir colapso
    logger.log_configuracion("🚑 Configurando Sistema de Rescate Empresarial...")
    mercado.gestor_rescate = GestorRescateEmpresarial(mercado)
    logger.log_configuracion(f"   Fondo rescate: {mercado.gestor_rescate.fondo_rescate_porcentaje:.1%} del PIB")
    
    # === SISTEMA DE AGENTES IA HIPERREALISTAS v3.0 ===
    logger.log_configuracion("🤖 CONFIGURANDO SISTEMA DE AGENTES IA HIPERREALISTAS v3.0...")
    ia_config = config.obtener_seccion('agentes_ia')
    if ia_config.get('activar', True):
        try:
            # Configuración del sistema de IA
            configuracion_ia = ConfiguracionSistemaIA(
                num_consumidores_ia=ia_config.get('num_consumidores', 15),
                num_empresas_ia=ia_config.get('num_empresas', 6),
                activar_deep_learning=ia_config.get('deep_learning', True),
                activar_redes_sociales=ia_config.get('redes_sociales', True),
                activar_coaliciones=ia_config.get('coaliciones', True),
                activar_logs_detallados=ia_config.get('logs_detallados', True),
                duracion_simulacion_minutos=ia_config.get('duracion_minutos', 3)
            )
            
            # Crear bienes para el sistema de IA
            bienes_ia = list(mercado.bienes.keys())[:10]  # Usar los primeros 10 bienes
            
            # Inicializar sistema integrador de IA
            mercado.sistema_ia = IntegradorAgentesIA(bienes_ia, configuracion_ia)
            logger.log_configuracion(f"   ✅ Sistema IA creado con {configuracion_ia.num_consumidores_ia} consumidores y {configuracion_ia.num_empresas_ia} empresas")
            logger.log_configuracion(f"   ✅ Deep Learning: {configuracion_ia.activar_deep_learning}")
            logger.log_configuracion(f"   ✅ Redes Sociales: {configuracion_ia.activar_redes_sociales}")
            logger.log_configuracion(f"   ✅ Coaliciones: {configuracion_ia.activar_coaliciones}")
            
        except Exception as e:
            logger.log_error(f"   ❌ Error integrando sistema IA: {e}")
            mercado.sistema_ia = None
    else:
        logger.log_configuracion("   🚫 Sistema de IA desactivado en configuración")
        mercado.sistema_ia = None
    
    logger.log_configuracion("🎯 HIPERREALISMO IMPLEMENTADO - Simulador transformado")

    logger.log_configuracion("Todos los sistemas avanzados integrados")

    # === MERCADO DE CAPITALES ===
    # Instanciar bolsa y listar empresas una vez creadas
    try:
        logger.log_configuracion("📈 Configurando Mercado de Capitales...")
        mercado.bolsa_valores = BolsaValores(mercado)
        mercado.bolsa_valores.listar_empresas()
        logger.log_configuracion("   Bolsa de Valores activa y empresas listadas")
    except Exception as e:
        logger.log_error(f"   ❌ No se pudo activar la Bolsa de Valores: {e}")


def ejecutar_simulacion_completa(config, prefijo_resultados: str | None = None):
    """Ejecuta la simulación completa con todas las mejoras hiperrealistas v3.0"""
    logger.log_inicio("INICIANDO SIMULACIÓN ECONÓMICA HIPERREALISTA v3.0")
    logger.log_inicio("=" * 70)

    # Inicializar sistema de logging (ya tenemos uno global, pero mantenemos el local para compatibilidad)
    local_logger = SimuladorLogger()
    local_logger.log_inicio("Simulación Económica Hiperrealista v3.0 iniciada")

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

        # === SISTEMAS AUTOMÁTICOS ===

        # === SISTEMAS HIPERREALISTAS v3.0 (EJECUTAR PRIMERO) ===
        
        # 1. BANCO CENTRAL - Política monetaria automática cada ciclo
        if hasattr(mercado, 'banco_central'):
            decision_bc = mercado.banco_central.ejecutar_politica_monetaria(ciclo)
            if decision_bc['accion_tomada']:
                local_logger.log_sistema(f"🏦 Banco Central - Ciclo {ciclo}: {decision_bc['descripcion']}")
                local_logger.log_sistema(f"   Nueva tasa: {decision_bc['nueva_tasa']:.2f}%, Justificación: {decision_bc['justificacion']}")
        
        # 2. CICLO ECONÓMICO REALISTA - Gestionar transiciones de fase
        if hasattr(mercado, 'gestor_ciclo'):
            fase_anterior = mercado.gestor_ciclo.fase_actual.value
            cambio_fase = mercado.gestor_ciclo.procesar_ciclo_economico(ciclo)
            if cambio_fase['transicion_ocurrida']:
                local_logger.log_sistema(f"📊 Ciclo Económico - Ciclo {ciclo}: {fase_anterior} → {cambio_fase['nueva_fase']}")
                local_logger.log_sistema(f"   Duración fase anterior: {cambio_fase['duracion_fase_anterior']} ciclos")
                local_logger.log_sistema(f"   Efectos económicos aplicados: {cambio_fase['efectos_aplicados']}")
        
        # 3. SISTEMA DE AGENTES IA HIPERREALISTAS v3.0 - ALGORITMO AVANZADO COMPLETO
        if hasattr(mercado, 'sistema_ia') and mercado.sistema_ia is not None:
            try:
                local_logger.log_sistema(f"🤖 Ejecutando IA Avanzada - Ciclo {ciclo}")
                
                # === FASE 1: ACTUALIZACIÓN DEL CONOCIMIENTO DEL MERCADO ===
                # Sincronizar datos del mercado tradicional con los agentes IA
                mercado.sistema_ia._sincronizar_estado_mercado(mercado, ciclo)
                
                # === FASE 2: EJECUCIÓN COORDINADA DE AGENTES IA ===
                resultado_ia = mercado.sistema_ia.ejecutar_ciclo_coordinado(mercado, ciclo)
                
                # === FASE 3: ANÁLISIS INTELIGENTE Y TOMA DE DECISIONES ===
                # Los agentes IA analizan el mercado y toman decisiones autónomas
                decisiones_consumidores = mercado.sistema_ia._procesar_decisiones_consumidores_ia(ciclo)
                decisiones_empresas = mercado.sistema_ia._procesar_decisiones_empresas_ia(ciclo)
                
                # === FASE 4: INTEGRACIÓN CON MERCADO TRADICIONAL ===
                # Aplicar las decisiones de IA al mercado tradicional
                transacciones_ia = mercado.sistema_ia._aplicar_decisiones_al_mercado(
                    mercado, decisiones_consumidores, decisiones_empresas, ciclo
                )
                
                # === FASE 5: APRENDIZAJE Y ADAPTACIÓN ===
                # El sistema IA aprende de los resultados y se adapta
                mercado.sistema_ia._actualizar_aprendizaje_global(resultado_ia, transacciones_ia, ciclo)
                
                # === REPORTE AVANZADO DE IA (cada 3 ciclos) ===
                if ciclo % 3 == 0:
                    stats_ia = mercado.sistema_ia._obtener_estadisticas_completas()
                    local_logger.log_sistema(f"🤖 IA AVANZADA - Ciclo {ciclo}:")
                    local_logger.log_sistema(f"   👥 Agentes Activos: {stats_ia['agentes_activos']}")
                    local_logger.log_sistema(f"   💰 Transacciones IA: {stats_ia['transacciones_ia']}")
                    local_logger.log_sistema(f"   🎯 Eficiencia Global: {stats_ia['eficiencia_global']:.3f}")
                    local_logger.log_sistema(f"   🧠 Redes Neuronales: {stats_ia['redes_neuronales']}")
                    local_logger.log_sistema(f"   🌐 Relaciones Sociales: {stats_ia['relaciones_sociales']}")
                    local_logger.log_sistema(f"   🤝 Coaliciones Activas: {stats_ia['coaliciones_activas']}")
                    local_logger.log_sistema(f"   📊 Predicciones Precisas: {stats_ia['precision_predicciones']:.1%}")
                    local_logger.log_sistema(f"   🔄 Adaptaciones por Ciclo: {stats_ia['adaptaciones_ciclo']}")
                
                # === ANÁLISIS PREDICTIVO AVANZADO (cada 10 ciclos) ===
                if ciclo % 10 == 0:
                    predicciones = mercado.sistema_ia._generar_predicciones_mercado(ciclo, horizonte=5)
                    local_logger.log_sistema(f"🔮 PREDICCIONES IA (próximos 5 ciclos):")
                    local_logger.log_sistema(f"   📈 PIB Esperado: ${predicciones['pib_esperado']:,.0f}")
                    local_logger.log_sistema(f"   💹 Tendencia Precios: {predicciones['tendencia_precios']}")
                    local_logger.log_sistema(f"   � Nuevas Empresas IA: {predicciones['nuevas_empresas_ia']}")
                    local_logger.log_sistema(f"   ⚡ Oportunidades Detectadas: {predicciones['oportunidades_detectadas']}")
                
                # === OPTIMIZACIÓN AUTOMÁTICA DEL SISTEMA ===
                # El sistema se auto-optimiza basándose en métricas de rendimiento
                if ciclo % 15 == 0:
                    optimizaciones = mercado.sistema_ia._auto_optimizar_parametros(ciclo)
                    if optimizaciones['cambios_realizados'] > 0:
                        local_logger.log_sistema(f"⚡ AUTO-OPTIMIZACIÓN IA:")
                        local_logger.log_sistema(f"   🔧 Parámetros ajustados: {optimizaciones['cambios_realizados']}")
                        local_logger.log_sistema(f"   📊 Mejora rendimiento: +{optimizaciones['mejora_rendimiento']:.1%}")
                
            except Exception as e:
                local_logger.log_error(f"   ❌ Error en IA avanzada (ciclo {ciclo}): {e}")
                # Sistema de recuperación automática
                try:
                    mercado.sistema_ia._recuperacion_automatica(e, ciclo)
                    local_logger.log_sistema(f"   🔄 Recuperación automática IA activada")
                except:
                    local_logger.log_error(f"   ⚠️ Sistema IA en modo degradado")
        
        # 4. RESCATE EMPRESARIAL - Evaluar y rescatar empresas en crisis
        if hasattr(mercado, 'gestor_rescate'):
            mercado.gestor_rescate.evaluar_y_rescatar_empresas(ciclo)
            mercado.gestor_rescate.procesar_liquidaciones_programadas(ciclo)
            
            # Log estadísticas cada 10 ciclos
            if ciclo % 10 == 0:
                stats_rescate = mercado.gestor_rescate.obtener_estadisticas_rescate()
                local_logger.log_sistema(f"🚑 Rescate Empresarial - Ciclo {ciclo}: "
                                       f"Rescates={stats_rescate['rescates_totales']}, "
                                       f"Fusiones={stats_rescate['fusiones_totales']}, "
                                       f"Liquidaciones={stats_rescate['liquidaciones_totales']}")

        # 5. SISTEMA FISCAL AVANZADO - Recaudación, gasto y política fiscal
        if hasattr(mercado, 'sistema_fiscal'):
            reporte_fiscal = mercado.sistema_fiscal.ejecutar_ciclo_fiscal(ciclo)
            
            # Log fiscal cada 5 ciclos
            if ciclo % 5 == 0:
                local_logger.log_sistema(f"💰 Sistema Fiscal - Ciclo {ciclo}: "
                                       f"Recaudación=${reporte_fiscal['recaudacion_total']:,.0f}, "
                                       f"Gasto=${reporte_fiscal['gasto_publico']:,.0f}, "
                                       f"Política={reporte_fiscal['politica_fiscal']}")
                local_logger.log_sistema(f"   Déficit/PIB: {reporte_fiscal['deficit_pib_ratio']:.1%}, "
                                       f"Deuda/PIB: {reporte_fiscal['deuda_pib_ratio']:.1%}")

        # 6. MERCADO DE CAPITALES - Trading y burbujas bursátiles
        if hasattr(mercado, 'bolsa_valores'):
            reporte_bursatil = mercado.bolsa_valores.ejecutar_ciclo_bursatil(ciclo)
            
            # Log bursátil cada 5 ciclos
            if ciclo % 5 == 0:
                local_logger.log_sistema(f"📈 Bolsa de Valores - Ciclo {ciclo}: "
                                       f"Sentimiento={reporte_bursatil['sentimiento_mercado']:.2f}, "
                                       f"Volumen={reporte_bursatil['volumen_total']:,}, "
                                       f"Índice General={reporte_bursatil['indices'].get('GENERAL', 0):.1f}")
                if reporte_bursatil['en_burbuja']:
                    local_logger.log_sistema(f"   🎈 BURBUJA BURSÁTIL ACTIVA")

        # 6. SISTEMA DE CLASES SOCIALES - Movilidad social
        if hasattr(mercado, 'sistema_clases'):
            reporte_social = mercado.sistema_clases.ejecutar_ciclo_movilidad_social(ciclo)
            
            # Log social cada 12 ciclos (anual)
            if reporte_social:  # Solo si hubo evaluación de movilidad
                local_logger.log_sistema(f"👥 Clases Sociales - Ciclo {ciclo}: "
                                       f"Movilidad={reporte_social['movimientos_totales']}, "
                                       f"Ascensos={reporte_social['movilidad_ascendente']}, "
                                       f"Descensos={reporte_social['movilidad_descendente']}")
                local_logger.log_sistema(f"   Gini={reporte_social['coeficiente_gini']:.3f}, "
                                       f"Ratio 90/10={reporte_social['ratio_90_10']:.1f}")

        # === SISTEMAS EXISTENTES ===

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

        # 3.1. Enhanced Labor Market - DMP-style matching and wage formation
        if hasattr(mercado, 'enhanced_labor_market'):
            labor_stats = mercado.enhanced_labor_market.labor_market_cycle()
            local_logger.log_sistema(
                f"Ciclo {ciclo}: Enhanced Labor Market - "
                f"Desempleo: {labor_stats['unemployment_rate']:.1%}, "
                f"Salario promedio: ${labor_stats['average_wage']:,.0f}, "
                f"Vacantes: {labor_stats['total_vacancies']}, "
                f"Emparejamientos: {labor_stats['matches_made']}")

        # 4. Analytics ML cada 5 ciclos
        if hasattr(mercado, 'analytics_ml') and ciclo % 5 == 0:
            local_logger.log_ml(
                f"Ciclo {ciclo}: Ejecutando ciclo de Analytics ML")
            mercado.analytics_ml.ciclo_analytics()

        # 5. Actualizar precios dinámicos cada 3 ciclos + Control realista
        if ciclo % 3 == 0:
            local_logger.log_precios(
                f"Ciclo {ciclo}: Actualizando precios dinámicos del mercado")
            actualizar_precios_mercado(mercado)
            
            # SISTEMA HIPERREALISTA: Control de precios realista (aplicar DESPUÉS de precios dinámicos)
            if hasattr(mercado, 'controlador_precios'):
                # NUEVO: Monitorear y responder a hiperinflación ANTES del control normal
                emergencia_activada = mercado.controlador_precios.monitorear_y_responder_hiperinflacion(ciclo)
                
                cambios_aplicados = mercado.controlador_precios.aplicar_control_masivo_precios(ciclo)
                if cambios_aplicados > 0:
                    local_logger.log_precios(
                        f"💰 Control Precios - Ciclo {ciclo}: {cambios_aplicados} precios controlados por inercia")
                    
                # Log de emergencia si está activa
                if emergencia_activada:
                    local_logger.log_sistema(f"🚨 CONTROLES DE EMERGENCIA ANTI-HIPERINFLACIÓN ACTIVADOS - Ciclo {ciclo}")
                    
                # Log estadísticas cada 15 ciclos
                if ciclo % 15 == 0:
                    stats_precios = mercado.controlador_precios.obtener_estadisticas_control()
                    local_logger.log_precios(f"💰 Control Precios - Estadísticas: "
                                            f"Cambios aplicados={stats_precios['cambios_aplicados']}, "
                                            f"Precio promedio=${stats_precios['precio_promedio_actual']:.2f}")

        # === CICLO ECONÓMICO PRINCIPAL ===
        local_logger.log_ciclo(
            f"Ciclo {ciclo}: Ejecutando ciclo económico principal")
        mercado.ejecutar_ciclo(ciclo)

        # === NUEVO: VALIDACIÓN ECONÓMICA POST-CICLO ===
        if hasattr(mercado, 'validador_economico'):
            alertas = mercado.validador_economico.validar_indicadores_macroeconomicos(mercado, ciclo)
            alertas_precios = mercado.validador_economico.detectar_anomalias_precios(mercado, ciclo)
            
            # Log alertas críticas inmediatamente
            alertas_criticas = [a for a in alertas + alertas_precios if a.tipo.value == "CRITICA"]
            if alertas_criticas:
                for alerta in alertas_criticas:
                    local_logger.log_error(f"🚨 ALERTA CRÍTICA: {alerta.mensaje}")
            
            # Log reporte de validación cada 10 ciclos
            if ciclo % 10 == 0:
                # Usar reporte avanzado si hay modelos disponibles
                if MODELOS_ECONOMICOS_DISPONIBLES and hasattr(mercado, 'validador_economico'):
                    reporte_validacion = mercado.validador_economico.generar_reporte_avanzado(mercado, ciclo)
                    local_logger.log_sistema("📊 REPORTE AVANZADO DE VALIDACIÓN ECONÓMICA:")
                else:
                    reporte_validacion = mercado.validador_economico.generar_reporte_validacion(mercado, ciclo)
                    local_logger.log_sistema("📊 REPORTE DE VALIDACIÓN ECONÓMICA:")
                
                for linea in reporte_validacion.split('\n'):
                    if linea.strip():
                        local_logger.log_sistema(f"   {linea}")
                
                # Análisis con modelos económicos avanzados cada 15 ciclos
                if MODELOS_ECONOMICOS_DISPONIBLES and hasattr(mercado, 'integrador_modelos') and ciclo % 15 == 0:
                    try:
                        # Obtener todas las empresas
                        todas_empresas = []
                        if hasattr(mercado, 'empresas_productoras'):
                            todas_empresas.extend(mercado.empresas_productoras)
                        if hasattr(mercado, 'empresas_comerciales'):
                            todas_empresas.extend(mercado.empresas_comerciales)
                        
                        estado_economico = {
                            'inflacion': getattr(mercado, 'inflacion_anual', 0.02),
                            'desempleo': getattr(mercado, 'tasa_desempleo', 0.05),
                            'crecimiento_pib': getattr(mercado, 'crecimiento_pib', 0.02),
                            'productividad': getattr(mercado, 'productividad_promedio', 1.0),
                            'pib': getattr(mercado, 'pib_total', 1000000),
                            'capital': sum(getattr(emp, 'capital', 0) for emp in todas_empresas),
                            'trabajo': len([c for c in mercado.consumidores if getattr(c, 'empleado', False)])
                        }
                        
                        analisis_completo = mercado.integrador_modelos.analisis_completo(estado_economico)
                        
                        local_logger.log_sistema("🧮 ANÁLISIS MODELOS ECONÓMICOS AVANZADOS:")
                        if 'sintesis' in analisis_completo:
                            sintesis = analisis_completo['sintesis']
                            local_logger.log_sistema(f"   📈 PIB Consenso: {sintesis.get('pib_consenso', 'N/A')}")
                            local_logger.log_sistema(f"   💰 Tasa Consenso: {sintesis.get('tasa_consenso', 'N/A'):.3f}%")
                            local_logger.log_sistema(f"   🎯 Consistencia: {sintesis.get('consistencia_modelos', 0):.1%}")
                        
                        # Detectar régimen económico
                        if hasattr(mercado, 'calibrador_economico'):
                            regimen = mercado.calibrador_economico.detectar_regimen_economico(estado_economico)
                            local_logger.log_sistema(f"   📊 Régimen Económico: {regimen}")
                            
                    except Exception as e:
                        local_logger.log_sistema(f"   ⚠️  Error en análisis avanzado: {e}")

        # === NUEVO: POLÍTICA MONETARIA AVANZADA ===
        if hasattr(mercado, 'banco_central_avanzado'):
            decision_monetaria = mercado.banco_central_avanzado.ejecutar_politica_monetaria(ciclo)
            if decision_monetaria:
                local_logger.log_sistema(f"🏦 POLÍTICA MONETARIA: {decision_monetaria.justificacion}")
                if abs(decision_monetaria.tasa_nueva - decision_monetaria.tasa_anterior) > 0.002:
                    comunicado = mercado.banco_central_avanzado.generar_comunicado_monetario(decision_monetaria)
                    local_logger.log_sistema("📢 COMUNICADO BANCO CENTRAL:")
                    for linea in comunicado.split('\n'):
                        if linea.strip() and not linea.startswith('='):
                            local_logger.log_sistema(f"   {linea}")

        # Actualizar dashboard después del ciclo (cuando ya se calculó PIB)
        mercado.dashboard.actualizar_metricas(ciclo)

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

            # Enhanced Labor Market metrics
            enhanced_metrics = {}
            if hasattr(mercado, 'enhanced_labor_market'):
                enhanced_metrics = mercado.enhanced_labor_market.metrics
                # Use enhanced metrics if available
                tasa_desempleo = enhanced_metrics.get('unemployment_rate', tasa_desempleo / 100) * 100

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

            # === MÉTRICAS HIPERREALISTAS v3.0 ===
            # Banco Central
            tasa_bc = 0.0
            politica_bc = "N/A"
            if hasattr(mercado, 'banco_central'):
                tasa_bc = mercado.banco_central.tasa_interes_base
                politica_bc = mercado.banco_central.historial_decisiones[-1]['decision'] if mercado.banco_central.historial_decisiones else "Inicial"
            
            # Ciclo Económico
            fase_economica = "N/A"
            if hasattr(mercado, 'gestor_ciclo'):
                fase_economica = mercado.gestor_ciclo.fase_actual.value
            
            # Rescate Empresarial
            empresas_rescatadas = fusiones = liquidaciones = 0
            if hasattr(mercado, 'gestor_rescate'):
                stats_rescate = mercado.gestor_rescate.obtener_estadisticas_rescate()
                empresas_rescatadas = stats_rescate['rescates_totales']
                fusiones = stats_rescate['fusiones_totales']
                liquidaciones = stats_rescate['liquidaciones_totales']

            local_logger.log_reporte(f"""
REPORTE HIPERREALISTA v3.0 - CICLO {ciclo}/{num_ciclos}:
═══════════════════════════════════════════════════════════
📊 MÉTRICAS PRINCIPALES:
   PIB: ${pib_actual:,.2f} | Inflación: {inflacion_actual*100:.2f}%
   Desempleo: {tasa_desempleo:.1f}% | Empresas Activas: {empresas_activas}
   Transacciones: {transacciones_ciclo} | Modelos ML: {modelos_entrenados}

🏦 SISTEMA BANCARIO:
   Depósitos: ${depositos_totales:,.0f} | Préstamos: ${prestamos_totales:,.0f}
   Tasa Banco Central: {tasa_bc:.2%} | Política: {politica_bc}

🚀 SISTEMAS HIPERREALISTAS:
   Fase Económica: {fase_economica}
   Rescates: {empresas_rescatadas} | Fusiones: {fusiones} | Liquidaciones: {liquidaciones}
   Crisis: {'🔴 Activa' if mercado.crisis_financiera_activa else '🟢 Inactiva'}

👔 MERCADO LABORAL MEJORADO:
   Salario Promedio: ${enhanced_metrics.get('average_wage', 0):,.0f}
   Vacantes Activas: {enhanced_metrics.get('total_vacancies', 0)}
   Tasa de Emparejamiento: {enhanced_metrics.get('match_rate', 0):.1%}
   Crecimiento Salarial: {enhanced_metrics.get('wage_growth', 0):+.1%}
═══════════════════════════════════════════════════════════""")

            # Log reporte detallado (mantener formato original para compatibilidad)
            local_logger.log_reporte(
                f"REPORTE CICLO {ciclo}: PIB=${pib_actual:,.2f}, Inflación={inflacion_actual*100:.2f}%, Desempleo={tasa_desempleo:.1f}%, Empresas={empresas_activas}, Transacciones={transacciones_ciclo}")
            local_logger.log_reporte(
                f"REPORTE CICLO {ciclo}: Depósitos=${depositos_totales:,.0f}, Préstamos=${prestamos_totales:,.0f}, Crisis={'Activa' if mercado.crisis_financiera_activa else 'Inactiva'}")
            local_logger.log_reporte(
                f"REPORTE HIPERREALISTA CICLO {ciclo}: TasaBC={tasa_bc:.2f}%, Fase={fase_economica}, Rescates={empresas_rescatadas}, Fusiones={fusiones}, Liquidaciones={liquidaciones}")

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

    # === FINALIZACIÓN DEL SISTEMA DE IA ===
    if hasattr(mercado, 'sistema_ia') and mercado.sistema_ia is not None:
        try:
            local_logger.log_sistema("🤖 Finalizando Sistema de Agentes IA...")
            mercado.sistema_ia.finalizar()
            local_logger.log_sistema("   ✅ Sistema IA finalizado correctamente")
        except Exception as e:
            local_logger.log_error(f"   ❌ Error finalizando sistema IA: {e}")

    # === RESULTADOS FINALES ===
    local_logger.log_sistema("Generando resultados finales de la simulación")
    generar_resultados_finales(mercado, tiempo_total, num_ciclos, prefijo_resultados=prefijo_resultados)

    # Log final de cierre
    local_logger.log_fin(
        "Simulación Económica Avanzada v3.0 completada exitosamente")

    return mercado


def generar_resultados_finales(mercado, tiempo_total, num_ciclos, prefijo_resultados: str | None = None):
    """Genera y guarda todos los resultados finales"""
    logger.log_sistema("GENERANDO RESULTADOS FINALES...")

    # === DASHBOARD COMPLETO ===
    mercado.dashboard.crear_dashboard_completo(
        num_ciclos, guardar_archivo=True, prefijo=prefijo_resultados)

    # === REPORTE TEXTUAL ===
    logger.log_reporte("Reporte textual generado:")
    logger.log_reporte(mercado.dashboard.generar_reporte_textual())

    # === EXPORTAR DATOS ===
    prefijo = prefijo_resultados or "simulacion_v2_1"
    csv_file, json_file, reporte_file = exportar_resultados_completos(
        mercado.dashboard, prefijo=prefijo
    )

    # === ESTADÍSTICAS ADICIONALES ===
    logger.log_sistema("ESTADÍSTICAS TÉCNICAS v3.0:")
    logger.log_sistema(f"   Tiempo total: {tiempo_total:.2f}s")
    logger.log_sistema(
        f"   Velocidad promedio: {tiempo_total/num_ciclos:.3f}s/ciclo")
    logger.log_sistema(f"   Agentes totales: {len(mercado.personas)}")
    logger.log_sistema(f"   Tipos de bienes: {len(mercado.bienes)}")
    logger.log_sistema(
        f"   Transacciones totales: {len(mercado.transacciones)}")

    # === ESTADÍSTICAS HIPERREALISTAS ===
    logger.log_sistema("ESTADÍSTICAS HIPERREALISTAS:")
    
    # Banco Central
    if hasattr(mercado, 'banco_central'):
        decisiones_bc = len(mercado.banco_central.historial_decisiones)
        tasa_final = mercado.banco_central.tasa_interes_base
        logger.log_sistema(f"   🏦 Banco Central - Decisiones: {decisiones_bc}, Tasa final: {tasa_final:.2%}")
    
    # Ciclo Económico
    if hasattr(mercado, 'gestor_ciclo'):
        transiciones = mercado.gestor_ciclo.contador_transiciones
        fase_final = mercado.gestor_ciclo.fase_actual.value
        logger.log_sistema(f"   📊 Ciclo Económico - Transiciones: {transiciones}, Fase final: {fase_final}")
    
    # Rescate Empresarial
    if hasattr(mercado, 'gestor_rescate'):
        stats_rescate = mercado.gestor_rescate.obtener_estadisticas_rescate()
        logger.log_sistema(f"   🚑 Rescate Empresarial - Rescates: {stats_rescate['rescates_totales']}, "
                          f"Fusiones: {stats_rescate['fusiones_totales']}, Liquidaciones: {stats_rescate['liquidaciones_totales']}")
    
    # NUEVO: Sistema Fiscal
    if hasattr(mercado, 'sistema_fiscal'):
        stats_fiscal = mercado.sistema_fiscal.obtener_estadisticas_fiscales()
        logger.log_sistema(f"   💰 Sistema Fiscal - Recaudación: ${stats_fiscal['recaudacion_total']:,.0f}")
        logger.log_sistema(f"      Presión Fiscal/PIB: {stats_fiscal['presion_fiscal_pib']:.1%}")
        logger.log_sistema(f"      Déficit Fiscal: ${stats_fiscal['deficit_fiscal']:,.0f}")
        logger.log_sistema(f"      Deuda/PIB: {stats_fiscal['deuda_publica']/(mercado.pib_historico[-1] if mercado.pib_historico else 1):.1%}")
        logger.log_sistema(f"      Política Actual: {stats_fiscal['politica_actual']}")
    
    # NUEVO: Mercado de Capitales
    if hasattr(mercado, 'bolsa_valores'):
        stats_bolsa = mercado.bolsa_valores.obtener_estadisticas_mercado()
        logger.log_sistema(f"   📈 Bolsa de Valores - Acciones: {stats_bolsa['acciones_listadas']}")
        logger.log_sistema(f"      Cap. Total: ${stats_bolsa['capitalizacion_total']:,.0f}")
        logger.log_sistema(f"      Rendimiento Promedio: {stats_bolsa['rendimiento_promedio']:.1%}")
        logger.log_sistema(f"      Sentimiento: {stats_bolsa['sentimiento_mercado']:.2f}")
        logger.log_sistema(f"      Burbuja Activa: {'Sí' if stats_bolsa['en_burbuja'] else 'No'}")
    
    # NUEVO: Sistema de Clases Sociales
    if hasattr(mercado, 'sistema_clases'):
        stats_social = mercado.sistema_clases.obtener_estadisticas_sociales()
        logger.log_sistema(f"   👥 Clases Sociales - Coef. Gini: {stats_social['coeficiente_gini']:.3f}")
        logger.log_sistema(f"      Ratio 90/10: {stats_social['ratio_90_10']:.1f}")
        logger.log_sistema(f"      Movilidad Total: {stats_social['movimientos_historicos_total']}")
        logger.log_sistema(f"      Tasa Ascenso: {stats_social['tasa_ascenso_historica']:.1%}")
        
        # Distribución por clase
        distribucion = stats_social['distribucion_clases']
        total_consumidores = sum(distribucion.values())
        if total_consumidores > 0:
            logger.log_sistema(f"      Distribución: Alta {distribucion.get('alta', 0)/total_consumidores:.0%}, "
                              f"Media-Alta {distribucion.get('media_alta', 0)/total_consumidores:.0%}, "
                              f"Media {distribucion.get('media', 0)/total_consumidores:.0%}, "
                              f"Baja {distribucion.get('baja', 0)/total_consumidores:.0%}")
    
    # Control de Precios
    if hasattr(mercado, 'controlador_precios'):
        stats_precios = mercado.controlador_precios.obtener_estadisticas_control()
        logger.log_sistema(f"   💰 Control Precios - Cambios aplicados: {stats_precios['cambios_aplicados']}, "
                          f"Precio promedio: ${stats_precios['precio_promedio_actual']:.2f}")

    # Estadísticas existentes
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

    # --- Persistencia ML: guardar modelos y registrar experimento ---
    try:
        if hasattr(mercado, 'analytics_ml'):
            resumen = mercado.analytics_ml.guardar_modelos('results/ml_models')
            run_path = mercado.analytics_ml.registrar_experimento(
                nombre='simulacion_completa',
                detalles={
                    'tiempo_total': tiempo_total,
                    'num_ciclos': num_ciclos,
                    'pib_final': mercado.pib_historico[-1] if mercado.pib_historico else 0.0
                },
                base_dir='results/ml_runs'
            )
            logger.log_sistema(f"Modelos ML guardados: {resumen.get('modelos_guardados', 0)} en results/ml_models/")
            logger.log_sistema(f"Experimento registrado: {run_path}")
    except Exception as e:
        logger.log_sistema(f"Advertencia: No se pudo guardar modelos ML: {e}")


def main():
    """Función principal mejorada v3.0"""
    logger.log_inicio("SIMULADOR ECONÓMICO HIPERREALISTA v3.0")
    logger.log_inicio("==========================================")
    logger.log_inicio("✅ Sistema ML con garantía de entrenamiento")
    logger.log_inicio("✅ Precios dinámicos implementados")
    logger.log_inicio("✅ Dashboard avanzado con múltiples métricas")
    logger.log_inicio("✅ Configuración externa JSON")
    logger.log_inicio("✅ Crisis financiera mejorada")
    logger.log_inicio("✅ Mercado laboral activado")
    logger.log_inicio("✅ Sistema bancario completamente funcional")
    logger.log_inicio("✅ Sistema de logging avanzado implementado")
    logger.log_inicio("🚀 NUEVO: Banco Central con política monetaria")
    logger.log_inicio("🚀 NUEVO: Control de precios realista")  
    logger.log_inicio("🚀 NUEVO: Ciclos económicos genuinos")
    logger.log_inicio("🚀 NUEVO: Sistema de rescate empresarial")
    logger.log_inicio("🤖 NUEVO v3.0: SISTEMA DE AGENTES IA HIPERREALISTAS")
    logger.log_inicio("=" * 70)

    try:
        # CLI: argumentos de escenario y semilla
        parser = argparse.ArgumentParser(description="Simulador de Mercado Hiperrealista v3.0")
        parser.add_argument("--escenario", type=str, default=None, help="Ruta a archivo JSON de escenario o nombre en carpeta 'escenarios/'")
        parser.add_argument("--seed", type=int, default=None, help="Semilla para aleatoriedad")
        args, unknown = parser.parse_known_args()

        # Semilla determinista opcional (CLI tiene prioridad)
        cli_seed = args.seed

        # Cargar configuración
        logger.log_configuracion("Cargando configuración...")
        logger.log_inicio("Cargando configuración del simulador")
        configurador = ConfiguradorSimulacion()
        # Aplicar seed global desde config o CLI
        configurador.aplicar_seed_global(cli_seed)

        # Si se especifica un escenario, intentar cargarlo
        escenario_nombre = None
        if args.escenario:
            def _deep_merge(base, overlay):
                if not isinstance(base, dict) or not isinstance(overlay, dict):
                    return overlay
                result = dict(base)
                for k, v in overlay.items():
                    if k in result and isinstance(result[k], dict) and isinstance(v, dict):
                        result[k] = _deep_merge(result[k], v)
                    else:
                        result[k] = v
                return result
            ruta = args.escenario
            if not os.path.isabs(ruta) and not os.path.exists(ruta):
                ruta = os.path.join(os.path.dirname(__file__), "escenarios", args.escenario if args.escenario.endswith('.json') else f"{args.escenario}.json")
            if os.path.exists(ruta):
                try:
                    with open(ruta, 'r', encoding='utf-8') as f:
                        escenario_cfg = json.load(f)
                    # Merge profundo sobre config base ya cargada
                    configurador.config = _deep_merge(configurador.config, escenario_cfg)
                    escenario_nombre = os.path.splitext(os.path.basename(ruta))[0]
                    logger.log_configuracion(f"✅ Escenario cargado: {ruta}")
                except Exception as e:
                    logger.log_configuracion(f"⚠️  No se pudo cargar el escenario '{ruta}': {e}. Se usará configuración por defecto.")
            else:
                logger.log_configuracion(f"⚠️  Escenario no encontrado: {ruta}. Se usará configuración por defecto.")

        # Ejecutar simulación
        logger.log_inicio("Iniciando ejecución de simulación hiperrealista")
        prefijo_resultados = None
        if escenario_nombre:
            prefijo_resultados = f"esc_{escenario_nombre}"
            if args.seed is not None:
                prefijo_resultados += f"_seed{args.seed}"

        mercado = ejecutar_simulacion_completa(configurador, prefijo_resultados=prefijo_resultados)

        logger.log_fin(
            "Simulación exitosa - SISTEMA DE AGENTES IA IMPLEMENTADO correctamente")
        logger.log_fin(
            "🎯 SIMULACIÓN ECONÓMICA HIPERREALISTA v3.0 COMPLETADA EXITOSAMENTE")

    except KeyboardInterrupt:
        logger.log_error(
            "Simulación interrumpida por el usuario (KeyboardInterrupt)")
    except Exception as e:
        logger.log_error(f"Error durante la simulación: {e}")
        import traceback
        logger.log_error(f"Traceback completo: {traceback.format_exc()}")
        # Mantenemos el traceback para debug si es necesario
        traceback.print_exc()


if __name__ == "__main__":
    main()
