import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMap = {}
        self._optSet = []
        self._optScore = 0

    def buildGraph(self):
        self._graph.clear()
        nodes = DAO.getAllNodes()
        for n in nodes:
            self._idMap[n.AlbumId] = n
        self._graph.add_nodes_from(nodes)
        edges = DAO.getAllEdges(self._idMap)
        for e in edges:
            self._graph.add_edge(e.a1, e.a2)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getDettagli(self):
        components = list(nx.connected_components(self._graph))
        num_comp = len(components)
        largest_comp = max(components, key=len) if components else []
        subgraph = self._graph.subgraph(largest_comp)
        return num_comp, largest_comp, subgraph

    def getBestSet(self, source, N):
        self._optSet = []
        self._optScore = 0
        parziale = [source]
        tutte_le_comp = list(nx.connected_components(self._graph))
        comp_di_source = next(c for c in tutte_le_comp if source in c)
        comp_rimaste = [c for c in tutte_le_comp if source not in c]
        self._ricorsione_set(parziale, N, comp_rimaste)
        return self._optSet, self._optScore

    def _ricorsione_set(self, parziale, N, comp_rimaste):
        if len(parziale) == N:
            score = sum([nodo.listaBrani for nodo in parziale])
            if score > self._optScore:
                self._optScore = score
                self._optSet = list(parziale)
            return
        if len(comp_rimaste) == 0:
            return
        comp_attuale = comp_rimaste[0]
        comp_successive = comp_rimaste[1:]
        for nodo in comp_attuale:
            parziale.append(nodo)
            self._ricorsione_set(parziale, N, comp_successive)
            parziale.pop()
        self._ricorsione_set(parziale, N, comp_successive)
