from ortools.linear_solver import pywraplp
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
import numpy as np
import sympy as sym

# Define a linear optimization problem on the following:
#
# Objective: max(3x + 4y)
# Constraints:
# x + 2y <= 14
# 3x - y >= 0 -> -3x + y <= 0
# x - y <= 2


def main():
# Instantiate a Glop solver, naming it LinearExample.
    solver = pywraplp.Solver('LinearProgrammingExample',
                             pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

    # Create the two variables and let them take on any non-negative value.
    x = solver.NumVar(0, solver.infinity(), 'x')
    y = solver.NumVar(0, solver.infinity(), 'y')

    # Constraint 0: x + 2y <= 14.
    constraint0 = solver.Constraint(-solver.infinity(), 14)
    constraint0.SetCoefficient(x, 1)
    constraint0.SetCoefficient(y, 2)

    # Constraint 1: 3x - y >= 0.
    constraint1 = solver.Constraint(0, solver.infinity())
    constraint1.SetCoefficient(x, 3)
    constraint1.SetCoefficient(y, -1)

    # Constraint 2: x - y <= 2.
    constraint2 = solver.Constraint(-solver.infinity(), 2)
    constraint2.SetCoefficient(x, 1)
    constraint2.SetCoefficient(y, -1)

    # Objective function: 3x + 4y.
    objective = solver.Objective()
    objective.SetCoefficient(x, 3)
    objective.SetCoefficient(y, 4)
    objective.SetMaximization()

    # Solve the system.
    solver.Solve()
    opt_solution = 3 * x.solution_value() + 4 * y.solution_value()
    print('Number of variables =', solver.NumVariables())
    print('Number of constraints =', solver.NumConstraints())
    # The value of each variable in the solution.
    print('Solution:')
    print('x = ', x.solution_value())
    print('y = ', y.solution_value())
    # The objective value of the solution.
    print('Optimal objective value =', opt_solution)

    
    plot_constraints(solver)

def plot_constraints(solver):
    variables = solver.variables()
    list_of_constraints = solver.constraints()
    x_coeffs = []
    y_coeffs = []
    rhs_values = []
    for constraint in list_of_constraints:
        low_bound = constraint.lb()
        upp_bound = constraint.ub()

        if (low_bound != solver.infinity() and low_bound != -solver.infinity()):
            rhs_values.append(low_bound)
        else:
            rhs_values.append(upp_bound)


        x_coeff = constraint.GetCoefficient(variables[0])
        y_coeff = constraint.GetCoefficient(variables[1])

        x_coeffs.append(x_coeff)
        y_coeffs.append(y_coeff)
    
    #print(x_coeffs)
    #print(y_coeffs)
    #print(rhs_values)

    numEquations = len(solver.constraints())
    y_vals = []
    
    #Display lines of constraints
    for i in range(numEquations):
        x_coeff = x_coeffs[i - 1]
        y_coeff = y_coeffs[i - 1]
        rhs = rhs_values[i - 1]

        x = np.linspace(-20, 20, 2000)

        #solve constraint in terms of x
        y = (rhs - (x_coeff*x)) / y_coeff
        y_vals.append(y)
        
        plt.plot(x, y)

    

    plt.show()

        

if __name__ == '__main__':
    main()