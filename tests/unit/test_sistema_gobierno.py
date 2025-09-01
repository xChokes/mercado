"""
Tests para el sistema de gobierno con enfoque en política fiscal y PIB
"""

import unittest
import sys
import os

# Agregar el directorio raíz del proyecto al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.models.Mercado import Mercado
from src.systems.government import Government, TipoPoliticaFiscal, ComponentePIB
from src.models.Consumidor import Consumidor
from src.models.Empresa import Empresa


class TestSistemaGobierno(unittest.TestCase):
    """Tests del sistema gubernamental y su impacto fiscal"""
    
    def setUp(self):
        """Configuración inicial para tests"""
        # Crear mercado simple para testing
        self.bienes = ['alimentos', 'ropa', 'tecnologia']
        self.mercado = Mercado(self.bienes)
        
        # Agregar algunos agentes para testing
        for i in range(10):
            consumidor = Consumidor(f"TestConsumidor{i}", self.mercado)
            consumidor.dinero = 5000 + i * 1000  # Ingresos variables
            consumidor.ingreso_mensual = 3000 + i * 500
            self.mercado.agregar_persona(consumidor)
        
        for i in range(3):
            empresa = Empresa(f"TestEmpresa{i}", self.mercado, self.bienes)
            empresa.dinero = 50000 + i * 10000
            self.mercado.agregar_persona(empresa)
    
    def test_inicializacion_government(self):
        """Test de inicialización del sistema government"""
        gov = Government(self.mercado)
        
        # Verificar inicialización correcta
        self.assertIsInstance(gov.politica_fiscal, TipoPoliticaFiscal)
        self.assertEqual(gov.politica_fiscal, TipoPoliticaFiscal.NEUTRAL)
        self.assertEqual(gov.presupuesto_disponible, 1000000)
        self.assertEqual(gov.deuda_publica, 0)
        
        # Verificar componentes PIB inicializados
        self.assertEqual(len(gov.componentes_pib), 4)
        self.assertTrue(ComponentePIB.CONSUMO in gov.componentes_pib)
        self.assertTrue(ComponentePIB.INVERSION in gov.componentes_pib)
        self.assertTrue(ComponentePIB.GASTO_GOBIERNO in gov.componentes_pib)
        self.assertTrue(ComponentePIB.EXPORTACIONES_NETAS in gov.componentes_pib)
    
    def test_calculo_pib_componentes(self):
        """Test del cálculo de PIB con componentes C+I+G+(NX)"""
        gov = self.mercado.government
        
        # Simular algunas transacciones
        self.mercado.transacciones_ciclo_actual = [
            {'costo_total': 1000},
            {'costo_total': 2000},
            {'costo_total': 1500}
        ]
        
        # Ejecutar ciclo fiscal
        resultado = gov.ejecutar_ciclo_fiscal(1)
        
        # Verificar que el PIB se calculó correctamente
        self.assertGreater(resultado['pib_total'], 0)
        self.assertGreater(resultado['componentes_pib'][ComponentePIB.CONSUMO], 0)
        self.assertGreater(resultado['componentes_pib'][ComponentePIB.INVERSION], 0)
        
        # Verificar que la suma de componentes es consistente
        suma_componentes = (
            resultado['componentes_pib'][ComponentePIB.CONSUMO] +
            resultado['componentes_pib'][ComponentePIB.INVERSION] +
            resultado['componentes_pib'][ComponentePIB.GASTO_GOBIERNO] +
            resultado['componentes_pib'][ComponentePIB.EXPORTACIONES_NETAS]
        )
        self.assertEqual(suma_componentes, resultado['pib_total'])
    
    def test_recaudacion_impuestos(self):
        """Test de recaudación de impuestos"""
        gov = self.mercado.government
        presupuesto_inicial = gov.presupuesto_disponible
        
        # Ejecutar ciclo fiscal
        resultado = gov.ejecutar_ciclo_fiscal(1)
        
        # Verificar que hubo recaudación
        self.assertGreater(resultado['recaudacion'], 0)
        self.assertGreater(gov.presupuesto_disponible, presupuesto_inicial)
        
        # Verificar que los agentes pagaron impuestos
        total_dinero_inicial = sum(c.dinero for c in self.mercado.getConsumidores()) + \
                              sum(e.dinero for e in self.mercado.getEmpresas())
        
        # Ejecutar otro ciclo
        gov.ejecutar_ciclo_fiscal(2)
        
        total_dinero_final = sum(c.dinero for c in self.mercado.getConsumidores()) + \
                            sum(e.dinero for e in self.mercado.getEmpresas())
        
        # El dinero total debería haber disminuido debido a impuestos
        self.assertLess(total_dinero_final, total_dinero_inicial)
    
    def test_gasto_publico(self):
        """Test de ejecución de gasto público"""
        gov = self.mercado.government
        
        # Asegurar presupuesto suficiente
        gov.presupuesto_disponible = 100000
        
        # Ejecutar ciclo fiscal
        resultado = gov.ejecutar_ciclo_fiscal(1)
        
        # Verificar que hubo gasto público
        self.assertGreater(resultado['gasto_publico'], 0)
        self.assertGreater(resultado['componentes_pib'][ComponentePIB.GASTO_GOBIERNO], 0)
        
        # Verificar que el gasto benefició a los agentes
        # (el dinero del gasto debería haber regresado a empresas y consumidores)
        dinero_empresas = sum(e.dinero for e in self.mercado.getEmpresas())
        dinero_consumidores = sum(c.dinero for c in self.mercado.getConsumidores())
        
        self.assertGreater(dinero_empresas + dinero_consumidores, 0)
    
    def test_balance_fiscal_y_deuda(self):
        """Test de cálculo de balance fiscal y deuda pública"""
        gov = self.mercado.government
        
        # Ejecutar varios ciclos fiscales
        balances = []
        for i in range(5):
            resultado = gov.ejecutar_ciclo_fiscal(i + 1)
            balances.append(resultado['balance_fiscal'])
        
        # Verificar que se registra el balance fiscal
        self.assertEqual(len(balances), 5)
        
        # Verificar que la deuda se actualiza correctamente
        if any(balance < 0 for balance in balances):
            # Si hubo déficit, debería haber deuda
            self.assertGreater(gov.deuda_publica, 0)
        
        # Verificar ratio deuda/PIB
        ratio_deuda = gov.obtener_deuda_pib_ratio()
        self.assertGreaterEqual(ratio_deuda, 0)
        self.assertIsInstance(ratio_deuda, (int, float))
    
    def test_politica_fiscal_adaptativa(self):
        """Test de cambio automático de política fiscal"""
        gov = self.mercado.government
        
        # Simular alta deuda para forzar política contractiva
        gov.deuda_publica = 2000000  # Deuda alta
        
        # Ejecutar ciclo fiscal
        resultado = gov.ejecutar_ciclo_fiscal(1)
        
        # La política debería cambiar a contractiva con deuda alta
        # (esto depende del PIB, pero con deuda alta debería tender a contractiva)
        if resultado['pib_total'] > 0:
            ratio_deuda = gov.deuda_publica / resultado['pib_total']
            if ratio_deuda > 0.9:
                self.assertEqual(gov.politica_fiscal, TipoPoliticaFiscal.CONTRACTIVA)
    
    def test_estabilidad_fiscal_baseline(self):
        """Test de estabilidad en escenario baseline"""
        gov = self.mercado.government
        
        # Ejecutar 10 ciclos en condiciones normales
        resultados = []
        for i in range(10):
            resultado = gov.ejecutar_ciclo_fiscal(i + 1)
            resultados.append(resultado)
        
        # Verificar estabilidad de los principales indicadores
        pibs = [r['pib_total'] for r in resultados]
        balances = [r['balance_fiscal'] for r in resultados]
        
        # PIB no debería variar dramáticamente
        pib_promedio = sum(pibs) / len(pibs)
        for pib in pibs:
            variacion = abs(pib - pib_promedio) / pib_promedio
            self.assertLess(variacion, 0.5, "PIB varía demasiado en escenario baseline")
        
        # Verificar que el sistema es estable
        self.assertTrue(all(r['pib_total'] > 0 for r in resultados))
        self.assertTrue(all(r['recaudacion'] > 0 for r in resultados))
        
        # Deuda no debería crecer descontroladamente
        ratio_deuda_final = gov.obtener_deuda_pib_ratio()
        self.assertLess(ratio_deuda_final, 2.0, "Ratio deuda/PIB excesivo en baseline")
    
    def test_integracion_mercado_government(self):
        """Test de integración entre Mercado y Government"""
        # Verificar que el mercado tiene el sistema government
        self.assertTrue(hasattr(self.mercado, 'government'))
        self.assertIsInstance(self.mercado.government, Government)
        
        # Ejecutar estadísticas del mercado (debería usar government)
        self.mercado.registrar_estadisticas()
        
        # Verificar que se generaron estadísticas fiscales
        stats_fiscales = self.mercado.obtener_estadisticas_fiscales()
        self.assertIsInstance(stats_fiscales, dict)
        
        # Verificar componentes del PIB
        pib_descompuesto = self.mercado.obtener_pib_descompuesto()
        self.assertIsInstance(pib_descompuesto, dict)
        
        # Verificar que el PIB histórico se registró
        self.assertGreater(len(self.mercado.pib_historico), 0)
    
    def test_reporte_fiscal_completo(self):
        """Test de generación de reporte fiscal"""
        gov = self.mercado.government
        
        # Ejecutar algunos ciclos
        for i in range(3):
            gov.ejecutar_ciclo_fiscal(i + 1)
        
        # Generar reporte
        reporte = gov.generar_reporte_fiscal()
        
        # Verificar que el reporte contiene información clave
        self.assertIsInstance(reporte, str)
        self.assertIn("PIB Total", reporte)
        self.assertIn("Consumo (C)", reporte)
        self.assertIn("Inversión (I)", reporte)
        self.assertIn("Gasto Gobierno (G)", reporte)
        self.assertIn("BALANCE FISCAL", reporte)
        self.assertIn("POLÍTICA FISCAL", reporte)


if __name__ == '__main__':
    unittest.main()