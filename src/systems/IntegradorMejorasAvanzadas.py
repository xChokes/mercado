"""
Integrador de Mejoras Avanzadas v3.1
====================================

Sistema centralizado que integra todas las mejoras desarrolladas:
1. Productividad Laboral Mejorada
2. Sistema de Diversificación Empresarial  
3. Mercado Laboral con Programas Masivos
4. Estabilización Económica
5. Validación Económica Avanzada
"""

import logging
from typing import Dict, List, Any, Optional
import sys
import os

class IntegradorMejorasAvanzadas:
    """Integra y coordina todas las mejoras del sistema económico"""
    
    def __init__(self, mercado, config: Dict):
        self.mercado = mercado
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Sistemas de mejoras
        self.estabilizador_economico = None
        self.gestor_diversificacion = None
        self.enhanced_labor_market = None
        self.validador_economico = None
        
        # Estado de mejoras
        self.mejoras_activas = {
            'productividad_mejorada': False,
            'diversificacion_empresarial': False,
            'mercado_laboral_avanzado': False,
            'estabilizacion_economica': False,
            'validacion_avanzada': False
        }
        
    def inicializar_mejoras(self):
        """Inicializa todos los sistemas de mejoras"""
        try:
            self.logger.info("🚀 Inicializando sistemas de mejoras avanzadas v3.1...")
            
            # 1. Inicializar Estabilizador Económico
            if self.config.get('estabilizacion_economica', {}).get('activar', False):
                self._inicializar_estabilizador_economico()
            
            # 2. Inicializar Diversificación Empresarial
            if self.config.get('diversificacion_empresarial', {}).get('activar', False):
                self._inicializar_diversificacion_empresarial()
            
            # 3. Mejorar Mercado Laboral
            if self.config.get('mercado_laboral', {}).get('activar_programas_masivos', False):
                self._mejorar_mercado_laboral()
            
            # 4. Activar Validación Económica Avanzada
            if self.config.get('validacion_economica', {}).get('validacion_estricta', False):
                self._inicializar_validacion_avanzada()
            
            # 5. Integrar mejoras en el mercado principal
            self._integrar_con_mercado()
            
            self.logger.info(f"✅ Mejoras inicializadas: {sum(self.mejoras_activas.values())}/5")
            
        except Exception as e:
            self.logger.error(f"Error inicializando mejoras: {e}")
    
    def _inicializar_estabilizador_economico(self):
        """Inicializa sistema de estabilización económica"""
        try:
            # Importar sistema de estabilización
            from .EstabilizadorEconomicoAvanzado import EstabilizadorEconomicoAvanzado
            
            self.estabilizador_economico = EstabilizadorEconomicoAvanzado(self.mercado)
            
            # Configurar parámetros
            config_estab = self.config.get('estabilizacion_economica', {})
            self.estabilizador_economico.volatilidad_maxima_pib = config_estab.get('volatilidad_maxima_pib', 0.20)
            self.estabilizador_economico.banda_estabilidad = config_estab.get('banda_estabilidad', 0.12)
            self.estabilizador_economico.crecimiento_objetivo_anual = config_estab.get('crecimiento_objetivo', 0.035)
            
            self.mejoras_activas['estabilizacion_economica'] = True
            self.logger.info("📊 Sistema de Estabilización Económica activado")
            
        except ImportError:
            self.logger.warning("⚠️  Sistema de Estabilización no disponible")
        except Exception as e:
            self.logger.error(f"Error inicializando estabilizador: {e}")
    
    def _inicializar_diversificacion_empresarial(self):
        """Inicializa sistema de diversificación empresarial"""
        try:
            # Importar sistema de diversificación
            from .GestorDiversificacionEmpresarial import GestorDiversificacionEmpresarial
            
            self.gestor_diversificacion = GestorDiversificacionEmpresarial(self.mercado)
            
            # Configurar parámetros
            config_div = self.config.get('diversificacion_empresarial', {})
            self.gestor_diversificacion.min_empresas_objetivo = config_div.get('min_empresas_objetivo', 4)
            self.gestor_diversificacion.max_empresas_objetivo = config_div.get('max_empresas_objetivo', 8)
            self.gestor_diversificacion.concentracion_maxima = config_div.get('concentracion_maxima', 0.55)
            
            self.mejoras_activas['diversificacion_empresarial'] = True
            self.logger.info("🏢 Sistema de Diversificación Empresarial activado")
            
        except ImportError:
            self.logger.warning("⚠️  Sistema de Diversificación no disponible")
        except Exception as e:
            self.logger.error(f"Error inicializando diversificación: {e}")
    
    def _mejorar_mercado_laboral(self):
        """Mejora el sistema de mercado laboral existente"""
        try:
            # Verificar si ya existe enhanced labor market
            if hasattr(self.mercado, 'enhanced_labor_market'):
                labor_market = self.mercado.enhanced_labor_market
                
                # Mejorar configuraciones existentes
                config_laboral = self.config.get('mercado_laboral', {})
                
                # Activar programas masivos
                if hasattr(labor_market, 'execute_mass_hiring_program'):
                    labor_market.umbral_desempleo_critico = config_laboral.get('umbral_desempleo_critico', 0.12)
                    self.mejoras_activas['mercado_laboral_avanzado'] = True
                    self.logger.info("👔 Mercado Laboral con Programas Masivos activado")
                else:
                    # Si no tiene los métodos nuevos, agregar funcionalidades
                    self._agregar_funcionalidades_laborales(labor_market)
                    
            else:
                self.logger.warning("⚠️  Enhanced Labor Market no encontrado")
                
        except Exception as e:
            self.logger.error(f"Error mejorando mercado laboral: {e}")
    
    def _agregar_funcionalidades_laborales(self, labor_market):
        """Agrega funcionalidades laborales mejoradas al mercado existente"""
        def execute_mass_hiring_program():
            """Programa de contratación masiva mejorado"""
            unemployment_rate = labor_market.calculate_unemployment_rate()
            
            if unemployment_rate > 0.12:  # 12% desempleo crítico
                unemployed = [c for c in self.mercado.getConsumidores() if not getattr(c, 'empleado', False)]
                target_hirings = max(5, int(len(unemployed) * 0.20))  # 20% de desempleados
                
                # Crear vacantes de emergencia
                companies_available = [c for c in self.mercado.getEmpresas() 
                                     if hasattr(c, 'dinero') and c.dinero > 40000]
                
                for company in companies_available[:target_hirings//2]:
                    # Subsidiar contratación
                    subsidy = random.uniform(20000, 40000)
                    company.dinero += subsidy
                    company.hiring_subsidy = getattr(company, 'hiring_subsidy', 0) + subsidy
        
        # Agregar método al objeto
        import types
        labor_market.execute_mass_hiring_program = types.MethodType(execute_mass_hiring_program, labor_market)
        self.mejoras_activas['mercado_laboral_avanzado'] = True
    
    def _inicializar_validacion_avanzada(self):
        """Inicializa sistema de validación económica avanzada"""
        try:
            # Verificar si ya existe validador
            if hasattr(self.mercado, 'validador_economico'):
                self.validador_economico = self.mercado.validador_economico
            else:
                # Crear nuevo validador si no existe
                from .ValidadorEconomico import ValidadorEconomico
                self.validador_economico = ValidadorEconomico(self.mercado)
                self.mercado.validador_economico = self.validador_economico
            
            # Configurar rangos personalizados
            config_val = self.config.get('validacion_economica', {})
            if hasattr(self.validador_economico, '_definir_rangos_normales'):
                # Actualizar rangos de productividad
                rangos_prod = config_val.get('rangos_productividad_laboral', [0.8, 1.2])
                # Nota: El validador ya tiene la mejora de productividad aplicada
                
            self.mejoras_activas['validacion_avanzada'] = True
            self.logger.info("✅ Validación Económica Avanzada activada")
            
        except Exception as e:
            self.logger.error(f"Error inicializando validación: {e}")
    
    def _integrar_con_mercado(self):
        """Integra los sistemas de mejoras con el mercado principal"""
        # Agregar métodos de mejoras al mercado si no existen
        
        # Método de estabilización
        if self.estabilizador_economico and not hasattr(self.mercado, 'aplicar_estabilizacion'):
            import types
            
            def aplicar_estabilizacion_pib(ciclo: int, pib_actual: float, pib_anterior: float = None):
                return self.estabilizador_economico.aplicar_estabilizacion(ciclo, pib_actual, pib_anterior)
            
            self.mercado.aplicar_estabilizacion_pib = types.MethodType(aplicar_estabilizacion_pib, self.mercado)
        
        # Método de diversificación empresarial
        if self.gestor_diversificacion and not hasattr(self.mercado, 'mantener_competencia'):
            import types
            
            def mantener_competencia_empresarial(ciclo: int):
                return self.gestor_diversificacion.evaluar_y_mantener_competencia(ciclo)
            
            self.mercado.mantener_competencia_empresarial = types.MethodType(mantener_competencia_empresarial, self.mercado)
        
        self.mejoras_activas['productividad_mejorada'] = True  # Ya está en ValidadorEconomico
        self.logger.info("🔗 Integración con mercado completada")
    
    def ejecutar_ciclo_mejoras(self, ciclo: int, pib_actual: float, pib_anterior: float = None) -> float:
        """Ejecuta todas las mejoras en cada ciclo"""
        try:
            pib_procesado = pib_actual
            
            # 1. Aplicar estabilización económica
            if self.mejoras_activas['estabilizacion_economica'] and self.estabilizador_economico:
                pib_procesado = self.estabilizador_economico.aplicar_estabilizacion(ciclo, pib_procesado, pib_anterior)
                
                # Aplicar políticas macroeconómicas
                if ciclo % 5 == 0:  # Cada 5 ciclos
                    self.estabilizador_economico.aplicar_politicas_macroeconomicas(ciclo)
            
            # 2. Mantener diversificación empresarial
            if self.mejoras_activas['diversificacion_empresarial'] and self.gestor_diversificacion:
                if ciclo % 3 == 0:  # Cada 3 ciclos
                    self.gestor_diversificacion.evaluar_y_mantener_competencia(ciclo)
            
            # 3. Ejecutar programas laborales masivos
            if self.mejoras_activas['mercado_laboral_avanzado']:
                if hasattr(self.mercado, 'enhanced_labor_market'):
                    labor_market = self.mercado.enhanced_labor_market
                    if hasattr(labor_market, 'execute_mass_hiring_program'):
                        unemployment_rate = labor_market.calculate_unemployment_rate()
                        if unemployment_rate > 0.10:  # 10% umbral
                            labor_market.execute_mass_hiring_program()
                            if hasattr(labor_market, 'improve_matching_efficiency'):
                                labor_market.improve_matching_efficiency()
            
            # 4. Validación económica avanzada (cada ciclo)
            if self.mejoras_activas['validacion_avanzada'] and self.validador_economico:
                alertas = self.validador_economico.validar_sistema_completo(ciclo)
                if alertas and len(alertas) > 3:  # Muchas alertas = aplicar medidas correctivas
                    self._aplicar_medidas_correctivas(ciclo, alertas)
            
            return pib_procesado
            
        except Exception as e:
            self.logger.error(f"Error ejecutando ciclo de mejoras: {e}")
            return pib_actual
    
    def _aplicar_medidas_correctivas(self, ciclo: int, alertas: List):
        """Aplica medidas correctivas basadas en alertas del validador"""
        try:
            # Contar tipos de alertas
            alertas_criticas = [a for a in alertas if hasattr(a, 'tipo') and a.tipo.name == 'CRITICA']
            
            if len(alertas_criticas) > 2:
                self.logger.warning(f"🚨 Aplicando medidas correctivas por {len(alertas_criticas)} alertas críticas")
                
                # Medida 1: Estímulo económico de emergencia
                if self.estabilizador_economico:
                    self.estabilizador_economico.fondo_estabilizacion += 50000  # Inyección de emergencia
                
                # Medida 2: Crear empresas adicionales si hay muy pocas
                empresas_activas = len([e for e in self.mercado.getEmpresas() if not getattr(e, 'en_quiebra', False)])
                if empresas_activas <= 2 and self.gestor_diversificacion:
                    self.gestor_diversificacion._crear_empresa_competidora(ciclo, "emergencia")
                
                # Medida 3: Subsidios laborales masivos
                if hasattr(self.mercado, 'enhanced_labor_market'):
                    labor_market = self.mercado.enhanced_labor_market
                    if hasattr(labor_market, '_subsidize_mass_hiring'):
                        labor_market._subsidize_mass_hiring()
                
        except Exception as e:
            self.logger.error(f"Error aplicando medidas correctivas: {e}")
    
    def obtener_estadisticas_mejoras(self) -> Dict[str, Any]:
        """Retorna estadísticas de todas las mejoras aplicadas"""
        stats = {
            'mejoras_activas': self.mejoras_activas.copy(),
            'total_mejoras_activas': sum(self.mejoras_activas.values())
        }
        
        # Estadísticas específicas de cada sistema
        if self.estabilizador_economico:
            stats['estabilizacion'] = self.estabilizador_economico.obtener_estadisticas()
        
        if self.gestor_diversificacion:
            stats['diversificacion'] = self.gestor_diversificacion.obtener_estadisticas()
        
        if self.validador_economico:
            stats['alertas_activas'] = len(getattr(self.validador_economico, 'alertas_activas', []))
        
        return stats
    
    def generar_reporte_mejoras(self, ciclo: int) -> str:
        """Genera reporte textual del estado de las mejoras"""
        stats = self.obtener_estadisticas_mejoras()
        
        reporte = f"\n🔧 REPORTE DE MEJORAS AVANZADAS - CICLO {ciclo}\n"
        reporte += "=" * 60 + "\n"
        
        reporte += f"✅ Mejoras Activas: {stats['total_mejoras_activas']}/5\n"
        
        for mejora, activa in self.mejoras_activas.items():
            emoji = "✅" if activa else "❌"
            reporte += f"   {emoji} {mejora.replace('_', ' ').title()}\n"
        
        # Estadísticas específicas
        if 'estabilizacion' in stats:
            est = stats['estabilizacion']
            reporte += f"\n📊 Estabilización Económica:\n"
            reporte += f"   Intervenciones: {est.get('intervenciones_realizadas', 0)}\n"
            reporte += f"   Ciclos Estables: {est.get('ciclos_estables', 0)}\n"
            reporte += f"   Volatilidad Promedio: {est.get('volatilidad_promedio', 0):.2%}\n"
            reporte += f"   Sistema Estable: {'SÍ' if est.get('sistema_estable', False) else 'NO'}\n"
        
        if 'diversificacion' in stats:
            div = stats['diversificacion']
            reporte += f"\n🏢 Diversificación Empresarial:\n"
            reporte += f"   Empresas Activas: {div.get('empresas_activas', 0)}\n"
            reporte += f"   Empresas Creadas: {div.get('empresas_creadas_total', 0)}\n"
            reporte += f"   Split-ups: {div.get('split_ups_realizados', 0)}\n"
            reporte += f"   Mercado Competitivo: {'SÍ' if div.get('mercado_competitivo', False) else 'NO'}\n"
        
        reporte += "\n" + "=" * 60
        
        return reporte


def crear_integrador_mejoras(mercado, config) -> IntegradorMejorasAvanzadas:
    """Factory function para crear el integrador de mejoras"""
    integrador = IntegradorMejorasAvanzadas(mercado, config)
    integrador.inicializar_mejoras()
    return integrador
