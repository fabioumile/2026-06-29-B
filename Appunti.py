"""
film_ordinati = sorted(lista_film, key=lambda x: (-x.year, x.title)) 
ord desc anno a parita ord asc titolo   

#Main
import flet as ft
from model.model import Model
from UI.view import View
from UI.controller import Controller
def main(page: ft.Page):
    my_model = Model()
    my_view = View(page)
    my_controller = Controller(my_view, my_model)
    my_view.set_controller(my_controller)
    my_view.load_interface()
ft.app(target=main)

#View
class View:
    def __init__(self, page: ft.Page):
        self._page = page
        self._controller = None
        self.bottone1 = None #ddPD è dropdown
        self.bottone2 = None #elevatedbutton()
        self.bottone3 = None #on_click = self._nome_metodo, appena clicco parte quel metodo
    def loadInterface(self):
        #row3
        self._ddAeroportoA = ft.Dropdown(label="Aeroporto di Arrivo") 
        self._txtInTratteMax = ft.TextField(label="N tratte max")
        self._btnCercaItinerario = ft.ElevatedButton(text="Cerca itinerario", on_click=self._controller.handleCerca) #on_click per cambiare nome metodo al controller
        row3 = ft.Row([ft.Container(self._ddAeroportoA, width=250),
                       ft.Container(self._txtInTratteMax, width=250),
                       ft.Container(self._btnCercaItinerario, width=250)],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._txtResults = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.add(row1, row2, row3, self._txtResults)
        self._page.update()

nella view ogni tanto devo aggiungere la seconda riga 
self._ddAnno = ft.Dropdown(label="Anno", width=200, alignment=ft.alignment.top_left) #aggiungere il tasto onchange se corrisponde a una azione
self._controller._fillDDYears()
self._dd=ft.Dropdown(label, disabled=True)  => in controller.handleCreaGrafo self._view.txtIdOggetto.disabled = False      

#Model
class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMap = {}
        self._optPath = []
        self._optCost = 0

    def getAllCountries(self):
        return DAO.getAllCountries()

    #se ho un parametro lo metto anche nel metodo    
    def buildGraph(self):
        self._graph.clear()
        nodes = DAO.getAllNodes() 
        for n in nodes:
            self._idMap[n.ArtistId] = n
        self._graph.add_nodes_from(nodes)
        edges = DAO.getAllEdges(self._idMap)
        for e in edges:
            self._graph.add_edge(e.a1, e.a2, weight=e.peso)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getDettagli(self): 
        # 1. Trova i 3 archi di peso maggiore
        edges = [(u, v, d['weight']) for u, v, d in self._graph.edges(data=True)]
        edges.sort(key=lambda x: x[2], reverse=True)
        top_3 = edges[:3]
        # 2. Numero di componenti connesse
        components = list(nx.connected_components(self._graph))
        num_comp = len(components)
        # 3. Componente più grande e nodi ordinati per grado decrescente
        largest_comp = max(components, key=len) if components else []
        #f"Dimensione della componente connessa più grande: {len(largest_comp)
        subgraph = self._graph.subgraph(largest_comp)
        nodi_grado = list(subgraph.degree())
        nodi_grado.sort(key=lambda x: x[1], reverse=True)
        # c. Tutte le componenti connesse > 1, ordinate per dimensione decrescente
        components = [c for c in nx.connected_components(self._graph) if len(c) > 1]
        components.sort(key=len, reverse=True)
        return len(self._graph.nodes), len(self._graph.edges), edges, components
        #4 calcolo differenza peso archi uscenti e entranti 
        bestCustomer = None
        bestInfluenza = float('-inf')  #Inizia col valore più basso possibile
        for c in self._graph.nodes():
            # somma pesi archi uscenti
            outWeight = 0
            for _, _, data in self._graph.out_edges(c, data=True):
                outWeight += data["weight"]
            # somma pesi archi entranti
            inWeight = 0
            for _, _, data in self._graph.in_edges(c, data=True):
                inWeight += data["weight"]
            influenza = outWeight - inWeight
            # Prendi il MAX (anche se negativo)
            if influenza > bestInfluenza:
                bestInfluenza = influenza
                bestCustomer = c
        if bestCustomer is None:
            return None, 0
        #5 nodo di grado/dimensione/ordine maggiore e suo peso
        artista = max(self._graph.nodes, key=lambda n: self._graph.degree[n])
        return artista, self._graph.degree(artista)
        best = None
        bestPeso = -1
        for n in self._graph.nodes():
            somma = 0
            for vicino in self._graph.neighbors(n):
                somma += self._graph[n][vicino]["weight"]
            if somma > bestPeso:
                bestPeso = somma
                best = n
        return top_3, num_comp, nodi_grado, bestCustomer, bestInfluenza, best, bestpeso

    def getDettagli(self, id_object):
        if id_object not in self._idMap:
            return None
        source = self._idMap[id_object]
        conn = nx.node_connected_component(self._graph, source)
        print("size connessa con node_connected_component", len(conn))
        return len(conn)

    def getBestPath(self, source, lun):
        self._optPath = []
        self._optCost = 0
        parziale = [source]
        self._ricorsione(parziale, lun)
        return self._optPath, self._optCost    

#tstModel altezza del main 
from model.model import Model
mdl = Model()
mdl.buildGraph()
print(f"Il grafo creato contiene {mdl.getNumNodes()} nodi e {mdl.getNumEdges()} archi")

#Controller
class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model
        self._ratingValue = None

    def fillDDsRating(self):
        ratings = self._model.getAllRatings()
        ratingsOptions = list(map(lambda x: ft.dropdown.Option(x), ratings))
        self._view._ddrating.options = ratingsOptions
        self._view.update_page()
        #se nel DAO ho fatto select * al posto di name uso categoriesDDOptions = list(map(lambda x: ft.dropdown.Option(data=x, key=x.category_name, on_click=self._choiceCategory), categories))

    def _choiceDdRatings(self, e):
        self._ratingValue = e.control.data 

    def handleCreaGrafo(self, e):
        self._model.buildGraph()
        n, m = self._model.getGraphDetails()
        try:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text(f"Grafo correttamente creato."))
            self._view._txt_result.controls.append(ft.Text(f"Numero di nodi: {n}"))
            self._view._txt_result.controls.append(ft.Text(f"Numero di archi: {m}"))
            self._view._btnStampaInfo.disabled = False
            self._view.update_page()
        except Exception as ex:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text(f"Errore: {ex}", color="red", weight="bold"))
            self._view.update_page()
            print(f"Dettaglio Errore : {ex}")

    #Se vuoi usare int(): Configura le opzioni come nel Caso 1 (key=str(ID), text=Nome). Poi in handleCreaGrafo scrivi id = int(dd.value). È la strada maestra.
    #Se vuoi usare l'oggetto: Configura le opzioni come nel Caso 2 (data=Oggetto). Poi in handleCreaGrafo non fare nessuna conversione, prendi direttamente id = self._genereValue.GenreId.  +  
        if self._view._ddrating1.value is None or self._view._ddrating2.value is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, selezionare un range di rating.", color="red"))
            self._view.update_page()
            return
        r1 = float(self._view._ddrating1.value)
        r2 = float(self._view._ddrating2.value)
        self._model.buildGraph(r1,r2)   

    def handleCreaGrafo(self,e):
        #se ho parametro ma è valore dd punto 1
        if self._genereValue is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, selezionare un genere.", color="red"))
            self._view.update_page()
            return
        genereId = self._genereValue.GenreId
        self._model.buildGraph(genereId)

        #se ho parametri query 
        store = self._view._ddStore.value
        k = self._view._txtIntK.value
        if store is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, inserire uno store.", color="red"))
            self._view.update_page()
            return
        if k == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, inserire un numero di k valido.", color="red"))
            self._view.update_page()
            return
        try:
            kint = int(k)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, inserire un valore numero di k.", color="red"))
            self._view.update_page()
            return
        if kint <= 0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, k deve essere un intero positivo.", color="red"))
            self._view.update_page()
            return
        self._model.buildGraph(store, kint)
        n, m = self._model.getGraphDetails()
        try:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato! il grafo è costituito di {n} nodi ed {m} archi"))
            top5 = self._model.getDettagli()
            #attivo il dd per il prossimo punto
            nodi = self._model._graph.nodes
            self._view._ddNode.options = [ft.dropdown.Option(key=str(n.order_id), text=str(n.order_id)) for n in nodi]
            self._view._ddNode.disabled = False
            self._view._btnCerca.disabled = False
            self._view._btnRicorsione.disabled = False
            self._view.update_page()
        except Exception as ex:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Errore: {ex}", color="red", weight="bold"))
            self._view.update_page()
            print(f"Dettaglio Errore : {ex}")

    def handleDettagli(self, e):
        if len(self._model._graph.nodes) == 0:
            self._view.txt_result.controls.append(ft.Text("Errore: Crea prima il grafo!", color="red"))
            self._view.update_page()
            return
        top3, num_comp, nodes_degree = self._model.getDettagli()
        self._view.txt_result.controls.append(ft.Text("Archi di peso maggiore:"))
        for u, v, w in top3:
            self._view.txt_result.controls.append(ft.Text(f"{u.driverRef} -> {v.driverRef} ({w})"))
        #for (i), (u, v, w) in enumerate(top_5):
                #self._view._txt_result.controls.append(ft.Text(f"{i+1} {u.__str__()} -> {v.__str__()} (peso: {w:.2f})"))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {num_comp} componenti connesse"))
        self._view.txt_result.controls.append(ft.Text(f"Dimensione della componente connessa più grande: {len(largest_comp)"))
        self._view.txt_result.controls.append(ft.Text("Nodi della componente maggiore:"))
        for nodo, grado in nodes_degree:
            self._view.txt_result.controls.append(ft.Text(f"{nodo.driverRef} (Grado: {grado})"))
        nodi = self._model._graph.nodes
        self._view._ddClienti.options = [ft.dropdown.Option(key=str(n.CustomerId), text=str(n)) for n in nodi]
        self._view._ddClienti.disabled = False
        self._view._btnSequenza.disabled = False
        self._view.update_page()

    def handleDettagli(self,e):
        txtIdOggetto = self._view._txtIdOggetto.value
        if txtIdOggetto == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Attenzione, inserire un valore nel campo id.", color="red"))
            self._view.update_page()
            return
        try:
            idOggetto = int(txtIdOggetto)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text(f"Attenzione, inserire un valore numerico nel campo id.", color="red"))
            self._view.update_page()
            return
        if idOggetto not in self._model._idMap:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text(f"Attenzione, l'id inserito non è presente nel grafo.", color="orange"))
            self._view.update_page()
            return
        sizeCompConn = self._model.getDettagli(idOggetto)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"La componente connessa contenente l'oggetto con id {idOggetto} è composta di {sizeCompConn} nodi."))
        self._view._ddLun.disabled = False
        self._view._btnCerca.disabled = False
        lunValues = list(range(2, sizeCompConn))
        lunValuesDD = list(map(lambda x: ft.dropdown.Option(key=str(x), text=str(x)), lunValues))
        self._view._ddLun.options = lunValuesDD
        self._view.update_page()

    def handleStampaInfo(self,e):
        num_comp, largest_comp, subgraph = self._model.getDettagli()
        try:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text(f"Numero di componenti connesse: {num_comp}"))
            self._view._txt_result.controls.append(ft.Text(f""))
            self._view._txt_result.controls.append(ft.Text(f"Dimensione della componente connessa più grande: {len(largest_comp)} album"))
            self._view._txt_result.controls.append(ft.Text(f""))
            self._view._txt_result.controls.append(ft.Text(f"Dettagli degli album appartenenti alla componente connessa più grande:"))
            self._view._txt_result.controls.append(ft.Text(f""))
            film_ordinati = sorted(subgraph, key=lambda x: x.Title)
            #preparo dd e tasto per metodo con ricorsione
            for nodo in film_ordinati:
                self._view._txt_result.controls.append(ft.Text(f"- {nodo.Title}: {nodo.listaBrani} brani"))
            self._view._btnSelezione.disabled = False
            nodi = list(self._model._graph.nodes)
            nodi.sort(key=lambda x: x.Title)
            self._view._ddAlbum.options = [ft.dropdown.Option(key=str(n.AlbumId), text=n.Title, data=n) for n in nodi]
            self._view.update_page()
        except Exception as ex:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text(f"Errore: {ex}", color="red", weight="bold"))
            self._view.update_page()
            print(f"Dettaglio Errore : {ex}")

    def handleCammino(self, e):
        idOggetto = int(self._view._txtIdOggetto.value)
        source = self._model._idMap[idOggetto]
        lun = self._view._ddLun.value
        if lun is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Attenzione, selezionare un valore di lunghezza fra le scelte proposte.", color="red"))
            self._view.update_page()
            return
        lunInt = int(lun)
        path, cost = self._model.getBestPath(source, lunInt)
        self._view.txt_result.controls.clear()
        if not path:
            self._view.txt_result.controls.append(
                ft.Text("Nessun cammino trovato che rispetti i criteri", color="red"))
            self._view.update_page()
            return
        self._view.txt_result.controls.append(
            ft.Text(f"Ho trovato un cammino che parte da {source} "
                    f"che ha un peso totale pari a {cost}."))
        self._view.txt_result.controls.append(
            ft.Text(f"Di seguito i nodi che compongono questo cammino:"))
        path_ordinato = sorted(path, key=lambda x: x.object_name)
        self._view._txt_result.controls.append(ft.Text("I nodi che compongono il cammino sono:"))
        for p in path:
            self._view._txt_result.controls.append(ft.Text(f"{p} - Fatturato: {p.fatturato_totale:.2f}"))
        self._view.update_page()

#DAO 
#res.append(ArtObject(**row))   **row appende a res tutti i campi al posto di  codins=row["codins"], sono i campi res.append(row["peso"]) per nuova var  if len(res) == 0: return None
    @staticmethod 
    def getAllArtisti():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """             """ #select c.country
        cursor.execute(query)
        result = []
        for row in cursor:
            res.append(row["Country"])
        cursor.close()
        cnx.close()
        return result

#query parametrica, con %s nella query  
    @staticmethod
    def getAllNodes(r1, r2):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """  """
        cursor.execute(query, (r1, r2))
        for row in cursor:
            results.append(Names(**row))
        cursor.close()
        conn.close()
        return results

query con idMap
    @staticmethod
    def getAllEdges(idMap):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """  """
        cursor.execute(query,store,store,k) #se ho 2 %s nella query annidata e una fuori
        result = []
        for row in cursor:
            if row["id1"] in idMap and row["id2"] in idMap:
                if row["pop1"] > row["pop2"]:
                    result.append(Arco(idMap[row["id1"]], idMap[row["id2"]], row["peso"]))
                elif row["pop2"] > row["pop1"]:
                    result.append(Arco(idMap[row["id2"]], idMap[row["id1"]], row["peso"]))
                else:
                    result.append(Arco(idMap[row["id1"]], idMap[row["id2"]], row["peso"]))
                    result.append(Arco(idMap[row["id2"]], idMap[row["id1"]], row["peso"]))
        cursor.close()
        cnx.close()
        return result

#tstDAO altezza del main 
from database.DAO import DAO
allObjects = DAO.getAllNodes()
print(len(allObjects))

#GRAFI
#i nostri nodi diventano oggetti dataclass
import networkx as nx
g = nx.Graph() #grafo vuoto, indiretto NON ORIENTATO
g2 = nx.DiGraph() #grafo vuoto, diretto  ORIENTATO
m = nx.MultiDiGraph() #supporta multipli archi tra i nodi (senza Di è indiretto)
#https://networkx.org/ documentazione da consultare all''esame
g.add_edges_from(elist) #per aggiungere una lista di archi
g.add_weighted_edges_from(elist)
g.add_node(ft.Text("Pippo"))
#sono dei dizionari di dizionari, le chiavi sono i nodi
#n in g  testo se il nodo n è in g
#for n in g: iteri tra l'intero grafo
#for nbr in g[n] iteri tra tutti i vicini di n-

#dbConnect già scritto
def get_connection() -> mysql.connector.connection:
    try:
        cnx = mysql.connector.connect(
            option_files='./database/connector.cnf'
        )
        return cnx
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            return None
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return None
        else:
            print(err)
            return None
#di solito non lo dobbiamo toccare, dobbiamo andare su connector.cnf e cambiare la password e databasee, dovremo compilare DAO e model
"""