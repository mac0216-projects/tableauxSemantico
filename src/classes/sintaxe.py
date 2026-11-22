# Um átomo é uma proposição que não pode ser decomposta em outras proposições, valorado
# Um operador é um simbolo que conecta proposições valoradas, sendo binário ou unário

from typing import Literal

OperadorSimbolo = Literal['~', '&', '|', '>>', '<>']
TABLEAUX_OPERADORES: list[OperadorSimbolo] = ['~', '&', '|', '>>', '<>']

class Operador:
    def __init__(self, simbolo: OperadorSimbolo):
        self.simbolo = simbolo

    def __eq__(self, other: Operador) -> bool:
        return self.simbolo == other.simbolo


class Proposicao:
    def __init__(self, simbolo: str):
        self.simbolo = simbolo

    def __eq__(self, other: Proposicao) -> bool:
        return self.simbolo == other.simbolo