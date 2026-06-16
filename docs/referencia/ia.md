# IA

A IA fica em `src/ia/` e usa o padrão Strategy. A classe `IA` é uma fachada que escolhe a estratégia e executa movimentos por meio de `Jogo`.

## Classe IA

Arquivo: [`src/ia/__init__.py`](../../src/ia/__init__.py)

Construtor:

```python
IA(jogo, dificuldade="normal", jogador=Jogador.JOGADOR2)
```

Chaves aceitas:

| Chave | Estratégia |
|---|---|
| `facil` | `EstrategiaFacil` |
| `normal` | `EstrategiaNormal` |
| `medio` | `EstrategiaMedia` |
| `dificil` | `EstrategiaDificil` |

Se a chave não existir, a implementação cai em `EstrategiaNormal`.

A interface gráfica oferece apenas `facil`, `medio` e `dificil`.

## Estratégias

### EstrategiaFacil

Escolhe aleatoriamente um movimento disponível.

### EstrategiaNormal

Heurística sem busca profunda. Prioridade:

1. Capturas.
2. Promoções.
3. Movimentos considerados seguros.
4. Qualquer movimento.

### EstrategiaMinimax

Base de `EstrategiaMedia` e `EstrategiaDificil`.

Características:

- Usa minimax com poda alfa-beta.
- Avalia material: peça comum = 1, dama = 3.
- Usa vitória/derrota como `10_000`.
- Aplica bônus posicional de centro e guarda final.
- Ordena capturas antes de movimentos simples para melhorar a poda.
- Simula movimentos chamando `jogo.mover_peca()` e desfaz com `jogo.desfazer_jogada()`.

Subclasses:

| Estratégia | Profundidade |
|---|---|
| `EstrategiaMedia` | 3 |
| `EstrategiaDificil` | 5 |

## Execução de movimento

`IA.fazer_movimento()`:

1. Gera todos os movimentos legais do jogador controlado pela IA.
2. Pede à estratégia que escolha um movimento.
3. Seleciona a peça se não houver captura sequencial em andamento.
4. Chama `Jogo.mover_peca()`.
5. Retorna `True` em sucesso.

## Integração com turno

A IA tem um atributo `jogador`. O código que agenda a IA deve comparar:

```python
if jogo.jogador_atual == ia.jogador:
    ia.fazer_movimento()
```

Não use `Jogador.JOGADOR2` fixo. No modo IA, o humano pode escolher azul; nesse caso a IA joga como vermelho.

## Próximo documento

[GUI](gui.md)
