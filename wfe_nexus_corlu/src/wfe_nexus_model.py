"""
Two-Stage Stochastic WFE Nexus Model using Gurobi
For Çorlu, Türkiye case study
"""

import gurobipy as gp
from gurobipy import GRB
import pandas as pd
import numpy as np
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.model_config import *

class WFENexusModel:
    def __init__(self, data_dir='../data', co2_policy='no_tax', objective='minimize_cost'):
        self.data_dir = data_dir
        self.co2_policy = co2_policy
        self.co2_tax = CO2_TAX_SCENARIOS[co2_policy]
        self.objective_type = objective
        
        # Load data
        self.load_data()
        
        # Create model
        self.model = gp.Model("WFE_Nexus_Corlu")
        
        # Define sets
        self.define_sets()
        
        # Create variables
        self.create_variables()
        
        # Add constraints
        self.add_constraints()
        
        # Set objective
        self.set_objective()
    
    def load_data(self):
        """Load all data from CSV files"""
        # Load technology parameters
        self.tech_params = pd.read_csv(os.path.join(self.data_dir, 'technology_parameters.csv'))
        self.tech_params.set_index('technology', inplace=True)
        
        # Load WWTP data
        self.wwtp_data = pd.read_csv(os.path.join(self.data_dir, 'wwtp_data.csv')).iloc[0]
        
        # Load scenarios
        self.scenarios_df = pd.read_csv(os.path.join(self.data_dir, 'scenarios.csv'))
        
        # Load time-series data for each scenario
        self.renewable_data = {}
        self.demand_data = {}
        self.price_data = {}
        
        for scenario in SCENARIOS:
            self.renewable_data[scenario] = pd.read_csv(
                os.path.join(self.data_dir, f'renewable_{scenario}.csv'), 
                index_col=0
            )
            self.demand_data[scenario] = pd.read_csv(
                os.path.join(self.data_dir, f'demand_{scenario}.csv'), 
                index_col=0
            )
            self.price_data[scenario] = pd.read_csv(
                os.path.join(self.data_dir, f'price_{scenario}.csv'), 
                index_col=0
            )
    
    def define_sets(self):
        """Define model sets"""
        # Technologies
        self.tech_generation = ['pv', 'wind', 'chp', 'fuel_cell']
        self.tech_storage = ['battery', 'h2_storage', 'nh3_storage']
        self.tech_conversion = ['electrolyzer', 'haber_bosch', 'p2g_methanation', 
                               'anaerobic_digester', 'biomethane_upgrading']
        self.tech_recovery = ['n_recovery', 'p_recovery', 'water_reclamation']
        self.tech_capture = ['carbon_capture']
        
        self.all_techs = (self.tech_generation + self.tech_storage + 
                         self.tech_conversion + self.tech_recovery + self.tech_capture)
        
        # Time periods (representative hours)
        self.time_periods = list(self.renewable_data[SCENARIOS[0]].index)
        
        # Scenarios
        self.scenarios = SCENARIOS
        
        # Resources
        self.resources = ['electricity', 'heat', 'water', 'hydrogen', 'ammonia', 
                         'biogas', 'biomethane', 'co2', 'nitrogen_fertilizer']
    
    def calculate_crf(self, tech):
        """Calculate Capital Recovery Factor"""
        r = DISCOUNT_RATE
        n = TECHNOLOGY_LIFESPANS.get(tech, 20)
        return (r * (1 + r)**n) / ((1 + r)**n - 1)
    
    def create_variables(self):
        """Create model variables"""
        # First-stage variables (investment decisions)
        self.v_cap = {}
        self.v_build = {}
        
        for tech in self.all_techs:
            # Capacity variables
            min_cap = CAPACITY_LIMITS.get(tech, {}).get('min', 0)
            max_cap = CAPACITY_LIMITS.get(tech, {}).get('max', 1000)
            
            self.v_cap[tech] = self.model.addVar(
                lb=0, ub=max_cap, name=f"cap_{tech}"
            )
            
            # Binary build decision
            self.v_build[tech] = self.model.addVar(
                vtype=GRB.BINARY, name=f"build_{tech}"
            )
        
        # Second-stage variables (operational decisions)
        self.v_gen = {}  # Generation
        self.v_charge = {}  # Storage charging
        self.v_discharge = {}  # Storage discharging
        self.v_soc = {}  # State of charge
        self.v_flow = {}  # Resource flows
        self.v_grid_buy = {}  # Grid purchases
        self.v_grid_sell = {}  # Grid sales
        self.v_production = {}  # Production from conversion units
        self.v_consumption = {}  # Consumption by conversion units
        self.v_emissions = {}  # CO2 emissions
        self.v_is_on = {}  # Unit commitment
        self.v_startup = {}  # Startup indicators
        self.v_shutdown = {}  # Shutdown indicators
        self.v_heat_slack = {}  # Heat slack variables
        self.v_h2_slack = {}  # H2 slack variables
        self.v_n_slack = {}  # N slack variables
        self.v_chp_gas = {}  # CHP gas consumption
        
        for scenario in self.scenarios:
            # Generation variables
            for tech in self.tech_generation:
                for t in self.time_periods:
                    self.v_gen[(tech, t, scenario)] = self.model.addVar(
                        lb=0, name=f"gen_{tech}_{t}_{scenario}"
                    )
                    
                    # Unit commitment for dispatchable units
                    if tech in ['chp', 'fuel_cell']:
                        self.v_is_on[(tech, t, scenario)] = self.model.addVar(
                            vtype=GRB.BINARY, name=f"on_{tech}_{t}_{scenario}"
                        )
                        if t != self.time_periods[0]:
                            self.v_startup[(tech, t, scenario)] = self.model.addVar(
                                vtype=GRB.BINARY, name=f"startup_{tech}_{t}_{scenario}"
                            )
                            self.v_shutdown[(tech, t, scenario)] = self.model.addVar(
                                vtype=GRB.BINARY, name=f"shutdown_{tech}_{t}_{scenario}"
                            )
            
            # Storage variables
            for storage in self.tech_storage:
                for t in self.time_periods:
                    self.v_charge[(storage, t, scenario)] = self.model.addVar(
                        lb=0, name=f"charge_{storage}_{t}_{scenario}"
                    )
                    self.v_discharge[(storage, t, scenario)] = self.model.addVar(
                        lb=0, name=f"discharge_{storage}_{t}_{scenario}"
                    )
                    self.v_soc[(storage, t, scenario)] = self.model.addVar(
                        lb=0, name=f"soc_{storage}_{t}_{scenario}"
                    )
            
            # Conversion unit variables
            for conv in self.tech_conversion:
                for t in self.time_periods:
                    self.v_production[(conv, t, scenario)] = self.model.addVar(
                        lb=0, name=f"prod_{conv}_{t}_{scenario}"
                    )
                    self.v_consumption[(conv, t, scenario)] = self.model.addVar(
                        lb=0, name=f"cons_{conv}_{t}_{scenario}"
                    )
            
            # Recovery unit variables
            for rec in self.tech_recovery:
                for t in self.time_periods:
                    self.v_production[(rec, t, scenario)] = self.model.addVar(
                        lb=0, name=f"prod_{rec}_{t}_{scenario}"
                    )
            
            # Grid interaction variables
            for t in self.time_periods:
                self.v_grid_buy[('electricity', t, scenario)] = self.model.addVar(
                    lb=0, name=f"grid_buy_elec_{t}_{scenario}"
                )
                self.v_grid_sell[('electricity', t, scenario)] = self.model.addVar(
                    lb=0, name=f"grid_sell_elec_{t}_{scenario}"
                )
                self.v_grid_buy[('gas', t, scenario)] = self.model.addVar(
                    lb=0, name=f"grid_buy_gas_{t}_{scenario}"
                )
                self.v_grid_sell[('gas', t, scenario)] = self.model.addVar(
                    lb=0, name=f"grid_sell_gas_{t}_{scenario}"
                )
            
            # Emissions variables
            for t in self.time_periods:
                self.v_emissions[(t, scenario)] = self.model.addVar(
                    lb=0, name=f"emissions_{t}_{scenario}"
                )
    
    def add_constraints(self):
        """Add all model constraints"""
        # First-stage constraints
        self.add_investment_constraints()
        
        # Second-stage constraints for each scenario
        for scenario in self.scenarios:
            self.add_operational_constraints(scenario)
    
    def add_investment_constraints(self):
        """Add first-stage investment constraints"""
        # Link capacity to build decision
        for tech in self.all_techs:
            min_cap = CAPACITY_LIMITS.get(tech, {}).get('min', 0)
            
            # Capacity can only be positive if technology is built
            self.model.addConstr(
                self.v_cap[tech] <= self.v_build[tech] * CAPACITY_LIMITS.get(tech, {}).get('max', 1000),
                name=f"cap_build_link_{tech}"
            )
            
            # Minimum capacity if built
            if min_cap > 0:
                self.model.addConstr(
                    self.v_cap[tech] >= self.v_build[tech] * min_cap,
                    name=f"min_cap_{tech}"
                )
    
    def add_operational_constraints(self, scenario):
        """Add second-stage operational constraints for a scenario"""
        # Renewable generation constraints
        for t in self.time_periods:
            # PV generation
            if 'pv' in self.tech_generation:
                pv_avail = self.renewable_data[scenario].loc[t, 'pv_availability']
                self.model.addConstr(
                    self.v_gen[('pv', t, scenario)] == self.v_cap['pv'] * pv_avail,
                    name=f"pv_gen_{t}_{scenario}"
                )
            
            # Wind generation
            if 'wind' in self.tech_generation:
                wind_avail = self.renewable_data[scenario].loc[t, 'wind_availability']
                self.model.addConstr(
                    self.v_gen[('wind', t, scenario)] == self.v_cap['wind'] * wind_avail,
                    name=f"wind_gen_{t}_{scenario}"
                )
        
        # Dispatchable generation constraints
        for tech in ['chp', 'fuel_cell']:
            for idx, t in enumerate(self.time_periods):
                # Generation limits
                self.model.addConstr(
                    self.v_gen[(tech, t, scenario)] <= self.v_cap[tech] * self.v_is_on[(tech, t, scenario)],
                    name=f"gen_max_{tech}_{t}_{scenario}"
                )
                
                # Minimum stable generation
                min_load = 0.3  # 30% minimum load
                self.model.addConstr(
                    self.v_gen[(tech, t, scenario)] >= min_load * self.v_cap[tech] * self.v_is_on[(tech, t, scenario)],
                    name=f"gen_min_{tech}_{t}_{scenario}"
                )
                
                # Ramp constraints
                if idx > 0:
                    t_prev = self.time_periods[idx-1]
                    ramp_up = RAMP_RATES[tech]['up']
                    ramp_down = RAMP_RATES[tech]['down']
                    
                    self.model.addConstr(
                        self.v_gen[(tech, t, scenario)] - self.v_gen[(tech, t_prev, scenario)] <= ramp_up * self.v_cap[tech],
                        name=f"ramp_up_{tech}_{t}_{scenario}"
                    )
                    self.model.addConstr(
                        self.v_gen[(tech, t_prev, scenario)] - self.v_gen[(tech, t, scenario)] <= ramp_down * self.v_cap[tech],
                        name=f"ramp_down_{tech}_{t}_{scenario}"
                    )
                    
                    # Unit commitment logic
                    self.model.addConstr(
                        self.v_startup[(tech, t, scenario)] >= self.v_is_on[(tech, t, scenario)] - self.v_is_on[(tech, t_prev, scenario)],
                        name=f"startup_{tech}_{t}_{scenario}"
                    )
                    self.model.addConstr(
                        self.v_shutdown[(tech, t, scenario)] >= self.v_is_on[(tech, t_prev, scenario)] - self.v_is_on[(tech, t, scenario)],
                        name=f"shutdown_{tech}_{t}_{scenario}"
                    )
        
        # Storage constraints
        for storage in self.tech_storage:
            params = STORAGE_PARAMS[storage]
            
            for idx, t in enumerate(self.time_periods):
                # Charge/discharge limits
                self.model.addConstr(
                    self.v_charge[(storage, t, scenario)] <= params['max_charge_rate'] * self.v_cap[storage],
                    name=f"charge_limit_{storage}_{t}_{scenario}"
                )
                self.model.addConstr(
                    self.v_discharge[(storage, t, scenario)] <= params['max_discharge_rate'] * self.v_cap[storage],
                    name=f"discharge_limit_{storage}_{t}_{scenario}"
                )
                
                # State of charge limits
                if storage == 'battery':
                    min_soc = params.get('min_soc', 0.1)
                    max_soc = params.get('max_soc', 0.9)
                else:
                    min_soc = params.get('min_level', 0.05)
                    max_soc = params.get('max_level', 0.95)
                
                self.model.addConstr(
                    self.v_soc[(storage, t, scenario)] >= min_soc * self.v_cap[storage],
                    name=f"soc_min_{storage}_{t}_{scenario}"
                )
                self.model.addConstr(
                    self.v_soc[(storage, t, scenario)] <= max_soc * self.v_cap[storage],
                    name=f"soc_max_{storage}_{t}_{scenario}"
                )
                
                # State of charge dynamics
                if storage == 'battery':
                    charge_eff = TECHNOLOGY_EFFICIENCIES.get('battery_charge', 0.95)
                    discharge_eff = TECHNOLOGY_EFFICIENCIES.get('battery_discharge', 0.95)
                else:
                    charge_eff = 0.95  # Default for other storage
                    discharge_eff = 0.95
                
                if idx == 0:
                    # Initial state (assume 50% charged)
                    self.model.addConstr(
                        self.v_soc[(storage, t, scenario)] == 0.5 * self.v_cap[storage] +
                        self.v_charge[(storage, t, scenario)] * charge_eff -
                        self.v_discharge[(storage, t, scenario)] / discharge_eff,
                        name=f"soc_init_{storage}_{t}_{scenario}"
                    )
                else:
                    t_prev = self.time_periods[idx-1]
                    self.model.addConstr(
                        self.v_soc[(storage, t, scenario)] == 
                        self.v_soc[(storage, t_prev, scenario)] * (1 - params['self_discharge']) +
                        self.v_charge[(storage, t, scenario)] * charge_eff -
                        self.v_discharge[(storage, t, scenario)] / discharge_eff,
                        name=f"soc_balance_{storage}_{t}_{scenario}"
                    )
        
        # Electrolyzer constraints
        if 'electrolyzer' in self.tech_conversion:
            for t in self.time_periods:
                # H2 production based on electricity consumption
                self.model.addConstr(
                    self.v_production[('electrolyzer', t, scenario)] == 
                    self.v_consumption[('electrolyzer', t, scenario)] / ENERGY_CONVERSIONS['electricity_to_h2'],
                    name=f"electrolyzer_h2_{t}_{scenario}"
                )
                
                # Capacity limit
                self.model.addConstr(
                    self.v_consumption[('electrolyzer', t, scenario)] <= self.v_cap['electrolyzer'],
                    name=f"electrolyzer_cap_{t}_{scenario}"
                )
        
        # Haber-Bosch constraints
        if 'haber_bosch' in self.tech_conversion:
            for t in self.time_periods:
                # NH3 production stoichiometry
                self.model.addConstr(
                    self.v_production[('haber_bosch', t, scenario)] * ENERGY_CONVERSIONS['h2_to_nh3'] == 
                    self.v_consumption[('haber_bosch', t, scenario)],
                    name=f"hb_stoich_{t}_{scenario}"
                )
                
                # Capacity limit (tons NH3/day -> tons/hour)
                self.model.addConstr(
                    self.v_production[('haber_bosch', t, scenario)] <= self.v_cap['haber_bosch'] / 24,
                    name=f"hb_cap_{t}_{scenario}"
                )
        
        # WWTP and biogas constraints
        if 'anaerobic_digester' in self.tech_conversion:
            # Biogas production from WWTP (constant)
            biogas_hourly = self.wwtp_data['potential_biogas'] / 24  # m³/hour
            ch4_hourly = self.wwtp_data['potential_ch4'] / 24  # m³ CH4/hour
            
            for t in self.time_periods:
                self.model.addConstr(
                    self.v_production[('anaerobic_digester', t, scenario)] == biogas_hourly,
                    name=f"biogas_prod_{t}_{scenario}"
                )
        
        # CHP constraints (can use biogas or natural gas)
        # CHP gas consumption constraint
        if 'chp' in self.tech_generation:
            ch4_energy = ENERGY_CONVERSIONS['ch4_lhv'] / 1000  # MWh/m³
            
            for t in self.time_periods:
                # Add variable for CHP gas consumption
                self.v_chp_gas[(t, scenario)] = self.model.addVar(
                    lb=0, name=f"chp_gas_{t}_{scenario}"
                )
                
                # CHP electricity generation = gas consumption * efficiency
                self.model.addConstr(
                    self.v_gen[('chp', t, scenario)] == 
                    self.v_chp_gas[(t, scenario)] * ch4_energy * TECHNOLOGY_EFFICIENCIES['chp_electric'],
                    name=f"chp_gas_conv_{t}_{scenario}"
                )
                
                # Gas can come from biogas or natural gas
                biogas_available = 0
                if 'anaerobic_digester' in self.tech_conversion:
                    biogas_available = self.v_production[('anaerobic_digester', t, scenario)] * WWTP_PARAMS['ch4_content']
                
                # Natural gas consumption = total gas - biogas
                self.model.addConstr(
                    self.v_grid_buy[('gas', t, scenario)] >= self.v_chp_gas[(t, scenario)] - biogas_available,
                    name=f"chp_natgas_{t}_{scenario}"
                )
        
        # Energy balance constraints
        for t in self.time_periods:
            # Electricity balance
            supply_elec = (
                sum(self.v_gen[(tech, t, scenario)] for tech in self.tech_generation if (tech, t, scenario) in self.v_gen) +
                self.v_discharge[('battery', t, scenario)] +
                self.v_grid_buy[('electricity', t, scenario)]
            )
            
            demand_elec = (
                self.demand_data[scenario].loc[t, 'electricity_demand'] +
                self.v_charge[('battery', t, scenario)] +
                self.v_consumption[('electrolyzer', t, scenario)] +
                self.v_grid_sell[('electricity', t, scenario)] +
                self.wwtp_data['energy_consumption'] * self.wwtp_data['influent_flow'] / 24 / 1000  # MWh
            )
            
            self.model.addConstr(
                supply_elec == demand_elec,
                name=f"elec_balance_{t}_{scenario}"
            )
            
            # Heat balance (if CHP provides heat)
            if 'chp' in self.tech_generation:
                heat_from_chp = self.v_gen[('chp', t, scenario)] * (TECHNOLOGY_EFFICIENCIES['chp_thermal'] / TECHNOLOGY_EFFICIENCIES['chp_electric'])
                heat_demand = self.demand_data[scenario].loc[t, 'heat_demand']
                
                # Add slack variable for heat demand that can't be met
                self.v_heat_slack[(t, scenario)] = self.model.addVar(lb=0, ub=1000, name=f"heat_slack_{t}_{scenario}")
                
                self.model.addConstr(
                    heat_from_chp + self.v_heat_slack[(t, scenario)] >= heat_demand,
                    name=f"heat_balance_{t}_{scenario}"
                )
            
            # Hydrogen balance
            if 'electrolyzer' in self.tech_conversion:
                h2_supply = (
                    self.v_production[('electrolyzer', t, scenario)] +
                    (self.v_discharge[('h2_storage', t, scenario)] if 'h2_storage' in self.tech_storage else 0)
                )
                
                # Calculate H2 consumption by fuel cell based on generation
                fuel_cell_h2_consumption = 0
                if 'fuel_cell' in self.tech_generation and (('fuel_cell', t, scenario) in self.v_gen):
                    # H2 consumption = electricity generation / (H2 LHV * fuel cell efficiency)
                    fuel_cell_h2_consumption = self.v_gen[('fuel_cell', t, scenario)] / (ENERGY_CONVERSIONS['h2_lhv'] * TECHNOLOGY_EFFICIENCIES['fuel_cell']) * 1000  # Convert MWh to kWh then to kg H2
                
                h2_demand = (
                    self.demand_data[scenario].loc[t, 'hydrogen_demand'] +
                    (self.v_charge[('h2_storage', t, scenario)] if 'h2_storage' in self.tech_storage else 0) +
                    (self.v_consumption[('haber_bosch', t, scenario)] if 'haber_bosch' in self.tech_conversion else 0) +
                    fuel_cell_h2_consumption
                )
                
                # Add slack variable for H2 demand that can't be met
                self.v_h2_slack[(t, scenario)] = self.model.addVar(lb=0, ub=1000, name=f"h2_slack_{t}_{scenario}")
                
                self.model.addConstr(
                    h2_supply + self.v_h2_slack[(t, scenario)] >= h2_demand,
                    name=f"h2_balance_{t}_{scenario}"
                )
            
            # Water balance
            water_reclaimed = (self.v_production[('water_reclamation', t, scenario)] 
                             if 'water_reclamation' in self.tech_recovery else 0)
            water_demand = self.demand_data[scenario].loc[t, 'water_demand']
            
            self.model.addConstr(
                water_reclaimed <= water_demand,
                name=f"water_balance_{t}_{scenario}"
            )
            
            # Fertilizer balance
            n_recovered = (self.v_production[('n_recovery', t, scenario)] 
                          if 'n_recovery' in self.tech_recovery else 0)
            nh3_produced = (self.v_production[('haber_bosch', t, scenario)] 
                           if 'haber_bosch' in self.tech_conversion else 0)
            n_demand = self.demand_data[scenario].loc[t, 'fertilizer_n_demand']
            
            # Add slack variable for N demand that can't be met
            self.v_n_slack[(t, scenario)] = self.model.addVar(lb=0, ub=1000, name=f"n_slack_{t}_{scenario}")
            
            self.model.addConstr(
                n_recovered + nh3_produced * 0.82 + self.v_n_slack[(t, scenario)] >= n_demand,  # NH3 is 82% nitrogen
                name=f"n_balance_{t}_{scenario}"
            )
        
        # Emissions calculation
        for t in self.time_periods:
            grid_emissions = (
                self.v_grid_buy[('electricity', t, scenario)] * EMISSION_FACTORS['grid_electricity'] +
                self.v_grid_buy[('gas', t, scenario)] * EMISSION_FACTORS['natural_gas'] / 1000
            )
            
            # Add CHP emissions if not captured
            if 'chp' in self.tech_generation and 'carbon_capture' not in self.tech_capture:
                # Biogas is considered carbon neutral
                chp_emissions = 0
            else:
                chp_emissions = 0
            
            self.model.addConstr(
                self.v_emissions[(t, scenario)] == grid_emissions + chp_emissions,
                name=f"emissions_{t}_{scenario}"
            )
    
    def set_objective(self):
        """Set the optimization objective"""
        # Calculate annualized investment cost
        investment_cost = gp.quicksum(
            self.calculate_crf(tech) * TECHNOLOGY_CAPEX[tech] * self.v_cap[tech]
            for tech in self.all_techs
        )
        
        # Calculate expected operational cost
        operational_cost = 0
        revenues = 0
        total_emissions = 0
        penalty_cost = 0
        
        for scenario in self.scenarios:
            prob = SCENARIO_PROBABILITIES[self.scenarios.index(scenario)]
            
            # Variable O&M costs
            for tech in self.tech_generation:
                if tech in VARIABLE_OPEX:
                    for t in self.time_periods:
                        operational_cost += prob * VARIABLE_OPEX[tech] * self.v_gen[(tech, t, scenario)] / 1000
            
            # Fixed O&M costs
            for tech in self.all_techs:
                operational_cost += prob * FIXED_OPEX_PERCENTAGE * TECHNOLOGY_CAPEX[tech] * self.v_cap[tech]
            
            # Energy purchases
            for t in self.time_periods:
                elec_price = self.price_data[scenario].loc[t, 'electricity_buy_price']
                gas_price = self.price_data[scenario].loc[t, 'natural_gas_price']
                
                operational_cost += prob * (
                    elec_price * self.v_grid_buy[('electricity', t, scenario)] / 1000 +
                    gas_price * self.v_grid_buy[('gas', t, scenario)] / 1000
                )
            
            # Revenues from sales
            for t in self.time_periods:
                elec_sell_price = self.price_data[scenario].loc[t, 'electricity_sell_price']
                
                revenues += prob * (
                    elec_sell_price * self.v_grid_sell[('electricity', t, scenario)] / 1000
                )
                
                # Revenue from products
                if 'water_reclamation' in self.tech_recovery:
                    revenues += prob * PRODUCT_PRICES['reclaimed_water'] * self.v_production[('water_reclamation', t, scenario)]
                
                if 'n_recovery' in self.tech_recovery:
                    revenues += prob * PRODUCT_PRICES['fertilizer_n'] * self.v_production[('n_recovery', t, scenario)] / 1000
                
                if 'haber_bosch' in self.tech_conversion:
                    revenues += prob * PRODUCT_PRICES['ammonia'] * self.v_production[('haber_bosch', t, scenario)] / 1000
            
            # CO2 costs
            for t in self.time_periods:
                operational_cost += prob * self.co2_tax * self.v_emissions[(t, scenario)]
                total_emissions += prob * self.v_emissions[(t, scenario)]
                
                # Add penalty for unmet demands (slack variables)
                # Moderate penalty to encourage meeting demands
                penalty_rate = 1000  # $/unit
                
                # Add penalties for slack variables
                if (t, scenario) in self.v_heat_slack:
                    penalty_cost += prob * penalty_rate * self.v_heat_slack[(t, scenario)]
                
                if (t, scenario) in self.v_h2_slack:
                    penalty_cost += prob * penalty_rate * self.v_h2_slack[(t, scenario)]
                
                if (t, scenario) in self.v_n_slack:
                    penalty_cost += prob * penalty_rate * self.v_n_slack[(t, scenario)]
        
        # Scale up from representative days to annual
        days_per_season = 365 / 4
        operational_cost *= days_per_season
        revenues *= days_per_season
        total_emissions *= days_per_season
        penalty_cost *= days_per_season
        
        # Set objective based on type
        if self.objective_type == 'minimize_cost':
            self.model.setObjective(
                investment_cost + operational_cost - revenues + penalty_cost,
                GRB.MINIMIZE
            )
        elif self.objective_type == 'minimize_emissions':
            self.model.setObjective(total_emissions + penalty_cost, GRB.MINIMIZE)
        elif self.objective_type == 'minimize_cost_with_emission_cap':
            # Add emission constraint
            emission_cap = 10000  # tons CO2/year (can be parameterized)
            self.model.addConstr(
                total_emissions <= emission_cap,
                name="emission_cap"
            )
            self.model.setObjective(
                investment_cost + operational_cost - revenues + penalty_cost,
                GRB.MINIMIZE
            )
    
    def optimize(self):
        """Optimize the model"""
        # Write model for debugging
        self.model.write("model_debug.lp")
        print("Model written to model_debug.lp for debugging")
        
        # First check if model is unbounded
        self.model.setParam('DualReductions', 0)
        self.model.optimize()
        
        if self.model.status == GRB.OPTIMAL:
            print("\nOptimization successful!")
            self.print_results()
        else:
            print(f"\nOptimization failed with status: {self.model.status}")
            
            # If unbounded, add bounds and retry
            if self.model.status == GRB.UNBOUNDED or self.model.status == GRB.INF_OR_UNBD:
                print("\nModel is unbounded. Adding reasonable bounds...")
                
                # Add upper bounds on all unbounded variables
                max_grid = 1000  # MW
                max_production = 10000  # tons/hour or m3/hour
                
                # Grid interactions
                for key in self.v_grid_buy:
                    self.v_grid_buy[key].UB = max_grid
                
                for key in self.v_grid_sell:
                    self.v_grid_sell[key].UB = max_grid
                
                # Production variables
                for key in self.v_production:
                    self.v_production[key].UB = max_production
                
                # Generation variables
                for key in self.v_gen:
                    self.v_gen[key].UB = max_grid
                
                # Consumption variables
                for key in self.v_consumption:
                    self.v_consumption[key].UB = max_grid
                
                # Re-optimize
                print("Re-optimizing with bounds...")
                self.model.optimize()
                
                if self.model.status == GRB.OPTIMAL:
                    print("\nOptimization successful after adding bounds!")
                    self.print_results()
                    return
            
            # If still infeasible, compute IIS
            if self.model.status == GRB.INFEASIBLE:
                print("\nModel is infeasible. Computing IIS...")
                self.model.computeIIS()
                self.model.write("model_iis.ilp")
                print("IIS written to model_iis.ilp")
                
                # Print conflicting constraints
                print("\nConflicting constraints:")
                constraint_count = 0
                for c in self.model.getConstrs():
                    if c.IISConstr:
                        print(f"  {c.ConstrName}")
                        constraint_count += 1
                        if constraint_count > 20:  # Limit output
                            print("  ... (more constraints)")
                            break
                
                # Check if any variables have conflicting bounds
                print("\nVariables with conflicting bounds:")
                var_count = 0
                for v in self.model.getVars():
                    if v.IISLB or v.IISUB:
                        print(f"  {v.VarName}: LB={v.LB}, UB={v.UB}")
                        var_count += 1
                        if var_count > 20:  # Limit output
                            print("  ... (more variables)")
                            break
    
    def print_results(self):
        """Print optimization results"""
        print("\n" + "="*80)
        print("OPTIMIZATION RESULTS - WFE NEXUS MODEL FOR ÇORLU")
        print("="*80)
        
        print(f"\nObjective Type: {self.objective_type}")
        print(f"CO2 Policy: {self.co2_policy} (Tax: ${self.co2_tax}/ton)")
        print(f"Optimal Objective Value: ${self.model.ObjVal:,.2f}")
        
        print("\n" + "-"*50)
        print("INVESTMENT DECISIONS (First Stage)")
        print("-"*50)
        
        print(f"{'Technology':<25} {'Built':<10} {'Capacity':<20} {'Units':<15}")
        print("-"*70)
        
        for tech in self.all_techs:
            built = self.v_build[tech].X
            capacity = self.v_cap[tech].X
            
            if built > 0.5:
                if tech in self.tech_generation:
                    units = "MW"
                elif tech in self.tech_storage:
                    units = "MWh" if tech == 'battery' else "tons"
                elif tech in ['haber_bosch', 'carbon_capture']:
                    units = "tons/day"
                elif tech in ['n_recovery', 'p_recovery']:
                    units = "kg/day"
                elif tech in ['water_reclamation', 'anaerobic_digester']:
                    units = "m³/day"
                else:
                    units = "MW"
                
                print(f"{tech:<25} {'Yes':<10} {capacity:>18.2f} {units:<15}")
        
        # Calculate key performance indicators
        print("\n" + "-"*50)
        print("KEY PERFORMANCE INDICATORS")
        print("-"*50)
        
        # Calculate total renewable capacity
        renewable_cap = self.v_cap['pv'].X + self.v_cap['wind'].X
        total_gen_cap = sum(self.v_cap[tech].X for tech in self.tech_generation)
        renewable_share = renewable_cap / total_gen_cap * 100 if total_gen_cap > 0 else 0
        
        print(f"Total Renewable Capacity: {renewable_cap:.2f} MW")
        print(f"Renewable Share of Generation Capacity: {renewable_share:.1f}%")
        
        # Calculate average operational metrics
        total_h2_production = 0
        total_nh3_production = 0
        total_water_reclaimed = 0
        total_n_recovered = 0
        total_emissions = 0
        
        for scenario in self.scenarios:
            prob = SCENARIO_PROBABILITIES[self.scenarios.index(scenario)]
            
            for t in self.time_periods:
                if 'electrolyzer' in self.tech_conversion:
                    total_h2_production += prob * self.v_production[('electrolyzer', t, scenario)].X
                if 'haber_bosch' in self.tech_conversion:
                    total_nh3_production += prob * self.v_production[('haber_bosch', t, scenario)].X
                if 'water_reclamation' in self.tech_recovery:
                    total_water_reclaimed += prob * self.v_production[('water_reclamation', t, scenario)].X
                if 'n_recovery' in self.tech_recovery:
                    total_n_recovered += prob * self.v_production[('n_recovery', t, scenario)].X
                
                total_emissions += prob * self.v_emissions[(t, scenario)].X
        
        # Scale to annual values
        hours_per_year = 365 * 24
        representative_hours = len(self.time_periods)
        scale_factor = hours_per_year / representative_hours
        
        print(f"\nAnnual H2 Production: {total_h2_production * scale_factor:.2f} tons/year")
        print(f"Annual NH3 Production: {total_nh3_production * scale_factor:.2f} tons/year")
        print(f"Annual Water Reclaimed: {total_water_reclaimed * scale_factor / 1000:.2f} million m³/year")
        print(f"Annual N Recovery: {total_n_recovered * scale_factor / 1000:.2f} tons/year")
        print(f"Annual CO2 Emissions: {total_emissions * scale_factor:.2f} tons/year")
        
        # Cost breakdown
        print("\n" + "-"*50)
        print("COST BREAKDOWN")
        print("-"*50)
        
        # Calculate investment cost
        total_capex = sum(
            TECHNOLOGY_CAPEX[tech] * self.v_cap[tech].X 
            for tech in self.all_techs if self.v_build[tech].X > 0.5
        )
        
        annualized_capex = sum(
            self.calculate_crf(tech) * TECHNOLOGY_CAPEX[tech] * self.v_cap[tech].X
            for tech in self.all_techs if self.v_build[tech].X > 0.5
        )
        
        print(f"Total Capital Investment: ${total_capex:,.0f}")
        print(f"Annualized Capital Cost: ${annualized_capex:,.0f}/year")
        
        if self.objective_type != 'minimize_emissions':
            print(f"Total Annualized Cost: ${self.model.objVal:,.0f}/year")
            print(f"Cost per ton CO2 avoided: ${(self.model.objVal / (50000 - total_emissions * scale_factor)):,.2f}/ton")
        
        print("\n" + "="*80)
    
    def save_results(self, filename):
        """Save detailed results to file"""
        with open(filename, 'w') as f:
            # Redirect print output to file
            import sys
            original_stdout = sys.stdout
            sys.stdout = f
            
            self.print_results()
            
            # Additional detailed results
            print("\n\nDETAILED OPERATIONAL RESULTS")
            print("="*80)
            
            # Sample operational profile for average scenario
            scenario = 'average_renewable'
            print(f"\nOperational Profile for {scenario} scenario (first 24 hours):")
            print(f"{'Hour':<6} {'PV Gen':<10} {'Wind Gen':<10} {'Battery':<10} {'Grid Buy':<10} {'Emissions':<10}")
            print("-"*56)
            
            for i, t in enumerate(self.time_periods[:24]):
                pv_gen = self.v_gen[('pv', t, scenario)].X if ('pv', t, scenario) in self.v_gen else 0
                wind_gen = self.v_gen[('wind', t, scenario)].X if ('wind', t, scenario) in self.v_gen else 0
                battery = self.v_discharge[('battery', t, scenario)].X - self.v_charge[('battery', t, scenario)].X
                grid_buy = self.v_grid_buy[('electricity', t, scenario)].X
                emissions = self.v_emissions[(t, scenario)].X
                
                print(f"{i:<6} {pv_gen:>9.2f} {wind_gen:>9.2f} {battery:>9.2f} {grid_buy:>9.2f} {emissions:>9.2f}")
            
            sys.stdout = original_stdout
            
        print(f"\nDetailed results saved to: {filename}")

if __name__ == "__main__":
    # Example usage
    model = WFENexusModel(
        data_dir='../data',
        co2_policy='medium_tax',
        objective='minimize_cost'
    )
    model.optimize()