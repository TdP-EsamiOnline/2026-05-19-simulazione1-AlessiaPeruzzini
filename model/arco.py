from dataclasses import dataclass

from model.artist import Artista


@dataclass
class Arco:
    a1: Artista
    a2: Artista
    peso: int