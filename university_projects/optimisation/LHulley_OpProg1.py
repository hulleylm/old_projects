# Optimisation programming assignment. Laura Hulley. ID: 201277571. Dec 2020

# Please note - Ideally I would have used pulp and much more efficient code in this assignment. I produce each input and output lp file individually as
# i believe this best fits the assignment description that was laid out.

import random
import subprocess
import re
import itertools

# Define original given trianglle as global variable. Polytope nodes described in terms of x.
ORIGINAL_TRIANGLE = [["0"],
                     ["6", "4"],
                     ["12", "x1", "7"],
                     ["16", "x2", "x3", "9"],
                     ["19", "x4", "x5", "x6", "11"],
                     ["22", "x7", "x8", "x9", "x10", "13"],
                     ["25", "x11", "x12", "x13", "x14", "x15", "14"],
                     ["28", "28", "27", "26", "25", "23", "20", "15"]]


# if a rhombus of the given shape exists at the given node, calculate the inequality that forms the constraint.
def get_inequality(acute, obtuse):
    lhs = ""
    rhs = ""

    for node in acute:
        if "x" in node:
            lhs += " + " + node
        else:
            rhs += " - " + node

    for node in obtuse:
        if "x" in node:
            lhs += " - " + node
        else:
            rhs += " + " + node

    if len(rhs) == 0:
        rhs = "0"

    lhs = lhs.lstrip(" +")
    rhs = str(eval(rhs.lstrip(" +")))  # work out integer value

    ineq = lhs + " <= " + rhs
    return ineq


# finds whether there is a 'diamond shaped' with the given node as the 'top' node.
def find_diamond_rhombus_constraint(row, col):
    if 0 <= row < len(ORIGINAL_TRIANGLE) - 2:
        acute = [ORIGINAL_TRIANGLE[row][col],
                 ORIGINAL_TRIANGLE[row + 2][col + 1]]
        obtuse = [ORIGINAL_TRIANGLE[row + 1][col],
                  ORIGINAL_TRIANGLE[row + 1][col + 1]]
        
        return get_inequality(acute, obtuse)

    else:
        return None

#                                                  __
# finds whether there is a 'left leaning rhombus' \__\ with the given node as the 'top left' node.
def find_left_lean_rhombus_constraint(row, col):
    if 0 <= col < len(ORIGINAL_TRIANGLE[row]) - 1 and 0 <= row < len(ORIGINAL_TRIANGLE) - 1:
        acute = [ORIGINAL_TRIANGLE[row][col],
                 ORIGINAL_TRIANGLE[row + 1][col + 2]]
        obtuse = [ORIGINAL_TRIANGLE[row][col + 1],
                  ORIGINAL_TRIANGLE[row + 1][col + 1]]
        
        return get_inequality(acute, obtuse)

    else:
        return None

#                                                   __
# finds whether there is a 'left leaning rhombus' /__/  with the given node as the 'top left' node.
def find_right_lean_rhombus_constraint(row, col):
    if 0 <= col < len(ORIGINAL_TRIANGLE[row]) - 1 and 0 <= row < len(ORIGINAL_TRIANGLE) - 1:
        acute = [ORIGINAL_TRIANGLE[row][col + 1],
                 ORIGINAL_TRIANGLE[row + 1][col]]
        obtuse = [ORIGINAL_TRIANGLE[row][col],
                  ORIGINAL_TRIANGLE[row + 1][col + 1]]
        
        return get_inequality(acute, obtuse)

    else:
        return None

# Use a regex to get the output results of the lp file as an array of values
def find_all_mountains():
    list_of_mountains = []
    for i in range(1000):
        with open(f'output{i}.txt') as f:
            mountain_file = f.read()
            mountain = re.findall(r"x[\d\s]+B\s+(\d+)", mountain_file)
            list_of_mountains.append(mountain)
    
    return list_of_mountains

if __name__ == "__main__":

    # Form the list of constraints by calculating the inequality given by each possible rhombus
    constraints = ""
    for row in range(len(ORIGINAL_TRIANGLE)):
        for col in range(len(ORIGINAL_TRIANGLE[row])):

            diamond_rhombus = find_diamond_rhombus_constraint(row, col)
            if diamond_rhombus is not None:
                constraints += diamond_rhombus + "\n"

            left_lean_rhombus = find_left_lean_rhombus_constraint(row, col)
            if left_lean_rhombus is not None:
                constraints += left_lean_rhombus + "\n"

            right_lean_rhombus = find_right_lean_rhombus_constraint(row, col)
            if right_lean_rhombus is not None:
                constraints += right_lean_rhombus + "\n"

    # generate 1000 lp files to solve
    for i in range(1000):

        # add random coefficients to the x values in the objective function
        objective_function = ""
        for x in range(15):
            a = random.randint(-999, 999)
            if a < 0:
                objective_function += " - " + str(a*-1) + f" x{x + 1}"
            else:
                objective_function += " + " + str(a) + f" x{x + 1}"
        objective_function = objective_function.lstrip(" + ")

        # write the objective function and constraints to an lp file in the correct format
        with open(f"input{i}.lp", "w") as f:
            contents = "Maximize\n" + objective_function + "\nSubject To\n" + constraints + "End\n"
            f.write(contents)

    # call glpsol on every lp file that was produced and store the output
    for i in range(1000):
        subprocess.run(["glpsol", "--lp", f"input{i}.lp", "-o", f"output{i}.txt"])
    
    # analyse the output to find the set of distinct mountains
    all_mountains = find_all_mountains()
    distinct_mountains = [list(i) for i in set(tuple(i) for i in all_mountains)]

    distinct_mountains_output = ""
    for i in range(len(distinct_mountains)):
        for x in range(15):
            distinct_mountains_output += f" x{x + 1}: " + str(distinct_mountains[i][x])
        distinct_mountains_output += "\n"
    
    with open(f"distinctMountains.txt", "w") as f:
            f.write(distinct_mountains_output)