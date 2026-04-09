"""
Módulo de interface gráfica do jogo de damas.
Exporta a classe principal GUIJogo.
"""

from src.gui.gerenciador_interface import GerenciadorInterface


class GUIJogo:
    """
    Classe principal que gerencia a interface gráfica do jogo de damas.
    
    Esta classe serve como fachada para o GerenciadorInterface,
    mantendo compatibilidade com código existente.
    """

    def __init__(self, janela):
        """
        Inicializa a interface gráfica.
        
        Args:
            janela: A janela raiz do tkinter
        """
        from src.game import Jogo
        
        self.janela = janela
        self.janela.title("Jogo de Damas")
        self.janela.geometry("900x1000")
        self.janela.resizable(False, False)

        # Instância do jogo
        self.jogo = Jogo()

        # Criar gerenciador de interface
        self._gerenciador = GerenciadorInterface(self.janela, self.jogo)
        self._gerenciador.criar_interface()

    def _atualizar_tela(self) -> None:
        """Atualiza a tela (mantido para compatibilidade com IA)."""
        self._gerenciador._atualizar_tela()

    def iniciar(self) -> None:
        """Inicia a interface gráfica."""
        self.janela.mainloop()
