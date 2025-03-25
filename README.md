# Operations Research - Assignment 1 Report

## Alexandria University  
**Faculty of Engineering**  
**Computer and Systems Department**  

### Team Members:
- Member 1: عبدالرحمن سعيد رمضان جمعه
- ID 1:     `22010879`
- Member 2: ايمن ابراهيم محمد قطب
- ID 2: `22010656`
- Member 3: فاروق اشرف فاروق
- ID 3: `22011012`

##

## 1. Introduction
This report presents the implementation of a Linear Programming (LP) solver using the Simplex Method and its variations. The solver is designed to handle different types of LP problems efficiently and provides a step-by-step solution process.

---
## 2. Code Flow and Architecture Report



### **2.1. Main Application Flow (main.py)**
The GUI application (`main.py`) serves as the entry point, built using PyQt5. It provides a user interface for defining LP problems and selecting solution methods.\

**Key components**:
- **Tabs**: Problem Definition, Solution, Iteration Steps.
- **Input Handling**: Collects variables, constraints, objective type (max/min), and method selection.
- **Solver Dispatch**: Calls appropriate solver based on user selection (Simplex, Big-M, Two-Phase, Goal Programming).

**Data Structures**:
- **Numpy Arrays**: For constraint matrices (`A`), objective coefficients (`c`), and RHS values (`b`).
- **Lists**: Track variable types (unrestricted/non-negative), constraint types (`<=`, `=`, `>=`), and goal priorities.
- **Dictionaries**: Store solutions and iterations for display.

---

### **2.2 Solver Methods**
The solver was implemented using **Python**.
#### **2.2.1 Standard Simplex Method (`Simplex.py`)**
**Purpose**: Solve LP problems with `<=` constraints and non-negative variables.  
**Key Functions**:
- `simplex_method(c, A, b, isMax)`:  
  - Initializes a tableau with slack variables.  
  - Iteratively selects entering/leaving variables using pivot operations.  
  - Returns the optimal solution and iteration steps.  

**Data Structures**:  
- **Tableau**: A 2D numpy array combining coefficients, slack variables, and RHS.  
- **Basic Variables**: List tracking slack variables (e.g., `s1`, `s2`).  

**Steps**:  
  1. Convert inequalities to equations using slack variables.  
  2. Iterate via pivoting to maximize/minimize the objective.  
---

### **2.2.2 Big-M Method (`Big_M.py`)**
**Purpose**: Handle problems with `>=` or `=` constraints using artificial variables and a penalty term (M).  
**Key Functions**:  
- `big_m_method(c, A, b, constraint_types, isMax, variable_types)`:  
  - Splits unrestricted variables into `x+` and `x-`.  
  - Adds artificial variables with large penalty coefficients (M).  
  - Uses simplex iterations to drive artificial variables out of the basis.  

**Data Structures**:  
- **Expanded Tableau**: Includes columns for artificial variables (`a1`, `a2`) and slack/excess variables.  
- **Variable Mapping**: Tracks split variables (e.g., `x1+`, `x1-`).  

**Steps**:  
  1. Add artificial variables with penalty coefficient M.  
  2. Solve using simplex, penalizing solutions where artificial variables are non-zero. 
---

### **2.2.3 Two-Phase Method (`Two_phase.py`)**
**Purpose**: Another way to Handle problems with `>=` or `=` constraints using two phases.\
phase 1 : To minimize the effect of artificial variables and find a feasible solution .\
phase 2 : Use the feasible basis to optimize the original objective.
**Key Functions**:  
- **Phase 1**: `__execute_phase1()` minimizes the sum of artificial variables.  
- **Phase 2**: `__execute_phase2()` optimizes the original objective after removing artificial variables.  
- `make_vars_zeros_Linearly()`: Adjusts the objective row to eliminate basic variables coefficients from it.  

**Data Structures**:  
- **Phase-Specific Tableaus**: Separate tableaus for feasibility (Phase 1) and optimization (Phase 2).  
- **Artificial Variables**: Tracked in `artificial_vars` list and removed post-Phase 1.  

---

### **2.2.4 Goal Programming (`Goal_Programming.py`)**
**Purpose**: Achieve multiple prioritized goals by minimizing deviations.  
**Key Functions**:  
- `goal_method()`:  
  - Adds deviation variables (`d+`, `d-`) for each goal.  
  - Modifies the tableau to prioritize goals.
  - Checks goal satisfaction via `isDone` list.  

**Data Structures**:  
- **Extended Tableau**: Includes columns for deviation variables and goal priorities.  
- **Priority List**: Tracks the importance of each goal (e.g., `[3, 2, 1]`).  

**Steps**:  
  1. Convert goals into constraints with deviation variables. 
  2. construct the objective function by summation of multiplyed priorities by deviation variables responsible for its Goal
  3. Optimize goals sequentially based on priority using lexicographic simplex.  

---

## 3. Key Data Structures  
1. **Tableau**:  
   - A 2D numpy array representing coefficients, slack/artificial variables, and RHS.  
   - Example: `tableau[-1, :]` stores the objective row.  
2. **Variable Lists**:  
   - `main_row`: Column headers (e.g., `x1`, `s1`, `a1`).  
   - `basic_var`: Current basic variables in the solution.  
3. **Solution Storage**:  
   - Dictionaries map variables to their values (e.g., `solution["x1"] = 5`).  

---

## 5. Function Interactions  
1. **GUI Inputs** → Converted to matrices (`A`, `b`, `c`) and constraint lists.  
2. **Solver Selection** → Dispatches to `simplex_method()`, `big_m_method()`, etc.  
3. **Tableau Initialization** → Built based on variable types and constraints.  
4. **Pivoting** → `__execute_simplex()` performs iterations across all methods.  
5. **Solution Extraction** → Post-processing (e.g., merging `x+`/`x-` for unrestricted variables).  

---

## 6. Sample Runs
Below are example cases solved using our program:

### 6.1 Example 1 - Simplex Method
```
Maximize Z = 3x1 + 5x2
Subject to:
  2x1 + 3x2 ≤ 8
  4x1 + x2 ≤ 6
  x1, x2 ≥ 0
```
**Output:**
- Optimal Solution: x1 = 1, x2 = 2
- Optimal Objective Value: Z = 13

### 6.2 Example 2 - Big-M Method
```
Maximize Z = 3x1 + 5x2
Subject to:
  2x1 + 3x2 ≤ 8
  4x1 + x2 ≤ 6
  x1, x2 ≥ 0
```
**Output:**
- Optimal Solution: x1 = 1, x2 = 2
- Optimal Objective Value: Z = 13
### 6.3 Example 3 - Two-Phase Method
```
Maximize Z = 3x1 + 5x2
Subject to:
  2x1 + 3x2 ≤ 8
  4x1 + x2 ≤ 6
  x1, x2 ≥ 0
```
**Output:**
- Optimal Solution: x1 = 1, x2 = 2
- Optimal Objective Value: Z = 13
### 6.4 Example 4 - Goal-programming Method
```
Maximize Z = 3x1 + 5x2
Subject to:
  2x1 + 3x2 ≤ 8
  4x1 + x2 ≤ 6
  x1, x2 ≥ 0
```
**Output:**
- Optimal Solution: x1 = 1, x2 = 2
- Optimal Objective Value: Z = 13

## 5. Bonus Feature
We developed a **user-friendly interface** by `pyQt5 in python` that allows users to input LP problems easily and view the solution process interactively.

## 6. Conclusion
This project provided hands-on experience in solving LP problems using different methods. The solver successfully handles various constraints and outputs detailed step-by-step solutions. Future improvements include extending support for additional optimization techniques and graphical visualization of results.
