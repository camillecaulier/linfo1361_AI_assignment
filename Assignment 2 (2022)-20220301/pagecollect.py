from search import *
import time
import sys
import math


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

    def find_distance(self, person, objective):
        return math.sqrt((person[0] - objective[0]) ** 2 + (person[1] - objective[1]) ** 2)

    def find_new_closest_objective(self, state, paper_coords, no_paper, person_positon):
        """we have state but we must be vigilant since it contains oldvalues such as no update paper coords or number
        of paper """

        if no_paper == 0:  # this means that there are no paper objectves and we can start looking for the last objective
            return state.door_position
        else:
            closest_objective_distance = (state.nbr * state.nbc) ** 2  # i just took an upper bound that i'm fairly certain that
            # I wouldn't be able to surpass
            closest_objective = paper_coords[0]
            for coords in range(len(paper_coords)):
                dist = distance(person_positon, paper_coords[coords])
                if dist < closest_objective_distance:
                    closest_objective = paper_coords[coords]
                    closest_objective_distance = dist
            return closest_objective

    def actions(self, state):
        """we can only move one square at a time north east south west"""

        # possible_locations = [[0, 1], [0, -1], [1, 0], [-1, 0]]  # right left down up
        possible_locations = [[1, 0],[0, -1],[0, 1],[-1, 0]]  # down left right up
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

        return action_list

    def result(self, state, action):

        new_grid = [x[:] for x in state.grid]  # state.grid.deepcopy()ppllll
        new_row, new_column, last_position = action

        # move the person
        # erase the person

        #"condition to make sure we don't erase the X accidentally
        if(last_position == state.door_position):
            new_grid[last_position[0]][last_position[1]] = 'X'
        else:
            new_grid[last_position[0]][last_position[1]] = ' '

        # new_grid[last_position[0]][last_position[1]] = ' '

        # move the person
        # check if that point is a page or the door (provided that there aren't any pages left)
        no_paper = state.no_paper
        paper_coords = state.paper_coords.copy()
        new_closest_objective = state.closest_objective
        if new_grid[new_row][new_column] == 'p':
            no_paper -= 1

            if state.isAstar:  # having this allows to avoid doing unnecessary actions for bfs
                # remove paper coord from coords
                paper_coords.remove([new_row, new_column])
                # new_closest_objective = problem.find_new_closest_objective(state, paper_coords, no_paper,
                #                                                            [new_row, new_column])

        goal = state.goal
        if new_grid[new_row][new_column] == 'X' and state.no_paper == 0:
            goal = True
            new_grid[new_row][new_column] = '@'

        #condition to make sure we don;t accidentally erase the "X" when there is still paper to take
        # if new_grid[new_row][new_column] != 'X' and state.no_paper >= 0:
        new_grid[new_row][new_column] = '@'

        # new_grid[new_row][new_column] = '@'

        if(state.isAstar):
            new_closest_objective = problem.find_new_closest_objective(state, paper_coords, no_paper,
                                                                   [new_row, new_column])

        return State(new_grid, problem.transform_list_to_tuple(new_grid), goal, no_paper, paper_coords,
                     state.door_position,
                     [new_row, new_column], state.isAstar, new_closest_objective)

    def goal_test(self, state):
        # if goal is true then we have reached the goal
        return state.goal

    def h(self, node):
        """down left is  (0,0)"""
        if node.state.isAstar:
            #check sum + the reduced path eg
            #nopaper * length constant + path length goal
            # use heuristic
            # by multiplying by number of paper left we force the algorithm to prioritise those with the least amount of
            # paper left to take ie we force to finish the almost finished algorithm
            # return distance(node.state.person_position, node.state.closest_objective) * (node.state.no_paper) #not admissible but will give a very good approximation
            # return node.state.no_paper
            return distance(node.state.person_position, node.state.closest_objective)  #will explore less
        else:  # we are using bfs and don't need a heuristic
            return 0.0

    def load(path):
        with open(path, 'r') as f:
            lines = f.readlines()

        state = State.from_string(''.join(lines))
        return PageCollect(state)


###############
# State class #
###############
class State:
    def __init__(self, grid, grid_tuple=None, goal=False, no_paper=None, paper_coords=None, door_position=None,
                 person_position=None, isAstar=False, closest_objective=None):
        self.nbr = len(grid)
        self.nbc = len(grid[0])
        self.grid = grid

        # these are parameters added to increase the speed

        self.grid_tuple = grid_tuple  # allows us to hash the grids
        self.no_paper = no_paper  # we have not achieved the final goal untill all the paper is collected
        self.paper_coords = paper_coords  # so that we can use the heuristic on the coordinates
        self.door_position = door_position  # so that we can use the heuristic on the coordinates
        self.person_position = person_position  # positon of the person so that we don't have to search for each iteration
        self.goal = goal  # turn true when we have no more paper and we are at the door
        self.closest_objective = closest_objective  # this allows us to avoid researching the closest objective
        self.isAstar = isAstar  # we added this value to allow optimisations in case we use bfs or astar

    # def __str__(self):
    #     '\n'.join(''.join(row) for row in self.grid)
    def __str__(self):
        s = "\n"
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


def print_info(problem):
    print("grid ")
    print(problem.initial.grid)
    print("grid_list")
    print(problem.initial.grid_tuple)
    print("number of paper left")
    print(problem.initial.no_paper)
    print("paper coords")
    print(problem.initial.paper_coords)
    print("position of person")
    print(problem.initial.person_position)
    print("position of door")
    print(problem.initial.door_position)


#####################
# Launch the search #
#####################
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: ./pagecollect.py <path_to_instance_file>")

    problem = PageCollect.load(sys.argv[1])


    problem.initial.no_paper, problem.initial.paper_coords, problem.initial.person_position, problem.initial.door_position = find_details(
        problem.initial.grid)

    problem.initial.grid_tuple = problem.transform_list_to_tuple(problem.initial.grid)  # this way we can hash the grid

    # print_info(problem)

    # IF YOU ARE USING BFS PUT FALSE this will allow optimisations for bfs
    problem.initial.isAstar = False

    if (problem.initial.isAstar):
        problem.initial.closest_objective = problem.find_new_closest_objective(problem.initial,
                                                                               problem.initial.paper_coords,
                                                                               problem.initial.no_paper,
                                                                               problem.initial.person_position)

    start_timer = time.perf_counter()
    # node, explored, frontier = astar_search(problem)
    # node = astar_search(problem)
    # node, explored, frontier = breadth_first_graph_search(problem)
    node = breadth_first_graph_search(problem)
    end_timer = time.perf_counter()
    # example of print
    # print(node.state)
    path = node.path()

    # print('Number of moves: ' + str(node.depth))
    for n in path:
        # print(n.state.no_paper)  # assuming that the __str__ function of state outputs the correct format
        # print(n.state.person_position)
        print(n.state)

    # print("* Execution time:\t", str(end_timer - start_timer))
    # print("* Path cost to goal:\t", node.depth, "moves")
    # print("nodes", explored)
    # print("frontier", frontier)
