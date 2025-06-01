"""
Data Generator for WFE Nexus Model
Generates synthetic data based on Çorlu parameters and typical profiles
"""

import numpy as np
import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.model_config import *

class DataGenerator:
    def __init__(self):
        self.seasons = ['winter', 'spring', 'summer', 'autumn']
        self.hours_per_season = HOURS_PER_DAY
        self.scenarios = SCENARIOS
        
    def generate_time_index(self):
        """Generate time index for representative days"""
        time_index = []
        for season in self.seasons:
            for hour in range(self.hours_per_season):
                time_index.append(f"{season}_h{hour:02d}")
        return time_index
    
    def generate_renewable_profiles(self):
        """Generate renewable availability profiles for PV and Wind"""
        time_index = self.generate_time_index()
        renewable_data = {}
        
        for scenario in self.scenarios:
            scenario_data = pd.DataFrame(index=time_index)
            
            # PV profiles (daily pattern with seasonal variation)
            pv_profile = []
            for season in self.seasons:
                base_factor = RENEWABLE_AVAILABILITY['pv'][season][scenario.split('_')[0]]
                for hour in range(24):
                    if 6 <= hour <= 18:  # Daylight hours
                        # Bell curve shape for solar
                        hour_factor = np.sin((hour - 6) * np.pi / 12)
                        pv_profile.append(base_factor * hour_factor * 4)  # Peak at noon
                    else:
                        pv_profile.append(0)
            
            # Wind profiles (more random with seasonal patterns)
            wind_profile = []
            for season in self.seasons:
                base_factor = RENEWABLE_AVAILABILITY['wind'][season][scenario.split('_')[0]]
                for hour in range(24):
                    # Wind with some randomness and daily pattern
                    hour_factor = 1 + 0.3 * np.sin(hour * np.pi / 12)
                    noise = np.random.normal(0, 0.1)
                    wind_profile.append(max(0, base_factor * hour_factor + noise))
            
            scenario_data['pv_availability'] = pv_profile
            scenario_data['wind_availability'] = wind_profile
            renewable_data[scenario] = scenario_data
            
        return renewable_data
    
    def generate_demand_profiles(self):
        """Generate demand profiles for electricity, heat, water, etc."""
        time_index = self.generate_time_index()
        demand_data = {}
        
        for scenario in self.scenarios:
            scenario_data = pd.DataFrame(index=time_index)
            
            # Electricity demand (daily and seasonal patterns)
            elec_demand = []
            for season in self.seasons:
                season_factor = {'winter': 1.2, 'spring': 1.0, 'summer': 1.1, 'autumn': 1.0}[season]
                for hour in range(24):
                    # Typical daily load curve
                    if 7 <= hour <= 9 or 18 <= hour <= 21:  # Peak hours
                        hour_factor = 1.3
                    elif 0 <= hour <= 6 or 22 <= hour <= 23:  # Off-peak
                        hour_factor = 0.7
                    else:  # Normal hours
                        hour_factor = 1.0
                    
                    base_demand = BASE_DEMANDS['electricity']
                    elec_demand.append(base_demand * season_factor * hour_factor)
            
            # Heat demand (stronger seasonal variation)
            heat_demand = []
            for season in self.seasons:
                season_factor = {'winter': 2.0, 'spring': 1.0, 'summer': 0.3, 'autumn': 1.2}[season]
                for hour in range(24):
                    # Heat demand peaks in morning and evening
                    if 6 <= hour <= 9 or 17 <= hour <= 22:
                        hour_factor = 1.3
                    else:
                        hour_factor = 0.8
                    
                    base_demand = BASE_DEMANDS['heat']
                    heat_demand.append(base_demand * season_factor * hour_factor)
            
            # Water demand (relatively constant with some daily variation)
            water_demand = []
            for season in self.seasons:
                season_factor = {'winter': 0.9, 'spring': 1.0, 'summer': 1.2, 'autumn': 1.0}[season]
                for hour in range(24):
                    # Water demand varies throughout the day
                    if 6 <= hour <= 22:
                        hour_factor = 1.1
                    else:
                        hour_factor = 0.8
                    
                    base_demand = BASE_DEMANDS['water'] / 24  # Convert daily to hourly
                    water_demand.append(base_demand * season_factor * hour_factor)
            
            # Fertilizer demand (seasonal for agriculture)
            fertilizer_demand = []
            for season in self.seasons:
                # Higher demand in spring and summer
                season_factor = {'winter': 0.2, 'spring': 2.0, 'summer': 1.5, 'autumn': 0.3}[season]
                daily_demand = BASE_DEMANDS['fertilizer_n'] * season_factor / 24
                fertilizer_demand.extend([daily_demand] * 24)
            
            # Hydrogen demand (industrial, relatively constant)
            h2_demand = [BASE_DEMANDS['hydrogen'] / 24] * len(time_index)
            
            scenario_data['electricity_demand'] = elec_demand
            scenario_data['heat_demand'] = heat_demand
            scenario_data['water_demand'] = water_demand
            scenario_data['fertilizer_n_demand'] = fertilizer_demand
            scenario_data['hydrogen_demand'] = h2_demand
            
            demand_data[scenario] = scenario_data
            
        return demand_data
    
    def generate_price_profiles(self):
        """Generate price profiles for electricity and other commodities"""
        time_index = self.generate_time_index()
        price_data = {}
        
        for scenario in self.scenarios:
            scenario_data = pd.DataFrame(index=time_index)
            
            # Electricity prices (time-of-use)
            elec_buy_price = []
            elec_sell_price = []
            
            for season in self.seasons:
                for hour in range(24):
                    base_buy = ENERGY_PRICES['electricity_buy']['base']
                    base_sell = ENERGY_PRICES['electricity_sell']['base']
                    
                    # Peak pricing
                    if 7 <= hour <= 9 or 18 <= hour <= 21:
                        buy_multiplier = ENERGY_PRICES['electricity_buy']['peak_multiplier']
                        sell_multiplier = 1.2
                    elif 0 <= hour <= 6 or 22 <= hour <= 23:
                        buy_multiplier = ENERGY_PRICES['electricity_buy']['off_peak_multiplier']
                        sell_multiplier = 0.8
                    else:
                        buy_multiplier = 1.0
                        sell_multiplier = 1.0
                    
                    # Add some market volatility
                    volatility = np.random.normal(1.0, 0.05)
                    
                    elec_buy_price.append(base_buy * buy_multiplier * volatility)
                    elec_sell_price.append(base_sell * sell_multiplier * volatility)
            
            # Natural gas price (seasonal variation)
            gas_price = []
            for season in self.seasons:
                season_factor = {'winter': 1.2, 'spring': 0.9, 'summer': 0.8, 'autumn': 1.0}[season]
                base_gas = ENERGY_PRICES['natural_gas']['base']
                season_price = base_gas * season_factor
                gas_price.extend([season_price] * 24)
            
            scenario_data['electricity_buy_price'] = elec_buy_price
            scenario_data['electricity_sell_price'] = elec_sell_price
            scenario_data['natural_gas_price'] = gas_price
            
            # Constant product prices
            for product, price in PRODUCT_PRICES.items():
                scenario_data[f'{product}_price'] = price
            
            price_data[scenario] = scenario_data
            
        return price_data
    
    def generate_wwtp_data(self):
        """Generate wastewater treatment plant data"""
        wwtp_data = {
            'influent_flow': WWTP_PARAMS['influent_flow'],
            'influent_characteristics': {
                'cod': WWTP_PARAMS['cod_concentration'],
                'tn': WWTP_PARAMS['tn_concentration'],
                'tp': WWTP_PARAMS['tp_concentration']
            },
            'removal_efficiencies': {
                'cod': WWTP_PARAMS['cod_removal'],
                'tn': WWTP_PARAMS['tn_removal'],
                'tp': WWTP_PARAMS['tp_removal']
            },
            'sludge_parameters': {
                'production_rate': WWTP_PARAMS['sludge_production'],
                'vs_content': WWTP_PARAMS['vs_content'],
                'biogas_yield': WWTP_PARAMS['biogas_yield'],
                'ch4_content': WWTP_PARAMS['ch4_content']
            },
            'energy_consumption': WWTP_PARAMS['energy_consumption']
        }
        
        # Calculate potential biogas production
        daily_sludge = wwtp_data['influent_flow'] * wwtp_data['sludge_parameters']['production_rate']
        vs_production = daily_sludge * wwtp_data['sludge_parameters']['vs_content'] * 1000  # kg VS/day
        biogas_production = vs_production * wwtp_data['sludge_parameters']['biogas_yield']  # m³/day
        ch4_production = biogas_production * wwtp_data['sludge_parameters']['ch4_content']  # m³ CH4/day
        
        wwtp_data['potential_biogas'] = biogas_production
        wwtp_data['potential_ch4'] = ch4_production
        wwtp_data['potential_energy_mwh'] = ch4_production * ENERGY_CONVERSIONS['ch4_lhv'] / 1000  # MWh/day
        
        return wwtp_data
    
    def save_all_data(self, output_dir):
        """Save all generated data to CSV files"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate all data
        renewable_data = self.generate_renewable_profiles()
        demand_data = self.generate_demand_profiles()
        price_data = self.generate_price_profiles()
        wwtp_data = self.generate_wwtp_data()
        
        # Save renewable profiles
        for scenario, data in renewable_data.items():
            data.to_csv(os.path.join(output_dir, f'renewable_{scenario}.csv'))
        
        # Save demand profiles
        for scenario, data in demand_data.items():
            data.to_csv(os.path.join(output_dir, f'demand_{scenario}.csv'))
        
        # Save price profiles
        for scenario, data in price_data.items():
            data.to_csv(os.path.join(output_dir, f'price_{scenario}.csv'))
        
        # Save WWTP data
        wwtp_df = pd.DataFrame([wwtp_data])
        wwtp_df.to_csv(os.path.join(output_dir, 'wwtp_data.csv'), index=False)
        
        # Save technology parameters
        tech_params = pd.DataFrame({
            'technology': list(TECHNOLOGY_CAPEX.keys()),
            'capex': list(TECHNOLOGY_CAPEX.values()),
            'lifespan': [TECHNOLOGY_LIFESPANS.get(tech, 20) for tech in TECHNOLOGY_CAPEX.keys()],
            'fixed_opex_pct': [FIXED_OPEX_PERCENTAGE] * len(TECHNOLOGY_CAPEX)
        })
        tech_params.to_csv(os.path.join(output_dir, 'technology_parameters.csv'), index=False)
        
        # Save scenario probabilities
        scenario_df = pd.DataFrame({
            'scenario': SCENARIOS,
            'probability': SCENARIO_PROBABILITIES
        })
        scenario_df.to_csv(os.path.join(output_dir, 'scenarios.csv'), index=False)
        
        print(f"All data saved to {output_dir}")
        
        # Print summary
        print("\nData Generation Summary:")
        print(f"- Time periods: {len(self.generate_time_index())} hours (4 representative days)")
        print(f"- Scenarios: {len(self.scenarios)}")
        print(f"- WWTP potential biogas: {wwtp_data['potential_biogas']:.0f} m³/day")
        print(f"- WWTP potential energy: {wwtp_data['potential_energy_mwh']:.1f} MWh/day")

if __name__ == "__main__":
    generator = DataGenerator()
    generator.save_all_data('../data')