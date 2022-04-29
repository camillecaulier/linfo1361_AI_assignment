#! /usr/bin/env python3
"""NAMES OF THE AUTHOR(S): Nicolas Golenvaux <nicolas.golenvaux@uclouvain.be>"""
from search import *
import sys
from queue import PriorityQueue
import random as rand

covers = set()  # think of symetric states
node_to_modify = 0

#

class VertexCover(Problem):


    # if you want you can implement this method and use it in the maxvalue and randomized_maxvalue functions
    def successor(self, state):
        queue = PriorityQueue()  # to make is max we will have to inverse the things
        # change the order of what to take
        n_vertices = state.n_vertices
        # node_to_change = rand.randint(0, n_vertices)
        # while(node_to_change not in state.cover):
        #     node_to_change = rand.randint(0, state.n_vertices)
        node_to_change = rand.randint(0, state.k-1)
        # global node_to_modify
        # node_to_modify += 1
        # node_to_change = (node_to_modify)%state.k

        states = []
        for new_node in range(n_vertices):
            new_cover = state.cover.copy()
            if new_node not in state.cover:  # so that we don't retake the same node
                new_cover[node_to_change] = new_node
                # print(new_cover)
                new_cover.sort()
                tuple_cover = tuple(new_cover)
                states.append((0, State(state.k, state.vertices, state.edges, cover=new_cover)))
                covers.add(tuple_cover)
                # if tuple_cover not in covers:
                #     states.append((0, State(state.k, state.vertices, state.edges, cover=new_cover)))
                #     covers.add(tuple_cover)
                # create binary number
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
    for step in range(limit):
        if callback is not None:
            callback(current)
            #we need to create a list of best nodes
        neighbours = [(item.value(), item) for item in list(current.expand())]
        neighbours.sort(key= lambda a: a[0], reverse=True)
        current = neighbours[0][1]
        # current = random.choice(list(current.expand()))
        if current.value() > best.value():
            best = current

    return best


# Attention : Depending of the objective function you use, your goal can be to maximize or to minimize it
def randomized_maxvalue(problem, limit=100, callback=None):

    current = LSNode(problem, problem.initial, 0)
    best = current
    for step in range(limit):
        if callback is not None:
            callback(current)
            # we need to create a list of best nodes
        neighbours = [(item.value(), item) for item in list(current.expand())]
        neighbours.sort(key=lambda a: a[0], reverse=True)
        # current = neighbours[0][1]
        current = random.choice(neighbours[:5])[1]
        if current.value() > best.value():
            best = current

    return best


#####################
#       Launch      #
#####################
if __name__ == '__main__':
    info = read_instance(sys.argv[1])
    init_state = State(info[0], info[1], info[2])
    vc_problem = VertexCover(init_state)

    # print(vc_problem.initial)  # print the intial state
    # print("cover: " + str(vc_problem.initial.cover))
    # print("vertices: " + str(vc_problem.initial.vertices))
    # print("edges: " + str(vc_problem.initial.edges))
    # print("not_covered : " + str(vc_problem.initial.not_cover))

    step_limit = vc_problem.initial.n_edges * vc_problem.initial.n_vertices# * 2
    # node = randomized_maxvalue(vc_problem, step_limit)
    node = maxvalue(vc_problem, limit=step_limit)
    # node = random_walk(vc_problem, step_limit)
    state = node.state
    print(state)
