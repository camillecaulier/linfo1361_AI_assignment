from search import *
import time
import sys

#################
# Problem class #
#################
class PageCollect(Problem):

    # def __init__(self, initial):
    #     pass

    def actions(self, state):
        """we can only move one square at a time"""
        pass
    
    def result(self, state, action):
        pass

    def goal_test(self, state):
        pass
    
    def h(self, node):
        """down left is  """
        h = 0.0
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






#####################
# Launch the search #
#####################
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: ./pagecollect.py <path_to_instance_file>")


    problem = PageCollect.load(sys.argv[1])
    print(problem.initial.grid)
    print(problem.goal)

    start_timer = time.perf_counter()
    node = astar_search(problem)
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