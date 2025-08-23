import random
import math
from .EmpresaProductora import EmpresaProductora
from .MercadoFinanciero import MercadoFinanciero
from .Consumidor import Consumidor
from .Empresa import Empresa
from .Gobierno import Gobierno
from ..config.ConfigEconomica import ConfigEconomica
from ..systems.SistemaBancario import SistemaBancario
from ..systems.SectoresEconomicos import EconomiaMultisectorial
from ..systems.PsicologiaEconomica import inicializar_perfiles_psicologicos
from ..systems.SistemaInnovacion import SistemaInnovacion
from ..systems.AnalyticsML import SistemaAnalyticsML
from ..systems.ComercioInternacional import Pais, TipoCambio
from ..systems.CrisisFinanciera import (
    detectar_burbuja_precios,
    evaluar_riesgo_sistemico,
    simular_corrida_bancaria,
    evaluar_recuperacion_crisis,
    aplicar_medidas_recuperacion,
)
from ..systems.MercadoLaboral import MercadoLaboral
from ..systems.EstimuloEconomico import ciclo_estimulo_economico


class Mercado:
    def __init__(self, bienes):
        self.bienes = bienes if bienes else {}
        self.personas = []
        self.contador_consumidores = 0
        self.mercado_financiero = MercadoFinanciero()
        self.transacciones = []
        self.gobierno = Gobierno(self)

        # Sistemas avanzados
        self.sistema_bancario = SistemaBancario(self)
        self.economia_sectorial = EconomiaMultisectorial(self)
        self.sistema_innovacion = SistemaInnovacion(self)
        self.mercado_laboral = MercadoLaboral(self)
        self.sistema_psicologia = None  # Se inicializa después
        self.sistema_analytics = SistemaAnalyticsML(self)

        # Comercio internacional
        self.paises = {}
        self.mercados_nacionales = {}
        self.flujos_comerciales = []
        self.tipo_cambio = None

        # Indicadores económicos
        self.ciclo_actual = 0
        self.pib_historico = []
        self.inflacion_historica = []
        self.desempleo_historico = []
        self.precios_historicos = {}

        # Factores macroeconómicos
        # expansion, recesion, depresion, recuperacion
        self.fase_ciclo_economico = 'expansion'
        self.ciclos_en_fase = 0
        self.shock_economico_activo = False
        self.mes_simulacion = 0

        # Estadísticas de mercado
        self.volumen_transacciones = []
        self.empresas_activas = []
        self.nivel_competencia = {}

        # Estado de crisis financiera
        self.crisis_financiera_activa = False
        self.ciclos_en_crisis = 0

        # Inicializar precios históricos
        for bien in self.bienes:
            self.precios_historicos[bien] = []

    def agregar_persona(self, persona):
        self.personas.append(persona)
        if isinstance(persona, Consumidor):
            self.contador_consumidores += 1

    def agregar_pais(self, pais, mercado_nacional=None):
        """Registra un país y opcionalmente su mercado nacional"""
        self.paises[pais.nombre] = pais
        if mercado_nacional:
            self.mercados_nacionales[pais.nombre] = mercado_nacional
            pais.mercado = mercado_nacional

    def registrar_flujo_comercial(self, pais_origen, pais_destino, bien,
                                  cantidad, valor):
        """Registra un flujo de comercio internacional"""
        registro = {
            'origen': pais_origen.nombre,
            'destino': pais_destino.nombre,
            'bien': bien,
            'cantidad': cantidad,
            'valor': valor
        }
        self.flujos_comerciales.append(registro)
        pais_origen.balanza_comercial += valor
        pais_destino.balanza_comercial -= valor
        return registro

    def realizar_transaccion_internacional(self, exportador, importador,
                                           bien, cantidad, precio,
                                           pais_origen, pais_destino):
        """Procesa una transacción internacional entre agentes"""
        if not self.tipo_cambio:
            raise ValueError("Sistema de tipo de cambio no inicializado")

        valor_origen = precio * cantidad
        valor_destino = self.tipo_cambio.convertir(
            valor_origen, pais_origen.moneda, pais_destino.moneda)

        costo_transporte = valor_destino * ConfigEconomica.COSTO_TRANSPORTE_BASE
        arancel = valor_destino * pais_destino.obtener_arancel(
            pais_origen.nombre)
        total_costo = valor_destino + costo_transporte + arancel

        if importador.dinero < total_costo:
            return False

        importador.dinero -= total_costo
        exportador.dinero += valor_origen
        self.registrar_flujo_comercial(
            pais_origen, pais_destino, bien, cantidad, valor_origen)
        return True

    def calcular_indice_precios(self):
        """Calcula un índice de precios ponderado con controles anti-volatilidad"""
        precios_actuales = []
        pesos = []

        for empresa in self.getEmpresas():
            for bien, precio in empresa.precios.items():
                # CONTROL: Filtrar precios extremos que pueden distorsionar el índice
                if precio <= 0 or precio > 1000000:  # Filtrar precios irreales
                    continue
                    
                categorias_map = getattr(ConfigEconomica, 'CATEGORIAS_BIENES_MAP', None)
                if isinstance(categorias_map, dict):
                    categoria = categorias_map.get(bien, 'servicios')
                else:
                    categoria = 'servicios'

                # Peso basado en importancia del bien
                if categoria == 'alimentos_basicos':
                    peso = 3.0
                elif categoria == 'alimentos_lujo':
                    peso = 1.5
                else:
                    peso = 1.0

                precios_actuales.append(precio)
                pesos.append(peso)

        if precios_actuales:
            if sum(pesos) > 0:
                # Calcular índice ponderado
                indice = sum(
                    p * w for p, w in zip(precios_actuales, pesos)) / sum(pesos)
                
                # NUEVO: Suavizar el índice para evitar cambios extremos
                if hasattr(self, 'indice_anterior') and self.indice_anterior > 0:
                    # Limitar variación del índice de precios a máximo 10% por ciclo
                    ratio_cambio = indice / self.indice_anterior
                    if ratio_cambio > 1.10:  # Subida > 10%
                        indice = self.indice_anterior * 1.10
                    elif ratio_cambio < 0.90:  # Bajada > 10%
                        indice = self.indice_anterior * 0.90
                
                self.indice_anterior = indice
            else:
                indice = 0
            return indice
        return 100  # Índice base

    def detectar_fase_ciclo_economico(self):
        """Detecta y actualiza la fase del ciclo económico"""
        if len(self.pib_historico) < 4:  # Necesitamos historial mínimo
            return

        # Calcular tendencia del PIB (últimos 4 períodos)
        pib_reciente = self.pib_historico[-4:]
        tendencia = (pib_reciente[-1] - pib_reciente[0]) / \
            pib_reciente[0] if pib_reciente[0] > 0 else 0

        # Calcular desempleo actual
        desempleo_actual = self.gobierno.tasa_desempleo

        # Lógica de transición de fases
        if self.fase_ciclo_economico == 'expansion':
            if tendencia < -0.02 or desempleo_actual > 0.08:  # 2% caída PIB o 8% desempleo
                self.fase_ciclo_economico = 'recesion'
                self.ciclos_en_fase = 0
        elif self.fase_ciclo_economico == 'recesion':
            if desempleo_actual > 0.15 or tendencia < -0.05:  # Crisis severa
                self.fase_ciclo_economico = 'depresion'
                self.ciclos_en_fase = 0
            elif tendencia > 0.01 and desempleo_actual < 0.06:  # Recuperación
                self.fase_ciclo_economico = 'recuperacion'
                self.ciclos_en_fase = 0
        elif self.fase_ciclo_economico == 'depresion':
            if tendencia > 0.005:  # Cualquier crecimiento positivo
                self.fase_ciclo_economico = 'recuperacion'
                self.ciclos_en_fase = 0
        elif self.fase_ciclo_economico == 'recuperacion':
            if tendencia > 0.03 and desempleo_actual < 0.05:  # Crecimiento sólido
                self.fase_ciclo_economico = 'expansion'
                self.ciclos_en_fase = 0

    def aplicar_efectos_ciclo_economico(self):
        """Aplica efectos del ciclo económico a todos los agentes"""
        factor_ciclo = 1.0

        if self.fase_ciclo_economico == 'expansion':
            factor_ciclo = 1.1  # 10% más actividad
        elif self.fase_ciclo_economico == 'recesion':
            factor_ciclo = 0.9   # 10% menos actividad
        elif self.fase_ciclo_economico == 'depresion':
            factor_ciclo = 0.8   # 20% menos actividad
        elif self.fase_ciclo_economico == 'recuperacion':
            factor_ciclo = 1.05  # 5% más actividad

        # Aplicar a consumidores
        for consumidor in self.getConsumidores():
            if self.fase_ciclo_economico in ['recesion', 'depresion']:
                # Aumentar probabilidad de desempleo
                if consumidor.empleado and random.random() < 0.05:
                    consumidor.perder_empleo()
                # Reducir propensión al consumo
                consumidor.propension_consumo *= 0.95
            elif self.fase_ciclo_economico == 'expansion':
                # Aumentar propensión al consumo
                consumidor.propension_consumo = min(
                    0.95, consumidor.propension_consumo * 1.02)

        # Aplicar a empresas
        for empresa in self.getEmpresas():
            if hasattr(empresa, 'eficiencia_produccion'):
                empresa.eficiencia_produccion *= factor_ciclo
                # Limitar entre 0.5 y 1.2
                empresa.eficiencia_produccion = max(
                    0.5, min(1.2, empresa.eficiencia_produccion))

    def simular_shock_economico(self):
        """Simula shocks económicos aleatorios"""
        if not self.shock_economico_activo and random.random() < 0.02:  # 2% probabilidad por ciclo
            tipo_shock = random.choice(
                ['inflacionario', 'deflacionario', 'financiero', 'oferta'])
            intensidad = random.uniform(0.8, 1.5)

            if tipo_shock == 'inflacionario':
                # Aumentar todos los costos de producción
                for empresa in self.getEmpresas():
                    if hasattr(empresa, 'costos_unitarios'):
                        for bien in empresa.costos_unitarios:
                            empresa.costos_unitarios[bien] *= intensidad

            elif tipo_shock == 'deflacionario':
                # Reducir demanda general
                for consumidor in self.getConsumidores():
                    # Reducir consumo
                    consumidor.propension_consumo *= (2 - intensidad)

            elif tipo_shock == 'financiero':
                # Crisis de liquidez
                for persona in self.personas:
                    persona.dinero *= (2 - intensidad)

            elif tipo_shock == 'oferta':
                # Reducir capacidades de producción
                for empresa in self.getEmpresas():
                    if hasattr(empresa, 'capacidad_produccion'):
                        for bien in empresa.capacidad_produccion:
                            empresa.capacidad_produccion[bien] = int(
                                empresa.capacidad_produccion[bien] * (2 - intensidad))

            self.shock_economico_activo = True
            self.ciclos_shock = 5  # Duración del shock

        elif self.shock_economico_activo:
            self.ciclos_shock -= 1
            if self.ciclos_shock <= 0:
                self.shock_economico_activo = False

    def actualizar_nivel_competencia(self):
        """Calcula nivel de competencia por bien"""
        for bien in self.bienes:
            empresas_compitiendo = len([e for e in self.getEmpresas()
                                        if bien in e.bienes and len(e.bienes[bien]) > 0])

            if empresas_compitiendo > 1:
                # Calcular HHI (Herfindahl-Hirschman Index) simplificado
                market_shares = []
                total_stock = sum([len(e.bienes.get(bien, []))
                                  for e in self.getEmpresas()])

                if total_stock > 0:
                    for empresa in self.getEmpresas():
                        stock = len(empresa.bienes.get(bien, []))
                        share = stock / total_stock
                        market_shares.append(share)

                    hhi = sum([share ** 2 for share in market_shares])

                    # Convertir HHI a nivel de competencia (0-1, donde 1 es muy competitivo)
                    competencia = 1 - hhi
                else:
                    competencia = 0
            else:
                competencia = 0  # Monopolio o no hay empresas

            self.nivel_competencia[bien] = competencia

    def generar_nuevos_consumidores(self):
        """Genera nuevos consumidores según la tasa de crecimiento poblacional"""
        tasa_mensual = ConfigEconomica.CRECIMIENTO_POBLACION_ANUAL / 12
        cantidad = int(len(self.getConsumidores()) * tasa_mensual)
        for _ in range(cantidad):
            self.contador_consumidores += 1
            nombre = f"Consumidor{self.contador_consumidores:03d}"
            nuevo = Consumidor(nombre, self)
            self.agregar_persona(nuevo)

    def retirar_consumidores(self):
        """Retira consumidores mayores o inactivos"""
        tasa_mensual = ConfigEconomica.CRECIMIENTO_POBLACION_ANUAL / 12
        cantidad = int(len(self.getConsumidores()) * tasa_mensual * 0.5)
        if cantidad <= 0:
            return
        candidatos = [c for c in self.getConsumidores()
                      if c.estado_demografico == 'jubilado']
        candidatos.sort(key=lambda c: c.edad, reverse=True)
        for consumidor in candidatos[:cantidad]:
            if consumidor.empleado:
                consumidor.perder_empleo()
            self.personas.remove(consumidor)

    def actualizar_demografia(self):
        """Actualiza la demografía del mercado"""
        for consumidor in self.getConsumidores():
            consumidor.envejecer()
        self.generar_nuevos_consumidores()
        self.retirar_consumidores()

    def registrar_estadisticas(self):
        """Registra estadísticas del ciclo actual con cálculo de PIB mejorado"""
        # PIB - Método mejorado que incluye toda la actividad económica
        pib_consumo = 0
        pib_inversion = 0
        pib_gasto_gobierno = 0

        # 1. CONSUMO: Transacciones del ciclo actual
        if hasattr(self, 'transacciones_ciclo_actual'):
            pib_consumo = sum([t.get('costo_total', 0)
                              for t in self.transacciones_ciclo_actual])
            self.transacciones_ciclo_actual = []  # Resetear para próximo ciclo
        else:
            transacciones_ciclo = [t for t in self.transacciones if t.get(
                'ciclo') == self.ciclo_actual]
            pib_consumo = sum([t.get('costo_total', 0)
                              for t in transacciones_ciclo])

        # 2. INVERSIÓN: Actividad empresarial y producción
        for empresa in self.getEmpresas():
            if hasattr(empresa, 'dinero') and empresa.dinero > 0:
                # Aproximar inversión como % del capital empresarial
                pib_inversion += empresa.dinero * 0.05  # 5% de inversión

            # Agregar valor de inventario como producción
            if hasattr(empresa, 'bienes'):
                for bien, lista_bien in empresa.bienes.items():
                    precio_bien = empresa.precios.get(bien, 10)
                    # 10% del valor de inventario
                    pib_inversion += len(lista_bien) * precio_bien * 0.1

        # 3. GASTO GUBERNAMENTAL: Presupuesto del gobierno
        if hasattr(self, 'gobierno') and self.gobierno:
            pib_gasto_gobierno = getattr(
                self.gobierno, 'gasto_ciclo_actual', 0)
            if pib_gasto_gobierno == 0:
                # Aproximar gasto gubernamental
                pib_gasto_gobierno = getattr(
                    self.gobierno, 'presupuesto', 0) * 0.1  # 10% del presupuesto

        # 4. PIB TOTAL con factor de escala realista
        pib_base = pib_consumo + pib_inversion + pib_gasto_gobierno

        # Factor de multiplicador económico (aproximadamente 1.5-2.0)
        multiplicador = 1.8
        pib_ciclo = pib_base * multiplicador

        # Asegurar PIB mínimo realista
        num_agentes = len(self.personas)
        pib_minimo = num_agentes * 50  # $50 por agente como mínimo
        pib_ciclo = max(pib_ciclo, pib_minimo)

        self.pib_historico.append(pib_ciclo)

        # Inflación con índice de precios mejorado
        indices_precios = getattr(self, 'indices_precios_historicos', [])
        indice_actual = self.calcular_indice_precios()
        indices_precios.append(indice_actual)
        self.indices_precios_historicos = indices_precios

        if len(indices_precios) > 1:
            indice_anterior = indices_precios[-2]
            if indice_anterior > 1:
                inflacion_bruta = (indice_actual / indice_anterior - 1)
                
                # NUEVO: Suavizar la inflación calculada para evitar extremos
                # Limitar inflación a ±15% por ciclo como máximo absoluto
                inflacion = max(-0.15, min(0.15, inflacion_bruta))
                
                # Si la inflación es muy alta, aplicar suavizado adicional
                if abs(inflacion) > 0.08:  # Si inflación > 8%
                    # Promediar con inflación anterior para suavizar
                    if len(self.inflacion_historica) > 0:
                        inflacion_anterior = self.inflacion_historica[-1]
                        inflacion = (inflacion * 0.7 + inflacion_anterior * 0.3)
            else:
                inflacion = 0
        else:
            inflacion = 0
        self.inflacion_historica.append(inflacion)

        # Desempleo
        self.desempleo_historico.append(self.gobierno.tasa_desempleo)

        # Precios por bien
        # Primero, recopilar todos los bienes que las empresas manejan actualmente
        todos_los_bienes = set(self.bienes)
        for empresa in self.getEmpresas():
            todos_los_bienes.update(empresa.precios.keys())
        
        for bien in todos_los_bienes:
            precios_bien = [e.precios.get(
                bien, 0) for e in self.getEmpresas() if bien in e.precios]
            precio_promedio = sum(precios_bien) / \
                len(precios_bien) if len(precios_bien) > 0 else 0
            
            # Asegurar que el bien existe en precios_historicos
            if bien not in self.precios_historicos:
                self.precios_historicos[bien] = []
            
            self.precios_historicos[bien].append(precio_promedio)

        # Volumen de transacciones
        transacciones_ciclo = len(
            [t for t in self.transacciones if t.get('ciclo') == self.ciclo_actual])
        self.volumen_transacciones.append(transacciones_ciclo)

    def ejecutar_ciclo(self, ciclo):
        """Ejecuta un ciclo completo del mercado con todos los efectos macroeconómicos"""
        self.ciclo_actual = ciclo
        self.mes_simulacion += 1
        self.ciclos_en_fase += 1

        # Inicializar contadores del ciclo actual
        self.volumen_ciclo_actual = 0
        if not hasattr(self, 'transacciones_ciclo_actual'):
            self.transacciones_ciclo_actual = []
        else:
            self.transacciones_ciclo_actual = []

        # 1. Efectos macroeconómicos tradicionales
        self.detectar_fase_ciclo_economico()
        self.aplicar_efectos_ciclo_economico()
        self.simular_shock_economico()

        # 2. Inicializar sistemas avanzados si es el primer ciclo
        if ciclo == 0:
            self.sistema_psicologia = inicializar_perfiles_psicologicos(self)
            self.economia_sectorial.asignar_empresas_a_sectores()

        # 3. Ciclos de sistemas avanzados
        self.sistema_bancario.ciclo_bancario()
        self.economia_sectorial.ciclo_economico_sectorial()
        self.sistema_innovacion.ciclo_innovacion()
        self.sistema_analytics.ciclo_analytics()
        if self.sistema_psicologia:
            self.sistema_psicologia.ciclo_psicologia_economica()

        # 4. Ciclo del gobierno (políticas, impuestos, regulación)
        indicadores_gobierno = self.gobierno.ciclo_gobierno(ciclo)

        # 4.5 Gestionar crisis financiera con mecanismos de recuperación
        riesgo = evaluar_riesgo_sistemico(self.sistema_bancario)
        burbuja = detectar_burbuja_precios(self)

        # Determinar si activar crisis
        if (riesgo > 0.6 or indicadores_gobierno['desempleo'] > 0.2 or burbuja):
            if not self.crisis_financiera_activa:
                self.crisis_financiera_activa = True
                self.ciclos_en_crisis = 0
            self.ciclos_en_crisis += 1
            self.sistema_bancario.banco_central.intervenir_en_crisis(
                self.sistema_bancario)
            simular_corrida_bancaria(self.sistema_bancario, intensidad=0.1)

            # Aplicar medidas de recuperación cada 3 ciclos en crisis
            if self.ciclos_en_crisis % 3 == 0:
                aplicar_medidas_recuperacion(self)

        # Evaluar si terminar crisis
        if self.crisis_financiera_activa and evaluar_recuperacion_crisis(self):
            self.crisis_financiera_activa = False
            self.ciclos_en_crisis = 0
            print("🎉 CRISIS FINANCIERA RESUELTA - Economía en recuperación")

        # 5. Actualizar competencia
        self.actualizar_nivel_competencia()

        # 6. Ejecutar ciclo del mercado laboral mejorado
        self.mercado_laboral.ciclo_mercado_laboral()

        # 6.5. Ejecutar sistema de estímulo económico
        ciclo_estimulo_economico(self)

        # 7. Ciclos individuales de cada persona
        personas_ordenadas = self.personas[:]
        random.shuffle(personas_ordenadas)  # Orden aleatorio para fairness

        for persona in personas_ordenadas:
            try:
                persona.ciclo_persona(ciclo, self)
            except ZeroDivisionError as e:
                print(
                    f"Error en ciclo de {getattr(persona, 'nombre', 'Persona desconocida')}: float division by zero - {e}")
                # Intentar corregir automáticamente algunos errores comunes
                if hasattr(persona, 'precios'):
                    for bien, precio in persona.precios.items():
                        if precio <= 0:
                            # Precio mínimo de seguridad
                            persona.precios[bien] = 1
                if hasattr(persona, 'acciones_emitidas') and persona.acciones_emitidas <= 0:
                    persona.acciones_emitidas = 1  # Evitar división por cero en acciones
            except Exception as e:
                print(
                    f"Error en ciclo de {getattr(persona, 'nombre', 'Persona desconocida')}: {e}")

        # 7. Registrar estadísticas
        self.registrar_estadisticas()

        # 8. Información del ciclo
        if ciclo % 5 == 0:  # Cada 5 ciclos mostrar resumen
            self.imprimir_resumen_economico()

    def imprimir_resumen_economico(self):
        """Imprime un resumen del estado económico"""
        pib_actual = self.pib_historico[-1] if self.pib_historico else 0
        inflacion_actual = self.inflacion_historica[-1] if self.inflacion_historica else 0
        desempleo_actual = self.desempleo_historico[-1] if self.desempleo_historico else 0

        print(f"\n--- RESUMEN ECONÓMICO (Ciclo {self.ciclo_actual}) ---")
        print(f"PIB: ${pib_actual:,.2f}")
        print(f"Inflación: {inflacion_actual:.2%}")
        print(f"Desempleo: {desempleo_actual:.2%}")
        print(f"Fase económica: {self.fase_ciclo_economico}")
        print(f"Empresas activas: {len(self.getEmpresas())}")
        print(f"Consumidores: {len(self.getConsumidores())}")
        if self.shock_economico_activo:
            print("⚠️  SHOCK ECONÓMICO ACTIVO")
        if self.crisis_financiera_activa:
            print("⚠️  CRISIS FINANCIERA ACTIVA")
        print("-" * 50)

    def obtener_estadisticas_completas(self):
        """Retorna estadísticas completas del mercado incluyendo sistemas avanzados"""
        stats_base = {
            'pib_historico': self.pib_historico[:],
            'inflacion_historica': self.inflacion_historica[:],
            'desempleo_historico': self.desempleo_historico[:],
            'precios_historicos': {k: v[:] for k, v in self.precios_historicos.items()},
            'volumen_transacciones': self.volumen_transacciones[:],
            'fase_ciclo_actual': self.fase_ciclo_economico,
            'nivel_competencia': self.nivel_competencia.copy(),
            'shock_activo': self.shock_economico_activo,
            'crisis_financiera': self.crisis_financiera_activa
        }

        # Agregar estadísticas de sistemas avanzados
        stats_base['sistema_bancario'] = self.sistema_bancario.obtener_estadisticas_sistema()
        stats_base['sectores_economicos'] = self.economia_sectorial.obtener_estadisticas_sectoriales()
        stats_base['estructura_economica'] = self.economia_sectorial.obtener_resumen_estructural()
        stats_base['innovacion'] = self.sistema_innovacion.obtener_estadisticas_innovacion()
        stats_base['analytics_ml'] = self.sistema_analytics.obtener_estadisticas_analytics()

        if self.sistema_psicologia:
            stats_base['psicologia_economica'] = self.sistema_psicologia.obtener_estadisticas_psicologicas()

        return stats_base

    def getDineroConsumidores(self):
        return [c.dinero for c in self.personas if isinstance(c, Consumidor)]

    def getDineroEmpresas(self):
        return [e.dinero for e in self.personas if isinstance(e, Empresa)]

    def getConsumidores(self):
        return [c for c in self.personas if isinstance(c, Consumidor)]

    def getEmpresas(self):
        return [e for e in self.personas if isinstance(e, (Empresa, EmpresaProductora))]

    def getPersonas(self):
        return self.personas

    def registrar_transaccion(self, consumidor, nombre_bien, cantidad, costo_total, ciclo):
        transaccion = {
            'consumidor': consumidor.nombre,
            'bien': nombre_bien,
            'cantidad': cantidad,
            'costo_total': costo_total,
            'ciclo': ciclo
        }
        self.transacciones.append(transaccion)

        # Registrar para PIB del ciclo actual
        if not hasattr(self, 'transacciones_ciclo_actual'):
            self.transacciones_ciclo_actual = []
        if not hasattr(self, 'volumen_ciclo_actual'):
            self.volumen_ciclo_actual = 0

        if ciclo == self.ciclo_actual:
            self.transacciones_ciclo_actual.append(transaccion)
            self.volumen_ciclo_actual += costo_total

    def getRegistroTransacciones(self):
        return self.transacciones
