"""
Sistema de Rescate Empresarial para prevenir colapso económico
Implementa rescates, fusiones y liquidaciones ordenadas
"""

import random
import math
from ..utils.SimuladorLogger import get_simulador_logger

class GestorRescateEmpresarial:
    """Gestiona rescates empresariales para mantener estabilidad económica"""
    
    def __init__(self, mercado):
        self.mercado = mercado
        self.fondo_rescate_porcentaje = 0.05  # 5% del PIB
        self.criterio_importancia_sistemica = 0.7  # Umbral para rescate
        
        # Historial de rescates
        self.empresas_rescatadas = []
        self.fusiones_realizadas = []
        self.liquidaciones_ejecutadas = []
        
        # Parámetros de rescate
        self.factor_rescate = 1.2  # 120% de la deuda para rescate
        self.max_rescates_por_ciclo = 2
        
        self.logger = get_simulador_logger()
        
    def evaluar_y_rescatar_empresas(self, ciclo):
        """Evalúa empresas en crisis y aplica medidas de rescate"""
        
        # Calcular fondo disponible
        fondo_disponible = self._calcular_fondo_rescate()
        
        # Identificar empresas en crisis
        empresas_en_crisis = self._identificar_empresas_en_crisis()
        
        if not empresas_en_crisis:
            return
        
        # Evaluar cada empresa para rescate
        rescates_ejecutados = 0
        for empresa in empresas_en_crisis:
            if rescates_ejecutados >= self.max_rescates_por_ciclo:
                break
                
            decision = self._evaluar_empresa_para_rescate(empresa, fondo_disponible)
            
            if decision['accion'] == 'RESCATAR':
                if self._ejecutar_rescate(empresa, decision['monto'], ciclo):
                    fondo_disponible -= decision['monto']
                    rescates_ejecutados += 1
                    
            elif decision['accion'] == 'FUSIONAR':
                socio_potencial = decision.get('socio')
                if socio_potencial and self._ejecutar_fusion(empresa, socio_potencial, ciclo):
                    rescates_ejecutados += 1
                    
            elif decision['accion'] == 'LIQUIDAR':
                self._ejecutar_liquidacion_ordenada(empresa, ciclo)
        
        # Log resumen de actividad
        if rescates_ejecutados > 0:
            self.logger.log_sistema(f"Rescate Empresarial - Ciclo {ciclo}: {rescates_ejecutados} acciones ejecutadas")
    
    def _calcular_fondo_rescate(self):
        """Calcula el fondo disponible para rescates"""
        pib_actual = self.mercado.pib_historico[-1] if self.mercado.pib_historico else 100000
        fondo_total = pib_actual * self.fondo_rescate_porcentaje
        
        # Descontar rescates ya utilizados en este período
        rescates_recientes = sum(r['monto'] for r in self.empresas_rescatadas[-5:])  # Últimos 5 rescates
        
        return max(0, fondo_total - rescates_recientes)
    
    def _identificar_empresas_en_crisis(self):
        """Identifica empresas que requieren intervención"""
        empresas_en_crisis = []
        
        for empresa in self.mercado.getEmpresas():
            if self._esta_en_crisis(empresa):
                empresas_en_crisis.append(empresa)
        
        # Ordenar por importancia sistémica (más importante primero)
        empresas_en_crisis.sort(key=self._calcular_importancia_sistemica, reverse=True)
        
        return empresas_en_crisis
    
    def _esta_en_crisis(self, empresa):
        """Determina si una empresa está en crisis"""
        if not hasattr(empresa, 'dinero'):
            return False
            
        # Criterios de crisis
        patrimonio_negativo = empresa.dinero < 0
        insolvencia_severa = empresa.dinero < -10000
        empresa_grande = self._es_empresa_grande(empresa)
        
        # Crisis si: patrimonio negativo Y (insolvencia severa O empresa grande)
        return patrimonio_negativo and (insolvencia_severa or empresa_grande)
    
    def _es_empresa_grande(self, empresa):
        """Determina si es una empresa grande (sistémicamente importante)"""
        # Criterios de tamaño
        muchos_empleados = hasattr(empresa, 'empleados') and len(empresa.empleados) > 10
        muchos_productos = hasattr(empresa, 'bienes') and len(empresa.bienes) > 5
        sector_critico = self._es_sector_critico(empresa)
        
        return muchos_empleados or muchos_productos or sector_critico
    
    def _es_sector_critico(self, empresa):
        """Determina si la empresa pertenece a un sector crítico"""
        sectores_criticos = ['alimentos_basicos', 'servicios', 'energia']
        
        if hasattr(empresa, 'bienes'):
            for bien in empresa.bienes.keys():
                if hasattr(self.mercado.bienes.get(bien), 'categoria'):
                    categoria = self.mercado.bienes[bien].categoria
                    if categoria in sectores_criticos:
                        return True
        
        return False
    
    def _calcular_importancia_sistemica(self, empresa):
        """Calcula un score de importancia sistémica (0-1)"""
        score = 0.0
        
        # Factor empleados (0-0.4)
        if hasattr(empresa, 'empleados'):
            num_empleados = len(empresa.empleados)
            score += min(0.4, num_empleados / 50)  # Máximo 0.4 con 50+ empleados
        
        # Factor productos (0-0.3)
        if hasattr(empresa, 'bienes'):
            num_productos = len(empresa.bienes)
            score += min(0.3, num_productos / 10)  # Máximo 0.3 con 10+ productos
        
        # Factor sector crítico (0-0.3)
        if self._es_sector_critico(empresa):
            score += 0.3
        
        return min(1.0, score)
    
    def _evaluar_empresa_para_rescate(self, empresa, fondo_disponible):
        """Evalúa qué acción tomar con una empresa en crisis"""
        
        importancia = self._calcular_importancia_sistemica(empresa)
        costo_rescate = abs(empresa.dinero) * self.factor_rescate
        viabilidad = self._evaluar_viabilidad_futura(empresa)
        
        # Decisión basada en importancia sistémica y viabilidad
        if importancia >= self.criterio_importancia_sistemica:
            if viabilidad > 0.6 and costo_rescate <= fondo_disponible:
                return {
                    'accion': 'RESCATAR',
                    'monto': costo_rescate,
                    'justificacion': f'Empresa sistémicamente importante (score: {importancia:.2f})'
                }
            elif viabilidad > 0.4:
                # Buscar socio para fusión
                socio = self._buscar_socio_fusion(empresa)
                if socio:
                    return {
                        'accion': 'FUSIONAR',
                        'socio': socio,
                        'justificacion': f'Fusión con {socio.nombre} para preservar empleo'
                    }
        
        # Si no califica para rescate o fusión
        if viabilidad < 0.3:
            return {
                'accion': 'LIQUIDAR',
                'justificacion': f'Empresa no viable (viabilidad: {viabilidad:.2f})'
            }
        
        # Default: dejar que la empresa maneje su crisis
        return {
            'accion': 'MONITOREAR',
            'justificacion': 'Crisis manejable sin intervención'
        }
    
    def _evaluar_viabilidad_futura(self, empresa):
        """Evalúa la viabilidad futura de la empresa (0-1)"""
        score_viabilidad = 0.5  # Base neutral
        
        # Factor empleados (empresa con empleados más viable)
        if hasattr(empresa, 'empleados') and empresa.empleados:
            score_viabilidad += 0.2
        
        # Factor productos (diversificación)
        if hasattr(empresa, 'bienes'):
            if len(empresa.bienes) > 3:
                score_viabilidad += 0.2
            elif len(empresa.bienes) > 1:
                score_viabilidad += 0.1
        
        # Factor sector (sectores críticos más viables)
        if self._es_sector_critico(empresa):
            score_viabilidad += 0.2
        
        # Factor ciclo económico
        if hasattr(self.mercado, 'fase_ciclo_economico'):
            if self.mercado.fase_ciclo_economico in ['expansion', 'recuperacion']:
                score_viabilidad += 0.1
            elif self.mercado.fase_ciclo_economico in ['recesion', 'depresion']:
                score_viabilidad -= 0.1
        
        # Factor gravedad de la crisis
        if hasattr(empresa, 'dinero'):
            if empresa.dinero < -50000:  # Crisis muy severa
                score_viabilidad -= 0.3
            elif empresa.dinero < -20000:  # Crisis moderada
                score_viabilidad -= 0.1
        
        return max(0.0, min(1.0, score_viabilidad))
    
    def _buscar_socio_fusion(self, empresa_crisis):
        """Busca una empresa compatible para fusión"""
        candidatos = []
        
        for empresa in self.mercado.getEmpresas():
            if empresa == empresa_crisis:
                continue
            
            # Debe ser empresa sana
            if hasattr(empresa, 'dinero') and empresa.dinero > 20000:
                # Debe tener productos relacionados o complementarios
                if self._son_compatibles_fusion(empresa_crisis, empresa):
                    candidatos.append(empresa)
        
        # Retornar el candidato más fuerte
        if candidatos:
            return max(candidatos, key=lambda e: getattr(e, 'dinero', 0))
        
        return None
    
    def _son_compatibles_fusion(self, empresa1, empresa2):
        """Determina si dos empresas son compatibles para fusión"""
        if not (hasattr(empresa1, 'bienes') and hasattr(empresa2, 'bienes')):
            return False
        
        # Productos en común o complementarios
        productos1 = set(empresa1.bienes.keys())
        productos2 = set(empresa2.bienes.keys())
        
        # Compatible si tienen algunos productos en común pero no todos (complementarios)
        interseccion = productos1.intersection(productos2)
        total_productos = productos1.union(productos2)
        
        # Compatibles si 20-80% de productos en común
        if len(total_productos) > 0:
            overlap_ratio = len(interseccion) / len(total_productos)
            return 0.2 <= overlap_ratio <= 0.8
        
        return False
    
    def _ejecutar_rescate(self, empresa, monto, ciclo):
        """Ejecuta el rescate de una empresa"""
        # Inyectar capital
        empresa.dinero += monto
        
        # Registrar rescate
        rescate = {
            'empresa': empresa.nombre,
            'monto': monto,
            'ciclo': ciclo,
            'tipo': 'rescate_capital'
        }
        self.empresas_rescatadas.append(rescate)
        
        # Log del rescate
        self.logger.log_sistema(f"🚑 RESCATE: {empresa.nombre} rescatada con ${monto:,.0f}")
        
        # Aplicar condiciones del rescate (reestructuración)
        self._aplicar_condiciones_rescate(empresa)
        
        return True
    
    def _ejecutar_fusion(self, empresa_crisis, empresa_sana, ciclo):
        """Ejecuta la fusión de dos empresas"""
        try:
            # Transferir activos
            if hasattr(empresa_crisis, 'empleados') and hasattr(empresa_sana, 'empleados'):
                # Transferir empleados
                for empleado in empresa_crisis.empleados.copy():
                    if len(empresa_sana.empleados) < 30:  # Límite de empleados
                        empleado.empleador = empresa_sana
                        empresa_sana.empleados.append(empleado)
                        empresa_crisis.empleados.remove(empleado)
                    else:
                        # Despedir si no hay capacidad
                        empleado.empleado = False
                        empleado.empleador = None
                        empresa_crisis.empleados.remove(empleado)
            
            # Transferir productos rentables
            if hasattr(empresa_crisis, 'bienes') and hasattr(empresa_sana, 'bienes'):
                for bien, inventario in empresa_crisis.bienes.items():
                    if bien not in empresa_sana.bienes:
                        empresa_sana.bienes[bien] = inventario
            
            # Transferir capital positivo
            if hasattr(empresa_crisis, 'dinero') and empresa_crisis.dinero > 0:
                empresa_sana.dinero += empresa_crisis.dinero * 0.5  # Solo 50% del capital
            
            # Eliminar empresa en crisis del mercado
            if empresa_crisis in self.mercado.personas:
                self.mercado.personas.remove(empresa_crisis)
            
            # Registrar fusión
            fusion = {
                'empresa_absorbida': empresa_crisis.nombre,
                'empresa_absorbente': empresa_sana.nombre,
                'ciclo': ciclo
            }
            self.fusiones_realizadas.append(fusion)
            
            self.logger.log_sistema(f"🤝 FUSIÓN: {empresa_crisis.nombre} fusionada con {empresa_sana.nombre}")
            
            return True
            
        except Exception as e:
            self.logger.log_error(f"Error en fusión: {e}")
            return False
    
    def _ejecutar_liquidacion_ordenada(self, empresa, ciclo):
        """Ejecuta liquidación ordenada de empresa no viable"""
        try:
            # Despedir empleados con compensación
            if hasattr(empresa, 'empleados'):
                for empleado in empresa.empleados:
                    empleado.empleado = False
                    empleado.empleador = None
                    # Compensación básica (simplificada)
                    if hasattr(empleado, 'dinero'):
                        empleado.dinero += 1000  # Compensación por despido
            
            # Liquidar inventarios a precios reducidos
            if hasattr(empresa, 'bienes'):
                for bien in empresa.bienes:
                    # Reducir precios para liquidación rápida
                    if hasattr(empresa, 'precios') and bien in empresa.precios:
                        empresa.precios[bien] *= 0.7  # 30% de descuento
            
            # Eliminar empresa del mercado después de 2 ciclos
            # (para permitir liquidación de inventarios)
            empresa._programada_liquidacion = ciclo + 2
            
            # Registrar liquidación
            liquidacion = {
                'empresa': empresa.nombre,
                'ciclo': ciclo,
                'empleados_afectados': len(getattr(empresa, 'empleados', []))
            }
            self.liquidaciones_ejecutadas.append(liquidacion)
            
            self.logger.log_sistema(f"📉 LIQUIDACIÓN: {empresa.nombre} liquidada ordenadamente")
            
            return True
            
        except Exception as e:
            self.logger.log_error(f"Error en liquidación: {e}")
            return False
    
    def _aplicar_condiciones_rescate(self, empresa):
        """Aplica condiciones de reestructuración tras rescate"""
        # Reducir costos operativos
        if hasattr(empresa, 'costos_fijos'):
            empresa.costos_fijos *= 0.85  # Reducir 15% costos fijos
        
        # Mejorar eficiencia
        if hasattr(empresa, 'productividad'):
            empresa.productividad *= 1.1  # Aumentar 10% productividad
        
        # Límites de crecimiento temporal
        empresa._rescatada_recientemente = True
    
    def procesar_liquidaciones_programadas(self, ciclo):
        """Procesa empresas programadas para liquidación"""
        empresas_a_liquidar = []
        
        for empresa in self.mercado.getEmpresas():
            if hasattr(empresa, '_programada_liquidacion'):
                if ciclo >= empresa._programada_liquidacion:
                    empresas_a_liquidar.append(empresa)
        
        for empresa in empresas_a_liquidar:
            if empresa in self.mercado.personas:
                self.mercado.personas.remove(empresa)
            self.logger.log_sistema(f"🗑️ LIQUIDACIÓN FINAL: {empresa.nombre} removida del mercado")
    
    def obtener_estadisticas_rescate(self):
        """Obtiene estadísticas del sistema de rescate"""
        return {
            'rescates_totales': len(self.empresas_rescatadas),
            'fusiones_totales': len(self.fusiones_realizadas),
            'liquidaciones_totales': len(self.liquidaciones_ejecutadas),
            'fondo_disponible': self._calcular_fondo_rescate(),
            'empresas_en_crisis': len(self._identificar_empresas_en_crisis())
        }
