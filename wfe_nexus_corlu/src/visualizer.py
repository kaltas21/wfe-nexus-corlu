"""
Visualization module for WFE Nexus Model Results
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches

class WFEVisualizer:
    def __init__(self, model):
        self.model = model
        self.results = self.extract_results()
        
        # Set style
        plt.style.use('seaborn-v0_8-darkgrid')
        sns.set_palette("husl")
    
    def extract_results(self):
        """Extract results from optimized model"""
        results = {
            'capacities': {},
            'operational': {},
            'costs': {},
            'emissions': {}
        }
        
        # Extract capacities
        for tech in self.model.all_techs:
            if self.model.v_build[tech].X > 0.5:
                results['capacities'][tech] = self.model.v_cap[tech].X
        
        # Extract operational data for average scenario
        scenario = 'average_renewable'
        time_data = []
        
        for t in self.model.time_periods[:24]:  # First day
            hour_data = {
                'hour': int(t.split('_h')[1]),
                'pv_gen': self.model.v_gen[('pv', t, scenario)].X if ('pv', t, scenario) in self.model.v_gen else 0,
                'wind_gen': self.model.v_gen[('wind', t, scenario)].X if ('wind', t, scenario) in self.model.v_gen else 0,
                'battery_discharge': self.model.v_discharge[('battery', t, scenario)].X if 'battery' in self.model.tech_storage else 0,
                'battery_charge': self.model.v_charge[('battery', t, scenario)].X if 'battery' in self.model.tech_storage else 0,
                'grid_buy': self.model.v_grid_buy[('electricity', t, scenario)].X,
                'grid_sell': self.model.v_grid_sell[('electricity', t, scenario)].X,
                'demand': self.model.demand_data[scenario].loc[t, 'electricity_demand']
            }
            
            if 'chp' in self.model.tech_generation:
                hour_data['chp_gen'] = self.model.v_gen[('chp', t, scenario)].X if ('chp', t, scenario) in self.model.v_gen else 0
            
            if 'electrolyzer' in self.model.tech_conversion:
                hour_data['h2_production'] = self.model.v_production[('electrolyzer', t, scenario)].X
            
            time_data.append(hour_data)
        
        results['operational'] = pd.DataFrame(time_data)
        
        return results
    
    def plot_capacity_portfolio(self):
        """Plot the installed capacity portfolio"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Capacity by technology type
        tech_types = {
            'Renewable': ['pv', 'wind'],
            'Storage': ['battery', 'h2_storage', 'nh3_storage'],
            'Conversion': ['electrolyzer', 'haber_bosch', 'anaerobic_digester'],
            'Recovery': ['n_recovery', 'p_recovery', 'water_reclamation']
        }
        
        type_capacities = {}
        for tech_type, techs in tech_types.items():
            total_cap = sum(self.results['capacities'].get(tech, 0) for tech in techs)
            if total_cap > 0:
                type_capacities[tech_type] = total_cap
        
        # Pie chart of capacity types
        if type_capacities:
            colors = plt.cm.Set3(np.linspace(0, 1, len(type_capacities)))
            ax1.pie(type_capacities.values(), labels=type_capacities.keys(), 
                   autopct='%1.1f%%', colors=colors, startangle=90)
            ax1.set_title('Investment Distribution by Technology Type', fontsize=14, fontweight='bold')
        
        # Bar chart of individual technologies
        if self.results['capacities']:
            techs = list(self.results['capacities'].keys())
            capacities = list(self.results['capacities'].values())
            
            bars = ax2.bar(range(len(techs)), capacities)
            ax2.set_xticks(range(len(techs)))
            ax2.set_xticklabels(techs, rotation=45, ha='right')
            ax2.set_ylabel('Capacity (MW/MWh/tons)', fontsize=12)
            ax2.set_title('Installed Capacities by Technology', fontsize=14, fontweight='bold')
            
            # Color bars by type
            colors = {'pv': 'gold', 'wind': 'skyblue', 'battery': 'green', 
                     'electrolyzer': 'purple', 'h2_storage': 'orange'}
            for bar, tech in zip(bars, techs):
                bar.set_color(colors.get(tech, 'gray'))
        
        plt.tight_layout()
        return fig
    
    def plot_daily_operation(self):
        """Plot daily operational profile"""
        fig, axes = plt.subplots(3, 1, figsize=(15, 12), sharex=True)
        
        hours = self.results['operational']['hour']
        
        # Plot 1: Generation dispatch
        ax1 = axes[0]
        ax1.plot(hours, self.results['operational']['pv_gen'], 
                label='PV', color='gold', linewidth=2)
        ax1.plot(hours, self.results['operational']['wind_gen'], 
                label='Wind', color='skyblue', linewidth=2)
        
        if 'chp_gen' in self.results['operational']:
            ax1.plot(hours, self.results['operational']['chp_gen'], 
                    label='CHP', color='brown', linewidth=2)
        
        ax1.plot(hours, self.results['operational']['demand'], 
                label='Demand', color='red', linestyle='--', linewidth=2)
        
        ax1.fill_between(hours, 0, self.results['operational']['pv_gen'], 
                        alpha=0.3, color='gold')
        ax1.fill_between(hours, self.results['operational']['pv_gen'], 
                        self.results['operational']['pv_gen'] + self.results['operational']['wind_gen'], 
                        alpha=0.3, color='skyblue')
        
        ax1.set_ylabel('Power (MW)', fontsize=12)
        ax1.set_title('Electricity Generation Dispatch', fontsize=14, fontweight='bold')
        ax1.legend(loc='upper right')
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Storage operation
        ax2 = axes[1]
        battery_net = self.results['operational']['battery_discharge'] - self.results['operational']['battery_charge']
        
        ax2.bar(hours, self.results['operational']['battery_charge'], 
               label='Battery Charging', color='red', alpha=0.7)
        ax2.bar(hours, self.results['operational']['battery_discharge'], 
               label='Battery Discharging', color='green', alpha=0.7)
        ax2.plot(hours, battery_net, label='Net Battery Flow', 
                color='black', linewidth=2, marker='o')
        
        ax2.axhline(y=0, color='black', linestyle='-', alpha=0.5)
        ax2.set_ylabel('Power (MW)', fontsize=12)
        ax2.set_title('Energy Storage Operation', fontsize=14, fontweight='bold')
        ax2.legend(loc='upper right')
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Grid interaction
        ax3 = axes[2]
        ax3.plot(hours, self.results['operational']['grid_buy'], 
                label='Grid Import', color='red', linewidth=2, marker='s')
        ax3.plot(hours, self.results['operational']['grid_sell'], 
                label='Grid Export', color='green', linewidth=2, marker='^')
        
        net_grid = self.results['operational']['grid_buy'] - self.results['operational']['grid_sell']
        ax3.fill_between(hours, 0, net_grid, where=(net_grid >= 0), 
                        interpolate=True, alpha=0.3, color='red', label='Net Import')
        ax3.fill_between(hours, 0, net_grid, where=(net_grid < 0), 
                        interpolate=True, alpha=0.3, color='green', label='Net Export')
        
        ax3.axhline(y=0, color='black', linestyle='-', alpha=0.5)
        ax3.set_xlabel('Hour of Day', fontsize=12)
        ax3.set_ylabel('Power (MW)', fontsize=12)
        ax3.set_title('Grid Interaction', fontsize=14, fontweight='bold')
        ax3.legend(loc='upper right')
        ax3.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def plot_wfe_nexus_flows(self):
        """Plot Sankey-style diagram of WFE nexus flows"""
        fig, ax = plt.subplots(figsize=(14, 10))
        
        # Define positions for nodes
        nodes = {
            # Sources (left)
            'WWTP': (1, 7),
            'Wind': (1, 5),
            'Solar': (1, 3),
            'Grid': (1, 1),
            
            # Conversion/Storage (middle)
            'Electricity Bus': (4, 4),
            'Battery': (4, 5.5),
            'Electrolyzer': (4, 2.5),
            'Anaerobic Digester': (4, 7),
            'CHP': (4, 6),
            'H2 Storage': (6, 2.5),
            'Haber-Bosch': (6, 1),
            'Water Recovery': (6, 7),
            'N Recovery': (6, 6),
            
            # Demands (right)
            'Elec Demand': (8, 4),
            'Heat Demand': (8, 5.5),
            'H2 Demand': (8, 2.5),
            'Water Demand': (8, 7),
            'Fertilizer Demand': (8, 1)
        }
        
        # Draw nodes
        for node, (x, y) in nodes.items():
            if node in ['Wind', 'Solar']:
                color = 'lightgreen'
            elif node == 'WWTP':
                color = 'lightblue'
            elif node == 'Grid':
                color = 'lightgray'
            elif 'Demand' in node:
                color = 'lightyellow'
            else:
                color = 'lightcoral'
            
            rect = Rectangle((x-0.3, y-0.2), 0.6, 0.4, 
                           facecolor=color, edgecolor='black', linewidth=2)
            ax.add_patch(rect)
            ax.text(x, y, node, ha='center', va='center', fontsize=9, fontweight='bold')
        
        # Draw flows (simplified representation)
        flows = [
            ('Wind', 'Electricity Bus', 'electricity'),
            ('Solar', 'Electricity Bus', 'electricity'),
            ('Grid', 'Electricity Bus', 'electricity'),
            ('Electricity Bus', 'Elec Demand', 'electricity'),
            ('Electricity Bus', 'Battery', 'electricity'),
            ('Battery', 'Electricity Bus', 'electricity'),
            ('Electricity Bus', 'Electrolyzer', 'electricity'),
            ('WWTP', 'Anaerobic Digester', 'sludge'),
            ('Anaerobic Digester', 'CHP', 'biogas'),
            ('CHP', 'Electricity Bus', 'electricity'),
            ('CHP', 'Heat Demand', 'heat'),
            ('Electrolyzer', 'H2 Storage', 'hydrogen'),
            ('H2 Storage', 'H2 Demand', 'hydrogen'),
            ('H2 Storage', 'Haber-Bosch', 'hydrogen'),
            ('Haber-Bosch', 'Fertilizer Demand', 'ammonia'),
            ('WWTP', 'Water Recovery', 'water'),
            ('Water Recovery', 'Water Demand', 'water'),
            ('WWTP', 'N Recovery', 'nutrients'),
            ('N Recovery', 'Fertilizer Demand', 'nitrogen')
        ]
        
        # Color mapping for flow types
        flow_colors = {
            'electricity': 'gold',
            'hydrogen': 'lightblue',
            'biogas': 'brown',
            'heat': 'red',
            'water': 'blue',
            'nutrients': 'green',
            'ammonia': 'purple',
            'nitrogen': 'darkgreen',
            'sludge': 'gray'
        }
        
        for source, target, flow_type in flows:
            if source in nodes and target in nodes:
                x1, y1 = nodes[source]
                x2, y2 = nodes[target]
                
                # Draw arrow
                ax.annotate('', xy=(x2-0.3, y2), xytext=(x1+0.3, y1),
                           arrowprops=dict(arrowstyle='->', lw=2, 
                                         color=flow_colors.get(flow_type, 'black'),
                                         alpha=0.7))
        
        # Add legend
        legend_elements = [mpatches.Patch(color=color, label=flow_type.capitalize()) 
                          for flow_type, color in flow_colors.items()]
        ax.legend(handles=legend_elements[:6], loc='upper left', bbox_to_anchor=(0, 1))
        
        ax.set_xlim(0, 9)
        ax.set_ylim(0, 8)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title('WFE Nexus Integration - System Overview', 
                    fontsize=16, fontweight='bold', pad=20)
        
        return fig
    
    def plot_scenario_comparison(self):
        """Compare results across different scenarios"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Placeholder for scenario comparison
        # This would require running the model with different CO2 policies
        
        scenarios = ['No Tax', 'Low Tax\n($30/ton)', 'Medium Tax\n($60/ton)', 'High Tax\n($100/ton)']
        
        # Example data (would be actual results from multiple runs)
        renewable_capacity = [50, 65, 85, 120]
        total_cost = [15, 16.5, 18, 22]
        co2_emissions = [50000, 35000, 20000, 10000]
        h2_production = [100, 250, 450, 800]
        
        # Plot 1: Renewable capacity
        ax1 = axes[0, 0]
        bars1 = ax1.bar(scenarios, renewable_capacity, color='green', alpha=0.7)
        ax1.set_ylabel('Renewable Capacity (MW)', fontsize=12)
        ax1.set_title('Renewable Investment vs CO2 Policy', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3, axis='y')
        
        # Plot 2: Total cost
        ax2 = axes[0, 1]
        bars2 = ax2.bar(scenarios, total_cost, color='blue', alpha=0.7)
        ax2.set_ylabel('Total Annual Cost (Million $)', fontsize=12)
        ax2.set_title('System Cost vs CO2 Policy', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='y')
        
        # Plot 3: CO2 emissions
        ax3 = axes[1, 0]
        bars3 = ax3.bar(scenarios, co2_emissions, color='red', alpha=0.7)
        ax3.set_ylabel('Annual CO2 Emissions (tons)', fontsize=12)
        ax3.set_title('Emissions vs CO2 Policy', fontsize=14, fontweight='bold')
        ax3.grid(True, alpha=0.3, axis='y')
        
        # Plot 4: H2 production
        ax4 = axes[1, 1]
        bars4 = ax4.bar(scenarios, h2_production, color='purple', alpha=0.7)
        ax4.set_ylabel('H2 Production (tons/year)', fontsize=12)
        ax4.set_title('Hydrogen Economy vs CO2 Policy', fontsize=14, fontweight='bold')
        ax4.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        return fig
    
    def create_all_plots(self, save_dir='../results/plots'):
        """Create and save all visualization plots"""
        import os
        os.makedirs(save_dir, exist_ok=True)
        
        # Create plots
        fig1 = self.plot_capacity_portfolio()
        fig1.savefig(os.path.join(save_dir, 'capacity_portfolio.png'), dpi=300, bbox_inches='tight')
        
        fig2 = self.plot_daily_operation()
        fig2.savefig(os.path.join(save_dir, 'daily_operation.png'), dpi=300, bbox_inches='tight')
        
        fig3 = self.plot_wfe_nexus_flows()
        fig3.savefig(os.path.join(save_dir, 'wfe_nexus_flows.png'), dpi=300, bbox_inches='tight')
        
        fig4 = self.plot_scenario_comparison()
        fig4.savefig(os.path.join(save_dir, 'scenario_comparison.png'), dpi=300, bbox_inches='tight')
        
        print(f"All plots saved to: {save_dir}")
        
        # Close all figures to free memory
        plt.close('all')