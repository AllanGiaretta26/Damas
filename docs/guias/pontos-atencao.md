# Pontos de atenção

Esta lista registra armadilhas reais do projeto. Parte da documentação anterior errava regras básicas; não repita isso.

## Erros comuns

### Inverter direção dos jogadores

Errado:

```python
# JOGADOR1 não começa na linha 2 e não move para baixo.
jogo.selecionar_peca(2, 1)
```

Correto:

```python
# JOGADOR1 começa embaixo e move para cima.
jogo.selecionar_peca(5, 0)
jogo.mover_peca(5, 0, 4, 1)
```

### Documentar dama voadora

Este código não implementa dama que anda várias casas. A dama apenas remove a restrição de direção:

- movimento simples: uma casa diagonal;
- captura: salto de duas casas diagonais.

### Usar assinatura antiga de `mover_peca`

Errado:

```python
jogo.mover_peca(4, 1)
```

Correto:

```python
jogo.mover_peca(5, 0, 4, 1)
```

### Mover direto no Tabuleiro durante uma partida

Errado para fluxo normal:

```python
jogo.tabuleiro.mover_peca(5, 0, 4, 1)
```

Isso não registra histórico nem contadores. Use `Jogo.mover_peca()`.

Exceção aceitável: montagem de cenários em testes, geralmente limpando `_casas` e usando `colocar_peca()`.

### Acessar services fora de Jogo

Errado:

```python
jogo._movimento_validator.calcular_movimentos_validos(...)
```

Correto:

```python
jogo.obter_movimentos_validos_para_peca(linha, coluna)
jogo.jogador_tem_capturas(jogador)
jogo.encontrar_capturas_para_peca(linha, coluna)
```

### Assumir que a IA é sempre azul

No modo IA, a IA controla a cor oposta à escolhida pelo humano. Compare sempre com `ia.jogador`.

## Invariantes que quebram testes

| Invariante | Onde aparece |
|---|---|
| Tabuleiro 8x8 | `Tabuleiro.TAMANHO`, testes de movimento e fim de jogo. |
| `JOGADOR1` promove na linha 0 | `PromotionHandler`, testes de promoção e undo. |
| `JOGADOR2` promove na linha 7 | `PromotionHandler`, testes de dama do jogador 2. |
| Captura obrigatória | `MovimentoValidator`, testes de captura obrigatória. |
| Captura sequencial mantém turno | `Jogo.mover_peca`, testes de sequência. |
| Undo reverte captura, promoção, turno e seleção | `Jogo.desfazer_jogada`, vários testes de undo. |
| IA minimax usa `desfazer_jogada()` | `EstrategiaMinimax`, teste de escolha de captura. |

## Checklist para mudanças

Antes de alterar regra de jogo:

- [ ] A mudança passa por `Jogo`, não só por `Tabuleiro`.
- [ ] Toda mutação nova entra no delta de `historico_jogadas`.
- [ ] `desfazer_jogada()` reverte a mutação.
- [ ] IA continua usando API pública de `Jogo`.
- [ ] GUI não passa a conter regra de domínio.
- [ ] `python tests/teste_jogo.py` passa.
- [ ] Documentos afetados foram atualizados.

## Performance

`EstrategiaDificil` usa minimax profundidade 5. Em posições com muitos movimentos, a execução pode ficar perceptível na interface. O agendamento por `after(500, ...)` melhora a experiência, mas não transforma cálculo pesado em assíncrono real.

## Verificação mínima

```bash
python tests/teste_jogo.py
git diff --check
```
