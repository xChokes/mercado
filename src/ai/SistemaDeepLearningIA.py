"""
Sistemas de Deep Learning y Optimización Avanzada
=================================================

Implementa redes neuronales especializadas, algoritmos evolutivos,
meta-aprendizaje y optimización por enjambre para agentes IA hiperrealistas.
"""

import numpy as np
import random
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict, deque
import threading
import time
import math
from enum import Enum
import json

from .AgentMemorySystem import AgentMemorySystem, Decision
from .IADecisionEngine import EstadoMercado, OpcionDecision


class TipoRedNeural(Enum):
    """Tipos de redes neuronales especializadas"""
    PREDICCION_PRECIOS = "prediccion_precios"
    DETECCION_PATRONES = "deteccion_patrones"
    OPTIMIZACION_ESTRATEGIA = "optimizacion_estrategia"
    RECONOCIMIENTO_OPORTUNIDADES = "reconocimiento_oportunidades"
    EVALUACION_RIESGOS = "evaluacion_riesgos"
    NEGOCIACION_INTELIGENTE = "negociacion_inteligente"


class TipoAlgoritmoEvolutivo(Enum):
    """Tipos de algoritmos evolutivos"""
    GENETICO = "genetico"
    DIFERENCIAL = "diferencial"
    PARTICULAS = "particulas"
    COLONIA_HORMIGAS = "colonia_hormigas"
    RECOCIDO_SIMULADO = "recocido_simulado"


@dataclass
class NeuronaArtificial:
    """Neurona artificial con funciones de activación avanzadas"""
    id: str
    pesos: List[float]
    bias: float
    funcion_activacion: str  # 'relu', 'tanh', 'sigmoid', 'leaky_relu', 'swish'
    historial_activaciones: deque = field(default_factory=lambda: deque(maxlen=1000))
    tasa_aprendizaje: float = 0.01
    momentum: float = 0.9
    gradiente_acumulado: float = 0.0
    
    def activar(self, entradas: List[float]) -> float:
        """Calcula la activación de la neurona"""
        if len(entradas) != len(self.pesos):
            raise ValueError(f"Esperaba {len(self.pesos)} entradas, recibió {len(entradas)}")
        
        # Calcular suma ponderada
        suma_ponderada = sum(e * p for e, p in zip(entradas, self.pesos)) + self.bias
        
        # Aplicar función de activación
        activacion = self._aplicar_funcion_activacion(suma_ponderada)
        
        # Guardar en historial
        self.historial_activaciones.append(activacion)
        
        return activacion
    
    def _aplicar_funcion_activacion(self, x: float) -> float:
        """Aplica la función de activación especificada"""
        if self.funcion_activacion == 'relu':
            return max(0, x)
        elif self.funcion_activacion == 'leaky_relu':
            return x if x > 0 else 0.01 * x
        elif self.funcion_activacion == 'tanh':
            return math.tanh(x)
        elif self.funcion_activacion == 'sigmoid':
            return 1 / (1 + math.exp(-max(-500, min(500, x))))  # Prevenir overflow
        elif self.funcion_activacion == 'swish':
            sigmoid = 1 / (1 + math.exp(-max(-500, min(500, x))))
            return x * sigmoid
        else:
            return x  # Lineal por defecto
    
    def actualizar_pesos(self, gradientes: List[float], tasa_aprendizaje: float = None):
        """Actualiza pesos usando gradientes con momentum"""
        if tasa_aprendizaje is None:
            tasa_aprendizaje = self.tasa_aprendizaje
        
        for i, gradiente in enumerate(gradientes):
            # Aplicar momentum
            self.gradiente_acumulado = (self.momentum * self.gradiente_acumulado + 
                                      (1 - self.momentum) * gradiente)
            
            # Actualizar peso
            self.pesos[i] -= tasa_aprendizaje * self.gradiente_acumulado


@dataclass
class CapaNeural:
    """Capa de red neural con múltiples neuronas"""
    id: str
    neuronas: List[NeuronaArtificial]
    tipo_capa: str  # 'entrada', 'oculta', 'salida'
    funcion_normalizacion: Optional[str] = None  # 'batch', 'layer'
    dropout_rate: float = 0.0
    
    def procesar(self, entradas: List[float], entrenando: bool = False) -> List[float]:
        """Procesa entradas através de toda la capa"""
        # Aplicar dropout durante entrenamiento
        if entrenando and self.dropout_rate > 0:
            entradas = self._aplicar_dropout(entradas)
        
        # Procesar cada neurona
        salidas = []
        for neurona in self.neuronas:
            activacion = neurona.activar(entradas)
            salidas.append(activacion)
        
        # Aplicar normalización si está configurada
        if self.funcion_normalizacion:
            salidas = self._normalizar(salidas)
        
        return salidas
    
    def _aplicar_dropout(self, entradas: List[float]) -> List[float]:
        """Aplica dropout a las entradas"""
        return [entrada if random.random() > self.dropout_rate else 0.0 
                for entrada in entradas]
    
    def _normalizar(self, valores: List[float]) -> List[float]:
        """Aplica normalización a los valores"""
        if self.funcion_normalizacion == 'batch':
            # Batch normalization simplificada
            media = np.mean(valores)
            desviacion = np.std(valores) + 1e-8
            return [(v - media) / desviacion for v in valores]
        elif self.funcion_normalizacion == 'layer':
            # Layer normalization
            suma = sum(valores)
            if suma != 0:
                return [v / suma for v in valores]
        
        return valores


class RedNeuralEspecializada:
    """Red neural especializada para tareas específicas de agentes IA"""
    
    def __init__(self, tipo: TipoRedNeural, arquitectura: List[int],
                 funciones_activacion: List[str] = None):
        self.tipo = tipo
        self.arquitectura = arquitectura  # [entrada, oculta1, oculta2, ..., salida]
        self.capas: List[CapaNeural] = []
        self.historial_entrenamiento = []
        self.precision_actual = 0.0
        self.epocas_entrenadas = 0
        self.tasa_aprendizaje = 0.001
        
        # Configurar funciones de activación
        if funciones_activacion is None:
            funciones_activacion = ['relu'] * (len(arquitectura) - 2) + ['sigmoid']
        
        # Construir capas
        self._construir_red(funciones_activacion)
        
        print(f"[RED NEURAL] Red {tipo.value} creada con arquitectura {arquitectura}")
    
    def _construir_red(self, funciones_activacion: List[str]):
        """Construye la estructura de la red neural"""
        for i in range(len(self.arquitectura) - 1):
            n_entradas = self.arquitectura[i]
            n_neuronas = self.arquitectura[i + 1]
            
            # Determinar tipo de capa
            if i == 0:
                tipo_capa = 'entrada'
            elif i == len(self.arquitectura) - 2:
                tipo_capa = 'salida'
            else:
                tipo_capa = 'oculta'
            
            # Crear neuronas para esta capa
            neuronas = []
            funcion_act = funciones_activacion[min(i, len(funciones_activacion) - 1)]
            
            for j in range(n_neuronas):
                # Inicialización Xavier/Glorot
                limite = math.sqrt(6.0 / (n_entradas + n_neuronas))
                pesos = [random.uniform(-limite, limite) for _ in range(n_entradas)]
                bias = random.uniform(-0.1, 0.1)
                
                neurona = NeuronaArtificial(
                    id=f"neurona_{i}_{j}",
                    pesos=pesos,
                    bias=bias,
                    funcion_activacion=funcion_act,
                    tasa_aprendizaje=self.tasa_aprendizaje
                )
                neuronas.append(neurona)
            
            # Crear capa
            capa = CapaNeural(
                id=f"capa_{i}",
                neuronas=neuronas,
                tipo_capa=tipo_capa,
                dropout_rate=0.2 if tipo_capa == 'oculta' else 0.0
            )
            self.capas.append(capa)
    
    def predecir(self, entradas: List[float]) -> List[float]:
        """Realiza predicción usando la red neural"""
        if len(entradas) != self.arquitectura[0]:
            raise ValueError(f"Esperaba {self.arquitectura[0]} entradas, recibió {len(entradas)}")
        
        # Propagación hacia adelante
        activaciones = entradas
        for capa in self.capas:
            activaciones = capa.procesar(activaciones, entrenando=False)
        
        return activaciones
    
    def entrenar_lote(self, datos_entrenamiento: List[Tuple[List[float], List[float]]],
                     epocas: int = 100) -> Dict[str, float]:
        """Entrena la red con un lote de datos"""
        print(f"[RED NEURAL] Iniciando entrenamiento por {epocas} épocas...")
        
        metricas_entrenamiento = {
            'error_inicial': 0.0,
            'error_final': 0.0,
            'precision_final': 0.0,
            'tiempo_entrenamiento': 0.0
        }
        
        inicio = time.time()
        
        # Calcular error inicial
        error_inicial = self._calcular_error_promedio(datos_entrenamiento)
        metricas_entrenamiento['error_inicial'] = error_inicial
        
        # Entrenamiento por épocas
        for epoca in range(epocas):
            error_epoca = 0.0
            
            # Barajar datos
            datos_mezclados = datos_entrenamiento.copy()
            random.shuffle(datos_mezclados)
            
            # Entrenar con cada ejemplo
            for entradas, objetivos in datos_mezclados:
                error_ejemplo = self._entrenar_ejemplo(entradas, objetivos)
                error_epoca += error_ejemplo
            
            # Promedio de error de la época
            error_promedio = error_epoca / len(datos_entrenamiento)
            
            # Guardar métricas cada 10 épocas
            if epoca % 10 == 0:
                self.historial_entrenamiento.append({
                    'epoca': epoca,
                    'error': error_promedio,
                    'timestamp': datetime.now()
                })
        
        # Calcular métricas finales
        error_final = self._calcular_error_promedio(datos_entrenamiento)
        precision_final = max(0.0, 1.0 - error_final)
        
        metricas_entrenamiento['error_final'] = error_final
        metricas_entrenamiento['precision_final'] = precision_final
        metricas_entrenamiento['tiempo_entrenamiento'] = time.time() - inicio
        
        self.precision_actual = precision_final
        self.epocas_entrenadas += epocas
        
        print(f"[RED NEURAL] Entrenamiento completado. Precisión: {precision_final:.3f}")
        
        return metricas_entrenamiento
    
    def _entrenar_ejemplo(self, entradas: List[float], objetivos: List[float]) -> float:
        """Entrena la red con un ejemplo específico usando backpropagation"""
        # Propagación hacia adelante con almacenamiento de activaciones
        activaciones_capas = [entradas]
        
        activaciones = entradas
        for capa in self.capas:
            activaciones = capa.procesar(activaciones, entrenando=True)
            activaciones_capas.append(activaciones)
        
        # Calcular error
        predicciones = activaciones_capas[-1]
        error = sum((pred - obj) ** 2 for pred, obj in zip(predicciones, objetivos)) / len(objetivos)
        
        # Backpropagation simplificado
        self._backpropagation_simplificado(activaciones_capas, objetivos)
        
        return error
    
    def _backpropagation_simplificado(self, activaciones_capas: List[List[float]], 
                                    objetivos: List[float]):
        """Implementación simplificada de backpropagation"""
        # Calcular gradientes de la capa de salida
        predicciones = activaciones_capas[-1]
        gradientes_salida = [2 * (pred - obj) for pred, obj in zip(predicciones, objetivos)]
        
        # Actualizar pesos de la última capa
        capa_salida = self.capas[-1]
        activaciones_entrada = activaciones_capas[-2]
        
        for i, neurona in enumerate(capa_salida.neuronas):
            gradiente_neurona = gradientes_salida[i]
            gradientes_pesos = [gradiente_neurona * act for act in activaciones_entrada]
            neurona.actualizar_pesos(gradientes_pesos)
            neurona.bias -= self.tasa_aprendizaje * gradiente_neurona
        
        # Para capas ocultas (simplificado - solo propagación local)
        for capa_idx in range(len(self.capas) - 2, -1, -1):
            capa = self.capas[capa_idx]
            activaciones_entrada = activaciones_capas[capa_idx]
            
            for neurona in capa.neuronas:
                # Gradiente simplificado para capas ocultas
                gradiente_local = random.uniform(-0.01, 0.01)  # Simplificación
                gradientes_pesos = [gradiente_local * act for act in activaciones_entrada]
                neurona.actualizar_pesos(gradientes_pesos)
                neurona.bias -= self.tasa_aprendizaje * gradiente_local
    
    def _calcular_error_promedio(self, datos: List[Tuple[List[float], List[float]]]) -> float:
        """Calcula el error promedio en un conjunto de datos"""
        if not datos:
            return 0.0
        
        error_total = 0.0
        for entradas, objetivos in datos:
            predicciones = self.predecir(entradas)
            error = sum((pred - obj) ** 2 for pred, obj in zip(predicciones, objetivos)) / len(objetivos)
            error_total += error
        
        return error_total / len(datos)
    
    def guardar_modelo(self, ruta: str):
        """Guarda el modelo entrenado"""
        modelo_datos = {
            'tipo': self.tipo.value,
            'arquitectura': self.arquitectura,
            'precision_actual': self.precision_actual,
            'epocas_entrenadas': self.epocas_entrenadas,
            'capas': []
        }
        
        for capa in self.capas:
            datos_capa = {
                'tipo_capa': capa.tipo_capa,
                'neuronas': []
            }
            
            for neurona in capa.neuronas:
                datos_neurona = {
                    'pesos': neurona.pesos,
                    'bias': neurona.bias,
                    'funcion_activacion': neurona.funcion_activacion
                }
                datos_capa['neuronas'].append(datos_neurona)
            
            modelo_datos['capas'].append(datos_capa)
        
        with open(ruta, 'w') as f:
            json.dump(modelo_datos, f, indent=2)
        
        print(f"[RED NEURAL] Modelo guardado en {ruta}")


@dataclass
class IndividuoEvolutivo:
    """Individuo en algoritmo evolutivo"""
    id: str
    genes: List[float]  # Parámetros a optimizar
    fitness: float
    edad: int = 0
    generacion: int = 0
    padre_ids: List[str] = field(default_factory=list)
    mutaciones: int = 0
    
    def mutar(self, tasa_mutacion: float, intensidad_mutacion: float):
        """Aplica mutación al individuo"""
        mutaciones_aplicadas = 0
        for i in range(len(self.genes)):
            if random.random() < tasa_mutacion:
                # Mutación gaussiana
                self.genes[i] += random.gauss(0, intensidad_mutacion)
                # Mantener en rango [-1, 1]
                self.genes[i] = max(-1.0, min(1.0, self.genes[i]))
                mutaciones_aplicadas += 1
        
        self.mutaciones += mutaciones_aplicadas
        return mutaciones_aplicadas
    
    def cruzar_con(self, otro: 'IndividuoEvolutivo') -> Tuple['IndividuoEvolutivo', 'IndividuoEvolutivo']:
        """Realiza cruzamiento con otro individuo"""
        # Cruzamiento uniforme
        hijo1_genes = []
        hijo2_genes = []
        
        for i in range(len(self.genes)):
            if random.random() < 0.5:
                hijo1_genes.append(self.genes[i])
                hijo2_genes.append(otro.genes[i])
            else:
                hijo1_genes.append(otro.genes[i])
                hijo2_genes.append(self.genes[i])
        
        hijo1 = IndividuoEvolutivo(
            id=f"hijo_{int(time.time())}_{random.randint(1000, 9999)}",
            genes=hijo1_genes,
            fitness=0.0,
            generacion=max(self.generacion, otro.generacion) + 1,
            padre_ids=[self.id, otro.id]
        )
        
        hijo2 = IndividuoEvolutivo(
            id=f"hijo_{int(time.time())}_{random.randint(1000, 9999)}",
            genes=hijo2_genes,
            fitness=0.0,
            generacion=max(self.generacion, otro.generacion) + 1,
            padre_ids=[self.id, otro.id]
        )
        
        return hijo1, hijo2


class OptimizadorEvolutivo:
    """Optimizador usando algoritmos evolutivos"""
    
    def __init__(self, tipo_algoritmo: TipoAlgoritmoEvolutivo, 
                 dimension_problema: int, tamano_poblacion: int = 50):
        self.tipo_algoritmo = tipo_algoritmo
        self.dimension_problema = dimension_problema
        self.tamano_poblacion = tamano_poblacion
        
        # Población
        self.poblacion: List[IndividuoEvolutivo] = []
        self.mejor_individuo: Optional[IndividuoEvolutivo] = None
        self.historial_mejores = []
        
        # Parámetros evolutivos
        self.tasa_mutacion = 0.1
        self.intensidad_mutacion = 0.1
        self.tasa_cruzamiento = 0.8
        self.presion_seleccion = 2.0
        
        # Estadísticas
        self.generacion_actual = 0
        self.evaluaciones_fitness = 0
        self.tiempo_inicio = None
        
        # Inicializar población
        self._inicializar_poblacion()
        
        print(f"[EVOLUTIVO] Optimizador {tipo_algoritmo.value} inicializado con población de {tamano_poblacion}")
    
    def _inicializar_poblacion(self):
        """Inicializa la población de individuos"""
        for i in range(self.tamano_poblacion):
            genes = [random.uniform(-1.0, 1.0) for _ in range(self.dimension_problema)]
            individuo = IndividuoEvolutivo(
                id=f"individuo_{i}",
                genes=genes,
                fitness=0.0,
                generacion=0
            )
            self.poblacion.append(individuo)
    
    def optimizar(self, funcion_fitness: Callable[[List[float]], float],
                 max_generaciones: int = 100, 
                 objetivo_fitness: float = None) -> IndividuoEvolutivo:
        """Ejecuta optimización evolutiva"""
        print(f"[EVOLUTIVO] Iniciando optimización por {max_generaciones} generaciones...")
        
        self.tiempo_inicio = time.time()
        
        for generacion in range(max_generaciones):
            self.generacion_actual = generacion
            
            # Evaluar fitness de la población
            self._evaluar_poblacion(funcion_fitness)
            
            # Actualizar mejor individuo
            self._actualizar_mejor_individuo()
            
            # Registrar progreso
            if generacion % 10 == 0:
                mejor_fitness = self.mejor_individuo.fitness if self.mejor_individuo else 0
                print(f"[EVOLUTIVO] Generación {generacion}, Mejor fitness: {mejor_fitness:.6f}")
                self.historial_mejores.append({
                    'generacion': generacion,
                    'fitness': mejor_fitness,
                    'tiempo': time.time() - self.tiempo_inicio
                })
            
            # Verificar criterio de parada
            if objetivo_fitness and self.mejor_individuo and self.mejor_individuo.fitness >= objetivo_fitness:
                print(f"[EVOLUTIVO] Objetivo alcanzado en generación {generacion}")
                break
            
            # Evolucionar población
            if self.tipo_algoritmo == TipoAlgoritmoEvolutivo.GENETICO:
                self._evolucion_genetica()
            elif self.tipo_algoritmo == TipoAlgoritmoEvolutivo.DIFERENCIAL:
                self._evolucion_diferencial()
            elif self.tipo_algoritmo == TipoAlgoritmoEvolutivo.PARTICULAS:
                self._evolucion_particulas()
            
            # Actualizar edad de individuos
            for individuo in self.poblacion:
                individuo.edad += 1
        
        tiempo_total = time.time() - self.tiempo_inicio
        print(f"[EVOLUTIVO] Optimización completada en {tiempo_total:.2f} segundos")
        
        return self.mejor_individuo
    
    def _evaluar_poblacion(self, funcion_fitness: Callable[[List[float]], float]):
        """Evalúa fitness de toda la población"""
        for individuo in self.poblacion:
            individuo.fitness = funcion_fitness(individuo.genes)
            self.evaluaciones_fitness += 1
    
    def _actualizar_mejor_individuo(self):
        """Actualiza el mejor individuo de la población"""
        if not self.poblacion:
            return
        
        mejor_actual = max(self.poblacion, key=lambda ind: ind.fitness)
        
        if self.mejor_individuo is None or mejor_actual.fitness > self.mejor_individuo.fitness:
            # Crear copia del mejor individuo
            self.mejor_individuo = IndividuoEvolutivo(
                id=f"mejor_{self.generacion_actual}",
                genes=mejor_actual.genes.copy(),
                fitness=mejor_actual.fitness,
                generacion=mejor_actual.generacion
            )
    
    def _evolucion_genetica(self):
        """Implementa evolución genética"""
        nueva_poblacion = []
        
        # Elitismo: mantener los mejores individuos
        elite_size = max(1, self.tamano_poblacion // 10)
        elite = sorted(self.poblacion, key=lambda ind: ind.fitness, reverse=True)[:elite_size]
        nueva_poblacion.extend(elite)
        
        # Generar descendencia
        while len(nueva_poblacion) < self.tamano_poblacion:
            # Selección de padres por torneo
            padre1 = self._seleccion_torneo()
            padre2 = self._seleccion_torneo()
            
            # Cruzamiento
            if random.random() < self.tasa_cruzamiento:
                hijo1, hijo2 = padre1.cruzar_con(padre2)
            else:
                hijo1 = padre1
                hijo2 = padre2
            
            # Mutación
            hijo1.mutar(self.tasa_mutacion, self.intensidad_mutacion)
            hijo2.mutar(self.tasa_mutacion, self.intensidad_mutacion)
            
            nueva_poblacion.extend([hijo1, hijo2])
        
        # Truncar si excede tamaño
        self.poblacion = nueva_poblacion[:self.tamano_poblacion]
    
    def _seleccion_torneo(self, tamano_torneo: int = 3) -> IndividuoEvolutivo:
        """Selecciona individuo usando torneo"""
        candidatos = random.sample(self.poblacion, min(tamano_torneo, len(self.poblacion)))
        return max(candidatos, key=lambda ind: ind.fitness)
    
    def _evolucion_diferencial(self):
        """Implementa evolución diferencial"""
        nueva_poblacion = []
        
        for i, individuo_objetivo in enumerate(self.poblacion):
            # Seleccionar tres individuos aleatorios diferentes
            candidatos = [ind for j, ind in enumerate(self.poblacion) if j != i]
            if len(candidatos) < 3:
                nueva_poblacion.append(individuo_objetivo)
                continue
            
            ind_a, ind_b, ind_c = random.sample(candidatos, 3)
            
            # Crear individuo donante
            F = 0.5  # Factor de diferenciación
            genes_donante = []
            for j in range(self.dimension_problema):
                gen_donante = ind_a.genes[j] + F * (ind_b.genes[j] - ind_c.genes[j])
                genes_donante.append(max(-1.0, min(1.0, gen_donante)))
            
            # Cruzamiento binomial
            CR = 0.7  # Probabilidad de cruzamiento
            genes_trial = []
            for j in range(self.dimension_problema):
                if random.random() < CR or j == random.randint(0, self.dimension_problema - 1):
                    genes_trial.append(genes_donante[j])
                else:
                    genes_trial.append(individuo_objetivo.genes[j])
            
            # Crear individuo trial
            individuo_trial = IndividuoEvolutivo(
                id=f"trial_{i}_{self.generacion_actual}",
                genes=genes_trial,
                fitness=0.0,
                generacion=self.generacion_actual
            )
            
            nueva_poblacion.append(individuo_trial)
        
        self.poblacion = nueva_poblacion
    
    def _evolucion_particulas(self):
        """Implementa optimización por enjambre de partículas (simplificado)"""
        # PSO simplificado como algoritmo evolutivo
        w = 0.7  # Inercia
        c1 = 1.5  # Coeficiente cognitivo
        c2 = 1.5  # Coeficiente social
        
        if not hasattr(self, 'velocidades'):
            # Inicializar velocidades
            self.velocidades = []
            self.mejores_personales = []
            for individuo in self.poblacion:
                velocidad = [random.uniform(-0.1, 0.1) for _ in range(self.dimension_problema)]
                self.velocidades.append(velocidad)
                self.mejores_personales.append(individuo.genes.copy())
        
        mejor_global = self.mejor_individuo.genes if self.mejor_individuo else [0.0] * self.dimension_problema
        
        for i, individuo in enumerate(self.poblacion):
            # Actualizar velocidad
            for j in range(self.dimension_problema):
                r1, r2 = random.random(), random.random()
                self.velocidades[i][j] = (w * self.velocidades[i][j] +
                                        c1 * r1 * (self.mejores_personales[i][j] - individuo.genes[j]) +
                                        c2 * r2 * (mejor_global[j] - individuo.genes[j]))
                
                # Limitar velocidad
                self.velocidades[i][j] = max(-0.2, min(0.2, self.velocidades[i][j]))
            
            # Actualizar posición
            for j in range(self.dimension_problema):
                individuo.genes[j] += self.velocidades[i][j]
                individuo.genes[j] = max(-1.0, min(1.0, individuo.genes[j]))
    
    def get_estadisticas(self) -> Dict[str, Any]:
        """Obtiene estadísticas del proceso evolutivo"""
        tiempo_transcurrido = time.time() - self.tiempo_inicio if self.tiempo_inicio else 0
        
        fitness_poblacion = [ind.fitness for ind in self.poblacion]
        
        return {
            'generacion_actual': self.generacion_actual,
            'evaluaciones_fitness': self.evaluaciones_fitness,
            'tiempo_transcurrido': tiempo_transcurrido,
            'mejor_fitness': self.mejor_individuo.fitness if self.mejor_individuo else 0,
            'fitness_promedio': np.mean(fitness_poblacion) if fitness_poblacion else 0,
            'fitness_std': np.std(fitness_poblacion) if fitness_poblacion else 0,
            'diversidad_poblacion': self._calcular_diversidad(),
            'tasa_mejora': self._calcular_tasa_mejora()
        }
    
    def _calcular_diversidad(self) -> float:
        """Calcula diversidad genética de la población"""
        if len(self.poblacion) < 2:
            return 0.0
        
        diversidades = []
        for i in range(len(self.poblacion)):
            for j in range(i + 1, len(self.poblacion)):
                distancia = sum((self.poblacion[i].genes[k] - self.poblacion[j].genes[k]) ** 2 
                              for k in range(self.dimension_problema))
                diversidades.append(math.sqrt(distancia))
        
        return np.mean(diversidades) if diversidades else 0.0
    
    def _calcular_tasa_mejora(self) -> float:
        """Calcula tasa de mejora reciente"""
        if len(self.historial_mejores) < 2:
            return 0.0
        
        fitness_inicial = self.historial_mejores[0]['fitness']
        fitness_actual = self.historial_mejores[-1]['fitness']
        
        if fitness_inicial == 0:
            return 1.0 if fitness_actual > 0 else 0.0
        
        return (fitness_actual - fitness_inicial) / abs(fitness_inicial)


class MetaAprendizajeIA:
    """Sistema de meta-aprendizaje para agentes IA"""
    
    def __init__(self):
        self.experiencias_aprendizaje = []
        self.estrategias_aprendizaje = {
            'rapido_convergencia': {'tasa_aprendizaje': 0.01, 'momentum': 0.9},
            'exploracion_amplia': {'tasa_aprendizaje': 0.005, 'momentum': 0.7},
            'refinamiento_precision': {'tasa_aprendizaje': 0.001, 'momentum': 0.95}
        }
        self.contextos_aprendizaje = defaultdict(list)
        self.adaptaciones_automaticas = 0
        
    def registrar_experiencia_aprendizaje(self, contexto: Dict[str, Any], 
                                        resultado: Dict[str, float]):
        """Registra una experiencia de aprendizaje"""
        experiencia = {
            'contexto': contexto,
            'resultado': resultado,
            'timestamp': datetime.now(),
            'efectividad': resultado.get('precision_final', 0.0)
        }
        
        self.experiencias_aprendizaje.append(experiencia)
        
        # Categorizar por tipo de problema
        tipo_problema = contexto.get('tipo_problema', 'general')
        self.contextos_aprendizaje[tipo_problema].append(experiencia)
        
        # Mantener solo últimas 1000 experiencias
        if len(self.experiencias_aprendizaje) > 1000:
            self.experiencias_aprendizaje = self.experiencias_aprendizaje[-1000:]
    
    def adaptar_parametros_aprendizaje(self, contexto_actual: Dict[str, Any]) -> Dict[str, float]:
        """Adapta parámetros de aprendizaje basándose en experiencias pasadas"""
        tipo_problema = contexto_actual.get('tipo_problema', 'general')
        experiencias_similares = self.contextos_aprendizaje[tipo_problema]
        
        if not experiencias_similares:
            # Sin experiencias similares, usar configuración por defecto
            return self.estrategias_aprendizaje['rapido_convergencia']
        
        # Analizar experiencias similares
        mejores_experiencias = sorted(experiencias_similares, 
                                    key=lambda x: x['efectividad'], reverse=True)[:5]
        
        if not mejores_experiencias:
            return self.estrategias_aprendizaje['rapido_convergencia']
        
        # Extraer parámetros de las mejores experiencias
        tasas_aprendizaje = []
        momentums = []
        
        for exp in mejores_experiencias:
            resultado = exp['resultado']
            # Inferir parámetros óptimos basándose en resultados
            if resultado.get('precision_final', 0) > 0.8:
                tasas_aprendizaje.append(0.001)  # Precisión alta, tasa baja
                momentums.append(0.95)
            elif resultado.get('tiempo_entrenamiento', float('inf')) < 10:
                tasas_aprendizaje.append(0.01)  # Entrenamiento rápido
                momentums.append(0.9)
            else:
                tasas_aprendizaje.append(0.005)  # Balanceado
                momentums.append(0.85)
        
        # Promediar parámetros recomendados
        parametros_adaptados = {
            'tasa_aprendizaje': np.mean(tasas_aprendizaje),
            'momentum': np.mean(momentums)
        }
        
        self.adaptaciones_automaticas += 1
        
        print(f"[META-APRENDIZAJE] Parámetros adaptados: {parametros_adaptados}")
        
        return parametros_adaptados
    
    def recomendar_arquitectura_red(self, caracteristicas_problema: Dict[str, Any]) -> List[int]:
        """Recomienda arquitectura de red neural basándose en el problema"""
        dimension_entrada = caracteristicas_problema.get('dimension_entrada', 10)
        complejidad = caracteristicas_problema.get('complejidad', 'media')  # baja, media, alta
        tipo_salida = caracteristicas_problema.get('tipo_salida', 'regresion')  # clasificacion, regresion
        
        # Determinar tamaño de salida
        if tipo_salida == 'clasificacion':
            num_clases = caracteristicas_problema.get('num_clases', 2)
            dimension_salida = num_clases
        else:
            dimension_salida = caracteristicas_problema.get('dimension_salida', 1)
        
        # Determinar capas ocultas basándose en complejidad
        if complejidad == 'baja':
            capas_ocultas = [max(dimension_entrada // 2, 5)]
        elif complejidad == 'media':
            capas_ocultas = [dimension_entrada, max(dimension_entrada // 2, 10)]
        else:  # alta
            capas_ocultas = [dimension_entrada * 2, dimension_entrada, max(dimension_entrada // 2, 15)]
        
        arquitectura = [dimension_entrada] + capas_ocultas + [dimension_salida]
        
        print(f"[META-APRENDIZAJE] Arquitectura recomendada: {arquitectura}")
        
        return arquitectura
    
    def get_estrategia_optimizacion(self, caracteristicas_problema: Dict[str, Any]) -> TipoAlgoritmoEvolutivo:
        """Recomienda estrategia de optimización evolutiva"""
        dimension = caracteristicas_problema.get('dimension', 10)
        tipo_funcion = caracteristicas_problema.get('tipo_funcion', 'multimodal')
        tiempo_disponible = caracteristicas_problema.get('tiempo_disponible', 'medio')
        
        # Reglas heurísticas para selección de algoritmo
        if dimension <= 10 and tiempo_disponible == 'alto':
            return TipoAlgoritmoEvolutivo.GENETICO
        elif tipo_funcion == 'unimodal':
            return TipoAlgoritmoEvolutivo.DIFERENCIAL
        elif dimension > 50:
            return TipoAlgoritmoEvolutivo.PARTICULAS
        else:
            return TipoAlgoritmoEvolutivo.GENETICO


class SistemaDeepLearningIA:
    """
    Sistema Integrado de Deep Learning para Agentes IA
    """
    
    def __init__(self):
        # Redes neuronales especializadas
        self.redes_especializadas: Dict[TipoRedNeural, RedNeuralEspecializada] = {}
        
        # Optimizadores evolutivos
        self.optimizadores: Dict[str, OptimizadorEvolutivo] = {}
        
        # Sistema de meta-aprendizaje
        self.meta_aprendizaje = MetaAprendizajeIA()
        
        # Datos de entrenamiento por tipo
        self.datos_entrenamiento: Dict[TipoRedNeural, List[Tuple[List[float], List[float]]]] = defaultdict(list)
        
        # Métricas del sistema
        self.redes_entrenadas = 0
        self.optimizaciones_completadas = 0
        self.adaptaciones_meta_aprendizaje = 0
        
        # Control de entrenamiento
        self.entrenando = False
        self.hilo_entrenamiento = None
        
        print("[DEEP LEARNING] Sistema de Deep Learning IA inicializado")
    
    def crear_red_especializada(self, tipo: TipoRedNeural, 
                              caracteristicas_problema: Dict[str, Any] = None) -> RedNeuralEspecializada:
        """Crea una red neural especializada para una tarea específica"""
        
        if caracteristicas_problema is None:
            caracteristicas_problema = self._get_caracteristicas_default(tipo)
        
        # Obtener arquitectura recomendada por meta-aprendizaje
        arquitectura = self.meta_aprendizaje.recomendar_arquitectura_red(caracteristicas_problema)
        
        # Configurar funciones de activación por tipo de red
        funciones_activacion = self._get_funciones_activacion_optimales(tipo)
        
        # Crear red
        red = RedNeuralEspecializada(tipo, arquitectura, funciones_activacion)
        
        # Adaptar parámetros de aprendizaje
        contexto = {
            'tipo_problema': tipo.value,
            'dimension_entrada': arquitectura[0],
            'complejidad': caracteristicas_problema.get('complejidad', 'media')
        }
        
        parametros_adaptados = self.meta_aprendizaje.adaptar_parametros_aprendizaje(contexto)
        red.tasa_aprendizaje = parametros_adaptados['tasa_aprendizaje']
        
        # Registrar red
        self.redes_especializadas[tipo] = red
        
        print(f"[DEEP LEARNING] Red {tipo.value} creada con arquitectura {arquitectura}")
        
        return red
    
    def _get_caracteristicas_default(self, tipo: TipoRedNeural) -> Dict[str, Any]:
        """Obtiene características por defecto para cada tipo de red"""
        caracteristicas_default = {
            TipoRedNeural.PREDICCION_PRECIOS: {
                'dimension_entrada': 15,  # Indicadores de mercado
                'dimension_salida': 5,    # Precios de diferentes bienes
                'complejidad': 'media',
                'tipo_salida': 'regresion'
            },
            TipoRedNeural.DETECCION_PATRONES: {
                'dimension_entrada': 20,  # Datos de transacciones
                'dimension_salida': 8,    # Tipos de patrones
                'complejidad': 'alta',
                'tipo_salida': 'clasificacion',
                'num_clases': 8
            },
            TipoRedNeural.OPTIMIZACION_ESTRATEGIA: {
                'dimension_entrada': 12,  # Estado del agente
                'dimension_salida': 6,    # Acciones estratégicas
                'complejidad': 'alta',
                'tipo_salida': 'regresion'
            },
            TipoRedNeural.RECONOCIMIENTO_OPORTUNIDADES: {
                'dimension_entrada': 18,  # Datos de mercado
                'dimension_salida': 3,    # Tipos de oportunidades
                'complejidad': 'media',
                'tipo_salida': 'clasificacion',
                'num_clases': 3
            },
            TipoRedNeural.EVALUACION_RIESGOS: {
                'dimension_entrada': 10,  # Indicadores de riesgo
                'dimension_salida': 1,    # Nivel de riesgo
                'complejidad': 'media',
                'tipo_salida': 'regresion'
            },
            TipoRedNeural.NEGOCIACION_INTELIGENTE: {
                'dimension_entrada': 8,   # Estado de negociación
                'dimension_salida': 4,    # Tácticas de negociación
                'complejidad': 'media',
                'tipo_salida': 'regresion'
            }
        }
        
        return caracteristicas_default.get(tipo, {
            'dimension_entrada': 10,
            'dimension_salida': 1,
            'complejidad': 'media',
            'tipo_salida': 'regresion'
        })
    
    def _get_funciones_activacion_optimales(self, tipo: TipoRedNeural) -> List[str]:
        """Obtiene funciones de activación óptimas para cada tipo de red"""
        configuraciones = {
            TipoRedNeural.PREDICCION_PRECIOS: ['relu', 'relu', 'leaky_relu'],
            TipoRedNeural.DETECCION_PATRONES: ['relu', 'swish', 'sigmoid'],
            TipoRedNeural.OPTIMIZACION_ESTRATEGIA: ['leaky_relu', 'swish', 'tanh'],
            TipoRedNeural.RECONOCIMIENTO_OPORTUNIDADES: ['relu', 'relu', 'sigmoid'],
            TipoRedNeural.EVALUACION_RIESGOS: ['relu', 'leaky_relu', 'sigmoid'],
            TipoRedNeural.NEGOCIACION_INTELIGENTE: ['swish', 'relu', 'tanh']
        }
        
        return configuraciones.get(tipo, ['relu', 'relu', 'sigmoid'])
    
    def entrenar_red_con_datos(self, tipo: TipoRedNeural, 
                              datos_entrenamiento: List[Tuple[List[float], List[float]]],
                              epocas: int = 100) -> Dict[str, float]:
        """Entrena una red específica con datos"""
        if tipo not in self.redes_especializadas:
            self.crear_red_especializada(tipo)
        
        red = self.redes_especializadas[tipo]
        
        # Registrar contexto para meta-aprendizaje
        contexto = {
            'tipo_problema': tipo.value,
            'tamano_datos': len(datos_entrenamiento),
            'epocas': epocas
        }
        
        # Entrenar red
        resultado = red.entrenar_lote(datos_entrenamiento, epocas)
        
        # Registrar experiencia para meta-aprendizaje
        self.meta_aprendizaje.registrar_experiencia_aprendizaje(contexto, resultado)
        
        self.redes_entrenadas += 1
        
        return resultado
    
    def optimizar_parametros_agente(self, agente_id: str, parametros_iniciales: List[float],
                                  funcion_evaluacion: Callable[[List[float]], float],
                                  max_generaciones: int = 50) -> List[float]:
        """Optimiza parámetros de un agente usando algoritmos evolutivos"""
        
        # Determinar algoritmo óptimo
        caracteristicas_problema = {
            'dimension': len(parametros_iniciales),
            'tipo_funcion': 'multimodal',  # Asumimos función multimodal
            'tiempo_disponible': 'medio'
        }
        
        tipo_algoritmo = self.meta_aprendizaje.get_estrategia_optimizacion(caracteristicas_problema)
        
        # Crear optimizador
        optimizador_id = f"opt_{agente_id}_{int(time.time())}"
        optimizador = OptimizadorEvolutivo(
            tipo_algoritmo=tipo_algoritmo,
            dimension_problema=len(parametros_iniciales),
            tamano_poblacion=30
        )
        
        # Establecer parámetros iniciales en la población
        if parametros_iniciales:
            optimizador.poblacion[0].genes = parametros_iniciales.copy()
        
        # Ejecutar optimización
        mejor_individuo = optimizador.optimizar(funcion_evaluacion, max_generaciones)
        
        # Registrar optimizador
        self.optimizadores[optimizador_id] = optimizador
        self.optimizaciones_completadas += 1
        
        print(f"[DEEP LEARNING] Parámetros optimizados para {agente_id}, fitness: {mejor_individuo.fitness:.6f}")
        
        return mejor_individuo.genes
    
    def predecir_con_red(self, tipo: TipoRedNeural, entradas: List[float]) -> List[float]:
        """Realiza predicción usando una red específica"""
        if tipo not in self.redes_especializadas:
            raise ValueError(f"Red {tipo.value} no ha sido creada")
        
        red = self.redes_especializadas[tipo]
        return red.predecir(entradas)
    
    def entrenar_automatico_continuo(self, intervalo_minutos: int = 30):
        """Inicia entrenamiento automático continuo"""
        if self.entrenando:
            print("[DEEP LEARNING] Entrenamiento continuo ya está activo")
            return
        
        self.entrenando = True
        
        def ciclo_entrenamiento():
            while self.entrenando:
                try:
                    # Entrenar redes que tengan datos suficientes
                    for tipo, datos in self.datos_entrenamiento.items():
                        if len(datos) >= 20:  # Mínimo de datos para entrenamiento
                            if tipo in self.redes_especializadas:
                                # Re-entrenar con nuevos datos
                                self.entrenar_red_con_datos(tipo, datos[-100:], epocas=10)
                            else:
                                # Crear y entrenar nueva red
                                self.crear_red_especializada(tipo)
                                self.entrenar_red_con_datos(tipo, datos, epocas=50)
                    
                    # Optimizar redes existentes ocasionalmente
                    if random.random() < 0.3:  # 30% de probabilidad
                        self._optimizar_redes_existentes()
                    
                except Exception as e:
                    print(f"[DEEP LEARNING] Error en entrenamiento continuo: {e}")
                
                time.sleep(intervalo_minutos * 60)
        
        self.hilo_entrenamiento = threading.Thread(target=ciclo_entrenamiento)
        self.hilo_entrenamiento.daemon = True
        self.hilo_entrenamiento.start()
        
        print(f"[DEEP LEARNING] Entrenamiento continuo iniciado (cada {intervalo_minutos} minutos)")
    
    def _optimizar_redes_existentes(self):
        """Optimiza redes existentes usando técnicas avanzadas"""
        for tipo, red in self.redes_especializadas.items():
            if len(self.datos_entrenamiento[tipo]) > 50:
                # Ajustar tasa de aprendizaje dinámicamente
                if red.precision_actual > 0.9:
                    red.tasa_aprendizaje *= 0.8  # Reducir para refinamiento
                elif red.precision_actual < 0.6:
                    red.tasa_aprendizaje *= 1.2  # Aumentar para escape de mínimos locales
                
                # Re-entrenar con parámetros ajustados
                datos_recientes = self.datos_entrenamiento[tipo][-50:]
                red.entrenar_lote(datos_recientes, epocas=5)
    
    def agregar_datos_entrenamiento(self, tipo: TipoRedNeural, 
                                  entradas: List[float], salidas: List[float]):
        """Agrega datos de entrenamiento para una red específica"""
        self.datos_entrenamiento[tipo].append((entradas, salidas))
        
        # Mantener solo últimos 1000 ejemplos por tipo
        if len(self.datos_entrenamiento[tipo]) > 1000:
            self.datos_entrenamiento[tipo] = self.datos_entrenamiento[tipo][-1000:]
    
    def obtener_estadisticas(self) -> Dict[str, Any]:
        """Obtiene estadísticas del sistema de Deep Learning"""
        return {
            'redes_activas': len(self.redes_especializadas),
            'redes_entrenadas': self.redes_entrenadas,
            'optimizaciones_completadas': self.optimizaciones_completadas,
            'datos_entrenamiento_total': sum(len(datos) for datos in self.datos_entrenamiento.values()),
            'entrenamiento_activo': self.entrenando,
            'precision_promedio': np.mean([red.precision_actual for red in self.redes_especializadas.values()]) if self.redes_especializadas else 0.0,
            'adaptaciones_meta_aprendizaje': self.meta_aprendizaje.adaptaciones_automaticas,
            'optimizadores_activos': len(self.optimizadores)
        }
    
    def entrenar_con_datos_recientes(self, tipo_red: Optional[TipoRedNeural] = None):
        """Entrena redes con los datos más recientes"""
        try:
            if tipo_red:
                # Entrenar red específica
                if tipo_red in self.redes_especializadas and tipo_red in self.datos_entrenamiento:
                    red = self.redes_especializadas[tipo_red]
                    datos = self.datos_entrenamiento[tipo_red]
                    if len(datos) > 10:  # Mínimo de datos para entrenamiento
                        datos_recientes = datos[-50:]  # Últimos 50 ejemplos
                        red.entrenar_lote(datos_recientes, epocas=3)
                        print(f"[DEEP LEARNING] Red {tipo_red.value} entrenada con {len(datos_recientes)} ejemplos")
            else:
                # Entrenar todas las redes
                for tipo, red in self.redes_especializadas.items():
                    datos = self.datos_entrenamiento.get(tipo, [])
                    if len(datos) > 10:
                        datos_recientes = datos[-50:]
                        red.entrenar_lote(datos_recientes, epocas=3)
                
                print(f"[DEEP LEARNING] Todas las redes entrenadas con datos recientes")
                
        except Exception as e:
            print(f"[DEEP LEARNING] Error en entrenamiento: {e}")

    def get_estadisticas_sistema(self) -> Dict[str, Any]:
        """Obtiene estadísticas completas del sistema"""
        return {
            'redes_creadas': len(self.redes_especializadas),
            'redes_entrenadas': self.redes_entrenadas,
            'optimizaciones_completadas': self.optimizaciones_completadas,
            'adaptaciones_meta_aprendizaje': self.meta_aprendizaje.adaptaciones_automaticas,
            'datos_entrenamiento_total': sum(len(datos) for datos in self.datos_entrenamiento.values()),
            'entrenamiento_activo': self.entrenando,
            'redes_por_tipo': {tipo.value: red.precision_actual 
                              for tipo, red in self.redes_especializadas.items()},
            'optimizadores_activos': len(self.optimizadores),
            'experiencias_meta_aprendizaje': len(self.meta_aprendizaje.experiencias_aprendizaje)
        }
    
    def finalizar(self):
        """Finaliza el sistema de deep learning"""
        print("[DEEP LEARNING] Finalizando sistema...")
        
        self.entrenando = False
        
        if self.hilo_entrenamiento and self.hilo_entrenamiento.is_alive():
            self.hilo_entrenamiento.join(timeout=3.0)
        
        print("[DEEP LEARNING] Sistema finalizado")
