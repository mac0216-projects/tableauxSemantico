from code_base_EP1 import *

ramo_inicial = {
    "nao_expandidas": [('T', P >> Q)],
    "expandidas": [],
    "atomos": {'P': True, 'Q': False},   # T P e F Q já são átomos!
    "fechado": False
}
ramos_abertos = [ramo_inicial]  # nossa "agenda" de ramos a processar
historico = []                  # vai guardar [(regra, formula), ...]