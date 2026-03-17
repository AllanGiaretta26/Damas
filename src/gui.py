"""
Módulo de interface gráfica do jogo de damas usando tkinter.
Responsável por renderizar o tabuleiro, peças e gerenciar interações do usuário.
"""

import tkinter as tk
from tkinter import messagebox
from src.game import Jogo, Jogador, TipoPeca, Tabuleiro
from src import config
from typing import Optional, Tuple


class GUIJogo:
    """
    Classe que gerencia a interface gráfica do jogo de damas.
    
    Renderiza o tabuleiro, peças e processa cliques do mouse.
    """
    
    def __init__(self, janela: tk.Tk):
        """
        Inicializa a interface gráfica.
        
        Args:
            janela: A janela raiz do tkinter
        """
        self.janela = janela
        self.janela.title("Jogo de Damas")
        self.janela.geometry("900x1000")
        self.janela.resizable(False, False)
        
        # Configurações visuais (usando arquivo de configuração)
        self.TAMANHO_CASA = config.TAMANHO_CASA_PIXELS
        self.COR_PRETA = config.COR_CASA_PRETA
        self.COR_BRANCA = config.COR_CASA_BRANCA
        self.COR_SELECIONADA = config.COR_SELECIONADA
        self.COR_MOVIMENTO = config.COR_MOVIMENTO_VALIDO
        self.COR_CAPTURA = config.COR_CAPTURA
        
        # Cores das peças
        self.COR_PECA_J1 = config.COR_PECA_JOGADOR1
        self.COR_PECA_J2 = config.COR_PECA_JOGADOR2
        self.COR_DAMA = config.COR_DAMA
        
        # Instância do jogo
        self.jogo = Jogo()
        self.peca_selecionada_canvas = None
        self.fim_de_jogo_exibido = False
        
        # Criar interface
        self._criar_interface()
    
    def _criar_interface(self):
        """Cria os elementos da interface."""
        # Frame superior para informações
        frame_info = tk.Frame(self.janela, bg="#CCCCCC", height=100)
        frame_info.pack(fill=tk.X, padx=10, pady=10)
        
        # Informações do jogo
        self.label_info = tk.Label(frame_info, text="", font=("Arial", 12),
                                   bg="#CCCCCC")
        self.label_info.pack()
        
        self.label_pecas = tk.Label(frame_info, text="", font=("Arial", 10),
                                    bg="#CCCCCC")
        self.label_pecas.pack()
        
        # Canvas para o tabuleiro
        self.canvas = tk.Canvas(
            self.janela,
            width=self.TAMANHO_CASA * 8,
            height=self.TAMANHO_CASA * 8,
            bg="#CCCCCC",
            cursor="hand2"
        )
        self.canvas.pack(padx=10, pady=10)
        self.canvas.bind("<Button-1>", self._ao_clicar_canvas)
        
        # Frame inferior para botões
        frame_botoes = tk.Frame(self.janela, bg="#CCCCCC")
        frame_botoes.pack(fill=tk.X, padx=10, pady=10)
        
        btn_novo = tk.Button(frame_botoes, text="Novo Jogo",
                            command=self._novo_jogo, width=15)
        btn_novo.pack(side=tk.LEFT, padx=5)
        
        btn_historico = tk.Button(frame_botoes, text="Histórico",
                                 command=self._mostrar_historico, width=15)
        btn_historico.pack(side=tk.LEFT, padx=5)
        
        btn_sair = tk.Button(frame_botoes, text="Sair",
                            command=self.janela.quit, width=15)
        btn_sair.pack(side=tk.LEFT, padx=5)
        
        # Desenhar tabuleiro inicial
        self._atualizar_tela()
    
    def _atualizar_tela(self):
        """Atualiza o canvas com o estado atual do jogo."""
        self.canvas.delete("all")
        
        # Desenhar tabuleiro
        self._desenhar_tabuleiro()
        
        # Desenhar peças
        self._desenhar_pecas()
        
        # Atualizar informações
        self._atualizar_info()
        
        # Verificar fim de jogo
        fim_jogo, vencedor = self.jogo.verificar_fim_de_jogo()
        if fim_jogo and not self.fim_de_jogo_exibido:
            self.fim_de_jogo_exibido = True
            self._mostrar_fim_de_jogo(vencedor)
    
    def _desenhar_tabuleiro(self):
        """Desenha o tabuleiro com cores alternadas."""
        for linha in range(Tabuleiro.TAMANHO):
            for coluna in range(Tabuleiro.TAMANHO):
                x1 = coluna * self.TAMANHO_CASA
                y1 = linha * self.TAMANHO_CASA
                x2 = x1 + self.TAMANHO_CASA
                y2 = y1 + self.TAMANHO_CASA
                
                # Determinar cor da casa
                if (linha + coluna) % 2 == 0:
                    cor = self.COR_BRANCA
                else:
                    cor = self.COR_PRETA
                
                # Destacar movimentos válidos
                if (linha, coluna) in self.jogo.movimentos_validos:
                    # Verificar se é captura ou movimento simples
                    if self.jogo.peca_selecionada:
                        diff = abs(linha - self.jogo.peca_selecionada.linha)
                        if diff == 2:
                            cor = self.COR_CAPTURA
                        else:
                            cor = self.COR_MOVIMENTO
                
                # Destacar peça selecionada
                if (self.jogo.peca_selecionada and
                    linha == self.jogo.peca_selecionada.linha and
                    coluna == self.jogo.peca_selecionada.coluna):
                    cor = self.COR_SELECIONADA
                
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=cor,
                                           outline="gray")
    
    def _desenhar_pecas(self):
        """Desenha todas as peças no tabuleiro."""
        for linha in range(Tabuleiro.TAMANHO):
            for coluna in range(Tabuleiro.TAMANHO):
                peca = self.jogo.tabuleiro.obter_peca(linha, coluna)
                if peca is None:
                    continue
                
                # Calcular posição no canvas
                x = coluna * self.TAMANHO_CASA + self.TAMANHO_CASA // 2
                y = linha * self.TAMANHO_CASA + self.TAMANHO_CASA // 2
                raio = self.TAMANHO_CASA // 2 - 5
                
                # Determinar cor da peça
                if peca.jogador == Jogador.JOGADOR1:
                    cor = self.COR_PECA_J1
                else:
                    cor = self.COR_PECA_J2
                
                # Desenhar círculo da peça
                self.canvas.create_oval(
                    x - raio, y - raio, x + raio, y + raio,
                    fill=cor, outline="black", width=2
                )
                
                # Desenhar coroa se for dama
                if peca.eh_dama():
                    self._desenhar_coroa(x, y, raio)
    
    def _desenhar_coroa(self, x: int, y: int, raio: int):
        """Desenha uma coroa no centro da peça para indicar dama."""
        tamanho = raio // 2
        # Desenha um "D" simples para indicar dama
        self.canvas.create_text(x, y, text="♛", font=("Arial", 20),
                               fill=self.COR_DAMA)
    
    def _atualizar_info(self):
        """Atualiza as informações exibidas no topo."""
        jogador = "Jogador 1 (Vermelho)" if self.jogo.jogador_atual == Jogador.JOGADOR1 else "Jogador 2 (Azul)"
        sequencia = " - CAPTURA EM SEQUÊNCIA" if self.jogo.em_sequencia_captura else ""
        self.label_info.config(text=f"Turno: {jogador}{sequencia}")
        
        pecas_j1 = self.jogo._contar_pecas(Jogador.JOGADOR1)
        pecas_j2 = self.jogo._contar_pecas(Jogador.JOGADOR2)
        self.label_pecas.config(
            text=f"Peças - J1: {pecas_j1} | J2: {pecas_j2} | "
                 f"Capturadas - J1: {self.jogo.piezas_capturadas_j1} | "
                 f"J2: {self.jogo.piezas_capturadas_j2}"
        )
    
    def _ao_clicar_canvas(self, event):
        """Processa cliques no canvas."""
        # Calcular qual casa foi clicada
        coluna = event.x // self.TAMANHO_CASA
        linha = event.y // self.TAMANHO_CASA
        
        # Validar posição
        if not (0 <= linha < Tabuleiro.TAMANHO and 
                0 <= coluna < Tabuleiro.TAMANHO):
            return
        
        # Se estamos em captura em sequência
        if self.jogo.em_sequencia_captura:
            if (linha, coluna) in self.jogo.movimentos_validos:
                if self.jogo.mover_peca(
                    self.jogo.peca_selecionada.linha,
                    self.jogo.peca_selecionada.coluna,
                    linha, coluna
                ):
                    self._atualizar_tela()
            return
        
        # Se já há uma peça selecionada
        if self.jogo.peca_selecionada:
            if (linha, coluna) in self.jogo.movimentos_validos:
                # Mover peça
                if self.jogo.mover_peca(
                    self.jogo.peca_selecionada.linha,
                    self.jogo.peca_selecionada.coluna,
                    linha, coluna
                ):
                    self._atualizar_tela()
            elif (self.jogo.peca_selecionada.linha == linha and
                  self.jogo.peca_selecionada.coluna == coluna):
                # Desselecionar peça
                self.jogo.peca_selecionada = None
                self.jogo.movimentos_validos = []
                self._atualizar_tela()
            else:
                # Selecionar outra peça
                if self.jogo.selecionar_peca(linha, coluna):
                    self._atualizar_tela()
        else:
            # Tentar selecionar uma peça
            if self.jogo.selecionar_peca(linha, coluna):
                self._atualizar_tela()
    
    def _novo_jogo(self):
        """Inicia um novo jogo."""
        self.jogo.resetar()
        self.peca_selecionada_canvas = None
        self.fim_de_jogo_exibido = False
        self._atualizar_tela()
    
    def _mostrar_historico(self):
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
        
        janela_historico = tk.Toplevel(self.janela)
        janela_historico.title("Histórico")
        janela_historico.geometry("400x400")
        
        frame_texto = tk.Frame(janela_historico)
        frame_texto.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(frame_texto)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_widget = tk.Text(frame_texto, yscrollcommand=scrollbar.set,
                             font=("Arial", 10))
        text_widget.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_widget.yview)
        
        text_widget.insert("1.0", texto)
        text_widget.config(state=tk.DISABLED)
    
    def _mostrar_fim_de_jogo(self, vencedor: Jogador):
        """Mostra uma mensagem de fim de jogo."""
        nome_vencedor = "Jogador 1 (Vermelho)" if vencedor == Jogador.JOGADOR1 else "Jogador 2 (Azul)"
        messagebox.showinfo("Fim de Jogo!",
                           f"{nome_vencedor} venceu!\n"
                           f"Clique em 'Novo Jogo' para jogar novamente.")
    
    def iniciar(self):
        """Inicia a interface gráfica."""
        self.janela.mainloop()
