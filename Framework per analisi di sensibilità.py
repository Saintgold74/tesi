# Framework per analisi di sensibilità GIST
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns
from SALib.sample import saltelli
from SALib.analyze import sobol
import warnings
warnings.filterwarnings('ignore')

class GISTSensitivityAnalysis:
    def __init__(self):
        # Parametri baseline
        self.params_baseline = {
            'neg_mu': 4.2,        # Log-normale negozi
            'neg_sigma': 0.8,
            'trans_mu': 1500,     # Transazioni/giorno
            'trans_sigma': 400,
            'weibull_beta': 2.1,  # Affidabilità
            'weibull_eta': 8760,
            'cost_min': 0.015,    # Costi IT (% fatturato)
            'cost_mode': 0.02,
            'cost_max': 0.035
        }
        
        # Pesi GIST
        self.gist_weights = {
            'physical': 0.15,
            'architectural': 0.35,
            'security': 0.30,
            'compliance': 0.20
        }
        
    def simulate_gist(self, neg_mu=None, neg_sigma=None, trans_mu=None, 
                     trans_sigma=None, weibull_beta=None, weibull_eta=None,
                     cost_min=None, cost_mode=None, cost_max=None):
        """Simula il calcolo del GIST score con i parametri dati"""
        
        # Usa parametri baseline se non specificati
        params = self.params_baseline.copy()
        local_vars = locals()
        for key in params.keys():
            if local_vars.get(key) is not None:
                params[key] = local_vars[key]
        
        # Simula componenti GIST
        np.random.seed(42)  # Per riproducibilità
        
        # Physical score (basato su affidabilità)
        reliability = 1 - (1 / params['weibull_eta']) ** params['weibull_beta']
        physical = min(0.4 + 0.6 * reliability, 1.0)
        
        # Architectural score (basato su scala e modernità)
        num_stores = np.exp(params['neg_mu'])
        scale_factor = min(num_stores / 100, 1.0)  # Normalizza a 100 negozi
        architectural = 0.3 + 0.5 * scale_factor + 0.2 * np.random.rand()
        
        # Security score (inversamente correlato a transazioni - più transazioni = più rischio)
        security_risk = params['trans_mu'] / 3000  # Normalizza a 3000 trans/giorno
        security = max(0.9 - 0.3 * security_risk, 0.4)
        
        # Compliance score (inversamente correlato a costi IT)
        cost_factor = (params['cost_mode'] - params['cost_min']) / (params['cost_max'] - params['cost_min'])
        compliance = 0.4 + 0.5 * (1 - cost_factor)
        
        # Calcola GIST score
        gist = (self.gist_weights['physical'] * physical +
                self.gist_weights['architectural'] * architectural +
                self.gist_weights['security'] * security +
                self.gist_weights['compliance'] * compliance)
        
        return gist
    
    def run_oat_analysis(self):
        """Esegue analisi di sensibilità one-at-a-time"""
        results = {}
        
        # Per ogni parametro
        for param_name, baseline_value in self.params_baseline.items():
            # Varia il parametro ±30%
            variations = np.linspace(0.7 * baseline_value, 
                                   1.3 * baseline_value, 
                                   20)
            
            outcomes = []
            for var_value in variations:
                # Crea dizionario parametri con variazione
                params_dict = self.params_baseline.copy()
                params_dict[param_name] = var_value
                
                # Esegui simulazione
                gist_score = self.simulate_gist(**params_dict)
                outcomes.append(gist_score)
            
            # Calcola elasticità
            x_norm = (variations - baseline_value) / baseline_value * 100  # Variazione %
            y_norm = (np.array(outcomes) - outcomes[10]) / outcomes[10] * 100  # Variazione % da baseline
            
            # Regressione lineare per elasticità
            elasticity = np.polyfit(x_norm, y_norm, 1)[0]
            
            results[param_name] = {
                'variations': variations,
                'outcomes': outcomes,
                'elasticity': elasticity,
                'x_norm': x_norm,
                'y_norm': y_norm
            }
        
        return results
    
    def plot_oat_results(self, results):
        """Visualizza risultati analisi OAT"""
        fig, axes = plt.subplots(3, 3, figsize=(15, 12))
        axes = axes.ravel()
        
        param_names_readable = {
            'neg_mu': 'Media Log(Negozi)',
            'neg_sigma': 'Dev.Std. Log(Negozi)',
            'trans_mu': 'Transazioni/Giorno',
            'trans_sigma': 'Dev.Std. Transazioni',
            'weibull_beta': 'Parametro Forma Weibull',
            'weibull_eta': 'Parametro Scala Weibull',
            'cost_min': 'Costo IT Min (%)',
            'cost_mode': 'Costo IT Tipico (%)',
            'cost_max': 'Costo IT Max (%)'
        }
        
        for idx, (param, data) in enumerate(results.items()):
            ax = axes[idx]
            
            # Plot
            ax.plot(data['x_norm'], data['y_norm'], 'b-', linewidth=2)
            ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
            ax.axvline(x=0, color='gray', linestyle='--', alpha=0.5)
            
            # Formattazione
            ax.set_title(f'{param_names_readable[param]}\nElasticità: {data["elasticity"]:.3f}')
            ax.set_xlabel('Variazione parametro (%)')
            ax.set_ylabel('Variazione GIST (%)')
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def run_sobol_analysis(self, n_samples=1024):
        """Esegue analisi Sobol per sensibilità globale"""
        from SALib.sample import saltelli
        from SALib.analyze import sobol
        
        # Definisci il problema per SALib
        problem = {
            'num_vars': 9,
            'names': list(self.params_baseline.keys()),
            'bounds': [[0.7*v, 1.3*v] for v in self.params_baseline.values()]
        }
        
        # Genera campioni usando Saltelli
        param_values = saltelli.sample(problem, n_samples)
        
        # Esegui simulazioni
        Y = np.zeros(param_values.shape[0])
        for i, params in enumerate(param_values):
            params_dict = dict(zip(problem['names'], params))
            Y[i] = self.simulate_gist(**params_dict)
        
        # Analizza con Sobol
        Si = sobol.analyze(problem, Y)
        
        return Si, problem
    
    def plot_sobol_results(self, Si, problem):
        """Visualizza indici di Sobol"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        param_names_short = ['Neg μ', 'Neg σ', 'Trans μ', 'Trans σ', 
                            'Weib β', 'Weib η', 'Cost min', 'Cost mode', 'Cost max']
        
        # First-order indices
        indices = Si['S1']
        sorted_idx = np.argsort(indices)[::-1]
        
        ax1.bar(range(len(indices)), indices[sorted_idx])
        ax1.set_xticks(range(len(indices)))
        ax1.set_xticklabels([param_names_short[i] for i in sorted_idx], rotation=45)
        ax1.set_ylabel('Indice di Sobol (Primo Ordine)')
        ax1.set_title('Effetti Principali')
        ax1.grid(True, alpha=0.3)
        
        # Total indices
        indices_total = Si['ST']
        
        ax2.bar(range(len(indices_total)), indices_total[sorted_idx])
        ax2.set_xticks(range(len(indices_total)))
        ax2.set_xticklabels([param_names_short[i] for i in sorted_idx], rotation=45)
        ax2.set_ylabel('Indice di Sobol (Totale)')
        ax2.set_title('Effetti Totali (con interazioni)')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def run_scenario_analysis(self):
        """Analisi scenari estremi ma realistici"""
        scenarios = {
            'Pessimista': {
                'neg_mu': 3.8,         # Meno negozi
                'neg_sigma': 1.0,      # Alta variabilità
                'trans_mu': 1000,      # Basse transazioni
                'trans_sigma': 500,    # Alta variabilità
                'weibull_beta': 1.5,   # Più guasti
                'weibull_eta': 6000,   # Vita più breve
                'cost_min': 0.02,      # Costi più alti
                'cost_mode': 0.03,
                'cost_max': 0.045
            },
            'Base': self.params_baseline,
            'Ottimista': {
                'neg_mu': 4.6,         # Più negozi
                'neg_sigma': 0.6,      # Bassa variabilità
                'trans_mu': 2000,      # Alte transazioni
                'trans_sigma': 300,    # Bassa variabilità
                'weibull_beta': 2.5,   # Meno guasti
                'weibull_eta': 12000,  # Vita più lunga
                'cost_min': 0.01,      # Costi più bassi
                'cost_mode': 0.015,
                'cost_max': 0.025
            }
        }
        
        results = {}
        
        for scenario_name, params in scenarios.items():
            # Esegui 1000 simulazioni per scenario con variabilità
            outcomes = []
            for _ in range(1000):
                # Aggiungi un po' di rumore per simulare incertezza
                noisy_params = params.copy()
                for key in noisy_params:
                    noisy_params[key] *= np.random.normal(1, 0.05)  # ±5% rumore
                
                gist = self.simulate_gist(**noisy_params)
                outcomes.append(gist)
            
            outcomes = np.array(outcomes)
            
            results[scenario_name] = {
                'mean': np.mean(outcomes),
                'std': np.std(outcomes),
                'min': np.min(outcomes),
                'max': np.max(outcomes),
                'p05': np.percentile(outcomes, 5),
                'p95': np.percentile(outcomes, 95),
                'prob_above_07': np.mean(outcomes > 0.7) * 100
            }
        
        return results
    
    def create_tornado_plot(self, oat_results):
        """Crea tornado plot per sensibilità"""
        # Calcola impatti per ±20% variazione
        impacts = []
        
        for param, data in oat_results.items():
            baseline_idx = len(data['variations']) // 2
            baseline_gist = data['outcomes'][baseline_idx]
            
            # Trova indici per ±20%
            idx_minus = int(len(data['variations']) * 0.3)  # -20% è al 30% dell'array
            idx_plus = int(len(data['variations']) * 0.7)   # +20% è al 70% dell'array
            
            impact_minus = data['outcomes'][idx_minus] - baseline_gist
            impact_plus = data['outcomes'][idx_plus] - baseline_gist
            
            impacts.append({
                'param': param,
                'impact_minus': impact_minus,
                'impact_plus': impact_plus,
                'total_impact': abs(impact_plus) + abs(impact_minus)
            })
        
        # Ordina per impatto totale
        impacts.sort(key=lambda x: x['total_impact'], reverse=True)
        
        # Crea plot
        fig, ax = plt.subplots(figsize=(10, 6))
        
        y_pos = np.arange(len(impacts))
        baseline = 0.7  # GIST baseline approssimativo
        
        for i, impact in enumerate(impacts):
            # Barra negativa
            ax.barh(i, impact['impact_minus'], left=baseline, 
                   color='red', alpha=0.7, label='Diminuzione -20%' if i == 0 else '')
            # Barra positiva
            ax.barh(i, impact['impact_plus'], left=baseline,
                   color='green', alpha=0.7, label='Aumento +20%' if i == 0 else '')
        
        ax.set_yticks(y_pos)
        ax.set_yticklabels([imp['param'] for imp in impacts])
        ax.set_xlabel('GIST Score')
        ax.set_title('Tornado Plot - Analisi di Sensibilità (±20% variazione)')
        ax.axvline(x=baseline, color='black', linestyle='--', alpha=0.5, label='Baseline')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig

# Esecuzione principale
if __name__ == "__main__":
    print("Inizializzazione analisi di sensibilità GIST...")
    analyzer = GISTSensitivityAnalysis()
    
    # 1. Analisi One-at-a-Time
    print("\n1. Esecuzione analisi One-at-a-Time...")
    oat_results = analyzer.run_oat_analysis()
    fig_oat = analyzer.plot_oat_results(oat_results)
    plt.savefig('oat_sensitivity.png', dpi=300, bbox_inches='tight')
    print("   - Salvato: oat_sensitivity.png")
    
    # 2. Tornado Plot
    print("\n2. Creazione Tornado Plot...")
    fig_tornado = analyzer.create_tornado_plot(oat_results)
    plt.savefig('tornado_plot.png', dpi=300, bbox_inches='tight')
    print("   - Salvato: tornado_plot.png")
    
    # 3. Analisi Sobol (richiede SALib)
    try:
        print("\n3. Esecuzione analisi Sobol...")
        Si, problem = analyzer.run_sobol_analysis(n_samples=512)
        fig_sobol = analyzer.plot_sobol_results(Si, problem)
        plt.savefig('sobol_indices.png', dpi=300, bbox_inches='tight')
        print("   - Salvato: sobol_indices.png")
        
        # Stampa risultati Sobol
        print("\n   Indici di Sobol (Primo Ordine):")
        for i, name in enumerate(problem['names']):
            print(f"   - {name}: {Si['S1'][i]:.3f}")
        
        print("\n   Contributo effetti di interazione: {:.1f}%".format(
            (1 - np.sum(Si['S1'])) * 100))
    except ImportError:
        print("\n3. SALib non installata. Installare con: pip install SALib")
        print("   Saltando analisi Sobol...")
    
    # 4. Analisi Scenari
    print("\n4. Esecuzione analisi scenari...")
    scenario_results = analyzer.run_scenario_analysis()
    
    # Crea tabella riassuntiva
    print("\n5. Risultati Analisi Scenari:")
    print("-" * 70)
    print(f"{'Scenario':<15} {'Media':<10} {'Std Dev':<10} {'P(GIST>0.7)':<15} {'5° perc':<10} {'95° perc':<10}")
    print("-" * 70)
    
    for scenario, results in scenario_results.items():
        print(f"{scenario:<15} {results['mean']:<10.3f} {results['std']:<10.3f} "
              f"{results['prob_above_07']:<15.1f}% {results['p05']:<10.3f} {results['p95']:<10.3f}")
    
    print("-" * 70)
    
    # Mostra tutti i grafici
    plt.show()
    
    print("\nAnalisi completata!")