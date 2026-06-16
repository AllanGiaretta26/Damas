# Game

`src/game.py` contém `Jogo`, o orquestrador do domínio. Esta é a API preferencial para GUI, IA, testes e uso programático.

## Estado mantido por Jogo

- `tabuleiro`: instância de `Tabuleiro`.
- `jogador_atual`: jogador cujo turno está ativo.
- `peca_selecionada`: peça selecionada ou `None`.
- `movimentos_validos`: destinos válidos da peça selecionada.
- `historico_jogadas`: lista de deltas reversíveis.
- `pecas_capturadas_j1` e `pecas_capturadas_j2`: contadores por jogador que capturou.
- `em_sequencia_captura`: indica captura múltipla em andamento.
- `modo_ia`: flag usada pela GUI para comportamento de undo.

## API pública

| Método/propriedade | Contrato |
|---|---|
| `selecionar_peca(linha, coluna)` | Seleciona uma peça do jogador atual e calcula movimentos. Retorna `True` em sucesso. |
| `mover_peca(linha_origem, coluna_origem, linha_destino, coluna_destino)` | Executa movimento legal. Retorna `True` em sucesso. |
| `desfazer_jogada()` | Reverte o último delta. Retorna `False` se não houver histórico. |
| `verificar_fim_de_jogo()` | Retorna `(fim: bool, vencedor: Optional[Jogador])`. |
| `resetar()` | Volta a partida ao estado inicial. |
| `obter_movimentos_validos_para_peca(linha, coluna)` | Retorna destinos válidos para a peça. |
| `jogador_tem_capturas(jogador)` | Retorna se o jogador possui captura obrigatória. |
| `encontrar_capturas_para_peca(linha, coluna)` | Retorna capturas da peça na posição. |
| `tentar_promover_peca(peca)` | Encaminha a promoção ao `PromotionHandler`. |

## Fluxo de `mover_peca()`

1. Obtém a peça da origem.
2. Rejeita origem vazia ou peça de outro jogador.
3. Calcula movimentos válidos com `MovimentoValidator`.
4. Rejeita destino fora dos movimentos válidos.
5. Salva estado anterior para undo.
6. Executa captura via `CaptureHandler` ou movimento simples via `Tabuleiro`.
7. Tenta promover a peça.
8. Registra delta em `historico_jogadas`.
9. Se houver captura sequencial, mantém turno e peça selecionada.
10. Caso contrário, limpa seleção e alterna jogador.

## Delta de histórico

Cada jogada registra:

- `de`: origem.
- `para`: destino.
- `peca_capturada`: peça removida ou `None`.
- `pos_capturada`: posição da peça capturada ou `None`.
- `promoveu`: se a jogada promoveu a peça.
- `em_sequencia_antes`: estado de sequência antes da jogada.
- `jogador_antes`: turno antes da jogada.
- `peca_selecionada_antes`: seleção anterior.

Qualquer nova mutação de estado em `Jogo` precisa entrar nesse delta ou o undo fica mentiroso.

## Fim de jogo

`verificar_fim_de_jogo()` encerra quando:

- um jogador não tem peças; ou
- o jogador atual não tem movimentos disponíveis.

O vencedor é o outro jogador nesses casos.

## Próximo documento

[IA](ia.md)
