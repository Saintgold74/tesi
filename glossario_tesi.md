# Glossario dei Termini Tecnici

## A

**Aggregated System Surface Attack (ASSA)**
Score composito (0-100) che quantifica la vulnerabilità complessiva di un sistema informatico, calcolato come combinazione pesata di porte aperte (30%), servizi esposti (40%) e vulnerabilità non patchate (30%). Introdotto nel Capitolo 2, utilizzato come metrica principale per l'ipotesi H2.

**API (Application Programming Interface)**
Insieme di definizioni e protocolli per la costruzione e l'integrazione di applicazioni software. Nel contesto della tesi, la maturità API è una componente della Architectural Maturity (Capitolo 3).

**Architectural Maturity**
Componente del framework GIST che misura il livello di evoluzione dell'architettura IT, includendo cloud adoption (35%), automation level (25%), API maturity (20%) e DevOps practices (20%). Dettagliata nel Capitolo 3.

**ARIMA (AutoRegressive Integrated Moving Average)**
Modello statistico per l'analisi e previsione di serie temporali, utilizzato nel Capitolo 2 per predire pattern di attacchi stagionali con formula ARIMA(2,1,2)(1,1,1)₁₂.

**Automation Level**
Grado di automazione dei processi IT, misurato come percentuale di operazioni eseguite senza intervento umano. Componente chiave per la validazione dell'ipotesi H3 sulla compliance integrata.

**Availability**
Percentuale di tempo in cui un sistema è operativo e accessibile. Target per H1: ≥99.95%, calcolata come: (Tempo operativo / Tempo totale) × 100.

## B

**Branch and Bound**
Algoritmo di ottimizzazione esatta utilizzato per il problema di set covering nella compliance optimization (Appendice C), con complessità O(2ⁿ) ma pruning efficace.

**Building Management System (BMS)**
Sistema integrato per il controllo e monitoraggio dell'infrastruttura fisica di un edificio, inclusi HVAC, alimentazione e sicurezza fisica. Discusso nel Capitolo 3.

**Business Continuity**
Capacità di un'organizzazione di continuare le operazioni critiche durante e dopo un evento disruptivo. Requisito fondamentale per la GDO data la natura 24/7 delle operazioni.

## C

**CAPEX (Capital Expenditure)**
Spese in conto capitale per l'acquisizione o miglioramento di asset fisici. Contrapposto a OPEX nell'analisi TCO del Capitolo 3.

**Cloud-Hybrid Architecture**
Architettura IT che combina risorse on-premise con servizi cloud pubblici e/o privati, permettendo flessibilità e ottimizzazione dei workload. Centrale per l'ipotesi H1.

**Cloud-Native**
Approccio allo sviluppo di applicazioni che sfrutta appieno i vantaggi del cloud computing, utilizzando microservizi, container e orchestrazione dinamica.

**Compliance-by-Design**
Approccio che integra i requisiti di conformità normativa fin dalle fasi iniziali di progettazione del sistema, piuttosto che come retrofit. Base dell'ipotesi H3.

**Compliance Integration Score**
Componente del framework GIST che misura l'efficacia dell'integrazione normativa, calcolata come: 0.40×Standards_overlap + 0.30×Automation_compliance + 0.30×Audit_readiness.

**Computational Fluid Dynamics (CFD)**
Analisi numerica e algoritmi per risolvere problemi di flusso dei fluidi, utilizzata nel Capitolo 3 per ottimizzare il raffreddamento dei data center.

**Container**
Unità di software che impacchetta codice e tutte le sue dipendenze, permettendo esecuzione rapida e affidabile tra diversi ambienti computing.

**CVE (Common Vulnerabilities and Exposures)**
Sistema di riferimento pubblico per le vulnerabilità di sicurezza informatica note. Database utilizzato nell'analisi del Capitolo 2.

## D

**Data Loss Prevention (DLP)**
Insieme di strumenti e processi utilizzati per assicurare che dati sensibili non vengano persi, mal utilizzati o acceduti da utenti non autorizzati.

**DevOps**
Insieme di pratiche che combinano sviluppo software (Dev) e operazioni IT (Ops) per abbreviare il ciclo di vita dello sviluppo e fornire continuous delivery. Misurato attraverso metriche DORA nel framework GIST.

**Digital Twin**
Rappresentazione virtuale di un oggetto o sistema fisico, utilizzata per simulazione e ottimizzazione. Menzionata nel contesto di testing architetture nel Capitolo 3.

**DORA Metrics**
Four key metrics (Deployment Frequency, Lead Time for Changes, Mean Time to Recovery, Change Failure Rate) per misurare le performance DevOps, integrate nel framework GIST.

## E

**Edge Computing**
Paradigma che porta computazione e storage dei dati vicino al luogo dove sono necessari, riducendo latenza e uso di banda. Analizzato nel Capitolo 3 per applicazioni retail real-time.

**Endpoint Detection and Response (EDR)**
Soluzione di sicurezza che monitora continuamente gli endpoint per rilevare e rispondere a minacce cyber. Parte della strategia Zero Trust discussa nel Capitolo 2.

**Event-Driven Architecture**
Pattern architetturale dove il flusso del programma è determinato da eventi come click utente, output sensori o messaggi da altri programmi.

## F

**Failover**
Capacità di un sistema di trasferire automaticamente il controllo a un sistema di backup quando il componente principale fallisce.

**False Positive Rate**
Percentuale di allarmi di sicurezza incorretti rispetto al totale. Metrica critica per l'efficacia dei sistemi di detection.

**Free Cooling**
Metodo di raffreddamento che utilizza aria esterna fredda invece di refrigerazione meccanica quando le condizioni lo permettono, riducendo PUE del 23% (Capitolo 3).

## G

**GDPR (General Data Protection Regulation)**
Regolamento UE 2016/679 sulla protezione dei dati personali. Uno dei tre standard principali analizzati per l'ipotesi H3.

**GDO (Grande Distribuzione Organizzata)**
Settore del commercio al dettaglio caratterizzato da catene di negozi con gestione centralizzata, tipicamente con più di 50 punti vendita.

**GIST (GDO Integrated Security Transformation)**
Framework sviluppato in questa ricerca che integra Physical infrastructure (P), Architectural maturity (A), Security posture (S) e Compliance integration (C) per guidare la trasformazione IT sicura nella GDO.

**Greedy Algorithm**
Algoritmo che fa la scelta localmente ottimale ad ogni step, utilizzato per il weighted set cover problem nella compliance optimization con garanzia di approssimazione ln(n).

## H

**High Availability (HA)**
Caratteristica di un sistema progettato per essere operativo per una percentuale di tempo molto alta, tipicamente 99.9% o superiore.

**HVAC (Heating, Ventilation, and Air Conditioning)**
Sistemi di riscaldamento, ventilazione e condizionamento dell'aria, critici per il mantenimento delle condizioni operative ottimali dell'infrastruttura IT.

**Hybrid Cloud**
Ambiente computing che combina cloud pubblico e infrastruttura privata, permettendo orchestrazione e movimento di dati e applicazioni tra i due.

## I

**IaaS (Infrastructure as a Service)**
Modello di cloud computing che fornisce risorse di computing virtualizzate via Internet, inclusi server, storage e networking.

**Identity and Access Management (IAM)**
Framework di politiche e tecnologie per assicurare che le persone giuste abbiano accesso appropriato alle risorse tecnologiche.

**Incident Response**
Approccio organizzato per gestire le conseguenze di una violazione di sicurezza o cyberattacco, seguendo il ciclo NIST: Preparation, Detection, Containment, Eradication, Recovery.

**Infrastructure as Code (IaC)**
Gestione e provisioning dell'infrastruttura attraverso file di definizione machine-readable piuttosto che configurazione hardware fisica o strumenti di configurazione interattivi.

**Isolation Forest**
Algoritmo di machine learning per anomaly detection utilizzato nel Capitolo 2 e implementato nell'Appendice C per rilevare comportamenti anomali nel traffico retail.

## J

**Jaccard Index**
Coefficiente di similarità utilizzato per confrontare la sovrapposizione tra requisiti normativi: J(A,B) = |A ∩ B| / |A ∪ B|. Utilizzato nel Capitolo 4 per quantificare overlap tra PCI-DSS, GDPR e NIS2.

## K

**Key Performance Indicator (KPI)**
Metrica utilizzata per valutare il successo di un'organizzazione o di una particolare attività. Il Capitolo 5 definisce KPI operativi, economici e strategici per il framework GIST.

**Kubernetes**
Piattaforma open-source per l'automazione del deployment, scaling e gestione di applicazioni containerizzate, menzionata come tecnologia abilitante per multi-cloud.

## L

**Latency**
Tempo di ritardo tra l'invio di una richiesta e la ricezione della risposta. Vincolo critico per H2: mantenere incremento <50ms con Zero Trust.

**Lead Time**
Tempo tra l'inizio e il completamento di un processo. Nel contesto DevOps (DORA metrics), tempo dal commit del codice al deployment in produzione.

**Lift and Shift**
Strategia di migrazione cloud che sposta applicazioni esistenti al cloud con modifiche minime. Analizzata nel Capitolo 3 come opzione più veloce ma con benefici limitati.

**LSTM (Long Short-Term Memory)**
Tipo di rete neurale ricorrente capace di apprendere dipendenze a lungo termine, implementata nell'Appendice C per previsione di pattern di attacco.

## M

**Machine Learning Operations (MLOps)**
Insieme di pratiche che combina Machine Learning, DevOps e Data Engineering per distribuire e mantenere sistemi ML in produzione.

**Mean Time Between Failures (MTBF)**
Tempo medio tra guasti di un sistema, metrica chiave per l'affidabilità dell'infrastruttura. Target per sistemi N+1: 52,560 ore.

**Mean Time To Recovery (MTTR)**
Tempo medio necessario per ripristinare un sistema dopo un guasto. Metrica DORA e indicatore chiave per la business continuity.

**Micro-segmentation**
Pratica di sicurezza che divide la rete in zone sicure distinte per singoli workload, componente chiave dell'implementazione Zero Trust che contribuisce al 30.7% della riduzione ASSA.

**Multi-Factor Authentication (MFA)**
Metodo di autenticazione che richiede due o più fattori di verifica per accedere a una risorsa, implementazione quick win nella roadmap GIST.

## N

**Network Functions Virtualization (NFV)**
Architettura di rete che utilizza tecnologie di virtualizzazione per virtualizzare intere classi di funzioni di nodo di rete in building block.

**NIS2 (Network and Information Security Directive 2)**
Direttiva UE 2022/2555 sulla sicurezza delle reti e dei sistemi informativi, applicabile dal 18 ottobre 2024. Terzo standard analizzato per H3.

**NPV (Net Present Value)**
Valore attuale netto, differenza tra il valore attuale dei flussi di cassa in entrata e in uscita su un periodo di tempo. Utilizzato per valutare investimenti IT.

## O

**OPEX (Operational Expenditure)**
Spese operative continue per il funzionamento di un prodotto, business o sistema. Contrapposto a CAPEX nell'analisi TCO.

**Orchestration**
Configurazione automatizzata, coordinamento e gestione di sistemi informatici e software. Critica per gestire ambienti multi-cloud complessi.

## P

**PaaS (Platform as a Service)**
Modello di cloud computing che fornisce una piattaforma permettendo ai clienti di sviluppare, eseguire e gestire applicazioni senza la complessità di costruire e mantenere l'infrastruttura.

**Patch Management**
Processo di distribuzione e applicazione di aggiornamenti al software. Gap critico identificato: 72 giorni medi nella GDO vs 30 giorni target.

**PCI-DSS (Payment Card Industry Data Security Standard)**
Standard di sicurezza per organizzazioni che gestiscono carte di pagamento. Versione 4.0 analizzata nel Capitolo 4 con 389 requisiti.

**Physical Infrastructure Score**
Componente del framework GIST che valuta power redundancy (25%), cooling efficiency (20%), network reliability (30%) e physical security (25%).

**Point of Sale (POS)**
Sistema dove avviene la transazione retail. Target primario di attacchi analizzati nel Capitolo 2, con 234 varianti di malware identificate.

**Power Usage Effectiveness (PUE)**
Rapporto tra energia totale consumata da un data center e energia usata dall'equipaggiamento IT. Target best practice: <1.4.

## Q

**Quality of Service (QoS)**
Descrizione o misurazione delle performance complessive di un servizio, particolarmente importante per traffico mission-critical in architetture SD-WAN.

**Quantum-Resistant Algorithms**
Algoritmi crittografici progettati per essere sicuri contro attacchi da computer quantistici, discussi nel Capitolo 5 come trend futuro.

## R

**RBAC (Role-Based Access Control)**
Metodo di regolazione dell'accesso a risorse informatiche basato sui ruoli degli utenti nell'organizzazione.

**Recovery Point Objective (RPO)**
Età massima dei file che devono essere recuperati dal backup storage per le normali operazioni da riprendere dopo un disastro.

**Recovery Time Objective (RTO)**
Durata di tempo entro cui un processo aziendale deve essere ripristinato dopo un disastro per evitare conseguenze inaccettabili.

**Refactoring**
Ristrutturazione del codice esistente senza cambiarne il comportamento esterno, strategia di migrazione cloud più complessa ma con maggiori benefici (58.9% riduzione OPEX).

**Reinforcement Learning**
Area del machine learning dove un agente impara a comportarsi in un ambiente eseguendo azioni e vedendo i risultati, utilizzato per orchestrazione edge computing.

**Replatforming**
Strategia di migrazione cloud che introduce ottimizzazioni moderate per sfruttare capacità cloud senza ristrutturazione completa.

**ROI (Return on Investment)**
Misura di performance utilizzata per valutare l'efficienza di un investimento. Formula: (Benefici - Costi) / Costi × 100. Target raggiunto: 287% a 24 mesi.

## S

**SaaS (Software as a Service)**
Modello di distribuzione software dove le applicazioni sono ospitate da un fornitore di servizi e rese disponibili via Internet.

**SCADA (Supervisory Control and Data Acquisition)**
Sistema di controllo industriale per il monitoraggio e controllo di processi industriali, target di attacchi cyber-physical analizzati nel Capitolo 4.

**SD-WAN (Software-Defined Wide Area Network)**
Architettura WAN virtuale che permette alle aziende di sfruttare qualsiasi combinazione di servizi di trasporto per connettere in modo sicuro utenti ad applicazioni.

**Security Information and Event Management (SIEM)**
Approccio alla gestione della sicurezza che combina SIM (Security Information Management) e SEM (Security Event Management).

**Security Operations Center (SOC)**
Unità centralizzata che si occupa di questioni di sicurezza a livello organizzativo e tecnico, proposta nella roadmap post-incident del Capitolo 4.

**Security Posture Score**
Componente GIST che misura Zero Trust implementation (30%), threat detection (25%), incident response (25%) e security training (20%).

**Service Level Agreement (SLA)**
Contratto tra fornitore di servizi e cliente che specifica il livello di servizio atteso. Target per H1: ≥99.95% availability.

**Service Mesh**
Livello di infrastruttura dedicato per facilitare comunicazioni service-to-service sicure, veloci e affidabili in architetture microservizi.

**Set Covering Problem**
Problema di ottimizzazione combinatoriale NP-hard utilizzato per ottimizzare l'implementazione dei controlli di compliance, risolto con algoritmi greedy nell'Appendice C.

**Spectral Clustering**
Tecnica di clustering che utilizza autovalori della matrice di similarità, applicata per network segmentation optimization nell'Appendice C.

## T

**TCO (Total Cost of Ownership)**
Stima finanziaria che aiuta a determinare i costi diretti e indiretti di un prodotto o sistema. Include CAPEX + OPEX + costi di rischio su orizzonte temporale definito.

**Threat Landscape**
Panorama complessivo delle minacce cyber che un'organizzazione affronta, analizzato specificamente per la GDO nel Capitolo 2.

**Time Series Analysis**
Analisi di punti dati indicizzati in ordine temporale, utilizzata per identificare pattern stagionali negli attacchi (incremento 340% durante Black Friday).

## U

**Uninterruptible Power Supply (UPS)**
Dispositivo che fornisce alimentazione di emergenza quando la fonte di alimentazione principale fallisce. Affidabilità target: 99.9% per commutazione automatica.

**Uptime**
Misura dell'affidabilità del sistema, espressa come percentuale di tempo in cui il sistema è operativo. Correlato inversamente al downtime.

## V

**Value at Risk (VaR)**
Tecnica di misurazione del rischio che stima la perdita potenziale in valore di un portfolio. VaR GDPR al 95° percentile: €3.2M/anno.

**Virtual Private Network (VPN)**
Estende una rete privata attraverso una rete pubblica, permettendo agli utenti di inviare e ricevere dati come se fossero direttamente connessi alla rete privata.

**Vulnerability Assessment**
Processo di identificazione, quantificazione e prioritizzazione delle vulnerabilità in un sistema, base per il calcolo dell'ASSA score.

## W

**Web Application Firewall (WAF)**
Firewall che monitora, filtra e blocca traffico HTTP da e verso un'applicazione web, componente della difesa perimetrale evoluta.

**Weighted Set Cover**
Versione del set covering problem dove ogni set ha un costo associato, utilizzato per ottimizzare l'implementazione di controlli di compliance multipli.

## Z

**Zero Trust Architecture**
Modello di sicurezza che richiede verifica rigorosa dell'identità per ogni persona e dispositivo che tenta di accedere a risorse, indipendentemente dalla posizione. Principio: "never trust, always verify".

**Zero-Day Vulnerability**
Vulnerabilità di sicurezza sconosciuta al fornitore del software, sfruttata nell'attacco Cleo-Carrefour analizzato nel Capitolo 2.

---

*Nota: I termini in corsivo all'interno delle definizioni rimandano ad altre voci del glossario. I riferimenti ai capitoli indicano dove il termine è discusso in maggior dettaglio nella tesi.*