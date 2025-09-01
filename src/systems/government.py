"""
Sistema Gubernamental para Simulación Económica Hiperrealista
Implementa políticas fiscales, impuestos, gasto público, transferencias y deuda pública
con enfoque en el impacto en el PIB y contabilidad nacional
"""

from enum import Enum
from ..utils.SimuladorLogger import get_simulador_logger


class TipoPoliticaFiscal(Enum):
    EXPANSIVA = "expansiva"
    CONTRACTIVA = "contractiva" 
    NEUTRAL = "neutral"


class ComponentePIB(Enum):
    CONSUMO = "C"
    INVERSION = "I" 
    GASTO_GOBIERNO = "G"
    EXPORTACIONES_NETAS = "NX"


class Government:
    """
    Sistema gubernamental que maneja política fiscal, impuestos y gasto público
    con enfoque en el impacto sobre la contabilidad nacional y PIB (C+I+G+NX)
    """
    
    def __init__(self, mercado):
        self.mercado = mercado
        self.logger = get_simulador_logger()
        
        # Estado fiscal
        self.presupuesto_disponible = 1000000  # Presupuesto inicial
        self.deuda_publica = 0
        self.deficit_acumulado = 0
        
        # Política fiscal actual
        self.politica_fiscal = TipoPoliticaFiscal.NEUTRAL
        
        # Contabilidad nacional - componentes del PIB
        self.componentes_pib = {
            ComponentePIB.CONSUMO: 0,
            ComponentePIB.INVERSION: 0,
            ComponentePIB.GASTO_GOBIERNO: 0,
            ComponentePIB.EXPORTACIONES_NETAS: 0
        }
        
        # Histórico fiscal
        self.historial_fiscal = []
        self.historial_deuda = []
        
        # Configuración de impuestos
        self.tasas_impuestos = {
            'renta_personal': 0.25,
            'renta_corporativa': 0.30,
            'iva_general': 0.19,
            'iva_basicos': 0.05
        }
        
        # Configuración de gasto público (% del PIB)
        self.ratios_gasto = {
            'infraestructura': 0.12,  # 12% del PIB en infraestructura
            'transferencias': 0.08,   # 8% del PIB en transferencias
            'salarios_publicos': 0.06, # 6% del PIB en salarios públicos
            'servicios': 0.04         # 4% del PIB en servicios públicos
        }
        
        self.logger.log_configuracion("✅ Sistema Government inicializado")
    
    def ejecutar_ciclo_fiscal(self, ciclo):
        """Ejecuta un ciclo completo de política fiscal"""
        
        # 1. Calcular PIB preliminar para determinar política fiscal
        pib_preliminar = self._calcular_pib_preliminar()
        
        # 2. Recaudar impuestos
        recaudacion = self._recaudar_impuestos(pib_preliminar)
        
        # 3. Ejecutar gasto público
        gasto_ejecutado = self._ejecutar_gasto_publico(pib_preliminar)
        
        # 4. Calcular PIB final con todos los componentes
        pib_actual = self._calcular_pib_con_componentes()
        
        # 5. Calcular balance fiscal
        balance_fiscal = recaudacion - gasto_ejecutado
        
        # 6. Actualizar deuda pública
        self._actualizar_deuda_publica(balance_fiscal)
        
        # 7. Evaluar política fiscal
        self._evaluar_politica_fiscal(pib_actual, balance_fiscal)
        
        # 8. Registrar estadísticas
        self._registrar_estadisticas_fiscales(ciclo, recaudacion, gasto_ejecutado, balance_fiscal)
        
        return {
            'pib_total': pib_actual,
            'componentes_pib': dict(self.componentes_pib),
            'recaudacion': recaudacion,
            'gasto_publico': gasto_ejecutado,
            'balance_fiscal': balance_fiscal,
            'deuda_publica': self.deuda_publica,
            'politica_fiscal': self.politica_fiscal.value
        }
    
    def _calcular_pib_preliminar(self):
        """Calcula PIB preliminar para decisiones de política fiscal"""
        # Calcular solo C + I (sin G que aún no se ejecuta)
        consumo = self._calcular_consumo_privado()
        inversion = self._calcular_inversion_privada()
        exportaciones_netas = self._calcular_exportaciones_netas()
        
        return consumo + inversion + exportaciones_netas
    
    def _calcular_pib_con_componentes(self):
        """Calcula PIB siguiendo la fórmula C + I + G + (NX)"""
        
        # C - Consumo: Suma de todas las transacciones de consumo
        consumo = self._calcular_consumo_privado()
        
        # I - Inversión: Inversión empresarial y formación de capital
        inversion = self._calcular_inversion_privada()
        
        # G - Gasto Gobierno: Gasto público en bienes y servicios
        gasto_gobierno = self._calcular_gasto_gobierno()
        
        # NX - Exportaciones Netas: (Exportaciones - Importaciones)
        exportaciones_netas = self._calcular_exportaciones_netas()
        
        # Actualizar componentes
        self.componentes_pib[ComponentePIB.CONSUMO] = consumo
        self.componentes_pib[ComponentePIB.INVERSION] = inversion
        self.componentes_pib[ComponentePIB.GASTO_GOBIERNO] = gasto_gobierno
        self.componentes_pib[ComponentePIB.EXPORTACIONES_NETAS] = exportaciones_netas
        
        pib_total = consumo + inversion + gasto_gobierno + exportaciones_netas
        
        return pib_total
    
    def _calcular_consumo_privado(self):
        """Calcula el consumo privado (C)"""
        # Sumar transacciones del ciclo actual
        if hasattr(self.mercado, 'transacciones_ciclo_actual'):
            return sum([t.get('costo_total', 0) for t in self.mercado.transacciones_ciclo_actual])
        else:
            # Fallback: transacciones del ciclo actual
            transacciones_ciclo = [t for t in self.mercado.transacciones 
                                 if t.get('ciclo') == self.mercado.ciclo_actual]
            return sum([t.get('costo_total', 0) for t in transacciones_ciclo])
    
    def _calcular_inversion_privada(self):
        """Calcula la inversión privada (I)"""
        inversion_total = 0
        
        # Inversión empresarial
        for empresa in self.mercado.getEmpresas():
            if hasattr(empresa, 'dinero') and empresa.dinero > 0:
                # Estimar inversión como % del capital empresarial
                inversion_total += empresa.dinero * 0.08  # 8% del capital se reinvierte
            
            # Valor de inventario como inversión en capital de trabajo
            if hasattr(empresa, 'bienes'):
                for bien, lista_bien in empresa.bienes.items():
                    precio_bien = getattr(empresa, 'precios', {}).get(bien, 10)
                    inversion_total += len(lista_bien) * precio_bien * 0.05  # 5% del inventario
        
        return inversion_total
    
    def _calcular_gasto_gobierno(self):
        """Calcula el gasto del gobierno (G)"""
        # Este será el gasto público efectivo del ciclo actual
        return getattr(self, 'gasto_publico_ciclo', 0)
    
    def _calcular_exportaciones_netas(self):
        """Calcula exportaciones netas (NX = Exportaciones - Importaciones)"""
        # Por ahora, en una economía cerrada, NX = 0
        # En futuras versiones se puede implementar comercio internacional
        return 0
    
    def _recaudar_impuestos(self, pib):
        """Recauda impuestos sobre ingresos y actividad económica"""
        recaudacion_total = 0
        
        # Impuesto a la renta personal
        for consumidor in self.mercado.getConsumidores():
            if hasattr(consumidor, 'ingreso_mensual') and consumidor.ingreso_mensual > 0:
                impuesto = consumidor.ingreso_mensual * self.tasas_impuestos['renta_personal']
                if consumidor.dinero >= impuesto:
                    consumidor.dinero -= impuesto
                    recaudacion_total += impuesto
        
        # Impuesto corporativo
        for empresa in self.mercado.getEmpresas():
            if hasattr(empresa, 'dinero') and empresa.dinero > 1000:  # Solo empresas con capital suficiente
                impuesto = empresa.dinero * 0.02  # 2% mensual sobre capital
                impuesto = min(impuesto, empresa.dinero * 0.1)  # Máximo 10% del capital
                empresa.dinero -= impuesto
                recaudacion_total += impuesto
        
        # IVA aproximado (sobre consumo)
        consumo_privado = self.componentes_pib[ComponentePIB.CONSUMO]
        iva_estimado = consumo_privado * self.tasas_impuestos['iva_general']
        recaudacion_total += iva_estimado
        
        self.presupuesto_disponible += recaudacion_total
        return recaudacion_total
    
    def _ejecutar_gasto_publico(self, pib):
        """Ejecuta el gasto público según política fiscal"""
        
        # Calcular gasto objetivo según política fiscal
        if self.politica_fiscal == TipoPoliticaFiscal.EXPANSIVA:
            ratio_gasto = 0.35  # 35% del PIB
        elif self.politica_fiscal == TipoPoliticaFiscal.CONTRACTIVA:
            ratio_gasto = 0.25  # 25% del PIB
        else:
            ratio_gasto = 0.30  # 30% del PIB (neutral)
        
        gasto_objetivo = pib * ratio_gasto
        gasto_ejecutado = min(gasto_objetivo, self.presupuesto_disponible)
        
        # Distribuir gasto según ratios configurados
        gasto_infraestructura = gasto_ejecutado * 0.40  # 40% infraestructura
        gasto_transferencias = gasto_ejecutado * 0.35   # 35% transferencias
        gasto_salarios = gasto_ejecutado * 0.25         # 25% salarios públicos
        
        # Ejecutar cada tipo de gasto
        self._ejecutar_gasto_infraestructura(gasto_infraestructura)
        self._ejecutar_transferencias_sociales(gasto_transferencias)
        self._ejecutar_salarios_publicos(gasto_salarios)
        
        self.presupuesto_disponible -= gasto_ejecutado
        self.gasto_publico_ciclo = gasto_ejecutado
        
        return gasto_ejecutado
    
    def _ejecutar_gasto_infraestructura(self, monto):
        """Gasto en infraestructura que impulsa demanda agregada"""
        # Compras del gobierno a empresas
        empresas = self.mercado.getEmpresas()
        if empresas:
            gasto_por_empresa = monto / len(empresas)
            for empresa in empresas:
                empresa.dinero += gasto_por_empresa
    
    def _ejecutar_transferencias_sociales(self, monto):
        """Transferencias directas a ciudadanos"""
        consumidores = self.mercado.getConsumidores()
        if consumidores:
            # Focalizar en quintil más bajo de ingresos
            consumidores_ordenados = sorted(consumidores, key=lambda c: getattr(c, 'dinero', 0))
            beneficiarios = consumidores_ordenados[:len(consumidores)//5]  # 20% más pobre
            
            if beneficiarios:
                transferencia_promedio = monto / len(beneficiarios)
                for beneficiario in beneficiarios:
                    beneficiario.dinero += transferencia_promedio
    
    def _ejecutar_salarios_publicos(self, monto):
        """Salarios del sector público"""
        # Distribuir como salarios adicionales a una porción de la población
        consumidores = self.mercado.getConsumidores()
        if consumidores:
            # Simular 10% de la población como empleados públicos
            empleados_publicos = consumidores[:len(consumidores)//10]
            if empleados_publicos:
                salario_promedio = monto / len(empleados_publicos)
                for empleado in empleados_publicos:
                    empleado.dinero += salario_promedio
    
    def _actualizar_deuda_publica(self, balance_fiscal):
        """Actualiza la deuda pública según el balance fiscal"""
        if balance_fiscal < 0:  # Déficit
            self.deuda_publica += abs(balance_fiscal)
            self.deficit_acumulado += abs(balance_fiscal)
        else:  # Superávit
            self.deuda_publica = max(0, self.deuda_publica - balance_fiscal)
        
        self.historial_deuda.append(self.deuda_publica)
    
    def _evaluar_politica_fiscal(self, pib, balance_fiscal):
        """Evalúa automáticamente si cambiar la política fiscal"""
        # Criterios para cambio de política
        ratio_deuda_pib = self.deuda_publica / pib if pib > 0 else 0
        
        # Política expansiva si: alta deuda/PIB y recesión
        if ratio_deuda_pib < 0.6 and self._detectar_recesion():
            self.politica_fiscal = TipoPoliticaFiscal.EXPANSIVA
        
        # Política contractiva si: deuda muy alta
        elif ratio_deuda_pib > 0.9:
            self.politica_fiscal = TipoPoliticaFiscal.CONTRACTIVA
        
        # Política neutral en casos normales
        else:
            self.politica_fiscal = TipoPoliticaFiscal.NEUTRAL
    
    def _detectar_recesion(self):
        """Detecta si la economía está en recesión"""
        if len(self.mercado.pib_historico) < 3:
            return False
        
        # Recesión = 2 trimestres consecutivos de decrecimiento
        pib_actual = self.mercado.pib_historico[-1]
        pib_anterior = self.mercado.pib_historico[-2]
        pib_anterior2 = self.mercado.pib_historico[-3]
        
        return pib_actual < pib_anterior and pib_anterior < pib_anterior2
    
    def _registrar_estadisticas_fiscales(self, ciclo, recaudacion, gasto, balance):
        """Registra estadísticas fiscales del ciclo"""
        pib_actual = self.componentes_pib[ComponentePIB.CONSUMO] + \
                    self.componentes_pib[ComponentePIB.INVERSION] + \
                    self.componentes_pib[ComponentePIB.GASTO_GOBIERNO] + \
                    self.componentes_pib[ComponentePIB.EXPORTACIONES_NETAS]
        
        estadisticas = {
            'ciclo': ciclo,
            'pib_total': pib_actual,
            'consumo_c': self.componentes_pib[ComponentePIB.CONSUMO],
            'inversion_i': self.componentes_pib[ComponentePIB.INVERSION],
            'gasto_gobierno_g': self.componentes_pib[ComponentePIB.GASTO_GOBIERNO],
            'exportaciones_netas_nx': self.componentes_pib[ComponentePIB.EXPORTACIONES_NETAS],
            'recaudacion': recaudacion,
            'gasto_publico': gasto,
            'balance_fiscal': balance,
            'deuda_publica': self.deuda_publica,
            'ratio_deuda_pib': self.deuda_publica / pib_actual if pib_actual > 0 else 0,
            'politica_fiscal': self.politica_fiscal.value
        }
        
        self.historial_fiscal.append(estadisticas)
        
        self.logger.log_sistema(f"Fiscal - PIB: ${pib_actual:,.0f} = C${self.componentes_pib[ComponentePIB.CONSUMO]:,.0f} + I${self.componentes_pib[ComponentePIB.INVERSION]:,.0f} + G${self.componentes_pib[ComponentePIB.GASTO_GOBIERNO]:,.0f}")
        self.logger.log_sistema(f"Fiscal - Balance: ${balance:,.0f}, Deuda: ${self.deuda_publica:,.0f} ({self.deuda_publica/pib_actual*100:.1f}% PIB)")
    
    def obtener_balance_fiscal(self):
        """Obtiene el balance fiscal actual"""
        if self.historial_fiscal:
            return self.historial_fiscal[-1]['balance_fiscal']
        return 0
    
    def obtener_deuda_pib_ratio(self):
        """Obtiene el ratio deuda/PIB actual"""
        if self.historial_fiscal:
            return self.historial_fiscal[-1]['ratio_deuda_pib']
        return 0
    
    def obtener_componentes_pib(self):
        """Obtiene los componentes actuales del PIB"""
        return dict(self.componentes_pib)
    
    def generar_reporte_fiscal(self):
        """Genera un reporte completo del estado fiscal"""
        if not self.historial_fiscal:
            return "No hay datos fiscales disponibles"
        
        ultimo = self.historial_fiscal[-1]
        
        reporte = f"""
REPORTE FISCAL GUBERNAMENTAL
============================
PIB Total: ${ultimo['pib_total']:,.0f}
  - Consumo (C): ${ultimo['consumo_c']:,.0f} ({ultimo['consumo_c']/ultimo['pib_total']*100:.1f}%)
  - Inversión (I): ${ultimo['inversion_i']:,.0f} ({ultimo['inversion_i']/ultimo['pib_total']*100:.1f}%)
  - Gasto Gobierno (G): ${ultimo['gasto_gobierno_g']:,.0f} ({ultimo['gasto_gobierno_g']/ultimo['pib_total']*100:.1f}%)
  - Exp. Netas (NX): ${ultimo['exportaciones_netas_nx']:,.0f}

BALANCE FISCAL:
  - Recaudación: ${ultimo['recaudacion']:,.0f}
  - Gasto Público: ${ultimo['gasto_publico']:,.0f}
  - Balance: ${ultimo['balance_fiscal']:,.0f}
  - Deuda Pública: ${ultimo['deuda_publica']:,.0f}
  - Ratio Deuda/PIB: {ultimo['ratio_deuda_pib']*100:.1f}%

POLÍTICA FISCAL: {ultimo['politica_fiscal'].upper()}
"""
        return reporte