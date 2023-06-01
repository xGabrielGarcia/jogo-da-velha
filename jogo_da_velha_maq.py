import os

def criar_tabela():
    return [' '] * 9

def imprimir_tabela(tab):
    os.system("clear")

    print("\n\tJogo da velha\n")
    print("\t {} | {} | {}".format(tab[0], tab[1], tab[2]))
    print("\t-----------")
    print("\t {} | {} | {}".format(tab[3], tab[4], tab[5]))
    print("\t-----------")
    print("\t {} | {} | {}".format(tab[6], tab[7], tab[8]))

def completou_diag_princ(tab, j):
    return tab[0] == j and tab[4] == j and tab[8] == j

def completou_diag_sec(tab, j):
    return tab[2] == j and tab[4] == j and tab[6] == j

def completou_linha(tab, j, pos1, pos2, pos3):
    return tab[pos1] == j and tab[pos2] == j and tab[pos3] == j

def completou_linhas(tab, j):
    return (completou_linha(tab, j, 0, 1, 2) or
            completou_linha(tab, j, 3, 4, 5) or
            completou_linha(tab, j, 6, 7, 8))

def completou_coluna(tab, j, pos1, pos2, pos3):
    return tab[pos1] == j and tab[pos2] == j and tab[pos3] == j

def completou_colunas(tab, j):
    return (completou_coluna(tab, j, 0, 3, 6) or
            completou_coluna(tab, j, 1, 4, 7) or
            completou_coluna(tab, j, 2, 5, 8))

def checagem(tab, pos):
    return 0 <= pos <= 8 and tab[pos] == ' '

def coordenadas(tab, j):
    pos = int(input("\nDigite uma posicao: "))

    while not checagem(tab, pos):
        print("Erro! Digite uma posicao: ")
        pos = int(input())

    tab[pos] = j

def vitoria(tab, j):
    return (completou_diag_princ(tab, j) or
            completou_diag_sec(tab, j) or
            completou_linhas(tab, j) or
            completou_colunas(tab, j))

def empate(tab):
    return ' ' not in tab

def criar_no(quadro):
    return {'quadro': quadro, 'filhos': [], 'pontuacao': 0}

def construir_arvore(no, jogadorAtual):
    if vitoria(no['quadro'], 'X'):
        no['pontuacao'] = 1
        return
    if vitoria(no['quadro'], 'O'):
        no['pontuacao'] = -1
        return
    if empate(no['quadro']):
        no['pontuacao'] = 0
        return

    nextPlayer = 'O' if jogadorAtual == 'X' else 'X'

    for i in range(9):
        if no['quadro'][i] == ' ':
            novoQuadro = no['quadro'][:]
            novoQuadro[i] = jogadorAtual

            filho = criar_no(novoQuadro)
            no['filhos'].append(filho)

            construir_arvore(filho, nextPlayer)

def minmax(no, jogadorAtual, maximizaPlayer):
    if vitoria(no['quadro'], 'X'):
        return 1
    if vitoria(no['quadro'], 'O'):
        return -1
    if empate(no['quadro']):
        return 0

    proxJogador = 'O' if jogadorAtual == 'X' else 'X'

    melhorPontuacao = float('-inf') if maximizaPlayer else float('inf')

    for filho in no['filhos']:
        pontuacao = minmax(filho, proxJogador, not maximizaPlayer)
        if maximizaPlayer:
            melhorPontuacao = max(melhorPontuacao, pontuacao)
        else:
            melhorPontuacao = min(melhorPontuacao, pontuacao)

    no['pontuacao'] = melhorPontuacao
    return melhorPontuacao

def melhor_jogada(tab):
    raiz = criar_no(tab)
    construir_arvore(raiz, 'O')
    minmax(raiz, 'X', True)

    melhorPontuacao = float('-inf')
    melhorJogada = -1

    for i, filho in enumerate(raiz['filhos']):
        if filho['pontuacao'] > melhorPontuacao:
            melhorPontuacao = filho['pontuacao']
            melhorJogada = i

    if melhorJogada != -1:
        tab[:] = raiz['filhos'][melhorJogada]['quadro']

def partida_com_jogador2(tab):
    jogador = 1
    p1 = p2 = jogadas = 0
    jogador1 = 'X'
    jogador2 = 'O'

    while p1 == 0 and p2 == 0 and jogadas < 9:
        imprimir_tabela(tab)

        if jogador == 1:
            coordenadas(tab, jogador1)
            p1 += completou_diag_princ(tab, jogador1)
            p1 += completou_diag_sec(tab, jogador1)
            p1 += completou_linhas(tab, jogador1)
            p1 += completou_colunas(tab, jogador1)
            jogador += 1
        else:
            melhor_jogada(tab)
            p2 += completou_diag_princ(tab, jogador2)
            p2 += completou_diag_sec(tab, jogador2)
            p2 += completou_linhas(tab, jogador2)
            p2 += completou_colunas(tab, jogador2)
            jogador -= 1

        jogadas += 1

    imprimir_tabela(tab)

    if p1 == 1:
        print("\n\tJogador 1 venceu!")
    elif p2 == 1:
        print("\n\tJogador 2 venceu!")
    else:
        print("\n\tEmpate!")

if __name__ == '__main__':
    tabela = criar_tabela()
    opcao = 1

    while opcao != 0:
        tabela = criar_tabela()
        partida_com_jogador2(tabela)

        opcao = int(input("\nContinuar jogando? (Sim - 1 / Nao - 0): "))
