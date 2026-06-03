import flet as ft

from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._genereValue = None

    def fillDDGenre(self):
        generi = self._model.getAllGenere()
        generiDD = list(map(lambda x: ft.dropdown.Option(data=x, key=x.Name, on_click = self.handleDDGenere), generi))
        self._view._ddGenre.options = generiDD
        self._view.update_page()

    def fillDDArtista(self, gen):

        artisti = DAO.getAllNodes(gen)
        artistiDD = list(map(lambda x: ft.dropdown.Option(data=x, key=x.Name, on_click = self.handleDDArtista), artisti))
        self._view._ddArtist.options = artistiDD
        self._view.update_page()

    def handleDDArtista(self, e):
        self._artistaValue = e.control.data

    def handleCreaGrafo(self, e):
        gen = self._genereValue

        self._model.buildGraph(gen)
        nNodi, nArchi = self._model.graphDetail()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo creato:"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {nNodi}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {nArchi} "))


        bestArtista = self._model.getinfluenzaArtista()

        self._view.txt_result.controls.append(ft.Text("L'artista più infuente:"))
        self._view.txt_result.controls.append(
            ft.Text(f"{bestArtista[0]}, con influenza = {bestArtista[1]}")
        )

        top3 = self._model.getTop5Archi()

        self._view.txt_result.controls.append(ft.Text(f"Archi di peso maggiore:"))
        for arco in top3:
            self._view.txt_result.controls.append(ft.Text(f"{arco[0]} -> {arco[1]} (peso: {arco[2]["weight"]})"))

        self._view.update_page()

        self.fillDDArtista(gen)

    def handleDDGenere(self, e):
        self._genereValue = e.control.data

    def handleCammino(self, e):
        #Trovare un cammino semplice di lunghezza massima tale che ogni arco successivo abbia peso strettamente
        #crescente.
        path, score = self._model.getBestPath(self._artistaValue)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Cammino migliore a partire da {self._artistaValue}")
        )

        for p in path:
            self._view.txt_result.controls.append(ft.Text(f"{p}"))

        self._view.txt_result.controls.append(
            ft.Text(f"Score: {score}")
        )

        self._view.update_page()