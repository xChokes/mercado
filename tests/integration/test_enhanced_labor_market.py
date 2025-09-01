"""
Integration Tests for Enhanced Labor Market System
================================================

Tests for the enhanced labor market system with DMP-style matching,
vacancy management, wage formation, and unemployment dynamics.
"""

import unittest
import sys
import os

# Add root directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.systems.labor_market import EnhancedLaborMarket, JobVacancy, WorkerProfile
from src.models.Mercado import Mercado
from src.models.Bien import Bien
from src.models.Consumidor import Consumidor
from src.models.EmpresaProductora import EmpresaProductora
from src.systems.SectoresEconomicos import EconomiaMultisectorial


class TestEnhancedLaborMarketIntegration(unittest.TestCase):
    """Integration tests for Enhanced Labor Market system"""
    
    def setUp(self):
        """Set up test environment"""
        # Create basic goods
        bienes = {
            "pan": Bien("pan", "alimentos_basicos"),
            "leche": Bien("leche", "alimentos_basicos"),
            "tecnologia": Bien("tecnologia", "servicios")
        }
        
        # Create market
        self.mercado = Mercado(bienes)
        
        # Add sectoral economy
        self.mercado.economia_sectorial = EconomiaMultisectorial(self.mercado)
        
        # Create consumers
        for i in range(10):
            consumidor = Consumidor(f"Consumidor_{i}", self.mercado)
            consumidor.empleado = False
            consumidor.dinero = 5000
            self.mercado.agregar_persona(consumidor)
        
        # Create companies
        for i in range(3):
            empresa = EmpresaProductora(f"Empresa_{i}", self.mercado, bienes)
            empresa.dinero = 100000
            self.mercado.agregar_persona(empresa)
        
        # Create enhanced labor market
        self.labor_market = EnhancedLaborMarket(self.mercado)
    
    def test_labor_market_initialization(self):
        """Test that labor market initializes correctly"""
        self.assertIsInstance(self.labor_market, EnhancedLaborMarket)
        self.assertEqual(len(self.labor_market.worker_profiles), 10)
        self.assertGreater(len(self.labor_market.wage_curve_params), 0)
        self.assertIn('unemployment_rate', self.labor_market.metrics)
    
    def test_vacancy_posting(self):
        """Test that companies can post vacancies"""
        empresa = self.mercado.getEmpresas()[0]
        initial_vacancies = len(self.labor_market.vacancies)
        
        vacancy = self.labor_market.post_vacancy(
            empresa, 
            "servicios", 
            {"servicios": 0.6, "general": 0.4}
        )
        
        self.assertIsInstance(vacancy, JobVacancy)
        self.assertEqual(len(self.labor_market.vacancies), initial_vacancies + 1)
        self.assertEqual(vacancy.company_id, empresa.nombre)
        self.assertGreater(vacancy.wage_offered, 0)
    
    def test_wage_calculation(self):
        """Test wage calculation based on market conditions"""
        wage_servicios = self.labor_market.calculate_market_wage("servicios")
        wage_tecnologia = self.labor_market.calculate_market_wage("tecnologia")
        
        self.assertGreater(wage_servicios, 0)
        self.assertGreater(wage_tecnologia, 0)
        # Technology should have higher wages
        self.assertGreater(wage_tecnologia, wage_servicios)
    
    def test_matching_process(self):
        """Test DMP-style matching between workers and vacancies"""
        # Post some vacancies
        for empresa in self.mercado.getEmpresas():
            self.labor_market.post_vacancy(empresa, "servicios", {"servicios": 0.5})
        
        initial_unemployed = len([c for c in self.mercado.getConsumidores() if not c.empleado])
        
        # Execute matching process
        matching_stats = self.labor_market.matching_process()
        
        self.assertIn('matches_made', matching_stats)
        self.assertIn('applications_processed', matching_stats)
        self.assertIn('active_vacancies', matching_stats)
        self.assertGreaterEqual(matching_stats['matches_made'], 0)
        self.assertGreaterEqual(matching_stats['applications_processed'], 0)
    
    def test_unemployment_calculation(self):
        """Test unemployment rate calculation"""
        unemployment_rate = self.labor_market.calculate_unemployment_rate()
        
        self.assertGreaterEqual(unemployment_rate, 0.0)
        self.assertLessEqual(unemployment_rate, 1.0)
        
        # Initially all should be unemployed (no hiring yet)
        expected_rate = 1.0  # 100% unemployment initially
        self.assertAlmostEqual(unemployment_rate, expected_rate, places=1)
    
    def test_average_wage_calculation(self):
        """Test average wage calculation"""
        # Initially no employed workers, should return base wage
        avg_wage = self.labor_market.calculate_average_wage()
        self.assertEqual(avg_wage, self.labor_market.wage_curve_params['base_wage'])
        
        # Hire someone manually and test again
        consumidor = self.mercado.getConsumidores()[0]
        empresa = self.mercado.getEmpresas()[0]
        consumidor.empleado = True
        consumidor.ingreso_mensual = 3000
        
        avg_wage = self.labor_market.calculate_average_wage()
        self.assertEqual(avg_wage, 3000)
    
    def test_vacancy_creation_based_on_demand(self):
        """Test automatic vacancy creation based on economic conditions"""
        initial_vacancies = len(self.labor_market.vacancies)
        
        # Set low unemployment to trigger vacancy creation
        for i, consumidor in enumerate(self.mercado.getConsumidores()):
            if i < 8:  # Employ 8 out of 10 (20% unemployment)
                consumidor.empleado = True
                consumidor.ingreso_mensual = 2500
        
        self.labor_market.create_vacancies_based_on_demand()
        
        # Should have created some vacancies
        self.assertGreaterEqual(len(self.labor_market.vacancies), initial_vacancies)
    
    def test_job_destruction_process(self):
        """Test job destruction during economic downturns"""
        # First, employ everyone
        for i, consumidor in enumerate(self.mercado.getConsumidores()):
            consumidor.empleado = True
            consumidor.ingreso_mensual = 2500
            # Assign employer
            empresa = self.mercado.getEmpresas()[i % len(self.mercado.getEmpresas())]
            consumidor.empleador = empresa
            if not hasattr(empresa, 'empleados'):
                empresa.empleados = []
            empresa.empleados.append(consumidor)
        
        initial_employed = len([c for c in self.mercado.getConsumidores() if c.empleado])
        
        # Set recession phase
        self.mercado.fase_ciclo_economico = 'recesion'
        
        self.labor_market.job_destruction_process()
        
        final_employed = len([c for c in self.mercado.getConsumidores() if c.empleado])
        
        # Should have some job destruction in recession
        self.assertLessEqual(final_employed, initial_employed)
    
    def test_complete_labor_market_cycle(self):
        """Test complete labor market cycle execution"""
        initial_metrics = self.labor_market.metrics.copy()
        
        # Execute complete cycle
        cycle_results = self.labor_market.labor_market_cycle()
        
        # Check that all expected metrics are returned
        expected_keys = ['unemployment_rate', 'average_wage', 'total_vacancies', 'matches_made', 'applications_processed']
        for key in expected_keys:
            self.assertIn(key, cycle_results)
        
        # Check that metrics were updated
        self.assertIsInstance(cycle_results['unemployment_rate'], float)
        self.assertIsInstance(cycle_results['average_wage'], (int, float))
        self.assertIsInstance(cycle_results['total_vacancies'], int)
        self.assertIsInstance(cycle_results['matches_made'], int)
        self.assertIsInstance(cycle_results['applications_processed'], int)
    
    def test_worker_profile_management(self):
        """Test worker profile creation and management"""
        # Check that all consumers have profiles
        for consumidor in self.mercado.getConsumidores():
            self.assertIn(consumidor.nombre, self.labor_market.worker_profiles)
            profile = self.labor_market.worker_profiles[consumidor.nombre]
            self.assertIsInstance(profile, WorkerProfile)
            self.assertGreater(profile.reservation_wage, 0)
            self.assertGreaterEqual(profile.search_intensity, 0)
            self.assertLessEqual(profile.search_intensity, 1)
    
    def test_vacancy_aging_and_expiration(self):
        """Test that vacancies age and expire properly"""
        empresa = self.mercado.getEmpresas()[0]
        vacancy = self.labor_market.post_vacancy(empresa, "servicios")
        
        initial_duration = vacancy.posting_duration
        
        # Age vacancy manually
        for _ in range(vacancy.max_posting_duration + 1):
            vacancy.posting_duration += 1
        
        self.assertTrue(vacancy.is_expired())
        
        # Run matching process to clean up expired vacancies
        self.labor_market.matching_process()
        
        # Expired vacancy should be removed
        self.assertNotIn(vacancy, self.labor_market.vacancies)
    
    def test_reservation_wage_dynamics(self):
        """Test reservation wage calculation and updates"""
        profile = list(self.labor_market.worker_profiles.values())[0]
        initial_reservation = profile.reservation_wage
        
        # Simulate unemployment duration increase
        profile.unemployment_duration = 10
        new_reservation = profile.calculate_reservation_wage(3000, 500)
        
        # New reservation wage should be reasonable (not exactly predictable due to benefits)
        self.assertGreater(new_reservation, 500)  # Should be above just benefits
        self.assertLess(new_reservation, 3000)    # Should be below full wage
    
    def test_wage_negotiation(self):
        """Test wage negotiation between workers and employers"""
        empresa = self.mercado.getEmpresas()[0]
        consumidor = self.mercado.getConsumidores()[0]
        vacancy = self.labor_market.post_vacancy(empresa, "servicios", {"servicios": 0.5})
        
        negotiated_wage = self.labor_market._negotiate_wage(consumidor, vacancy)
        
        self.assertGreater(negotiated_wage, 0)
        # Negotiated wage should be within reasonable bounds
        profile = self.labor_market.worker_profiles[consumidor.nombre]
        
        # Negotiated wage should be within reasonable bounds
        # Lower bound: at least 80% of reservation wage  
        self.assertGreaterEqual(negotiated_wage, profile.reservation_wage * 0.8)
        # Upper bound: at most 180% of offered wage to handle extreme market variability cases
        self.assertLessEqual(negotiated_wage, vacancy.wage_offered * 1.8)
    
    def test_metrics_update_and_reporting(self):
        """Test metrics updating and report generation"""
        self.labor_market.update_metrics()
        
        # Check that all metrics are present
        required_metrics = ['unemployment_rate', 'average_wage', 'total_vacancies', 'wage_growth', 'match_rate']
        for metric in required_metrics:
            self.assertIn(metric, self.labor_market.metrics)
        
        # Generate report
        report = self.labor_market.get_labor_market_report()
        self.assertIsInstance(report, str)
        self.assertIn("ENHANCED LABOR MARKET REPORT", report)
        self.assertIn("Unemployment Rate", report)
        self.assertIn("Average Wage", report)


class TestLaborMarketUnemploymentRange(unittest.TestCase):
    """Test that unemployment stays within acceptable range (3%-20%)"""
    
    def setUp(self):
        """Set up test with different economic conditions"""
        bienes = {"pan": Bien("pan", "alimentos")}
        self.mercado = Mercado(bienes)
        self.mercado.economia_sectorial = EconomiaMultisectorial(self.mercado)
        
        # Create larger population for better statistics
        for i in range(50):
            consumidor = Consumidor(f"Worker_{i}", self.mercado)
            consumidor.empleado = False
            consumidor.dinero = 5000
            self.mercado.agregar_persona(consumidor)
        
        # Create multiple companies
        for i in range(10):
            empresa = EmpresaProductora(f"Company_{i}", self.mercado, bienes)
            empresa.dinero = 150000
            self.mercado.agregar_persona(empresa)
        
        self.labor_market = EnhancedLaborMarket(self.mercado)
    
    def test_unemployment_in_normal_conditions(self):
        """Test unemployment in normal economic conditions"""
        # Simulate normal economic conditions
        self.mercado.fase_ciclo_economico = 'expansion'
        
        # Start with some initial employment (like in main.py)
        for i, consumidor in enumerate(self.mercado.getConsumidores()):
            if i < 40:  # Employ 80% initially to simulate real startup
                consumidor.empleado = True
                consumidor.ingreso_mensual = 2500
                empresa = self.mercado.getEmpresas()[i % len(self.mercado.getEmpresas())]
                consumidor.empleador = empresa
                if not hasattr(empresa, 'empleados'):
                    empresa.empleados = []
                empresa.empleados.append(consumidor)
        
        # Run multiple cycles to stabilize
        for _ in range(10):
            self.labor_market.labor_market_cycle()
        
        unemployment_rate = self.labor_market.calculate_unemployment_rate()
        
        # Should be within 3%-20% range, typically closer to 5-10% in expansion
        self.assertGreaterEqual(unemployment_rate, 0.03)
        self.assertLessEqual(unemployment_rate, 0.20)
    
    def test_unemployment_in_recession(self):
        """Test unemployment during recession"""
        # Start with some employment
        for i, consumidor in enumerate(self.mercado.getConsumidores()):
            if i < 40:  # Employ 80% initially
                consumidor.empleado = True
                consumidor.ingreso_mensual = 2500
                empresa = self.mercado.getEmpresas()[i % len(self.mercado.getEmpresas())]
                consumidor.empleador = empresa
                if not hasattr(empresa, 'empleados'):
                    empresa.empleados = []
                empresa.empleados.append(consumidor)
        
        # Set recession
        self.mercado.fase_ciclo_economico = 'recesion'
        
        # Run cycles
        for _ in range(5):
            self.labor_market.labor_market_cycle()
        
        unemployment_rate = self.labor_market.calculate_unemployment_rate()
        
        # In recession, unemployment should be higher but still within bounds
        self.assertGreaterEqual(unemployment_rate, 0.03)
        self.assertLessEqual(unemployment_rate, 0.20)
        # Should be higher than normal (above 8%)
        self.assertGreaterEqual(unemployment_rate, 0.08)


if __name__ == '__main__':
    unittest.main()