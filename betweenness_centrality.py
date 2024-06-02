import igraph as ig
from math import *
from pprint import pprint as pp

# from cryptography.hazmat.backends.openssl.decode_asn1 import _decode_name_constraints

# g = ig.Graph.Read_Pajek("karate.paj")

# Method example of Berine Hogan-a which calculates BC. This represents normalization
# of Betweenness Centrality metric:


def betweenness_centralization(g):
    vnum = g.vcount()
    if vnum < 3:
        raise ValueError("Graph must have at least 3 vertices")
    denom = (vnum - 1) * (vnum - 2)
    temparr = [2 * i / denom for i in g.betweeness()]
    max_temparr = max(temparr)
    return sum(max_temparr - i for i in temparr) / (vnum - 1)


def compute_d_and_p_matrices(g):
    for n in g.vs:
        bfs(g, n)


def bfs(g, start):
    """ This method implemenents Breadth-First-Search (BFS) algorithm to traverse tree begging from "start" vertice. 

        Args:
            start: Node from traversing starts
        Params:
            visited:                Set of vertices which are visited during traversal of tree.
            queue:                  Queue represented as a list which stores vertices which are in traversal process.
            start:                  Pocetni/korenski cvor od kog se zapocinje izvrsavanje BFS algoritma
            start:                  Start/root vertice from which execution of BFS algorithm is started.
            tekuci:                 vertice which has been poped from queue named `queue`
            susedi_tekuci_indexes:  list of indicies of vertices adjacent to `tekuci` vertice
            susedi_tekuci:          VertexSeq, tj. list containing elements of Vertex type which are incident to the the `tekuci` vertice
            mat_d:                  Distance matrix which represents distances between 2 different vertices in 'g' graph
            mat_p:                  Shortest path numbers matrix which contains number of shortest paths between 2 diffrent nodes in 'g' graph
    """
    visited = set()  # initialze empty set
    queue = list()
    visited.add(start)
    queue.append(start)

    while queue != []:  # TEST bool(visited) condition!
        # removes FIRST node from `queue` list and returns same removed element
        tekuci = queue.pop(0)
        # returns list of indices of adjacent vertices to 'tekuci' vertice
        susedi_tekuci_indexes = g.neighbors(tekuci)
        susedi_tekuci = g.vs.select(susedi_tekuci_indexes)

        for sused in susedi_tekuci:
            if sused not in visited:
                visited.add(sused)
                queue.append(sused)

                mat_d[start.index][sused.index] = mat_d[start.index][tekuci.index] + 1
                if (tekuci == start):
                    mat_p[start.index][sused.index] = 1
                else:
                    mat_p[start.index][sused.index] = mat_p[start.index][tekuci.index]
            else:
                if (mat_d[start.index][sused.index] == mat_d[start.index][tekuci.index] + 1):
                    mat_p[start.index][sused.index] += mat_p[start.index][tekuci.index]


def betwenness_centrality(g):
    list_bc = []
    return list_bc


def sortiraj_listu_rangova(nesortirana_lista):
    sortirana_lista = []
    cvor_id = 1

    for value in nesortirana_lista:
        sortirana_lista.append([cvor_id, value])
        cvor_id += 1

    sortirana_lista.sort(key=lambda lis: lis[1], reverse=True)
    return sortirana_lista


def stampaj_listu(lista):
    for row in lista:
        print row


if __name__ == '__main__':
    g = ig.Graph.Read_Pajek("karate.paj")
    print "type of 'g' object:", type(g)

    # initializating element values of Distance Matrix
    mat_d = [[0 for cols in range(g.vcount())] for rows in range(g.vcount())]
    # initializing element values of Shortest path numbers matrix
    mat_p = [[0 for edge in range(g.vcount())] for edges in range(g.vcount())]

    compute_d_and_p_matrices(g)
    print "len(mat_d) =", len(mat_d), ", mat_d =", mat_d
    print "len(mat_p) =", len(mat_p), ", mat_p =", mat_p
    print "Reached the end!"
