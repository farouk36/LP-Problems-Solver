import numpy as np

def two_phase_method(c, A, b, constraint_types, isMax):
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

    # Initialize main row
    for i in range(vars_num):
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

    phase1_tableau[:-1, :vars_num] = A

    start = vars_num
    end = len(main_row) - 1

    for i in range(start, end + 1):
        for j in range(len(basic_var)):
            #artifical variables
            if i >= (len(main_row) - len(artificial_vars)):
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

    # add objective function (r)
    for i in range((len(main_row) - len(artificial_vars)), len(main_row)):
        phase1_tableau[-1, i] = -1
    # add right hand side
    phase1_tableau[:-1, -1] = b

    copied_phase1_tableau = np.copy(phase1_tableau)
    ## excute phase 1
    iterations, solution, new_basic_vars = __execute_phase1(phase1_tableau, artificial_vars, main_row, np.copy(basic_var))

    if solution is None:
        raise ValueError("The problem is unbounded")

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

    ################    Initialize tableau for phase 2  ########################
    #delete artifical variables cols from phase 1 tableau
    index_to_delete = -2
    for i in range (len(artificial_vars)):
        new_tablue = np.delete(new_tablue, index_to_delete, axis=1)

    #replace objective function (r) with c
    for i in range(len(c)):
        new_tablue[-1, i] = -c[i]

    #excute Phase 2
    iterations, solution = __execute_phase2(new_tablue, artificial_vars, main_row, new_basic_vars, isMax)

    if solution is None:
        raise ValueError("The problem is unbounded")

    #add steps
    sol_steps.append(iterations)

    #make the sol array
    sol_array = np.array(list(solution.values())[:len(c)])


    return sol_array, sol_steps, main_row, basic_var


def __execute_phase1(phase1_tableau, artificial_vars, main_row, basic_var):
    # Phase 1 make a simplix
    #add row of a's to (r) row
    make_vars_zeros_Linearly(phase1_tableau, main_row, basic_var.tolist())

    iterations = []
    solution = None
    iterations, solution, new_basic_vars = __excute_simplex(phase1_tableau, basic_var, main_row, artificial_vars, 1, 0)
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
        basic_var[leaving_var] = main_row[entering_var]

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





# #Try
# c = np.array([1,2,1])  # Coefficients of the objective function on the form z = 3*x1 + 2*x2 ==> z -3*x1 - 2*x2 =0
# A = np.array([[1,1,1], [ 2,-5,1]])  # Coefficients of the constraints
# b = np.array([7, 10])  # Right-hand side of the constraints
# constraints_type = ['=', '>=']  # Constraint types
# isMax = 1  # 0 for minimization, 1 for maximization

# sol, iter, mainRow, basic_var = two_phase_method(c, A, b, constraints_type, isMax)

# iter_count = 0
# for i in range(2):
#     print(f"Phase {i + 1}:")
#     for i, iteration in enumerate(iter[i]):
#         print(f"Iteration {iter_count + 1}:")
#         print(iteration)
#         print()
#         iter_count += 1

# print(sol)
# print(mainRow)
# print(basic_var)
