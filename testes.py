from code_base_EP1 import *
from tableau import *


def rodar_test(nome: str, argumento: ArgumentForm):
    valido_tab, contraexemplo, historico = provar_sequente(argumento)
    valido_tv = argumento.is_valid_truth_table()

    print("Nome do teste e o sequente (str(argumento)):", nome)

    if valido_tab:
        print("Resultado do tableau: VÁLIDO")

    else:
        print("Resultado do tableau: INVALIDO")
        print("Contraexemplo: ", contraexemplo)

    print("Histórico: ", historico)
    print("Tabloux bateu com a tabela verdade: ", valido_tab == valido_tv)
    print("\n\n")


P, Q, R, S = vars("P", "Q", "R", "S")

# ==========================================================
# GRUPO 1: Exemplos do arquivo code_base_EP1_demo.py
# ==========================================================
modus_ponens = ArgumentForm(P, P >> Q, conclusion=Q)  

modus_tollens = ArgumentForm(P >> Q, ~Q, conclusion=~P)  

disjunctive_syllogism = ArgumentForm(P | Q, ~P, conclusion=Q)  

hypothetical_syllogism = ArgumentForm(P >> Q, Q >> R, conclusion=R)  

non_sequitur = ArgumentForm(P, conclusion=Q)  

affirming_the_consequent = ArgumentForm(P >> Q, Q, conclusion=P)  

denying_the_antecedent = ArgumentForm(P >> Q, ~P, conclusion=~Q)  

fallacy_of_the_excluded_middle = ArgumentForm(P | Q, P, conclusion=~Q)  


# ==========================================================
# GRUPO 2: Fórmulas ricas, aninhadas e operadores n-ários
# ==========================================================

# Fórmula do caderno (sem premissas — inválida; contraexemplo esperado: P=T, Q=T, R=F)
formula_caderno = ArgumentForm(conclusion=P >> ((Q >> R) | (Q >> (P & R))))

# Lei de De Morgan (válida — testa alpha_~, alpha_v, beta_~ e beta_^)
de_morgan = ArgumentForm(~(P & Q), conclusion=~P | ~Q)

# Operadores n-ários com 3 filhos (testa o laço em f.children)
conjuncao_naria = ArgumentForm(P & Q & R, conclusion=R)

disjuncao_naria = ArgumentForm(P | Q | R, conclusion=P)

# Distributiva com múltiplas ramificações sucessivas (válida)
multiplas_ramificacoes = ArgumentForm(
    P | Q, R | S, conclusion=(P & R) | (P & S) | (Q & R) | (Q & S)
)

# ==========================================================
# GRUPO 3: Casos de borda
# ==========================================================

# Sem premissas (tautologia — terceiro excluído)
sem_premissas_tautologia = ArgumentForm(conclusion=P | ~P)

# Constante False nas premissas (válido — T False fecha o ramo imediatamente)
premissa_falsa = ArgumentForm(False, conclusion=P)

# Constante True na conclusão (válido — F True fecha o ramo imediatamente)
conclusao_verdadeira = ArgumentForm(P, conclusion=True)

# Premissas repetidas (válido — não deve expandir a mesma fórmula duas vezes)
premissas_repetidas = ArgumentForm(P >> Q, P >> Q, P, conclusion=Q)

# Átomo livre no contraexemplo (inválido — P, Q e R devem aparecer no dicionário)
atomo_livre = ArgumentForm(P | Q, conclusion=R)

# Apenas átomos, sem conectivos (válido — histórico vazio [])
apenas_atomos = ArgumentForm(P, conclusion=P)

# ==========================================================
# GRUPO 4: Bi-implicação (Iff) e Implicação reversa (ImpliedBy)
# ==========================================================
implicacao_reversa = ArgumentForm(Q << P, P, conclusion=Q)

# Lei de De Morgan com bi-implicação (Exercício 4c da p. 48 do livro)
bi_implicacao_demorgan = ArgumentForm(conclusion=(~(P | Q)).iff(~P & ~Q))

# Bi-implicação inválida (contraexemplo esperado: P=T, Q=F ou P=F, Q=T)
bi_implicacao_invalida = ArgumentForm(conclusion=P.iff(Q))

testes = [
    ("Grupo 1 - modus_ponens", modus_ponens),
    ("Grupo 1 - modus_tollens", modus_tollens),
    ("Grupo 1 - disjunctive_syllogism", disjunctive_syllogism),
    ("Grupo 1 - hypothetical_syllogism", hypothetical_syllogism),
    ("Grupo 1 - non_sequitur", non_sequitur),
    ("Grupo 1 - affirming_the_consequent", affirming_the_consequent),
    ("Grupo 1 - denying_the_antecedent", denying_the_antecedent),
    ("Grupo 1 - fallacy_of_the_excluded_middle", fallacy_of_the_excluded_middle),
    ("Grupo 2 - Fórmula do caderno", formula_caderno),
    ("Grupo 2 - De Morgan", de_morgan),
    ("Grupo 2 - Conjunção n-ária (3 filhos)", conjuncao_naria),
    ("Grupo 2 - Disjunção n-ária (3 filhos)", disjuncao_naria),
    ("Grupo 2 - Múltiplas ramificações", multiplas_ramificacoes),
    ("Grupo 3 - Sem premissas (Tautologia)", sem_premissas_tautologia),
    ("Grupo 3 - Constante False na premissa", premissa_falsa),
    ("Grupo 3 - Constante True na conclusão", conclusao_verdadeira),
    ("Grupo 3 - Premissas repetidas", premissas_repetidas),
    ("Grupo 3 - Átomo livre no contraexemplo", atomo_livre),
    ("Grupo 3 - Apenas átomos", apenas_atomos),
    ("Grupo 4 - Implicação reversa", implicacao_reversa),
    ("Grupo 4 - Bi-implicação De Morgan", bi_implicacao_demorgan),
    ("Grupo 4 - Bi-implicação inválida", bi_implicacao_invalida),
]

print("GRUPO 1: Exemplos do arquivo code_base_EP1_demo.py")
print("GRUPO 2: Fórmulas ricas, aninhadas e operadores n-ários")
print("GRUPO 3: Casos de borda")
print("GRUPO 4: Bi-implicação (Iff) e Implicação reversa (ImpliedBy)\n")

for titulo, arg in testes:
    rodar_test(f"{titulo} | {arg}", arg)
