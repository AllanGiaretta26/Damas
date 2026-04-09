# Explicação do Código - Jogo de Damas

1. O projeto implementa um **jogo de damas completo** em Python com interface gráfica utilizando tkinter.

2. A **classe AplicacaoDamas** é o ponto de entrada que gerencia a seleção do modo de jogo (jogador vs jogador ou jogador vs IA).

3. O módulo **src/game.py** contém a lógica do jogo com as regras completas: movimentos diagonais, capturas, promoções e detecção de fim de jogo.

4. O módulo **src/gui.py** gerencia a interface gráfica com tabuleiro 8x8, cores alternadas, destaque visual de movimentos válidos e histórico de jogadas.

5. O módulo **src/ia.py** implementa uma inteligência artificial simples que permite jogar contra o computador com estratégias de movimento automático.

6. O **tabuleiro** segue as regras clássicas de damas com peças brancas e pretas distribuídas corretamente nas posições iniciais.

7. O sistema de **turnos alternados** garante que apenas o jogador ativo possa realizar movimentos e validar automaticamente todas as jogadas.

8. A **detecção de movimentos válidos** considera apenas deslocamentos nas diagonais, respeitando a captura de peças adversárias quando disponível.

9. As **peças promovidas** se tornam damas (reis) quando atingem o final do tabuleiro, ganhando a habilidade de se mover em múltiplas diagonais.

10. A aplicação oferece opções de **reinício de partida** e **visualização do histórico de movimentos** para melhor experiência do usuário.
