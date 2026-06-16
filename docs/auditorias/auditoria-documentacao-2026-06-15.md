# Auditoria de documentação 2026-06-15

## Escopo

Arquivos auditados:

- `README.md`
- `docs/README.md`
- `docs/arquitetura/visao-geral.md`
- `docs/referencia/models.md`
- `docs/referencia/services.md`
- `docs/referencia/game.md`
- `docs/referencia/ia.md`
- `docs/referencia/gui.md`
- `docs/referencia/main.md`
- `docs/guias/uso-exemplo.md`
- `docs/guias/pontos-atencao.md`

Fontes confrontadas:

- `src/game.py`
- `src/models/`
- `src/services/`
- `src/ia/`
- `src/gui/`
- `main.py`
- `tests/teste_jogo.py`
- `CLAUDE.md`

## Achados

### A documentação invertia a orientação dos jogadores

Vários exemplos tratavam `JOGADOR1` como se começasse no topo e promovesse na linha 7. O código faz o oposto: `JOGADOR1` começa nas linhas 5-7, move para cima e promove na linha 0.

Impacto: exemplos de README e docs falhavam ou ensinavam regra errada.

### A documentação dizia que dama move qualquer distância

O código não implementa dama voadora. `MovimentoValidator` permite à dama uma casa diagonal em qualquer direção e captura com salto de duas casas.

Impacto: expectativa de regra incompatível com testes e implementação.

### Exemplos usavam assinaturas antigas ou inválidas

Havia exemplos com `mover_peca()` recebendo dois argumentos, `Tabuleiro.mover_peca(peca, linha, coluna)` e seleção de peças em casas que não pertencem ao jogador atual.

Impacto: material de onboarding quebrado.

### GUI e main estavam documentados como uma versão antiga

`GUIJogo` era descrito como `tk.Frame`, mas hoje é fachada sobre `GerenciadorInterface`. O menu, tamanhos, labels e agendamento de IA também estavam divergentes.

Impacto: documentação de arquitetura de janela única ficava parcialmente falsa.

### Índice de documentação era ruidoso

O índice usava decoração visual excessiva e não explicava autoridade entre documentos. Isso escondia o que deve ser atualizado quando código e docs divergem.

Impacto: manutenção ruim e risco de nova divergência.

## Ações aplicadas

- Reescrito `README.md` como guia de usuário: requisitos, execução, testes, regras reais, IA e mapa de docs.
- Reescrito `docs/README.md` com ordem de autoridade, índice e regras de manutenção.
- Reescritos documentos técnicos para separar explicação, referência e exemplos.
- Corrigidas regras de jogador, promoção, movimento de dama, assinatura de APIs e integração da IA.
- Criado este relatório de auditoria em `docs/auditorias/`.
- Reorganizado `docs/` em subpastas: `arquitetura/`, `referencia/`, `guias/` e `auditorias/`; `docs/indice.md` foi removido por duplicar o índice principal.

## Pendências

- Não há `CHANGELOG.md`. Se o projeto passar a versionar entregas, crie um changelog convencional com seção `Unreleased`.
- Labels da GUI ainda têm texto sem acento (`Voce`, `Pecas`, `sessao`). A documentação cita isso como comportamento real; corrigir a interface é mudança de produto, não de documentação.
- `requirements.txt` é informativo e contém comentário com erro de digitação antigo. Não foi alterado porque a auditoria focou documentação Markdown.

## Verificação

- `python tests/teste_jogo.py`: passou; todos os testes do script procedural retornaram `[OK] TODOS OS TESTES PASSARAM!`.
- `git diff --check`: passou; o Git avisou apenas que arquivos Markdown com CRLF serão normalizados para LF quando tocados.
- Validação de H1 único e links relativos: executada após excluir `.git` e `.venv`; passou.
- Exemplos documentados em `README.md` e `docs/guias/uso-exemplo.md`: executados por script Python com assertions; passaram.
