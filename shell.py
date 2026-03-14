#!/usr/bin/env python3
# =============================================================================
# CIC304 – Sistemas Operacionais
# Projeto: Interpretador de comandos simples (shell) em Python
#
# Integrante:
#   - Nome: Pedro do Couto Rosa Canova | RA: 24.01570-9
# =============================================================================

import os
import sys


def ler_comando():
    """Exibe o prompt e lê uma linha de comando do usuário.

    Retorna None em caso de EOF (Ctrl+D), indicando que o shell deve encerrar.
    """
    try:
        linha = input("shell> ")
        return linha.strip()
    except EOFError:
        # Ctrl+D — trata como saída limpa
        print()
        return None


def parsear_comando(linha):
    """Divide a linha de comando em uma lista [comando, arg1, arg2, ...].

    Retorna lista vazia se a linha estiver em branco.
    """
    return linha.split()


def executar_comando(partes):
    """Cria um processo filho via fork() e executa o comando com execvp().

    O processo pai aguarda o término do filho e verifica o código de saída.
    """
    pid = os.fork()

    if pid == 0:
        # ── Processo filho ──────────────────────────────────────────────────
        try:
            # execvp busca o executável no PATH automaticamente
            os.execvp(partes[0], partes)
        except FileNotFoundError:
            print(f"shell: {partes[0]}: comando não encontrado")
        except PermissionError:
            print(f"shell: {partes[0]}: permissão negada")
        except Exception as e:
            print(f"shell: erro ao executar '{partes[0]}': {e}")
        # Encerra o filho imediatamente após erro (sem executar o pai)
        os._exit(1)

    else:
        # ── Processo pai ────────────────────────────────────────────────────
        _, status = os.wait()

        # os.wait() retorna o status em formato "raw"; extraímos o exit code
        codigo_saida = os.WEXITSTATUS(status)

        if codigo_saida != 0:
            print(f"shell: o comando terminou com código de saída {codigo_saida}")


def main():
    """Loop principal do shell: lê, parseia e executa comandos indefinidamente."""

    while True:
        linha = ler_comando()

        # EOF (Ctrl+D) — encerra o shell
        if linha is None:
            print("Saindo do shell...")
            sys.exit(0)

        # Linha em branco — exibe prompt novamente
        if not linha:
            continue

        # Parseia a linha em partes
        partes = parsear_comando(linha)

        # Comandos internos de saída
        if partes[0] in ("exit", "quit"):
            print("Saindo do shell...")
            sys.exit(0)

        # Executa o comando externo
        executar_comando(partes)


if __name__ == "__main__":
    main()
