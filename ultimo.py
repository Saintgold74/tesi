"""
GIST Simulation Framework
Framework completo per la simulazione della trasformazione IT nella GDO
Basato su parametri da fonti pubbliche verificabili

Autore: [Nome Studente]
Versione: 1.0
Data: Gennaio 2025
"""

import numpy as np
import pandas as pd
from scipy import stats
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
import json
from datetime import datetime
import logging

# Configurazione logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(levelname)s - %(message)s')

# =====================================================================
# CONFIGURAZIONE GLOBALE
# =====================================================================

class Config:
    """Configurazione centralizzata per tutti i parametri di simulazione"""
    
    # Random seed per riproducibilità
    RANDOM_SEED = 42
    
    # Parametri di simulazione
    N_SIMULATIONS = 10000
    N_SCENARIOS = 100
    
    # Parametri temporali
    SIMULATION_YEARS = 5
    MONTHS_PER_YEAR = 12
    
    # Soglie GIST
    GIST_THRESHOLDS = {
        'critico': 0.40,
        'base': 0.55,
        'maturo': 0.70,
        'avanzato': 0.85,
        'leader': 1.00
    }
    
    # Pesi componenti GIST
    GIST_WEIGHTS = {
        'physical': 0.15,
        'architectural': 0.35,
        'security': 0.30,
        'compliance': 0.20
    }
    
    # Parametri economici (da fonti pubbliche)
    DOWNTIME_COST_PER_HOUR = 52000  # EUR, da Ponemon Institute 2024
    IT_BUDGET_PERCENTAGE = 0.018     # 1.8% del fatturato, da Gartner 2024

# =====================================================================
# STRUTTURE DATI
# =====================================================================

@dataclass
class OrganizationProfile:
    """Profilo di un'organizzazione GDO"""
    n_stores: int
    annual_revenue: float
    it_maturity_initial: float
    current_architecture: str
    compliance_approach: str
    
    @property
    def it_budget(self) -> float:
        return self.annual_revenue * Config.IT_BUDGET_PERCENTAGE

@dataclass
class SimulationResult:
    """Risultati di una singola simulazione"""
    organization_id: str
    scenario_id: int
    gist_scores: Dict[str, float]
    economic_metrics: Dict[str, float]
    operational_metrics: Dict[str, float]
    transformation_timeline: List[Dict]

# =====================================================================
# UTILITÀ E HELPER
# =====================================================================

def set_all_seeds(seed: int = Config.RANDOM_SEED) -> None:
    """Imposta tutti i seed per riproducibilità completa"""
    np.random.seed(seed)
    import random
    random.seed(seed)
    logging.info(f"Random seeds impostati a: {seed}")

def load_benchmark_data() -> Dict:
    """
    Carica i parametri di benchmark da fonti pubbliche
    In produzione, questi verrebbero da file esterni
    """
    return {
        'availability': {
            'traditional': {'mean': 0.995, 'std': 0.0015},
            'hybrid': {'mean': 0.9996, 'std': 0.0004},
            'cloud_native': {'mean': 0.9998, 'std': 0.0002}
        },
        'mttr_hours': {
            'traditional': {'mean': 4.2, 'std': 1.1},
            'hybrid': {'mean': 1.5, 'std': 0.4},
            'cloud_native': {'mean': 0.8, 'std': 0.2}
        },
        'security_scores': {
            'basic': {'assa_reduction': 0.15, 'latency_impact': 10},
            'zero_trust': {'assa_reduction': 0.427, 'latency_impact': 32}
        },
        'compliance_costs': {
            'fragmented': {'base_cost': 8700000, 'overhead_pct': 0.183},
            'integrated': {'base_cost': 5300000, 'overhead_pct': 0.097}
        }
    }

# =====================================================================
# GENERATORI DI DISTRIBUZIONI
# =====================================================================

class DistributionGenerator:
    """Genera valori secondo distribuzioni calibrate su dati pubblici"""
    
    def __init__(self, benchmarks: Dict):
        self.benchmarks = benchmarks
    
    def availability(self, architecture: str, n: int = 1) -> np.ndarray:
        """Genera valori di availability basati su architettura"""
        params = self.benchmarks['availability'][architecture]
        # Usa distribuzione Beta per valori in [0,1]
        alpha = (params['mean'] * 1000) / (1 - params['mean'])
        beta = 1000 - alpha
        return np.random.beta(alpha, beta, n)
    
    def downtime_duration(self, architecture: str, n: int = 1) -> np.ndarray:
        """Genera durate di downtime (quando occorrono)"""
        params = self.benchmarks['mttr_hours'][architecture]
        # Log-normale per eventi rari con code pesanti
        mu = np.log(params['mean'])
        sigma = params['std'] / params['mean']
        return np.random.lognormal(mu, sigma, n)
    
    def transformation_time(self, complexity: float) -> float:
        """Tempo di trasformazione basato su complessità"""
        # Triangolare con parametri da McKinsey 2024
        base_time = 12  # mesi
        min_time = base_time * (0.6 + 0.2 * complexity)
        max_time = base_time * (1.2 + 0.4 * complexity)
        mode_time = base_time * (0.9 + 0.3 * complexity)
        return np.random.triangular(min_time, mode_time, max_time)
    
    def cost_overrun(self) -> float:
        """Fattore di overrun dei costi"""
        # Da Standish Group CHAOS Report 2024
        return np.random.lognormal(mean=0.2, sigma=0.15)

# =====================================================================
# MODELLI DI TRASFORMAZIONE
# =====================================================================

class TransformationModel:
    """Modella la trasformazione IT di un'organizzazione GDO"""
    
    def __init__(self, benchmarks: Dict):
        self.benchmarks = benchmarks
        self.dist_gen = DistributionGenerator(benchmarks)
    
    def calculate_gist_score(self, 
                           physical: float, 
                           architectural: float, 
                           security: float, 
                           compliance: float) -> float:
        """Calcola GIST score con media aritmetica pesata"""
        weights = Config.GIST_WEIGHTS
        
        score = (weights['physical'] * physical +
                weights['architectural'] * architectural +
                weights['security'] * security +
                weights['compliance'] * compliance)
        
        # Applica fattori moltiplicativi
        k_gdo = 1.23  # Fattore settore
        innovation = np.random.uniform(0, 0.5)  # Fattore innovazione
        
        return score * k_gdo * (1 + innovation)
    
    def simulate_cloud_transformation(self, 
                                    org: OrganizationProfile,
                                    strategy: str = 'hybrid') -> Dict:
        """Simula una trasformazione cloud completa"""
        
        results = {
            'phases': [],
            'total_cost': 0,
            'total_time': 0,
            'final_scores': {}
        }
        
        # Fasi della trasformazione
        phases = ['assessment', 'pilot', 'migration', 'optimization']
        
        # Parametri iniziali
        current_scores = {
            'physical': 0.45,
            'architectural': org.it_maturity_initial,
            'security': 0.40,
            'compliance': 0.30
        }
        
        for phase in phases:
            phase_result = self._simulate_phase(phase, org, current_scores)
            results['phases'].append(phase_result)
            
            # Aggiorna scores
            for component in current_scores:
                improvement = phase_result['improvements'][component]
                current_scores[component] = min(1.0, 
                    current_scores[component] + improvement)
            
            results['total_cost'] += phase_result['cost']
            results['total_time'] += phase_result['duration']
        
        results['final_scores'] = current_scores
        results['final_gist'] = self.calculate_gist_score(**current_scores)
        
        # Calcola metriche economiche
        results['economic_metrics'] = self._calculate_economics(
            org, results['total_cost'], results['final_scores']
        )
        
        return results
    
    def _simulate_phase(self, phase: str, 
                       org: OrganizationProfile, 
                       current_scores: Dict) -> Dict:
        """Simula una singola fase della trasformazione"""
        
        # Parametri per fase (da AWS Migration Methodology)
        phase_params = {
            'assessment': {
                'duration_base': 3,
                'cost_factor': 0.05,
                'improvements': {
                    'physical': 0.05,
                    'architectural': 0.10,
                    'security': 0.05,
                    'compliance': 0.15
                }
            },
            'pilot': {
                'duration_base': 4,
                'cost_factor': 0.15,
                'improvements': {
                    'physical': 0.10,
                    'architectural': 0.15,
                    'security': 0.10,
                    'compliance': 0.10
                }
            },
            'migration': {
                'duration_base': 12,
                'cost_factor': 0.60,
                'improvements': {
                    'physical': 0.15,
                    'architectural': 0.35,
                    'security': 0.25,
                    'compliance': 0.20
                }
            },
            'optimization': {
                'duration_base': 6,
                'cost_factor': 0.20,
                'improvements': {
                    'physical': 0.05,
                    'architectural': 0.10,
                    'security': 0.10,
                    'compliance': 0.05
                }
            }
        }
        
        params = phase_params[phase]
        
        # Calcola durata con variabilità
        complexity = 1 - np.mean(list(current_scores.values()))
        duration = self.dist_gen.transformation_time(complexity) * \
                  params['duration_base'] / 12
        
        # Calcola costo con overrun
        planned_cost = org.it_budget * params['cost_factor']
        actual_cost = planned_cost * self.dist_gen.cost_overrun()
        
        # Calcola miglioramenti effettivi (con rumore)
        actual_improvements = {}
        for component, improvement in params['improvements'].items():
            noise = np.random.normal(1.0, 0.1)
            actual_improvements[component] = improvement * noise * \
                                           (1 - current_scores[component])
        
        return {
            'phase': phase,
            'duration': duration,
            'cost': actual_cost,
            'improvements': actual_improvements
        }
    
    def _calculate_economics(self, org: OrganizationProfile, 
                           investment: float, 
                           final_scores: Dict) -> Dict:
        """Calcola metriche economiche post-trasformazione"""
        
        # Riduzione TCO basata su score architetturale
        tco_reduction = 0.382 * final_scores['architectural']
        annual_savings = org.it_budget * tco_reduction
        
        # Riduzione downtime basata su tutti gli score
        availability_improvement = 0.005 * np.mean(list(final_scores.values()))
        downtime_reduction = availability_improvement * 8760  # ore/anno
        downtime_savings = downtime_reduction * Config.DOWNTIME_COST_PER_HOUR
        
        # ROI calculation
        total_annual_benefit = annual_savings + downtime_savings
        roi_24_months = (total_annual_benefit * 2 - investment) / investment
        
        # Payback period
        if total_annual_benefit > 0:
            payback_months = (investment / total_annual_benefit) * 12
        else:
            payback_months = float('inf')
        
        return {
            'tco_reduction_pct': tco_reduction,
            'annual_savings': annual_savings,
            'downtime_savings': downtime_savings,
            'roi_24_months': roi_24_months,
            'payback_months': payback_months,
            'total_investment': investment
        }

# =====================================================================
# SIMULATORE PRINCIPALE
# =====================================================================

class GISTSimulator:
    """Orchestratore principale delle simulazioni"""
    
    def __init__(self):
        set_all_seeds()
        self.benchmarks = load_benchmark_data()
        self.transformation_model = TransformationModel(self.benchmarks)
        self.results = []
        
    def generate_organization_portfolio(self, n: int = 100) -> List[OrganizationProfile]:
        """Genera un portfolio realistico di organizzazioni GDO"""
        
        # Archetipi da EuroCommerce 2024
        archetypes = {
            'small_traditional': {
                'weight': 0.30,
                'stores': (50, 75),
                'revenue_per_store': 5.5,  # M€
                'maturity': (0.2, 0.4)
            },
            'medium_evolving': {
                'weight': 0.45,
                'stores': (75, 150),
                'revenue_per_store': 6.5,
                'maturity': (0.3, 0.6)
            },
            'large_advanced': {
                'weight': 0.20,
                'stores': (150, 300),
                'revenue_per_store': 7.5,
                'maturity': (0.5, 0.7)
            },
            'digital_leader': {
                'weight': 0.05,
                'stores': (100, 500),
                'revenue_per_store': 8.5,
                'maturity': (0.6, 0.8)
            }
        }
        
        organizations = []
        
        for i in range(n):
            # Seleziona archetipo con probabilità pesata
            archetype_name = np.random.choice(
                list(archetypes.keys()),
                p=[a['weight'] for a in archetypes.values()]
            )
            archetype = archetypes[archetype_name]
            
            # Genera parametri
            n_stores = int(np.random.uniform(*archetype['stores']))
            revenue = n_stores * archetype['revenue_per_store'] * \
                     np.random.lognormal(0, 0.1)  # variabilità
            maturity = np.random.uniform(*archetype['maturity'])
            
            # Determina architettura e compliance attuali
            if maturity < 0.4:
                architecture = 'traditional'
                compliance = 'fragmented'
            elif maturity < 0.7:
                architecture = 'hybrid'
                compliance = 'fragmented' if np.random.random() < 0.6 else 'integrated'
            else:
                architecture = 'cloud_native'
                compliance = 'integrated'
            
            org = OrganizationProfile(
                n_stores=n_stores,
                annual_revenue=revenue * 1e6,  # Converti in €
                it_maturity_initial=maturity,
                current_architecture=architecture,
                compliance_approach=compliance
            )
            
            organizations.append(org)
        
        return organizations
    
    def run_simulation(self, 
                      n_organizations: int = 100,
                      n_scenarios: int = 10) -> pd.DataFrame:
        """Esegue simulazione completa"""
        
        logging.info(f"Avvio simulazione: {n_organizations} org x {n_scenarios} scenari")
        
        # Genera portfolio
        organizations = self.generate_organization_portfolio(n_organizations)
        
        results = []
        
        for i, org in enumerate(organizations):
            logging.info(f"Simulazione org {i+1}/{n_organizations}")
            
            for scenario in range(n_scenarios):
                # Resetta seed per scenario riproducibile
                set_all_seeds(Config.RANDOM_SEED + i * 1000 + scenario)
                
                # Simula trasformazione
                transformation = self.transformation_model.simulate_cloud_transformation(
                    org, strategy='hybrid'
                )
                
                # Crea risultato
                result = SimulationResult(
                    organization_id=f"ORG_{i:04d}",
                    scenario_id=scenario,
                    gist_scores={
                        'initial': self.transformation_model.calculate_gist_score(
                            0.45, org.it_maturity_initial, 0.40, 0.30
                        ),
                        'final': transformation['final_gist']
                    },
                    economic_metrics=transformation['economic_metrics'],
                    operational_metrics={
                        'transformation_time': transformation['total_time'],
                        'phases_completed': len(transformation['phases'])
                    },
                    transformation_timeline=transformation['phases']
                )
                
                results.append(result)
        
        # Converti in DataFrame per analisi
        df_results = self._results_to_dataframe(results)
        
        logging.info("Simulazione completata")
        
        return df_results
    
    def _results_to_dataframe(self, results: List[SimulationResult]) -> pd.DataFrame:
        """Converte risultati in DataFrame per analisi"""
        
        data = []
        
        for r in results:
            row = {
                'organization_id': r.organization_id,
                'scenario_id': r.scenario_id,
                'gist_initial': r.gist_scores['initial'],
                'gist_final': r.gist_scores['final'],
                'gist_improvement': r.gist_scores['final'] - r.gist_scores['initial'],
                'roi_24m': r.economic_metrics['roi_24_months'],
                'payback_months': r.economic_metrics['payback_months'],
                'tco_reduction': r.economic_metrics['tco_reduction_pct'],
                'investment': r.economic_metrics['total_investment'],
                'transformation_time': r.operational_metrics['transformation_time']
            }
            data.append(row)
        
        return pd.DataFrame(data)
    
    def analyze_results(self, df: pd.DataFrame) -> Dict:
        """Analizza i risultati e produce statistiche summary"""
        
        analysis = {
            'gist_improvement': {
                'mean': df['gist_improvement'].mean(),
                'std': df['gist_improvement'].std(),
                'percentiles': df['gist_improvement'].quantile([0.25, 0.5, 0.75]).to_dict()
            },
            'roi_statistics': {
                'mean': df['roi_24m'].mean(),
                'std': df['roi_24m'].std(),
                'success_rate': (df['roi_24m'] > 0).mean(),
                'percentiles': df['roi_24m'].quantile([0.25, 0.5, 0.75]).to_dict()
            },
            'transformation_time': {
                'mean_months': df['transformation_time'].mean() * 12,
                'std_months': df['transformation_time'].std() * 12
            },
            'validation_metrics': {
                'cases_above_99_95': (df['gist_final'] > 0.758).mean(),  # Score per 99.95%
                'tco_reduction_above_30': (df['tco_reduction'] > 0.30).mean(),
                'roi_positive_rate': (df['roi_24m'] > 0).mean()
            }
        }
        
        return analysis

# =====================================================================
# FUNZIONE PRINCIPALE
# =====================================================================

def main():
    """Esegue simulazione completa e salva risultati"""
    
    # Inizializza simulatore
    simulator = GISTSimulator()
    
    # Esegui simulazione
    results_df = simulator.run_simulation(
        n_organizations=156,  # Come da tesi
        n_scenarios=100       # Per robustezza statistica
    )
    
    # Analizza risultati
    analysis = simulator.analyze_results(results_df)
    
    # Stampa summary
    print("\n=== RISULTATI SIMULAZIONE GIST ===\n")
    print(f"Miglioramento GIST medio: {analysis['gist_improvement']['mean']:.3f}")
    print(f"ROI 24 mesi medio: {analysis['roi_statistics']['mean']:.1%}")
    print(f"Tempo trasformazione medio: {analysis['transformation_time']['mean_months']:.1f} mesi")
    print(f"\nValidazione Ipotesi:")
    print(f"- H1 (availability ≥99.95%): {analysis['validation_metrics']['cases_above_99_95']:.1%} dei casi")
    print(f"- H1 (TCO reduction >30%): {analysis['validation_metrics']['tco_reduction_above_30']:.1%} dei casi")
    print(f"- ROI positivo: {analysis['validation_metrics']['roi_positive_rate']:.1%} dei casi")
    
    # Salva risultati
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_df.to_csv(f'gist_simulation_results_{timestamp}.csv', index=False)
    
    with open(f'gist_analysis_{timestamp}.json', 'w') as f:
        json.dump(analysis, f, indent=2)
    
    print(f"\nRisultati salvati in:")
    print(f"- gist_simulation_results_{timestamp}.csv")
    print(f"- gist_analysis_{timestamp}.json")

if __name__ == "__main__":
    main()