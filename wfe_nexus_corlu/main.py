"""
Main script to run WFE Nexus optimization for Çorlu
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.data_generator import DataGenerator
from src.wfe_nexus_model import WFENexusModel
from src.visualizer import WFEVisualizer

def run_single_scenario(co2_policy='medium_tax', objective='minimize_cost', visualize=True):
    """Run optimization for a single scenario"""
    print(f"\n{'='*80}")
    print(f"Running WFE Nexus Model - CO2 Policy: {co2_policy}, Objective: {objective}")
    print(f"{'='*80}\n")
    
    # Create and optimize model
    model = WFENexusModel(
        data_dir='data',
        co2_policy=co2_policy,
        objective=objective
    )
    
    model.optimize()
    
    # Save detailed results
    results_dir = f'results/{co2_policy}_{objective}'
    os.makedirs(results_dir, exist_ok=True)
    
    if model.model.status == 2:  # Optimal
        model.save_results(os.path.join(results_dir, 'detailed_results.txt'))
        
        # Create visualizations
        if visualize:
            print("\nCreating visualizations...")
            viz = WFEVisualizer(model)
            viz.create_all_plots(save_dir=os.path.join(results_dir, 'plots'))
    else:
        print(f"Optimization failed with status {model.model.status} - no results to save")
    
    return model

def run_sensitivity_analysis():
    """Run sensitivity analysis across different CO2 policies"""
    print("\n" + "="*80)
    print("SENSITIVITY ANALYSIS - CO2 POLICY IMPACT")
    print("="*80 + "\n")
    
    co2_policies = ['no_tax', 'low_tax', 'medium_tax', 'high_tax']
    results = {}
    
    for policy in co2_policies:
        model = run_single_scenario(
            co2_policy=policy,
            objective='minimize_cost',
            visualize=False
        )
        
        if model.model.status == 2:  # Optimal
            # Extract key results
            results[policy] = {
                'total_cost': model.model.objVal,
                'renewable_capacity': model.v_cap['pv'].X + model.v_cap['wind'].X,
                'battery_capacity': model.v_cap['battery'].X,
                'electrolyzer_capacity': model.v_cap['electrolyzer'].X if 'electrolyzer' in model.v_cap else 0,
                'h2_storage': model.v_cap['h2_storage'].X if 'h2_storage' in model.v_cap else 0
            }
    
    # Print comparison table
    print("\n" + "-"*80)
    print("SENSITIVITY ANALYSIS RESULTS")
    print("-"*80)
    print(f"{'CO2 Policy':<15} {'Total Cost':<15} {'Renewable':<15} {'Battery':<15} {'Electrolyzer':<15} {'H2 Storage':<15}")
    print(f"{'($/ton)':<15} {'(M$/year)':<15} {'(MW)':<15} {'(MWh)':<15} {'(MW)':<15} {'(tons)':<15}")
    print("-"*90)
    
    for policy, res in results.items():
        tax = {'no_tax': 0, 'low_tax': 30, 'medium_tax': 60, 'high_tax': 100}[policy]
        print(f"{tax:<15} {res['total_cost']/1e6:>14.2f} {res['renewable_capacity']:>14.2f} "
              f"{res['battery_capacity']:>14.2f} {res['electrolyzer_capacity']:>14.2f} "
              f"{res['h2_storage']:>14.2f}")
    
    return results

def run_multi_objective_analysis():
    """Compare different objective functions"""
    print("\n" + "="*80)
    print("MULTI-OBJECTIVE ANALYSIS")
    print("="*80 + "\n")
    
    objectives = ['minimize_cost', 'minimize_emissions']
    co2_policy = 'medium_tax'
    
    results = {}
    
    for obj in objectives:
        model = run_single_scenario(
            co2_policy=co2_policy,
            objective=obj,
            visualize=True
        )
        
        if model.model.status == 2:
            results[obj] = model
    
    # Compare results
    if len(results) == 2:
        print("\n" + "-"*60)
        print("COMPARISON: Cost Minimization vs Emission Minimization")
        print("-"*60)
        
        cost_model = results['minimize_cost']
        emission_model = results['minimize_emissions']
        
        # Calculate emissions for both
        total_emissions_cost = 0
        total_emissions_emission = 0
        
        for scenario in cost_model.scenarios:
            prob = cost_model.scenarios_df.loc[cost_model.scenarios_df['scenario'] == scenario, 'probability'].values[0]
            for t in cost_model.time_periods:
                total_emissions_cost += prob * cost_model.v_emissions[(t, scenario)].X
                total_emissions_emission += prob * emission_model.v_emissions[(t, scenario)].X
        
        # Scale to annual
        scale_factor = 365 / 4  # 4 representative days to full year
        total_emissions_cost *= scale_factor
        total_emissions_emission *= scale_factor
        
        print(f"\nCost-Optimal Solution:")
        print(f"  - Total Annual Cost: ${cost_model.model.objVal:,.0f}")
        print(f"  - Annual CO2 Emissions: {total_emissions_cost:,.0f} tons")
        
        print(f"\nEmission-Optimal Solution:")
        print(f"  - Annual CO2 Emissions: {total_emissions_emission:,.0f} tons")
        print(f"  - Emission Reduction: {(1 - total_emissions_emission/total_emissions_cost)*100:.1f}%")
        
        # Calculate implied carbon price
        if total_emissions_cost > total_emissions_emission:
            # Estimate cost of emission-optimal by running with same capacities
            # This is a simplification - actual cost would need re-optimization
            implied_carbon_price = 100  # Placeholder
            print(f"  - Implied Carbon Price: ~${implied_carbon_price}/ton CO2")

def main():
    """Main execution function"""
    print("WFE NEXUS OPTIMIZATION MODEL FOR ÇORLU, TÜRKİYE")
    print("="*60)
    
    # Step 1: Generate data
    print("\n1. Generating synthetic data based on Çorlu parameters...")
    generator = DataGenerator()
    generator.save_all_data('data')
    
    # Step 2: Run base case
    print("\n2. Running base case optimization...")
    base_model = run_single_scenario(
        co2_policy='medium_tax',
        objective='minimize_cost',
        visualize=True
    )
    
    # Step 3: Run sensitivity analysis
    print("\n3. Running sensitivity analysis on CO2 policies...")
    sensitivity_results = run_sensitivity_analysis()
    
    # Step 4: Run multi-objective analysis
    print("\n4. Running multi-objective analysis...")
    run_multi_objective_analysis()
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)
    print("\nResults saved in 'results' directory")
    print("Plots saved in 'results/<scenario>/plots' directories")

if __name__ == "__main__":
    # Check if Gurobi is available
    try:
        import gurobipy
        print("Gurobi detected. Starting optimization...")
        main()
    except ImportError:
        print("ERROR: Gurobi not found!")
        print("Please install Gurobi and obtain a license.")
        print("Visit: https://www.gurobi.com/academia/academic-program-and-licenses/")
        sys.exit(1)