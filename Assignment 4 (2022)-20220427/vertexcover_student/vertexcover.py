#! /usr/bin/env python3
"""NAMES OF THE AUTHOR(S): Nicolas Golenvaux <nicolas.golenvaux@uclouvain.be>"""
from search import *
import sys
import time
import numpy

covers = set()  # think of symetric states
node_to_modify = 0

#

class VertexCover(Problem):


    # if you want you can implement this method and use it in the maxvalue and randomized_maxvalue functions
    def successor(self, state):
        states = []
        for node_to_change in range(len(state.cover)):
            for new_node in state.not_cover:
                new_cover = state.cover.copy()
                if new_node not in state.cover:  # so that we don't retake the same node
                    new_cover[node_to_change] = new_node
                    # print(new_cover)
                    new_cover.sort()
                    tuple_cover = tuple(new_cover)
                    states.append((0, State(state.k, state.vertices, state.edges, cover=new_cover)))
                    covers.add(tuple_cover)
        return tuple(states)

    # if you want you can implement this method and use it in the maxvalue and randomized_maxvalue functions
    def value(self, state):
        # edges captured - nodes
        used_edges = set()
        edges_covered = 0
        for node in state.cover:
            for edge in state.vertices[node]:  # it give the list of edges taken
                if edge not in used_edges:
                    edges_covered += 1
                    used_edges.add(edge)
        # print("in edges")
        # print(edges_covered)
        return edges_covered


class State:

    def __init__(self, k, vertices, edges, cover=None, not_cover=None):  # perhaps take a good inital cover
        self.k = k
        self.n_vertices = len(vertices)
        self.n_edges = len(edges)
        self.vertices = vertices
        self.edges = edges
        if cover is None:
            self.cover = self.build_init()
        else:
            self.cover = cover
        if not_cover is None:
            self.not_cover = [v for v in range(self.n_vertices) if v not in self.cover]
        else:
            self.not_cover = not_cover

    # an init state building is provided here but you can change it at will
    def build_init(self):
        return list(range(self.k))

    def __str__(self):
        s = ''
        for v in self.cover:
            s += ' ' + str(v)
        return s



def read_instance(instanceFile):
    file = open(instanceFile)
    line = file.readline()
    k = int(line.split(' ')[0])
    n_vertices = int(line.split(' ')[1])
    n_edges = int(line.split(' ')[2])
    vertices = {}
    for i in range(n_vertices):
        vertices[i] = []
    edges = {}
    line = file.readline()
    while line:
        [edge, vertex1, vertex2] = [int(x) for x in line.split(' ')]
        vertices[vertex1] += [edge]
        vertices[vertex2] += [edge]
        # if vertex1 > vertex2:
        #     edges[(vertex2, vertex1)] = edge
        # else:
        #     edges[(vertex1,vertex2)] = edge
        edges[edge] = (vertex1, vertex2)
        line = file.readline()
    return k, vertices, edges


# Attention : Depending of the objective function you use, your goal can be to maximize or to minimize it
# def cost_function(node): #we are searching for all the edges
# edges - nodes


def maxvalue(problem, limit=100, callback=None):
    # current = LSNode(problem, problem.initial, 0)
    # best = current
    current = LSNode(problem, problem.initial, 0)
    best = current
    best_step = 100
    for step in range(limit):
        if callback is not None:
            callback(current)
            #we need to create a list of best nodes
        neighbours = [(state.value(), state) for state in list(current.expand())]
        neighbours.sort(key= lambda a: a[0], reverse=True)
        current = neighbours[0][1]
        # current = random.choice(list(current.expand()))
        if current.value() > best.value():
            best = current
            best_step = step

    return best


# Attention : Depending of the objective function you use, your goal can be to maximize or to minimize it
def randomized_maxvalue(problem, limit=100, callback=None):

    current = LSNode(problem, problem.initial, 0)
    best = current
    best_step = 100
    for step in range(limit):
        if callback is not None:
            callback(current)
            # we need to create a list of best nodes
        neighbours = [(item.value(), item) for item in list(current.expand())]
        neighbours.sort(key=lambda a: a[0], reverse=True)
        # current = neighbours[0][1]
        current = random.choice(neighbours[:5])[1]
        # print(neighbours)
        # print(current)
        if current.value() > best.value():
            best = current
            best_step = step

    return best,best_step


#####################
#       Launch      #
#####################
if __name__ == '__main__':
    info = read_instance(sys.argv[1])
    init_state = State(info[0], info[1], info[2])
    vc_problem = VertexCover(init_state)

    step_limit = vc_problem.initial.n_edges * vc_problem.initial.n_vertices
    start = time.perf_counter()
    node, step = randomized_maxvalue(vc_problem, step_limit)
    # node,step = maxvalue(vc_problem, limit=step_limit)
    # node = random_walk(vc_problem, step_limit)
    end = time.perf_counter()
    time_maxval = end-start
    steps_maxval = step
    val_maxval = node.value()

    total_time= 0
    total_steps= 0
    total_value = 0
    for i in range(10):

        start = time.perf_counter()
        node,step = randomized_maxvalue(vc_problem, step_limit)
        # node,step = maxvalue(vc_problem, limit=step_limit)
        # node = random_walk(vc_problem, step_limit)
        end = time.perf_counter()
        time_spent = end - start
        total_time += time_spent
        total_value += node.value()
        total_steps += step

    total_time = total_time / 10
    total_value = int(total_value / 10)
    total_steps = total_steps/10

    total_time_2 = 0
    total_steps_2 = 0
    total_value_2 = 0
    for i in range(10):
        start = time.perf_counter()
        # node, step = randomized_maxvalue(vc_problem, step_limit)
        # node,step = maxvalue(vc_problem, limit=step_limit)
        node,step = random_walk(vc_problem, step_limit)
        end = time.perf_counter()
        time_spent = end - start
        total_time_2 += time_spent
        total_value_2 += node.value()
        total_steps_2 += step

    total_time_2 = total_time_2 / 10
    total_value_2 = total_value_2 / 10
    total_steps_2 = total_steps_2 / 10
    print(" &  " + str(time_maxval) + " & "+ str(val_maxval) + " & "+ str(steps_maxval) + " & " + str(total_time) + " & " + str(total_value) + " & " + str(total_steps) + "& " + str(total_time_2) + " & " + str(total_value_2) + " & " + str(total_steps_2) +"\\\\")

    # state = node.state
    # node, step = randomized_maxvalue(vc_problem, step_limit)
    # node,step = maxvalue(vc_problem, limit=step_limit)
    # node = random_walk(vc_problem, step_limit)
    # print(state)
