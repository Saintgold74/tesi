#!/usr/bin/env python3
"""
VERSIONE FINALE CORRETTA - ZERO ERRORI
=====================================
Framework di simulazione per validazione ipotesi H1, H2, H3
Versione corretta per NumPy moderno, garantisce funzionamento completo
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
from scipy import stats
from datetime import datetime

# Seed per riproducibilità
np.random.seed(42)
random.seed(42)

class OrganizationProfile:
    """Profilo organizzazione GDO"""
    def __init__(self, org_id, revenue_m_euro, num_stores, num_employees, 
                 current_architecture, security_maturity, compliance_baseline_cost, it_budget_m_euro):
        self.org_id = org_id
        self.revenue_m_euro = revenue_m_euro
        self.num_stores = num_stores
        self.num_employees = num_employees
        self.current_architecture = current_architecture
        self.security_maturity = security_maturity
        self.compliance_baseline_cost = compliance_baseline_cost
        self.it_budget_m_euro = it_budget_m_euro

class GDOSimulationFramework:
    """Framework di simulazione per validazione ipotesi"""
    
    def __init__(self, num_organizations=15):
        self.num_orgs = num_organizations
        self.organizations = []
        self.results = {'h1_results': [], 'h2_results': [], 'h3_results': []}
        
        # Parametri da letteratura
        self.params = {
            'legacy_availability': 0.997,
            'cloud_target_availability': 0.9995,
            'cloud_tco_reduction_min': 0.15,
            'cloud_tco_reduction_max': 0.25,
            'migration_overhead_min': 0.01,
            'migration_overhead_max': 0.05,
            'assa_baseline': 100,
            'zt_reduction_min': 0.35,
            'zt_reduction_max': 0.55,
            'baseline_latency_min': 45,
            'baseline_latency_max': 85,
            'zt_latency_overhead_min': 15,
            'zt_latency_overhead_max': 25,
            'zt_max_acceptable_latency': 25,
            'compliance_cost_min_percent': 2.0,
            'compliance_cost_max_percent': 3.5,
            'cost_reduction_min': 0.30,
            'cost_reduction_max': 0.45,
            'operational_overhead_min': 0.05,
            'operational_overhead_max': 0.12,
        }
        
        self.generate_organizations()
    
    def generate_organizations(self):
        """Genera profili organizzazioni realistici"""
        revenue_distribution = [50, 75, 120, 200, 350, 500, 800, 1200, 
                              1800, 2500, 3200, 4100, 5500, 8000, 12000]
        
        for i in range(self.num_orgs):
            revenue = revenue_distribution[i] + random.uniform(-10, 10)
            num_stores = int(revenue * random.uniform(0.8, 1.2))
            num_employees = int(num_stores * random.uniform(80, 150))
            it_budget = revenue * random.uniform(0.015, 0.025)
            
            if revenue < 100:
                arch_weights = [0.7, 0.25, 0.05]
                security_maturity = random.uniform(0.3, 0.6)
            elif revenue < 1000:
                arch_weights = [0.4, 0.5, 0.1]
                security_maturity = random.uniform(0.5, 0.75)
            else:
                arch_weights = [0.2, 0.6, 0.2]
                security_maturity = random.uniform(0.7, 0.9)
            
            current_arch = np.random.choice(['legacy', 'hybrid', 'cloud-first'], p=arch_weights)
            
            compliance_cost = revenue * random.uniform(
                self.params['compliance_cost_min_percent'],
                self.params['compliance_cost_max_percent']
            ) / 100
            
            org = OrganizationProfile(
                org_id=f"GDO_{i+1:02d}",
                revenue_m_euro=revenue,
                num_stores=num_stores,
                num_employees=num_employees,
                current_architecture=current_arch,
                security_maturity=security_maturity,
                compliance_baseline_cost=compliance_cost,
                it_budget_m_euro=it_budget
            )
            
            self.organizations.append(org)
    
    def simulate_h1_cloud_migration(self, org):
        """Simula H1: Cloud-First"""
        baseline_availability = self.params['legacy_availability']
        baseline_tco = org.it_budget_m_euro
        
        migration_complexity = 1.0 - org.security_maturity
        migration_duration = random.uniform(6, 18) * (1 + migration_complexity * 0.5)
        
        target_availability = self.params['cloud_target_availability']
        achieved_availability = random.uniform(
            target_availability - 0.0003,
            target_availability + 0.0005
        )
        achieved_availability += (org.security_maturity - 0.5) * 0.0002
        
        base_tco_reduction = random.uniform(
            self.params['cloud_tco_reduction_min'],
            self.params['cloud_tco_reduction_max']
        )
        tco_reduction = base_tco_reduction * (0.8 + org.security_maturity * 0.4)
        
        base_overhead = random.uniform(
            self.params['migration_overhead_min'],
            self.params['migration_overhead_max']
        )
        operational_overhead = base_overhead * (1.5 - org.security_maturity)
        
        availability_target_met = achieved_availability >= self.params['cloud_target_availability']
        tco_reduction_adequate = tco_reduction >= 0.15
        overhead_acceptable = operational_overhead <= 0.03
        
        h1_success = availability_target_met and tco_reduction_adequate and overhead_acceptable
        
        return {
            'org_id': org.org_id,
            'revenue': org.revenue_m_euro,
            'security_maturity': org.security_maturity,
            'migration_duration_months': migration_duration,
            'baseline_availability': baseline_availability,
            'achieved_availability': achieved_availability,
            'availability_improvement': achieved_availability - baseline_availability,
            'baseline_tco_m_euro': baseline_tco,
            'tco_reduction_percent': tco_reduction * 100,
            'tco_savings_m_euro': baseline_tco * tco_reduction,
            'operational_overhead_percent': operational_overhead * 100,
            'h1_success': h1_success,
            'success_factors': {
                'availability_target_met': availability_target_met,
                'tco_reduction_adequate': tco_reduction_adequate,
                'overhead_acceptable': overhead_acceptable
            }
        }
    
    def simulate_h2_zero_trust(self, org):
        """Simula H2: Zero Trust"""
        baseline_assa = self.params['assa_baseline'] * (1.2 - org.security_maturity)
        zt_implementation_duration = random.uniform(8, 16)
        
        base_assa_reduction = random.uniform(
            self.params['zt_reduction_min'],
            self.params['zt_reduction_max']
        )
        assa_reduction = base_assa_reduction * (0.7 + org.security_maturity * 0.6)
        final_assa = baseline_assa * (1 - assa_reduction)
        
        baseline_latency = random.uniform(
            self.params['baseline_latency_min'],
            self.params['baseline_latency_max']
        )
        
        base_zt_overhead = random.uniform(
            self.params['zt_latency_overhead_min'],
            self.params['zt_latency_overhead_max']
        )
        zt_latency_overhead = base_zt_overhead * (1.3 - org.security_maturity)
        final_latency = baseline_latency + zt_latency_overhead
        
        assa_reduction_adequate = assa_reduction >= 0.20
        latency_acceptable = zt_latency_overhead <= self.params['zt_max_acceptable_latency']
        ux_maintained = final_latency <= 110
        
        h2_success = assa_reduction_adequate and latency_acceptable and ux_maintained
        
        return {
            'org_id': org.org_id,
            'revenue': org.revenue_m_euro,
            'security_maturity': org.security_maturity,
            'implementation_duration_months': zt_implementation_duration,
            'baseline_assa_score': baseline_assa,
            'final_assa_score': final_assa,
            'assa_reduction_percent': assa_reduction * 100,
            'baseline_latency_ms': baseline_latency,
            'zt_latency_overhead_ms': zt_latency_overhead,
            'final_latency_ms': final_latency,
            'h2_success': h2_success,
            'success_factors': {
                'assa_reduction_adequate': assa_reduction_adequate,
                'latency_acceptable': latency_acceptable,
                'ux_maintained': ux_maintained
            }
        }
    
    def simulate_h3_compliance_integration(self, org):
        """Simula H3: Compliance-by-Design"""
        baseline_compliance_cost = org.compliance_baseline_cost
        integration_duration = random.uniform(10, 18)
        
        base_cost_reduction = random.uniform(
            self.params['cost_reduction_min'],
            self.params['cost_reduction_max']
        )
        cost_reduction = base_cost_reduction * (0.8 + org.security_maturity * 0.4)
        
        base_op_overhead = random.uniform(
            self.params['operational_overhead_min'],
            self.params['operational_overhead_max']
        )
        operational_overhead = base_op_overhead * (1.2 - org.security_maturity)
        
        baseline_audit_days = random.uniform(45, 90)
        integrated_audit_days = random.uniform(20, 40)
        audit_efficiency = (baseline_audit_days - integrated_audit_days) / baseline_audit_days
        
        base_coverage = random.uniform(0.85, 0.98)
        compliance_coverage = base_coverage * (0.7 + org.security_maturity * 0.3)
        
        cost_reduction_adequate = cost_reduction >= 0.30
        overhead_acceptable = operational_overhead <= 0.10
        coverage_adequate = compliance_coverage >= 0.90
        
        h3_success = cost_reduction_adequate and overhead_acceptable and coverage_adequate
        
        return {
            'org_id': org.org_id,
            'revenue': org.revenue_m_euro,
            'security_maturity': org.security_maturity,
            'implementation_duration_months': integration_duration,
            'baseline_compliance_cost_m_euro': baseline_compliance_cost,
            'cost_reduction_percent': cost_reduction * 100,
            'cost_savings_m_euro': baseline_compliance_cost * cost_reduction,
            'operational_overhead_percent': operational_overhead * 100,
            'baseline_audit_days': baseline_audit_days,
            'integrated_audit_days': integrated_audit_days,
            'audit_efficiency_improvement_percent': audit_efficiency * 100,
            'compliance_coverage_percent': compliance_coverage * 100,
            'h3_success': h3_success,
            'success_factors': {
                'cost_reduction_adequate': cost_reduction_adequate,
                'overhead_acceptable': overhead_acceptable,
                'coverage_adequate': coverage_adequate
            }
        }
    
    def run_complete_simulation(self):
        """Esegue simulazione completa"""
        print(f"SIMULAZIONE {self.num_orgs} ORGANIZZAZIONI GDO")
        print("=" * 50)
        
        for i, org in enumerate(self.organizations, 1):
            print(f"[{i:2d}/15] {org.org_id}: €{org.revenue_m_euro:.0f}M, {org.current_architecture}, maturità {org.security_maturity:.2f}")
            
            h1_result = self.simulate_h1_cloud_migration(org)
            self.results['h1_results'].append(h1_result)
            
            h2_result = self.simulate_h2_zero_trust(org)
            self.results['h2_results'].append(h2_result)
            
            h3_result = self.simulate_h3_compliance_integration(org)
            self.results['h3_results'].append(h3_result)
        
        return self.analyze_results()
    
    def analyze_results(self):
        """Analisi statistiche"""
        h1_df = pd.DataFrame(self.results['h1_results'])
        h2_df = pd.DataFrame(self.results['h2_results'])
        h3_df = pd.DataFrame(self.results['h3_results'])
        
        analysis = {
            'h1': {
                'success_rate': h1_df['h1_success'].mean(),
                'availability_mean': h1_df['achieved_availability'].mean(),
                'availability_std': h1_df['achieved_availability'].std(),
                'tco_reduction_mean': h1_df['tco_reduction_percent'].mean(),
                'tco_reduction_std': h1_df['tco_reduction_percent'].std(),
                'overhead_mean': h1_df['operational_overhead_percent'].mean(),
                'overhead_std': h1_df['operational_overhead_percent'].std(),
                'total_savings_m_euro': h1_df['tco_savings_m_euro'].sum()
            },
            'h2': {
                'success_rate': h2_df['h2_success'].mean(),
                'assa_reduction_mean': h2_df['assa_reduction_percent'].mean(),
                'assa_reduction_std': h2_df['assa_reduction_percent'].std(),
                'latency_overhead_mean': h2_df['zt_latency_overhead_ms'].mean(),
                'latency_overhead_std': h2_df['zt_latency_overhead_ms'].std(),
            },
            'h3': {
                'success_rate': h3_df['h3_success'].mean(),
                'cost_reduction_mean': h3_df['cost_reduction_percent'].mean(),
                'cost_reduction_std': h3_df['cost_reduction_percent'].std(),
                'overhead_mean': h3_df['operational_overhead_percent'].mean(),
                'overhead_std': h3_df['operational_overhead_percent'].std(),
                'coverage_mean': h3_df['compliance_coverage_percent'].mean(),
                'total_savings_m_euro': h3_df['cost_savings_m_euro'].sum(),
                'audit_efficiency_mean': h3_df['audit_efficiency_improvement_percent'].mean()
            }
        }
        
        return analysis
    
    def validate_hypotheses_statistically(self, analysis):
        """Validazione statistica"""
        print("\nVALIDAZIONE STATISTICA IPOTESI")
        print("=" * 40)
        
        alpha = 0.05
        
        # H1
        h1_data = pd.DataFrame(self.results['h1_results'])
        t_avail, p_avail = stats.ttest_1samp(h1_data['achieved_availability'], 0.9995, alternative='greater')
        t_tco, p_tco = stats.ttest_1samp(h1_data['tco_reduction_percent'], 15, alternative='greater')
        t_overhead, p_overhead = stats.ttest_1samp(h1_data['operational_overhead_percent'], 3, alternative='less')
        
        h1_validated = (p_avail < alpha and p_tco < alpha and p_overhead < alpha and analysis['h1']['success_rate'] >= 0.8)
        
        print(f"H1 - CLOUD-FIRST:")
        print(f"  Availability: p={p_avail:.4f} {'✓' if p_avail < alpha else '✗'}")
        print(f"  TCO: p={p_tco:.4f} {'✓' if p_tco < alpha else '✗'}")
        print(f"  Overhead: p={p_overhead:.4f} {'✓' if p_overhead < alpha else '✗'}")
        print(f"  RISULTATO: {'✅ VALIDATA' if h1_validated else '❌ NON VALIDATA'}")
        
        # H2
        h2_data = pd.DataFrame(self.results['h2_results'])
        t_assa, p_assa = stats.ttest_1samp(h2_data['assa_reduction_percent'], 20, alternative='greater')
        t_latency, p_latency = stats.ttest_1samp(h2_data['zt_latency_overhead_ms'], 25, alternative='less')
        
        h2_validated = (p_assa < alpha and p_latency < alpha and analysis['h2']['success_rate'] >= 0.8)
        
        print(f"\nH2 - ZERO TRUST:")
        print(f"  ASSA: p={p_assa:.4f} {'✓' if p_assa < alpha else '✗'}")
        print(f"  Latency: p={p_latency:.4f} {'✓' if p_latency < alpha else '✗'}")
        print(f"  RISULTATO: {'✅ VALIDATA' if h2_validated else '❌ NON VALIDATA'}")
        
        # H3
        h3_data = pd.DataFrame(self.results['h3_results'])
        t_cost, p_cost = stats.ttest_1samp(h3_data['cost_reduction_percent'], 30, alternative='greater')
        t_oh, p_oh = stats.ttest_1samp(h3_data['operational_overhead_percent'], 10, alternative='less')
        t_coverage, p_coverage = stats.ttest_1samp(h3_data['compliance_coverage_percent'], 90, alternative='greater')
        
        h3_validated = (p_cost < alpha and p_oh < alpha and p_coverage < alpha and analysis['h3']['success_rate'] >= 0.8)
        
        print(f"\nH3 - COMPLIANCE:")
        print(f"  Cost: p={p_cost:.4f} {'✓' if p_cost < alpha else '✗'}")
        print(f"  Overhead: p={p_oh:.4f} {'✓' if p_oh < alpha else '✗'}")
        print(f"  Coverage: p={p_coverage:.4f} {'✓' if p_coverage < alpha else '✗'}")
        print(f"  RISULTATO: {'✅ VALIDATA' if h3_validated else '❌ NON VALIDATA'}")
        
        total_validated = sum([h1_validated, h2_validated, h3_validated])
        
        print(f"\n🎯 FINALE: {total_validated}/3 ipotesi validate")
        
        return {
            'h1_validated': h1_validated,
            'h2_validated': h2_validated,
            'h3_validated': h3_validated,
            'total_validated': total_validated,
            'statistical_tests': {
                'h1': {'availability': p_avail, 'tco': p_tco, 'overhead': p_overhead},
                'h2': {'assa': p_assa, 'latency': p_latency},
                'h3': {'cost': p_cost, 'overhead': p_oh, 'coverage': p_coverage}
            }
        }
    
    def generate_visualizations(self):
        """Genera grafici"""
        print("\nGenerazione grafici...")
        
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle('Risultati Simulazione - Validazione Ipotesi H1, H2, H3', fontsize=14, fontweight='bold')
        
        h1_data = pd.DataFrame(self.results['h1_results'])
        h2_data = pd.DataFrame(self.results['h2_results'])
        h3_data = pd.DataFrame(self.results['h3_results'])
        
        # H1: Availability
        axes[0,0].hist(h1_data['achieved_availability'], bins=10, alpha=0.7, color='blue', edgecolor='black')
        axes[0,0].axvline(0.9995, color='red', linestyle='--', linewidth=2, label='Target (99.95%)')
        axes[0,0].set_title('H1: Availability Raggiunta')
        axes[0,0].set_xlabel('Availability')
        axes[0,0].set_ylabel('Frequenza')
        axes[0,0].legend()
        axes[0,0].grid(True, alpha=0.3)
        
        # H1: TCO
        axes[0,1].hist(h1_data['tco_reduction_percent'], bins=10, alpha=0.7, color='green', edgecolor='black')
        axes[0,1].axvline(15, color='red', linestyle='--', linewidth=2, label='Target (15%)')
        axes[0,1].set_title('H1: Riduzione TCO (%)')
        axes[0,1].set_xlabel('TCO Reduction (%)')
        axes[0,1].set_ylabel('Frequenza')
        axes[0,1].legend()
        axes[0,1].grid(True, alpha=0.3)
        
        # H2: ASSA
        axes[0,2].hist(h2_data['assa_reduction_percent'], bins=10, alpha=0.7, color='orange', edgecolor='black')
        axes[0,2].axvline(20, color='red', linestyle='--', linewidth=2, label='Target (20%)')
        axes[0,2].set_title('H2: Riduzione Superficie Attacco (%)')
        axes[0,2].set_xlabel('ASSA Reduction (%)')
        axes[0,2].set_ylabel('Frequenza')
        axes[0,2].legend()
        axes[0,2].grid(True, alpha=0.3)
        
        # H2: Latency
        axes[1,0].hist(h2_data['zt_latency_overhead_ms'], bins=10, alpha=0.7, color='purple', edgecolor='black')
        axes[1,0].axvline(25, color='red', linestyle='--', linewidth=2, label='Max (25ms)')
        axes[1,0].set_title('H2: Latency Overhead (ms)')
        axes[1,0].set_xlabel('Latency Overhead (ms)')
        axes[1,0].set_ylabel('Frequenza')
        axes[1,0].legend()
        axes[1,0].grid(True, alpha=0.3)
        
        # H3: Cost
        axes[1,1].hist(h3_data['cost_reduction_percent'], bins=10, alpha=0.7, color='red', edgecolor='black')
        axes[1,1].axvline(30, color='blue', linestyle='--', linewidth=2, label='Target Min (30%)')
        axes[1,1].axvline(40, color='blue', linestyle=':', linewidth=2, label='Target Max (40%)')
        axes[1,1].set_title('H3: Riduzione Costi (%)')
        axes[1,1].set_xlabel('Cost Reduction (%)')
        axes[1,1].set_ylabel('Frequenza')
        axes[1,1].legend()
        axes[1,1].grid(True, alpha=0.3)
        
        # Success rates
        success_rates = [
            h1_data['h1_success'].mean(),
            h2_data['h2_success'].mean(),
            h3_data['h3_success'].mean()
        ]
        
        bars = axes[1,2].bar(['H1\n(Cloud)', 'H2\n(ZeroT)', 'H3\n(Compl)'], 
                           success_rates, color=['blue', 'orange', 'red'], alpha=0.7, edgecolor='black')
        axes[1,2].axhline(0.8, color='green', linestyle='--', linewidth=2, label='Target (80%)')
        axes[1,2].set_title('Tasso di Successo')
        axes[1,2].set_ylabel('Success Rate')
        axes[1,2].set_ylim(0, 1)
        axes[1,2].legend()
        axes[1,2].grid(True, alpha=0.3)
        
        for bar, rate in zip(bars, success_rates):
            height = bar.get_height()
            axes[1,2].text(bar.get_x() + bar.get_width()/2., height + 0.01,
                         f'{rate:.1%}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('hypothesis_validation_results.png', dpi=300, bbox_inches='tight')
        print("Grafici salvati: hypothesis_validation_results.png")
        return fig
    
    def save_results_simple(self, analysis, validation_results):
        """Salvataggio semplificato - no JSON"""
        h1_df = pd.DataFrame(self.results['h1_results'])
        h2_df = pd.DataFrame(self.results['h2_results'])
        h3_df = pd.DataFrame(self.results['h3_results'])
        
        h1_df.to_csv('h1_cloud_results.csv', index=False)
        h2_df.to_csv('h2_zerotrust_results.csv', index=False)
        h3_df.to_csv('h3_compliance_results.csv', index=False)
        
        # Report per tesi
        with open('thesis_simulation_report.txt', 'w', encoding='utf-8') as f:
            f.write("REPORT SIMULAZIONE PER TESI\n")
            f.write("=" * 35 + "\n\n")
            
            f.write("VALIDAZIONE IPOTESI:\n")
            f.write(f"H1 (Cloud-First): {'VALIDATA' if validation_results['h1_validated'] else 'NON VALIDATA'}\n")
            f.write(f"H2 (Zero Trust): {'VALIDATA' if validation_results['h2_validated'] else 'NON VALIDATA'}\n")
            f.write(f"H3 (Compliance): {'VALIDATA' if validation_results['h3_validated'] else 'NON VALIDATA'}\n")
            f.write(f"Totale: {validation_results['total_validated']}/3\n\n")
            
            f.write("METRICHE PRINCIPALI:\n")
            f.write(f"H1 - Availability: {analysis['h1']['availability_mean']:.4f} (target: ≥0.9995)\n")
            f.write(f"H1 - TCO reduction: {analysis['h1']['tco_reduction_mean']:.1f}% (target: ≥15%)\n")
            f.write(f"H1 - Overhead: {analysis['h1']['overhead_mean']:.1f}% (target: <3%)\n")
            f.write(f"H2 - ASSA reduction: {analysis['h2']['assa_reduction_mean']:.1f}% (target: ≥20%)\n")
            f.write(f"H2 - Latency overhead: {analysis['h2']['latency_overhead_mean']:.1f}ms (target: <25ms)\n")
            f.write(f"H3 - Cost reduction: {analysis['h3']['cost_reduction_mean']:.1f}% (target: 30-40%)\n")
            f.write(f"H3 - Overhead: {analysis['h3']['overhead_mean']:.1f}% (target: <10%)\n")
            f.write(f"H3 - Coverage: {analysis['h3']['coverage_mean']:.1f}% (target: ≥90%)\n\n")
            
            f.write("BENEFICI ECONOMICI:\n")
            f.write(f"Risparmi TCO: €{analysis['h1']['total_savings_m_euro']:.1f}M\n")
            f.write(f"Risparmi compliance: €{analysis['h3']['total_savings_m_euro']:.1f}M\n")
            f.write(f"Totale: €{analysis['h1']['total_savings_m_euro'] + analysis['h3']['total_savings_m_euro']:.1f}M\n\n")
            
            f.write("SIGNIFICATIVITÀ STATISTICA (α=0.05):\n")
            for hypothesis, tests in validation_results['statistical_tests'].items():
                f.write(f"{hypothesis.upper()}:\n")
                for test_name, p_value in tests.items():
                    f.write(f"  {test_name}: p={p_value:.4f}\n")
                f.write("\n")
        
        print("\nFile salvati:")
        print("- h1_cloud_results.csv")
        print("- h2_zerotrust_results.csv")
        print("- h3_compliance_results.csv")
        print("- thesis_simulation_report.txt")
        print("- hypothesis_validation_results.png")

def main():
    """Funzione principale"""
    print("FRAMEWORK SIMULAZIONE - VERSIONE CORRETTA")
    print("========================================")
    
    sim = GDOSimulationFramework(num_organizations=15)
    analysis = sim.run_complete_simulation()
    validation_results = sim.validate_hypotheses_statistically(analysis)
    sim.generate_visualizations()
    sim.save_results_simple(analysis, validation_results)
    
    print("\n🎉 SIMULAZIONE COMPLETATA SENZA ERRORI!")

if __name__ == "__main__":
    main()
