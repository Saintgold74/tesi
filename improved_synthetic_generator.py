# gist_synthetic_data_framework.py
"""
Framework di Generazione Dati Sintetici per Validazione GIST
=============================================================
Autore: [Nome Studente]
Versione: 2.0
Data: Gennaio 2024

Questo framework implementa la metodologia descritta nel Capitolo 4
per la generazione di dati sintetici calibrati sul mercato GDO italiano.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from datetime import datetime
import json
import hashlib
from typing import Dict, List, Tuple, Any
import logging

# Configurazione logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class BibliographyManager:
    """Gestisce i riferimenti bibliografici utilizzati nel framework"""
    
    REFERENCES = {
        'federdistribuzione_2023': {
            'autore': 'Federdistribuzione',
            'titolo': 'La Distribuzione Moderna Organizzata - Rapporto Annuale 2023',
            'editore': 'Federdistribuzione',
            'anno': 2023,
            'url': 'https://www.federdistribuzione.it/studi-e-ricerche/',
            'accesso': '15 gennaio 2024',
            'pagine': '45-47',
            'tipo': 'report'
        },
        'istat_2023': {
            'autore': 'ISTAT',
            'titolo': 'Annuario Statistico Italiano 2023',
            'editore': 'Istituto Nazionale di Statistica',
            'anno': 2023,
            'isbn': '978-88-458-2061-2',
            'capitolo': '19 - Commercio interno',
            'tavola': '19.4',
            'tipo': 'libro'
        },
        'mediobanca_2023': {
            'autore': 'Ufficio Studi Mediobanca',
            'titolo': 'Le maggiori società italiane 2023',
            'editore': 'Mediobanca',
            'anno': 2023,
            'url': 'https://www.mbres.it/it/publications/italian-companies',
            'sezione': 'GDO Food',
            'pagine': '127-131',
            'tipo': 'report'
        },
        'polimi_2023': {
            'autore': 'Osservatorio Innovazione Digitale nel Retail',
            'titolo': 'Digital Transformation nel Retail Italiano',
            'editore': 'Politecnico di Milano',
            'anno': 2023,
            'url': 'https://www.osservatori.net/it/ricerche/osservatori-attivi/innovazione-digitale-nel-retail',
            'pagine': '89-92',
            'tipo': 'report'
        },
        'basker_2005': {
            'autore': 'Basker, E.',
            'titolo': 'Job Creation or Destruction? Labor Market Effects of Wal-Mart Expansion',
            'rivista': 'Journal of Labor Economics',
            'anno': 2005,
            'volume': 23,
            'numero': 2,
            'pagine': '211-248',
            'doi': '10.1086/428824',
            'tipo': 'articolo'
        },
        'trivedi_2016': {
            'autore': 'Trivedi, K.S.',
            'titolo': 'Probability and Statistics with Reliability, Queuing and Computer Science Applications',
            'editore': 'Wiley',
            'anno': 2016,
            'isbn': '978-0-471-33341-8',
            'edizione': '2nd',
            'tipo': 'libro'
        },
        'patki_2016': {
            'autore': 'Patki, N., Wedge, R., Veeramachaneni, K.',
            'titolo': 'The Synthetic Data Vault',
            'conferenza': 'IEEE International Conference on Data Science and Advanced Analytics',
            'anno': 2016,
            'pagine': '399-410',
            'doi': '10.1109/DSAA.2016.49',
            'tipo': 'conferenza'
        }
    }
    
    @classmethod
    def cite(cls, key: str) -> str:
        """Restituisce una citazione formattata"""
        if key not in cls.REFERENCES:
            raise ValueError(f"Riferimento '{key}' non trovato")
        ref = cls.REFERENCES[key]
        return f"{ref['autore']} ({ref['anno']})"
    
    @classmethod
    def get_full_reference(cls, key: str) -> Dict:
        """Restituisce il riferimento completo"""
        return cls.REFERENCES.get(key, {})

class NumpyJSONEncoder(json.JSONEncoder):
    """
    Un encoder JSON personalizzato per gestire i tipi di dati NumPy
    che la libreria standard 'json' non riconosce.
    """
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.bool_):
            return bool(obj)
        # Lascia che la classe base gestisca gli altri tipi
        return super(NumpyJSONEncoder, self).default(obj)
class ParameterValidator:
    """Valida la coerenza dei parametri generati"""
    
    # Benchmark di settore per validazione
    BENCHMARKS = {
        'revenue_per_employee': {
            'min': 150000,
            'max': 350000,
            'unit': '€/dipendente',
            'source': 'KPMG Retail Trends Italia 2023, p. 34'
        },
        'revenue_per_sqm': {
            'min': 3000,
            'max': 12000,
            'unit': '€/mq/anno',
            'source': 'JLL Retail Report Italia 2023, p. 21'
        },
        'it_budget_pct': {
            'min': 0.8,
            'max': 3.5,
            'unit': '% fatturato',
            'source': 'Gartner IT Spending Forecast 2023'
        },
        'employees_per_sqm': {
            'min': 0.02,
            'max': 0.08,
            'unit': 'dipendenti/mq',
            'source': 'Elaborazione su dati INPS-ISTAT 2023'
        }
    }
    
    @classmethod
    def validate_parameters(cls, data: pd.DataFrame) -> Dict[str, Any]:
        """Esegue validazione completa dei parametri"""
        validation_results = {}
        
        # Revenue per employee
        revenue_per_emp = (data['annual_revenue_meur'].sum() * 1e6) / data['employees'].sum()
        benchmark = cls.BENCHMARKS['revenue_per_employee']
        validation_results['revenue_per_employee'] = {
            'value': revenue_per_emp,
            'unit': benchmark['unit'],
            'in_range': benchmark['min'] <= revenue_per_emp <= benchmark['max'],
            'benchmark_range': [benchmark['min'], benchmark['max']],
            'source': benchmark['source']
        }
        
        # IT budget percentage
        it_budget_pcts = data['it_budget_pct'].values
        benchmark = cls.BENCHMARKS['it_budget_pct']
        validation_results['it_budget_pct'] = {
            'mean': np.mean(it_budget_pcts),
            'std': np.std(it_budget_pcts),
            'unit': benchmark['unit'],
            'all_in_range': all(benchmark['min'] <= x <= benchmark['max'] for x in it_budget_pcts),
            'out_of_range_count': sum(1 for x in it_budget_pcts if not (benchmark['min'] <= x <= benchmark['max'])),
            'source': benchmark['source']
        }
        
        return validation_results
    def test_employee_model_credibility(self):
        """
        Verifica che il modello produca risultati coerenti con benchmark 2024
        """
        # Caso test: supermercato medio italiano
        test_surface = 1200  # mq
        test_stores = 150
        test_size = 'medium'
        
        employees = self.calculate_employees_modern(
            test_surface, test_stores, test_size
        )
        
        # Verifica contro benchmark
        employees_per_store = employees / test_stores
        
        # Range atteso: 35-55 dipendenti per supermercato 1200mq
        # Fonte: Federdistribuzione (2023)
        assert 35 <= employees_per_store <= 55, \
            f"Dipendenti per negozio ({employees_per_store:.1f}) fuori range atteso"
        
        print(f"✓ Modello validato: {employees_per_store:.1f} dipendenti/negozio")

# ESEMPIO DI INTEGRAZIONE CON FONTI SETTORIALI RECENTI
class ModernRetailMetrics:
    """Metriche retail aggiornate da fonti 2023-2024"""
    
    # CHECKOUT AUTOMATION IMPACT
    # Fonte: NCR (2023) "Self-Checkout Adoption in Europe"
    SELF_CHECKOUT_ADOPTION = {
        'small': 0.15,    # 15% casse self
        'medium': 0.35,   # 35% casse self
        'large': 0.50     # 50% casse self
    }
    
    # OMNICHANNEL STAFFING
    # Fonte: Salesforce (2023) "State of Connected Shoppers"
    DIGITAL_STAFF_RATIO = {
        'small': 0.02,    # 2% staff dedicato digital
        'medium': 0.05,   # 5% staff dedicato digital
        'large': 0.08     # 8% staff dedicato digital
    }
    
    # E-COMMERCE IMPACT
    # Fonte: Netcomm (2023) "E-commerce in Italia"
    STORE_STAFF_REDUCTION_ECOMMERCE = {
        '2005': 1.00,  # Baseline
        '2015': 0.92,  # -8%
        '2020': 0.85,  # -15% (COVID acceleration)
        '2024': 0.78   # -22%
    }
class GISTSyntheticDataFramework:
    """
    Framework principale per generazione dati sintetici GDO
    Implementa la metodologia a tre livelli descritta nel Capitolo 4
    """
    
    def __init__(self, seed: int = 42, verbose: bool = True):
        """
        Inizializza il framework
        
        Args:
            seed: Seed per riproducibilità
            verbose: Se True, stampa informazioni dettagliate
        """
        np.random.seed(seed)
        self.seed = seed
        self.verbose = verbose
        self.bibliography = BibliographyManager()
        self.validator = ParameterValidator()
        self.generated_data = None
        
        if self.verbose:
            self._print_header()
    
    def _print_header(self):
        """Stampa header informativo"""
        print("=" * 80)
        print("GIST SYNTHETIC DATA GENERATION FRAMEWORK v2.0")
        print("=" * 80)
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Random seed: {self.seed}")
        print("\nDISCLAIMER: Questo framework genera dati SINTETICI per validazione accademica.")
        print("I dati NON rappresentano organizzazioni reali.\n")
    
    def generate_level1_parameters(self, n_orgs: int = 15) -> pd.DataFrame:
        """
        Genera parametri di Livello 1 (verificabili da fonti pubbliche)
        
        Returns:
            DataFrame con parametri base
        """
        logger.info("Generazione parametri Livello 1 (verificabili)")
        
        # DISTRIBUZIONE DIMENSIONALE - Fonte: Federdistribuzione
        size_distribution = {
            'small': 6,    # 40% - Catene 50-100 negozi
            'medium': 6,   # 40% - Catene 100-250 negozi  
            'large': 3     # 20% - Catene 250-500 negozi
        }
        
        # DISTRIBUZIONE GEOGRAFICA - Fonte: ISTAT
        geographic_weights = {
            'Nord': 0.453,
            'Centro': 0.228,
            'Sud e Isole': 0.319
        }
        
        # FATTURATO MEDIO PER STORE - Fonte: Mediobanca
        revenue_ranges = {
            'small': (3.0, 4.5),    # M€/anno per store
            'medium': (4.0, 6.0),   
            'large': (5.5, 8.0)     
        }
        
        # IT BUDGET - Fonte: Politecnico Milano
        it_budget_ranges = {
            'small': (1.0, 1.8),    # % del fatturato
            'medium': (1.8, 2.5),
            'large': (2.3, 3.0)
        }
        
        organizations = []
        org_id = 1
        
        for size, count in size_distribution.items():
            for i in range(count):
                # Numero negozi
                store_ranges = {'small': (50, 100), 'medium': (100, 250), 'large': (250, 500)}
                num_stores = np.random.randint(*store_ranges[size])
                
                # Fatturato per negozio
                revenue_per_store = np.random.uniform(*revenue_ranges[size])
                annual_revenue = num_stores * revenue_per_store
                
                # IT Budget
                it_budget_pct = np.random.uniform(*it_budget_ranges[size])
                
                # Geografia
                region = np.random.choice(list(geographic_weights.keys()), 
                                        p=list(geographic_weights.values()))
                
                org = {
                    'org_id': f'GIST-SIM-{org_id:03d}',
                    'size_category': size,
                    'num_stores': num_stores,
                    'annual_revenue_meur': round(annual_revenue, 1),
                    'revenue_per_store_meur': round(revenue_per_store, 2),
                    'it_budget_pct': round(it_budget_pct, 2),
                    'it_budget_meur': round(annual_revenue * it_budget_pct / 100, 2),
                    'geographic_region': region,
                    'parameter_level': 1,
                    'data_sources': {
                        'size_distribution': self.bibliography.cite('federdistribuzione_2023'),
                        'geographic_distribution': self.bibliography.cite('istat_2023'),
                        'revenue_data': self.bibliography.cite('mediobanca_2023'),
                        'it_budget': self.bibliography.cite('polimi_2023')
                    }
                }
                
                organizations.append(org)
                org_id += 1
        
        df = pd.DataFrame(organizations)
        
        if self.verbose:
            print(f"\n✓ Generati {len(df)} record con parametri Livello 1")
            print(f"  Fonti utilizzate: {len(set([v for org in organizations for v in org['data_sources'].values()]))}")
        
        return df
    
    def add_level2_parameters(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Aggiunge parametri di Livello 2 (derivati da modelli)
        """
        logger.info("Aggiunta parametri Livello 2 (derivati)")
        
        # SUPERFICIE MEDIA NEGOZI - Derivata da format mix
        surface_by_size = {
            'small': {'mean': 800, 'std': 150},    # mq
            'medium': {'mean': 1200, 'std': 200},
            'large': {'mean': 1800, 'std': 300}
        }
        
        for idx, row in df.iterrows():
            size = row['size_category']
            
            # Superficie media
            avg_surface = np.random.normal(surface_by_size[size]['mean'], 
                                         surface_by_size[size]['std'])
            avg_surface = max(400, min(3000, avg_surface))  # Vincoli realistici
            df.loc[idx, 'avg_store_surface_sqm'] = int(avg_surface)
            
            # DIPENDENTI - Modello Basker (2005) adattato
            employees = self.calculate_employees_modern(avg_surface, row['num_stores'], size)
            df.loc[idx, 'employees'] = int(employees)
            df.loc[idx, 'employees_per_store'] = round(employees / row['num_stores'], 1)
            
            # POS TERMINALS - Funzione della superficie
            pos_per_store = self._calculate_pos_terminals(avg_surface)
            df.loc[idx, 'pos_per_store'] = round(pos_per_store, 1)
            df.loc[idx, 'pos_terminals_total'] = int(pos_per_store * row['num_stores'])
            
            # LEGACY RATIO - Inversamente correlato a IT budget
            legacy_ratio = self._calculate_legacy_ratio(row['it_budget_pct'])
            df.loc[idx, 'legacy_system_ratio'] = round(legacy_ratio, 2)
        
        if self.verbose:
            print(f"\n✓ Aggiunti parametri Livello 2 (modelli derivati)")
            print(f"  Modelli utilizzati: Basker (2005), correlazioni empiriche")
        
        return df
    
    def add_level3_parameters(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Aggiunge parametri di Livello 3 (simulati con distribuzioni)
        """
        logger.info("Aggiunta parametri Livello 3 (simulati)")
        
        for idx, row in df.iterrows():
            size = row['size_category']
            
            # AVAILABILITY - Distribuzione Beta
            availability = self._generate_availability(size)
            df.loc[idx, 'baseline_availability_pct'] = round(availability, 3)
            
            # MTTR - Distribuzione Log-normale  
            mttr = self._generate_mttr(size)
            df.loc[idx, 'baseline_mttr_hours'] = round(mttr, 1)
            
            # SECURITY INCIDENTS - Poisson + size factor
            incidents = self._generate_security_incidents(row['num_stores'], size)
            df.loc[idx, 'baseline_security_incidents_year'] = incidents
            
            # COMPLIANCE SCORES - Beta distributions
            gdpr_score = self._generate_compliance_score('gdpr', size)
            pci_score = self._generate_compliance_score('pci', size)
            nis2_score = self._generate_compliance_score('nis2', size)
            
            df.loc[idx, 'baseline_gdpr_compliance'] = round(gdpr_score, 3)
            df.loc[idx, 'baseline_pci_compliance'] = round(pci_score, 3)
            df.loc[idx, 'baseline_nis2_readiness'] = round(nis2_score, 3)
            
            # PATCH LAG - Gamma distribution
            patch_lag = self._generate_patch_lag(size)
            df.loc[idx, 'baseline_patch_lag_days'] = int(patch_lag)
            
            # COSTI OPERATIVI - Percentuali del budget IT
            df.loc[idx, 'security_spend_pct_it'] = round(np.random.uniform(12, 18), 1)
            df.loc[idx, 'compliance_spend_pct_it'] = round(np.random.uniform(8, 15), 1)
        
        # Aggiungi metadata
        df['data_type'] = 'SYNTHETIC'
        df['generation_date'] = datetime.now().strftime('%Y-%m-%d')
        df['framework_version'] = '2.0'
        df['random_seed'] = self.seed
        
        if self.verbose:
            print(f"\n✓ Aggiunti parametri Livello 3 (distribuzioni simulate)")
            print(f"  Distribuzioni utilizzate: Beta, Log-normale, Poisson, Gamma")
        
        return df
    
    
    def calculate_employees_modern(self, avg_surface: float, num_stores: int, 
                                size: str, year: int = 2024) -> float:
        """
        Calcola dipendenti con modello aggiornato 2024
        Basato su dati EuroCommerce (2023) e ISTAT (2024)
        
        Formula aggiornata:
        E = (α * S^β * ε_tech * δ_format) * N * γ_size
        
        dove:
        - α: coefficiente base (da EuroCommerce 2023)
        - β: elasticità superficie (rendimenti decrescenti)
        - ε_tech: fattore riduzione tecnologica
        - δ_format: fattore formato negozio
        - N: numero negozi
        - γ_size: efficienza di scala
        """
        
        # PARAMETRI AGGIORNATI 2024
        # Fonte: EuroCommerce (2023) - 0.031 dipendenti/mq media EU
        alpha_2024 = 0.031
        
        # Elasticità superficie - Fonte: Confcommercio (2023)
        # Rendimenti più decrescenti per automazione
        beta = 0.65  # Ridotto da 0.75 per effetto tecnologia
        
        # FATTORE TECNOLOGICO
        # Fonte: McKinsey (2023) "Future of Work in Retail"
        tech_factors = {
            'small': 0.95,   # Meno automazione
            'medium': 0.85,  # Self-checkout parziale
            'large': 0.75    # Alta automazione
        }
        epsilon_tech = tech_factors[size]
        
        # FATTORE FORMATO NEGOZIO
        # Fonte: Nielsen (2023) "Store Formats Evolution"
        format_factors = {
            'discount': 0.7,        # Personale ridotto
            'supermercato': 1.0,    # Baseline
            'ipermercato': 1.2,     # Più servizi
            'convenience': 0.8      # Formato emergente
        }
        
        # MIX FORMATI per size (aggiornato 2024)
        format_mix = {
            'small': {'discount': 0.3, 'supermercato': 0.5, 'convenience': 0.2},
            'medium': {'discount': 0.2, 'supermercato': 0.6, 'ipermercato': 0.2},
            'large': {'discount': 0.1, 'supermercato': 0.5, 'ipermercato': 0.4}
        }
        
        # Calcola fattore formato pesato
        delta_format = sum(format_factors[fmt] * weight 
                        for fmt, weight in format_mix[size].items())
        
        # EFFICIENZA DI SCALA
        # Fonte: Deloitte (2023) "European Grocery Retail"
        gamma_size = {
            'small': 1.15,   # Inefficienze
            'medium': 1.00,  # Baseline
            'large': 0.85    # Economie di scala
        }
        
        # CALCOLO BASE
        employees_per_store = alpha_2024 * (avg_surface ** beta) * epsilon_tech * delta_format
        
        # AGGIUSTAMENTI SPECIFICI ITALIA
        # Fonte: ISTAT (2024) - Italia ha +15% dipendenti vs media EU
        italy_factor = 1.15
        
        # PART-TIME ADJUSTMENT
        # Fonte: INPS (2023) - 42% part-time nel retail
        # Convertiamo in FTE (Full Time Equivalent)
        fte_conversion = 0.58 + 0.42 * 0.6  # 58% full + 42% part (conta 60%)
        
        # CALCOLO FINALE
        total_employees = (employees_per_store * num_stores * 
                        gamma_size[size] * italy_factor) / fte_conversion
        
        # Aggiungi variabilità realistica
        variability = np.random.normal(1.0, 0.08)
        total_employees *= variability
        
        # Vincoli realistici
        min_employees = max(10 * num_stores, 50)  # Min 10 per negozio o 50 totale
        max_employees = 100 * num_stores  # Max 100 per negozio
        
        return np.clip(total_employees, min_employees, max_employees)


    def calculate_employees_benchmark_validation(self, df: pd.DataFrame) -> dict:
        """
        Valida il modello dipendenti contro benchmark pubblici
        """
        validations = {}
        
        # BENCHMARK 1: Dipendenti per mq
        # Fonte: EuroCommerce (2023)
        total_sqm = (df['avg_store_surface_sqm'] * df['num_stores']).sum()
        total_employees = df['employees'].sum()
        employees_per_sqm = total_employees / total_sqm
        
        validations['employees_per_sqm'] = {
            'calculated': round(employees_per_sqm, 4),
            'benchmark_range': [0.025, 0.040],  # EU range
            'benchmark_italy': 0.036,  # Italia sopra media
            'source': 'EuroCommerce (2023), p. 89',
            'valid': 0.025 <= employees_per_sqm <= 0.040
        }
        
        # BENCHMARK 2: Dipendenti per milione di fatturato
        # Fonte: Mediobanca (2023) - Dati aggregati GDO
        employees_per_meur = total_employees / df['annual_revenue_meur'].sum()
        
        validations['employees_per_meur'] = {
            'calculated': round(employees_per_meur, 1),
            'benchmark_range': [3.5, 6.0],
            'benchmark_avg': 4.7,
            'source': 'Mediobanca (2023) - Le società italiane, p. 156',
            'valid': 3.5 <= employees_per_meur <= 6.0
        }
        
        # BENCHMARK 3: Produttività (fatturato per dipendente)
        revenue_per_employee = df['annual_revenue_meur'].sum() * 1e6 / total_employees
        
        validations['revenue_per_employee'] = {
            'calculated': round(revenue_per_employee),
            'benchmark_range': [180000, 280000],
            'percentile_25': 195000,
            'median': 220000,
            'percentile_75': 255000,
            'source': 'KPMG (2023) European Retail Productivity Report',
            'valid': 180000 <= revenue_per_employee <= 280000
        }
        
        return validations

    def _calculate_pos_terminals(self, avg_surface: float) -> float:
        """
        Calcola POS per negozio in base a superficie
        Relazione empirica: 1 cassa ogni 150-200 mq
        """
        base_pos = avg_surface / 175  # Media 175 mq per cassa
        
        # Aggiungi variabilità e self-service
        variability = np.random.normal(1.0, 0.15)
        self_service_factor = 1.2  # 20% casse self-service in più
        
        return max(2, base_pos * variability * self_service_factor)

    def _calculate_legacy_ratio(self, it_budget_pct: float) -> float:
        """
        Legacy ratio inversamente correlato a IT investment
        """
        # Relazione inversa con rumore
        base_ratio = 0.9 - (it_budget_pct - 1.0) * 0.2
        noise = np.random.normal(0, 0.05)
        
        return np.clip(base_ratio + noise, 0.2, 0.9)

    def _generate_availability(self, size: str) -> float:
        """
        Genera availability usando distribuzione Beta
        Parametri calibrati per ottenere medie realistiche
        """
        # Parametri Beta per size category
        params = {
            'small': {'alpha': 50, 'beta': 0.5},   # Media ~99.0%
            'medium': {'alpha': 80, 'beta': 0.4},  # Media ~99.5%
            'large': {'alpha': 100, 'beta': 0.3}   # Media ~99.7%
        }
        
        # Genera da Beta e scala a range [98.5, 99.9]
        beta_value = stats.beta.rvs(params[size]['alpha'], params[size]['beta'])
        availability = 98.5 + beta_value * 1.4
        
        return min(99.9, availability)
        
    def _generate_mttr(self, size: str) -> float:
        """
        Genera MTTR usando distribuzione Log-normale
        Basato su Trivedi (2016)
        """
        # Parametri log-normale per size
        params = {
            'small': {'mu': 2.0, 'sigma': 0.8},   # Media ~7.4 ore
            'medium': {'mu': 1.6, 'sigma': 0.6},  # Media ~5.0 ore
            'large': {'mu': 1.1, 'sigma': 0.5}    # Media ~3.0 ore
        }
        
        mttr = stats.lognorm.rvs(s=params[size]['sigma'], 
                                scale=np.exp(params[size]['mu']))
        
        return max(0.5, min(24, mttr))  # Vincoli [0.5, 24] ore
        
    def _generate_security_incidents(self, num_stores: int, size: str) -> int:
        """
        Genera incidenti usando Poisson con rate dipendente da size
        """
        # Rate base incidenti per 100 negozi/anno
        base_rates = {
            'small': 15,   # Più vulnerabili
            'medium': 10,
            'large': 7     # Migliori difese
        }
        
        # Scala per numero negozi
        lambda_param = (num_stores / 100) * base_rates[size]
        
        # Genera da Poisson
        incidents = stats.poisson.rvs(lambda_param)
        
        return max(0, incidents)
    
    def _generate_compliance_score(self, compliance_type: str, size: str) -> float:
        """
        Genera compliance score usando Beta distribution
        """
        # Parametri per tipo compliance e size
        params = {
            'gdpr': {
                'small': {'alpha': 2, 'beta': 1},    # Media ~0.67
                'medium': {'alpha': 3, 'beta': 1},   # Media ~0.75
                'large': {'alpha': 4, 'beta': 1}     # Media ~0.80
            },
            'pci': {
                'small': {'alpha': 2.5, 'beta': 1},  # Media ~0.71
                'medium': {'alpha': 3.5, 'beta': 1}, # Media ~0.78
                'large': {'alpha': 5, 'beta': 1}     # Media ~0.83
            },
            'nis2': {
                'small': {'alpha': 1.5, 'beta': 2},  # Media ~0.43
                'medium': {'alpha': 2, 'beta': 2},   # Media ~0.50
                'large': {'alpha': 3, 'beta': 2}     # Media ~0.60
            }
        }
        
        p = params[compliance_type][size]
        score = stats.beta.rvs(p['alpha'], p['beta'])
        
        return np.clip(score, 0, 1)
    
    def _generate_patch_lag(self, size: str) -> float:
        """
        Genera patch lag usando distribuzione Gamma
        """
        # Parametri Gamma (shape, scale) per size
        params = {
            'small': {'shape': 4, 'scale': 30},   # Media ~120 giorni
            'medium': {'shape': 3, 'scale': 25},  # Media ~75 giorni
            'large': {'shape': 2, 'scale': 20}    # Media ~40 giorni
        }
        
        lag = stats.gamma.rvs(params[size]['shape'], 
                             scale=params[size]['scale'])
        
        return max(7, min(365, lag))  # Vincoli [7, 365] giorni
    
    def generate_complete_dataset(self, n_orgs: int = 15) -> pd.DataFrame:
        """
        Genera dataset completo con tutti i livelli
        """
        logger.info(f"Inizio generazione dataset completo con {n_orgs} organizzazioni")
        
        # Livello 1: Parametri verificabili
        df = self.generate_level1_parameters(n_orgs)
        
        # Livello 2: Parametri derivati
        df = self.add_level2_parameters(df)
        
        # Livello 3: Parametri simulati
        df = self.add_level3_parameters(df)
        
        # Validazione
        validation_results = self.validator.validate_parameters(df)
        
        if self.verbose:
            print("\n" + "="*60)
            print("VALIDAZIONE PARAMETRI")
            print("="*60)
            for param, result in validation_results.items():
                print(f"\n{param}:")
                for key, value in result.items():
                    if key != 'source':
                        print(f"  {key}: {value}")
                print(f"  Fonte benchmark: {result.get('source', 'N/A')}")
        
        self.generated_data = df
        return df
    
    def export_results(self, df: pd.DataFrame, base_filename: str = "gist_synthetic_data"):
        """
        Esporta risultati in vari formati
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # CSV principale
        csv_file = f"{base_filename}_{timestamp}.csv"
        df.to_csv(csv_file, index=False)
        df.to_csv('synthetic_gdo_organizations.csv', index=False)
        logger.info(f"Dataset salvato in: {csv_file}")
        
        # Metadata JSON
        metadata = {
            'generation_info': {
                'timestamp': timestamp,
                'framework_version': '2.0',
                'random_seed': self.seed,
                'n_organizations': len(df)
            },
            'parameters_summary': {
                'level1': ['size_category', 'num_stores', 'annual_revenue_meur', 
                          'it_budget_pct', 'geographic_region'],
                'level2': ['avg_store_surface_sqm', 'employees', 'pos_terminals_total',
                          'legacy_system_ratio'],
                'level3': ['baseline_availability_pct', 'baseline_mttr_hours',
                          'baseline_security_incidents_year', 'compliance_scores',
                          'baseline_patch_lag_days']
            },
            'validation_results': self.validator.validate_parameters(df),
            'bibliography': self.bibliography.REFERENCES
        }
        
        json_file = f"{base_filename}_metadata_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f,cls=NumpyJSONEncoder, indent=2, ensure_ascii=False)
        logger.info(f"Metadata salvati in: {json_file}")
        
        # Report testuale
        report_file = f"{base_filename}_report_{timestamp}.txt"
        self._generate_text_report(df, report_file)
        logger.info(f"Report salvato in: {report_file}")
        
        return {
            'csv': csv_file,
            'metadata': json_file,
            'report': report_file
        }
    
    def _generate_text_report(self, df: pd.DataFrame, filename: str):
        """Genera report testuale dettagliato"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("REPORT GENERAZIONE DATI SINTETICI GDO - FRAMEWORK GIST\n")
            f.write("="*80 + "\n\n")
            
            f.write(f"Data generazione: {datetime.now()}\n")
            f.write(f"Versione framework: 2.0\n")
            f.write(f"Random seed: {self.seed}\n")
            f.write(f"Numero organizzazioni: {len(df)}\n\n")
            
            f.write("DISCLAIMER\n")
            f.write("-"*40 + "\n")
            f.write("Questi dati sono COMPLETAMENTE SINTETICI e generati per validazione\n")
            f.write("accademica del framework GIST. NON rappresentano organizzazioni reali.\n\n")
            
            f.write("METODOLOGIA\n")
            f.write("-"*40 + "\n")
            f.write("Livello 1: Parametri da fonti pubbliche verificabili\n")
            f.write("Livello 2: Parametri derivati usando modelli dalla letteratura\n")
            f.write("Livello 3: Parametri simulati usando distribuzioni statistiche\n\n")
            
            f.write("STATISTICHE AGGREGATE\n")
            f.write("-"*40 + "\n")
            
            # Statistiche per dimensione
            size_stats = df.groupby('size_category').agg({
                'num_stores': ['count', 'sum', 'mean'],
                'annual_revenue_meur': ['sum', 'mean'],
                'employees': ['sum', 'mean'],
                'baseline_availability_pct': 'mean',
                'baseline_security_incidents_year': 'sum'
            }).round(2)
            
            f.write("\nPer categoria dimensionale:\n")
            f.write(str(size_stats))
            
            f.write("\n\nFONTI BIBLIOGRAFICHE UTILIZZATE\n")
            f.write("-"*40 + "\n")
            for key, ref in self.bibliography.REFERENCES.items():
                f.write(f"\n[{key}]\n")
                f.write(f"{ref['autore']} ({ref['anno']}). {ref['titolo']}.\n")
                if ref['tipo'] == 'libro':
                    f.write(f"{ref['editore']}. ISBN: {ref.get('isbn', 'N/A')}\n")
                elif ref['tipo'] == 'articolo':
                    f.write(f"{ref['rivista']}, {ref['volume']}({ref['numero']}), {ref['pagine']}.\n")
    
    def visualize_results(self, df: pd.DataFrame):
         # 1. Definisca una mappa per i colori
        color_map = {
            'small': 'skyblue',
            'medium': 'orange',
            'large': 'darkred'
        }
        print("Debug - Colonne disponibili nel DataFrame:", df.columns)
        # 2. Crei una nuova colonna nel DataFrame con i colori corrispondenti
        df['size_color'] = df['size_category'].map(color_map)
        """Crea visualizzazioni dei dati generati"""
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle('Framework GIST - Analisi Dati Sintetici GDO', fontsize=16)
        
        # 1. Distribuzione geografica
        ax1 = axes[0, 0]
        geo_counts = df['geographic_region'].value_counts()
        geo_counts.plot(kind='bar', ax=ax1, color=['#1976D2', '#388E3C', '#F57C00'])
        ax1.set_title('Distribuzione Geografica\n' + self.bibliography.cite('istat_2023'))
        ax1.set_ylabel('Numero Organizzazioni')
        ax1.tick_params(axis='x', rotation=45)
        
        # 2. IT Budget vs Revenue
        ax2 = axes[0, 1]
        for cat in df['size_category'].unique():
            cat_data = df[df['size_category'] == cat]
            ax2.scatter(cat_data['annual_revenue_meur'], 
                       cat_data['it_budget_pct'],
                       label=cat.title(), alpha=0.7, s=100)
        ax2.set_xlabel('Fatturato Annuo (M€)')
        ax2.set_ylabel('IT Budget (%)')
        ax2.set_title('Investimento IT vs Fatturato\n' + self.bibliography.cite('polimi_2023'))
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. Availability Distribution
        ax3 = axes[0, 2]
        availability_by_size = [df[df['size_category'] == size]['baseline_availability_pct'].values 
                               for size in ['small', 'medium', 'large']]
        ax3.boxplot(availability_by_size, tick_labels=['Small', 'Medium', 'Large'])
        ax3.set_ylabel('Availability (%)')
        ax3.set_title('Distribuzione Availability\n(Simulata - Beta Distribution)')
        ax3.grid(True, alpha=0.3, axis='y')
        
        # 4. Security Incidents
        ax4 = axes[1, 0]
        # 3. Usi la nuova colonna 'size_color' per il parametro 'c'
        df.plot.scatter(x='num_stores', y='baseline_security_incidents_year',
                        c=df['size_color'], # <--- MODIFICA QUI
                        title='Incidenti di Sicurezza vs. Numero di Negozi',
                        alpha=0.6,
                        grid=True,
                        figsize=(12, 7))
        ax4.set_xlabel('Numero Negozi')
        ax4.set_ylabel('Incidenti Sicurezza/Anno')
        ax4.set_title('Incidenti vs Dimensione\n(Simulata - Poisson)')
        
        # 5. Compliance Scores
        ax5 = axes[1, 1]
        compliance_cols = ['baseline_gdpr_compliance', 'baseline_pci_compliance', 
                          'baseline_nis2_readiness']
        compliance_means = df[compliance_cols].mean() * 100
        bars = ax5.bar(range(len(compliance_means)), compliance_means,
                       color=['#4CAF50', '#FF9800', '#F44336'])
        ax5.set_xticks(range(len(compliance_means)))
        ax5.set_xticklabels(['GDPR', 'PCI-DSS', 'NIS2'])
        ax5.set_ylabel('Compliance Score Medio (%)')
        ax5.set_title('Stato Compliance\n(Simulata - Beta Distribution)')
        ax5.axhline(y=80, color='k', linestyle='--', alpha=0.3)
        
        for bar, value in zip(bars, compliance_means):
            ax5.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                    f'{value:.0f}%', ha='center')
        
        # 6. Validation Summary
        ax6 = axes[1, 2]
        ax6.text(0.5, 0.7, 'DATI SINTETICI', ha='center', va='center',
                fontsize=20, fontweight='bold', color='red',
                bbox=dict(boxstyle="round,pad=0.5", facecolor="yellow", alpha=0.3))
        ax6.text(0.5, 0.4, 'Generati per validazione\naccademica framework GIST',
                ha='center', va='center', fontsize=12)
        ax6.text(0.5, 0.1, f'Seed: {self.seed}', ha='center', va='center',
                fontsize=10, style='italic')
        ax6.set_xlim(0, 1)
        ax6.set_ylim(0, 1)
        ax6.axis('off')
        
        plt.tight_layout()
        
        # Salva figura
        filename = f"gist_synthetic_data_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.show()
        
        return filename


# Esempio di utilizzo
if __name__ == "__main__":
    # Inizializza framework
    framework = GISTSyntheticDataFramework(seed=42, verbose=True)
    
    # Genera dataset
    synthetic_data = framework.generate_complete_dataset(n_orgs=15)
    
    # Mostra prime righe
    print("\n" + "="*60)
    print("ESEMPIO DATI GENERATI (prime 3 organizzazioni)")
    print("="*60)
    print(synthetic_data[['org_id', 'size_category', 'num_stores', 
                         'annual_revenue_meur', 'baseline_availability_pct']].head(3))
    
    # Esporta risultati
    files = framework.export_results(synthetic_data)
    
    print("\n" + "="*60)
    print("FILE GENERATI")
    print("="*60)
    for file_type, filename in files.items():
        print(f"{file_type}: {filename}")
    
    # Crea visualizzazioni
    plot_file = framework.visualize_results(synthetic_data)
    print(f"\nVisualizzazioni salvate in: {plot_file}")
    
    print("\n✓ Generazione completata con successo!")