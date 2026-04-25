"""
Jogo de Damas em Python com Interface Gráfica.
Ponto de entrada principal da aplicação.
"""

import tkinter as tk
from tkinter import ttk
from src.gui import GUIJogo
from src.models import Jogador
from src.ia import IA
from src import config

_BG = config.COR_FUNDO_TABULEIRO
_FG = config.COR_TEXTO_PRINCIPAL
_FG2 = config.COR_TEXTO_SECUNDARIO


def _estilo_btn(frame, text, command, width=25, height=3,
                bg=None, active_bg=None, font=None):
    bg = bg or config.COR_BOTAO_PADRAO
    active_bg = active_bg or config.COR_BOTAO_PADRAO_HOVER
    font = font or ("Arial", 12, "bold")
    b = tk.Button(
        frame, text=text, command=command,
        width=width, height=height,
        bg=bg, fg="#FFFFFF",
        activebackground=active_bg, activeforeground="#FFFFFF",
        font=font, relief=tk.FLAT, cursor="hand2",
    )
    b.bind("<Enter>", lambda e: b.config(bg=active_bg))
    b.bind("<Leave>", lambda e: b.config(bg=bg))
    return b


class AplicacaoDamas:
    """Gerencia o ciclo de vida da aplicação com uma única janela raiz."""

    _MENU_W, _MENU_H = 420, 440
    _JOGO_W, _JOGO_H = 720, 840

    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Jogo de Damas")
        self.janela.resizable(False, False)
        self.janela.configure(bg=_BG)

        # Placar da sessão: compartilhado por referência com GerenciadorInterface
        self._placar = {Jogador.JOGADOR1: 0, Jogador.JOGADOR2: 0}

        # ID do after() da IA pendente (para cancelamento)
        self._after_ia_id = None

        self._centralizar_janela(self._MENU_W, self._MENU_H)
        self._mostrar_menu_principal()

    # ------------------------------------------------------------------
    # Utilitários
    # ------------------------------------------------------------------

    def _centralizar_janela(self, largura: int, altura: int) -> None:
        self.janela.update_idletasks()
        sw = self.janela.winfo_screenwidth()
        sh = self.janela.winfo_screenheight()
        x = (sw - largura) // 2
        y = (sh - altura) // 2
        self.janela.geometry(f"{largura}x{altura}+{x}+{y}")

    def _limpar_janela(self) -> None:
        for widget in self.janela.winfo_children():
            widget.destroy()

    # ------------------------------------------------------------------
    # Menu principal
    # ------------------------------------------------------------------

    def _mostrar_menu_principal(self) -> None:
        self._limpar_janela()
        self._centralizar_janela(self._MENU_W, self._MENU_H)

        frame = tk.Frame(self.janela, bg=_BG)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            frame, text="Jogo de Damas",
            font=("Arial", 22, "bold"), bg=_BG, fg=_FG,
        ).pack(pady=(30, 4))

        tk.Label(
            frame, text="Escolha o modo de jogo",
            font=("Arial", 11), bg=_BG, fg=_FG2,
        ).pack(pady=(0, 20))

        _estilo_btn(
            frame, "Dois Jogadores\n(Humano vs Humano)",
            lambda: self._iniciar_jogo("humano"),
            bg=config.COR_BOTAO_NOVO, active_bg=config.COR_BOTAO_NOVO_HOVER,
        ).pack(pady=8)

        _estilo_btn(
            frame, "Contra a IA\n(Humano vs Computador)",
            self._mostrar_opcoes_ia,
            bg=config.COR_BOTAO_IA, active_bg=config.COR_BOTAO_IA_HOVER,
        ).pack(pady=8)

        _estilo_btn(
            frame, "Sair", self.janela.quit,
            height=2, bg=config.COR_BOTAO_PADRAO,
            active_bg=config.COR_BOTAO_PADRAO_HOVER,
            font=("Arial", 11),
        ).pack(pady=8)

        tk.Label(
            frame, text="Vermelho = Jogador 1  |  Azul = Jogador 2",
            font=("Arial", 9), bg=_BG, fg=_FG2,
        ).pack(pady=(16, 0))

    # ------------------------------------------------------------------
    # Tela de opções da IA
    # ------------------------------------------------------------------

    def _mostrar_opcoes_ia(self) -> None:
        self._limpar_janela()

        frame = tk.Frame(self.janela, bg=_BG)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            frame, text="Contra a IA",
            font=("Arial", 18, "bold"), bg=_BG, fg=_FG,
        ).pack(pady=(30, 4))

        tk.Label(
            frame, text="Configure a partida",
            font=("Arial", 11), bg=_BG, fg=_FG2,
        ).pack(pady=(0, 20))

        tk.Label(
            frame, text="Dificuldade:",
            font=("Arial", 11, "bold"), bg=_BG, fg=_FG,
        ).pack(pady=(0, 4))

        dificuldade_var = tk.StringVar(value="medio")

        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure(
            "Menu.TCombobox",
            fieldbackground="#34495E", background="#34495E",
            foreground="#ECF0F1", selectbackground="#34495E",
            selectforeground="#ECF0F1",
        )

        combo = ttk.Combobox(
            frame, textvariable=dificuldade_var, state="readonly",
            values=["facil", "medio", "dificil"],
            width=22, style="Menu.TCombobox",
        )
        combo.pack(pady=(0, 16))

        tk.Label(
            frame, text="Sua cor:",
            font=("Arial", 11, "bold"), bg=_BG, fg=_FG,
        ).pack(pady=(0, 6))

        cor_var = tk.StringVar(value="vermelho")
        for valor, texto in [("vermelho", "Vermelho (voce comeca)"),
                              ("azul", "Azul (IA comeca)")]:
            tk.Radiobutton(
                frame, text=texto, variable=cor_var, value=valor,
                bg=_BG, fg=_FG, selectcolor="#1A252F",
                activebackground=_BG, activeforeground=_FG,
                font=("Arial", 10),
            ).pack(anchor=tk.CENTER)

        tk.Frame(frame, bg=_BG, height=16).pack()

        _estilo_btn(
            frame, "Iniciar Jogo",
            lambda: self._iniciar_jogo(
                "ia",
                dificuldade=dificuldade_var.get(),
                cor_humano=(Jogador.JOGADOR1 if cor_var.get() == "vermelho"
                            else Jogador.JOGADOR2),
            ),
            height=2,
            bg=config.COR_BOTAO_IA, active_bg=config.COR_BOTAO_IA_HOVER,
        ).pack(pady=8)

        _estilo_btn(
            frame, "Voltar", self._mostrar_menu_principal,
            height=2,
            bg=config.COR_BOTAO_PADRAO, active_bg=config.COR_BOTAO_PADRAO_HOVER,
            font=("Arial", 10),
        ).pack()

    # ------------------------------------------------------------------
    # Início e retorno do jogo
    # ------------------------------------------------------------------

    def _iniciar_jogo(self, modo: str, dificuldade: str = "medio",
                      cor_humano: Jogador = Jogador.JOGADOR1) -> None:
        self._limpar_janela()
        self._centralizar_janela(self._JOGO_W, self._JOGO_H)

        modo_ia = (modo == "ia")
        gui = GUIJogo(
            self.janela,
            modo_ia=modo_ia,
            callback_menu=self._retornar_ao_menu,
            dificuldade=dificuldade,
            cor_humano=cor_humano,
            placar=self._placar,
        )

        if modo_ia:
            jogador_ia = (Jogador.JOGADOR2 if cor_humano == Jogador.JOGADOR1
                          else Jogador.JOGADOR1)
            gui.jogo.modo_ia = True
            ia = IA(gui.jogo, dificuldade=dificuldade, jogador=jogador_ia)
            self._configurar_ia(gui, ia)

            if gui.jogo.jogador_atual == ia.jogador:
                self._agendar_ia(gui, ia)

    def _retornar_ao_menu(self) -> None:
        self._cancelar_ia_pendente()
        self._limpar_janela()
        self._mostrar_menu_principal()

    # ------------------------------------------------------------------
    # IA
    # ------------------------------------------------------------------

    def _agendar_ia(self, gui: GUIJogo, ia: IA) -> None:
        self._cancelar_ia_pendente()
        self._after_ia_id = self.janela.after(
            500, lambda: self._executar_ia(gui, ia)
        )

    def _cancelar_ia_pendente(self) -> None:
        if self._after_ia_id is not None:
            self.janela.after_cancel(self._after_ia_id)
            self._after_ia_id = None

    def _configurar_ia(self, gui: GUIJogo, ia: IA) -> None:
        def callback_ia():
            if gui.jogo.jogador_atual == ia.jogador:
                self._agendar_ia(gui, ia)

        gui._gerenciador.callback_pos_atualizacao = callback_ia

    def _executar_ia(self, gui: GUIJogo, ia: IA) -> None:
        self._after_ia_id = None
        if gui.jogo.jogador_atual == ia.jogador:
            ia.fazer_movimento()
            gui._atualizar_tela()

    # ------------------------------------------------------------------

    def executar(self) -> None:
        self.janela.mainloop()


if __name__ == "__main__":
    print("=" * 60)
    print("JOGO DE DAMAS EM PYTHON".center(60))
    print("=" * 60)
    print("\nControles:")
    print("- Clique em uma peca para selecioná-la")
    print("- Clique em uma casa destacada para mover")
    print("- Verde = movimento simples | Laranja = captura")
    print("- Capturas sao obrigatorias quando disponíveis")
    print("=" * 60 + "\n")

    app = AplicacaoDamas()
    app.executar()
