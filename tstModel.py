from model.genere import Genere
from model.model import Model

mymdl = Model()

gen = Genere(2,"Jazz")
mymdl.buildGraph(gen)
n, e= mymdl.graphDetail()

print("N nodi: ",n, "N archi: ",e)
