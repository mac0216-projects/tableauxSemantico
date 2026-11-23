from code_base_EP1 import *


class FormulaMarcada:
    def __init__(self, sinal, formula):
        # valida se o sinal é valido
        if sinal not in ("T", "F"):
            raise ValueError("Sinal inválido")

        # guarda os valores dentro do objeto
        self.sinal = sinal
        self.formula = formula

    def __str__(self):
        # f-string: funcionacomo um print(objeto)
        return f"{self.sinal} {self.formula}"

    def eh_igual(self, outra):
        # compara objetos
        cmp = self.sinal == outra.sinal and self.formula.is_identical(outra.formula)

        return cmp


# TEST ===================================================

# P, Q, R = vars("P", "Q", "R")

# f1 = FormulaMarcada("T", P)
# f2 = FormulaMarcada("T", ~~P)
# f3 = FormulaMarcada("T", P)

# print("f1 == f2: ", f1.eh_igual(f2))
# print("f1 == f3: ", f1.eh_igual(f3))
# print("f1: ", f1)
# print("f2: ", f2)

# ========================================================


class Ramo:
    def __init__(self, id_ramo: str = "1"):
        self.id_ramo = id_ramo
        self.nao_expandidas = []
        self.expandidas = []
        self.atomos = {}
        self.fechado = False
        self.motivo_fechamento = ""

    def adicionar(self, fm: FormulaMarcada):
        if self.fechado:
            return
        valor = fm.sinal == "T"

        # caso 1 - fm.formula é uma constante (True ou False)
        if isinstance(fm.formula, Constant):
            contradicao = fm.formula.value != valor

            if contradicao:
                self.fechado = True
                self.motivo_fechamento = f"constante {fm.formula.value} com sinal {fm.sinal}"

        # caso 2 - fm.formula é uma variable (atomo)
        elif isinstance(fm.formula, Variable):
            nome = fm.formula.name

            if nome in self.atomos:
                if self.atomos[nome] != valor:
                    self.fechado = True
                    sinal_antigo = "T" if self.atomos[nome] else "F"
                    self.motivo_fechamento = (
                        f"contradição em {nome} ({sinal_antigo} {nome} e {fm.sinal} {nome})"
                    )

            else:
                self.atomos[nome] = valor

        # caso 3 - formula composta (~, and, or, =>)
        else:
            ja_existe_formula = False
            for formula in self.nao_expandidas + self.expandidas:
                if formula.eh_igual(fm):
                    ja_existe_formula = True

            if not ja_existe_formula:
                self.nao_expandidas.append(fm)

    def clonar(self, sufixo: str = ""):
        novo_ramo = Ramo(id_ramo=f"{self.id_ramo}{sufixo}")
        novo_ramo.atomos = self.atomos.copy()
        novo_ramo.expandidas = self.expandidas.copy()
        novo_ramo.nao_expandidas = self.nao_expandidas.copy()
        novo_ramo.fechado = self.fechado
        novo_ramo.motivo_fechamento = self.motivo_fechamento

        return novo_ramo

    def esta_saturada(self):
        if not self.fechado and len(self.nao_expandidas) == 0:
            return True

        return False


# TEST ===================================================

# P, Q, R = vars("P", "Q", "R")

# r = Ramo()

# f1 = FormulaMarcada("T", P)
# f2 = FormulaMarcada("T", P >> Q)

# r.adicionar(f1)
# r.adicionar(f2)

# r_esq = r.clonar()
# r_dir = r.clonar()

# f_esq = FormulaMarcada("F", P)
# r_esq.adicionar(f_esq)

# f_dir = FormulaMarcada("T", Q)
# r_dir.adicionar(f_dir)

# print(r_esq.fechado, r_dir.fechado, r_dir.atomos)

# ========================================================


def expandir_formula(fm: FormulaMarcada) -> tuple[str, str, list[FormulaMarcada]]:
    sinal = fm.sinal
    f = fm.formula

    # regras de expansçao do tableaux:
    # +---------+-----------+------------+----------------------+----------------------+
    # | Grupo   | Regra     | Fórmula    | Resultado            | Efeito no tableau    |
    # +---------+-----------+------------+----------------------+----------------------+
    # | alpha   | alpha_^   | T (C & B)  | T C, T B             | Mesmo ramo           |
    # | alpha   | alpha_v   | F (C | B)  | F C, F B             | Mesmo ramo           |
    # | alpha   | alpha_>>  | F (C >> B) | T C, F B             | Mesmo ramo           |
    # | alpha   | alpha_<<  | F (C << B) | T B, F C             | Mesmo ramo           |
    # | alpha   | alpha_<=> | T (C<=>B)  | T(C>>B), T(B>>C)     | Mesmo ramo           |
    # | alpha   | alpha_~   | T (~C)     | F C                  | Mesmo ramo           |
    # +---------+-----------+------------+----------------------+----------------------+
    # | beta    | beta_^    | F (C & B)  | F C  |  F B          | Divide em ramos      |
    # | beta    | beta_v    | T (C | B)  | T C  |  T B          | Divide em ramos      |
    # | beta    | beta_>>   | T (C >> B) | F C  |  T B          | Divide em ramos      |
    # | beta    | beta_<<   | T (C << B) | F B  |  T C          | Divide em ramos      |
    # | beta    | beta_<=>  | F (C<=>B)  | F(C>>B) | F(B>>C)    | Divide em ramos      |
    # | beta(*) | beta_~    | F (~C)     | T C                  | Tratada sem dividir  |
    # +---------+-----------+------------+----------------------+----------------------+

    # conectivo: Conjunção (AND)
    if isinstance(f, And):
        if sinal == "T":
            # regra alpha_^: todos os filhos ganham sinal "T" no mesmo ramo
            novas = []
            for filho in f.children:
                novas.append(FormulaMarcada("T", filho))
            return "alpha_^", "alpha", novas

        else:
            # regra beta_^: cada filho ganha sinal "F" em um ramo separado
            novas = []
            for filho in f.children:
                novas.append(FormulaMarcada("F", filho))
            return "beta_^", "beta", novas

    # conectivo: Disjunção (OR)
    elif isinstance(f, Or):
        if sinal == "F":
            # regra alpha_v: todos os filhos ganham sinal "F" no mesmo ramo
            novas = []
            for filho in f.children:
                novas.append(FormulaMarcada("F", filho))
            return "alpha_v", "alpha", novas

        else:
            # regra beta_v: todos os filhos ganham sinal "T" em ramos separados
            novas = []
            for filho in f.children:
                novas.append(FormulaMarcada("T", filho))
            return "beta_v", "beta", novas

    # conectivo: Implicação (=>)
    elif isinstance(f, Implies):
        if sinal == "F":
            # regra alpha_>>: o primeiro filho recebe o sinal "T" e o segundo recebe o sinal "F"
            novas = []
            novas.append(FormulaMarcada("T", f.children[0]))
            novas.append(FormulaMarcada("F", f.children[1]))
            return "alpha_>>", "alpha", novas

        else:
            # regra beta_>>: o primeiro filho recebe o sinal "F" e o segundo recebe o sinal "T"
            novas = []
            novas.append(FormulaMarcada("F", f.children[0]))
            novas.append(FormulaMarcada("T", f.children[1]))
            return "beta_>>", "beta", novas

    # conectivo: Negação (~)
    elif isinstance(f, Not):
        if sinal == "T":
            # regra alpha_~: o primeiro filho recebe "F"
            novas = []
            novas.append(FormulaMarcada("F", f.children[0]))
            return "alpha_~", "alpha", novas

        else:
            # regra beta_~: o segundo filho recebe "T"
            # OBS: irei considerar essa regra como regra alfa para diminuir as bifurcações (evitar multiplicações de ramos sem necessidades)
            novas = []
            novas.append(FormulaMarcada("T", f.children[0]))
            return "beta_~", "alpha", novas

    # conectivo: Implicação reversa (<<) - equivalente a B => C
    elif isinstance(f, ImpliedBy):
        if sinal == "F":
            # regra alpha_<<: o segundo filho recebe "T" e o primeiro recebe "F"
            novas = []
            novas.append(FormulaMarcada("T", f.children[1]))
            novas.append(FormulaMarcada("F", f.children[0]))
            return "alpha_<<", "alpha", novas

        else:
            # regra beta_<<: o segundo filho recebe "F" e o primeiro recebe "T"
            novas = []
            novas.append(FormulaMarcada("F", f.children[1]))
            novas.append(FormulaMarcada("T", f.children[0]))
            return "beta_<<", "beta", novas

    # conectivo: Bi-implicação (<=>) - equivalente a (C => B) ^ (B => C)
    elif isinstance(f, Iff):
        imp1 = f.children[0] >> f.children[1]
        imp2 = f.children[1] >> f.children[0]

        if sinal == "T":
            # regra alpha_<=>: ambas as implicações recebem "T" no mesmo ramo
            novas = []
            novas.append(FormulaMarcada("T", imp1))
            novas.append(FormulaMarcada("T", imp2))
            return "alpha_<=>", "alpha", novas

        else:
            # regra beta_<=>: cada implicação recebe "F" em um ramo separado
            novas = []
            novas.append(FormulaMarcada("F", imp1))
            novas.append(FormulaMarcada("F", imp2))
            return "beta_<=>", "beta", novas
        
    else:
        raise ValueError(f"Fórmula não suportada para expansão: {fm}")


# TEST ===================================================

# P, Q, R = vars("P", "Q", "R")

# casos_teste = [
#     FormulaMarcada("F", P >> Q),      # esperado: alpha_>>, alpha -> T P, F Q
#     FormulaMarcada("T", P >> Q),      # esperado: beta_>>,  beta  -> F P | T Q
#     FormulaMarcada("F", P & Q & R),   # esperado: beta_^,   beta  -> F P | F Q | F R
#     FormulaMarcada("F", ~P),          # esperado: beta_~,   alpha -> T P
# ]

# for fm in casos_teste:
#     regra, tipo, novas = expandir_formula(fm)
#     print(f"Fórmula: {fm}  -->  Regra: {regra} | Tipo: {tipo}")

#     for n in novas:
#         print(f"    -> {n}")

# ========================================================


def escolher_formula(ramo: Ramo) -> FormulaMarcada:
    # procura a primeira formula alpha não expandida
    for i in range(len(ramo.nao_expandidas)):
        fm = ramo.nao_expandidas[i]
        regra, tipo, novas = expandir_formula(fm)

        if tipo == "alpha":
            removida = ramo.nao_expandidas.pop(i)
            ramo.expandidas.append(removida)

            return removida

    # se não tem nenhuma alpha, pegar a primeira beta
    removida = ramo.nao_expandidas.pop(0)
    ramo.expandidas.append(removida)
    return removida


# TEST ===================================================

# P, Q, R = vars("P", "Q", "R")

# r = Ramo()

# f1 = FormulaMarcada("T", P >> Q) # regra beta
# f2 = FormulaMarcada("F", Q >> R) # regra alfa

# r.adicionar(f1)
# r.adicionar(f2)

# f_escolhida = escolher_formula(r)
# print("a escolhida deve ser regra alfa: ", f_escolhida)
# print("deve haver 1 não expandida (a formula beta): ", len(r.nao_expandidas))

# ========================================================


def provar_sequente(
    argumento: ArgumentForm,
    exibir_passos: bool = False,
    arquivo_txt: str | None = None,
) -> tuple[bool, dict[str, bool] | None, list[tuple[str, str]]]:

    traco = [f"=== Sequente: {argumento} ===", "Ramo 1 (inicial):"]
    ramo_inicial = Ramo(id_ramo="1")

    # montando o ramo inicial com todas as premissas "T" e a conclusão "F"
    for premissa in argumento.premises:
        fm = FormulaMarcada("T", premissa)
        ramo_inicial.adicionar(fm)
        traco.append(f"  + {fm}")

    fm_conc = FormulaMarcada("F", argumento.conclusion)
    ramo_inicial.adicionar(fm_conc)
    traco.append(f"  + {fm_conc}")

    if ramo_inicial.fechado:
        traco.append(f"  [X] Ramo 1 fechou na inicialização ({ramo_inicial.motivo_fechamento})")

    pilha = [ramo_inicial]
    historico = []
    passo = 1

    def finalizar_saida():
        texto = "\n".join(traco) + "\n\n"
        if exibir_passos:
            print(texto)
        if arquivo_txt:
            with open(arquivo_txt, "a", encoding="utf-8") as arq:
                arq.write(texto)

    # iterar enquanto há ramos abertos
    while len(pilha) > 0:
        ramo_atual = pilha.pop()

        # se o ramo já está fechado, passa para o proximo
        if ramo_atual.fechado:
            continue

        # se o ramo está aberto e não tem como expandir mais, achamos o contraexemplo e o sequente é invalido
        if ramo_atual.esta_saturada():
            contraexemplo = ramo_atual.atomos.copy()

            for atomo in argumento.variables():
                if atomo not in contraexemplo:
                    contraexemplo[atomo] = False

            traco.append(
                f"[Ramo {ramo_atual.id_ramo}] SATURADO E ABERTO -> Contra-exemplo: {contraexemplo}"
            )
            finalizar_saida()
            return False, contraexemplo, historico

        # se está aberto e tem como expandir, segue para a proxima formula (alfa antes de beta)
        fm = escolher_formula(ramo_atual)
        regra, tipo, novas = expandir_formula(fm)
        historico.append((regra, str(fm)))

        if tipo == "alpha":
            traco.append(
                f"Passo {passo} [Ramo {ramo_atual.id_ramo}]: {regra} em ({fm}) -> {[str(n) for n in novas]}"
            )
            for nova in novas:
                ramo_atual.adicionar(nova)

            if ramo_atual.fechado:
                traco.append(
                    f"  [X] Ramo {ramo_atual.id_ramo} FECHOU ({ramo_atual.motivo_fechamento})"
                )
            else:
                pilha.append(ramo_atual)

        else:
            traco.append(
                f"Passo {passo} [Ramo {ramo_atual.id_ramo}]: {regra} em ({fm}) -> BIFURCA:"
            )
            sub_ramos = []
            for idx, nova in enumerate(novas, start=1):
                copia = ramo_atual.clonar(sufixo=f".{idx}")
                copia.adicionar(nova)

                if copia.fechado:
                    traco.append(
                        f"  -> Ramo {copia.id_ramo} recebe ({nova}) -> [X] FECHADO ({copia.motivo_fechamento})"
                    )
                else:
                    traco.append(f"  -> Ramo {copia.id_ramo} recebe ({nova}) -> [ABERTO]")
                    sub_ramos.append(copia)

            # empilha invertido para explorar o primeiro sub-ramo antes na busca em profundidade
            for copia in reversed(sub_ramos):
                pilha.append(copia)

        passo += 1

    # se a pilha esvaziou sem nenhum ramo aberto saturado, todos os ramos fecharam, portanto é valido
    traco.append("Resultado: VÁLIDO (todos os ramos fecharam)")
    finalizar_saida()
    return True, None, historico


# TEST ===================================================

# P, Q, R = vars("P", "Q", "R")

# # sequenstes do arquivo coe_base_EP1_demo.py
# modus_ponens = ArgumentForm(P, P >> Q, conclusion=Q)  # exemplo valido  # premises

# affirming_the_consequent = ArgumentForm(  # exemplo invalido
#     P >> Q, Q, conclusion=P  # premises
# )

# modus_ponens_eh_valido, modus_ponens_contraexemplo, modus_ponens_historico = (
#     provar_sequente(modus_ponens)
# )
# (
#     affirming_the_consequent_eh_valido,
#     affirming_the_consequent_contraexemplo,
#     affirming_the_consequent_historico,
# ) = provar_sequente(affirming_the_consequent)

# print(
#     "modus_ponens: ",
#     modus_ponens_eh_valido,
#     modus_ponens_contraexemplo,
#     modus_ponens_historico,
# )
# print(
#     "affirming_the_consequent: ",
#     affirming_the_consequent_eh_valido,
#     affirming_the_consequent_contraexemplo,
#     affirming_the_consequent_historico,
# )

# ========================================================
