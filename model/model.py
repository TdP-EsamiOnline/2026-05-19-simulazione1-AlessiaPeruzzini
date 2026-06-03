import copy

import networkx as nx
from networkx import DiGraph

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._artisti = []
        self._idMapP = {}
        self._bestPath = []
        self._bestScore = 0


    def getBestPath(self, start):
        self._bestPath = []
        self._bestScore = 0

        parziale = [start]
        self._ricorsione(parziale)

        return self._bestPath, self._bestScore

    def _ricorsione(self, parziale):

        if len(parziale) > len(self._bestPath):
            self._bestPath = parziale.copy()
            self._bestScore = self._getScore(parziale)

        for n in self._graph.successors(parziale[-1]):

            if n not in parziale:

                if len(parziale) == 1:
                    parziale.append(n)
                    self._ricorsione(parziale)
                    parziale.pop()

                else:
                    ultimoPeso = self._graph[parziale[-2]][parziale[-1]]["weight"]
                    nuovoPeso = self._graph[parziale[-1]][n]["weight"]

                    if nuovoPeso > ultimoPeso:
                        parziale.append(n)
                        self._ricorsione(parziale)
                        parziale.pop()

    def _getScore(self, parziale):
        score = 0
        for i in range(0, len(parziale) - 1):
            score += self._graph[parziale[i]][parziale[i + 1]]["weight"]
        return score



    def buildGraph(self, gen):
        self._graph.clear()
        self._artisti = DAO.getAllNodes(gen)
        for a in self._artisti:
            self._idMapP[a.ArtistId] = a

        self._graph.add_nodes_from(self._artisti)
        allEdges = DAO.getAllEdges(gen, self._idMapP)
        for a in allEdges:
            self._graph.add_edge(a.a1, a.a2, weight=a.peso)

    def getinfluenzaArtista(self):
        listNodesPesata = []
        for n in self._graph.nodes:
            score = 0
            for e in self._graph.out_edges(n, data=True):
                score += e[2]["weight"]
            for e in self._graph.in_edges(n, data=True):
                score -= e[2]["weight"]
            listNodesPesata.append((n, score))

        listNodesPesata.sort(key=lambda x:x[1], reverse=True)
        #print (listNodesPesata)
        return listNodesPesata[0]

    def getTop5Archi(self):
        #MI DA GLI ARCHI DI PESO MAGGIORE
        lista5Top = sorted (self._graph.edges(data = True), key = lambda x:x[2]["weight"], reverse=True )  #SORTAMELI ER PESI DAL PIù PICCOL OAL PIù GRANDE
        return lista5Top[0:5]


    def getAllGenere(self):
        return DAO.getAllGenere()

    def graphDetail(self):
        return len(self._graph.nodes), len(self._graph.edges)


