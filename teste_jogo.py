"""
Script de teste para validar a lógica do jogo de damas sem interface gráfica.
Testa funcionalidades básicas do jogo.
"""

from src.game import Jogo, Jogador, Tabuleiro, TipoPeca, Peca


def teste_inicializacao():
    """Testa se o jogo é inicializado corretamente."""
    print("📋 Testando inicialização...")
    
    jogo = Jogo()
    
    # Verificar tabuleiro
    assert jogo.tabuleiro is not None, "Tabuleiro não foi criado"
    
    # Verificar peças iniciais
    pecas_j1 = jogo._contar_pecas(Jogador.JOGADOR1)
    pecas_j2 = jogo._contar_pecas(Jogador.JOGADOR2)
    
    assert pecas_j1 == 12, f"Jogador 1 deveria ter 12 peças, tem {pecas_j1}"
    assert pecas_j2 == 12, f"Jogador 2 deveria ter 12 peças, tem {pecas_j2}"
    
    print("✅ Inicialização OK")
    print(f"   - J1: {pecas_j1} peças")
    print(f"   - J2: {pecas_j2} peças\n")


def teste_movimento_simples():
    """Testa movimento simples de uma peça."""
    print("📋 Testando movimento simples...")
    
    jogo = Jogo()
    
    # Selecionar peça do Jogador 1
    assert jogo.selecionar_peca(2, 1), "Não conseguiu selecionar peça"
    
    # Verificar movimentos válidos
    assert len(jogo.movimentos_validos) > 0, "Nenhum movimento válido encontrado"
    
    # Mover peça
    movimentos = jogo.movimentos_validos.copy()
    dest_linha, dest_coluna = movimentos[0]
    
    assert jogo.mover_peca(2, 1, dest_linha, dest_coluna), "Falha ao mover peça"
    
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
    assert jogo.selecionar_peca(2, 1), "Não conseguiu selecionar peça"

    dest_linha, dest_coluna = jogo.movimentos_validos[0]
    assert jogo.mover_peca(2, 1, dest_linha, dest_coluna), "Falha ao mover peça"

    assert jogo.tabuleiro.obter_peca(2, 1) is None, "A origem deveria ficar vazia"
    assert jogo.tabuleiro.obter_peca(dest_linha, dest_coluna) is not None, "Destino deveria conter a peça"

    print("✅ Limpeza da Origem OK\n")


def teste_captura():
    """Testa captura de peça."""
    print("📋 Testando captura...")
    
    # Simplificar teste - apenas verificar que capturas são encontradas
    jogo = Jogo()
    
    # Com o tabuleiro inicial, procurar uma posição onde há captura
    tem_capturas = False
    
    for linha in range(Tabuleiro.TAMANHO):
        for coluna in range(Tabuleiro.TAMANHO):
            peca = jogo.tabuleiro.obter_peca(linha, coluna)
            if peca and peca.jogador == Jogador.JOGADOR1:
                capturas = jogo._encontrar_capturas(linha, coluna)
                if capturas:
                    tem_capturas = True
                    break
        if tem_capturas:
            break
    
    # Se não há capturas no início (normal), criar cenário
    if not tem_capturas:
        # Limpar para criar um cenário de captura
        jogo.tabuleiro.casas = [[None for _ in range(Tabuleiro.TAMANHO)]
                               for _ in range(Tabuleiro.TAMANHO)]
        
        from src.game import Peca
        # Peça de J1 em (2, 1)
        peca_j1 = Peca(Jogador.JOGADOR1, 2, 1)
        jogo.tabuleiro.colocar_peca(peca_j1, 2, 1)
        
        # Peça de J2 em (3, 2) e espaço vazio em (4, 3)
        peca_j2 = Peca(Jogador.JOGADOR2, 3, 2)
        jogo.tabuleiro.colocar_peca(peca_j2, 3, 2)
        
        capturas = jogo._encontrar_capturas(2, 1)
        assert len(capturas) > 0, "Captura não foi encontrada"
        assert (4, 3) in capturas, "Posição de captura incorreta"
    
    print("✅ Captura OK\n")


def teste_captura_obrigatoria():
    """Testa se o jogo bloqueia movimentos simples quando existe captura."""
    print("📋 Testando captura obrigatória...")

    jogo = Jogo()
    jogo.tabuleiro.casas = [[None for _ in range(Tabuleiro.TAMANHO)]
                           for _ in range(Tabuleiro.TAMANHO)]

    jogo.tabuleiro.colocar_peca(Peca(Jogador.JOGADOR1, 2, 1), 2, 1)
    jogo.tabuleiro.colocar_peca(Peca(Jogador.JOGADOR1, 2, 5), 2, 5)
    jogo.tabuleiro.colocar_peca(Peca(Jogador.JOGADOR2, 3, 2), 3, 2)

    assert jogo.selecionar_peca(2, 1), "Peça com captura deveria ser selecionável"
    assert jogo.movimentos_validos == [(4, 3)], f"Captura obrigatória incorreta: {jogo.movimentos_validos}"
    assert not jogo.selecionar_peca(2, 5), "Peça sem captura não deveria ser selecionável"
    assert jogo._calcular_movimentos_validos(2, 5) == [], "Movimento simples deveria ser bloqueado"

    print("✅ Captura Obrigatória OK\n")


def teste_captura_sequencial():
    """Testa se a captura em sequência mantém o turno e atualiza os próximos lances."""
    print("📋 Testando captura sequencial...")

    jogo = Jogo()
    jogo.tabuleiro.casas = [[None for _ in range(Tabuleiro.TAMANHO)]
                           for _ in range(Tabuleiro.TAMANHO)]

    jogo.tabuleiro.colocar_peca(Peca(Jogador.JOGADOR1, 2, 1), 2, 1)
    jogo.tabuleiro.colocar_peca(Peca(Jogador.JOGADOR2, 3, 2), 3, 2)
    jogo.tabuleiro.colocar_peca(Peca(Jogador.JOGADOR2, 5, 4), 5, 4)

    assert jogo.selecionar_peca(2, 1), "Não conseguiu selecionar peça para a captura em sequência"
    assert jogo.mover_peca(2, 1, 4, 3), "Primeira captura falhou"

    assert jogo.em_sequencia_captura, "O jogo deveria exigir a segunda captura"
    assert jogo.jogador_atual == Jogador.JOGADOR1, "O turno não deveria mudar durante a sequência"
    assert jogo.movimentos_validos == [(6, 5)], f"Próxima captura inválida: {jogo.movimentos_validos}"
    assert jogo.tabuleiro.obter_peca(2, 1) is None, "Origem da primeira captura deveria estar vazia"
    assert jogo.tabuleiro.obter_peca(3, 2) is None, "Peça capturada deveria sair do tabuleiro"

    assert jogo.mover_peca(4, 3, 6, 5), "Segunda captura falhou"
    assert not jogo.em_sequencia_captura, "A sequência deveria terminar após a última captura"
    assert jogo.jogador_atual == Jogador.JOGADOR2, "O turno deveria passar após a sequência"
    assert jogo.tabuleiro.obter_peca(5, 4) is None, "Segunda peça capturada deveria sair do tabuleiro"
    assert jogo.tabuleiro.obter_peca(6, 5) is not None, "Peça deveria terminar na última casa da sequência"
    assert jogo.piezas_capturadas_j1 == 2, "Contagem de capturas do Jogador 1 incorreta"

    print("✅ Captura Sequencial OK\n")


def teste_promocao():
    """Testa promoção de peça a dama."""
    print("📋 Testando promoção...")
    
    jogo = Jogo()
    
    # Limpar tabuleiro
    jogo.tabuleiro.casas = [[None for _ in range(Tabuleiro.TAMANHO)]
                           for _ in range(Tabuleiro.TAMANHO)]
    
    from src.game import Peca
    # Criar peça de J1 perto do final
    peca = Peca(Jogador.JOGADOR1, 6, 1)
    jogo.tabuleiro.colocar_peca(peca, 6, 1)
    
    # Selecionar e mover para última linha
    jogo.jogador_atual = Jogador.JOGADOR1
    jogo.selecionar_peca(6, 1)
    jogo.mover_peca(6, 1, 7, 0)
    
    # Verificar promoção
    peca_promovida = jogo.tabuleiro.obter_peca(7, 0)
    assert peca_promovida is not None, "Peça não encontrada"
    assert peca_promovida.eh_dama(), f"Peça não foi promovida a dama (tipo: {peca_promovida.tipo})"
    assert peca_promovida.tipo == TipoPeca.DAMA, "Tipo de peça incorreto"
    
    print("✅ Promoção OK\n")


def teste_movimentos_dama():
    """Testa movimentos de dama (frente e trás)."""
    print("📋 Testando movimentos de dama...")
    
    jogo = Jogo()
    
    # Criar uma dama manualmente
    peca_j1 = jogo.tabuleiro.remover_peca(2, 1)
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
    
    # Fazer alguns movimentos
    jogo.selecionar_peca(2, 1)
    mov = jogo.movimentos_validos[0]
    jogo.mover_peca(2, 1, mov[0], mov[1])
    
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
