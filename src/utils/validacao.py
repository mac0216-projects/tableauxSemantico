from classes.operador import TABLEAUX_OPERADORES

TABLEAUX_CACTERES_PERMITIDOS = ['(', ')', ',']

def validar_proposicao_entrada(stringEntrada: str):
    proposicoes = stringEntrada.replace(' ', '').split(',')
    listaOperadores = [operador.value for operador in TABLEAUX_OPERADORES]

    for proposicao in proposicoes:
        match True:
            case _ if not proposicao: # Aparentemente o if é como um operador , e o _ recebe o valor para testar no match
                raise ValueError(f'{proposicoes.index(proposicao) + 1}ª Proposição é vazia')

            case _ if proposicao.count('(') != proposicao.count(')'):
                raise ValueError(f'{proposicoes.index(proposicao) + 1}ª não possui parênteses completos')

            case _ if (
                proposicao in listaOperadores or
                (len(proposicao) == 1 and not proposicao.isalpha())
            ):
                raise ValueError(f'{proposicoes.index(proposicao) + 1}ª Proposição é inválida')

    return proposicoes