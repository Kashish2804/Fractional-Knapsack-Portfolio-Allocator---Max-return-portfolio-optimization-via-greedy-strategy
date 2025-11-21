import operator
from typing import List, Dict, Any

# Define the Asset structure as a dictionary for Pythonic data organization.
# A class could also be used, but a dictionary list is often simpler for this type of problem.
# Keys will mirror the C struct fields: name, risk, expected_return, ratio, allocated_risk.

def portfolio_allocator_knapsack(assets: List[Dict[str, Any]], max_risk: float) -> None:
    """
    @brief Implements the Fractional Knapsack Algorithm for Portfolio Allocation.
    
    The algorithm selects assets based on the greedy choice (highest Return-to-Risk ratio)
    until the maximum allowed risk budget is depleted.
    
    Time Complexity: O(N log N) due to the sorting step, where N is the number of assets.
    
    :param assets: List of asset dictionaries.
    :param max_risk: The total allowed risk budget (Knapsack capacity).
    """
    n = len(assets)

    # 1. Calculate the Return-to-Risk Ratio for each asset (Value/Weight)
    for asset in assets:
        # Avoid division by zero, treat zero risk as a very high ratio (highest priority)
        # Ratio = expected_return / risk
        asset['ratio'] = asset['expected_return'] / asset['risk'] if asset['risk'] > 0 else 999999.0
        asset['allocated_risk'] = 0.0  # Initialize allocation to zero

    # 2. Sort the assets based on the ratio in descending order
    # This is the O(N log N) step and defines the greedy strategy.
    # Python's sort is stable and uses Timsort (O(N log N)).
    # We use 'operator.itemgetter' for fast key-based sorting.
    assets.sort(key=operator.itemgetter('ratio'), reverse=True)

    current_risk_budget = max_risk
    total_return = 0.0

    print("\n--- Allocation Process (Greedy Choice) ---")

    # 3. Perform the Greedy Selection
    for asset in assets:
        # If the entire asset can fit into the remaining risk budget
        if asset['risk'] <= current_risk_budget:
            
            # Take the whole asset (100% allocation)
            asset['allocated_risk'] = asset['risk']
            current_risk_budget -= asset['risk']
            total_return += asset['expected_return']

            print(f"  > Took 100% of {asset['name']:<20} (Ratio: {asset['ratio']:.2f}) | Risk Consumed: {asset['risk']:.2f} | Remaining Budget: {current_risk_budget:.2f}")
            
        elif current_risk_budget > 0:
            
            # Take a fraction of the asset (Fractional Knapsack Step)
            fraction = current_risk_budget / asset['risk']
            fractional_return = asset['expected_return'] * fraction

            asset['allocated_risk'] = current_risk_budget
            current_risk_budget = 0.0  # Budget is now fully used
            total_return += fractional_return
            
            print(f"  > Took {fraction * 100:.2f}% of {asset['name']:<20} (Ratio: {asset['ratio']:.2f}) | Risk Consumed: {asset['allocated_risk']:.2f} | Remaining Budget: 0.00")
            
            break  # Knapsack is full

    # 4. Print Final Results
    print("\n============================================\n")
    print("      OPTIMAL PORTFOLIO ALLOCATION SUMMARY\n")
    print("============================================\n")
    print(f"Maximum Allowed Risk Budget (Knapsack Capacity): {max_risk:.2f}")
    print(f"Total Expected Portfolio Return:                 ${total_return:.2f}")
    # Calculate the exact risk consumed (max_risk - remaining_budget)
    consumed_risk = max_risk - current_risk_budget
    print(f"Total Risk Consumed:                             {consumed_risk:.2f}")
    print("--------------------------------------------")
    print("Asset Name            | Investment Risk")
    print("--------------------------------------------")
    
    # Display the allocated risk for each asset
    for asset in assets:
        allocated_risk = asset['allocated_risk']
        
        # Calculate allocation percentage safely
        if allocated_risk > 0.0001: 
            if asset['risk'] == 0:
                allocation_percentage = 100.0
            else:
                allocation_percentage = (allocated_risk / asset['risk']) * 100

            print(f"{asset['name']:<20} | {allocated_risk:.2f} ({allocation_percentage:.1f}% of Asset Risk)")
    
    print("============================================\n")

def main():
    """
    @brief Main function for the Portfolio Allocator.
    """
    # Define the investment assets (The "Items" for the Knapsack)
    # Using a List of Dictionaries to represent the Asset structure.
    investment_assets = [
        {"name": "Tech Growth Fund", "risk": 12.5, "expected_return": 250.0},
        {"name": "US Treasury Bonds", "risk": 4.0, "expected_return": 40.0},
        {"name": "Real Estate Index", "risk": 7.0, "expected_return": 84.0},
        {"name": "Emerging Markets ETF", "risk": 18.0, "expected_return": 270.0},
        {"name": "Gold Futures", "risk": 6.0, "expected_return": 78.0}
    ]

    # Define the personalized risk constraint (The "Capacity" of the Knapsack)
    max_allowable_risk = 20.0  

    # Header and Problem Statement
    print("============================================\n")
    print("DAA Project: Personalized Investment Portfolio Allocator")
    print("Algorithm: Fractional Knapsack (Greedy)")
    print("Goal: Maximize Total Expected Return within a Max Risk Constraint.")
    print("============================================\n")
    print("Available Assets (Return/Risk):")
    for asset in investment_assets:
        print(f"  - {asset['name']:<20} | Return: ${asset['expected_return']:.2f} | Risk Score: {asset['risk']:.2f}")
    print("--------------------------------------------")

    # Run the Fractional Knapsack Algorithm
    # Note: Dictionaries are passed by reference in Python, so the 'assets' list
    # will be modified in-place with 'ratio' and 'allocated_risk' fields.
    portfolio_allocator_knapsack(investment_assets, max_allowable_risk)

    # DAA Analysis/Discussion Point
    print("--- Algorithm Analysis (For DA Subject) ---")
    print("1. Design Paradigm: Greedy Method")
    print("2. Greedy Choice Property: Prioritizing the asset with the highest Return-to-Risk Ratio.")
    print("3. Optimal Substructure: The optimal solution includes an optimal solution to the subproblem created by removing the chosen asset.")
    print("4. Complexity: O(N log N), primarily due to the Python's list sort (Timsort) used for sorting the 'Value-to-Weight' ratios.")
    print("5. Note: Since this is 'Fractional' Knapsack, we can take parts of assets, which guarantees the global optimal solution for the return maximization problem.")
    print("--------------------------------------------")

if __name__ == "__main__":
    main()
