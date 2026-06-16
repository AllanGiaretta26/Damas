# GUI

A interface gráfica fica em `src/gui/` e usa tkinter. Ela renderiza estado e encaminha ações para `Jogo`; regra de jogo não deve ser implementada na GUI.

## Componentes

| Arquivo | Papel |
|---|---|
| `src/gui/__init__.py` | Exporta `GUIJogo`, fachada sobre `GerenciadorInterface`. |
| `src/gui/gerenciador_interface.py` | Cria widgets, trata cliques, botões, histórico, fim de jogo e placar. |
| `src/gui/renderizador.py` | Desenha coordenadas, casas, destaques e peças no canvas. |

## GUIJogo

`GUIJogo` não é `tk.Frame`. Ela recebe uma janela raiz existente, cria um `Jogo` e delega a interface para `GerenciadorInterface`.

Parâmetros principais:

- `janela`: instância de `tk.Tk` criada por `AplicacaoDamas`.
- `modo_ia`: habilita comportamento específico do modo IA.
- `callback_menu`: função chamada pelo botão `Menu`.
- `dificuldade`: chave de IA exibida no topo.
- `cor_humano`: cor controlada pelo humano no modo IA.
- `placar`: dicionário compartilhado com a aplicação.

`GUIJogo.iniciar()` é no-op porque `mainloop()` pertence a `AplicacaoDamas.executar()`.

## GerenciadorInterface

Responsabilidades:

- Criar labels, canvas e botões.
- Converter clique do canvas em coordenadas de tabuleiro.
- Chamar `Jogo.selecionar_peca()` e `Jogo.mover_peca()`.
- Redesenhar a tela após mudanças.
- Exibir histórico e fim de jogo.
- Atualizar contadores de peças, capturas e placar de sessão.
- Disparar `callback_pos_atualizacao` para integração com IA.

Botões criados:

| Grupo | Botões |
|---|---|
| Ações da partida | `Novo Jogo`, `Empate`, `Desfazer` somente em modo IA |
| Navegação | `Histórico`, `Menu` quando há callback, `Sair` |

Observação ruim mas real: alguns textos da GUI ainda estão sem acento (`Voce`, `Pecas`, `sessao`). A documentação deve citar labels literais sem corrigir silenciosamente.

## RenderizadorTabuleiro

Responsabilidades:

- Limpar e redesenhar o canvas.
- Desenhar coordenadas A-H e 8-1.
- Desenhar casas claras/escuras.
- Destacar casa selecionada e movimentos válidos.
- Desenhar peças e coroa de dama.

Destaques:

- `COR_SELECIONADA`: casa da peça selecionada.
- `COR_MOVIMENTO_VALIDO`: destino de movimento simples.
- `COR_CAPTURA`: destino de captura.

## Fluxo de clique

1. `_ao_clicar_canvas()` converte pixels em `(linha, coluna)`.
2. `_processar_clique()` decide se seleciona, move, desseleciona ou continua captura sequencial.
3. `Jogo` valida e executa a ação.
4. `_atualizar_tela()` redesenha e checa fim de jogo.
5. Se houver callback da IA e for turno dela, `main.AplicacaoDamas` agenda o movimento.

## Próximo documento

[Main](main.md)
