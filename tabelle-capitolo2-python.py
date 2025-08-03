import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Configurazione per output pulito
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.precision', 2)

# ========== TABELLA 2.1: Caratterizzazione delle Minacce ==========

def create_threat_characterization_table():
    """Crea tabella caratterizzazione minacce GDO"""
    
    data = {
        'Tipologia': ['Malware POS', 'Ransomware Operativo', 'Supply Chain', 
                      'AI-Powered Phishing', 'Cyber-Physical', 'Insider Threats'],
        'Incidenti_Totali': [512, 334, 156, 243, 89, 67],
        'Crescita_YoY': [23, 45, 87, 156, 67, 12],
        'Dwell_Time_ore': [127, 103.2, 189, 72, 96, 234],  # 4.3gg = 103.2h
        'Impatto_Medio_MEur': [2.3, 4.8, 8.2, 1.2, 3.4, 2.8],
        'Target_Primario': ['Pagamenti', 'Continuità', 'Multi-retailer', 
                           'Credenziali', 'OT/HVAC', 'Dati clienti'],
        'Trend_2025': ['↑↑', '↑↑↑', '↑↑↑', '↑↑↑', '↑↑', '→']
    }
    
    df = pd.DataFrame(data)
    
    # Calcola totali e medie
    df.loc['Totale'] = ['TOTALE', 
                        df['Incidenti_Totali'].sum(),
                        df['Crescita_YoY'].mean(),
                        df['Dwell_Time_ore'].mean(),
                        df['Impatto_Medio_MEur'].mean(),
                        '-', '-']
    
    # Formatta per LaTeX
    latex_table = df.to_latex(index=False, 
                             column_format='lcccccl',
                             float_format=lambda x: f'{x:.1f}',
                             escape=False)
    
    # Salva anche come CSV
    df.to_csv('tabella_2_1_threat_characterization.csv', index=False)
    
    return df, latex_table

# ========== TABELLA 2.2: Parametri ASSA ==========

def create_assa_parameters_table():
    """Crea tabella parametri modello ASSA"""
    
    # Dati principali
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
    
    # Genera statistiche dettagliate
    print("=== Tabella 2.2: Parametri ASSA ===")
    print("\nComponenti e Pesi:")
    print(components)
    print("\nFattori di Amplificazione:")
    print(amplification)
    
    # Salva
    components.to_csv('tabella_2_2a_assa_components.csv', index=False)
    amplification.to_csv('tabella_2_2b_assa_amplification.csv', index=False)
    
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
        'Predictability': [89, 84, 76, 72, 68, 0]
    }
    
    df = pd.DataFrame(data)
    
    # Aggiungi metriche SARIMA
    sarima_metrics = pd.DataFrame({
        'Metrica': ['MAPE', 'RMSE', 'R²', 'AIC'],
        'Valore': ['12.7%', '23.4 att/sett', '0.84', '1,247.3']
    })
    
    print("=== Tabella 2.3: Pattern Stagionali ===")
    print(df)
    print("\nMetriche Modello SARIMA:")
    print(sarima_metrics)
    
    df.to_csv('tabella_2_3_seasonal_patterns.csv', index=False)
    
    return df

# ========== TABELLA 2.4: Tecnologie Difensive ==========

def create_defensive_technologies_table():
    """Crea tabella comparativa tecnologie difensive"""
    
    data = {
        'Tecnologia': ['EDR', 'SASE', 'SOAR', 'Zero Trust', 'SIEM+AI', 'MFA'],
        'Efficacia_Detection': [73, 89, 67, 94, 91, 89],
        'CAPEX_k_per_store_min': [0.3, 0.8, 2.1, 4.5, 1.8, 0.15],
        'CAPEX_k_per_store_max': [0.5, 1.2, 3.5, 6.8, 2.4, 0.25],
        'OPEX_percent_anno': [18, 12, 22, 15, 20, 10],
        'ROI_3_anni': [312, 234, 189, 287, 267, 423],
        'Payback_mesi': [14, 18, 24, 28, 22, 4],
        'Criticita_Principale': ['Config drift', 'Latenza edge', 'Skill gap', 
                                'Complessità', 'False positive', 'User friction']
    }
    
    df = pd.DataFrame(data)
    
    # Calcola CAPEX medio per analisi
    df['CAPEX_medio'] = (df['CAPEX_k_per_store_min'] + df['CAPEX_k_per_store_max']) / 2
    
    # Ordina per ROI
    df_sorted = df.sort_values('ROI_3_anni', ascending=False)
    
    print("=== Tabella 2.4: Tecnologie Difensive ===")
    print(df_sorted)
    
    df_sorted.to_csv('tabella_2_4_defensive_technologies.csv', index=False)
    
    return df_sorted

# ========== TABELLA 2.5: Roadmap Implementativa ==========

def create_implementation_roadmap_table():
    """Crea tabella roadmap implementativa"""
    
    phases = []
    
    # Fase 1
    phase1 = {
        'Fase': 'Fase 1: Quick Wins',
        'Periodo': '0-6 mesi',
        'Interventi': ['MFA universale', 'EDR deployment', 'Basic segmentation'],
        'Investimento_MEur': 0.8,
        'ROI_Atteso': 312,
        'KPI_Target': ['Detection rate >90%', 'MTTD <48h', 'ASSA -24%']
    }
    phases.append(phase1)
    
    # Fase 2
    phase2 = {
        'Fase': 'Fase 2: Core Transformation',
        'Periodo': '6-18 mesi',
        'Interventi': ['SD-WAN completo', 'Cloud migration (30%)', 
                      'Zero Trust phase 1', 'SIEM deployment'],
        'Investimento_MEur': 3.5,
        'ROI_Atteso': 187,
        'KPI_Target': ['Availability >99.9%', 'TCO -23%', 'ASSA -52% totale', 
                      'Compliance score >85%']
    }
    phases.append(phase2)
    
    # Fase 3
    phase3 = {
        'Fase': 'Fase 3: Advanced Optimization',
        'Periodo': '18-36 mesi',
        'Interventi': ['SOC con AI/ML', 'Cloud-native (70%)', 
                      'Compliance automation', 'Threat hunting proattivo'],
        'Investimento_MEur': 8.2,
        'ROI_Atteso': 234,
        'KPI_Target': ['MTTD <24h', 'TCO -38% totale', 
                      'Automation >60%', 'Incident rate -75%']
    }
    phases.append(phase3)
    
    # Crea DataFrame espanso
    expanded_data = []
    for phase in phases:
        for i, intervento in enumerate(phase['Interventi']):
            for j, kpi in enumerate(phase['KPI_Target']):
                if i == 0 and j == 0:
                    # Prima riga con tutti i dati
                    expanded_data.append({
                        'Fase': phase['Fase'],
                        'Periodo': phase['Periodo'],
                        'Intervento': intervento,
                        'Investimento_MEur': phase['Investimento_MEur'],
                        'ROI_%': phase['ROI_Atteso'],
                        'KPI': kpi
                    })
                elif j == 0:
                    # Nuovo intervento
                    expanded_data.append({
                        'Fase': '',
                        'Periodo': '',
                        'Intervento': intervento,
                        'Investimento_MEur': '',
                        'ROI_%': '',
                        'KPI': kpi
                    })
                elif i == len(phase['Interventi']) - 1:
                    # Solo KPI
                    expanded_data.append({
                        'Fase': '',
                        'Periodo': '',
                        'Intervento': '',
                        'Investimento_MEur': '',
                        'ROI_%': '',
                        'KPI': kpi
                    })
    
    df = pd.DataFrame(expanded_data)
    
    print("=== Tabella 2.5: Roadmap Implementativa ===")
    print(df)
    
    # Salva versione semplificata
    df_simple = pd.DataFrame(phases)
    df_simple.to_csv('tabella_2_5_roadmap_simple.csv', index=False)
    
    # Calcola totali
    totals = {
        'Investimento_Totale_MEur': sum(p['Investimento_MEur'] for p in phases),
        'ROI_Medio': np.mean([p['ROI_Atteso'] for p in phases]),
        'Durata_Totale_mesi': 36
    }
    
    print(f"\nTotali: Investimento {totals['Investimento_Totale_MEur']}M€, "
          f"ROI Medio {totals['ROI_Medio']:.0f}%, Durata {totals['Durata_Totale_mesi']} mesi")
    
    return df, totals

# ========== TABELLA 2.6: Zero Trust e ASSA ==========

def create_zero_trust_assa_table():
    """Crea tabella contributo Zero Trust a riduzione ASSA"""
    
    data = {
        'Componente_ZT': ['Micro-segmentazione', 'Identity Verification', 
                         'Continuous Monitoring', 'Least Privilege', 
                         'Traffic Inspection'],
        'Riduzione_Porte': [-80, -15, -10, -20, -25],
        'Riduzione_Servizi': [-45, -60, -25, -30, -40],
        'Riduzione_Vuln': [-20, -30, -50, -15, -35],
        'ASSA_Totale': [-30.7, -24.1, -18.4, -12.3, -15.2],
        'Latenza_ms': [8, 12, 5, 3, 15]
    }
    
    df = pd.DataFrame(data)
    
    # Calcola effetto combinato
    combined = {
        'Componente_ZT': 'Effetto Combinato',
        'Riduzione_Porte': -87,
        'Riduzione_Servizi': -76,
        'Riduzione_Vuln': -68,
        'ASSA_Totale': -42.7,
        'Latenza_ms': 44
    }
    
    df = pd.concat([df, pd.DataFrame([combined])], ignore_index=True)
    
    print("=== Tabella 2.6: Zero Trust e Riduzione ASSA ===")
    print(df)
    
    df.to_csv('tabella_2_6_zero_trust_assa.csv', index=False)
    
    return df

# ========== FUNZIONE PER GENERARE GRAFICI DELLE TABELLE ==========

def create_table_visualizations():
    """Crea visualizzazioni grafiche dei dati delle tabelle"""
    
    # Setup
    plt.style.use('seaborn-v0_8')
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. Threat Growth Visualization
    threat_data, _ = create_threat_characterization_table()
    threat_data_clean = threat_data[threat_data['Tipologia'] != 'TOTALE']
    
    ax1 = axes[0, 0]
    bars = ax1.bar(threat_data_clean['Tipologia'], 
                    threat_data_clean['Incidenti_Totali'],
                    color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b'])
    
    # Aggiungi crescita YoY sopra le barre
    for i, (bar, growth) in enumerate(zip(bars, threat_data_clean['Crescita_YoY'])):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 10,
                f'+{growth}%', ha='center', va='bottom', fontsize=9)
    
    ax1.set_ylabel('Numero di Incidenti')
    ax1.set_title('Incidenti per Tipologia di Minaccia (2020-2025)')
    ax1.set_xticklabels(threat_data_clean['Tipologia'], rotation=45, ha='right')
    
    # 2. ROI Comparison
    tech_data = create_defensive_technologies_table()
    
    ax2 = axes[0, 1]
    bars = ax2.barh(tech_data['Tecnologia'], tech_data['ROI_3_anni'],
                     color='#2ca02c')
    
    # Aggiungi valori
    for bar in bars:
        width = bar.get_width()
        ax2.text(width + 5, bar.get_y() + bar.get_height()/2.,
                f'{width:.0f}%', ha='left', va='center')
    
    ax2.set_xlabel('ROI a 3 anni (%)')
    ax2.set_title('ROI delle Tecnologie Difensive')
    ax2.set_xlim(0, 450)
    
    # 3. Seasonal Patterns
    seasonal_data = create_seasonal_patterns_table()
    seasonal_data_clean = seasonal_data[seasonal_data['Periodo'] != 'Baseline']
    
    ax3 = axes[1, 0]
    x = np.arange(len(seasonal_data_clean))
    bars = ax3.bar(x, seasonal_data_clean['Moltiplicatore'],
                    color=['#d62728', '#ff7f0e', '#2ca02c', '#1f77b4', '#9467bd'])
    
    ax3.set_xlabel('Periodo')
    ax3.set_ylabel('Moltiplicatore vs Baseline')
    ax3.set_title('Pattern Stagionali degli Attacchi')
    ax3.set_xticks(x)
    ax3.set_xticklabels(seasonal_data_clean['Periodo'], rotation=45, ha='right')
    ax3.axhline(y=1, color='black', linestyle='--', alpha=0.5)
    
    # Aggiungi valori
    for bar in bars:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                f'{height:.1f}x', ha='center', va='bottom')
    
    # 4. Zero Trust Impact
    zt_data = create_zero_trust_assa_table()
    zt_data_clean = zt_data[zt_data['Componente_ZT'] != 'Effetto Combinato']
    
    ax4 = axes[1, 1]
    x = np.arange(len(zt_data_clean))
    width = 0.35
    
    bars1 = ax4.bar(x - width/2, zt_data_clean['ASSA_Totale'], 
                     width, label='Riduzione ASSA (%)')
    bars2 = ax4.bar(x + width/2, zt_data_clean['Latenza_ms'], 
                     width, label='Latenza Aggiunta (ms)')
    
    ax4.set_xlabel('Componente Zero Trust')
    ax4.set_ylabel('Valore')
    ax4.set_title('Trade-off Zero Trust: Sicurezza vs Latenza')
    ax4.set_xticks(x)
    ax4.set_xticklabels(zt_data_clean['Componente_ZT'], rotation=45, ha='right')
    ax4.legend()
    
    plt.tight_layout()
    plt.savefig('tabelle_capitolo2_visualizations.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("\nVisualizzazioni salvate in 'tabelle_capitolo2_visualizations.png'")

# ========== ESECUZIONE PRINCIPALE ==========

if __name__ == "__main__":
    print("Generazione Tabelle Capitolo 2...")
    print("="*60)
    
    # Genera tutte le tabelle
    print("\n1. Generazione Tabella 2.1...")
    threat_df, threat_latex = create_threat_characterization_table()
    
    print("\n2. Generazione Tabella 2.2...")
    assa_comp, assa_amp = create_assa_parameters_table()
    
    print("\n3. Generazione Tabella 2.3...")
    seasonal_df = create_seasonal_patterns_table()
    
    print("\n4. Generazione Tabella 2.4...")
    tech_df = create_defensive_technologies_table()
    
    print("\n5. Generazione Tabella 2.5...")
    roadmap_df, roadmap_totals = create_implementation_roadmap_table()
    
    print("\n6. Generazione Tabella 2.6...")
    zt_assa_df = create_zero_trust_assa_table()
    
    print("\n7. Creazione visualizzazioni...")
    create_table_visualizations()
    
    print("\n" + "="*60)
    print("Tutte le tabelle sono state generate!")
    print("File CSV salvati nella directory corrente")
    print("Codice LaTeX disponibile nell'artifact 'tabelle-capitolo2-latex'")
    
    # Genera summary report
    summary = f"""
    SUMMARY REPORT - Tabelle Capitolo 2
    =====================================
    
    Tabella 2.1: {len(threat_df)-1} tipologie di minacce analizzate
    Tabella 2.2: {len(assa_comp)} componenti ASSA + {len(assa_amp)} fattori amplificazione
    Tabella 2.3: {len(seasonal_df)-1} pattern stagionali identificati
    Tabella 2.4: {len(tech_df)} tecnologie difensive comparate
    Tabella 2.5: 3 fasi implementative su {roadmap_totals['Durata_Totale_mesi']} mesi
    Tabella 2.6: {len(zt_assa_df)-1} componenti Zero Trust analizzati
    
    Investimento totale roadmap: €{roadmap_totals['Investimento_Totale_MEur']}M
    ROI medio atteso: {roadmap_totals['ROI_Medio']:.0f}%
    """
    
    print(summary)
    
    with open('tabelle_capitolo2_summary.txt', 'w') as f:
        f.write(summary)
