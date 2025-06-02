# Parameter Validation Report: WFE Nexus Model Configuration

## Executive Summary

This report provides a detailed comparison between the parameters in `model_config.py` and the recommendations from the critical review of energy system modeling parameters for the Turkish context. Critical discrepancies have been identified that may significantly impact model accuracy and decision-making.

## 1. Critical Parameter Discrepancies

### 1.1 Economic Parameters

#### Discount Rate
| Parameter | Current Value | Recommended Value | Impact | Action Required |
|-----------|---------------|-------------------|---------|----------------|
| DISCOUNT_RATE | 8% | **4.4-5.1%** (social) or **~20%** (commercial real) | **CRITICAL** | Immediate revision needed |

**Analysis**: The current 8% appears to be a compromise between social (4.4-5.1%) and commercial rates. However:
- For long-term social welfare analysis: Should use **4.5%**
- For commercial viability in current Turkish market: Should use **~20%** real discount rate
- The 8% value lacks clear justification and may lead to suboptimal investment decisions

#### Carbon Pricing
| Parameter | Current Values | Recommended Value | Impact | Action Required |
|-----------|----------------|-------------------|---------|----------------|
| CO2_TAX_SCENARIOS | 0, 30, 60, 100 $/ton | **0 $/ton** (baseline) | **HIGH** | Clarify scenario nature |

**Analysis**: Turkey has no operational carbon pricing as of 2025. Non-zero values should be clearly labeled as **hypothetical policy scenarios**, not current reality.

### 1.2 Technology Capital Costs

#### Solar PV
| Parameter | Current Value | Recommended Value | Impact | Action Required |
|-----------|---------------|-------------------|---------|----------------|
| PV CAPEX | 900 $/kWp | **760-1160 $/kW_DC** | MEDIUM | Within range, verify DC/AC basis |

#### Wind
| Parameter | Current Value | Recommended Value | Impact | Action Required |
|-----------|---------------|-------------------|---------|----------------|
| Wind CAPEX | 1400 $/kW | **1700-2000 $/kW** | **HIGH** | Underestimated by ~20-30% |

#### Battery Storage
| Parameter | Current Value | Recommended Value | Impact | Action Required |
|-----------|---------------|-------------------|---------|----------------|
| Battery CAPEX | 228 $/kWh | **270-480 $/kWh** | **HIGH** | Potentially underestimated |

#### Electrolyzer
| Parameter | Current Value | Recommended Value | Impact | Action Required |
|-----------|---------------|-------------------|---------|----------------|
| Electrolyzer CAPEX | 800 $/kW | **1000-1800 $/kW** (PEM) | **HIGH** | Significantly underestimated |

### 1.3 Technology Lifespans

| Technology | Current Value | Recommended Value | Impact | Action Required |
|------------|---------------|-------------------|---------|----------------|
| PV | 25 years | **30 years** | MEDIUM | Update recommended |
| Wind | 20 years | **25-30 years** | MEDIUM | Update recommended |
| Electrolyzer | 20 years | **40,000-60,000 hours** (~7-10 years continuous) | **HIGH** | Major overestimation |
| Fuel Cell | 15 years | **40,000-60,000 hours** (~7-10 years continuous) | MEDIUM | Needs clarification |

### 1.4 Energy Prices

#### Electricity Prices
| Parameter | Current Value | Recommended Value | Impact | Action Required |
|-----------|---------------|-------------------|---------|----------------|
| electricity_buy | 150 $/MWh | **~135 $/MWh** (2024-2025) | LOW | Reasonable approximation |
| electricity_sell | 60 $/MWh | Market dependent | MEDIUM | Needs verification |

#### Natural Gas
| Parameter | Current Value | Recommended Value | Impact | Action Required |
|-----------|---------------|-------------------|---------|----------------|
| natural_gas | 500 $/1000 m³ | **~430 $/1000 m³** | LOW | Slightly overestimated |

### 1.5 Technical Parameters

#### Electrolyzer Efficiency
| Parameter | Current Value | Recommended Value | Impact | Action Required |
|-----------|---------------|-------------------|---------|----------------|
| electricity_to_h2 | 55 kWh/kg | **50-56 kWh/kg** | LOW | Within range |
| electrolyzer efficiency | 65% | **60-67%** | LOW | Within range |

#### Grid Emission Factor
| Parameter | Current Value | Recommended Value | Impact | Action Required |
|-----------|---------------|-------------------|---------|----------------|
| grid_electricity | 0.442 ton CO2/MWh | Needs verification with 2023 data | MEDIUM | Update recommended |

## 2. Missing Critical Parameters

### 2.1 Technology-Specific O&M
The model uses a simplified 1.5% fixed O&M for all technologies. Recommended values:
- **Solar PV**: ~22 $/kW-yr (~2.4% of CAPEX)
- **Wind**: ~43-44 $/kW-yr (~2.5% of CAPEX)
- **Battery**: 2.5% of CAPEX/year
- **Electrolyzer**: 3-5% of CAPEX/year

### 2.2 Storage Parameters
- **Battery round-trip efficiency**: Should be **85%** (not 95% × 95% = 90.25%)
- **H2 storage leakage**: 0.1%/hour seems high; should be **<0.1%/day** for stationary storage

### 2.3 Regional Renewable Capacity Factors
Current seasonal averages (e.g., PV summer 25%) need validation against Turkish solar resource data.

## 3. Recommendations by Priority

### CRITICAL (Immediate Action Required)
1. **Discount Rate**: Implement dual approach - 4.5% for social welfare, 20% for commercial analysis
2. **Carbon Pricing**: Clearly label as scenarios, not current policy
3. **Electrolyzer CAPEX**: Update to 1000-1800 $/kW range
4. **Electrolyzer Lifespan**: Convert to operational hours (40,000-60,000)

### HIGH PRIORITY
1. **Wind CAPEX**: Update to 1700-2000 $/kW
2. **Battery CAPEX**: Update to 270-480 $/kWh
3. **Technology-specific O&M**: Replace uniform 1.5% with technology-specific values
4. **Grid Emission Factor**: Update with 2023 Turkish data

### MEDIUM PRIORITY
1. **Technology Lifespans**: Update PV (30 years), Wind (25-30 years)
2. **Storage Efficiency**: Correct battery round-trip efficiency to 85%
3. **Renewable Capacity Factors**: Validate against Turkish resource data

### LOW PRIORITY
1. **Product Prices**: Verify ammonia (400-450 $/ton) and hydrogen (3-6 $/kg) prices
2. **Natural Gas Price**: Minor adjustment to ~430 $/1000 m³

## 4. Implementation Guidelines

### 4.1 Scenario Structure
Implement a clear scenario structure:
```python
SCENARIOS = {
    'discount_rate_type': ['social', 'commercial'],
    'carbon_policy': ['current', 'future_low', 'future_high'],
    'technology_cost': ['current', 'future_optimistic']
}
```

### 4.2 Parameter Uncertainty
Consider implementing parameter ranges rather than point estimates:
```python
PARAMETER_RANGES = {
    'pv_capex': {'low': 760, 'mid': 960, 'high': 1160},
    'battery_capex': {'low': 270, 'mid': 375, 'high': 480}
}
```

### 4.3 Documentation
Each parameter should include:
- Source and year of data
- Assumptions (e.g., DC vs AC for solar)
- Applicability to Turkish context

## 5. Conclusion

The current `model_config.py` contains several critical parameter values that deviate significantly from current best-practice data for the Turkish energy context. Implementing the recommended changes will substantially improve model accuracy and reliability. Priority should be given to correcting the discount rate approach, updating technology costs to 2023-2024 values, and properly framing carbon pricing as scenarios rather than current policy.

**Next Steps**:
1. Create updated parameter file with recommended values
2. Implement sensitivity analysis for critical uncertain parameters
3. Document all parameter sources and assumptions
4. Establish regular parameter review process (annual)