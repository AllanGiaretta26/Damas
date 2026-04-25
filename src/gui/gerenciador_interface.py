"""
Módulo de interface gráfica do jogo de damas usando tkinter.
Responsável por gerenciar a interface e interações do usuário.
"""

import tkinter as tk
from tkinter import messagebox
from src.models import Jogador, Tabuleiro
from src import config
from src.gui.renderizador import RenderizadorTabuleiro

_BG = config.COR_FUNDO_TABULEIRO
_FG = config.COR_TEXTO_PRINCIPAL
_FG2 = config.COR_TEXTO_SECUNDARIO
_BTN_BG = config.COR_BOTAO_PADRAO
_BTN_BG_H = config.COR_BOTAO_PADRAO_HOVER


def _btn(parent, text, command, width=12, bg=None, fg="#FFFFFF",
         active_bg=None, font=None):
    bg = bg or _BTN_BG
    active_bg = active_bg or _BTN_BG_H
    font = font or config.FONTE_PEQUENA
    b = tk.Button(
        parent, text=text, command=command, width=width,
        bg=bg, fg=fg, activebackground=active_bg, activeforeground=fg,
        font=font, relief=tk.FLAT, cursor="hand2",
        padx=6, pady=4,
    )
    b.bind("<Enter>", lambda e: b.config(bg=active_bg))
    b.bind("<Leave>", lambda e: b.config(bg=bg))
    return b


class GerenciadorInterface:
    """
    Gerencia a interface gráfica do jogo de damas.

    Responsabilidades:
    - Criar elementos da interface (labels, botões, canvas)
    - Processar eventos de clique
    - Atualizar informações exibidas
    - Exibir diálogos (histórico, fim de jogo)
    """

    def __init__(self, janela: tk.Tk, jogo, modo_ia: bool = False,
                 callback_menu=None, dificuldade: str = "",
                 cor_humano: Jogador = Jogador.JOGADOR1,
                 placar: dict = None):
        self.janela = janela
        self.jogo = jogo
        self.modo_ia = modo_ia
        self.callback_menu = callback_menu
        self.dificuldade = dificuldade
        self.cor_humano = cor_humano
        self.placar = placar  # dict compartilhado; chaves Jogador (HvH) ou "humano"/"ia" (IA)
        self.renderizador = RenderizadorTabuleiro(None)
        self.fim_de_jogo_exibido = False
        self.callback_pos_atualizacao = None

        self.label_modo = None
        self.label_info = None
        self.label_pecas = None
        self.label_placar = None
        self.canvas = None

    def criar_interface(self) -> None:
        self._criar_frame_info()
        self._criar_canvas()
        self._criar_frame_botoes()
        self._atualizar_tela()

    # ------------------------------------------------------------------
    # Criação de widgets
    # ------------------------------------------------------------------

    def _criar_frame_info(self) -> None:
        frame_info = tk.Frame(self.janela, bg=_BG, pady=8)
        frame_info.pack(fill=tk.X, padx=12)

        if self.modo_ia:
            nomes = {"facil": "Fácil", "medio": "Médio", "dificil": "Difícil"}
            nivel = nomes.get(self.dificuldade, self.dificuldade.capitalize())
            cor_nome = "Vermelho" if self.cor_humano == Jogador.JOGADOR1 else "Azul"
            self.label_modo = tk.Label(
                frame_info,
                text=f"Modo: IA — {nivel}  |  Você joga de {cor_nome}",
                font=config.FONTE_PEQUENA, bg=_BG, fg=_FG2,
            )
            self.label_modo.pack()

        self.label_info = tk.Label(
            frame_info, text="", font=config.FONTE_INFO, bg=_BG, fg=_FG,
        )
        self.label_info.pack()

        self.label_pecas = tk.Label(
            frame_info, text="", font=config.FONTE_PEQUENA, bg=_BG, fg=_FG2,
        )
        self.label_pecas.pack()

        self.label_placar = tk.Label(
            frame_info, text="", font=config.FONTE_PEQUENA, bg=_BG, fg=_FG2,
        )
        self.label_placar.pack()

    def _criar_canvas(self) -> None:
        coord = config.TAMANHO_COORDENADAS_PIXELS
        tamanho = config.TAMANHO_CASA_PIXELS * 8 + coord
        self.canvas = tk.Canvas(
            self.janela, width=tamanho, height=tamanho,
            bg=_BG, cursor="hand2", highlightthickness=0,
        )
        self.canvas.pack(padx=12, pady=4)
        self.canvas.bind("<Button-1>", self._ao_clicar_canvas)
        self.renderizador = RenderizadorTabuleiro(self.canvas)

    def _criar_frame_botoes(self) -> None:
        frame_botoes = tk.Frame(self.janela, bg=_BG, pady=6)
        frame_botoes.pack(fill=tk.X, padx=12)

        # Grupo: ações da partida
        _btn(frame_botoes, "Novo Jogo", self._novo_jogo,
             bg=config.COR_BOTAO_NOVO, active_bg=config.COR_BOTAO_NOVO_HOVER,
             ).pack(side=tk.LEFT, padx=4)

        _btn(frame_botoes, "Empate", self._oferecer_empate,
             bg=config.COR_BOTAO_EMPATE, active_bg=config.COR_BOTAO_EMPATE_HOVER,
             ).pack(side=tk.LEFT, padx=4)

        if self.modo_ia:
            _btn(frame_botoes, "Desfazer", self._desfazer,
                 ).pack(side=tk.LEFT, padx=4)

        # Separador visual
        tk.Frame(frame_botoes, bg="#3D5166", width=2).pack(
            side=tk.LEFT, fill=tk.Y, padx=8, pady=4,
        )

        # Grupo: navegação
        _btn(frame_botoes, "Histórico", self._mostrar_historico,
             ).pack(side=tk.LEFT, padx=4)

        if self.callback_menu:
            _btn(frame_botoes, "Menu", self._confirmar_menu,
                 ).pack(side=tk.LEFT, padx=4)

        _btn(frame_botoes, "Sair", self.janela.quit,
             ).pack(side=tk.LEFT, padx=4)

    # ------------------------------------------------------------------
    # Atualização de estado
    # ------------------------------------------------------------------

    def _atualizar_tela(self) -> None:
        self.renderizador.desenhar_tabuleiro(self.jogo)
        self._atualizar_info()

        fim_jogo, vencedor = self.jogo.verificar_fim_de_jogo()
        if fim_jogo and not self.fim_de_jogo_exibido:
            self.fim_de_jogo_exibido = True
            self._mostrar_fim_de_jogo(vencedor)

        if self.callback_pos_atualizacao:
            self.callback_pos_atualizacao()

    def _atualizar_info(self) -> None:
        eh_j1 = self.jogo.jogador_atual == Jogador.JOGADOR1

        if self.modo_ia:
            eh_humano = self.jogo.jogador_atual == self.cor_humano
            jogador_str = "Seu turno" if eh_humano else "Vez da IA..."
        else:
            jogador_str = (
                "Jogador 1 (Vermelho)" if eh_j1 else "Jogador 2 (Azul)"
            )

        sequencia = "  —  CAPTURA EM SEQUENCIA" if self.jogo.em_sequencia_captura else ""
        self.label_info.config(text=f"Turno: {jogador_str}{sequencia}")

        pecas_j1 = self.jogo.tabuleiro.contar_pecas(Jogador.JOGADOR1)
        pecas_j2 = self.jogo.tabuleiro.contar_pecas(Jogador.JOGADOR2)
        self.label_pecas.config(
            text=(
                f"Pecas  J1: {pecas_j1}  |  J2: {pecas_j2}  |  "
                f"Capturadas  J1: {self.jogo.pecas_capturadas_j1}  |  "
                f"J2: {self.jogo.pecas_capturadas_j2}"
            )
        )

        if self.placar and self.label_placar:
            if self.modo_ia:
                h = self.placar.get("humano", 0)
                a = self.placar.get("ia", 0)
                self.label_placar.config(text=f"Placar (sessao): Voce {h} x {a} IA")
            else:
                v1 = self.placar.get(Jogador.JOGADOR1, 0)
                v2 = self.placar.get(Jogador.JOGADOR2, 0)
                self.label_placar.config(text=f"Placar (sessao): J1 {v1} x {v2} J2")

    # ------------------------------------------------------------------
    # Eventos do canvas
    # ------------------------------------------------------------------

    def _ao_clicar_canvas(self, event) -> None:
        coord = config.TAMANHO_COORDENADAS_PIXELS
        x = event.x - coord
        y = event.y - coord
        if x < 0 or y < 0:
            return
        coluna = x // config.TAMANHO_CASA_PIXELS
        linha = y // config.TAMANHO_CASA_PIXELS
        if not (0 <= linha < Tabuleiro.TAMANHO and 0 <= coluna < Tabuleiro.TAMANHO):
            return
        self._processar_clique(linha, coluna)

    def _processar_clique(self, linha: int, coluna: int) -> None:
        if self.jogo.em_sequencia_captura:
            if (linha, coluna) in self.jogo.movimentos_validos:
                self.jogo.mover_peca(
                    self.jogo.peca_selecionada.linha,
                    self.jogo.peca_selecionada.coluna,
                    linha, coluna,
                )
                self._atualizar_tela()
            return

        if self.jogo.peca_selecionada:
            if (linha, coluna) in self.jogo.movimentos_validos:
                self.jogo.mover_peca(
                    self.jogo.peca_selecionada.linha,
                    self.jogo.peca_selecionada.coluna,
                    linha, coluna,
                )
            elif (self.jogo.peca_selecionada.linha == linha and
                  self.jogo.peca_selecionada.coluna == coluna):
                self.jogo.peca_selecionada = None
                self.jogo.movimentos_validos = []
            else:
                self.jogo.selecionar_peca(linha, coluna)
        else:
            self.jogo.selecionar_peca(linha, coluna)

        self._atualizar_tela()

    # ------------------------------------------------------------------
    # Ações dos botões
    # ------------------------------------------------------------------

    def _novo_jogo(self) -> None:
        if (self.jogo.historico_jogadas and
                not messagebox.askyesno(
                    "Novo Jogo", "Deseja abandonar a partida atual?")):
            return
        self.jogo.resetar()
        self.fim_de_jogo_exibido = False
        self._atualizar_tela()

    def _oferecer_empate(self) -> None:
        if not self.jogo.historico_jogadas:
            return
        if not messagebox.askyesno(
                "Propor Empate",
                "Propor empate?\nO jogo sera encerrado sem vencedor."):
            return
        self.jogo.resetar()
        self.fim_de_jogo_exibido = False
        self._atualizar_tela()
        messagebox.showinfo("Empate", "Empate registrado.\nNenhuma pontuacao atribuida.")

    def _desfazer(self) -> None:
        if not self.jogo.historico_jogadas:
            return
        self.jogo.desfazer_jogada()
        if self.jogo.modo_ia and self.jogo.historico_jogadas:
            self.jogo.desfazer_jogada()
        self.fim_de_jogo_exibido = False
        self._atualizar_tela()

    def _confirmar_menu(self) -> None:
        if (self.jogo.historico_jogadas and
                not messagebox.askyesno(
                    "Voltar ao Menu", "Deseja abandonar a partida atual?")):
            return
        self.callback_menu()

    def _mostrar_historico(self) -> None:
        if not self.jogo.historico_jogadas:
            messagebox.showinfo("Historico", "Nenhuma jogada realizada ainda.")
            return

        texto = "Historico de Jogadas:\n\n"
        for i, jogada in enumerate(self.jogo.historico_jogadas, 1):
            jogador = "J1" if jogada['jogador'] == Jogador.JOGADOR1 else "J2"
            de = jogada['de']
            para = jogada['para']
            texto += f"{i:>3}. {jogador}: ({de[0]},{de[1]}) -> ({para[0]},{para[1]})\n"

        self._criar_janela_historico(texto)

    def _criar_janela_historico(self, texto: str) -> None:
        win = tk.Toplevel(self.janela)
        win.title("Historico de Jogadas")
        win.geometry("360x420")
        win.configure(bg=_BG)
        win.resizable(False, False)
        win.transient(self.janela)
        win.grab_set()

        frame = tk.Frame(win, bg=_BG)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        text_widget = tk.Text(
            frame, yscrollcommand=scrollbar.set, font=config.FONTE_INFO,
            bg="#1A252F", fg=_FG, relief=tk.FLAT, padx=8, pady=8,
        )
        text_widget.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_widget.yview)

        text_widget.insert("1.0", texto)
        text_widget.config(state=tk.DISABLED)

    def _mostrar_fim_de_jogo(self, vencedor: Jogador) -> None:
        if self.placar is not None:
            chave = ("humano" if vencedor == self.cor_humano else "ia") if self.modo_ia else vencedor
            self.placar[chave] = self.placar.get(chave, 0) + 1
            self._atualizar_info()

        if self.modo_ia:
            eh_humano = vencedor == self.cor_humano
            nome_vencedor = "Voce venceu!" if eh_humano else "A IA venceu!"
        else:
            nome_vencedor = (
                "Jogador 1 (Vermelho) venceu!"
                if vencedor == Jogador.JOGADOR1
                else "Jogador 2 (Azul) venceu!"
            )
        messagebox.showinfo(
            "Fim de Jogo",
            f"{nome_vencedor}\n\nClique em 'Novo Jogo' para jogar novamente.",
        )
