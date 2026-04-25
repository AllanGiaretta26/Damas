# IA (Inteligência Artificial)

Motor de IA com quatro estratégias que implementam o **Strategy Pattern**.

## Classe IA (src/ia/\_\_init\_\_.py)

```python
class IA:
    """Facade sobre EstrategiaIA. Usa Strategy Pattern para trocar nível em runtime."""

    _estrategias = {
        "facil":   EstrategiaFacil,
        "normal":  EstrategiaNormal,
        "medio":   EstrategiaMedia,    # Minimax depth 3
        "dificil": EstrategiaDificil,  # Minimax depth 5
    }

    def __init__(self, jogo: Jogo, dificuldade: str = "normal",
                 jogador: Jogador = Jogador.JOGADOR2):
        self.jogo = jogo
        self.jogador = jogador
        self._estrategia = self._criar_estrategia(dificuldade)
```

### Uso

```python
from src.game import Jogo
from src.ia import IA
from src.models import Jogador

jogo = Jogo()
jogo.modo_ia = True

ia = IA(jogo, dificuldade="dificil", jogador=Jogador.JOGADOR2)
ia.fazer_movimento()
```

> **Chaves de dificuldade** são minúsculas e sem acento: `"facil"`, `"normal"`, `"medio"`, `"dificil"`.

---

## EstrategiaFacil

**Aleatória** — escolhe qualquer movimento disponível.

```python
class EstrategiaFacil(EstrategiaIA):
    def escolher_movimento(self, jogo: Jogo, movimentos: List[Movimento]) -> Optional[Movimento]:
        return random.choice(movimentos) if movimentos else None
```

### Características

- Rápida — sem cálculo
- Imprevisível — boa para testes
- Nível iniciante

---

## EstrategiaNormal

**Heurística com prioridades** — sem busca, avalia o estado imediato.

```python
class EstrategiaNormal(EstrategiaIA):
    def escolher_movimento(self, jogo: Jogo, movimentos: List[Movimento]) -> Optional[Movimento]:
        """
        Prioridades (em ordem):
        1. Capturar peças inimigas (escolhe a que abre mais sequências)
        2. Promover peça a dama
        3. Mover para casa segura (não fica exposta a captura)
        4. Qualquer movimento
        """
```

### Características

- Sem minimax — heurística pura
- Rápida (~ms)
- Nível intermediário

---

## EstrategiaMedia

**Minimax profundidade 3** — subclasse de `EstrategiaMinimax`.

```python
class EstrategiaMedia(EstrategiaMinimax):
    def __init__(self):
        super().__init__(profundidade=3)
```

### Características

- Boa relação custo/benefício (~500ms)
- Nível normal-difícil

---

## EstrategiaDificil

**Minimax profundidade 5** — subclasse de `EstrategiaMinimax`.

```python
class EstrategiaDificil(EstrategiaMinimax):
    def __init__(self):
        super().__init__(profundidade=5)
```

### Características

- Mais forte, mas mais lenta (~5-10s)
- Nível difícil

---

## EstrategiaMinimax (com Alfa-Beta)

Base de `EstrategiaMedia` e `EstrategiaDificil`.

```python
class EstrategiaMinimax(EstrategiaIA):
    VALOR_PECA = 1
    VALOR_DAMA = 3
    VALOR_VITORIA = 10_000
    BONUS_CENTRO = 0.05
    BONUS_GUARDA_FINAL = 0.3

    def __init__(self, profundidade: int):
        self.profundidade = profundidade

    def escolher_movimento(self, jogo: Jogo, movimentos: List[Movimento]) -> Optional[Movimento]:
        """
        1. Ordena capturas primeiro (melhora poda alfa-beta)
        2. Para cada movimento: executa, minimax, desfaz
        3. Retorna o de maior score
        """
        jogador_max = jogo.jogador_atual
        melhor_mov = movimentos[0]
        melhor_score = -float('inf')
        alfa, beta = -float('inf'), float('inf')

        for mov in self._ordenar_movimentos(movimentos):
            (lo, co), (ld, cd) = mov
            if not jogo.mover_peca(lo, co, ld, cd):
                continue
            score = self._minimax(jogo, self.profundidade - 1, alfa, beta, jogador_max)
            jogo.desfazer_jogada()
            if score > melhor_score:
                melhor_score = score
                melhor_mov = mov
        return melhor_mov
```

### Avaliação de posição

```python
def _avaliar(self, jogo: Jogo, jogador_max: Jogador) -> float:
    """Material + bônus posicional."""
    # peça = 1, dama = 3
    # bônus de centro e guarda de última fileira
    # vitória = ±10_000 (avaliada em _minimax antes de chegar aqui)
```

### Profundidades

| Profundidade | Tempo típico | Usado em |
|---|---|---|
| 3 | ~500ms | EstrategiaMedia |
| 5 | ~5-10s | EstrategiaDificil |

---

## Hierarquia de Classes

```
EstrategiaIA (ABC)
├── EstrategiaFacil
├── EstrategiaNormal
└── EstrategiaMinimax(profundidade)
    ├── EstrategiaMedia   (depth=3)
    └── EstrategiaDificil (depth=5)
```

---

## Como a IA executa um movimento

```python
def fazer_movimento(self) -> bool:
    movimentos = self._encontrar_todos_movimentos()
    if not movimentos:
        return False

    melhor = self._estrategia.escolher_movimento(self.jogo, movimentos)
    if melhor is None:
        melhor = random.choice(movimentos)

    (lo, co), (ld, cd) = melhor

    if not self.jogo.em_sequencia_captura:
        self.jogo.selecionar_peca(lo, co)

    return self.jogo.mover_peca(lo, co, ld, cd)
```

---

**Próximo:** [GUI (Interface)](gui.md)
