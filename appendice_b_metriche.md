# Appendice B - Strumenti di Misurazione e Metriche Dettagliate

## B.1 Framework di Misurazione GIST

### B.1.1 Struttura Gerarchica delle Metriche

Il framework GIST utilizza un sistema di metriche gerarchico a tre livelli:

```
Livello 1: GIST Score Complessivo (0-1)
├── Livello 2: Componenti Principali (P, A, S, C)
│   ├── Livello 3: Sub-metriche per Componente
│   │   └── Livello 4: Indicatori Operativi Misurabili
```

### B.1.2 Calcolo del GIST Score

**Formula Generale**:
```
GIST = [(P^0.15 × A^0.35 × S^0.30 × C^0.20)^(1/0.87)] × K_GDO × (1 + I)
```

**Parametri**:
- γ = 0.87 (fattore di normalizzazione non-lineare)
- K_GDO = 1.23 (coefficiente settore GDO)
- I ∈ [0, 0.5] (fattore innovazione)

**Procedura di Calcolo**:
1. Normalizzare ogni sub-metrica su scala 0-1
2. Calcolare score componenti (P, A, S, C)
3. Applicare pesi esponenziali
4. Normalizzare con γ
5. Applicare moltiplicatori K_GDO e I

## B.2 Componente P: Physical Infrastructure

### B.2.1 Power Redundancy (P₁) - Peso: 0.25

**Definizione**: Capacità del sistema di alimentazione di mantenere operatività in caso di guasto

**Formula**:
```
P₁ = (MTBF_actual / MTBF_target) × (1 - PDU_failure_rate) × Redundancy_factor
```

**Misurazione**:
- MTBF_actual: Calcolato su rolling 12 mesi
- MTBF_target: 52,560 ore (6 anni) per N+1
- PDU_failure_rate: Eventi/anno normalizzati
- Redundancy_factor: {1.0 per N+1, 1.5 per N+2, 0.5 per N+0}

**Strumenti di Raccolta**:
```python
# Script monitoraggio UPS
def calculate_power_redundancy():
    uptime_seconds = get_ups_uptime()
    failure_events = count_power_failures()
    mtbf_hours = uptime_seconds / 3600 / max(failure_events, 1)
    
    redundancy = get_redundancy_config()
    rf = {0: 0.5, 1: 1.0, 2: 1.5}.get(redundancy, 1.0)
    
    p1 = min((mtbf_hours / 52560) * (1 - failure_rate) * rf, 1.0)
    return p1
```

### B.2.2 Cooling Efficiency (P₂) - Peso: 0.20

**Definizione**: Efficienza del sistema di raffreddamento misurata attraverso PUE parziale

**Formula**:
```
P₂ = 2.0 - PUE_cooling / (1 + ΔT_variance)
```

**Parametri**:
- PUE_cooling: Power Usage Effectiveness componente cooling
- ΔT_variance: Deviazione standard temperatura su 24h
- Target: PUE < 1.4, ΔT < 2°C

**Protocollo di Misurazione**:
1. Sensori temperatura ogni 5m² in sala server
2. Letture ogni 60 secondi
3. Calcolo PUE ogni 15 minuti
4. Aggregazione giornaliera con media mobile

### B.2.3 Network Reliability (P₃) - Peso: 0.30

**Definizione**: Disponibilità e performance della connettività di rete

**Formula**:
```
P₃ = 0.4×Availability + 0.3×Bandwidth_util + 0.3×Latency_score
```

**Componenti**:
```
Availability = (Uptime_minutes / Total_minutes) × Multi_path_factor
Bandwidth_util = 1 - (Peak_usage / Total_capacity)^2
Latency_score = 1 - (Actual_latency / Target_latency)
```

**Thresholds**:
- Availability target: 99.95%
- Bandwidth headroom: >40%
- Latency target: <20ms intra-site, <50ms inter-site

### B.2.4 Physical Security (P₄) - Peso: 0.25

**Definizione**: Livello di protezione fisica dell'infrastruttura IT

**Checklist Valutazione** (0-10 punti per categoria):

| Categoria | Peso | Criteri di Valutazione |
|-----------|------|------------------------|
| Access Control | 30% | Biometria, badge, mantrap |
| Surveillance | 25% | CCTV coverage, retention, AI analytics |
| Environmental | 25% | Fumo, acqua, temperatura, movimento |
| Compliance | 20% | Certificazioni, audit, procedure |

**Scoring**:
```
P₄ = Σ(Score_i × Weight_i) / 10
```

## B.3 Componente A: Architectural Maturity

### B.3.1 Cloud Adoption (A₁) - Peso: 0.35

**Definizione**: Grado di adozione e maturità delle tecnologie cloud

**Modello di Maturità Cloud** (5 livelli):

```
Livello 1 (0.0-0.2): Nessun cloud, tutto on-premise
Livello 2 (0.2-0.4): IaaS per workload non critici
Livello 3 (0.4-0.6): Hybrid cloud con disaster recovery
Livello 4 (0.6-0.8): Cloud-first, multi-cloud strategy
Livello 5 (0.8-1.0): Cloud-native, serverless adoption
```

**Metriche Quantitative**:
- % Workload in cloud: W_cloud / W_total
- Elasticità: Auto-scaling events / Peak events
- Ottimizzazione costi: (Provisioned - Used) / Provisioned

**Formula Composita**:
```
A₁ = 0.5×Cloud_percentage + 0.3×Elasticity_score + 0.2×Cost_optimization
```

### B.3.2 Automation Level (A₂) - Peso: 0.25

**Definizione**: Grado di automazione dei processi IT

**Categorie di Automazione**:

| Processo | Peso | KPI Target | Misurazione |
|----------|------|------------|-------------|
| Provisioning | 25% | <30 min | Time to deploy |
| Patching | 20% | <48h critical | Patch latency |
| Monitoring | 20% | 100% coverage | Systems monitored |
| Backup | 15% | RPO <4h | Actual vs target |
| Incident Response | 20% | <15 min detect | Detection time |

**Infrastructure as Code Metrics**:
```
IaC_coverage = (Resources_managed_by_code / Total_resources) × 100
Change_automation = Automated_changes / Total_changes
Drift_detection = Resources_in_compliance / Total_managed
```

### B.3.3 API Maturity (A₃) - Peso: 0.20

**Richardson Maturity Model Mapping**:

| Level | Score | Caratteristiche | Indicatori |
|-------|-------|----------------|------------|
| 0 | 0.0-0.25 | SOAP/RPC | Single endpoint |
| 1 | 0.25-0.50 | Resources | Multiple URIs |
| 2 | 0.50-0.75 | HTTP Verbs | GET, POST, PUT, DELETE |
| 3 | 0.75-1.0 | HATEOAS | Self-descriptive |

**Metriche API**:
```
API_availability = Uptime / Total_time
API_performance = Requests_within_SLA / Total_requests
API_adoption = Internal_consumers × External_consumers / Total_possible
```

### B.3.4 DevOps Practices (A₄) - Peso: 0.20

**DORA Metrics Implementation**:

```
1. Deployment Frequency (DF)
   Target: Daily per applicazione critica
   Score: log(deployments_per_day + 1) / log(2)

2. Lead Time for Changes (LT)
   Target: <24 ore
   Score: 1 - (actual_hours / 168)  # 168h = 1 week max

3. Mean Time to Recovery (MTTR)
   Target: <1 ora
   Score: 1 - (actual_minutes / 240)  # 240min = 4h max

4. Change Failure Rate (CFR)
   Target: <5%
   Score: 1 - (failures / deployments)
```

**Formula DevOps**:
```
A₄ = 0.3×DF + 0.3×(1-LT) + 0.3×(1-MTTR) + 0.1×(1-CFR)
```

## B.4 Componente S: Security Posture

### B.4.1 Zero Trust Implementation (S₁) - Peso: 0.30

**Maturity Model Zero Trust** (NIST SP 800-207):

| Pillar | Peso | Metriche | Target |
|--------|------|----------|--------|
| Identity | 20% | MFA coverage | 100% |
| Device | 20% | Managed devices | >95% |
| Network | 20% | Micro-segmentation | >80% |
| Application | 20% | RBAC implementation | 100% |
| Data | 20% | Encryption at rest/transit | 100% |

**Zero Trust Score Calculation**:
```python
def calculate_zero_trust_score():
    identity = get_mfa_coverage() * get_sso_adoption()
    device = get_managed_devices() / get_total_devices()
    network = count_microsegments() / count_total_segments()
    app = get_rbac_apps() / get_total_apps()
    data = get_encrypted_data() / get_total_sensitive_data()
    
    weights = [0.2, 0.2, 0.2, 0.2, 0.2]
    scores = [identity, device, network, app, data]
    
    return sum(w * s for w, s in zip(weights, scores))
```

### B.4.2 Threat Detection (S₂) - Peso: 0.25

**MITRE ATT&CK Coverage Analysis**:

```
Coverage = Tactics_detected / Total_tactics (14)
Depth = Σ(Techniques_per_tactic) / Σ(Total_techniques_per_tactic)
Speed = 1 - (Mean_detection_time / 86400)  # 24h max
```

**Composite Score**:
```
S₂ = 0.4×Coverage + 0.3×Depth + 0.3×Speed
```

**Detection Metrics by Source**:

| Source | Weight | Metric | Threshold |
|--------|--------|--------|-----------|
| Network | 25% | IDS alerts investigated | >90% |
| Endpoint | 25% | EDR coverage | >95% |
| Identity | 25% | Anomalous logins detected | >80% |
| Application | 25% | WAF effectiveness | >85% |

### B.4.3 Incident Response (S₃) - Peso: 0.25

**NIST Incident Response Lifecycle Metrics**:

```
1. Preparation (20%)
   - Playbooks coverage = Scenarios_documented / Critical_scenarios
   - Team readiness = Trained_staff / Total_staff

2. Detection & Analysis (30%)
   - Detection rate = True_positives / (True_positives + False_negatives)
   - Analysis speed = 1 - (Mean_analysis_time / 3600)  # 1h target

3. Containment (30%)
   - Containment time = 1 - (Mean_containment / 14400)  # 4h max
   - Containment effectiveness = Systems_contained / Systems_affected

4. Recovery (20%)
   - Recovery time = 1 - (Mean_recovery / 86400)  # 24h max
   - Recovery completeness = Services_restored / Services_affected
```

### B.4.4 Security Training (S₄) - Peso: 0.20

**Training Effectiveness Model**:

```
Knowledge = (Post_test_score - Pre_test_score) / (100 - Pre_test_score)
Retention = Score_90days / Score_immediate
Application = Security_incidents_prevented / Employee_count
Engagement = Completed_training / Assigned_training
```

**Composite Training Score**:
```
S₄ = 0.3×Knowledge + 0.2×Retention + 0.3×Application + 0.2×Engagement
```

## B.5 Componente C: Compliance Integration

### B.5.1 Standards Overlap Optimization (C₁) - Peso: 0.40

**Overlap Quantification Matrix**:

```
Controlli Totali:
- PCI-DSS 4.0: 389 requirements
- GDPR: 99 articles → 344 technical controls
- NIS2: 21 measures → 156 technical controls

Overlap Matrix:
            PCI     GDPR    NIS2
PCI         389     173     156
GDPR        173     344     194
NIS2        156     194     156

Common to all: 128 controls
```

**Integration Efficiency**:
```
C₁ = (Implemented_common / Total_common) × Deduplication_factor
Deduplication_factor = 1 - (Unique_implemented / Total_required)
```

### B.5.2 Automation Compliance (C₂) - Peso: 0.30

**Automation Maturity Levels**:

| Level | Score | Caratteristiche | Coverage Target |
|-------|-------|----------------|-----------------|
| Manual | 0.0-0.2 | Spreadsheets, email | <20% |
| Assisted | 0.2-0.4 | Tools, dashboards | 20-40% |
| Automated | 0.4-0.6 | Scheduled scans | 40-60% |
| Orchestrated | 0.6-0.8 | Workflow integration | 60-80% |
| Autonomous | 0.8-1.0 | Self-remediation | >80% |

**Metrics**:
```
Evidence_automation = Auto_collected / Total_evidence
Control_automation = Auto_tested / Total_controls  
Remediation_automation = Auto_fixed / Total_findings
Report_automation = Auto_generated / Total_reports
```

### B.5.3 Audit Readiness (C₃) - Peso: 0.30

**Audit Readiness Index**:

```
Documentation = Current_docs / Required_docs
Evidence_freshness = Σ(1 - Age_days/365) / Count_evidence
Finding_closure = Closed_findings / Total_findings
Continuous_monitoring = Monitored_controls / Total_controls
```

**Composite Score**:
```
C₃ = 0.25×Documentation + 0.25×Evidence_freshness + 
     0.25×Finding_closure + 0.25×Continuous_monitoring
```

## B.6 Strumenti di Raccolta Automatizzata

### B.6.1 Infrastructure Monitoring Stack

```yaml
# docker-compose.yml per monitoring stack
version: '3.8'
services:
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
    
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=secure_password
    
  node_exporter:
    image: prom/node-exporter:latest
    ports:
      - "9100:9100"
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
```

### B.6.2 Security Scanning Automation

```python
# security_scanner.py
import nmap
import requests
from datetime import datetime
import json

class SecurityScanner:
    def __init__(self, targets):
        self.targets = targets
        self.nm = nmap.PortScanner()
        
    def calculate_assa_score(self):
        """Calculate Aggregated System Surface Attack score"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'scans': []
        }
        
        for target in self.targets:
            # Port scanning
            self.nm.scan(target, '1-65535', '-sV')
            open_ports = len(self.nm[target]['tcp'].keys())
            
            # Service enumeration
            services = self.enumerate_services(target)
            
            # Vulnerability assessment
            vulns = self.check_vulnerabilities(target)
            
            # Calculate scores
            port_score = min(open_ports / 100, 1.0) * 30
            service_score = min(len(services) / 50, 1.0) * 40
            vuln_score = min(vulns['critical'] * 10 + vulns['high'] * 5, 30)
            
            assa = port_score + service_score + vuln_score
            
            results['scans'].append({
                'target': target,
                'open_ports': open_ports,
                'services': len(services),
                'vulnerabilities': vulns,
                'assa_score': assa
            })
            
        return results
```

### B.6.3 Compliance Automation Framework

```python
# compliance_automation.py
class ComplianceAutomation:
    def __init__(self, standards=['PCI-DSS', 'GDPR', 'NIS2']):
        self.standards = standards
        self.control_library = self.load_control_library()
        
    def assess_compliance(self, organization_id):
        """Automated compliance assessment"""
        results = {
            'org_id': organization_id,
            'timestamp': datetime.now(),
            'standards': {}
        }
        
        for standard in self.standards:
            controls = self.control_library[standard]
            
            total_controls = len(controls)
            passed_controls = 0
            automated_controls = 0
            
            for control in controls:
                # Check if control is automated
                if control['automation_possible']:
                    automated_controls += 1
                    result = self.execute_automated_check(control)
                else:
                    result = self.get_manual_attestation(control)
                
                if result['status'] == 'PASS':
                    passed_controls += 1
                    
            results['standards'][standard] = {
                'total_controls': total_controls,
                'passed_controls': passed_controls,
                'compliance_percentage': passed_controls / total_controls * 100,
                'automation_percentage': automated_controls / total_controls * 100
            }
            
        return results
```

## B.7 Procedure di Validazione e Calibrazione

### B.7.1 Validazione delle Metriche

**Processo di Validazione** (trimestrale):

1. **Accuracy Check**
   - Confronto con misurazioni manuali (campione 10%)
   - Deviazione accettabile: ±5%
   - Azione correttiva se deviazione >5%

2. **Completeness Verification**
   - Controllo copertura: >95% sistemi monitorati
   - Missing data analysis
   - Root cause per gap >5%

3. **Consistency Analysis**
   - Cross-validation tra fonti multiple
   - Trend analysis per anomalie
   - Statistical process control (SPC)

### B.7.2 Calibrazione degli Strumenti

**Calendario Calibrazione**:

| Strumento | Frequenza | Metodo | Responsabile |
|-----------|-----------|--------|--------------|
| Sensori temperatura | Mensile | Confronto termometro certificato | Facility |
| Network monitoring | Settimanale | Synthetic transactions | Network Team |
| Security scanners | Quindicinale | Known vulnerability test | Security Team |
| Power meters | Trimestrale | Calibrazione professionale | Vendor |

### B.7.3 Inter-rater Reliability

Per metriche che richiedono valutazione umana:

```
Cohen's Kappa = (P_o - P_e) / (1 - P_e)

Dove:
P_o = Proporzione di accordo osservato
P_e = Proporzione di accordo atteso per caso

Target: κ > 0.80 (accordo sostanziale)
```

## B.8 Dashboard e Reporting

### B.8.1 Real-time Dashboard Structure

```
┌─────────────────────────────────────────────┐
│           GIST SCORE: 0.67                  │
│    ▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░  67%              │
├─────────────┬─────────────┬─────────────────┤
│ Physical    │ Architecture │ Security        │
│ P: 0.72     │ A: 0.65     │ S: 0.61        │
│ ▓▓▓▓▓▓▓░░░ │ ▓▓▓▓▓▓░░░░ │ ▓▓▓▓▓▓░░░░    │
├─────────────┴─────────────┴─────────────────┤
│ Compliance: 0.69                            │
│ ▓▓▓▓▓▓▓░░░░                               │
├─────────────────────────────────────────────┤
│ Trend (30d): ↑ +0.08  │ Target: 0.75       │
└─────────────────────────────────────────────┘
```

### B.8.2 Automated Reporting Templates

**Executive Summary Report** (mensile):
- GIST score e trend
- Top 3 miglioramenti
- Top 3 aree critiche
- Confronto con peer group
- Raccomandazioni prioritizzate

**Technical Deep Dive** (settimanale):
- Dettaglio per componente
- Anomalie rilevate
- Azioni correttive in corso
- Metriche di dettaglio
- Proiezioni forward-looking

### B.8.3 Alert Thresholds

| Metrica | Warning | Critical | Azione |
|---------|---------|----------|--------|
| GIST Score | <0.60 | <0.50 | Executive escalation |
| Availability | <99.9% | <99.5% | Incident response |
| ASSA Score | >60 | >75 | Security team alert |
| Compliance | <85% | <80% | Remediation plan |

---

**Note Tecniche**:
- Tutti gli script sono disponibili nel repository Git del progetto
- Documentazione API completa: /docs/api/metrics/v2
- Supporto tecnico: metrics-support@gdo-security.it
- Ultimo aggiornamento calibrazione: 30/01/2024