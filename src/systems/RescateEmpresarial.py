"""
Sistema de Rescate Empresarial y Gestión de Quiebras
Previene colapso empresarial total y mantiene economía funcionando
"""

import random
from ..utils.SimuladorLogger import get_simulador_logger

class GestorRescateEmpresarial:
    """Gestiona rescates empresariales y previene colapso económico"""
    
    def __init__(self, mercado):
        self.mercado = mercado
        self.fondo_rescate = 0
        self.empresas_rescatadas = []
        self.criterios_rescate = {
            'empleados_minimos': 10,
            'importancia_sectorial': 0.3,
            'deficit_maximo_rescatable': 100000
        }
        self.logger = get_simulador_logger()
        
        # Inicializar fondo de rescate
        self._inicializar_fondo_rescate()
    
    def _inicializar_fondo_rescate(self):
        """Inicializa fondo de rescate basado en tamaño de la economía"""
        pib_estimado = len(self.mercado.personas) * 2000  # Estimación básica
        self.fondo_rescate = pib_estimado * 0.05  # 5% del PIB para rescates
        
        self.logger.log_sistema(f"Fondo de rescate empresarial inicializado: ${self.fondo_rescate:,.0f}")
    
    def evaluar_rescate(self, empresa):
        """Evalúa si una empresa específica puede ser rescatada"""
        try:
            # Verificar si la empresa cumple criterios básicos para rescate
            if not self._empresa_en_problemas(empresa):
                return False
            
            # Evaluar la decisión de rescate
            decision = self._evaluar_rescate_vs_liquidacion(empresa)
            
            if decision == 'RESCATAR':
                return self._ejecutar_rescate(empresa, 0)  # ciclo = 0 por defecto
            elif decision == 'FUSIONAR':
                return self._buscar_fusion_empresa(empresa, 0)
            
            return False
            
        except Exception as e:
            self.logger.log_error(f"Error evaluando rescate para {empresa.nombre}: {e}")
            return False

    def evaluar_y_rescatar_empresas(self, ciclo):
        """Evalúa todas las empresas y rescata las que cumplan criterios"""
        empresas_rescatadas_ciclo = 0
        empresas_liquidadas_ciclo = 0
        
        for empresa in self.mercado.getEmpresas():
            if self._empresa_en_problemas(empresa):
                decision = self._evaluar_rescate_vs_liquidacion(empresa)
                
                if decision == 'RESCATAR':
                    if self._ejecutar_rescate(empresa, ciclo):
                        empresas_rescatadas_ciclo += 1
                elif decision == 'LIQUIDAR':
                    self._liquidar_empresa(empresa, ciclo)
                    empresas_liquidadas_ciclo += 1
                elif decision == 'FUSIONAR':
                    self._buscar_fusion_empresa(empresa, ciclo)
        
        if empresas_rescatadas_ciclo > 0 or empresas_liquidadas_ciclo > 0:
            self.logger.log_sistema(
                f"Ciclo {ciclo}: {empresas_rescatadas_ciclo} empresas rescatadas, "
                f"{empresas_liquidadas_ciclo} liquidadas"
            )
    
    def _empresa_en_problemas(self, empresa):
        """Determina si una empresa está en problemas serios - CRITERIOS MÁS SENSIBLES"""
        # CRITERIOS ULTRA PERMISIVOS para detectar empresas en riesgo temprano
        
        # Criterio 1: Dinero insuficiente para 2 ciclos (vs 5000 negativos antes)
        dinero_insuficiente = False
        if hasattr(empresa, 'dinero'):
            if hasattr(empresa, '_calcular_costos_operativos'):
                try:
                    costos_estimados = empresa._calcular_costos_operativos()
                    dinero_insuficiente = empresa.dinero < (costos_estimados * 2)  # 2 ciclos de supervivencia
                except:
                    dinero_insuficiente = empresa.dinero < 5000  # Fallback
            else:
                dinero_insuficiente = empresa.dinero < 5000
        
        # Criterio 2: Ciclos en crisis (más sensible)
        en_crisis_prolongada = False
        if hasattr(empresa, 'ciclos_crisis_financiera'):
            en_crisis_prolongada = empresa.ciclos_crisis_financiera >= 2  # 2 vs 3+ anteriormente
        elif hasattr(empresa, 'ciclos_sin_actividad'):
            en_crisis_prolongada = empresa.ciclos_sin_actividad >= 2
        
        # Criterio 3: Sin empleados (empresas fantasma)
        sin_empleados = False
        if hasattr(empresa, 'empleados'):
            sin_empleados = len(empresa.empleados) == 0
        
        # Criterio 4: Producción nula reciente
        sin_produccion = False
        if hasattr(empresa, 'produccion_actual'):
            produccion_total = sum(empresa.produccion_actual.values())
            sin_produccion = produccion_total == 0
        
        # Una empresa está en problemas si cumple CUALQUIERA de estos criterios
        en_problemas = dinero_insuficiente or en_crisis_prolongada or (sin_empleados and sin_produccion)
        
        if en_problemas:
            self.logger.log_debug(
                f"Empresa {empresa.nombre} detectada en problemas: "
                f"dinero_insuficiente={dinero_insuficiente}, crisis={en_crisis_prolongada}, "
                f"sin_empleados={sin_empleados}, sin_produccion={sin_produccion}"
            )
        
        return en_problemas
    
    def _empresa_sin_ventas_recientes(self, empresa):
        """Verifica si empresa no ha tenido ventas recientes"""
        # Simplificado: si tiene inventario pero dinero negativo
        if hasattr(empresa, 'bienes') and hasattr(empresa, 'dinero'):
            tiene_inventario = any(
                len(items) > 0 for items in empresa.bienes.values()
            )
            return tiene_inventario and empresa.dinero < -1000
        return False
    
    def _costos_exceden_capacidad(self, empresa):
        """Verifica si los costos exceden capacidad de la empresa"""
        if hasattr(empresa, 'dinero') and hasattr(empresa, 'empleados'):
            costo_salarios = len(empresa.empleados) * 3000  # Asumimos $3k salario promedio
            return empresa.dinero < -(costo_salarios * 2)  # 2 meses de salarios
        return False
    
    def _evaluar_rescate_vs_liquidacion(self, empresa):
        """Evalúa si rescatar, fusionar o liquidar empresa - MÁS PERMISIVO"""
        viabilidad = self._evaluar_viabilidad_rescate(empresa)
        costo_rescate = self._estimar_costo_rescate(empresa)
        
        # CRITERIOS MUY PERMISIVOS: Priorizar rescate sobre liquidación
        
        # Si tiene empleados o capacidad productiva, SIEMPRE intentar rescate primero
        tiene_empleados = hasattr(empresa, 'empleados') and len(empresa.empleados) > 0
        tiene_capacidad = hasattr(empresa, 'capacidad_produccion') and sum(empresa.capacidad_produccion.values()) > 0
        
        if tiene_empleados or tiene_capacidad:
            # Con empleados o capacidad, rescatar si es remotamente viable
            if viabilidad >= 0.15:  # Bajar de 0.4 a 0.15
                return 'RESCATAR'
            else:
                return 'FUSIONAR'  # Intentar fusión antes de liquidar
        
        # Sin empleados ni capacidad, pero si es relativamente nueva o barata de rescatar
        if costo_rescate < self.fondo_rescate * 0.3:  # Menos del 30% del fondo
            if viabilidad >= 0.10:  # Muy permisivo para rescates baratos
                return 'RESCATAR'
        
        # Última oportunidad: fusión
        if viabilidad >= 0.05:  # Cualquier mínima viabilidad
            return 'FUSIONAR'
        
        # Solo liquidar como último recurso
        return 'LIQUIDAR'
    
    def _calcular_importancia_sistemica(self, empresa):
        """Calcula importancia sistémica de la empresa"""
        score = 0.0
        
        # Factor 1: Número de empleados
        if hasattr(empresa, 'empleados'):
            empleados = len(empresa.empleados)
            score += min(0.4, empleados / 50)  # Máximo 0.4 por empleados
        
        # Factor 2: Sector crítico
        if hasattr(empresa, 'sector'):
            sectores_criticos = ['alimentos_basicos', 'energia', 'salud', 'servicios']
            if any(sector in str(empresa.sector).lower() for sector in sectores_criticos):
                score += 0.3
        
        # Factor 3: Participación de mercado
        participacion = self._calcular_participacion_mercado(empresa)
        score += participacion * 0.3
        
        return min(1.0, score)
    
    def _evaluar_viabilidad_rescate(self, empresa):
        """Evalúa viabilidad de rescatar la empresa"""
        score = 0.0
        
        # Factor 1: Capacidad productiva
        if hasattr(empresa, 'bienes'):
            tiene_productos = len(empresa.bienes) > 0
            score += 0.3 if tiene_productos else 0
        
        # Factor 2: Capital humano
        if hasattr(empresa, 'empleados'):
            empleados_capacitados = len(empresa.empleados)
            score += min(0.4, empleados_capacitados / 20)
        
        # Factor 3: Posición de mercado
        if hasattr(empresa, 'precios'):
            competitividad = self._evaluar_competitividad_precios(empresa)
            score += competitividad * 0.3
        
        return min(1.0, score)
    
    def _estimar_costo_rescate(self, empresa):
        """Estima el costo de rescatar una empresa"""
        if not hasattr(empresa, 'dinero'):
            return 50000  # Costo por defecto
        
        # Costo base: cubrir deudas + capital de trabajo
        deuda = abs(min(0, empresa.dinero))
        capital_trabajo = 10000  # Capital de trabajo básico
        
        # Costo de reestructuración
        if hasattr(empresa, 'empleados'):
            costo_reestructuracion = len(empresa.empleados) * 1000
        else:
            costo_reestructuracion = 5000
        
        return deuda + capital_trabajo + costo_reestructuracion
    
    def _ejecutar_rescate(self, empresa, ciclo):
        """Ejecuta el rescate de una empresa - RESCATE MÁS GENEROSO"""
        costo_rescate = self._estimar_costo_rescate(empresa)
        
        # MEJORA: Rescatar incluso si excede el fondo (usar déficit temporal)
        puede_rescatar = (costo_rescate <= self.fondo_rescate or 
                         self.fondo_rescate >= 5000)  # Mínimo de emergencia
        
        if not puede_rescatar:
            self.logger.log_debug(f"Rescate de {empresa.nombre} rechazado: fondos insuficientes")
            return False
        
        # RESCATE INTEGRAL Y GENEROSO
        if hasattr(empresa, 'dinero'):
            # 1. Limpiar todas las deudas
            deuda_actual = abs(min(0, empresa.dinero))
            
            # 2. Inyección de capital generosa (150K vs 75K anterior)
            capital_rescate = max(150000, deuda_actual * 3)  # Triple de deuda o 150K mínimo
            empresa.dinero = capital_rescate
            
            # 3. Resetear contadores de crisis
            if hasattr(empresa, 'ciclos_crisis_financiera'):
                empresa.ciclos_crisis_financiera = 0
            if hasattr(empresa, 'ciclos_sin_actividad'):
                empresa.ciclos_sin_actividad = 0
            if hasattr(empresa, 'en_quiebra'):
                empresa.en_quiebra = False
            
            # 4. Reestructuración de costos agresiva (50% reducción)
            if hasattr(empresa, 'costos_fijos_mensuales'):
                if not hasattr(empresa, 'costos_fijos_originales'):
                    empresa.costos_fijos_originales = empresa.costos_fijos_mensuales
                empresa.costos_fijos_mensuales *= 0.5  # 50% reducción vs 20% anterior
            
            # 5. Mejora temporal de eficiencia
            if hasattr(empresa, 'eficiencia_produccion'):
                empresa.eficiencia_produccion = min(1.0, empresa.eficiencia_produccion * 1.15)
            
            # 6. Garantizar empleados mínimos
            if hasattr(empresa, 'empleados') and len(empresa.empleados) == 0:
                # Nota: El sistema de contratación se encargará en el próximo ciclo
                # Marcar para priorización en contratación
                if not hasattr(empresa, '_necesita_contratacion_urgente'):
                    empresa._necesita_contratacion_urgente = True
        
        # Actualizar contabilidad del rescate
        costo_real = min(costo_rescate, capital_rescate)
        self.fondo_rescate -= costo_real
        
        # Inicializar contador de empresas rescatadas si no existe
        if not hasattr(self, 'total_gastado'):
            self.total_gastado = 0
        if not hasattr(self, 'empresas_rescatadas'):
            self.empresas_rescatadas = []
            
        self.total_gastado += costo_real
        
        # Registrar rescate
        self.empresas_rescatadas.append({
            'empresa': empresa.nombre,
            'ciclo': ciclo,
            'costo': costo_rescate,
            'razon': 'importancia_sistemica'
        })
        
        self.logger.log_sistema(
            f"RESCATE EXITOSO: {empresa.nombre} rescatada con ${capital_rescate:,.0f} "
            f"(costo: ${costo_real:,.0f}, fondo restante: ${self.fondo_rescate:,.0f})"
        )
        
        return True
    
    def _aplicar_condiciones_rescate(self, empresa):
        """Aplica condiciones al rescate (reestructuración)"""
        # Reducir costos operativos
        if hasattr(empresa, 'empleados') and len(empresa.empleados) > 5:
            # Despedir 20% de empleados
            empleados_a_despedir = max(1, len(empresa.empleados) // 5)
            for _ in range(empleados_a_despedir):
                if empresa.empleados:
                    empleado = empresa.empleados.pop()
                    empleado.empleado = False
                    empleado.empleador = None
        
        # Mejorar eficiencia (simplificado)
        if hasattr(empresa, 'eficiencia'):
            empresa.eficiencia = min(1.0, empresa.eficiencia * 1.1)
    
    def _liquidar_empresa(self, empresa, ciclo):
        """Liquida una empresa no viable"""
        # Despedir todos los empleados
        if hasattr(empresa, 'empleados'):
            for empleado in empresa.empleados:
                empleado.empleado = False
                empleado.empleador = None
            empresa.empleados.clear()
        
        # Liquidar inventario a precios de liquidación
        if hasattr(empresa, 'bienes'):
            self._liquidar_inventario(empresa)
        
        # Marcar empresa como inactiva pero no eliminar
        # (en economías reales, empresas pueden reactivarse)
        empresa.activa = False
        empresa.dinero = 0
        
        self.logger.log_sistema(
            f"💀 LIQUIDACIÓN: {empresa.nombre} liquidada en ciclo {ciclo}"
        )
    
    def _buscar_fusion_empresa(self, empresa, ciclo):
        """Busca fusionar empresa con otra más sana"""
        empresas_candidatas = [
            e for e in self.mercado.getEmpresas()
            if hasattr(e, 'dinero') and e.dinero > 20000 and e != empresa
        ]
        
        if empresas_candidatas:
            empresa_adquirente = random.choice(empresas_candidatas)
            self._ejecutar_fusion(empresa, empresa_adquirente, ciclo)
    
    def _ejecutar_fusion(self, empresa_objetivo, empresa_adquirente, ciclo):
        """Ejecuta fusión entre dos empresas"""
        # Transferir empleados
        if hasattr(empresa_objetivo, 'empleados') and hasattr(empresa_adquirente, 'empleados'):
            empresa_adquirente.empleados.extend(empresa_objetivo.empleados)
            empresa_objetivo.empleados.clear()
        
        # Transferir inventario
        if hasattr(empresa_objetivo, 'bienes') and hasattr(empresa_adquirente, 'bienes'):
            for bien, items in empresa_objetivo.bienes.items():
                if bien in empresa_adquirente.bienes:
                    empresa_adquirente.bienes[bien].extend(items)
                else:
                    empresa_adquirente.bienes[bien] = items
            empresa_objetivo.bienes.clear()
        
        # Costos de integración
        if hasattr(empresa_adquirente, 'dinero'):
            empresa_adquirente.dinero -= 5000  # Costo de integración
        
        # Marcar empresa objetivo como fusionada
        empresa_objetivo.activa = False
        empresa_objetivo.dinero = 0
        
        self.logger.log_sistema(
            f"🤝 FUSIÓN: {empresa_objetivo.nombre} fusionada con {empresa_adquirente.nombre} en ciclo {ciclo}"
        )
    
    def _liquidar_inventario(self, empresa):
        """Liquida inventario de empresa en quiebra"""
        if hasattr(empresa, 'bienes'):
            valor_liquidacion = 0
            for bien, items in empresa.bienes.items():
                # Vender a 30% del precio de mercado
                precio_mercado = self._obtener_precio_mercado(bien)
                valor_item = precio_mercado * 0.3
                valor_liquidacion += len(items) * valor_item
            
            empresa.dinero += valor_liquidacion
            empresa.bienes.clear()
    
    def _calcular_participacion_mercado(self, empresa):
        """Calcula participación de mercado aproximada"""
        # Simplificado: basado en número de empleados vs total
        if not hasattr(empresa, 'empleados'):
            return 0.1
        
        total_empleados_sector = sum(
            len(e.empleados) for e in self.mercado.getEmpresas()
            if hasattr(e, 'empleados')
        )
        
        if total_empleados_sector > 0:
            return len(empresa.empleados) / total_empleados_sector
        return 0.1
    
    def _evaluar_competitividad_precios(self, empresa):
        """Evalúa competitividad de precios de la empresa"""
        # Simplificado: asumimos competitividad media
        return 0.5
    
    def _obtener_precio_mercado(self, bien):
        """Obtiene precio promedio de mercado para un bien"""
        precios = []
        for empresa in self.mercado.getEmpresas():
            if hasattr(empresa, 'precios') and bien in empresa.precios:
                precios.append(empresa.precios[bien])
        
        return sum(precios) / len(precios) if precios else 10.0
    
    def reponer_fondo_rescate(self, aporte_gobierno):
        """Repone fondo de rescate con aporte gubernamental"""
        self.fondo_rescate += aporte_gobierno
        
    def obtener_estadisticas_rescate(self):
        """Obtiene estadísticas del sistema de rescate"""
        return {
            'fondo_disponible': self.fondo_rescate,
            'empresas_rescatadas_total': len(self.empresas_rescatadas),
            'ultima_actividad': self.empresas_rescatadas[-1] if self.empresas_rescatadas else None
        }
