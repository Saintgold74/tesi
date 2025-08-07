import pandas as pd
import numpy as np

# Versione semplificata che genera solo i file CSV senza visualizzazioni

# ========== TABELLA 2.1: Caratterizzazione delle Minacce ==========

def create_threat_characterization_table():
    """Crea tabella caratterizzazione minacce GDO"""
    
    data = {
        'Tipologia': ['Malware POS', 'Ransomware Operativo', 'Supply Chain', 
                      'AI-Powered Phishing', 'Cyber-Physical', 'Insider Threats'],
        'Incidenti_Totali': [512, 334, 156, 243, 89, 67],
        'Crescita_YoY': [23, 45, 87, 156, 67, 12],
        'Dwell_Time_ore': [127, 103.2, 189, 72, 96, 234],
        'Impatto_Medio_MEur': [2.3, 4.8, 8.2, 1.2, 3.4, 2.8],
        'Target_Primario': ['Pagamenti', 'Continuità', 'Multi-retailer', 
                           'Credenziali', 'OT/HVAC', 'Dati clienti'],
        'Trend_2025': ['↑↑', '↑↑↑', '↑↑↑', '↑↑↑', '↑↑', '→']
    }
    
    df = pd.DataFrame(data)
    
    # Calcola totali
    totals = {
        'Tipologia': 'TOTALE',
        'Incidenti_Totali': df['Incidenti_Totali'].sum(),
        'Crescita_YoY': f"{df['Crescita_YoY'].mean():.1f} (media)",
        'Dwell_Time_ore': f"{df['Dwell_Time_ore'].mean():.1f} (media)",
        'Impatto_Medio_MEur': f"{df['Impatto_Medio_MEur'].mean():.1f} (media)",
        'Target_Primario': '-',
        'Trend_2025': '-'
    }
    
    df = pd.concat([df, pd.DataFrame([totals])], ignore_index=True)
    df.to_csv('tabella_2_1_threat_characterization.csv', index=False)
    
    print("Tabella 2.1 salvata: tabella_2_1_threat_characterization.csv")
    return df

# ========== TABELLA 2.2: Parametri ASSA ==========

def create_assa_parameters_table():
    """Crea tabella parametri modello ASSA"""
    
    # Componenti
    components = pd.DataFrame({
        'Componente': ['Porte Aperte', 'Servizi Esposti', 'Vulnerabilità Note'],
        'Simbolo': ['P_i', 'S_i', 'V_i'],
        'Peso': [0.30, 0.40, 0.30],
        'Store_Media': [8, 5, 3],
        'Store_Std': [2.1, 1.4, 1.0],
        'Hub_Media': [25, 15, 8],
        'Hub_Std': [4.3, 3.2, 2.5]
    })
    
    # Fattori di amplificazione
    amplification = pd.DataFrame({
        'Punti_Vendita': [50, 100, 200, 500],
        'Fattore_Amplificazione': [2.3, 3.8, 6.2, 11.7]
    })
    
    components.to_csv('tabella_2_2a_assa_components.csv', index=False)
    amplification.to_csv('tabella_2_2b_assa_amplification.csv', index=False)
    
    print("Tabella 2.2a salvata: tabella_2_2a_assa_components.csv")
    print("Tabella 2.2b salvata: tabella_2_2b_assa_amplification.csv")
    
    return components, amplification

# ========== TABELLA 2.3: Pattern Stagionali ==========

def create_seasonal_patterns_table():
    """Crea tabella pattern stagionali attacchi"""
    
    data = {
        'Periodo': ['Black Friday/CM', 'Periodo Natalizio', 'Back-to-School', 
                    'Saldi Estivi', 'Pasqua', 'Baseline'],
        'Settimana_Anno': ['47-48', '49-52', '34-36', '26-28', 'var.', '-'],
        'Moltiplicatore': [3.4, 2.7, 1.8, 1.4, 1.3, 1.0],
        'Durata_Giorni': ['4-7', '21-28', '14-21', '14-21', '7-10', '-'],
        'Attacchi_Predominanti': ['Ransomware, POS', 'Phishing, Supply', 
                                 'Malware, Insider', 'DDoS, Phishing', 
                                 'POS, Ransomware', 'Misto'],
        'Predictability_%': [89, 84, 76, 72, 68, 0]
    }
    
    df = pd.DataFrame(data)
    
    # Aggiungi metriche SARIMA
    sarima_metrics = pd.DataFrame({
        'Metrica': ['MAPE', 'RMSE', 'R²', 'AIC'],
        'Valore': ['12.7%', '23.4 att/sett', '0.84', '1,247.3']
    })
    
    df.to_csv('tabella_2_3_seasonal_patterns.csv', index=False)
    sarima_metrics.to_csv('tabella_2_3_sarima_metrics.csv', index=False)
    
    print("Tabella 2.3 salvata: tabella_2_3_seasonal_patterns.csv")
    print("Metriche SARIMA salvate: tabella_2_3_sarima_metrics.csv")
    
    return df, sarima_metrics

# ========== TABELLA 2.4: Tecnologie Difensive ==========

def create_defensive_technologies_table():
    """Crea tabella comparativa tecnologie difensive"""
    
    data = {
        'Tecnologia': ['EDR', 'SASE', 'SOAR', 'Zero Trust', 'SIEM+AI', 'MFA'],
        'Efficacia_Detection_%': [73, 89, 67, 94, 91, 89],
        'CAPEX_k_per_store': ['0.3-0.5', '0.8-1.2', '2.1-3.5', '4.5-6.8', '1.8-2.4', '0.15-0.25'],
        'OPEX_%_anno': [18, 12, 22, 15, 20, 10],
        'ROI_3_anni_%': [312, 234, 189, 287, 267, 423],
        'Payback_mesi': [14, 18, 24, 28, 22, 4],
        'Criticita_Principale': ['Config drift', 'Latenza edge', 'Skill gap', 
                                'Complessità', 'False positive', 'User friction']
    }
    
    df = pd.DataFrame(data)
    df = df.sort_values('ROI_3_anni_%', ascending=False)
    
    df.to_csv('tabella_2_4_defensive_technologies.csv', index=False)
    
    print("Tabella 2.4 salvata: tabella_2_4_defensive_technologies.csv")
    
    return df

# ========== TABELLA 2.5: Roadmap Implementativa ==========

def create_implementation_roadmap_table():
    """Crea tabella roadmap implementativa"""
    
    data = {
        'Fase': ['Fase 1: Quick Wins', 'Fase 2: Core Transformation', 
                'Fase 3: Advanced Optimization'],
        'Periodo': ['0-6 mesi', '6-18 mesi', '18-36 mesi'],
        'Interventi_Principali': [
            'MFA universale; EDR deployment; Basic segmentation',
            'SD-WAN completo; Cloud migration (30%); Zero Trust phase 1; SIEM deployment',
            'SOC con AI/ML; Cloud-native (70%); Compliance automation; Threat hunting proattivo'
        ],
        'Investimento_MEur': [0.8, 3.5, 8.2],
        'ROI_Atteso_%': [312, 187, 234],
        'KPI_Target': [
            'Detection rate >90%; MTTD <48h; ASSA -24%',
            'Availability >99.9%; TCO -23%; ASSA -52% totale; Compliance score >85%',
            'MTTD <24h; TCO -38% totale; Automation >60%; Incident rate -75%'
        ]
    }
    
    df = pd.DataFrame(data)
    
    # Calcola totali
    totals = {
        'Investimento_Totale_MEur': df['Investimento_MEur'].sum(),
        'ROI_Medio_%': df['ROI_Atteso_%'].mean(),
        'Durata_Totale_mesi': 36
    }
    
    df.to_csv('tabella_2_5_roadmap_implementation.csv', index=False)
    
    # Salva anche i totali
    totals_df = pd.DataFrame([totals])
    totals_df.to_csv('tabella_2_5_roadmap_totals.csv', index=False)
    
    print("Tabella 2.5 salvata: tabella_2_5_roadmap_implementation.csv")
    print("Totali salvati: tabella_2_5_roadmap_totals.csv")
    
    return df, totals

# ========== TABELLA 2.6: Zero Trust e ASSA ==========

def create_zero_trust_assa_table():
    """Crea tabella contributo Zero Trust a riduzione ASSA"""
    
    data = {
        'Componente_ZT': ['Micro-segmentazione', 'Identity Verification', 
                         'Continuous Monitoring', 'Least Privilege', 
                         'Traffic Inspection', 'Effetto Combinato'],
        'Riduzione_Porte_%': [-80, -15, -10, -20, -25, -87],
        'Riduzione_Servizi_%': [-45, -60, -25, -30, -40, -76],
        'Riduzione_Vuln_%': [-20, -30, -50, -15, -35, -68],
        'ASSA_Totale_%': [-30.7, -24.1, -18.4, -12.3, -15.2, -42.7],
        'Latenza_ms': [8, 12, 5, 3, 15, 44]
    }
    
    df = pd.DataFrame(data)
    df.to_csv('tabella_2_6_zero_trust_assa.csv', index=False)
    
    print("Tabella 2.6 salvata: tabella_2_6_zero_trust_assa.csv")
    
    return df

# ========== ESECUZIONE PRINCIPALE ==========

if __name__ == "__main__":
    print("Generazione Tabelle Capitolo 2 (Versione Semplificata)")
    print("="*60)
    
    # Genera tutte le tabelle
    print("\n1. Generazione Tabella 2.1...")
    threat_df = create_threat_characterization_table()
    
    print("\n2. Generazione Tabella 2.2...")
    assa_comp, assa_amp = create_assa_parameters_table()
    
    print("\n3. Generazione Tabella 2.3...")
    seasonal_df, sarima_metrics = create_seasonal_patterns_table()
    
    print("\n4. Generazione Tabella 2.4...")
    tech_df = create_defensive_technologies_table()
    
    print("\n5. Generazione Tabella 2.5...")
    roadmap_df, roadmap_totals = create_implementation_roadmap_table()
    
    print("\n6. Generazione Tabella 2.6...")
    zt_assa_df = create_zero_trust_assa_table()
    
    print("\n" + "="*60)
    print("COMPLETATO! Tutte le tabelle sono state generate come file CSV.")
    print("\nFile generati:")
    print("- tabella_2_1_threat_characterization.csv")
    print("- tabella_2_2a_assa_components.csv")
    print("- tabella_2_2b_assa_amplification.csv")
    print("- tabella_2_3_seasonal_patterns.csv")
    print("- tabella_2_3_sarima_metrics.csv")
    print("- tabella_2_4_defensive_technologies.csv")
    print("- tabella_2_5_roadmap_implementation.csv")
    print("- tabella_2_5_roadmap_totals.csv")
    print("- tabella_2_6_zero_trust_assa.csv")
    
    # Genera summary report
    summary = f"""
SUMMARY REPORT - Tabelle Capitolo 2
=====================================

Tabella 2.1: {len(threat_df)-1} tipologie di minacce analizzate
- Totale incidenti: {threat_df.iloc[:-1]['Incidenti_Totali'].sum()}
- Crescita media YoY: {threat_df.iloc[:-1]['Crescita_YoY'].mean():.1f}%

Tabella 2.2: {len(assa_comp)} componenti ASSA + {len(assa_amp)} fattori amplificazione
- Pesi componenti: {list(assa_comp['Peso'])}
- Max amplificazione: {assa_amp['Fattore_Amplificazione'].max()}x

Tabella 2.3: {len(seasonal_df)-1} pattern stagionali identificati
- Picco massimo: Black Friday {seasonal_df.iloc[0]['Moltiplicatore']}x
- Predictability media: {seasonal_df.iloc[:-1]['Predictability_%'].mean():.1f}%

Tabella 2.4: {len(tech_df)} tecnologie difensive comparate
- ROI massimo: MFA {tech_df[tech_df['Tecnologia']=='MFA']['ROI_3_anni_%'].values[0]}%
- Payback più veloce: {tech_df[tech_df['Tecnologia']=='MFA']['Payback_mesi'].values[0]} mesi

Tabella 2.5: 3 fasi implementative su 36 mesi
- Investimento totale: €{roadmap_totals['Investimento_Totale_MEur']}M
- ROI medio atteso: {roadmap_totals['ROI_Medio_%']:.0f}%

Tabella 2.6: {len(zt_assa_df)-1} componenti Zero Trust analizzati
- Riduzione ASSA totale: {zt_assa_df.iloc[-1]['ASSA_Totale_%']}%
- Latenza totale aggiunta: {zt_assa_df.iloc[-1]['Latenza_ms']}ms
"""
    
    print(summary)
    
    with open('tabelle_capitolo2_summary.txt', 'w', encoding='utf-8') as f:
        f.write(summary)
    
    print("\nReport summary salvato: tabelle_capitolo2_summary.txt")
