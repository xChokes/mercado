"""
Sistema Fiscal Avanzado para Simulación Económica Hiperrealista
Implementa impuestos progresivos, IVA, política fiscal automática y redistribución
"""

import random
import math
from enum import Enum
from ..utils.SimuladorLogger import get_simulador_logger


class TipoImpuesto(Enum):
    RENTA = "renta"
    IVA = "iva"
    CORPORATIVO = "corporativo"
    PATRIMONIO = "patrimonio"
    SEGURIDAD_SOCIAL = "seguridad_social"


class PoliticaFiscal(Enum):
    EXPANSIVA = "expansiva"        # Más gasto, menos impuestos
    CONTRACTIVA = "contractiva"    # Menos gasto, más impuestos
    NEUTRAL = "neutral"            # Balance estable


class SistemaFiscal:
    """Sistema fiscal completo con impuestos progresivos y política fiscal automática"""
    
    def __init__(self, mercado):
        self.mercado = mercado
        self.logger = get_simulador_logger()
        
        # === ESTRUCTURA TRIBUTARIA ===
        # Impuesto a la Renta (progresivo)
        self.escalas_renta = [
            (0, 24000, 0.19),      # 19% hasta $24,000
            (24000, 60000, 0.24),  # 24% de $24,001 a $60,000
            (60000, 120000, 0.35), # 35% de $60,001 a $120,000
            (120000, float('inf'), 0.45)  # 45% sobre $120,000
        ]
        
        # IVA por categoría de bien
        self.iva_rates = {
            'alimentos_basicos': 0.0,    # Exento
            'alimentos_lujo': 0.10,      # 10% reducido
            'bienes_duraderos': 0.21,    # 21% general
            'tecnologia': 0.21,          # 21% general
            'servicios': 0.21,           # 21% general
            'servicios_lujo': 0.25,      # 25% lujo
            'capital': 0.0,              # Exento
            'intermedio': 0.10           # 10% reducido
        }
        
        # Impuesto corporativo
        self.impuesto_corporativo = 0.25  # 25%
        
        # Impuesto al patrimonio (anual)
        self.impuesto_patrimonio = 0.002  # 0.2%
        self.umbral_patrimonio = 500000   # Aplica sobre $500K
        
        # Seguridad social
        self.contrib_social_empleado = 0.11   # 11% empleado
        self.contrib_social_empleador = 0.17  # 17% empleador
        
        # === RECAUDACIÓN Y GASTO ===
        self.recaudacion_total = 0
        self.recaudacion_por_tipo = {tipo: 0 for tipo in TipoImpuesto}
        self.gasto_publico_total = 0
        
        # === POLÍTICA FISCAL AUTOMÁTICA ===
        self.politica_actual = PoliticaFiscal.NEUTRAL
        self.deficit_fiscal = 0
        self.deuda_publica = 0
        self.multiplicador_fiscal = 1.2  # Efecto multiplicador
        
        # === PROGRAMAS SOCIALES ===
        self.programas_sociales = {
            'seguro_desempleo': {'rate': 0.6, 'duracion_max': 12},  # 60% salario por 12 ciclos
            'pension_minima': 15000,    # Pensión mínima
            'subsidio_vivienda': 8000,  # Subsidio habitacional
            'transferencias_condicionadas': 5000  # Programas focalizados
        }
        
        self.logger.log_configuracion("Sistema Fiscal Avanzado inicializado")
        self.logger.log_configuracion(f"   Escalas de renta: {len(self.escalas_renta)} tramos")
        self.logger.log_configuracion(f"   IVA diferenciado por {len(self.iva_rates)} categorías")
        
    def ejecutar_ciclo_fiscal(self, ciclo):
        """Ejecuta el ciclo fiscal completo: recaudación + gasto + política"""
        
        # 1. Recaudar impuestos
        self._recaudar_impuestos(ciclo)
        
        # 2. Ejecutar gasto público
        self._ejecutar_gasto_publico(ciclo)
        
        # 3. Evaluar y ajustar política fiscal
        self._evaluar_politica_fiscal(ciclo)
        
        # 4. Procesar programas sociales
        self._procesar_programas_sociales(ciclo)
        
        # 5. Actualizar estadísticas fiscales
        self._actualizar_estadisticas_fiscales(ciclo)
        
        return self._generar_reporte_fiscal(ciclo)
    
    def _recaudar_impuestos(self, ciclo):
        """Recauda todos los tipos de impuestos"""
        recaudacion_ciclo = {tipo: 0 for tipo in TipoImpuesto}
        
        # === IMPUESTO A LA RENTA (PERSONAS) ===
        for consumidor in self.mercado.getConsumidores():
            if consumidor.empleado and consumidor.ingreso_mensual > 0:
                impuesto_renta = self._calcular_impuesto_renta(consumidor.ingreso_mensual)
                consumidor.dinero -= impuesto_renta
                recaudacion_ciclo[TipoImpuesto.RENTA] += impuesto_renta
                
                # Seguridad social empleado
                contrib_empleado = consumidor.ingreso_mensual * self.contrib_social_empleado
                consumidor.dinero -= contrib_empleado
                recaudacion_ciclo[TipoImpuesto.SEGURIDAD_SOCIAL] += contrib_empleado
        
        # === IMPUESTO CORPORATIVO ===
        for empresa in self.mercado.getEmpresas():
            if hasattr(empresa, 'dinero') and empresa.dinero > 0:
                # Estimar utilidades (simplificado)
                utilidades_estimadas = max(0, empresa.dinero * 0.05)  # 5% del capital como utilidad
                impuesto_corp = utilidades_estimadas * self.impuesto_corporativo
                empresa.dinero -= impuesto_corp
                recaudacion_ciclo[TipoImpuesto.CORPORATIVO] += impuesto_corp
                
                # Seguridad social empleador
                if hasattr(empresa, 'empleados'):
                    for empleado in empresa.empleados:
                        contrib_empleador = empleado.ingreso_mensual * self.contrib_social_empleador
                        empresa.dinero -= contrib_empleador
                        recaudacion_ciclo[TipoImpuesto.SEGURIDAD_SOCIAL] += contrib_empleador
        
        # === IVA (en transacciones) ===
        # Se aplica automáticamente en las transacciones (ver método aplicar_iva)
        
        # === IMPUESTO AL PATRIMONIO (anual, cada 12 ciclos) ===
        if ciclo % 12 == 0:  # Una vez al año
            for consumidor in self.mercado.getConsumidores():
                if consumidor.dinero > self.umbral_patrimonio:
                    impuesto_patrim = (consumidor.dinero - self.umbral_patrimonio) * self.impuesto_patrimonio
                    consumidor.dinero -= impuesto_patrim
                    recaudacion_ciclo[TipoImpuesto.PATRIMONIO] += impuesto_patrim
        
        # Actualizar recaudación total
        for tipo, monto in recaudacion_ciclo.items():
            self.recaudacion_por_tipo[tipo] += monto
            self.recaudacion_total += monto
        
        self.logger.log_sistema(f"Fiscal - Ciclo {ciclo}: Recaudación ${sum(recaudacion_ciclo.values()):,.0f}")
    
    def _calcular_impuesto_renta(self, ingreso_anual):
        """Calcula impuesto a la renta con escalas progresivas"""
        impuesto = 0
        
        for escala_min, escala_max, tasa in self.escalas_renta:
            if ingreso_anual > escala_min:
                base_imponible = min(ingreso_anual, escala_max) - escala_min
                impuesto += base_imponible * tasa
            
            if ingreso_anual <= escala_max:
                break
        
        return impuesto
    
    def aplicar_iva(self, precio_base, categoria_bien):
        """Aplica IVA según categoría del bien"""
        tasa_iva = self.iva_rates.get(categoria_bien, 0.21)  # 21% por defecto
        iva = precio_base * tasa_iva
        precio_final = precio_base + iva
        
        # Registrar recaudación IVA
        self.recaudacion_por_tipo[TipoImpuesto.IVA] += iva
        self.recaudacion_total += iva
        
        return precio_final
    
    def _ejecutar_gasto_publico(self, ciclo):
        """Ejecuta el gasto público según política fiscal"""
        if not hasattr(self.mercado, 'gobierno'):
            return
            
        # Calcular gasto público objetivo (% del PIB)
        pib_actual = self.mercado.pib_historico[-1] if self.mercado.pib_historico else 100000
        
        if self.politica_actual == PoliticaFiscal.EXPANSIVA:
            gasto_objetivo = pib_actual * 0.35  # 35% del PIB
        elif self.politica_actual == PoliticaFiscal.CONTRACTIVA:
            gasto_objetivo = pib_actual * 0.25  # 25% del PIB
        else:
            gasto_objetivo = pib_actual * 0.30  # 30% del PIB
        
        # Distribuir gasto público
        gasto_ejecutado = min(gasto_objetivo, self.mercado.gobierno.presupuesto)
        
        # 40% infraestructura y servicios (impulso directo al PIB)
        gasto_infraestructura = gasto_ejecutado * 0.40
        self._ejecutar_gasto_infraestructura(gasto_infraestructura)
        
        # 35% transferencias a personas
        gasto_transferencias = gasto_ejecutado * 0.35
        self._ejecutar_transferencias_directas(gasto_transferencias)
        
        # 25% salarios sector público
        gasto_salarios_publicos = gasto_ejecutado * 0.25
        self._ejecutar_salarios_publicos(gasto_salarios_publicos)
        
        self.gasto_publico_total += gasto_ejecutado
        self.mercado.gobierno.presupuesto -= gasto_ejecutado
        
        self.logger.log_sistema(f"Fiscal - Gasto público: ${gasto_ejecutado:,.0f} ({self.politica_actual.value})")
    
    def _ejecutar_gasto_infraestructura(self, monto):
        """Gasto en infraestructura - impulsa demanda agregada"""
        # Compras gubernamentales directas a empresas
        empresas = self.mercado.getEmpresas()
        if empresas:
            gasto_por_empresa = monto / len(empresas)
            for empresa in empresas:
                empresa.dinero += gasto_por_empresa * random.uniform(0.5, 1.5)  # Distribución realista
    
    def _ejecutar_transferencias_directas(self, monto):
        """Transferencias directas a consumidores"""
        consumidores = self.mercado.getConsumidores()
        if consumidores:
            # Focalizar en quintiles más bajos
            consumidores_ordenados = sorted(consumidores, key=lambda c: c.dinero)
            quintil_inferior = consumidores_ordenados[:len(consumidores)//5]
            
            if quintil_inferior:
                transferencia_promedio = monto / len(quintil_inferior)
                for consumidor in quintil_inferior:
                    consumidor.dinero += transferencia_promedio
    
    def _ejecutar_salarios_publicos(self, monto):
        """Salarios del sector público"""
        # Crear empleados públicos virtuales o aumentar ingresos existentes
        consumidores = self.mercado.getConsumidores()
        empleados_publicos = random.sample(consumidores, min(len(consumidores)//10, 25))  # 10% empleados públicos
        
        if empleados_publicos:
            salario_promedio = monto / len(empleados_publicos)
            for empleado in empleados_publicos:
                empleado.dinero += salario_promedio
                empleado.ingreso_mensual += salario_promedio * 0.1  # Aumentar ingreso base
    
    def _evaluar_politica_fiscal(self, ciclo):
        """Evalúa automáticamente si cambiar política fiscal"""
        if len(self.mercado.pib_historico) < 3:
            return
            
        # Indicadores económicos
        pib_actual = self.mercado.pib_historico[-1]
        pib_anterior = self.mercado.pib_historico[-2]
        crecimiento_pib = (pib_actual - pib_anterior) / pib_anterior if pib_anterior > 0 else 0
        
        desempleo = self._calcular_tasa_desempleo()
        inflacion = self.mercado.inflacion_historica[-1] if self.mercado.inflacion_historica else 0
        
        # Reglas de política fiscal automática
        politica_anterior = self.politica_actual
        
        # POLÍTICA EXPANSIVA: Crisis o alto desempleo
        if crecimiento_pib < -0.02 or desempleo > 0.12:  # Recesión o desempleo >12%
            self.politica_actual = PoliticaFiscal.EXPANSIVA
            
        # POLÍTICA CONTRACTIVA: Sobrecalentamiento o alta inflación
        elif crecimiento_pib > 0.05 and inflacion > 0.04:  # Crecimiento >5% e inflación >4%
            self.politica_actual = PoliticaFiscal.CONTRACTIVA
            
        # POLÍTICA NEUTRAL: Condiciones normales
        else:
            self.politica_actual = PoliticaFiscal.NEUTRAL
        
        # Log cambio de política
        if self.politica_actual != politica_anterior:
            self.logger.log_sistema(f"Cambio Política Fiscal: {politica_anterior.value} → {self.politica_actual.value}")
            self.logger.log_sistema(f"   Justificación: PIB {crecimiento_pib:.1%}, Desempleo {desempleo:.1%}, Inflación {inflacion:.1%}")
    
    def _procesar_programas_sociales(self, ciclo):
        """Procesa programas sociales y transferencias condicionadas"""
        # Seguro de desempleo
        desempleados = [c for c in self.mercado.getConsumidores() if not c.empleado]
        
        for desempleado in desempleados:
            if not hasattr(desempleado, 'ciclos_desempleo'):
                desempleado.ciclos_desempleo = 0
            
            desempleado.ciclos_desempleo += 1
            
            # Pagar seguro de desempleo (máximo 12 ciclos)
            if desempleado.ciclos_desempleo <= 12:
                seguro = self.programas_sociales['seguro_desempleo']['rate'] * 3000  # 60% de salario promedio
                desempleado.dinero += seguro
                self.gasto_publico_total += seguro
        
        # Pensión mínima (personas >65 años)
        jubilados = [c for c in self.mercado.getConsumidores() if getattr(c, 'edad', 30) >= 65]
        for jubilado in jubilados:
            pension = self.programas_sociales['pension_minima']
            jubilado.dinero += pension
            self.gasto_publico_total += pension
    
    def _calcular_tasa_desempleo(self):
        """Calcula la tasa de desempleo actual"""
        consumidores = self.mercado.getConsumidores()
        desempleados = len([c for c in consumidores if not c.empleado])
        return desempleados / len(consumidores) if consumidores else 0
    
    def _actualizar_estadisticas_fiscales(self, ciclo):
        """Actualiza estadísticas fiscales del ciclo"""
        # Calcular déficit/superávit fiscal
        self.deficit_fiscal = self.gasto_publico_total - self.recaudacion_total
        
        # Actualizar deuda pública
        if self.deficit_fiscal > 0:
            self.deuda_publica += self.deficit_fiscal
        else:
            self.deuda_publica = max(0, self.deuda_publica + self.deficit_fiscal)  # Pagar deuda con superávit
    
    def _generar_reporte_fiscal(self, ciclo):
        """Genera reporte completo del ciclo fiscal"""
        pib_actual = self.mercado.pib_historico[-1] if self.mercado.pib_historico else 100000
        
        return {
            'ciclo': ciclo,
            'recaudacion_total': self.recaudacion_total,
            'recaudacion_por_tipo': dict(self.recaudacion_por_tipo),
            'gasto_publico': self.gasto_publico_total,
            'deficit_fiscal': self.deficit_fiscal,
            'deficit_pib_ratio': self.deficit_fiscal / pib_actual if pib_actual > 0 else 0,
            'deuda_publica': self.deuda_publica,
            'deuda_pib_ratio': self.deuda_publica / pib_actual if pib_actual > 0 else 0,
            'politica_fiscal': self.politica_actual.value,
            'presion_fiscal': self.recaudacion_total / pib_actual if pib_actual > 0 else 0
        }
    
    def obtener_estadisticas_fiscales(self):
        """Obtiene estadísticas fiscales consolidadas"""
        pib_actual = self.mercado.pib_historico[-1] if self.mercado.pib_historico else 100000
        
        return {
            'recaudacion_total': self.recaudacion_total,
            'recaudacion_renta': self.recaudacion_por_tipo[TipoImpuesto.RENTA],
            'recaudacion_iva': self.recaudacion_por_tipo[TipoImpuesto.IVA],
            'recaudacion_corporativo': self.recaudacion_por_tipo[TipoImpuesto.CORPORATIVO],
            'gasto_publico_total': self.gasto_publico_total,
            'deficit_fiscal': self.deficit_fiscal,
            'deuda_publica': self.deuda_publica,
            'presion_fiscal_pib': self.recaudacion_total / pib_actual if pib_actual > 0 else 0,
            'politica_actual': self.politica_actual.value,
            'multiplicador_fiscal_estimado': self.multiplicador_fiscal
        }
