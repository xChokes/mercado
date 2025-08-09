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
from ..systems.CrisisFinanciera import (
    detectar_burbuja_precios,
    evaluar_riesgo_sistemico,
    simular_corrida_bancaria,
)
from ..systems.MercadoLaboral import MercadoLaboral


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

        # Inicializar precios históricos
        for bien in self.bienes:
            self.precios_historicos[bien] = []

    def agregar_persona(self, persona):
        self.personas.append(persona)
        if isinstance(persona, Consumidor):
            self.contador_consumidores += 1

    def calcular_indice_precios(self):
        """Calcula un índice de precios ponderado"""
        precios_actuales = []
        pesos = []

        for empresa in self.getEmpresas():
            for bien, precio in empresa.precios.items():
                categoria = ConfigEconomica.CATEGORIAS_BIENES.get(
                    bien, 'servicios')

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
            indice = sum(
                p * w for p, w in zip(precios_actuales, pesos)) / sum(pesos)
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
        """Registra estadísticas del ciclo actual"""
        # PIB
        pib_ciclo = sum([t['costo_total'] for t in self.transacciones
                        if t.get('ciclo') == self.ciclo_actual])
        self.pib_historico.append(pib_ciclo)

        # Inflación
        indice_actual = self.calcular_indice_precios()
        if len(self.pib_historico) > 1:
            indice_anterior = 100 if len(
                self.pib_historico) == 2 else self.calcular_indice_precios()
            inflacion = (indice_actual / indice_anterior -
                         1) if indice_anterior > 0 else 0
        else:
            inflacion = 0
        self.inflacion_historica.append(inflacion)

        # Desempleo
        self.desempleo_historico.append(self.gobierno.tasa_desempleo)

        # Precios por bien
        for bien in self.bienes:
            precios_bien = [e.precios.get(
                bien, 0) for e in self.getEmpresas() if bien in e.precios]
            precio_promedio = sum(precios_bien) / \
                len(precios_bien) if precios_bien else 0
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

        # 4.5 Evaluar posible crisis financiera e intervenir
        riesgo = evaluar_riesgo_sistemico(self.sistema_bancario)
        burbuja = detectar_burbuja_precios(self)
        if (riesgo > 0.6 or indicadores_gobierno['desempleo'] > 0.2 or burbuja):
            self.crisis_financiera_activa = True
            self.sistema_bancario.banco_central.intervenir_en_crisis(self.sistema_bancario)
            simular_corrida_bancaria(self.sistema_bancario, intensidad=0.1)
        else:
            self.crisis_financiera_activa = False

        # 5. Actualizar competencia
        self.actualizar_nivel_competencia()

        # 6. Ciclos individuales de cada persona
        personas_ordenadas = self.personas[:]
        random.shuffle(personas_ordenadas)  # Orden aleatorio para fairness

        for persona in personas_ordenadas:
            try:
                persona.ciclo_persona(ciclo, self)
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
        self.transacciones.append({
            'consumidor': consumidor.nombre,
            'bien': nombre_bien,
            'cantidad': cantidad,
            'costo_total': costo_total,
            'ciclo': ciclo
        })

    def getRegistroTransacciones(self):
        return self.transacciones
