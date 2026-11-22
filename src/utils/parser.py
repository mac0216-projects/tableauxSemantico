from classes.sintaxe.operador import TABLEAUX_OPERADORES

OPERADORES_DE_PARSING = [*TABLEAUX_OPERADORES, '|-']

def parsear_proposicoes(stringEntrada: str):
    proposicoes = stringEntrada.replace(' ', '').split(',')

    for proposicao in proposicoes:
        match True:
            case _ if not proposicao: # Aparentemente o if é como um operador , e o _ recebe o valor para testar no match
                raise ValueError(f'{proposicoes.index(proposicao) + 1}ª Proposição é vazia')

            case _ if proposicao.count('(') != proposicao.count(')'):
                raise ValueError(f'{proposicoes.index(proposicao) + 1}ª não possui parênteses completos')

            case _ if (
                (len(proposicao) == 1 and not proposicao.isalpha()) or
                proposicao in OPERADORES_DE_PARSING
            ):
                raise ValueError(f'{proposicoes.index(proposicao) + 1}ª Proposição é inválida')

    return proposicoes