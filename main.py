"""
Jogo de Damas em Python com Interface Gráfica
Ponto de entrada principal da aplicação.

Este programa implementa um jogo de damas completo com as seguintes características:
- Interface gráfica em tkinter
- Tabuleiro 8x8 com cores alternadas
- Peças distribuídas corretamente
- Movimentos válidos apenas nas diagonais (preto e branco)
- Regras completas: movimentos simples, capturas, promoções
- Sistema de turnos entre dois jogadores
- Destaque visual para movimentos válidos
- Validação automática de jogadas
- Detecção de fim de jogo
- IA simples (opcional) para jogar contra o computador
- Histórico de jogadas
- Reinício de partida
"""

import tkinter as tk
from tkinter import simpledialog, messagebox
from src.gui import GUIJogo
from src.game import Jogo, Jogador
from src.ia import IA


class AplicacaoDamas:
    """
    Classe principal da aplicação que gerencia a seleção de modo de jogo
    e a inicialização da interface gráfica.
    """
    
    def __init__(self):
        """Inicializa a aplicação."""
        self.janela = tk.Tk()
        self.modo_jogo = None
        self.ia = None
        self._criar_tela_inicial()
    
    def _criar_tela_inicial(self):
        """Cria a tela inicial de seleção de modo."""
        self.janela.title("Jogo de Damas")
        self.janela.geometry("400x300")
        self.janela.resizable(False, False)
        
        # Frame principal
        frame_principal = tk.Frame(self.janela, bg="#CCCCCC")
        frame_principal.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = tk.Label(frame_principal, text="Bem-vindo ao Jogo de Damas!",
                         font=("Arial", 18, "bold"), bg="#CCCCCC")
        titulo.pack(pady=20)
        
        # Subtítulo
        subtitulo = tk.Label(frame_principal,
                            text="Escolha o modo de jogo:",
                            font=("Arial", 12), bg="#CCCCCC")
        subtitulo.pack(pady=10)
        
        # Botão para jogar contra humano
        btn_humano = tk.Button(
            frame_principal,
            text="👥 Dois Jogadores\n(Humano vs Humano)",
            font=("Arial", 12, "bold"),
            width=25, height=3,
            bg="#FF6B6B",
            activebackground="#FF5555",
            command=lambda: self._iniciar_jogo("humano")
        )
        btn_humano.pack(pady=10)
        
        # Botão para jogar contra IA
        btn_ia = tk.Button(
            frame_principal,
            text="🤖 Contra a IA\n(Humano vs Computador)",
            font=("Arial", 12, "bold"),
            width=25, height=3,
            bg="#4A90E2",
            activebackground="#3A7FD7",
            command=lambda: self._iniciar_jogo("ia")
        )
        btn_ia.pack(pady=10)
        
        # Botão para sair
        btn_sair = tk.Button(
            frame_principal,
            text="Sair",
            font=("Arial", 12),
            width=25,
            bg="#CCCCCC",
            command=self.janela.quit
        )
        btn_sair.pack(pady=10)
        
        # Informações
        info = tk.Label(
            frame_principal,
            text="Jogador 1: Vermelho | Jogador 2: Azul",
            font=("Arial", 9),
            bg="#CCCCCC"
        )
        info.pack(pady=20)
    
    def _iniciar_jogo(self, modo: str):
        """Inicia o jogo no modo especificado."""
        self.modo_jogo = modo
        self.janela.destroy()
        
        # Criar nova janela para o jogo
        janela_jogo = tk.Tk()
        gui = GUIJogo(janela_jogo)
        
        if modo == "ia":
            self.ia = IA(gui.jogo)
            # Configurar callback para movimento da IA
            self._configurar_ia(gui)
        
        gui.iniciar()
    
    def _configurar_ia(self, gui: GUIJogo):
        """Configura os callbacks para a IA jogar automaticamente."""
        def ao_atualizar_tela():
            """Chamado após cada atualização da tela."""
            if gui.jogo.jogador_atual == Jogador.JOGADOR2:
                # Programar movimento da IA
                gui.janela.after(500, lambda: executar_ia(gui))
        
        # Salvar método original
        gui._atualizar_tela_original = gui._atualizar_tela
        
        def nova_atualizar_tela():
            """Sobrepõe o método de atualizar tela."""
            gui._atualizar_tela_original()
            ao_atualizar_tela()
        
        # Substituir método
        gui._atualizar_tela = nova_atualizar_tela
    
    def executar(self):
        """Executa a aplicação."""
        self.janela.mainloop()


def executar_ia(gui: GUIJogo):
    """Executa um movimento da IA."""
    if gui.jogo.jogador_atual == Jogador.JOGADOR2:
        ia = IA(gui.jogo)
        ia.fazer_movimento()
        gui._atualizar_tela()


if __name__ == "__main__":
    """Ponto de entrada da aplicação."""
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
    print("- Verde = movimento simples")
    print("- Laranja = captura")
    print("=" * 60 + "\n")
    
    app = AplicacaoDamas()
    app.executar()
