"""
Name of the author(s):
- Louis Navarre <louis.navarre@uclouvain.be>
"""
import time
import sys
from search import *


#################
# Problem class #
#################
class Rubik2D(Problem):
    def is_identical_line(self,line):
        print(line)
        first_element = line[0]
        for element in line:
            if first_element != element:
                return False
        return True

    def get_column(self,grid,i):
        column = [item[i] for item in grid] #this doesn't work if it's a tuple
        return column

    def move_column(self, grid,i,n_move):
        pass
    def move_row(self, grid, i, n_move): #return tuple
        line = grid[i]
        n_cols = len(grid)
        newline = line[slice(n_cols - n_move)] + line[slice(0, n_cols - n_move)]
        return newline

    def actions(self, state):
        """return a set of actions"""
        #look at all the horizontal line changes
        #LINES
        #check if line is identical

        n_cols = len(state.grid[0])
        n_rows = len(state.grid)
        action_list = []
        #the actions list will have a list of tuples of movements the first number will be the direction
        #0 means horizontal
        #1 means vertical
        #the second number will be by how much we move in a certain direction
        for line_number in range(len(state.grid)):
            line = state.grid[line_number]
            # print("hi")
            if not self.is_identical_line(line): #if line is not identical we do nothing
                for n_move in range(1,n_cols): #number of movements start from 1 to n_cols
                    newline = line[slice(n_cols - n_move)] + line[slice(0,n_cols-n_move)]
                    if(newline != line): #if not identical add list to move
                        action_list.append((0,line_number,n_move))

        #we will now work with vertical movements which is tricky

        for i in range(n_cols):
            # print("hey")
            line = self.get_column(state.grid,i) #get the column in list form
            if not self.is_identical_line(line):
                for n_move in range(1,n_rows):
                    newline = line[slice(n_rows - n_move)] + line[slice(0,n_rows-n_move)]
                    if (newline != line):  # if not identical add list to move
                        action_list.append((1,i, n_move))

        return action_list

    def result(self, state, action):
        """return the new grid"""
        #action is (0 or 1, n_move)
        (axe,axe_number,n_move) = action
        # print(axe,axe_number, n_move)
        list_grid = list(state.grid)
        if axe == 0:#move row
            list_grid[axe_number] = self.move_row(state.grid,axe_number,n_move)
            return tuple(list_grid)
        else:#move column
            #this requires a large amount of transforming
            #we will transform everything into a list of list
            for tuple in range(len(list_grid)):
                list_grid[tuple]= list(list_grid[tuple])

            #we can now manipulate a column
            column =self.get_column(list_grid,axe_number)
            n_rows = len(state.grid)
            newcolumn = column[slice(n_rows - n_move)] + column[slice(0, n_rows - n_move)]
            for line in range(n_rows):
                list_grid[line][axe_number] = newcolumn[line]

            #transform everything back to normal
            for element in range(n_rows):
                list_grid[]




    def goal_test(self, state):
        for i in range(len(state.grid)):
            if state.grid[i] != state.answer[i]:
                return False
        return True


###############
# State class #
###############
class State:

    def __init__(self, shape, grid, answer=None, move="Init"):
        self.shape = shape
        self.answer = answer
        self.grid = grid
        self.move = move

    def __str__(self):
        s = self.move + "\n"
        for line in self.grid:
            s += "".join(line) + "\n"
        # print(s)
        return s


def read_instance_file(filepath):
    with open(filepath) as fd:
        lines = fd.read().splitlines()

    shape_x, shape_y = tuple([int(i) for i in lines[0].split(" ")]) # x is the first number and y is the second number
    initial_grid = list()
    for row in lines[1:1 + shape_x]:
        initial_grid.append(tuple([i for i in row]))

    goal_grid = list()
    for row in lines[1 + shape_x + 1:]:
        goal_grid.append(tuple([i for i in row]))

    return (shape_x, shape_y), initial_grid, goal_grid


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: ./rubik2D.py <path_to_instance_file>")
    filepath = sys.argv[1]

    shape, initial_grid, goal_grid = read_instance_file(filepath)

    init_state = State(shape, tuple(initial_grid), tuple(goal_grid), "Init")
    problem = Rubik2D(init_state)

    # Example of search
    start_timer = time.perf_counter()
    node, nb_explored, remaining_nodes = breadth_first_tree_search(problem)
    end_timer = time.perf_counter()

    # Example of print
    path = node.path()

    for n in path:
        # assuming that the __str__ function of state outputs the correct format
        print(n.state)

    print("* Execution time:\t", str(end_timer - start_timer))
    print("* Path cost to goal:\t", node.depth, "moves")
    print("* #Nodes explored:\t", nb_explored)
    print("* Queue size at goal:\t",  remaining_nodes)
