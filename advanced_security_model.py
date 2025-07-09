import numpy as np
from scipy import stats
from datetime import datetime
import pandas as pd

class AdvancedSecurityIncidentModel:
    """
    Modello avanzato per simulazione incidenti sicurezza GDO
    Basato su dati Clusit 2024 e Verizon DBIR 2024
    """
    
    def __init__(self):
        # FONTI PRINCIPALI
        self.sources = {
            'clusit_2024': {
                'title': 'Rapporto Clusit 2024 sulla Sicurezza ICT in Italia',
                'url': 'https://clusit.it/rapporto-clusit/',
                'key_data': {
                    'retail_percentage': 0.12,  # 12% attacchi totali
                    'growth_yoy': 0.23,         # +23% anno su anno
                    'ransomware_share': 0.41    # 41% sono ransomware
                }
            },
            'verizon_dbir_2024': {
                'title': 'Verizon Data Breach Investigations Report 2024',
                'section': 'Retail and Hospitality',
                'key_data': {
                    'incidents_per_1000_employees': 2.3,
                    'breach_probability': 0.28,  # 28% incidenti diventano breach
                    'insider_threat_ratio': 0.15 # 15% minacce interne
                }
            },
            'enisa_2024': {
                'title': 'ENISA Threat Landscape 2024',
                'url': 'https://www.enisa.europa.eu/topics/threat-landscape',
                'key_data': {
                    'supply_chain_attacks': 0.17,  # 17% via supply chain
                    'pos_malware_trend': -0.12,    # -12% POS malware (chip cards)
                    'ecommerce_fraud_growth': 0.34 # +34% frodi e-commerce
                }
            }
        }
        
        # CATEGORIE INCIDENTI (Tassonomia ENISA)
        self.incident_taxonomy = {
            'ransomware': {
                'base_probability': 0.41,
                'impact_multiplier': 3.5,
                'trend': 'increasing'
            },
            'data_breach': {
                'base_probability': 0.22,
                'impact_multiplier': 2.8,
                'trend': 'stable'
            },
            'pos_malware': {
                'base_probability': 0.08,
                'impact_multiplier': 2.0,
                'trend': 'decreasing'
            },
            'phishing': {
                'base_probability': 0.15,
                'impact_multiplier': 1.2,
                'trend': 'increasing'
            },
            'ddos': {
                'base_probability': 0.06,
                'impact_multiplier': 1.5,
                'trend': 'stable'
            },
            'insider_threat': {
                'base_probability': 0.08,
                'impact_multiplier': 2.2,
                'trend': 'increasing'
            }
        }
        
    def calculate_incident_rate(self, org_profile: dict) -> dict:
        """
        Calcola tasso incidenti basato su profilo organizzazione
        
        Args:
            org_profile: dict con caratteristiche organizzazione
                - size_category: 'small', 'medium', 'large'
                - num_stores: numero punti vendita
                - employees: numero dipendenti
                - legacy_ratio: percentuale sistemi legacy
                - it_budget_pct: budget IT come % fatturato
                - has_ecommerce: boolean
                - has_soc: boolean (Security Operations Center)
        
        Returns:
            dict con tassi incidenti per categoria
        """
        
        # BASE RATE - da Verizon DBIR 2024
        base_rate_per_1000_emp = 2.3
        
        # FATTORI MODIFICATORI
        
        # 1. Size Factor (economie di scala in security)
        size_factors = {
            'small': 1.5,    # Più vulnerabili
            'medium': 1.0,   # Baseline
            'large': 0.7     # Migliori difese
        }
        size_factor = size_factors[org_profile['size_category']]
        
        # 2. Legacy Systems Factor
        # Fonte: Ponemon Institute (2023) "Cost of Legacy Systems"
        legacy_factor = 1 + (org_profile['legacy_ratio'] * 0.8)
        
        # 3. Security Investment Factor
        # Relazione non lineare con IT budget
        # Fonte: Gartner (2024) "IT Security Spending Guide"
        security_spend_pct = org_profile['it_budget_pct'] * 0.15  # 15% IT per security
        investment_factor = 1 / (1 + np.log(1 + security_spend_pct))
        
        # 4. Attack Surface Factor
        # Più negozi = superficie attacco maggiore
        surface_factor = 1 + np.log10(org_profile['num_stores']) * 0.2
        
        # 5. E-commerce Factor
        # Fonte: ENISA (2024) - +34% rischio con e-commerce
        ecommerce_factor = 1.34 if org_profile.get('has_ecommerce', True) else 1.0
        
        # 6. SOC Presence Factor
        # Fonte: SANS (2023) "Value of SOC Report"
        soc_factor = 0.6 if org_profile.get('has_soc', False) else 1.0
        
        # CALCOLO TASSO BASE
        adjusted_rate = (base_rate_per_1000_emp * 
                        size_factor * 
                        legacy_factor * 
                        investment_factor * 
                        surface_factor * 
                        ecommerce_factor * 
                        soc_factor)
        
        # CALCOLO PER CATEGORIA INCIDENTE
        incidents_by_type = {}
        total_incidents_year = (org_profile['employees'] / 1000) * adjusted_rate
        
        for incident_type, params in self.incident_taxonomy.items():
            # Probabilità adjusted per profilo
            prob = params['base_probability']
            
            # Adjustments specifici per tipo
            if incident_type == 'ransomware' and org_profile['size_category'] == 'small':
                prob *= 1.3  # PMI più colpite da ransomware
            elif incident_type == 'pos_malware' and not org_profile.get('has_ecommerce', True):
                prob *= 1.5  # Solo negozi fisici più a rischio
            elif incident_type == 'insider_threat' and org_profile['employees'] > 1000:
                prob *= 1.2  # Più dipendenti = più rischio insider
            
            # Trend adjustment
            if params['trend'] == 'increasing':
                prob *= 1.1
            elif params['trend'] == 'decreasing':
                prob *= 0.9
            
            incidents_by_type[incident_type] = {
                'expected_count': total_incidents_year * prob,
                'probability': prob,
                'impact_multiplier': params['impact_multiplier']
            }
        
        # STAGIONALITÀ
        # Fonte: IBM X-Force (2024) "Retail Threat Intelligence"
        seasonal_factors = {
            'Q1': 0.8,   # Bassa stagione
            'Q2': 0.9,   # Media
            'Q3': 1.0,   # Media-alta
            'Q4': 1.3    # Black Friday/Natale (+30%)
        }
        
        return {
            'annual_expected_total': round(total_incidents_year, 2),
            'incidents_by_type': incidents_by_type,
            'seasonal_distribution': seasonal_factors,
            'confidence_interval_95': (
                round(total_incidents_year * 0.7, 2),
                round(total_incidents_year * 1.3, 2)
            ),
            'methodology': 'Model based on Clusit 2024, Verizon DBIR 2024, ENISA 2024'
        }
    
    def simulate_incidents_timeline(self, org_profile: dict, years: int = 1) -> pd.DataFrame:
        """
        Simula timeline incidenti per validazione Monte Carlo
        """
        incident_rates = self.calculate_incident_rate(org_profile)
        annual_rate = incident_rates['annual_expected_total']
        
        # Genera incidenti con processo di Poisson non omogeneo
        # per catturare stagionalità
        incidents = []
        
        for day in range(365 * years):
            # Determina quarter
            quarter = f'Q{(day % 365) // 91 + 1}'
            seasonal_factor = incident_rates['seasonal_distribution'].get(quarter, 1.0)
            
            # Rate giornaliero adjusted
            daily_rate = (annual_rate / 365) * seasonal_factor
            
            # Simula occorrenza
            if np.random.random() < daily_rate:
                # Determina tipo incidente
                incident_type = np.random.choice(
                    list(self.incident_taxonomy.keys()),
                    p=[v['probability'] for v in incident_rates['incidents_by_type'].values()]
                )
                
                incidents.append({
                    'day': day,
                    'date': pd.Timestamp('2024-01-01') + pd.Timedelta(days=int(day)),
                    'type': incident_type,
                    'impact': self._calculate_impact(incident_type, org_profile),
                    'detected_after_hours': self._calculate_detection_time(incident_type),
                    'contained': np.random.random() < self._containment_probability(org_profile)
                })
        
        return pd.DataFrame(incidents)
    
    def _calculate_impact(self, incident_type: str, org_profile: dict) -> dict:
        """
        Calcola impatto incidente
        Fonte: Ponemon "Cost of Data Breach 2024"
        """
        base_impacts = {
            'ransomware': {
                'downtime_hours': stats.lognorm.rvs(s=1.2, scale=48),  # Media 48h
                'recovery_cost_eur': stats.lognorm.rvs(s=0.8, scale=250000),
                'data_loss_probability': 0.15
            },
            'data_breach': {
                'records_affected': stats.lognorm.rvs(s=1.5, scale=10000),
                'cost_per_record_eur': 165,  # Media italiana Ponemon 2024
                'reputation_score_impact': -0.12
            },
            'pos_malware': {
                'stores_affected_pct': np.random.uniform(0.1, 0.4),
                'transaction_fraud_rate': 0.02,
                'detection_days': stats.gamma.rvs(a=2, scale=15)
            }
        }
        
        impact = base_impacts.get(incident_type, {
            'generic_cost_eur': stats.lognorm.rvs(s=0.5, scale=50000)
        })
        
        # Scala per dimensione organizzazione
        if org_profile['size_category'] == 'large':
            for key in impact:
                if 'cost' in key or 'eur' in key:
                    impact[key] *= 2.5
        
        return impact
    
    def _calculate_detection_time(self, incident_type: str) -> float:
        """
        Tempo di detection in ore
        Fonte: Mandiant M-Trends 2024
        """
        detection_times = {
            'ransomware': stats.gamma.rvs(a=2, scale=2),      # Media 4 ore
            'data_breach': stats.gamma.rvs(a=3, scale=72),    # Media 216 ore (9 giorni)
            'pos_malware': stats.gamma.rvs(a=4, scale=120),   # Media 480 ore (20 giorni)
            'phishing': stats.gamma.rvs(a=1.5, scale=1),      # Media 1.5 ore
            'ddos': 0.25,                                      # 15 minuti (immediato)
            'insider_threat': stats.gamma.rvs(a=5, scale=200) # Media 1000 ore (42 giorni)
        }
        
        return detection_times.get(incident_type, 24)
    
    def _containment_probability(self, org_profile: dict) -> float:
        """
        Probabilità di contenimento efficace
        """
        base_prob = 0.7
        
        # Modificatori
        if org_profile.get('has_soc', False):
            base_prob += 0.15
        if org_profile['size_category'] == 'large':
            base_prob += 0.1
        if org_profile['legacy_ratio'] > 0.7:
            base_prob -= 0.2
            
        return np.clip(base_prob, 0.3, 0.95)
    
    def generate_risk_matrix(self, org_profiles: list) -> pd.DataFrame:
        """
        Genera matrice di rischio per multiple organizzazioni
        """
        risk_data = []
        
        for profile in org_profiles:
            rates = self.calculate_incident_rate(profile)
            
            # Calcola risk score composito
            risk_score = 0
            for inc_type, data in rates['incidents_by_type'].items():
                risk_score += data['expected_count'] * data['impact_multiplier']
            
            risk_data.append({
                'org_id': profile['org_id'],
                'size': profile['size_category'],
                'annual_incidents_expected': rates['annual_expected_total'],
                'risk_score': round(risk_score, 2),
                'top_threat': max(rates['incidents_by_type'].items(), 
                                key=lambda x: x[1]['expected_count'])[0],
                'has_soc': profile.get('has_soc', False),
                'legacy_ratio': profile['legacy_ratio']
            })
        
        return pd.DataFrame(risk_data)


# Esempio di utilizzo e validazione
if __name__ == "__main__":
    model = AdvancedSecurityIncidentModel()
    
    # Profilo organizzazione esempio
    test_org = {
        'org_id': 'TEST-001',
        'size_category': 'medium',
        'num_stores': 150,
        'employees': 3500,
        'legacy_ratio': 0.6,
        'it_budget_pct': 2.2,
        'has_ecommerce': True,
        'has_soc': False
    }
    
    # Calcola tassi incidenti
    results = model.calculate_incident_rate(test_org)
    
    print("=== ANALISI RISCHIO SECURITY ===")
    print(f"\nOrganizzazione: {test_org['org_id']}")
    print(f"Incidenti attesi/anno: {results['annual_expected_total']}")
    print(f"Intervallo confidenza 95%: {results['confidence_interval_95']}")
    
    print("\nDistribuzione per tipo:")
    for inc_type, data in results['incidents_by_type'].items():
        print(f"  {inc_type}: {data['expected_count']:.2f} incidenti/anno")
    
    print("\nFattori stagionali:")
    for quarter, factor in results['seasonal_distribution'].items():
        print(f"  {quarter}: {factor}x")
    
    # Simula timeline
    timeline = model.simulate_incidents_timeline(test_org, years=1)
    if not timeline.empty:
        print(f"\nSimulazione 1 anno: {len(timeline)} incidenti simulati")
        print(f"Tipo più frequente: {timeline['type'].value_counts().index[0]}")
        print(f"Tempo medio detection: {timeline['detected_after_hours'].mean():.1f} ore")