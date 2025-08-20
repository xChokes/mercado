"""
Motor de Decisiones con Inteligencia Artificial
==============================================

Este módulo implementa el motor central de decisiones que utilizan
los agentes IA para tomar decisiones inteligentes basadas en aprendizaje
por refuerzo, redes neuronales y optimización estratégica.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass
import random
from collections import defaultdict
import math

# Importar bibliotecas de ML/IA (simuladas si no están disponibles)
try:
    from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
    from sklearn.neural_network import MLPRegressor
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import train_test_split
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    print("Librerías ML no disponibles. Usando implementación básica.")

from .AgentMemorySystem import AgentMemorySystem, Decision


@dataclass
class EstadoMercado:
    """Representa el estado actual del mercado para toma de decisiones"""
    precios: Dict[str, float]
    demanda: Dict[str, float]
    oferta: Dict[str, float]
    competidores: List[str]
    tendencias: Dict[str, float]
    volatilidad: Dict[str, float]
    ciclo_economico: str  # 'expansion', 'pico', 'recesion', 'valle'
    liquidez_mercado: float
    riesgo_sistemico: float


@dataclass
class OpcionDecision:
    """Representa una opción de decisión disponible"""
    id: str
    tipo: str
    parametros: Dict[str, Any]
    costo_estimado: float
    beneficio_estimado: float
    riesgo_estimado: float
    complejidad: float


class ReinforcementLearningModel:
    """
    Modelo básico de Aprendizaje por Refuerzo para agentes
    Implementa Q-Learning adaptado para decisiones económicas
    """
    
    def __init__(self, learning_rate: float = 0.1, discount_factor: float = 0.95, 
                 epsilon: float = 0.1):
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon  # Tasa de exploración
        
        # Tabla Q para mapear estados-acciones a valores
        self.q_table: Dict[str, Dict[str, float]] = defaultdict(lambda: defaultdict(float))
        
        # Historial de experiencias para entrenamiento
        self.experiencias = []
        
    def discretizar_estado(self, estado: EstadoMercado) -> str:
        """Convierte el estado continuo en estado discreto para Q-table"""
        estado_discreto = []
        
        # Discretizar precios (bajo, medio, alto)
        precio_promedio = np.mean(list(estado.precios.values())) if estado.precios else 0
        if precio_promedio < 20:
            estado_discreto.append("precio_bajo")
        elif precio_promedio < 50:
            estado_discreto.append("precio_medio")
        else:
            estado_discreto.append("precio_alto")
        
        # Discretizar demanda
        demanda_promedio = np.mean(list(estado.demanda.values())) if estado.demanda else 0
        if demanda_promedio < 30:
            estado_discreto.append("demanda_baja")
        elif demanda_promedio < 70:
            estado_discreto.append("demanda_media")
        else:
            estado_discreto.append("demanda_alta")
        
        # Ciclo económico
        estado_discreto.append(f"ciclo_{estado.ciclo_economico}")
        
        # Riesgo sistémico
        if estado.riesgo_sistemico < 0.3:
            estado_discreto.append("riesgo_bajo")
        elif estado.riesgo_sistemico < 0.7:
            estado_discreto.append("riesgo_medio")
        else:
            estado_discreto.append("riesgo_alto")
        
        return "_".join(estado_discreto)
    
    def seleccionar_accion(self, estado: EstadoMercado, 
                          acciones_disponibles: List[str]) -> str:
        """Selecciona la mejor acción usando ε-greedy"""
        estado_str = self.discretizar_estado(estado)
        
        # Exploración vs Explotación
        if random.random() < self.epsilon:
            # Exploración: acción aleatoria
            return random.choice(acciones_disponibles)
        else:
            # Explotación: mejor acción conocida
            q_valores = [self.q_table[estado_str][accion] for accion in acciones_disponibles]
            mejor_indice = np.argmax(q_valores)
            return acciones_disponibles[mejor_indice]
    
    def actualizar_q_valor(self, estado_anterior: EstadoMercado, accion: str,
                          recompensa: float, nuevo_estado: EstadoMercado,
                          acciones_disponibles: List[str]):
        """Actualiza el valor Q usando la ecuación de Bellman"""
        estado_ant_str = self.discretizar_estado(estado_anterior)
        nuevo_estado_str = self.discretizar_estado(nuevo_estado)
        
        # Valor Q actual
        q_actual = self.q_table[estado_ant_str][accion]
        
        # Mejor valor Q del nuevo estado
        if acciones_disponibles:
            max_q_nuevo = max([self.q_table[nuevo_estado_str][a] for a in acciones_disponibles])
        else:
            max_q_nuevo = 0
        
        # Actualización Q-Learning
        nuevo_q = q_actual + self.learning_rate * (
            recompensa + self.discount_factor * max_q_nuevo - q_actual
        )
        
        self.q_table[estado_ant_str][accion] = nuevo_q
        
        # Decaimiento de epsilon
        self.epsilon = max(0.01, self.epsilon * 0.999)


class NeuralNetwork:
    """
    Red neuronal básica para predicción de valores
    """
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        
        if ML_AVAILABLE:
            self.model = MLPRegressor(
                hidden_layer_sizes=(64, 32, 16),
                activation='relu',
                solver='adam',
                learning_rate='adaptive',
                max_iter=500,
                random_state=42
            )
    
    def preparar_features(self, estado: EstadoMercado, accion: OpcionDecision) -> np.ndarray:
        """Convierte estado y acción en features numéricas"""
        features = []
        
        # Features del estado del mercado
        features.extend(list(estado.precios.values())[:5])  # Máximo 5 precios
        features.extend(list(estado.demanda.values())[:5])  # Máximo 5 demandas
        features.append(estado.liquidez_mercado)
        features.append(estado.riesgo_sistemico)
        
        # Codificar ciclo económico
        ciclos = {'expansion': 0.8, 'pico': 1.0, 'recesion': 0.2, 'valle': 0.0}
        features.append(ciclos.get(estado.ciclo_economico, 0.5))
        
        # Features de la acción
        features.append(accion.costo_estimado)
        features.append(accion.beneficio_estimado)
        features.append(accion.riesgo_estimado)
        features.append(accion.complejidad)
        
        # Rellenar con ceros si faltan features
        while len(features) < 20:
            features.append(0.0)
        
        return np.array(features[:20])  # Mantener exactamente 20 features
    
    def entrenar(self, experiencias: List[Tuple[EstadoMercado, OpcionDecision, float]]):
        """Entrena la red neuronal con experiencias"""
        if not ML_AVAILABLE or len(experiencias) < 10:
            return
        
        X = []
        y = []
        
        for estado, accion, recompensa in experiencias:
            features = self.preparar_features(estado, accion)
            X.append(features)
            y.append(recompensa)
        
        X = np.array(X)
        y = np.array(y)
        
        # Normalizar features
        X_scaled = self.scaler.fit_transform(X)
        
        # Entrenar modelo
        self.model.fit(X_scaled, y)
        self.is_trained = True
    
    def predecir_valor(self, estado: EstadoMercado, accion: OpcionDecision) -> float:
        """Predice el valor esperado de una acción en un estado dado"""
        if not ML_AVAILABLE or not self.is_trained:
            # Fallback: cálculo heurístico simple
            return accion.beneficio_estimado - accion.costo_estimado - accion.riesgo_estimado
        
        features = self.preparar_features(estado, accion)
        features_scaled = self.scaler.transform([features])
        prediccion = self.model.predict(features_scaled)[0]
        
        return prediccion


class StrategyOptimizer:
    """
    Optimizador de estrategias usando algoritmos evolutivos
    """
    
    def __init__(self, poblacion_size: int = 20):
        self.poblacion_size = poblacion_size
        self.estrategias_poblacion = []
        self.generacion = 0
    
    def generar_estrategia_aleatoria(self) -> Dict[str, Any]:
        """Genera una estrategia aleatoria"""
        return {
            'agresividad_precio': random.uniform(0.5, 1.5),
            'tolerancia_riesgo': random.uniform(0.1, 0.9),
            'horizonte_planificacion': random.randint(5, 20),
            'factor_competencia': random.uniform(0.7, 1.3),
            'adaptabilidad': random.uniform(0.1, 1.0),
            'conservadurismo': random.uniform(0.0, 0.8)
        }
    
    def evaluar_estrategia(self, estrategia: Dict[str, Any], 
                          resultados_historicos: List[float]) -> float:
        """Evalúa la fitness de una estrategia"""
        if not resultados_historicos:
            return 0.0
        
        # Fitness basada en múltiples criterios
        rendimiento_promedio = np.mean(resultados_historicos)
        estabilidad = 1.0 / (np.std(resultados_historicos) + 0.1)
        crecimiento = resultados_historicos[-1] - resultados_historicos[0] if len(resultados_historicos) > 1 else 0
        
        fitness = rendimiento_promedio * 0.5 + estabilidad * 0.3 + crecimiento * 0.2
        return fitness
    
    def cruzar_estrategias(self, estrategia1: Dict[str, Any], 
                          estrategia2: Dict[str, Any]) -> Dict[str, Any]:
        """Cruza dos estrategias para crear una nueva"""
        nueva_estrategia = {}
        
        for clave in estrategia1.keys():
            if random.random() < 0.5:
                nueva_estrategia[clave] = estrategia1[clave]
            else:
                nueva_estrategia[clave] = estrategia2[clave]
        
        return nueva_estrategia
    
    def mutar_estrategia(self, estrategia: Dict[str, Any], 
                        tasa_mutacion: float = 0.1) -> Dict[str, Any]:
        """Muta una estrategia con cierta probabilidad"""
        estrategia_mutada = estrategia.copy()
        
        for clave, valor in estrategia_mutada.items():
            if random.random() < tasa_mutacion:
                if isinstance(valor, float):
                    factor_mutacion = random.uniform(0.8, 1.2)
                    estrategia_mutada[clave] = valor * factor_mutacion
                elif isinstance(valor, int):
                    estrategia_mutada[clave] = valor + random.randint(-2, 2)
        
        return estrategia_mutada
    
    def evolucionar_estrategias(self, fitness_scores: List[float]) -> List[Dict[str, Any]]:
        """Evoluciona la población de estrategias"""
        if len(self.estrategias_poblacion) != len(fitness_scores):
            return self.estrategias_poblacion
        
        # Ordenar por fitness
        parejas = list(zip(self.estrategias_poblacion, fitness_scores))
        parejas.sort(key=lambda x: x[1], reverse=True)
        
        # Seleccionar mejores estrategias (élite)
        elite_size = self.poblacion_size // 4
        nueva_poblacion = [parejas[i][0] for i in range(elite_size)]
        
        # Generar nueva población por cruzamiento
        while len(nueva_poblacion) < self.poblacion_size:
            # Selección por torneo
            padre1 = self.seleccion_torneo(parejas)
            padre2 = self.seleccion_torneo(parejas)
            
            # Cruzamiento
            hijo = self.cruzar_estrategias(padre1, padre2)
            
            # Mutación
            hijo = self.mutar_estrategia(hijo)
            
            nueva_poblacion.append(hijo)
        
        self.estrategias_poblacion = nueva_poblacion
        self.generacion += 1
        
        return nueva_poblacion
    
    def seleccion_torneo(self, parejas: List[Tuple[Dict[str, Any], float]], 
                        tamano_torneo: int = 3) -> Dict[str, Any]:
        """Selección por torneo para algoritmo evolutivo"""
        competidores = random.sample(parejas, min(tamano_torneo, len(parejas)))
        ganador = max(competidores, key=lambda x: x[1])
        return ganador[0]


class IADecisionEngine:
    """
    Motor principal de decisiones con IA que integra todos los componentes
    """
    
    def __init__(self, agente_id: str):
        self.agente_id = agente_id
        
        # Componentes principales
        self.modelo_rl = ReinforcementLearningModel()
        self.red_neural = NeuralNetwork()
        self.optimizador_estrategia = StrategyOptimizer()
        
        # Configuración
        self.usar_ensemble = True
        self.experiencias_entrenamiento = []
        self.estrategia_actual = self.optimizador_estrategia.generar_estrategia_aleatoria()
        
        # Métricas de desempeño
        self.decisiones_tomadas = 0
        self.decisiones_exitosas = 0
        self.valor_acumulado = 0.0
        
    def tomar_decision_inteligente(self, estado: EstadoMercado, 
                                 opciones: List[OpcionDecision]) -> OpcionDecision:
        """
        Toma una decisión inteligente considerando el estado y opciones disponibles
        """
        if not opciones:
            return None
        
        self.decisiones_tomadas += 1
        
        # Método 1: Q-Learning
        if len(opciones) > 1:
            acciones_str = [f"{op.tipo}_{op.id}" for op in opciones]
            accion_rl = self.modelo_rl.seleccionar_accion(estado, acciones_str)
            opcion_rl = next((op for op in opciones if f"{op.tipo}_{op.id}" == accion_rl), opciones[0])
        else:
            opcion_rl = opciones[0]
        
        # Método 2: Red Neuronal
        if self.red_neural.is_trained:
            valores_nn = [(op, self.red_neural.predecir_valor(estado, op)) for op in opciones]
            opcion_nn = max(valores_nn, key=lambda x: x[1])[0]
        else:
            opcion_nn = opciones[0]
        
        # Método 3: Análisis heurístico con estrategia actual
        opcion_heuristica = self._analisis_heuristico(estado, opciones)
        
        # Ensemble: combinar métodos
        if self.usar_ensemble:
            # Votar por la mejor opción
            votos = {}
            for opcion in [opcion_rl, opcion_nn, opcion_heuristica]:
                votos[opcion.id] = votos.get(opcion.id, 0) + 1
            
            # Seleccionar opción con más votos
            mejor_id = max(votos, key=votos.get)
            decision_final = next(op for op in opciones if op.id == mejor_id)
        else:
            # Usar solo red neuronal si está entrenada, sino heurística
            decision_final = opcion_nn if self.red_neural.is_trained else opcion_heuristica
        
        # Aplicar ajustes basados en estrategia actual
        decision_final = self._ajustar_por_estrategia(decision_final, estado)
        
        return decision_final
    
    def _analisis_heuristico(self, estado: EstadoMercado, 
                           opciones: List[OpcionDecision]) -> OpcionDecision:
        """Análisis heurístico basado en reglas económicas"""
        scores = []
        
        for opcion in opciones:
            score = 0
            
            # Factor 1: Relación beneficio/costo
            if opcion.costo_estimado > 0:
                ratio_beneficio = opcion.beneficio_estimado / opcion.costo_estimado
                score += ratio_beneficio * 30
            
            # Factor 2: Penalizar riesgo alto
            score -= opcion.riesgo_estimado * 20
            
            # Factor 3: Ajuste por ciclo económico
            if estado.ciclo_economico == 'expansion':
                score += 10  # Ser más agresivo en expansión
            elif estado.ciclo_economico == 'recesion':
                score -= opcion.riesgo_estimado * 10  # Ser más conservador
            
            # Factor 4: Ajuste por liquidez del mercado
            if estado.liquidez_mercado < 0.3:  # Baja liquidez
                score -= opcion.complejidad * 5
            
            # Factor 5: Aplicar estrategia actual
            score *= self.estrategia_actual.get('agresividad_precio', 1.0)
            score -= opcion.riesgo_estimado * (1 - self.estrategia_actual.get('tolerancia_riesgo', 0.5)) * 10
            
            scores.append((opcion, score))
        
        # Devolver opción con mayor score
        return max(scores, key=lambda x: x[1])[0]
    
    def _ajustar_por_estrategia(self, opcion: OpcionDecision, 
                              estado: EstadoMercado) -> OpcionDecision:
        """Ajusta la opción seleccionada basándose en la estrategia actual"""
        opcion_ajustada = OpcionDecision(
            id=opcion.id,
            tipo=opcion.tipo,
            parametros=opcion.parametros.copy(),
            costo_estimado=opcion.costo_estimado,
            beneficio_estimado=opcion.beneficio_estimado,
            riesgo_estimado=opcion.riesgo_estimado,
            complejidad=opcion.complejidad
        )
        
        # Ajustar parámetros según estrategia
        agresividad = self.estrategia_actual.get('agresividad_precio', 1.0)
        conservadurismo = self.estrategia_actual.get('conservadurismo', 0.5)
        
        # Modificar parámetros de precio si es una decisión de precio
        if 'precio' in opcion_ajustada.parametros:
            precio_base = opcion_ajustada.parametros['precio']
            opcion_ajustada.parametros['precio'] = precio_base * agresividad
        
        # Ajustar cantidad por conservadurismo
        if 'cantidad' in opcion_ajustada.parametros:
            cantidad_base = opcion_ajustada.parametros['cantidad']
            factor_conservador = 1 - conservadurismo * 0.3
            opcion_ajustada.parametros['cantidad'] = int(cantidad_base * factor_conservador)
        
        return opcion_ajustada
    
    def evaluar_riesgo_recompensa(self, accion: OpcionDecision, 
                                estado: EstadoMercado) -> Dict[str, float]:
        """Evalúa el riesgo y recompensa esperada de una acción"""
        # Cálculo base de riesgo-recompensa
        recompensa_esperada = accion.beneficio_estimado - accion.costo_estimado
        
        # Ajustar por estado del mercado
        ajuste_ciclo = {
            'expansion': 1.2,
            'pico': 1.0,
            'recesion': 0.6,
            'valle': 0.8
        }
        recompensa_esperada *= ajuste_ciclo.get(estado.ciclo_economico, 1.0)
        
        # Calcular riesgo ajustado
        riesgo_ajustado = accion.riesgo_estimado
        
        # Incrementar riesgo por volatilidad del mercado
        if estado.volatilidad:
            volatilidad_promedio = np.mean(list(estado.volatilidad.values()))
            riesgo_ajustado *= (1 + volatilidad_promedio)
        
        # Incrementar riesgo por riesgo sistémico
        riesgo_ajustado *= (1 + estado.riesgo_sistemico)
        
        # Calcular ratio Sharpe simplificado
        if riesgo_ajustado > 0:
            ratio_sharpe = recompensa_esperada / riesgo_ajustado
        else:
            ratio_sharpe = recompensa_esperada
        
        return {
            'recompensa_esperada': recompensa_esperada,
            'riesgo_ajustado': riesgo_ajustado,
            'ratio_sharpe': ratio_sharpe,
            'confianza': min(1.0, max(0.0, 0.5 + ratio_sharpe * 0.1))
        }
    
    def aprender_de_resultado(self, accion: OpcionDecision, estado_anterior: EstadoMercado,
                            nuevo_estado: EstadoMercado, resultado: Dict[str, Any]):
        """Aprende del resultado de una acción tomada"""
        # Calcular recompensa real
        recompensa_real = resultado.get('beneficio_neto', 0)
        
        # Actualizar modelo de Q-Learning
        acciones_disponibles = [f"{accion.tipo}_{accion.id}"]
        self.modelo_rl.actualizar_q_valor(
            estado_anterior, 
            f"{accion.tipo}_{accion.id}",
            recompensa_real,
            nuevo_estado,
            acciones_disponibles
        )
        
        # Agregar experiencia para entrenamiento de red neuronal
        self.experiencias_entrenamiento.append((estado_anterior, accion, recompensa_real))
        
        # Reentrenar red neuronal periódicamente
        if len(self.experiencias_entrenamiento) % 50 == 0:
            self.red_neural.entrenar(self.experiencias_entrenamiento[-200:])  # Últimas 200 experiencias
        
        # Actualizar métricas
        if recompensa_real > 0:
            self.decisiones_exitosas += 1
        
        self.valor_acumulado += recompensa_real
        
        # Evolucionar estrategia periódicamente
        if self.decisiones_tomadas % 100 == 0:
            self._evolucionar_estrategia()
    
    def _evolucionar_estrategia(self):
        """Evoluciona la estrategia actual basándose en el desempeño"""
        # Calcular fitness de estrategia actual
        if self.decisiones_tomadas > 0:
            tasa_exito = self.decisiones_exitosas / self.decisiones_tomadas
            valor_promedio = self.valor_acumulado / self.decisiones_tomadas
            fitness_actual = tasa_exito * 0.6 + valor_promedio * 0.4
        else:
            fitness_actual = 0
        
        # Si el rendimiento es bajo, generar nueva estrategia
        if fitness_actual < 0.3:
            self.estrategia_actual = self.optimizador_estrategia.generar_estrategia_aleatoria()
        elif fitness_actual > 0.7:
            # Refinar estrategia exitosa con pequeñas mutaciones
            self.estrategia_actual = self.optimizador_estrategia.mutar_estrategia(
                self.estrategia_actual, tasa_mutacion=0.05
            )
    
    def get_estadisticas_ia(self) -> Dict[str, Any]:
        """Obtiene estadísticas del motor de IA"""
        tasa_exito = (self.decisiones_exitosas / max(self.decisiones_tomadas, 1))
        valor_promedio = (self.valor_acumulado / max(self.decisiones_tomadas, 1))
        
        return {
            'agente_id': self.agente_id,
            'decisiones_tomadas': self.decisiones_tomadas,
            'decisiones_exitosas': self.decisiones_exitosas,
            'tasa_exito': tasa_exito,
            'valor_acumulado': self.valor_acumulado,
            'valor_promedio_decision': valor_promedio,
            'experiencias_acumuladas': len(self.experiencias_entrenamiento),
            'red_neural_entrenada': self.red_neural.is_trained,
            'epsilon_actual': self.modelo_rl.epsilon,
            'generacion_estrategia': self.optimizador_estrategia.generacion,
            'estrategia_actual': self.estrategia_actual
        }
