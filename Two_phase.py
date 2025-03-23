import numpy as np

def two_phase_method(c, A, b, constraint_types, isMax,variable_types):
    # Initialization
    vars_num = len(c)
    constrains_num = len(b)
    main_row = []
    basic_var = []
    artificial_vars = []#   As
    slack_vars2 = []#   Es
    slack_vars1 = []#   As
    relations_of_es_and_as = [] #[Es, As]
    sol_steps = []

    #handle know which index of variable is unrestricted
    unrestricted_indices = [i for i, v_type in enumerate(variable_types) if v_type == "Unrestricted"]

    # Initialize main row
    for i in range(vars_num):
        if i in unrestricted_indices:
            main_row.append("x" + str(i + 1))
            main_row.append("x" + str(i + 1) + "-")
        else:
            main_row.append("x" + str(i + 1))

    #add slack variables and artifical variables
    num_of_slack = 0
    current_artificial_var = 0
    num_of_slack2 = 0
    for i, constraint_type in enumerate(constraint_types):
        if constraint_type == ">=":
            slack_vars2.append("e" + str(num_of_slack2 + 1))
            num_of_slack2 += 1
        if constraint_type == ">=" or constraint_type == "=":
            artificial_vars.append("a" + str(current_artificial_var + 1))
            current_artificial_var += 1
        else:
            basic_var.append("s" + str(num_of_slack + 1))
            main_row.append("s" + str(num_of_slack + 1))
            slack_vars1.append("s" + str(num_of_slack + 1))
            num_of_slack += 1
        if constraint_type == ">=":
            relations_of_es_and_as.append(["e" + str(num_of_slack2), "a" + str(current_artificial_var)])

    # add slack variables
    if len(slack_vars2) > 0:
        main_row.extend(slack_vars2)

    # add artifical variables
    if len(artificial_vars) > 0:
        main_row.extend(artificial_vars)
        basic_var.extend(artificial_vars)

    ################    Initialize tableau for phase 1  ########################

    col_nums = len(main_row) + 1
    phase1_tableau = np.zeros((len(basic_var) + 1, col_nums))

    index_of_main_vars = 1
    for i in range(len(main_row)):
        for j in range(len(basic_var)):
            #handle main vars
            if i < (vars_num + len(unrestricted_indices)):
                if main_row[i] == "x" + str(index_of_main_vars):
                    phase1_tableau[j, i] = A[j, index_of_main_vars - 1]
                else:
                    phase1_tableau[j, i] = -A[j, index_of_main_vars - 1]
            #artifical variables
            elif i >= (len(main_row) - len(artificial_vars)):
                if main_row[i] == basic_var[j]:
                    phase1_tableau[j, i] = 1
            #slack variables (E's)
            elif (len(main_row) - len(artificial_vars)) > i >= (len(main_row) - len(artificial_vars) - len(slack_vars2)):
                for k in range(len(relations_of_es_and_as)):
                    if main_row[i] == relations_of_es_and_as[k][0] and basic_var[j] == relations_of_es_and_as[k][1]:
                        phase1_tableau[j, i] = -1
            #slack variables (S's)
            else:
                if main_row[i] == basic_var[j]:
                    phase1_tableau[j, i] = 1

        if i < (vars_num + len(unrestricted_indices)) and (main_row[i]) + "-" != main_row[i + 1]:
            index_of_main_vars += 1


    # add objective function (r)
    for i in range((len(main_row) - len(artificial_vars)), len(main_row)):
        phase1_tableau[-1, i] = -1
    # add right hand side
    phase1_tableau[:-1, -1] = b

    copied_phase1_tableau = np.copy(phase1_tableau)
    ## excute phase 1
    iterations, solution, new_basic_vars = __execute_phase1(phase1_tableau, artificial_vars, main_row, basic_var)

    if solution is None:
        raise ValueError("The problem is unbounded")

    #update the sol in new_table
    update_sol(solution, new_basic_vars, unrestricted_indices)

    #add steps
    iterations.insert(0, copied_phase1_tableau)
    initial_tablue = np.copy(copied_phase1_tableau)
    for i in range(len(phase1_tableau[0])):
        if i < len(c):
            initial_tablue[-1, i] = -c[i]
        else:
            initial_tablue[-1, i] = 0
    iterations.insert(0, initial_tablue)
    #add steps
    sol_steps.append(iterations)

    new_tablue = iterations[len(iterations) - 1]

    #update the sol in new_table
    for i in range(len(new_tablue) - 1):
        new_tablue[i][len(new_tablue[0]) - 1] = solution.get(new_basic_vars[i], 0)

    ################    Initialize tableau for phase 2  ########################
    #delete artifical variables cols from phase 1 tableau
    index_to_delete = -2
    for i in range (len(artificial_vars)):
        new_tablue = np.delete(new_tablue, index_to_delete, axis=1)

    #replace objective function (r) with c
    num_of_passes = 0
    for i in range(len(c)):
        new_tablue[-1, i + num_of_passes] = -c[i]
        if i in unrestricted_indices:
            num_of_passes += 1
            new_tablue[-1, i + 1] = c[i]

    #excute Phase 2
    iterations, solution = __execute_phase2(new_tablue, artificial_vars, main_row, new_basic_vars, isMax)

    if solution is None:
        raise ValueError("The problem is unbounded")

    #add steps
    sol_steps.append(iterations)

    #delete all unrestricted and all without objective function in the solution
    for i in range(len(solution)):
        if "x" + str(i + 1) + "-" in solution:
            solution["x" + str(i + 1)] = solution["x" + str(i + 1)] - solution["x" + str(i + 1) + "-"]
            del solution["x" + str(i + 1) + "-"]

    #make the sol array
    sol_array = np.array(list(solution.values())[:len(c)])


    return sol_array, sol_steps, main_row, basic_var


def update_sol(solution, new_basic_vars, unrestricted_indices):
    # Combine unrestricted variables (x = x+ - x-)
    for i in unrestricted_indices:
        x_plus = solution.get("x" + str(i + 1), 0)
        x_minus = solution.get("-x" + str(i + 1), 0)
        if "x" + str(i + 1) in new_basic_vars:
            solution["x" + str(i + 1)] = x_plus - x_minus
        else:
            solution["-x" + str(i + 1)] = x_minus - x_plus

    return solution


def __execute_phase1(phase1_tableau, artificial_vars, main_row, basic_var):
    #add row of a's to (r) row
    make_vars_zeros_Linearly(phase1_tableau, main_row, basic_var)

    iterations = []
    solution = None
    iterations, solution, new_basic_vars = __excute_simplex(phase1_tableau, basic_var.copy(), main_row, artificial_vars, 1, 0)
    return iterations, solution, new_basic_vars

def __execute_phase2(tablue, artificial_vars, main_row, basic_var, isMax):
    # Phase 2 make a simplix
    iterations = []
    solution = None

    iterations, solution, new_basic_vars = __excute_simplex(tablue, basic_var, main_row, artificial_vars, 2, isMax)
    return iterations, solution 


def make_vars_zeros_Linearly(tablue, main_row, basic_var):
    index_in_basic = 0
    for i in range(len(main_row)):
        if main_row[i] in basic_var:
            index_in_basic = basic_var.index(main_row[i])
            cofficient_to_make_zero = (-1.0 * (tablue[len(tablue) - 1, i])) / (tablue[index_in_basic, i])
            tablue[len(tablue) - 1] += (cofficient_to_make_zero * tablue[index_in_basic])


def __excute_simplex(tableau, basic_var, main_row, artificial_vars ,phase, isMax):
    iterations = []

    while True:
        entering_leaving_var = []
        iterations.append(np.copy(tableau))

        # For Phase 1, we always minimize
        current_isMax = 0 if phase == 1 else isMax

        if current_isMax == 1:  # maximization
            # Check if we reach the optimal solution
            if all(x >= -1e-10 for x in tableau[-1, :-1]):
                break

            # Find the entering variable (most negative coefficient in the objective row)
            entering_var = np.argmin(tableau[-1, :-1])
            entering_leaving_var.append(main_row[entering_var])

        else:  # minimization
            # Check if we reach the optimal solution
            if all(x <= 1e-10 for x in tableau[-1, :-1]):
                break

            # Find the entering variable (most positive coefficient in the objective row)
            entering_var = np.argmax(tableau[-1, :-1])
            entering_leaving_var.append(str(main_row[entering_var]))

        # Minimum ratio test
        ratios = []
        for i in range(len(tableau) - 1):  # Exclude the objective row
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
        if entering_leaving_var[0] != entering_leaving_var[1]:
                iterations.append(entering_leaving_var)

        # Update the basic variable
        basic_var[leaving_var] = str(main_row[entering_var])

        # Pivot operation
        pivot_element = tableau[leaving_var, entering_var]
        tableau[leaving_var, :] /= pivot_element

        for i in range(len(tableau)):
            if i != leaving_var:
                tableau[i, :] -= tableau[i, entering_var] * tableau[leaving_var, :]

    # Check if phase 1 was successful (all artificial variables = 0)
    if phase == 1 and artificial_vars:
        # Check if the objective value is non-zero
        if abs(tableau[-1, -1]) > 1e-10:
            raise ValueError("Problem has no feasible solution. Phase 1 could not eliminate artificial variables.")

        # Check if any artificial variables are basic with non-zero values
        for i, var in enumerate(basic_var):
            if var in artificial_vars and abs(tableau[i, -1]) > 1e-10:
                raise ValueError("Problem has no feasible solution. Artificial variable remains in basis.")

    # Extract solution
    solution = {}
    for var in main_row:
        solution[var] = 0

    for i, var in enumerate(basic_var):
        solution[var] = tableau[i, -1]

    # Add objective value
    solution['objective_value'] = tableau[-1, -1]

    return iterations, solution, basic_var




# # Define the problem
# c = np.array([-1,-5])  # Objective function coefficients
# A = np.array([[1,10], [1,-1]])  # Constraint coefficients
# b = np.array([4,1])  # RHS of constraints
# constraints_type = ['<=', '>=']  # Constraint types
# isMax = 0  # 0 for minimization, 1 for maximization
# variables_types =np.array(["Unrestricted","Non-negative"])
# np.set_printoptions(precision=3, suppress=True)

# # Solve using the two-phase method
# sol_array, sol_steps, main_row, basic_var = two_phase_method(c, A, b, constraints_type, isMax, variables_types)

# # Print the solution
# print("Optimal solution:", sol_array)
# print("Column headers:", main_row)
# print("Basic variables:", basic_var)
# print()
# iter_count = 0
# # Print the solution steps
# for i in range(len(sol_steps)):
#     print("Phase", i + 1)
#     for j in range(len(sol_steps[i])):
#         print("iteration", iter_count, ":\n", sol_steps[i][j])
#         iter_count += 1
#         print()
#     print()