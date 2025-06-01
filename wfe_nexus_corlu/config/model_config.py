"""
Configuration file for WFE Nexus Model Parameters
Based on Çorlu, Türkiye case study
"""

# General Parameters
DISCOUNT_RATE = 0.08  # 8% for public projects in Turkey
SCENARIOS = ['low_renewable', 'average_renewable', 'high_renewable']
SCENARIO_PROBABILITIES = [0.25, 0.50, 0.25]
TIME_PERIODS = 8760  # Hours in a year
REPRESENTATIVE_DAYS = 4  # Seasonal representative days (simplified)
HOURS_PER_DAY = 24

# CO2 Policy Scenarios
CO2_TAX_SCENARIOS = {
    'no_tax': 0,
    'low_tax': 30,  # $/ton CO2
    'medium_tax': 60,  # $/ton CO2
    'high_tax': 100  # $/ton CO2
}

# Technology Lifespans (years)
TECHNOLOGY_LIFESPANS = {
    'pv': 25,
    'wind': 20,
    'battery': 15,
    'electrolyzer': 20,
    'fuel_cell': 15,
    'chp': 20,
    'anaerobic_digester': 20,
    'biomethane_upgrading': 20,
    'wwtp_upgrade': 25,
    'h2_storage': 25,
    'nh3_storage': 25,
    'carbon_capture': 20,
    'haber_bosch': 25,
    'p2g_methanation': 20,
    'n_recovery': 20,
    'p_recovery': 20,
    'water_reclamation': 20
}

# Technology CAPEX ($/kW or $/kWh or $/m³/day)
TECHNOLOGY_CAPEX = {
    'pv': 900,  # $/kWp (SHURA, 2023)
    'wind': 1400,  # $/kW (SHURA, 2023)
    'battery': 228,  # $/kWh (SHURA, 2023)
    'electrolyzer': 800,  # $/kW (SHURA, 2022)
    'fuel_cell': 1500,  # $/kW
    'chp': 1200,  # $/kW
    'anaerobic_digester': 500,  # $/m³/day
    'biomethane_upgrading': 400,  # $/m³/day
    'wwtp_upgrade': 300,  # $/m³/day
    'h2_storage': 500,  # $/kg
    'nh3_storage': 200,  # $/ton
    'carbon_capture': 600,  # $/ton CO2/day
    'haber_bosch': 500,  # $/ton NH3/day
    'p2g_methanation': 1000,  # $/kW SNG
    'n_recovery': 1000,  # $/kg N/day
    'p_recovery': 1500,  # $/kg P/day
    'water_reclamation': 200  # $/m³/day
}

# Fixed O&M Costs (% of CAPEX per year)
FIXED_OPEX_PERCENTAGE = 0.015  # 1.5% of CAPEX

# Variable O&M Costs
VARIABLE_OPEX = {
    'pv': 5,  # $/MWh
    'wind': 10,  # $/MWh
    'battery': 2,  # $/MWh
    'electrolyzer': 2,  # $/kg H2
    'fuel_cell': 5,  # $/MWh
    'chp': 8,  # $/MWh
    'carbon_capture': 10,  # $/ton CO2
    'haber_bosch': 20,  # $/ton NH3
    'p2g_methanation': 5  # $/MWh SNG
}

# Technology Efficiencies
TECHNOLOGY_EFFICIENCIES = {
    'electrolyzer': 0.65,  # 65% efficiency
    'fuel_cell': 0.60,  # 60% efficiency
    'chp_electric': 0.40,  # 40% electric efficiency
    'chp_thermal': 0.45,  # 45% thermal efficiency
    'battery_charge': 0.95,  # 95% charge efficiency
    'battery_discharge': 0.95,  # 95% discharge efficiency
    'biomethane_upgrading': 0.97,  # 97% methane recovery
    'carbon_capture': 0.90,  # 90% CO2 capture rate
    'p2g_efficiency': 0.60  # 60% overall efficiency
}

# Wastewater Treatment Parameters
WWTP_PARAMS = {
    'influent_flow': 50000,  # m³/day (for Çorlu)
    'cod_concentration': 500,  # mg/L
    'tn_concentration': 50,  # mg/L
    'tp_concentration': 10,  # mg/L
    'cod_removal': 0.90,  # 90% removal
    'tn_removal': 0.75,  # 75% removal
    'tp_removal': 0.80,  # 80% removal
    'sludge_production': 0.001,  # m³ sludge/m³ wastewater
    'vs_content': 0.70,  # 70% volatile solids in sludge
    'biogas_yield': 0.35,  # m³ biogas/kg VS
    'ch4_content': 0.60,  # 60% methane in biogas
    'energy_consumption': 0.5  # kWh/m³ wastewater
}

# Energy Conversion Factors
ENERGY_CONVERSIONS = {
    'h2_lhv': 33.33,  # kWh/kg H2 (Lower Heating Value)
    'ch4_lhv': 9.97,  # kWh/m³ CH4
    'nh3_lhv': 5.17,  # kWh/kg NH3
    'electricity_to_h2': 55,  # kWh/kg H2 (electrolyzer consumption)
    'h2_to_nh3': 0.178,  # kg H2/kg NH3 (stoichiometric)
    'n2_to_nh3': 0.822,  # kg N2/kg NH3 (stoichiometric)
    'co2_to_ch4': 2.75,  # kg CO2/kg CH4 (for P2G)
    'h2_to_ch4': 0.5  # kg H2/kg CH4 (for P2G)
}

# Grid Emission Factors
EMISSION_FACTORS = {
    'grid_electricity': 0.442,  # ton CO2/MWh (Turkey, 2022)
    'natural_gas': 0.202,  # ton CO2/MWh
    'biogas': 0  # Considered carbon neutral
}

# Ramp Rates (% of capacity per hour)
RAMP_RATES = {
    'chp': {'up': 0.30, 'down': 0.30},
    'electrolyzer': {'up': 0.80, 'down': 0.80},
    'fuel_cell': {'up': 0.50, 'down': 0.50}
}

# Minimum Uptime/Downtime (hours)
MIN_UPDOWN_TIME = {
    'chp': {'up': 3, 'down': 2},
    'electrolyzer': {'up': 0, 'down': 0},
    'fuel_cell': {'up': 1, 'down': 1}
}

# Storage Parameters
STORAGE_PARAMS = {
    'battery': {
        'max_charge_rate': 0.5,  # C-rate
        'max_discharge_rate': 0.5,  # C-rate
        'self_discharge': 0.0001,  # 0.01% per hour
        'min_soc': 0.1,  # 10% minimum state of charge
        'max_soc': 0.9  # 90% maximum state of charge
    },
    'h2_storage': {
        'max_charge_rate': 0.2,  # fraction of capacity per hour
        'max_discharge_rate': 0.2,
        'self_discharge': 0.001,  # 0.1% per hour
        'min_level': 0.05,
        'max_level': 0.95
    },
    'nh3_storage': {
        'max_charge_rate': 0.1,
        'max_discharge_rate': 0.1,
        'self_discharge': 0.0001,
        'min_level': 0.05,
        'max_level': 0.95
    }
}

# Demand Profiles (simplified - will be expanded with actual data)
BASE_DEMANDS = {
    'electricity': 50,  # MW average
    'heat': 20,  # MW average
    'water': 30000,  # m³/day
    'fertilizer_n': 10,  # tons N/day
    'hydrogen': 1  # tons H2/day
}

# Renewable Availability Factors (seasonal averages)
RENEWABLE_AVAILABILITY = {
    'pv': {
        'winter': {'low': 0.08, 'average': 0.12, 'high': 0.16},
        'spring': {'low': 0.16, 'average': 0.20, 'high': 0.24},
        'summer': {'low': 0.20, 'average': 0.25, 'high': 0.30},
        'autumn': {'low': 0.12, 'average': 0.16, 'high': 0.20}
    },
    'wind': {
        'winter': {'low': 0.20, 'average': 0.30, 'high': 0.40},
        'spring': {'low': 0.15, 'average': 0.25, 'high': 0.35},
        'summer': {'low': 0.10, 'average': 0.20, 'high': 0.30},
        'autumn': {'low': 0.18, 'average': 0.28, 'high': 0.38}
    }
}

# Energy Price Parameters (TL converted to USD, 1 USD ≈ 30 TL)
ENERGY_PRICES = {
    'electricity_buy': {
        'base': 150,  # $/MWh (~4.48 TL/kWh)
        'peak_multiplier': 1.5,
        'off_peak_multiplier': 0.7
    },
    'electricity_sell': {
        'base': 60,  # $/MWh (~1.78 TL/kWh)
        'renewable_premium': 1.2  # 20% premium for renewable
    },
    'natural_gas': {
        'base': 500  # $/1000 m³ (~15 TL/Sm³)
    }
}

# Product Prices
PRODUCT_PRICES = {
    'hydrogen': 3000,  # $/ton
    'ammonia': 500,  # $/ton
    'sng': 400,  # $/1000 m³
    'reclaimed_water': 0.5,  # $/m³
    'fertilizer_n': 600,  # $/ton N
    'fertilizer_p': 800  # $/ton P
}

# Capacity Limits
CAPACITY_LIMITS = {
    'pv': {'min': 0, 'max': 100},  # MW
    'wind': {'min': 0, 'max': 150},  # MW
    'battery': {'min': 0, 'max': 200},  # MWh
    'electrolyzer': {'min': 0, 'max': 50},  # MW
    'h2_storage': {'min': 0, 'max': 1000},  # kg
    'nh3_storage': {'min': 0, 'max': 5000},  # kg
    'haber_bosch': {'min': 0, 'max': 20},  # tons NH3/day
    'carbon_capture': {'min': 0, 'max': 100},  # tons CO2/day
    'p2g_methanation': {'min': 0, 'max': 20}  # MW SNG
}