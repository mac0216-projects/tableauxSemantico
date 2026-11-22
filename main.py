import string
from code_base_EP1 import *
from tableau import *


def ler_formula(texto: str) -> Proposition:
    """Converte uma string (ex: '(p>>q) & (~s)') em um objeto Proposition."""
    texto = texto.strip()
    if not texto:
        raise ValueError("Fórmula vazia.")

    # Ambiente seguro: sem funções embutidas do Python, apenas átomos e constantes
    ambiente = {
        "__builtins__": None,
        "T": Constant(True),
        "F": Constant(False),
        "True": Constant(True),
        "False": Constant(False),
    }
    for letra in string.ascii_letters:
        if letra not in ("T", "F"):
            ambiente[letra] = Variable(letra)

    try:
        resultado = eval(texto, ambiente, {})
    except Exception as erro:
        raise ValueError(
            f"Sintaxe inválida em '{texto}'. Use conectivos ~, &, |, >> e parênteses."
        ) from erro

    return cast_to_proposition(resultado)


def modo_interativo():
    print("=== Provador de Teoremas por Tableaux Semânticos ===")
    print("Conectivos: ~ (não), & (e), | (ou), >> (implica)")
    print("Átomos: 1 letra (exceto T e F, que representam True e False)")
    print("Digite 'sair' a qualquer momento para encerrar.\n")

    while True:
        entrada_premissas = input(
            "Premissas separadas por vírgula (ou Enter se não houver): "
        ).strip()
        if entrada_premissas.lower() == "sair":
            break

        entrada_conclusao = input("Conclusão: ").strip()
        if entrada_conclusao.lower() == "sair":
            break

        try:
            premissas = []
            if entrada_premissas:
                for p in entrada_premissas.split(","):
                    premissas.append(ler_formula(p))

            conclusao = ler_formula(entrada_conclusao)
            sequente = ArgumentForm(*premissas, conclusion=conclusao)

            exibir = input("Exibir passo a passo no terminal? (s/n): ").strip().lower() == "s"
            salvar = input("Salvar passo a passo em 'saida_tableau.txt'? (s/n): ").strip().lower() == "s"

            valido, contraexemplo, historico = provar_sequente(
                sequente,
                exibir_passos=exibir,
                arquivo_txt="saida_tableau.txt" if salvar else None,
            )

            print(f"\nSequente analisado: {sequente}")
            if valido:
                print("Resultado: VÁLIDO")
            else:
                print("Resultado: INVÁLIDO")
                print(f"Contra-exemplo: {contraexemplo}")

            print(f"Regras aplicadas ({len(historico)}): {historico}\n")
            print("-" * 55)

        except ValueError as e:
            print(f"\n[Erro de entrada] {e}\n")

if __name__ == "__main__":
    modo_interativo()