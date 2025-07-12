import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection='3d')

# Generare superficie di Pareto
latency = np.linspace(10, 100, 30)
security = np.linspace(0, 100, 30)
latency_grid, security_grid = np.meshgrid(latency, security)

# Funzione di throughput (inversamente correlata con latenza e sicurezza)
throughput_grid = 10000 * np.exp(-0.02 * latency_grid) * (1 + 0.005 * security_grid)

# Plot superficie
surf = ax.plot_surface(latency_grid, security_grid, throughput_grid, 
                      cmap='viridis', alpha=0.7, edgecolor='none')

# Aggiungere punti di configurazioni ottimali
configs = {
    'Alta Sicurezza': (80, 90, 4500),
    'Basse Latenze': (20, 40, 8500),
    'Bilanciata': (50, 70, 6500),
    'GIST Ottimale': (32, 75, 7800)
}

for name, (lat, sec, thr) in configs.items():
    color = 'red' if name == 'GIST Ottimale' else 'black'
    size = 100 if name == 'GIST Ottimale' else 50
    ax.scatter(lat, sec, thr, color=color, s=size)
    ax.text(lat, sec, thr+200, name, fontsize=9)

# Configurazione assi
ax.set_xlabel('Latenza (ms)', fontsize=11, fontweight='bold')
ax.set_ylabel('Sicurezza (ASSA Score)', fontsize=11, fontweight='bold')
ax.set_zlabel('Throughput (TPS)', fontsize=11, fontweight='bold')
ax.set_title('Trade-off Multi-Obiettivo nel Framework GIST\n' +
             'Frontiera di Pareto per Configurazioni Ottimali',
             fontsize=14, fontweight='bold', pad=20)

# Colorbar
cbar = fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
cbar.set_label('Throughput (TPS)', fontsize=10)

# Vista ottimale
ax.view_init(elev=20, azim=45)

plt.tight_layout()
plt.savefig('figura_1_7_nuova.png', dpi=300, bbox_inches='tight')