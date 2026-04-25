# Models (Dados)

Os **models** representam o **estado puro** do jogo — dados sem lógica complexa.

## Enums (enums.py)

Tipos de dados fundamentais:

```python
class TipoPeca(Enum):
    PECA = 1    # Peça comum
    DAMA = 2    # Peça promovida

class Jogador(Enum):
    JOGADOR1 = 1   # Vermelho (começa no topo, linha 0-2)
    JOGADOR2 = 2   # Azul (começa embaixo, linha 5-7)

class CorPeca(Enum):
    JOGADOR1 = "#FF0000"   # Vermelho
    JOGADOR2 = "#0000FF"   # Azul
    DAMA = "#FFD700"       # Dourado (realce)
```

### Por que Enum?
Evitam erros de digitação. Python tipifica e valida automaticamente.

---

## Classe Peca (peca.py)

Representa uma peça individual no tabuleiro.

```python
class Peca:
    def __init__(self, jogador: Jogador, linha: int, coluna: int):
        self.jogador = jogador           # JOGADOR1 ou JOGADOR2
        self.tipo = TipoPeca.PECA        # Começa como PECA
        self.linha = linha               # 0-7 (topo → embaixo)
        self.coluna = coluna             # 0-7 (esquerda → direita)
    
    def promover(self):
        """Transforma em dama."""
        self.tipo = TipoPeca.DAMA
    
    def despromover(self):
        """Desfaz promoção (usada em undo)."""
        self.tipo = TipoPeca.PECA
```

### Comportamento

#### Peça Comum (PECA)
- Move **1 casa** na diagonal **para frente** (direção do oponente)
- Se JOGADOR1: só para baixo (linha aumenta)
- Se JOGADOR2: só para cima (linha diminui)

#### Dama (DAMA)
- Move **qualquer número de casas** na diagonal
- Pode mover em **qualquer direção** (frente e trás)

### Exemplo de Visualização

```
    0   1   2   3   4   5   6   7
0   ·   🔴  ·   🔴  ·   🔴  ·   🔴   ← JOGADOR1 (vermelho)
1   🔴  ·   🔴  ·   🔴  ·   🔴  ·
2   ·   🔴  ·   🔴  ·   🔴  ·   🔴
3   ·   ·   ·   ·   ·   ·   ·   ·    ← Vazio
4   ·   ·   ·   ·   ·   ·   ·   ·
5   🔵  ·   🔵  ·   🔵  ·   🔵  ·    ← JOGADOR2 (azul)
6   ·   🔵  ·   🔵  ·   🔵  ·   🔵
7   🔵  ·   🔵  ·   🔵  ·   🔵  ·
```

---

## Classe Tabuleiro (tabuleiro.py)

Representa o estado do tabuleiro 8×8.

```python
class Tabuleiro:
    def __init__(self):
        self._casas = [[None]*8 for _ in range(8)]  # 8×8 grid
        self._inicializar()  # Coloca peças no início
    
    def obter_peca(self, linha: int, coluna: int) -> Peca:
        """Retorna a peça na posição ou None."""
        return self._casas[linha][coluna]
    
    def mover_peca(self, peca: Peca, nova_linha: int, nova_coluna: int):
        """Move uma peça para nova posição."""
        self._casas[peca.linha][peca.coluna] = None  # Remove de antiga
        self._casas[nova_linha][nova_coluna] = peca   # Coloca em nova
        peca.linha = nova_linha
        peca.coluna = nova_coluna
    
    def _inicializar(self):
        """Coloca peças nas posições iniciais."""
        # JOGADOR1 nas linhas 0, 1, 2
        # JOGADOR2 nas linhas 5, 6, 7
        # Só em casas escuras (linha + coluna é par)
```

### Acesso ao Tabuleiro

```python
tabuleiro = Tabuleiro()

# Obter peça
peca = tabuleiro.obter_peca(0, 1)

# Mover peça
tabuleiro.mover_peca(peca, 3, 2)

# Verificar se casa está vazia
if tabuleiro.obter_peca(3, 3) is None:
    print("Vazia")
```

### Layout Interno

```python
self._casas[linha][coluna] = Peca ou None
```

---

**Próximo:** [Services (Regras)](services.md)
