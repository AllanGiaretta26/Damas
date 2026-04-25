# Main & Aplicação (main.py)

Gerencia o **ciclo de vida** da aplicação: Menu → Opções IA → Jogo.

## Arquitetura da Janela

```python
class AplicacaoDamas:
    """
    Gerencia ÚNICA janela (tk.Tk) durante toda a sessão.
    Nunca destruir a janela — apenas limpar e reconstruir conteúdo.
    """
    
    def __init__(self):
        self.janela = tk.Tk()  # Criada uma vez e reutilizada
        self.janela.title("Jogo de Damas")
        self._placar = {}  # Contador de vitórias
```

### Por que única janela?

✅ Mais eficiente  
✅ Mantém estado (posição, redimensionamento)  
✅ Evita flickering  
❌ Não criar `tk.Tk()` novo em cada tela

---

## Fluxo Principal

```
Executar
    ↓
_mostrar_menu_principal() ← Menu inicial
    ↓
Opção 1: Humano vs Humano → _iniciar_jogo(modo_ia=False)
    ↓
Jogo funciona normalmente
    ↓
Fim → Pergunta jogar novamente ou voltar menu
    ↓
_retornar_ao_menu() → volta para menu


Opção 2: Humano vs IA → _mostrar_opcoes_ia()
    ↓
Escolhe dificuldade + cor
    ↓
_iniciar_jogo(modo_ia=True, dificuldade=..., cor_humano=...)
    ↓
Jogo com IA
    ↓
```

---

## Métodos Principais

### executar()

```python
def executar(self):
    """Inicia o loop principal."""
    self._mostrar_menu_principal()
    self.janela.mainloop()  # Roda até fechar a janela
```

---

### _mostrar_menu_principal()

```python
def _mostrar_menu_principal(self):
    """Exibe tela inicial."""
    self._limpar_janela()
    self.janela.geometry("420x440")
    
    frame = tk.Frame(self.janela, bg=COR_FUNDO)
    frame.pack(fill=tk.BOTH, expand=True)
    
    tk.Label(
        frame,
        text="Bem-vindo ao Jogo de Damas",
        font=("Arial", 20, "bold"),
        bg=COR_FUNDO,
        fg=COR_TEXTO_PRINCIPAL
    ).pack(pady=20)
    
    tk.Button(
        frame,
        text="Humano vs Humano",
        command=self._iniciar_jogo_hvh,
        bg=COR_BOTAO,
        fg="white",
        font=("Arial", 12)
    ).pack(pady=10)
    
    tk.Button(
        frame,
        text="Humano vs IA",
        command=self._mostrar_opcoes_ia,
        bg=COR_BOTAO,
        fg="white",
        font=("Arial", 12)
    ).pack(pady=10)
    
    # Placar
    placar_text = self._formatar_placar()
    tk.Label(frame, text=placar_text, bg=COR_FUNDO, fg=COR_TEXTO_SECUNDARIO).pack(pady=10)
    
    tk.Button(frame, text="Sair", command=self.janela.quit).pack(pady=10)
```

---

### _mostrar_opcoes_ia()

```python
def _mostrar_opcoes_ia(self):
    """Tela para escolher dificuldade e cor."""
    self._limpar_janela()
    self.janela.geometry("420x440")
    
    frame = tk.Frame(self.janela, bg=COR_FUNDO)
    frame.pack(fill=tk.BOTH, expand=True)
    
    tk.Label(frame, text="Escolha dificuldade", font=("Arial", 14, "bold")).pack(pady=10)
    
    dificuldade_combo = ttk.Combobox(
        frame,
        values=["Fácil", "Normal", "Difícil"],
        state="readonly"
    )
    dificuldade_combo.set("Normal")
    dificuldade_combo.pack(pady=10)
    
    tk.Label(frame, text="Escolha sua cor", font=("Arial", 14, "bold")).pack(pady=10)
    
    cor = tk.StringVar(value="JOGADOR1")
    
    tk.Radiobutton(
        frame,
        text="Vermelho (você começa)",
        variable=cor,
        value="JOGADOR1"
    ).pack()
    
    tk.Radiobutton(
        frame,
        text="Azul (IA começa)",
        variable=cor,
        value="JOGADOR2"
    ).pack()
    
    def iniciar():
        self._iniciar_jogo(
            modo_ia=True,
            dificuldade=dificuldade_combo.get(),
            cor_humano=Jogador[cor.get()]
        )
    
    tk.Button(frame, text="Começar", command=iniciar).pack(pady=20)
    tk.Button(frame, text="Voltar", command=self._mostrar_menu_principal).pack()
```

---

### _iniciar_jogo()

```python
def _iniciar_jogo(self, modo_ia=False, dificuldade="Normal", cor_humano=Jogador.JOGADOR1):
    """Cria e inicia o jogo."""
    self._limpar_janela()
    self.janela.geometry("700x820")
    
    # Cria GUI do jogo
    gui = GUIJogo(
        self.janela,
        modo_ia=modo_ia,
        callback_menu=self._retornar_ao_menu,
        dificuldade=dificuldade,
        cor_humano=cor_humano
    )
    gui.pack(fill=tk.BOTH, expand=True)
    
    self._gui_ativa = gui
```

---

### _retornar_ao_menu()

```python
def _retornar_ao_menu(self):
    """Callback chamado pelo botão 'Menu' na GUI."""
    self._limpar_janela()
    self._mostrar_menu_principal()
```

---

### _limpar_janela()

```python
def _limpar_janela(self):
    """Remove todos os widgets da janela."""
    for widget in self.janela.winfo_children():
        widget.destroy()
```

---

### _centralizar_janela()

```python
def _centralizar_janela(self, largura: int, altura: int):
    """Posiciona a janela no centro da tela."""
    x = (self.janela.winfo_screenwidth() - largura) // 2
    y = (self.janela.winfo_screenheight() - altura) // 2
    self.janela.geometry(f"{largura}x{altura}+{x}+{y}")
```

---

## Placar (Session Scoreboard)

```python
def _formatar_placar(self) -> str:
    """Formata placar para exibição."""
    # Modo HvH: usa chaves "JOGADOR1", "JOGADOR2"
    # Modo IA: usa chaves "humano", "ia"
    
    j1 = self._placar.get("JOGADOR1", 0)
    j2 = self._placar.get("JOGADOR2", 0)
    humano = self._placar.get("humano", 0)
    ia = self._placar.get("ia", 0)
    
    if ia > 0 or humano > 0:
        return f"Placar: Humano {humano} x IA {ia}"
    else:
        return f"Placar: J1 {j1} x J2 {j2}"

def _registrar_vitoria(self, vencedor: str):
    """Registra vitória no placar."""
    self._placar[vencedor] = self._placar.get(vencedor, 0) + 1
```

---

## Entrada Principal

```python
if __name__ == "__main__":
    app = AplicacaoDamas()
    app.executar()
```

---

**Próximo:** [Exemplos de Uso](uso-exemplo.md)
