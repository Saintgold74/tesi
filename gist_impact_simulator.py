import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple
import seaborn as sns

class GISTImpactSimulator:
    """
    Simula l'impatto dell'implementazione GIST sulle metriche GDO
    Basato su letteratura e case studies reali di Zero Trust implementations
    """
    
    def __init__(self):
        # FONTI E RIFERIMENTI PER IMPROVEMENT FACTORS
        self.improvement_references = {
            'forrester_2023': {
                'title': 'The Total Economic Impact of Zero Trust',
                'publisher': 'Forrester Research',
                'year': 2023,
                'key_findings': {
                    'breach_reduction': 0.50,  # -50% probabilità breach
                    'incident_response_time': 0.65,  # -65% tempo risposta
                    'compliance_improvement': 0.30  # +30% compliance score
                }
            },
            'gartner_2024': {
                'title': 'Market Guide for Zero Trust Network Access',
                'publisher': 'Gartner',
                'year': 2024,
                'key_findings': {
                    'availability_improvement': 0.0045,  # Da 99.5% a 99.95%
                    'mttr_reduction': 0.60,  # -60% MTTR
                    'operational_efficiency': 0.25  # +25% efficienza
                }
            },
            'microsoft_2023': {
                'title': 'Zero Trust Adoption Report 2023',
                'url': 'https://www.microsoft.com/security/blog/zero-trust-adoption-report/',
                'key_findings': {
                    'ransomware_impact_reduction': 0.72,  # -72% impatto ransomware
                    'insider_threat_reduction': 0.45,  # -45% insider threats
                    'patch_deployment_acceleration': 0.55  # -55% tempo patch
                }
            }
        }
        
        # COMPONENTI GIST E LORO IMPATTI
        self.gist_components = {
            'zero_trust_architecture': {
                'description': 'Implementazione architettura Zero Trust',
                'impacts': {
                    'security_incidents': -0.45,  # -45% incidenti
                    'lateral_movement': -0.80,    # -80% movimento laterale
                    'compliance_gdpr': +0.20,     # +20% GDPR score
                    'compliance_nis2': +0.25      # +25% NIS2 readiness
                }
            },
            'continuous_authentication': {
                'description': 'Autenticazione continua e adattiva',
                'impacts': {
                    'insider_threats': -0.50,     # -50% minacce insider
                    'account_takeover': -0.75,    # -75% account compromise
                    'compliance_pci': +0.15,      # +15% PCI compliance
                    'user_friction': +0.10        # +10% friction (negativo)
                }
            },
            'micro_segmentation': {
                'description': 'Micro-segmentazione della rete',
                'impacts': {
                    'blast_radius': -0.85,        # -85% raggio esplosione
                    'ransomware_spread': -0.90,   # -90% diffusione ransomware
                    'network_visibility': +0.60,  # +60% visibilità
                    'complexity': +0.20           # +20% complessità
                }
            },
            'automated_response': {
                'description': 'Risposta automatizzata agli incidenti',
                'impacts': {
                    'mttr': -0.65,                # -65% MTTR
                    'human_error': -0.40,         # -40% errori umani
                    'availability': +0.004,       # +0.4% availability
                    'false_positives': +0.15      # +15% falsi positivi iniziali
                }
            },
            'supply_chain_security': {
                'description': 'Sicurezza della supply chain',
                'impacts': {
                    'third_party_breaches': -0.60,  # -60% breach da terze parti
                    'compliance_nis2': +0.30,       # +30% NIS2 (requisito chiave)
                    'vendor_management_cost': +0.25, # +25% costi gestione
                    'onboarding_time': +0.20        # +20% tempo onboarding
                }
            }
        }
        
        # FASI DI IMPLEMENTAZIONE
        self.implementation_phases = {
            'phase1_foundation': {
                'duration_months': 6,
                'components': ['zero_trust_architecture'],
                'maturity_multiplier': 0.4  # 40% dei benefici
            },
            'phase2_identity': {
                'duration_months': 4,
                'components': ['continuous_authentication'],
                'maturity_multiplier': 0.6  # 60% dei benefici
            },
            'phase3_network': {
                'duration_months': 6,
                'components': ['micro_segmentation'],
                'maturity_multiplier': 0.7  # 70% dei benefici
            },
            'phase4_automation': {
                'duration_months': 4,
                'components': ['automated_response'],
                'maturity_multiplier': 0.8  # 80% dei benefici
            },
            'phase5_ecosystem': {
                'duration_months': 4,
                'components': ['supply_chain_security'],
                'maturity_multiplier': 1.0  # 100% dei benefici
            }
        }
    
    def calculate_gist_impact(self, baseline_metrics: dict, 
                            implementation_level: str = 'full') -> dict:
        """
        Calcola l'impatto di GIST sulle metriche baseline
        
        Args:
            baseline_metrics: Metriche pre-GIST
            implementation_level: 'basic', 'intermediate', 'full'
        
        Returns:
            Metriche post-GIST con miglioramenti
        """
        
        # Determina componenti implementati
        if implementation_level == 'basic':
            active_components = ['zero_trust_architecture']
            implementation_factor = 0.3
        elif implementation_level == 'intermediate':
            active_components = ['zero_trust_architecture', 
                               'continuous_authentication',
                               'micro_segmentation']
            implementation_factor = 0.7
        else:  # full
            active_components = list(self.gist_components.keys())
            implementation_factor = 1.0
        
        # Copia metriche baseline
        improved_metrics = baseline_metrics.copy()
        improvement_details = {}
        
        # 1. SECURITY INCIDENTS
        incident_reduction = 0
        for component in active_components:
            if 'security_incidents' in self.gist_components[component]['impacts']:
                incident_reduction += self.gist_components[component]['impacts']['security_incidents']
        
        incident_reduction = min(incident_reduction * implementation_factor, -0.75)  # Cap at -75%
        improved_metrics['security_incidents_year'] = int(
            baseline_metrics['security_incidents_year'] * (1 + incident_reduction)
        )
        improvement_details['security_incidents_reduction'] = f"{-incident_reduction:.0%}"
        
        # 2. AVAILABILITY
        availability_improvement = 0
        for component in active_components:
            if 'availability' in self.gist_components[component]['impacts']:
                availability_improvement += self.gist_components[component]['impacts']['availability']
        
        # Logarithmic improvement (harder to improve already high availability)
        current_availability = baseline_metrics['availability_pct']
        max_availability = 99.99
        improvement_potential = max_availability - current_availability
        
        improved_availability = current_availability + (improvement_potential * 
                                                      availability_improvement * 
                                                      implementation_factor)
        improved_metrics['availability_pct'] = round(min(improved_availability, max_availability), 3)
        improvement_details['availability_improvement'] = f"+{improved_availability - current_availability:.2f}%"
        
        # 3. MTTR
        mttr_reduction = 0
        for component in active_components:
            if 'mttr' in self.gist_components[component]['impacts']:
                mttr_reduction += self.gist_components[component]['impacts']['mttr']
        
        mttr_reduction = min(mttr_reduction * implementation_factor, -0.70)  # Cap at -70%
        improved_metrics['mttr_hours'] = round(
            baseline_metrics['mttr_hours'] * (1 + mttr_reduction), 1
        )
        improvement_details['mttr_reduction'] = f"{-mttr_reduction:.0%}"
        
        # 4. COMPLIANCE SCORES
        for compliance_type in ['gdpr', 'pci', 'nis2']:
            compliance_key = f'compliance_{compliance_type}'
            baseline_key = f'{compliance_type}_compliance'
            
            if baseline_key in baseline_metrics:
                improvement = 0
                for component in active_components:
                    if compliance_key in self.gist_components[component]['impacts']:
                        improvement += self.gist_components[component]['impacts'][compliance_key]
                
                # Diminishing returns for already high compliance
                current_score = baseline_metrics[baseline_key]
                improvement_adjusted = improvement * (1 - current_score) * implementation_factor
                
                improved_score = min(current_score + improvement_adjusted, 0.95)  # Cap at 95%
                improved_metrics[baseline_key] = round(improved_score, 3)
                improvement_details[f'{compliance_type}_improvement'] = f"+{(improved_score - current_score)*100:.1f}%"
        
        # 5. PATCH LAG
        patch_improvement = 0.40 * implementation_factor  # -40% con full implementation
        improved_metrics['patch_lag_days'] = int(
            baseline_metrics['patch_lag_days'] * (1 - patch_improvement)
        )
        improvement_details['patch_lag_reduction'] = f"-{patch_improvement:.0%}"
        
        # 6. CALCOLO ROI
        roi_calculation = self._calculate_roi(baseline_metrics, improved_metrics, 
                                            implementation_level)
        
        return {
            'baseline_metrics': baseline_metrics,
            'improved_metrics': improved_metrics,
            'improvement_details': improvement_details,
            'implementation_level': implementation_level,
            'active_components': active_components,
            'roi_analysis': roi_calculation
        }
    
    def _calculate_roi(self, baseline: dict, improved: dict, 
                      implementation_level: str) -> dict:
        """
        Calcola ROI dell'implementazione GIST
        Basato su TCO analysis e risk reduction
        """
        
        # COSTI IMPLEMENTAZIONE (basati su Forrester TEI methodology)
        base_costs = {
            'basic': {
                'initial_investment': 250_000,
                'annual_operating': 50_000,
                'training': 30_000
            },
            'intermediate': {
                'initial_investment': 600_000,
                'annual_operating': 120_000,
                'training': 75_000
            },
            'full': {
                'initial_investment': 1_200_000,
                'annual_operating': 200_000,
                'training': 150_000
            }
        }
        
        costs = base_costs[implementation_level]
        
        # Scala per dimensione organizzazione (revenue-based)
        if 'annual_revenue_meur' in baseline:
            revenue = baseline['annual_revenue_meur']
            if revenue < 500:
                scale_factor = 0.6
            elif revenue < 1500:
                scale_factor = 1.0
            else:
                scale_factor = 1.5
        else:
            scale_factor = 1.0
        
        # Costi scalati
        total_cost_year1 = (costs['initial_investment'] + 
                          costs['annual_operating'] + 
                          costs['training']) * scale_factor
        annual_cost_ongoing = costs['annual_operating'] * scale_factor
        
        # BENEFICI QUANTIFICATI
        
        # 1. Riduzione costi incidenti
        incident_cost_per = 85_000  # Costo medio incidente GDO (Ponemon 2024)
        incidents_prevented = (baseline['security_incidents_year'] - 
                             improved['security_incidents_year'])
        incident_savings = incidents_prevented * incident_cost_per
        
        # 2. Riduzione downtime
        availability_improvement = improved['availability_pct'] - baseline['availability_pct']
        # Assumendo 2M€ revenue/giorno per organizzazione media
        daily_revenue = baseline.get('annual_revenue_meur', 1000) * 1e6 / 365
        downtime_cost_per_day = daily_revenue * 0.5  # 50% revenue loss durante downtime
        
        downtime_days_saved = (availability_improvement / 100) * 365
        downtime_savings = downtime_days_saved * downtime_cost_per_day
        
        # 3. Riduzione costi compliance
        compliance_penalty_risk = baseline.get('expected_sanctions_eur', 200_000)
        compliance_improvement = np.mean([
            improved.get('gdpr_compliance', 0.7) - baseline.get('gdpr_compliance', 0.7),
            improved.get('pci_compliance', 0.7) - baseline.get('pci_compliance', 0.7),
            improved.get('nis2_compliance', 0.5) - baseline.get('nis2_compliance', 0.5)
        ])
        compliance_savings = compliance_penalty_risk * compliance_improvement
        
        # 4. Efficienza operativa
        mttr_improvement = (baseline['mttr_hours'] - improved['mttr_hours']) / baseline['mttr_hours']
        operational_savings = 150_000 * mttr_improvement  # Basato su costi team IT
        
        # CALCOLO ROI
        total_annual_benefits = (incident_savings + downtime_savings + 
                               compliance_savings + operational_savings)
        
        roi_year1 = ((total_annual_benefits - total_cost_year1) / 
                    total_cost_year1) * 100
        
        roi_3year = ((total_annual_benefits * 3 - total_cost_year1 - annual_cost_ongoing * 2) /
                    (total_cost_year1 + annual_cost_ongoing * 2)) * 100
        
        payback_months = (total_cost_year1 / (total_annual_benefits / 12)) if total_annual_benefits > 0 else 999
        
        return {
            'implementation_cost_year1': round(total_cost_year1),
            'annual_operating_cost': round(annual_cost_ongoing),
            'annual_benefits': {
                'incident_prevention': round(incident_savings),
                'downtime_reduction': round(downtime_savings),
                'compliance_improvement': round(compliance_savings),
                'operational_efficiency': round(operational_savings),
                'total': round(total_annual_benefits)
            },
            'roi_year1_pct': round(roi_year1, 1),
            'roi_3year_pct': round(roi_3year, 1),
            'payback_months': round(payback_months, 1),
            'benefit_cost_ratio': round(total_annual_benefits / total_cost_year1, 2)
        }
    
    def simulate_phased_implementation(self, baseline_metrics: dict, 
                                     duration_months: int = 24) -> pd.DataFrame:
        """
        Simula implementazione per fasi nel tempo
        """
        results = []
        current_metrics = baseline_metrics.copy()
        
        month = 0
        for phase_name, phase_details in self.implementation_phases.items():
            # Periodo pre-implementazione fase
            phase_duration = phase_details['duration_months']
            
            for m in range(phase_duration):
                month += 1
                if month > duration_months:
                    break
                
                # Graduale improvement durante la fase
                progress = (m + 1) / phase_duration
                maturity = phase_details['maturity_multiplier'] * progress
                
                # Applica improvements parziali
                phase_metrics = self._apply_phase_improvements(
                    current_metrics, 
                    phase_details['components'],
                    maturity
                )
                
                results.append({
                    'month': month,
                    'phase': phase_name,
                    'phase_progress': round(progress * 100),
                    'availability_pct': phase_metrics['availability_pct'],
                    'security_incidents_monthly': phase_metrics['security_incidents_year'] / 12,
                    'mttr_hours': phase_metrics['mttr_hours'],
                    'compliance_score': np.mean([
                        phase_metrics.get('gdpr_compliance', 0.7),
                        phase_metrics.get('pci_compliance', 0.7),
                        phase_metrics.get('nis2_compliance', 0.5)
                    ])
                })
                
            current_metrics = phase_metrics
            
            if month >= duration_months:
                break
        
        return pd.DataFrame(results)
    
    def _apply_phase_improvements(self, current_metrics: dict, 
                                components: list, maturity: float) -> dict:
        """
        Applica miglioramenti di una fase specifica
        """
        improved = current_metrics.copy()
        
        for component in components:
            impacts = self.gist_components[component]['impacts']
            
            # Applica impacts con maturity factor
            if 'security_incidents' in impacts:
                factor = 1 + (impacts['security_incidents'] * maturity)
                improved['security_incidents_year'] = int(
                    current_metrics['security_incidents_year'] * factor
                )
            
            if 'availability' in impacts:
                improved['availability_pct'] = min(
                    current_metrics['availability_pct'] + impacts['availability'] * maturity,
                    99.99
                )
            
            if 'mttr' in impacts:
                factor = 1 + (impacts['mttr'] * maturity)
                improved['mttr_hours'] = current_metrics['mttr_hours'] * factor
        
        return improved
    
    def generate_comparison_report(self, organization_data: pd.DataFrame) -> dict:
        """
        Genera report comparativo per tutte le organizzazioni
        """
        results = []
        
        for _, org in organization_data.iterrows():
            baseline = {
                'org_id': org['org_id'],
                'size_category': org['size_category'],
                'annual_revenue_meur': org['annual_revenue_meur'],
                'security_incidents_year': org['baseline_security_incidents_year'],
                'availability_pct': org['baseline_availability_pct'],
                'mttr_hours': org['baseline_mttr_hours'],
                'gdpr_compliance': org['baseline_gdpr_compliance'],
                'pci_compliance': org['baseline_pci_compliance'],
                'nis2_compliance': org['baseline_nis2_readiness'],
                'patch_lag_days': org['baseline_patch_lag_days']
            }
            
            # Determina livello implementazione per size
            if org['size_category'] == 'small':
                impl_level = 'basic'
            elif org['size_category'] == 'medium':
                impl_level = 'intermediate'
            else:
                impl_level = 'full'
            
            impact = self.calculate_gist_impact(baseline, impl_level)
            
            results.append({
                'org_id': org['org_id'],
                'size_category': org['size_category'],
                'implementation_level': impl_level,
                'incidents_reduction_pct': float(impact['improvement_details']['security_incidents_reduction'].strip('%')),
                'availability_improvement_pp': impact['improved_metrics']['availability_pct'] - baseline['availability_pct'],
                'mttr_reduction_pct': float(impact['improvement_details']['mttr_reduction'].strip('%')),
                'roi_year1_pct': impact['roi_analysis']['roi_year1_pct'],
                'payback_months': impact['roi_analysis']['payback_months'],
                'annual_benefits_eur': impact['roi_analysis']['annual_benefits']['total']
            })
        
        return pd.DataFrame(results)
    
    def visualize_improvements(self, baseline_data: pd.DataFrame, 
                             improved_data: pd.DataFrame):
        """
        Crea visualizzazioni before/after
        """
        fig, axes = plt.subplots(2, 3, figsize=(16, 10))
        fig.suptitle('Impatto GIST Framework - Analisi Before/After', fontsize=16)
        
        # 1. Security Incidents Reduction
        ax1 = axes[0, 0]
        categories = ['Small', 'Medium', 'Large']
        
        baseline_incidents = baseline_data.groupby('size_category')['baseline_security_incidents_year'].mean()
        improved_incidents = improved_data.groupby('size_category')['improved_security_incidents_year'].mean()
        
        x = np.arange(len(categories))
        width = 0.35
        
        ax1.bar(x - width/2, baseline_incidents, width, label='Baseline', color='#E53935')
        ax1.bar(x + width/2, improved_incidents, width, label='Post-GIST', color='#43A047')
        ax1.set_xlabel('Categoria')
        ax1.set_ylabel('Incidenti/Anno')
        ax1.set_title('Riduzione Incidenti Sicurezza')
        ax1.set_xticks(x)
        ax1.set_xticklabels(categories)
        ax1.legend()
        
        # Aggiungi percentuali riduzione
        for i, (cat, base, imp) in enumerate(zip(categories, baseline_incidents, improved_incidents)):
            reduction = (base - imp) / base * 100
            ax1.text(i, max(base, imp) + 2, f'-{reduction:.0f}%', ha='center', fontweight='bold')
        
        # 2. Availability Improvement
        ax2 = axes[0, 1]
        
        baseline_avail = baseline_data.groupby('size_category')['baseline_availability_pct'].mean()
        improved_avail = improved_data.groupby('size_category')['improved_availability_pct'].mean()
        
        # Grafico a linee per mostrare piccoli cambiamenti
        ax2.plot(categories, baseline_avail, 'o-', label='Baseline', markersize=10, linewidth=2)
        ax2.plot(categories, improved_avail, 's-', label='Post-GIST', markersize=10, linewidth=2)
        ax2.set_xlabel('Categoria')
        ax2.set_ylabel('Availability (%)')
        ax2.set_title('Miglioramento Disponibilità')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim(99.0, 100.0)  # Zoom su range rilevante
        
        # 3. MTTR Reduction
        ax3 = axes[0, 2]
        
        baseline_mttr = baseline_data.groupby('size_category')['baseline_mttr_hours'].mean()
        improved_mttr = improved_data.groupby('size_category')['improved_mttr_hours'].mean()
        
        ax3.bar(x - width/2, baseline_mttr, width, label='Baseline', color='#E53935')
        ax3.bar(x + width/2, improved_mttr, width, label='Post-GIST', color='#43A047')
        ax3.set_xlabel('Categoria')
        ax3.set_ylabel('MTTR (ore)')
        ax3.set_title('Riduzione Tempo di Ripristino')
        ax3.set_xticks(x)
        ax3.set_xticklabels(categories)
        ax3.legend()
        
        # 4. Compliance Score Improvement (Radar Chart simulato)
        ax4 = axes[1, 0]
        
        # Media compliance scores
        compliance_types = ['GDPR', 'PCI-DSS', 'NIS2']
        baseline_compliance = [
            baseline_data['baseline_gdpr_compliance'].mean(),
            baseline_data['baseline_pci_compliance'].mean(),
            baseline_data['baseline_nis2_readiness'].mean()
        ]
        improved_compliance = [
            improved_data['improved_gdpr_compliance'].mean(),
            improved_data['improved_pci_compliance'].mean(),
            improved_data['improved_nis2_readiness'].mean()
        ]
        
        x_comp = np.arange(len(compliance_types))
        ax4.bar(x_comp - width/2, baseline_compliance, width, label='Baseline', color='#FFA726')
        ax4.bar(x_comp + width/2, improved_compliance, width, label='Post-GIST', color='#26A69A')
        ax4.set_xlabel('Framework')
        ax4.set_ylabel('Compliance Score')
        ax4.set_title('Miglioramento Compliance')
        ax4.set_xticks(x_comp)
        ax4.set_xticklabels(compliance_types)
        ax4.legend()
        ax4.set_ylim(0, 1)
        
        # 5. ROI Analysis
        ax5 = axes[1, 1]
        
        roi_data = improved_data.groupby('size_category')['roi_year1_pct'].mean()
        colors = ['#FF7043', '#FFA726', '#66BB6A']
        bars = ax5.bar(categories, roi_data, color=colors)
        ax5.set_xlabel('Categoria')
        ax5.set_ylabel('ROI Anno 1 (%)')
        ax5.set_title('Return on Investment')
        ax5.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        
        # Aggiungi valori sulle barre
        for bar, roi in zip(bars, roi_data):
            height = bar.get_height()
            ax5.text(bar.get_x() + bar.get_width()/2., height + 5,
                    f'{roi:.0f}%', ha='center', va='bottom', fontweight='bold')
        
        # 6. Timeline Implementation
        ax6 = axes[1, 2]
        
        # Simula timeline per organizzazione media
        sample_org = baseline_data[baseline_data['size_category'] == 'medium'].iloc[0]
        timeline = self.simulate_phased_implementation(
            sample_org.to_dict(), 
            duration_months=24
        )
        
        ax6.plot(timeline['month'], timeline['availability_pct'], label='Availability %')
        ax6.set_xlabel('Mesi')
        ax6.set_ylabel('Availability %')
        ax6.set_title('Timeline Implementazione (Org. Media)')
        ax6.grid(True, alpha=0.3)
        
        # Aggiungi fasi
        phase_colors = plt.cm.Set3(np.linspace(0, 1, 5))
        for i, (phase, group) in enumerate(timeline.groupby('phase')):
            ax6.axvspan(group['month'].min(), group['month'].max(), 
                       alpha=0.2, color=phase_colors[i], 
                       label=phase.replace('_', ' ').title())
        
        ax6.legend(loc='lower right', fontsize=8)
        
        plt.tight_layout()
        return fig


# Test e dimostrazione
if __name__ == "__main__":
    simulator = GISTImpactSimulator()
    
    # Test con organizzazione singola
    test_baseline = {
        'org_id': 'TEST-001',
        'size_category': 'medium',
        'annual_revenue_meur': 850,
        'security_incidents_year': 45,
        'availability_pct': 99.35,
        'mttr_hours': 6.5,
        'gdpr_compliance': 0.72,
        'pci_compliance': 0.68,
        'nis2_compliance': 0.45,
        'patch_lag_days': 85,
        'expected_sanctions_eur': 180_000
    }
    
    # Calcola impatto
    results = simulator.calculate_gist_impact(test_baseline, 'intermediate')
    
    print("=== GIST IMPACT ANALYSIS ===")
    print(f"\nOrganizzazione: {test_baseline['org_id']}")
    print(f"Livello Implementazione: {results['implementation_level']}")
    
    print("\nMIGLIORAMENTI CHIAVE:")
    for metric, improvement in results['improvement_details'].items():
        print(f"  {metric}: {improvement}")
    
    print("\nANALISI ROI:")
    roi = results['roi_analysis']
    print(f"  Costo Implementazione Anno 1: €{roi['implementation_cost_year1']:,}")
    print(f"  Benefici Annuali: €{roi['annual_benefits']['total']:,}")
    print(f"  ROI Anno 1: {roi['roi_year1_pct']:.1f}%")
    print(f"  ROI 3 Anni: {roi['roi_3year_pct']:.1f}%")
    print(f"  Payback: {roi['payback_months']:.1f} mesi")
    
    print("\nBREAKDOWN BENEFICI:")
    for benefit, value in roi['annual_benefits'].items():
        if benefit != 'total':
            print(f"  {benefit}: €{value:,}")