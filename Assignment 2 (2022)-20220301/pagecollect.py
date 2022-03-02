from search import *
import time
import sys

#################
# Problem class #
#################
class PageCollect(Problem):

    def __init__(self, initial):
        # super().__init__(initial.state)
        super().__init__(initial)
        position = [-1,-1] #to keep track of positions -1 -1 to show that we're at initial condition
        #it is worth finding the position of p once because index() is a linear function and can bottleneck
        #position[0] = row , position[1] = column

        no_paper_left = 1 #we have not achieved the final goal untill

        # pass

    def actions(self, state):
        """we can only move one square at a time north east south west"""
        possible_locations = [[0, 1], [0, -1], [1, 0], [-1, 0]] #right left down up

        position = find_position(state.grid)#this very costly since it is O(nxm)

        row = position[0] #y
        column = position[1] #x

        action_list = []
        for [i,j] in possible_locations:
            new_row = row +i
            new_column = column + j
            #check if the action is legal
            if(state.grid[new_row][new_column] != '#' and new_row < len(state.grid) and new_column< len(state.grid[0])):
                action_list.append([new_row,new_column, position]) #we store the old position to avoid redoing a search

        return action_list
    
    def result(self, state, action):
        new_grid = state.grid
        new_row, new_column,last_position  = action

        #move the person
        #erase the person
        new_grid[last_position[0]][last_position[1]] = ' '
        #move the person
        if(new_grid[new_row][new_column] ==)
        pass

    def goal_test(self, state):
        #goal if one of the paper has been removed
        #when all paper are gone we have a goal when we are in the class room
        pass
    
    def h(self, node):
        """down left is  0.0"""
        h = 0.0
        possible_locations= [[0,1],[0,-1],[1,0],[-1,0]]
        # ...
        # compute an heuristic value
        # ...
        return h
    
    def load(path):
        with open(path, 'r') as f:
            lines = f.readlines()
            
        state = State.from_string(''.join(lines))
        return PageCollect(state)



###############
# State class #
###############
class State:
    def __init__(self, grid):
        self.nbr = len(grid)
        self.nbc = len(grid[0])
        self.grid = grid

    def __str__(self):
        '\n'.join(''.join(row) for row in self.grid)

    # def __eq__(self, other_state):
    #     pass
    #
    # def __hash__(self):
    #     pass
    
    def __lt__(self, other):
        return hash(self) < hash(other)
    
    def from_string(string):
        lines = string.strip().splitlines()
        return State(list(
            map(lambda x: list(x.strip()), lines)
        ))




def find_position(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if(grid[i][j] == '@'):
                return [i,j]


#####################
# Launch the search #
#####################
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: ./pagecollect.py <path_to_instance_file>")


    problem = PageCollect.load(sys.argv[1])
    print(problem.initial.grid)
    print(problem.goal)


    problem.position = find_position(problem.initial.grid)
    print(problem.position)


    start_timer = time.perf_counter()
    # node = astar_search(problem)
    node = best_first_graph_search(problem)
    end_timer = time.perf_counter()
    # example of print
    path = node.path()

    print('Number of moves: ' + str(node.depth))
    for n in path:
        print(n.state)  # assuming that the __str__ function of state outputs the correct format

    print("* Execution time:\t", str(end_timer - start_timer))
    print("* Path cost to goal:\t", node.depth, "moves")
    # print("* #Nodes explored:\t", nb_explored)
    # print("* Queue size at goal:\t", remaining_nodes)