"""
Exemplos avançados de uso do Jogo de Damas

Este arquivo mostra como usar as classes do jogo de forma programática
além da interface gráfica.
"""

from src.game import Jogo, Jogador, Tabuleiro, Peca, TipoPeca
from src.ia import IA


def exemplo_1_jogo_automatizado():
    """
    Exemplo 1: Simular um jogo entre a IA e ela mesma
    (Útil para testar estratégias)
    """
    print("\n" + "="*60)
    print("EXEMPLO 1: IA vs IA (Jogo Automatizado)")
    print("="*60 + "\n")
    
    jogo = Jogo()
    ia1 = IA(jogo)
    ia1.jogador = Jogador.JOGADOR1
    
    ia2 = IA(jogo)
    ia2.jogador = Jogador.JOGADOR2
    
    movimento_num = 0
    max_movimentos = 50  # Limite para evitar loops infinitos
    
    while movimento_num < max_movimentos:
        # Verificar fim de jogo
        fim_jogo, vencedor = jogo.verificar_fim_de_jogo()
        if fim_jogo:
            nome = "IA 1" if vencedor == Jogador.JOGADOR1 else "IA 2"
            print(f"\n✅ Jogo terminado! {nome} venceu!")
            print(f"   Total de movimentos: {movimento_num}")
            break
        
        # Fazer movimento
        ia_atual = ia1 if jogo.jogador_atual == Jogador.JOGADOR1 else ia2
        sucesso = ia_atual.fazer_movimento()
        
        if not sucesso:
            print("\n❌ Erro ao fazer movimento")
            break
        
        movimento_num += 1
        
        # Mostrar status a cada 5 movimentos
        if movimento_num % 5 == 0:
            j1_count = jogo._contar_pecas(Jogador.JOGADOR1)
            j2_count = jogo._contar_pecas(Jogador.JOGADOR2)
            print(f"Movimento {movimento_num}: J1={j1_count} peças, J2={j2_count} peças")


def exemplo_2_criar_tabuleiro_customizado():
    """
    Exemplo 2: Criar um tabuleiro com posição customizada
    (Útil para testar cenários específicos)
    """
    print("\n" + "="*60)
    print("EXEMPLO 2: Tabuleiro Customizado")
    print("="*60 + "\n")
    
    jogo = Jogo()
    
    # Limpar tabuleiro
    jogo.tabuleiro.casas = [[None for _ in range(Tabuleiro.TAMANHO)]
                           for _ in range(Tabuleiro.TAMANHO)]
    
    # Criar cenário: final de jogo
    peca_j1_1 = Peca(Jogador.JOGADOR1, 7, 0)
    peca_j1_1.promover()  # Promover para dama
    jogo.tabuleiro.colocar_peca(peca_j1_1, 7, 0)
    
    peca_j2_1 = Peca(Jogador.JOGADOR2, 0, 7)
    peca_j2_1.promover()  # Promover para dama
    jogo.tabuleiro.colocar_peca(peca_j2_1, 0, 7)
    
    peca_j2_2 = Peca(Jogador.JOGADOR2, 2, 3)
    jogo.tabuleiro.colocar_peca(peca_j2_2, 2, 3)
    
    # Exibir estatísticas
    print("Cenário criado:")
    print(f"  - J1: {jogo._contar_pecas(Jogador.JOGADOR1)} peça(s)")
    print(f"  - J2: {jogo._contar_pecas(Jogador.JOGADOR2)} peça(s)")
    
    # Mostrar movimentos disponíveis para J1
    jogo.selecionar_peca(7, 0)
    print(f"\nMovimentos disponíveis para J1 em (7,0):")
    if jogo.movimentos_validos:
        for mov in jogo.movimentos_validos:
            print(f"  → ({mov[0]},{mov[1]})")
    else:
        print("  (nenhum)")


def exemplo_3_analisar_movimentos():
    """
    Exemplo 3: Analisar todos os movimentos disponíveis
    """
    print("\n" + "="*60)
    print("EXEMPLO 3: Análise de Movimentos Disponíveis")
    print("="*60 + "\n")
    
    jogo = Jogo()
    
    print(f"Jogador atual: {jogo.jogador_atual.name}\n")
    
    # Contar movimentos de cada peça
    total_movimentos = 0
    pecas_com_capturas = 0
    
    for linha in range(Tabuleiro.TAMANHO):
        for coluna in range(Tabuleiro.TAMANHO):
            peca = jogo.tabuleiro.obter_peca(linha, coluna)
            if peca and peca.jogador == jogo.jogador_atual:
                movimentos = jogo._calcular_movimentos_validos(linha, coluna)
                capturas = jogo._encontrar_capturas(linha, coluna)
                
                total_movimentos += len(movimentos)
                if capturas:
                    pecas_com_capturas += 1
                
                tipo = "DAMA" if peca.eh_dama() else "PEÇA"
                print(f"({linha},{coluna}) [{tipo}]: {len(movimentos)} movimentos")
    
    print(f"\n{'='*40}")
    print(f"Total de movimentos: {total_movimentos}")
    print(f"Peças com capturas: {pecas_com_capturas}")


def exemplo_4_replay_historico():
    """
    Exemplo 4: Mostrar histórico de um jogo
    """
    print("\n" + "="*60)
    print("EXEMPLO 4: Histórico de Jogo")
    print("="*60 + "\n")
    
    jogo = Jogo()
    
    # Fazer alguns movimentos
    movimentos_exemplo = [
        (2, 1, 3, 0),
        (5, 4, 4, 5),
        (2, 3, 3, 2),
    ]
    
    for origem_linha, origem_coluna, dest_linha, dest_coluna in movimentos_exemplo:
        if jogo.selecionar_peca(origem_linha, origem_coluna):
            if jogo.mover_peca(origem_linha, origem_coluna, 
                               dest_linha, dest_coluna):
                print(f"✅ Movimento OK: ({origem_linha},{origem_coluna}) → ({dest_linha},{dest_coluna})")
            else:
                print(f"❌ Movimento falhou")
        else:
            break
    
    # Mostrar histórico
    print(f"\nHistórico total: {len(jogo.historico_jogadas)} movimento(s)")
    print("-" * 50)
    
    for i, jogada in enumerate(jogo.historico_jogadas, 1):
        jogador_nome = "J1" if jogada['jogador'] == Jogador.JOGADOR1 else "J2"
        de = jogada['de']
        para = jogada['para']
        print(f"{i}. {jogador_nome}: ({de[0]},{de[1]}) → ({para[0]},{para[1]})")


def exemplo_5_testar_regras():
    """
    Exemplo 5: Testar regras específicas do jogo
    """
    print("\n" + "="*60)
    print("EXEMPLO 5: Validação de Regras")
    print("="*60 + "\n")
    
    jogo = Jogo()
    
    # Teste 1: Peça comum não pode se mover para trás
    print("1. Teste: Peça comum não pode se mover para trás")
    peca = jogo.tabuleiro.obter_peca(2, 1)
    movimentos = jogo._calcular_movimentos_validos(2, 1)
    todos_para_frente = all(m[0] > 2 for m in movimentos)
    print(f"   ✅ Validado" if todos_para_frente else "   ❌ Falhou")
    
    # Teste 2: Movimentos devem ser apenas nas diagonais
    print("\n2. Teste: Movimentos apenas em diagonais")
    movimentos = jogo._calcular_movimentos_validos(2, 1)
    todas_diagonais = all(
        abs(m[0] - 2) == abs(m[1] - 1) for m in movimentos
    )
    print(f"   ✅ Validado" if todas_diagonais else "   ❌ Falhou")
    
    # Teste 3: Peça não pode se mover para posição ocupada
    print("\n3. Teste: Posições ocupadas são inacessíveis")
    for linha in range(Tabuleiro.TAMANHO):
        for coluna in range(Tabuleiro.TAMANHO):
            movimentos = jogo._calcular_movimentos_validos(linha, coluna)
            todas_vazias = all(
                jogo.tabuleiro.obter_peca(m[0], m[1]) is None 
                for m in movimentos
            )
            if not todas_vazias:
                print(f"   ❌ Falhou")
                return
    print(f"   ✅ Validado")


if __name__ == "__main__":
    print("\n" * 2)
    print("╔" + "="*58 + "╗")
    print("║" + "EXEMPLOS DE USO DO JOGO DE DAMAS".center(58) + "║")
    print("╚" + "="*58 + "╝")
    
    exemplo_1_jogo_automatizado()
    exemplo_2_criar_tabuleiro_customizado()
    exemplo_3_analisar_movimentos()
    exemplo_4_replay_historico()
    exemplo_5_testar_regras()
    
    print("\n" * 2)
    print("✅ Todos os exemplos executados com sucesso!")
    print("")
