import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
import numpy as np
import sympy as sym
from scipy.spatial import ConvexHull
from matplotlib.patches import Polygon

class Line:
    def __init__(self, x_coeff, y_coeff, rhs):
        self.x_coeff = x_coeff
        self.y_coeff = y_coeff
        self.rhs = rhs
        

def plot_constraints(solver, solution_point):
    variables = solver.variables()
    list_of_constraints = solver.constraints()
    x_coeffs = []
    y_coeffs = []
    rhs_values = []
    lines = []
    for constraint in list_of_constraints:
        low_bound = constraint.lb()
        upp_bound = constraint.ub()

        if (low_bound != solver.infinity() and low_bound != -solver.infinity()):
            rhs = low_bound
        else:
            rhs = upp_bound

        x_coeff = constraint.GetCoefficient(variables[0])
        y_coeff = constraint.GetCoefficient(variables[1])

        new_line = Line(x_coeff, y_coeff, rhs)
        lines.append(new_line)

        x_coeffs.append(x_coeff)
        y_coeffs.append(y_coeff)
        rhs_values.append(rhs)

    numEquations = len(solver.constraints())
    y_vals = []

    #Display lines of constraints
    for i in range(numEquations):
        x_coeff = x_coeffs[i - 1]
        y_coeff = y_coeffs[i - 1]
        rhs = rhs_values[i - 1]

        x = np.linspace(-20, 20, 2000)

        #solve constraint in terms of x
        if (y_coeff == 0):
            y = 0
        else:
            y = (rhs - (x_coeff*x)) / y_coeff
        y_vals.append(y)
        

    points = []
    #Find points of intersection
    for lineOne in lines:
        for lineTwo in lines:
            if (lineOne != lineTwo):
                (x, y) = find_intersect(lineOne, lineTwo)
                points.append([x, y])
                

    points = np.array(points)

    
    #Shade feasible region
    chull = ConvexHull(points)
    for simplex in chull.simplices:
        plt.plot(points[simplex, 0], points[simplex, 1], 'k-')

    cent = np.mean(points, 0)
    pts = []
    for pt in points[chull.simplices]:
        pts.append(pt[0].tolist())
        pts.append(pt[1].tolist())
    pts.sort(key=lambda p: np.arctan2(p[1] - cent[1], p[0] - cent[0]))
    pts = pts[0::2]  # Deleting duplicates
    pts.insert(len(pts), pts[0])
    k = 1.0
    color = 'red'
    poly = Polygon(k*(np.array(pts)- cent) + cent,
                facecolor=color, alpha=0.2)
    poly.set_capstyle('round')
    plt.gca().add_patch(poly)
    
    plt.arrow(3, 2, -2, -2, shape = 'full', head_width = 0.05, head_length = 0.05, color = 'blue')
    plt.arrow(3.2, 1, -2.2, -2, shape = 'full', head_width = 0.05, head_length = 0.05, color = 'blue')


    #Plot solution point
    plt.plot(solution_point[0], solution_point[1], color='green', marker='x', markersize = 10.0)

    plt.show()

def find_intersect(lineOne, lineTwo):
    # Returns the x, y position of the intersection of two lines
    # if one exists. Otherwise, return nil
    # In: lineOne, lineTwo
    a = lineOne.x_coeff
    b = lineOne.y_coeff
    c = lineOne.rhs
    d = lineTwo.x_coeff
    e = lineTwo.y_coeff
    f = lineTwo.rhs

    x = 0
    y = 0
    if (a == 0):
        y = c/b
        x = (f - e*y)/d
    elif (b == 0):
        x = c/a
        y = (f - d*x)/e
    elif (d == 0):
        y = f/e
        x = (c - b*y)/a
    elif (e == 0):
        x = f/d
        y = (c - a*x)/b
    else:
        x = (e*c - b*f)/(e*a - b*d)


    #print("x: ", x, "y: ", y)

    return (x, y)
