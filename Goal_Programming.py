import numpy as np
# from PyQt6.QtNetwork.QHttpHeaders import insert


def __excute_simplex(tableau, basic_var, main_row, artificial_vars ,phase, isMax  , priorities):
    iterations = []

    isDone = []
    for i in range(len(priorities)):
        isDone.append(False)

    while True:
        maxPriority = max(priorities)
        indices = np.where(np.array(priorities) == maxPriority)[0]
        entering_leaving_var = []
        iterations.append(np.copy(tableau))

        # For Phase 1, we always minimize
        current_isMax = 0 if phase == 1 else isMax

        if current_isMax == 1:  # maximization
            # Check if we reach the optimal solution
            # if all(x >= -1e-10 for x in tableau[-1, :-1]):
            #     break

            # Find the entering variable (most negative coefficient in the objective row)
            entering_var = np.argmin(tableau[priorities.index(maxPriority)+len(basic_var), :-1])
            entering_leaving_var.append(main_row[entering_var])

        else:  # minimization
            # Check if we reach the optimal solution
            # if all(x <= 1e-10 for x in tableau[-1, :-1]):
            #     break

            # Find the entering variable (most positive coefficient in the objective row)
            i=0
            maxCoefficient = tableau[indices[i]+len(basic_var),np.argmax(tableau[indices[i]+len(basic_var), :-1])]
            savedIndex = indices[i]+len(basic_var)
            for i in range(1,len(indices)):
                if (tableau[indices[i]+len(basic_var),np.argmax(tableau[indices[i]+len(basic_var), :-1])]>maxCoefficient):
                    maxCoefficient = tableau[indices[i]+len(basic_var), np.argmax(tableau[indices[i]+len(basic_var), :-1])]
                    savedIndex = indices[i]+len(basic_var)
            entering_var = np.argmax(tableau[savedIndex, :-1])
            entering_leaving_var.append(str(main_row[entering_var]))

        # Minimum ratio test
        ratios = []
        for i in range(len(basic_var)):  # Exclude the objective row
            if tableau[i, entering_var] > 0:
                ratios.append(tableau[i, -1] / tableau[i, entering_var])
            else:
                ratios.append(np.inf)

        if all(r == np.inf for r in ratios):
            if phase == 1:
                raise ValueError("Phase 1 problem is unbounded, which indicates an error in the formulation.")
            else:
                raise ValueError("Problem is unbounded. There is no finite optimal solution.")

        leaving_var = np.argmin(ratios)
        entering_leaving_var.append(str(basic_var[leaving_var]))
        if (isDone[savedIndex-len(basic_var)]==False):
            isDone[savedIndex-len(basic_var)]=True
            if entering_leaving_var[0] != entering_leaving_var[1]:
                iterations.append(entering_leaving_var)
        else:
            break
        # Update the basic variable
        basic_var[leaving_var] = str(main_row[entering_var])

        # Pivot operation
        pivot_element = tableau[leaving_var, entering_var]
        tableau[leaving_var, :] /= pivot_element

        for i in range(len(tableau)):
            if i != leaving_var:
                tableau[i, :] -= tableau[i, entering_var] * tableau[leaving_var, :]
        priorities[savedIndex-len(basic_var)] = 0

    # Check if phase 1 was successful (all artificial variables = 0)
    if phase == 1 and artificial_vars:
        # Check if the objective value is non-zero
        if abs(tableau[-1, -1]) > 1e-10:
            raise ValueError("Problem has no feasible solution. Phase 1 could not eliminate artificial variables.")

        # Check if any artificial variables are basic with non-zero values
        for i, var in enumerate(basic_var):
            if var in artificial_vars and abs(tableau[i, -1]) > 1e-10:
                raise ValueError("Problem has no feasible solution. Artificial variable remains in basis.")
    for i in range (len(basic_var), len(tableau)):
        if (all(tableau[i , :-1]<=0)):
            isDone[i-len(basic_var)] = True

        else :
            isDone[i-len(basic_var)] = False
    # Extract solution
    solution = {}
    for var in main_row:
        solution[var] = 0

    for i, var in enumerate(basic_var):
        solution[var] = tableau[i, -1]

    # Add objective value
    solution['objective_value'] = tableau[-1, -1]

    return iterations, solution, basic_var , isDone


def make_vars_zeros_Linearly(tablue, main_row, basic_var):
    print(main_row)
    print(basic_var)
    index_in_basic = 0
    for i in range(len(main_row)):
        if main_row[i] in basic_var:
            index_in_basic = basic_var.index(main_row[i])
            for j in range(len(basic_var) ,len(tablue)):
                cofficient_to_make_zero = (-1.0 * (tablue[j , i])) / (tablue[index_in_basic, i])
                tablue[j] += (cofficient_to_make_zero * tablue[index_in_basic])


def goal_method( num_vars_original , A, RHS_A, G, RHS_G, constraint_types, Goal_types,variable_types , priorities):



    # Handle unrestricted variables by splitting them into positive and negative parts
    unrestricted_indices = [i for i, v_type in enumerate(variable_types) if v_type == "Unrestricted"]
    # print(unrestricted_indices)

    # if unrestricted_indices:
    #     new_c = []
    #     for i in range(num_vars_original):
    #         if i in unrestricted_indices:
    #             new_c.append(c[i])
    #             new_c.append(-c[i])
    #         else:
    #             new_c.append(c[i])
    #     c = np.array(new_c)

    #     # Expand constraint matrix
    #     new_A = np.zeros((A.shape[0], A.shape[1] + len(unrestricted_indices)))
    #     col_idx = 0
    #     for i in range(num_vars_original):
    #         if i in unrestricted_indices:
    #             new_A[:, col_idx] = A[:, i]
    #             new_A[:, col_idx + 1] = -A[:, i]
    #             col_idx += 2
    #         else:
    #             new_A[:, col_idx] = A[:, i]
    #             col_idx += 1
    #     A = new_A

    num_vars = num_vars_original
    num_constraints = len(RHS_A)
    num_goals = len(RHS_G)
    j = 1
    num_slack=0
    mainRow = []
    basic_var = []

    #initialize main row with urs vars
    for i in range(num_vars):
        if i in unrestricted_indices:
            mainRow.append("x" + str(i + 1)+"+")
            mainRow.append("x" + str(i + 1)+"-")
        else:
            mainRow.append("x" + str(i + 1))


    # Add original decision variable labels
    # if unrestricted_indices:
    #     var_idx = 1
    #     for i in range(num_vars_original):
    #         if i in unrestricted_indices:
    #             mainRow.append("x" + str(var_idx)+"+")
    #             mainRow.append("x" + str(var_idx)+"-")
    #         else:
    #             mainRow.append("x" + str(var_idx))
    #         var_idx += 1
    # else:
    #     for i in range(num_vars):
    #         mainRow.append("x" + str(i+1))

    deviation_vars = []
    Zs = []
    for i in range(len(RHS_G)):
        Zs.append("z" + str(i+1))
        deviation_vars.append("d" + str(i+1)+ "-")
        deviation_vars.append("d" + str(i+1)+ "+")
        if Goal_types[i] == ">=":
            basic_var.append(deviation_vars[i*2])
        else:
            basic_var.append(deviation_vars[i*2+1])

    mainRow.extend(deviation_vars)
    print(mainRow)

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
    tableau = np.zeros((len(basic_var) + len(Zs), num_cols))
    start_artificial = num_vars + num_slack+ len(RHS_G)*2
    temp = start_artificial
    start_slack = num_vars +  len(RHS_G)*2

    tableau[len(RHS_G):-len(Zs) , -1] = RHS_A
    tableau[:len(RHS_G) , -1] = RHS_G

    #add A and G to the Tablue
    num_of_urs_gone = 0
    for i in range(len(G) + len(A)):
        num_of_urs_gone = 0
        for j in range(num_vars + len(unrestricted_indices)):
            if i < len(G):
                if mainRow[j][-1] == "-":
                    if abs(tableau[i][j - 1]) > 1e-10:
                        tableau[i, j] = -tableau[i][j - 1]
                    num_of_urs_gone += 1
                else:
                    tableau[i, j] = G[i][j - num_of_urs_gone]
            else:
                if mainRow[j][-1] == "-":
                    if abs(tableau[i][j - 1]) > 1e-10:
                        tableau[i, j] = -tableau[i][j - 1]
                    num_of_urs_gone += 1
                else:
                    tableau[i, j] = A[i - len(G)][j - num_of_urs_gone]

    # tableau[len(RHS_G):-len(Zs) , :num_vars] = A
    # tableau[:len(RHS_G) , :num_vars] = G

    # number_of_urs = 0
    # for i in range(tableau[0]):
    #     if mainRow[i] :
    i=0
    for j in range (len(RHS_G)):
        tableau[len(RHS_G)+len(RHS_A)+i , mainRow.index(basic_var[j] )] = (-priorities[i])
        i+=1
    j = num_vars + len(unrestricted_indices)
    for i in range (len(RHS_G)):
        tableau[i, j] = 1
        tableau[i, j+1] = -1
        j= j+2

    for i in range(len(RHS_G), len(RHS_G)+len(RHS_A), 1):

        j=0
        for k in range(num_vars+len(RHS_G)*2, num_cols-1, 1):
            if j < num_constraints:
                if constraint_types[j] == ">=":
                    tableau[i, start_slack + len(unrestricted_indices)] = -1
                    tableau[i, start_artificial+ len(unrestricted_indices)] = 1
                    start_artificial += 1
                    start_slack += 1
                elif constraint_types[j] == "=":
                    tableau[ i, start_artificial + len(unrestricted_indices)] = 1
                    start_artificial += 1
                else:
                    tableau[i, start_slack+ len(unrestricted_indices)] = 1
                    start_slack += 1
                j += 1

    new_tableau = tableau.copy()
    print(tableau)
    make_vars_zeros_Linearly(tableau,mainRow ,basic_var)
    isDone = []
    iterations, solution,  new_basic_var , isDone  = __excute_simplex(tableau, basic_var.copy() ,mainRow,artificial_vars, 2,0, priorities)

    print(solution)

    iterations = [new_tableau] + iterations

    # Handle unrestricted variables in solution
    # if unrestricted_indices:
    #     original_solution = {}
    #     sol_values = list(solution.values())
    #     print(solution)
    #     print(sol_values)
    #     var_idx = 0

    #     for i in range(num_vars_original):
    #         if i in unrestricted_indices:
    #             x_plus = sol_values[var_idx] if var_idx < len(sol_values) else 0
    #             x_minus = sol_values[var_idx + 1] if var_idx + 1 < len(sol_values) else 0
    #             original_solution["x" + str(i+1)] = x_plus - x_minus
    #             var_idx += 2
    #         else:
    #             original_solution["x" + str(i+1)] = sol_values[var_idx] if var_idx < len(sol_values) else 0
    #             var_idx += 1

    #     # Convert back to original variable space
    #     solution_array = np.array([original_solution.get("x" + str(i+1), 0) for i in range(num_vars_original)])
    # else:
    #     solution_array = np.array(list(solution.values())[:num_vars])
    # delete all unrestricted and all without objective function in the solution

    #handle delete all unrestricted
    for i in range(len(solution)):
        if "x" + str(i + 1) + "-" in solution:
            solution["x" + str(i + 1) + "+"] = solution["x" + str(i + 1) + "+"] - solution["x" + str(i + 1) + "-"]
            del solution["x" + str(i + 1) + "-"]


    sol_array = np.array(list(solution.values())[:num_vars_original])
    return sol_array, iterations, mainRow, basic_var , isDone


# Example usage
# c = np.array([-1,-5])  # Objective function coefficients
# Example with URS variable
A = np.array([[15, 30]])  # Constraint coefficients (15x1 + 30x2 <= 150)
G = np.array([[200, 0], [100, 400], [0, 250]])  # Goals coefficients
RHS_A = np.array([150])  # RHS of constraints
RHS_G = np.array([1000, 1200, 800])  # RHS of goals
constraints_type = ['<=']  # Constraint types
goals_type = ['>=', '>=', '>=']  # Goals types
priorities = [1, 2, 1]  # Priorities for goals
variables_types = ["Non-negative", "Non-negative"]  # x1 is non-negative, x2 is URS
np.set_printoptions(precision=3, suppress=True)

solution, iterations, mainRow, basic_var, isDone = goal_method(
    2, A, RHS_A, G, RHS_G, constraints_type, goals_type, variables_types, priorities
)

# Print results
for i in range(len(isDone)):
    if isDone[i]:
        print(f"Goal {i+1} is achieved")
    else:
        print(f"Goal {i+1} is not achieved")

print("\nOptimal solution:", solution)
print("\nBasic variables:", basic_var)
print("\nMain row variables:", mainRow)

# Print iterations
for i, iteration in enumerate(iterations):
    if isinstance(iteration, list):  # Skip entering/leaving var info
        continue
    print(f"\nIteration {i}:")
    print(iteration)

print("Column headers:", mainRow)
print("Basic variables:", basic_var)
print("Solution", solution)