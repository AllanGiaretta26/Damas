"""
Módulo de interface gráfica do jogo de damas.
Exporta a classe principal GUIJogo.
"""

from src.gui.gerenciador_interface import GerenciadorInterface
from src.models import Jogador


class GUIJogo:
    """
    Fachada sobre GerenciadorInterface.

    Aceita a janela raiz já existente para que o ciclo de vida da janela
    seja controlado externamente (arquitetura de janela única).
    """

    def __init__(self, janela, modo_ia: bool = False, callback_menu=None,
                 dificuldade: str = "", cor_humano: Jogador = Jogador.JOGADOR1,
                 placar: dict = None):
        from src.game import Jogo

        self.janela = janela
        self.janela.title("Jogo de Damas")

        self.jogo = Jogo()

        self._gerenciador = GerenciadorInterface(
            janela, self.jogo,
            modo_ia=modo_ia,
            callback_menu=callback_menu,
            dificuldade=dificuldade,
            cor_humano=cor_humano,
            placar=placar,
        )
        self._gerenciador.criar_interface()

    def _atualizar_tela(self) -> None:
        self._gerenciador._atualizar_tela()

    def iniciar(self) -> None:
        """No-op: o mainloop é gerenciado pela raiz em AplicacaoDamas.executar()."""
