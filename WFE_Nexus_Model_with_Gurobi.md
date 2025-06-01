# Template: Two-Stage Stochastic WFE Nexus Model (Gurobi Formulation)

## 1. Introduction

This document provides a complete template for developing a two-stage stochastic Mixed-Integer (Non)Linear Programming model for the optimal design and operation of an integrated Water-Food-Energy (WFE) nexus. The model is tailored for the specific context of Çorlu, Türkiye, and incorporates renewable energy, wastewater treatment and resource recovery, hydrogen and nitrogen cycles, and various energy carriers.

The model's primary goal is to determine the optimal investment decisions (**first-stage**) and operational strategies (**second-stage**) under uncertainty to achieve specific objectives, such as minimizing costs or environmental impact. This formulation is designed for direct implementation in a powerful solver like Gurobi by constructing the full deterministic equivalent of the stochastic program.

***
## 2. Conceptual Model Graph (Graph Theory Representation) 🕸️

The WFE nexus can be conceptualized as a directed graph `G = (V, E)`, where nodes `V` are technologies, resources, or demands, and edges `E` represent the flow of material or energy. This provides a powerful mental model for understanding system interdependencies and formulating balance constraints.

* **Nodes (Vertices) `V`**:
    * **Resource Nodes**: `ATMOSPHERE` (source of N2, sink for CO2), `WATER_SOURCE` (e.g., river), `GRID` (source/sink for electricity), `GAS_GRID` (source/sink for natural gas/biomethane), `SUN` (source for PV), `WIND` (source for Turbines).
    * **Technology Nodes**: `PV`, `WIND_TURBINE`, `WWTP` (Wastewater Treatment Plant), `ANAEROBIC_DIGESTER`, `BIOGAS_CHP`, `BIOMETHANE_UPGRADING`, `N_RECOVERY`, `P_RECOVERY`, `WATER_RECLAMATION`, `ELECTROLYZER` (AE/PEME), `SMR` (Steam Methane Reforming), `HABER_BOSCH`, `AMMONIA_CRACKER`, `FUEL_CELL`, `BATTERY_STORAGE`, `H2_STORAGE`, `NH3_STORAGE`, `CARBON_CAPTURE`, `P2G_METHANATION`.
    * **Demand Nodes**: `ELEC_DEMAND`, `HEAT_DEMAND`, `WATER_DEMAND`, `FERTILIZER_DEMAND`, `H2_DEMAND`, `SNG_DEMAND`.

* **Edges (Flows) `E`**:
    * `WIND` → `WIND_TURBINE` (Kinetic Energy)
    * `SUN` → `PV` (Solar Irradiance)
    * `WIND_TURBINE` → `GRID` (Electricity)
    * `WIND_TURBINE` → `BATTERY_STORAGE` (Electricity)
    * `WIND_TURBINE` → `ELECTROLYZER` (Electricity)
    * `PV` → `ELEC_DEMAND` (Electricity)
    * `WWTP_INFLUENT` → `WWTP` (Wastewater)
    * `WWTP` → `WATER_RECLAMATION` (Treated Effluent)
    * `WWTP` → `ANAEROBIC_DIGESTER` (Sludge)
    * `ANAEROBIC_DIGESTER` → `BIOGAS_CHP` (Biogas)
    * `ANAEROBIC_DIGESTER` → `BIOMETHANE_UPGRADING` (Biogas)
    * `BIOGAS_CHP` → `ELEC_DEMAND` (Electricity)
    * `BIOGAS_CHP` → `HEAT_DEMAND` (Heat)
    * `BIOMETHANE_UPGRADING` → `GAS_GRID` (Biomethane/SNG)
    * `BIOMETHANE_UPGRADING` → `CARBON_CAPTURE` (CO2 Stream)
    * `WATER_RECLAMATION` → `WATER_DEMAND` (Reclaimed Water)
    * `WWTP` → `N_RECOVERY` / `P_RECOVERY` (Nutrient-rich streams)
    * `N_RECOVERY` → `FERTILIZER_DEMAND` (Nitrogen Fertilizer)
    * `ELECTROLYZER` → `H2_STORAGE` (Hydrogen)
    * `H2_STORAGE` → `HABER_BOSCH` (Hydrogen)
    * `H2_STORAGE` → `FUEL_CELL` (Hydrogen)
    * `H2_STORAGE` → `P2G_METHANATION` (Hydrogen)
    * `ATMOSPHERE` → `HABER_BOSCH` (Nitrogen)
    * `HABER_BOSCH` → `NH3_STORAGE` (Ammonia)
    * `NH3_STORAGE` → `FERTILIZER_DEMAND` (Ammonia)
    * `NH3_STORAGE` → `AMMONIA_CRACKER` (Ammonia)
    * `CARBON_CAPTURE` → `P2G_METHANATION` (CO2)
    * `GRID` ↔ `SYSTEM_BUS` (Electricity Purchase/Sale)

***
## 3. Mathematical Formulation

### **A. Sets and Indices**

* `i, j ∈ I`: Set of all technologies.
* `g ∈ I_gen ⊂ I`: Subset of generation technologies (PV, Wind, CHP, etc.).
* `s ∈ I_stor ⊂ I`: Subset of storage technologies (Batteries, H2 Storage, etc.).
* `c ∈ I_conv ⊂ I`: Subset of conversion technologies (Electrolyzer, WWTP, etc.).
* `r ∈ R`: Set of resources (electricity, heat, water, H2, NH3, CO2, biogas, etc.).
* `t ∈ T`: Set of time periods in the operational horizon (e.g., hours 1...8760).
* `ω ∈ Ω`: Set of scenarios for uncertain parameters.

### **B. Parameters**

This table details the parameters required for the model. Placeholder values are illustrative and should be refined with specific data for Çorlu where available.

| Parameter                      | Symbol                    | Description                                                                  | Units                  | Illustrative Value / Source                                  |
| ------------------------------ | ------------------------- | ---------------------------------------------------------------------------- | ---------------------- | ------------------------------------------------------------ |
| **General** | `p_prob[ω]`               | Probability of scenario `ω` occurring.                                       | -                      | `1 / len(Ω)` (if equally likely)                             |
|                                | `p_discount_rate`         | Annual discount rate for investments.                                        | %                      | 8.0 / (SBB/Public Projects in Turkey)                      |
|                                | `p_lifespan[i]`           | Operational lifetime of technology `i`.                                      | years                  | Varies (e.g., PV: 25, Wind: 20, Battery: 15)                 |
|                                | `p_CRF[i]`                | Capital Recovery Factor for technology `i`.                                  | -                      | `(d * (1+d)^L) / ((1+d)^L - 1)`                              |
| **Techno-Economic** |                           |                                                                              |                        |                                                              |
| *Capital Costs* | `p_CAPEX[i]`              | Investment cost per unit of capacity for technology `i`.                     | `$/kW` or `$/kWh` etc. | PV: 900 $/kWp, Wind: 1400 $/kW, Battery: 228 $/kWh (SHURA, 2023) |
| *Fixed O&M Costs* | `p_OPEX_fix[i]`           | Fixed annual operation & maintenance cost per unit of capacity.            | `$/kW/yr`              | Varies (e.g., 1.5% of CAPEX)                                 |
| *Variable O&M Costs* | `p_OPEX_var[i]`           | Variable O&M cost per unit of generation/production.                         | `$/MWh` or `$/kg`      | Wind: 10 $/MWh, PV: 5 $/MWh                                  |
| *Efficiency* | `p_eff[i]`                | Conversion efficiency of technology `i`.                                     | %                      | Electrolyzer: 65%, Fuel Cell: 60%, CHP: 85% (elec+therm)   |
| *Ramp Rates* | `p_ramp_up[i]` / `down[i]` | Max ramp-up/down rate as a fraction of capacity per time step.             | `% of Cap/hr`          | CHP: 30%, Electrolyzer: 80%                                  |
| *Min Uptime/Downtime* | `p_min_up[i]` / `down[i]` | Minimum uptime/downtime after starting/stopping.                             | hours                  | CHP: 3 hours                                                 |
| **Resource & Market (Stochastic)** |                           |                                                                              |                        |                                                              |
| *Renewable Availability* | `p_avail[i,t,ω]`          | Availability factor for renewable tech `i` (solar, wind) at time `t`, scenario `ω`. | %                      | Based on historical weather data for Çorlu (GEPA/REPA)       |
| *Energy Prices* | `p_price_elec_buy[t,ω]`   | Price to buy electricity from the grid.                                      | `$/MWh`                | Based on EPDK/TREPAŞ tariffs (e.g., ~4.48 TL/kWh for industry) |
|                                | `p_price_elec_sell[t,ω]`  | Price to sell electricity to the grid.                                       | `$/MWh`                | Based on YEKDEM or market prices (e.g., ~1.78 TL/kWh)      |
|                                | `p_price_gas[t,ω]`        | Price of natural gas.                                                        | `$/m³`                 | ~15.00 TL/Sm³ (for electricity gen) / BOTAŞ                |
| *CO2 Price* | `p_price_co2[ω]`          | Cost of CO2 emissions (tax or trading price).                                | `$/ton CO2`            | Scenario-dependent (e.g., 30, 60, 100 $/ton)                 |
| *Demand Profiles* | `p_demand[r,t,ω]`         | Demand for resource `r` (electricity, heat, water) at time `t`, scenario `ω`. | `MW`, `m³/hr` etc.     | Based on Çorlu SECAP annual totals, scaled with typical profiles |
| **Technology Specific** |                           |                                                                              |                        |                                                              |
| *WWTP* | `p_ww_removal[p]`         | Removal efficiency of pollutant `p` (COD, N, P) in the WWTP.                 | %                      | COD: 90%, TN: 75%, TP: 80% (typical for advanced bio)      |
|                                | `p_biogas_yield`          | Biogas yield from sludge in anaerobic digester.                              | `m³/kg VS`             | 0.35                                                         |
|                                | `p_ch4_content`           | Methane content of biogas.                                                   | %                      | 60%                                                          |
| *Electrolyzer* | `p_elec_cons_H2`          | Electricity consumption to produce 1 kg of H2.                               | `MWh/kg H2`            | ~0.055 MWh/kg (SHURA, 2022)                                  |
| *Haber-Bosch* | `p_h2_for_nh3`            | H2 required to produce 1 kg of NH3.                                          | `kg H2/kg NH3`         | 0.178                                                        |
|                                | `p_n2_for_nh3`            | N2 required to produce 1 kg of NH3.                                          | `kg N2/kg NH3`         | 0.822                                                        |
| *Carbon Capture* | `p_capture_rate[i]`       | Fraction of CO2 captured from the flue gas of technology `i`.                | %                      | 90% (for MEA solvent)                                        |
|                                | `p_capture_energy`        | Energy penalty for carbon capture.                                           | `MWh/ton CO2`          | 0.7 MWh/ton CO2                                              |
| *Storage* | `p_storage_loss[s]`       | Self-discharge/loss rate of storage technology `s` per time step.            | `% per hour`           | Battery: 0.01%, H2 Storage (compressed): 0.1%              |
| **Emissions** | `p_emis_factor[r]`        | CO2 emission factor for resource `r` (grid electricity, natural gas).        | `ton CO2/MWh`          | Grid: 0.442 (Enerji Bülteni, 2022), NG: 0.202               |

### **C. Decision Variables**

**First-Stage (Here-and-Now / Investment):**
* `v_cap[i]`: Continuous variable for the capacity of technology `i` to be built (e.g., in MW, MWh, m³/day).
* `v_build[i]`: Binary variable indicating if technology `i` is built (`1`) or not (`0`).

**Second-Stage (Wait-and-See / Operational - scenario dependent):**
* `v_gen[i,t,ω]`: Power generated by technology `i` at time `t` in scenario `ω`.
* `v_cons[i,t,ω]`: Power/resource consumed by technology `i` at time `t` in scenario `ω`.
* `v_flow[r,i,j,t,ω]`: Flow of resource `r` from technology/node `i` to `j` at time `t` in scenario `ω`.
* `v_storage_level[s,t,ω]`: Energy/mass stored in storage unit `s` at the end of time `t` in scenario `ω`.
* `v_charge[s,t,ω]`: Energy/mass charged into storage unit `s` at time `t` in scenario `ω`.
* `v_discharge[s,t,ω]`: Energy/mass discharged from storage unit `s` at time `t` in scenario `ω`.
* `v_buy[r,t,ω]`: Amount of resource `r` (e.g., electricity, gas) purchased from the grid at time `t` in scenario `ω`.
* `v_sell[r,t,ω]`: Amount of resource `r` sold to the grid at time `t` in scenario `ω`.
* `v_emissions[t,ω]`: Total CO2 emissions at time `t` in scenario `ω`.
* `v_is_on[i,t,ω]`: Binary variable indicating if dispatchable unit `i` is on (`1`) at time `t`, scenario `ω`.
* `v_startup[i,t,ω]`: Binary variable indicating if unit `i` starts up at time `t`, scenario `ω`.
* `v_shutdown[i,t,ω]`: Binary variable indicating if unit `i` shuts down at time `t`, scenario `ω`.

### **D. Objective Function(s)**

The model can be optimized for different objectives.

**Objective 1: Minimize Total Expected Annualized Cost (TAC)**
`Minimize Z = InvestmentCost + ExpectedOperationCost`
* `InvestmentCost = sum( p_CRF[i] * p_CAPEX[i] * v_cap[i] for i in I )`
* `ExpectedOperationCost = sum( p_prob[ω] * (OperationalCosts[ω] - Revenues[ω]) for ω in Ω )`
    * `OperationalCosts[ω] = sum( v_gen[i,t,ω] * p_OPEX_var[i] + v_buy[r,t,ω] * p_price[r,t,ω] + v_emissions[t,ω] * p_price_co2[ω] for i,r,t ) + sum( v_cap[i] * p_OPEX_fix[i] for i)`
    * `Revenues[ω] = sum( v_sell[r,t,ω] * p_price_sell[r,t,ω] for r,t )`

**Objective 2: Minimize Total Expected CO2 Emissions**
`Minimize Z_CO2 = sum( p_prob[ω] * sum(v_emissions[t,ω] for t in T) for ω in Ω )`

**Objective 3: Minimize TAC with an Emissions Cap**
`Minimize Z` (from Objective 1)
* **Subject to:** `sum( p_prob[ω] * sum(v_emissions[t,ω] for t in T) for ω in Ω ) <= p_CO2_Cap`

### **E. Constraints**

For each scenario `ω ∈ Ω` and time period `t ∈ T`.

**1. Investment and Capacity Constraints**
* `v_cap[i] <= v_build[i] * M` (Big-M constraint linking capacity to build decision)
* `v_cap[i] >= v_build[i] * p_min_capacity[i]` (Minimum capacity if built)
* `sum( p_CAPEX[i] * v_cap[i] for i in I ) <= p_Total_Budget` (Optional budget constraint)

**2. General Energy/Mass Balance Constraints**
For each resource `r` (e.g., electricity, heat, H2, water) and at each internal node/bus:
`Sum(Generation of r) + Sum(In-Flows of r) + Sum(Discharge of r) + Sum(Purchases of r) == Sum(Consumption of r) + Sum(Out-Flows of r) + Sum(Charge of r) + Sum(Demand for r)`

**3. Technology-Specific Constraints**

* **Renewable Generation (PV, Wind):**
    `v_gen[i,t,ω] == v_cap[i] * p_avail[i,t,ω]`

* **Dispatchable Generation (CHP, Fuel Cell, etc.):**
    * `v_gen[i,t,ω] <= v_cap[i] * v_is_on[i,t,ω]` (Max output)
    * `v_gen[i,t,ω] >= p_min_load[i] * v_cap[i] * v_is_on[i,t,ω]` (Min stable load)
    * `v_gen[i,t,ω] - v_gen[i,t-1,ω] <= p_ramp_up[i] * v_cap[i]` (Ramp-up limit)
    * `v_gen[i,t-1,ω] - v_gen[i,t,ω] <= p_ramp_down[i] * v_cap[i]` (Ramp-down limit)
    * `v_startup[i,t,ω] >= v_is_on[i,t,ω] - v_is_on[i,t-1,ω]`
    * `v_shutdown[i,t,ω] >= v_is_on[i,t-1,ω] - v_is_on[i,t,ω]`
    * `Sum(v_is_on[i,k,ω] for k from t to t+p_min_up[i]-1) >= p_min_up[i] * v_startup[i,t,ω]` (Min uptime)

* **Wastewater Treatment Plant (WWTP):**
    * `v_flow_out[WWTP, 'TreatedWater', t, ω] == v_flow_in[WWTP, 'Wastewater', t, ω] * (1 - p_water_loss_wwtp)`
    * `v_pollutant_out[p,t,ω] == v_pollutant_in[p,t,ω] * (1 - p_ww_removal[p])` (For COD, N, P)
    * `v_flow_out[WWTP, 'Sludge', t, ω] == v_flow_in[WWTP, 'Wastewater', t, ω] * p_sludge_production_rate`

* **Anaerobic Digester & Biogas:**
    * `v_flow_out[AD, 'Biogas', t, ω] == v_flow_in[AD, 'Sludge', t, ω] * p_VS_content * p_biogas_yield`
    * `v_flow_out[Biogas, 'CH4', t, ω] == v_flow_out[Biogas, 'Total', t, ω] * p_ch4_content`
    * `v_flow_out[Biogas, 'CO2', t, ω] == v_flow_out[Biogas, 'Total', t, ω] * (1 - p_ch4_content)`

* **Electrolyzer:**
    * `v_flow_out[Electrolyzer, 'H2', t, ω] == v_cons[Electrolyzer, 'Elec', t, ω] / p_elec_cons_H2`
    * `v_cons[Electrolyzer, 'Elec', t, ω] <= v_cap[Electrolyzer]`

* **Haber-Bosch (Ammonia Synthesis):**
    * `v_flow_out[HB, 'NH3', t, ω] * p_h2_for_nh3 == v_flow_in[HB, 'H2', t, ω]`
    * `v_flow_out[HB, 'NH3', t, ω] * p_n2_for_nh3 == v_flow_in[HB, 'N2', t, ω]`

* **Carbon Capture:**
    * `v_co2_captured[i,t,ω] == v_co2_produced[i,t,ω] * p_capture_rate[i]`
    * `v_cons_energy[Capture,t,ω] == v_co2_captured[i,t,ω] * p_capture_energy`

**4. Storage Constraints**
For each storage technology `s`, time `t > 1`, scenario `ω`:
* `v_storage_level[s,t,ω] == v_storage_level[s,t-1,ω] * (1 - p_storage_loss[s]) + (v_charge[s,t,ω] * p_eff_charge[s]) - (v_discharge[s,t,ω] / p_eff_discharge[s])` (Inventory balance)
* `v_storage_level[s,t,ω] <= v_cap[s]` (Max storage capacity)
* `v_charge[s,t,ω] <= p_max_charge_rate[s] * v_cap[s]` (Max charge rate)
* `v_discharge[s,t,ω] <= p_max_discharge_rate[s] * v_cap[s]` (Max discharge rate)
* `v_storage_level[s, T_final, ω] == v_storage_level[s, T_initial, ω]` (Optional: cyclic storage)

**5. Demand Satisfaction and Emissions**
* `Sum(Supply of r at t,ω) >= p_demand[r,t,ω]` (For all resources `r` with a demand)
* `v_emissions[t,ω] == v_buy['Elec',t,ω] * p_emis_factor['Grid'] + v_cons['Gas',t,ω] * p_emis_factor['Gas'] + Sum(unabated emissions from tech i)`

***
## 4. Gurobi Implementation Guide

1.  **Import `gurobipy`**.
2.  **Load Data**: Load all parameters from data files (e.g., CSV, Excel) into Python data structures (e.g., dictionaries, pandas DataFrames).
3.  **Create Model**: `m = gp.Model("WFE_Nexus_Stochastic")`
4.  **Define Variables**:
    * Define first-stage variables (`v_cap`, `v_build`) directly.
    * Define second-stage variables for all time periods `t` and scenarios `ω`. For a large number of scenarios, this creates a very large number of variables. For example: `v_gen = m.addVars(I_gen, T, Ω, name="generation")`.
5.  **Set Objective**: Build the objective function expression using the defined variables and parameters. `m.setObjective(investment_cost + expected_op_cost, GRB.MINIMIZE)`.
6.  **Add Constraints**:
    * Loop through scenarios `ω` and time periods `t` to add all the operational constraints.
    * Add the first-stage investment constraints.
7.  **Optimize**: `m.optimize()`
8.  **Analyze Results**: Query the optimal values of the variables (`v_cap.X`, `v_gen[i,t,ω].X`) to understand the optimal system design and operational strategy.

