"""
Jogo de Damas em Python com Interface Gráfica.
Ponto de entrada principal da aplicação.
"""

import tkinter as tk
from tkinter import ttk
from src.gui import GUIJogo
from src.models import Jogador
from src.ia import IA


class AplicacaoDamas:
    """Gerencia a tela inicial (seleção de modo/dificuldade/cor) e lança o jogo."""

    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Jogo de Damas")
        self.janela.geometry("400x420")
        self.janela.resizable(False, False)
        self._mostrar_menu_principal()

    def _limpar_janela(self) -> None:
        for widget in self.janela.winfo_children():
            widget.destroy()

    def _mostrar_menu_principal(self) -> None:
        """Tela inicial com escolha de modo."""
        self._limpar_janela()
        frame = tk.Frame(self.janela, bg="#CCCCCC")
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="Bem-vindo ao Jogo de Damas!",
                 font=("Arial", 18, "bold"), bg="#CCCCCC").pack(pady=20)
        tk.Label(frame, text="Escolha o modo de jogo:",
                 font=("Arial", 12), bg="#CCCCCC").pack(pady=10)

        tk.Button(
            frame,
            text="Dois Jogadores\n(Humano vs Humano)",
            font=("Arial", 12, "bold"), width=25, height=3,
            bg="#FF6B6B", activebackground="#FF5555",
            command=lambda: self._iniciar_jogo("humano")
        ).pack(pady=10)

        tk.Button(
            frame,
            text="Contra a IA\n(Humano vs Computador)",
            font=("Arial", 12, "bold"), width=25, height=3,
            bg="#4A90E2", activebackground="#3A7FD7",
            command=self._mostrar_opcoes_ia
        ).pack(pady=10)

        tk.Button(
            frame, text="Sair", font=("Arial", 12), width=25,
            bg="#CCCCCC", command=self.janela.quit
        ).pack(pady=10)

        tk.Label(
            frame, text="Jogador 1: Vermelho | Jogador 2: Azul",
            font=("Arial", 9), bg="#CCCCCC"
        ).pack(pady=20)

    def _mostrar_opcoes_ia(self) -> None:
        """Tela de opções do modo contra IA: dificuldade e cor do humano."""
        self._limpar_janela()
        frame = tk.Frame(self.janela, bg="#CCCCCC")
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="Contra a IA",
                 font=("Arial", 16, "bold"), bg="#CCCCCC").pack(pady=15)

        tk.Label(frame, text="Dificuldade:",
                 font=("Arial", 11), bg="#CCCCCC").pack(pady=(10, 2))
        dificuldade_var = tk.StringVar(value="medio")
        combo = ttk.Combobox(
            frame, textvariable=dificuldade_var, state="readonly",
            values=["facil", "medio", "dificil"], width=20
        )
        combo.pack(pady=5)

        tk.Label(frame, text="Sua cor:",
                 font=("Arial", 11), bg="#CCCCCC").pack(pady=(15, 2))
        cor_var = tk.StringVar(value="vermelho")
        tk.Radiobutton(
            frame, text="Vermelho (começa)", variable=cor_var, value="vermelho",
            bg="#CCCCCC", font=("Arial", 10)
        ).pack()
        tk.Radiobutton(
            frame, text="Azul (IA começa)", variable=cor_var, value="azul",
            bg="#CCCCCC", font=("Arial", 10)
        ).pack()

        tk.Button(
            frame, text="Iniciar Jogo", font=("Arial", 12, "bold"),
            width=20, bg="#4A90E2", activebackground="#3A7FD7",
            command=lambda: self._iniciar_jogo(
                "ia",
                dificuldade=dificuldade_var.get(),
                cor_humano=(Jogador.JOGADOR1 if cor_var.get() == "vermelho"
                            else Jogador.JOGADOR2),
            )
        ).pack(pady=20)

        tk.Button(
            frame, text="Voltar", font=("Arial", 10), width=15,
            command=self._mostrar_menu_principal
        ).pack()

    def _iniciar_jogo(self, modo: str, dificuldade: str = "medio",
                      cor_humano: Jogador = Jogador.JOGADOR1) -> None:
        """Fecha o menu e abre a janela do jogo."""
        self.janela.destroy()

        janela_jogo = tk.Tk()
        gui = GUIJogo(janela_jogo)

        if modo == "ia":
            jogador_ia = (Jogador.JOGADOR2 if cor_humano == Jogador.JOGADOR1
                          else Jogador.JOGADOR1)
            gui.jogo.modo_ia = True
            ia = IA(gui.jogo, dificuldade=dificuldade, jogador=jogador_ia)
            self._configurar_ia(gui, ia)

            # Se a IA joga primeiro (humano escolheu azul), disparar após render inicial
            if gui.jogo.jogador_atual == ia.jogador:
                gui.janela.after(500, lambda: self._executar_ia(gui, ia))

        gui.iniciar()

    def _configurar_ia(self, gui: GUIJogo, ia: IA) -> None:
        """Instala callback para a IA jogar automaticamente após cada atualização."""
        def callback_ia():
            if gui.jogo.jogador_atual == ia.jogador:
                gui.janela.after(500, lambda: self._executar_ia(gui, ia))

        gui._gerenciador.callback_pos_atualizacao = callback_ia

    def _executar_ia(self, gui: GUIJogo, ia: IA) -> None:
        """Executa o movimento da IA, re-verificando o turno (pode ter mudado via undo)."""
        if gui.jogo.jogador_atual == ia.jogador:
            ia.fazer_movimento()
            gui._atualizar_tela()

    def executar(self) -> None:
        self.janela.mainloop()


if __name__ == "__main__":
    print("=" * 60)
    print("JOGO DE DAMAS EM PYTHON".center(60))
    print("=" * 60)
    print("\nRegras do Jogo:")
    print("1. Peças movem apenas nas diagonais (casas pretas)")
    print("2. Peças comuns movem apenas para frente")
    print("3. Damas (promovidas) movem para frente e para trás")
    print("4. Capturas são obrigatórias")
    print("5. Múltiplas capturas em sequência são permitidas")
    print("6. Peça promovida a dama ao alcançar o lado oposto")
    print("7. Vence quem eliminar todas as peças do oponente")
    print("\nControles:")
    print("- Clique em uma peça para selecioná-la")
    print("- Clique em uma casa destacada para mover")
    print("- Verde = movimento simples | Laranja = captura")
    print("- Botão Desfazer reverte a última jogada")
    print("=" * 60 + "\n")

    app = AplicacaoDamas()
    app.executar()
