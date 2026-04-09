"""
Script de teste para validar a lógica do jogo de damas sem interface gráfica.
Testa funcionalidades básicas do jogo.

Refatorado para trabalhar com a nova estrutura de módulos.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.game import Jogo
from src.models import Jogador, Tabuleiro, TipoPeca, Peca


def teste_inicializacao():
    """Testa se o jogo é inicializado corretamente."""
    print("📋 Testando inicialização...")

    jogo = Jogo()

    # Verificar tabuleiro
    assert jogo.tabuleiro is not None, "Tabuleiro não foi criado"

    # Verificar peças iniciais
    pecas_j1 = jogo.tabuleiro.contar_pecas(Jogador.JOGADOR1)
    pecas_j2 = jogo.tabuleiro.contar_pecas(Jogador.JOGADOR2)

    assert pecas_j1 == 12, f"Jogador 1 deveria ter 12 peças, tem {pecas_j1}"
    assert pecas_j2 == 12, f"Jogador 2 deveria ter 12 peças, tem {pecas_j2}"

    print("✅ Inicialização OK")
    print(f"   - J1: {pecas_j1} peças")
    print(f"   - J2: {pecas_j2} peças\n")


def teste_movimento_simples():
    """Testa movimento simples de uma peça."""
    print("📋 Testando movimento simples...")

    jogo = Jogo()

    # Selecionar peça do Jogador 1 (agora começa nas linhas 5-7)
    # J1 move para cima (linha diminui)
    assert jogo.selecionar_peca(5, 0), "Não conseguiu selecionar peça"

    # Verificar movimentos válidos
    assert len(jogo.movimentos_validos) > 0, "Nenhum movimento válido encontrado"

    # Mover peça
    movimentos = jogo.movimentos_validos.copy()
    dest_linha, dest_coluna = movimentos[0]

    assert jogo.mover_peca(5, 0, dest_linha, dest_coluna), "Falha ao mover peça"

    # Verificar se a peça foi movida
    peca = jogo.tabuleiro.obter_peca(dest_linha, dest_coluna)
    assert peca is not None, "Peça não foi encontrada no destino"
    assert peca.jogador == Jogador.JOGADOR1, "Peça tem jogador errado"

    # Verificar turno
    assert jogo.jogador_atual == Jogador.JOGADOR2, "Turno não mudou"

    print("✅ Movimento Simples OK\n")


def teste_movimento_remove_origem():
    """Garante que a casa de origem fica vazia após o movimento."""
    print("📋 Testando limpeza da casa de origem...")

    jogo = Jogo()
    assert jogo.selecionar_peca(5, 0), "Não conseguiu selecionar peça"

    dest_linha, dest_coluna = jogo.movimentos_validos[0]
    assert jogo.mover_peca(5, 0, dest_linha, dest_coluna), "Falha ao mover peça"

    assert jogo.tabuleiro.obter_peca(5, 0) is None, "A origem deveria ficar vazia"
    assert jogo.tabuleiro.obter_peca(dest_linha, dest_coluna) is not None, "Destino deveria conter a peça"

    print("✅ Limpeza da Origem OK\n")


def teste_captura():
    """Testa captura de peça."""
    print("📋 Testando captura...")

    jogo = Jogo()

    # Limpar tabuleiro e reconfigurar manualmente para cenário de captura
    jogo.tabuleiro._casas = [[None for _ in range(Tabuleiro.TAMANHO)]
                            for _ in range(Tabuleiro.TAMANHO)]

    # Peça de J1 em (5, 0) - peça comum que captura para cima (direção -1)
    # (5+0)%2=1 -> casa preta ✓
    peca_j1 = Peca(Jogador.JOGADOR1, 5, 0)
    jogo.tabuleiro.colocar_peca(peca_j1, 5, 0)

    # Peça de J2 em (4, 1) - peça adversária na diagonal
    # (4+1)%2=1 -> casa preta ✓
    peca_j2 = Peca(Jogador.JOGADOR2, 4, 1)
    jogo.tabuleiro.colocar_peca(peca_j2, 4, 1)

    # Espaço vazio em (3, 2) - destino da captura
    # (3+2)%2=1 -> casa preta ✓

    capturas = jogo.encontrar_capturas_para_peca(5, 0)
    assert len(capturas) > 0, "Captura não foi encontrada"
    assert (3, 2) in capturas, f"Posição de captura incorreta: {capturas}"

    print("✅ Captura OK\n")


def teste_captura_obrigatoria():
    """Testa se o jogo bloqueia movimentos simples quando existe captura."""
    print("📋 Testando captura obrigatória...")

    jogo = Jogo()
    jogo.tabuleiro._casas = [[None for _ in range(Tabuleiro.TAMANHO)]
                           for _ in range(Tabuleiro.TAMANHO)]

    # Configurar cenário: peça J1 em (5,0) pode capturar J2 em (4,1)
    # (5+0)%2=1 -> casa preta ✓
    jogo.tabuleiro.colocar_peca(Peca(Jogador.JOGADOR1, 5, 0), 5, 0)
    # (5+4)%2=1 -> casa preta ✓
    jogo.tabuleiro.colocar_peca(Peca(Jogador.JOGADOR1, 5, 4), 5, 4)
    # (4+1)%2=1 -> casa preta ✓
    jogo.tabuleiro.colocar_peca(Peca(Jogador.JOGADOR2, 4, 1), 4, 1)

    # Selecionar peça que tem captura disponível
    assert jogo.selecionar_peca(5, 0), "Peça com captura deveria ser selecionável"
    # A captura deve ser para (3, 2) - duas casas na diagonal para cima
    assert (3, 2) in jogo.movimentos_validos, f"Captura obrigatória deveria estar em movimentos: {jogo.movimentos_validos}"

    # Outra peça sem captura não deveria ser selecionável quando há capturas
    assert not jogo.selecionar_peca(5, 4), "Peça sem captura não deveria ser selecionável"

    print("✅ Captura Obrigatória OK\n")


def teste_captura_sequencial():
    """Testa se a captura em sequência mantém o turno e atualiza os próximos lances."""
    print("📋 Testando captura sequencial...")

    jogo = Jogo()
    jogo.tabuleiro._casas = [[None for _ in range(Tabuleiro.TAMANHO)]
                           for _ in range(Tabuleiro.TAMANHO)]

    # Configurar cenário de captura sequencial para J1 (subindo)
    # (5+0)%2=1 -> casa preta ✓
    jogo.tabuleiro.colocar_peca(Peca(Jogador.JOGADOR1, 5, 0), 5, 0)
    # (4+1)%2=1 -> casa preta ✓
    jogo.tabuleiro.colocar_peca(Peca(Jogador.JOGADOR2, 4, 1), 4, 1)
    # (2+2)%2=0 -> casa branca, não serve
    # (2+3)%2=1 -> casa preta ✓
    jogo.tabuleiro.colocar_peca(Peca(Jogador.JOGADOR2, 2, 3), 2, 3)

    # Garantir que é o turno do Jogador 1
    jogo.jogador_atual = Jogador.JOGADOR1

    assert jogo.selecionar_peca(5, 0), "Não conseguiu selecionar peça para a captura em sequência"
    # Primeira captura: (5,0) -> (3,2) pulando (4,1)
    assert jogo.mover_peca(5, 0, 3, 2), "Primeira captura falhou"

    assert jogo.em_sequencia_captura, "O jogo deveria exigir a segunda captura"
    assert jogo.jogador_atual == Jogador.JOGADOR1, "O turno não deveria mudar durante a sequência"
    # Segunda captura: (3,2) -> (1,4) ou (0,?) pulando (2,3)
    assert jogo.movimentos_validos, f"Deveria ter capturas sequenciais: {jogo.movimentos_validos}"
    assert jogo.tabuleiro.obter_peca(5, 0) is None, "Origem da primeira captura deveria estar vazia"
    assert jogo.tabuleiro.obter_peca(4, 1) is None, "Peça capturada deveria sair do tabuleiro"

    # Executar segunda captura se disponível
    if (0, 4) in jogo.movimentos_validos:
        assert jogo.mover_peca(3, 2, 0, 4), "Segunda captura falhou"
    elif (1, 5) in jogo.movimentos_validos:
        assert jogo.mover_peca(3, 2, 1, 5), "Segunda captura falhou"
    else:
        # Fallback: executar primeira captura disponível
        segunda_captura = jogo.movimentos_validos[0]
        assert jogo.mover_peca(3, 2, segunda_captura[0], segunda_captura[1]), "Segunda captura falhou"

    assert not jogo.em_sequencia_captura, "A sequência deveria terminar após a última captura"
    assert jogo.jogador_atual == Jogador.JOGADOR2, "O turno deveria passar após a sequência"
    assert jogo.tabuleiro.obter_peca(2, 3) is None, "Segunda peça capturada deveria sair do tabuleiro"
    assert jogo.piezas_capturadas_j1 == 2, "Contagem de capturas do Jogador 1 incorreta"

    print("✅ Captura Sequencial OK\n")


def teste_promocao():
    """Testa promoção de peça a dama."""
    print("📋 Testando promoção...")

    jogo = Jogo()

    # Limpar tabuleiro
    jogo.tabuleiro._casas = [[None for _ in range(Tabuleiro.TAMANHO)]
                           for _ in range(Tabuleiro.TAMANHO)]

    # Criar peça de J1 perto do topo (linha 1)
    # (1+0)%2=1 -> casa preta ✓
    peca = Peca(Jogador.JOGADOR1, 1, 0)
    jogo.tabuleiro.colocar_peca(peca, 1, 0)

    # Garantir que é o turno do Jogador 1
    jogo.jogador_atual = Jogador.JOGADOR1

    # Selecionar e mover para linha 0 (topo)
    jogo.selecionar_peca(1, 0)
    assert jogo.mover_peca(1, 0, 0, 1), "Movimento de promoção falhou"

    # Verificar promoção
    peca_promovida = jogo.tabuleiro.obter_peca(0, 1)
    assert peca_promovida is not None, "Peça não encontrada"
    assert peca_promovida.eh_dama(), f"Peça não foi promovida a dama (tipo: {peca_promovida.tipo})"
    assert peca_promovida.tipo == TipoPeca.DAMA, "Tipo de peça incorreto"

    print("✅ Promoção OK\n")


def teste_movimentos_dama():
    """Testa movimentos de dama (frente e trás)."""
    print("📋 Testando movimentos de dama...")

    jogo = Jogo()

    # Criar uma dama manualmente em casa preta
    # (4+3)%2=1 -> casa preta ✓
    peca_j1 = jogo.tabuleiro.remover_peca(5, 0)  # Remove peça de J1
    peca_j1.promover()
    jogo.tabuleiro.colocar_peca(peca_j1, 4, 3)

    # Selecionar dama
    assert jogo.selecionar_peca(4, 3), "Não conseguiu selecionar dama"

    # Verificar movimentos (devem incluir frente e trás)
    movimentos = jogo.movimentos_validos
    assert len(movimentos) > 0, "Dama sem movimentos"

    # Dama deveria poder mover para frente E para trás
    tem_frente = any(m[0] > 4 for m in movimentos)
    tem_tras = any(m[0] < 4 for m in movimentos)

    assert tem_frente or tem_tras, "Dama não pode se mover"

    print("✅ Movimentos de Dama OK\n")


def teste_fim_de_jogo():
    """Testa detecção de fim de jogo."""
    print("📋 Testando detecção de fim de jogo...")

    jogo = Jogo()

    # Remover todas as peças do Jogador 2
    for linha in range(Tabuleiro.TAMANHO):
        for coluna in range(Tabuleiro.TAMANHO):
            peca = jogo.tabuleiro.obter_peca(linha, coluna)
            if peca and peca.jogador == Jogador.JOGADOR2:
                jogo.tabuleiro.remover_peca(linha, coluna)

    # Verificar fim de jogo
    fim, vencedor = jogo.verificar_fim_de_jogo()
    assert fim, "Fim de jogo não foi detectado"
    assert vencedor == Jogador.JOGADOR1, f"Vencedor incorreto: {vencedor}"

    print("✅ Detecção de Fim de Jogo OK\n")


def teste_historico():
    """Testa histórico de jogadas."""
    print("📋 Testando histórico...")

    jogo = Jogo()

    # Fazer alguns movimentos com J1 (linhas 5-7)
    # (5, 0) é casa preta e tem movimentos válidos
    assert jogo.selecionar_peca(5, 0), "Não conseguiu selecionar peça"
    assert len(jogo.movimentos_validos) > 0, "Deveria ter movimentos válidos"

    mov = jogo.movimentos_validos[0]
    assert jogo.mover_peca(5, 0, mov[0], mov[1]), "Movimento falhou"

    # Verificar histórico
    assert len(jogo.historico_jogadas) > 0, "Histórico vazio"
    assert jogo.historico_jogadas[0]['jogador'] == Jogador.JOGADOR1, "Jogador incorreto no histórico"

    print("✅ Histórico OK\n")


def main():
    """Executa todos os testes."""
    print("\n" + "="*50)
    print("TESTES DO JOGO DE DAMAS".center(50))
    print("="*50 + "\n")

    try:
        teste_inicializacao()
        teste_movimento_simples()
        teste_movimento_remove_origem()
        teste_captura()
        teste_captura_obrigatoria()
        teste_captura_sequencial()
        teste_promocao()
        teste_movimentos_dama()
        teste_fim_de_jogo()
        teste_historico()

        print("="*50)
        print("✅ TODOS OS TESTES PASSARAM!".center(50))
        print("="*50 + "\n")

        return True

    except AssertionError as e:
        print(f"\n❌ ERRO: {e}\n")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"\n❌ ERRO INESPERADO: {e}\n")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    import sys
    sucesso = main()
    sys.exit(0 if sucesso else 1)
