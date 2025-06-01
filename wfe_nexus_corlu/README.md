# WFE Nexus Optimization Model for Çorlu, Türkiye

This repository contains a comprehensive two-stage stochastic optimization model for the Water-Food-Energy (WFE) nexus in Çorlu, Türkiye. The model optimizes the design and operation of an integrated wastewater-energy-resource network under uncertainty.

## Overview

The model integrates:
- **Wastewater Treatment**: Resource recovery from wastewater (biogas, nutrients, water)
- **Renewable Energy**: Solar PV and wind generation
- **Energy Storage**: Batteries, hydrogen, and ammonia storage
- **Hydrogen Economy**: Electrolyzers, fuel cells, and ammonia synthesis
- **Circular Economy**: Nutrient recovery, water reclamation, and CO2 utilization

## Features

- **Two-stage stochastic programming** to handle uncertainties in:
  - Renewable energy availability
  - Energy prices
  - Demands
- **Multiple objectives**:
  - Minimize total annualized cost
  - Minimize CO2 emissions
  - Cost minimization with emission constraints
- **Comprehensive technology portfolio** including:
  - Renewable generation (PV, wind)
  - Energy storage (batteries, H2, NH3)
  - Conversion technologies (electrolyzers, Haber-Bosch)
  - Resource recovery (N, P, water)
  - Carbon capture and utilization

## Project Structure

```
wfe_nexus_corlu/
├── config/
│   └── model_config.py      # Model parameters and configuration
├── src/
│   ├── data_generator.py    # Synthetic data generation
│   ├── wfe_nexus_model.py   # Main optimization model (Gurobi)
│   └── visualizer.py        # Results visualization
├── data/                    # Generated data files (CSV)
├── results/                 # Optimization results and plots
└── main.py                  # Main execution script
```

## Requirements

- Python 3.8+
- Gurobi Optimizer (with valid license)
- Required Python packages:
  ```
  gurobipy
  pandas
  numpy
  matplotlib
  seaborn
  ```

## Installation

1. Install Gurobi Optimizer:
   - Academic users: https://www.gurobi.com/academia/academic-program-and-licenses/
   - Commercial users: https://www.gurobi.com/

2. Install Python dependencies:
   ```bash
   pip install gurobipy pandas numpy matplotlib seaborn
   ```

3. Clone or download this repository

## Usage

### Basic Usage

Run the main script to execute the complete analysis:

```bash
cd wfe_nexus_corlu
python main.py
```

This will:
1. Generate synthetic data based on Çorlu parameters
2. Run base case optimization (medium CO2 tax, cost minimization)
3. Perform sensitivity analysis on CO2 policies
4. Compare different objective functions
5. Generate visualizations

### Custom Analysis

To run a specific scenario:

```python
from src.wfe_nexus_model import WFENexusModel

# Create model with specific settings
model = WFENexusModel(
    data_dir='data',
    co2_policy='high_tax',  # Options: 'no_tax', 'low_tax', 'medium_tax', 'high_tax'
    objective='minimize_emissions'  # Options: 'minimize_cost', 'minimize_emissions'
)

# Optimize
model.optimize()

# Results are printed automatically
```

### Data Generation Only

To regenerate data with different parameters:

```python
from src.data_generator import DataGenerator

generator = DataGenerator()
generator.save_all_data('data')
```

## Model Parameters

Key parameters can be modified in `config/model_config.py`:

- **Technology costs**: CAPEX, OPEX, lifespans
- **Efficiencies**: Conversion efficiencies for all technologies
- **Resource data**: WWTP characteristics, renewable availability
- **Economic data**: Energy prices, product prices
- **Policy scenarios**: CO2 tax levels

## Results

The model provides:

1. **Investment Decisions**:
   - Optimal technology portfolio
   - Capacity sizing for each technology

2. **Operational Strategy**:
   - Hourly dispatch profiles
   - Storage operation patterns
   - Grid interaction strategies

3. **Performance Metrics**:
   - Total annualized cost
   - CO2 emissions
   - Resource recovery rates
   - Renewable energy share

4. **Visualizations**:
   - Technology capacity portfolio
   - Daily operational profiles
   - WFE nexus flow diagram
   - Scenario comparison charts

## Key Insights

The model demonstrates:
- The value of integrating wastewater treatment with energy systems
- Impact of CO2 policies on technology adoption
- Trade-offs between cost and emissions objectives
- Benefits of energy storage and hydrogen economy
- Synergies in the Water-Food-Energy nexus

## Limitations

- Uses representative days instead of full annual simulation
- Linear/piecewise linear approximations of some nonlinear processes
- Simplified grid interaction model
- Does not include detailed spatial considerations

## Future Extensions

- Multi-stage stochastic programming for long-term planning
- Detailed nonlinear process models
- Spatial optimization for facility siting
- Integration with agricultural and food system models
- Social and employment impact assessment

## References

Based on the research paper: "Optimal Design and Operation of an Integrated Wastewater-Energy-Resource Network under Uncertainty: A Two-Stage Stochastic Programming Approach for Çorlu, Türkiye"

## Contact

For questions or collaboration, please contact the research team.