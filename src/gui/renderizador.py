"""
Módulo de renderização da interface gráfica do jogo de damas.
Responsável apenas por desenhar elementos na tela (SRP).
"""

import tkinter as tk
from src.models import Tabuleiro, Peca, Jogador, TipoPeca
from src import config


class RenderizadorTabuleiro:
    """
    Responsável apenas por renderizar o tabuleiro e peças.
    Segue SRP: não gerencia estado do jogo, apenas desenha.
    """

    def __init__(self, canvas: tk.Canvas):
        """Inicializa o renderizador."""
        self.canvas = canvas
        self.tamanho_casa = config.TAMANHO_CASA_PIXELS

    def desenhar_tabuleiro(self, jogo) -> None:
        """
        Desenha o tabuleiro completo com peças e destaques.
        
        Args:
            jogo: Instância do jogo atual
        """
        self.canvas.delete("all")
        self._desenhar_casas(jogo)
        self._desenhar_pecas(jogo)

    def _desenhar_casas(self, jogo) -> None:
        """Desenha as casas do tabuleiro com destaques."""
        for linha in range(Tabuleiro.TAMANHO):
            for coluna in range(Tabuleiro.TAMANHO):
                x1 = coluna * self.tamanho_casa
                y1 = linha * self.tamanho_casa
                x2 = x1 + self.tamanho_casa
                y2 = y1 + self.tamanho_casa

                cor = self._determinar_cor_casa(linha, coluna, jogo)
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=cor,
                                           outline="gray")

    def _determinar_cor_casa(self, linha: int, coluna: int, jogo) -> str:
        """Determina a cor de uma casa baseada em seu estado."""
        # Destacar movimentos válidos
        if (linha, coluna) in jogo.movimentos_validos:
            return self._cor_destaque_movimento(jogo)

        # Destacar peça selecionada
        if (jogo.peca_selecionada and
            linha == jogo.peca_selecionada.linha and
            coluna == jogo.peca_selecionada.coluna):
            return config.COR_SELECIONADA

        # Cor normal
        if (linha + coluna) % 2 == 0:
            return config.COR_CASA_BRANCA
        else:
            return config.COR_CASA_PRETA

    def _cor_destaque_movimento(self, jogo) -> str:
        """Retorna cor de destaque baseada no tipo de movimento."""
        if jogo.peca_selecionada:
            # Obter primeira posição de movimento válido para determinar tipo
            for (mov_linha, mov_coluna) in jogo.movimentos_validos:
                diff = abs(mov_linha - jogo.peca_selecionada.linha)
                if diff == 2:
                    return config.COR_CAPTURA
                else:
                    return config.COR_MOVIMENTO_VALIDO
        return config.COR_MOVIMENTO_VALIDO

    def _desenhar_pecas(self, jogo) -> None:
        """Desenha todas as peças no tabuleiro."""
        for linha in range(Tabuleiro.TAMANHO):
            for coluna in range(Tabuleiro.TAMANHO):
                peca = jogo.tabuleiro.obter_peca(linha, coluna)
                if peca is None:
                    continue

                self._desenhar_peca_individual(peca, linha, coluna)

    def _desenhar_peca_individual(self, peca: Peca, linha: int, coluna: int) -> None:
        """Desenha uma única peça."""
        x = coluna * self.tamanho_casa + self.tamanho_casa // 2
        y = linha * self.tamanho_casa + self.tamanho_casa // 2
        raio = self.tamanho_casa // 2 - 5

        cor = config.COR_PECA_JOGADOR1 if peca.jogador == Jogador.JOGADOR1 else config.COR_PECA_JOGADOR2

        # Desenhar círculo da peça
        self.canvas.create_oval(
            x - raio, y - raio, x + raio, y + raio,
            fill=cor, outline="black", width=2
        )

        # Desenhar coroa se for dama
        if peca.eh_dama():
            self._desenhar_coroa(x, y)

    def _desenhar_coroa(self, x: int, y: int) -> None:
        """Desenha uma coroa no centro da peça para indicar dama."""
        self.canvas.create_text(x, y, text="♛", font=("Arial", 20),
                               fill=config.COR_DAMA)
