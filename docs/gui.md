# GUI (Interface Gráfica)

Interface em **tkinter** (biblioteca nativa do Python).

## Camadas da GUI

```
GUIJogo (src/gui/__init__.py)
    ├─ Renderizador (desenha)
    ├─ GerenciadorInterface (cliques)
    └─ Canvas (tkinter)
```

---

## Renderizador (renderizador.py)

Desenha o tabuleiro no canvas.

```python
class Renderizador:
    def desenhar_tabuleiro(self, canvas, tabuleiro, peca_selecionada, movimentos_validos):
        """
        Para cada célula (8×8):
        1. Desenha casa (branca ou preta, padrão xadrez)
        2. Se tem peça, desenha círculo + cor
        3. Se é dama, desenha "D" no centro
        4. Se foi selecionada, destaca com borda amarela
        5. Se é movimento válido, desenha ponto verde
        """
        
        for linha in range(8):
            for coluna in range(8):
                # Casa branca ou preta
                cor = COR_CASA_BRANCA if (linha + coluna) % 2 == 0 else COR_CASA_PRETA
                
                x1 = coluna * TAMANHO_CASA
                y1 = linha * TAMANHO_CASA
                x2 = x1 + TAMANHO_CASA
                y2 = y1 + TAMANHO_CASA
                
                canvas.create_rectangle(x1, y1, x2, y2, fill=cor)
                
                # Peça
                peca = tabuleiro.obter_peca(linha, coluna)
                if peca:
                    cor_peca = CorPeca.JOGADOR1.value if peca.jogador == Jogador.JOGADOR1 else CorPeca.JOGADOR2.value
                    
                    canvas.create_oval(
                        x1 + 5, y1 + 5,
                        x2 - 5, y2 - 5,
                        fill=cor_peca
                    )
                    
                    # Dama (letra "D")
                    if peca.tipo == TipoPeca.DAMA:
                        canvas.create_text(
                            (x1 + x2) // 2,
                            (y1 + y2) // 2,
                            text="D",
                            font=("Arial", 14, "bold"),
                            fill="white"
                        )
                
                # Seleção (borda amarela)
                if peca == peca_selecionada:
                    canvas.create_rectangle(x1, y1, x2, y2, outline="YELLOW", width=3)
                
                # Movimentos válidos (ponto verde)
                if (linha, coluna) in movimentos_validos:
                    raio = TAMANHO_CASA // 6
                    cx = (x1 + x2) // 2
                    cy = (y1 + y2) // 2
                    canvas.create_oval(
                        cx - raio, cy - raio,
                        cx + raio, cy + raio,
                        fill="GREEN"
                    )
```

### Constantes Visuais

Veja [src/config.py](../src/config.py) para cores e tamanhos.

---

## GerenciadorInterface (gerenciador_interface.py)

Lida com cliques do mouse e lógica de seleção.

```python
class GerenciadorInterface:
    def __init__(self, jogo: Jogo, canvas: tk.Canvas):
        self.jogo = jogo
        self.canvas = canvas
        self.renderizador = Renderizador()
        
        self.canvas.bind("<Button-1>", self.ao_clicar)
    
    def ao_clicar(self, evento):
        """Usuário clicou no tabuleiro."""
        
        # Converte pixel em linha/coluna
        linha = evento.y // TAMANHO_CASA
        coluna = evento.x // TAMANHO_CASA
        
        # Valida limites
        if not (0 <= linha < 8 and 0 <= coluna < 8):
            return
        
        peca_clicada = self.jogo.tabuleiro.obter_peca(linha, coluna)
        
        # Caso 1: Clicou em uma peça própria
        if peca_clicada and peca_clicada.jogador == self.jogo.jogador_atual:
            self.jogo.peca_selecionada = peca_clicada
            self.jogo.movimentos_validos = self.jogo.obter_movimentos_validos_para_peca(peca_clicada)
            self._renderizar()
        
        # Caso 2: Clicou em um movimento válido
        elif (linha, coluna) in self.jogo.movimentos_validos:
            try:
                self.jogo.mover_peca(linha, coluna)
                self._renderizar()
                
                # Callback para IA (se aplicável)
                if self.callback_pos_atualizacao:
                    self.callback_pos_atualizacao()
            except Exception as e:
                print(f"Movimento inválido: {e}")
    
    def _renderizar(self):
        """Redesenha o tabuleiro."""
        self.canvas.delete("all")
        self.renderizador.desenhar_tabuleiro(
            self.canvas,
            self.jogo.tabuleiro,
            self.jogo.peca_selecionada,
            self.jogo.movimentos_validos
        )
```

---

## GUIJogo (src/gui/__init__.py)

Widget tkinter que encapsula tudo.

```python
class GUIJogo(tk.Frame):
    def __init__(self, parent, modo_ia: bool = False, 
                 callback_menu=None, dificuldade="Normal", 
                 cor_humano=Jogador.JOGADOR1):
        super().__init__(parent)
        
        self.jogo = Jogo()
        self.modo_ia = modo_ia
        self.callback_menu = callback_menu
        self.dificuldade = dificuldade
        self.cor_humano = cor_humano
        
        # Cria widgets
        self._criar_widgets()
        
        # Se IA deve fazer primeiro movimento
        if modo_ia and cor_humano == Jogador.JOGADOR2:
            self._ia_fazer_movimento()
    
    def _criar_widgets(self):
        """Cria canvas, botões e labels."""
        
        # Canvas do tabuleiro
        self.canvas = tk.Canvas(self, width=640, height=640, bg=COR_FUNDO_TABULEIRO)
        self.canvas.pack()
        
        # Gerenciador de interface
        self._gerenciador = GerenciadorInterface(self.jogo, self.canvas)
        self._gerenciador.callback_pos_atualizacao = self._ao_atualizar_posicao
        
        # Botões
        frame_botoes = tk.Frame(self)
        frame_botoes.pack()
        
        if self.modo_ia:
            tk.Button(frame_botoes, text="Desfazer", command=self._desfazer_duplo).pack(side=tk.LEFT)
        
        tk.Button(frame_botoes, text="Empate", command=self._empate).pack(side=tk.LEFT)
        tk.Button(frame_botoes, text="Menu", command=self._voltar_menu).pack(side=tk.LEFT)
    
    def _ao_atualizar_posicao(self):
        """Callback chamado após movimento do humano."""
        
        # Se é turno da IA, faz movimento
        if self.modo_ia and self.jogo.jogador_atual == self._ia.jogador:
            self.after(500)  # Delay para parecer mais humano
            self._ia_fazer_movimento()
    
    def _ia_fazer_movimento(self):
        """IA escolhe e executa movimento."""
        try:
            self._ia.fazer_movimento()
            self._gerenciador._renderizar()
            
            # Callback novamente (em caso de capturas sequenciais)
            self._ao_atualizar_posicao()
        except Exception as e:
            print(f"Erro na IA: {e}")
```

---

## Integração com IA

```python
# Em GUIJogo.__init__

if self.modo_ia:
    self._ia = IA(self.jogo, self.dificuldade, jogador=cor_oponente)
    
    # Instala callback que verifica se é turno da IA
    self._gerenciador.callback_pos_atualizacao = self._ao_atualizar_posicao
```

### Fluxo

1. **Humano clica** → `ao_clicar()` → `jogo.mover_peca()`
2. `_ao_atualizar_posicao()` é chamado
3. Se `jogo.jogador_atual == ia.jogador` → `ia.fazer_movimento()`
4. Renderiza → volta para passo 1

---

**Próximo:** [Main & Aplicação](main.md)
