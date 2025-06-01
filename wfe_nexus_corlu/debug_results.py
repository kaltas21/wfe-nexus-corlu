#!/usr/bin/env python3
"""
Debug script to check slack variable values
"""

from src.wfe_nexus_model import WFENexusModel

# Create and optimize model
model = WFENexusModel(data_dir='data', co2_policy='medium_tax', objective='minimize_cost')
model.optimize()

if model.model.status == 2:  # Optimal
    print("\n" + "="*60)
    print("CHECKING SLACK VARIABLES")
    print("="*60)
    
    # Check heat slack
    total_heat_slack = 0
    for (t, scenario) in model.v_heat_slack:
        if model.v_heat_slack[(t, scenario)].X > 0.01:
            print(f"Heat slack at {t}, {scenario}: {model.v_heat_slack[(t, scenario)].X:.2f} MW")
            total_heat_slack += model.v_heat_slack[(t, scenario)].X
    
    # Check H2 slack
    total_h2_slack = 0
    for (t, scenario) in model.v_h2_slack:
        if model.v_h2_slack[(t, scenario)].X > 0.01:
            print(f"H2 slack at {t}, {scenario}: {model.v_h2_slack[(t, scenario)].X:.2f} tons")
            total_h2_slack += model.v_h2_slack[(t, scenario)].X
    
    # Check N slack
    total_n_slack = 0
    for (t, scenario) in model.v_n_slack:
        if model.v_n_slack[(t, scenario)].X > 0.01:
            print(f"N slack at {t}, {scenario}: {model.v_n_slack[(t, scenario)].X:.2f} tons")
            total_n_slack += model.v_n_slack[(t, scenario)].X
    
    print(f"\nTotal heat slack: {total_heat_slack:.2f}")
    print(f"Total H2 slack: {total_h2_slack:.2f}")
    print(f"Total N slack: {total_n_slack:.2f}")
    
    # Check penalty cost
    penalty_rate = 10000
    days_per_season = 365 / 4
    avg_prob = 1/3
    
    penalty_cost = (total_heat_slack + total_h2_slack + total_n_slack) * penalty_rate * avg_prob * days_per_season
    print(f"\nEstimated annual penalty cost: ${penalty_cost:,.0f}")