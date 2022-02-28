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
        super().__init__(state)
        self.hashset = set()

    def move_row(self, list_grid, axe_number, n_move):
        line = list_grid[axe_number]
        n_column = len(list_grid[0])
        new_line = line[slice(n_column-n_move, n_column)] +line[slice(0, n_column-n_move)]
        return new_line

    def get_column(self,list_list_grid, axe_number):
        column = [item[axe_number] for item in list_list_grid]
        return column

    def move_column(self,list_list_grid, axe_number, n_move):
        column = self.get_column(list_list_grid, axe_number)
        n_rows = len(list_list_grid)
        new_column = column[slice(n_rows-n_move, n_rows)] + column[slice(0,n_rows-n_move)]
        return new_column

    def put_column(self,list_list_grid, axe_number, new_column):
        new_grid = list_list_grid
        # print(list_list_grid)
        # print(new_column)
        for i in range(len(list_list_grid)):
            new_grid[i][axe_number] = new_column[i]
        return new_grid



    def actions(self, state):
        """return a set of actions"""
        #horizontal lines
        n_column = len(state.grid[0])
        n_lines = len(state.grid)
        actions_list = []
        list_grid = []

        for i in range(n_lines):
            list_grid.append(list(state.grid[i]))


        for axe_number in range(n_lines):
            for n_move in range(1, n_column):
                if(self.move_row(list_grid,axe_number, n_move) != list_grid[axe_number]):
                    new_line = self.move_row(list_grid, axe_number, n_move)
                    list_grid[axe_number] = new_line
                    string_grid = str(list_grid)
                    if string_grid not in self.hashset:
                        actions_list.append((0, axe_number, n_move))
                        self.hashset.add(string_grid)

        #vertical
        for axe_number in range(n_column):
            for n_move in range(1, n_lines):
                if(self.move_column(list_grid, axe_number, n_move) != self.get_column(list_grid,axe_number)):
                    new_column = self.move_column(list_grid, axe_number, n_move)
                    list_grid = self.put_column(list_grid, axe_number, new_column)
                    string_grid = str(list_grid)
                    if string_grid not in self.hashset:
                        actions_list.append((1, axe_number, n_move))
                        self.hashset.add(string_grid)

        # print(actions_list)
        return actions_list

    def result(self, state, action):

        list_grid = list(state.grid) #list of tuples
        n_rows = len(list_grid)

        axe, axe_number, n_move = action
        if(axe == 0):#horizontal
            new_line = self.move_row(list_grid, axe_number, n_move)
            list_grid[axe_number] = new_line
            return State(state.shape, tuple(list_grid), state.answer, action)
        else:
            for i in range(n_rows):
                list_grid[i] = list(list_grid[i])

            new_column = self.move_column(list_grid, axe_number, n_move)
            list_grid = self.put_column(list_grid, axe_number, new_column)

            for i in range(len(list_grid)):
                list_grid[i] = tuple(list_grid[i])

            return State(state.shape, tuple(list_grid), state.answer,action)

    def goal_test(self, state):
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
        s = str(self.move) + "\n"
        for line in self.grid:
            s += "".join(line) + "\n"
        return s

    def __eq__(self, other):
        return isinstance(other,State) and self.grid == other.grid

    def __hash__(self) -> int:
        return hash(self.grid)

def read_instance_file(filepath):
    with open(filepath) as fd:
        lines = fd.read().splitlines()

    shape_x, shape_y = tuple([int(i) for i in lines[0].split(" ")])
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
    node, nb_explored, remaining_nodes = breadth_first_graph_search(problem)
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
