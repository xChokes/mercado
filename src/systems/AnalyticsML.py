"""
Sistema de Analytics y Machine Learning para optimización económica
Implementa predicción de demanda, optimización de precios y análisis de agentes
"""
import random
import math
import numpy as np
from collections import defaultdict
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')


class PredictorDemanda:
    """Predictor de demanda usando técnicas de Machine Learning"""

    def __init__(self):
        self.modelo = LinearRegression()
        self.scaler = StandardScaler()
        self.historial_entrenamiento = []
        self.caracteristicas_entrenadas = False

    def extraer_caracteristicas(self, mercado, bien):
        """Extrae características para predicción de demanda"""
        caracteristicas = []

        # Precios históricos
        if bien in mercado.precios_historicos and mercado.precios_historicos[bien]:
            precios = mercado.precios_historicos[bien][-5:]  # Últimos 5 ciclos
            precio_promedio = sum(precios) / len(precios)
            caracteristicas.append(precio_promedio)

            # Tendencia de precios
            if len(precios) >= 2:
                tendencia = (precios[-1] - precios[0]) / len(precios)
                caracteristicas.append(tendencia)
            else:
                caracteristicas.append(0)
        else:
            caracteristicas.extend([10.0, 0])  # Valores por defecto

        # Factores económicos
        pib_actual = mercado.pib_historico[-1] if mercado.pib_historico else 100000
        caracteristicas.append(pib_actual / 100000)  # Normalizado

        desempleo = mercado.desempleo_historico[-1] if mercado.desempleo_historico else 0.05
        caracteristicas.append(desempleo)

        inflacion = mercado.inflacion_historica[-1] if mercado.inflacion_historica else 0.02
        caracteristicas.append(inflacion)

        # Fase del ciclo económico (codificada)
        fases = {'expansion': 1, 'recesion': 0.3,
                 'depresion': 0, 'recuperacion': 0.7}
        caracteristicas.append(fases.get(mercado.fase_ciclo_economico, 0.5))

        # Estacionalidad (basada en ciclo)
        ciclo_mod = mercado.ciclo_actual % 12  # Simular estacionalidad anual
        caracteristicas.append(math.sin(2 * math.pi * ciclo_mod / 12))
        caracteristicas.append(math.cos(2 * math.pi * ciclo_mod / 12))

        return caracteristicas

    def entrenar(self, mercado, bien):
        """Entrena el modelo con datos históricos mejorados - SIEMPRE USA DATOS SINTÉTICOS"""
        X = []
        y = []

        # MEJORADO: Siempre generar datos sintéticos para garantizar entrenamiento
        try:
            # Usar datos históricos si existen
            if len(mercado.transacciones) >= 5:
                for i in range(max(0, len(mercado.transacciones) - 30), len(mercado.transacciones)):
                    transaccion = mercado.transacciones[i]
                    if transaccion.get('bien') == bien:
                        caracteristicas = self._simular_caracteristicas_historicas(
                            mercado, bien, i)
                        cantidad = transaccion.get('cantidad', 1)

                        if all(isinstance(x, (int, float)) and not np.isnan(x) for x in caracteristicas):
                            X.append(caracteristicas)
                            y.append(cantidad)

            # SIEMPRE complementar con datos sintéticos para garantizar suficientes datos
            X_sinteticos, y_sinteticos = self._generar_datos_complementarios(
                mercado, bien, 25)
            X.extend(X_sinteticos)
            y.extend(y_sinteticos)

            # Ahora debemos tener suficientes datos
            if len(X) >= 10:
                X_scaled = self.scaler.fit_transform(X)
                self.modelo.fit(X_scaled, y)
                self.caracteristicas_entrenadas = True
                return True
            else:
                # Fallback: usar solo datos sintéticos puros
                return self._generar_datos_sinteticos_y_entrenar(mercado, bien)

        except Exception as e:
            # Si falla todo, usar método sintético puro que siempre funciona
            print(
                f"Entrenamiento híbrido falló para {bien}, usando sintético puro: {e}")
            return self._generar_datos_sinteticos_y_entrenar(mercado, bien)

    def _generar_datos_sinteticos_y_entrenar(self, mercado, bien, num_puntos=20):
        """Genera datos sintéticos realistas para entrenar el modelo"""
        X = []
        y = []

        for i in range(num_puntos):
            # Características sintéticas realistas
            precio = random.uniform(5, 50)
            pib_factor = random.uniform(0.8, 1.2)
            desempleo = random.uniform(0.05, 0.25)
            inflacion = random.uniform(-0.05, 0.1)
            fase_economica = random.uniform(0, 1)
            estacionalidad_sin = random.uniform(-0.5, 0.5)
            estacionalidad_cos = random.uniform(-0.5, 0.5)
            tendencia = random.uniform(-2, 2)

            caracteristicas = [precio, tendencia, pib_factor, desempleo, inflacion,
                               fase_economica, estacionalidad_sin, estacionalidad_cos]

            # Demanda sintética basada en lógica económica
            elasticidad_precio = -0.8  # Demanda disminuye con precio
            demanda_base = 20
            demanda = demanda_base * \
                (precio ** elasticidad_precio) * pib_factor * (1 - desempleo)
            demanda = max(1, int(demanda + random.uniform(-5, 5)))

            X.append(caracteristicas)
            y.append(demanda)

        try:
            X_scaled = self.scaler.fit_transform(X)
            self.modelo.fit(X_scaled, y)
            self.caracteristicas_entrenadas = True
            return True
        except:
            return False

    def _generar_datos_complementarios(self, mercado, bien, num_puntos):
        """Genera datos complementarios para mejorar el entrenamiento"""
        X = []
        y = []

        for _ in range(num_puntos):
            # Variaciones alrededor de las condiciones actuales
            caracteristicas_base = self.extraer_caracteristicas(mercado, bien)
            caracteristicas_variadas = []

            for caracteristica in caracteristicas_base:
                if isinstance(caracteristica, (int, float)) and not np.isnan(caracteristica):
                    variacion = caracteristica * random.uniform(0.7, 1.3)
                    caracteristicas_variadas.append(variacion)
                else:
                    caracteristicas_variadas.append(random.uniform(0, 1))

            # Asegurar 8 características (mismo formato que extraer_caracteristicas)
            while len(caracteristicas_variadas) < 8:
                caracteristicas_variadas.append(random.uniform(0, 1))
            caracteristicas_variadas = caracteristicas_variadas[:8]

            # Demanda basada en lógica económica realista
            precio = caracteristicas_variadas[0]
            pib_factor = caracteristicas_variadas[2]
            desempleo = caracteristicas_variadas[3]

            # Elasticidad precio-demanda realista
            demanda_base = 25
            elasticidad = -0.8  # Demanda disminuye con precio
            demanda_estimada = demanda_base * \
                (precio ** elasticidad) * pib_factor * (1 - desempleo * 0.5)
            demanda_estimada = max(
                1, int(demanda_estimada + random.uniform(-3, 3)))

            X.append(caracteristicas_variadas)
            y.append(demanda_estimada)

        return X, y

    def _simular_caracteristicas_historicas(self, mercado, bien, indice_transaccion):
        """Simula las características que habrían existido en un momento anterior"""
        # Usar datos actuales con pequeñas variaciones para simular historial
        caracteristicas_actuales = self.extraer_caracteristicas(mercado, bien)
        factor_variacion = random.uniform(0.85, 1.15)

        return [c * factor_variacion for c in caracteristicas_actuales]

    def predecir_demanda(self, mercado, bien):
        """Predice la demanda futura para un bien"""
        if not self.caracteristicas_entrenadas:
            # Predicción básica sin ML
            return self._prediccion_basica(mercado, bien)

        try:
            caracteristicas = self.extraer_caracteristicas(mercado, bien)
            X_scaled = self.scaler.transform([caracteristicas])
            demanda_predicha = self.modelo.predict(X_scaled)[0]

            # Asegurar que sea positiva y razonable
            return max(1, min(1000, int(demanda_predicha)))
        except:
            return self._prediccion_basica(mercado, bien)

    def _prediccion_basica(self, mercado, bien):
        """Predicción básica sin ML como fallback"""
        # Basado en transacciones recientes
        transacciones_bien = [t for t in mercado.transacciones[-20:]
                              if t.get('bien') == bien]
        if transacciones_bien:
            demanda_promedio = sum(
                [t.get('cantidad', 1) for t in transacciones_bien]) / len(transacciones_bien)
            return max(1, int(demanda_promedio))
        return 10  # Valor por defecto


class OptimizadorPrecios:
    """Optimizador de precios usando algoritmos genéticos simplificados"""

    def __init__(self):
        self.poblacion_precios = []
        self.tamano_poblacion = 20
        self.generaciones = 10

    def optimizar_precio(self, empresa, bien, demanda_predicha):
        """Optimiza el precio de un bien para maximizar utilidad"""
        precio_actual = empresa.precios.get(bien, 10.0)
        costo_unitario = empresa.costos_unitarios.get(bien, 5.0)

        # Rango de precios a explorar
        precio_min = costo_unitario * 1.1  # Mínimo 10% margen
        precio_max = costo_unitario * 3.0   # Máximo 200% margen

        # Generar población inicial
        self.poblacion_precios = []
        for _ in range(self.tamano_poblacion):
            precio = random.uniform(precio_min, precio_max)
            self.poblacion_precios.append(precio)

        # Evolución
        for generacion in range(self.generaciones):
            # Evaluar fitness (utilidad estimada)
            fitness_scores = []
            for precio in self.poblacion_precios:
                utilidad = self._calcular_utilidad_estimada(
                    precio, costo_unitario, demanda_predicha, empresa, bien)
                fitness_scores.append(utilidad)

            # Seleccionar mejores
            indices_ordenados = sorted(range(len(fitness_scores)),
                                       key=lambda i: fitness_scores[i], reverse=True)

            # Mantener top 50%
            sobrevivientes = [self.poblacion_precios[i]
                              for i in indices_ordenados[:self.tamano_poblacion//2]]

            # Generar nueva población con mutación y cruce
            nueva_poblacion = sobrevivientes.copy()
            while len(nueva_poblacion) < self.tamano_poblacion:
                padre1 = random.choice(sobrevivientes)
                padre2 = random.choice(sobrevivientes)

                # Cruce simple
                hijo = (padre1 + padre2) / 2

                # Mutación
                if random.random() < 0.2:  # 20% probabilidad
                    hijo *= random.uniform(0.9, 1.1)

                # Mantener en rango válido
                hijo = max(precio_min, min(precio_max, hijo))
                nueva_poblacion.append(hijo)

            self.poblacion_precios = nueva_poblacion

        # Retornar mejor precio
        fitness_final = [self._calcular_utilidad_estimada(
            p, costo_unitario, demanda_predicha, empresa, bien)
            for p in self.poblacion_precios]

        mejor_indice = fitness_final.index(max(fitness_final))
        return self.poblacion_precios[mejor_indice]

    def _calcular_utilidad_estimada(self, precio, costo, demanda_base, empresa, bien):
        """Calcula utilidad estimada para un precio dado"""
        # Función de demanda elástica simple
        elasticidad = -1.2  # Elasticidad típica
        precio_referencia = empresa.precios.get(bien, precio)

        if precio_referencia > 0:
            cambio_precio = (precio - precio_referencia) / precio_referencia
            cambio_demanda = elasticidad * cambio_precio
            demanda_ajustada = demanda_base * (1 + cambio_demanda)
        else:
            demanda_ajustada = demanda_base

        demanda_ajustada = max(0, demanda_ajustada)

        # Utilidad = (precio - costo) * demanda
        utilidad = (precio - costo) * demanda_ajustada

        return max(0, utilidad)


class ClusterizadorAgentes:
    """Clusterizador de agentes económicos para análisis de comportamiento"""

    def __init__(self, n_clusters=5):
        self.n_clusters = n_clusters
        self.modelo_kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        self.scaler = StandardScaler()
        self.clusters_entrenados = False

    def extraer_caracteristicas_consumidor(self, consumidor):
        """Extrae características de un consumidor para clustering"""
        # Calcular total de bienes en inventario
        total_bienes = sum(consumidor.bienes.values()) if hasattr(
            consumidor, 'bienes') and consumidor.bienes else 0

        caracteristicas = [
            consumidor.dinero / 10000,  # Normalizado
            consumidor.ingreso_mensual / 5000,  # Normalizado
            total_bienes,  # Total de cantidades de bienes
            int(consumidor.empleado),
            consumidor.propension_consumo,
            consumidor.aversion_riesgo,
            consumidor.ahorros / 10000  # Normalizado
        ]

        # Agregar características psicológicas si están disponibles
        if hasattr(consumidor, 'perfil_psicologico'):
            perfil = consumidor.perfil_psicologico
            caracteristicas.extend([
                perfil.tolerancia_riesgo,
                perfil.paciencia,
                perfil.racionalidad,
                perfil.optimismo
            ])
        else:
            caracteristicas.extend([0.5, 0.5, 0.5, 0.5])  # Valores neutrales

        return caracteristicas

    def clusterizar_consumidores(self, mercado):
        """Agrupa consumidores en clusters por comportamiento"""
        consumidores = mercado.getConsumidores()
        if len(consumidores) < self.n_clusters:
            return {}

        # Extraer características
        X = []
        for consumidor in consumidores:
            caracteristicas = self.extraer_caracteristicas_consumidor(
                consumidor)
            X.append(caracteristicas)

        try:
            # Normalizar y clusterizar
            X_scaled = self.scaler.fit_transform(X)
            clusters = self.modelo_kmeans.fit_predict(X_scaled)
            self.clusters_entrenados = True

            # Agrupar resultados
            clusters_dict = defaultdict(list)
            for i, cluster in enumerate(clusters):
                clusters_dict[cluster].append(consumidores[i])

            return dict(clusters_dict)
        except:
            return {}

    def analizar_clusters(self, clusters):
        """Analiza las características de cada cluster"""
        analisis = {}

        for cluster_id, consumidores in clusters.items():
            if not consumidores:
                continue

            dinero_promedio = sum(
                [c.dinero for c in consumidores]) / len(consumidores)
            ingreso_promedio = sum(
                [c.ingreso_mensual for c in consumidores]) / len(consumidores)
            empleados = sum([1 for c in consumidores if c.empleado])
            tasa_empleo = empleados / len(consumidores)

            propension_promedio = sum(
                [c.propension_consumo for c in consumidores]) / len(consumidores)
            aversion_promedio = sum(
                [c.aversion_riesgo for c in consumidores]) / len(consumidores)

            analisis[cluster_id] = {
                'tamano': len(consumidores),
                'dinero_promedio': dinero_promedio,
                'ingreso_promedio': ingreso_promedio,
                'tasa_empleo': tasa_empleo,
                'propension_consumo': propension_promedio,
                'aversion_riesgo': aversion_promedio,
                'perfil': self._determinar_perfil_cluster(
                    dinero_promedio, ingreso_promedio, tasa_empleo,
                    propension_promedio, aversion_promedio)
            }

        return analisis

    def _determinar_perfil_cluster(self, dinero, ingreso, empleo, propension, aversion):
        """Determina el perfil descriptivo de un cluster"""
        if dinero > 30000 and ingreso > 5000:
            return "Clase Alta - Consumidores premium"
        elif dinero > 15000 and empleo > 0.8:
            return "Clase Media - Trabajadores estables"
        elif propension > 0.7:
            return "Consumidores impulsivos"
        elif aversion > 0.7:
            return "Conservadores - Ahorradores"
        elif empleo < 0.5:
            return "Desempleados - Vulnerable económicamente"
        else:
            return "Clase trabajadora - Comportamiento mixto"


class SistemaAnalyticsML:
    """Sistema coordinador de Analytics y Machine Learning"""

    def __init__(self, mercado):
        self.mercado = mercado
        self.predictor_demanda = {}  # Un predictor por bien
        self.optimizador_precios = OptimizadorPrecios()
        self.clusterizador = ClusterizadorAgentes()
        self.ciclo_analisis = 0

    def ciclo_analytics(self):
        """Ejecuta ciclo de análisis y optimización"""
        self.ciclo_analisis += 1

        # Solo hacer análisis cada 5 ciclos para eficiencia
        if self.ciclo_analisis % 5 != 0:
            return

        # Entrenar predictores de demanda
        for bien in self.mercado.bienes:
            if bien not in self.predictor_demanda:
                self.predictor_demanda[bien] = PredictorDemanda()

            self.predictor_demanda[bien].entrenar(self.mercado, bien)

        # Clusterizar consumidores cada 10 ciclos
        if self.ciclo_analisis % 10 == 0:
            clusters = self.clusterizador.clusterizar_consumidores(
                self.mercado)
            self.analisis_clusters = self.clusterizador.analizar_clusters(
                clusters)

    def obtener_prediccion_demanda(self, bien):
        """Obtiene predicción de demanda para un bien"""
        if bien in self.predictor_demanda:
            return self.predictor_demanda[bien].predecir_demanda(self.mercado, bien)
        return 10  # Valor por defecto

    def optimizar_precio_empresa(self, empresa, bien):
        """Optimiza el precio de un bien para una empresa"""
        demanda_predicha = self.obtener_prediccion_demanda(bien)
        precio_optimo = self.optimizador_precios.optimizar_precio(
            empresa, bien, demanda_predicha)
        return precio_optimo

    def obtener_estadisticas_analytics(self):
        """Retorna estadísticas del sistema de analytics"""
        stats = {
            'modelos_entrenados': len([p for p in self.predictor_demanda.values()
                                       if p.caracteristicas_entrenadas]),
            'predictores_disponibles': len(self.predictor_demanda),
            'ciclo_analisis': self.ciclo_analisis
        }

        # Estadísticas de clustering
        if hasattr(self, 'analisis_clusters'):
            stats['clusters_identificados'] = len(self.analisis_clusters)
            stats['perfiles_consumidor'] = {
                f'cluster_{k}': v['perfil']
                for k, v in self.analisis_clusters.items()
            }

        return stats
