"""
Test script to verify the setup and run a simple optimization
"""

import sys
import os

def test_imports():
    """Test if all required packages are available"""
    print("Testing package imports...")
    
    packages = {
        'pandas': 'Data manipulation',
        'numpy': 'Numerical computing',
        'matplotlib': 'Plotting',
        'seaborn': 'Statistical plotting',
        'gurobipy': 'Optimization solver'
    }
    
    failed = []
    for package, description in packages.items():
        try:
            __import__(package)
            print(f"✓ {package:<12} - {description}")
        except ImportError:
            print(f"✗ {package:<12} - {description} (NOT FOUND)")
            failed.append(package)
    
    return failed

def test_data_generation():
    """Test data generation module"""
    print("\nTesting data generation...")
    
    try:
        from src.data_generator import DataGenerator
        generator = DataGenerator()
        
        # Test time index generation
        time_index = generator.generate_time_index()
        print(f"✓ Generated {len(time_index)} time periods")
        
        # Test renewable profiles
        renewable_data = generator.generate_renewable_profiles()
        print(f"✓ Generated renewable profiles for {len(renewable_data)} scenarios")
        
        # Test WWTP data
        wwtp_data = generator.generate_wwtp_data()
        print(f"✓ WWTP potential biogas: {wwtp_data['potential_biogas']:.0f} m³/day")
        print(f"✓ WWTP potential energy: {wwtp_data['potential_energy_mwh']:.1f} MWh/day")
        
        return True
    except Exception as e:
        print(f"✗ Data generation failed: {str(e)}")
        return False

def test_simple_optimization():
    """Test a simple optimization problem with Gurobi"""
    print("\nTesting Gurobi optimization...")
    
    try:
        import gurobipy as gp
        from gurobipy import GRB
        
        # Create a simple test model
        m = gp.Model("test")
        
        # Create variables
        x = m.addVar(name="x")
        y = m.addVar(name="y")
        
        # Set objective
        m.setObjective(x + y, GRB.MINIMIZE)
        
        # Add constraint
        m.addConstr(x + 2*y >= 3)
        m.addConstr(x >= 0)
        m.addConstr(y >= 0)
        
        # Optimize
        m.optimize()
        
        if m.status == GRB.OPTIMAL:
            print(f"✓ Gurobi optimization successful")
            print(f"  Optimal value: {m.objVal}")
            print(f"  x = {x.X}, y = {y.X}")
            return True
        else:
            print(f"✗ Optimization failed with status {m.status}")
            return False
            
    except Exception as e:
        print(f"✗ Gurobi test failed: {str(e)}")
        if "No Gurobi license" in str(e):
            print("\nNote: You need a valid Gurobi license to run the optimization.")
            print("Academic users can get a free license at:")
            print("https://www.gurobi.com/academia/academic-program-and-licenses/")
        return False

def main():
    """Run all tests"""
    print("WFE NEXUS MODEL - SETUP TEST")
    print("="*50)
    
    # Add project directory to path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    # Test imports
    failed_imports = test_imports()
    
    if 'gurobipy' in failed_imports:
        print("\nCRITICAL: Gurobi is required to run the optimization model.")
        print("Please install Gurobi and obtain a license.")
        return
    
    # Test data generation
    if not failed_imports or (len(failed_imports) == 1 and 'gurobipy' in failed_imports):
        data_ok = test_data_generation()
    else:
        data_ok = False
    
    # Test Gurobi
    if 'gurobipy' not in failed_imports:
        gurobi_ok = test_simple_optimization()
    else:
        gurobi_ok = False
    
    # Summary
    print("\n" + "="*50)
    print("SETUP TEST SUMMARY")
    print("="*50)
    
    if not failed_imports and data_ok and gurobi_ok:
        print("✓ All tests passed! The model is ready to run.")
        print("\nTo run the full model:")
        print("  python main.py")
    else:
        print("✗ Some tests failed. Please fix the issues above.")
        if failed_imports:
            print(f"\nMissing packages: {', '.join(failed_imports)}")
            print("Install with: pip install -r requirements.txt")

if __name__ == "__main__":
    main()