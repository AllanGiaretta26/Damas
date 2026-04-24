"""
Módulo de interface gráfica do jogo de damas usando tkinter.
Responsável por gerenciar a interface e interações do usuário.
"""

import tkinter as tk
from tkinter import messagebox
from src.models import Jogador, Tabuleiro
from src import config
from src.gui.renderizador import RenderizadorTabuleiro


class GerenciadorInterface:
    """
    Gerencia a interface gráfica do jogo de damas.
    
    Responsabilidades:
    - Criar elementos da interface (labels, botões, canvas)
    - Processar eventos de clique
    - Atualizar informações exibidas
    - Exibir diálogos (histórico, fim de jogo)
    
    Segue SRP: apenas gerencia UI, não lógica do jogo.
    """

    def __init__(self, janela: tk.Tk, jogo):
        """
        Inicializa o gerenciador de interface.
        
        Args:
            janela: A janela raiz do tkinter
            jogo: Instância do jogo atual
        """
        self.janela = janela
        self.jogo = jogo
        self.renderizador = RenderizadorTabuleiro(None)  # Será criado com canvas
        self.fim_de_jogo_exibido = False
        self.callback_pos_atualizacao = None  # Callback para IA

        # Elementos da UI
        self.label_info = None
        self.label_pecas = None
        self.canvas = None

    def criar_interface(self) -> None:
        """Cria todos os elementos da interface."""
        self._criar_frame_info()
        self._criar_canvas()
        self._criar_frame_botoes()
        self._atualizar_tela()

    def _criar_frame_info(self) -> None:
        """Cria frame superior para informações."""
        frame_info = tk.Frame(self.janela, bg="#CCCCCC", height=100)
        frame_info.pack(fill=tk.X, padx=10, pady=10)

        # Informações do jogo
        self.label_info = tk.Label(frame_info, text="", font=config.FONTE_INFO,
                                   bg="#CCCCCC")
        self.label_info.pack()

        self.label_pecas = tk.Label(frame_info, text="", font=config.FONTE_PEQUENA,
                                    bg="#CCCCCC")
        self.label_pecas.pack()

    def _criar_canvas(self) -> None:
        """Cria canvas para o tabuleiro."""
        self.canvas = tk.Canvas(
            self.janela,
            width=config.TAMANHO_CASA_PIXELS * 8,
            height=config.TAMANHO_CASA_PIXELS * 8,
            bg="#CCCCCC",
            cursor="hand2"
        )
        self.canvas.pack(padx=10, pady=10)
        self.canvas.bind("<Button-1>", self._ao_clicar_canvas)

        # Configurar renderizador com canvas
        self.renderizador = RenderizadorTabuleiro(self.canvas)

    def _criar_frame_botoes(self) -> None:
        """Cria frame inferior para botões."""
        frame_botoes = tk.Frame(self.janela, bg="#CCCCCC")
        frame_botoes.pack(fill=tk.X, padx=10, pady=10)

        btn_novo = tk.Button(frame_botoes, text="Novo Jogo",
                            command=self._novo_jogo, width=15)
        btn_novo.pack(side=tk.LEFT, padx=5)

        btn_desfazer = tk.Button(frame_botoes, text="Desfazer",
                                 command=self._desfazer, width=15)
        btn_desfazer.pack(side=tk.LEFT, padx=5)

        btn_historico = tk.Button(frame_botoes, text="Histórico",
                                 command=self._mostrar_historico, width=15)
        btn_historico.pack(side=tk.LEFT, padx=5)

        btn_sair = tk.Button(frame_botoes, text="Sair",
                            command=self.janela.quit, width=15)
        btn_sair.pack(side=tk.LEFT, padx=5)

    def _atualizar_tela(self) -> None:
        """Atualiza o canvas com o estado atual do jogo."""
        self.renderizador.desenhar_tabuleiro(self.jogo)
        self._atualizar_info()

        # Verificar fim de jogo
        fim_jogo, vencedor = self.jogo.verificar_fim_de_jogo()
        if fim_jogo and not self.fim_de_jogo_exibido:
            self.fim_de_jogo_exibido = True
            self._mostrar_fim_de_jogo(vencedor)
        
        # Chamar callback pós-atualização (para IA)
        if self.callback_pos_atualizacao:
            self.callback_pos_atualizacao()

    def _atualizar_info(self) -> None:
        """Atualiza as informações exibidas no topo."""
        jogador = "Jogador 1 (Vermelho)" if self.jogo.jogador_atual == Jogador.JOGADOR1 else "Jogador 2 (Azul)"
        sequencia = " - CAPTURA EM SEQUÊNCIA" if self.jogo.em_sequencia_captura else ""
        self.label_info.config(text=f"Turno: {jogador}{sequencia}")

        pecas_j1 = self.jogo.tabuleiro.contar_pecas(Jogador.JOGADOR1)
        pecas_j2 = self.jogo.tabuleiro.contar_pecas(Jogador.JOGADOR2)
        self.label_pecas.config(
            text=f"Peças - J1: {pecas_j1} | J2: {pecas_j2} | "
                 f"Capturadas - J1: {self.jogo.pecas_capturadas_j1} | "
                 f"J2: {self.jogo.pecas_capturadas_j2}"
        )

    def _ao_clicar_canvas(self, event) -> None:
        """Processa cliques no canvas."""
        # Calcular qual casa foi clicada
        coluna = event.x // config.TAMANHO_CASA_PIXELS
        linha = event.y // config.TAMANHO_CASA_PIXELS

        # Validar posição
        if not (0 <= linha < Tabuleiro.TAMANHO and
                0 <= coluna < Tabuleiro.TAMANHO):
            return

        # Delegar lógica do jogo para a classe Jogo
        self._processar_clique(linha, coluna)

    def _processar_clique(self, linha: int, coluna: int) -> None:
        """
        Processa clique em uma casa do tabuleiro.
        
        Args:
            linha: Linha clicada
            coluna: Coluna clicada
        """
        # Se estamos em captura em sequência
        if self.jogo.em_sequencia_captura:
            if (linha, coluna) in self.jogo.movimentos_validos:
                self.jogo.mover_peca(
                    self.jogo.peca_selecionada.linha,
                    self.jogo.peca_selecionada.coluna,
                    linha, coluna
                )
                self._atualizar_tela()
            return

        # Se já há uma peça selecionada
        if self.jogo.peca_selecionada:
            if (linha, coluna) in self.jogo.movimentos_validos:
                # Mover peça
                self.jogo.mover_peca(
                    self.jogo.peca_selecionada.linha,
                    self.jogo.peca_selecionada.coluna,
                    linha, coluna
                )
            elif (self.jogo.peca_selecionada.linha == linha and
                  self.jogo.peca_selecionada.coluna == coluna):
                # Desselecionar peça
                self.jogo.peca_selecionada = None
                self.jogo.movimentos_validos = []
            else:
                # Selecionar outra peça
                self.jogo.selecionar_peca(linha, coluna)
        else:
            # Tentar selecionar uma peça
            self.jogo.selecionar_peca(linha, coluna)

        self._atualizar_tela()

    def _novo_jogo(self) -> None:
        """Inicia um novo jogo."""
        self.jogo.resetar()
        self.fim_de_jogo_exibido = False
        self._atualizar_tela()

    def _desfazer(self) -> None:
        """Desfaz a última jogada. No modo IA, desfaz também o lance anterior do humano."""
        if not self.jogo.historico_jogadas:
            return

        self.jogo.desfazer_jogada()
        if getattr(self.jogo, 'modo_ia', False) and self.jogo.historico_jogadas:
            self.jogo.desfazer_jogada()

        self.fim_de_jogo_exibido = False
        self._atualizar_tela()

    def _mostrar_historico(self) -> None:
        """Mostra o histórico de jogadas."""
        if not self.jogo.historico_jogadas:
            messagebox.showinfo("Histórico", "Nenhuma jogada realizada ainda.")
            return

        texto = "Histórico de Jogadas:\n\n"
        for i, jogada in enumerate(self.jogo.historico_jogadas, 1):
            jogador = "J1" if jogada['jogador'] == Jogador.JOGADOR1 else "J2"
            de = jogada['de']
            para = jogada['para']
            texto += f"{i}. {jogador}: ({de[0]},{de[1]}) → ({para[0]},{para[1]})\n"

        self._criar_janela_historico(texto)

    def _criar_janela_historico(self, texto: str) -> None:
        """Cria janela de histórico."""
        janela_historico = tk.Toplevel(self.janela)
        janela_historico.title("Histórico")
        janela_historico.geometry("400x400")

        frame_texto = tk.Frame(janela_historico)
        frame_texto.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scrollbar = tk.Scrollbar(frame_texto)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        text_widget = tk.Text(frame_texto, yscrollcommand=scrollbar.set,
                             font=config.FONTE_INFO)
        text_widget.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_widget.yview)

        text_widget.insert("1.0", texto)
        text_widget.config(state=tk.DISABLED)

    def _mostrar_fim_de_jogo(self, vencedor: Jogador) -> None:
        """Mostra uma mensagem de fim de jogo."""
        nome_vencedor = "Jogador 1 (Vermelho)" if vencedor == Jogador.JOGADOR1 else "Jogador 2 (Azul)"
        messagebox.showinfo("Fim de Jogo!",
                           f"{nome_vencedor} venceu!\n"
                           f"Clique em 'Novo Jogo' para jogar novamente.")
