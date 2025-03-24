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

## 2. Objective
The objective of this assignment is to develop a software tool capable of solving LP problems using:
- **Standard Simplex Method** for standard form LP problems (≤ constraints, non-negative variables).
- **BIG-M Method** to handle "greater-than-or-equal-to" (≥) and equality (=) constraints.
- **Two-Phase Method** as an alternative to the BIG-M method for artificial variables.
- **Preemptive Method for Goal Programming** for multi-objective optimization.

Additionally, support for unrestricted variables has been included.

## 3. Implementation Details

### 3.1 Programming Language
The solver was implemented using **Python**.

### 3.2 Input Format
The program accepts LP problems in the following standard format:
- **Objective function coefficients**
- **Constraint coefficients**
- **Right-hand side values**
- **Constraint types (≤, ≥, =)**
- **Variable restrictions (non-negative, unrestricted)**
- **Chosen method (BIG-M or Two-Phase, if applicable)**
- **Goal values and priority levels for goal programming**

### 3.3 Output Format
The program provides:
- **Optimal solution** (values of decision variables)
- **Optimal objective function value**
- **Problem status** (optimal, infeasible, unbounded)
- **Goal satisfaction (for goal programming)**
- **Step-by-step solution tables**

## 4. Sample Runs
Below are example cases solved using our program:

### 4.1 Example 1 - Simplex Method
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

### 4.2 Example 2 - Big-M Method
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
### 4.3 Example 3 - Two-Phase Method
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
### 4.4 Example 4 - Goal-programming Method
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