"""
RICORSIONE:
#TIPOLOGIA 1:  (ArtsMia/exFlight)
-Il testo dice esplicitamente "lunghezza pari a LUN", "usando al massimo t tratte", oppure impone un nodo finale obbligatorio ("percorso da A a B").
-Pattern Logico: Poiché sai esattamente quando fermarti (quando arrivi alla lunghezza LUN o al nodo target),
-la verifica dell'ottimo (if costo > optCost) va fatta SOLO dentro la condizione di terminazione.

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMap = {}
        self._optPath = []
        self._optCost = 0

def getBestPath(self, source, lun):
        self._optPath = []
        self._optCost = 0
        parziale = [source]
        self._ricorsione(parziale, lun)
        return self._optPath, self._optCost

    def _ricorsione(self, parziale, lun):
        # 1. Condizione di Terminazione
        if len(parziale) == lun + 1:
            costo_attuale = self._costoPath(parziale)
            if costo_attuale > self._optCost:
                self._optCost = costo_attuale
                self._optPath = list(parziale)
            return
        # 2. Condizione di Continuazione
        for n in self._graph.neighbors(parziale[-1]):
            if n not in parziale:
                # Eventuali altri vincoli del testo (es. stessa classification)
                if n.classification == parziale[0].classification:
                    parziale.append(n)
                    self._ricorsione(parziale, lun)
                    parziale.pop()

    def _costoPath(self, path):
        costo = 0
        for i in range(0, len(path) - 1):
            costo += self._graph[path[i]][path[i + 1]]["weight"]
        return costo

Controller:
def handleCammino(self, e):
        source = self._view._ddNode.value # Assumendo abbia gli oggetti mappati
        lun = self._view._txtLUN.value
        if source is None or lun == "":
            self._view.txt_result.controls.append(ft.Text("Seleziona tutti i campi!"))
            self._view.update_page()
            return
        path, cost = self._model.getBestPath(source, int(lun))
        self._view.txt_result.controls.clear()
        if not path:
            self._view.txt_result.controls.append(ft.Text("Nessun cammino trovato."))
        else:
            self._view.txt_result.controls.append(ft.Text(f"Cammino trovato! Peso: {cost}"))
            for p in path:
                self._view.txt_result.controls.append(ft.Text(str(p)))
        self._view.update_page()

TIPOLOGIA 2: Cammino Libero con Vincoli Relazionali (Il più frequente)
(Esami: IMDB Simulazione, Baseball, Bike Store, Chinook A)
-Il testo dice "cammino di lunghezza massima" o "cammino di peso massimo". Non c'è LUN!
-In compenso, ti dà una regola per passare da un nodo all'altro: "il peso degli archi deve essere strettamente crescente",
-oppure "l'età del nodo successivo deve essere minore".
-Pattern Logico (La Trappola): Siccome non sai quanto sarà lungo il cammino alla fine, ogni singolo nodo che aggiungi potrebbe essere il cammino ottimo finale.
-L'aggiornamento dell'ottimo va fatto ALL'INIZIO del metodo ricorsivo, prima di ogni altra cosa.
-La ricorsione si fermerà da sola quando il ciclo for non troverà più vicini validi.
class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMap = {}
        self._optPath = []
        self._optCost = 0 #o optLun
    def getBestPath(self, source):
        self._optPath = []
        self._optCost = 0  # Può essere il peso, o la lunghezza se chiede "il più lungo"
        parziale = [source]
        self._ricorsione(parziale)
        return self._optPath, self._optCost

    def _ricorsione(self, parziale):
        # 1. Aggiornamento OTTIMO AD OGNI SINGOLO PASSO
        costo_attuale = self._costoPath(parziale) #se chiede lun non serve
        # Se l'esame chiede "Lunghezza massima", la condizione è: if len(parziale) > len(self._optPath):
        if costo_attuale > self._optCost:
            self._optCost = costo_attuale #self._optlun = len(parziale) per lunghezza
            self._optPath = list(parziale)
        # 2. Continuazione (NESSUN RETURN ESPLICITO, si ferma quando finiscono i vicini validi)
        for n in self._graph.neighbors(parziale[-1]):
            if n not in parziale:
                # ESEMPIO DI VINCOLO RELAZIONALE SULL'ARCO (es. peso crescente)
                if len(parziale) == 1:
                    # Al primo passo accetto sempre, non ho archi precedenti con cui confrontare
                    parziale.append(n)
                    self._ricorsione(parziale)
                    parziale.pop()
                else:
                    # Dal secondo passo, confronto l'arco vecchio con quello nuovo
                    peso_vecchio = self._graph[parziale[-2]][parziale[-1]]["weight"]
                    peso_nuovo = self._graph[parziale[-1]][n]["weight"]
                    if peso_nuovo > peso_vecchio: # vincolo crescente
                        parziale.append(n)
                        self._ricorsione(parziale)
                        parziale.pop()
Controller:
#Codice Controller: (Identico alla Tipologia 1, ma togli la lettura e il passaggio di LUN al metodo getBestPath).
#se non devo partire dal dd del  nodo, ma da un tasto:
        if not self._model._graph.nodes:
            return None
        source = min(self._model._graph.nodes, key=lambda n: n.date_of_birth)
        if source is None:
            self._view.txt_result.controls.append(ft.Text("Grafo vuoto!", color="red"))
            return
        path, lun = self._model.getBestPath(source)
        ...

def handleCammino(self, e):
        nodo_scelto = self._view._ddNode.value
        if nodo_scelto is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Attenzione, seleziona un nodo di partenza!", color="red"))
            self._view.update_page()
            return
        # N.B. Se il Dropdown salva solo l'ID come stringa, ricordati di estrarre
        # l'oggetto completo dalla mappa (es. source = self._model._idMap[int(nodo_scelto)])
        source = nodo_scelto
        path, cost = self._model.getBestPath(source)
        self._view.txt_result.controls.clear()
        if not path:
            self._view.txt_result.controls.append(
                ft.Text("Nessun cammino trovato che rispetti i criteri.", color="red"))
            self._view.update_page()
            return
        self._view.txt_result.controls.append(
            ft.Text(f"Trovato cammino ottimo! Costo/Peso totale: {cost}.", color="green"))
        self._view.txt_result.controls.append(
            ft.Text("I nodi che compongono il cammino sono:", color="green"))
        for p in path:
            self._view.txt_result.controls.append(ft.Text(str(p)))
        self._view._ddNode.disabled = False #se ci sono tasti disabilitati
        self._view._btnCerca.disabled = False
        self._view._btnRicorsione.disabled = False
        self._view.update_page()

TIPOLOGIA 3: Insiemi su Componenti Connesse (Ricerca a Salti)
(Esami: Chinook B, Formula 1 2026)
-Non c'è la parola "Cammino" o "Percorso". Il testo chiede di trovare un "Gruppo/Insieme di N elementi" e specifica che ciascun elemento deve appartenere a una "Componente Connessa Diversa".
-Pattern Logico: Non puoi usare self._graph.neighbors(), perché i nodi da pescare non sono collegati tra loro (essendo in componenti diverse)!
-Devi passare alla ricorsione la lista delle componenti connesse e fare la logica "Prendo un nodo da questa componente, oppure la salto e passo alla prossima".

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMap = {}
        self._optSet = []
        self._optScore = 0
    def getBestSet(self, source, N):
        self._optSet = []
        self._optScore = 0
        parziale = [source]
        # 1. Calcolo tutte le componenti connesse
        tutte_le_comp = list(nx.connected_components(self._graph))
        comp_di_source = next(c for c in tutte_le_comp if source in c)
        # 2. Filtro via la componente che contiene già il "source" (non posso più pescare da lì)
        comp_rimaste = [c for c in tutte_le_comp if source not in c]
        self._ricorsione_set(parziale, N, comp_rimaste)
        return self._optSet, self._optScore

    def _ricorsione_set(self, parziale, N, comp_rimaste):
        # 1. Terminazione: Ho trovato N elementi
        if len(parziale) == N:
            # Calcolo lo "score" dell'insieme come richiesto dall'esame
            # (es. Somma dei brani degli album, o differenza di età per F1)
            score = sum([nodo.num_brani for nodo in parziale])
            if score > self._optCost:
                self._optCost = score
                self._optPath = list(parziale)
            return
        # 2. Terminazione: Ho finito le componenti da esplorare ma non ho raggiunto N
        if len(comp_rimaste) == 0:
            return
        # 3. Logica PRENDO o LASCIO
        comp_attuale = comp_rimaste[0]
        comp_successive = comp_rimaste[1:] # Il resto della lista
        # Scelta A: Provo a inserire nell'insieme un nodo di questa componente
        for nodo in comp_attuale:
            parziale.append(nodo)
            self._ricorsione_set(parziale, N, comp_successive)
            parziale.pop()
        # Scelta B: Ignoro questa componente e vado avanti a cercare nelle prossime
        self._ricorsione_set(parziale, N, comp_successive)

controller:
    def handleInsieme(self, e):
        # 1. Lettura dati (Nodo sorgente + Valore N)
        nodo_scelto = self._view._ddNode.value
        valore_n = self._view._txtN.value
        # Controlli di sicurezza standard
        if nodo_scelto is None or valore_n == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, seleziona un nodo e inserisci N!", color="red"))
            self._view.update_page()
            return
        try:
            N = int(valore_n)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Attenzione, N deve essere un numero intero!", color="red"))
            self._view.update_page()
            return
        # Assumo che source sia l'oggetto. Se il DD ha solo l'ID, usa la idMap. source = self._model._idMap[int(nodo_scelto)]
        source = nodo_scelto #source = self._model._idMap[int(nodo_scelto)]
        # 2. Chiamata al Model
        # (Nota il nome: getBestSet invece di getBestPath, e score invece di cost)
        best_set, score = self._model.getBestSet(source, N)
        # 3. Stampa dei risultati
        self._view.txt_result.controls.clear()
        if not best_set:
            self._view.txt_result.controls.append(
                ft.Text("Nessun insieme trovato che rispetti i criteri.", color="red"))
            self._view.update_page()
            return
        self._view.txt_result.controls.append(
            ft.Text(f"Trovato insieme ottimo! Score totale: {score}."))
        self._view.txt_result.controls.append(
            ft.Text(f"I {len(best_set)} elementi selezionati sono:"))
        # Spesso in queste tipologie il testo chiede di stamparli in ordine alfabetico
        set_ordinato = sorted(best_set, key=lambda x: x.Title) # Cambia .Title con l'attributo giusto
        for p in set_ordinato:
            self._view.txt_result.controls.append(ft.Text(str(p)))
        self._view.update_page()

TIPOLOGIA 4: Il Sottografo Adiacente (Espansione a Macchia d'Olio)
(Esami: Chinook C)
-Chiede di formare un "Gruppo di N elementi", ma il vincolo è: "Ogni elemento aggiunto deve essere adiacente ad almeno uno degli elementi già presenti nel gruppo".
-Pattern Logico: A differenza di un cammino (dove guardi i vicini solo dell'ultimo nodo inserito), qui il nuovo nodo può attaccarsi a qualsiasi nodo già presente nel tuo insieme parziale.
-È un'espansione "a macchia d'olio".

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMap = {}
        self._optSet = []
        self._optScore = 0
    def getBestGroup(self, source, N):
        self._optSet = []
        self._optScore = 0
        parziale = [source]
        self._ricorsione_group(parziale, N)
        return self._optSet, self._optScore

    def _ricorsione_group(self, parziale, N):
        # 1. Terminazione: Insieme raggiunto
        if len(parziale) == N:
            costo = sum([nodo.num_brani for nodo in parziale]) # La statistica da massimizzare
            if costo > self._optCost:
                self._optCost = costo
                self._optPath = list(parziale)
            return
        # 2. Trovo TUTTI i vicini possibili dell'intero gruppo corrente
        # Creo un set per evitare duplicati
        vicini_possibili = set()
        for nodo_in_parziale in parziale:
            for vicino in self._graph.neighbors(nodo_in_parziale):
                if vicino not in parziale:
                    vicini_possibili.add(vicino)
        # 3. Continuazione: Provo ad aggiungere i vicini trovati
        for v in vicini_possibili:
            # Applico eventuali vincoli del testo (es. "nessun arco di peso 1")
            # Devo controllare se v ha un arco di peso 1 con i nodi GIA' in parziale a cui è collegato
            arco_invalido = False
            for n_p in parziale:
                if self._graph.has_edge(v, n_p):
                    if self._graph[v][n_p]["weight"] == 1:
                        arco_invalido = True
                        break
            if not arco_invalido:
                parziale.append(v)
                self._ricorsione_group(parziale, N)
                parziale.pop()

controller:
def handleInsieme(self, e):
        # 1. Lettura dati (Nodo sorgente + Valore N)
        nodo_scelto = self._view._ddNode.value
        valore_n = self._view._txtN.value
        # Controlli di sicurezza standard
        if nodo_scelto is None or valore_n == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Attenzione, seleziona un nodo e inserisci N!", color="red"))
            self._view.update_page()
            return
        try:
            N = int(valore_n)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Attenzione, N deve essere un numero intero!", color="red"))
            self._view.update_page()
            return
        # Assumo che source sia l'oggetto. Se il DD ha solo l'ID, usa la idMap.
        source = nodo_scelto
        # 2. Chiamata al Model
        # (Nota il nome: getBestSet invece di getBestPath, e score invece di cost)
        best_set, score = self._model.getBestSet(source, N)
        self._view.txt_result.controls.clear()
        if not best_set:
            self._view.txt_result.controls.append(
                ft.Text("Nessun insieme trovato che rispetti i criteri.", color="red"))
            self._view.update_page()
            return
        self._view.txt_result.controls.append(
            ft.Text(f"Trovato insieme ottimo! Score totale: {score}.", color="green"))
        self._view.txt_result.controls.append(
            ft.Text(f"I {len(best_set)} elementi selezionati sono:", color="green"))
        # Spesso in queste tipologie il testo chiede di stamparli in ordine alfabetico
        set_ordinato = sorted(best_set, key=lambda x: x.Title) # Cambia .Title con l'attributo giusto
        for p in set_ordinato:
            self._view.txt_result.controls.append(ft.Text(str(p)))
        self._view.update_page()
"""