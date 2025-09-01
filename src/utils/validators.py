"""
Sistema de Validación Económica Formal
=====================================

Validadores automáticos para resultados de simulación económica
que verifican consistencia, rangos razonables y métricas clave.

Autor: Sistema de Validación Económica
Versión: 1.0
"""

import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


class TipoValidacion(Enum):
    """Tipos de validación económica"""
    CRITICA = "CRITICA"
    ADVERTENCIA = "ADVERTENCIA" 
    INFO = "INFO"


@dataclass
class ResultadoValidacion:
    """Resultado de una validación individual"""
    indicador: str
    valor_actual: float
    rango_esperado: Tuple[float, float]
    tipo: TipoValidacion
    mensaje: str
    escenario: str = "default"
    
    def to_dict(self) -> Dict:
        """Convierte a diccionario para JSON"""
        return {
            'indicador': self.indicador,
            'valor_actual': self.valor_actual,
            'rango_esperado': list(self.rango_esperado),
            'tipo': self.tipo.value,
            'mensaje': self.mensaje,
            'escenario': self.escenario
        }


class ValidadorEconomicoFormal:
    """
    Validador formal de KPIs económicos que verifica:
    - PIB en rangos razonables
    - Inflación dentro de límites estándar
    - Consistencia de stocks y flujos
    - Balances del sistema bancario
    """
    
    # Rangos estándar para validación económica
    RANGOS_KPIS = {
        'pib': (15000, 2000000),  # PIB en rango realista
        'inflacion_pct': (-10.0, 20.0),  # Inflación anual razonable
        'desempleo_pct': (0.0, 25.0),  # Desempleo máximo aceptable
        'empresas_activas': (1, 20),  # Número de empresas razonable
        'transacciones': (0, 100000),  # Volumen de transacciones
        'duracion_s': (0, 300),  # Tiempo de ejecución máximo
        # Rangos bancarios
        'ratio_prestamos_depositos': (0.0, 1.0),  # Ratio conservador
        'ratio_capital_depositos': (0.08, 0.5),  # Requisitos de capital
        'tasa_interes': (0.0, 25.0),  # Tasa de interés central
    }
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """Inicializa el validador"""
        self.logger = logger or logging.getLogger('ValidadorEconomico')
        self.resultados: List[ResultadoValidacion] = []
        self.validaciones_exitosas = 0
        self.advertencias = 0
        self.errores = 0
    
    def validar_pib(self, pib: float, escenario: str = "default") -> ResultadoValidacion:
        """Valida que el PIB esté en rango razonable"""
        rango = self.RANGOS_KPIS['pib']
        
        if rango[0] <= pib <= rango[1]:
            resultado = ResultadoValidacion(
                indicador='pib',
                valor_actual=pib,
                rango_esperado=rango,
                tipo=TipoValidacion.INFO,
                mensaje=f"PIB {pib:,.2f} en rango normal",
                escenario=escenario
            )
            self.validaciones_exitosas += 1
        else:
            # PIB fuera de rango - determinar severidad
            if pib < rango[0] * 0.3 or pib > rango[1] * 1.5:
                tipo = TipoValidacion.CRITICA
                self.errores += 1
            else:
                tipo = TipoValidacion.ADVERTENCIA
                self.advertencias += 1
                
            resultado = ResultadoValidacion(
                indicador='pib',
                valor_actual=pib,
                rango_esperado=rango,
                tipo=tipo,
                mensaje=f"PIB {pib:,.2f} fuera de rango esperado [{rango[0]:,.0f}, {rango[1]:,.0f}]",
                escenario=escenario
            )
            
        self.resultados.append(resultado)
        return resultado
    
    def validar_inflacion(self, inflacion_pct: float, escenario: str = "default") -> ResultadoValidacion:
        """Valida que la inflación esté en rango razonable"""
        rango = self.RANGOS_KPIS['inflacion_pct']
        
        if rango[0] <= inflacion_pct <= rango[1]:
            resultado = ResultadoValidacion(
                indicador='inflacion_pct',
                valor_actual=inflacion_pct,
                rango_esperado=rango,
                tipo=TipoValidacion.INFO,
                mensaje=f"Inflación {inflacion_pct:.2f}% en rango normal",
                escenario=escenario
            )
            self.validaciones_exitosas += 1
        else:
            # Inflación fuera de rango
            if abs(inflacion_pct) > 50:  # Hiperinflación o deflación severa
                tipo = TipoValidacion.CRITICA
                self.errores += 1
            else:
                tipo = TipoValidacion.ADVERTENCIA
                self.advertencias += 1
                
            resultado = ResultadoValidacion(
                indicador='inflacion_pct',
                valor_actual=inflacion_pct,
                rango_esperado=rango,
                tipo=tipo,
                mensaje=f"Inflación {inflacion_pct:.2f}% fuera de rango esperado [{rango[0]:.1f}%, {rango[1]:.1f}%]",
                escenario=escenario
            )
            
        self.resultados.append(resultado)
        return resultado
    
    def validar_sistema_bancario(self, depositos: float, prestamos: float, 
                                capital: float, escenario: str = "default") -> List[ResultadoValidacion]:
        """Valida la consistencia del sistema bancario"""
        resultados = []
        
        # 1. Ratio préstamos/depósitos
        if depositos > 0:
            ratio_prestamos = prestamos / depositos
            rango = self.RANGOS_KPIS['ratio_prestamos_depositos']
            
            if rango[0] <= ratio_prestamos <= rango[1]:
                resultado = ResultadoValidacion(
                    indicador='ratio_prestamos_depositos',
                    valor_actual=ratio_prestamos,
                    rango_esperado=rango,
                    tipo=TipoValidacion.INFO,
                    mensaje=f"Ratio préstamos/depósitos {ratio_prestamos:.3f} es conservador",
                    escenario=escenario
                )
                self.validaciones_exitosas += 1
            else:
                tipo = TipoValidacion.ADVERTENCIA if ratio_prestamos > rango[1] else TipoValidacion.INFO
                self.advertencias += 1 if tipo == TipoValidacion.ADVERTENCIA else 0
                
                resultado = ResultadoValidacion(
                    indicador='ratio_prestamos_depositos',
                    valor_actual=ratio_prestamos,
                    rango_esperado=rango,
                    tipo=tipo,
                    mensaje=f"Ratio préstamos/depósitos {ratio_prestamos:.3f} fuera de rango conservador",
                    escenario=escenario
                )
            
            resultados.append(resultado)
        
        # 2. Ratio capital/depósitos (adecuación de capital)
        if depositos > 0:
            ratio_capital = capital / depositos
            rango = self.RANGOS_KPIS['ratio_capital_depositos']
            
            if rango[0] <= ratio_capital <= rango[1]:
                resultado = ResultadoValidacion(
                    indicador='ratio_capital_depositos',
                    valor_actual=ratio_capital,
                    rango_esperado=rango,
                    tipo=TipoValidacion.INFO,
                    mensaje=f"Ratio capital/depósitos {ratio_capital:.3f} cumple requisitos",
                    escenario=escenario
                )
                self.validaciones_exitosas += 1
            else:
                tipo = TipoValidacion.CRITICA if ratio_capital < rango[0] else TipoValidacion.ADVERTENCIA
                if tipo == TipoValidacion.CRITICA:
                    self.errores += 1
                else:
                    self.advertencias += 1
                    
                resultado = ResultadoValidacion(
                    indicador='ratio_capital_depositos',
                    valor_actual=ratio_capital,
                    rango_esperado=rango,
                    tipo=tipo,
                    mensaje=f"Ratio capital/depósitos {ratio_capital:.3f} {'insuficiente' if ratio_capital < rango[0] else 'excesivo'}",
                    escenario=escenario
                )
            
            resultados.append(resultado)
        
        self.resultados.extend(resultados)
        return resultados
    
    def validar_consistencia_stocks_flujos(self, datos_simulacion: Dict, 
                                         escenario: str = "default") -> List[ResultadoValidacion]:
        """Valida consistencia entre stocks y flujos económicos"""
        resultados = []
        
        # Verificar que las transacciones sean consistentes con el PIB
        if 'transacciones' in datos_simulacion and 'pib' in datos_simulacion:
            transacciones = datos_simulacion['transacciones']
            pib = datos_simulacion['pib']
            
            # PIB debería tener alguna correlación con transacciones
            if pib > 0 and transacciones == 0:
                resultado = ResultadoValidacion(
                    indicador='consistencia_transacciones_pib',
                    valor_actual=transacciones,
                    rango_esperado=(1, 100000),
                    tipo=TipoValidacion.ADVERTENCIA,
                    mensaje=f"PIB {pib:,.2f} pero 0 transacciones - posible inconsistencia",
                    escenario=escenario
                )
                self.advertencias += 1
                resultados.append(resultado)
            else:
                resultado = ResultadoValidacion(
                    indicador='consistencia_transacciones_pib',
                    valor_actual=transacciones,
                    rango_esperado=(0, 100000),
                    tipo=TipoValidacion.INFO,
                    mensaje=f"Transacciones {transacciones} consistentes con PIB {pib:,.2f}",
                    escenario=escenario
                )
                self.validaciones_exitosas += 1
                resultados.append(resultado)
        
        # Verificar empresas activas vs PIB
        if 'empresas_activas' in datos_simulacion and 'pib' in datos_simulacion:
            empresas = datos_simulacion['empresas_activas']
            pib = datos_simulacion['pib']
            
            if empresas == 0 and pib > 0:
                resultado = ResultadoValidacion(
                    indicador='consistencia_empresas_pib',
                    valor_actual=empresas,
                    rango_esperado=(1, 20),
                    tipo=TipoValidacion.CRITICA,
                    mensaje=f"PIB {pib:,.2f} sin empresas activas - inconsistencia crítica",
                    escenario=escenario
                )
                self.errores += 1
                resultados.append(resultado)
        
        self.resultados.extend(resultados)
        return resultados
    
    def validar_datos_completos(self, datos_simulacion: Dict, 
                               escenario: str = "default") -> ResultadoValidacion:
        """Valida que todos los datos económicos principales estén presentes"""
        campos_requeridos = ['pib', 'inflacion', 'desempleo', 'empresas_activas', 'transacciones']
        campos_faltantes = [campo for campo in campos_requeridos if campo not in datos_simulacion]
        
        if not campos_faltantes:
            resultado = ResultadoValidacion(
                indicador='datos_completos',
                valor_actual=len(campos_requeridos),
                rango_esperado=(len(campos_requeridos), len(campos_requeridos)),
                tipo=TipoValidacion.INFO,
                mensaje="Todos los datos económicos principales están presentes",
                escenario=escenario
            )
            self.validaciones_exitosas += 1
        else:
            resultado = ResultadoValidacion(
                indicador='datos_completos',
                valor_actual=len(campos_requeridos) - len(campos_faltantes),
                rango_esperado=(len(campos_requeridos), len(campos_requeridos)),
                tipo=TipoValidacion.ADVERTENCIA,
                mensaje=f"Campos económicos faltantes: {', '.join(campos_faltantes)}",
                escenario=escenario
            )
            self.advertencias += 1
        
        self.resultados.append(resultado)
        return resultado
    
    def ejecutar_validacion_completa(self, datos_simulacion: Dict, 
                                   escenario: str = "default") -> Dict:
        """Ejecuta validación completa de datos de simulación"""
        self.resultados.clear()
        self.validaciones_exitosas = 0
        self.advertencias = 0
        self.errores = 0
        
        # 1. Validar datos completos
        self.validar_datos_completos(datos_simulacion, escenario)
        
        # 2. Validar KPIs principales
        if 'pib' in datos_simulacion:
            self.validar_pib(datos_simulacion['pib'], escenario)
        
        if 'inflacion' in datos_simulacion:
            self.validar_inflacion(datos_simulacion['inflacion'], escenario)
        
        # 3. Validar sistema bancario si hay datos
        if all(k in datos_simulacion for k in ['depositos_bancarios', 'prestamos_totales']):
            depositos = datos_simulacion['depositos_bancarios']
            prestamos = datos_simulacion['prestamos_totales']
            capital = datos_simulacion.get('capital_bancario', depositos * 0.1)  # Default 10%
            self.validar_sistema_bancario(depositos, prestamos, capital, escenario)
        
        # 4. Validar consistencia de stocks y flujos
        self.validar_consistencia_stocks_flujos(datos_simulacion, escenario)
        
        return self.generar_reporte_completo()
    
    def generar_reporte_completo(self) -> Dict:
        """Genera reporte completo de validación"""
        reporte = {
            'timestamp': datetime.now().isoformat(),
            'resumen': {
                'validaciones_exitosas': self.validaciones_exitosas,
                'advertencias': self.advertencias,
                'errores': self.errores,
                'total_validaciones': len(self.resultados)
            },
            'validaciones': [r.to_dict() for r in self.resultados],
            'estado_general': self._determinar_estado_general()
        }
        
        return reporte
    
    def _determinar_estado_general(self) -> str:
        """Determina el estado general del sistema"""
        if self.errores > 0:
            return "CRITICO"
        elif self.advertencias > 3:
            return "ADVERTENCIA"
        elif self.advertencias > 0:
            return "ACEPTABLE"
        else:
            return "ESTABLE"
    
    def guardar_reporte_json(self, ruta: str = None) -> str:
        """Guarda el reporte de validación en formato JSON"""
        if ruta is None:
            timestamp = int(datetime.now().timestamp())
            ruta = f"results/validation_report_{timestamp}.json"
        
        # Asegurar que el directorio existe
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        
        reporte = self.generar_reporte_completo()
        
        with open(ruta, 'w', encoding='utf-8') as f:
            json.dump(reporte, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Reporte de validación guardado en: {ruta}")
        return ruta


def validar_resultados_simulacion(datos_simulacion: Dict, escenario: str = "main_simulation") -> Dict:
    """
    Función principal para validar resultados de simulación.
    
    Args:
        datos_simulacion: Diccionario con métricas de la simulación
        escenario: Nombre del escenario ejecutado
    
    Returns:
        Diccionario con reporte completo de validación
    """
    validador = ValidadorEconomicoFormal()
    return validador.ejecutar_validacion_completa(datos_simulacion, escenario)