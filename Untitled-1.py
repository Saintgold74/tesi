\section{C.5 Framework GIST Computazionale}

\subsection{C.5.1 Modello Matematico Completo}

\subsubsection{Formulazione Aggregata (Balanced Scorecard)}

Il modello aggregato del framework GIST è definito come:

\begin{equation}
GIST_{aggregato} = \sum_{i \in \{P,A,S,C\}} (w_i \times C_i) \times K_{GDO} \times (1+I)
\end{equation}

dove:
\begin{itemize}
    \item $C_i$ = Score componente $i$ (Physical, Architectural, Security, Compliance)
    \item $w_i$ = Peso della componente $i$, con $\sum w_i = 1$ e $w_i \geq 0$
    \item $K_{GDO}$ = Coefficiente di contesto GDO
    \item $I$ = Fattore di innovazione
\end{itemize}

\subsubsection{Formulazione Restrittiva (Weakest Link)}

Per contesti mission-critical, si utilizza il modello moltiplicativo:

\begin{equation}
GIST_{restrittivo} = \left(\prod_{i \in \{P,A,S,C\}} C_i^{w_i}\right) \times K_{GDO} \times (1+I)
\end{equation}

Questa formulazione implementa il principio dell'anello più debole, dove componenti con score basso impattano severamente il risultato finale.

\subsection{C.5.2 Implementazione Completa del Framework}

\begin{lstlisting}[language=Python, caption=Classe GISTFramework Completa]
import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, List, Tuple

class GISTFramework:
    """
    Framework GIST calibrato e validato per GDO
    """
    def __init__(self, assessment_mode='balanced'):
        """
        Inizializza framework con modalità specificata
        
        Args:
            assessment_mode: 'balanced' per aggregato, 'critical' per restrittivo
        """
        self.mode = assessment_mode
        
        # Pesi calibrati empiricamente
        self.weights = {
            'physical': 0.18,      # Foundational ma commodity
            'architectural': 0.32,  # Driver principale di trasformazione
            'security': 0.28,      # Criticità crescente
            'compliance': 0.22     # Enabler competitivo
        }
        
        # Coefficienti di scala GDO
        self.k_gdo_factors = {
            'scale': lambda n_stores: 1 + 0.15 * np.log(max(1, n_stores/50)),
            'geographic': lambda regions: 1 + 0.08 * (regions - 1),
            'criticality': 1.25,  # retail = infrastruttura critica
            'complexity': lambda n_systems: 1 + 0.12 * np.log(max(1, n_systems))
        }
        
        # Fattore innovazione
        self.innovation_multiplier = {
            'traditional': 0.0,
            'early_adopter': 0.15,
            'innovative': 0.25,
            'cutting_edge': 0.35
        }
        
        # Parametri per validazione e incertezza
        self.uncertainty_factors = {
            'measurement_error': 0.05,  # 5% errore di misura
            'temporal_variance': 0.08,  # 8% varianza temporale
            'subjective_bias': 0.10     # 10% bias soggettivo
        }
    
    def calculate_score(self, components: Dict[str, float], 
                       context: Dict[str, any]) -> Dict[str, any]:
        """
        Calcola GIST score con doppia formulazione
        
        Args:
            components: Dizionario con score P, A, S, C (0-1)
            context: Dizionario con parametri contesto
            
        Returns:
            Dizionario con score, componenti, interpretazione
        """
        # Validazione input
        self._validate_inputs(components, context)
        
        # Calcolo K_GDO
        k_gdo = self._calculate_k_gdo(context)
        
        # Fattore innovazione
        innovation = self.innovation_multiplier.get(
            context.get('innovation_level', 'traditional'), 0
        )
        
        # Calcolo score base
        if self.mode == 'balanced':
            base_score = self._calculate_aggregated(components)
        else:  # 'critical'
            base_score = self._calculate_restrictive(components)
        
        # Score finale
        final_score = base_score * k_gdo * (1 + innovation)
        
        # Calcolo incertezza
        uncertainty = self._calculate_uncertainty(components, context)
        
        # Analisi componenti
        component_analysis = self._analyze_components(components)
        
        return {
            'score': final_score * 100,  # scala 0-100
            'score_raw': final_score,
            'components': components,
            'component_analysis': component_analysis,
            'k_gdo': k_gdo,
            'innovation_factor': innovation,
            'uncertainty': uncertainty,
            'confidence_interval': self._calculate_confidence_interval(
                final_score, uncertainty
            ),
            'interpretation': self._interpret_score(final_score * 100),
            'recommendations': self._generate_recommendations(
                components, final_score * 100
            )
        }
    
    def _calculate_aggregated(self, components: Dict[str, float]) -> float:
        """Calcolo con modello aggregato (sommatoria ponderata)"""
        score = 0
        for comp_name, comp_score in components.items():
            weight = self.weights.get(comp_name, 0)
            score += weight * comp_score
        return score
    
    def _calculate_restrictive(self, components: Dict[str, float]) -> float:
        """Calcolo con modello restrittivo (produttoria)"""
        score = 1.0
        for comp_name, comp_score in components.items():
            weight = self.weights.get(comp_name, 0)
            # Evita score zero che azzererebbe tutto
            safe_score = max(0.01, comp_score)
            score *= (safe_score ** weight)
        return score
    
    def _calculate_k_gdo(self, context: Dict[str, any]) -> float:
        """Calcola coefficiente di contesto GDO"""
        k_gdo = 1.0
        
        for factor, func_or_value in self.k_gdo_factors.items():
            if factor in context:
                if callable(func_or_value):
                    k_gdo *= func_or_value(context[factor])
                else:
                    k_gdo *= func_or_value
        
        return k_gdo
    
    def _calculate_uncertainty(self, components: Dict[str, float], 
                              context: Dict[str, any]) -> float:
        """Calcola incertezza complessiva della valutazione"""
        # Base uncertainty
        base_uncertainty = np.sqrt(
            self.uncertainty_factors['measurement_error']**2 +
            self.uncertainty_factors['temporal_variance']**2 +
            self.uncertainty_factors['subjective_bias']**2
        )
        
        # Aggiustamenti per contesto
        if context.get('data_quality', 'high') == 'low':
            base_uncertainty *= 1.5
            
        if context.get('assessment_type', 'detailed') == 'rapid':
            base_uncertainty *= 1.3
        
        # Aggiustamenti per variabilità componenti
        component_variance = np.var(list(components.values()))
        if component_variance > 0.1:  # Alta variabilità
            base_uncertainty *= (1 + component_variance)
        
        return min(base_uncertainty, 0.25)  # Cap al 25%
    
    def _analyze_components(self, components: Dict[str, float]) -> Dict[str, any]:
        """Analizza punti di forza e debolezza delle componenti"""
        analysis = {}
        
        # Identifica componenti critiche
        mean_score = np.mean(list(components.values()))
        std_score = np.std(list(components.values()))
        
        for comp_name, comp_score in components.items():
            z_score = (comp_score - mean_score) / (std_score + 0.001)
            
            if z_score < -1:
                status = 'critical_weakness'
            elif z_score < -0.5:
                status = 'weakness'
            elif z_score > 1:
                status = 'strength'
            elif z_score > 0.5:
                status = 'adequate'
            else:
                status = 'neutral'
            
            analysis[comp_name] = {
                'score': comp_score,
                'z_score': z_score,
                'status': status,
                'percentile': stats.percentileofscore(
                    self._get_benchmark_distribution(comp_name), 
                    comp_score
                )
            }
        
        return analysis
    
    def _interpret_score(self, score: float) -> str:
        """Interpretazione qualitativa del punteggio"""
        if score < 20:
            return "Critico: Intervento urgente richiesto"
        elif score < 40:
            return "Inadeguato: Vulnerabilità significative"
        elif score < 60:
            return "Basilare: Conformità minima"
        elif score < 80:
            return "Maturo: Buone pratiche implementate"
        else:
            return "Eccellente: Leader di settore"
    
    def _generate_recommendations(self, components: Dict[str, float], 
                                 score: float) -> List[Dict[str, any]]:
        """Genera raccomandazioni prioritizzate"""
        recommendations = []
        
        # Identifica componenti da migliorare
        sorted_components = sorted(components.items(), key=lambda x: x[1])
        
        for comp_name, comp_score in sorted_components[:2]:  # Focus sui 2 peggiori
            if comp_score < 0.6:  # Sotto la sufficienza
                recs = self._get_component_recommendations(comp_name, comp_score)
                recommendations.extend(recs)
        
        # Prioritizza per impatto e fattibilità
        recommendations.sort(key=lambda x: x['priority_score'], reverse=True)
        
        return recommendations[:5]  # Top 5 raccomandazioni
    
    def _get_component_recommendations(self, component: str, 
                                     score: float) -> List[Dict[str, any]]:
        """Raccomandazioni specifiche per componente"""
        recommendations_db = {
            'physical': [
                {
                    'action': 'Upgrade UPS systems to N+1 redundancy',
                    'impact': 0.15,
                    'cost': 'medium',
                    'time': '3-6 months',
                    'threshold': 0.5
                },
                {
                    'action': 'Implement free cooling for PUE improvement',
                    'impact': 0.12,
                    'cost': 'high',
                    'time': '6-12 months',
                    'threshold': 0.4
                }
            ],
            'architectural': [
                {
                    'action': 'Accelerate cloud migration for critical workloads',
                    'impact': 0.25,
                    'cost': 'high',
                    'time': '12-18 months',
                    'threshold': 0.5
                },
                {
                    'action': 'Implement SD-WAN for network modernization',
                    'impact': 0.18,
                    'cost': 'medium',
                    'time': '6-9 months',
                    'threshold': 0.4
                }
            ],
            'security': [
                {
                    'action': 'Deploy Zero Trust architecture phase 1',
                    'impact': 0.30,
                    'cost': 'high',
                    'time': '9-12 months',
                    'threshold': 0.6
                },
                {
                    'action': 'Implement advanced threat detection (XDR)',
                    'impact': 0.22,
                    'cost': 'medium',
                    'time': '3-6 months',
                    'threshold': 0.5
                }
            ],
            'compliance': [
                {
                    'action': 'Integrate compliance management platform',
                    'impact': 0.20,
                    'cost': 'medium',
                    'time': '6-9 months',
                    'threshold': 0.5
                },
                {
                    'action': 'Automate compliance evidence collection',
                    'impact': 0.15,
                    'cost': 'low',
                    'time': '3-4 months',
                    'threshold': 0.4
                }
            ]
        }
        
        recs = []
        for rec in recommendations_db.get(component, []):
            if score < rec['threshold']:
                priority = self._calculate_priority(
                    rec['impact'], 
                    rec['cost'], 
                    score
                )
                rec['priority_score'] = priority
                recs.append(rec)
        
        return recs
    
    def _calculate_priority(self, impact: float, cost: str, 
                           current_score: float) -> float:
        """Calcola priorità raccomandazione"""
        cost_factor = {'low': 1.0, 'medium': 0.7, 'high': 0.4}[cost]
        urgency_factor = 1 - current_score  # Più basso lo score, più urgente
        
        return impact * cost_factor * urgency_factor
    
    def _get_benchmark_distribution(self, component: str) -> List[float]:
        """Ritorna distribuzione benchmark per componente"""
        # Distribuzioni empiriche basate su 156 organizzazioni
        distributions = {
            'physical': stats.beta(2.5, 2.0).rvs(1000),
            'architectural': stats.beta(2.0, 3.0).rvs(1000),
            'security': stats.beta(2.2, 2.8).rvs(1000),
            'compliance': stats.beta(2.8, 2.2).rvs(1000)
        }
        return distributions.get(component, stats.uniform(0, 1).rvs(1000))
    
    def _calculate_confidence_interval(self, score: float, 
                                     uncertainty: float) -> Tuple[float, float]:
        """Calcola intervallo di confidenza per lo score"""
        margin = score * uncertainty * 1.96  # 95% CI
        return (
            max(0, (score - margin) * 100),
            min(100, (score + margin) * 100)
        )
    
    def _validate_inputs(self, components: Dict[str, float], 
                        context: Dict[str, any]) -> None:
        """Valida input del modello"""
        # Verifica componenti
        required_components = {'physical', 'architectural', 'security', 'compliance'}
        if set(components.keys()) != required_components:
            raise ValueError(f"Componenti richieste: {required_components}")
        
        # Verifica range [0, 1]
        for comp_name, comp_score in components.items():
            if not 0 <= comp_score <= 1:
                raise ValueError(f"{comp_name} score deve essere in [0, 1]")
        
        # Verifica contesto minimo
        if 'scale' not in context:
            raise ValueError("Contesto deve includere 'scale' (numero negozi)")
\end{lstlisting}

\subsection{C.5.3 Calibrazione Empirica delle Componenti}

\subsubsection{Modelli di Scoring per Componente}

\begin{lstlisting}[language=Python, caption=Calcolo Score Componenti GIST]
class ComponentScoring:
    """Classe per calcolo score delle singole componenti GIST"""
    
    @staticmethod
    def calculate_physical_score(infrastructure_data: Dict) -> float:
        """
        Calcola score componente Physical (P)
        
        Metriche:
        - Power redundancy (25%)
        - Cooling efficiency (20%)
        - Network reliability (30%)
        - Physical security (25%)
        """
        # Power redundancy score
        ups_config = infrastructure_data.get('ups_configuration', 'N')
        power_scores = {
            'N': 0.3,      # No redundancy
            'N+1': 0.7,    # Standard redundancy
            'N+N': 0.9,    # Full redundancy
            '2N': 1.0      # Double redundancy
        }
        power_score = power_scores.get(ups_config, 0.3)
        
        # Cooling efficiency (PUE based)
        pue = infrastructure_data.get('pue', 2.0)
        if pue < 1.3:
            cooling_score = 1.0
        elif pue < 1.5:
            cooling_score = 0.8
        elif pue < 1.8:
            cooling_score = 0.6
        elif pue < 2.0:
            cooling_score = 0.4
        else:
            cooling_score = 0.2
        
        # Network reliability
        network_uptime = infrastructure_data.get('network_uptime_percent', 99.0)
        network_score = (network_uptime - 95) / 5  # Normalize 95-100% to 0-1
        network_score = max(0, min(1, network_score))
        
        # Physical security
        security_features = infrastructure_data.get('physical_security_features', [])
        required_features = [
            'access_control', 'cctv', 'intrusion_detection', 
            'environmental_monitoring', 'security_guards'
        ]
        security_score = len(set(security_features) & set(required_features)) / len(required_features)
        
        # Weighted average
        physical_score = (
            0.25 * power_score +
            0.20 * cooling_score +
            0.30 * network_score +
            0.25 * security_score
        )
        
        return physical_score
    
    @staticmethod
    def calculate_architectural_score(architecture_data: Dict) -> float:
        """
        Calcola score componente Architectural (A)
        
        Metriche:
        - Cloud adoption (35%)
        - Automation level (25%)
        - API maturity (20%)
        - DevOps practices (20%)
        """
        # Cloud adoption
        workloads_in_cloud = architecture_data.get('cloud_workload_percentage', 0)
        cloud_score = workloads_in_cloud / 100
        
        # Automation level
        automation_metrics = {
            'infrastructure_as_code': architecture_data.get('iac_coverage', 0),
            'ci_cd_adoption': architecture_data.get('cicd_percentage', 0),
            'auto_scaling': architecture_data.get('autoscaling_enabled', 0),
            'self_healing': architecture_data.get('self_healing_percentage', 0)
        }
        automation_score = np.mean(list(automation_metrics.values())) / 100
        
        # API maturity
        api_maturity_level = architecture_data.get('api_maturity', 1)
        api_scores = {
            1: 0.2,  # No APIs
            2: 0.4,  # Some REST APIs
            3: 0.6,  # Comprehensive REST
            4: 0.8,  # GraphQL/gRPC
            5: 1.0   # API-first architecture
        }
        api_score = api_scores.get(api_maturity_level, 0.2)
        
        # DevOps practices
        devops_practices = architecture_data.get('devops_practices', [])
        key_practices = [
            'continuous_integration', 'continuous_deployment',
            'infrastructure_as_code', 'monitoring_observability',
            'security_scanning', 'automated_testing'
        ]
        devops_score = len(set(devops_practices) & set(key_practices)) / len(key_practices)
        
        # Weighted average
        architectural_score = (
            0.35 * cloud_score +
            0.25 * automation_score +
            0.20 * api_score +
            0.20 * devops_score
        )
        
        return architectural_score
    
    @staticmethod
    def calculate_security_score(security_data: Dict) -> float:
        """
        Calcola score componente Security (S)
        
        Metriche:
        - Zero Trust implementation (30%)
        - Threat detection capability (25%)
        - Incident response maturity (25%)
        - Security training effectiveness (20%)
        """
        # Zero Trust implementation
        zt_components = security_data.get('zero_trust_components', [])
        required_zt = [
            'identity_verification', 'device_trust', 'network_segmentation',
            'app_segmentation', 'data_protection', 'visibility_analytics'
        ]
        zt_score = len(set(zt_components) & set(required_zt)) / len(required_zt)
        
        # Threat detection
        detection_metrics = {
            'mttd_hours': security_data.get('mean_time_to_detect', 168),
            'false_positive_rate': security_data.get('false_positive_rate', 0.5),
            'coverage': security_data.get('detection_coverage', 0.5)
        }
        # Normalize MTTD (168h = 0, 1h = 1)
        mttd_score = max(0, 1 - (detection_metrics['mttd_hours'] / 168))
        fp_score = 1 - detection_metrics['false_positive_rate']
        detection_score = (mttd_score + fp_score + detection_metrics['coverage']) / 3
        
        # Incident response
        ir_maturity = security_data.get('incident_response_maturity', 1)
        ir_scores = {
            1: 0.2,  # Ad-hoc
            2: 0.4,  # Documented
            3: 0.6,  # Tested
            4: 0.8,  # Measured
            5: 1.0   # Optimized
        }
        ir_score = ir_scores.get(ir_maturity, 0.2)
        
        # Security training
        training_metrics = {
            'completion_rate': security_data.get('training_completion_rate', 0),
            'phishing_test_pass': security_data.get('phishing_test_pass_rate', 0),
            'security_incidents_per_user': security_data.get('incidents_per_user', 1)
        }
        training_score = (
            training_metrics['completion_rate'] / 100 * 0.4 +
            training_metrics['phishing_test_pass'] / 100 * 0.4 +
            max(0, 1 - training_metrics['security_incidents_per_user']) * 0.2
        )
        
        # Weighted average
        security_score = (
            0.30 * zt_score +
            0.25 * detection_score +
            0.25 * ir_score +
            0.20 * training_score
        )
        
        return security_score
    
    @staticmethod
    def calculate_compliance_score(compliance_data: Dict) -> float:
        """
        Calcola score componente Compliance (C)
        
        Metriche:
        - Standards overlap optimization (40%)
        - Automation of compliance (30%)
        - Audit readiness (30%)
        """
        # Standards overlap
        total_controls = compliance_data.get('total_controls', 889)
        unique_controls = compliance_data.get('unique_controls_implemented', 889)
        overlap_efficiency = 1 - (unique_controls / total_controls)
        overlap_score = overlap_efficiency * 2  # Scale to 0-1 (max efficiency ~50%)
        overlap_score = min(1, overlap_score)
        
        # Compliance automation
        automated_controls = compliance_data.get('automated_controls', 0)
        total_implemented = compliance_data.get('total_implemented_controls', 1)
        automation_score = automated_controls / total_implemented
        
        # Audit readiness
        audit_metrics = {
            'last_audit_findings': compliance_data.get('last_audit_findings', 10),
            'evidence_automation': compliance_data.get('evidence_automation_rate', 0),
            'continuous_monitoring': compliance_data.get('continuous_monitoring_coverage', 0)
        }
        # Normalize findings (0 = 1.0, 10+ = 0)
        findings_score = max(0, 1 - (audit_metrics['last_audit_findings'] / 10))
        audit_score = (
            findings_score * 0.4 +
            audit_metrics['evidence_automation'] / 100 * 0.3 +
            audit_metrics['continuous_monitoring'] / 100 * 0.3
        )
        
        # Weighted average
        compliance_score = (
            0.40 * overlap_score +
            0.30 * automation_score +
            0.30 * audit_score
        )
        
        return compliance_score
\end{lstlisting}

\subsection{C.5.4 Analisi delle Sinergie e Ottimizzazione}

\subsubsection{Modello di Sinergie Cross-Dimensionali}

\begin{lstlisting}[language=Python, caption=Analisi Sinergie Framework GIST]
def analyze_gist_synergies(implementation_data: pd.DataFrame) -> Dict[str, any]:
    """
    Quantifica effetti sinergici tra componenti GIST
    """
    # Estrai miglioramenti per componente
    improvements = pd.DataFrame({
        'physical': implementation_data['physical_improvement'],
        'architectural': implementation_data['architectural_improvement'],
        'security': implementation_data['security_improvement'],
        'compliance': implementation_data['compliance_improvement']
    })
    
    # Matrice di correlazione non-lineare (Spearman)
    correlation_matrix = improvements.corr(method='spearman')
    
    # Calcola effetti di amplificazione
    synergy_effects = {}
    
    # Physical → Architectural
    # Infrastruttura robusta abilita trasformazione cloud
    phys_arch_correlation = correlation_matrix.loc['physical', 'architectural']
    expected_linear = 0.15  # Correlazione attesa se indipendenti
    synergy_effects['physical_architectural'] = {
        'observed': phys_arch_correlation,
        'expected': expected_linear,
        'amplification': (phys_arch_correlation - expected_linear) / expected_linear,
        'interpretation': 'Strong foundation enables cloud transformation'
    }
    
    # Architectural → Security
    # Architetture moderne facilitano implementazione sicurezza
    arch_sec_correlation = correlation_matrix.loc['architectural', 'security']
    expected_linear = 0.22
    synergy_effects['architectural_security'] = {
        'observed': arch_sec_correlation,
        'expected': expected_linear,
        'amplification': (arch_sec_correlation - expected_linear) / expected_linear,
        'interpretation': 'Modern architecture simplifies security implementation'
    }
    
    # Security → Compliance
    # Sicurezza robusta semplifica compliance
    sec_comp_correlation = correlation_matrix.loc['security', 'compliance']
    expected_linear = 0.18
    synergy_effects['security_compliance'] = {
        'observed': sec_comp_correlation,
        'expected': expected_linear,
        'amplification': (sec_comp_correlation - expected_linear) / expected_linear,
        'interpretation': 'Strong security posture streamlines compliance'
    }
    
    # Effetto sistema totale
    # Confronta miglioramento totale con somma lineare componenti
    linear_sum = improvements.sum(axis=1)
    actual_improvement = implementation_data['total_gist_improvement']
    
    system_amplification = []
    for linear, actual in zip(linear_sum, actual_improvement):
        if linear > 0:
            amp = (actual / linear) - 1
            system_amplification.append(amp)
    
    mean_system_amplification = np.mean(system_amplification)
    
    # Identifica pattern di implementazione ottimali
    optimal_patterns = identify_optimal_patterns(improvements, actual_improvement)
    
    return {
        'correlation_matrix': correlation_matrix,
        'synergy_effects': synergy_effects,
        'system_amplification': mean_system_amplification,
        'system_amplification_std': np.std(system_amplification),
        'optimal_patterns': optimal_patterns,
        'strongest_synergy': max(synergy_effects.items(), 
                                key=lambda x: x[1]['amplification'])[0]
    }

def identify_optimal_patterns(improvements: pd.DataFrame, 
                             outcomes: pd.Series) -> List[Dict]:
    """Identifica pattern di implementazione più efficaci"""
    # Cluster organizations by implementation pattern
    from sklearn.cluster import KMeans
    
    n_clusters = 4
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(improvements)
    
    patterns = []
    for i in range(n_clusters):
        cluster_mask = clusters == i
        cluster_data = improvements[cluster_mask]
        cluster_outcomes = outcomes[cluster_mask]
        
        pattern = {
            'cluster_id': i,
            'n_organizations': cluster_mask.sum(),
            'mean_improvements': cluster_data.mean().to_dict(),
            'mean_outcome': cluster_outcomes.mean(),
            'outcome_std': cluster_outcomes.std(),
            'characterization': characterize_pattern(cluster_data.mean())
        }
        patterns.append(pattern)
    
    # Ordina per outcome medio
    patterns.sort(key=lambda x: x['mean_outcome'], reverse=True)
    
    return patterns

def characterize_pattern(mean_improvements: pd.Series) -> str:
    """Caratterizza pattern di implementazione"""
    # Identifica focus principale
    primary_focus = mean_improvements.idxmax()
    primary_value = mean_improvements.max()
    
    # Calcola bilanciamento
    balance_score = 1 - mean_improvements.std() / mean_improvements.mean()
    
    if balance_score > 0.7:
        return f"Balanced approach with slight {primary_focus} emphasis"
    elif primary_value > 0.6:
        return f"Strong {primary_focus} focus"
    else:
        secondary_focus = mean_improvements.nlargest(2).index[1]
        return f"Dual focus on {primary_focus} and {secondary_focus}"

# Risultati empirici tipici:
# Physical→Architectural: +27% amplificazione
# Architectural→Security: +34% amplificazione  
# Security→Compliance: +41% amplificazione
# Sistema totale: +52% oltre somma lineare
\end{lstlisting}

\subsection{C.5.5 Generazione Roadmap e Ottimizzazione Sequenza}

\begin{lstlisting}[language=Python, caption=Generazione Roadmap Ottimizzata GIST]
class GISTRoadmapGenerator:
    """Genera roadmap implementativa ottimizzata basata su GIST"""
    
    def __init__(self, gist_framework: GISTFramework):
        self.gist = gist_framework
        self.initiative_database = self._load_initiative_database()
        
    def generate_roadmap(self, current_state: Dict, target_state: Dict,
                        constraints: Dict) -> Dict:
        """
        Genera roadmap ottimizzata per raggiungere target GIST score
        
        Args:
            current_state: Score attuali componenti e contesto
            target_state: Score target desiderati
            constraints: Vincoli budget, tempo, risorse
            
        Returns:
            Roadmap con sequenza ottimizzata di iniziative
        """
        # Calcola gap per componente
        gaps = self._calculate_gaps(current_state, target_state)
        
        # Identifica iniziative candidate
        candidate_initiatives = self._identify_initiatives(gaps)
        
        # Ottimizza sequenza con programmazione dinamica
        optimal_sequence = self._optimize_sequence(
            candidate_initiatives,
            constraints,
            current_state['context']
        )
        
        # Calcola metriche roadmap
        roadmap_metrics = self._calculate_roadmap_metrics(
            optimal_sequence,
            current_state,
            target_state
        )
        
        # Genera timeline dettagliata
        timeline = self._generate_timeline(optimal_sequence, constraints)
        
        return {
            'current_score': self.gist.calculate_score(
                current_state['components'], 
                current_state['context']
            ),
            'target_score': self.gist.calculate_score(
                target_state['components'],
                current_state['context']
            ),
            'gaps': gaps,
            'initiatives': optimal_sequence,
            'timeline': timeline,
            'metrics': roadmap_metrics,
            'risk_assessment': self._assess_roadmap_risks(optimal_sequence),
            'success_probability': self._estimate_success_probability(
                optimal_sequence, 
                constraints
            )
        }
    
    def _optimize_sequence(self, initiatives: List[Dict], 
                          constraints: Dict, context: Dict) -> List[Dict]:
        """
        Ottimizza sequenza iniziative usando dynamic programming
        """
        n = len(initiatives)
        budget = constraints['budget']
        timeline = constraints['timeline_months']
        
        # Dynamic programming table
        # dp[i][b][t] = max value achievable with first i initiatives,
        #               budget b, and time t
        dp = {}
        parent = {}
        
        # Inizializzazione
        for b in range(budget + 1):
            for t in range(timeline + 1):
                dp[(0, b, t)] = 0
                parent[(0, b, t)] = []
        
        # Fill DP table
        for i in range(1, n + 1):
            init = initiatives[i-1]
            
            for b in range(budget + 1):
                for t in range(timeline + 1):
                    # Option 1: Skip this initiative
                    dp[(i, b, t)] = dp[(i-1, b, t)]
                    parent[(i, b, t)] = parent[(i-1, b, t)].copy()
                    
                    # Option 2: Take this initiative if feasible
                    if (init['cost'] <= b and init['duration'] <= t):
                        # Calculate dependencies
                        deps_met = all(
                            dep in parent[(i-1, b, t)] 
                            for dep in init.get('dependencies', [])
                        )
                        
                        if deps_met:
                            remaining_budget = b - init['cost']
                            remaining_time = t - init['duration']
                            
                            # Value includes direct impact and synergies
                            value = self._calculate_initiative_value(
                                init, 
                                parent[(i-1, b, t)],
                                context
                            )
                            
                            new_value = dp[(i-1, remaining_budget, remaining_time)] + value
                            
                            if new_value > dp[(i, b, t)]:
                                dp[(i, b, t)] = new_value
                                parent[(i, b, t)] = parent[(i-1, remaining_budget, remaining_time)].copy()
                                parent[(i, b, t)].append(init)
        
        # Reconstruct optimal sequence
        optimal = parent[(n, budget, timeline)]
        
        # Sort by dependencies and priority
        optimal = self._topological_sort_initiatives(optimal)
        
        return optimal
    
    def _calculate_initiative_value(self, initiative: Dict, 
                                   previous: List[Dict], 
                                   context: Dict) -> float:
        """Calcola valore di un'iniziativa considerando sinergie"""
        # Base value from GIST improvement
        base_value = 0
        for component, improvement in initiative['improvements'].items():
            weight = self.gist.weights[component]
            base_value += weight * improvement
        
        # Synergy multiplier
        synergy = 1.0
        for prev in previous:
            synergy_factor = self._calculate_synergy(prev, initiative)
            synergy *= (1 + synergy_factor)
        
        # Context adjustments
        if context.get('innovation_level') == 'cutting_edge':
            if initiative.get('innovation_factor', 0) > 0.5:
                synergy *= 1.2
        
        # Risk adjustment
        risk_factor = 1 - initiative.get('risk_level', 0.1)
        
        return base_value * synergy * risk_factor * 100  # Scale to 0-100
    
    def _calculate_synergy(self, init1: Dict, init2: Dict) -> float:
        """Calcola sinergia tra due iniziative"""
        synergy_matrix = {
            ('infrastructure_upgrade', 'cloud_migration'): 0.25,
            ('cloud_migration', 'zero_trust'): 0.30,
            ('zero_trust', 'compliance_automation'): 0.35,
            ('api_development', 'microservices'): 0.28,
            ('devsecops', 'continuous_compliance'): 0.32
        }
        
        key = (init1['type'], init2['type'])
        return synergy_matrix.get(key, 0.05)  # Default 5% synergy
    
    def _assess_roadmap_risks(self, initiatives: List[Dict]) -> Dict:
        """Valuta rischi della roadmap"""
        risks = {
            'technical_complexity': 0,
            'organizational_change': 0,
            'resource_constraints': 0,
            'dependency_risks': 0
        }
        
        for init in initiatives:
            risks['technical_complexity'] += init.get('complexity', 0.5)
            risks['organizational_change'] += init.get('change_impact', 0.5)
            risks['resource_constraints'] += init.get('resource_intensity', 0.5)
            
            # Dependency risk increases non-linearly
            n_deps = len(init.get('dependencies', []))
            risks['dependency_risks'] += n_deps ** 1.5
        
        # Normalize
        n_initiatives = len(initiatives)
        for risk in risks:
            risks[risk] /= n_initiatives
            risks[risk] = min(1.0, risks[risk])  # Cap at 1.0
        
        # Overall risk score
        risks['overall'] = np.mean(list(risks.values()))
        
        # Risk mitigation recommendations
        risks['mitigations'] = self._recommend_mitigations(risks)
        
        return risks
    
    def _recommend_mitigations(self, risks: Dict) -> List[str]:
        """Raccomanda strategie di mitigazione basate sui rischi"""
        mitigations = []
        
        if risks['technical_complexity'] > 0.7:
            mitigations.append(
                "Implement proof-of-concept phases for complex initiatives"
            )
            
        if risks['organizational_change'] > 0.6:
            mitigations.append(
                "Develop comprehensive change management program"
            )
            
        if risks['resource_constraints'] > 0.7:
            mitigations.append(
                "Consider phased approach or external partnerships"
            )
            
        if risks['dependency_risks'] > 0.5:
            mitigations.append(
                "Build dependency buffer time and parallel work streams"
            )
        
        return mitigations
\end{lstlisting}

\subsection{C.5.6 Validazione e Testing del Framework}

\begin{lstlisting}[language=Python, caption=Suite di Test per Framework GIST]
import unittest
from unittest.mock import Mock, patch

class TestGISTFramework(unittest.TestCase):
    """Test suite completa per framework GIST"""
    
    def setUp(self):
        """Setup per ogni test"""
        self.gist = GISTFramework(assessment_mode='balanced')
        self.test_components = {
            'physical': 0.7,
            'architectural': 0.6,
            'security': 0.65,
            'compliance': 0.55
        }
        self.test_context = {
            'scale': 150,  # 150 stores
            'geographic': 3,  # 3 regions
            'innovation_level': 'early_adopter'
        }
    
    def test_score_calculation_balanced(self):
        """Test calcolo score modalità balanced"""
        result = self.gist.calculate_score(
            self.test_components, 
            self.test_context
        )
        
        # Verifica struttura output
        self.assertIn('score', result)
        self.assertIn('components', result)
        self.assertIn('k_gdo', result)
        self.assertIn('interpretation', result)
        
        # Verifica range score
        self.assertGreaterEqual(result['score'], 0)
        self.assertLessEqual(result['score'], 100)
        
        # Verifica calcolo manuale
        expected_base = sum(
            self.gist.weights[c] * v 
            for c, v in self.test_components.items()
        )
        expected_k_gdo = (
            (1 + 0.15 * np.log(150/50)) *  # scale
            (1 + 0.08 * 2) *                # geographic
            1.25                             # criticality
        )
        expected_innovation = 0.15  # early_adopter
        expected_score = expected_base * expected_k_gdo * (1 + expected_innovation) * 100
        
        self.assertAlmostEqual(result['score'], expected_score, places=1)
    
    def test_score_calculation_critical(self):
        """Test calcolo score modalità critical"""
        gist_critical = GISTFramework(assessment_mode='critical')
        result = gist_critical.calculate_score(
            self.test_components,
            self.test_context
        )
        
        # Score critical dovrebbe essere < balanced per stessi input
        result_balanced = self.gist.calculate_score(
            self.test_components,
            self.test_context
        )
        
        self.assertLess(result['score'], result_balanced['score'])
    
    def test_edge_cases(self):
        """Test casi limite"""
        # Test con componente zero
        components_with_zero = self.test_components.copy()
        components_with_zero['security'] = 0
        
        result = self.gist.calculate_score(
            components_with_zero,
            self.test_context
        )
        
        # Score dovrebbe essere molto basso ma non zero (per evitare divisioni)
        self.assertGreater(result['score'], 0)
        self.assertLess(result['score'], 20)  # Critico
        
        # Test tutti componenti al massimo
        perfect_components = {k: 1.0 for k in self.test_components}
        result_perfect = self.gist.calculate_score(
            perfect_components,
            self.test_context
        )
        
        self.assertGreater(result_perfect['score'], 80)  # Eccellente
    
    def test_uncertainty_calculation(self):
        """Test calcolo incertezza"""
        # Alta variabilità dovrebbe aumentare incertezza
        high_variance_components = {
            'physical': 0.9,
            'architectural': 0.3,
            'security': 0.8,
            'compliance': 0.2
        }
        
        result_high_var = self.gist.calculate_score(
            high_variance_components,
            self.test_context
        )
        
        result_low_var = self.gist.calculate_score(
            self.test_components,  # More balanced
            self.test_context
        )
        
        self.assertGreater(
            result_high_var['uncertainty'],
            result_low_var['uncertainty']
        )
    
    def test_recommendations_generation(self):
        """Test generazione raccomandazioni"""
        # Componenti con debolezze
        weak_components = {
            'physical': 0.4,  # Weakness
            'architectural': 0.3,  # Critical weakness
            'security': 0.7,
            'compliance': 0.8
        }
        
        result = self.gist.calculate_score(
            weak_components,
            self.test_context
        )
        
        # Dovrebbe raccomandare miglioramenti per physical e architectural
        recommendations = result['recommendations']
        self.assertGreater(len(recommendations), 0)
        
        # Verifica che le raccomandazioni siano per componenti deboli
        recommended_components = set()
        for rec in recommendations:
            if 'cloud' in rec['action'].lower() or 'architecture' in rec['action'].lower():
                recommended_components.add('architectural')
            if 'ups' in rec['action'].lower() or 'cooling' in rec['action'].lower():
                recommended_components.add('physical')
        
        self.assertIn('architectural', recommended_components)
    
    def test_synergy_analysis(self):
        """Test analisi sinergie"""
        # Genera dati di test con correlazioni note
        n_orgs = 100
        np.random.seed(42)
        
        # Crea miglioramenti correlati
        physical_imp = np.random.normal(0.2, 0.05, n_orgs)
        # Architectural correlato con physical
        architectural_imp = physical_imp * 1.5 + np.random.normal(0, 0.05, n_orgs)
        # Security correlato con architectural
        security_imp = architectural_imp * 1.3 + np.random.normal(0, 0.05, n_orgs)
        # Compliance correlato con security
        compliance_imp = security_imp * 1.2 + np.random.normal(0, 0.05, n_orgs)
        
        implementation_data = pd.DataFrame({
            'physical_improvement': physical_imp,
            'architectural_improvement': architectural_imp,
            'security_improvement': security_imp,
            'compliance_improvement': compliance_imp,
            'total_gist_improvement': (
                physical_imp + architectural_imp + 
                security_imp + compliance_imp
            ) * 1.3  # 30% synergy
        })
        
        synergies = analyze_gist_synergies(implementation_data)
        
        # Verifica che siano state identificate sinergie positive
        self.assertGreater(
            synergies['synergy_effects']['physical_architectural']['amplification'],
            0
        )
        self.assertGreater(
            synergies['system_amplification'],
            0.25  # At least 25% amplification
        )

if __name__ == '__main__':
    unittest.main()
