# Optimal Design and Operation of an Integrated Wastewater-Energy-Resource Network under Uncertainty: A Two-Stage Stochastic Programming Approach for Çorlu, Türkiye

## I. Introduction

### A. Background: The Imperative for Integrated Urban Resource Management

Urban environments worldwide are experiencing unprecedented pressures stemming from rapid population growth, escalating resource consumption, and the pervasive impacts of climate change. These challenges necessitate a paradigm shift in how cities manage their essential resources, moving away from siloed approaches towards integrated and sustainable systems. The Water-Food-Energy (WFE) nexus has emerged as a critical conceptual framework for understanding the complex interdependencies between these vital sectors. Effective WFE nexus management aims to enhance resource use efficiency, minimize environmental degradation, and foster resilience, thereby contributing to the achievement of overarching sustainable development goals.

A significant contributor to urban environmental stress is the substantial carbon footprint associated with energy consumption, waste management, and industrial activities. Consequently, the decarbonization of urban systems is a paramount objective. The complexities inherent in decarbonizing energy-intensive sectors, such as the oil refining industry which is actively exploring strategies like green hydrogen, carbon capture, and process electrification¹, mirror the challenges faced in transforming urban metabolisms. The transition towards sustainable urban systems is thus not merely a matter of adopting individual advanced technologies but requires a systemic integration that acknowledges and leverages the interconnections between water, food, and energy pathways.

Current urban planning and management practices often treat these sectors in isolation. However, their profound interlinkages—such as the energy required for water and wastewater treatment, water needed for energy generation and agricultural irrigation, and energy consumed in food processing and distribution—imply that optimizing one sector independently can lead to unintended negative consequences or missed opportunities in others. The WFE nexus framework compels a holistic perspective, promoting solutions that optimize the overall system performance rather than individual components.

### B. Specific Context: Wastewater as a Nexus Hub in Çorlu, Türkiye

This study focuses on the region of Çorlu, Türkiye, an area characterized by significant urban and industrial activity, making it a pertinent case for exploring innovative resource management strategies. Within this context, wastewater treatment plants (WWTPs) are traditionally viewed primarily as sanitation infrastructure, responsible for mitigating water pollution. However, a paradigm shift is underway, repositioning WWTPs as potential resource recovery facilities capable of generating energy, reclaiming clean water, and extracting valuable nutrients.

An initial, relatively small-scale wastewater energy network model has been implemented for Çorlu, primarily focusing on cost minimization through the integration of wind turbines and photovoltaic solar panels, with interconnections and capital expenditure considerations for energy storage systems using electricity, or energy carriers like ammonia, ethanol, and biodiesel. This existing model, while a foundational step, possesses limitations in its scope and its deterministic approach to what is an inherently uncertain operational environment.

The vision for an expanded system involves transforming WWTPs from net energy consumers into energy-neutral or even energy-positive entities, and concurrently, into sources of valuable materials that can be reintegrated into the urban or regional economy. The organic content within wastewater, for instance, represents a significant source of chemical energy that can be converted into biogas. Furthermore, thermal energy can be recovered from wastewater streams, and the treated effluent itself constitutes a reusable water resource. Nutrients such as nitrogen and phosphorus, if recovered, can serve as valuable inputs for agricultural applications.

By systematically exploring and implementing these recovery pathways, the WWTP can evolve into a central node within a circular economy model, deeply embedded in the local WFE nexus and fundamentally altering its contribution to the urban metabolism. This aligns with broader industrial sustainability trends that emphasize waste valorization and process integration, similar to the decarbonization efforts observed in sectors like refining where by-products and waste streams are increasingly viewed as resources.¹

### C. Research Gap and Problem Statement

Despite the growing recognition of the WFE nexus and the potential of WWTPs as resource hubs, a significant research gap exists concerning comprehensive optimization models that address the complexities of such integrated systems under uncertainty. Specifically, there is a scarcity of stochastic optimization frameworks designed to guide the design and operational planning of systems that cohesively integrate wastewater management with advanced energy solutions—including hydrogen (H₂) and nitrogen (N₂) cycles, a diverse portfolio of energy carriers, and explicit WFE nexus considerations—at an urban or regional scale.

Many existing energy system models are deterministic, which may not adequately capture the implications of fluctuating renewable energy supplies or market prices for long-term investment robustness.¹ While some stochastic models exist for energy systems, such as those for multi-energy microgrids¹, they often do not encompass the full breadth of WFE interlinkages, particularly the detailed integration of wastewater processing and resource recovery with emerging H₂/N₂ economies.

The inherent variability of renewable energy sources (e.g., wind and solar), the volatility of energy and carbon market prices, and fluctuating demands for recovered resources necessitate a modeling approach that can explicitly account for these uncertainties to support robust decision-making. The current research aims to address this gap by developing a sophisticated two-stage stochastic programming model. The substantial increase in complexity and scope compared to the initial Çorlu model warrants a fresh implementation, allowing for a more comprehensive and integrated system representation.

The novelty of this work is therefore situated in the synergistic combination of a stochastic optimization approach, the extensive range of integrated cycles (wastewater treatment, energy generation and storage, hydrogen and nitrogen pathways, and nutrient recovery linking to food systems), and its application to a real-world urban-industrial setting like Çorlu.

### D. Objectives and Contributions of the Study

The primary objective of this research is to develop and apply a two-stage stochastic optimization model to determine the most economically efficient (e.g., minimum total annualized cost) or environmentally optimal (e.g., minimum CO₂ emissions) configuration and operational strategy for an integrated wastewater-energy-resource network in Çorlu, Türkiye.

Secondary objectives include:

- Evaluating the technical role and economic viability of incorporating hydrogen and nitrogen cycles (e.g., production and use of green hydrogen, ammonia as an energy carrier or chemical feedstock) within the proposed integrated network.
- Analyzing the impact of different carbon dioxide emission policies, such as carbon taxes or emission constraints, on the optimal system design and operational dispatch.
- Quantifying the systemic benefits derived from WFE nexus integration, including enhanced resource recovery efficiencies, reduced reliance on external resource inputs, and minimized environmental discharges.

The anticipated contributions of this study are threefold:

1. **Methodological:** The development of a novel, comprehensive two-stage stochastic optimization model tailored for integrated urban wastewater-energy-resource systems, incorporating a wide array of technologies and their interconnections.

2. **Practical:** The generation of specific insights and decision-support for the sustainable development of Çorlu, offering potential pathways for resource management and infrastructure investment.

3. **Policy-Relevant:** An assessment of the effectiveness of different environmental policy instruments in steering the transition towards more sustainable and decarbonized urban systems.

## II. System Definition and Technology Superstructure

### A. Overview of the Integrated Wastewater-Energy-Resource Network for Çorlu

The proposed system for Çorlu envisions a highly integrated network where wastewater treatment facilities act as central nexuses for resource recovery and energy transformation. The superstructure encompasses various interconnected subsystems, including wastewater treatment and valorization units, renewable and conventional energy generation technologies, hydrogen and nitrogen cycle components, diverse energy carrier production and storage options, and pathways for carbon capture and utilization.

Material and energy flows are tracked throughout the system, from resource input and conversion to final end-use or export. The system boundaries are defined to include the key WWTPs in the Çorlu region, local renewable energy resources, potential interactions with external energy grids (electricity, natural gas), and local demands for energy, water, and recovered products (e.g., fertilizers).

A conceptual diagram of this superstructure would illustrate the potential pathways for transforming wastewater into valuable outputs like biogas, reclaimed water, and nutrients, and integrating these with energy technologies such as wind turbines, PV panels, electrolyzers for hydrogen production, and ammonia synthesis units.

### B. Detailed Description of Considered Technologies and Pathways

The integrated network model considers a comprehensive suite of technologies, each characterized by specific technical, economic, and environmental parameters.

#### 1. Wastewater Treatment and Resource Recovery

The core of the system involves advanced wastewater treatment processes with a strong emphasis on resource recovery. Beyond conventional pollutant removal, technologies considered include:

**Anaerobic Digestion (AD):** For the stabilization of sewage sludge and concentrated organic wastewater streams, producing biogas (a mixture primarily of methane (CH₄) and carbon dioxide (CO₂)).

**Biogas Utilization:**

- **Combined Heat and Power (CHP):** Direct combustion of biogas in CHP units to generate electricity and heat for on-site use or export.
- **Biomethane Upgrading:** Removal of CO₂ and other impurities from biogas to produce high-purity biomethane, which can be injected into the natural gas grid, used as a vehicle fuel, or serve as a feedstock for steam methane reforming (SMR) to produce hydrogen. The CO₂ separated during upgrading is a relatively pure stream that could be captured for utilization (e.g., in Power-to-Gas systems) or sequestration. This potential for CO₂ capture from biogas is an important consideration, as Power-to-Gas (P2G) systems, which can convert CO₂ and hydrogen to synthetic natural gas (SNG), are increasingly being explored.¹

**Nutrient Recovery:** Technologies to recover nitrogen (N) and phosphorus (P) from wastewater or sludge, such as struvite precipitation or ammonia stripping. Recovered nutrients can be processed into fertilizers, creating a direct link to the "Food" component of the WFE nexus and contributing to the nitrogen cycle.

**Water Reclamation and Reuse:** Advanced treatment processes (e.g., membrane filtration, disinfection) to produce reclaimed water suitable for various non-potable uses, such as industrial processes, agricultural irrigation, or urban landscaping, thereby reducing freshwater demand.

**Wastewater Heat Recovery:** Utilization of heat exchangers or heat pumps to extract thermal energy from wastewater effluent, which can be used for space heating or other low-temperature heat demands.

#### 2. Energy Generation

Primary energy generation focuses on renewable sources, supplemented by existing or potential conventional options if economically or operationally justified.

**Wind Turbines (WT):** Modeled based on site-specific wind resource data for Çorlu. Key parameters include investment cost ($/kW), operation and maintenance (O&M) costs, power curve characteristics, and a very low lifecycle CO₂ emission factor. Detailed models for wind turbine power output often consider rotor diameter and hub height.¹ While optimizing these design parameters within the larger system model adds complexity, particularly if it leads to a Mixed-Integer Nonlinear Program (MINLP), standard available turbine sizes and configurations might be assumed to maintain a Mixed-Integer Linear Program (MILP) structure for tractability in a large-scale WFE network model.

**Photovoltaic (PV) Panels:** Modeled based on solar irradiance data for Çorlu. Parameters include investment cost ($/kW), O&M costs, cell efficiency (which can depend on material type, solar irradiance, and ambient temperature), and potentially the optimization of tilt angles. Lifecycle CO₂ emissions are also very low. Similar to wind turbines, detailed PV cell efficiency and tilt angle optimization equations¹ can be incorporated if an MINLP formulation is pursued, or simplified for a MILP approach by using average efficiencies for fixed configurations.

#### 3. Hydrogen (H₂) Cycle

Hydrogen is considered a key energy vector for decarbonization and energy storage.

**Production:**

- **Green H₂:** Produced via electrolysis of water using renewable electricity. Both Alkaline Electrolyzers (AE) and Proton Exchange Membrane Electrolyzers (PEME) are considered candidate technologies.¹ Essential parameters are CAPEX ($/kW), OPEX ($/kg H₂ or $/kWh), electrical efficiency (kWh/kg H₂), and operational flexibility (e.g., ramp rates, part-load performance).

- **Blue H₂ (Optional):** If natural gas infrastructure is readily available and economically competitive in Çorlu, and if carbon capture is feasible, SMR of natural gas or upgraded biogas could be an option. This pathway requires coupling SMR units with Carbon Capture (CC) technology to capture the CO₂ produced.¹ Parameters include feedstock consumption (NG or biomethane per kg H₂), H₂ yield, CO₂ production and capture rate, and thermal energy demand/production. The economic trade-off between green H₂ (driven by renewable electricity costs) and blue H₂ (driven by gas prices and CCS costs) is a critical evaluation point. Studies on refinery decarbonization suggest that natural gas with carbon capture can be more economically favorable than electricity-based options unless electricity prices are significantly low or carbon emission regulations are very stringent.¹ This economic dynamic is directly relevant to the choice of hydrogen production pathway.

**Storage:** Options include pressurized gas storage (most common for on-site), and potentially liquid hydrogen or Liquid Organic Hydrogen Carriers (LOHCs) if long-duration or large-volume storage is a strategic requirement, though these are generally more complex and costly for localized systems.

**Utilization:**

- Direct use as a fuel in modified gas turbines or boilers for heat/power generation, or in fuel cells for high-efficiency electricity generation.
- Feedstock for ammonia (NH₃) synthesis, linking to the nitrogen cycle.
- Feedstock for P2G systems, where H₂ is reacted with CO₂ (e.g., from biogas upgrading or industrial capture) to produce SNG via methanation.¹
- Potential use in upgrading biofuels like ethanol or biodiesel, if these are produced locally.

#### 4. Nitrogen (N₂) Cycle / Ammonia (NH₃)

Ammonia is considered as a versatile energy carrier and chemical.

**Production:** Synthesized via the Haber-Bosch process, reacting hydrogen (preferably green or blue H₂) with nitrogen extracted from air (via an Air Separation Unit, ASU). Key parameters are energy consumption (primarily for H₂ production and N₂ separation/compression), H₂ demand per ton of NH₃, and the CAPEX/OPEX of the Haber-Bosch unit and ASU.

**Storage:** Typically stored as a liquid under moderate pressure or refrigeration.

**Utilization:**

- **Energy Carrier:** Ammonia can be combusted directly in modified turbines or internal combustion engines, or used in solid oxide fuel cells (SOFCs) or direct ammonia fuel cells.
- **H₂ Carrier:** Ammonia can be "cracked" back into hydrogen and nitrogen at the point of use, offering a denser and easier-to-transport alternative to pure hydrogen.
- **Chemical Feedstock / Fertilizer:** Ammonia is a primary component of many fertilizers. Integrating synthesized ammonia with nutrients (N, P) recovered from the WWTP could create enhanced local fertilizer products, strongly linking the energy system to agricultural productivity within the WFE nexus. This pathway offers a route to valorize both synthesized ammonia and recovered wastewater nutrients.

#### 5. Other Energy Carriers

To diversify energy options and leverage local resources, other carriers are considered:

**Ethanol/Biodiesel:**

- **Production:** Pathways could involve fermentation of sugars (from specific organic waste streams or energy crops, if sustainably available in the Çorlu region) for bioethanol, or transesterification of lipids/oils (from WWTP sludge if lipid content is high, microalgae cultivation using wastewater nutrients, or other local oilseed/waste oil sources) for biodiesel. The feasibility of these pathways is highly dependent on the consistent availability and cost-effectiveness of suitable feedstocks at a scale relevant to Çorlu.
- **Parameters:** Feedstock requirements, conversion efficiencies, CAPEX/OPEX of conversion plants, co-product generation (e.g., glycerol from biodiesel production).
- **Utilization:** As transport fuels (pure or blended), or for local stationary energy generation.

#### 6. Energy Storage Systems

Energy storage is crucial for balancing intermittent renewable generation with demand.

**Batteries:** Lithium-ion batteries are commonly considered for short-duration electricity storage, providing services like peak shaving, load leveling, and grid stabilization.¹ Parameters include CAPEX ($/kWh or $/kW), OPEX, round-trip efficiency, cycle life, and depth of discharge limitations.

**Thermal Storage:** If significant fluctuating thermal loads or supplies exist (e.g., from solar thermal collectors, industrial waste heat recovery, or if a district heating/cooling network is part of the system), sensible or latent heat storage technologies could be included.

**Hydrogen/Ammonia Storage:** As detailed in their respective sections, these chemical energy carriers also serve as medium-to-long-term energy storage options.

#### 7. Carbon Capture, Utilization, and Storage (CCUS)

CCUS technologies are vital for mitigating CO₂ emissions from any remaining fossil fuel use or from biogenic sources where CO₂ is a byproduct.

**Capture Technologies:**

- **Post-combustion Capture:** Typically applied to flue gases from combustion processes (e.g., biogas-fired or natural gas-fired CHPs, SMR units if blue H₂ is produced without integrated pre-combustion capture). Solvent-based absorption using amines like Monoethanolamine (MEA) is a mature technology for this purpose.¹ It's important to note that post-combustion CCS may be most feasible for large point sources and might not capture 100% of emissions, potentially leaving around 30% unaddressed, which is a critical factor for achieving deep decarbonization targets.¹

- **Pre-combustion Capture:** Relevant for processes where CO₂ can be removed before combustion, such as in SMR where CO₂ is separated from the shifted syngas (H₂ and CO₂ mixture), or in integrated gasification combined cycle (IGCC) plants. This method often results in a more concentrated CO₂ stream, potentially lowering capture costs.¹

**CO₂ Utilization (CCU):**

- **Methanation (P2G):** Reaction of captured CO₂ with green or blue hydrogen to produce SNG. This is a prominent CCU pathway, effectively recycling carbon and producing a dispatchable fuel.¹
- Other chemical conversions (e.g., production of urea, polymers, or other chemicals) could be considered if there are local demands or economic drivers in Çorlu, though these are often more niche.

**CO₂ Storage (CCS):** If captured CO₂ is not utilized, permanent geological storage is the alternative. The feasibility of this depends entirely on the availability of suitable geological formations near Çorlu, which may be a significant constraint. If storage is not an option, then utilization becomes the only route for captured CO₂. The costs associated with CO₂ capture, transport (if needed), and storage/utilization are critical parameters, with literature suggesting decarbonization costs ranging from $113/ton to $477/ton CO₂ for some industrial applications, heavily influenced by factors like feedstock costs for bio-options or CCS infrastructure.¹

#### 8. Interconnections

The integrated system will interact with broader energy networks:

- **Electricity Grid:** Enabling the purchase of electricity during deficits and the sale of surplus electricity generated within the system.
- **Natural Gas Grid:** If SNG is produced via P2G, it could be injected into the existing gas grid. Conversely, natural gas might be drawn from the grid if it's used as a feedstock (e.g., for blue H₂) or fuel.
- **Heat Network (District Heating/Cooling):** If a centralized district energy system exists or is planned for Çorlu, the integrated network could supply or draw thermal energy.

To effectively model this complex superstructure, a comprehensive database of techno-economic and environmental parameters for each technology is essential. Table 1 outlines the key data categories required.

**Table 1: Illustrative Techno-economic and Environmental Parameters of Technologies**

| Parameter Category | Examples | Units | Potential Data Sources |
|:---|:---|:---|:---|
| **Capital Costs (CAPEX)** | Investment cost per unit of capacity | $/kW, $/kg/h, $/m³, etc. | Literature¹, vendor quotes, engineering estimates |
| **Operating Costs (OPEX)** | Fixed annual costs, Variable costs per unit of production/input | $/year, $/kWh, $/kg, etc. | Literature¹, supplier data |
| **Efficiency** | Energy conversion, mass conversion, capture rate | %, dimensionless | Technical specifications, literature |
| **Lifetime** | Operational lifespan before major overhaul or replacement | years | Manufacturer data, literature |
| **Input/Output Coefficients** | Feedstock per unit product, energy per unit product | kg/kg, kWh/kg, MJ/kWh, etc. | Stoichiometry, process simulations, literature |
| **CO₂ Emission Factor** | Direct emissions, lifecycle emissions (if available) | kg CO₂/kWh, kg CO₂/kg product | Emission databases, lifecycle assessment studies |
| **Operational Parameters** | Ramp rates, min/max load levels, start-up/shut-down times | %/min, MW, hours | Technical specifications, literature |

This table, when fully populated with reliable and, where possible, localized data for Çorlu, will form the bedrock of the optimization model, directly influencing the objective function coefficients and constraint definitions. The accuracy and transparency of these parameters are paramount for the credibility and reproducibility of the research findings.

## III. Two-Stage Stochastic Optimization Model Formulation

### A. General Framework and Mathematical Notation

The problem of determining the optimal design and operation of the integrated wastewater-energy-resource network under uncertainty is formulated as a two-stage stochastic program (2SP). In this framework, first-stage decisions, typically related to design and investment, are made "here-and-now" before the realization of uncertain parameters. Second-stage decisions, related to system operation, are "wait-and-see" or recourse actions, made after the uncertainties for a particular scenario unfold, adapting operations to the prevailing conditions given the committed first-stage investments.

The general form of a 2SP can be expressed as¹:

$$\text{Minimize } Z = c^T x + E_\omega[Q(x,\omega)]$$

Subject to:

$$Ax \leq b \quad \text{(First-stage constraints)}$$
$$x \geq 0$$

Where $Q(x,\omega)$ is the optimal value of the second-stage problem for a given first-stage decision $x$ and realization of uncertain parameters $\omega$:

$$Q(x,\omega) = \min q(\omega)^T y(\omega)$$

Subject to:

$$T(\omega)x + W(\omega)y(\omega) \leq h(\omega) \quad \text{(Second-stage constraints linking first and second stage)}$$
$$y(\omega) \geq 0$$

**Notation:**

**Sets:**
- $i \in I$: Set of technologies or processes.
- $t \in T$: Set of time periods in the operational horizon (e.g., hours, days, seasons).
- $\omega \in \Omega$: Set of scenarios, each representing a possible realization of uncertain parameters with probability $p_\omega$.
- $r \in R$: Set of resources (e.g., electricity, water, H₂, NH₃, CO₂).

**Parameters:**
- $c$: Vector of first-stage investment costs.
- $A,b$: Matrices and vectors defining first-stage constraints.
- $q(\omega)$: Vector of second-stage operational costs under scenario $\omega$.
- $T(\omega), W(\omega), h(\omega)$: Matrices and vectors defining second-stage constraints under scenario $\omega$.
- Techno-economic parameters (CAPEX, OPEX, efficiencies, etc.) for each technology $i$, as detailed in Table 1.

**Decision Variables:**

**First-Stage (Here-and-Now):**
- $x_i$: Investment decision for technology $i$ (e.g., binary for selection, continuous for capacity).

**Second-Stage (Wait-and-See, scenario-dependent $\forall \omega \in \Omega, \forall t \in T$):**
- $y_{i,t,\omega}$: Operational level of technology $i$ at time $t$ under scenario $\omega$.
- $f_{r,t,\omega}$: Flow rate of resource $r$ at time $t$ under scenario $\omega$.
- $s_{st,t,\omega}$: State of charge/level of storage unit $st$ at time $t$ under scenario $\omega$.

The choice between formulating the model as a Mixed-Integer Linear Program (MILP) or a Mixed-Integer Nonlinear Program (MINLP) depends on the nature of the relationships within the system. If key aspects such as technology efficiencies, part-load performance, or reaction kinetics (e.g., for P2G systems¹) are inherently nonlinear and crucial for accurate representation, an MINLP formulation would be appropriate. However, MINLPs are generally more computationally challenging to solve, especially for large-scale stochastic problems. Many large energy system models opt for MILP formulations, potentially using piecewise linear approximations for nonlinearities.¹ Given the anticipated complexity of the integrated WFE network, an initial MILP formulation is advisable, with nonlinearities introduced selectively if deemed essential and computationally feasible.

### B. Uncertainty Modeling and Scenario Generation

The accurate representation of uncertainty is fundamental to stochastic programming.

**Identification of Stochastic Parameters:**

Key parameters subject to uncertainty in this system include:

- **Renewable Energy Availability:** Hourly or daily profiles of solar irradiance and wind speed, directly impacting PV and wind turbine output.
- **Energy Prices:** Market prices for purchasing electricity from the grid or selling surplus electricity. Prices for natural gas if it is used as a feedstock (e.g., for blue H₂) or if SNG is produced and sold to the grid.
- **CO₂ Price/Tax:** The cost associated with CO₂ emissions, either as a direct tax or the market price of CO₂ allowances in an emissions trading system.¹
- **Demands:** Fluctuations in demand for electricity, heat (if applicable), reclaimed water, and potentially for recovered products like fertilizers or SNG.
- **Policy Parameters:** As demonstrated in some studies¹, parameters like the carbon emission trading (CET) price or the mandated CO₂ emission limits themselves can be treated as uncertain over a long-term planning horizon, reflecting evolving regulatory landscapes.

**Scenario Generation Method:**

To represent these uncertainties, a finite set of discrete scenarios ($\Omega$) is typically generated. Common methods include:

- **Sampling from Probability Distributions:** If historical data or expert knowledge allows for the characterization of uncertainties using probability distributions (e.g., Weibull for wind speed, Beta for solar irradiance, Normal or Lognormal for prices), Monte Carlo sampling can be used to generate a large number of scenarios. These are often then reduced to a smaller, computationally manageable set using scenario reduction techniques (e.g., k-means clustering, Kantorovich distance minimization).

- **Historical Data Analysis:** Direct use of historical time series for renewable availability and demands, possibly clustered into representative days or periods.

- **Discretization of Distributions:** Approximating continuous probability distributions with a few discrete points and associated probabilities.

Consideration should also be given to correlations between uncertain parameters (e.g., solar irradiance and ambient temperature, which affects PV efficiency; or wind speed and electricity prices in some markets). The number of scenarios ($K = |\Omega|$) involves a trade-off: more scenarios provide a better approximation of the underlying uncertainty but significantly increase the computational burden of solving the 2SP, as solving the extensive form can become intractable with a large number of variables and constraints.¹

A sophisticated approach to modeling long-term policy uncertainty involves defining scenarios based on different future trajectories of policy instruments.¹ For instance, scenarios could represent different levels of carbon tax escalation or tightening of emission caps over the planning horizon (e.g., a 20-year period). This allows the model to assess the robustness of investment decisions against varying degrees of future policy stringency, which is highly relevant for a long-lived infrastructure project.

### C. First-Stage Decisions (Here-and-Now)

First-stage decisions are made before the specific realization of any scenario's uncertain parameters. These typically include:

- **Investment in New Technologies:** Binary variables ($b_i \in \{0,1\}$) indicating whether to install technology $i$.
- **Sizing of Units:** Continuous variables ($Cap_i$) representing the installed capacity of selected technologies (e.g., MW for power plants, MWh for storage, kg/h for chemical plants).
- **Network Infrastructure Decisions:** Investments in pipelines, transmission lines, or other fixed infrastructure, if these are decision variables rather than fixed assumptions.

These decisions define the physical configuration of the system for its entire operational lifetime.

### D. Second-Stage Decisions (Wait-and-See / Recourse Actions)

Second-stage decisions are operational choices made for each specific scenario $\omega$ and each time period $t$ within that scenario, given the first-stage investment decisions. They represent how the system is operated to meet demands and optimize the objective function under the conditions of that particular scenario. These include:

- **Production/Consumption Levels:** Operational output or input of each installed technology unit (e.g., $P_{i,t,\omega}$ for power generation).
- **Flow Rates:** Movement of all resources (electricity, water, H₂, NH₃, biogas, CO₂, etc.) between units and with external systems.
- **Energy Dispatch:** Allocation of generation to meet demands.
- **Storage Operation:** Charging and discharging rates for all storage units ($P_{ch,st,t,\omega}$, $P_{dis,st,t,\omega}$), and their state of charge ($SOC_{st,t,\omega}$).
- **Grid Interactions:** Amount of electricity or gas purchased from or sold to external grids.
- **CO₂ Management:** Amount of CO₂ captured by CCUS units, utilized in processes like P2G, or emitted to the atmosphere.

The complexity of the second-stage problem, particularly if it involves numerous scenarios with integer variables (e.g., unit commitment) or nonlinearities, can make the overall 2SP computationally challenging. Advanced solution techniques, such as training a neural network to approximate the expected second-stage objective function (as in the Neur2SP approach¹), can be employed if the traditional extensive form becomes intractable. This surrogate model, if using MIP-representable activation functions like ReLU, can then be embedded into a more manageable first-stage optimization problem. While the initial model for Çorlu is small, the planned expansion could lead to such computational hurdles, making these advanced methods relevant for future consideration.

### E. Objective Function(s)

The choice of objective function directs the optimization towards specific goals.

**Primary Objective: Minimization of Total Expected Annualized Cost (TAC)**

The most common objective is to minimize the sum of annualized first-stage investment costs and the expected value of second-stage net operational costs over all scenarios:

$$TAC = \sum_{i \in I} AnnFactor \cdot CAPEX_i \cdot x_i + \sum_{\omega \in \Omega} p_\omega \left(\sum_{t \in T} (OpCosts_{t,\omega} - Revenues_{t,\omega})\right)$$

Where:

- $AnnFactor$: Capital recovery factor to annualize investment costs.
- $CAPEX_i$: Total capital expenditure for technology $i$ if selected ($x_i$ represents capacity or a binary selection variable).¹
- $p_\omega$: Probability of scenario $\omega$.
- $OpCosts_{t,\omega}$: Sum of all operational costs in period $t$ of scenario $\omega$, including fuel, electricity purchases, variable O&M for all units, and any CO₂ taxes or costs for purchasing emission allowances.¹
- $Revenues_{t,\omega}$: Sum of all revenues in period $t$ of scenario $\omega$, from selling electricity, SNG, ammonia, recovered water, fertilizers, or other valuable byproducts.¹

**Alternative 1: Minimization of Total Expected CO₂ Emissions**

This objective focuses purely on environmental performance:

$$\text{Minimize } TotalCO_2 = \sum_{\omega \in \Omega} p_\omega \left(\sum_{t \in T} Emissions_{t,\omega}\right)$$

Where $Emissions_{t,\omega}$ are the total CO₂ emissions in period $t$ of scenario $\omega$.

**Alternative 2: Minimize TAC with a Constraint on Total Expected CO₂ Emissions**

This approach allows for exploring the economic implications of achieving specific environmental targets:

$$\text{Minimize } TAC$$

Subject to: $\text{Total Expected CO₂ Emissions} \leq CO_2Cap$

This is a common strategy in energy system modeling to analyze the trade-off between economic cost and environmental impact.¹ By varying $CO_2Cap$, a Pareto frontier can be generated.

The selection of the objective function fundamentally shapes the model's outcomes. A purely cost-driven optimization might favor more polluting technologies if they are cheaper, unless carbon pricing mechanisms (taxes or cap-and-trade) effectively internalize the environmental cost of CO₂ emissions. Explicitly minimizing CO₂ or imposing emission constraints enables the exploration of decarbonization pathways that might entail higher initial investments or operational costs but deliver superior environmental performance.

### F. Key Constraints

The model is defined by a set of constraints that ensure physical laws, technological limitations, resource availability, and policy requirements are met. Illustrative examples include:

**Mass Balances:** For every resource $r$ (water, H₂, N₂, NH₃, CH₄, CO₂, biomass, etc.) at each process unit or node $j$, and in each time step $t$ for each scenario $\omega$:

$$\sum_{i \in In(j)} Flow_{i,j,r,t,\omega} + Production_{j,r,t,\omega} = \sum_{k \in Out(j)} Flow_{j,k,r,t,\omega} + Consumption_{j,r,t,\omega} + StorageChange_{j,r,t,\omega}$$

(Detailed mass balance equations for specific units like boilers, SMRs, CC units, and overall system balances are found in¹).

**Energy Balances:** Similar balances for different forms of energy (electricity, heat) at each relevant node and time step.

(Overall energy balance considering generation, consumption, demand, and storage is exemplified in¹).

**Technology-Specific Constraints:**

- **Capacity Limits:** The output of any technology unit $i$ cannot exceed its installed capacity ($Cap_i$) multiplied by its availability factor:
  
  $$Production_{i,t,\omega} \leq Cap_i \cdot Availability_{i,t,\omega}$$¹

- **Conversion Efficiencies:** Input-output relationships based on technology-specific efficiencies (e.g., kWh of electricity per kg of H₂ produced by an electrolyzer; kg of H₂ and N₂ per kg of NH₃ from Haber-Bosch). These can be linear or piecewise linear approximations of nonlinear curves.

- **Ramp Rate Limits:** Constraints on how quickly the output of a unit can change (if dynamic operations are modeled in detail).

- **Minimum/Maximum Operating Loads:** Many units cannot operate below a certain minimum load or above their design capacity.¹

- **Electrolyzer Model:** Relating electricity consumption to H₂ production rate based on efficiency.¹

- **SMR Model:** Relating natural gas or biogas feedstock input to H₂ output, considering steam requirements and CO₂ co-production.

- **Haber-Bosch Model:** Stoichiometric requirements for H₂ and N₂ to produce NH₃, and associated energy consumption.

- **P2G (Methanation) Model:** Stoichiometric consumption of H₂ and CO₂ to produce CH₄ and H₂O. If an MINLP is used, thermodynamic equilibrium constraints can be included.¹ For MILP, a fixed conversion efficiency might be assumed.

- **Carbon Capture Model:** Amount of CO₂ captured as a function of flue gas flow rate from the source unit and the capture efficiency of the CC technology.¹

- **Energy Storage Model:** Constraints governing charging/discharging power limits, state of charge evolution (accounting for efficiencies and self-discharge if significant), and minimum/maximum SOC levels.¹

**Resource Availability Constraints:** Limits on the availability of external resources such as freshwater intake, sustainably sourced biomass, or land for technology deployment.

**Demand Satisfaction Constraints:** All specified demands (electricity, heat, reclaimed water, fertilizers, SNG, etc.) must be met in each time period $t$ for every scenario $\omega$.

**CO₂ Emission Accounting and Policies:**

- **Total CO₂ Emissions:** Sum of emissions from all emitting sources (e.g., combustion of fossil fuels or biogas if CO₂ is not captured, process emissions).

- **Emission Constraint (if applicable):** Total CO₂ emissions in a given period (or annually) must be less than or equal to a specified emission cap ($CO_2Cap$).¹

- **Carbon Tax (if applicable):** An additional cost term in the objective function, calculated as $TaxRate \times TotalCO_2Emissions$.¹

- **Cap-and-Trade System (if applicable):** Costs incurred or revenues generated from buying or selling CO₂ emission allowances.¹

**Logical Constraints:** For example, a technology unit can only operate if the corresponding investment decision (first-stage) was made to build it.¹ Binary variables for unit on/off status (unit commitment) might be needed if start-up/shut-down costs and times are significant.

The precise mathematical formulation of these constraints will depend on the level of detail desired and the choice between MILP and MINLP. For instance, the operational cost function for conventional generators or the feasible operating region of CHP units can be highly nonlinear¹, requiring either direct MINLP modeling or careful linearization/approximation for MILP.

To ensure transparency and facilitate model validation, a clear definition of uncertain parameters and their scenario properties is crucial, as outlined in Table 2.

**Table 2: Definition of Uncertain Parameters and Scenario Properties**

| Category | Details | Example/Source Basis |
|:---|:---|:---|
| **List of Stochastic Parameters** | e.g., Hourly solar irradiance, hourly wind speed, electricity purchase price, electricity sale price, natural gas price, CO₂ tax/allowance price, key demands. | User-defined based on system sensitivity and data availability. |
| **Probability Distributions** | For each stochastic parameter: type of distribution (e.g., Normal, Lognormal, Weibull, Beta, Uniform, empirical), mean, standard deviation, min/max values. | Historical data analysis for Çorlu, literature for typical energy system parameters. |
| **Correlations** | Correlation matrix specifying dependencies between stochastic parameters (e.g., solar irradiance and ambient temperature). | Statistical analysis of historical data. |
| **Scenario Generation Method** | e.g., Monte Carlo sampling with k-means clustering for reduction; Latin Hypercube Sampling; specific discrete scenarios based on expert judgment or policy variations (as in¹ for CET price/CO₂ limits, or¹ using seasonal data combined with price/policy variations). | Chosen based on data availability and desired accuracy vs. computational effort. |
| **Final Scenario Set** | Number of scenarios ($K$) used in the optimization model, and the probability ($p_\omega$) assigned to each scenario $\omega$. | Balance between representation quality and solvability. |

This table documents the critical assumptions underpinning the stochastic analysis, defining the "uncertain future" against which the system's design and operational strategy are optimized.

## IV. Case Study: Çorlu, Türkiye

### A. Data Collection and Assumptions

The application of the proposed two-stage stochastic model to Çorlu, Türkiye, necessitates the collection of comprehensive local data and the establishment of clear assumptions.

**Wastewater System Data for Çorlu:**

- **Influent Characteristics:** Average and time-varying (e.g., seasonal, diurnal) flow rates of municipal and industrial wastewater entering the main WWTP(s). Key quality parameters such as Biochemical Oxygen Demand (BOD₅), Chemical Oxygen Demand (COD), Total Suspended Solids (TSS), and concentrations of nutrients like Total Nitrogen (TN) and Total Phosphorus (TP).

- **Existing WWTP Configuration:** Details of current treatment processes, their capacities, and operational performance (e.g., removal efficiencies, energy consumption per m³ treated).

- **Energy Consumption:** Historical energy (electricity, thermal) consumption data for the existing WWTP(s).

- **Sludge Management:** Current sludge production rates, characteristics (e.g., volatile solids content), and existing treatment and disposal/utilization methods (e.g., digestion, dewatering, landfilling, agricultural use).

**Demand Data for Çorlu:**

- **Electricity Demand:** Aggregated hourly or sub-hourly electricity demand profiles for the relevant industrial and residential sectors within the system boundary, considering seasonal and daily variations.

- **Heat Demand:** If district heating or direct supply of process heat to industries is considered, corresponding demand profiles are needed. This may be less defined than electricity demand and might require estimation based on building stock, industrial processes, and climate.

- **Water Demand (for Reclaimed Water):** Potential local demands for reclaimed water (e.g., from industries, agriculture for irrigation, urban non-potable uses), including quality requirements and seasonal patterns.

- **Demand for Recovered Products:** Market potential or internal system demand for products like biogas/biomethane, SNG, hydrogen, ammonia (e.g., as fuel, chemical feedstock), and recovered nutrients (e.g., as fertilizer for local agriculture).

**Renewable Resource Potential in Çorlu:**

- **Solar Irradiance:** Time series data (e.g., hourly Global Horizontal Irradiance - GHI, Diffuse Horizontal Irradiance - DHI) specific to the Çorlu region, obtainable from meteorological services, national renewable energy agencies, or satellite-derived databases (e.g., PVGIS, NASA POWER).

- **Wind Speed:** Time series data (e.g., hourly wind speed at standard anemometer height, typically 10m, and at potential turbine hub heights – e.g., 80m, 100m, 120m) for the Çorlu region. This data can be sourced from meteorological masts, wind atlases, or reanalysis datasets. Wind power density and Weibull distribution parameters are also valuable.

**Techno-economic Parameters (Localized for Türkiye/Çorlu):**

- **Technology Costs:** CAPEX and OPEX for all considered technologies (WWTP units, WT, PV, electrolyzers, SMR, Haber-Bosch, storage systems, CCUS units, etc.). While generic international cost data from literature¹ provides a baseline, these must be adjusted for local conditions in Türkiye, considering factors like import duties, local manufacturing capabilities, labor costs, land prices, and specific site preparation needs.

- **Utility Prices:** Current and projected prices for purchasing electricity from the grid, natural gas (if applicable), and any other externally sourced utilities. Tariffs for selling surplus electricity or SNG back to the respective grids.

- **Discount Rate:** An appropriate discount rate for calculating the Net Present Value (NPV) or annualized costs, reflecting the economic context and risk profile in Türkiye.

- **CO₂ Emission Factors:** Specific CO₂ emission factors for grid electricity in Türkiye (g CO₂/kWh), and for any fossil fuels used (e.g., natural gas, if applicable, kg CO₂/MJ or kg CO₂/m³).

**Policy and Regulatory Assumptions:**

- **Carbon Pricing:** Current or credibly projected carbon tax levels or CO₂ allowance prices relevant to Türkiye.

- **Renewable Energy Incentives:** Feed-in tariffs, subsidies, tax credits, or other support mechanisms for renewable energy generation or green hydrogen production in Türkiye.

- **Environmental Regulations:** Emission standards, water quality regulations for effluent discharge or reuse, and waste management policies.

The credibility and practical relevance of the case study findings will heavily depend on the quality, granularity, and local specificity of the collected data. Where precise local data is unavailable, assumptions must be clearly documented and justified, potentially supported by sensitivity analyses on critical parameters.

### B. Scenario Definitions for Stochastic Analysis

Building upon the uncertainty modeling framework (Section III.B), specific scenarios for the Çorlu case study will be defined to capture a representative range of plausible future conditions. These scenarios will be combinations of different realizations of the identified stochastic parameters. For example:

- **Renewable Availability Scenarios:** Based on historical meteorological data, scenarios representing years with low, average, and high solar irradiance and wind speed could be constructed.

- **Energy Price Scenarios:** Scenarios reflecting different future trajectories for electricity and natural gas prices (e.g., low, medium, high price levels, or different volatility patterns).

- **CO₂ Policy Scenarios:** Following the approach in some studies¹, scenarios could model different levels of CO₂ tax (e.g., $30, $60, $100 per ton CO₂) or different emission cap trajectories (e.g., aggressive vs. moderate reduction targets by 2030, 2040, 2050).

- **Demand Scenarios:** Scenarios representing variations in future electricity, heat, or water demands due to economic growth, population changes, or efficiency improvements.

Each defined scenario $\omega$ will be assigned a probability $p_\omega$, such that $\sum_{\omega \in \Omega} p_\omega = 1$. The selection of scenarios should aim to test the robustness of the investment decisions against a diverse set of future possibilities. For instance, a scenario matrix could be constructed by combining 2-3 levels (e.g., low, medium, high) for 2-3 key uncertain drivers (e.g., renewable availability, carbon price, energy demand growth), leading to a manageable number of discrete scenarios (e.g., $2^3 = 8$ or $3^3 = 27$ scenarios, potentially reduced further if needed).

## V. Results and Discussion

This section will present and interpret the anticipated outcomes from the two-stage stochastic optimization model applied to the Çorlu case study. As actual model runs are beyond the scope of this report, the discussion will focus on the types of results expected and their potential implications.

### A. Optimal System Design and Investment Strategy (First-Stage Decisions)

The model's primary output for first-stage decisions will be the optimal selection and sizing of technologies to be included in the integrated wastewater-energy-resource network. This will be presented for the primary objective function (e.g., minimization of Total Expected Annualized Cost - TAC).

**Table V.1: Optimal First-Stage Investment Decisions (Illustrative)**

| Technology Category | Unit Example | Min TAC (Base Case) Capacity | Min TAC (High CO₂ Tax) Capacity | Min CO₂ Emissions Capacity |
|:---|:---|:---|:---|:---|
| **Wastewater Treatment** | Anaerobic Digester Upgrade | e.g., 500 m³/d | e.g., 500 m³/d | e.g., 600 m³/d |
| | Nutrient Recovery (N) | e.g., 1 tN/d | e.g., 1.2 tN/d | e.g., 1.5 tN/d |
| **Energy Generation** | Wind Turbines | e.g., 10 MW | e.g., 15 MW | e.g., 20 MW |
| | PV Panels | e.g., 8 MWp | e.g., 12 MWp | e.g., 18 MWp |
| | Biogas CHP | e.g., 1 MWe | e.g., 0.8 MWe (if CCUS added) | e.g., 0.5 MWe |
| **Hydrogen Cycle** | Green H₂ (Electrolyzer) | e.g., 2 MW | e.g., 5 MW | e.g., 8 MW |
| | H₂ Storage | e.g., 500 kg | e.g., 1000 kg | e.g., 1500 kg |
| **Nitrogen Cycle/Ammonia** | Ammonia Synthesis | e.g., 0 t/d (or small pilot) | e.g., 5 t/d | e.g., 10 t/d |
| | Ammonia Storage | e.g., 0 m³ | e.g., 50 m³ | e.g., 100 m³ |
| **Other Energy Carriers** | Biodiesel Plant | e.g., Not Selected | e.g., 0.5 t/d (if feedstock) | e.g., 1 t/d |
| **Energy Storage** | Battery Storage | e.g., 2 MWh | e.g., 4 MWh | e.g., 6 MWh |
| **CCUS** | CO₂ Capture (from Biogas CHP) | e.g., Not Selected | e.g., 80% of CHP CO₂ | e.g., 90% of CHP CO₂ |
| | P2G (Methanation) | e.g., Not Selected | e.g., 0.5 MW SNG | e.g., 1 MW SNG |

The selection of specific technologies and their capacities will be driven by the interplay of Çorlu's local resource availability (wastewater characteristics, renewable potential), demand profiles, technology costs, and the prevailing CO₂ policy assumptions. For instance, if natural gas prices are high and renewable electricity is relatively inexpensive, green hydrogen production via electrolysis might be favored over blue hydrogen from SMR, even if the latter could be cheaper under different price regimes as suggested by findings in other sectors.¹

The model might reveal that certain WFE nexus linkages, such as nutrient recovery for fertilizer production or the use of CO₂ from biogas upgrading in P2G systems, offer significant economic or environmental advantages. Comparisons between solutions obtained under different objective functions (e.g., min TAC vs. min CO₂ emissions) will highlight the trade-offs involved in pursuing purely economic versus environmental goals.

### B. Expected Operational Performance and Recourse Actions (Second-Stage Decisions)

Analysis of the second-stage decisions will reveal the expected operational dynamics of the optimized system. This includes:

- **Energy Dispatch:** Hourly or seasonal profiles showing how electricity and heat demands are met by the various generation units (wind, PV, CHP, etc.) and storage systems.

- **Storage Operation:** Typical charging and discharging patterns for batteries, hydrogen storage, and ammonia storage, illustrating their role in balancing supply and demand and managing intermittency.

- **Resource Flows:** Quantification of the production, conversion, and utilization rates of key resources like biogas, hydrogen, ammonia, SNG, reclaimed water, and recovered nutrients.

- **Adaptation to Scenarios:** Crucially, the results will demonstrate how the system's operation (recourse actions) adapts to different realizations of uncertainty. For example, in scenarios with low renewable energy availability, the system might rely more on stored energy, dispatchable generation (e.g., biogas CHP), or grid imports. Conversely, in high renewable availability scenarios, surplus energy might be used for increased hydrogen/ammonia production or exported to the grid.

Key Performance Indicators (KPIs) will be calculated to summarize the system's overall performance:

**Table V.2: Key Performance Indicators (KPIs) of the Optimal System (Illustrative)**

| KPI | Unit | Min TAC (Base Case) | Min TAC (High CO₂ Tax) | Min CO₂ Emissions |
|:---|:---|:---|:---|:---|
| **Expected Total Annualized Cost (TAC)** | Million $/yr | e.g., 15.0 | e.g., 18.5 | e.g., 25.0 |
| - Annualized CAPEX | Million $/yr | e.g., 5.0 | e.g., 7.0 | e.g., 12.0 |
| - Expected Annual OPEX | Million $/yr | e.g., 12.0 | e.g., 14.0 | e.g., 16.0 |
| - Expected Annual Revenues | Million $/yr | e.g., 2.0 | e.g., 2.5 | e.g., 3.0 |
| **Expected Total CO₂ Emissions** | kt CO₂/yr | e.g., 50 | e.g., 20 | e.g., 5 |
| **H₂ Production (Green)** | t H₂/yr | e.g., 100 | e.g., 300 | e.g., 500 |
| **NH₃ Production** | t NH₃/yr | e.g., 0 | e.g., 150 | e.g., 400 |
| **SNG Production (from P2G)** | TJ/yr | e.g., 0 | e.g., 20 | e.g., 50 |
| **Renewable Energy Share in Electricity** | % | e.g., 60% | e.g., 80% | e.g., 95% |
| **Water Recovery Rate from WWTP** | % | e.g., 70% | e.g., 75% | e.g., 80% |
| **Nutrient (N) Recovery Rate** | % | e.g., 40% | e.g., 50% | e.g., 60% |
| **Value of Stochastic Solution (VSS)** | Million $/yr | e.g., 1.2 (8%) | e.g., 1.5 (8.1%) | e.g., 2.0 (8%) |

The Value of Stochastic Solution (VSS), calculated as the difference between the expected cost of the stochastic solution and the expected cost of a deterministic solution (obtained by solving the model with average values of uncertain parameters and then evaluating that fixed design across all scenarios), will quantify the economic benefit of using the 2SP approach.¹ A positive VSS indicates that the stochastic model leads to a more cost-effective design when uncertainties are considered.

The variability in second-stage operational decisions across different scenarios underscores the importance of designing systems with inherent operational flexibility. A robust first-stage design, guided by the stochastic model, should enable efficient and cost-effective operation across a wide spectrum of potential future conditions.

### C. Analysis of Integrated Hydrogen and Nitrogen Cycles

The model will provide detailed insights into the role and economic viability of hydrogen and nitrogen (via ammonia) cycles within the integrated system for Çorlu. This includes:

- **Quantification:** Optimal production levels of green H₂ (and blue H₂, if modeled), capacities of H₂ storage, and flow rates of H₂ to various end-uses (direct fuel, ammonia synthesis, P2G). Similarly, for ammonia, the model will determine production levels, storage capacities, and utilization pathways (energy carrier, H₂ source, fertilizer component).

- **Economic Viability:** The levelized cost of producing H₂ and NH₃ within the system will be an important output. The analysis will reveal under what conditions (e.g., renewable electricity prices, carbon prices, demand for H₂/NH₃) these cycles become economically competitive.

- **Drivers for Adoption:** The primary factors driving the selection of H₂/NH₃ technologies will be identified. These could include strict decarbonization targets (as H₂/NH₃ can be zero-carbon energy carriers if produced from renewables), the need for medium-to-long-term energy storage (where H₂/NH₃ offer advantages over batteries), or specific local demands for these products (e.g., industrial H₂ demand, agricultural demand for ammonia-based fertilizers).

The interaction between hydrogen production (its cost and associated CO₂ footprint, especially if comparing green vs. blue pathways) and its downstream applications is a critical aspect. The model will determine which applications of hydrogen (e.g., direct use, conversion to ammonia, or conversion to SNG) provide the greatest overall system value, considering both economic and environmental objectives. For instance, if a high carbon tax is imposed, the production of green H₂ for synthesizing ammonia (a zero-carbon fuel or chemical feedstock) might be prioritized over pathways that involve fossil-derived hydrogen or direct use of fossil fuels for certain energy services.

### D. Impact of WFE Nexus Linkages

A key focus of the research is to evaluate the benefits of integrating WFE nexus components. The model will quantify how the recovery of resources from wastewater impacts:

- **Overall Energy Balance and Costs:** For example, on-site energy generation from biogas (via CHP) can reduce the need to purchase electricity or other fuels. Reclaimed water can reduce costs associated with freshwater abstraction and treatment.

- **CO₂ Emissions:** Utilizing biogas instead of fossil fuels, or producing fertilizers from recovered nutrients instead of energy-intensive synthetic fertilizers, can lead to significant CO₂ emission reductions.

- **Reliance on External Resources:** Increased water reclamation reduces dependence on external freshwater sources. Nutrient recovery lessens the need for imported synthetic fertilizers. On-site energy generation from waste streams reduces reliance on grid electricity or external fuels.

The model will also quantify the benefits of circularity within the system. Examples include the potential utilization of CO₂ separated from biogas upgrading in P2G systems (if green H₂ is available) to produce SNG, effectively recycling carbon. Similarly, the integration of recovered nutrients with synthesized ammonia to produce enhanced fertilizers closes a loop between waste management, energy systems, and agriculture.

These WFE nexus integrations are expected to create synergistic benefits, leading to a system that is more cost-effective, environmentally sound, and resource-efficient than a collection of decoupled, independently optimized subsystems.

### E. Evaluation of Different Optimization Objectives / CO₂ Policies

The study will systematically evaluate how different optimization objectives and CO₂ policies influence the system's design and performance.

- **Objective Function Comparison:** If the model is run to minimize total CO₂ emissions, the resulting system design (technology choices, capacities) and its associated TAC will be compared to the solution obtained from minimizing TAC. This will reveal the "cost of decarbonization" for Çorlu under the modeled conditions.

- **Impact of CO₂ Policies:** The model will be run with varying levels of CO₂ tax or different CO₂ emission caps. The results will show:
  - Changes in the optimal technology mix (e.g., increased adoption of renewables, H₂/NH₃, CCUS as CO₂ penalties rise).
  - The penetration level of specific low-carbon pathways (e.g., green H₂ production, P2G).
  - The overall TAC and its components.
  - The cost of carbon abatement (e.g., $/ton CO₂ reduced) at different levels of emission reduction.

These analyses will mirror findings from other studies where CO₂ policies have been shown to be a powerful driver for technological change in energy and industrial systems.¹ For instance, as carbon taxes increase or emission caps become more stringent, capital-intensive but low-emission technologies like CCS, green hydrogen, and P2G systems are expected to become more economically viable compared to conventional, more polluting alternatives. The model will quantify these switching points and policy sensitivities specifically for the Çorlu WFE network. The finding that higher CET prices or lower CO₂ limits generally lead to increased adoption of renewable energy technologies¹ is anticipated to be a consistent outcome.

**Table V.3: Impact of CO₂ Policy on Technology Mix and Costs (Illustrative)**

| Parameter/Technology | Unit | No CO₂ Tax | Low CO₂ Tax (e.g., $30/t) | Medium CO₂ Tax (e.g., $60/t) | High CO₂ Tax (e.g., $100/t) |
|:---|:---|:---|:---|:---|:---|
| Green H₂ Capacity | MW | e.g., 0.5 | e.g., 2.0 | e.g., 5.0 | e.g., 8.0 |
| CO₂ Capture Capacity (CCS) | t CO₂/h | e.g., 0 | e.g., 0.5 | e.g., 1.5 | e.g., 2.5 |
| P2G (SNG) Capacity | MW SNG | e.g., 0 | e.g., 0.2 | e.g., 0.8 | e.g., 1.5 |
| Electricity from PV | GWh/yr | e.g., 10 | e.g., 15 | e.g., 25 | e.g., 35 |
| Electricity from Wind | GWh/yr | e.g., 15 | e.g., 25 | e.g., 40 | e.g., 60 |
| Total Expected TAC | M$/yr | e.g., 16.0 | e.g., 17.5 | e.g., 19.0 | e.g., 22.0 |
| Total Expected CO₂ Emissions | kt CO₂/yr | e.g., 60 | e.g., 40 | e.g., 20 | e.g., 10 |

### F. Sensitivity Analyses on Key Parameters

To assess the robustness of the model's conclusions, sensitivity analyses will be performed on critical deterministic parameters that were not included as stochastic variables but still possess inherent uncertainty or variability. These may include:

- **Technology Investment Costs:** Particularly for emerging technologies like electrolyzers, fuel cells, ammonia synthesis units, and CCUS, where future cost reductions are anticipated but uncertain. For example, a study on refinery decarbonization highlighted that a significant reduction (over 65%) in electricity prices was necessary for electric boilers to become more favorable than natural gas boilers with CCS¹; similar thresholds might exist for electrification versus gas-based routes in the Çorlu system.

- **Key Fuel/Energy Prices (Mean Values):** If mean values were used for parameters like biomass cost, or if certain price forecasts are highly uncertain.

- **Discount Rate:** The choice of discount rate can significantly influence the trade-off between upfront capital investments and long-term operational savings.

- **Efficiency of Key Conversion Processes:** Variations in the assumed efficiencies of electrolyzers, reformers, CHPs, etc.

The results of these sensitivity analyses (e.g., presented as tornado charts or spider plots) will indicate which parameters have the most significant influence on the optimal system design, operational strategy, TAC, and CO₂ emissions. This helps to identify areas where more precise data collection would be most beneficial and to understand the conditions under which the main conclusions of the study might change. If the optimal solution proves to be highly sensitive to a particular parameter (e.g., electrolyzer CAPEX), it would underscore the importance of future technological advancements or targeted policies to influence that parameter and thereby accelerate the adoption of desired pathways (like green hydrogen).

**Table V.4: Results of Sensitivity Analyses (Illustrative)**

| Parameter Varied | Variation Range | Impact on TAC (%) | Impact on Green H₂ Production (%) | Key Technology Choice Changes (if any) |
|:---|:---|:---|:---|:---|
| Electrolyzer CAPEX | +/- 30% | e.g., +/- 5% | e.g., +/- 20% | e.g., Switch from Green H₂ to Blue H₂ at +30% CAPEX |
| Renewable Electricity Price (if purchased) | +/- 20% | e.g., +/- 8% | e.g., +/- 15% | e.g., Increased grid purchase at -20% price |
| Discount Rate | 5% vs. 10% | e.g., +12% with 10% | e.g., -8% with 10% | e.g., Less CAPEX-intensive tech with 10% |
| Biogas Yield from AD | +/- 15% | e.g., +/- 3% | e.g., Minor impact | No major change |

## VI. Conclusions and Future Work

### A. Summary of Key Findings

This study will propose a novel two-stage stochastic programming model for the optimal design and operation of an integrated wastewater-energy-resource network tailored to the specific context of Çorlu, Türkiye. The key findings are expected to revolve around:

- **Optimal System Configuration:** Identification of the most cost-effective or emission-minimal combination of technologies from a diverse superstructure, including wastewater resource recovery units, renewable energy sources, hydrogen and nitrogen cycle components, various energy carriers, and CCUS options.

- **Role of H₂/N₂ Cycles:** Quantitative assessment of the conditions under which green/blue hydrogen and ammonia become integral parts of the urban energy and resource system, considering their production costs, storage requirements, and value in various end-use applications (e.g., fuel, feedstock, energy storage).

- **WFE Nexus Synergies:** Demonstration of tangible benefits from integrating wastewater treatment with energy production and resource recovery, such as reduced net energy consumption, lower CO₂ emissions, and decreased reliance on external inputs of water and nutrients.

- **Impact of Uncertainty and CO₂ Policies:** Elucidation of how uncertainties (in renewable availability, energy prices, demands) and CO₂ policies (carbon tax, emission caps) influence investment decisions and operational strategies. Stricter CO₂ policies are anticipated to drive greater adoption of low-carbon technologies, including renewables, H₂/NH₃, and CCUS.

- **Value of Stochastic Modeling:** Quantification of the VSS, highlighting the economic advantages of employing a stochastic optimization approach over deterministic methods for robust long-term planning in the face of multiple uncertainties.

The novel insights will stem from the comprehensive integration of these diverse elements within a rigorous stochastic optimization framework, applied to a real-world case study.

### B. Policy and Practical Implications

The findings of this research are intended to have direct policy and practical implications for urban planning and resource management in Çorlu and other similar urban-industrial regions:

- **Decision Support for Investment:** The model can provide data-driven guidance for strategic investments in sustainable infrastructure, identifying pathways that offer the best balance of economic viability and environmental performance under uncertain future conditions.

- **Policy Design:** The analysis of different CO₂ pricing mechanisms and emission targets can inform policymakers about the effectiveness of various instruments in achieving decarbonization goals and promoting the adoption of specific technologies (e.g., setting appropriate carbon tax levels to incentivize green hydrogen).

- **Utility Operations:** Insights into optimal operational strategies can help utility operators (wastewater, energy, water) to improve resource efficiency and reduce operational costs within an integrated system context.

- **Promotion of Circular Economy:** The study will highlight opportunities for closing resource loops (e.g., waste-to-energy, nutrient recycling, water reuse, CO₂ utilization), fostering a more circular economy at the urban scale.

The research will delineate the specific conditions (e.g., thresholds for renewable electricity costs, carbon prices, technology investment costs) under which investments in advanced technologies like green hydrogen production, ammonia infrastructure, or comprehensive wastewater resource recovery facilities become economically attractive and environmentally beneficial.

### C. Limitations of the Current Study

It is important to acknowledge the inherent limitations of this modeling study:

- **Data Availability and Accuracy:** The quality of the results is contingent upon the accuracy and completeness of the input data, particularly localized techno-economic parameters for Çorlu and detailed time-series data for demands and renewable resources. Assumptions made due to data gaps will be clearly stated.

- **Model Simplifications:** To maintain computational tractability, certain simplifications may be necessary (e.g., linear or piecewise linear approximations of nonlinear technology performance, aggregation of time periods or spatial details).

- **Scope of WFE Nexus:** While comprehensive, the model may not capture every conceivable WFE interlinkage, and the depth of modeling for certain components (e.g., detailed agricultural impacts of fertilizer use) might be constrained.

- **Computational Limitations:** Solving large-scale two-stage stochastic MILP or MINLP models can be computationally intensive, potentially limiting the number of scenarios or the level of detail that can be practically included.

### D. Avenues for Future Research

This research opens several avenues for future work:

- **Enhanced Dynamic Modeling:** Incorporation of more detailed intra-day operational dynamics, including finer time resolutions (e.g., sub-hourly), unit commitment decisions for dispatchable plants, and more precise modeling of ramp rates and start-up/shut-down characteristics.

- **Expanded WFE Nexus Scope:** Integration with more detailed agricultural models to assess the impact of recovered fertilizers on crop yields and food production, or linking with urban food supply chain models.

- **Multi-Objective Optimization:** Explicitly developing Pareto frontiers to explore the trade-offs between multiple conflicting objectives (e.g., cost, CO₂ emissions, water scarcity index, job creation) using multi-objective optimization algorithms.

- **Consideration of Other Sustainability Dimensions:** Incorporating social aspects (e.g., public acceptance, employment impacts) or a broader range of environmental indicators beyond CO₂ emissions (e.g., water footprint, land use, ecotoxicity).

- **Advanced Solution Techniques:** If the expanded model proves computationally intractable using standard solvers for the extensive form, future research could explore the application of advanced decomposition algorithms (e.g., Benders decomposition, Lagrangian relaxation) or heuristic methods. The Neur2SP approach¹, which uses machine learning to create a surrogate for the second-stage value function, is a particularly promising direction for tackling very complex 2SP problems where the second stage itself might be a difficult MIP or NLP. This could allow for the inclusion of more scenarios or greater model detail without prohibitive computational times.

- **Spatial Optimization:** Integrating geographical aspects, such as optimal siting of new facilities (e.g., renewable energy plants, decentralized H₂ production units) within the Çorlu region.

- **Multi-Stage Stochastic Programming:** Extending the model to a multi-stage framework to better capture sequential decision-making under evolving uncertainties over a longer planning horizon.

---

## References

¹ References cited throughout the document refer to various literature sources on energy system optimization, renewable energy technologies, carbon capture and storage, hydrogen production pathways, stochastic programming methods, and industrial decarbonization strategies. Complete bibliographic details would be provided in the full academic paper.