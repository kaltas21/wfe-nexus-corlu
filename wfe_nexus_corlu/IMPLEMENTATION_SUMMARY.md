# WFE Nexus Model Implementation Summary

## Overview

This implementation provides a comprehensive two-stage stochastic optimization model for the Water-Food-Energy (WFE) nexus in Çorlu, Türkiye. The model is built using Gurobi as the optimization solver and follows the mathematical formulation detailed in the research documentation.

## Key Features Implemented

### 1. **Two-Stage Stochastic Programming Framework**
- **First Stage**: Investment decisions (technology selection and sizing)
- **Second Stage**: Operational decisions under uncertainty scenarios

### 2. **Technology Portfolio**
The model includes a comprehensive set of technologies:

#### Energy Generation
- **Solar PV**: Variable renewable with hourly availability profiles
- **Wind Turbines**: Variable renewable with seasonal patterns
- **Biogas CHP**: Dispatchable generation using biogas from WWTP
- **Fuel Cells**: Hydrogen-based electricity generation

#### Energy Storage
- **Battery Storage**: Short-term electricity storage
- **Hydrogen Storage**: Medium-term energy storage
- **Ammonia Storage**: Long-term energy and chemical storage

#### Conversion Technologies
- **Electrolyzer**: Electricity to hydrogen conversion
- **Haber-Bosch**: Hydrogen + nitrogen to ammonia synthesis
- **Anaerobic Digester**: Sludge to biogas conversion
- **P2G Methanation**: Power-to-gas for synthetic natural gas
- **Biomethane Upgrading**: Biogas to biomethane

#### Resource Recovery
- **Water Reclamation**: Treated wastewater for reuse
- **Nitrogen Recovery**: Nutrient extraction from wastewater
- **Phosphorus Recovery**: Phosphorus extraction for fertilizers

### 3. **Uncertainty Modeling**
Three renewable availability scenarios:
- Low renewable (25% probability)
- Average renewable (50% probability)
- High renewable (25% probability)

Each scenario includes:
- Hourly solar and wind availability profiles
- Seasonal variations
- Time-of-use electricity pricing
- Demand fluctuations

### 4. **Optimization Objectives**
- **Minimize Total Annualized Cost**: Investment + operational costs - revenues
- **Minimize CO2 Emissions**: Total system emissions
- **Cost with Emission Cap**: Economic optimization with environmental constraint

### 5. **CO2 Policy Analysis**
Four policy scenarios implemented:
- No carbon tax ($0/ton)
- Low carbon tax ($30/ton)
- Medium carbon tax ($60/ton)
- High carbon tax ($100/ton)

## Data Sources and Assumptions

### Çorlu-Specific Data
- **WWTP Capacity**: 50,000 m³/day influent flow
- **Biogas Potential**: 12,250 m³/day (7,350 m³ CH4/day)
- **Energy Recovery**: 73.3 MWh/day potential from biogas

### Technology Parameters (Turkey-Specific)
- **PV CAPEX**: $900/kWp (SHURA, 2023)
- **Wind CAPEX**: $1,400/kW (SHURA, 2023)
- **Battery CAPEX**: $228/kWh (SHURA, 2023)
- **Electrolyzer**: $800/kW (SHURA, 2022)
- **Grid Emission Factor**: 0.442 ton CO2/MWh (Turkey, 2022)

### Energy Prices
- **Electricity Buy**: ~$150/MWh (4.48 TL/kWh industrial rate)
- **Electricity Sell**: ~$60/MWh (1.78 TL/kWh feed-in)
- **Natural Gas**: $500/1000 m³ (15 TL/Sm³)

## Model Constraints

### Energy Balance
- Electricity supply = demand at each hour
- Heat supply ≥ demand (from CHP)
- Hydrogen balance with storage
- Water and nutrient balances

### Technology Constraints
- Capacity limits and minimum stable generation
- Ramp rate constraints for dispatchable units
- Storage state-of-charge dynamics
- Conversion efficiency relationships

### Resource Recovery
- Biogas production from anaerobic digestion
- Nutrient recovery rates (N: 75%, P: 80%)
- Water reclamation potential

## Results and Insights

The model provides:

1. **Optimal Technology Mix**
   - Renewable capacity sizing
   - Storage requirements
   - Hydrogen infrastructure needs

2. **Operational Strategy**
   - Hourly dispatch profiles
   - Storage cycling patterns
   - Grid interaction strategy

3. **Economic Analysis**
   - Total system cost
   - Cost breakdown (CAPEX vs OPEX)
   - Revenue streams from products

4. **Environmental Performance**
   - Annual CO2 emissions
   - Renewable energy share
   - Resource recovery rates

5. **Policy Impact**
   - Technology adoption vs carbon price
   - Cost of decarbonization
   - Critical switching points

## Usage Instructions

### Basic Run
```bash
python main.py
```

### Custom Analysis
```python
from src.wfe_nexus_model import WFENexusModel

model = WFENexusModel(
    co2_policy='high_tax',
    objective='minimize_emissions'
)
model.optimize()
```

### Visualization
The model automatically generates:
- Capacity portfolio charts
- Daily operational profiles
- WFE nexus flow diagrams
- Scenario comparison plots

## Limitations and Future Work

### Current Limitations
- Uses 4 representative days instead of full 8760 hours
- Linear approximations of some nonlinear processes
- Simplified grid model without transmission constraints
- No spatial optimization for facility siting

### Potential Extensions
- Multi-stage stochastic programming for long-term planning
- Detailed MINLP formulations for process units
- Integration with agricultural models
- Social and employment impact assessment
- Detailed financial analysis with loans and subsidies

## File Structure
```
wfe_nexus_corlu/
├── config/model_config.py      # All parameters and settings
├── src/
│   ├── data_generator.py      # Synthetic data generation
│   ├── wfe_nexus_model.py     # Main Gurobi model
│   └── visualizer.py          # Results visualization
├── data/                      # Generated input data
├── results/                   # Optimization results
├── main.py                    # Main execution script
├── test_setup.py             # Setup verification
└── requirements.txt          # Python dependencies
```

## Technical Requirements
- Python 3.8+
- Gurobi Optimizer (with valid license)
- Standard scientific Python stack (pandas, numpy, matplotlib)