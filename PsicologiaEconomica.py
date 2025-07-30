"""
Sistema de Psicología Económica y Behavioral Economics
Implementa sesgos cognitivos y decisiones irracionales en agentes económicos
"""
import random
import math
from enum import Enum


class SesgosCognitivos(Enum):
    ANCLAJE = "anclaje"                    # Dependencia del primer precio visto
    # Pérdidas duelen más que ganancias equivalentes
    AVERSION_PERDIDAS = "aversion_perdidas"
    EFECTO_MANADA = "efecto_manada"        # Seguir comportamiento de otros
    # Buscar información que confirme creencias
    SESGO_CONFIRMACION = "sesgo_confirmacion"
    PRESENTE_BIAS = "presente_bias"         # Sobrevaluación del presente vs futuro
    EXCESO_CONFIANZA = "exceso_confianza"  # Sobreestimar habilidades propias
    EFECTO_DOTACION = "efecto_dotacion"    # Sobrevaluación de lo que ya se posee


class PerfilPsicologico:
    """Perfil psicológico que influye en decisiones económicas"""

    def __init__(self):
        # Intensidad de cada sesgo (0.0 a 1.0)
        self.sesgos = {
            SesgosCognitivos.ANCLAJE: random.uniform(0.2, 0.8),
            SesgosCognitivos.AVERSION_PERDIDAS: random.uniform(0.3, 0.9),
            SesgosCognitivos.EFECTO_MANADA: random.uniform(0.1, 0.7),
            SesgosCognitivos.SESGO_CONFIRMACION: random.uniform(0.2, 0.6),
            SesgosCognitivos.PRESENTE_BIAS: random.uniform(0.1, 0.8),
            SesgosCognitivos.EXCESO_CONFIANZA: random.uniform(0.2, 0.7),
            SesgosCognitivos.EFECTO_DOTACION: random.uniform(0.3, 0.8)
        }

        # Características psicológicas generales
        self.tolerancia_riesgo = random.uniform(0.1, 0.9)
        self.paciencia = random.uniform(0.2, 0.9)  # Capacidad de esperar
        self.racionalidad = random.uniform(0.3, 0.9)  # Qué tan racional es
        self.influenciabilidad = random.uniform(0.1, 0.8)

        # Estados emocionales (cambian dinámicamente)
        self.optimismo = random.uniform(0.3, 0.8)
        self.estres_financiero = random.uniform(0.0, 0.3)
        self.satisfaccion_vida = random.uniform(0.4, 0.9)

        # Memoria y aprendizaje
        self.memoria_precios = {}  # Recuerda precios pasados
        self.experiencias_negativas = []  # Malas experiencias de compra
        self.marcas_confiables = set()  # Marcas en las que confía


class SistemaPsicologiaEconomica:
    """Sistema que aplica psicología económica a las decisiones"""

    def __init__(self, mercado):
        self.mercado = mercado
        self.tendencias_sociales = {}  # Qué está "de moda"
        self.noticias_economicas = []  # Noticias que afectan sentimiento
        self.indice_confianza_consumidor = 0.7  # Confianza general

    def aplicar_sesgo_anclaje(self, agente, bien, precio_propuesto):
        """Aplica sesgo de anclaje en decisiones de precio"""
        perfil = agente.perfil_psicologico
        intensidad = perfil.sesgos[SesgosCognitivos.ANCLAJE]

        # Si tiene precio anclado en memoria
        if bien in perfil.memoria_precios:
            precio_anclado = perfil.memoria_precios[bien]

            # El precio "justo" se sesga hacia el anclaje
            precio_percibido = (precio_propuesto * (1 - intensidad) +
                                precio_anclado * intensidad)

            return precio_percibido
        else:
            # Primer precio se convierte en anclaje
            perfil.memoria_precios[bien] = precio_propuesto
            return precio_propuesto

    def aplicar_aversion_perdidas(self, agente, ganancia, perdida):
        """Aplica aversión a las pérdidas en evaluación de utilidad"""
        perfil = agente.perfil_psicologico
        intensidad = perfil.sesgos[SesgosCognitivos.AVERSION_PERDIDAS]

        # Las pérdidas duelen más que las ganancias equivalentes
        factor_perdida = 1 + intensidad  # Pérdidas se sienten 1.5-2x más

        utilidad_ajustada = ganancia - (perdida * factor_perdida)
        return utilidad_ajustada

    def aplicar_efecto_manada(self, agente, decision_tipo, bien=None):
        """Aplica efecto manada en decisiones de compra"""
        perfil = agente.perfil_psicologico
        intensidad = perfil.sesgos[SesgosCognitivos.EFECTO_MANADA]

        if decision_tipo == "compra" and bien:
            # Buscar qué están comprando otros consumidores
            otros_consumidores = [c for c in self.mercado.getConsumidores()
                                  if c != agente]

            if otros_consumidores:
                # Contar compras recientes del bien
                compras_recientes = sum([
                    c.historial_compras.get(bien, 0)
                    for c in otros_consumidores[-10:]  # Últimos 10
                ])

                if compras_recientes > 0:
                    # Aumentar probabilidad de compra por efecto manada
                    factor_manada = 1 + (intensidad * compras_recientes * 0.1)
                    return factor_manada

        return 1.0  # Sin efecto

    def actualizar_estado_emocional(self, agente, evento):
        """Actualiza estado emocional basado en eventos"""
        perfil = agente.perfil_psicologico

        if evento == "compra_exitosa":
            perfil.satisfaccion_vida = min(
                1.0, perfil.satisfaccion_vida + 0.02)
            perfil.optimismo = min(1.0, perfil.optimismo + 0.01)

        elif evento == "compra_fallida":
            perfil.satisfaccion_vida = max(
                0.0, perfil.satisfaccion_vida - 0.03)
            perfil.estres_financiero = min(
                1.0, perfil.estres_financiero + 0.05)

        elif evento == "perdida_empleo":
            perfil.optimismo = max(0.1, perfil.optimismo - 0.2)
            perfil.estres_financiero = min(1.0, perfil.estres_financiero + 0.3)

        elif evento == "ganancia_inesperada":
            perfil.optimismo = min(1.0, perfil.optimismo + 0.1)
            perfil.estres_financiero = max(0.0, perfil.estres_financiero - 0.1)

    def calcular_utilidad_percibida(self, agente, bien, cantidad, precio):
        """Calcula utilidad percibida considerando sesgos"""
        perfil = agente.perfil_psicologico

        # Utilidad base racional
        utilidad_base = agente.satisfaccion_bien.get(bien, 0.5) * cantidad

        # Aplicar sesgo de anclaje al precio
        precio_percibido = self.aplicar_sesgo_anclaje(agente, bien, precio)

        # Efecto dotación (si ya tiene el bien, lo valora más)
        if bien in agente.bienes and len(agente.bienes[bien]) > 0:
            intensidad_dotacion = perfil.sesgos[SesgosCognitivos.EFECTO_DOTACION]
            utilidad_base *= (1 + intensidad_dotacion * 0.2)

        # Sesgo del presente (descontar futuro)
        if perfil.sesgos[SesgosCognitivos.PRESENTE_BIAS] > 0.5:
            # Prefiere satisfacción inmediata
            utilidad_base *= 1.1

        # Efecto del estado emocional
        if perfil.estres_financiero > 0.5:
            utilidad_base *= 0.8  # Reduce utilidad cuando está estresado

        if perfil.optimismo > 0.7:
            utilidad_base *= 1.1  # Aumenta utilidad cuando está optimista

        # Aversión a pérdidas aplicada al costo
        costo_percibido = precio_percibido * cantidad
        perdida_percibida = self.aplicar_aversion_perdidas(
            agente, 0, costo_percibido)

        return utilidad_base + perdida_percibida

    def influencia_social_precios(self, agente, precio_observado, bien):
        """Influencia de observar precios de otros en la percepción"""
        perfil = agente.perfil_psicologico

        # Si ve que otros pagan más, el precio le parece más razonable
        if perfil.influenciabilidad > 0.5:
            otros_precios = []

            # Simular observación de otros consumidores
            for otro in random.sample(self.mercado.getConsumidores(),
                                      min(5, len(self.mercado.getConsumidores()))):
                if bien in otro.historial_compras:
                    # Precio aproximado que pagó (simplificado)
                    precio_otro = precio_observado * random.uniform(0.8, 1.2)
                    otros_precios.append(precio_otro)

            if otros_precios:
                precio_promedio_otros = sum(otros_precios) / len(otros_precios)

                # Ajustar percepción basada en lo que pagan otros
                factor_social = perfil.influenciabilidad * 0.3
                precio_ajustado = (precio_observado * (1 - factor_social) +
                                   precio_promedio_otros * factor_social)

                return precio_ajustado

        return precio_observado

    def generar_shock_psicologico(self, tipo_shock):
        """Genera shocks psicológicos que afectan a todos los agentes"""
        if tipo_shock == "crisis_confianza":
            # Crisis de confianza reduce optimismo general
            for consumidor in self.mercado.getConsumidores():
                perfil = consumidor.perfil_psicologico
                perfil.optimismo = max(0.1, perfil.optimismo - 0.3)
                perfil.estres_financiero = min(
                    1.0, perfil.estres_financiero + 0.2)

                # Aumenta aversión al riesgo
                perfil.tolerancia_riesgo = max(
                    0.1, perfil.tolerancia_riesgo - 0.2)

            self.indice_confianza_consumidor = max(
                0.2, self.indice_confianza_consumidor - 0.3)

        elif tipo_shock == "euforia_mercado":
            # Euforia aumenta optimismo y tolerancia al riesgo
            for consumidor in self.mercado.getConsumidores():
                perfil = consumidor.perfil_psicologico
                perfil.optimismo = min(1.0, perfil.optimismo + 0.2)
                perfil.tolerancia_riesgo = min(
                    0.9, perfil.tolerancia_riesgo + 0.1)

            self.indice_confianza_consumidor = min(
                1.0, self.indice_confianza_consumidor + 0.2)

    def actualizar_tendencias_sociales(self):
        """Actualiza qué bienes están 'de moda'"""
        # Analizar patrones de compra reciente
        compras_por_bien = {}

        # Últimas 50 transacciones
        for transaccion in self.mercado.transacciones[-50:]:
            bien = transaccion['bien']
            if bien not in compras_por_bien:
                compras_por_bien[bien] = 0
            compras_por_bien[bien] += transaccion['cantidad']

        # Los bienes más comprados se vuelven "tendencia"
        if compras_por_bien:
            bien_moda = max(compras_por_bien.items(), key=lambda x: x[1])
            self.tendencias_sociales[bien_moda[0]] = min(1.0,
                                                         self.tendencias_sociales.get(bien_moda[0], 0) + 0.1)

        # Decay de tendencias anteriores
        for bien in list(self.tendencias_sociales.keys()):
            self.tendencias_sociales[bien] = max(
                0, self.tendencias_sociales[bien] - 0.05)
            if self.tendencias_sociales[bien] == 0:
                del self.tendencias_sociales[bien]

    def ciclo_psicologia_economica(self):
        """Ejecuta el ciclo de psicología económica"""
        # Actualizar tendencias sociales
        self.actualizar_tendencias_sociales()

        # Shocks psicológicos aleatorios
        if random.random() < 0.03:  # 3% probabilidad por ciclo
            tipo_shock = random.choice(["crisis_confianza", "euforia_mercado"])
            self.generar_shock_psicologico(tipo_shock)

        # Decay natural del estrés financiero
        for consumidor in self.mercado.getConsumidores():
            perfil = consumidor.perfil_psicologico
            perfil.estres_financiero = max(0, perfil.estres_financiero - 0.02)

            # Regresión del optimismo hacia la media
            media_optimismo = 0.6
            perfil.optimismo += (media_optimismo - perfil.optimismo) * 0.05

        # Actualizar índice de confianza del consumidor
        optimismo_promedio = sum([c.perfil_psicologico.optimismo
                                  for c in self.mercado.getConsumidores()]) / \
            max(1, len(self.mercado.getConsumidores()))

        self.indice_confianza_consumidor = optimismo_promedio * 0.7 + \
            self.indice_confianza_consumidor * 0.3

    def obtener_estadisticas_psicologicas(self):
        """Retorna estadísticas del estado psicológico del mercado"""
        if not self.mercado.getConsumidores():
            return {}

        consumidores = self.mercado.getConsumidores()

        # Promedios de características psicológicas
        stats = {
            'indice_confianza': self.indice_confianza_consumidor,
            'optimismo_promedio': sum([c.perfil_psicologico.optimismo for c in consumidores]) / len(consumidores),
            'estres_promedio': sum([c.perfil_psicologico.estres_financiero for c in consumidores]) / len(consumidores),
            'tolerancia_riesgo_promedio': sum([c.perfil_psicologico.tolerancia_riesgo for c in consumidores]) / len(consumidores),
            'racionalidad_promedio': sum([c.perfil_psicologico.racionalidad for c in consumidores]) / len(consumidores),
            'tendencias_sociales': dict(self.tendencias_sociales)
        }

        # Distribución de sesgos
        for sesgo in SesgosCognitivos:
            valores_sesgo = [c.perfil_psicologico.sesgos[sesgo]
                             for c in consumidores]
            stats[f'{sesgo.value}_promedio'] = sum(
                valores_sesgo) / len(valores_sesgo)

        return stats


def inicializar_perfiles_psicologicos(mercado):
    """Inicializa perfiles psicológicos para todos los agentes existentes"""
    for consumidor in mercado.getConsumidores():
        if not hasattr(consumidor, 'perfil_psicologico'):
            consumidor.perfil_psicologico = PerfilPsicologico()

    # Crear sistema de psicología económica
    sistema_psicologia = SistemaPsicologiaEconomica(mercado)
    mercado.sistema_psicologia = sistema_psicologia

    return sistema_psicologia
