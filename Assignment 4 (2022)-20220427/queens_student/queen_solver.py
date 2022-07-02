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


def get_expression(size, queens=None): #queens is the queens alreadyt placed

    expression = []
    # your code here
    #return in cnf
    for queen in queens:
        clause = Clause(size)
        clause.add_positive(queen[0],queen[1]) #i fix that at i j it is true
        expression.append(clause)

    #conditions for rows
    for row in range(size):
        #atleast one
        clause = Clause(size)
        for column in range(size):
            clause.add_positive(row,column)
        expression.append(clause)

        #at most 1
        for column in range(size-1):#we don't take the last column
            for column2 in range(column+1,size):
                clause = Clause(size)
                clause.add_negative(row, column)
                clause.add_negative(row,column2)
                expression.append(clause)

    #conditions for columns
    for column in range(size):
        #atleast one
        clause = Clause(size)
        for row in range(size):
            clause.add_positive(row,column)
        expression.append(clause)

        for row in range(size-1):
            for row2 in range(row+1,size):
                clause = Clause(size)
                clause.add_negative(row,column)
                clause.add_negative(row2,column)
                expression.append(clause)

    #diagonal k-
    #i-j = k = -N+1,.. N +1
    #k = i-j = -N+1, .. 0
    #its easier to create the tuples then add them since i'm going mad
    #start with [0,0] to [n,n]
    #create bottom half
    #we take main diagonal
    #k = {-N -2 , ... 0}
    for k in range(size -1):
        for i in range(k,size - 1):
            for j in range(i + 1, size):
                clause = Clause(size)
                clause.add_negative(i,i-k)
                clause.add_negative(j,j-k)
                expression.append(clause)

    #we don't take the main diagonal
    #top half
    #this is essenitally sort of mixing the indexes
    for k in range(1,size - 1):
        for i in range(k,size-1):
            for j in range(i + 1, size):
                clause = Clause(size)
                clause.add_negative(i-k,i)
                clause.add_negative(j-k,j)
                expression.append(clause)


    #we take the main line
    #top half k = i +j
    #k = {1,..,N-1}
    for k in range(1,size):
        for i in range(k): #the max is always the k
            for j in range(i+1,k+1): #one further
                clause = Clause(size)
                clause.add_negative(i, k-i)
                clause.add_negative(j,k-j)#since it's one further
                expression.append(clause)

    #now we can make the other half
    #bottom half
    #we do not take the main diagonal
    for k in range(1,size-1):
        for i in range(1,size - k):
            for j in range(i+1, k + 1):
                clause = Clause(size)
                clause.add_negative(i,size-i)
                clause.add_negative(j,size-j)
                expression.append(clause)
    print("fourth diagonal")
    return expression


if __name__ == '__main__':
    expression = get_expression(3)
    for clause in expression:
        print(clause)
