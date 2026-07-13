import flet as ft

class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

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

    def handleSelezione(self,e):
        nodo_scelto = self._view._ddAlbum.value
        valore_n = self._view._txtInN.value
        if nodo_scelto is None or valore_n == "":
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Attenzione, seleziona un nodo e inserisci N!", color="red"))
            self._view.update_page()
            return
        try:
            N = int(valore_n)
        except ValueError:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Attenzione, N deve essere un numero intero!", color="red"))
            self._view.update_page()
            return
        source = self._model._idMap[int(nodo_scelto)]
        best_set, score = self._model.getBestSet(source, N)
        self._view._txt_result.controls.clear()
        if not best_set:
            self._view._txt_result.controls.append(ft.Text("Nessun insieme trovato che rispetti i criteri.", color="red"))
            self._view.update_page()
            return
        self._view._txt_result.controls.append(ft.Text(f"Trovato insieme ottimo! Score totale: {score}."))
        self._view._txt_result.controls.append(
            ft.Text(f"I {len(best_set)} elementi selezionati sono:"))
        set_ordinato = sorted(best_set, key=lambda x: x.Title)
        for p in set_ordinato:
            self._view._txt_result.controls.append(ft.Text(str(p)))
        self._view.update_page()