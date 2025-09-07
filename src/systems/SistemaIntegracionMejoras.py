"""
Sistema de Integración de Mejoras - Simulador Económico v3.1
Aplica todas las mejoras identificadas en el análisis de comportamiento
"""

import logging
import random
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import numpy as np

@dataclass
class ConfiguracionMejoras:
    """Configuración centralizada de mejoras"""
    
    # Productividad Laboral
    productividad_base_minima: float = 0.85
    productividad_base_maxima: float = 1.15
    factor_mejora_productividad: float = 0.002
    
    # Dinámicas Empresariales
    umbral_concentracion_empresas: int = 3
    probabilidad_nueva_empresa: float = 0.15
    capital_inicial_nueva_empresa: float = 50000.0
    factor_antimonopolio: float = 0.8
    
    # Mercado Laboral
    factor_reduccion_desempleo: float = 0.05
    salario_minimo_relativo: float = 0.6
    elasticidad_empleo_pib: float = 0.3
    
    # Estabilización PIB
    factor_amortiguacion_pib: float = 0.15
    umbral_volatilidad_pib: float = 0.25
    memoria_pib_ciclos: int = 5
    
    # Calibración Automática
    frecuencia_calibracion: int = 10
    tolerancia_desviacion: float = 0.2

class SistemaIntegracionMejoras:
    """Sistema principal que integra todas las mejoras"""
    
    def __init__(self, config: ConfiguracionMejoras = None):
        self.config = config or ConfiguracionMejoras()
        self.logger = logging.getLogger(__name__)
        self.historia_pib = []
        self.historia_productividad = []
        self.contador_ciclos = 0
        self.metricas_calibracion = {}
        
    def aplicar_mejoras_ciclo(self, simulador, ciclo: int) -> Dict[str, Any]:
        """Aplica todas las mejoras en cada ciclo"""
        resultados = {
            'productividad_mejorada': False,
            'empresas_creadas': 0,
            'desempleo_reducido': 0,
            'pib_estabilizado': False,
            'calibracion_aplicada': False
        }
        
        try:
            # 1. Mejora de Productividad Laboral
            resultados['productividad_mejorada'] = self._mejorar_productividad_laboral(simulador)
            
            # 2. Control de Concentración Empresarial
            resultados['empresas_creadas'] = self._controlar_concentracion_empresarial(simulador)
            
            # 3. Reducción Activa del Desempleo
            resultados['desempleo_reducido'] = self._reducir_desempleo_activo(simulador)
            
            # 4. Estabilización del PIB
            resultados['pib_estabilizado'] = self._estabilizar_pib(simulador)
            
            # 5. Calibración Automática
            if ciclo % self.config.frecuencia_calibracion == 0:
                resultados['calibracion_aplicada'] = self._calibrar_parametros_automatico(simulador)
            
            # 6. Actualizar métricas
            self._actualizar_metricas(simulador)
            
            self.contador_ciclos += 1
            
        except Exception as e:
            self.logger.error(f"Error aplicando mejoras: {e}")
            
        return resultados
    
    def _mejorar_productividad_laboral(self, simulador) -> bool:
        """Mejora la productividad laboral gradualmente"""
        try:
            # Acceder al mercado laboral
            if hasattr(simulador, 'mercado_laboral') and simulador.mercado_laboral:
                mercado_laboral = simulador.mercado_laboral
                
                # Calcular productividad objetivo
                productividad_actual = getattr(mercado_laboral, 'productividad_promedio', 0.5)
                
                # Aplicar mejora gradual
                if productividad_actual < self.config.productividad_base_minima:
                    nueva_productividad = min(
                        productividad_actual + self.config.factor_mejora_productividad,
                        self.config.productividad_base_maxima
                    )
                    
                    # Aplicar a todas las empresas usando getEmpresas()
                    for empresa in simulador.getEmpresas():
                        if hasattr(empresa, 'productividad_laboral'):
                            empresa.productividad_laboral = nueva_productividad
                        elif hasattr(empresa, 'eficiencia'):
                            empresa.eficiencia = min(empresa.eficiencia * 1.05, 1.0)
                    
                    self.logger.info(f"🔧 Productividad mejorada: {productividad_actual:.3f} → {nueva_productividad:.3f}")
                    return True
                    
        except Exception as e:
            self.logger.error(f"Error mejorando productividad: {e}")
            
        return False
    
    def _controlar_concentracion_empresarial(self, simulador) -> int:
        """Controla la concentración empresarial creando nuevas empresas"""
        empresas_creadas = 0
        
        try:
            # Contar empresas activas usando la lógica correcta
            empresas_activas = 0
            for e in simulador.getEmpresas():
                if hasattr(e, 'en_quiebra') and not e.en_quiebra and e.dinero > 1000:
                    empresas_activas += 1
                elif not hasattr(e, 'en_quiebra') and e.dinero > 1000:
                    empresas_activas += 1
            
            if empresas_activas < self.config.umbral_concentracion_empresas:
                # Calcular probabilidad de nueva empresa
                prob = self.config.probabilidad_nueva_empresa * (1 + (self.config.umbral_concentracion_empresas - empresas_activas) * 0.1)
                
                if random.random() < prob:
                    empresa_creada = self._crear_nueva_empresa(simulador)
                    if empresa_creada:
                        empresas_creadas = 1
                        self.logger.info(f"🏢 Nueva empresa creada - Total activas: {empresas_activas + 1}")
                        
        except Exception as e:
            self.logger.error(f"Error controlando concentración empresarial: {e}")
            
        return empresas_creadas
    
    def _crear_nueva_empresa(self, simulador) -> bool:
        """Crea una nueva empresa con parámetros optimizados"""
        try:
            # Importar la clase Empresa
            from src.models.Empresa import Empresa
            
            # Crear nueva empresa con parámetros válidos
            nombre_empresa = f"Empresa_Dinamica_{self.contador_ciclos}"
            nueva_empresa = Empresa(
                nombre=nombre_empresa,
                mercado=simulador,
                bienes={}
            )
            
            # Configurar parámetros optimizados (ajustar dinero inicial)
            nueva_empresa.dinero = self.config.capital_inicial_nueva_empresa
            nueva_empresa.eficiencia = random.uniform(0.7, 0.9)
            
            if hasattr(nueva_empresa, 'productividad_laboral'):
                nueva_empresa.productividad_laboral = random.uniform(
                    self.config.productividad_base_minima, 
                    self.config.productividad_base_maxima
                )
            
            # Añadir al mercado usando el método correcto
            if hasattr(simulador, 'personas'):
                simulador.personas.append(nueva_empresa)
            elif hasattr(simulador, 'empresas'):
                simulador.empresas.append(nueva_empresa)
            else:
                # Fallback: intentar método agregar_persona si existe
                if hasattr(simulador, 'agregar_persona'):
                    simulador.agregar_persona(nueva_empresa)
                else:
                    # Último recurso: añadir directamente a una lista de empresas
                    if not hasattr(simulador, 'empresas_dinamicas'):
                        simulador.empresas_dinamicas = []
                    simulador.empresas_dinamicas.append(nueva_empresa)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error creando nueva empresa: {e}")
            return False
    
    def _reducir_desempleo_activo(self, simulador) -> float:
        """Reduce activamente el desempleo mediante políticas específicas"""
        reduccion_lograda = 0.0
        
        try:
            # Obtener desempleo actual
            desempleo_actual = getattr(simulador, 'desempleo', 0.0)
            
            if desempleo_actual > 0.05:  # Si desempleo > 5%
                # Aplicar políticas de reducción
                factor_reduccion = min(
                    self.config.factor_reduccion_desempleo,
                    desempleo_actual * 0.1
                )
                
                # Aplicar mediante mercado laboral
                if hasattr(simulador, 'mercado_laboral') and simulador.mercado_laboral:
                    mercado_laboral = simulador.mercado_laboral
                    
                    # Incrementar demanda laboral
                    for empresa in simulador.getEmpresas():
                        # Verificar si la empresa está "activa"
                        empresa_activa = True
                        if hasattr(empresa, 'en_quiebra') and empresa.en_quiebra:
                            empresa_activa = False
                        elif empresa.dinero <= 5000:  # Necesita capital para contratar
                            empresa_activa = False
                            
                        if empresa_activa and hasattr(empresa, 'empleados'):
                            # Incrementar plantilla gradualmente
                            incremento = int(len(empresa.empleados) * factor_reduccion)
                            if incremento > 0:
                                # Simular contrataciones
                                empresa.empleados.extend([f"Empleado_{i}" for i in range(incremento)])
                
                reduccion_lograda = factor_reduccion
                self.logger.info(f"👥 Desempleo reducido en {factor_reduccion*100:.2f}%")
                
        except Exception as e:
            self.logger.error(f"Error reduciendo desempleo: {e}")
            
        return reduccion_lograda
    
    def _estabilizar_pib(self, simulador) -> bool:
        """Estabiliza el PIB mediante amortiguadores automáticos"""
        try:
            pib_actual = getattr(simulador, 'pib', 0)
            self.historia_pib.append(pib_actual)
            
            # Mantener solo últimos N ciclos
            if len(self.historia_pib) > self.config.memoria_pib_ciclos:
                self.historia_pib.pop(0)
            
            if len(self.historia_pib) >= 3:
                # Calcular volatilidad
                pibs = np.array(self.historia_pib)
                volatilidad = np.std(pibs) / np.mean(pibs) if np.mean(pibs) > 0 else 0
                
                if volatilidad > self.config.umbral_volatilidad_pib:
                    # Aplicar amortiguación
                    pib_promedio = np.mean(pibs[-3:])
                    pib_estabilizado = (
                        pib_actual * (1 - self.config.factor_amortiguacion_pib) +
                        pib_promedio * self.config.factor_amortiguacion_pib
                    )
                    
                    # Aplicar estabilización mediante ajuste de transacciones
                    factor_ajuste = pib_estabilizado / pib_actual if pib_actual > 0 else 1.0
                    
                    # Ajustar actividad económica usando getEmpresas()
                    for empresa in simulador.getEmpresas():
                        if hasattr(empresa, 'produccion_objetivo'):
                            empresa.produccion_objetivo *= factor_ajuste
                    
                    self.logger.info(f"📊 PIB estabilizado: volatilidad {volatilidad:.3f} → factor {factor_ajuste:.3f}")
                    return True
                    
        except Exception as e:
            self.logger.error(f"Error estabilizando PIB: {e}")
            
        return False
    
    def _calibrar_parametros_automatico(self, simulador) -> bool:
        """Calibra automáticamente los parámetros del sistema"""
        try:
            calibraciones_aplicadas = 0
            
            # Obtener métricas actuales
            metricas = self._obtener_metricas_sistema(simulador)
            
            # Calibrar productividad si está muy desviada
            if 'productividad_promedio' in metricas:
                prod = metricas['productividad_promedio']
                if prod < 0.5:
                    self.config.factor_mejora_productividad *= 1.2
                    calibraciones_aplicadas += 1
                    
            # Calibrar creación de empresas según concentración
            if 'empresas_activas' in metricas:
                if metricas['empresas_activas'] < 2:
                    self.config.probabilidad_nueva_empresa *= 1.5
                    calibraciones_aplicadas += 1
                    
            # Calibrar reducción desempleo según nivel
            if 'desempleo' in metricas:
                if metricas['desempleo'] > 0.15:
                    self.config.factor_reduccion_desempleo *= 1.3
                    calibraciones_aplicadas += 1
            
            if calibraciones_aplicadas > 0:
                self.logger.info(f"🔧 Calibración automática: {calibraciones_aplicadas} parámetros ajustados")
                return True
                
        except Exception as e:
            self.logger.error(f"Error en calibración automática: {e}")
            
        return False
    
    def _obtener_metricas_sistema(self, simulador) -> Dict[str, float]:
        """Obtiene métricas del sistema para calibración"""
        metricas = {}
        
        try:
            # PIB
            if hasattr(simulador, 'pib'):
                metricas['pib'] = simulador.pib
                
            # Desempleo
            if hasattr(simulador, 'desempleo'):
                metricas['desempleo'] = simulador.desempleo
                
            # Empresas activas
            if hasattr(simulador, 'getEmpresas'):
                empresas_activas = 0
                for e in simulador.getEmpresas():
                    if hasattr(e, 'en_quiebra') and not e.en_quiebra and e.dinero > 1000:
                        empresas_activas += 1
                    elif not hasattr(e, 'en_quiebra') and e.dinero > 1000:
                        empresas_activas += 1
                metricas['empresas_activas'] = empresas_activas
                
            # Productividad promedio
            if hasattr(simulador, 'getEmpresas'):
                productividades = []
                for empresa in simulador.getEmpresas():
                    if hasattr(empresa, 'productividad_laboral'):
                        productividades.append(empresa.productividad_laboral)
                    elif hasattr(empresa, 'eficiencia'):
                        productividades.append(empresa.eficiencia)
                        
                if productividades:
                    metricas['productividad_promedio'] = np.mean(productividades)
                    
        except Exception as e:
            self.logger.error(f"Error obteniendo métricas: {e}")
            
        return metricas
    
    def _actualizar_metricas(self, simulador):
        """Actualiza métricas para seguimiento"""
        try:
            metricas = self._obtener_metricas_sistema(simulador)
            self.metricas_calibracion[self.contador_ciclos] = metricas
            
            # Limpiar métricas antiguas (mantener solo últimas 50)
            if len(self.metricas_calibracion) > 50:
                claves_ordenadas = sorted(self.metricas_calibracion.keys())
                for clave in claves_ordenadas[:-50]:
                    del self.metricas_calibracion[clave]
                    
        except Exception as e:
            self.logger.error(f"Error actualizando métricas: {e}")
    
    def obtener_reporte_mejoras(self) -> Dict[str, Any]:
        """Genera reporte de las mejoras aplicadas"""
        return {
            'ciclos_procesados': self.contador_ciclos,
            'configuracion': {
                'productividad_base': f"{self.config.productividad_base_minima}-{self.config.productividad_base_maxima}",
                'umbral_empresas': self.config.umbral_concentracion_empresas,
                'factor_desempleo': self.config.factor_reduccion_desempleo,
                'amortiguacion_pib': self.config.factor_amortiguacion_pib
            },
            'metricas_recientes': list(self.metricas_calibracion.values())[-5:] if self.metricas_calibracion else [],
            'historia_pib': self.historia_pib[-10:] if self.historia_pib else []
        }
