import matplotlib.pyplot as plt
import numpy as np

# Dati per il grafico
categorie = ['Modelli\nComputazionali', 'Algoritmi\nDistribuiti', 'Vincoli\nReal-Time', 'Scalabilità\nSistemica']
gap_scores = [72, 84, 76, 69]
colori = ['#3498db', '#e74c3c', '#f39c12', '#27ae60']

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(categorie, gap_scores, color=colori, alpha=0.8, edgecolor='black', linewidth=1.5)

# Aggiungere valori sopra le barre
for bar, score in zip(bars, gap_scores):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
            f'{score}%', ha='center', va='bottom', fontsize=12, fontweight='bold')

ax.set_ylim(0, 100)
ax.set_ylabel('Gap Score (%)', fontsize=12, fontweight='bold')
ax.set_xlabel('Aree di Ricerca Tecnica', fontsize=12, fontweight='bold')
ax.set_title('Gap Identificati tra Stato dell\'Arte e Requisiti GDO\n(Analisi su 234 paper IEEE/ACM)', 
             fontsize=14, fontweight='bold', pad=20)

# Aggiungere griglia
ax.grid(axis='y', alpha=0.3, linestyle='--')

# Aggiungere annotazioni tecniche
ax.axhline(y=50, color='red', linestyle='--', alpha=0.5)
ax.text(3.5, 52, 'Soglia Critica', ha='right', va='bottom', fontsize=10, style='italic', color='red')

plt.tight_layout()
plt.savefig('figura_1_1_rivista.png', dpi=300, bbox_inches='tight')