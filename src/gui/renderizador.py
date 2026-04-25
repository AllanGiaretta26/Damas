"""
Módulo de renderização da interface gráfica do jogo de damas.
Responsável apenas por desenhar elementos na tela (SRP).
"""

import tkinter as tk
from src.models import Tabuleiro, Peca, Jogador, TipoPeca
from src import config

_LETRAS = "ABCDEFGH"
_COR_COORD = "#BDC3C7"


class RenderizadorTabuleiro:
    """
    Responsável apenas por renderizar o tabuleiro e peças.
    Segue SRP: não gerencia estado do jogo, apenas desenha.
    """

    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas
        self.tamanho_casa = config.TAMANHO_CASA_PIXELS
        self.offset = config.TAMANHO_COORDENADAS_PIXELS

    def desenhar_tabuleiro(self, jogo) -> None:
        self.canvas.delete("all")
        self._desenhar_coordenadas()
        self._desenhar_casas(jogo)
        self._desenhar_pecas(jogo)

    # ------------------------------------------------------------------
    # Coordenadas
    # ------------------------------------------------------------------

    def _desenhar_coordenadas(self) -> None:
        off = self.offset
        tc = self.tamanho_casa
        meio = tc // 2
        fonte = ("Arial", 9, "bold")

        for i, letra in enumerate(_LETRAS):
            x = off + i * tc + meio
            self.canvas.create_text(x, off // 2, text=letra,
                                    fill=_COR_COORD, font=fonte)

        for i in range(Tabuleiro.TAMANHO):
            y = off + i * tc + meio
            numero = str(Tabuleiro.TAMANHO - i)
            self.canvas.create_text(off // 2, y, text=numero,
                                    fill=_COR_COORD, font=fonte)

    # ------------------------------------------------------------------
    # Casas
    # ------------------------------------------------------------------

    def _desenhar_casas(self, jogo) -> None:
        off = self.offset
        tc = self.tamanho_casa
        for linha in range(Tabuleiro.TAMANHO):
            for coluna in range(Tabuleiro.TAMANHO):
                x1 = off + coluna * tc
                y1 = off + linha * tc
                cor = self._determinar_cor_casa(linha, coluna, jogo)
                self.canvas.create_rectangle(
                    x1, y1, x1 + tc, y1 + tc,
                    fill=cor, outline="gray",
                )

    def _determinar_cor_casa(self, linha: int, coluna: int, jogo) -> str:
        if (linha, coluna) in jogo.movimentos_validos:
            return self._cor_destaque_movimento(jogo)

        if (jogo.peca_selecionada and
                linha == jogo.peca_selecionada.linha and
                coluna == jogo.peca_selecionada.coluna):
            return config.COR_SELECIONADA

        return config.COR_CASA_BRANCA if (linha + coluna) % 2 == 0 else config.COR_CASA_PRETA

    def _cor_destaque_movimento(self, jogo) -> str:
        if jogo.peca_selecionada:
            for (mov_linha, _) in jogo.movimentos_validos:
                diff = abs(mov_linha - jogo.peca_selecionada.linha)
                return config.COR_CAPTURA if diff == 2 else config.COR_MOVIMENTO_VALIDO
        return config.COR_MOVIMENTO_VALIDO

    # ------------------------------------------------------------------
    # Peças
    # ------------------------------------------------------------------

    def _desenhar_pecas(self, jogo) -> None:
        for linha in range(Tabuleiro.TAMANHO):
            for coluna in range(Tabuleiro.TAMANHO):
                peca = jogo.tabuleiro.obter_peca(linha, coluna)
                if peca is not None:
                    self._desenhar_peca_individual(peca, linha, coluna)

    def _desenhar_peca_individual(self, peca: Peca, linha: int, coluna: int) -> None:
        off = self.offset
        tc = self.tamanho_casa
        x = off + coluna * tc + tc // 2
        y = off + linha * tc + tc // 2
        raio = tc // 2 - 5

        cor = (config.COR_PECA_JOGADOR1
               if peca.jogador == Jogador.JOGADOR1
               else config.COR_PECA_JOGADOR2)

        self.canvas.create_oval(
            x - raio, y - raio, x + raio, y + raio,
            fill=cor, outline="black", width=2,
        )

        if peca.eh_dama():
            self.canvas.create_text(x, y, text="♛",
                                    font=("Arial", 20), fill=config.COR_DAMA)
