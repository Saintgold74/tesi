# Abstract

## Abstract (Italiano)

### Infrastrutture IT Sicure per la Grande Distribuzione Organizzata: Un Framework Integrato per la Trasformazione Cloud-First con Validazione Empirica

La Grande Distribuzione Organizzata (GDO) italiana rappresenta un'infrastruttura critica che gestisce oltre 27.000 punti vendita e processa 45 milioni di transazioni giornaliere, affrontando sfide uniche in termini di sicurezza informatica, continuità operativa e conformità normativa. Questa ricerca affronta il problema di come progettare e implementare infrastrutture IT che bilancino simultaneamente requisiti di sicurezza, performance, compliance e sostenibilità economica in un contesto caratterizzato da minacce informatiche in crescita esponenziale (+312% nel periodo 2021-2023) e complessità normativa crescente.

Lo studio propone e valida empiricamente il framework GIST (GDO Integrated Security Transformation), un modello quantitativo che integra quattro componenti fondamentali: infrastruttura fisica (P), maturità architetturale (A), postura di sicurezza (S) e integrazione della compliance (C). La validazione si basa su uno studio longitudinale di 24 mesi condotto su 15 organizzazioni GDO italiane con fatturato compreso tra €100M e €2B, utilizzando un approccio mixed-methods che combina analisi quantitativa rigorosa con modellazione predittiva.

I risultati dimostrano la validità delle tre ipotesi di ricerca formulate. Primo, le architetture cloud-ibride permettono di raggiungere livelli di disponibilità del 99.95% (incremento medio +0.55%, p<0.001) con una riduzione del Total Cost of Ownership del 38.2% su 5 anni (IC 95%: 34.6%-41.7%). Secondo, l'implementazione di principi Zero Trust riduce la superficie di attacco aggregata (ASSA) del 42.7% (IC 95%: 39.2%-46.2%), superando il target del 35%, mantenendo l'incremento di latenza sotto i 50ms (media 32.1ms). Terzo, l'approccio compliance-by-design genera riduzioni dei costi di conformità del 39.1% (IC 95%: 35.7%-42.5%) con overhead operativo contenuto al 9.7% delle risorse IT.

L'analisi economica rivela un Return on Investment del 287% a 24 mesi per l'implementazione completa del framework, con payback period medio di 15.7 mesi. Il modello predittivo sviluppato mostra R²=0.783 per gli outcome di sicurezza e R²=0.817 per i risultati economici, confermando la robustezza del framework.

Le implicazioni pratiche includono una roadmap implementativa strutturata in tre fasi (quick wins, core transformation, advanced optimization) con investimento totale di €15.4M per organizzazione media, e la dimostrazione che sicurezza e performance aziendale non sono obiettivi contrapposti ma sinergici nel contesto della trasformazione digitale della GDO.

**Parole chiave**: Grande Distribuzione Organizzata, Zero Trust Architecture, Cloud-Hybrid Systems, Compliance Integration, GIST Framework, Retail IT Security, Digital Transformation

---

## Abstract (English)

### Secure IT Infrastructures for Large-Scale Organized Distribution: An Integrated Framework for Cloud-First Transformation with Empirical Validation

The Italian Large-Scale Organized Distribution (GDO) sector represents critical infrastructure managing over 27,000 retail locations and processing 45 million daily transactions, facing unique challenges in cybersecurity, operational continuity, and regulatory compliance. This research addresses the problem of designing and implementing IT infrastructures that simultaneously balance security requirements, performance, compliance, and economic sustainability in a context characterized by exponentially growing cyber threats (+312% in the 2021-2023 period) and increasing regulatory complexity.

The study proposes and empirically validates the GIST (GDO Integrated Security Transformation) framework, a quantitative model integrating four fundamental components: physical infrastructure (P), architectural maturity (A), security posture (S), and compliance integration (C). Validation is based on a 24-month longitudinal study conducted on 15 Italian GDO organizations with revenues between €100M and €2B, using a mixed-methods approach combining rigorous quantitative analysis with predictive modeling.

Results demonstrate the validity of the three formulated research hypotheses. First, cloud-hybrid architectures enable availability levels of 99.95% (mean increase +0.55%, p<0.001) with a Total Cost of Ownership reduction of 38.2% over 5 years (95% CI: 34.6%-41.7%). Second, Zero Trust principles implementation reduces the Aggregated System Surface Attack (ASSA) score by 42.7% (95% CI: 39.2%-46.2%), exceeding the 35% target while maintaining latency increase under 50ms (mean 32.1ms). Third, the compliance-by-design approach generates compliance cost reductions of 39.1% (95% CI: 35.7%-42.5%) with operational overhead contained at 9.7% of IT resources.

Economic analysis reveals a 287% Return on Investment at 24 months for complete framework implementation, with an average payback period of 15.7 months. The developed predictive model shows R²=0.783 for security outcomes and R²=0.817 for economic results, confirming framework robustness.

Practical implications include a structured implementation roadmap in three phases (quick wins, core transformation, advanced optimization) with a total investment of €15.4M for an average organization, and the demonstration that security and business performance are not opposing but synergistic objectives in the context of GDO digital transformation.

**Keywords**: Large-Scale Organized Distribution, Zero Trust Architecture, Cloud-Hybrid Systems, Compliance Integration, GIST Framework, Retail IT Security, Digital Transformation

---

## Riassunto Esteso (Extended Abstract - 1000 parole)

### Contesto e Motivazione

La Grande Distribuzione Organizzata rappresenta un settore strategico dell'economia italiana, con un impatto diretto sulla vita quotidiana di milioni di consumatori. L'infrastruttura tecnologica che supporta queste operazioni ha raggiunto livelli di complessità comparabili a quelli di operatori di telecomunicazioni o istituzioni finanziarie, ma con vincoli operativi unici derivanti dalla natura distribuita delle operazioni, dalla necessità di continuità operativa H24, e dalla gestione di dati sensibili sia finanziari che personali.

Il panorama delle minacce informatiche specifico per il settore retail ha subito un'evoluzione drammatica negli ultimi anni. L'incremento del 312% negli attacchi documentati tra il 2021 e il 2023, combinato con l'emergere di attacchi cyber-fisici che possono compromettere non solo i sistemi informativi ma anche le infrastrutture operative (come i sistemi di refrigerazione), ha reso obsoleti gli approcci tradizionali alla sicurezza informatica basati su perimetri statici e controlli reattivi.

Parallelamente, l'evoluzione normativa ha introdotto requisiti sempre più stringenti e spesso sovrapposti. L'entrata in vigore del PCI-DSS 4.0, gli aggiornamenti continui del GDPR, e l'implementazione della direttiva NIS2 creano un panorama di compliance che richiede investimenti significativi e può assorbire fino al 2-3% del fatturato se gestito con approcci tradizionali frammentati.

### Obiettivi e Metodologia

Questa ricerca si propone di rispondere alla domanda fondamentale: come possono le organizzazioni GDO progettare e implementare infrastrutture IT che non solo rispondano alle sfide attuali di sicurezza e compliance, ma che lo facciano in modo economicamente sostenibile e abilitando l'innovazione piuttosto che limitandola?

Per rispondere a questa domanda, la ricerca ha sviluppato e validato il framework GIST (GDO Integrated Security Transformation), basato su tre ipotesi fondamentali:
1. Le architetture cloud-ibride possono migliorare simultaneamente performance e sicurezza riducendo i costi
2. L'implementazione di Zero Trust può ridurre significativamente la superficie di attacco senza compromettere l'usabilità
3. Un approccio integrato alla compliance genera efficienze economiche significative

La metodologia adottata combina rigorosità scientifica con rilevanza pratica attraverso uno studio longitudinale di 24 mesi su 15 organizzazioni GDO italiane, selezionate per rappresentare la diversità del settore in termini di dimensione, maturità tecnologica e distribuzione geografica. La raccolta dati ha utilizzato strumenti automatizzati di monitoring, analisi di log di sicurezza, metriche finanziarie certificate, e valutazioni di compliance strutturate.

### Risultati Principali

I risultati dello studio forniscono evidenze robuste per tutte e tre le ipotesi di ricerca. Per quanto riguarda le architetture cloud-ibride (H1), le organizzazioni partecipanti hanno raggiunto livelli di disponibilità media del 99.95%, con 9 su 15 organizzazioni che superano questa soglia critica. La riduzione del TCO a 5 anni è stata in media del 38.2%, superando significativamente il target del 30%. L'analisi di regressione mostra che la maturità cloud e il livello di automazione sono i predittori più significativi del successo.

Per l'implementazione Zero Trust (H2), la riduzione della superficie di attacco aggregata (ASSA) è stata del 42.7%, con la micro-segmentazione che contribuisce per il 30.7% di questa riduzione. Particolarmente significativo è il fatto che questo miglioramento della sicurezza è stato ottenuto mantenendo l'impatto sulla latenza sotto i 50ms (media 32.1ms), dimostrando che sicurezza e performance non sono necessariamente in conflitto quando l'architettura è progettata correttamente.

Per la compliance integrata (H3), l'approccio unificato ha generato risparmi del 39.1% rispetto ad approcci frammentati, con l'overhead operativo ridotto dal 17.2% al 9.7% delle risorse IT. Il ROI dell'automazione della compliance è stato del 241% a 24 mesi, con payback period medio di 15.3 mesi.

### Framework GIST

Il framework GIST emergente dalla ricerca fornisce un modello quantitativo per valutare e guidare la trasformazione sicura dell'IT nella GDO. Il modello integra quattro componenti principali:

GIST = f(P, A, S, C) × K_GDO × (1 + I)

Dove P rappresenta l'infrastruttura fisica (alimentazione, raffreddamento, connettività), A la maturità architetturale (cloud adoption, automazione, DevOps), S la postura di sicurezza (Zero Trust, threat detection, incident response), e C l'integrazione della compliance. Il coefficiente K_GDO (1.23) cattura le specificità del settore, mentre I rappresenta il fattore di innovazione.

### Implicazioni e Conclusioni

Le implicazioni di questa ricerca sono molteplici e significative. Per i practitioner, il framework GIST fornisce uno strumento pratico per valutare la maturità attuale e pianificare investimenti futuri. La roadmap implementativa strutturata in tre fasi (quick wins 0-6 mesi, core transformation 6-18 mesi, advanced optimization 18-36 mesi) offre un percorso chiaro e validato empiricamente.

Per i decisori aziendali, la dimostrazione che investimenti in sicurezza generano ROI positivi e miglioramenti operativi trasforma la sicurezza da centro di costo a enabler strategico. L'evidenza che compliance integrata riduce i costi totali fornisce giustificazione economica per approcci olistici piuttosto che frammentati.

Per la comunità accademica, la ricerca contribuisce modelli quantitativi validati empiricamente che colmano il gap tra teoria e pratica nel dominio della sicurezza IT retail. Il dataset anonimizzato (disponibile dopo embargo di 24 mesi) fornirà base per future ricerche.

In conclusione, questa ricerca dimostra che la trasformazione digitale sicura della GDO non solo è possibile ma economicamente vantaggiosa quando guidata da principi ingegneristici solidi e implementata attraverso framework strutturati. Il futuro della GDO sarà caratterizzato da infrastrutture che sono simultaneamente più sicure, più efficienti e più innovative - un apparente paradosso risolto attraverso l'applicazione rigorosa di principi di system engineering e l'integrazione olistica di requisiti precedentemente considerati in conflitto.