# Arquitetura

## Estrutura de Camadas

O projeto segue uma **arquitetura em camadas** que separa responsabilidades de forma clara:

```
src/
├── models/              ← Estado puro (dados)
│   ├── enums.py         Tipos: TipoPeca, Jogador, CorPeca
│   ├── peca.py          Classe Peca (posição, tipo, promoção)
│   └── tabuleiro.py     Classe Tabuleiro (8×8, peças)
│
├── services/            ← Regras de negócio (lógica do jogo)
│   ├── movimento_validator.py    Valida movimentos legais
│   ├── capture_handler.py        Executa capturas
│   └── promotion_handler.py      Promove peças a dama
│
├── ia/                  ← Motor de inteligência artificial
│   ├── estrategias.py   EstrategiaFacil, EstrategiaNormal, EstrategiaMinimax,
│   │                    EstrategiaMedia (depth 3), EstrategiaDificil (depth 5)
│   └── __init__.py      Classe IA (Strategy Pattern, 4 dificuldades)
│
├── gui/                 ← Interface gráfica (tkinter)
│   ├── renderizador.py          Desenha o tabuleiro
│   ├── gerenciador_interface.py Lida com cliques
│   └── __init__.py              Classe GUIJogo
│
├── game.py              ← Orquestrador principal
│   └── Classe Jogo (maestro central)
│
└── config.py            ← Configurações visuais (cores, tamanhos)
```

## Padrão de Dependências

**Sempre para baixo** — não há imports circulares:

```
GUI (interface)
    ↓
Jogo (orquestrador)
    ↓
Services (regras)
    ↓
Models (dados puros)

IA (inteligência) → Jogo (usa desfazer_jogada para explorar)
```

### Por que dessa forma?

- **Models** (base) — não dependem de nada, apenas dados puros
- **Services** — usam models para aplicar regras
- **Jogo** — orquestra services e models
- **GUI** — consome Jogo, não acessa models ou services diretamente
- **IA** — depende de Jogo (pode explorar com `desfazer_jogada()`)

## Conceitos-Chave

### 1. Estado Imutável (Models)
Models como `Peca` e `Tabuleiro` representam o estado. Não contêm lógica complexa — só dados com getters/setters.

### 2. Separação de Responsabilidades (Services)
Cada serviço faz uma coisa bem:
- `MovimentoValidator` — apenas valida
- `CaptureHandler` — apenas executa captura
- `PromotionHandler` — apenas promove

### 3. Orquestração (Game.py)
A classe `Jogo` coordena tudo. É o único lugar que:
- Chama múltiplos services
- Gerencia histórico
- Controla fluxo de turno

### 4. Strategy Pattern (IA)
`IA` em `src/ia/__init__.py` seleciona a estratégia por chave (minúscula, sem acento):
```python
ia = IA(jogo, "dificil", Jogador.JOGADOR2)  # Usa EstrategiaDificil (minimax depth 5)
ia = IA(jogo, "normal",  Jogador.JOGADOR2)  # Usa EstrategiaNormal (heurística)
```
Dificuldades disponíveis: `"facil"`, `"normal"`, `"medio"`, `"dificil"`.

---

**Próximo:** [Models (Dados)](models.md)
