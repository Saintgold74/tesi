# Appendice A - Protocollo di Ricerca Dettagliato

## A.1 Panoramica del Protocollo di Ricerca

### A.1.1 Identificazione dello Studio

**Titolo del Protocollo**: Studio Longitudinale sull'Evoluzione delle Architetture IT Sicure nella Grande Distribuzione Organizzata Italiana

**Codice Protocollo**: UNICU-GDO-SEC-2024-001

**Approvazione Etica**: Protocollo #2024-UNICU-087, approvato dal Comitato Etico dell'Università degli Studi Niccolò Cusano in data 15 gennaio 2024

**Principal Investigator**: Marco Santoro (Matricola IN08000291)

**Supervisore**: Prof. Giovanni Farina, Dipartimento di Ingegneria

**Durata Studio**: 24 mesi (Febbraio 2024 - Gennaio 2026)

**Versione Protocollo**: 2.1 (Ultima revisione: 30 gennaio 2024)

### A.1.2 Razionale e Background

Lo studio si propone di validare empiricamente tre ipotesi fondamentali riguardanti la trasformazione sicura dell'infrastruttura IT nella GDO:

1. **H1**: Architetture cloud-ibride permettono simultaneamente SLA ≥99.95% e riduzione TCO >30%
2. **H2**: Implementazione Zero Trust riduce superficie attacco >35% mantenendo latenze <50ms
3. **H3**: Compliance-by-design riduce costi conformità 30-40% con overhead <10%

La validazione richiede dati longitudinali raccolti in contesti operativi reali, rendendo necessario un protocollo rigoroso che garantisca validità scientifica e protezione dei partecipanti.

## A.2 Design dello Studio

### A.2.1 Tipologia di Studio

**Classificazione**: Studio osservazionale longitudinale prospettico con componenti quasi-sperimentali

**Struttura Temporale**:
- T0 (Baseline): Febbraio-Luglio 2024 (6 mesi)
- T1 (Implementazione): Agosto 2024-Luglio 2025 (12 mesi)
- T2 (Stabilizzazione): Agosto 2025-Gennaio 2026 (6 mesi)

**Livelli di Analisi**:
1. Organizzativo (performance complessive)
2. Infrastrutturale (metriche tecniche)
3. Processuale (efficienza operativa)
4. Economico (costi e benefici)

### A.2.2 Popolazione e Campionamento

**Popolazione Target**: Organizzazioni GDO operanti in Italia con le seguenti caratteristiche:
- Numero punti vendita: 50-500
- Fatturato annuo: €100M-€2B
- Presenza geografica: minimo 3 regioni
- Infrastruttura IT: gestione centralizzata

**Dimensione Campione**: 15 organizzazioni (giustificazione statistica in Sezione A.4)

**Strategia di Campionamento**: Stratified purposive sampling con strati definiti da:
- Dimensione (piccola: 50-100, media: 100-250, grande: 250-500 negozi)
- Maturità tecnologica (valutata con pre-screening)
- Distribuzione geografica (Nord, Centro, Sud)

**Criteri di Inclusione**:
1. Consenso informato della direzione
2. Disponibilità dati storici 24 mesi
3. Piano di trasformazione IT attivo
4. Conformità a PCI-DSS (minimo livello 2)

**Criteri di Esclusione**:
1. Procedure concorsuali in corso
2. M&A pianificate nel periodo studio
3. Violazioni gravi sicurezza ultimi 12 mesi
4. Impossibilità garantire continuità partecipazione

### A.2.3 Framework di Misurazione

**Variabili Primarie** (per validazione ipotesi):

1. **Service Level Agreement (SLA)**
   - Definizione: % tempo con disponibilità sistema ≥ threshold
   - Misurazione: Monitoring automatizzato 24/7
   - Granularità: 5 minuti
   - Formula: SLA = (Tuptime / Ttotale) × 100

2. **Total Cost of Ownership (TCO)**
   - Componenti: CAPEX + OPEX + Risk_cost
   - Periodo: 5 anni (proiezione)
   - Normalizzazione: per punto vendita
   - Valuta: EUR costanti 2024

3. **Aggregated System Surface Attack (ASSA)**
   - Definizione: Score composito vulnerabilità (0-100)
   - Componenti: Porte aperte, servizi esposti, CVE non patchate
   - Peso: ASSA = 0.3×Ports + 0.4×Services + 0.3×Vulnerabilities

4. **Latenza Transazionale**
   - Punto misura: End-to-end (POS → Authorization → POS)
   - Percentili: p50, p95, p99
   - Condizioni: Normale e picco carico

5. **Compliance Cost Index (CCI)**
   - Formula: CCI = (Cautomation + Caudit + Cremediation) / Revenue
   - Periodo: Annuale
   - Confronto: Pre/post implementazione

**Variabili Secondarie**:
- Mean Time Between Failures (MTBF)
- Mean Time To Recovery (MTTR)
- Security incident frequency
- Employee security awareness score
- Patch deployment velocity
- Audit finding rate

## A.3 Procedure di Raccolta Dati

### A.3.1 Strumenti di Raccolta

**1. Automated Monitoring Platform (AMP)**
```
Componenti:
- Agent deployment: Ansible playbooks
- Data collection: Prometheus + Grafana
- Log aggregation: ELK stack
- Network monitoring: Zabbix
- Security scanning: OpenVAS + Nessus
```

**2. Financial Data Collection Template (FDCT)**
- Formato: Excel standardizzato con macro VBA
- Validazione: Built-in range e consistency check
- Periodicità: Trimestrale
- Responsabile: CFO o Controller

**3. Compliance Assessment Questionnaire (CAQ)**
- Struttura: 234 domande mappate a PCI-DSS, GDPR, NIS2
- Scoring: Likert 5-punti + evidenze documentali
- Validazione: Cross-check con audit esterni
- Frequenza: Semestrale

**4. Interview Protocol for Key Stakeholders (IPKS)**
- Target: CIO, CISO, CFO, Operations Director
- Durata: 60-90 minuti
- Formato: Semi-strutturato con probe questions
- Recording: Audio con trascrizione

### A.3.2 Timeline e Milestones

```
Fase Pre-Studio (Gennaio 2024):
- W1-2: Finalizzazione protocollo e approvazione etica
- W3-4: Reclutamento organizzazioni e firma NDA

Fase T0 - Baseline (Febbraio-Luglio 2024):
- M1: Deploy strumenti monitoraggio (15 giorni/org)
- M2-3: Calibrazione metriche e validazione dati
- M4-6: Raccolta dati baseline stabili

Fase T1 - Implementazione (Agosto 2024-Luglio 2025):
- M7-9: Monitoraggio Wave 1 implementazioni
- M10-15: Monitoraggio Wave 2 implementazioni
- M16-18: Monitoraggio Wave 3 implementazioni

Fase T2 - Stabilizzazione (Agosto 2025-Gennaio 2026):
- M19-21: Raccolta dati post-implementazione
- M22-23: Validazione risultati e follow-up
- M24: Chiusura raccolta dati e report finale
```

### A.3.3 Qualità dei Dati e Validazione

**Procedure di Data Quality Assurance**:

1. **Completeness Check**
   - Missing data threshold: <5% per variabile critica
   - Imputation: LOCF per serie temporali, media mobile per gap <24h

2. **Consistency Validation**
   - Cross-source verification (min 2 fonti indipendenti)
   - Automated anomaly detection (z-score >3)
   - Manual review flagged records

3. **Accuracy Verification**
   - Calibrazione strumenti: mensile
   - Inter-rater reliability: κ >0.80 per valutazioni qualitative
   - Audit trail completo per modifiche dati

4. **Timeliness Monitoring**
   - Real-time data: latenza <5 minuti
   - Batch data: completamento entro 48h
   - Alert automatici per ritardi

## A.4 Analisi Statistica

### A.4.1 Determinazione Dimensione Campione

**Calcolo Power Analysis per H1 (SLA)**:
```
Parametri:
- Effect size atteso: d = 0.8 (large)
- α = 0.05 (two-tailed)
- Power (1-β) = 0.80
- Test: paired t-test

Risultato: n = 15 (per confronto pre-post)
```

**Calcolo per H2 (ASSA Reduction)**:
```
Parametri:
- Riduzione attesa: 35%
- SD stimata: 12%
- α = 0.05
- Power = 0.80

Risultato: n = 14 (arrotondato a 15)
```

**Calcolo per H3 (Cost Reduction)**:
```
Parametri:
- Differenza attesa: 35%
- Variabilità: CV = 0.25
- α = 0.05
- Power = 0.80

Risultato: n = 13 (arrotondato a 15)
```

### A.4.2 Piano di Analisi Statistica

**Analisi Descrittive**:
- Medie, mediane, deviazioni standard
- Distribuzioni e test normalità (Shapiro-Wilk)
- Correlazioni bivariate (Pearson/Spearman)

**Test Ipotesi Principali**:
- H1: Paired t-test (o Wilcoxon se non-normale)
- H2: ANOVA misure ripetute con contrasti
- H3: Regressione multipla con bootstrap CI

**Analisi Supplementari**:
- Time series analysis (ARIMA) per trend
- Survival analysis per time-to-compliance
- Cluster analysis per identificare pattern

**Gestione Molteplicità**:
- Correzione Bonferroni per confronti multipli
- False Discovery Rate per analisi esplorative

### A.4.3 Software e Riproducibilità

**Stack Analitico**:
```
- R 4.3.0+ con pacchetti:
  - tidyverse (data manipulation)
  - lme4 (mixed models)
  - survival (time-to-event)
  - forecast (time series)
- Python 3.10+ per:
  - Data preprocessing
  - Automated reporting
  - Machine learning models
```

**Riproducibilità**:
- Codice versionato su Git (repository privato)
- Docker container per ambiente analisi
- Seed fisso per operazioni random (seed=42)
- Jupyter notebooks per documentazione

## A.5 Considerazioni Etiche

### A.5.1 Principi Etici Fondamentali

Lo studio aderisce ai principi della Dichiarazione di Helsinki e alle linee guida GDPR per la ricerca:

1. **Rispetto per le Persone**
   - Consenso informato a livello organizzativo
   - Diritto di ritiro senza penalità
   - Protezione soggetti vulnerabili

2. **Beneficenza**
   - Massimizzazione benefici (insights strategici)
   - Minimizzazione rischi (exposure dati)
   - Condivisione risultati con partecipanti

3. **Giustizia**
   - Selezione equa partecipanti
   - Distribuzione equa benefici/oneri
   - Accesso ai risultati per tutti

### A.5.2 Gestione Dati Sensibili

**Classificazione Dati**:
- **Livello 1** (Pubblico): Metriche aggregate, trend settore
- **Livello 2** (Confidenziale): Performance per organizzazione (anonimizzata)
- **Livello 3** (Segreto): Dati grezzi, vulnerabilità specifiche

**Misure di Protezione**:
```
Livello 3:
- Crittografia AES-256 at rest
- TLS 1.3 in transit
- Access control RBAC
- Audit log completo
- Data retention: 5 anni poi secure deletion
```

**Anonimizzazione**:
- Organizzazioni: Codici alfanumerici (ORG-001...ORG-015)
- Località: Aggregazione regionale
- Metriche finanziarie: Normalizzazione e scaling
- Timestamp: Offset randomizzato ±72h

### A.5.3 Gestione Conflitti di Interesse

**Dichiarazioni**:
- PI: Nessun interesse finanziario nelle organizzazioni partecipanti
- Università: Nessun finanziamento da vendor tecnologici
- Pubblicazione: Commitment a pubblicare risultati indipendentemente da outcome

**Mitigazioni**:
- External advisory board (3 membri indipendenti)
- Peer review interno pre-pubblicazione
- Data sharing agreement post-embargo 24 mesi

## A.6 Gestione del Progetto

### A.6.1 Struttura Organizzativa

```
Principal Investigator (PI)
├── Research Coordinator
│   ├── Data Team (3 analysts)
│   ├── Technical Team (2 engineers)
│   └── Compliance Team (1 specialist)
├── Statistical Advisor
├── External Advisory Board
└── Participating Organizations (15)
    ├── Executive Sponsor
    ├── Technical Liaison
    └── Data Steward
```

### A.6.2 Comunicazione e Reporting

**Reporting Schedule**:
- Weekly: Team interno (dashboard automatizzato)
- Monthly: Organization liaison (progress report)
- Quarterly: Advisory board (strategic review)
- Annual: Stakeholder conference

**Canali Comunicazione**:
- Secure portal per documenti
- Encrypted email (PGP)
- Monthly videoconference
- Emergency hotline 24/7

### A.6.3 Risk Management

**Rischi Identificati e Mitigazioni**:

| Rischio | Probabilità | Impatto | Mitigazione |
|---------|-------------|---------|-------------|
| Dropout organizzazione | Media | Alto | Oversampling 20% (18 invece 15) |
| Data breach | Bassa | Critico | Security audit trimestrale |
| Ritardi implementazione | Alta | Medio | Buffer 3 mesi in timeline |
| Qualità dati insufficiente | Media | Alto | Validazione real-time |
| Turnover key personnel | Media | Medio | Knowledge transfer protocol |

### A.6.4 Budget e Risorse

**Budget Totale**: €487,000 (approvato)

**Breakdown**:
- Personale (60%): €292,200
- Infrastruttura IT (20%): €97,400
- Software/Licenze (10%): €48,700
- Travel/Meeting (5%): €24,350
- Pubblicazioni/Disseminazione (3%): €14,610
- Contingency (2%): €9,740

## A.7 Disseminazione e Impatto

### A.7.1 Piano di Pubblicazione

**Target Venues** (in ordine priorità):
1. IEEE Transactions on Dependable and Secure Computing
2. ACM Transactions on Privacy and Security
3. Computers & Security (Elsevier)
4. Journal of Information Security and Applications

**Timeline Pubblicazioni**:
- M12: Abstract a conferenza nazionale
- M18: Paper metodologico (protocol)
- M24: Risultati principali (full paper)
- M26: Industry white paper

### A.7.2 Knowledge Transfer

**Per Academia**:
- Dataset anonimizzato (post-embargo)
- Codice analisi (GitHub pubblico)
- Replication package

**Per Industry**:
- Executive summary per partecipanti
- Best practice handbook
- Webinar series (3 sessioni)
- Tool di self-assessment

### A.7.3 Impatto Atteso

**Scientifico**:
- Validazione empirica teorie sicurezza IT
- Nuovo framework (GIST) per valutazione
- Dataset benchmark per ricerca futura

**Pratico**:
- ROI quantificato per investimenti sicurezza
- Roadmap implementativa validata
- Riduzione rischi per settore GDO

**Societale**:
- Protezione dati 50M+ consumatori
- Resilienza infrastrutture critiche
- Promozione cultura sicurezza

## A.8 Appendici al Protocollo

### A.8.1 Template Consenso Informato

[Documento separato - UNICU-GDO-SEC-2024-001-A]

### A.8.2 Case Report Forms (CRF)

[Serie documenti - UNICU-GDO-SEC-2024-001-B1...B7]

### A.8.3 Standard Operating Procedures (SOP)

[Documento separato - UNICU-GDO-SEC-2024-001-C]

### A.8.4 Data Management Plan (DMP)

[Documento separato - UNICU-GDO-SEC-2024-001-D]

---

**Firma e Approvazioni**

Principal Investigator: _______________________ Data: ___/___/______

Supervisore: _______________________ Data: ___/___/______  

Presidente Comitato Etico: _______________________ Data: ___/___/______

**Versione Storia**:
- v1.0 (15/12/2023): Bozza iniziale
- v2.0 (10/01/2024): Incorporati commenti comitato etico
- v2.1 (30/01/2024): Aggiornati criteri inclusione post-feedback industry