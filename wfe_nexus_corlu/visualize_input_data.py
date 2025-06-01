"""
Visualize input data for the WFE Nexus Model
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def visualize_input_data():
    """Create visualizations of the input data"""
    
    # Set style
    plt.style.use('seaborn-v0_8-darkgrid')
    sns.set_palette("husl")
    
    # Create figure with subplots
    fig = plt.figure(figsize=(20, 16))
    
    # 1. Renewable availability profiles
    ax1 = plt.subplot(3, 2, 1)
    for scenario in ['low_renewable', 'average_renewable', 'high_renewable']:
        renewable_data = pd.read_csv(f'data/renewable_{scenario}.csv', index_col=0)
        hours = range(24)  # First day only
        
        pv_data = renewable_data['pv_availability'][:24]
        line_style = {'low_renewable': '--', 'average_renewable': '-', 'high_renewable': ':'}[scenario]
        label = scenario.replace('_', ' ').title()
        
        ax1.plot(hours, pv_data, label=f'PV - {label}', linewidth=2, linestyle=line_style)
    
    ax1.set_xlabel('Hour of Day')
    ax1.set_ylabel('Capacity Factor')
    ax1.set_title('Solar PV Availability Profiles (Winter Day)', fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. Wind availability profiles
    ax2 = plt.subplot(3, 2, 2)
    for scenario in ['low_renewable', 'average_renewable', 'high_renewable']:
        renewable_data = pd.read_csv(f'data/renewable_{scenario}.csv', index_col=0)
        hours = range(24)
        
        wind_data = renewable_data['wind_availability'][:24]
        line_style = {'low_renewable': '--', 'average_renewable': '-', 'high_renewable': ':'}[scenario]
        label = scenario.replace('_', ' ').title()
        
        ax2.plot(hours, wind_data, label=f'Wind - {label}', linewidth=2, linestyle=line_style)
    
    ax2.set_xlabel('Hour of Day')
    ax2.set_ylabel('Capacity Factor')
    ax2.set_title('Wind Availability Profiles (Winter Day)', fontsize=14, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. Electricity demand profile
    ax3 = plt.subplot(3, 2, 3)
    demand_data = pd.read_csv('data/demand_average_renewable.csv', index_col=0)
    
    # Plot seasonal patterns
    seasons = ['winter', 'spring', 'summer', 'autumn']
    colors = ['blue', 'green', 'red', 'orange']
    
    for i, season in enumerate(seasons):
        start_idx = i * 24
        end_idx = (i + 1) * 24
        hours = range(24)
        
        elec_demand = demand_data['electricity_demand'][start_idx:end_idx]
        ax3.plot(hours, elec_demand, label=season.title(), color=colors[i], linewidth=2)
    
    ax3.set_xlabel('Hour of Day')
    ax3.set_ylabel('Demand (MW)')
    ax3.set_title('Electricity Demand Profiles by Season', fontsize=14, fontweight='bold')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # 4. Heat demand profile
    ax4 = plt.subplot(3, 2, 4)
    for i, season in enumerate(seasons):
        start_idx = i * 24
        end_idx = (i + 1) * 24
        hours = range(24)
        
        heat_demand = demand_data['heat_demand'][start_idx:end_idx]
        ax4.plot(hours, heat_demand, label=season.title(), color=colors[i], linewidth=2)
    
    ax4.set_xlabel('Hour of Day')
    ax4.set_ylabel('Demand (MW)')
    ax4.set_title('Heat Demand Profiles by Season', fontsize=14, fontweight='bold')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    # 5. Electricity prices
    ax5 = plt.subplot(3, 2, 5)
    price_data = pd.read_csv('data/price_average_renewable.csv', index_col=0)
    hours = range(24)
    
    buy_price = price_data['electricity_buy_price'][:24]
    sell_price = price_data['electricity_sell_price'][:24]
    
    ax5.plot(hours, buy_price, label='Buy Price', color='red', linewidth=2)
    ax5.plot(hours, sell_price, label='Sell Price', color='green', linewidth=2)
    ax5.fill_between(hours, sell_price, buy_price, alpha=0.2, color='gray')
    
    ax5.set_xlabel('Hour of Day')
    ax5.set_ylabel('Price ($/MWh)')
    ax5.set_title('Electricity Prices (Time-of-Use)', fontsize=14, fontweight='bold')
    ax5.legend()
    ax5.grid(True, alpha=0.3)
    
    # 6. WWTP and technology parameters
    ax6 = plt.subplot(3, 2, 6)
    
    # Read WWTP data
    wwtp_data = pd.read_csv('data/wwtp_data.csv')
    tech_params = pd.read_csv('data/technology_parameters.csv')
    
    # Create bar chart of key WWTP outputs
    wwtp_outputs = {
        'Influent Flow': wwtp_data['influent_flow'].values[0] / 1000,  # Convert to thousand m³/day
        'Biogas Potential': wwtp_data['potential_biogas'].values[0] / 1000,  # thousand m³/day
        'CH4 Potential': wwtp_data['potential_ch4'].values[0] / 1000,  # thousand m³/day
        'Energy Potential': wwtp_data['potential_energy_mwh'].values[0]  # MWh/day
    }
    
    bars = ax6.bar(range(len(wwtp_outputs)), list(wwtp_outputs.values()))
    ax6.set_xticks(range(len(wwtp_outputs)))
    ax6.set_xticklabels(list(wwtp_outputs.keys()), rotation=45, ha='right')
    ax6.set_ylabel('Value')
    ax6.set_title('WWTP Resource Recovery Potential (per day)', fontsize=14, fontweight='bold')
    
    # Add value labels on bars
    for i, (bar, value) in enumerate(zip(bars, wwtp_outputs.values())):
        unit = ['k m³', 'k m³', 'k m³', 'MWh'][i]
        ax6.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                f'{value:.1f} {unit}', ha='center', va='bottom')
    
    plt.tight_layout()
    
    # Save figure
    os.makedirs('results/input_data', exist_ok=True)
    plt.savefig('results/input_data/input_data_summary.png', dpi=300, bbox_inches='tight')
    print("Input data visualization saved to: results/input_data/input_data_summary.png")
    
    # Create technology cost comparison
    fig2, ax = plt.subplots(figsize=(12, 8))
    
    # Sort technologies by CAPEX
    tech_params_sorted = tech_params.sort_values('capex', ascending=False)
    
    techs = tech_params_sorted['technology']
    capex = tech_params_sorted['capex']
    
    bars = ax.barh(range(len(techs)), capex)
    ax.set_yticks(range(len(techs)))
    ax.set_yticklabels(techs)
    ax.set_xlabel('CAPEX ($/kW or equivalent)', fontsize=12)
    ax.set_title('Technology Capital Costs', fontsize=14, fontweight='bold')
    
    # Color code by technology type
    colors = []
    for tech in techs:
        if tech in ['pv', 'wind']:
            colors.append('green')
        elif tech in ['battery', 'h2_storage', 'nh3_storage']:
            colors.append('blue')
        elif tech in ['electrolyzer', 'fuel_cell', 'haber_bosch']:
            colors.append('purple')
        else:
            colors.append('gray')
    
    for bar, color in zip(bars, colors):
        bar.set_color(color)
    
    # Add value labels
    for bar, value in zip(bars, capex):
        ax.text(bar.get_width() + 20, bar.get_y() + bar.get_height()/2, 
               f'${value:.0f}', ha='left', va='center')
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='green', label='Renewable Generation'),
        Patch(facecolor='blue', label='Storage'),
        Patch(facecolor='purple', label='Conversion'),
        Patch(facecolor='gray', label='Other')
    ]
    ax.legend(handles=legend_elements, loc='lower right')
    
    ax.grid(True, alpha=0.3, axis='x')
    plt.tight_layout()
    
    plt.savefig('results/input_data/technology_costs.png', dpi=300, bbox_inches='tight')
    print("Technology cost comparison saved to: results/input_data/technology_costs.png")
    
    plt.show()

if __name__ == "__main__":
    visualize_input_data()