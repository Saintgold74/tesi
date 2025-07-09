"""
GIST Score Calculation Algorithm
================================
Unified security posture score for Zero Trust environments
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import math
import json

class SecurityDimension(Enum):
    """Dimensioni di sicurezza valutate dal GIST Score"""
    IDENTITY_TRUST = "identity_trust"
    NETWORK_ISOLATION = "network_isolation" 
    THREAT_RESILIENCE = "threat_resilience"
    DATA_PROTECTION = "data_protection"
    ADAPTIVE_RESPONSE = "adaptive_response"

@dataclass
class GISTMetrics:
    """Metriche raw per calcolo GIST Score"""
    # Identity & Access
    avg_trust_score: float  # 0-1
    mfa_adoption_rate: float  # 0-1
    privileged_account_monitoring: float  # 0-1
    identity_anomaly_detection_rate: float  # 0-1
    
    # Network Segmentation
    micro_segmentation_coverage: float  # 0-1
    east_west_traffic_inspection: float  # 0-1
    network_isolation_effectiveness: float  # 0-1
    segment_compromise_containment: float  # 0-1
    
    # Threat Detection & Response
    mean_time_to_detect: float  # minuti
    mean_time_to_respond: float  # minuti
    automated_response_rate: float  # 0-1
    threat_hunting_maturity: float  # 0-1
    
    # Data Protection
    encryption_at_rest_coverage: float  # 0-1
    encryption_in_transit_coverage: float  # 0-1
    data_classification_accuracy: float  # 0-1
    dlp_effectiveness: float  # 0-1
    
    # System Resilience
    availability_percentage: float  # 99.x
    recovery_time_objective: float  # minuti
    backup_verification_rate: float  # 0-1
    incident_containment_rate: float  # 0-1

class GISTScoreCalculator:
    """
    Calcola GIST Score unificato
    Range: 0-1000 (simile a credit score per interpretabilità)
    """
    
    def __init__(self):
        # Pesi per dimensioni (somma = 1.0)
        self.dimension_weights = {
            SecurityDimension.IDENTITY_TRUST: 0.25,
            SecurityDimension.NETWORK_ISOLATION: 0.25,
            SecurityDimension.THREAT_RESILIENCE: 0.20,
            SecurityDimension.DATA_PROTECTION: 0.15,
            SecurityDimension.ADAPTIVE_RESPONSE: 0.15
        }
        
        # Parametri per normalizzazione non-lineare
        self.normalization_params = {
            'mean_time_to_detect': {'optimal': 5, 'acceptable': 60, 'critical': 1440},
            'mean_time_to_respond': {'optimal': 15, 'acceptable': 120, 'critical': 2880},
            'availability_percentage': {'optimal': 99.99, 'acceptable': 99.9, 'critical': 99.0},
            'recovery_time_objective': {'optimal': 15, 'acceptable': 240, 'critical': 1440}
        }
    
    def calculate_gist_score(self, metrics: GISTMetrics) -> Dict:
        """
        Calcola GIST Score principale e sub-scores
        
        Returns:
            Dict con score totale, sub-scores per dimensione, e raccomandazioni
        """
        # Calcola score per ogni dimensione
        dimension_scores = {
            SecurityDimension.IDENTITY_TRUST: self._calculate_identity_score(metrics),
            SecurityDimension.NETWORK_ISOLATION: self._calculate_network_score(metrics),
            SecurityDimension.THREAT_RESILIENCE: self._calculate_threat_score(metrics),
            SecurityDimension.DATA_PROTECTION: self._calculate_data_score(metrics),
            SecurityDimension.ADAPTIVE_RESPONSE: self._calculate_adaptive_score(metrics)
        }
        
        # Calcola score pesato
        weighted_score = sum(
            dimension_scores[dim] * self.dimension_weights[dim]
            for dim in SecurityDimension
        )
        
        # Applica funzione di trasformazione non-lineare
        # Penalizza score bassi più severamente
        transformed_score = self._apply_transformation(weighted_score)
        
        # Scala a 0-1000
        gist_score = int(transformed_score * 1000)
        
        # Calcola confidence interval
        confidence = self._calculate_confidence(metrics)
        
        # Genera raccomandazioni
        recommendations = self._generate_recommendations(dimension_scores, metrics)
        
        # Calcola trend (richiede historical data)
        trend = self._calculate_trend(gist_score)
        
        return {
            'gist_score': gist_score,
            'dimension_scores': {dim.value: round(score * 100, 1) 
                               for dim, score in dimension_scores.items()},
            'confidence_interval': confidence,
            'security_rating': self._score_to_rating(gist_score),
            'maturity_level': self._score_to_maturity(gist_score),
            'trend': trend,
            'recommendations': recommendations,
            'risk_indicators': self._identify_risk_indicators(metrics, dimension_scores),
            'benchmark_percentile': self._calculate_percentile(gist_score)
        }
    
    def _calculate_identity_score(self, metrics: GISTMetrics) -> float:
        """
        Calcola score per Identity & Trust dimension
        Formula: Weighted geometric mean per enfatizzare weakest link
        """
        components = {
            'trust_score': metrics.avg_trust_score,
            'mfa_adoption': metrics.mfa_adoption_rate,
            'privileged_monitoring': metrics.privileged_account_monitoring,
            'anomaly_detection': metrics.identity_anomaly_detection_rate
        }
        
        weights = {
            'trust_score': 0.35,
            'mfa_adoption': 0.30,
            'privileged_monitoring': 0.20,
            'anomaly_detection': 0.15
        }
        
        # Geometric mean pesata
        score = 1.0
        for component, value in components.items():
            # Evita log(0)
            value = max(value, 0.01)
            score *= value ** weights[component]
        
        # Bonus per full MFA adoption
        if metrics.mfa_adoption_rate >= 0.95:
            score *= 1.1
        
        return min(score, 1.0)
    
    def _calculate_network_score(self, metrics: GISTMetrics) -> float:
        """
        Calcola score per Network Isolation dimension
        """
        # Base score da copertura micro-segmentazione
        base_score = metrics.micro_segmentation_coverage
        
        # Moltiplicatori per effectiveness
        effectiveness_multiplier = (
            0.3 * metrics.east_west_traffic_inspection +
            0.4 * metrics.network_isolation_effectiveness +
            0.3 * metrics.segment_compromise_containment
        )
        
        # Formula: base * (1 + bonus da effectiveness)
        score = base_score * (0.5 + 0.5 * effectiveness_multiplier)
        
        # Penalità se isolation è basso
        if metrics.network_isolation_effectiveness < 0.5:
            score *= 0.8
        
        return score
    
    def _calculate_threat_score(self, metrics: GISTMetrics) -> float:
        """
        Calcola score per Threat Resilience dimension
        """
        # Normalizza tempi di detection/response
        detect_score = self._normalize_time_metric(
            metrics.mean_time_to_detect, 
            'mean_time_to_detect'
        )
        respond_score = self._normalize_time_metric(
            metrics.mean_time_to_respond,
            'mean_time_to_respond'
        )
        
        # Combina metriche
        components = {
            'detection': detect_score,
            'response': respond_score,
            'automation': metrics.automated_response_rate,
            'hunting': metrics.threat_hunting_maturity
        }
        
        # Media armonica per penalizzare weak links
        harmonic_mean = len(components) / sum(1/max(v, 0.01) for v in components.values())
        
        # Bonus per automazione alta
        if metrics.automated_response_rate > 0.8:
            harmonic_mean *= 1.15
        
        return min(harmonic_mean, 1.0)
    
    def _calculate_data_score(self, metrics: GISTMetrics) -> float:
        """
        Calcola score per Data Protection dimension
        """
        # Encryption è fondamentale - usa minimo
        encryption_score = min(
            metrics.encryption_at_rest_coverage,
            metrics.encryption_in_transit_coverage
        )
        
        # Altri componenti
        classification_score = metrics.data_classification_accuracy
        dlp_score = metrics.dlp_effectiveness
        
        # Formula: encryption domina (60%), resto 40%
        score = (
            0.6 * encryption_score +
            0.25 * classification_score +
            0.15 * dlp_score
        )
        
        # Penalità severa per encryption bassa
        if encryption_score < 0.8:
            score *= 0.7
        
        return score
    
    def _calculate_adaptive_score(self, metrics: GISTMetrics) -> float:
        """
        Calcola score per Adaptive Response dimension
        """
        # Availability normalizzata
        avail_score = self._normalize_availability(metrics.availability_percentage)
        
        # RTO normalizzato
        rto_score = self._normalize_time_metric(
            metrics.recovery_time_objective,
            'recovery_time_objective'
        )
        
        # Resilience factors
        resilience_score = (
            0.5 * metrics.backup_verification_rate +
            0.5 * metrics.incident_containment_rate
        )
        
        # Weighted combination
        score = (
            0.4 * avail_score +
            0.3 * rto_score +
            0.3 * resilience_score
        )
        
        return score
    
    def _normalize_time_metric(self, value: float, metric_name: str) -> float:
        """
        Normalizza metriche temporali usando funzione sigmoidale
        """
        params = self.normalization_params[metric_name]
        optimal = params['optimal']
        acceptable = params['acceptable']
        critical = params['critical']
        
        if value <= optimal:
            return 1.0
        elif value >= critical:
            return 0.0
        elif value <= acceptable:
            # Interpolazione lineare tra optimal e acceptable
            return 1.0 - 0.3 * (value - optimal) / (acceptable - optimal)
        else:
            # Decadimento esponenziale tra acceptable e critical
            decay_rate = -math.log(0.1) / (critical - acceptable)
            return 0.7 * math.exp(-decay_rate * (value - acceptable))
    
    def _normalize_availability(self, availability: float) -> float:
        """
        Normalizza availability percentage con curva steep
        """
        if availability >= 99.99:
            return 1.0
        elif availability >= 99.9:
            return 0.9 + 0.1 * (availability - 99.9) / 0.09
        elif availability >= 99.0:
            return 0.6 + 0.3 * (availability - 99.0) / 0.9
        else:
            return 0.6 * availability / 99.0
    
    def _apply_transformation(self, raw_score: float) -> float:
        """
        Applica trasformazione non-lineare per enfatizzare differenze
        Usa funzione logistica modificata
        """
        # Parametri della curva sigmoidale
        k = 10  # Steepness
        x0 = 0.5  # Midpoint
        
        # Logistic function
        transformed = 1 / (1 + math.exp(-k * (raw_score - x0)))
        
        # Scala per evitare estremi
        return 0.1 + 0.8 * transformed
    
    def _calculate_confidence(self, metrics: GISTMetrics) -> Tuple[int, int]:
        """
        Calcola intervallo di confidenza basato su data quality
        """
        # In produzione: basato su data freshness, coverage, etc.
        base_confidence = 0.95
        margin = 50  # +/- 50 punti
        
        return (-margin, +margin)
    
    def _score_to_rating(self, score: int) -> str:
        """Converte score in rating letter-based"""
        if score >= 900:
            return "A+"
        elif score >= 850:
            return "A"
        elif score >= 800:
            return "A-"
        elif score >= 750:
            return "B+"
        elif score >= 700:
            return "B"
        elif score >= 650:
            return "B-"
        elif score >= 600:
            return "C+"
        elif score >= 550:
            return "C"
        elif score >= 500:
            return "C-"
        elif score >= 450:
            return "D"
        else:
            return "F"
    
    def _score_to_maturity(self, score: int) -> str:
        """Converte score in maturity level"""
        if score >= 850:
            return "Optimized"
        elif score >= 700:
            return "Managed"
        elif score >= 550:
            return "Defined"
        elif score >= 400:
            return "Developing"
        else:
            return "Initial"
    
    def _generate_recommendations(self, dimension_scores: Dict, 
                                metrics: GISTMetrics) -> List[Dict]:
        """
        Genera raccomandazioni prioritizzate basate su score
        """
        recommendations = []
        
        # Trova dimensione più debole
        weakest_dim = min(dimension_scores.items(), key=lambda x: x[1])
        
        if weakest_dim[0] == SecurityDimension.IDENTITY_TRUST:
            if metrics.mfa_adoption_rate < 0.8:
                recommendations.append({
                    'priority': 'HIGH',
                    'area': 'Identity',
                    'action': 'Increase MFA adoption to 95%+',
                    'impact': '+50-80 GIST points',
                    'effort': 'Medium'
                })
        
        elif weakest_dim[0] == SecurityDimension.NETWORK_ISOLATION:
            if metrics.micro_segmentation_coverage < 0.7:
                recommendations.append({
                    'priority': 'HIGH', 
                    'area': 'Network',
                    'action': 'Expand micro-segmentation coverage',
                    'impact': '+40-60 GIST points',
                    'effort': 'High'
                })
        
        elif weakest_dim[0] == SecurityDimension.THREAT_RESILIENCE:
            if metrics.mean_time_to_detect > 60:
                recommendations.append({
                    'priority': 'CRITICAL',
                    'area': 'Detection',
                    'action': 'Deploy advanced threat detection',
                    'impact': '+60-100 GIST points',
                    'effort': 'High'
                })
        
        # Aggiungi quick wins
        if metrics.automated_response_rate < 0.5:
            recommendations.append({
                'priority': 'MEDIUM',
                'area': 'Automation',
                'action': 'Increase response automation',
                'impact': '+30-40 GIST points',
                'effort': 'Low'
            })
        
        return sorted(recommendations, 
                     key=lambda x: {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2}[x['priority']])
    
    def _identify_risk_indicators(self, metrics: GISTMetrics, 
                                dimension_scores: Dict) -> List[str]:
        """Identifica indicatori di rischio critici"""
        risks = []
        
        if metrics.avg_trust_score < 0.5:
            risks.append("Low average trust score indicates authentication weaknesses")
        
        if metrics.mean_time_to_detect > 1440:  # >24 hours
            risks.append("Extended detection time leaves attacks undetected")
        
        if metrics.network_isolation_effectiveness < 0.3:
            risks.append("Poor network isolation enables lateral movement")
        
        if metrics.encryption_at_rest_coverage < 0.5:
            risks.append("Insufficient encryption exposes sensitive data")
        
        if dimension_scores[SecurityDimension.ADAPTIVE_RESPONSE] < 0.4:
            risks.append("Low adaptive response capability")
        
        return risks[:3]  # Top 3 risks
    
    def _calculate_trend(self, current_score: int) -> str:
        """Calcola trend (richiede historical data)"""
        # In produzione: confronta con storia
        return "stable"  # Placeholder
    
    def _calculate_percentile(self, score: int) -> int:
        """
        Calcola percentile rispetto a peer organizations
        Basato su distribuzione empirica di score
        """
        # Distribuzione empirica (normale con mean=650, std=120)
        mean = 650
        std = 120
        
        from scipy import stats
        percentile = stats.norm.cdf(score, mean, std) * 100
        
        return int(percentile)

class GISTScoreDashboard:
    """
    Visualizzazione e reporting del GIST Score
    """
    
    def __init__(self):
        self.calculator = GISTScoreCalculator()
    
    def generate_score_report(self, metrics: GISTMetrics) -> str:
        """Genera report testuale del GIST Score"""
        result = self.calculator.calculate_gist_score(metrics)
        
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║                     GIST SCORE REPORT                        ║
╚══════════════════════════════════════════════════════════════╝

Overall GIST Score: {result['gist_score']} ({result['security_rating']})
Maturity Level: {result['maturity_level']}
Percentile: {result['benchmark_percentile']}th
Confidence Interval: {result['gist_score']}{result['confidence_interval'][0]:+d} to {result['gist_score']}{result['confidence_interval'][1]:+d}

═══════════════════════════════════════════════════════════════
DIMENSION SCORES
═══════════════════════════════════════════════════════════════
"""
        
        for dim, score in result['dimension_scores'].items():
            bar_length = int(score / 5)  # 20 chars max
            bar = '█' * bar_length + '░' * (20 - bar_length)
            report += f"{dim:.<30} {bar} {score:>5.1f}%\n"
        
        report += f"""
═══════════════════════════════════════════════════════════════
KEY RISK INDICATORS
═══════════════════════════════════════════════════════════════
"""
        for i, risk in enumerate(result['risk_indicators'], 1):
            report += f"{i}. ⚠️  {risk}\n"
        
        report += f"""
═══════════════════════════════════════════════════════════════
PRIORITIZED RECOMMENDATIONS  
═══════════════════════════════════════════════════════════════
"""
        for rec in result['recommendations']:
            icon = {'CRITICAL': '🔴', 'HIGH': '🟡', 'MEDIUM': '🟢'}[rec['priority']]
            report += f"\n{icon} [{rec['priority']}] {rec['area']}\n"
            report += f"   Action: {rec['action']}\n"
            report += f"   Impact: {rec['impact']} | Effort: {rec['effort']}\n"
        
        return report
    
    def calculate_improvement_potential(self, current_metrics: GISTMetrics,
                                      planned_improvements: Dict) -> Dict:
        """
        Calcola GIST Score potenziale dopo improvements
        """
        # Clone metrics
        improved_metrics = GISTMetrics(**current_metrics.__dict__)
        
        # Applica improvements
        for metric, improvement in planned_improvements.items():
            if hasattr(improved_metrics, metric):
                current_value = getattr(improved_metrics, metric)
                if 'relative' in improvement:
                    new_value = current_value * (1 + improvement['relative'])
                else:
                    new_value = improvement['absolute']
                setattr(improved_metrics, metric, max(0, min(1, new_value)))
        
        # Calcola nuovo score
        current_result = self.calculator.calculate_gist_score(current_metrics)
        improved_result = self.calculator.calculate_gist_score(improved_metrics)
        
        return {
            'current_score': current_result['gist_score'],
            'projected_score': improved_result['gist_score'],
            'improvement': improved_result['gist_score'] - current_result['gist_score'],
            'current_rating': current_result['security_rating'],
            'projected_rating': improved_result['security_rating'],
            'dimension_improvements': {
                dim: improved_result['dimension_scores'][dim] - current_result['dimension_scores'][dim]
                for dim in current_result['dimension_scores']
            }
        }


# ============== ESEMPIO E TEST ==============

def test_gist_score():
    """Test e dimostrazione del calcolo GIST Score"""
    
    # Metriche di esempio per organizzazione GDO media
    sample_metrics = GISTMetrics(
        # Identity
        avg_trust_score=0.72,
        mfa_adoption_rate=0.65,
        privileged_account_monitoring=0.80,
        identity_anomaly_detection_rate=0.55,
        
        # Network
        micro_segmentation_coverage=0.40,
        east_west_traffic_inspection=0.30,
        network_isolation_effectiveness=0.60,
        segment_compromise_containment=0.70,
        
        # Threat
        mean_time_to_detect=120,  # 2 ore
        mean_time_to_respond=240,  # 4 ore
        automated_response_rate=0.35,
        threat_hunting_maturity=0.45,
        
        # Data
        encryption_at_rest_coverage=0.85,
        encryption_in_transit_coverage=0.95,
        data_classification_accuracy=0.60,
        dlp_effectiveness=0.50,
        
        # Resilience
        availability_percentage=99.5,
        recovery_time_objective=180,  # 3 ore
        backup_verification_rate=0.90,
        incident_containment_rate=0.75
    )
    
    # Calcola score
    dashboard = GISTScoreDashboard()
    
    print("=== GIST SCORE CALCULATION DEMO ===\n")
    print(dashboard.generate_score_report(sample_metrics))
    
    # Simula improvements
    print("\n=== IMPROVEMENT ANALYSIS ===")
    
    planned_improvements = {
        'mfa_adoption_rate': {'absolute': 0.95},
        'micro_segmentation_coverage': {'absolute': 0.80},
        'mean_time_to_detect': {'absolute': 30},
        'automated_response_rate': {'absolute': 0.75}
    }
    
    improvement = dashboard.calculate_improvement_potential(
        sample_metrics, planned_improvements
    )
    
    print(f"\nCurrent GIST Score: {improvement['current_score']} ({improvement['current_rating']})")
    print(f"Projected GIST Score: {improvement['projected_score']} ({improvement['projected_rating']})")
    print(f"Total Improvement: +{improvement['improvement']} points")
    
    print("\nDimension Improvements:")
    for dim, imp in improvement['dimension_improvements'].items():
        if imp > 0:
            print(f"  {dim}: +{imp:.1f}%")

if __name__ == "__main__":
    test_gist_score()