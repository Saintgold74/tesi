import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

fig, ax = plt.subplots(figsize=(12, 10))

# Sfondo
bg = patches.Rectangle((0, 0), 10, 10, linewidth=2, 
                      edgecolor='black', facecolor='#ecf0f1')
ax.add_patch(bg)

# Titolo
ax.text(5, 9.5, 'Validazione Tecnica Framework GIST', 
        ha='center', va='center', fontsize=18, fontweight='bold')
ax.text(5, 9, 'Metriche di Performance e Affidabilità', 
        ha='center', va='center', fontsize=12, style='italic')

# Sezioni
sections = [
    {
        'title': 'Performance Computazionale',
        'y': 7.5,
        'metrics': [
            ('Latenza P99', '49.7ms', '✓', 'green'),
            ('Throughput', '8,760 TPS', '+170%', 'green'),
            ('Complessità', 'O(n log n)', 'ottimale', 'green')
        ]
    },
    {
        'title': 'Affidabilità Sistema',
        'y': 5.5,
        'metrics': [
            ('MTTF', '52,560 ore', '6 anni', 'green'),
            ('Availability', '99.96%', '4 nine', 'green'),
            ('MTTR', '<4 ore', 'RTO OK', 'green')
        ]
    },
    {
        'title': 'Sicurezza',
        'y': 3.5,
        'metrics': [
            ('ASSA Score', '-42.7%', 'target -35%', 'green'),
            ('CVE Density', '0.3/KLOC', 'basso', 'green'),
            ('MTBD', '15 minuti', 'rapido', 'green')
        ]
    },
    {
        'title': 'Efficienza Algoritmica',
        'y': 1.5,
        'metrics': [
            ('Convergenza', '10³ iter', 'veloce', 'green'),
            ('Gap ottimalità', '<5%', 'accettabile', 'green'),
            ('Tempo comp.', '<10 min', 'pratico', 'green')
        ]
    }
]

# Disegnare sezioni
for section in sections:
    # Box sezione
    section_box = patches.FancyBboxPatch((0.5, section['y']-0.8), 9, 1.5,
                                        boxstyle="round,pad=0.05",
                                        facecolor='white',
                                        edgecolor='black',
                                        linewidth=1.5)
    ax.add_patch(section_box)
    
    # Titolo sezione
    ax.text(1, section['y']+0.3, section['title'], 
            fontsize=12, fontweight='bold')
    
    # Metriche
    x_positions = [2.5, 5, 7.5]
    for i, (metric, value, note, color) in enumerate(section['metrics']):
        x = x_positions[i % 3]
        y = section['y'] - 0.2 if i < 3 else section['y'] - 0.5
        
        ax.text(x, y, f'{metric}:', fontsize=9, fontweight='bold')
        ax.text(x, y-0.2, value, fontsize=9, color=color)
        ax.text(x, y-0.4, f'({note})', fontsize=8, style='italic', color='gray')

# Footer
footer_box = patches.Rectangle((0.5, 0.1), 9, 0.6, 
                              facecolor='#34495e', 
                              edgecolor='black')
ax.add_patch(footer_box)
ax.text(5, 0.4, 'Validazione: Bootstrap 10,000 iterazioni | Significatività: p < 0.001', 
        ha='center', va='center', fontsize=10, color='white')

# Configurazione assi
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

plt.tight_layout()
plt.savefig('figura_1_5_rivista.png', dpi=300, bbox_inches='tight')