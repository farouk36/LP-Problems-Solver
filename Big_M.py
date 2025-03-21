import numpy as np
from Two_phase import __excute_simplex
def make_vars_zeros_Linearly(tablue, main_row, basic_var):
    index_in_basic = 0
    for i in range(len(main_row)):
        if main_row[i] in basic_var:
            index_in_basic = basic_var.index(main_row[i])
            cofficient_to_make_zero = (-1.0 * (tablue[len(tablue) - 1, i])) / (tablue[index_in_basic, i])
            tablue[len(tablue) - 1] += (cofficient_to_make_zero * tablue[index_in_basic])

    return tablue
def big_m_method(c, A, b, constraint_types, isMax):
   
    num_vars = len(c)
    num_constraints = len(b)
    j = 1
    num_slack=0
    
  
    mainRow = []
    basic_var = []
    for i in range(num_vars):
        mainRow.append("x" + str(i + 1))
   
   
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
    temp=start_artificial
    start_slack = num_vars

    # print(start_slack)
    # print(start_artificial)

    tableau[:-1, -1] = b
    tableau[:-1, :num_vars] = A
    tableau[-1, :num_vars] = -c
    tableau[-1, temp:-1] = (-100 if (isMax==0) else 100)
    for i in range(len(basic_var)):
        flag=0
        # if(i!=len(basic_var)):tableau[i, -1] = b[i]
        for k in range(num_vars,num_cols, 1):

            if(tableau[i, k] == 1 or  flag):
                break
            elif i < num_constraints:  
                # if k < num_vars:  
                #     tableau[i, k] = A[i, k]
                # if k >= num_vars:
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
            # else:  
            #     if k < num_vars:  
            #         tableau[i, k] = -c[k]
            #     elif k ==temp and k!=num_cols-1:
            #         tableau[i, k] = -100 
            #         temp+=1
    tableau = make_vars_zeros_Linearly(tableau,mainRow ,basic_var)
    iterations, solution,  basic_var = __excute_simplex(tableau,  basic_var ,mainRow,artificial_vars, 2, isMax)
    solution = np.array(list(solution.values())[:len(c)])
    print ("################################################################")
    return solution, iterations,mainRow,basic_var




# Example usage
c = np.array([1, 2, 1])  # Objective function coefficients
A = np.array([[1, 1, 1], [2, -5, 1]])  # Constraint coefficients
b = np.array([7, 10])  # RHS of constraints
constraints_type = ['=', '>=']  # Constraint types
isMax = 1  # 0 for minimization, 1 for maximization
solution, iterations,mainRow,basic_var=  big_m_method(c, A, b, constraints_type, isMax)

# solution, iterations, mainRow, basic_var = big_m_method(c, A, b, constraints_type, isMax)

print("Optimal solution:", solution)

for i, iteration in enumerate(iterations):
    if i % 2 == 0:  # Only print tableaus, not entering/leaving vars
        print(f"Iteration {i//2}:")
        print(iteration)
        print()

print("Column headers:", mainRow)
print("Basic variables:", basic_var)