import numpy as np
from Two_phase import __excute_simplex
def make_vars_zeros_Linearly(tablue, main_row, basic_var):
    index_in_basic = 0
    for i in range(len(main_row)):
        if main_row[i] in basic_var:
            index_in_basic = basic_var.index(main_row[i])
            cofficient_to_make_zero = (-1.0 * (tablue[len(tablue) - 1, i])) / (tablue[index_in_basic, i])
            tablue[len(tablue) - 1] += (cofficient_to_make_zero * tablue[index_in_basic])


def big_m_method(c, A, b, constraint_types, isMax,variable_types):

    num_vars_original = len(c)
    # Handle unrestricted variables by splitting them into positive and negative parts
    unrestricted_indices = [i for i, v_type in enumerate(variable_types) if v_type == "Unrestricted"]
    print(unrestricted_indices)

    if unrestricted_indices:
        new_c = []
        for i in range(num_vars_original):
            if i in unrestricted_indices:
                new_c.append(c[i])
                new_c.append(-c[i])
            else:
                new_c.append(c[i])
        c = np.array(new_c)

        # Expand constraint matrix
        new_A = np.zeros((A.shape[0], A.shape[1] + len(unrestricted_indices)))
        col_idx = 0
        for i in range(num_vars_original):
            if i in unrestricted_indices:
                new_A[:, col_idx] = A[:, i]
                new_A[:, col_idx + 1] = -A[:, i]
                col_idx += 2
            else:
                new_A[:, col_idx] = A[:, i]
                col_idx += 1
        A = new_A

    num_vars = len(c)
    num_constraints = len(b)
    j = 1
    num_slack=0
    mainRow = []
    basic_var = []

    # Add original decision variable labels
    if unrestricted_indices:
        var_idx = 1
        for i in range(num_vars_original):
            if i in unrestricted_indices:
                mainRow.append("x" + str(var_idx)+"+")
                mainRow.append("x" + str(var_idx)+"-")
            else:
                mainRow.append("x" + str(var_idx))
            var_idx += 1
    else:
        for i in range(num_vars):
            mainRow.append("x" + str(i+1))

    artificial_vars = []
    for i, constraint_type in enumerate(constraint_types):
        if constraint_type == ">=":
            mainRow.append("e" + str(j)) 
            num_slack+=1
            j += 1
        if constraint_type == ">=" or constraint_type == "=":
            artificial_vars.append("a" + str(i+1))
            basic_var.append("a" + str(i+1))
        else:
            num_slack+=1
            basic_var.append("s" + str(i + 1))
            mainRow.append("s" + str(i + 1))    

    if len(artificial_vars) > 0:
        mainRow.extend(artificial_vars)
        # basic_var.extend(artificial_vars)

    num_cols = len(mainRow) + 1
    tableau = np.zeros((len(basic_var) + 1, num_cols))
    start_artificial = num_vars + num_slack
    temp = start_artificial
    start_slack = num_vars

    tableau[:-1, -1] = b
    tableau[:-1, :num_vars] = A
    tableau[-1, :num_vars] = -c
    tableau[-1, temp:-1] = (-100 if (isMax==0) else 100)

    for i in range(len(basic_var)):
        flag=0
        for k in range(num_vars,num_cols, 1):
            if(tableau[i, k] == 1 or  flag):
                break
            elif i < num_constraints:  
                if constraint_types[i] == ">=":
                    tableau[i, start_slack] = -1
                    tableau[i, start_artificial] = 1
                    start_artificial += 1
                    start_slack += 1
                elif constraint_types[i] == "=":
                    tableau[i, start_artificial] = 1
                    start_artificial += 1
                else:
                    tableau[i, start_slack] = 1
                    start_slack += 1
                flag=1

    new_tableau = tableau.copy()
    make_vars_zeros_Linearly(tableau,mainRow ,basic_var)
    iterations, solution,  new_basic_var = __excute_simplex(tableau, basic_var.copy() ,mainRow,artificial_vars, 2, isMax)

    iterations = [new_tableau] + iterations

    # Handle unrestricted variables in solution
    if unrestricted_indices:
        original_solution = {}
        sol_values = list(solution.values())
        print(solution)
        print(sol_values)
        var_idx = 0

        for i in range(num_vars_original):
            if i in unrestricted_indices:
                x_plus = sol_values[var_idx] if var_idx < len(sol_values) else 0
                x_minus = sol_values[var_idx + 1] if var_idx + 1 < len(sol_values) else 0
                original_solution["x" + str(i+1)] = x_plus - x_minus
                var_idx += 2
            else:
                original_solution["x" + str(i+1)] = sol_values[var_idx] if var_idx < len(sol_values) else 0
                var_idx += 1

        # Convert back to original variable space
        solution_array = np.array([original_solution.get("x" + str(i+1), 0) for i in range(num_vars_original)])
    else:
        solution_array = np.array(list(solution.values())[:num_vars])

    print("################################################################")

    return solution_array, iterations, mainRow, basic_var


# # Example usage
# c = np.array([-1,-5])  # Objective function coefficients
# A = np.array([[1,1], [1,-1]])  # Constraint coefficients
# b = np.array([4,1])  # RHS of constraints
# constraints_type = ['<=', '=']  # Constraint types
# isMax = 0  # 0 for minimization, 1 for maximization
# variables_types =np.array(["Unrestricted","Non-negative"])
# np.set_printoptions(precision=3, suppress=True)
# solution, iterations,mainRow,basic_var=  big_m_method(c, A, b, constraints_type, isMax,variables_types)
#
# print("Optimal solution:", solution)
#
# for i, iteration in enumerate(iterations):
#       # Only print tableaus, not entering/leaving vars
#         print(f"Iteration {i}:")
#         print(iteration)
#         print()
#
# print("Column headers:", mainRow)
# print("Basic variables:", basic_var)