# Main

`main.py` contém `AplicacaoDamas`, responsável pelo ciclo de vida da janela, menus e integração da IA.

## Janela única

`AplicacaoDamas` cria uma única instância de `tk.Tk` em `__init__`. A aplicação troca telas destruindo widgets filhos, não destruindo a janela raiz.

Tamanhos usados:

| Tela | Tamanho |
|---|---|
| Menu e opções de IA | 420x440 |
| Jogo | 720x840 |

`_centralizar_janela(largura, altura)` atualiza a geometria e centraliza a janela na tela.

## Fluxo da aplicação

```text
AplicacaoDamas.__init__
└── _mostrar_menu_principal()
    ├── Dois Jogadores -> _iniciar_jogo("humano")
    └── Contra a IA -> _mostrar_opcoes_ia()
        └── Iniciar Jogo -> _iniciar_jogo("ia", dificuldade, cor_humano)
```

`executar()` chama apenas `self.janela.mainloop()`.

## Menu principal

Labels e botões principais:

- `Jogo de Damas`.
- `Escolha o modo de jogo`.
- `Dois Jogadores
(Humano vs Humano)`.
- `Contra a IA
(Humano vs Computador)`.
- `Sair`.

## Opções da IA

A tela de IA permite:

- dificuldade: `facil`, `medio`, `dificil`;
- cor humana: `vermelho` ou `azul`.

Mapeamento de cor:

- `vermelho` -> `Jogador.JOGADOR1`;
- `azul` -> `Jogador.JOGADOR2`.

Se o humano escolher azul, a IA joga como `Jogador.JOGADOR1` e pode abrir a partida.

## Início do jogo

`_iniciar_jogo()`:

1. Limpa a janela.
2. Centraliza no tamanho de jogo.
3. Cria `GUIJogo` com `modo_ia`, `callback_menu`, `dificuldade`, `cor_humano` e `placar`.
4. Se for modo IA, instancia `IA` com o jogador oposto ao humano.
5. Configura callback pós-atualização.
6. Agenda a IA se o turno inicial pertencer a ela.

## Agendamento da IA

A IA é executada com `janela.after(500, ...)`.

Métodos relacionados:

| Método | Papel |
|---|---|
| `_agendar_ia(gui, ia)` | Cancela agendamento anterior e agenda novo movimento. |
| `_cancelar_ia_pendente()` | Cancela `after()` pendente ao sair da tela. |
| `_configurar_ia(gui, ia)` | Instala callback que agenda IA quando `jogo.jogador_atual == ia.jogador`. |
| `_executar_ia(gui, ia)` | Executa movimento e atualiza a tela. |

## Placar de sessão

`self._placar` é compartilhado por referência com `GerenciadorInterface`.

- Em humano vs. humano, as chaves são `Jogador.JOGADOR1` e `Jogador.JOGADOR2`.
- Em modo IA, o gerenciador usa chaves `"humano"` e `"ia"` para vitórias por papel.

## Próximo documento

[Exemplos de uso](../guias/uso-exemplo.md)
