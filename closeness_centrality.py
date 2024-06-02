""" Implementacija algoritma za racunanje Closeness Centrality  metrike u NEUSMERENIM
    NETEZINSKIM grafovima/mrezama

    Osnovna pretpostavka: VAZNI/BITNI cvorovi su BLIZU ostalim cvorovima u grafu,
    tj. nalaze se na najkracem putu u grafu. Dakle, sto se cvor nalazi na kracem
    putu izmedju svaka dva cvora u grafu onda mu je centralnost bliskosti (CC) VECA!
"""
import igraph as ig


def popuni_matricu_distanci(g):
    for cvor in g.vs:
        bfs(g, cvor)


def bfs(g, start):
    """
    Argumenti:
        g:     Graf nad kojim se izvrsava BFS algoritam
        start: Pocetni cvor od kog se pocinje izvrsavanje BFS algoritma
    Parametri:
        visited:               Skup posecenih cvorova
        queue:                 Lista cvorova koji treba da se posete, tj. "red cekanja"/buffer za cvorove
        tekuci:                Cvor koji je PRVI 'skinut' sa reda cekanja 'queue'
        susedi_tekuci_indexes: Lista indeksa susednih cvorova cvora 'tekuci'
        susedi_tekuci:         VertexSeq, tj. lista koja sadrzi elemente tipa Vertex koji su incidentni sa cvorom 'tekuci'
        matrica_d:             Matrica distanci izmedju 2 razlicita cvora
    """
    visited = set()
    queue = list()
    visited.add(start)
    queue.append(start)

    while queue != []:
        # print "queue =", queue
        tekuci = queue.pop(0)
        # print "tekuci = {}, type(tekuci) = {}".format(tekuci, type(tekuci))
        susedi_tekuci_indexes = g.neighbors(tekuci)
        susedi_tekuci = g.vs.select(
            susedi_tekuci_indexes)  # vraca podsekvencu cvorova na osnovu INDEKSA susednih cvorova
        for sused in susedi_tekuci:
            if sused not in visited:
                visited.add(sused)
                queue.append(sused)
                matrica_d[start.index][sused.index] = matrica_d[start.index][tekuci.index] + 1


def closeness_centrality_norm(g):
    """ Ovaj metod vrsi racunanje metrike za normalizovanu formu formule
        za centralnost bliskosti za SVE cvorove u 'g' grafu.

        Args:
            g: Graf
            z: cvor 'g' grafa

        Normalizovana FORM(UL)A:
            C_c(z) = (N-1) / sum_ieV(d_zi), za i<>z
            gde N oznacava broj cvorova u tekucem grafu

            * IZUZETAK - u VELIKIM grafovima razlika N-1 postaje NEVAZNA, pa onda formula izgleda ovako:
                  N / sum_ieV(d_zi), za i<>z
            ovo omogucava POREDJENJE cvorova grafova RAZLICITIH velicina!

        Parametri (formule):
            V: skup cvorova 'g' grafa
            ieV: oznacava i-ovi pripadaju skupu V (cvorova grafa)
            d_zi: distanca izmedju cvora 'z' i cvora 'i'

        Returns:
            Vrednost izmedju 0-1 -> Ova vrednost je inverzno proporcionalna sa kumulativnom
            distancom izmedju 'z' i OSTALIM cvorevima u 'g' grafu.
    """

    lista_cc_norm = list()
    cvor_id = 1  # prati ID cvora grafa 'g'
    N = g.vcount()

    for row in matrica_d:
        # print "{}. row = {}".format(cvor_id,row)
        sum = 0.0
        for distance in row:
            sum += distance
        ret = (N - 1) / sum
        lista_cc_norm.append([cvor_id, ret])
        cvor_id += 1

    lista_cc_norm.sort(key=lambda lis: lis[1], reverse=True)
    return lista_cc_norm


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
    # NAPRAVI jos 3 grafa i nad njima testiraj ovu centralnost
    g = ig.Graph.Read_Pajek("karate.paj")
    # g = ig.Graph.Read_Pajek("power_grid.net")
    print g.summary()

    # inicijalizacija matrice distanci
    matrica_d = [[0 for cols in range(g.vcount())] for rows in range(g.vcount())]

    """ Popunjavanje matrice vrednostima koje oznacavaju udaljenost
        za odredjeni cvor do ostalih cvorova u 'g' grafu """
    popuni_matricu_distanci(g)
    # popuni_matricu_distanci(g2)

    cc_cvoreva_g1_igraph = g.closeness(vertices=None)  # vraca Closeness za SVE CVOROVE u grafu 'g'
    sorted_rang_list = sortiraj_listu_rangova(cc_cvoreva_g1_igraph)

    print "\n==========================================="
    print "sorted_rang_list (igraph):"
    stampaj_listu(sorted_rang_list[0:10])

    print "\n============================================="
    print "sortirana lista_rangiranih_lista_cc_norm_ns:"
    lista_rangiranih_lista_cc_norm_ns = closeness_centrality_norm(g)
    stampaj_listu(lista_rangiranih_lista_cc_norm_ns[0:10])

    print "\nStigao na  'closeness_centralnost.py' modula!"
