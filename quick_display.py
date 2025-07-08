#!/usr/bin/env python3
"""
VISUALIZZAZIONE RAPIDA RISULTATI SIMULAZIONE
============================================
Mostra i risultati della simulazione senza problemi di serializzazione JSON
"""

import pandas as pd
from scipy import stats
import numpy as np

def display_results():
    """Mostra risultati rapidi della simulazione"""
    
    try:
        # Carica risultati CSV
        h1_df = pd.read_csv('h1_cloud_results.csv')
        h2_df = pd.read_csv('h2_zerotrust_results.csv') 
        h3_df = pd.read_csv('h3_compliance_results.csv')
        
        print("RISULTATI SIMULAZIONE - VALIDAZIONE IPOTESI H1, H2, H3")
        print("=" * 65)
        print(f"Campione: {len(h1_df)} organizzazioni GDO simulate")
        print(f"Metodologia: Discrete Event Simulation")
        print(f"Confidence Level: 95% (α = 0.05)")
        
        print("\nH1 - EFFICACIA CLOUD-FIRST")
        print("-" * 35)
        print(f"Target: SLA ≥99.95%, TCO reduction ≥15%, overhead <3%")
        print()
        
        # Metriche H1
        h1_success_rate = h1_df['h1_success'].mean()
        availability_mean = h1_df['achieved_availability'].mean()
        availability_std = h1_df['achieved_availability'].std()
        tco_mean = h1_df['tco_reduction_percent'].mean()
        tco_std = h1_df['tco_reduction_percent'].std()
        overhead_mean = h1_df['operational_overhead_percent'].mean()
        overhead_std = h1_df['operational_overhead_percent'].std()
        total_savings = h1_df['tco_savings_m_euro'].sum()
        
        print(f"Success Rate: {h1_success_rate:.1%}")
        print(f"Availability media: {availability_mean:.4f} (σ={availability_std:.4f})")
        print(f"TCO reduction media: {tco_mean:.1f}% (σ={tco_std:.1f}%)")
        print(f"Overhead operativo: {overhead_mean:.1f}% (σ={overhead_std:.1f}%)")
        print(f"Risparmi totali: €{total_savings:.1f}M")
        
        # Test statistici H1
        t_avail, p_avail = stats.ttest_1samp(h1_df['achieved_availability'], 0.9995, alternative='greater')
        t_tco, p_tco = stats.ttest_1samp(h1_df['tco_reduction_percent'], 15, alternative='greater')
        t_overhead, p_overhead = stats.ttest_1samp(h1_df['operational_overhead_percent'], 3, alternative='less')
        
        print(f"\nTest Statistici H1:")
        print(f"  Availability ≥99.95%: t={t_avail:.3f}, p={p_avail:.4f} {'✓' if p_avail < 0.05 else '✗'}")
        print(f"  TCO reduction ≥15%:   t={t_tco:.3f}, p={p_tco:.4f} {'✓' if p_tco < 0.05 else '✗'}")
        print(f"  Overhead <3%:         t={t_overhead:.3f}, p={p_overhead:.4f} {'✓' if p_overhead < 0.05 else '✗'}")
        
        h1_validated = (p_avail < 0.05 and p_tco < 0.05 and p_overhead < 0.05 and h1_success_rate >= 0.8)
        print(f"\n🔍 CONCLUSIONE H1: {'✅ VALIDATA' if h1_validated else '❌ NON VALIDATA'}")
        
        print("\n" + "=" * 65)
        print("H2 - INTEGRAZIONE ZERO TRUST")
        print("-" * 35)
        print(f"Target: ASSA reduction ≥20%, latency overhead <25ms")
        print()
        
        # Metriche H2
        h2_success_rate = h2_df['h2_success'].mean()
        assa_mean = h2_df['assa_reduction_percent'].mean()
        assa_std = h2_df['assa_reduction_percent'].std()
        latency_mean = h2_df['zt_latency_overhead_ms'].mean()
        latency_std = h2_df['zt_latency_overhead_ms'].std()
        
        print(f"Success Rate: {h2_success_rate:.1%}")
        print(f"ASSA reduction media: {assa_mean:.1f}% (σ={assa_std:.1f}%)")
        print(f"Latency overhead: {latency_mean:.1f}ms (σ={latency_std:.1f}ms)")
        
        # Test statistici H2
        t_assa, p_assa = stats.ttest_1samp(h2_df['assa_reduction_percent'], 20, alternative='greater')
        t_latency, p_latency = stats.ttest_1samp(h2_df['zt_latency_overhead_ms'], 25, alternative='less')
        
        print(f"\nTest Statistici H2:")
        print(f"  ASSA reduction ≥20%: t={t_assa:.3f}, p={p_assa:.4f} {'✓' if p_assa < 0.05 else '✗'}")
        print(f"  Latency <25ms:       t={t_latency:.3f}, p={p_latency:.4f} {'✓' if p_latency < 0.05 else '✗'}")
        
        h2_validated = (p_assa < 0.05 and p_latency < 0.05 and h2_success_rate >= 0.8)
        print(f"\n🔍 CONCLUSIONE H2: {'✅ VALIDATA' if h2_validated else '❌ NON VALIDATA'}")
        
        print("\n" + "=" * 65)
        print("H3 - COMPLIANCE-BY-DESIGN")
        print("-" * 35)
        print(f"Target: Cost reduction 30-40%, overhead operativo <10%")
        print()
        
        # Metriche H3
        h3_success_rate = h3_df['h3_success'].mean()
        cost_mean = h3_df['cost_reduction_percent'].mean()
        cost_std = h3_df['cost_reduction_percent'].std()
        oh_mean = h3_df['operational_overhead_percent'].mean()
        oh_std = h3_df['operational_overhead_percent'].std()
        coverage_mean = h3_df['compliance_coverage_percent'].mean()
        compliance_savings = h3_df['cost_savings_m_euro'].sum()
        audit_efficiency = h3_df['audit_efficiency_improvement_percent'].mean()
        
        print(f"Success Rate: {h3_success_rate:.1%}")
        print(f"Cost reduction media: {cost_mean:.1f}% (σ={cost_std:.1f}%)")
        print(f"Overhead operativo: {oh_mean:.1f}% (σ={oh_std:.1f}%)")
        print(f"Coverage compliance: {coverage_mean:.1f}%")
        print(f"Risparmi compliance: €{compliance_savings:.1f}M")
        print(f"Efficienza audit: +{audit_efficiency:.1f}%")
        
        # Test statistici H3
        t_cost, p_cost = stats.ttest_1samp(h3_df['cost_reduction_percent'], 30, alternative='greater')
        t_oh, p_oh = stats.ttest_1samp(h3_df['operational_overhead_percent'], 10, alternative='less')
        t_coverage, p_coverage = stats.ttest_1samp(h3_df['compliance_coverage_percent'], 90, alternative='greater')
        
        print(f"\nTest Statistici H3:")
        print(f"  Cost reduction ≥30%: t={t_cost:.3f}, p={p_cost:.4f} {'✓' if p_cost < 0.05 else '✗'}")
        print(f"  Overhead <10%:       t={t_oh:.3f}, p={p_oh:.4f} {'✓' if p_oh < 0.05 else '✗'}")
        print(f"  Coverage ≥90%:       t={t_coverage:.3f}, p={p_coverage:.4f} {'✓' if p_coverage < 0.05 else '✗'}")
        
        h3_validated = (p_cost < 0.05 and p_oh < 0.05 and p_coverage < 0.05 and h3_success_rate >= 0.8)
        print(f"\n🔍 CONCLUSIONE H3: {'✅ VALIDATA' if h3_validated else '❌ NON VALIDATA'}")
        
        # RISULTATO FINALE
        total_validated = sum([h1_validated, h2_validated, h3_validated])
        
        print("\n" + "=" * 65)
        print("🎯 RISULTATO FINALE VALIDAZIONE")
        print("=" * 65)
        
        print(f"Ipotesi validate: {total_validated}/3")
        print(f"H1 (Cloud-First): {'✅ VALIDATA' if h1_validated else '❌ NON VALIDATA'}")
        print(f"H2 (Zero Trust):  {'✅ VALIDATA' if h2_validated else '❌ NON VALIDATA'}")
        print(f"H3 (Compliance):  {'✅ VALIDATA' if h3_validated else '❌ NON VALIDATA'}")
        
        print(f"\n📊 METRICHE CHIAVE AGGREGATE:")
        print(f"• Risparmi TCO totali: €{total_savings:.1f}M")
        print(f"• Risparmi compliance: €{compliance_savings:.1f}M")
        print(f"• Riduzione superficie attacco: {assa_mean:.1f}%")
        print(f"• Availability media: {availability_mean:.4f}")
        print(f"• Coverage compliance: {coverage_mean:.1f}%")
        
        if total_validated >= 2:
            print(f"\n🎉 SUCCESSO: {total_validated}/3 ipotesi validate con significatività statistica!")
            print("   Le evidenze supportano la fattibilità delle trasformazioni proposte.")
        else:
            print(f"\n⚠️  RISULTATO PARZIALE: Solo {total_validated}/3 ipotesi validate.")
            print("   Considerare revisione parametri o rafforzamento metodologia.")
        
        # Raccomandazioni per la tesi
        print(f"\n📝 PER LA TESI:")
        print("• Utilizzare i p-values mostrati per validazione statistica")
        print("• Includere grafici già generati: hypothesis_validation_results.png")
        print("• Citare metodologia DES nella sezione metodologica")
        print("• Evidenziare correlazioni maturità-performance")
        
        # Salva riassunto per la tesi
        with open('thesis_summary_results.txt', 'w', encoding='utf-8') as f:
            f.write("RIASSUNTO RISULTATI PER TESI\n")
            f.write("=" * 35 + "\n\n")
            
            f.write("VALIDAZIONE IPOTESI:\n")
            f.write(f"H1 (Cloud-First): {'VALIDATA' if h1_validated else 'NON VALIDATA'}\n")
            f.write(f"H2 (Zero Trust): {'VALIDATA' if h2_validated else 'NON VALIDATA'}\n")
            f.write(f"H3 (Compliance): {'VALIDATA' if h3_validated else 'NON VALIDATA'}\n")
            f.write(f"Totale: {total_validated}/3\n\n")
            
            f.write("METRICHE PRINCIPALI:\n")
            f.write(f"• Availability media: {availability_mean:.4f} (target: ≥0.9995)\n")
            f.write(f"• TCO reduction: {tco_mean:.1f}% (target: ≥15%)\n")
            f.write(f"• ASSA reduction: {assa_mean:.1f}% (target: ≥20%)\n")
            f.write(f"• Cost reduction compliance: {cost_mean:.1f}% (target: 30-40%)\n")
            f.write(f"• Latency overhead: {latency_mean:.1f}ms (target: <25ms)\n\n")
            
            f.write("SIGNIFICATIVITÀ STATISTICA (α=0.05):\n")
            f.write(f"• H1 Availability: p={p_avail:.4f}\n")
            f.write(f"• H1 TCO: p={p_tco:.4f}\n")
            f.write(f"• H2 ASSA: p={p_assa:.4f}\n")
            f.write(f"• H2 Latency: p={p_latency:.4f}\n")
            f.write(f"• H3 Cost: p={p_cost:.4f}\n")
            f.write(f"• H3 Overhead: p={p_oh:.4f}\n\n")
            
            f.write("BENEFICI ECONOMICI:\n")
            f.write(f"• Risparmi TCO: €{total_savings:.1f}M\n")
            f.write(f"• Risparmi compliance: €{compliance_savings:.1f}M\n")
            f.write(f"• Totale: €{total_savings + compliance_savings:.1f}M\n")
        
        print(f"\n💾 File salvato: thesis_summary_results.txt")
        
    except FileNotFoundError as e:
        print("❌ Errore: File CSV non trovati!")
        print("Verificare che la simulazione principale sia stata eseguita.")
        print(f"File mancante: {e.filename}")
    
    except Exception as e:
        print(f"❌ Errore nell'analisi: {e}")

if __name__ == "__main__":
    display_results()
