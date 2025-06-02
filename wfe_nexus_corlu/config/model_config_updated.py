"""
Updated Configuration file for WFE Nexus Model Parameters
Based on Critical Review Recommendations for Turkish Context (2024-2025)
All parameters include sources and assumptions
"""

# General Economic Parameters
ECONOMIC_SCENARIOS = {
    'social_welfare': {
        'discount_rate': 0.045,  # 4.5% - Academic recommendation for Turkey (Halicioglu & Karatas, 2019)
        'description': 'Long-term social cost-benefit analysis'
    },
    'commercial': {
        'discount_rate': 0.20,  # 20% real - Current Turkish market conditions (2024-2025)
        'description': 'Commercial project evaluation under market conditions'
    }
}

# Scenario Structure
SCENARIOS = ['low_renewable', 'average_renewable', 'high_renewable']
SCENARIO_PROBABILITIES = [0.25, 0.50, 0.25]
TIME_PERIODS = 8760  # Hours in a year
REPRESENTATIVE_DAYS = 4  # Seasonal representative days
HOURS_PER_DAY = 24

# CO2 Policy Scenarios - HYPOTHETICAL (Turkey has no carbon pricing as of 2025)
CO2_POLICY_SCENARIOS = {
    'current_baseline': {
        'price': 0,  # $/ton CO2 - No carbon pricing in Turkey
        'description': 'Current policy - no carbon tax or ETS'
    },
    'future_low': {
        'price': 30,  # $/ton CO2
        'description': 'Hypothetical future scenario - low carbon price'
    },
    'future_medium': {
        'price': 60,  # $/ton CO2
        'description': 'Hypothetical future scenario - medium carbon price'
    },
    'future_high': {
        'price': 100,  # $/ton CO2
        'description': 'Hypothetical future scenario - high carbon price'
    }
}

# Technology Lifespans (years or operational hours)
TECHNOLOGY_LIFESPANS = {
    'pv': 30,  # years (NREL ATB 2024)
    'wind': 25,  # years (conservative, up to 30 possible)
    'battery': 15,  # years for battery component (facility 30 years with replacement)
    'electrolyzer_hours': 50000,  # operational hours (PEM/AEL)
    'electrolyzer_years': 10,  # years at 5000 hours/year operation
    'fuel_cell_hours': 50000,  # operational hours
    'fuel_cell_years': 10,  # years at 5000 hours/year operation
    'chp': 20,  # years
    'anaerobic_digester': 20,  # years (15-25 range)
    'biomethane_upgrading': 20,  # years (15-20 range)
    'wwtp_upgrade': 20,  # years (equipment components)
    'h2_storage': 30,  # years (steel/composite vessels)
    'nh3_storage': 30,  # years (refrigerated tanks)
    'carbon_capture': 25,  # years (plant infrastructure)
    'haber_bosch': 25,  # years
    'p2g_methanation': 20,  # years (15-25 range)
    'n_recovery': 20,  # years
    'p_recovery': 20,  # years
    'water_reclamation': 20  # years
}

# Technology CAPEX (2023-2024 values in $/kW, $/kWh, or $/m³/day)
TECHNOLOGY_CAPEX = {
    'pv': {
        'value': 960,  # $/kW_DC (mid-range)
        'range': {'low': 760, 'high': 1160},
        'source': 'IRENA 2023, NREL ATB 2024'
    },
    'wind': {
        'value': 1850,  # $/kW (updated from 1400)
        'range': {'low': 1700, 'high': 2000},
        'source': 'NREL Cost of Wind Energy Review 2024'
    },
    'battery': {
        'value': 375,  # $/kWh (updated from 228)
        'range': {'low': 270, 'high': 480},
        'source': 'IRENA 2023 (273) to NREL 2023 (482)'
    },
    'electrolyzer': {
        'value': 1400,  # $/kW (PEM, updated from 800)
        'range': {'low': 1000, 'high': 1800},
        'source': 'NREL 2023, DOE Pathways 2023'
    },
    'alkaline_electrolyzer': {
        'value': 1150,  # $/kW (AEL alternative)
        'range': {'low': 800, 'high': 1500},
        'source': 'DOE Pathways 2023'
    },
    'fuel_cell': {
        'value': 3500,  # $/kW (SOFC stationary, updated from 1500)
        'range': {'low': 2500, 'high': 5000},
        'source': 'NREL ATB 2024'
    },
    'chp': {
        'value': 2000,  # $/kW (CCGT CHP, updated from 1200)
        'range': {'low': 1700, 'high': 2700},
        'source': 'EIA AEO 2025 adjusted for CHP'
    },
    'anaerobic_digester': 500,  # $/m³/day (needs specific validation)
    'biomethane_upgrading': {
        'value': 2850,  # $/Nm³/h raw biogas (updated methodology)
        'range': {'low': 2300, 'high': 3400},
        'source': 'IEA ETSAP 2013 adjusted to 2023'
    },
    'wwtp_upgrade': {
        'value': 1750,  # $/m³/day (BNR upgrade)
        'range': {'low': 1000, 'high': 2500},
        'source': 'Literature review 2023'
    },
    'h2_storage': {
        'value': 900,  # $/kg (compressed, updated from 500)
        'range': {'low': 600, 'high': 1500},
        'source': 'DOE 2023'
    },
    'nh3_storage': {
        'value': 600,  # $/ton (refrigerated, updated from 200)
        'range': {'low': 500, 'high': 700},
        'source': '2017 data adjusted to 2023'
    },
    'carbon_capture': {
        'value': 300,  # $/(ton CO2/year) capacity
        'range': {'low': 150, 'high': 450},
        'source': 'Various 2023 estimates'
    },
    'haber_bosch': {
        'value': 2300,  # $/(ton NH3/year) for green NH3
        'range': {'low': 2000, 'high': 2800},
        'source': 'IEA 2021 adjusted'
    },
    'p2g_methanation': {
        'value': 650,  # $/kW_SNG output
        'range': {'low': 430, 'high': 860},
        'source': '2022 studies'
    },
    'n_recovery': 1000,  # $/kg N/day (needs validation)
    'p_recovery': 1500,  # $/kg P/day (needs validation)
    'water_reclamation': {
        'value': 1000,  # $/m³/day (MBR system)
        'range': {'low': 800, 'high': 2000},
        'source': 'Literature 2023'
    }
}

# Fixed O&M Costs (% of CAPEX per year) - Technology Specific
FIXED_OPEX_PERCENTAGE = {
    'pv': 0.024,  # 2.4% (22 $/kW-yr at 920 $/kW)
    'wind': 0.025,  # 2.5% (44 $/kW-yr at 1760 $/kW)
    'battery': 0.025,  # 2.5% of $/kW CAPEX
    'electrolyzer': 0.04,  # 4% (3-5% range)
    'alkaline_electrolyzer': 0.03,  # 3% (2-4% range)
    'fuel_cell': 0.04,  # 4% (3-5% range)
    'chp': 0.015,  # 1.5% (30 $/kW-yr at 2000 $/kW)
    'anaerobic_digester': 0.03,  # 3% (2-5% range)
    'biomethane_upgrading': 0.03,  # 3% (2-4% range)
    'wwtp_upgrade': 0.03,  # 3% (2-4% range)
    'h2_storage': 0.01,  # 1% (0.5-1.5% range)
    'nh3_storage': 0.015,  # 1.5% (1-2% range)
    'carbon_capture': 0.04,  # 4% (3-5% range)
    'haber_bosch': 0.025,  # 2.5% (2-3% range)
    'p2g_methanation': 0.03,  # 3% (2-4% range)
    'n_recovery': 0.04,  # 4% estimate
    'p_recovery': 0.04,  # 4% estimate
    'water_reclamation': 0.035  # 3.5% (MBR systems)
}

# Variable O&M Costs (Updated with technology-specific values)
VARIABLE_OPEX = {
    'pv': 0,  # $/MWh (typically negligible)
    'wind': 0,  # $/MWh (typically negligible)
    'battery': 0,  # $/MWh (captured in fixed O&M)
    'electrolyzer': 0.03,  # $/kg H2 (non-stack VOM)
    'fuel_cell': 15,  # $/MWh (10-20 range for SOFC)
    'chp': 4,  # $/MWh (3-5 range for CCGT)
    'carbon_capture': 5,  # $/ton CO2 (3-10 range, solvent makeup)
    'haber_bosch': 15,  # $/ton NH3 (10-20 range)
    'p2g_methanation': 3  # $/MWh SNG (2-5 range)
}

# Technology Efficiencies (Updated based on review)
TECHNOLOGY_EFFICIENCIES = {
    'electrolyzer': 0.63,  # 63% LHV efficiency (50-56 kWh/kg range)
    'fuel_cell': 0.55,  # 55% LHV efficiency (50-60% for SOFC)
    'chp_electric': 0.55,  # 55% electric (CCGT CHP)
    'chp_thermal': 0.30,  # 30% thermal (total 85%)
    'battery_roundtrip': 0.85,  # 85% round-trip (not separate charge/discharge)
    'biomethane_upgrading': 0.98,  # 98% methane recovery
    'carbon_capture': 0.90,  # 90% CO2 capture rate
    'p2g_efficiency': 0.55  # 55% overall electricity-to-SNG
}

# Wastewater Treatment Parameters (Validated)
WWTP_PARAMS = {
    'influent_flow': 50000,  # m³/day (Çorlu estimate)
    'cod_concentration': 500,  # mg/L
    'tn_concentration': 50,  # mg/L
    'tp_concentration': 10,  # mg/L
    'cod_removal': 0.90,  # 90% removal
    'tn_removal': 0.75,  # 75% removal (BNR)
    'tp_removal': 0.80,  # 80% removal (BNR)
    'sludge_production': 0.00025,  # kg DS/m³ wastewater
    'vs_content': 0.70,  # 70% volatile solids
    'biogas_yield': 0.35,  # m³ biogas/kg VS
    'ch4_content': 0.65,  # 65% methane (60-70% range)
    'energy_consumption': 0.7  # kWh/m³ (0.45-1.0 for BNR)
}

# Energy Conversion Factors (Validated)
ENERGY_CONVERSIONS = {
    'h2_lhv': 33.33,  # kWh/kg H2 (Lower Heating Value)
    'ch4_lhv': 9.97,  # kWh/m³ CH4
    'nh3_lhv': 5.17,  # kWh/kg NH3
    'electricity_to_h2': 53,  # kWh/kg H2 (50-56 range, mid-point)
    'h2_to_nh3': 0.178,  # kg H2/kg NH3 (stoichiometric)
    'n2_to_nh3': 0.822,  # kg N2/kg NH3 (stoichiometric)
    'co2_to_ch4': 2.75,  # kg CO2/kg CH4 (for P2G)
    'h2_to_ch4': 0.5,  # kg H2/kg CH4 (for P2G)
    'asu_energy': 0.6  # kWh/kg NH3 for N2 separation (400-900 range)
}

# Grid Emission Factors (Needs 2023 update)
EMISSION_FACTORS = {
    'grid_electricity': 0.442,  # ton CO2/MWh (Turkey 2022, needs 2023 data)
    'natural_gas': 0.202,  # ton CO2/MWh
    'biogas': 0  # Considered carbon neutral
}

# Ramp Rates (Validated and technology-specific)
RAMP_RATES = {
    'chp': {'up': 0.10, 'down': 0.10},  # 10%/min for gas turbines
    'electrolyzer': {'up': 0.20, 'down': 0.20},  # 20%/min for PEM
    'alkaline_electrolyzer': {'up': 0.04, 'down': 0.04},  # 4%/min
    'fuel_cell': {'up': 0.04, 'down': 0.04},  # 4%/min for SOFC
    'pem_fuel_cell': {'up': 0.15, 'down': 0.15}  # 15%/min for PEMFC
}

# Minimum Uptime/Downtime (hours)
MIN_UPDOWN_TIME = {
    'chp': {'up': 3, 'down': 2},
    'electrolyzer': {'up': 0, 'down': 0},  # Very flexible
    'fuel_cell': {'up': 2, 'down': 1},  # SOFC needs warmup
    'pem_fuel_cell': {'up': 0.1, 'down': 0.1}  # Fast response
}

# Storage Parameters (Updated with realistic values)
STORAGE_PARAMS = {
    'battery': {
        'max_charge_rate': 0.5,  # C-rate
        'max_discharge_rate': 0.5,  # C-rate
        'self_discharge': 0.00015,  # 1.5% per month ≈ 0.002%/hour
        'min_soc': 0.1,  # 10% minimum
        'max_soc': 0.9,  # 90% maximum
        'round_trip_efficiency': 0.85  # 85% total
    },
    'h2_storage': {
        'max_charge_rate': 0.2,  # fraction/hour
        'max_discharge_rate': 0.2,
        'leakage_rate': 0.00001,  # <0.1% per day ≈ 0.004%/hour
        'min_level': 0.05,
        'max_level': 0.95
    },
    'nh3_storage': {
        'max_charge_rate': 0.1,
        'max_discharge_rate': 0.1,
        'boil_off_rate': 0.000004,  # 0.04-0.1% per day
        'min_level': 0.05,
        'max_level': 0.95
    }
}

# Energy Price Parameters (Updated for 2024-2025)
ENERGY_PRICES = {
    'electricity_buy': {
        'base': 135,  # $/MWh (123 in 2023 + 10% increase)
        'peak_multiplier': 1.5,
        'off_peak_multiplier': 0.7,
        'source': 'EPDK 2023-2024'
    },
    'electricity_sell': {
        'base': 60,  # $/MWh (needs market verification)
        'renewable_premium': 1.2  # 20% premium
    },
    'natural_gas': {
        'base': 430,  # $/1000 m³ (12-14 $/MMBtu equivalent)
        'source': 'BOTAS 2024-2025'
    }
}

# Product Prices (Updated based on review)
PRODUCT_PRICES = {
    'hydrogen': {
        'value': 4500,  # $/ton (3-6 $/kg range, mid-point)
        'range': {'low': 3000, 'high': 6000},
        'source': 'Global production costs 2023-2024'
    },
    'ammonia': {
        'value': 425,  # $/ton (updated from 500)
        'range': {'low': 400, 'high': 450},
        'source': 'Turkey CFR Dec 2024'
    },
    'sng': {
        'value': 1300,  # $/1000 m³ (3x natural gas price)
        'range': {'low': 1100, 'high': 1600},
        'source': 'European estimates 2023'
    },
    'reclaimed_water': 0.5,  # $/m³
    'fertilizer_n': 600,  # $/ton N
    'fertilizer_p': 800  # $/ton P
}

# Demand Profiles (Çorlu-specific where available)
BASE_DEMANDS = {
    'electricity': 50,  # MW average (needs validation)
    'heat': 20,  # MW average (needs validation)
    'water': 30000,  # m³/day
    'fertilizer_n': 10,  # tons N/day (agricultural region)
    'hydrogen': 1  # tons H2/day (emerging demand)
}

# Renewable Capacity Factors (Needs validation with Turkish data)
# These should be replaced with hourly profiles from GEPA/REPA
RENEWABLE_CAPACITY_FACTORS = {
    'pv': {
        'annual_average': 0.22,  # 22% (18-28% range for Turkey)
        'seasonal': {
            'winter': 0.12,
            'spring': 0.20,
            'summer': 0.30,
            'autumn': 0.16
        }
    },
    'wind': {
        'annual_average': 0.35,  # 35% (30-50% range for good sites)
        'seasonal': {
            'winter': 0.40,
            'spring': 0.30,
            'summer': 0.25,
            'autumn': 0.35
        }
    }
}

# Capacity Limits (Project-specific)
CAPACITY_LIMITS = {
    'pv': {'min': 0, 'max': 100},  # MW
    'wind': {'min': 0, 'max': 150},  # MW
    'battery': {'min': 0, 'max': 200},  # MWh
    'electrolyzer': {'min': 0, 'max': 50},  # MW
    'h2_storage': {'min': 0, 'max': 1000},  # kg
    'nh3_storage': {'min': 0, 'max': 5000},  # ton
    'haber_bosch': {'min': 0, 'max': 20},  # tons NH3/day
    'carbon_capture': {'min': 0, 'max': 100},  # tons CO2/day
    'p2g_methanation': {'min': 0, 'max': 20}  # MW SNG
}

# Model Configuration Metadata
MODEL_CONFIG_METADATA = {
    'version': '2.0',
    'last_updated': '2025-01-06',
    'currency': 'USD',
    'base_year': '2024',
    'sources': [
        'Critical Review of Energy System Parameters (2025)',
        'NREL ATB 2024',
        'IRENA Renewable Power Generation Costs 2023',
        'IEA Reports 2023-2024',
        'Turkish Energy Market Data (EPDK, BOTAS) 2024-2025'
    ]
}