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

    def __init__(self,state):
        super().__init__(state, goal=state.answer)
        self.hashmap = {}


    def is_identical_line(self,line):
        first_element = line[0]
        for element in line:
            if first_element != element:
                return False
        return True

    def get_column(self,grid,i):
        column = [item[i] for item in grid] #this doesn't work if it's a tuple
        return column

    def move_row(self, grid, i, n_move): #return tuple
        line = grid[i]
        n_cols = len(grid)
        newline = line[slice(n_cols - n_move,n_cols)] + line[slice(0, n_cols - n_move)]
        return newline

    def move_column(self,list_grid,axe_number,n_move):
        column = self.get_column(list_grid, axe_number)
        n_rows = len(list_grid)
        newcolumn = column[slice(n_rows - n_move, n_rows)] + column[slice(0, n_rows - n_move)]
        return newcolumn

    def actions(self, state):
        """return a set of actions"""
        #look at all the horizontal line changes
        #LINES
        #check if line is identical
        # print("orignal:" )
        # print(state.grid)
        n_cols = len(state.grid[0])
        n_rows = len(state.grid)
        action_list = []

        #the actions list will have a list of tuples of movements the first number will be the direction
        #0 means horizontal
        #1 means vertical
        #the second number will be by how much we move in a certain direction
        for line_number in range(len(state.grid)):
            line = state.grid[line_number]
            if not self.is_identical_line(line): #if line is not identical we do nothing
                for n_move in range(1,n_cols): #number of movements start from 1 to n_cols
                    newline = line[slice(n_cols - n_move,n_cols)] + line[slice(0,n_cols-n_move)]
                    if(newline != line): #if not identical add list to move
                        #create matrix to see if it has already been seen before
                        # if state.grid in self.hashmap: # if self.hashmap[state.grid]
                        #     self.hashmap[state.grid] = True
                        #     print(self.hashmap)
                        action_list.append((0,line_number,n_move))

        #we will now work with vertical movements which is tricky

        for column_number in range(n_cols):
            column = self.get_column(state.grid,column_number) #get the column in list form
            if not self.is_identical_line(column):
                for n_move in range(1,n_rows):
                    newcolumn = column[slice(n_rows - n_move, n_rows)] + column[slice(0,n_rows-n_move)]
                    if (newcolumn != column):  # if not identical add list to move
                        action_list.append((1,column_number, n_move))

        # print(action_list)
        return action_list

    def result(self, state, action):
        """return the new grid"""
        #action is (0 or 1, n_move)
        (axe,axe_number,n_move) = action
        # print(axe,axe_number, n_move)
        list_grid = list(state.grid)
        n_rows = len(list_grid)

        if axe == 0:#move row
            list_grid[axe_number] = self.move_row(state.grid,axe_number,n_move)
            # print(list_grid)
            state.grid = tuple(list_grid)
            # return state
            return State(state.shape, state.answer, state.grid, "not init")

        else:#move column
            #this requires a large amount of transforming
            #we will transform everything into a list of list
            for tuple_index in range(len(list_grid)):
                list_grid[tuple_index]= list(list_grid[tuple_index])

            #we can now manipulate a column
            newcolumn = self.move_column(list_grid,axe_number,n_move)

            #insert
            for line in range(n_rows):
                list_grid[line][axe_number] = newcolumn[line]

            #transform everything back to normal
            for element in range(n_rows):
                list_grid[element] = tuple(list_grid[element])

            # print(list_grid)
            state.grid = tuple(list_grid)
            # print(state.grid)
            return State(state.shape, state.answer, state.grid, "not init")



    def goal_test(self, state):
        # for i in range(len(state.grid)):
        #     if state.grid[i] != state.answer[i]:
        #         return False
        # return True
        # print(type(state))
        # print(str(state))
        return state.grid == state.answer


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
    print(initial_grid)
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
