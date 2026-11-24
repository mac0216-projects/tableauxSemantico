import string
import sys
from code_base_EP1 import *
from tableau import *


def ler_formula(texto: str) -> Proposition:
    # converte uma string (ex: '(p>>q) & (~s)' ou 'P.iff(Q)') em um objeto Proposition
    texto = texto.strip()
    if not texto:
        raise ValueError("Fórmula vazia.")

    # ambiente seguro: apenas átomos, constantes e conectivos da base
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
            f"Sintaxe inválida em '{texto}'. Use ~, &, |, >>, <<, .iff() e parênteses."
        ) from erro

    return cast_to_proposition(resultado)


def separar_premissas(texto: str) -> list[str]:
    # separa por vírgula apenas fora de parênteses
    partes = []
    atual = []
    nivel = 0

    for char in texto:
        if char == "(":
            nivel += 1
        elif char == ")":
            nivel -= 1

        if char == "," and nivel == 0:
            partes.append("".join(atual).strip())
            atual = []
        else:
            atual.append(char)

    if atual:
        partes.append("".join(atual).strip())

    return [p for p in partes if p]


def interpretar_linha(linha: str) -> ArgumentForm:
    # aceita 'P, P >> Q |- Q' (sequente) ou 'P | ~P' (fórmula sem premissas)
    separador = None
    if "|-" in linha:
        separador = "|-"
    elif "|=" in linha:
        separador = "|="

    if separador is not None:
        partes = linha.split(separador)
        if len(partes) != 2:
            raise ValueError(f"Use apenas um '{separador}' por linha.")

        lado_esq, lado_dir = partes[0].strip(), partes[1].strip()
        if not lado_dir:
            raise ValueError("Conclusão ausente após o separador.")

        premissas = [ler_formula(p) for p in separar_premissas(lado_esq)] if lado_esq else []
        conclusao = ler_formula(lado_dir)
        return ArgumentForm(*premissas, conclusion=conclusao)

    # caso sem separador: trata a proposição única como conclusão sem premissas
    conclusao = ler_formula(linha)
    return ArgumentForm(conclusion=conclusao)


def executar_sequente(sequente: ArgumentForm, exibir: bool, arquivo_saida: str | None):
    valido, contraexemplo, historico = provar_sequente(
        sequente,
        exibir_passos=exibir,
        arquivo_txt=arquivo_saida,
    )

    print(f"Sequente analisado: {sequente}")
    if valido:
        print("Resultado: VÁLIDO")
    else:
        print("Resultado: INVÁLIDO")
        print(f"Contra-exemplo: {contraexemplo}")
    print(f"Regras aplicadas ({len(historico)}): {historico}")


def modo_arquivo(caminho: str):
    try:
        with open(caminho, "r", encoding="utf-8") as arq:
            linhas = arq.readlines()
    except FileNotFoundError:
        print(f"Erro: arquivo '{caminho}' não encontrado.")
        return

    exibir = input("Exibir passo a passo no terminal? (s/n): ").strip().lower() == "s"
    salvar = input("Salvar passo a passo em 'saida_tableau.txt'? (s/n): ").strip().lower() == "s"
    arquivo_saida = "saida_tableau.txt" if salvar else None

    # limpa o arquivo de saída anterior antes de processar o lote
    if arquivo_saida:
        open(arquivo_saida, "w", encoding="utf-8").close()

    total = 0
    for num_linha, bruta in enumerate(linhas, start=1):
        linha = bruta.strip()
        if not linha or linha.startswith("#"):
            continue

        total += 1
        print(f"\n--- Linha {num_linha} ---")
        try:
            sequente = interpretar_linha(linha)
            executar_sequente(sequente, exibir, arquivo_saida)
        except ValueError as erro:
            print(f"Erro na linha {num_linha} ('{linha}'): {erro}")

    print(f"\nProcessamento concluído: {total} entrada(s) analisada(s).")


def modo_terminal():
    print("\nConectivos: ~ (não), & (e), | (ou), >> (implica), << (implicado por), <=> (bi-implicação)")
    print("Átomos: 1 letra (exceto T e F, que representam True e False)")
    print("Digite 'sair' a qualquer momento para encerrar.\n")

    while True:
        entrada_premissas = input("Premissas separadas por vírgula (ou Enter se não houver): ").strip()
        if entrada_premissas.lower() == "sair":
            break

        entrada_conclusao = input("Conclusão: ").strip()
        if entrada_conclusao.lower() == "sair":
            break

        exibir = input("Exibir passo a passo no terminal? (s/n): ").strip().lower() == "s"
        salvar = input("Salvar passo a passo em 'saida_tableau.txt'? (s/n): ").strip().lower() == "s"

        try:
            premissas = (
                [ler_formula(p) for p in separar_premissas(entrada_premissas)]
                if entrada_premissas
                else []
            )
            conclusao = ler_formula(entrada_conclusao)
            sequente = ArgumentForm(*premissas, conclusion=conclusao)

            print()
            executar_sequente(sequente, exibir, "saida_tableau.txt" if salvar else None)

        except ValueError as erro:
            print(f"\nErro na entrada: {erro}")

        print("\n" + "-" * 55)


def main():
    # permite rodar direto via 'python main.py entrada.txt'
    if len(sys.argv) > 1:
        modo_arquivo(sys.argv[1])
        return

    print("=== Provador de Teoremas por Tableaux Semânticos ===")
    print("1 - Digitar fórmulas no terminal")
    print("2 - Ler arquivo com uma ou mais proposições/sequentes")
    opcao = input("Escolha uma opção (1/2): ").strip()

    if opcao == "2":
        caminho = input("Caminho do arquivo (ex: entrada.txt): ").strip()
        modo_arquivo(caminho)
    else:
        modo_terminal()


if __name__ == "__main__":
    main()