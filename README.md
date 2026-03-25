# SMD Line Capacity Optimization

> **Integer Linear Programming** model for allocating production across SMD (Surface Mount Device) assembly lines to maximize demand fulfillment under capacity constraints.

Developed during an industrial engineering project at an electronics manufacturing facility with **27 product types** across **6 assembly lines**.

---

## Problem Statement

SMD assembly lines have different machine configurations (CPH — components per hour) and each product requires a different share of line capacity (utilization parameter). Given a demand plan, the goal is to find the optimal allocation of production quantities across lines such that:

- All product demands are satisfied (where capacity allows)
- No line exceeds 100% utilization
- Production quantities are integers

---

## Mathematical Model

**Sets**
- `i` — product index (1…27)
- `j` — line index (1…6)

**Parameters**
- `U_ij` — utilization consumed per unit of product `i` on line `j` (cycle-based)
- `D_i` — demand for product `i`

**Decision Variable**
- `P_ij` — units of product `i` produced on line `j` *(integer)*

**Objective**
```
Minimize  Σ_{i,j}  U_ij × P_ij
```

**Constraints**
```
Σ_j  P_ij  =  D_i           ∀i   (all demand must be met)
Σ_i  U_ij × P_ij  ≤  1     ∀j   (line utilization ≤ 100%)
P_ij ≥ 0,  integer           ∀i,j
```

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.x | Core language |
| [PuLP](https://coin-or.github.io/pulp/) | ILP modeling & CBC solver |
| pandas | Data I/O, results processing |
| openpyxl | Excel input/output |

---

## Project Structure

```
smd-capacity-optimization/
├── optimize.py              # Main optimization script
├── data/
│   ├── utilization_parameter.xlsx   # U_ij matrix (27 products × 6 lines)
│   ├── demand_all_cards.xlsx        # D_i demand vector
│   └── production_results.xlsx      # Output (generated after run)
├── requirements.txt
└── README.md
```

---

## Getting Started

```bash
# 1. Clone
git clone https://github.com/<your-username>/smd-capacity-optimization.git
cd smd-capacity-optimization

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
python optimize.py
```

**Expected output:**
```
Status: Optimal
--- Line Summary ---
OD0: Total Production = X,XXX | Utilization = 0.XXXX
...
Fill Rate: XX.X%
Results saved to 'data/production_results.xlsx'
```

---

## Results

The model finds the **optimal integer production allocation** in under 60 seconds (CBC solver, 1% optimality gap).

Key outputs:
- Per-line production quantities and utilization rates
- Unmet demand breakdown by product
- Overall demand fill rate

---

## Context

This model was built as part of a capacity planning study for an SMD electronics manufacturing line. It supports scenario analysis (e.g., removing a product family from a line, adding a new line) by simply updating the input Excel files and re-running.

---

## Author

**Gizem Bal** — Industrial Engineer | Data Analyst  
[LinkedIn](https://linkedin.com/in/gizembal) · [GitHub](https://github.com/gizembal)
