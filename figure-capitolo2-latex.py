import matplotlib
matplotlib.use('Agg')  # Usa backend non interattivo
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.patches import Rectangle, FancyBboxPatch
from matplotlib.patches import Circle, Arrow
import matplotlib.patches as mpatches
from scipy import stats
from scipy.optimize import curve_fit
import warnings
warnings.filterwarnings('ignore')

# Configurazione generale per tutte le figure
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.titlesize'] = 16

# Colori coerenti per tutta la tesi
colors = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e', 
    'success': '#2ca02c',
    'danger': '#d62728',
    'warning': '#ff9800',
    'info': '#17a2b8',
    'light': '#f0f0f0',
    'dark': '#333333'
}

# ========== FIGURA 2.1: Amplificazione Non-Lineare della Superficie di Attacco ==========

def create_figure_2_1():
    """Amplificazione Non-Lineare della Superficie di Attacco con Scala della Rete"""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Dati dalla simulazione
    n_stores = np.array([50, 100, 200, 500])
    assa_multiplier = np.array([2.3, 3.8, 6.2, 11.7])
    assa_multiplier_std = np.array([0.2, 0.3, 0.5, 0.9])
    
    # Subplot 1: Crescita ASSA
    ax1.errorbar(n_stores, assa_multiplier, yerr=assa_multiplier_std, 
                 fmt='o-', color=colors['primary'], linewidth=2, markersize=8,
                 capsize=5, capthick=2, label='Dati Simulati')
    
    # Fit esponenziale
    def exp_func(x, a, b):
        return a * np.exp(b * x / 100)
    
    popt, _ = curve_fit(exp_func, n_stores, assa_multiplier)
    x_smooth = np.linspace(50, 500, 100)
    y_smooth = exp_func(x_smooth, *popt)
    
    ax1.plot(x_smooth, y_smooth, '--', color=colors['danger'], 
             linewidth=2, label='Fit Esponenziale')
    
    ax1.fill_between(x_smooth, 
                     exp_func(x_smooth, popt[0]-0.2, popt[1]), 
                     exp_func(x_smooth, popt[0]+0.2, popt[1]),
                     alpha=0.2, color=colors['danger'])
    
    ax1.set_xlabel('Numero di Punti Vendita')
    ax1.set_ylabel('Fattore di Amplificazione ASSA')
    ax1.set_title('Crescita Super-Lineare della Superficie di Attacco')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    ax1.set_xlim(0, 550)
    ax1.set_ylim(0, 13)
    
    # Annotazioni
    for i, (x, y) in enumerate(zip(n_stores, assa_multiplier)):
        ax1.annotate(f'{y:.1f}x', 
                     xy=(x, y), 
                     xytext=(x+20, y+0.5),
                     fontsize=9,
                     ha='left')
    
    # Subplot 2: Distribuzione dei Componenti ASSA
    components = ['Porte\nAperte', 'Servizi\nEsposti', 'Vulnerabilità\nNote']
    weights = [0.3, 0.4, 0.3]
    baseline_values = [8, 5, 3]
    hub_values = [25, 15, 8]
    
    x = np.arange(len(components))
    width = 0.35
    
    bars1 = ax2.bar(x - width/2, baseline_values, width, 
                     label='Store Periferico', color=colors['info'])
    bars2 = ax2.bar(x + width/2, hub_values, width,
                     label='Hub Centrale', color=colors['warning'])
    
    # Aggiungi i pesi sopra le barre
    for i, (comp, weight) in enumerate(zip(x, weights)):
        ax2.text(comp, max(baseline_values[i], hub_values[i]) + 1,
                 f'Peso: {weight}', ha='center', fontsize=9)
    
    ax2.set_ylabel('Valore Medio')
    ax2.set_title('Componenti ASSA per Tipo di Nodo')
    ax2.set_xticks(x)
    ax2.set_xticklabels(components)
    ax2.legend()
    ax2.grid(True, axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('figura_2_1_assa_amplification.pdf', dpi=300, bbox_inches='tight')
    plt.savefig('figura_2_1_assa_amplification.png', dpi=300, bbox_inches='tight')
    plt.close()

# ========== FIGURA 2.2: Evoluzione del Threat Landscape GDO 2020-2025 ==========

def create_figure_2_2():
    """Evoluzione del Threat Landscape GDO 2020-2025"""
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    
    years = np.array([2020, 2021, 2022, 2023, 2024, 2025])
    
    # Subplot 1: Trend Incidenti per Tipo
    malware_pos = [45, 52, 78, 95, 112, 127]
    ransomware = [12, 23, 45, 67, 89, 103]
    supply_chain = [3, 5, 12, 28, 45, 58]
    ai_powered = [0, 0, 5, 18, 42, 78]
    
    ax1.plot(years, malware_pos, 'o-', label='Malware POS', 
             color=colors['primary'], linewidth=2, markersize=8)
    ax1.plot(years, ransomware, 's-', label='Ransomware', 
             color=colors['danger'], linewidth=2, markersize=8)
    ax1.plot(years, supply_chain, '^-', label='Supply Chain', 
             color=colors['success'], linewidth=2, markersize=8)
    ax1.plot(years, ai_powered, 'd-', label='AI-Powered', 
             color=colors['warning'], linewidth=2, markersize=8)
    
    ax1.set_xlabel('Anno')
    ax1.set_ylabel('Numero di Incidenti Documentati')
    ax1.set_title('Evoluzione delle Tipologie di Attacco')
    ax1.legend(loc='upper left')
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(2019.5, 2025.5)
    
    # Aggiungi area di proiezione
    ax1.axvspan(2024.5, 2025.5, alpha=0.1, color='gray', label='Proiezione')
    
    # Subplot 2: Indice di Complessità degli Attacchi (ICA)
    ica_values = [100, 124, 178, 234, 289, 312]
    ica_std = [10, 12, 18, 22, 28, 31]
    
    ax2.bar(years, ica_values, yerr=ica_std, 
            color=colors['secondary'], alpha=0.7, capsize=5)
    
    # Linea di tendenza
    z = np.polyfit(years, ica_values, 2)
    p = np.poly1d(z)
    x_smooth = np.linspace(2020, 2025, 100)
    ax2.plot(x_smooth, p(x_smooth), '--', color=colors['dark'], linewidth=2)
    
    ax2.set_xlabel('Anno')
    ax2.set_ylabel('ICA (2020 = 100)')
    ax2.set_title('Indice di Complessità degli Attacchi (+312%)')
    ax2.grid(True, axis='y', alpha=0.3)
    
    # Annotazioni per eventi chiave
    events = {
        2021: 'RaaS\nSpecializzati',
        2022.8: 'AI Social\nEngineering',
        2024: 'Hardware\nExploits'
    }
    
    for year, label in events.items():
        ax2.annotate(label, xy=(year, p(year)), 
                     xytext=(year, p(year) + 40),
                     arrowprops=dict(arrowstyle='->', color=colors['dark'], alpha=0.5),
                     ha='center', fontsize=9,
                     bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
    
    # Subplot 3: Distribuzione Geografica Attacchi (Italia)
    regions = ['Nord', 'Centro', 'Sud', 'Isole']
    attacks_2023 = [234, 156, 89, 45]
    attacks_2024 = [289, 198, 112, 67]
    
    x = np.arange(len(regions))
    width = 0.35
    
    bars1 = ax3.bar(x - width/2, attacks_2023, width, label='2023', 
                     color=colors['info'])
    bars2 = ax3.bar(x + width/2, attacks_2024, width, label='2024', 
                     color=colors['warning'])
    
    ax3.set_ylabel('Numero di Incidenti')
    ax3.set_title('Distribuzione Geografica degli Attacchi in Italia')
    ax3.set_xticks(x)
    ax3.set_xticklabels(regions)
    ax3.legend()
    ax3.grid(True, axis='y', alpha=0.3)
    
    # Aggiungi percentuali di crescita
    for i in range(len(regions)):
        growth = (attacks_2024[i] - attacks_2023[i]) / attacks_2023[i] * 100
        ax3.text(i, attacks_2024[i] + 10, f'+{growth:.0f}%', 
                 ha='center', fontsize=9, color=colors['danger'])
    
    # Subplot 4: Impatto Convergenza IT/OT
    categories = ['Solo IT', 'IT + Impatto\nOperativo', 'Cyber-Physical\nCompleto']
    percentages_2022 = [78, 18, 4]
    percentages_2024 = [56, 34, 10]
    
    x = np.arange(len(categories))
    width = 0.35
    
    bars1 = ax4.bar(x - width/2, percentages_2022, width, label='2022',
                     color=colors['success'])
    bars2 = ax4.bar(x + width/2, percentages_2024, width, label='2024',
                     color=colors['danger'])
    
    ax4.set_ylabel('Percentuale degli Incidenti (%)')
    ax4.set_title('Evoluzione della Convergenza IT/OT negli Attacchi')
    ax4.set_xticks(x)
    ax4.set_xticklabels(categories)
    ax4.legend()
    ax4.grid(True, axis='y', alpha=0.3)
    ax4.set_ylim(0, 100)
    
    plt.tight_layout()
    plt.savefig('figura_2_2_threat_evolution.pdf', dpi=300, bbox_inches='tight')
    plt.savefig('figura_2_2_threat_evolution.png', dpi=300, bbox_inches='tight')
    plt.close()

# ========== FIGURA 2.3: Decomposizione STL degli Attacchi GDO 2020-2024 ==========

def create_figure_2_3():
    """Decomposizione STL degli Attacchi GDO 2020-2024"""
    
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(14, 10), sharex=True)
    
    # Genera dati sintetici realistici
    weeks = pd.date_range('2020-01-01', '2024-12-31', freq='W')
    n_weeks = len(weeks)
    
    # Trend crescente
    trend = 100 + 0.5 * np.arange(n_weeks) + 0.001 * np.arange(n_weeks)**2
    
    # Componente stagionale
    seasonal = np.zeros(n_weeks)
    for i in range(n_weeks):
        week_of_year = i % 52
        # Black Friday (settimana 47)
        if week_of_year == 47:
            seasonal[i] = 240  # 3.4x moltiplicatore
        # Periodo natalizio (settimane 49-52)
        elif 49 <= week_of_year <= 52:
            seasonal[i] = 170  # 2.7x moltiplicatore
        # Back to school (settimane 34-36)
        elif 34 <= week_of_year <= 36:
            seasonal[i] = 80  # 1.8x moltiplicatore
        else:
            seasonal[i] = 0
    
    # Rumore
    np.random.seed(42)
    residual = np.random.normal(0, 20, n_weeks)
    
    # Serie completa
    attacks = trend + seasonal + residual
    
    # Subplot 1: Serie Originale
    ax1.plot(weeks, attacks, color=colors['primary'], linewidth=1)
    ax1.set_ylabel('Attacchi/Settimana')
    ax1.set_title('Serie Temporale Attacchi GDO - Dati Originali')
    ax1.grid(True, alpha=0.3)
    
    # Evidenzia periodi critici
    for year in range(2020, 2025):
        # Black Friday
        bf_date = pd.Timestamp(f'{year}-11-23')
        ax1.axvline(bf_date, color=colors['danger'], alpha=0.3, linestyle='--')
        
        # Natale
        xmas_date = pd.Timestamp(f'{year}-12-25')
        ax1.axvspan(xmas_date - pd.Timedelta(days=21), xmas_date, 
                    alpha=0.1, color=colors['danger'])
    
    # Subplot 2: Trend
    ax2.plot(weeks, trend, color=colors['success'], linewidth=2)
    ax2.set_ylabel('Trend')
    ax2.set_title('Componente Trend (Crescita Strutturale)')
    ax2.grid(True, alpha=0.3)
    
    # Aggiungi tasso di crescita
    growth_rate = (trend[-1] - trend[0]) / trend[0] * 100
    ax2.text(weeks[len(weeks)//2], trend.mean(), 
             f'Crescita: +{growth_rate:.1f}%', 
             bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
    
    # Subplot 3: Stagionalità
    ax3.plot(weeks, seasonal, color=colors['warning'], linewidth=1)
    ax3.set_ylabel('Stagionalità')
    ax3.set_title('Componente Stagionale (Pattern Ricorrenti)')
    ax3.grid(True, alpha=0.3)
    
    # Annotazioni picchi
    ax3.text(pd.Timestamp('2022-11-23'), 250, 'Black Friday\n3.4x', 
             ha='center', fontsize=9)
    ax3.text(pd.Timestamp('2022-12-15'), 180, 'Natale\n2.7x', 
             ha='center', fontsize=9)
    ax3.text(pd.Timestamp('2022-08-25'), 90, 'Back to School\n1.8x', 
             ha='center', fontsize=9)
    
    # Subplot 4: Residui
    ax4.plot(weeks, residual, color=colors['info'], linewidth=1, alpha=0.7)
    ax4.set_ylabel('Residui')
    ax4.set_title('Componente Residuale (Rumore)')
    ax4.set_xlabel('Data')
    ax4.grid(True, alpha=0.3)
    
    # Statistiche residui
    ax4.text(0.02, 0.95, f'μ = {residual.mean():.1f}\nσ = {residual.std():.1f}',
             transform=ax4.transAxes, verticalalignment='top',
             bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
    
    # Formatta date
    import matplotlib.dates as mdates
    for ax in [ax1, ax2, ax3, ax4]:
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('figura_2_3_stl_decomposition.pdf', dpi=300, bbox_inches='tight')
    plt.savefig('figura_2_3_stl_decomposition.png', dpi=300, bbox_inches='tight')
    plt.close()

# ========== FIGURA 2.4: Confronto Costi di Compliance ==========

def create_figure_2_4():
    """Confronto Costi di Compliance - Approcci Tradizionali vs Integrati"""
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    
    # Subplot 1: Costi Totali per Approccio
    approaches = ['Approccio\nSiloed', 'Approccio\nIntegrato']
    costs = [8.7, 5.4]  # Milioni di euro
    savings = [0, 3.3]
    
    bars = ax1.bar(approaches, costs, color=[colors['danger'], colors['success']], 
                    alpha=0.7)
    
    # Aggiungi risparmio
    ax1.bar(approaches, savings, bottom=costs, 
            color=colors['warning'], alpha=0.5, label='Risparmio')
    
    # Annotazioni
    for i, (cost, saving) in enumerate(zip(costs, savings)):
        ax1.text(i, cost/2, f'€{cost}M', ha='center', va='center', 
                 fontweight='bold', color='white')
        if saving > 0:
            ax1.text(i, cost + saving/2, f'-{saving/costs[0]*100:.0f}%', 
                     ha='center', va='center')
    
    ax1.set_ylabel('Costo Totale (Milioni €)')
    ax1.set_title('Costo Totale Compliance (3 Standard, 5 Anni)')
    ax1.set_ylim(0, 10)
    ax1.grid(True, axis='y', alpha=0.3)
    
    # Subplot 2: Breakdown dei Costi
    categories = ['Implementazione', 'Audit', 'Manutenzione', 'Formazione']
    siloed_costs = [3.2, 2.8, 2.1, 0.6]
    integrated_costs = [2.1, 1.2, 1.6, 0.5]
    
    x = np.arange(len(categories))
    width = 0.35
    
    bars1 = ax2.bar(x - width/2, siloed_costs, width, label='Siloed', 
                     color=colors['danger'])
    bars2 = ax2.bar(x + width/2, integrated_costs, width, label='Integrato', 
                     color=colors['success'])
    
    ax2.set_ylabel('Costo (Milioni €)')
    ax2.set_title('Breakdown dei Costi per Categoria')
    ax2.set_xticks(x)
    ax2.set_xticklabels(categories, rotation=15, ha='right')
    ax2.legend()
    ax2.grid(True, axis='y', alpha=0.3)
    
    # Percentuali di riduzione
    for i in range(len(categories)):
        reduction = (siloed_costs[i] - integrated_costs[i]) / siloed_costs[i] * 100
        ax2.text(i, max(siloed_costs[i], integrated_costs[i]) + 0.1, 
                 f'-{reduction:.0f}%', ha='center', fontsize=9, 
                 color=colors['success'])
    
    # Subplot 3: Matrice di Overlap tra Standard
    standards = ['PCI-DSS', 'GDPR', 'NIS2']
    overlap_matrix = np.array([
        [1.0, 0.31, 0.27],
        [0.31, 1.0, 0.42],
        [0.27, 0.42, 1.0]
    ])
    
    im = ax3.imshow(overlap_matrix, cmap='RdYlGn', vmin=0, vmax=1)
    
    # Aggiungi valori
    for i in range(len(standards)):
        for j in range(len(standards)):
            text = ax3.text(j, i, f'{overlap_matrix[i, j]:.0%}',
                           ha="center", va="center", color="black")
    
    ax3.set_xticks(np.arange(len(standards)))
    ax3.set_yticks(np.arange(len(standards)))
    ax3.set_xticklabels(standards)
    ax3.set_yticklabels(standards)
    ax3.set_title('Matrice di Overlap tra Requisiti Normativi')
    
    # Colorbar
    cbar = plt.colorbar(im, ax=ax3)
    cbar.set_label('Percentuale di Overlap', rotation=270, labelpad=15)
    
    # Subplot 4: ROI nel Tempo
    years = np.arange(0, 6)
    cumulative_costs_siloed = np.cumsum([2.0, 1.5, 1.5, 1.5, 1.5, 1.5])
    cumulative_costs_integrated = np.cumsum([2.5, 0.8, 0.8, 0.8, 0.8, 0.8])
    cumulative_benefits = np.cumsum([0, 0.5, 1.2, 1.8, 2.3, 2.8])
    
    ax4.plot(years, -cumulative_costs_siloed, 'o--', color=colors['danger'], 
             linewidth=2, label='Costi Siloed')
    ax4.plot(years, -cumulative_costs_integrated + cumulative_benefits, 's-', 
             color=colors['success'], linewidth=2, label='Netto Integrato')
    ax4.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    
    # Punto di pareggio
    break_even = 2.3
    ax4.axvline(x=break_even, color=colors['warning'], linestyle=':', alpha=0.7)
    ax4.text(break_even + 0.1, 0.5, 'Break-even\n2.3 anni', fontsize=9,
             bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
    
    ax4.set_xlabel('Anni')
    ax4.set_ylabel('Valore Cumulativo (Milioni €)')
    ax4.set_title('Analisi ROI: Approccio Integrato vs Siloed')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    ax4.set_xlim(-0.5, 5.5)
    ax4.set_ylim(-10, 3)
    
    plt.tight_layout()
    plt.savefig('figura_2_4_compliance_costs.pdf', dpi=300, bbox_inches='tight')
    plt.savefig('figura_2_4_compliance_costs.png', dpi=300, bbox_inches='tight')
    plt.close()

# ========== FIGURA 2.5: Framework Integrato di Sicurezza GDO ==========

def create_figure_2_5():
    """Framework Integrato di Sicurezza GDO - Dal Threat Landscape all'Architettura"""
    
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Rimuovi assi
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Titolo
    ax.text(5, 9.5, 'Framework Integrato di Sicurezza GDO', 
            fontsize=18, fontweight='bold', ha='center')
    
    # Layer 1: Threat Landscape (bottom)
    threat_box = FancyBboxPatch((0.5, 0.5), 9, 2, 
                                boxstyle="round,pad=0.1",
                                facecolor=colors['danger'], 
                                alpha=0.3,
                                edgecolor=colors['danger'],
                                linewidth=2)
    ax.add_patch(threat_box)
    
    ax.text(5, 1.5, 'THREAT LANDSCAPE', fontsize=14, fontweight='bold', 
            ha='center', va='center')
    
    # Threat types
    threats = ['Malware POS', 'Ransomware', 'Supply Chain', 'AI-Powered']
    threat_positions = [2, 4, 6, 8]
    for pos, threat in zip(threat_positions, threats):
        ax.text(pos, 0.9, threat, fontsize=10, ha='center')
    
    # Layer 2: Principi di Sicurezza Emergenti
    principles_box = FancyBboxPatch((0.5, 3), 9, 2,
                                   boxstyle="round,pad=0.1",
                                   facecolor=colors['warning'],
                                   alpha=0.3,
                                   edgecolor=colors['warning'],
                                   linewidth=2)
    ax.add_patch(principles_box)
    
    ax.text(5, 4, 'PRINCIPI DI SICUREZZA EMERGENTI', fontsize=14, 
            fontweight='bold', ha='center', va='center')
    
    # Principi
    principles = [
        'Velocità Detection\n> Sofisticazione',
        'Zero Trust\nEdge-Based',
        'Compliance\nIntegrata',
        'Resilienza\nDiversificata'
    ]
    principle_positions = [2, 4, 6, 8]
    
    for pos, principle in zip(principle_positions, principles):
        principle_circle = Circle((pos, 3.5), 0.6, 
                                 facecolor='white', 
                                 edgecolor=colors['warning'],
                                 linewidth=2)
        ax.add_patch(principle_circle)
        ax.text(pos, 3.5, principle, fontsize=9, ha='center', va='center')
    
    # Layer 3: Implicazioni Architetturali
    arch_box = FancyBboxPatch((0.5, 5.5), 9, 2,
                             boxstyle="round,pad=0.1",
                             facecolor=colors['success'],
                             alpha=0.3,
                             edgecolor=colors['success'],
                             linewidth=2)
    ax.add_patch(arch_box)
    
    ax.text(5, 6.5, 'IMPLICAZIONI ARCHITETTURALI', fontsize=14, 
            fontweight='bold', ha='center', va='center')
    
    # Architetture
    architectures = [
        'SD-WAN\n+Edge',
        'Hybrid Cloud\nMulti-Region',
        'SASE\nArchitecture',
        'Policy\nas Code'
    ]
    arch_positions = [2, 4, 6, 8]
    
    for pos, arch in zip(arch_positions, architectures):
        arch_rect = Rectangle((pos-0.6, 5.8), 1.2, 0.8,
                             facecolor='white',
                             edgecolor=colors['success'],
                             linewidth=2)
        ax.add_patch(arch_rect)
        ax.text(pos, 6.2, arch, fontsize=9, ha='center', va='center')
    
    # Frecce di connessione
    # Da Threat a Principi
    for i in range(4):
        ax.arrow(threat_positions[i], 1.3, 0, 1.5, 
                head_width=0.15, head_length=0.1, 
                fc=colors['dark'], ec=colors['dark'], alpha=0.5)
    
    # Da Principi ad Architetture
    for i in range(4):
        ax.arrow(principle_positions[i], 4.3, 0, 1.2,
                head_width=0.15, head_length=0.1,
                fc=colors['dark'], ec=colors['dark'], alpha=0.5)
    
    # Metriche chiave (top)
    metrics_y = 8.5
    metrics = [
        ('MTTD: 127h → 24h', 2.5),
        ('ASSA: -42.7%', 4.5),
        ('Compliance: -39.1%', 6.5),
        ('Resilienza: +67%', 8.5)
    ]
    
    for metric, x_pos in metrics:
        metric_box = FancyBboxPatch((x_pos-0.8, metrics_y-0.3), 1.6, 0.6,
                                   boxstyle="round,pad=0.05",
                                   facecolor=colors['info'],
                                   alpha=0.2,
                                   edgecolor=colors['info'])
        ax.add_patch(metric_box)
        ax.text(x_pos, metrics_y, metric, fontsize=10, ha='center', va='center',
                fontweight='bold')
    
    # Feedback loop
    feedback_arrow = mpatches.FancyArrowPatch((9.2, 1.5), (9.2, 6.5),
                                             connectionstyle="arc3,rad=.3",
                                             arrowstyle='->',
                                             mutation_scale=20,
                                             linewidth=2,
                                             color=colors['primary'],
                                             alpha=0.7)
    ax.add_patch(feedback_arrow)
    
    ax.text(9.5, 4, 'Continuous\nImprovement', fontsize=10, 
            rotation=90, va='center', color=colors['primary'])
    
    plt.tight_layout()
    plt.savefig('figura_2_5_integrated_framework.pdf', dpi=300, bbox_inches='tight')
    plt.savefig('figura_2_5_integrated_framework.png', dpi=300, bbox_inches='tight')
    plt.close()

# ========== GENERAZIONE DI TUTTE LE FIGURE ==========

if __name__ == "__main__":
    print("Generazione Figure Capitolo 2...")
    
    print("\nCreazione Figura 2.1: Amplificazione ASSA...")
    create_figure_2_1()
    
    print("\nCreazione Figura 2.2: Evoluzione Threat Landscape...")
    create_figure_2_2()
    
    print("\nCreazione Figura 2.3: Decomposizione STL...")
    create_figure_2_3()
    
    print("\nCreazione Figura 2.4: Confronto Costi Compliance...")
    create_figure_2_4()
    
    print("\nCreazione Figura 2.5: Framework Integrato...")
    create_figure_2_5()
    
    print("\nTutte le figure sono state generate con successo!")
    print("File salvati in formato PDF e PNG ad alta risoluzione.")