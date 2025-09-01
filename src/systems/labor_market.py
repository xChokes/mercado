"""
Enhanced Labor Market System with DMP-style Matching and Wage Formation
======================================================================

This module implements an enhanced labor market system with:
- Diamond-Mortensen-Pissarides (DMP) style job matching
- Vacancy posting and search frictions
- Salary formation with reservation wages and wage curves
- Advanced unemployment dynamics
- Comprehensive labor market metrics

Author: Enhanced Labor Market Team
"""

import random
import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum


class JobMatchingStatus(Enum):
    """Status of job matching process"""
    SEARCHING = "searching"
    MATCHED = "matched"
    REJECTED = "rejected"
    VACANT = "vacant"


@dataclass
class JobVacancy:
    """Represents a job vacancy with DMP-style characteristics"""
    company_id: str
    sector: str
    wage_offered: float
    skill_requirements: Dict[str, float]
    posting_duration: int = 0
    max_posting_duration: int = 10  # Maximum cycles to keep vacancy open
    applications_received: int = 0
    status: JobMatchingStatus = JobMatchingStatus.VACANT
    
    def is_expired(self) -> bool:
        """Check if vacancy has expired"""
        return self.posting_duration >= self.max_posting_duration
    
    def calculate_match_probability(self, worker_skills: Dict[str, float]) -> float:
        """Calculate probability of successful match with worker"""
        if not self.skill_requirements:
            return 0.5  # Base probability if no requirements
        
        total_match = 0.0
        total_weight = 0.0
        
        for skill, required_level in self.skill_requirements.items():
            worker_level = worker_skills.get(skill, 0.0)
            # Match probability based on how well worker meets requirements
            match_score = min(1.0, worker_level / max(0.1, required_level))
            total_match += match_score
            total_weight += 1.0
        
        base_match = total_match / total_weight if total_weight > 0 else 0.5
        
        # Add friction - longer posting duration reduces match probability
        friction_penalty = 0.05 * self.posting_duration
        return max(0.1, base_match - friction_penalty)


@dataclass
class WorkerProfile:
    """Enhanced worker profile for DMP matching"""
    worker_id: str
    skills: Dict[str, float]
    reservation_wage: float
    search_intensity: float = 1.0  # How actively they search (0-1)
    unemployment_duration: int = 0
    preferred_sectors: List[str] = field(default_factory=list)
    
    def calculate_reservation_wage(self, base_wage: float, unemployment_benefits: float = 0.0) -> float:
        """Calculate reservation wage based on unemployment duration and benefits"""
        # Reservation wage decreases with unemployment duration
        duration_factor = max(0.5, 1.0 - 0.02 * self.unemployment_duration)
        benefit_factor = unemployment_benefits / max(1, base_wage)
        
        return base_wage * duration_factor + unemployment_benefits * benefit_factor
    
    def update_search_intensity(self, market_conditions: float) -> None:
        """Update search intensity based on market conditions"""
        # More intense search in worse market conditions
        base_intensity = 0.8 + 0.2 * (1 - market_conditions)
        # Fatigue factor with long unemployment
        fatigue_factor = max(0.3, 1.0 - 0.01 * self.unemployment_duration)
        self.search_intensity = min(1.0, base_intensity * fatigue_factor)


class EnhancedLaborMarket:
    """
    Enhanced Labor Market with DMP-style matching and advanced wage formation
    """
    
    def __init__(self, market):
        self.market = market
        self.vacancies: List[JobVacancy] = []
        self.worker_profiles: Dict[str, WorkerProfile] = {}
        self.wage_curve_params = {
            'base_wage': 2500,
            'unemployment_elasticity': -0.1,  # Wage response to unemployment
            'productivity_factor': 1.0,
            'inflation_adjustment': 0.02
        }
        self.matching_efficiency = 0.6  # Base matching efficiency
        self.search_frictions = 0.15    # Search friction parameter
        
        # Labor market metrics
        self.metrics = {
            'unemployment_rate': 0.0,
            'average_wage': 0.0,
            'total_vacancies': 0,
            'job_creation_rate': 0.0,
            'job_destruction_rate': 0.0,
            'wage_growth': 0.0,
            'match_rate': 0.0
        }
        
        # Initialize worker profiles
        self._initialize_worker_profiles()
    
    def _initialize_worker_profiles(self):
        """Initialize profiles for all workers"""
        for consumer in self.market.getConsumidores():
            skills = getattr(consumer, 'perfil_habilidades', None)
            if skills and hasattr(skills, 'habilidades'):
                skill_dict = skills.habilidades
            else:
                # Create basic skills if none exist
                sectors = getattr(self.market, 'economia_sectorial', None)
                if sectors and hasattr(sectors, 'sectores'):
                    skill_dict = {sector: random.uniform(0.2, 0.8) 
                                for sector in sectors.sectores.keys()}
                else:
                    skill_dict = {'general': random.uniform(0.2, 0.8)}
            
            base_wage = getattr(consumer, 'ingreso_mensual', 0)
            if base_wage <= 0:
                base_wage = self.wage_curve_params['base_wage']
            reservation_wage = base_wage * random.uniform(0.7, 0.9)
            
            self.worker_profiles[consumer.nombre] = WorkerProfile(
                worker_id=consumer.nombre,
                skills=skill_dict,
                reservation_wage=reservation_wage,
                search_intensity=random.uniform(0.6, 1.0)
            )
    
    def post_vacancy(self, company, sector: str, required_skills: Dict[str, float] = None) -> JobVacancy:
        """Post a new job vacancy with DMP characteristics"""
        if required_skills is None:
            required_skills = {'general': 0.5}
        
        # Calculate wage offer based on company characteristics and market conditions
        base_wage = self.calculate_market_wage(sector)
        company_wage_premium = 1.0
        
        if hasattr(company, 'dinero') and company.dinero > 100000:
            company_wage_premium = 1.1  # 10% premium for well-capitalized companies
        
        wage_offered = base_wage * company_wage_premium
        
        vacancy = JobVacancy(
            company_id=company.nombre if hasattr(company, 'nombre') else str(company),
            sector=sector,
            wage_offered=wage_offered,
            skill_requirements=required_skills,
            max_posting_duration=random.randint(8, 15)  # Vary posting duration
        )
        
        self.vacancies.append(vacancy)
        return vacancy
    
    def calculate_market_wage(self, sector: str) -> float:
        """Calculate market wage using wage curve and market conditions"""
        base_wage = self.wage_curve_params['base_wage']
        
        # Wage curve: wages respond negatively to unemployment
        unemployment_rate = self.metrics['unemployment_rate']
        unemployment_effect = (unemployment_rate * self.wage_curve_params['unemployment_elasticity'])
        
        # Productivity and inflation adjustments
        productivity_adjustment = self.wage_curve_params['productivity_factor']
        inflation_adjustment = self.wage_curve_params['inflation_adjustment']
        
        # Sector-specific adjustments
        sector_premium = 1.0
        if 'tecnologia' in sector.lower():
            sector_premium = 1.2
        elif 'servicios' in sector.lower():
            sector_premium = 0.9
        
        market_wage = (base_wage * 
                      (1 + unemployment_effect) * 
                      productivity_adjustment * 
                      (1 + inflation_adjustment) * 
                      sector_premium)
        
        return max(base_wage * 0.5, market_wage)  # Minimum wage floor
    
    def matching_process(self) -> Dict[str, int]:
        """
        Execute DMP-style matching process between workers and vacancies
        Returns: Dictionary with matching statistics
        """
        matches_made = 0
        applications_processed = 0
        
        # Get unemployed workers
        unemployed_workers = [c for c in self.market.getConsumidores() if not getattr(c, 'empleado', False)]
        
        # Update worker profiles
        for worker in unemployed_workers:
            if worker.nombre in self.worker_profiles:
                profile = self.worker_profiles[worker.nombre]
                profile.unemployment_duration += 1
                profile.update_search_intensity(1 - self.metrics['unemployment_rate'])
        
        # Matching algorithm - workers search and apply to vacancies
        for worker in unemployed_workers:
            if worker.nombre not in self.worker_profiles:
                continue
                
            profile = self.worker_profiles[worker.nombre]
            
            # Worker searches with intensity
            search_success = random.random() < profile.search_intensity
            if not search_success:
                continue
            
            # Find suitable vacancies
            suitable_vacancies = []
            for vacancy in self.vacancies:
                if vacancy.status != JobMatchingStatus.VACANT:
                    continue
                
                match_prob = vacancy.calculate_match_probability(profile.skills)
                wage_acceptable = vacancy.wage_offered >= profile.reservation_wage
                
                if match_prob > 0.3 and wage_acceptable:  # Minimum match threshold
                    suitable_vacancies.append((vacancy, match_prob))
            
            if not suitable_vacancies:
                continue
            
            # Sort by match probability and apply to best matches
            suitable_vacancies.sort(key=lambda x: x[1], reverse=True)
            applications_this_worker = min(3, len(suitable_vacancies))  # Max 3 applications
            
            for vacancy, match_prob in suitable_vacancies[:applications_this_worker]:
                applications_processed += 1
                vacancy.applications_received += 1
                
                # Matching success depends on match probability and market frictions
                friction_factor = 1 - self.search_frictions
                final_match_prob = match_prob * friction_factor * self.matching_efficiency
                
                if random.random() < final_match_prob:
                    # Successful match!
                    if self._execute_hiring(worker, vacancy):
                        matches_made += 1
                        vacancy.status = JobMatchingStatus.MATCHED
                        profile.unemployment_duration = 0  # Reset unemployment duration
                        break  # Worker found job, stop searching
        
        # Age and clean up vacancies
        self._age_vacancies()
        
        return {
            'matches_made': matches_made,
            'applications_processed': applications_processed,
            'active_vacancies': len([v for v in self.vacancies if v.status == JobMatchingStatus.VACANT])
        }
    
    def _execute_hiring(self, worker, vacancy: JobVacancy) -> bool:
        """Execute the actual hiring process"""
        # Find the company
        company = None
        for emp in self.market.getEmpresas():
            if (hasattr(emp, 'nombre') and emp.nombre == vacancy.company_id):
                company = emp
                break
        
        if not company or not hasattr(company, 'contratar'):
            return False
        
        # Attempt to hire with negotiated wage
        negotiated_wage = self._negotiate_wage(worker, vacancy)
        
        # Temporarily set worker's expected wage for hiring process
        original_wage = getattr(worker, 'ingreso_mensual', 0)
        worker.ingreso_mensual = negotiated_wage
        
        success = company.contratar(worker)
        
        if success and hasattr(worker, 'ingreso_mensual'):
            # Update worker profile
            if worker.nombre in self.worker_profiles:
                profile = self.worker_profiles[worker.nombre]
                profile.reservation_wage = negotiated_wage * 0.9  # Lower reservation for future
        else:
            # Restore original wage if hiring failed
            worker.ingreso_mensual = original_wage
        
        return success
    
    def _negotiate_wage(self, worker, vacancy: JobVacancy) -> float:
        """Negotiate wage between worker and employer"""
        profile = self.worker_profiles.get(worker.nombre)
        if not profile:
            return vacancy.wage_offered
        
        # Simple Nash bargaining
        worker_power = 0.4  # Worker bargaining power
        employer_power = 1 - worker_power
        
        # Worker's fallback is reservation wage
        worker_fallback = profile.reservation_wage
        
        # Employer's fallback is cost of continued search
        search_cost = vacancy.wage_offered * 0.1 * vacancy.posting_duration
        employer_fallback = vacancy.wage_offered + search_cost
        
        # Nash bargaining solution
        if employer_fallback > worker_fallback:
            surplus = employer_fallback - worker_fallback
            negotiated_wage = worker_fallback + worker_power * surplus
        else:
            negotiated_wage = vacancy.wage_offered
        
        return max(worker_fallback, min(employer_fallback, negotiated_wage))
    
    def _age_vacancies(self):
        """Age vacancies and remove expired ones"""
        active_vacancies = []
        
        for vacancy in self.vacancies:
            if vacancy.status == JobMatchingStatus.VACANT:
                vacancy.posting_duration += 1
                
                if not vacancy.is_expired():
                    active_vacancies.append(vacancy)
                # Expired vacancies are removed
            elif vacancy.status == JobMatchingStatus.MATCHED:
                # Remove filled vacancies
                pass
        
        self.vacancies = active_vacancies
    
    def create_vacancies_based_on_demand(self):
        """Create new vacancies based on economic conditions and company needs"""
        unemployment_rate = self.calculate_unemployment_rate()
        
        # Companies create vacancies when unemployment is low or they're growing
        for company in self.market.getEmpresas():
            if not hasattr(company, 'dinero'):
                continue
            
            # Probability of posting vacancy based on company health and market conditions
            if company.dinero > 50000:  # Healthy companies
                base_prob = 0.3 if unemployment_rate < 0.08 else 0.15
                
                # Higher probability if company is very profitable
                if company.dinero > 200000:
                    base_prob *= 1.5
                
                if random.random() < base_prob:
                    # Determine sector
                    sector = getattr(company, 'sector_principal', 'general')
                    
                    # Create skill requirements based on sector
                    if hasattr(self.market, 'economia_sectorial') and hasattr(self.market.economia_sectorial, 'sectores'):
                        skill_reqs = {sector: random.uniform(0.4, 0.8)}
                        # Add some complementary skills
                        other_sectors = list(self.market.economia_sectorial.sectores.keys())
                        if len(other_sectors) > 1:
                            complement_sector = random.choice([s for s in other_sectors if s != sector])
                            skill_reqs[complement_sector] = random.uniform(0.2, 0.5)
                    else:
                        skill_reqs = {'general': random.uniform(0.4, 0.8)}
                    
                    self.post_vacancy(company, sector, skill_reqs)
    
    def job_destruction_process(self):
        """Handle job destruction due to economic conditions"""
        if not hasattr(self.market, 'fase_ciclo_economico'):
            return
        
        destruction_rate = 0.02  # Base 2% job destruction rate
        
        # Adjust based on economic cycle
        if self.market.fase_ciclo_economico in ['recesion', 'depresion']:
            destruction_rate = 0.08  # Higher destruction in recession
        elif self.market.fase_ciclo_economico in ['expansion']:
            destruction_rate = 0.01  # Lower destruction in expansion
        
        employed_workers = [c for c in self.market.getConsumidores() if getattr(c, 'empleado', False)]
        workers_to_fire = int(len(employed_workers) * destruction_rate)
        
        if workers_to_fire > 0:
            # Prioritize firing from struggling companies
            candidates = []
            for worker in employed_workers:
                if hasattr(worker, 'empleador') and hasattr(worker.empleador, 'dinero'):
                    # More likely to fire from companies with less money
                    company_health = worker.empleador.dinero
                    fire_probability = max(0.1, 1.0 - company_health / 100000)
                    candidates.append((worker, fire_probability))
            
            # Sort by fire probability and fire top candidates
            candidates.sort(key=lambda x: x[1], reverse=True)
            
            for worker, _ in candidates[:workers_to_fire]:
                if hasattr(worker.empleador, 'despedir'):
                    worker.empleador.despedir(worker)
    
    def calculate_unemployment_rate(self) -> float:
        """Calculate current unemployment rate"""
        total_workers = len(self.market.getConsumidores())
        if total_workers == 0:
            return 0.0
        
        unemployed = len([c for c in self.market.getConsumidores() if not getattr(c, 'empleado', False)])
        return unemployed / total_workers
    
    def calculate_average_wage(self) -> float:
        """Calculate average wage in the economy"""
        employed_workers = [c for c in self.market.getConsumidores() 
                          if getattr(c, 'empleado', False) and hasattr(c, 'ingreso_mensual')]
        
        if not employed_workers:
            return self.wage_curve_params['base_wage']
        
        total_wages = sum(worker.ingreso_mensual for worker in employed_workers)
        return total_wages / len(employed_workers)
    
    def update_metrics(self):
        """Update all labor market metrics"""
        prev_unemployment = self.metrics['unemployment_rate']
        prev_avg_wage = self.metrics['average_wage']
        
        self.metrics['unemployment_rate'] = self.calculate_unemployment_rate()
        self.metrics['average_wage'] = self.calculate_average_wage()
        self.metrics['total_vacancies'] = len(self.vacancies)
        
        # Calculate rates of change
        if prev_avg_wage > 0:
            self.metrics['wage_growth'] = (self.metrics['average_wage'] - prev_avg_wage) / prev_avg_wage
        
        # Match rate from recent matching
        self.metrics['match_rate'] = self.matching_efficiency * (1 - self.search_frictions)
    
    def labor_market_cycle(self):
        """Execute complete labor market cycle"""
        # 1. Update metrics
        self.update_metrics()
        
        # 2. Create new vacancies based on demand
        self.create_vacancies_based_on_demand()
        
        # 3. Execute matching process
        matching_stats = self.matching_process()
        
        # 4. Handle job destruction
        self.job_destruction_process()
        
        # 5. Update wage curve parameters based on conditions
        self._update_wage_curve()
        
        return {
            'unemployment_rate': self.metrics['unemployment_rate'],
            'average_wage': self.metrics['average_wage'],
            'total_vacancies': self.metrics['total_vacancies'],
            'matches_made': matching_stats['matches_made'],
            'applications_processed': matching_stats['applications_processed']
        }
    
    def _update_wage_curve(self):
        """Update wage curve parameters based on economic conditions"""
        # Adjust productivity factor based on economic cycle
        if hasattr(self.market, 'fase_ciclo_economico'):
            if self.market.fase_ciclo_economico == 'expansion':
                self.wage_curve_params['productivity_factor'] = min(1.2, 
                    self.wage_curve_params['productivity_factor'] + 0.01)
            elif self.market.fase_ciclo_economico in ['recesion', 'depresion']:
                self.wage_curve_params['productivity_factor'] = max(0.8,
                    self.wage_curve_params['productivity_factor'] - 0.01)
        
        # Adjust matching efficiency based on unemployment
        unemployment = self.metrics['unemployment_rate']
        if unemployment > 0.15:  # High unemployment improves matching efficiency
            self.matching_efficiency = min(0.8, self.matching_efficiency + 0.02)
        elif unemployment < 0.05:  # Low unemployment creates bottlenecks
            self.matching_efficiency = max(0.4, self.matching_efficiency - 0.01)
    
    def get_labor_market_report(self) -> str:
        """Generate comprehensive labor market report"""
        report = f"""
=== ENHANCED LABOR MARKET REPORT ===
Unemployment Rate: {self.metrics['unemployment_rate']:.1%}
Average Wage: ${self.metrics['average_wage']:,.0f}
Total Vacancies: {self.metrics['total_vacancies']}
Wage Growth: {self.metrics['wage_growth']:+.1%}
Match Rate: {self.metrics['match_rate']:.1%}

Wage Curve Parameters:
- Base Wage: ${self.wage_curve_params['base_wage']:,.0f}
- Unemployment Elasticity: {self.wage_curve_params['unemployment_elasticity']:.2f}
- Productivity Factor: {self.wage_curve_params['productivity_factor']:.2f}

Market Frictions:
- Matching Efficiency: {self.matching_efficiency:.1%}
- Search Frictions: {self.search_frictions:.1%}

Worker Profiles: {len(self.worker_profiles)} active
        """.strip()
        
        return report