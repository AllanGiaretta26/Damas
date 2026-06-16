# Arquitetura

O projeto usa uma arquitetura em camadas simples. A regra principal é impedir que detalhes de interface contaminem regras de jogo e estado puro.

## Estrutura de camadas

```text
src/
├── models/              # Estado puro: Peca, Tabuleiro, enums
├── services/            # Regras de movimento, captura e promoção
├── game.py              # Orquestrador e API pública do domínio
├── ia/                  # Estratégias de IA; depende de Jogo
├── gui/                 # Interface tkinter; depende de Jogo
└── config.py            # Constantes visuais e temas
```

## Direção de dependência

```text
gui ────────► game ─────► services ─────► models
ia  ────────► game
config ─────► usado pela GUI e renderização
```

Regras:

- `models` não importa `services`, `game`, `ia` ou `gui`.
- `services` operam sobre `models` e não conhecem tkinter.
- `game.Jogo` é a entrada pública para regras e mutações.
- `ia` usa `Jogo` para consultar e simular movimentos; não chama services diretamente.
- `gui` chama `Jogo` e renderiza estado. Não deve implementar regra de dama.

## Invariantes do domínio

- O tabuleiro tem 8x8 posições.
- `JOGADOR1` é vermelho, começa nas linhas 5-7 e move para linhas menores.
- `JOGADOR2` é azul, começa nas linhas 0-2 e move para linhas maiores.
- Peças comuns movem uma casa diagonal para frente.
- Damas movem uma casa diagonal em qualquer direção. Este projeto não implementa dama voadora.
- Capturas pulam exatamente duas casas diagonais e são obrigatórias quando disponíveis.
- Promoção é automática: `JOGADOR1` na linha 0; `JOGADOR2` na linha 7.
- Toda mutação por `Jogo.mover_peca()` deve registrar delta reversível para `desfazer_jogada()`.

## Fluxo de movimento

1. A GUI ou a IA chama `Jogo.selecionar_peca()` ou `Jogo.mover_peca()`.
2. `Jogo` consulta `MovimentoValidator`.
3. Se for captura, `CaptureHandler` remove a peça capturada e move a peça atacante.
4. `PromotionHandler` tenta promover a peça movida.
5. `Jogo` registra a jogada no histórico.
6. Se houver captura sequencial, o turno continua com a mesma peça selecionada.
7. Caso contrário, `Jogo` encerra o turno e alterna o jogador.

## Janela única

`main.AplicacaoDamas` cria uma única instância de `tk.Tk`. Menu, tela de opções da IA e jogo são reconstruídos dentro dessa mesma janela. `GUIJogo.iniciar()` é no-op; o `mainloop()` pertence a `AplicacaoDamas.executar()`.

## Próximo documento

[Models](../referencia/models.md)
