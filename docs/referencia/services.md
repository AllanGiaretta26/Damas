# Services

Services implementam regras de jogo sobre `Tabuleiro` e `Peca`. Eles não exibem interface e não controlam placar.

## MovimentoValidator

Arquivo: [`src/services/movimento_validator.py`](../../src/services/movimento_validator.py)

Responsabilidades:

- Calcular movimentos válidos para uma peça.
- Aplicar captura obrigatória.
- Restringir a peça correta durante captura sequencial.
- Detectar se um jogador tem movimentos disponíveis.

Métodos principais:

| Método | Contrato |
|---|---|
| `calcular_movimentos_validos(linha, coluna, jogador_atual, em_sequencia_captura=False, peca_selecionada=None)` | Retorna destinos válidos como lista de `(linha, coluna)`. |
| `encontrar_capturas(linha, coluna)` | Retorna apenas destinos de captura para a peça. |
| `jogador_tem_capturas(jogador)` | Retorna `True` se qualquer peça do jogador puder capturar. |
| `tem_movimentos_disponiveis(jogador)` | Retorna `True` se o jogador tiver pelo menos um movimento legal. |

Regras implementadas:

- Peça comum do `JOGADOR1` move/captura para cima: `linha - 1` ou `linha - 2`.
- Peça comum do `JOGADOR2` move/captura para baixo: `linha + 1` ou `linha + 2`.
- Dama move uma casa diagonal em qualquer direção.
- Dama captura pulando duas casas diagonais em qualquer direção.
- Se o jogador tiver qualquer captura, movimentos simples são bloqueados.

## CaptureHandler

Arquivo: [`src/services/capture_handler.py`](../../src/services/capture_handler.py)

Responsabilidades:

- Remover a peça capturada.
- Mover a peça atacante para o destino.
- Consultar capturas sequenciais a partir da nova posição.

Métodos:

| Método | Contrato |
|---|---|
| `executar_captura(linha_origem, coluna_origem, linha_destino, coluna_destino)` | Remove a peça no meio do caminho, move a atacante e retorna a peça capturada. |
| `tem_capturas_sequenciais(linha, coluna)` | Retorna `True` se a peça na posição puder capturar de novo. |
| `obter_capturas_sequenciais(linha, coluna)` | Retorna destinos disponíveis para continuar a sequência. |

`CaptureHandler` não atualiza contadores de captura; isso fica em `Jogo._registrar_captura()` para manter o delta de undo centralizado.

## PromotionHandler

Arquivo: [`src/services/promotion_handler.py`](../../src/services/promotion_handler.py)

Método principal:

| Método | Contrato |
|---|---|
| `tentar_promover(peca)` | Promove automaticamente e retorna `True` se a peça comum alcançou a última linha. |

Linhas de promoção:

- `JOGADOR1`: linha 0.
- `JOGADOR2`: linha 7.

Damas já promovidas não são promovidas de novo.

## Próximo documento

[Game](game.md)
