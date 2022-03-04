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
    def transform_list_to_tuple(self, grid):
        list_grid = []
        for i in range(len(grid)):
            list_grid.append(tuple(grid[i]))
        return tuple(list_grid)

    def actions(self, state):
        """we can only move one square at a time north east south west"""
        print("action")
        possible_locations = [[0, 1], [0, -1], [1, 0], [-1, 0]]  # right left down up

        position = state.person_position

        row = position[0]  # y
        column = position[1]  # x

        action_list = []
        for [i, j] in possible_locations:
            new_row = row + i
            new_column = column + j
            # check if the action is legal
            if (state.grid[new_row][new_column] != '#' and new_row < len(state.grid) and new_column < len(
                    state.grid[0])):
                action_list.append(
                    [new_row, new_column, position])  # we store the old position to avoid redoing a search
        print(action_list)
        return action_list

    def result(self, state, action):
        print("result")
        print(state.closest_objective)
        print(state.grid)
        print(state.person_position)
        print(action)
        new_grid = [x[:] for x in state.grid] #state.grid.deepcopy()ppllll
        new_row, new_column, last_position = action

        # move the person
        # erase the person
        new_grid[last_position[0]][last_position[1]] = ' '

        # move the person
        # check if that point is a page or the door (provided that there aren't any pages left)

        if new_grid[new_row][new_column] == 'p':
            state.no_paper -= 1
            #remove paper coord from coords

        elif new_grid[new_row][new_column] == 'X' and state.no_paper == 0:
            state.goal = True

        new_grid[new_row][new_column] = '@'
        print(new_grid)
        print([new_row, new_column])

        return State(new_grid, problem.transform_list_to_tuple(new_grid), state.goal, state.no_paper, state.paper_coords, state.door_position,
                     [new_row, new_column],random.randint(1,10000000000))

    def goal_test(self, state):
        # goal if one of the paper has been removed
        # when all paper are gone we have a goal when we are in the class room
        if state.goal== True:
            print("we have found the path")
        # print(state.goal)
        # print(state.no_paper)
        return state.goal

    def h(self, node):
        """down left is  0.0"""
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
    def __init__(self, grid, grid_tuple =None,  goal=False, no_paper=None, paper_coords=None, door_position=None,
                 person_position=None, closest_objective=None):
        self.nbr = len(grid)
        self.nbc = len(grid[0])
        self.grid = grid
        self.grid_tuple = grid_tuple
        ##added this
        self.no_paper = no_paper  # we have not achieved the final goal untill
        self.paper_coords = paper_coords
        self.door_position = door_position
        self.person_position = person_position
        self.goal = goal
        self.closest_objective = closest_objective

    # def __str__(self):
    #     '\n'.join(''.join(row) for row in self.grid)
    def __str__(self):
        s= "\n"
        for line in self.grid:
            s += "".join(line) + "\n"
        return s

    def __eq__(self, other_state):
        return isinstance(other_state, State) and self.grid_tuple == other_state.grid_tuple

    def __hash__(self) -> int:
        return hash(self.grid_tuple)

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
            if (grid[i][j] == '@'):
                return [i, j]


def find_details(grid):
    """scan the area for the amount of paper and the quantity and where the person is
    returns number of paper, their coords, coord of initial position and coord of the door"""
    no_paper = 0
    paper_coords = []
    person_position = []
    door_position = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (grid[i][j] == 'p'):
                no_paper += 1
                paper_coords.append([i, j])
            if (grid[i][j] == '@'):
                person_position = [i, j]
            if (grid[i][j] == 'X'):
                door_position = [i, j]

    return no_paper, paper_coords, person_position, door_position


#####################
# Launch the search #
#####################
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: ./pagecollect.py <path_to_instance_file>")

    problem = PageCollect.load(sys.argv[1])
    # print(problem.initial.grid)
    # print(problem.goal)

    problem.initial.no_paper, problem.initial.paper_coords, problem.initial.person_position, problem.initial.door_position = find_details(
        problem.initial.grid)


    problem.initial.grid_tuple  = problem.transform_list_to_tuple(problem.initial.grid)  # this way we can hash the grid

    # print("grid ")
    # print(problem.initial.grid)
    # print("grid_list")
    # print(problem.initial.grid_list)
    # print("number of paper left")
    # print(problem.initial.no_paper)
    # print("paper coords")
    # print(problem.initial.paper_coords)
    # print("position of person")
    # print(problem.initial.person_position)
    # print("position of door")
    # print(problem.initial.door_position)

    start_timer = time.perf_counter()
    # node = astar_search(problem)
    node,explored, frontier = breadth_first_graph_search(problem)
    end_timer = time.perf_counter()
    # example of print
    # print(node.state)
    path = node.path()

    print('Number of moves: ' + str(node.depth))
    for n in path:
        print(n.state)  # assuming that the __str__ function of state outputs the correct format

    print("* Execution time:\t", str(end_timer - start_timer))
    print("* Path cost to goal:\t", node.depth, "moves")
    print("nodes", explored)
    print("frontier", frontier)
    # print("* #Nodes explored:\t", nb_explored)
    # print("* Queue size at goal:\t", remaining_nodes)
