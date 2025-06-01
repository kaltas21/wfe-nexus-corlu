#!/usr/bin/env python3
"""
Test script to debug model infeasibility with a simplified version
"""

import gurobipy as gp
from gurobipy import GRB
import pandas as pd
import numpy as np
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.model_config import *

def test_simple_model():
    """Create a simplified model to test feasibility"""
    
    # Create model
    model = gp.Model("Simple_WFE_Test")
    
    # Simple variables - just PV and battery
    v_cap_pv = model.addVar(lb=0, ub=100, name="cap_pv")
    v_cap_battery = model.addVar(lb=0, ub=100, name="cap_battery")
    v_build_pv = model.addVar(vtype=GRB.BINARY, name="build_pv")
    v_build_battery = model.addVar(vtype=GRB.BINARY, name="build_battery")
    
    # Link capacity to build
    model.addConstr(v_cap_pv <= v_build_pv * 100, "link_pv")
    model.addConstr(v_cap_battery <= v_build_battery * 100, "link_battery")
    
    # Simple operational variables for one time period
    v_gen_pv = model.addVar(lb=0, ub=100, name="gen_pv")
    v_charge = model.addVar(lb=0, ub=100, name="charge")
    v_discharge = model.addVar(lb=0, ub=100, name="discharge")
    v_soc = model.addVar(lb=0, ub=100, name="soc")
    v_grid_buy = model.addVar(lb=0, ub=100, name="grid_buy")
    v_grid_sell = model.addVar(lb=0, ub=100, name="grid_sell")
    
    # Simple constraints
    # PV generation limited by capacity and availability (50%)
    model.addConstr(v_gen_pv == v_cap_pv * 0.5, "pv_gen")
    
    # Battery constraints
    model.addConstr(v_charge <= v_cap_battery * 0.5, "charge_limit")
    model.addConstr(v_discharge <= v_cap_battery * 0.5, "discharge_limit")
    model.addConstr(v_soc == v_cap_battery * 0.5 + v_charge - v_discharge, "soc_balance")
    model.addConstr(v_soc >= v_cap_battery * 0.1, "soc_min")
    model.addConstr(v_soc <= v_cap_battery * 0.9, "soc_max")
    
    # Energy balance
    demand = 50  # MW
    model.addConstr(
        v_gen_pv + v_discharge + v_grid_buy == demand + v_charge + v_grid_sell,
        "energy_balance"
    )
    
    # Simple objective - minimize cost
    capex_pv = 900 * v_cap_pv * 0.1  # Annualized
    capex_battery = 228 * v_cap_battery * 0.1
    opex = v_grid_buy * 100 - v_grid_sell * 50
    
    model.setObjective(capex_pv + capex_battery + opex, GRB.MINIMIZE)
    
    # Optimize
    print("Optimizing simple model...")
    model.optimize()
    
    if model.status == GRB.OPTIMAL:
        print("\nSimple model is feasible!")
        print(f"Objective: {model.objVal:.2f}")
        print(f"PV Capacity: {v_cap_pv.X:.2f} MW")
        print(f"Battery Capacity: {v_cap_battery.X:.2f} MWh")
        print(f"Grid Buy: {v_grid_buy.X:.2f} MW")
        print(f"Grid Sell: {v_grid_sell.X:.2f} MW")
    else:
        print(f"\nSimple model failed with status: {model.status}")
        if model.status == GRB.INFEASIBLE:
            model.computeIIS()
            print("\nIIS constraints:")
            for c in model.getConstrs():
                if c.IISConstr:
                    print(f"  {c.ConstrName}")

if __name__ == "__main__":
    test_simple_model()