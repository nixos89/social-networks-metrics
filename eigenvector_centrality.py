import igraph as ig
import networkx as nx
from math import *
import operator


def eg_centrality_ns(g, max_steps, eps):
    N = g.vcount()
    ec = [0.0 for x in range(N)]
    ec_prim = [0.0 for x in range(N)]

    for i in range(N):
        ec[i] = 1.0 / N

    num_steps = 0
    convergence = False
    while (num_steps < max_steps and not convergence):
        for i in range(N):
            ec_prim[i] = 0.0
            susedi_i_cvora_indeksi = g.neighbors(i)
            susedi_i_cvora = g.vs.select(susedi_i_cvora_indeksi)
            for sused in susedi_i_cvora:
                ec_prim[i] += ec[sused.index]

        # normiranje ec_prim - POCETAK
        c = 0.0
        for i in range(N):
            c += ec_prim[i]

        # print "c =", c
        for i in range(N):
            ec_prim[i] = ec_prim[i] / sqrt(c)

        for i in range(N):
            convergence = abs(ec_prim[i] - ec[i]) < eps

        for i in range(N):
            ec[i] = ec_prim[i]

        num_steps += 1

    return ec_prim


def sortiraj_listu_rangova(nesortirana_lista):
    sortirana_lista = []
    cvor_id = 1

    for value in nesortirana_lista:
        sortirana_lista.append([cvor_id, value])
        cvor_id += 1

    sortirana_lista.sort(key=lambda lis: lis[1], reverse=True)
    return sortirana_lista


def sortiraj_dict(nesortirani_dict):
    sortirana_list_od_dict = []
    sortirana_list_od_dict = sorted(nesortirani_dict.items(), key=operator.itemgetter(1), reverse=True)
    # print "type(sortirana_list_od_dict) =", type(sortirana_list_od_dict)
    return sortirana_list_od_dict


def stampaj_listu(lista):
    for row in lista:
        print row


if __name__ == '__main__':
    # g = ig.Graph.Read_Pajek("karate.paj")
    g = ig.Graph.Read_Pajek("power_grid.net")
    g_nx_multigraph = nx.read_pajek("power_grid.net")
    g_nx = nx.Graph(g_nx_multigraph)
    print g.summary()
    print "type(g_nx) =", type(g_nx)

    ig_ev_c_list = g.eigenvector_centrality(scale=True)
    sorted_ig_list = sortiraj_listu_rangova(ig_ev_c_list)
    print "\nLista vrednosti Eigenvector centralnosti (igraph implementacija):"
    stampaj_listu(sorted_ig_list[0:10])

    ng_ev_c_dict = dict()
    ng_ev_c_dict = nx.eigenvector_centrality(g_nx)
    print "\nLista vrednosti Eigenvector centralnosti (NetworkX implementacija):"
    sortirana_list_od_dict = []
    sortirana_list_od_dict = sortiraj_dict(ng_ev_c_dict)
    stampaj_listu(sortirana_list_od_dict[0:10])

    lista_eigenvec_c_ns = eg_centrality_ns(g, max_steps=5000, eps=1.0e-6)
    sorted_lista_eigenvec_c_ns = sortiraj_listu_rangova(lista_eigenvec_c_ns)
    print "\nLista vrednosti Eigenvector centralnosti (NS implementacija):"
    stampaj_listu(sorted_lista_eigenvec_c_ns[0:10])
