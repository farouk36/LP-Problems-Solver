import numpy as np

def simplex_method(c, A, b, isMax):
    # Number of variables and constraints
    num_vars = len(c)
    num_constraints = len(b)
    mainRow = []
    entering_leaving_var = []
    basic_var = []
    for i in range(num_vars):
        mainRow.append("x" + str(i+1))
    for i in range (num_constraints):
        mainRow.append("s" + str(i+1))
        basic_var.append("s" + str(i+1))
    
    
    tableau = np.zeros((num_constraints + 1, num_vars + num_constraints + 1))
    
    tableau[:-1, :num_vars] = A
    tableau[:-1, num_vars:num_vars + num_constraints] = np.eye(num_constraints)
    tableau[:-1, -1] = b
    tableau[-1, :num_vars] = -c
    
    iterations = []
    
    while True:
        entering_leaving_var = [] 
        iterations.append(np.copy(tableau))

        if (isMax==1):    # maximization
            # Check if we reach the optimal soln.
            if all(x >= 0 for x in tableau[-1, :-1]):
                break
            
            # Find the entering variable (most -ve coefficient in the objective row)
            entering_var = np.argmin(tableau[-1, :-1])
            entering_leaving_var.append(mainRow[entering_var])


        else :   #minimization
            # Check if we reach the optimal soln.
            if all(x <= 0 for x in tableau[-1, :-1]):
                break
            
            # Find the entering variable (most +ve coefficient in the objective row)
            entering_var = np.argmax(tableau[-1, :-1])
            entering_leaving_var.append(mainRow[entering_var])

        # minimum ratio test
        ratios = []
        for i in range(num_constraints):
            if tableau[i, entering_var] > 0:
                ratios.append(tableau[i, -1]*1.0 / tableau[i, entering_var])
            else:
                ratios.append(np.inf)
        
        if all(r == np.inf for r in ratios):
            raise Exception("Problem is unbounded")
        
        leaving_var = np.argmin(ratios)
        entering_leaving_var.append(mainRow[num_vars + leaving_var])
        iterations.append(entering_leaving_var)
        
        # Pivot operation
        pivot_element = tableau[leaving_var, entering_var]
        tableau[leaving_var, :] /= (pivot_element*1.0)
        
        for i in range(num_constraints + 1):
            if i != leaving_var:
                tableau[i, :] -= tableau[i, entering_var] * tableau[leaving_var, :]
    
    solution = np.zeros(num_vars)
    for i in range(num_vars):
        col = tableau[:, i]
        if np.sum(col == 1) == 1 and np.sum(col == 0) == num_constraints:
            solution[i] = tableau[np.where(col == 1)[0][0], -1]
    
    return solution, iterations,mainRow,basic_var

# # # Example usage
# c = np.array([5, -4,6,-8])  # Coefficients of the objective function on the form z = 3*x1 + 2*x2 ==> z -3*x1 - 2*x2 =0
# A = np.array([[1,2,2,4], [ 2,-1,1,2],[4,-2,1,-1]])  # Coefficients of the constraints
# b = np.array([40, 8,10])  # Right-hand side of the constraints
#
# solution, iterations,mainRow,basic_var = simplex_method(c, A, b , 0)   # 1 for maximization and 0 for minimization
#
# print("Optimal solution:", solution)
#
# for i, iteration in enumerate(iterations):
#     print(f"Iteration {i+1}:")
#     print(iteration)
#     print()
#
# print(mainRow)
# print(basic_var)