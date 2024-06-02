""" U ovom modulu je implementirana metrika za izracunavanje ugnjezdenosti cvora. """
import igraph as ig
from math import *
from pprint import pprint as pp

# from cryptography.hazmat.backends.openssl.decode_asn1 import _decode_name_constraints

# g = ig.Graph.Read_Pajek("karate.paj")


# Primer metoda od Berine Hogan-a koji racuna BC (promene nacinio
# Tamas Nepusz) - Ovo predstavlja NORMALIZACIJU Betweenness
# Centrality metrike:
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
    """ Ovaj metod implementira pretrazivanje u SIRINU (BFS) algoritam
        da obidje stablo pocevsi od cvora 'start'.

        Args:
            start: Node from traversing starts
        Params:
            visited:                Skup cvoreva koji su poseceni prolaskom kroz stablo
            queue:                  Red opsluzivanja u vidu liste koji cuva cvorove koji u procesu za posecivanje
            start:                  Pocetni/korenski cvor od kog se zapocinje izvrsavanje BFS algoritma
            tekuci:                 cvor koji je PRVI 'skinut' sa reda cekanja 'queue'
            susedi_tekuci_indexes:  lista indeksa susednih cvorova cvora 'tekuci'
            susedi_tekuci:          VertexSeq, tj. lista koja sadrzi elemente tipa Vertex koji su incidentni sa cvorom 'tekuci'
            mat_d:                  matrica distanci izmedju 2 razlicita cvora u 'g' grafu
            mat_p:                  matrica sa brojem najkracih puteva izmedju 2 razlicita cvora u 'g' grafu
    """
    visited = set()  # incijalizacija praznog skupa
    queue = list()
    visited.add(start)
    queue.append(start)

    while queue != []:  # TESTIRAJ bool(visited) uslov!
        tekuci = queue.pop(0)  # brise PRVI cvor sa liste 'queue' i vraca isti element
        susedi_tekuci_indexes = g.neighbors(tekuci)  # vraca listu indeksa susednih cvorova cvora 'tekuci'
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
    print "tip 'g' objekta:", type(g)

    # incijalizacija vrednosti elemenata matrice distanci
    mat_d = [[0 for cols in range(g.vcount())] for rows in range(g.vcount())]
    # incijalizacija vrednosti elemenata matrice broja NAJKRACIH puteva
    mat_p = [[0 for edge in range(g.vcount())] for edges in range(g.vcount())]

    compute_d_and_p_matrices(g)
    print "len(mat_d) =", len(mat_d), ", mat_d =", mat_d  # PROVERI na INTERNETU dimenzije matrice DISTANCI !!!!
    print "len(mat_p) =", len(mat_p), ", mat_p =", mat_p  # PROVERI na INTERNETU dimenzije matrice PUTEVA!!!

    print "Stigao na KRAJ!"
