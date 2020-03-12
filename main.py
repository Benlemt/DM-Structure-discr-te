import networkx as nx
import matplotlib.pyplot as plt

filename = "graph.txt"
G = nx.DiGraph()


def build_graph(ins):
    for line in ins:
        if len(line) == 2:
            G.add_node(line[0])
        elif len(line) == 4 or len(line) == 3:
            node_start = line[0]
            node_end = line[2]
            G.add_edge(node_start, node_end)


def create_matrix_h(graph):
    matrix = []
    nodes = []

    for i in graph.nodes:
        nodes.append(i)

    for node in graph:
        temp = [0] * graph.number_of_nodes()
        for node_neighbors in graph[node]:
            temp[nodes.index(node_neighbors)] = 1
        matrix.append(temp)
    return matrix


def create_matrix_s(matrix_h):
    matrix_s = matrix_h.copy()

    for i in range(0, len(matrix_s)):
        number_one = matrix_s[i].count(1)
        for j in range(0, len(matrix_s[i])):
            if matrix_s[i][j] == 1:
                matrix_s[i][j] = matrix_s[i][j] / number_one
    return matrix_s.copy()


def update_matrix_s(s):
    for i in range(0, len(s)):
        if s[i] == [0] * len(s):
            for j in range(0, len(s[i])):
                s[i][j] = 1 / len(s)
    return s


def create_google_matrix(s, alpha):
    for i in range(0, len(s)):
        for j in range(0, len(s[i])):
            s[i][j] = s[i][j] * alpha

    # create matrix E
    e = []
    for k in range(0, len(s)):
        temp = [1] * len(s)
        e.append(temp)

    pg = 1 / len(s)

    for i in range(0, len(e)):
        for j in range(0, len(e[i])):
            e[i][j] = e[i][j] * pg * (1 - alpha)

    # S * E
    g = s.copy()
    for i in range(0, len(g)):
        for j in range(0, len(g[i])):
            g[i][j] = g[i][j] + e[i][j]

    return g


def init_pagerank(g):
    return [1 / len(g)] * len(g)


def calc_pagerank(pg_init, g):
    pg = [0] * len(g)
    for i in range(0, len(g)):
        for j in range(0, len(g[i])):
            pg[i] += pg_init[i] * g[j][i]
    return pg


with open(filename) as f:
    content = f.readlines()

build_graph(content)

h = create_matrix_h(G)
s = create_matrix_s(h)
s = update_matrix_s(s)
g = create_google_matrix(s, 0.85)
pg_init = init_pagerank(g)

pg = calc_pagerank(pg_init, g)
print(pg)


nx.draw(G, with_labels=True)
plt.show()

