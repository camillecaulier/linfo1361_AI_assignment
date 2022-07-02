from clause import *

"""
For the queen problem, the only code you have to do is in this file.

You should replace

# your code here

by a code generating a list of clauses modeling the queen problem
for the input file.

You should build clauses using the Clause class defined in clause.py

Read the comment on top of clause.py to see how this works.
"""


def get_expression(size, queens=None):
    expression = []
    
    # add all fixed queens
    for queen in queens:
        clause = Clause(size)
        clause.add_positive(queen[0], queen[1])
        expression.append(clause)

    # at least one queen per row
    for row in range(size):
        clause = Clause(size)
        for col in range(size):
            clause.add_positive(row, col)
        expression.append(clause)

    # max one queen per row
    for row in range(size):
        for col in range(size - 1):
            for col2 in range(col + 1, size):
                clause = Clause(size)
                clause.add_negative(row, col)
                clause.add_negative(row, col2)
                expression.append(clause)

    # max one queen per column
    for col in range(size):
        for row in range(size - 1):
            for row2 in range(row + 1, size):
                clause = Clause(size)
                clause.add_negative(row, col)
                clause.add_negative(row2, col)
                expression.append(clause)

    # max one queen per downward diagonal
    # lower triangle
    for start_row in range(size - 1):
        for row in range(start_row, size - 1):
            for row2 in range(row + 1, size):
                clause = Clause(size)
                clause.add_negative(row, row - start_row)
                clause.add_negative(row2, row2 - start_row)
                expression.append(clause)
    # upper triangle
    for start_col in range(1, size - 1):
        for col in range(start_col, size - 1):
            for col2 in range(col + 1, size):
                clause = Clause(size)
                clause.add_negative(col - start_col, col)
                clause.add_negative(col2 - start_col, col2)
                expression.append(clause)


    # max one queen per upward diagonal
    # upper triangle
    for start_row in range(1, size):
        for row in range(start_row):
            for row2 in range(row + 1, start_row + 1):
                clause = Clause(size)
                clause.add_negative(row, start_row - row)
                clause.add_negative(row2, start_row - row2)
                expression.append(clause)
    # lower triangle
    for start_col in range(1, size - 1):
        for col in range(start_col, size - 1):
            for col2 in range(col + 1, size):
                clause = Clause(size)
                clause.add_negative(size + start_col - 1 - col, col)
                clause.add_negative(size + start_col - 1 - col2, col2)
                expression.append(clause)

    return expression


if __name__ == '__main__':
    expression = get_expression(3)
    for clause in expression:
        print(clause)
