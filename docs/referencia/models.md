# Models

Os models mantêm estado. Eles não calculam regra de movimento nem conhecem a interface.

## Enums

Arquivo: [`src/models/enums.py`](../../src/models/enums.py)

| Enum | Valores | Uso |
|---|---|---|
| `TipoPeca` | `PECA`, `DAMA` | Tipo da peça. |
| `Jogador` | `JOGADOR1`, `JOGADOR2` | Dono da peça e turno atual. |
| `CorPeca` | `JOGADOR1`, `JOGADOR2`, `DAMA` | Cores usadas pela interface. |

## Peca

Arquivo: [`src/models/peca.py`](../../src/models/peca.py)

Estado mantido:

- `jogador`: `Jogador.JOGADOR1` ou `Jogador.JOGADOR2`.
- `tipo`: `TipoPeca.PECA` por padrão; pode virar `TipoPeca.DAMA`.
- `linha` e `coluna`: coordenadas internas de 0 a 7.

Métodos públicos relevantes:

| Método | Contrato |
|---|---|
| `promover()` | Define `tipo` como `TipoPeca.DAMA`. |
| `despromover()` | Volta `tipo` para `TipoPeca.PECA`; usado pelo undo. |
| `atualizar_posicao(linha, coluna)` | Atualiza coordenadas da peça. |
| `eh_dama()` | Retorna `True` quando a peça é dama. |
| `pertence_ao_jogador(jogador)` | Verifica dono da peça. |

## Tabuleiro

Arquivo: [`src/models/tabuleiro.py`](../../src/models/tabuleiro.py)

`Tabuleiro` mantém uma matriz 8x8 em `_casas`.

Posição inicial:

- `JOGADOR2` nas linhas 0, 1 e 2.
- `JOGADOR1` nas linhas 5, 6 e 7.
- Peças só são colocadas em casas pretas, onde `(linha + coluna) % 2 == 1`.

Métodos públicos:

| Método | Contrato |
|---|---|
| `obter_peca(linha, coluna)` | Retorna `Peca` ou `None`; retorna `None` para posição inválida. |
| `colocar_peca(peca, linha, coluna)` | Coloca a peça e sincroniza suas coordenadas. |
| `mover_peca(linha_origem, coluna_origem, linha_destino, coluna_destino)` | Move se origem/destino forem válidos e destino estiver vazio; retorna a peça movida ou `None`. |
| `remover_peca(linha, coluna)` | Remove e retorna a peça, ou `None`. |
| `eh_casa_preta_publico(linha, coluna)` | Expõe a validação de casa preta. |
| `resetar()` | Recria a posição inicial. |
| `obter_todas_pecas(jogador)` | Lista peças de um jogador. |
| `contar_pecas(jogador)` | Conta peças restantes de um jogador. |
| `obter_matriz_casas()` | Retorna a matriz interna para renderização. |

## Uso correto

Código de aplicação deve preferir `Jogo` para mutações de partida. Mover peça diretamente no `Tabuleiro` não registra histórico e quebra undo.

## Próximo documento

[Services](services.md)
