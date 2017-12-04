from matplotlib import pyplot as plt
from random import randint


class Graph:
    def __init__(self, adjacent_list=None, v=None, edges_list=None, colors=None):
        if adjacent_list is not None:
            self.V = len(adjacent_list)
            self.E = sum(len(e) for e in adjacent_list)
            self.vertices = adjacent_list
        elif v is not None and edges_list is not None:
            self.V = v
            self.E = len(edges_list)
            self.vertices = [[] for _ in range(v)]
            for e in edges_list:
                self.vertices[e[0]].append(e[1])
                self.vertices[e[1]].append(e[0])
        else:
            self.V = 0
            self.E = 0
            self.vertices = None
        if colors is None:
            self.colors = [randint(0, 1) for _ in range(self.V)]
        else:
            self.colors = colors
        self.discrepancy = []
        self.total_discrepancy = 0
        self.positive_d, self.negative_d = 0, 0
        self.init_discrepancy()

    def worst_graph(self, n, colors=None):
        self.V = 4 * n + 1
        self.E = 5 * n
        self.vertices = [[] for _ in range(self.V)]
        for i in range(n):
            self.vertices[0].append(4 * i + 1)
            self.vertices[0].append(4 * i + 4)
            self.vertices[4 * i + 1] .append(0)
            self.vertices[4 * i + 1] .append(4 * i + 2)
            self.vertices[4 * i + 2] .append(4 * i + 1)
            self.vertices[4 * i + 2] .append(4 * i + 3)
            self.vertices[4 * i + 3] .append(4 * i + 2)
            self.vertices[4 * i + 3] .append(4 * i + 4)
            self.vertices[4 * i + 4] .append(4 * i + 3)
            self.vertices[4 * i + 4] .append(0)
        if colors is None:
            self.colors = [randint(0, 1) for _ in range(self.V)]
        else:
            self.colors = colors
        self.init_discrepancy()
        return self

    def worst_graph_worst_cut(self, n):
        self.worst_graph(n, [(i // 2) % 2 for i in range(4 * n + 1)])
        return self

    def random_graph(self, v, e):
        self.V = v
        self.E = e
        self.vertices = [[] for _ in range(v)]
        for _ in range(e):
            v1 = randint(0, v - 1)
            v2 = randint(0, v - 2)
            v2 += (v2 >= v1)
            self.vertices[v1].append(v2)
            self.vertices[v2].append(v1)
        self.colors = [randint(0, 1) for _ in range(v)]
        self.init_discrepancy()
        return self

    def init_discrepancy(self):
        self.discrepancy = [0] * self.V

        for i in range(self.V):
            for v in self.vertices[i]:
                self.discrepancy[i] += -1 + 2 * (self.colors[i] == self.colors[v])
            self.positive_d += self.discrepancy[i] > 0
            self.negative_d += self.discrepancy[i] < 0

        self.total_discrepancy = sum(self.discrepancy)

    def worth_flip(self, i):
        return self.discrepancy[i] >= 0

    def flip(self, i):
        self.colors[i] = 1 - self.colors[i]
        # after the flip all the bad edges become the good ones and vice versa
        # so the discrepancy of the flipped vertex becomes reversed (over zero):
        self.total_discrepancy -= 2 * self.discrepancy[i]
        self.discrepancy[i] *= -1
        if self.discrepancy[i] > 0:
            self.positive_d += 1
            self.negative_d -= 1
        elif self.discrepancy[i] < 0:
            self.positive_d -= 1
            self.negative_d += 1
        # also we should change the discrepancy of all the adjacent vertices
        for vertex in self.vertices[i]:
            if self.colors[vertex] == self.colors[i]: # then this edge has become a "bad" edge
                self.discrepancy[vertex] += 2
                # now we should recalculate the number of vertices of ech type
                self.positive_d += self.discrepancy[vertex] in (1, 2)
                self.negative_d -= self.discrepancy[vertex] in (0, 1)
                # self.zero_d += (self.discrepancy[vertex] == 0) - (self.discrepancy[vertex] == 2)
            else: # the edge has become a good one
                self.discrepancy[vertex] -= 2
                # and recalculate number of vertices of each type
                self.positive_d -= self.discrepancy[vertex] in (-1, 0)
                self.negative_d += self.discrepancy[vertex] in (-2, -1)
                # self.zero_d += (self.discrepancy[vertex] == 0) - (self.discrepancy[vertex] == -2)

    def stats(self):
        return self.total_discrepancy, self.positive_d, self.V - self.positive_d - self.negative_d

def evo_run(graph):
    d, p, z = graph.stats()
    d_track, p_track, z_track = [d], [p], [z + p]
    while d > 0:
        i = randint(0, graph.V - 1)
        if graph.worth_flip(i):
            graph.flip(i)

        d, p, z = graph.stats()
        d_track.append(d)
        p_track.append(p)
        z_track.append(z + p)
    iterations = len(d_track)
    if iterations == 1: return
    plt.plot(range(iterations), [graph.V] * iterations, 'go-')
    plt.plot(range(iterations), p_track, 'bo-')
    plt.plot(range(iterations), z_track, 'ro-')
    plt.plot(range(iterations), d_track, 'g-')
    plt.show()

for i in range(10):
    print(i)
    evo_run(Graph().random_graph(100, 1000))

# res = [12.14, 12.02, 10.6, 10.99, 13.15, 13.12, 14.95, 15.38, 16.84, 17.94, 18.05, 19.72, 21.46, 21.02, 25.34, 25.15, 36.31, 36.52, 37.62, 38.81, 39.88, 43.54, 43.83, 46.77, 44.59, 43.95, 47.59, 48.08, 47.92, 51.82, 52.43, 52.86, 60.25, 61.39, 61.58, 61.79, 67.57, 67.59, 64.38, 73.43, 75.12, 72.29, 78.45, 76.98, 76.12, 79.51, 78.55, 79.76, 92.9, 90.95, 92.11, 92.82, 91.52, 94.99, 92.0, 97.42, 98.9, 101.43, 102.78, 100.09, 101.44, 108.58, 108.04, 110.03, 113.1, 122.43, 118.09, 123.05, 125.12, 128.57, 125.03, 128.51, 123.08, 125.64, 130.61, 134.96, 134.12, 135.36, 130.88, 134.02, 148.23, 146.42, 149.34, 152.48, 149.01, 155.18, 153.68, 153.23, 154.71, 163.43, 151.85, 157.47, 165.35, 161.86, 171.78, 166.88, 173.67, 174.99, 175.11]

# for n in range(1, 100):
#     expected_runtime = sum([evo_run(Graph(n)) for _ in range(100)]) / 100
#     res.append(expected_runtime)
#     print(expected_runtime)

# print(res)
#
# plt.plot(range(1, 100), res, 'bo-')
# plt.plot(range(1, 100), [1.75 * i for i in range(1, 100)], 'ro-')
# plt.show()