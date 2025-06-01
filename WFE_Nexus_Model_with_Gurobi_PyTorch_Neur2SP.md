# Template: Hybrid WFE Nexus Model (Gurobi + PyTorch/Neur2SP Approach)
## 1. Introduction & Motivation

This document provides a complete template for a **hybrid modeling approach** to solve the WFE nexus problem, combining Gurobi for optimization with PyTorch for machine learning. This method is inspired by advanced techniques like Neur2SP and is most suitable when the two-stage stochastic program becomes too large or complex to be solved as a single deterministic equivalent.

**When to use this approach:**
* **High-Dimensional Uncertainty**: You have a very large number of scenarios (e.g., thousands), making the deterministic equivalent model too large for memory or too slow to solve.
* **Complex Second Stage**: The operational (second-stage) problem has difficult non-linearities or combinatorial complexities that make its repeated evaluation within a traditional decomposition algorithm intractable.

The core idea is to **replace the explicit second-stage problem with a trained neural network that acts as a surrogate**, predicting the expected operational cost based on the first-stage investment decisions.

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
## 3. Two-Phase Hybrid Workflow

### **Phase 1: Training the Surrogate Model (PyTorch)**

The goal is to train a neural network `NN(x)` that approximates the expected second-stage cost function, `E[Q(x,ω)]`, where `x` is the vector of first-stage investment decisions (capacities `v_cap[i]`).

**A. Data Generation**
1.  **Sample Investment Vectors**: Generate `N` diverse samples of the first-stage investment vector `x_n = (v_cap[1], v_cap[2], ...)` from a reasonable distribution (e.g., Latin Hypercube Sampling).
2.  **Solve the Second-Stage Problem**: For each sample `x_n`, solve the operational (second-stage) problem to find the optimal operational cost. This must be done for a representative set of scenarios `ω`.
    * `Q(x_n, ω) = min {Operational cost for scenario ω given investments x_n}`
3.  **Calculate Expected Cost**: For each `x_n`, calculate the expected operational cost:
    * `y_n = E[Q(x_n, ω)] = sum(p_prob[ω] * Q(x_n, ω) for ω in Ω)`
4.  **Create Dataset**: Your training dataset is `(X, Y)` where `X = {x_1, ..., x_N}` and `Y = {y_1, ..., y_N}`.

**B. Neural Network Architecture (PyTorch)**
A simple feed-forward neural network with ReLU activation functions is recommended, as it can be perfectly represented by MIP constraints.

```python
import torch
import torch.nn as nn

class SurrogateNet(nn.Module):
    def __init__(self, input_size, hidden_size1, hidden_size2, output_size):
        super(SurrogateNet, self).__init__()
        self.layer1 = nn.Linear(input_size, hidden_size1)
        self.relu1 = nn.ReLU()
        self.layer2 = nn.Linear(hidden_size1, hidden_size2)
        self.relu2 = nn.ReLU()
        self.output_layer = nn.Linear(hidden_size2, output_size)

    def forward(self, x):
        out = self.layer1(x)
        out = self.relu1(out)
        out = self.layer2(out)
        out = self.relu2(out)
        out = self.output_layer(out)
        return out
```

**C. Training**
1.  Define a loss function (e.g., Mean Squared Error): `loss_fn = nn.MSELoss()`
2.  Choose an optimizer (e.g., Adam): `optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)`
3.  Train the model on the `(X, Y)` dataset for a number of epochs, minimizing the loss.
4.  Save the trained model's state dictionary: `torch.save(model.state_dict(), 'surrogate_net.pth')`

### **Phase 2: Solving the Master Investment Problem (Gurobi)**

Now, we formulate the first-stage problem in Gurobi and embed the trained neural network.

**A. Parameters & Variables**
* Only **first-stage** parameters and variables are needed for the master problem.
* **Parameters**: `p_CAPEX`, `p_OPEX_fix`, `p_CRF`, etc.
* **First-Stage Variables**: `v_cap[i]`, `v_build[i]`.
* **Additional Variable**: `v_predicted_op_cost` to hold the output of the neural network.

**B. Objective Function**
The objective is to minimize the total investment cost plus the *predicted* operational cost from the neural network.

`Minimize Z = InvestmentCost + v_predicted_op_cost`
* `InvestmentCost = sum( p_CRF[i] * p_CAPEX[i] * v_cap[i] for i in I ) + sum( v_cap[i] * p_OPEX_fix[i] for i)`

**C. Constraints**

1.  **Investment Constraints**
    * `v_cap[i] <= v_build[i] * M`
    * `v_cap[i] >= v_build[i] * p_min_capacity[i]`
    * `sum( p_CAPEX[i] * v_cap[i] for i in I ) <= p_Total_Budget`

2.  **Neural Network Constraint**
    This is the key step. Use a library like `gurobi-ml` to add the trained PyTorch model as a set of MIP constraints. This library translates the NN's structure (layers, weights, biases, ReLU activations) into equivalent linear constraints and binary variables that Gurobi can solve.

    `add_predictor_constr(gurobi_model, trained_pytorch_model, input_vars, output_vars)`
    * `gurobi_model`: Your `gp.Model` object.
    * `trained_pytorch_model`: The PyTorch model object loaded with trained weights.
    * `input_vars`: An ordered list of the Gurobi input variables, which are the capacities `v_cap[i]`.
    * `output_vars`: The Gurobi output variable, `v_predicted_op_cost`.

***
## 4. Gurobi + PyTorch Implementation Guide

**File Structure:**
* `generate_data.py`: A script to run Phase 1.A (Data Generation).
* `train_surrogate.py`: A script for Phase 1.B and 1.C (NN definition and training).
* `solve_master.py`: The main script for Phase 2 (Solving the master problem).

**`solve_master.py` - High-Level Code Structure:**

```python
import gurobipy as gp
from gurobipy import GRB
import torch
from gurobi_ml import add_predictor_constr

# --- 1. Load Data & Trained Model ---
# Load first-stage parameters (CAPEX, OPEX, etc.)
# ...

# Instantiate the NN architecture and load the trained weights
input_size = len(all_technologies)
trained_nn = SurrogateNet(input_size, 64, 32, 1) # Must match training architecture
trained_nn.load_state_dict(torch.load('surrogate_net.pth'))

# --- 2. Create Gurobi Master Model ---
master_model = gp.Model("WFE_Hybrid_Master")

# --- 3. Define First-Stage Investment Variables ---
v_cap = master_model.addVars(techs, name="Capacity", lb=0.0)
v_build = master_model.addVars(techs, vtype=GRB.BINARY, name="Build")
# ...

# --- 4. Add the NN as a "Black-Box" Constraint ---
# Gurobi needs an ordered list of input variables for the NN
nn_input_vars = [v_cap[i] for i in techs_in_order] 
# And a variable to hold the NN's output
predicted_op_cost = master_model.addVar(name="predicted_op_cost", lb=-GRB.INFINITY)

# This function builds all the MIP constraints that represent the NN
add_predictor_constr(master_model, trained_nn, nn_input_vars, predicted_op_cost)

# --- 5. Define the Full Master Objective Function ---
# Use the same cost expressions from the Gurobi-only file
investment_cost = gp.quicksum(p_CRF[i] * p_CAPEX[i] * v_cap[i] for i in techs)
fixed_opex_cost = gp.quicksum(v_cap[i] * p_OPEX_fix[i] for i in techs)

total_cost = investment_cost + fixed_opex_cost + predicted_op_cost
master_model.setObjective(total_cost, GRB.MINIMIZE)

# --- 6. Add other first-stage constraints ---
# e.g., budget limits, linking v_cap to v_build
for i in techs:
    master_model.addConstr(v_cap[i] <= p_max_capacity[i] * v_build[i])

# --- 7. Optimize and Analyze ---
master_model.optimize()
# Query results for v_cap.X
```