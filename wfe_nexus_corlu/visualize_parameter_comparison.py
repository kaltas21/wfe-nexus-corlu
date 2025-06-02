"""
Visualization of Parameter Comparison between Original and Updated Model Configuration
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle
import seaborn as sns

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Create figure with subplots
fig = plt.figure(figsize=(20, 24))

# 1. Technology CAPEX Comparison
ax1 = plt.subplot(4, 2, 1)
technologies = ['PV', 'Wind', 'Battery\n($/kWh)', 'Electrolyzer', 'Fuel Cell', 'CHP']
original_capex = [900, 1400, 228, 800, 1500, 1200]
updated_capex = [960, 1850, 375, 1400, 3500, 2000]
updated_low = [760, 1700, 270, 1000, 2500, 1700]
updated_high = [1160, 2000, 480, 1800, 5000, 2700]

x = np.arange(len(technologies))
width = 0.35

bars1 = ax1.bar(x - width/2, original_capex, width, label='Original', alpha=0.8, color='#ff7f0e')
bars2 = ax1.bar(x + width/2, updated_capex, width, label='Updated (Mid)', alpha=0.8, color='#2ca02c')

# Add error bars for ranges
yerr_low = [updated_capex[i] - updated_low[i] for i in range(len(technologies))]
yerr_high = [updated_high[i] - updated_capex[i] for i in range(len(technologies))]
ax1.errorbar(x + width/2, updated_capex, yerr=[yerr_low, yerr_high], 
             fmt='none', color='black', capsize=5, alpha=0.5)

ax1.set_ylabel('CAPEX ($/kW or $/kWh)', fontsize=12)
ax1.set_title('Technology Capital Costs Comparison', fontsize=14, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(technologies, rotation=45, ha='right')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Add percentage change labels
for i, (orig, upd) in enumerate(zip(original_capex, updated_capex)):
    pct_change = ((upd - orig) / orig) * 100
    ax1.text(i, max(orig, upd) + 200, f'{pct_change:+.0f}%', 
             ha='center', va='bottom', fontsize=10, fontweight='bold',
             color='darkgreen' if pct_change > 0 else 'darkred')

# 2. Discount Rate Scenarios
ax2 = plt.subplot(4, 2, 2)
scenarios = ['Original\n(All purposes)', 'Social Welfare\n(Updated)', 'Commercial\n(Updated)']
discount_rates = [8, 4.5, 20]
colors = ['#ff7f0e', '#2ca02c', '#d62728']

bars = ax2.bar(scenarios, discount_rates, color=colors, alpha=0.8)
ax2.set_ylabel('Discount Rate (%)', fontsize=12)
ax2.set_title('Discount Rate Comparison', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3, axis='y')

# Add value labels
for bar, rate in zip(bars, discount_rates):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height + 0.5,
             f'{rate}%', ha='center', va='bottom', fontsize=12, fontweight='bold')

# 3. Carbon Pricing Scenarios
ax3 = plt.subplot(4, 2, 3)
carbon_scenarios = ['Current\nBaseline', 'Future\nLow', 'Future\nMedium', 'Future\nHigh']
carbon_prices = [0, 30, 60, 100]
colors_carbon = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

bars = ax3.bar(carbon_scenarios, carbon_prices, color=colors_carbon, alpha=0.8)
ax3.set_ylabel('Carbon Price ($/ton CO2)', fontsize=12)
ax3.set_title('Carbon Pricing Scenarios (Hypothetical for Turkey)', fontsize=14, fontweight='bold')
ax3.grid(True, alpha=0.3, axis='y')

# Add annotation
ax3.text(0.5, 0.95, 'Note: Turkey has no carbon pricing as of 2025', 
         transform=ax3.transAxes, ha='center', va='top',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
         fontsize=10, style='italic')

# 4. Technology Lifespans
ax4 = plt.subplot(4, 2, 4)
tech_life = ['PV', 'Wind', 'Battery', 'Electrolyzer', 'Fuel Cell', 'CHP']
original_life = [25, 20, 15, 20, 15, 20]
updated_life = [30, 25, 15, 10, 10, 20]  # Electrolyzer and FC converted from hours

x = np.arange(len(tech_life))
width = 0.35

bars1 = ax4.bar(x - width/2, original_life, width, label='Original', alpha=0.8, color='#ff7f0e')
bars2 = ax4.bar(x + width/2, updated_life, width, label='Updated', alpha=0.8, color='#2ca02c')

ax4.set_ylabel('Lifespan (years)', fontsize=12)
ax4.set_title('Technology Lifespans Comparison', fontsize=14, fontweight='bold')
ax4.set_xticks(x)
ax4.set_xticklabels(tech_life, rotation=45, ha='right')
ax4.legend()
ax4.grid(True, alpha=0.3)

# Add notes for electrolyzer and fuel cell
ax4.text(3, 22, '50,000 hrs\n@ 5000 hrs/yr', ha='center', fontsize=9, 
         bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))
ax4.text(4, 17, '50,000 hrs\n@ 5000 hrs/yr', ha='center', fontsize=9,
         bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))

# 5. Energy Prices Comparison
ax5 = plt.subplot(4, 2, 5)
energy_types = ['Electricity Buy\n($/MWh)', 'Electricity Sell\n($/MWh)', 'Natural Gas\n($/1000 m³)']
original_prices = [150, 60, 500]
updated_prices = [135, 60, 430]

x = np.arange(len(energy_types))
width = 0.35

bars1 = ax5.bar(x - width/2, original_prices, width, label='Original', alpha=0.8, color='#ff7f0e')
bars2 = ax5.bar(x + width/2, updated_prices, width, label='Updated', alpha=0.8, color='#2ca02c')

ax5.set_ylabel('Price', fontsize=12)
ax5.set_title('Energy Prices Comparison (2024-2025)', fontsize=14, fontweight='bold')
ax5.set_xticks(x)
ax5.set_xticklabels(energy_types)
ax5.legend()
ax5.grid(True, alpha=0.3)

# 6. Fixed O&M Comparison (% of CAPEX)
ax6 = plt.subplot(4, 2, 6)
tech_om = ['PV', 'Wind', 'Battery', 'Electrolyzer', 'Fuel Cell', 'CHP']
original_om = [1.5, 1.5, 1.5, 1.5, 1.5, 1.5]  # All 1.5% in original
updated_om = [2.4, 2.5, 2.5, 4.0, 4.0, 1.5]

x = np.arange(len(tech_om))
width = 0.35

bars1 = ax6.bar(x - width/2, original_om, width, label='Original (Uniform)', alpha=0.8, color='#ff7f0e')
bars2 = ax6.bar(x + width/2, updated_om, width, label='Updated (Specific)', alpha=0.8, color='#2ca02c')

ax6.set_ylabel('Fixed O&M (% of CAPEX/year)', fontsize=12)
ax6.set_title('Fixed O&M Costs Comparison', fontsize=14, fontweight='bold')
ax6.set_xticks(x)
ax6.set_xticklabels(tech_om, rotation=45, ha='right')
ax6.legend()
ax6.grid(True, alpha=0.3)
ax6.set_ylim(0, 5)

# 7. Product Prices
ax7 = plt.subplot(4, 2, 7)
products = ['Hydrogen\n($/ton)', 'Ammonia\n($/ton)', 'SNG\n($/1000 m³)']
original_prod = [3000, 500, 400]
updated_prod = [4500, 425, 1300]
updated_prod_low = [3000, 400, 1100]
updated_prod_high = [6000, 450, 1600]

x = np.arange(len(products))
width = 0.35

bars1 = ax7.bar(x - width/2, original_prod, width, label='Original', alpha=0.8, color='#ff7f0e')
bars2 = ax7.bar(x + width/2, updated_prod, width, label='Updated', alpha=0.8, color='#2ca02c')

# Add error bars
yerr_low = [updated_prod[i] - updated_prod_low[i] for i in range(len(products))]
yerr_high = [updated_prod_high[i] - updated_prod[i] for i in range(len(products))]
ax7.errorbar(x + width/2, updated_prod, yerr=[yerr_low, yerr_high], 
             fmt='none', color='black', capsize=5, alpha=0.5)

ax7.set_ylabel('Price', fontsize=12)
ax7.set_title('Product Prices Comparison', fontsize=14, fontweight='bold')
ax7.set_xticks(x)
ax7.set_xticklabels(products)
ax7.legend()
ax7.grid(True, alpha=0.3)

# 8. Summary Impact Table
ax8 = plt.subplot(4, 1, 4)
ax8.axis('tight')
ax8.axis('off')

impact_data = [
    ['Parameter', 'Impact Level', 'Key Changes', 'Recommendation'],
    ['Discount Rate', 'CRITICAL', '8% → 4.5% (social) or 20% (commercial)', 'Use dual approach'],
    ['Wind CAPEX', 'HIGH', '1400 → 1850 $/kW (+32%)', 'Update immediately'],
    ['Battery CAPEX', 'HIGH', '228 → 375 $/kWh (+64%)', 'Update immediately'],
    ['Electrolyzer CAPEX', 'HIGH', '800 → 1400 $/kW (+75%)', 'Update immediately'],
    ['Carbon Pricing', 'HIGH', 'Non-zero values → Scenario-based only', 'Label as hypothetical'],
    ['Technology O&M', 'MEDIUM', 'Uniform 1.5% → Technology-specific', 'Apply specific rates'],
    ['Grid Emissions', 'MEDIUM', '0.442 ton CO2/MWh (2022 data)', 'Update with 2023 data'],
    ['Energy Prices', 'LOW', 'Minor adjustments needed', 'Verify with current data']
]

# Create table with colors
cell_colors = []
for i, row in enumerate(impact_data):
    if i == 0:  # Header
        cell_colors.append(['lightgray'] * 4)
    else:
        impact = row[1]
        if impact == 'CRITICAL':
            cell_colors.append(['white', '#ff4444', 'white', 'white'])
        elif impact == 'HIGH':
            cell_colors.append(['white', '#ff8844', 'white', 'white'])
        elif impact == 'MEDIUM':
            cell_colors.append(['white', '#ffcc44', 'white', 'white'])
        else:
            cell_colors.append(['white', '#44ff44', 'white', 'white'])

table = ax8.table(cellText=impact_data, cellLoc='left', loc='center',
                  cellColours=cell_colors, colWidths=[0.2, 0.15, 0.35, 0.3])
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2)

# Style the header row
for i in range(4):
    cell = table[(0, i)]
    cell.set_text_props(weight='bold')
    cell.set_facecolor('#cccccc')

ax8.set_title('Parameter Update Impact Summary', fontsize=16, fontweight='bold', pad=20)

# Add overall title and save
plt.suptitle('WFE Nexus Model Parameter Validation:\nComparison of Original vs Updated Configuration', 
             fontsize=18, fontweight='bold')
plt.tight_layout()
plt.savefig('/Users/kaanredstone/Library/CloudStorage/OneDrive-KocUniversitesi/WEN/wfe_nexus_corlu/results/parameter_comparison.png', 
            dpi=300, bbox_inches='tight')
plt.savefig('/Users/kaanredstone/Library/CloudStorage/OneDrive-KocUniversitesi/WEN/wfe_nexus_corlu/results/parameter_comparison.pdf', 
            bbox_inches='tight')
plt.show()

print("Parameter comparison visualization saved to results/parameter_comparison.png and .pdf")