"""
SMD Line Capacity Optimization
--------------------------------
Allocates production across SMD assembly lines to maximize demand satisfaction
under capacity (utilization) constraints, using Integer Linear Programming.

Author: Gizem Bal
"""

import pandas as pd
import pulp
from pulp import LpProblem, LpVariable, lpSum, PULP_CBC_CMD


def load_data(utilization_path: str, demand_path: str):
    utilization_df = pd.read_excel(utilization_path, index_col=0)
    demand_df = pd.read_excel(demand_path, index_col=0)
    return utilization_df, demand_df


def build_model(utilization_df: pd.DataFrame, demand_df: pd.DataFrame) -> tuple:
    products = utilization_df.index.tolist()
    lines = utilization_df.columns.tolist()

    model = LpProblem(name="SMD_Capacity_Optimization", sense=pulp.LpMinimize)

    # Decision variables: units of product i produced on line j
    production = {
        (p, l): LpVariable(name=f"x_{p}_{l}", lowBound=0, cat="Integer")
        for p in products
        for l in lines
    }

    # Objective: minimize total utilization (assign production to most efficient lines)
    model += lpSum(
        utilization_df.loc[p, l] * production[p, l]
        for p in products
        for l in lines
    )

    # Constraint 1: All demand must be exactly met
    for p in products:
        model += (
            lpSum(production[p, l] for l in lines) == demand_df.loc[p, "Demand"],
            f"demand_{p}",
        )

    # Constraint 2: Total utilization per line <= 1 (100% capacity)
    for l in lines:
        model += (
            lpSum(utilization_df.loc[p, l] * production[p, l] for p in products) <= 1,
            f"utilization_{l}",
        )

    return model, production, products, lines


def solve_and_report(model, production, products, lines, utilization_df, demand_df):
    model.solve(PULP_CBC_CMD(msg=True, timeLimit=1000, options=["ratioGap=0.01"]))

    print(f"\nStatus: {pulp.LpStatus[model.status]}")
    print("=" * 60)

    results = []
    for p in products:
        for l in lines:
            val = int(production[p, l].value() or 0)
            util = utilization_df.loc[p, l] * val
            results.append({"Product": p, "Line": l, "Production": val, "Utilization": util})

    results_df = pd.DataFrame(results)

    # Line summary
    print("\n--- Line Summary ---")
    for l in lines:
        line_df = results_df[results_df["Line"] == l]
        total_prod = line_df["Production"].sum()
        total_util = line_df["Utilization"].sum()
        print(f"{l}: Total Production = {total_prod:,} | Utilization = {total_util:.4f}")

    # Unmet demand
    print("\n--- Unmet Demand ---")
    for p in products:
        produced = results_df[results_df["Product"] == p]["Production"].sum()
        demand = demand_df.loc[p, "Demand"]
        unmet = max(0, demand - produced)
        if unmet > 0:
            print(f"{p}: {unmet:,} units unmet (demand={demand:,}, produced={produced:,})")

    total_produced = results_df["Production"].sum()
    total_demand = demand_df["Demand"].sum()
    print(f"\nTotal Produced : {total_produced:,}")
    print(f"Total Demand   : {total_demand:,}")
    print(f"Fill Rate      : {total_produced / total_demand:.1%}")

    return results_df


def main():
    utilization_df, demand_df = load_data(
        "data/utilization_parameter.xlsx",
        "data/demand_all_cards.xlsx",
    )

    model, production, products, lines = build_model(utilization_df, demand_df)
    results_df = solve_and_report(model, production, products, lines, utilization_df, demand_df)

    output_path = "data/production_results.xlsx"
    results_df.to_excel(output_path, index=False)
    print(f"\nResults saved to '{output_path}'")


if __name__ == "__main__":
    main()
