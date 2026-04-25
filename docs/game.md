# Game (Orquestrador)

A classe **Jogo** em `src/game.py` é o **maestro** — coordena tudo.

## Responsabilidades de Jogo

```python
class Jogo:
    def __init__(self):
        self.tabuleiro = Tabuleiro()
        self.jogador_atual = Jogador.JOGADOR1
        self._peca_selecionada = None
        self._movimentos_validos = []
        self.historico_jogadas = []  # Para undo
        self.modo_ia = False
        
        # Services
        self._movimento_validator = MovimentoValidator(self.tabuleiro)
        self._capture_handler = CaptureHandler(self.tabuleiro)
        self._promotion_handler = PromotionHandler()
```

---

## Fluxo Principal: mover_peca()

```python
def mover_peca(self, linha_origem: int, coluna_origem: int,
               linha_destino: int, coluna_destino: int) -> bool:
    """
    Fluxo principal do jogo:
    1. Valida movimento via MovimentoValidator
    2. Se captura (diff_linha == 2): executa com CaptureHandler
    3. Verifica promoção com PromotionHandler
    4. Registra delta reversível em historico_jogadas
    5. Se há capturas sequenciais: mantém peça selecionada (não muda turno)
    6. Caso contrário: encerra turno (alterna jogador)
    
    Returns:
        True se o movimento foi bem-sucedido.
    """

    # Snapshot salvo no delta reversível
    delta = {
        'jogador':               jogador_antes,
        'de':                    (linha_origem, coluna_origem),
        'para':                  (linha_destino, coluna_destino),
        'peca_capturada':        peca_capturada,    # Peca ou None
        'pos_capturada':         pos_capturada,     # (linha, col) ou None
        'promoveu':              promoveu,          # bool
        'em_sequencia_antes':    em_sequencia_antes,
        'jogador_antes':         jogador_antes,
        'peca_selecionada_antes': peca_selecionada_antes,
    }
```

---

## Sistema de Undo

```python
def desfazer_jogada(self) -> bool:
    """
    Desfaz o último movimento.
    Reverte: posição, captura, promoção, turno, seleção.
    Retorna False se o histórico estiver vazio.
    """
    delta = self.historico_jogadas.pop()
    linha_origem, coluna_origem = delta['de']
    linha_destino, coluna_destino = delta['para']

    peca = self.tabuleiro.obter_peca(linha_destino, coluna_destino)

    # Desfaz promoção (antes de mover de volta)
    if delta.get('promoveu'):
        peca.despromover()

    # Volta peça para posição original
    self.tabuleiro.mover_peca(linha_destino, coluna_destino,
                              linha_origem, coluna_origem)

    # Recoloca peça capturada
    if delta.get('peca_capturada') is not None:
        linha_cap, coluna_cap = delta['pos_capturada']
        self.tabuleiro.colocar_peca(delta['peca_capturada'], linha_cap, coluna_cap)
        # Decrementa contadores de captura

    # Restaura turno e seleção
    self.jogador_atual      = delta.get('jogador_antes', self.jogador_atual)
    self._peca_selecionada  = delta.get('peca_selecionada_antes')
    self._em_sequencia_captura = delta.get('em_sequencia_antes', False)
    self._movimentos_validos   = []
```

### Princípio de Undo

**Todo movimento que muda o estado deve ser reversível.**

Se você adiciona uma nova mutação em `Jogo`, deve:
1. Salvar estado anterior no `delta`
2. Implementar a reversão em `desfazer_jogada()`

---

## Métodos Públicos

```python
# Aceita coordenadas, não objeto Peca
def obter_movimentos_validos_para_peca(self, linha: int, coluna: int) -> List[Tuple]:
    """Retorna movimentos válidos (respeitando captura obrigatória)."""

def jogador_tem_capturas(self, jogador: Jogador) -> bool:
    """Verifica se o jogador pode capturar."""

def encontrar_capturas_para_peca(self, linha: int, coluna: int) -> List[Tuple]:
    """Encontra apenas capturas possíveis para uma peça."""

def tentar_promover_peca(self, peca: Peca) -> bool:
    """Tenta promover, retorna True se promoveu."""

def verificar_fim_de_jogo(self) -> Tuple[bool, Optional[Jogador]]:
    """Retorna (True, vencedor) se acabou, ou (False, None)."""

def selecionar_peca(self, linha: int, coluna: int) -> bool:
    """Seleciona a peça na posição. Retorna True em sucesso."""

def resetar(self) -> None:
    """Reseta o jogo ao estado inicial."""
```

### ⚠️ Importante

**Não acesse services diretamente!** Use os métodos de `Jogo`.

```python
# ❌ ERRADO
resultado = jogo._movimento_validator.calcular_movimentos_validos(linha, coluna, ...)

# ✅ CORRETO
resultado = jogo.obter_movimentos_validos_para_peca(linha, coluna)
```

**`verificar_fim_de_jogo()` retorna uma tupla:**

```python
# ❌ ERRADO
if jogo.verifica_fim_de_jogo():
    ...

# ✅ CORRETO
fim, vencedor = jogo.verificar_fim_de_jogo()
if fim:
    print(vencedor)
```

---

**Próximo:** [IA (Inteligência Artificial)](ia.md)
