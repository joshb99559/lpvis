from ortools.linear_solver import pywraplp
from draw import plot_constraints

# Define a linear optimization problem on the following:
#
# Objective: max(-x - y), such that:
# x + y <= 4
# -x + 2y >= -4
# x >= 1


def main():


# Instantiate a Glop solver, naming it LinearExample.
    solver = pywraplp.Solver('LinearProgrammingExample',
                             pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

    # Create the two variables and let them take on any non-negative value.
    x = solver.NumVar(-solver.infinity(), solver.infinity(), 'x')
    y = solver.NumVar(-solver.infinity(), solver.infinity(), 'y')

    # Constraint 0: x + y <= 4.
    constraint0 = solver.Constraint(-solver.infinity(), 4)
    constraint0.SetCoefficient(x, 1)
    constraint0.SetCoefficient(y, 1)

    # Constraint 1: -x + 2y >= -4
    constraint1 = solver.Constraint(-4, solver.infinity())
    constraint1.SetCoefficient(x, -1)
    constraint1.SetCoefficient(y, 2)

    # Constraint 2: x >= 1
    constraint2 = solver.Constraint(1, solver.infinity())
    constraint2.SetCoefficient(x, 1)
    constraint2.SetCoefficient(y, 0)

    # Objective function: -x - y.
    objective = solver.Objective()
    objective.SetCoefficient(x, -1)
    objective.SetCoefficient(y, -1)
    objective.SetMaximization()

    # Solve the system.
    solver.Solve()
    print(x.solution_value(), y.solution_value())
    solution_point = (x.solution_value(), y.solution_value())
    opt_solution = -1 * x.solution_value() + -1 * y.solution_value()
    print('Number of variables =', solver.NumVariables())
    print('Number of constraints =', solver.NumConstraints())
    # The value of each variable in the solution.
    print('Solution:')
    print('x = ', round(x.solution_value()))
    print('y = ', round(y.solution_value()))
    # The objective value of the solution.
    print('Optimal objective value =', (opt_solution))

    
    plot_constraints(solver, solution_point)
        

if __name__ == "__main__":
    main()